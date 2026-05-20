#!/usr/bin/env bash
# Spawn a new Claude agent in a fresh iTerm split pane, working on its own
# isolated git worktree. This is what lets you build N features at once safely:
# each agent gets a separate checkout + branch, so they never collide.
#
# Usage: spawn-agent.sh <feature-id> ["initial prompt for the new agent"]
#   feature-id     short slug used for the branch + worktree dir (e.g. dark-mode)
#   initial prompt optional first message handed to the new Claude instance
set -euo pipefail

feature_id="${1:?usage: spawn-agent.sh <feature-id> [\"initial prompt\"]}"
initial_prompt="${2:-}"

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

# --- read config (best-effort; sensible defaults if project.md is absent) ---
cfg="$repo_root/.claude/project.md"
cfg_val() {
  [ -f "$cfg" ] || return 0
  grep -E "\*\*$1:\*\*" "$cfg" | head -1 | sed -E "s/.*\*\*$1:\*\*[[:space:]]*//" | tr -d '[:space:]'
}
prefix="$(cfg_val branch_prefix)";   prefix="${prefix:-feature/}"
worktree_dir="$(cfg_val worktree_dir)"; worktree_dir="${worktree_dir:-..}"

default_branch=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || true)
if [ -z "$default_branch" ]; then default_branch=$(git rev-parse --abbrev-ref HEAD); fi

branch="${prefix}${feature_id}"
wt="$(cd "$repo_root/$worktree_dir" && pwd)/$(basename "$repo_root")-${feature_id}"

# --- create the worktree if it doesn't already exist ---
if git worktree list | grep -Fq "$wt"; then
  echo "Worktree already exists: $wt"
else
  git worktree add "$wt" -b "$branch" "$default_branch"
fi

# --- build the launch command for the new pane (via a temp script to dodge
#     any quoting headaches inside AppleScript) ---
launcher=$(mktemp "${TMPDIR:-/tmp}/clanker-agent.XXXXXX")   # X's must be last (BSD mktemp)
{
  echo "#!/usr/bin/env bash"
  echo "cd $(printf '%q' "$wt")"
  if [ -n "$initial_prompt" ]; then
    echo "exec claude $(printf '%q' "$initial_prompt")"
  else
    echo "exec claude"
  fi
} > "$launcher"
chmod +x "$launcher"

# --- split the current iTerm pane and run it; fall back to instructions ---
if [ "${TERM_PROGRAM:-}" = "iTerm.app" ]; then
  osascript <<OSA
tell application "iTerm2"
  tell current session of current window
    set newSession to (split vertically with same profile)
    tell newSession to write text "bash $launcher"
  end tell
end tell
OSA
  echo "✅ Spawned agent for '$feature_id' in a new pane."
  echo "   branch:   $branch"
  echo "   worktree: $wt"
else
  echo "Not inside iTerm — open a new pane/tab yourself and run:"
  echo "   bash $launcher"
  echo "(branch: $branch, worktree: $wt)"
fi
