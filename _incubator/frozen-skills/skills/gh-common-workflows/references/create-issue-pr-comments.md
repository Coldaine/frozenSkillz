# Issues, PR Creation, and Status Comments

Use this reference only when the task is creation or status communication rather than PR triage/review.

## Create an Issue

Search for duplicates:

```bash
gh issue list --state open --search "keyword"
```

Create the issue:

```bash
gh issue create --title "feat: short outcome-focused title" --body-file issue.md --label enhancement
```

Optional context comment:

```bash
gh issue comment <issue-number> --body "Context: scope, risks, and next steps."
```

Issue body format:

```markdown
## Problem
What is broken or missing?

## Desired Outcome
What user-visible result is expected?

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
Risks, dependencies, or constraints.
```

## Create a Pull Request

Push branch first, then open draft PR:

```bash
gh pr create --draft --title "feat: implement <capability>" --body-file pr.md --reviewer team-name
```

Watch required checks:

```bash
gh pr checks --watch --required
```

Mark ready:

```bash
gh pr ready
```

PR body format:

```markdown
## Summary
What changed and why.

## Linked Issue
Fixes #123

## Validation
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual verification

## Risks / Rollback
Known risks and rollback plan.
```

## Status Comments

Create or edit latest comment:

```bash
gh issue comment <issue-number> --body-file update.md
gh issue comment <issue-number> --edit-last --create-if-none --body-file update.md
gh pr comment <pr-number> --body-file update.md
gh pr comment <pr-number> --edit-last --create-if-none --body-file update.md
```

Comment format:

```markdown
Status: <done|blocked|needs-review>
What changed: ...
Why: ...
Next step: ...
```
