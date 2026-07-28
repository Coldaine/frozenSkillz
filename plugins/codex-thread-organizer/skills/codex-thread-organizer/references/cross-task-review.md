# Cross-Task Relevance Review

## Goal

Review accessible Codex task bodies in one repository or project family together and identify whether each remains current, is a durable completed reference, or was replaced by later work.

This review is proposal-only. It does not rename, archive, pin, reparent, delete, or merge tasks.

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

## Manifest Fields

Record one item per reviewed task:

- `thread_id` and `host_id`;
- `repository_family` and attribution basis;
- `current_title` for review context only;
- `classification` and confidence;
- related task IDs, directed relationships, and evidence;
- body-derived outcome summary and remaining work;
- proposed follow-up: `keep`, `review`, or separately authorized future mutation candidate.

Also record inventory totals, review time, inaccessible tasks, unassigned tasks, and ambiguous relationships.
