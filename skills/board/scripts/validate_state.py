#!/usr/bin/env python3
"""Validate and commit a write to the Pau project state.

Pau is the only writer of state, and this is the only path. A write is staged under
.pau/.staging/ and applied only if it passes. Nothing here depends on a particular
host: it is plain files and the standard library.

Usage
-----
  validate_state.py --project <dir>
      Validate the current store. Exit 0 if clean.

  validate_state.py --project <dir> --staged
      Validate what .pau/.staging/ would produce, without applying it.

  validate_state.py --project <dir> --commit --session <id>
      Validate the staged write and, only if it passes, apply it.

Exit codes: 0 valid, 1 rejected, 2 usage or I/O error.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone

STORE = ".pau"
STAGING = os.path.join(STORE, ".staging")

COLLECTIONS = ("state", "tasks", "gates", "decisions")
LOG = "log.jsonl"

MAX_OPEN_DECISIONS = 3
MAX_TASKS_IN_FLIGHT = 3

STATE_FIELDS = {
    "project", "source", "phase", "status", "status_note",
    "next_gate", "next_gate_due",
    "last_progress_at", "last_progress_what",
    "resume_point",
    "lease_holder", "lease_until",
    "open_decisions", "queued_decisions", "tasks_in_flight",
    "budget_runs_total", "budget_runs_used", "usage_pct",
    "stop_requested", "stopped_by", "stopped_at", "resumed_by", "resumed_at",
    "updated_at", "updated_by",
}
STATE_REQUIRED = {"project", "source", "status", "updated_at", "updated_by"}
STATE_STATUS = {"running", "attention", "stopped"}

TASK_FIELDS = {
    "title", "owner", "status", "done_when", "stop", "budget",
    "depends_on", "blocks", "due", "critical",
    "attempts", "max_attempts", "source",
    "deliverable", "evidence", "reviewed_by", "reviewed_at",
    "red_action", "note",
}
TASK_REQUIRED = {"title", "status", "done_when", "source"}
TASK_STATUS = {"pending", "in_progress", "blocked", "done", "stopped"}

GATE_FIELDS = {"title", "date", "criteria", "numbers", "result", "decided_by", "decided_at", "source"}
GATE_REQUIRED = {"title", "date", "criteria", "result", "source"}
GATE_RESULT = {"pending", "pass", "fail"}

DECISION_FIELDS = {
    "title", "recommendation", "why", "alternative", "cost_risk", "if_no_answer",
    "status", "opened_at", "due", "answered_at", "answer",
    "blocks_gate", "reversible", "default_option", "source", "by",
}
DECISION_REQUIRED = {"title", "recommendation", "why", "alternative", "cost_risk",
                     "if_no_answer", "status", "opened_at", "source", "by"}
DECISION_STATUS = {"open", "queued", "answered"}
DECISION_BY = {"pau", "owner"}

LOG_FIELDS = {"ts", "by", "run_id", "kind", "text", "changed", "chosen", "rejected"}
LOG_REQUIRED = {"ts", "by", "kind", "text", "changed"}
LOG_KIND = {"cycle", "progress", "decision", "gate", "stop", "quality", "norm"}

PROGRESS_KINDS = {"task_status", "gate_passed", "decision_answered", "deliverable"}


class Rejected(Exception):
    pass


def _read_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        text = fh.read().strip()
    if not text:
        return default
    return json.loads(text)


def _read_log(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise Rejected(f"{LOG} line {n} is not valid JSON: {exc}")
    return out


def _parse_ts(value, where):
    if not isinstance(value, str):
        raise Rejected(f"{where}: timestamp must be a string, got {type(value).__name__}")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise Rejected(f"{where}: '{value}' is not an ISO 8601 timestamp")


def _check_fields(obj, allowed, required, where, errors):
    if not isinstance(obj, dict):
        errors.append(f"{where}: expected an object, got {type(obj).__name__}")
        return
    for key in sorted(set(obj) - allowed):
        errors.append(f"{where}: unknown field '{key}'. The schema is closed")
    for key in sorted(required - set(obj)):
        errors.append(f"{where}: missing required field '{key}'")


def load_store(root):
    store = {}
    for name in COLLECTIONS:
        path = os.path.join(root, f"{name}.json")
        default = {} if name != "state" else {}
        try:
            store[name] = _read_json(path, default)
        except json.JSONDecodeError as exc:
            raise Rejected(f"{name}.json is not valid JSON: {exc}")
    store["log"] = _read_log(os.path.join(root, LOG))
    return store


def validate(store, session=None, previous=None):
    errors = []

    state = store["state"]
    _check_fields(state, STATE_FIELDS, STATE_REQUIRED, "state", errors)
    if isinstance(state, dict):
        if state.get("status") not in STATE_STATUS:
            errors.append(f"state.status must be one of {sorted(STATE_STATUS)}")
        if state.get("updated_by") != "pau":
            errors.append("state.updated_by must be 'pau'. Pau is the only writer of state")
        if state.get("last_progress_what") not in (None, "") and \
                state.get("last_progress_what") not in PROGRESS_KINDS:
            errors.append(
                "state.last_progress_what must be one of "
                f"{sorted(PROGRESS_KINDS)}. A log entry saying nothing changed is not progress"
            )
        for key in ("last_progress_at", "updated_at", "lease_until"):
            if state.get(key):
                try:
                    _parse_ts(state[key], f"state.{key}")
                except Rejected as exc:
                    errors.append(str(exc))

    tasks = store["tasks"]
    if not isinstance(tasks, dict):
        errors.append("tasks.json must be an object keyed by task id")
        tasks = {}
    in_flight = 0
    for tid, task in sorted(tasks.items()):
        _check_fields(task, TASK_FIELDS, TASK_REQUIRED, f"tasks/{tid}", errors)
        if not isinstance(task, dict):
            continue
        if task.get("status") not in TASK_STATUS:
            errors.append(f"tasks/{tid}.status must be one of {sorted(TASK_STATUS)}")
        if not str(task.get("done_when", "")).strip():
            errors.append(f"tasks/{tid}: done_when is empty. A task starts with its criterion, not without it")
        if not str(task.get("source", "")).strip():
            errors.append(f"tasks/{tid}: source is empty. No source, no element - nothing is invented")
        if task.get("status") == "in_progress":
            in_flight += 1
        if task.get("status") == "done" and not str(task.get("evidence", "")).strip():
            errors.append(f"tasks/{tid}: marked done with no evidence")
        attempts = task.get("attempts", 0)
        cap = task.get("max_attempts", 3)
        if isinstance(attempts, int) and isinstance(cap, int) and attempts > cap:
            errors.append(f"tasks/{tid}: {attempts} attempts past a cap of {cap}. Escalate instead of retrying")
    if in_flight > MAX_TASKS_IN_FLIGHT:
        errors.append(f"{in_flight} tasks in flight, the limit is {MAX_TASKS_IN_FLIGHT}")

    gates = store["gates"]
    if not isinstance(gates, dict):
        errors.append("gates.json must be an object keyed by gate id")
        gates = {}
    for gid, gate in sorted(gates.items()):
        _check_fields(gate, GATE_FIELDS, GATE_REQUIRED, f"gates/{gid}", errors)
        if isinstance(gate, dict) and gate.get("result") not in GATE_RESULT:
            errors.append(f"gates/{gid}.result must be one of {sorted(GATE_RESULT)}")

    decisions = store["decisions"]
    if not isinstance(decisions, dict):
        errors.append("decisions.json must be an object keyed by decision id")
        decisions = {}
    open_count = 0
    for did, dec in sorted(decisions.items()):
        _check_fields(dec, DECISION_FIELDS, DECISION_REQUIRED, f"decisions/{did}", errors)
        if not isinstance(dec, dict):
            continue
        if dec.get("status") not in DECISION_STATUS:
            errors.append(f"decisions/{did}.status must be one of {sorted(DECISION_STATUS)}")
        if dec.get("by") not in DECISION_BY:
            errors.append(
                f"decisions/{did}.by must be one of {sorted(DECISION_BY)}. "
                "Pau records its own decisions too, or '0 reversed' has no denominator"
            )
        if not str(dec.get("recommendation", "")).strip():
            errors.append(f"decisions/{did}: no recommendation. A decision is never escalated as an open question")
        why = dec.get("why")
        if isinstance(why, list) and len(why) > 3:
            errors.append(f"decisions/{did}: 'why' has {len(why)} points, the limit is 3")
        if dec.get("status") == "open":
            open_count += 1
        if dec.get("status") == "answered" and not str(dec.get("answer", "")).strip():
            errors.append(f"decisions/{did}: answered with no answer recorded")
    if open_count > MAX_OPEN_DECISIONS:
        errors.append(
            f"{open_count} open decisions, the limit is {MAX_OPEN_DECISIONS}. "
            "A fourth is queued and counted, never auto-applied"
        )

    log = store["log"]
    for n, entry in enumerate(log, 1):
        _check_fields(entry, LOG_FIELDS, LOG_REQUIRED, f"{LOG}:{n}", errors)
        if not isinstance(entry, dict):
            continue
        if entry.get("kind") not in LOG_KIND:
            errors.append(f"{LOG}:{n}.kind must be one of {sorted(LOG_KIND)}")
        if not isinstance(entry.get("changed"), bool):
            errors.append(
                f"{LOG}:{n}.changed must be true or false. "
                "Without it, cycles that changed nothing cannot be counted"
            )

    if previous is not None:
        if len(log) <= len(previous["log"]):
            errors.append(
                "this write adds no log entry. A run that leaves no trace did not happen"
            )

    if session is not None and isinstance(state, dict):
        holder = state.get("lease_holder")
        until = state.get("lease_until")
        if holder and until and holder != session:
            try:
                if _parse_ts(until, "state.lease_until") > datetime.now(timezone.utc):
                    errors.append(
                        f"the turn is held by '{holder}' until {until}. "
                        "Do no work: log the skipped cycle and stop"
                    )
            except Rejected:
                pass

    return errors


def commit(project):
    staging = os.path.join(project, STAGING)
    store = os.path.join(project, STORE)
    moved = []
    for name in COLLECTIONS:
        src = os.path.join(staging, f"{name}.json")
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(store, f"{name}.json"))
            moved.append(f"{name}.json")
    src_log = os.path.join(staging, LOG)
    if os.path.exists(src_log):
        shutil.copy2(src_log, os.path.join(store, LOG))
        moved.append(LOG)
    shutil.rmtree(staging, ignore_errors=True)
    return moved


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate and commit a Pau state write.")
    ap.add_argument("--project", default=".", help="project directory holding .pau/")
    ap.add_argument("--staged", action="store_true", help="validate .pau/.staging/ instead of the store")
    ap.add_argument("--commit", action="store_true", help="validate the staged write, then apply it")
    ap.add_argument("--session", help="this session's id, checked against the lease")
    args = ap.parse_args(argv)

    project = os.path.abspath(args.project)
    store_dir = os.path.join(project, STORE)
    if not os.path.isdir(store_dir):
        print(f"no {STORE}/ in {project}. Run /pau:take first.", file=sys.stderr)
        return 2

    try:
        if args.staged or args.commit:
            staging = os.path.join(project, STAGING)
            if not os.path.isdir(staging):
                print(f"nothing staged: {STAGING}/ does not exist", file=sys.stderr)
                return 2
            previous = load_store(store_dir)
            merged = dict(previous)
            staged = load_store(staging)
            for key in staged:
                path = os.path.join(staging, f"{key}.json" if key != "log" else LOG)
                if os.path.exists(path):
                    merged[key] = staged[key]
            errors = validate(merged, session=args.session, previous=previous)
        else:
            errors = validate(load_store(store_dir), session=args.session)
    except Rejected as exc:
        print(f"REJECTED: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"I/O error: {exc}", file=sys.stderr)
        return 2

    if errors:
        print(f"REJECTED - {len(errors)} problem(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        print("\nNothing was written. Fix the staged write and run again.", file=sys.stderr)
        return 1

    if args.commit:
        moved = commit(project)
        print("OK - written: " + (", ".join(moved) if moved else "nothing staged"))
    else:
        print("OK - state is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
