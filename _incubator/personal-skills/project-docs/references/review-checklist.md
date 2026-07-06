# Review Checklist

This is the router for critiquing an existing authority document. The per-doc guide contains its own review section; this file routes you there and adds the cross-doc check at the end.

<by_document>

## Route to the per-doc review section

| Doc to review | Open this guide and run its checks |
|---|---|
| NORTH_STAR.md | `north-star-guide.md` — Structure, Goals, Requirements, Anti-Goals, Pillars, In/Out/Shape, Provenance |
| architecture.md | `architecture-md-guide.md` — Status labels, Review lanes, Architecture problems to flag |
| PROGRESS.md | `progress-md-guide.md` — Roll-off rule, Review questions |
| AGENTS.md | `agents-md-guide.md` — Decision tree, Bare paths, Pure-router / 60-line cap, Identity-only inline, Working rules |

</by_document>

<severity>

## Classifying findings

The skill does not assign Guardian-style severities. It produces *findings*, which the user can act on. Where weighting helps the user prioritize, classify each finding as:

**Structural** — the document's shape is broken in a way that will produce wrong agent behavior.
- Fabricated content (constraints the owner did not state)
- Goals that are actually requirements
- Pillars without costs
- `@` references inside AGENTS.md
- AGENTS.md inlining content that belongs in another doc (router defeated)
- AGENTS.md over the 60-line cap
- Unlabeled aspiration in architecture.md
- Decisions buried in PROGRESS.md
- Premature In/Out/Shape locking in unearned decisions

**Drift** — the document was right once, but the project has moved.
- Stale `last_confirmed` (older than three months on a living doc)
- Empty sections on a mature project
- Status labels that no longer match current implementation
- PROGRESS.md items completed but not rolled to `docs/history/`

**Style** — the document is sound but readability or precision could improve.
- Underspecified verbs ("learns," "intelligently handles")
- Anti-goals that ban mechanisms instead of intent
- Working rules that are vague or unenforceable
- Tool-specific cruft in shared docs

The user decides what to fix. The skill does not block on any finding.

</severity>

<cross_doc>

## Cross-document authority-flow check

After reviewing a single doc, always run the authority-flow check. The per-doc review catches problems inside the doc; the authority-flow check catches problems between docs. See `authority-flow.md` for the full pass.

Quick version:

| Pair | Question |
|---|---|
| architecture.md vs NORTH_STAR.md | Does the technical approach serve the stated intent without inventing new purpose? |
| PROGRESS.md vs architecture.md | Does current work match the technical direction and the implementation state declared by status labels? |
| PROGRESS.md vs NORTH_STAR.md | Is the project drifting from goals, anti-goals, or pillars? |
| AGENTS.md vs everything | Does the agent entrypoint route to the right authorities without absorbing them? |
| CLAUDE.md vs AGENTS.md | Is CLAUDE.md exactly the two-line stub (`@AGENTS.md` + `@NORTH_STAR.md`), or has content drifted into it? |

A conflict between two docs is always a *finding* against the downstream doc. Authority order is fixed: NORTH_STAR → architecture → PROGRESS → AGENTS.

</cross_doc>

<reporting>

## Output format

When the user asks for a review, produce a structured report:

```text
## [Doc Name] Review

### Structural findings
- [finding] — citing [section]; suggested fix: [edit]

### Drift findings
- [finding] — citing [section]; suggested action: [archive / refresh / mark]

### Style findings
- [finding] — citing [section]; suggested rewording: [edit]

### Authority-flow findings (from cross-doc pass)
- [finding] — between [doc A] and [doc B]; downstream is [doc B]; suggested action: [edit B to align]
```

Do not silently rewrite neighboring docs as a side effect of reviewing one. Suggested edits are presented; the user decides what to apply.

</reporting>
