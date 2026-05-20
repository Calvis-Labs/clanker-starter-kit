---
description: Open a pull request for the current branch — stack-aware PR body, configurable base branch, never mentioning AI authorship.
allowed-tools: Bash, Read, Glob, Grep, Task, AskUserQuestion
---

Open a PR for the current branch. If `$ARGUMENTS` names a base branch (e.g. `/ship develop`), target that.

Read `.claude/project.md` for the tracker and the base branch. Resolve the **base branch** in this order: `$ARGUMENTS` → `pr_base` in `.claude/project.md` → the repo's default branch (`origin/HEAD`).

## Prerequisites — check before doing anything
Surface a clear, friendly message and stop (don't produce a cryptic failure) if:
- **`gh` not authenticated** (`gh auth status` fails) → tell them to run `gh auth login`.
- **No remote `origin`** (`git remote get-url origin` fails) → explain how to add one, or offer git-only.
- **A PR already exists** for this branch (`gh pr list --head <branch>`) → show its URL and ask whether to update it instead of opening a new one.

## Then delegate to the `pr-creator` agent
Pass it the resolved **base branch**. It will:

1. Push the branch (`git push -u origin <branch>`) if needed. If the push is rejected (protected branch, no permission), report exactly why and stop.
2. Analyze the diff and build a stack-appropriate PR title and body (summary, changes, test plan, validation, notes) — **written as a human**, no mention of AI, Claude, or co-authorship.
3. Run a final sanity pass (build/lint clean, no debug prints/logs left). **On failure:** if the project has no build/lint configured, skip it; if a check fails, show the user what failed and ask "open the PR anyway?" before continuing — never silently ship a broken build.
4. Open the PR: `gh pr create --base <base> --title "..." --body "..."`, and link the tracker issue if one exists.

Before opening, show the user the title and body for a quick confirm. After opening, hand back the PR URL and suggest the **`worktree-cleaner`** agent once it's merged.
