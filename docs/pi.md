# Why Pi starts with a small configuration

Pi carries the same verification, small-diff, language, and Git expectations as
OpenCode, without importing OpenCode's named agent workforce. Global instructions
live in `pi/AGENTS.md`; project instructions supply local requirements. Pi's own
system prompt remains intact.

## Model selection is explicit

The scoped cycle contains GPT-6 Luna at xhigh, GPT-6.1 Sol at low, and DeepSeek
V4.1 Flash at low. Luna is the startup default. DeepSeek's direct API calls
V4.1 Flash `deepseek-flash`; there is no custom provider or model alias file.
Thinking levels are set both per model and in cycle entries so a model change
does not accidentally carry Luna's xhigh setting into lighter work.

The portable settings file is merged rather than linked. Pi writes settings
itself, and machine-specific theme, identity, packages, and unrelated model
preferences must remain local. `scripts/configure-pi.py` backs up changed settings
and preserves unrelated keys, including unrelated per-model thinking levels.
Re-running installation reapplies the tracked model defaults and scope.

## Review is a prompt, not an agent framework

`pi/prompts/review.md` keeps the adversarial diff review from OpenCode. It asks
for severity-ordered findings, concrete failure scenarios, evidence, and no
modifications. It does not spawn a child agent, select a model, or enforce tool
permissions. A fresh session avoids exposing the reviewer to the implementation
discussion. Independent review automation can be added later if the manual
workflow becomes a bottleneck.

## Two selected packages

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

`pi/web-search.json` holds credential-free defaults. The installer follows the
extension's XDG/agent-directory discovery and merges those defaults into a real
machine-local file with private permissions. Credentials come from the local
`tavilyApiKey` field, its secret-source reference, or `TAVILY_API_KEY`; they are
never added to tracked defaults. Existing credentials survive reinstallation,
and private backups remain outside the repository. The repository scanner also
recognizes Tavily token shapes and reports matches without revealing values.

Herdr continues to own its generated Pi extension. Shared skills already in
`~/.agents/skills` are discovered by Pi and are not duplicated here. Browser MCP,
planning agents, and custom compaction settings are deliberately absent.

## Permissions are not silently equivalent

OpenCode's approval rules and role restrictions are not imported. Global
instructions ask for care around destructive operations and sensitive files,
but they do not enforce approval or provide isolation. Pi and installed
extensions run with the current user's permissions. Sensitive tasks need an
appropriate execution boundary, not just a prompt claiming to be read-only.
