# Pau

**A plan you approved. Someone to run it.**

Pau is a Claude plugin that takes a project from approval to result. It turns the plan into one state
schema, pushes a whole unit of work end to end before it schedules anything, stops at the first defect, and
calls you only when price, date, scope or reputation changes - with the recommendation already made.

> Focus & Sian define. You approve. Pau delivers.

[Español](README.es.md) · [Català](README.ca.md)

---

## What it is for

You have a plan you already agreed to. What you do not want is to become the secretary of your own plan:
chasing what happened, re-reading your own notes to find where things stopped, answering twelve questions a
day that someone could have answered without you.

Pau is the layer between the plan and the work. You paste the plan, you get a board, you answer a few
decisions, and you can see the truth without asking for it.

## Install

**claude.ai and Cowork** - Customize → Plugins → Add → Add marketplace, and give it this repository's URL.
Then install `pau` from it.

**Claude Code**

```bash
claude plugin marketplace add cintocasals/pau
claude plugin install pau@pau
```

## Start

```
/pau:take  <paste your plan, or give a path to it>
```

Pau reads the plan, builds the state, names every assumption nobody has checked, stops the risky actions
that depend on them, and starts the work that does not. You get `BOARD.md` and a short note: what it took
on, what is stopped and why, what is waiting on you.

Then:

| Command | What it does |
|---|---|
| `/pau:take` | Hand over an approved plan |
| `/pau:cycle` | Run one management pass |
| `/pau:decide` | See the open decisions, or answer one |
| `/pau:board` | Rebuild the board and check it against the state |
| `/pau:close` | Close a task, judge a gate, close the project |

## How it decides

**Pau decides** four things: the order of work, the assignment, the retries, and the replanning that does
not move the date. That list is closed.

**You decide** the rest. Seven actions are prepared to one click and **never run in a session nobody is
watching**:

> spend · send to a third party · publish · delete · sign · create an account · change another project's
> production systems

A scheduled task's prompt is not your consent. An agent running at 3 a.m. has nobody to ask, so it does not
get to act on your behalf.

Plus the four contract changes, which come to you as decisions: **scope, date, budget, client**.

Every decision arrives in the same shape, and never without a recommendation:

```
DECISION NEEDED - Legal basis for the first email
Recommendation: Send only to addresses with recorded consent; do not buy a list.
Why: no address has a verified legal basis; sending is a red action; the gate does not need email.
Rejected alternative: Legitimate interest on public addresses - nobody verified it, and Pau does
  not issue legal opinions.
Cost / risk: none.
If you do not decide: the send stays prepared and stopped. The gate is unaffected.
```

**Never more than three open at once.** A fourth is queued and counted, not quietly decided for you.

## What is in the box

**Two agents.** `pau` directs, prioritises, delegates, and is the only one that writes state. `reviewer`
checks finished work against its own criterion with eyes that did not do it, and can stop the line.

**Five skills.** `intake` takes the plan and drives the first unit. `cycle` runs one pass. `decide` holds
the line between what is yours and what is Pau's. `board` is the only path that writes state. `close`
finishes a task, a gate or a project.

**One state schema,** in plain files at your project root:

```
.pau/state.json  .pau/tasks.json  .pau/gates.json  .pau/decisions.json  .pau/log.jsonl
BOARD.md
```

Every write is staged, validated and only then applied. A write that breaks the schema changes nothing and
tells you exactly what was wrong.

## Three things that are unusual, and why

**No clock-driven loop by default.** Checking something every hour and finding nothing is movement, not
work. Pau runs on events - you answered something, a piece came back, a gate falls due - with one daily
beat so a quiet project does not go dark, and a ceiling of four scheduled runs a day.

**Every run leaves a trace, even a run that did nothing.** The validator refuses a write that adds no log
entry. This sounds like bookkeeping until you try to answer "how much of this was real?" about a system
that only wrote things down when something happened: a loop like that looks perfect from the inside and
tells you nothing.

**Nothing is invented.** Every element of state carries a `source` - the line of the plan it came from. No
source, no element. The board is a view of the state, never a second version of it, and when the two
disagree the state wins.

## The silence detector

When an account hits its usage limit, scheduled runs are refused and nothing announces it. A watchdog
inside the same account stops at the same moment.

`templates/silence-check.yml` is a GitHub Action you copy into your own repository. It watches **progress,
not runs** - a task moving, a gate passing, a decision answered, a new deliverable - and opens an issue
when that stops. No server, no extra account.

## What this does not do

It does not replace your issue tracker, your calendar or your CI. It does not write code for you or do the
domain work; it decides what gets done next, gets it done by whoever does it, checks it, and keeps the
record straight.

It does not sit between you and your own tools. A department - a subagent, a skill you already have, a
person - receives a work order and returns a note of delivery. Pau converts that into state. That is the
only reason there is one writer and not ten.

One honest note about enforcement: on surfaces where plugin hooks run, a hook can intercept a write. In
claude.ai chat they do not run. So the single-writer rule is held by the validator and by discipline, not
by the platform. The validator refuses a bad write and catches a bad edit the next time it runs; it cannot
stop someone editing a JSON file by hand.

## Requirements

Python 3 for the two scripts. Nothing else - no server, no database, no account beyond the one you already
have.

## Licence

MIT. See [LICENSE](LICENSE).
