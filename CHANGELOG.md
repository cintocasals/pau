# Changelog

## 0.1.1 - 2026-10-20

Two defects found by running the plugin against a real plan, before it was made public.

- **The board counted quiet cycles over log entries instead of over runs**, which is exactly what
  `skills/board/references/schema.md` says never to do. A loop that writes only when something happens
  looked better than it was: on the test run the board said 4 of 6 entries where the truth was 3 of 4 runs.
  Fixed: a run is one `cycle` entry found by its `run_id`, and a run counts as having changed something if
  any of its entries carries `changed: true`. The validator now requires `run_id` on every cycle entry.
- **The state had no money budget.** With a plan whose first red action is spending, `BOARD.md` said "no
  budget set". Added `budget_money_total`, `budget_money_spent` and `budget_currency`, rendered on the
  board with the same stop-at-80 mark as usage.

Also: `dist/` removed from the repository. The packaged plugin is attached to the release instead, so an
install no longer carries a copy of itself.

## 0.1.0 - 2026-10-18

First build. Not yet released.

- Two agents: `pau` (the only writer of state) and `reviewer` (eyes that did not do the work).
- Five skills: `intake`, `cycle`, `decide`, `board`, `close`.
- Five commands: `/pau:take`, `/pau:cycle`, `/pau:decide`, `/pau:board`, `/pau:close`.
- A closed state schema in plain files, with a validator that stages a write, checks it, and applies it
  only if it passes. It refuses a write that adds no log entry, a task with no `done_when` or no `source`,
  a decision with no recommendation, a fourth open decision, a fourth task in flight, a write by anyone
  other than `pau`, a write while another session holds the turn, and any field outside the schema.
- `BOARD.md` rendered from the same schema, with hours since real progress rather than since the last run.
- A silence detector as a GitHub Action template, to run outside the account it watches.
- README in English, Spanish and Catalan.

No `bin/` directory, deliberately: a plugin with executables at the top level is refused outright by
claude.ai chat and Cowork. The scripts live inside the `board` skill and are called with a path relative to
its `SKILL.md`.
