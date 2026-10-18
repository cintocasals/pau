# Changelog

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
