# The Pau state schema

Closed: a field that is not here is rejected. Enforced by `scripts/validate_state.py`.

## `.pau/state.json` - one object

| Field | Type | Notes |
|---|---|---|
| `project` | string | **required** |
| `source` | string | **required**. Where the approved plan came from |
| `phase` | string | |
| `status` | enum | **required**. `running` \| `attention` \| `stopped` |
| `status_note` | string | one line; why it is not `running` |
| `next_gate` | gate id | |
| `next_gate_due` | date | |
| `last_progress_at` | ISO 8601 | the clock the board turns red on |
| `last_progress_what` | enum | `task_status` \| `gate_passed` \| `decision_answered` \| `deliverable`. Nothing else counts as progress |
| `resume_point` | string | one line: where it stopped, what came next, what it waited for |
| `lease_holder` | string | the session holding the turn |
| `lease_until` | ISO 8601 | |
| `open_decisions` | int | at most 3 |
| `queued_decisions` | int | the ones past 3 |
| `tasks_in_flight` | int | at most 3 |
| `budget_runs_total` | int | execution budget |
| `budget_runs_used` | int | |
| `usage_pct` | number | stop at 80 |
| `stop_requested` | bool | the owner's stop |
| `stopped_by`, `stopped_at` | string, ISO | |
| `resumed_by`, `resumed_at` | string, ISO | |
| `updated_at` | ISO 8601 | **required** |
| `updated_by` | string | **required**, and must be `pau` |

## `.pau/tasks.json` - `{id: task}`

| Field | Type | Notes |
|---|---|---|
| `title` | string | **required** |
| `status` | enum | **required**. `pending` \| `in_progress` \| `blocked` \| `done` \| `stopped` |
| `done_when` | string | **required, non-empty**. Checkable by someone who did not do the work |
| `source` | string | **required, non-empty**. The line of the plan this came from |
| `owner` | string | who does it: an agent, a skill, a person |
| `stop` | string | the stop signal: when to stop and report instead of continuing |
| `budget` | string | runs, time or money |
| `depends_on`, `blocks` | list of ids | |
| `due` | date | |
| `critical` | bool | on the critical path |
| `attempts` | int | rounds used |
| `max_attempts` | int | 3 for a deliverable, 2 for a technical step |
| `deliverable` | string | path or link |
| `evidence` | string | required in practice once `status` is `done` |
| `reviewed_by`, `reviewed_at` | string, ISO | the reviewer, who did not do the work |
| `red_action` | bool | needs the owner present; never runs unattended |
| `note` | string | for a `blocked` task, the cause |

## `.pau/gates.json` - `{id: gate}`

`title`\*, `date`\*, `criteria`\* (list), `result`\* (`pending` \| `pass` \| `fail`), `source`\*,
`numbers`, `decided_by`, `decided_at`.

## `.pau/decisions.json` - `{id: decision}`

The six lines, as fields. All of these are required: `title`, `recommendation`, `why` (list, at most 3),
`alternative`, `cost_risk`, `if_no_answer`, `status` (`open` \| `queued` \| `answered`), `opened_at`,
`source`, `by` (`pau` \| `owner`).

Optional: `due`, `answered_at`, `answer`, `blocks_gate`, `reversible`, `default_option`.

`by` matters. **Pau records the decisions it takes itself,** not only the ones it escalates. Without that,
"decisions the owner reversed: 0" is satisfied just as well by an agent that decided nothing.

## `.pau/log.jsonl` - one JSON object per line

| Field | Type | Notes |
|---|---|---|
| `ts` | ISO 8601 | **required** |
| `by` | string | **required** |
| `kind` | enum | **required**. `cycle` \| `progress` \| `decision` \| `gate` \| `stop` \| `quality` \| `norm` |
| `text` | string | **required**, one line |
| `changed` | bool | **required**. Did this run change state? |
| `run_id` | string | |
| `chosen`, `rejected` | task ids | the task picked, and the first one passed over |

`changed` is the field that makes "how many cycles did nothing?" a number instead of a feeling. Count it
over runs, never over log entries: a loop that writes only when something happens will look perfect and
tell you nothing.

`chosen` and `rejected` make the priority order checkable: the task worked on should be the first on the
ordered list every time.
