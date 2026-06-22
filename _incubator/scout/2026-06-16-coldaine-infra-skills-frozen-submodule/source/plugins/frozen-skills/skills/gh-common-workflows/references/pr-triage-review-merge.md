# PR Triage, Review, and Merge

Use this reference when deciding what a PR does, what to review next, and whether to merge, hold, or close it.

## Triage Order

1. Review open PRs newest-first by update time.
```bash
gh pr list --state open --sort updated --limit 30 --json number,title,author,updatedAt,createdAt,labels,assignees,reviewDecision,mergeStateStatus
```
2. Pull each PR's high-level summary.
```bash
gh pr view <pr-number> --json number,title,author,body,createdAt,updatedAt,labels,state,mergeStateStatus,mergeable,reviewDecision,commits,additions,deletions
```
3. Read changed files.
```bash
gh pr diff <pr-number> --name-only
```
4. Read the actual patch before deciding action.
```bash
gh pr diff <pr-number>
```

## Triage Decision Rules

Apply these in order:

1. Review newest actively updated PRs first.
2. Prefer the PR whose package boundary and NORTH_STAR alignment are correct.
3. Prefer the PR that preserves the most useful work with the fewest contradictions.
4. Check competing PRs for unique salvageable ideas, files, or implementation details before closing them.
5. Merge the canonical PR first when possible, then close superseded PRs with explicit rationale.

## Full Review Surface

Do not make a merge decision until you have checked all of these:

1. Aggregate PR state.
```bash
gh pr view <pr-number> --json files,commits,reviews,comments,latestReviews,reviewDecision,statusCheckRollup,mergeStateStatus
```
2. Inline review comments.
```bash
gh api repos/<owner>/<repo>/pulls/<pr-number>/comments --paginate
```
3. Review records.
```bash
gh api repos/<owner>/<repo>/pulls/<pr-number>/reviews --paginate
```
4. Top-level discussion comments.
```bash
gh pr view <pr-number> --comments
```
5. Required checks.
```bash
gh pr checks <pr-number> --watch --required
```

## Decision Actions

Use one of these outcomes:

- `merge`: scope is right, checks are green, and review blockers are resolved
- `hold`: direction is right but contradictions, failing checks, or unresolved reviews remain
- `close`: PR is superseded, wrong-package, or strategically redundant after salvage review

## Review Checklist

Before merging or closing, confirm:

- The PR purpose is clear from title, body, changed files, and patch.
- Inline review comments were fetched from the pull-comments API.
- Top-level reviews and top-level comments were read separately.
- Required checks are green or there is an explicit reason not to wait.
- Competing PRs were checked for unique salvage before closure.
- The final reasoning is written in a PR comment when non-obvious.

## Merge and Close Commands

Merge:

```bash
gh pr merge <pr-number> --squash --delete-branch
```

Close as superseded:

```bash
gh pr close <pr-number> --comment "Superseded by #<replacement-pr>. Closing by triage decision."
```

Dismiss stale blocking review:

```bash
gh api -X PUT repos/<owner>/<repo>/pulls/<pr-number>/reviews/<review-id>/dismissals -f message="Superseded by commit <sha>; feedback points were addressed or invalidated by scope changes."
```
