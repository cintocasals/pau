---
description: Close a task, judge a gate on its numbers, or close the project.
argument-hint: "[task id, gate id, or 'project']"
---

$ARGUMENTS

Use the `close` skill.

**A task:** the `reviewer` checks the `done_when` against the evidence first - always if it opens a gate,
one in three otherwise. Then record `status`, `deliverable`, `evidence`, who reviewed it and when, and the
real progress. A task marked done with no evidence will be rejected, and should be.

**A gate:** judge it on the numbers against the criteria it was written with. Record `result`, `numbers`,
who decided and when. A `fail` is a result: write the cause and what moves. **Never lower the criterion to
make it pass** - move the date and write down why. If the same criterion fails twice, say so plainly: the
thing being tested needs redesigning, not patching.

**The project:** every task resolved, every gate judged, every decision answered or recorded as unanswered
with what was done instead, a final log entry, and `BOARD.md` rendered one last time as the dated copy.

Report in this order: what was done, what you decided yourself, what is left for me. Numbers against their
thresholds. No figure the system does not actually measure.
