# Stacked PR Workflow Docs

This section documents a stacked PR workflow for `frozenSkillz` and other agent-managed repositories.

The baseline is intentionally plain:

- use `git` for branch and history operations
- use `gh` for PR creation, base retargeting, comments, and merge state
- use the included PowerShell helpers for inventory and review-surface checks
- use Graphite `gt` only as an optional accelerator when it is installed and explicitly useful

Start here when you need the big-picture answer to:

- what are we building?
- why are we building it this way?
- which doc or workflow should be read next?

## Reading Order

1. [architecture.md](architecture.md)
   Read this first for the overall model: what belongs in the skill, what belongs in docs, what belongs in helper scripts, and where optional Graphite tooling fits.

2. [scenario-router.md](scenario-router.md)
   Read this next when you have a real repo problem and need to route quickly to the right workflow.

3. [helper-scripts.md](helper-scripts.md)
   Read this when you want to understand what the helper scripts do and how they support stack repair without requiring Graphite.

4. [optional-graphite-models.md](optional-graphite-models.md)
   Read this when the question is "what does Graphite actually do?" or "why doesn't a flattened PR graph automatically become a stack?"

5. [forward-space.md](forward-space.md)
   Read this for the state machine, timeline, and forward process from messy Git reality to a clean review stack.

## Skill Entry Point

The reusable skill lives at:

- [plugins/frozen-skills/skills/stacked-pr-workflow/SKILL.md](../../plugins/frozen-skills/skills/stacked-pr-workflow/SKILL.md)

That skill is the operator-facing playbook.

These docs are the design notes and routing layer around it.
