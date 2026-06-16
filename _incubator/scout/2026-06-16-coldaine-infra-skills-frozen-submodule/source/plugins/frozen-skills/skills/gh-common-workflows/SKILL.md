---
name: gh-common-workflows
description: "Use when working with the standard GitHub CLI (`gh`) for repository collaboration workflows, especially opening, triaging, reviewing, merging, or closing GitHub pull requests. Apply when Codex needs an opinionated PR queue workflow with explicit review-comment retrieval, merge/close decisions, and supporting issue or PR creation commands."
---

# GH Common Workflows

Use this skill for standard GitHub CLI workflows with emphasis on pull request triage, review, and merge/close decisions.
Keep scope limited to core `gh` commands.

## Core Rules

- Treat PR review as the primary workflow; issue/PR creation is secondary.
- Read canonical scope docs before deciding whether a PR should merge.
- Do not treat `gh pr view --comments` as complete review coverage.
- Do not merge or close overlapping PRs until you have checked for unique salvageable work.

## Preflight

Run these checks before changing review state or opening/closing anything:

```bash
gh auth status
gh repo view --json nameWithOwner,defaultBranchRef,isArchived
gh issue list --state open --limit 20
gh pr status
```

Add `-R owner/repo` for non-default repositories.

## Workflow Selection

- If the task is "what PRs are open and what should happen next", load `references/pr-triage-review-merge.md`.
- If the task is "review this PR and decide merge/hold/close", load `references/pr-triage-review-merge.md`.
- If the task is "open an issue", "open a PR", or "post/update a status comment", load `references/create-issue-pr-comments.md`.

## Guardrails

- Prefer newest actively updated PRs first, then move backward.
- Prefer the PR whose package boundary and NORTH_STAR alignment are correct.
- Prefer explicit PR comments when the merge/close reasoning is non-obvious.
- Prefer `--body-file` over long inline `--body`.
