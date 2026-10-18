# The five classes of precondition

A plan that has been approved is a plan somebody believes. Intake's job is to find the places where belief
and reality have not been compared yet, before a loop is built on top of them.

These five classes are not a taxonomy for its own sake. They exist because **each one is checked
differently**, and treating them the same is how a project passes intake and stops on day one.

---

## 1. A figure you read

A balance, a quota, a credit, a count of something.

**Test:** read it. One call, one number.

**If you have no access:** ask the owner for it **as data, not as a decision**. "What is the balance on X?"
is not a decision; it has no options and no recommendation. Record it as a blocked task with the cause, and
open a decision only for the action that depends on it, with the default "stop that action".

**Failure mode:** assuming a balance is fine because it was fine when the plan was written. A plan written
on Monday and run on Friday is a plan with a stale number in it.

---

## 2. A connection you try

A connector, an API, a credential, an integration that has to be live.

**Test:** one read-only call. Not a write. A connector that reads is not necessarily a connector that
writes, so if the plan needs a write, say which one you tested.

**If it fails:** open a decision to reconnect it, and prepare the red action behind it without running it.

**Failure mode:** the connector was authorised once, and the token expired quietly. Nothing announces this.

---

## 3. A permission someone must give

A legal basis for contacting people, a right to publish, an approval, a licence, a consent.

**Test: there isn't one.** This is the class people get wrong, because the habit of checking is to go and
look, and here there is nothing to look at. A permission that nobody has granted does not become granted by
querying harder.

**What you do instead:** name it, stop the red action that depends on it, open a decision for the owner,
and continue with the rest of the plan. **Do not reason your way to it being probably fine.** Pau does not
issue legal opinions, and "we can probably rely on X" written by an agent is worth nothing to the person
who would be answering for it.

**Failure mode:** a plan says "email the list" and nobody asked where the list came from or what gives the
right to use it. The plan is not wrong; it just never contained the answer.

---

## 4. An account limit

Usage, rate limits, spend ceilings, quotas on the account the work runs in.

**Test:** read the consumption and compare it with the ceiling. Stop at 80 %, not at the ceiling: by the
time a run is refused there is nobody there to notice.

**If no ceiling has been set:** create no heartbeat at all. Work only in attended sessions and open the
decision. A scheduled loop with no budget is a loop that stops silently on a day you did not choose.

**Failure mode:** scheduled runs start being refused, each refusal is invisible, and the board keeps
showing the last good state. This is the one that needs the silence detector, because the project does not
report its own absence.

---

## 5. Absent hardware or a missing tool

A machine that has to be awake, a local bridge, a tool only present on one surface.

**Test:** check the tool answers before planning work that needs it.

**If it does not:** the task stays `blocked` with the cause - not failed, not retried in a loop - and the
line continues with something else. A scheduled task bound to a machine that is not there suspends itself,
and a suspended task is not a task that reports a problem.

**Failure mode:** half the plan silently depends on one machine being awake, and nobody noticed because it
usually is.

---

## The pattern underneath

Classes 1, 2, 4 and 5 are **discoverable**: there is a thing to read or call, and the answer exists
somewhere.

Class 3 is **not discoverable**: the answer exists only in a decision somebody has to take.

An intake that only knows how to look will find four of the five and walk confidently past the fifth, which
is usually the one with the legal or reputational cost behind it.
