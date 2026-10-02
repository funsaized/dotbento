---
description: Implement a ready plan with no previous-session context required
argument-hint: "[plan-path]"
---
Read `${1:-PLAN.md}` completely and follow repository instructions.

Treat the plan as the durable handoff, not as proof the repository is unchanged.
Check its status, requirements, decisions, findings, and validation against the
current files and working tree before editing. If it is blocked or not ready for
implementation, resolve routine uncertainty from repository evidence; ask one
focused question for consequential requirements that cannot be resolved. Do not
implement a plan with unresolved blockers.

Implement the smallest correct change, in dependency order, without unrelated
cleanup. Reuse the plan's verified findings, but inspect affected code and callers
before changing behavior. Record material deviations and their reasons in the
plan. Preserve unrelated work and do not commit or push unless explicitly asked.

Run the narrowest relevant checks, using confirmed repository commands. Update
PLAN.md with implementation progress, verification results, and remaining work;
distinguish completed work from checks that could not run. Finish with changed
files, actual verification, and unresolved issues.
