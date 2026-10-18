---
name: close
description: Closes a task, a gate or a whole project properly. Use it when a piece of work is finished and needs reviewing, recording and reporting; when a gate falls due and has to be judged on its numbers; and when a project ends. It also holds the learned-rules mechanism - how a rule earns its place after something goes wrong.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# close - finishing something properly

## Closing a task

1. **Review.** The `reviewer` checks the `done_when` against the evidence. Every task that opens a gate,
   and one in three of the rest.
2. **Record** through the `board` skill: `status`, `deliverable`, `evidence`, `reviewed_by`,
   `reviewed_at`, and `last_progress_at` with `last_progress_what: "task_status"`.
3. **Report** in one line, in the log: what was done, what was decided, what is needed from the owner.

A task marked done with no evidence is rejected by the validator. That is deliberate: "done" without proof
is the cheapest lie a project tells itself.

## Closing a gate

A gate is judged **on its numbers**, against the criteria written when the gate was created. Not on a
feeling that things are going well.

- Write `result` (`pass` or `fail`), `numbers`, `decided_by`, `decided_at`.
- A `fail` is a result, not a failure to report. Record the cause and what moves.
- **The criterion is never lowered to make a gate pass.** If it cannot be met, the date moves and the cause
  is written down. If the same criterion fails twice, the thing being tested needs redesigning, not
  patching.
- If the gate decision belongs to the owner, escalate it in the six-line shape with the numbers in it.

## Closing a project

1. Every task `done`, `blocked` with a cause, or explicitly `stopped`.
2. Every gate with a result.
3. Every decision answered, or recorded as never answered and what was done instead.
4. A final log entry: what the project delivered, what it cost in runs, what was learned.
5. The board rendered one last time. `BOARD.md` is the dated copy that outlives the state.

## Learned rules

A rule that stops being re-argued every time. The mechanism, not a list - the list belongs to each project.

- **A learned rule is born from a recorded fact**: an incident, a stop, a decision reversed. With the date.
- **One line, imperative.**
- **It is not renegotiated inside a cycle.** Removing one needs the owner.
- **It lives in the project state, not in this plugin.** It is the project's memory, not the product's.

Write it to the log with `kind: "norm"`. Target: every learned rule carries a date and a reference to the
entry it came from. A rule with no fact behind it is an opinion that got promoted.

## The two questions a reviewer asks when a task has no criterion of its own

- **Proof, not promise.** Is there a fact, a figure or a demonstration, and not only adjectives? **No figure
  without a measurement date.**
- **Actionable.** Who does it, when, and how do we know it is done?

## Reporting

Short, and in this order: what was done, what Pau decided itself, what the owner has to decide. Numbers
against their thresholds, never adjectives. If something failed, the cause, and what changes because of it.

Never report a figure the system does not measure. If a threshold has no instrument behind it yet, say so
rather than implying it is being tracked.
