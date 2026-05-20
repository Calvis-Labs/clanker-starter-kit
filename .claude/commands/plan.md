---
description: Plan a feature with parallel research before any code is written. Spawns agents to explore the codebase, assess complexity, and design an approach.
allowed-tools: Bash, Read, Glob, Grep, Task, AskUserQuestion
---

You are planning a feature: **$ARGUMENTS** (if empty, extract the feature from the conversation above — don't ask the user to repeat themselves).

Read `.claude/project.md` for stack/conventions if it exists. Then orchestrate research per the `planning-agent`. Don't write production code in this command — produce a plan.

## 1. Assess complexity
Judge whether this is SIMPLE (touches one area, well-understood) or COMPLEX (cross-cutting, new architecture, ambiguous). This sets how many research agents to spawn.

## 2. Spawn research agents in parallel
Invoke the **`planning-agent`** (via Task) — it fans out to its own sub-agents (codebase explorer, complexity assessor, design strategist, and for complex work an implementation planner + testing strategist) and returns a consolidated view. Pass it the feature description and the project root.

## 3. Consolidate and decide
From what comes back:
- **Auto-fill** the obvious choices (standard patterns, file locations, naming) — don't ask.
- **Ask the user** only the genuinely hard calls (architectural trade-offs, scope cuts, priority conflicts) via `AskUserQuestion`.

## 4. Present the plan
Lay out: the approach, the files to touch, the steps in order, the test strategy, and any risks. Keep it concrete and reviewable.

## 5. Offer to build
Once they're happy with the plan, offer to run **`/start-ticket`** with the feature summary to implement it on an isolated branch.
