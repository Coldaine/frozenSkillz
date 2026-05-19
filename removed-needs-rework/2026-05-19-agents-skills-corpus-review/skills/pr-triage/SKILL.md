---
name: pr-triage
description: Triage and resolve GitHub pull request review comments before merge using gh CLI with metadata-first prioritization, selective body expansion, and strict merge blocking on unresolved root comments. Use this whenever an agent is preparing a PR for review, re-review, or merge readiness.
metadata:
  short-description: Triage PR review comments before merge
---

# PR Triage

## Core Principle

Prioritize complete PR comment closure while minimizing context load: fetch metadata first, expand only needed bodies, resolve threads, and block merge when unresolved root comments remain.

## When To Use

Use this skill when:
- A PR is about to be merged, or an agent says it is "ready for review" or "ready to merge".
- You need a repeatable pass over review comments from humans and bots.
- You want to convert noisy review threads into a deterministic action list.

Do not use this skill for general issue triage or non-PR discussions.

## Required Workflow

1. Preflight auth and repo context.
2. Gather metadata-only review comments.
3. Rank comments root-first (no human-vs-bot priority bias).
4. Expand bodies only for comments that need decision quality.
5. Apply fixes and resolve thread; only reply when substantive explanation is required.
6. Run merge gate and block merge if any root comments remain unresolved.

## Instructions

1. Confirm `gh` is authenticated.
2. Run metadata scan:
   - `bun run scripts/pr-comments.ts list <owner/repo> <pr>`
   - `bun run scripts/pr-comments.ts triage <owner/repo> <pr>`
3. Pull targeted bodies:
   - `bun run scripts/pr-comments.ts expand <owner/repo> <comment_id>`
4. For each actionable comment:
   - Fix code where needed.
   - If acknowledgment only, use:
     - `bun run scripts/pr-comments.ts resolve <owner/repo> <pr> <comment_id>`
   - If substantive response needed:
     - `bun run scripts/pr-comments.ts reply <owner/repo> <pr> <comment_id> "<message>"`
5. Verify and enforce merge gate:
   - `bun run scripts/pr-comments.ts gate <owner/repo> <pr>`
6. Emit final summary:
   - fixed comments (with commit refs),
   - acknowledged/resolved comments,
   - deferred comments with rationale.

## Assumptions

- `gh` CLI is installed and authenticated for the repository.
- `bun` runtime is available for script execution.
- PR comment triage is run before merge, not after merge.
- Bot identities are configurable and should reflect your actual agent stack.

## Files

- `scripts/pr-comments.ts`: triage, expand, reply, resolve, and summary commands.
- `references/gh-api-patterns.md`: API and query patterns for advanced use.
