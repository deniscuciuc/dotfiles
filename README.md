# Ubuntu workstation dotfiles

Portable configuration for Bash, Git, Starship, Kitty, VS Code, Claude/Codex and rootless Podman, managed with [chezmoi](https://www.chezmoi.io/). Software installation belongs to [ws-setup](https://github.com/deniscuciuc/ws-setup).

`ws-ssh-agent` runs a command with Bitwarden Desktop's Snap SSH agent, without replacing the parent terminal's agent. Use `ws-ssh-agent ssh HOST` after enabling the agent in Bitwarden. CLI installation, Windows key migration and recovery steps live in the [workstation SSH guide](https://github.com/deniscuciuc/ws-setup/blob/main/docs/SSH_MIGRATION.md). Private keys, vault sessions and host configuration stay outside this repository.

## Install

`ws-storage` reports pnpm/filesystem sharing, worktrees and disk usage. `ws-maintenance` supplies low-space/backup checks for ws-setup's user timers. Their schedules, exclusions and controls are documented in [storage and maintenance](https://github.com/deniscuciuc/ws-setup/blob/main/docs/MAINTENANCE.md).

Read the [Workstation Handbook](https://github.com/deniscuciuc/ws-setup/blob/main/docs/handbook/README.md) for the purpose and daily use of the installed tools, configuration locations, maintenance and troubleshooting. This repository's [terminal guide](docs/TERMINAL.md) and [backup guide](docs/BACKUP.md) describe the user configuration it owns.

Use the workstation installer so the required commands exist first:

```bash
bash /path/to/ws-setup/setup.sh --dotfiles-source /path/to/dotfiles
```

The source can contain your candidate changes. Setup renders templates, backs up affected files, preserves the existing `.bashrc`/`.profile` through small managed includes, and records which source you selected. Restart your login session afterwards.

```bash
ws-dotfiles diff       # Review source → home changes
ws-dotfiles apply      # Apply intentionally
ws-dotfiles status
ws-dotfiles edit ~/.config/starship.toml
```

`ws-dotfiles` uses the source remembered by the installer. There are no automatic commits/pushes. Review before using `chezmoi add` on private application directories: credentials and personal histories must never enter Git.

## Configuration and ownership

| Area | Managed behavior |
|---|---|
| Bash | Interactive suggestions/highlighting, completion, history search, zoxide and explicit aliases |
| Login/desktop environment | User tools on PATH and a rootless Podman socket endpoint |
| Git | Existing identity, main branch, rebase pulls, prune and delta; private override include |
| Kitty | Existing color theme, JetBrainsMono Nerd Font and practical shortcuts; Ubuntu's default terminal stays default |
| VS Code | Bash login terminal, Python/web formatting, container paths, reduced dependency watchers |
| mise | Node 24.18.0 baseline; per-project overrides supported |
| Claude/Codex | Small portable defaults; normal permission prompts and no credentials/model pins |
| Backups | Explicit Restic commands with home-relative targets and an external-disk check |

Read [terminal shortcuts](docs/TERMINAL.md) and [backup setup](docs/BACKUP.md).

## Private overrides

Create only what you need; none of these files is tracked:

- `~/.config/shell/local.sh` — environment overrides.
- `~/.config/bash/local.bash` — interactive aliases.
- `~/.gitconfig.local` — Git identity/credential overrides.
- `~/.config/workstation/backup.conf` — backup disk/repository settings.

Do not store API keys, `.ssh` private keys, GPG keys, cloud credentials, browser profiles or account tokens in this repository. AI configuration and history can be retained in the **encrypted external backup**, not Git. Reapplying managed VS Code/AI settings restores the source version; back up personal changes or edit the source deliberately.

Neovim and legacy Zsh configuration have been retired from the managed source. Setup leaves any existing personal files on disk. `.chezmoiignore` prevents documentation and tests from appearing in your home directory.

## Test

```bash
python3 tests/test_dotfiles.py
```

For the actual chezmoi application, prompt, backup restore and full workstation tests, follow ws-setup's `docs/TESTING.md`. Candidates are not migration-certified until the Ubuntu desktop and physical-PC checks pass.

Starship allows runtime commands up to 5 seconds for mise first-use initialization. The managed mise setting `node.corepack = true` enables pnpm/yarn launchers when new project Node versions are installed. For a Node version installed before this setting, run `mise exec node@VERSION -- corepack enable` followed by `mise reshim`. Corepack keeps using each project’s `packageManager` version.
