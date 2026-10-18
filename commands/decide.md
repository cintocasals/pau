---
description: Show the open decisions, record an answer, or work out whether something needs me at all.
argument-hint: "[decision id and your answer, or a question to triage]"
---

$ARGUMENTS

Use the `decide` skill.

**If I gave you an answer:** record it on that decision (`status: answered`, `answered_at`, `answer`)
through the `board` skill, promote a queued decision to open if there is one, count it as real progress,
and act on it in this same pass if you can.

**If I asked about a question:** run the test before anything else. It only comes to me if no agent and no
tool you have can answer it **and** the answer changes a red action or one of scope, date, budget or
client. Otherwise answer it yourself and record that you did.

**If I asked for nothing in particular:** show me what is open, in the six-line shape, newest first, and
the queued ones underneath with nothing but their titles. Tell me which ones block a gate.

Never show me a decision without a recommendation.
