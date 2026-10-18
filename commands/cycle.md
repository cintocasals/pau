---
description: Run one management cycle - read, take the turn, prioritise, do or delegate, check, write. Always leaves a log entry, even when nothing changed.
argument-hint: "[optional: something to focus on]"
---

Run one cycle. $ARGUMENTS

Use the `cycle` skill. The six steps, in order: read (including the resume point), take the turn,
prioritise, do or delegate, check the `done_when`, write.

Hard rules for this pass:

- If another session holds the turn and it has not expired, do no work: log the skipped cycle and stop.
- At most three tasks in flight.
- Red actions are prepared, never run, unless I am here and say so.
- Write a log entry whichever way it goes, with `changed` set honestly, and the task you picked plus the
  first one you passed over.
- Write the resume point before releasing the turn.

Then render `BOARD.md` and tell me in a few lines what moved. If nothing moved, say that in one line - do
not pad it.
