---
name: graphite-stacked-pr-workflow
description: "Use when replicating a Graphite-style stacked PR workflow with normal git/github tooling. Applies when a branch must be split into reviewable slices, PR bases need retargeting, descendant branches need restacking, or checkpoint-heavy work must converge into a coherent bottom-up stacked PR story."
version: 1.0.0
tags:
  - graphite
  - stacked-prs
  - git
  - github
  - branch-repair
---

# Graphite Stacked PR Workflow

Use a Graphite-style stacked PR workflow around deliberate semantic cleanup.

The useful model is:
- creating a branch above the current branch
- submitting a dependent PR chain
- syncing/restacking descendants when lower branches change
- maintaining correct PR base relationships

This skill should work even when `gt` is absent. The important part is the workflow logic, not the Graphite binary.

## When to Use

- The user wants a Graphite-style stacked PR workflow
- The user has a messy branch and wants to turn it into clean stacked PRs
- Existing PRs point at the wrong base branches and need repair
- Lower branches in a stack changed or merged and descendants need restacking
- The team wants a repeatable path from checkpoint-heavy work to a coherent review story

## When NOT to Use

- Do not use for plain Git cleanup with no stacked PR workflow
- Do not use when the repo should stay on flat PRs against `main`
- Do not use as a substitute for Graphite’s hosted inbox or merge queue
- Do not use when the task is only merge queue administration

## Core Rules

- Freeze PR topology before repairing a broken stack.
- Separate messy working history from review history.
- Every PR should diff against its parent branch, not `main`.
- Prefer plain `git`, `gh`, and the helper scripts unless real Graphite tooling is explicitly available and useful.
- If the current PR graph is wrong, retarget or recreate it instead of preserving a bad review surface.

## Graphite Command Model

The core Graphite flow is built around a small set of commands:

| Command | Use For |
|---------|---------|
| `gt init` | Initialize the repo and choose trunk |
| `gt create` | Create the next branch in the stack |
| `gt modify` | Change the current branch and automatically restack descendants |
| `gt submit` / `gt submit --stack` | Push and create or update PRs |
| `gt sync` | Sync trunk, clean merged branches, and restack what can be restacked |
| `gt log short` / `gt ls` | View the stack |
| `gt info --diff --stat` | Inspect the current branch's parent-relative diff |
| `gt move` | Move a branch onto a different parent |
| `gt reorder` | Reorder branches between trunk and the current branch |
| `gt split` | Split one branch into multiple branches |
| `gt squash` | Collapse a branch to one commit |
| `gt absorb` | Absorb staged hunks into relevant downstack commits |
| `gt track` | Start tracking an existing branch with Graphite or repair metadata |
| `gt get` | Pull a remote branch or stack to another machine |
| `gt freeze` / `gt unfreeze` | Protect or unprotect pulled branches from local edits |
| `gt merge` | Merge PRs from trunk to the current branch |

## Workflow Selection

- If the starting point is one clean branch, read [workflows/greenfield-stack.md](workflows/greenfield-stack.md).
- If the starting point is one mixed branch, read [workflows/messy-branch-to-stack.md](workflows/messy-branch-to-stack.md).
- If there are already multiple wrong-base or overlapping PRs, read [workflows/messy-pr-graph.md](workflows/messy-pr-graph.md).
- If the stack used to be correct but drifted after merges or rebases, read [workflows/stack-maintenance.md](workflows/stack-maintenance.md).

## Practical Sequence

### Phase 1: Inventory

1. Inspect local branches and open PR base relationships.
2. Identify the current state:
   - one clean branch
   - one mixed branch
   - messy PR graph
   - stack drift
3. Write down the intended review slices from bottom to top.

Exit criteria:
- the target stack order is explicit
- each intended PR has a short purpose statement

Use helper scripts first:

```powershell
powershell -File {baseDir}/scripts/graphite-preflight.ps1 -RepoRoot .
powershell -File {baseDir}/scripts/stack-inventory.ps1 -RepoRoot .
powershell -File {baseDir}/scripts/route-stack-scenario.ps1 -RepoRoot .
powershell -File {baseDir}/scripts/pr-base-audit.ps1 -RepoRoot .
powershell -File {baseDir}/scripts/infer-pr-dependencies.ps1 -RepoRoot .
```

