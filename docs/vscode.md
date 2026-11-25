# VS Code profile

The optional Dotbento profile uses VSCodeVim, a Space leader menu, Catppuccin
Mocha with Latte file icons, and Operator Mono Lig with a monospace fallback.
It keeps the file tree on the right and the terminal at the bottom. Relative
line numbers, inline Git blame, and autosave on focus change follow Zed.

[Import the profile](../README.md#vs-code) to use it alongside your other
profiles. Update the editable sources in `vscode/` and regenerate the profile
to pick up changes. Importing makes a copy of the configuration.

## Vim shortcuts

Press Space in Normal or Visual mode to open Which Key. You can also use it in
an empty editor group.

| Keys | Action |
|---|---|
| `Space Space`, `Space f f` | Find a file |
| `Space /`, `Space s g` | Search the project in a Search Editor |
| `Space e`, `Ctrl+h` from the file tree | Focus the file tree, then return to the editor |
| `Space ,`, `[b` / `]b`, `Space b d` | Pick, cycle, and close tabs |
| `gd`, `gr`, `K`, `[r` / `]r` | Definition, references, hover, previous / next occurrence |
| `Space c a`, `Space c r`, `Space c f` | Code actions, rename, format |
| `[d` / `]d`, `Space s d` | Navigate diagnostics or open Problems |
| `Space g s`, `[h` / `]h` | Source Control and Git hunks |
| `Space f t`, `Space m p`, `Space y p` | Terminal, Markdown preview, and copy the relative file path |
| `Ctrl+h/j/l`, `Ctrl+w k` | Focus left, down, right, or up |
| `Space w v`, `Space w s`, `Space w d` | Split right, split down, or close the editor group |
| `Ctrl+b` | Toggle the left dock, which VS Code calls the Secondary Side Bar |

`Ctrl+k` then `a` moves between VS Code Chat and the editor. Use
`Ctrl+k n` for a new chat, `Ctrl+k c` in chat to attach context, or
`Ctrl+k s` with an editor selection to attach it. Chat availability depends
on the VS Code distribution and account. Set up any additional agent
extensions and connections in your own profile.

Inlay hints are hidden until you hold `Ctrl+Alt` on Linux and Windows or
`Ctrl+Option` on macOS. Use VS Code's terminal Accessible View to read its
scrollback from the keyboard.

## Formatting and linting

`Space c f` or `Alt+Shift+F` formats the document explicitly. Oxfmt handles
JS, JSX, TS, TSX, JSON, and JSONC. Install `oxfmt` and `oxlint` in each Oxc
project with its package manager so the editor and CI use the same versions
and project settings. Use `Space c x` to apply safe Oxlint fixes explicitly.
CSS, SCSS, HTML, and Markdown use Prettier. Projects can override the default
formatter or opt into formatting on save.

Java uses the Red Hat language extension and the JDK configured on the
machine or in the project. For projects with Maven Spotless, run the
project's Spotless task so formatting uses the build configuration.
