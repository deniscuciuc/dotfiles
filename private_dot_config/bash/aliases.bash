# Explicit conveniences; cat/find/grep/ls keep their standard behavior.
alias ..='cd ..'
alias ...='cd ../..'
alias ll='eza --long --all --group-directories-first'
alias treeview='eza --tree --level=2'
alias gs='git status --short --branch'
alias ga='git add'
alias gc='git commit'
alias gd='git diff'
alias gl='git log --oneline --graph --decorate'
alias gsw='git switch'
alias gsm='git submodule update --init --recursive'
alias lg='lazygit'
alias dc='docker compose'
alias dcu='docker compose up -d'
alias dcd='docker compose down'
alias dcl='docker compose logs --follow'
alias dps='podman ps'
alias cz='ws-dotfiles'
alias czd='ws-dotfiles diff'
alias cza='ws-dotfiles apply'
alias czs='ws-dotfiles status'
alias cze='ws-dotfiles edit'
alias backup='ws-backup backup'
alias backups='ws-backup snapshots'
alias backupcheck='ws-backup check'
mkcd() {
  [[ $# == 1 ]] || {
    printf 'Usage: mkcd directory\n' >&2
    return 2
  }
  mkdir -p -- "$1" && cd -- "$1"
}
