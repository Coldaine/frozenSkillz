# Cross-Task Relevance Review

## Goal

Review accessible Codex task bodies in one repository or project family together and identify whether each remains current, is a durable completed reference, or was replaced by later work.

This review is proposal-only. It does not rename, archive, pin, reparent, delete, or merge tasks. An Archive Candidate label or `🗄️` title marker is a recommendation that still requires separate authorization before any archive mutation.

## Attribution Order

1. Resolve the repository root from the task working directory when possible.
2. Use stable body evidence: repository name, remote, branch, issue, pull request, artifact, or explicit path.
3. Use a stable owner-provided project-family mapping.
4. Otherwise mark the task unassigned.

A title, dated Codex task directory, attachment path, or age is not repository identity by itself.

## Required Body Evidence

For each candidate, read enough to identify:

- dominant purpose and deliverable;
- later pivots or corrections;
- substantive outcome and remaining work;
- branches, commits, pull requests, issues, files, and artifacts;
- explicit continuation, correction, duplication, or replacement language.

For a long task, selective paging is acceptable only after reading the opening request, later substantive outcome, and all passages relevant to the proposed relationship.

## Classifications

| Classification | Meaning |
|---|---|
| `current` | Best available current source for the workstream or decision |
| `completed-reference` | Scoped work has a durable result worth retaining |
| `superseded` | Identified later work replaces the operative plan, decision, implementation, or outcome |
| `duplicate` | Substantially repeats another task without a distinct durable result |
| `needs-review` | Evidence is incomplete, conflicting, or too weak |

Directed relationships are `continues`, `supersedes`, `corrects`, `duplicates`, and `independent`.

## Confidence

- **High:** explicit successor language, a shared named issue or artifact with later verified state, or direct repository evidence.
- **Medium:** subject, repository, deliverable, and chronology strongly align, but there is no explicit successor statement.
- **Low:** relationship is plausible but decisive evidence is absent. Classify the task as `needs-review` rather than `superseded` or `duplicate`.

Age ranks what to inspect first. It never establishes a relationship or an archive recommendation.

## Attention Review

After classification, compare all eligible `current` tasks in the frozen audited scope:

1. Exclude completed references, duplicates, superseded tasks, and tasks with no unfinished outcome.
2. Identify every task with a concrete remaining action, decision, or follow-up; these are eligible for `🟡`.
3. Rank unfinished current tasks by explicit owner urgency, safety or loss risk, downstream blocking impact, time sensitivity, then action readiness.
4. Assign `🔴` to the single highest-priority unfinished task only when the comparison is credible. Otherwise assign none.
5. Verify the final manifest contains zero or one red marker.

The red marker is scope-relative. State the audited scope and coverage beside the selection; never imply a repository-wide or history-wide winner from a partial sample. Recency may break no ties by itself.

## Archive Candidate Review

An Archive Candidate requires both a safe disposition and a retention judgment. Recommend `🗄️` only when one of these evidence patterns holds:

- a verified completed one-off has no meaningful durable reference value and no remaining work;
- a duplicate has no distinct result and a named canonical task is retained;
- a superseded task's operative value is preserved in a named accessible successor or durable artifact.

Do not recommend archive merely because a task is described as “one-off,” old, verified complete, superseded, quiet, or inconvenient. “Delivered” and “no remaining work” establish outcome state, not retention value. Make the retention judgment from the body, related tasks, and durable artifacts. Keep a completed task when its verified result remains a useful reference. Keep an unfinished task when it is still the only source for active work, regardless of age. When value is uncertain, use `needs-review` and do not add `🗄️`.

## Manifest Fields

Record one item per reviewed task:

- `thread_id` and `host_id`;
- `repository_family` and attribution basis;
- `current_title` for review context only;
- `classification` and confidence;
- related task IDs, directed relationships, and evidence;
- body-derived outcome summary and remaining work;
- proposed markers and evidence for each marker;
- archive-candidate basis, retained canonical task or artifact, and separate authorization status;
- proposed follow-up: `keep`, `review`, or separately authorized future mutation candidate.

Also record inventory totals, review time, inaccessible tasks, unassigned tasks, ambiguous relationships, red-marker count, the red selection basis when present, and coverage limits on that selection.
