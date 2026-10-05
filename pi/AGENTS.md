# Global working rules

Project instructions add specifics and override these preferences on conflict.

## Environment

- Read the project's AGENTS.md and check lockfiles before choosing a package manager or build tool.

## How to work

- Prefer the smallest correct solution consistent with the existing architecture. No drive-by refactors, reformatting untouched code, or speculative abstractions.
- Read files fully before editing them. For investigations or broad changes, trace the relevant flow rather than relying on search snippets.
- Verify unfamiliar dependency APIs against installed types/source or version-matched documentation; do not guess.
- Investigate routine uncertainty using the repository. Ask one focused question when a consequential requirement cannot be resolved from evidence, or applicable instructions genuinely conflict.
- Prefer isolated tests. Ask before checks that use live credentials, incur charges, or mutate external services or machine configuration.
- Verify changes with the narrowest relevant test, lint, or build. Never imply verification that did not happen; say explicitly when a check cannot run.
- Keep noisy output bounded, but preserve command exit status. When piping tests or builds through filters, enable `set -o pipefail` or capture the original exit status. Read saved full output when truncation hides important evidence.
- If the same test still fails after two fix attempts, stop and summarize what you tried and what you suspect.

## Code conventions

- TypeScript: assume strict mode; no `any` without a comment justifying it; functional React components only.
- Java: constructor injection, no field `@Autowired`; annotate nullability at boundaries.
- Rust: no `unwrap()` or `expect()` outside tests and `main()`; propagate errors with `?`.
- Comments explain why, not narrate obvious code.
- Do not preserve backward compatibility unless the user asks for it.

## Formatting

- Format only modified files; project instructions take precedence.
- Rust: use rustfmt on changed files, or `cargo fmt` when it will not introduce unrelated changes.
- TS/JS: use oxfmt and oxlint on modified files, rather than Prettier or ESLint, unless project instructions specify otherwise.
- Java: respect existing Checkstyle/Spotless configuration; otherwise preserve existing formatting.

## Git and sensitive files

- Never commit or push unless explicitly asked. Staging is allowed.
- Treat pre-existing changes as user or other-session work. Do not overwrite, revert, or stash them.
- Stage explicit paths only, never `git add .` or `git add -A`. Before committing, inspect the staged diff and include only this session's changes.
- Do not bypass Git hooks unless explicitly asked.
- Use conventional commit messages: imperative, under 72 characters, with a body only when the reason is not obvious.
- Never commit secrets, environment files, or credentials. If you encounter an exposed secret, flag it without repeating its value and stop.
- Ask before destructive operations, reading secret-bearing `.env` files, or changing configuration outside the requested scope. These instructions are behavioral guidance, not a sandbox or enforced approval gate.

## Communication

- When asked a question or for analysis, answer first. Do not treat it as permission to implement changes.
- Lead with the outcome, then relevant details. No preamble or restating the request.
- Name consequential judgment calls so they can be overridden.
- Be concise; report changed files, verification, and unresolved issues when finishing implementation.

## Web research

- Prefer repository source, installed dependency types/source, and project docs before web search.
- Use web search when behavior depends on current or version-specific external information, when an unfamiliar API cannot be resolved locally, or when the user explicitly asks for research/current information.
- Prefer official/version-matched documentation over blogs or summaries.
- Be proactive about researching current, version-appropriate conventions and recommended approaches when the user's query or repository does not clearly establish them. Prefer official documentation and primary sources, and verify unfamiliar APIs rather than guessing.
- Do not search the web for facts that can be determined reliably from the repository.

## pinata subagents

- For pinata jobs, first look for `.pi/pinata.json` at the project root. If it exists, use it as the job's `config`; it may set `models`, `fallbacks`, `setup`, `codemode`, `limits`, and `passEnv`. Show me any `setup` command it contains before starting the run.
- If the project has no `.pi/pinata.json`, use `models` and `fallbacks` from ~/Projects/dotbento/pi/pinata/models.json.
- Models I name in a request override both.
- To give a project its own config, copy ~/Projects/dotbento/pi/pinata/models.json to `.pi/pinata.json` in that project and edit it.
