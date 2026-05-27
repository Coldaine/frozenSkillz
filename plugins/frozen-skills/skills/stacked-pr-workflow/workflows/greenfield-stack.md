# Greenfield Stack

Use this when starting from one clean branch or one clear feature stream.

## Entry Criteria

- The work already has a clear bottom-up dependency order
- No existing PR graph needs repair

## Steps

1. Initialize the repo if needed:

   ```bash
   gt init
   ```

2. Start from trunk:

   ```bash
   gt checkout main
   ```

3. Make the lowest-slice edits and create the first branch:

   ```bash
   gt create --all --message "feat(...): lowest slice"
   gt submit
   ```

4. For each next slice, make edits and create a child branch:

   ```bash
   gt create --all --message "feat(...): next slice"
   ```

5. Submit the whole stack:

   ```bash
   gt submit --stack
   ```

6. Verify the stack:

   ```bash
   gt log short
   gt info --diff --stat
   ```

## Exit Criteria

- Every branch has the correct parent
- Every PR targets its parent branch
- Review can start at the bottom of the stack
