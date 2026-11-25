# Zed

Zed starts in Vim Normal mode with relative line numbers, smart-case search,
system clipboard integration, and a which-key menu for pending shortcuts.
Space is the LazyVim leader.

| Keys | Action |
|---|---|
| `Space Space`, `Space f f` | Find files |
| `Space /`, `Space s g` | Project search |
| `Space e`, `Space ,`, `Space b d` | File tree, tab picker, close tab |
| `[b` / `]b`, `Shift+H` / `Shift+L` | Previous / next tab |
| `Ctrl+h/j/l`, `Ctrl+w k` | Focus the pane left, down, right, or up |
| `gd`, `gr`, `K` | Definition, references, hover |
| `Space c a`, `Space c r`, `Space c f` | Code actions, rename, format |
| `[d` / `]d`, `Space s d` | Navigate diagnostics, open project diagnostics |
| `Space g s`, `[h` / `]h` | Git panel, previous / next hunk |
| `Space f t`, `Esc Esc` in the terminal | Toggle the terminal, toggle terminal Vi navigation |
| `Space m p`, `Space y p` | Open Markdown preview, copy file location |
| `Space j` | Jump to a visible word using Zed's labeled motion |

`Ctrl+K` remains a prefix for the Agent Panel and terminal shortcuts. Follow
it with `a` to focus the agent, `t` for the terminal, `c` for the context
menu, `s` to add a selection to the thread, or `n` for a new thread.
`Alt+Shift+F` also runs the formatter.

## Formatting and language servers

Autosave runs on focus change. Formatting and safe Oxlint fixes run on an
explicit format command. Projects can opt into formatting on save in
`.zed/settings.json`.

Zed installs the Oxc extension and selects its named Oxfmt server for JS, TS,
JSON, and JSONC. For JS and TS, vtsls provides language intelligence and
Oxlint provides diagnostics and safe fixes. CSS, SCSS, HTML, and Markdown
use the `prettier` executable on Zed's project PATH. Projects can override
the formatter in their Zed settings.

Java discovers its JDK from the machine or project settings. In projects that
use Maven Spotless, define a project task for the module's `spotless:apply`
goal so the build controls the format. The Java language server remains
available for navigation and diagnostics.

## Installing

Run `./install.sh --only=zed` to merge the tracked settings and keybindings
into the local Zed config. Existing settings outside the managed keys,
including MCP credentials, SSH connections, Java paths, and the selected
theme, stay in the local file. Omazed can continue to generate its theme on
Omarchy. A fresh install uses Catppuccin Mocha. Operator Mono Lig requires a
local font installation.

On a changed install, Dotbento saves private, timestamped backups of existing
files and writes JSON that Zed can read. The backups retain any JSONC comments.
Use `./install.sh --dry-run --only=zed` to preview the operation.
