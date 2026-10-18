---
description: Hand an approved plan to Pau. Builds the state, names every unverified assumption, and drives one whole unit end to end before anything is scheduled.
argument-hint: "[path to the plan, a link, or paste it]"
---

Take this project.

Plan: $ARGUMENTS

Use the `intake` skill, and follow it in order. In short:

1. Turn the plan into the state schema in `.pau/`, through the `board` skill. Every element carries a
   `source` - the line of the plan it came from. No source, no element.
2. Every open question becomes a decision with a default option. Do not stop to ask; start the work that
   does not depend on it.
3. Walk the four places assumptions come from (red actions, third parties, accesses, balances and limits)
   and test each one by its class. A permission nobody has granted is **named and stopped**, not reasoned
   around.
4. Push one unit end to end, dry if it touches a red line.
5. Record the heartbeat as "would create". **Create no scheduled run.**
6. Render `BOARD.md` and tell me, in a few lines: what you took on, what is stopped and why, and what is
   waiting on me.

If I am not here to answer, take the most reasonable reading, say at the top which reading you took, and
carry on.
