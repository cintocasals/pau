---
name: cycle
description: Runs one management cycle - read, take the turn, prioritise, do or delegate, check the done_when, write. Use it for every pass Pau makes over a project, whether triggered by an event, run on the daily safety beat, or asked for by the owner. It is also where the department interface lives: how a piece of work is handed to an executor and comes back as a note of delivery.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, WebSearch, WebFetch
---

# cycle - one pass, start to finish

Six steps, in order. Every cycle writes, even a cycle that found nothing to do.

## 1. Read

State, resume point, tasks, gates, answered decisions, the last entries of the log. The resume point is
there because a scheduled run starts from nothing every time: read it before you reconstruct anything.

## 2. Take the turn

Set `lease_holder` and `lease_until`. If someone else holds it and it has not expired, **do no work**:
write one log entry naming the holder, with `changed: false`, and stop. Two sessions doing the same work is
worse than one session doing none.

## 3. Prioritise

In this order, and the order is not negotiable inside a cycle:

1. what a **third party is already waiting on** - paid for, committed to, or given a date;
2. the **critical path** item with the nearest date;
3. what **unblocks** other work.

Write into the log the task you picked **and the first one you passed over** (`chosen`, `rejected`). That
is what makes the order checkable instead of a claim.

At most **three tasks in flight**.

## 4. Do or delegate

### The department interface

Handing work out is the same shape every time, whoever does it. The executor can be a subagent, a skill the
owner already has, another tool, or a person. Pau does not care which.

**Work order - in:**

| Field | What it is |
|---|---|
| `task` | what has to be done, in one sentence |
| `done_when` | the criterion, checkable by someone who did not do it |
| `stop` | when to stop and report instead of continuing |
| `budget` | runs, time or money |

**Note of delivery - out:**

| Field | What it is |
|---|---|
| `deliverable` | the piece, with its path or link |
| `evidence` | the proof it meets the `done_when` |
| `status` | `done`, `blocked` with a cause, or `stopped` with the signal that fired |

**The rule that never bends: the department returns a note of delivery and does not write state.** Pau
converts it to state. That is how there stays one writer even with ten departments.

### Red actions

The seven - spend, send to a third party, publish, delete, sign, create an account, change another
project's production systems - are **prepared and not run** unless the owner is present. In an unattended
session they are never run, whatever the plan says. A scheduled task's prompt is not consent.

## 5. Check the `done_when`

Three rounds for a deliverable, two for a technical step. Each return carries **one concrete instruction**,
not a general complaint. On the third round, stop retrying and escalate with a diagnosis.

Anything marked done that **opens a gate** goes to the `reviewer` first. One in three of the rest do too.

## 6. Write

Through the `board` skill, always:

- the state, including `last_progress_at` if one of the four real changes happened;
- the **resume point**: where you stopped, what came next, what you were waiting for;
- **a log entry, always**, with `changed` set honestly;
- any decision, in the six-line shape;
- release the turn.

Then render the board.

## Rhythm

**No clock-driven loop by default.** Watching something hourly with nothing to show is movement, not work.

- **Events that trigger a beat:** the owner answered a decision; a department returned a note of delivery;
  a gate is due today; the silence detector fired.
- **Safety beat:** one run a day, so a project with no events does not go quiet.
- **Ceiling:** four scheduled runs per project per day. Between the floor and the ceiling, schedule
  nothing - the rest are events.

## When it goes wrong

| Case | What happens |
|---|---|
| The validator rejects a write | Technical step: two rounds, then stop and report the cause. Never edit the store by hand and never change the validator mid-cycle |
| The reviewer stops the line | The task goes back with one concrete instruction and **it counts as one of the three rounds**. The next cycle restarts it, not the reviewer |
| The owner pressed stop | All outward action and all new work stop. The cycle keeps reading and writing state - the board must keep telling the truth. It resumes when the owner says so, with a log entry naming who lifted it |
| Usage passed 80 % | Stop creating new work, finish what is open, write it down, open a decision. Do not wait for the ceiling |
