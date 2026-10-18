---
description: Rebuild BOARD.md from the state, and check the two against each other on a sample of ten.
argument-hint: "[optional: sample, or a stagnation threshold in hours]"
---

$ARGUMENTS

Use the `board` skill.

1. Validate the state as it stands:
   `python3 scripts/validate_state.py --project .`
   If it is rejected, show me every problem and change nothing.
2. Render it: `python3 scripts/render_board.py --project .`
3. If I asked for a sample, or if a gate is opening: have the `reviewer` take ten elements of state at
   random and check them against `BOARD.md`. Report a count - "10 sampled, 0 mismatches" - never an
   impression. Any mismatch is a stop, and the state wins over the view.

Then give me the top of the board in a few lines: status, next gate with its numbers, hours since real
progress, what is open for me.
