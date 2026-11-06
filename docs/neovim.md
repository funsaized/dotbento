# Why Neovim is portable rather than platform-specific

Dotbento keeps one LazyVim configuration for macOS and Omarchy Linux. Platform
differences are resolved at runtime instead of maintaining two plugin trees.

## LazyVim is the base, not a template to fork

`nvim/init.lua` delegates to `config.lazy`, which bootstraps `lazy.nvim` when
needed and imports LazyVim's plugin specification. Local files override only
the behavior Dotbento intentionally changes.

This preserves LazyVim's maintained defaults for completion, diagnostics,
navigation, Git integration, and UI behavior. Dotbento does not reimplement
those systems.

Plugin releases are pinned by commit in `lazy-lock.json`. The config currently
resolves to 62 plugins. The lockfile gives both supported platforms the same
plugin graph after synchronization.

## Extras reflect the reference development workload

`nvim/lazyvim.json` is the source of enabled extras. The current set is:

- DAP core (`dap.core`) and Neovim-Lua DAP (`dap.nlua`);
- Snacks explorer, dial, and inc-rename;
- JSON with SchemaStore support, Markdown rendering and preview;
- TypeScript with vtsls for types and navigation;
- TypeScript Oxc (`lang.typescript.oxc`) for oxlint diagnostics and oxfmt;
- Java (`lang.java`);
- util extras for dotfiles and mini.hipatterns.

Markdownlint is disabled for both nvim-lint diagnostics and Conform fixes.
Example specs and the preload cache for every Omarchy theme are excluded.
LazyVim's own Catppuccin and Tokyo Night support remains. Parity means matching
active development capabilities, not retaining every package once downloaded.

## Debugging uses DAP extras, not a custom plugin tree

`dap.core` is the generic Debug Adapter Protocol stack: `nvim-dap`,
`nvim-dap-ui`, virtual text, and Mason installation of adapters. Language
debuggers (for example Mason's `js-debug-adapter` for JavaScript and
TypeScript) plug into that stack. They are not extra LazyVim extras.

`dap.nlua` only debugs Neovim Lua, via `one-small-step-for-vimkind`. It is
present so the editor config itself can be stepped. It is not the TypeScript
path.

## Formatting remains an explicit action

`vim.g.autoformat` is disabled. Format-on-save can produce broad changes when
opening an unfamiliar repository, so Dotbento leaves formatting on
`<leader>cf`.

The Oxc extra registers **oxfmt** with conform for JavaScript, TypeScript, and
JSON, and attaches **oxlint** as an LSP. The oxfmt LSP is left disabled so
conform stays the only format owner, matching Zed's "one owner per language"
choice. Project-local `oxfmt` / `.oxfmtrc.json` still win when present;
Mason's `oxfmt` is the fallback binary.

vtsls remains for hover, go-to-definition, and TypeScript language features.
Oxlint does not replace it.

The formatter integration still exists. Only the trigger changes from implicit
to deliberate.

## Java formatting belongs to the project, not jdtls

`lang.java` still supplies nvim-jdtls for language features. It does not own
layout. `lua/plugins/java-spotless.lua` turns jdtls formatting off and
registers a Conform formatter named `spotless_maven`.

The formatter is portable because it discovers the work from the buffer, not
from a machine-specific path:

- the nearest `pom.xml` is the module root;
- the formatter is active only when that POM contains `spotless-maven-plugin`;
- `./mvnw` is preferred when present, otherwise `mvn` from PATH;
- `-DspotlessFiles` is the absolute file path, regex-quoted for an exact match.

Palantir JavaFormat is whatever the module's Spotless configuration already
pins. Dotbento does not vendor a Palantir version or a style XML. Repositories
without Spotless keep jdtls formatting disabled and get no Conform Java
formatter, so `<leader>cf` does not invent a house style.

This matches Zed's "one owner per language" rule: the Maven module is the
owner. The same spec is copied onto Omarchy and linked on macOS, so both
platforms run the same Maven goal against the same POM.

