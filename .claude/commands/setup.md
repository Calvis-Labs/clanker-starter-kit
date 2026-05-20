---
description: First-run setup — pick where the toolkit lives, connect a task tracker, detect the stack, and write the project config the dev loop reads.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, AskUserQuestion, mcp__linear__list_teams, mcp__linear__get_team
---

You are setting up the Claude dev loop for this person's machine and project. When you finish, `/plan`, `/start-ticket`, `/review`, and `/ship` all work end-to-end. Go one step at a time and keep the recipient oriented — they may be technical or may have opened a terminal for the first time this week. Match your tone to the `CLAUDE.md` track that's active.

Do everything yourself. Never make the recipient type git/gh/config commands by hand unless they explicitly want to.

## Step 1 — Where should the toolkit live?

The commands and agents currently sit in **this folder's** `.claude/`. That means they only work while Claude runs from here. Decide with the recipient where they should live:

Use `AskUserQuestion`:
- **Install globally (recommended)** — copy `.claude/commands`, `.claude/agents`, `.claude/hooks`, and `.claude/settings.json` into `~/.claude/`. After this, `/plan`, `/start-ticket`, etc. work in **every** project they ever open. Best if they'll build more than one thing.
- **Keep it local** — copy `.claude/` (commands, agents, hooks, settings, `project.example.md`) **into the project folder you identify in Step 2**, so the loop works in that one project. Simplest and fully contained, but unavailable in their other projects.

**Order note:** a global install can happen now; a local install needs the project folder first, so do it right after Step 2. Either way, don't overwrite an existing `<name>.md` without asking (if a name collides, tell them and skip or rename), make the copied `hooks/approve-readonly.py` executable, and confirm what landed where.

Record the choice as `scope:` in the project config (Step 5).

## Step 2 — Which project are we wiring up?

Find out what they're building and where the code lives.

- If they already have a project folder/repo, `cd` there.
- If they don't have one yet (common for non-technical folks who just said "I want to build X"), help them create it: `~/projects/<name>`, then `git init`. Explain in one line that git is the tool that tracks versions of their work so nothing is ever lost.
- If the folder isn't a git repo, run `git init` (with a one-line plain-English why).

This project's folder is where you'll write `.claude/project.md` in Step 5.

## Step 3 — Detect the stack

Look at the project files and infer the stack and the right commands. Don't ask if you can tell:

| Signal | Stack | build / test (typical) |
|---|---|---|
| `package.json` | node / react-ts | `npm run build` / `npm test` (read scripts to confirm) |
| `pyproject.toml`, `requirements.txt`, `manage.py` | python / django | (per project) / `pytest` |
| `*.xcodeproj`, `Package.swift` | swift-ios | xcodebuild / `swift test` |
| `build.gradle`, `build.gradle.kts` | kotlin-android | `./gradlew build` / `./gradlew test` |
| `go.mod` | go | `go build ./...` / `go test ./...` |
| `Cargo.toml` | rust | `cargo build` / `cargo test` |

Read the actual scripts/manifest to get exact commands rather than guessing. If it's a brand-new empty folder, leave the commands blank and note the stack as `unknown` — they'll fill in once there's code.

## Step 4 — Connect a task tracker

Ask what they use, with `AskUserQuestion`:
- **Linear** — help them connect it (see below). Suggest this if they have no tracker and leave the choice to you.
- **GitHub Issues** — needs the `gh` CLI authenticated.
- **None / git-only** — zero setup; task IDs live in branch and commit names. Always works.

The loop must work day-one regardless, so **default to git-only and upgrade** once auth succeeds. Don't block setup on a tracker.

**GitHub Issues:** check `gh auth status`. If not authed, walk them through `gh auth login` (tell them to run it themselves with `! gh auth login` since it's interactive). Capture `owner/repo` from `gh repo view --json nameWithOwner -q .nameWithOwner` (or ask if there's no remote yet).

**Linear:** the Linear MCP must be connected in their Claude Code. If `mcp__linear__list_teams` works, list their teams and have them pick one; store the team's UUID. If the tool isn't available, explain Linear isn't connected yet, point them to add the Linear MCP server, and fall back to git-only for now — they can re-run `/setup` later.

## Step 5 — Write the config

Write `.claude/project.md` **in the project folder** (Step 2), using `.claude/project.example.md` from this kit as the shape. Fill in: name, what it does, root, detected stack + commands, default branch (`git symbolic-ref refs/remotes/origin/HEAD` or current branch for a fresh repo), branch prefix (`feature/`), tracker type + IDs, and install scope.

## Step 6 — Confirm it works

Summarize in plain English what you set up: where the toolkit lives, what tracker is connected, the test/build commands, the default branch. Then tell them the loop is ready and what to type next:

> Setup's done. Here's your loop: **`/plan`** to think through a feature, **`/start-ticket`** to build it on an isolated branch, **`/review`** to check the work, **`/ship`** to open the PR. Try `/plan <something you want to build>` when you're ready.

Don't run a feature now unless they ask.
