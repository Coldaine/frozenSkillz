# Graphite Capability Map

Graphite is best treated as the stack transport layer, not the semantic cleanup engine.

## What Graphite Is Good At

- Creating a child branch above the current branch
- Submitting dependent PRs with correct base relationships
- Keeping branch ancestry and PR base chains aligned
- Restacking descendants when a lower branch changes
- Syncing a stack after merges or rebases
- Supporting bottom-up stacked review and landing

## What Graphite Does Not Primarily Solve

- Deciding where one PR should end and the next should begin
- Untangling a mixed branch into semantic slices by itself
- Reconstructing user intent from checkpoint commits without judgment
- Replacing a hosted inbox or merge queue with a single local skill

## Practical Rule

Use Graphite after you can answer these questions:

1. What are the intended review slices?
2. In what order should they be reviewed?
3. Which branch should be the parent of each slice?
4. Which existing PRs must be retargeted, recreated, or closed?

If you cannot answer those, do semantic cleanup first.
