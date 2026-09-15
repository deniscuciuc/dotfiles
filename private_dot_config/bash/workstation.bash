# Interactive Bash only. Scripts and TERM=dumb remain quiet.
[[ $- == *i* ]] || return 0
[[ -z ${WS_BASH_LOADED:-} ]] || return 0
WS_BASH_LOADED=1
source "$HOME/.config/shell/environment.sh"
[[ ${TERM:-dumb} != dumb && -t 0 && -t 1 ]] || return 0

HISTSIZE=50000
HISTFILESIZE=100000
HISTCONTROL=ignoreboth:erasedups
shopt -s histappend checkwinsize
ws_history_sync() {
  history -a
  history -n
}
# Preserve other tools' prompt hooks and do not evaluate user-controlled strings.
PROMPT_COMMAND+=(ws_history_sync)
bind 'set completion-ignore-case on'
bind 'set show-all-if-ambiguous on'
bind 'set mark-symlinked-directories on'
bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'

if ! declare -F _completion_loader >/dev/null && [[ -r /usr/share/bash-completion/bash_completion ]]; then
  source /usr/share/bash-completion/bash_completion
fi
# ble.sh's documented deferred attach keeps prompt integrations in the right order.
if [[ -r $HOME/.local/share/blesh/ble.sh ]]; then source "$HOME/.local/share/blesh/ble.sh" --noattach; fi
if command -v fzf >/dev/null; then
  if [[ -n ${BLE_VERSION:-} ]]; then
    # ble.sh's integration installs the fzf widgets without competing Readline hooks.
    # Ubuntu splits fzf's shell scripts from its binary directory.
    if [[ -r /usr/share/doc/fzf/examples/key-bindings.bash ]]; then
      _ble_contrib_fzf_base=/usr/share/doc/fzf/examples
    fi
    ble-import -d integration/fzf-completion
    ble-import -d integration/fzf-key-bindings
  else
    eval "$(fzf --bash)"
  fi
fi
if command -v zoxide >/dev/null; then eval "$(zoxide init bash)"; fi
if command -v starship >/dev/null; then eval "$(starship init bash)"; fi
source "$HOME/.config/bash/aliases.bash"
if [[ -r $HOME/.config/bash/local.bash ]]; then source "$HOME/.config/bash/local.bash"; fi
if [[ -n ${BLE_VERSION:-} ]]; then ble-attach; fi