Relative line numbers remain enabled because that matches the reference
Omarchy setup and supports movement-oriented editing.

## Omarchy owns the current theme

On startup, `plugins/theme.lua` checks:

```text
~/.local/state/omarchy/current/theme/neovim.lua
```

When readable, that file supplies the complete Lazy plugin specification for
the active Omarchy theme. Dotbento does not translate theme names or duplicate
Omarchy's palette.

Outside Omarchy, the same loader returns an Aether specification with the
bundled Gruvy Glass palette.

## Why theme changes require a restart

An earlier design preloaded every supported colorscheme and watched Omarchy's
theme state. That supported live switching, but it required a custom reload
pipeline and many otherwise unused plugins.

The current design reads the theme once during startup. After
`omarchy theme set`, restart Neovim. Lazy can install the newly referenced
colorscheme if needed.

This trades a rare restart for a much smaller plugin and maintenance surface.

## Semantic italics survive colorscheme application

Colorschemes own highlight groups and may replace them when loaded. Dotbento
therefore applies its italic convention:

- once during config loading;
- after `ColorScheme`;
- after LazyVim's `VeryLazy` event.

The helper reads each existing highlight first and changes only `italic`. It
preserves foreground colors and other theme attributes.

## Transparency belongs to the terminal

The transparency plugin removes backgrounds from core windows, floating
windows, menus, line-number areas, and WhichKey. It does not define an
independent opacity value.

The active terminal remains the owner of actual background opacity and blur:
Ghostty on macOS, and Omarchy's selected terminal on Linux. Neovim only allows
that surface to show through.

## Why remote clipboard handling is custom

Local graphical Neovim sessions use the built-in clipboard provider. The custom
provider activates only under tmux, SSH, or herdr.

Copies take two paths when possible:

1. Write to the local OS clipboard using `wl-copy` or `pbcopy`.
2. Emit OSC 52 so tmux or the visible terminal can forward the text.

Pastes prefer `wl-paste` or `pbpaste`. Without a local display clipboard, they
fall back to an OSC 52 query.

This dual path preserves both directions of work. An explicit clipboard copy can reach the
laptop when forwarding is enabled; ordinary yanks depend on `clipboard`.

Linux and macOS use different process APIs when detecting a herdr ancestor.
Linux reads `/proc`; macOS queries `ps`. That small runtime branch avoids a
second configuration tree.

## Omarchy and macOS install differently

macOS receives a symlink at `~/.config/nvim`, or the configured XDG equivalent.
Live edits therefore remain repository edits.

Omarchy receives a copy because its package tooling owns and may replace the
Neovim config directory. Identical copies are skipped. After an Omarchy refresh,
run Dotbento again to restore this configuration.

## Verification

The headless startup check uses the repository as `XDG_CONFIG_HOME`:

```bash
XDG_CONFIG_HOME="$PWD" nvim --headless +qa
```

A stricter parity check should compare every resolved Lazy plugin with a
matching `lazy-lock.json` entry.

## Related

