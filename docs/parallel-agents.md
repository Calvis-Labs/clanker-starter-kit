# Building N features at once — parallel agents in split panes

You can run **several Claude agents side by side**, each building a different
feature at the same time, without them ever stepping on each other. The trick is
the same isolation the dev loop already uses: **git worktrees**.

## Why it's safe

A *worktree* is a second (third, fourth…) checkout of your repo in its own
folder, on its own branch, sharing the same history. Two agents in two worktrees
edit completely separate files on disk and separate branches — so there's no way
for one to overwrite the other's work. Each opens its own PR when it's done.

The one rule: **one agent per worktree.** Never point two agents at the same
folder or the same branch. That's the only way they'd collide, and the tooling
below is built to prevent it.

## The fast way — `/parallel`

From any agent, in iTerm:

```
/parallel add a dark mode toggle
```

That creates a fresh worktree + branch, **splits your iTerm pane**, and starts a
new Claude in the new pane already working on that feature. Your original agent
keeps doing whatever it was doing. Run it again for a third feature, a fourth,
and so on — your screen fills with independent agents, each on its own branch.

When a feature lands, ask any agent to run the `worktree-cleaner` to tidy up.

## The manual way (good to know)

iTerm split-pane shortcuts:

| Action | Shortcut |
|---|---|
| Split pane **vertically** (side by side) | `⌘` + `D` |
| Split pane **horizontally** (top/bottom) | `⌘` + `Shift` + `D` |
| Move between panes | `⌘` + `Option` + arrow keys |
| Maximize / restore the focused pane | `⌘` + `Shift` + `Enter` |

To do by hand what `/parallel` automates:

```bash
# 1. from your repo, make an isolated worktree for the new feature
git worktree add ../<repo>-<feature> -b feature/<feature>

# 2. split the iTerm pane (⌘D), then in the new pane:
cd ../<repo>-<feature>
claude
```

Now you have two agents, two branches, zero risk of collision.

## First run: the automation prompt

The very first time `/parallel` tries to open a pane, macOS asks whether iTerm
may control itself. **Click OK.** If you miss it (or clicked Don't Allow), the
split won't happen and you'll see a hint pointing you to:

**System Settings → Privacy & Security → Automation → iTerm → enable iTerm**

Turn it on and run `/parallel` again. Either way the worktree was still created,
and the command prints the exact line to run by hand in a new pane (`⌘D`), so
you're never blocked.

## A good mental model

Think of each pane as a **separate workshop**. Same blueprint (your repo's
history), separate benches (worktrees). You can walk between them, give each a
different job, and nobody knocks over anyone else's work. When a piece is
finished, it ships (a PR) and the bench gets cleared (worktree removed).
