---
name: intake
description: Turns an approved plan into one state schema and drives the first whole unit of work end to end before anything is scheduled. Use it when a project is handed to Pau for the first time - a plan, a brief, a PDF, an email thread. It extracts tasks with criteria, gates, decisions, red lines and budget, names every unverified assumption, stops the red actions that depend on them, and only proposes a heartbeat once one unit has actually gone through.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
---

# intake - the contract, and the first whole unit

Two jobs, in this order. **Never the second before the first, and never a scheduled run before both.**

## Job 1: the contract

Read the plan and produce one state schema: tasks with an owner, a `done_when` and a stop signal; gates;
indicators; decisions; red lines; budget. Write it through the `board` skill.

**Every element carries a `source`** - the line of the plan it came from. No source, no element. That is
what "nothing invented" means when it is a rule and not a wish.

**Every open question becomes a decision with a default option,** and work that does not depend on it
starts. You do not stop to ask.

**If the input is not a structured plan** - a PDF, an email, a ticket board, a conversation - read what you
were given and, **for each of the six elements it does not contain, open a decision with a default
option** instead of asking. The six: tasks, gates, indicators, red lines, budget, and who the owner is.

**Target: the board is live and the first unit is moving within 10 minutes** of being handed the plan. If
you are past that, you are designing instead of taking the project.

## Job 2: the first whole unit, before any loop

Verify every assumption against reality, then push **one unit of work end to end** - dry if it touches a
red line. Only when that unit has passed do you propose a heartbeat. Until then the heartbeat is recorded
as "would create", not created.

### a) Where assumptions come from

Do not hunt by intuition. Walk the plan and take one assumption for each of these four, because these are
what stop a line:

1. **every red action** the plan takes for granted;
2. **every third party** in it - supplier, gateway, customer, recipient;
3. **every access** needed - credential, connector, account, hardware;
4. **every balance or limit** an action depends on.

### b) The test, by class

Different classes of precondition are checked differently. Getting this wrong is how a project looks ready
and is not. Full detail in `references/precondition-classes.md`.

| Class | How you test it | When you cannot |
|---|---|---|
| **A figure you read** (a balance, a quota, a count) | Read it. If you have no access, ask for it as **data**, not as a decision | Decision: "what is X", default "stop the action that depends on it" |
| **A connection you try** (a connector, an API, a credential) | One read-only call | Decision: "reconnect X", red action prepared |
| **A permission someone must give** (a legal basis, an approval, a right to contact) | **You do not test it. There is nothing to query.** Name it and stop the red action that depends on it | Always a decision for the owner |
| **An account limit** (usage, rate, spend) | Read the consumption and compare it with the ceiling | With no ceiling set, create no heartbeat: work only in attended sessions |
| **Absent hardware or a missing tool** | Check the tool answers before planning work on it | The task stays `blocked` with the cause, and the line continues elsewhere |

The third row is the one people get wrong. A permission that nobody has granted cannot be discovered by
trying harder; it can only be named.

### c) What "stop dry" means, exactly

It is not doing nothing. It is these four, in order:

1. **Name** the unverified assumption, in one line, in the log.
2. **Stop only the red action that depends on it** - not the whole line.
3. **Open a decision** in the six-line shape, with a recommendation and a default option.
4. **Carry on** with everything that does not depend on it.

Doing those four is what "finding a blocker" means. **It is not resolving it.** Pau does not issue legal
opinions, and an assumption named and stopped is worth more than one quietly assumed away.

### d) When a question goes to the owner, and when it does not

A question is escalated **only if both hold**:

- no agent and no tool available to you can answer it, **and**
- the answer changes a red action or one of the four contract changes (scope, date, budget, client).

If it can be answered by reading, trying or calculating, you answer it and record that you did. If it
changes nothing on that list, it is a note, not a decision.

This is the test that keeps the count at zero. A question the owner did not need to see is a defect in Pau.

## What good looks like at the end of intake

- The board is live, and every element on it has a `source`.
- Every unverified assumption is named, with the red action that depends on it stopped.
- At most three decisions are open, each in the six-line shape, each with a recommendation.
- One unit of work has gone end to end, or it is stopped at a named blocker.
- **No scheduled run exists yet.** The heartbeat is recorded as "would create".
