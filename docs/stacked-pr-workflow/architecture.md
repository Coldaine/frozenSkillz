# Stacked PR Workflow Architecture

This document explains what we are building, why we are building it, and how the pieces fit together.

## Core Position

We are **not** building a skill that depends on Graphite being present.

We are building a skill that reproduces the useful parts of the stacked PR workflow:

- identify the current repo state
- choose the right stacked-PR repair or creation path
- normalize branch and PR ancestry
- verify parent-relative diffs
- keep the review surface clean and bottom-up

If `gt` exists, the skill can use it as a compatibility path.
If `gt` does not exist, nothing important should break. The core workflow should stand on ordinary `git`, `gh`, and helper scripts.

## Why This Exists

The real problem is not "how do I type Graphite commands?"

The real problem is:

- branches are messy
- PRs have the wrong bases
- changes overlap
- checkpoint-heavy work needs to converge into a readable review story
- the operator needs fast routing from "what is broken?" to "what do I do next?"

That means the skill needs more than command reference material.
It needs routing, diagnostics, and repeatable repair logic.

## System Shape

There are four layers:

### 1. External docs

Purpose:

- explain what the system is
- explain why it exists
- route the operator to the right workflow quickly
- document the state machine and decision rules

These docs are for orientation, not execution.

### 2. Skill

Purpose:

- provide the reusable operational playbook
- map repo states to specific workflows
- map tasks to commands and helper scripts
- explain how stacked PR operations work

The skill is the reusable interface the router can activate.

### 3. Helper scripts

Purpose:

- automate inventory
- check prerequisites
- audit branches and PRs
- verify parent-relative diffs
- provide safe wrappers for repeatable operations

These scripts are how we avoid hand-running the same checks over and over.

### 4. Optional Graphite tooling

Purpose:

- provide compatibility with real Graphite when someone explicitly wants it

This is optional.
It is not the foundation of the system.

## Boundary Between "Graphite" And "Replica"

Graphite itself gives you:

- stack-aware branch creation
- stack-aware PR submission
- stack-aware navigation and restacking
- a product UI and hosted state

This replica should give you:

- a way to understand the current repo state
- a way to decide the canonical stack order
- a way to repair or construct that order
- a way to validate that each PR tells one clean story

The replica is trying to preserve the workflow logic, not the full SaaS product.

## Required Outcomes

The skill/doc/script package is successful when it lets an operator answer these questions quickly:

1. What state is this repo in right now?
2. Is this a greenfield stack, a mixed branch, a broken PR graph, or stack drift?
3. What is the canonical bottom-up review order?
4. Which branch or PR should be repaired, retargeted, recreated, or closed?
5. How do I verify that each PR only contains its incremental slice?

## Packaging In This Repo

External docs:

- [README.md](README.md)
- [architecture.md](architecture.md)
- [scenario-router.md](scenario-router.md)
- [helper-scripts.md](helper-scripts.md)
- [optional-graphite-models.md](optional-graphite-models.md)
- [forward-space.md](forward-space.md)

Skill:

- [plugins/frozen-skills/skills/stacked-pr-workflow/SKILL.md](../../plugins/frozen-skills/skills/stacked-pr-workflow/SKILL.md)

Helper scripts:

- [plugins/frozen-skills/skills/stacked-pr-workflow/scripts/stack-preflight.ps1](../../plugins/frozen-skills/skills/stacked-pr-workflow/scripts/stack-preflight.ps1)
- [plugins/frozen-skills/skills/stacked-pr-workflow/scripts/stack-inventory.ps1](../../plugins/frozen-skills/skills/stacked-pr-workflow/scripts/stack-inventory.ps1)
- [plugins/frozen-skills/skills/stacked-pr-workflow/scripts/pr-base-audit.ps1](../../plugins/frozen-skills/skills/stacked-pr-workflow/scripts/pr-base-audit.ps1)
- [plugins/frozen-skills/skills/stacked-pr-workflow/scripts/verify-parent-diffs.ps1](../../plugins/frozen-skills/skills/stacked-pr-workflow/scripts/verify-parent-diffs.ps1)
- [plugins/frozen-skills/skills/stacked-pr-workflow/scripts/submit-with-graphite.ps1](../../plugins/frozen-skills/skills/stacked-pr-workflow/scripts/submit-with-graphite.ps1)

## Design Rule

If a future reader cannot tell, within a minute, which path applies to their repo and which helper to run first, the package is still under-specified.
