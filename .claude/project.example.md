# Project configuration

<!--
  This is the TEMPLATE. The real config lives at `.claude/project.md` inside
  YOUR project, and is written automatically by `/setup`. Every command in this
  kit reads it to know your tracker, your test command, and your branch names —
  so the dev loop works without hardcoding anything.

  You can edit it by hand any time, or re-run `/setup` to regenerate it.
-->

## Project

- **name:** my-app
- **what it does:** one-line description
- **root:** /Users/you/projects/my-app

## Stack

<!-- auto-detected by /setup from the files in the repo -->
- **detected:** react-typescript        # e.g. python-django, swift-ios, kotlin-android, go, rust, node
- **build_command:** npm run build
- **test_command:** npm test
- **lint_command:** npm run lint

## Git

- **default_branch:** main               # auto-detected; the branch new task branches are based on
- **pr_base:**                            # optional; PR target branch if different from default_branch (e.g. develop)
- **branch_prefix:** feature/            # task branches become feature/<issue-id>
- **worktree_dir:** ../                   # where isolated worktrees are created

## Tracker

<!-- one of: linear | github | none -->
- **type:** github
- **linear_team_id:**                     # only when type is linear (UUID from /setup)
- **github_repo:** you/my-app             # only when type is github (owner/repo)

## Install

- **scope:** global                       # global = toolkit lives in ~/.claude; local = lives in this project
