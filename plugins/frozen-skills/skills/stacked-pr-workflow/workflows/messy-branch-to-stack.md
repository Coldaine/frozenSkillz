# Messy Branch To Stack

Use this when one branch contains multiple storylines that should become separate PRs.

## Entry Criteria

- One branch contains mixed work
- The user still wants stacked PRs instead of one giant review

## Steps

1. Inventory the branch and identify the intended review slices.
2. If the current branch history already has useful internal boundaries, start with:

   ```bash
   gt split --by-commit
   ```

3. If the boundaries are file-driven, use:

   ```bash
   gt split --by-file path/to/files
   ```

4. If the boundaries are hunk-driven, use:

   ```bash
   gt split --by-hunk
   ```

5. Collapse over-granular branches when needed:

   ```bash
   gt squash
   ```

6. Move or reorder branches to match the real dependency order:

   ```bash
   gt move --onto <parent-branch>
   gt reorder
   ```

7. Submit the repaired stack:

   ```bash
   gt submit --stack
   ```

8. Verify each PR against its parent, not `main`:

   ```bash
   gt info --diff --stat
   ```

## Exit Criteria

- The original mixed branch is no longer the review surface
- Each new PR has one coherent story
