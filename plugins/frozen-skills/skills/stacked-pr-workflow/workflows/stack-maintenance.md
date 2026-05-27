# Stack Maintenance

Use this when the stack was once correct but drifted after merges, rebases, or lower-branch edits.

## Entry Criteria

- The stack already exists
- Lower branches changed, merged, or were rewritten

## Steps

1. Identify which lower branch changed and which descendants are affected.
2. If you changed the current branch, apply edits with:

   ```bash
   gt modify --all
   ```

3. Restack descendants:

   ```bash
   gt restack --upstack
   ```

4. Refresh remote state:

   ```bash
   gt submit --stack
   # or
   gt sync
   ```

5. For another machine or collaborator copy, use:

   ```bash
   gt get <branch-or-pr>
   ```

6. Re-check the effective diff of each child PR.

## Exit Criteria

- No child PR contains already-merged lower-stack changes
- The stack is readable bottom-up again

- No child PR contains already-merged lower-stack changes
- The stack is readable bottom-up again
