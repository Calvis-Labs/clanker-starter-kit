---
description: Spin up another Claude agent in a new iTerm split pane, working on its own isolated worktree — so you can build several features at once without collisions.
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
---

The user wants to build **$ARGUMENTS** in parallel with their current work, in a separate agent. Each parallel agent gets its own git worktree (separate checkout + branch), which is exactly what makes running many at once safe.

## Steps

1. **Derive a feature id** — a short kebab-case slug for the branch/worktree (e.g. `dark-mode`, `csv-export`). If `$ARGUMENTS` is empty, ask what feature the new agent should take on.

2. **Craft the new agent's opening instruction.** The new pane starts already inside the worktree, so it must NOT create another one. Something like:
   > You're in a dedicated worktree on branch `<branch>` for: **<feature>**. Implement it here, run the tests, then `/review` and `/ship`. Don't create another worktree — this one is yours.

3. **Spawn it:**
   ```bash
   .claude/scripts/spawn-agent.sh <feature-id> "<opening instruction>"
   ```
   The script creates the worktree (if needed), splits the current iTerm pane vertically, and launches `claude` there with the instruction. If not running in iTerm, it prints the exact command for the user to run in a new pane themselves.

4. **Report back** — tell the user a new agent is now working on `<feature>` in the split pane on its own branch, and that this session is free to keep doing what it was doing. Remind them, briefly, that the two agents are isolated and won't interfere.

## Safety

- **One agent per worktree, always.** Never point two agents at the same directory or branch — that's the only way they'd clash. The script enforces a unique worktree per feature id.
- When a parallel feature is merged, clean it up with the `worktree-cleaner` agent.
