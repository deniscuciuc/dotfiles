# Bash and terminal shortcuts

Ubuntu's terminal remains the primary terminal. Kitty and VS Code use the same Bash setup. Nano is the terminal editor; `code --wait` is the graphical editor.

| Action | Command/shortcut |
|---|---|
| Search history | Ctrl+R (fzf) |
| Search files | Ctrl+T (fzf) |
| Jump directory interactively | Alt+C (fzf), or `zi name` |
| Jump to a frequent directory | `z name` |
| Previous matching command | Type a prefix, then Up/Down |
| Accept suggestion | Right/End, using ble.sh's normal editing bindings |
| List files | `ll`, `treeview` |
| Read/search files | `bat file`, `fd name`, `rg text`, `jq . file.json` |
| Git status/diff/history | `gs`, `gd`, `gl`, `lg` |
| Create and enter a directory | `mkcd path` |
| Compose start/stop/logs | `dcu`, `dcd`, `dcl` |
| Running containers | `dps` |
| Preview/apply dotfiles | `czd`, `cza` |
| Backup/snapshots/check | `backup`, `backups`, `backupcheck` |
| Kitty split/tab in current directory | Ctrl+Shift+Enter / Ctrl+Shift+T |

Standard `cat`, `find`, `grep` and `ls` remain unchanged. The Debian names `batcat` and `fdfind` are also available; setup exposes `bat` and `fd` without replacing other commands.

Interactive helpers load only on an interactive TTY with a usable terminal type. Scripts, agent tool shells and `TERM=dumb` remain quiet. Prompt hooks preserve existing hooks; history is stored locally, without cloud history synchronization.

For a temporary clean shell, run `bash --noprofile --norc`. Permanent personal shortcuts belong in `~/.config/bash/local.bash`. A custom `~/.bash_profile` must source `~/.profile` if you want these login settings there too.
