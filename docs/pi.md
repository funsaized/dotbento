# Why Pi starts with a small configuration

Pi carries the same verification, small-diff, language, and Git expectations as
OpenCode, without importing OpenCode's named agent workforce. Global instructions
live in `pi/AGENTS.md`; project instructions supply local requirements. Pi's own
system prompt remains intact.

## Model selection is explicit

The scoped cycle contains GPT-6 Luna at xhigh, GPT-6 Astra at medium,
GPT-6.1 Sol at low, and DeepSeek V4.1 Flash at max. Luna is the startup
default. DeepSeek's direct API calls V4.1 Flash `deepseek-flash`; there is no
custom provider or model alias file.
Thinking levels are set both per model and in cycle entries so a model change
does not accidentally carry Luna's xhigh setting into lighter work.

The portable settings file is merged rather than linked. Pi writes settings
itself, and machine-specific theme, identity, packages, and unrelated model
preferences must remain local. `scripts/configure-pi.py` backs up changed settings
and preserves unrelated keys, including unrelated per-model thinking levels.
Re-running installation reapplies the tracked model defaults and scope.

## Context management

Pi 1.1.0 supports per-model compaction budgets. Automatic compaction stays
enabled, with a fallback reserve of 32,768 tokens and 32,000 recent tokens kept
without summarization. The selected models override those budgets:

| Models | Pi catalog context window | Reserved tokens | Compaction above | Recent tokens kept |
|---|---:|---:|---:|---:|
| GPT-6 Luna, Astra, and GPT-6.1 Sol | 272,000 | 72,000 | 200,000 | 32,000 |
| DeepSeek V4.1 Flash | 1,000,000 | 600,000 | 400,000 | 48,000 |

These are starting points for coding sessions, not model capability limits.
Pi triggers compaction when context exceeds the catalog window minus the reserve;
recalculate reserves if catalog windows change. The retained-token budget does
not include every component of the resulting context, such as the summary.
`reserveTokens` also influences summarization output limits, capped by the model's
maximum output tokens. Monitor DeepSeek summary usage in particular because its
large reserve permits a large output budget.

Cache-miss notices are enabled to make cache behavior and compaction usage visible.
Cache warming, retries, and model context metadata retain Pi's defaults. Use the
existing `PLAN.md` handoff workflow to preserve decisions and unfinished work
across compaction or fresh sessions.

## Review is a prompt, not an agent framework

`pi/prompts/review.md` keeps the adversarial diff review from OpenCode. It asks
for severity-ordered findings, concrete failure scenarios, evidence, and no
modifications. It does not spawn a child agent, select a model, or enforce tool
permissions. A fresh session avoids exposing the reviewer to the implementation
discussion. Independent review automation can be added later if the manual
workflow becomes a bottleneck.

## Planning and fresh-session handoff

`/plan <task>` ports the OpenCode planner into a prompt template. It investigates
real call paths and maintains root `PLAN.md` with requirements, current state,
decisions, concrete implementation steps, findings, and confirmed validation
commands. It ends at `Ready for implementation` or `Blocked`, without implementing.
The template does not change the selected model; choose Astra at medium through
Pi's model picker when wanted.

Optionally run `/plan-review-adversarial [plan-path] [feedback-output-path]`.
Defaults are `PLAN.md` and `PLAN-REVIEW.md`. The lazily loaded review skill checks
references and failure modes and writes separate feedback without changing the
plan. Unlike the original OpenCode skill, it uses proportional review criteria,
not blanket bans on mocks or mandatory code-snippet lengths. Return to the
planning session to reconcile findings before implementation.

Start a fresh session in the same repository, then run `/implement-plan` (or
`/implement-plan path/to/plan.md`). It reads the plan, checks readiness and current
repository state, implements, verifies, and records progress in the plan. No
previous conversation is needed. For a direct CLI kickoff:

```bash
pi -n "Implement plan" @PLAN.md "/implement-plan"
```

All three commands are instructions, not permission restrictions, separate agent
roles, or automatic model switches. No edit-permission guard is installed.

## Three selected packages

Ponytail is installed through Pi's native package manager, pinned to the reviewed
4.10.0 release commit. It contributes a Pi extension and lazily loaded skills;
it is not a port of the OpenCode plugin. Package installation remains opt-in
through `--packages`, or the explicit commands in the root README.

pi-web-access adds search, page fetching, and retrieval of stored results. Search
is explicitly limited to Tavily, rather than inheriting the package's broad
fallback chain. The default workflow returns results without a generated summary
or curator browser. Source-check tooling, curator commands, browser cookies,
YouTube, and local-video features are initially disabled. Page extraction uses
direct HTTP only, without handing URLs to hosted extraction services.

Pi Atelier 0.13.0 adds a model/status rail and live activity sidebar, opened with
`/atelier` or F6. Dotbento installs the pinned npm release through `--packages`;
its user configuration stays in Atelier's own `pi-atelier.json` file rather than
being merged into Pi's general settings. Its defaults remain package-owned.

`pi/web-search.json` holds credential-free defaults. The installer follows the
extension's XDG/agent-directory discovery and merges those defaults into a real
machine-local file with private permissions. Credentials come from the local
`tavilyApiKey` field, its secret-source reference, or `TAVILY_API_KEY`; they are
never added to tracked defaults. Existing credentials survive reinstallation,
and private backups remain outside the repository. The repository scanner also
recognizes Tavily token shapes and reports matches without revealing values.

Herdr continues to own its generated Pi extension. Shared skills already in
`~/.agents/skills` are discovered by Pi and are not duplicated here. Browser MCP
and agent-framework extensions are deliberately absent from package installation.

## Permissions are not silently equivalent

OpenCode's approval rules and role restrictions are not imported. Global
instructions ask for care around destructive operations and sensitive files,
but they do not enforce approval or provide isolation. Pi and installed
extensions run with the current user's permissions. Sensitive tasks need an
appropriate execution boundary, not just a prompt claiming to be read-only.
