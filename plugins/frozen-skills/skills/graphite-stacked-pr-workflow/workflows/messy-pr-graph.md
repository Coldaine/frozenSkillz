# Messy PR Graph

Use this when multiple PRs already exist but the base chain is wrong or the diffs overlap badly.

## Entry Criteria

- Multiple open PRs exist
- At least one PR points at the wrong base branch or duplicates lower changes

## Steps

1. Freeze new branch and PR churn while choosing the canonical stack order.
2. Inventory every open PR, current base, intended parent, and actual semantic slice.
3. Mark each PR as one of:
   - keep and retarget
   - recreate from cleaned history
   - close as superseded
4. Repair local branch tracking when needed:

   ```bash
   gt track
   ```

5. Rebuild the parent chain locally:

   ```bash
   gt move --onto <parent-branch>
   gt reorder
   gt restack
   ```

6. Resubmit the repaired stack:

   ```bash
   gt submit --stack
   ```

7. Close or annotate superseded PRs with a pointer to the canonical replacements.

## Exit Criteria

- There is one canonical stack
- Each active PR has the correct parent
- Superseded PRs are clearly marked
