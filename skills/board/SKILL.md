---
name: board
description: The only path that writes project state, and the only thing that renders the board. Use it whenever Pau has to record anything - a task moving, a gate result, a decision opened or answered, a log entry, the lease, the resume point - and whenever the board has to be rebuilt or sampled against the state. Every write is staged, validated and only then applied; a rejected write changes nothing.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# board - one writer, one path

All project state lives in `.pau/` at the project root. **Pau is the only agent that writes it, and this
skill is the only path.** Nothing else writes, not even a one-character fix.

```
.pau/state.json       one object: status, gate, progress, lease, resume point, budget
.pau/tasks.json       {id: task}
.pau/gates.json       {id: gate}
.pau/decisions.json   {id: decision}
.pau/log.jsonl        one JSON object per line, one line per run, always
.pau/.staging/        a write in progress, never read by anything else
BOARD.md              the rendered view, at the project root
```

Field by field, the schema is in `references/schema.md`. It is **closed**: a field that is not in it is
rejected.

## Be honest about what this guarantees

On a surface where plugin hooks run, a hook can intercept a write. **On claude.ai chat they do not run.**
So this is not a platform guarantee: it is a discipline with a tool behind it. The validator cannot stop
somebody editing `.pau/state.json` by hand; it can only refuse to apply a write that breaks the schema, and
it will catch the breakage the next time it runs. Say it that way in reports too. Do not describe the board
as tamper-proof, because it is not.

## How to write

Never edit `.pau/*.json` in place. Always:

**1. Stage.** Copy only what you are changing into `.pau/.staging/`, with the full new contents of each
file you touch. Always include an updated `log.jsonl` with at least one new entry - a write that adds no
log entry is rejected, by design.

**2. Validate and apply, in one command:**

```bash
python3 scripts/validate_state.py --project <project-dir> --commit --session "<this-session-id>"
```

Exit 0 means it was applied and the staging directory is gone. Exit 1 means **nothing was written**; the
message lists every problem. Fix the staged files and run it again.

To check without applying, drop `--commit` and pass `--staged`. To check the store as it stands, pass
neither.

**3. Render the board:**

```bash
python3 scripts/render_board.py --project <project-dir> --stagnation-hours 4
```

## If the validator rejects you

It is a technical step, so it gets **two rounds**. On the second rejection for the same reason: stop, write
a log entry with the cause, and report it. Do not force the write by editing the store directly, and do not
change the validator inside a cycle to make your write pass. If the schema is genuinely wrong, that is a
decision, not a fix.

## The rules it enforces, and why each one exists

| Rejected | Why |
|---|---|
| A write that adds no log entry | A run that leaves no trace did not happen. This is the single most common failure of scheduled work: green runs that recorded nothing, so the project looked busier than it was |
| `state.updated_by` that is not `pau` | One writer. Two writers is how a board starts lying |
| A task with no `done_when` | A task begins with its criterion or it does not begin |
| A task with no `source` | Every element names the line of the plan it came from. No source, no element: that is what "nothing invented" means in practice |
| A decision with no `recommendation` | A decision escalated as an open question is the failure this whole plugin exists to prevent |
| A fourth open decision | Three is the limit. The fourth is queued and counted - **never auto-applied**. Clearing the queue by deciding for the owner would satisfy the number and defeat the point |
| A fourth task in flight | Three is the limit |
| `last_progress_what` outside the four | Real progress is: a task moved, a gate passed, a decision was answered, a new deliverable. A log entry saying nothing changed is **not** progress, or the clock never turns red |
| A write while another session holds the lease | Log the skipped cycle and stop. Do not do the work twice |
| Any field outside the schema | The schema is closed |

## The lease

Take it at the start of a cycle: set `lease_holder` to this session's id and `lease_until` to a time far
enough ahead to finish. Release it at the end by setting `lease_until` to now.

If you find it held by someone else and not expired, **do no work**: write one log entry
(`kind: "cycle"`, `changed: false`, text naming the holder) and stop.

## The sample

Every cycle that opens a gate, the `reviewer` takes ten elements of state at random and checks them against
BOARD.md. Report a count, never an impression: "10 sampled, 0 mismatches". Any mismatch is a stop - the view
and the source must agree, and when they do not, the source wins.

## The resume point

Every cycle writes one line into `state.resume_point`: where it stopped, what came next, what it was
waiting for. A scheduled run starts from nothing every time; without this, a session that dies mid-cycle
leaves the next one guessing, and guessing is where discrepancies come from.
