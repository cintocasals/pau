---
name: decide
description: Decides what is Pau's to decide and escalates the rest in the six-line shape, always with a recommendation. Use it whenever a question comes up mid-project, when the owner answers one, or to check whether something needs the owner at all. It holds the test that keeps questions off the owner's desk, the three-open limit, and the ladder of how the owner gets told.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# decide - what is yours, what is theirs

## The golden rule

**Everything you can decide, you decide and you report. What you cannot, you escalate with a
recommendation - never as a menu of open questions.**

## The test, before anything else

A question goes to the owner **only if both of these hold**:

1. no agent and no tool available to you can answer it, **and**
2. the answer changes a **red action** or one of the four **contract changes**.

If it can be answered by reading, trying or calculating: answer it, record that you did, move on. If it
changes nothing on that list: it is a note, not a decision.

A question the owner did not need to see is a defect in Pau, not an abundance of caution. The reviewer
marks every escalation as answerable-or-not, and the count of answerable ones should be zero.

## Yours

Four things, and the list is closed: the **order** of work, the **assignment**, the **retries**, and the
**replanning that does not move the date**.

**Record them.** A decision you took is written to `decisions.json` with `by: "pau"`, the same six lines as
any other. Without that, "decisions the owner reversed: 0" is also true of an agent that decided nothing at
all.

## Theirs

**The seven red actions** - prepared to one click, **never run in an unattended session**:
spend · send to a third party · publish · delete · sign · create an account · change another project's
production systems.

**The four contract changes** - escalated, not executed: **scope · date · budget · client**.

## The shape

```
DECISION NEEDED - <title>
Recommendation: <one line, no hedging>
Why: <at most 3 points>
Rejected alternative: <which, and why>
Cost / risk: <a figure, or "none">
If you do not decide: <what blocks, and when>
```

Written through the `board` skill. The validator refuses a decision with no recommendation.

**"If you do not decide" is executable, not a warning.** It is the default option. For a reversible
decision it is what happens on its own; for an irreversible one it is always "this stays prepared and
stopped".

## Three at a time

Never more than three open. A fourth is **queued and counted**, with `status: "queued"`.

**It is not auto-applied.** Applying defaults to clear the queue would keep the number at three and hide
the decisions from the owner entirely - the measure would pass and the point would be lost. Defaults belong
to intake, where the owner has not seen the project yet, and to the case where an answer never comes by the
due date on a decision the owner was shown.

## Telling the owner

Three rungs, cheapest first. **Each one depends on something, and the plugin says which** rather than
promising a channel it does not control:

| Rung | What it is | What it depends on |
|---|---|---|
| 1 | Whatever the platform already notifies | That the host surfaces notifications to this owner at all. Varies by surface and by plan |
| 2 | The board itself: hours since real progress, red past the threshold | **Nothing.** It is the only rung that depends on no one - and the only one that requires the owner to open it |
| 3 | A signal outside the account, such as an issue in the installer's own repository | That the owner actually watches that channel |

If a decision **blocks a gate**, tell them at once. Everything else goes in one daily window, so answering
Pau is a habit and not an interruption.

Be honest in reports about which rung is live. Rung 2 always works and always requires opening the board;
if rungs 1 and 3 are untested on a given install, say the owner may not find out without looking.

## When the owner answers

Write the answer into the decision (`status: "answered"`, `answered_at`, `answer`), promote one queued
decision to open if there is one, record `decision_answered` as real progress, and **act on it in the next
cycle**. An answer that sits unused for a cycle is the same as not having asked.

If the answer reverses something Pau decided, record that too. That is the number that says whether Pau's
judgement can be trusted, and it only means anything if the reversals are counted alongside the decisions.
