#!/usr/bin/env python3
"""Render BOARD.md from the Pau state.

The board paints the same schema Pau writes. It is a view, never a second source:
if the two ever disagree, the state wins and the disagreement is a defect.

Usage:
  render_board.py --project <dir> [--out BOARD.md] [--stagnation-hours 4]

Exit codes: 0 written, 2 usage or I/O error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

STORE = ".pau"

PROGRESS_LABEL = {
    "task_status": "a task moved",
    "gate_passed": "a gate passed",
    "decision_answered": "a decision was answered",
    "deliverable": "a new deliverable",
}


def _read_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        text = fh.read().strip()
    return json.loads(text) if text else default


def _read_log(path):
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def _parse(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except ValueError:
        return None


def _hours_since(ts, now):
    moment = _parse(ts)
    if moment is None:
        return None
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return (now - moment).total_seconds() / 3600.0


def render(project, stagnation_hours):
    store = os.path.join(project, STORE)
    state = _read_json(os.path.join(store, "state.json"), {})
    tasks = _read_json(os.path.join(store, "tasks.json"), {})
    gates = _read_json(os.path.join(store, "gates.json"), {})
    decisions = _read_json(os.path.join(store, "decisions.json"), {})
    log = _read_log(os.path.join(store, "log.jsonl"))

    now = datetime.now(timezone.utc)
    idle = _hours_since(state.get("last_progress_at"), now)

    # The red light is driven by real progress, never by the last run.
    if idle is None:
        progress_line = "no real progress recorded yet"
    else:
        flag = " **RED**" if idle >= stagnation_hours else ""
        what = PROGRESS_LABEL.get(state.get("last_progress_what"), state.get("last_progress_what") or "-")
        progress_line = f"{idle:.1f} h since real progress ({what}){flag}"

    open_decisions = {k: v for k, v in decisions.items() if v.get("status") == "open"}
    queued = {k: v for k, v in decisions.items() if v.get("status") == "queued"}
    in_flight = {k: v for k, v in tasks.items() if v.get("status") == "in_progress"}
    blocked = {k: v for k, v in tasks.items() if v.get("status") == "blocked"}
    done = {k: v for k, v in tasks.items() if v.get("status") == "done"}

    next_gate = gates.get(state.get("next_gate") or "", {})

    quiet = sum(1 for e in log if e.get("changed") is False)
    quiet_pct = (quiet / len(log) * 100.0) if log else 0.0

    used = state.get("budget_runs_used")
    total = state.get("budget_runs_total")
    budget = f"{used} of {total} runs" if used is not None and total else "no budget set"
    usage = state.get("usage_pct")
    if usage is not None:
        budget += f" - usage {usage} %" + (" **stop at 80**" if usage >= 80 else "")

    lines = []
    add = lines.append
    add(f"# {state.get('project', 'Project')}")
    add("")
    add(f"> Rendered {now.strftime('%Y-%m-%d %H:%M')} UTC from `{STORE}/`. "
        "This file is a view. The state is the source; if they disagree, the state wins.")
    add("")
    add("| | |")
    add("|---|---|")
    add(f"| **Status** | {state.get('status', '-')}"
        + (f" - {state['status_note']}" if state.get("status_note") else "") + " |")
    add(f"| **Phase** | {state.get('phase', '-')} |")
    if next_gate:
        add(f"| **Next gate** | {next_gate.get('title', state.get('next_gate'))} "
            f"- due {next_gate.get('date', '?')} - {next_gate.get('numbers', 'no numbers yet')} |")
    else:
        add(f"| **Next gate** | {state.get('next_gate') or 'none'} |")
    add(f"| **Last real progress** | {progress_line} |")
    add(f"| **Tasks** | {len(in_flight)} in flight, {len(blocked)} blocked, "
        f"{len(done)} done, {len(tasks)} total |")
    add(f"| **Decisions** | {len(open_decisions)} open, {len(queued)} queued |")
    add(f"| **Budget** | {budget} |")
    add(f"| **Cycles with no state change** | {quiet} of {len(log)} ({quiet_pct:.0f} %) |")
    if state.get("stop_requested"):
        add(f"| **STOPPED** | by {state.get('stopped_by', '?')} at {state.get('stopped_at', '?')} |")
    add("")
    add(f"**Resume point.** {state.get('resume_point') or 'none recorded'}")
    add("")

    if open_decisions:
        add("## Decisions waiting on you")
        add("")
        for did, dec in sorted(open_decisions.items()):
            add(f"### {dec.get('title', did)}  `{did}`")
            add("")
            add(f"**Recommendation:** {dec.get('recommendation', '-')}")
            add("")
            for point in dec.get("why", [])[:3]:
                add(f"- {point}")
            add("")
            add(f"**Rejected alternative:** {dec.get('alternative', '-')}  ")
            add(f"**Cost / risk:** {dec.get('cost_risk', '-')}  ")
            add(f"**If you do not decide:** {dec.get('if_no_answer', '-')}")
            if dec.get("due"):
                add(f"  \n**Due:** {dec['due']}")
            add("")
        add("To answer: set `status` to `answered` and write your `answer` in "
            f"`{STORE}/decisions.json`, or tell Pau. The next cycle acts on it.")
        add("")

    if queued:
        add(f"## Queued decisions ({len(queued)})")
        add("")
        add("Held back because three are already open. They are counted, not decided for you.")
        add("")
        for did, dec in sorted(queued.items()):
            add(f"- `{did}` {dec.get('title', '')}")
        add("")

    if blocked:
        add("## Blocked")
        add("")
        for tid, task in sorted(blocked.items()):
            add(f"- `{tid}` {task.get('title', '')} - {task.get('note') or 'no cause recorded'}")
        add("")

    if in_flight:
        add("## In flight")
        add("")
        for tid, task in sorted(in_flight.items()):
            add(f"- `{tid}` {task.get('title', '')} - done when: {task.get('done_when', '?')}")
        add("")

    red = {k: v for k, v in tasks.items() if v.get("red_action") and v.get("status") != "done"}
    if red:
        add("## Prepared, not run")
        add("")
        add("Red actions. They are ready to one click and never run in an unattended session.")
        add("")
        for tid, task in sorted(red.items()):
            add(f"- `{tid}` {task.get('title', '')}")
        add("")

    add("## Last entries")
    add("")
    for entry in log[-10:][::-1]:
        mark = "·" if entry.get("changed") else " "
        add(f"- `{entry.get('ts', '')}` **{entry.get('by', '?')}** {mark} {entry.get('text', '')}")
    add("")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render BOARD.md from the Pau state.")
    ap.add_argument("--project", default=".")
    ap.add_argument("--out", default="BOARD.md")
    ap.add_argument("--stagnation-hours", type=float, default=4.0,
                    help="hours without real progress before the board goes red "
                         "(prior use, not a validated figure - calibrate it)")
    args = ap.parse_args(argv)

    project = os.path.abspath(args.project)
    if not os.path.isdir(os.path.join(project, STORE)):
        print(f"no {STORE}/ in {project}. Run /pau:take first.", file=sys.stderr)
        return 2
    try:
        text = render(project, args.stagnation_hours)
        out = os.path.join(project, args.out)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"could not render the board: {exc}", file=sys.stderr)
        return 2
    print(f"OK - wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
