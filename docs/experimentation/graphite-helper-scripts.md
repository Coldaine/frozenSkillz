# Graphite Helper Scripts

This document explains the helper scripts that support the Graphite-style workflow replica.

These are not just convenience wrappers.
They are part of the workflow package.

Their job is to replace repeated human inspection with deterministic checks.

Their job is **not** to decide semantic independence.
That still comes from reviewing the actual changes.

## Key Constraint

These scripts are designed to work even when Graphite is **not** installed.

They prefer:

- `git`
- `gh`
- PowerShell

`gt` is optional and mostly irrelevant to the useful parts of the package.

## Scripts

### `graphite-preflight.ps1`

Path:

- [graphite-preflight.ps1](../../plugins/frozen-skills/skills/graphite-stacked-pr-workflow/scripts/graphite-preflight.ps1)

Purpose:

- verify repo context
- detect the current branch and likely trunk
- detect whether `git` and `gh` are available
- detect dirty state and conflicts

Use it when:

- you need the first basic sanity pass
- you want to know whether the repo is safe enough to analyze

### `stack-inventory.ps1`

Path:

- [stack-inventory.ps1](../../plugins/frozen-skills/skills/graphite-stacked-pr-workflow/scripts/stack-inventory.ps1)

Purpose:

- list local branches
- list open PRs
- surface current stack context
- surface Graphite stack output when available

Use it when:

- you are routing the repo into one of the scenarios
- you need a quick branch/PR picture before choosing a repair strategy

### `route-stack-scenario.ps1`

Path:

- [route-stack-scenario.ps1](../../plugins/frozen-skills/skills/graphite-stacked-pr-workflow/scripts/route-stack-scenario.ps1)

Purpose:

- turn inventory into a first-pass scenario recommendation
- tell the operator which workflow docs to read next
- distinguish between greenfield, messy-branch, and messy-graph starting states

Use it when:

- you want the repo to tell you "what kind of problem is this?"
- you want a quick jump from raw inventory to the right workflow

### `pr-base-audit.ps1`

Path:

- [pr-base-audit.ps1](../../plugins/frozen-skills/skills/graphite-stacked-pr-workflow/scripts/pr-base-audit.ps1)

Purpose:

- audit open PR base branches
- flag flattened review graphs where dependent work is all targeting trunk
- flag existing non-trunk relationships that need verification

Use it when:

- the main question is whether the PR graph is structurally wrong
- you need a fast answer to "are these PRs stacked, parallel, or just broken?"

Important:

- the script can tell you the PR graph is flat
- it cannot tell you whether the flat PRs are truly independent
- that decision still comes from semantic review of the diffs

### `infer-pr-dependencies.ps1`

Path:

- [infer-pr-dependencies.ps1](../../plugins/frozen-skills/skills/graphite-stacked-pr-workflow/scripts/infer-pr-dependencies.ps1)

Purpose:

- programmatically inspect open PR branches
- infer likely dependency relationships from branch ancestry
- surface overlap where ancestry is unclear

Use it when:

- you want tooling to tell you which PRs are probably stacked already
- you want a first-pass dependency graph before manual review

Important:

- this is an inference helper, not an oracle
- ancestry is stronger evidence than file overlap
- semantic review is still the final tie-breaker when overlap exists without clear ancestry

### `verify-parent-diffs.ps1`

Path:

- [verify-parent-diffs.ps1](../../plugins/frozen-skills/skills/graphite-stacked-pr-workflow/scripts/verify-parent-diffs.ps1)

Purpose:

- check the incremental diff story bottom-up
- confirm that each branch only introduces its own slice relative to its parent

Use it when:

- the stack structure looks correct, but you need to prove the review surfaces are actually clean

### `graphite-submit-safe.ps1`

Path:

- [graphite-submit-safe.ps1](../../plugins/frozen-skills/skills/graphite-stacked-pr-workflow/scripts/graphite-submit-safe.ps1)

Purpose:

- provide a safer wrapper around `gt submit`
- keep any real Graphite usage isolated as an optional compatibility path

Use it when:

- you explicitly choose to use real Graphite tooling
- the repo is initialized for Graphite
- the stack is ready to be submitted or updated

## How These Fit The Replica

The point of the replica is not "pretend `gt` exists."

The point is:

- use scriptable checks for the repeatable parts
- keep the routing and stack logic explicit
- allow optional Graphite acceleration where available

That means the normal flow is:

1. preflight
2. inventory
3. route to the right workflow
4. audit PR bases
5. infer likely dependencies
6. repair or build
7. verify parent-relative diffs
8. optionally submit with `gt` if available

## Planned Expansion

The next useful helpers are:

- PR base audit against the intended stack order
- bulk PR retargeting for repaired chains
- branch ancestry comparison for "expected stack" vs "actual stack"
- stack report generation as Markdown for review handoff
