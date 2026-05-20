# Clanker Starter Kit

A drop-in **Claude-powered development loop**: plan a feature, build it on an
isolated branch, review it, and ship a PR — without hand-rolling any of the
machinery. Works whether you're an experienced engineer or have never opened a
terminal.

## Two ways in

- **Non-technical?** Don't read this file. Drag this folder into a Claude Desktop
  chat and follow along — it'll install everything and walk you to a working
  terminal. (`START-HERE.md` drives that.)
- **Technical?** You're in the right place. Read on.

## Quick start (technical)

1. Make sure you have [Claude Code](https://claude.com/claude-code) installed and logged in.
2. From this folder: `claude`
3. Run **`/setup`** once. It asks:
   - **Where the toolkit lives** — install to `~/.claude/` (works in *every* project you open) or keep it local to one folder.
   - **Your task tracker** — Linear, GitHub Issues, or git-only (no setup, task IDs live in branch names). Defaults to git-only so it works day one, and upgrades once you connect a tracker.
   - It auto-detects your stack and test/build commands and writes `.claude/project.md`.

## The loop

| Command | What it does |
|---|---|
| `/plan <feature>` | Parallel research → a concrete implementation plan. |
| `/start-ticket <feature \| issue-id>` | Creates a tracker issue, spins an isolated git worktree, implements, runs your tests, validates. |
| `/review [PR#]` | Stack-aware code review of the changes; triages and applies fixes. |
| `/ship` | Opens a clean PR against your default branch. |
| `/parallel <feature>` | Splits your iTerm pane and starts another agent on its own worktree — build N features at once, safely. See [docs/parallel-agents.md](docs/parallel-agents.md). |

Plus agents the commands call on their own: `planning-agent`, `ticket-creator`,
`pr-reviewer` (stack-aware), `pr-creator`, `worktree-cleaner`.

### Build several features at once

Because every task runs in its own git worktree, you can run multiple agents in
parallel without them colliding. `/parallel <feature>` splits your iTerm pane
and launches a fresh agent on a new worktree + branch; your current agent keeps
working. Full guide: [docs/parallel-agents.md](docs/parallel-agents.md).

## How it stays project-agnostic

Everything reads `.claude/project.md` (see `.claude/project.example.md` for the
shape) — your stack, test command, default branch, and tracker. There's no
hardcoding to any specific repo or org. The single `pr-reviewer` detects your
stack (JS/TS, Python, Swift, Kotlin, Go, Rust, …) and applies the matching
rubric, so it works on whatever you build.

## What's in the box

```
.claude/
├── settings.json          # permissions + the read-only auto-approve hook
├── project.example.md     # config template (/setup writes the real one)
├── hooks/approve-readonly.py
├── commands/              # setup, plan, start-ticket, review, ship
└── agents/                # planning-agent, ticket-creator, pr-reviewer, pr-creator, worktree-cleaner
```
