---
name: plan-review-adversarial
description: Adversarially review an implementation plan using repository evidence and pre-mortem analysis. Use when asked to challenge a plan, find its failure modes, or run plan-review-adversarial. Write separate feedback without modifying the plan or implementing changes.
---

# Adversarial plan review

Assume the plan failed. Find the concrete assumptions and failure modes that
would explain it, then check whether repository evidence disproves them.
Be skeptical, not performatively negative: do not invent risks to fill a quota.

## Inputs and boundaries

Use the supplied `plan-path` and `feedback-output-path`; default to `PLAN.md` and
`PLAN-REVIEW.md` in the current repository. Read repository instructions and the
entire plan before reviewing. Verify that the output is not the plan itself
(including symlink aliases). If they resolve to the same file, ask for a separate
output path without writing. If the plan is missing, report that blocker rather
than fabricating a review.

Only write the feedback file. Do not modify the plan, source, tests, configuration,
or dependencies. Do not begin implementation or run destructive commands. If an
existing feedback file concerns another task, ask before replacing it.

## Review

1. Check the objective and scope against the user's request and repository rules.
2. Trace the relevant behavior, affected callers, state/data flow, and persistence
   boundaries. Read files rather than trusting names or the plan's claims.
3. Independently verify implementation-critical file, symbol, library, and API
   references against the installed version, source, or authoritative docs.
   Check signatures and behavior. Distinguish existing symbols from proposed
   ones; new symbols need a clear contract, not an existing implementation.
4. Classify consequential assumptions as verified, plausible but unverified, or
   risky. Cite evidence. If external documentation is unavailable, say so and
   require a verification step when implementation depends on it.
5. Examine failure behavior, edge cases, compatibility, ordering, permissions,
   external dependencies, blast radius, detection, and recovery where relevant.
6. Check that steps identify concrete locations, are dependency-ordered, reuse
   existing patterns, and include proportional validation with real commands.
   Identify stale findings, missing blockers, and unnecessary scope.
7. Review the whole plan, then write all findings in one pass. Use independent
   parallel investigations only when those tools are available and useful.

## Proportionality

Judge correctness and delivery risk, not compliance with arbitrary ceremony.
Small configuration/documentation changes need precise changes and focused
checks, not implementation snippets or broad test suites. Require signatures,
examples, formulas, or pseudocode only where they resolve consequential ambiguity.
Prefer existing algorithms and abstractions; do not demand state-of-the-art
citations for ordinary engineering choices.

Follow repository rules for testing, typing, compatibility, and linting. Do not
categorically reject mocks, necessary compatibility behavior, primitive types,
or an otherwise sound plan lacking a new lint rule. Distinguish genuine safety
problems from preferences. Mark irrelevant checks N/A and avoid minimum finding
counts, blanket requirements, or arbitrary snippet lengths.

Keep delivery estimates out of technical plans; an `Updated:` maintenance
metadata line is fine. A missing detail is blocking only if it prevents safe,
correct implementation and cannot reasonably be resolved during implementation.

## Feedback format

Write Markdown to the feedback output path:

# Adversarial Review: <plan name>

- Plan: `<path>`
- Overall assessment: **APPROVED** or **NEEDS REVISION**

## Summary

Briefly state whether implementing the plan would achieve the objective safely.

## Reference validation

List consequential references, expected behavior, verified source locations,
and VERIFIED / MISMATCH / UNVERIFIED status. Identify proposed contracts clearly.

## Assumptions and failure modes

For each meaningful risk, state the assumption, failure scenario, root cause,
impact, detection, mitigation already in the plan, and evidence. Include single
points of failure where relevant. Separate verified facts from judgments.

## Blocking findings

Order by severity. For each finding include the exact plan section or reference,
why it threatens the objective, the required outcome, acceptance criteria, and
how to verify them. Say "None" if there are no blockers. Do not prescribe a full
implementation or demand unrelated cleanup.

## Non-blocking recommendations

List proportional improvements separately from approval requirements.

## Verification limits

State what could not be confirmed, what checks actually ran, and any N/A areas.
Do not claim tests or documentation verification that did not happen.

Approve when implementation-critical assumptions are verified or have adequate
verification/mitigation steps, the approach fits the repository, and no material
blockers remain. Otherwise request revision with specific evidence-based reasons.
Finish the chat response with the feedback path, assessment, and top findings;
do not duplicate the complete report.
