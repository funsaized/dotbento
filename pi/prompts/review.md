---
description: Adversarial review of staged and unstaged changes, without edits
argument-hint: "[focus]"
---
Review the current changes as an independent senior engineer. Try to falsify the solution rather than validate it.

Run `git diff` and `git diff --staged`; inspect surrounding code, callers, and tests as necessary. Prioritize correctness, security, regressions, broken invariants, concurrency/state problems, architectural mismatches, unnecessary complexity, and missing tests.

Additional focus: ${@:-none}.

Do not modify files, stage changes, commit, or push. Only run non-mutating inspection commands; ask before any verification that could alter files or external state.

Report concrete findings in severity order with file:line references, the failure scenario, and supporting evidence. Separate confirmed defects from speculative concerns and optional suggestions. If no concrete defects are found, say so and identify remaining verification gaps.

This prompt does not create a separate agent, switch models, or enforce read-only access. For independent review, invoke it in a fresh session that has not seen the implementation discussion.
