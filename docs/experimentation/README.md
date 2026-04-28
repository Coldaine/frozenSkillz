# Graphite Replica Docs

This section documents the Graphite-style stacked PR workflow we are building into `frozenSkillz`.

The key point is simple:

- this is **not** a wrapper that assumes Graphite is installed
- this is a **replica of the Graphite workflow shape**
- the skill and helper scripts should let an agent diagnose the repo state, choose the right repair path, and perform as much of the stack-management work as possible with normal `git`, `gh`, and PowerShell
- if `gt` is installed, it becomes an optional accelerator rather than a dependency

Start here when you need the big-picture answer to:

- what are we building?
- why are we building it this way?
- which doc or workflow do I read next?

## Reading Order

1. [graphite-replica-architecture.md](graphite-replica-architecture.md)
   Read this first for the overall model: what belongs in the skill, what belongs in docs, what belongs in helper scripts, and where optional Graphite tooling fits.

2. [graphite-scenario-router.md](graphite-scenario-router.md)
   Read this next when you have a real repo problem and need to route quickly to the right workflow.

3. [graphite-helper-scripts.md](graphite-helper-scripts.md)
   Read this when you want to understand what the helper scripts do and how they replace or approximate parts of the Graphite workflow.

4. [graphite-visual-models.md](graphite-visual-models.md)
   Read this when the question is "what does Graphite actually do?" or "why doesn't a flattened PR graph magically become a stack?"

5. [graphite-stacked-pr-forward-space.md](graphite-stacked-pr-forward-space.md)
   Read this for the state machine, timeline, and the forward process from messy Git reality to a clean review stack.

## Skill Entry Point

The reusable skill lives at:

- [plugins/frozen-skills/skills/graphite-stacked-pr-workflow/SKILL.md](../../plugins/frozen-skills/skills/graphite-stacked-pr-workflow/SKILL.md)

That skill is the operator-facing playbook.

These docs are the design notes and routing layer around it.
