---
description: Open a pull request for the current branch — stack-aware PR body, correct base branch, never mentioning AI authorship.
allowed-tools: Bash, Read, Glob, Grep, Task, AskUserQuestion
---

Open a PR for the current branch.

Read `.claude/project.md` for the default branch and tracker. Then delegate to the **`pr-creator`** agent, which will:

1. Confirm the branch is pushed (`git push -u origin <branch>` if not).
2. Determine the base branch (the repo's default branch, from config / `origin/HEAD`).
3. Analyze the diff and build a stack-appropriate PR title and body (summary, changes, test plan, validation, notes) — **written as a human**, with no mention of AI, Claude, or co-authorship.
4. Run a final sanity pass (build/lint clean, no debug prints/logs left behind).
5. Open the PR with `gh pr create --base <default> --title "..." --body "..."` and link the tracker issue if one exists.

Before opening, show the user the title and body for a quick confirm. After opening, hand back the PR URL and suggest the **`worktree-cleaner`** agent once it's merged.