- [Bootstrap ownership](bootstrap.md#why-neovim-is-copied-on-omarchy)
- [Visual system](visual-system.md)
- [Ghostty clipboard policy](ghostty.md#clipboard-and-selection)

## Working alongside Pi

Space is `<leader>`. These keys were checked against installed LazyVim commit
`999700997f72227187d49d8b92667183dc7fc809`, matching our lockfile:

| Key | Action |
| --- | --- |
| Space `gd` | Snacks Git diff picker (hunks) |
| Space `ghp` | Preview hunk inline (Gitsigns, after attaching to a file) |
| Space `ghs` | Stage hunk; Visual mode stages the selected range |
| Space `gg` / `gG` | LazyGit at Git root / current directory |
| Space `ft` / `fT` | Terminal at detected project root / current directory |
| Ctrl-/ | Focus root terminal; terminal-local mapping hides it |
| Esc Esc | Leave terminal input mode |
| Space `yp` | Copy current file path and cursor line to clipboard |
| Visual, Space `ys` | Copy selected buffer text as a fenced Markdown snippet |

LazyGit mappings are absent when `lazygit` is missing at startup. Install it
separately and restart, or use `git diff`, `git add -p`, and `git commit` in a
terminal. No existing review mappings were changed. The new keys have descriptive
which-key labels and no matching keys in the local config or pinned defaults.

Practice this loop:

1. Save the relevant buffers with `:w`. Check `:pwd` and the file you are editing.
2. Open Space `ft`. Run `pwd`, `git rev-parse --show-toplevel`, and
   `git status --short --branch`. LazyVim's project root may come from an LSP;
   verify the actual worktree before starting `pi`. Use Space `fT` after
   `:cd /your/worktree` when you want an explicit directory. Verify reused
   terminals too: their shell may have changed directory.
3. Give Pi a bounded task. Avoid editing the same files concurrently.
4. Return to Neovim, run `:checktime`, then Space `gd` and Space `ghp` to review.
   In a multi-repository session, confirm the picker's directory; use a terminal
   in the verified worktree for `git diff` if uncertain.
5. Run the project's documented checks in that terminal. Stage selected hunks
   with Space `ghs` or `git add -p`; inspect `git diff --cached` before committing.

If an agent changes a file with unsaved editor changes, do not blindly write or
use `:edit!`. Preserve your buffer with `:write /tmp/my-buffer-backup`, compare
it against disk, then reconcile deliberately. `:edit!` discards buffer edits;
use it only after preserving or intentionally abandoning them. LazyVim runs
`checktime` on FocusGained, TermClose, and TermLeave. Those events are not a lock,
merge mechanism, or protection against every concurrent edit.

### Copying context

Space `yp` produces `src/app.ts#L42`. Visual Space `ys` adds that location above
a Markdown fence, lengthened when the selection contains backticks. Character,
line, and block selections use Neovim's selection extraction, including the
`selection` option. Neither helper saves, moves the cursor, yanks into numbered
registers, or sends anything to Pi. The clipboard register is intentionally
replaced. Paste into your agent only when ready.

Paths are resolved from the file, not the editor directory. Symlinks identify
their physical target; nested repositories and worktrees use their own Git root.
The notification identifies that root. Outside Git or without Git, the fallback
is an absolute path; unnamed buffers use `[unnamed buffer]`. New files use their
resolved parent directory. Modified buffers copy current buffer text and line
numbers, which may differ from disk; the notification explicitly says so.

Both helpers write `+` explicitly. Locally this uses Neovim's existing provider
(`pbcopy` on macOS, normally `wl-copy` on Omarchy). Under SSH/tmux/Herdr the
custom provider also emits OSC 52 unless disabled. Ordinary yanks need not reach
that provider: LazyVim leaves `clipboard` empty under `SSH_CONNECTION`.
Forwarding depends on terminal and multiplexer support and policy.

On each machine, run `:checkhealth vim.provider`, try `:let @+ = 'clipboard test'`,
and paste into another application. Check `:let @* = 'primary test'` separately
(on Wayland this is the primary selection). Repeat through SSH, tmux, and Herdr;
OSC 52 paste queries may be unsupported even when copying works.

### Apply and verify

No installer or live configuration changes are required for repository tests:

```bash
nvim -i NONE --headless -u NONE -l tests/agent_context.lua
```

On macOS an existing Dotbento symlink picks up these edits on restart. On Omarchy,
review `./install.sh --dry-run --only=nvim`, then run `./install.sh --only=nvim`
when ready to replace the installed copy. Restart Neovim. Check `:verbose nmap
<Space>yp` and `:verbose xmap <Space>ys`, then practice both helpers and paste into
another app. Local clipboard and remote forwarding require this machine-level
check; a headless mocked provider cannot prove delivery to your desktop.
