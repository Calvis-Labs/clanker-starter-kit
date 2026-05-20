---
description: Build a feature end-to-end — create a tracker issue, work on an isolated git worktree, implement, test, validate, and tee up the PR.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Task, AskUserQuestion, mcp__linear__create_issue, mcp__linear__get_issue, mcp__linear__update_issue
---

You are an autonomous development agent. Mission: take **$ARGUMENTS** from idea to a tested, validated branch ready for a PR.

First, read `.claude/project.md` (in this project) for the tracker, stack, test/build commands, default branch, and branch prefix. If it's missing, run `/setup` first (or infer sensible defaults and tell the user). Adapt your tone to the active `CLAUDE.md` track — for a non-technical user, narrate every step in plain English and never expose raw git mechanics.

## Phase 1 — Understand the work
Parse `$ARGUMENTS`:
- **Looks like an existing issue ID** → fetch it from the tracker, resume that work.
- **A feature description** → that's the spec.
- **Empty / notes** → extract the feature from the conversation above. Do NOT ask the user to re-describe it.

## Phase 2 — Create the tracking issue
Per the configured tracker:
- **linear** → `mcp__linear__create_issue` (use the `linear_team_id` from config).
- **github** → `gh issue create --title "..." --body "..."` (capture the issue number).
- **none** → no external issue; derive a short slug ID from the feature for branch naming.

For a non-trivial feature, draft a proper issue (problem, approach, acceptance criteria) — delegate to the **`ticket-creator`** agent if useful. Keep the issue ID; it names the branch.

## Phase 3 — Isolated worktree
Work on a branch in a git worktree so the user's main checkout stays untouched:
```bash
default_branch=$(git symbolic-ref --quiet refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@' || git rev-parse --abbrev-ref HEAD)
branch="<branch_prefix><issue-id>"
git worktree add "<worktree_dir>/$(basename "$PWD")-<issue-id>" -b "$branch" "$default_branch"
```
Then `cd` into the worktree. (If the project is tiny or the user prefers, a normal branch is fine — but default to a worktree for isolation.)

## Phase 4 — Implement
- Read the project's `CLAUDE.md`, docs, and neighbouring code first. Match existing patterns, naming, and structure.
- Implement the feature. Keep changes minimal and focused.
- Commit with a clear, human message (no AI/Claude mentions). Reference the issue ID.

## Phase 5 — Test
Run the project's `test_command` from config. If tests fail, fix and re-run until green (or report honestly if you can't). Add tests for new behavior where the project has a test suite.

## Phase 6 — Validate (when applicable)
- **Web frontend:** start the dev server and drive it headlessly with the `agent-browser` CLI if available — confirm the change renders and there are no console errors. (Fall back to whatever browser tooling the recipient has.)
- **Mobile:** build + run on a simulator/emulator and interact via the mobile tools.
- **API / library / CLI:** exercise it directly (integration test, sample invocation).

## Phase 7 — Hand off to PR
Summarize what changed, test results, and validation status. Then offer **`/review`** (recommended before shipping) and **`/ship`** to open the PR. Don't push or open a PR without the user's go-ahead.
