---
name: Codex-md-enhancer
description: Analyzes, generates, and improves AGENTS.md files for Codex-style workflows. Prefer a thin root AGENTS.md that captures durable agent-only context, points to docs as the source of truth, and uses nested AGENTS.md files only where local behavior truly differs.
---

# Codex AGENTS.md Enhancer

This skill rewrites or improves `AGENTS.md` files to match current best practice for agent context files.

The default target is not a giant repo encyclopedia. The default target is a short, durable, navigational file that helps an agent start correctly and find the real documentation.

## Core Standard

Treat `AGENTS.md` as an agent-facing entrypoint, not as the full documentation system.

### Root `AGENTS.md` should usually be:

- Short: usually 40-120 lines
- Durable: avoid volatile status dumps, issue counts, or branch-specific notes
- Navigational: point to canonical docs, indexes, and local entrypoints
- Operational: include invariants and "ask first" boundaries
- Specific: capture repo context the agent cannot reliably infer from code alone

### Root `AGENTS.md` should usually NOT be:

- A duplicate of `README.md`
- A full architecture manual
- A giant style guide
- A status dashboard
- A dumping ground for every workflow in the repo

### Put long-form detail elsewhere:

- `docs/` for architecture, plans, references, and history
- nested `AGENTS.md` files for directory-local behavior that truly differs
- normal project files (`README.md`, `CONTRIBUTING.md`, `docs/INDEX.md`) for human-oriented documentation

## What Good Looks Like

A strong root `AGENTS.md` usually contains only these things:

1. Purpose or one-line framing
2. Read order or canonical anchors
3. Source-of-truth / precedence rules
4. A few critical working rules
5. "Ask first" boundaries for risky changes
6. Links to deeper docs

If the repo has a true direction document, the root file should usually foreground it. In many repos this is a `NORTH_STAR.md`, `north-star.md`, or equivalent product-intent file.

## Canonical Docs To Prefer

When a repo has durable documentation, root `AGENTS.md` should usually point to canonical docs in roughly this order:

1. Direction / intent
  - `docs/NORTH_STAR.md`
  - `docs/north-star.md`
  - `docs/NorthStar.md`
  - equivalent product-intent or mission document
2. Architecture
  - `docs/ARCHITECTURE.md`
  - `docs/architecture.md`
  - equivalent technical overview
3. Navigation
  - `docs/INDEX.md`
  - `docs/README.md`
  - equivalent corpus index
4. Current priorities
  - `TODO.md`
  - `docs/TODO.md`
  - `docs/ROADMAP.md`
  - equivalent active-work tracker
5. Planning documents for substantial work
  - `PLANS.md`
  - `docs/plans/`
  - equivalent execution-plan or design-plan docs

If a section does not help the agent start faster or avoid a mistake, it probably does not belong in root `AGENTS.md`.

## Default Workflow

### 1. Inspect before writing

Before proposing changes:

- Read the current `AGENTS.md` if it exists
- Read the root `README.md`
- Read any docs index or canonical anchors such as `docs/INDEX.md`, `docs/README.md`, `docs/NORTH_STAR.md`, `docs/ARCHITECTURE.md`
- Read current priorities such as `TODO.md`, `docs/TODO.md`, `docs/ROADMAP.md`, or equivalent
- Check whether the repo uses `PLANS.md`, execution plans, or a `docs/plans/` workflow
- Check whether nested `AGENTS.md` files already exist
- Identify what information is durable versus volatile

Do not infer repo conventions without checking.

### 2. Classify the current file

Classify the existing `AGENTS.md` into one of these shapes:

- Thin entrypoint
- Good but overloaded
- Duplicate of other docs
- Missing critical agent-only context
- Needs hierarchy via nested files

### 3. Improve toward the thin-root model

When editing:

- Keep the root file concise
- Replace duplicated detail with links
- Preserve real agent-only constraints
- Foreground the repo's direction document if one exists
- Add explicit read order where needed
- Add canonical precedence where docs can conflict
- Prefer a documentation/planning workflow when the repo uses one
- Do not include a long command catalog in root `AGENTS.md`

### 4. Handle commands conservatively

Commands are optional in root `AGENTS.md`.

Use this rule:

- If the repo has a canonical command reference in `README.md`, `docs/`, `package.json`, `Makefile`, `justfile`, CI, or tool metadata, prefer linking to that source instead of duplicating commands in root `AGENTS.md`
- Only include commands in root `AGENTS.md` when they are short, stable, and high-value for verification or startup
- If command usage is volatile or extensive, move it to docs and link there

### 5. Use nested `AGENTS.md` files carefully

Add nested `AGENTS.md` files only when:

- a subdirectory has a distinct workflow
- local commands or invariants differ materially
- there is enough complexity to justify local instructions

Do not create a tree of `AGENTS.md` files just because the repo has many folders.

