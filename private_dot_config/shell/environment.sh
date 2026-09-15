# POSIX login environment. No commands with output and no network activity.
case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) PATH="$HOME/.local/bin:$PATH" ;; esac
case ":$PATH:" in *":$HOME/.local/share/mise/shims:"*) ;; *) PATH="$HOME/.local/share/mise/shims:$PATH" ;; esac
export PATH
export EDITOR=nano
export VISUAL='code --wait'
# An explicit per-project/remote Docker endpoint always takes precedence.
if [ -z "${DOCKER_HOST:-}" ] && [ -n "${XDG_RUNTIME_DIR:-}" ]; then
  export DOCKER_HOST="unix://$XDG_RUNTIME_DIR/podman/podman.sock"
fi
if [ -r "$HOME/.config/shell/local.sh" ]; then . "$HOME/.config/shell/local.sh"; fi
