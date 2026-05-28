---
name: stacked-pr-workflow
description: "Use when converting messy branch or PR state into reviewable stacked pull requests with normal git and GitHub tooling. Applies when branches need semantic slicing, PR bases need retargeting, descendant branches need restacking, or checkpoint-heavy work must converge into a coherent bottom-up review story. Graphite gt can be used as an optional accelerator, but is not required."
version: 1.0.0
tags:
  - stacked-prs
  - git
  - github
  - branch-repair
  - graphite-compatible
---

# Stacked PR Workflow

Use this skill to turn messy branch or PR state into a coherent stacked PR sequence. The execution baseline is plain `git`, `gh`, and the included PowerShell helpers. If Graphite `gt` is installed and initialized, it may be used as an optional transport layer, but the workflow must still be understandable and executable without it.

## When To Use

- The user wants stacked PRs rather than flat PRs against `main`.
- A mixed branch needs to be split into reviewable semantic slices.
- Existing PRs point at the wrong base branches.
- Lower branches in a stack changed or merged and descendants need restacking.
- Checkpoint-heavy agent work needs to be converted into a clean bottom-up review story.

## When Not To Use

- Do not use for plain branch cleanup when all PRs should stay flat against `main`.
- Do not use as a substitute for a hosted merge queue, PR inbox, or reviewer policy.
- Do not preserve a bad PR graph just because retargeting is awkward.

## Core Rules

- Freeze the current PR topology before editing it.
- Separate messy working history from review history.
- Every PR should diff against its parent branch, not `main`, unless it is the bottom PR.
- Prefer `git`, `gh`, and helper scripts; use `gt` only when it is explicitly available and helpful.
- If the current PR graph is wrong, retarget or recreate it instead of tolerating duplicate review surfaces.

## Workflow Selection

- One clean branch: read [workflows/greenfield-stack.md](workflows/greenfield-stack.md).
- One mixed branch: read [workflows/messy-branch-to-stack.md](workflows/messy-branch-to-stack.md).
- Multiple wrong-base or overlapping PRs: read [workflows/messy-pr-graph.md](workflows/messy-pr-graph.md).
- Previously correct stack drifted after merges or rebases: read [workflows/stack-maintenance.md](workflows/stack-maintenance.md).

## Practical Sequence

### Phase 1: Inventory

1. Inspect local branches and open PR base relationships.
2. Identify the state: one clean branch, one mixed branch, messy PR graph, or stack drift.
3. Write the intended review slices from bottom to top.

Use helper scripts first:

```powershell
powershell -File {baseDir}/scripts/stack-preflight.ps1 -RepoRoot .
powershell -File {baseDir}/scripts/stack-inventory.ps1 -RepoRoot .
powershell -File {baseDir}/scripts/route-stack-scenario.ps1 -RepoRoot .
powershell -File {baseDir}/scripts/pr-base-audit.ps1 -RepoRoot .
powershell -File {baseDir}/scripts/infer-pr-dependencies.ps1 -RepoRoot .
```

Exit criteria:
- the target stack order is explicit
- each intended PR has a short purpose statement

### Phase 2: Normalize History

1. Split or condense mixed work into semantic slices.
2. Decide which PRs should be kept and retargeted versus recreated.
3. Remove overlap so each slice has a narrow review story.

Baseline commands:

```bash
git switch -c <child-branch> <parent-branch>
git cherry-pick <commit>
git restore --source=<branch> -- <path>
git add -p
git commit -m "feat(scope): focused slice"
gh pr create --base <parent-branch> --head <child-branch>
gh pr edit <number> --base <new-parent-branch>
```

Optional Graphite equivalents are documented in [references/optional-graphite-command-map.md](references/optional-graphite-command-map.md).

Exit criteria:
- each intended PR maps to one coherent slice of work
- later PRs no longer duplicate lower-layer changes

### Phase 3: Build Or Repair The Stack

1. Create or reorder branches from the bottom up.
2. Ensure every branch is based on its parent branch, not `main`.
3. Create or update PRs so base branches match the intended stack.

Exit criteria:
- branch ancestry matches the intended order
- PR bases point at the right parent branches

### Phase 4: Verify Review Surfaces

1. Check each PR's effective diff against its parent.
2. Confirm the bottom PR is independently reviewable.
3. Confirm each higher PR only contains its incremental slice.

Use:

```bash
git diff --stat <parent-branch>...<child-branch>
gh pr diff <number> --name-only
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

Exit criteria:
- no child PR points at the wrong base
- no merged lower branch remains as an active parent

## Optional Graphite Compatibility

Use local help as the source of truth before relying on `gt`:

```bash
gt --help
gt <command> --help
```

Common optional command families:
- `gt create`
- `gt modify`
- `gt submit`
- `gt sync`
- `gt log`

Graphite references:
- [references/optional-graphite-capability-map.md](references/optional-graphite-capability-map.md)
- [references/optional-graphite-command-map.md](references/optional-graphite-command-map.md)

Optional compatibility helper:
- [scripts/submit-with-graphite.ps1](scripts/submit-with-graphite.ps1)

## Rationalizations To Reject

- "We can just open every PR against main for now."
- "Reviewers can figure out the mixed branch."
- "Retargeting is messy, so leave the bad base chain in place."
- "Graphite will infer the right story from bad commit history."
- "We can clean up after merge."

## Reference Index

- [workflows/greenfield-stack.md](workflows/greenfield-stack.md)
- [workflows/messy-branch-to-stack.md](workflows/messy-branch-to-stack.md)
- [workflows/messy-pr-graph.md](workflows/messy-pr-graph.md)
- [workflows/stack-maintenance.md](workflows/stack-maintenance.md)
- [scripts/stack-preflight.ps1](scripts/stack-preflight.ps1)
- [scripts/stack-inventory.ps1](scripts/stack-inventory.ps1)
- [scripts/route-stack-scenario.ps1](scripts/route-stack-scenario.ps1)
- [scripts/pr-base-audit.ps1](scripts/pr-base-audit.ps1)
- [scripts/infer-pr-dependencies.ps1](scripts/infer-pr-dependencies.ps1)
- [scripts/verify-parent-diffs.ps1](scripts/verify-parent-diffs.ps1)

## Success Criteria

- Every stack slice has a clear purpose.
- Every branch is based on its actual parent.
- Every PR contains only its incremental slice.
- Wrong-base or superseded PRs are repaired rather than tolerated.
- Review can happen bottom-up cleanly.
