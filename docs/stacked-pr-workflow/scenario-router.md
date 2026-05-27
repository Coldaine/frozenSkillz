# Stacked PR Scenario Router

Use this document when the operator already has a repo problem and needs to jump directly to the right path.

This is the "What is your problem? Where are you going?" router.

## First Move

Always start with inventory.

Run:

```powershell
powershell -File .\plugins\frozen-skills\skills\stacked-pr-workflow\scripts\stack-preflight.ps1 -RepoRoot .
powershell -File .\plugins\frozen-skills\skills\stacked-pr-workflow\scripts\stack-inventory.ps1 -RepoRoot .
powershell -File .\plugins\frozen-skills\skills\stacked-pr-workflow\scripts\route-stack-scenario.ps1 -RepoRoot .
powershell -File .\plugins\frozen-skills\skills\stacked-pr-workflow\scripts\pr-base-audit.ps1 -RepoRoot .
powershell -File .\plugins\frozen-skills\skills\stacked-pr-workflow\scripts\infer-pr-dependencies.ps1 -RepoRoot .
```

Then do the part no tool can skip:

- review the actual branch and PR diffs
- decide whether the work is semantically independent or dependent

The scripts can flag likely stack problems.
They do **not** decide independence for you.

Then pick the scenario below.

## Scenario A: One clean branch, no real PR mess yet

Symptoms:

- one branch contains one coherent story
- no overlapping PRs
- no wrong-base PR chain

Go to:

- Skill workflow: [greenfield-stack.md](../../plugins/frozen-skills/skills/stacked-pr-workflow/workflows/greenfield-stack.md)

Goal:

- create the stack cleanly from the bottom up

## Scenario B: One branch contains multiple unrelated or semi-related stories

Symptoms:

- the branch is checkpoint-heavy
- the diff is too large or mixed to review directly
- you can already see 2-4 logical PR slices hiding inside it

Go to:

- Skill workflow: [messy-branch-to-stack.md](../../plugins/frozen-skills/skills/stacked-pr-workflow/workflows/messy-branch-to-stack.md)

Goal:

- slice the branch into reviewable units before publishing or updating a stack

## Scenario C: Multiple open PRs exist, but their bases or boundaries are wrong

Symptoms:

- PRs point at `main` when they should point at other PR branches
- multiple PRs repeat the same lower-layer changes
- reviewers are being forced to re-review already-reviewed code

Go to:

- Skill workflow: [messy-pr-graph.md](../../plugins/frozen-skills/skills/stacked-pr-workflow/workflows/messy-pr-graph.md)

Goal:

- review the PRs semantically, decide whether they should remain parallel or become a stack, then retarget, recreate, or supersede PRs until the review graph is clean

## Scenario D: The stack used to be fine, but then merges or rebases knocked it out of alignment

Symptoms:

- a lower PR changed or merged
- descendants now show noisy diffs
- branch ancestry and PR bases drifted

Go to:

- Skill workflow: [stack-maintenance.md](../../plugins/frozen-skills/skills/stacked-pr-workflow/workflows/stack-maintenance.md)

Goal:

- restack and resync instead of rebuilding from zero

## Decision Rules

Pick **messy branch** when:

- the main problem is inside one branch

Pick **messy PR graph** when:

- the main problem is the relationship between multiple branches or PRs

Pick **stack maintenance** when:

- the semantic slices are still good, but the stack drifted

Pick **greenfield** when:

- the slices are clean enough that repair is not the main job

## Verification Gate

No scenario is complete until the parent-relative review surfaces are checked.

Run:

```powershell
powershell -File .\plugins\frozen-skills\skills\stacked-pr-workflow\scripts\verify-parent-diffs.ps1 -RepoRoot . -Branches branch-a,branch-b,branch-c
```

If the diffs are still noisy, go back to the relevant scenario and tighten the slices or ancestry.