## Evaluation Criteria

Use these questions when analyzing a file:

### Signal

- Does it contain information the agent actually needs?
- Does it avoid repeating what code or docs already say clearly?

### Navigation

- Does it point to the right source documents?
- Is there an explicit read order for high-risk or high-context work?
- Does it foreground the repo's true direction document, such as `NORTH_STAR.md`, when one exists?

### Durability

- Will this still be correct next month?
- Are volatile details pushed into docs, plans, or status files instead?

### Scope

- Is root `AGENTS.md` acting like a table of contents plus working contract?
- Or is it trying to be the entire documentation system?

### Locality

- Are nested `AGENTS.md` files used only where local behavior differs?

### Planning

- Does the file explain when to consult planning docs for substantial work?
- If the repo uses `PLANS.md` or `docs/plans/`, does root `AGENTS.md` route the agent there?

## Recommended Output Shapes

### Shape A: Thin Root Entrypoint

Use this by default.

```markdown
# AGENT ENTRYPOINT

Read these first:
1. `docs/NORTH_STAR.md`
2. `docs/ARCHITECTURE.md`
3. `docs/INDEX.md`

If guidance conflicts, use:
1. `docs/NORTH_STAR.md`
2. `docs/ARCHITECTURE.md`
3. this file

Working rules:
- Use `uv run` for Python commands.
- Run tests before declaring work complete.
- Do not change schema files without approval.

Ask first:
- schema changes
- destructive data cleanup
```

### Shape B: Thin Root Plus Nested Local Files

Use when the repo has genuinely distinct subsystems.

Root file:

- points to canonical docs
- explains precedence
- links to nested `AGENTS.md` files

Nested file:

- only covers local commands, invariants, and pitfalls for that subtree

## Anti-Patterns

Avoid these:

- Long project histories in root `AGENTS.md`
- Repeating full architecture explanations already present in `docs/`
- Storing fast-changing branch, PR, or issue status in root `AGENTS.md`
- Adding broad generic advice like "write clean code" or "use best practices"
- Creating many nested `AGENTS.md` files without clear local need
- Large command catalogs copied from README, CI, or package metadata

## Documentation And Planning Workflow

If the repo has a documentation system, root `AGENTS.md` should usually encode a simple workflow for consulting it.

Example workflow:

1. Read the direction document first (`NORTH_STAR.md` or equivalent)
2. Read architecture second
3. Read the docs index or docs README for corpus navigation
4. Read current priorities (`TODO`, `ROADMAP`, active tracker)
5. For substantial features or refactors, consult `PLANS.md` or `docs/plans/` before implementation

This is especially useful for repositories that separate:

- durable product intent
- durable technical architecture
- current priorities
- execution plans
- historical notes

If the repo uses planning shorthand such as `ExecPlan` or a `PLANS.md` contract, preserve that terminology rather than replacing it with generic wording.

## How To Use

### Analyze an existing file

Prompt pattern:

```text
Use the Codex-md-enhancer skill to review this repo's AGENTS.md against current thin-root best practice. Tell me what should stay, what should move to docs, and what should be cut.
```

Expected output:

- current file shape
- top problems
- recommended target structure
- minimal rewrite plan

### Rewrite an existing file

Prompt pattern:

```text
Use the Codex-md-enhancer skill to rewrite this repo's AGENTS.md into a thin agent entrypoint. Keep durable agent-only context, add read order and precedence, and move duplicated detail behind links.
```

### Create a new file

Prompt pattern:

```text
Use the Codex-md-enhancer skill to create a root AGENTS.md for this repo. Keep it concise and navigational. Assume docs are the source of truth and only include agent-specific constraints, commands, and read order.
```

### Consider nested files

Prompt pattern:

```text
Use the Codex-md-enhancer skill to decide whether this repo needs nested AGENTS.md files. Only recommend them where local behavior clearly differs.
```

## When To Escalate

Ask the user before:

- rolling out many nested `AGENTS.md` files
- moving large amounts of text out of existing docs
- deleting or replacing large instruction corpora
- changing a repo's documented precedence model

## Practical Editing Rules

When applying edits:

- Prefer the smallest rewrite that clarifies the contract
- Preserve working read-order and precedence rules
- Preserve real constraints and approval boundaries
- Preserve or improve the repo's documentation/planning workflow if it exists
- Cut generic filler
- Convert long sections into links to canonical docs
- Do not claim a root file should be comprehensive by default
- Prefer linking to canonical command docs over copying long command lists into root `AGENTS.md`

## Compatibility Notes

This skill is for Codex-style `AGENTS.md` workflows, but the same thin-root pattern is also compatible with other tools that read repo-local instruction files.

Nested files are useful. Massive root files are usually not.

## Version

Version: 2.0.0
Last Updated: 2026-04-01