### Phase 2: Normalize history

1. Split or condense mixed work into semantic slices.
2. Decide which PRs should be kept and retargeted versus recreated.
3. Remove overlap so each slice has a narrow review story.

Common Graphite commands for this phase:

```bash
gt split --by-commit
gt split --by-hunk
gt split --by-file path/to/files
gt squash
gt absorb --all
gt move --onto <new-parent>
gt reorder
gt track
```

Exit criteria:
- each intended PR maps to one coherent slice of work
- later PRs no longer duplicate lower-layer changes

### Phase 3: Build or repair the stack

1. Create or reorder branches from the bottom up.
2. Ensure every branch is based on its parent branch, not `main`.
3. Use Graphite to submit or update the stack.

Common Graphite commands for this phase:

```bash
gt create --all --message "feat(...): ..."
gt submit --stack
gt move --onto <parent-branch>
gt reorder
gt track --parent <tracked-parent>
```

Exit criteria:
- branch ancestry matches the intended order
- PR bases point at the right parent branches

### Phase 4: Verify review surfaces

1. Check each PR’s effective diff against its parent.
2. Confirm the bottom PR is independently reviewable.
3. Confirm each higher PR only contains its incremental slice.

Use:

```bash
gt info --diff --stat
```

and the helper verifier:

```powershell
powershell -File {baseDir}/scripts/verify-parent-diffs.ps1 -RepoRoot . -Branches branch-a,branch-b,branch-c
```

Exit criteria:
- reviewers can read bottom-up without re-reviewing the same changes

### Phase 5: Maintain

1. Restack descendants after lower-branch changes or merges.
2. Prune or close superseded branches and PRs.
3. Keep the stack aligned with the actual semantic order.

Common Graphite commands for this phase:

```bash
gt modify --all
gt restack --upstack
gt submit --stack
gt sync
gt get <branch-or-pr>
gt freeze <branch>
gt unfreeze <branch>
```

Exit criteria:
- no child PR points at the wrong base
- no merged lower branch remains as an active parent

## Quick Command Guidance

Use local help as the source of truth:

```bash
gt --help
gt <command> --help
```

Common Graphite command families:
- `gt create`
- `gt modify`
- `gt submit`
- `gt sync`
- `gt log`

See:
- [references/graphite-capability-map.md](references/graphite-capability-map.md)
- [references/graphite-command-map.md](references/graphite-command-map.md)

## Rationalizations to Reject

- "We can just open every PR against main for now."
- "Reviewers can figure out the mixed branch."
- "Retargeting is messy, so leave the bad base chain in place."
- "Graphite will infer the right story from bad commit history."
- "We can clean up after merge."

## Reference Index

- [references/graphite-capability-map.md](references/graphite-capability-map.md)
- [references/graphite-command-map.md](references/graphite-command-map.md)
- [workflows/greenfield-stack.md](workflows/greenfield-stack.md)
- [workflows/messy-branch-to-stack.md](workflows/messy-branch-to-stack.md)
- [workflows/messy-pr-graph.md](workflows/messy-pr-graph.md)
- [workflows/stack-maintenance.md](workflows/stack-maintenance.md)

Primary helper scripts:
- [scripts/graphite-preflight.ps1](scripts/graphite-preflight.ps1)
- [scripts/stack-inventory.ps1](scripts/stack-inventory.ps1)
- [scripts/route-stack-scenario.ps1](scripts/route-stack-scenario.ps1)
- [scripts/pr-base-audit.ps1](scripts/pr-base-audit.ps1)
- [scripts/infer-pr-dependencies.ps1](scripts/infer-pr-dependencies.ps1)
- [scripts/verify-parent-diffs.ps1](scripts/verify-parent-diffs.ps1)

Optional compatibility helper:
- [scripts/graphite-submit-safe.ps1](scripts/graphite-submit-safe.ps1)

## Success Criteria

- Every stack slice has a clear purpose
- Every branch is based on its actual parent
- Every PR contains only its incremental slice
- Wrong-base or superseded PRs are repaired rather than tolerated
- Review can happen bottom-up cleanly
