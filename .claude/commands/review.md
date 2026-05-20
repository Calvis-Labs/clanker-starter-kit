---
description: Review the current changes — detect which stack(s) changed and run a stack-aware code review, then triage and optionally apply fixes.
allowed-tools: Bash, Read, Glob, Grep, Task, AskUserQuestion
---

Review the work in progress (or PR **$ARGUMENTS** if a PR number/branch is given).

Read `.claude/project.md` for the default branch and stack. Then:

## 1. Find what changed
```bash
base="<default_branch from config, else origin/HEAD>"
git diff --stat "$base"...HEAD
git diff --name-only "$base"...HEAD
```
If reviewing a pushed PR, also pull existing review comments: `gh pr view <n> --comments`.

## 2. Detect the stack(s) touched
From the changed file paths, identify which stacks are involved (a change can span more than one). The **`pr-reviewer`** agent carries the per-stack rubric library.

## 3. Run the review
Invoke the **`pr-reviewer`** agent (via Task), passing the project root, the base branch, the changed files, and the detected stack(s). For a large multi-stack change, you may spawn one reviewer per stack in parallel.

## 4. Triage and act
Sort the feedback into **Fix** (real bugs, security, correctness, broken patterns) vs **Skip** (nitpicks, false positives) — show the user this split. With their go-ahead, apply the Fix items, commit, and re-validate if behavior changed. Don't auto-apply sweeping changes without confirmation.
