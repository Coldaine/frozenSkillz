# Review Checklist

Router for critiquing an existing authority document. Per-doc guides own detailed checks; this file routes and adds the cross-doc pass.

<by_document>

| Doc to review | Guide |
|---|---|
| NORTH_STAR.md | `north-star-guide.md` |
| architecture.md | `architecture-md-guide.md` |
| AGENTS.md | `agents-md-guide.md` — pure router, 60-line cap, bare paths, no PROGRESS/history routes |
| CLAUDE.md | One-line pointer to AGENTS only |
| Legacy PROGRESS.md | `progress-md-guide.md` — migrate away; do not refresh as living handoff |
| Plans / Issues usage | `current-work-and-lifecycle.md` |

</by_document>

<severity>

## Classifying findings

**Structural** — wrong agent behavior:
- Fabricated constraints
- AGENTS inlining doctrine / over 60 lines / `@` inside AGENTS
- CLAUDE.md with prose or multi-file doctrine
- New PROGRESS.md or recommended `docs/history/` roll-off
- Unlabeled aspiration in architecture.md

**Drift** — was right once:
- Stale `last_confirmed`
- Status labels that no longer match reality
- AGENTS still routing to deleted PROGRESS / history
- Finished plans left undeleted after promote

**Style** — sound but imprecise:
- Vague rules
- Anti-goals that ban mechanisms instead of intent
- Tool-specific cruft in shared docs

</severity>

<cross_doc>

After a single-doc review, run `authority-flow.md`.

Authority order: NORTH_STAR → architecture → AGENTS.

Quick pairs: architecture vs NORTH_STAR · plans/Issues vs architecture · plans/Issues vs NORTH_STAR · AGENTS vs everything · CLAUDE vs AGENTS.

</cross_doc>

<reporting>

```text
## [Doc Name] Review

### Structural findings
- [finding] — citing [section]; suggested fix: [edit]

### Drift findings
- [finding] — citing [section]; suggested action: [promote-delete / refresh / fix route]

### Style findings
- [finding] — citing [section]; suggested rewording: [edit]

### Authority-flow findings
- [finding] — between [A] and [B]; downstream is [B]; suggested action: [edit]
```

Do not silently rewrite neighboring docs.

</reporting>
