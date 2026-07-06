# Authority Flow

The per-doc guides catch problems inside one document. The authority-flow pass catches problems *between* documents. Run it after creating, reviewing, or revising any single document.

---

## The Hierarchy

Authority flows one direction:

```
NORTH_STAR.md
   ↓ (intent)
architecture.md
   ↓ (technical strategy)
PROGRESS.md
   ↓ (current state)
AGENTS.md
   (routes to all of the above)
```

Each downstream doc derives from the upstream docs. When they disagree, the downstream doc is always the wrong one. The skill's job is to surface the disagreement, not to silently fix it.

---

## The Five Pairwise Checks

| Pair | Question | Conflict surfaces as |
|---|---|---|
| architecture.md vs NORTH_STAR.md | Does the technical approach serve the stated intent without inventing new purpose? | architecture.md describes a system NORTH_STAR doesn't ask for; or NORTH_STAR has anti-goals architecture.md crosses. |
| PROGRESS.md vs architecture.md | Does current work match the technical direction and the Current/Planned status labels? | PROGRESS.md is building something architecture.md labels Deferred; or PROGRESS.md treats a Planned item as Current. |
| PROGRESS.md vs NORTH_STAR.md | Is the project drifting from its goals, anti-goals, or pillars? | Active work pursues a thing NORTH_STAR's anti-goals say not to build; or work has stalled on the things NORTH_STAR says matter. |
| AGENTS.md vs everything | Does the agent entrypoint route to the right authorities without absorbing them? | AGENTS.md inlines content that belongs in NORTH_STAR / architecture / PROGRESS; or routes are missing for actual task categories the project encounters. |
| CLAUDE.md vs AGENTS.md | Is CLAUDE.md the two-line eager-load stub (`@AGENTS.md` + `@NORTH_STAR.md`)? | CLAUDE.md has prose, headers, duplicated doctrine, or `@`-references a third file. |

---

## How to Run the Pass

Open all four primary docs. For each pairwise check above:

1. State the question.
2. Read the relevant sections of both docs.
3. Note whether they agree, disagree, or have an asymmetric gap (one says something the other should mirror).
4. Classify the finding: **conflict**, **gap**, or **alignment-only-needed**.

### Finding types

- **Conflict** — two docs make incompatible claims. The downstream doc updates, or the user explicitly chooses to revise the upstream doc and propagate.
- **Gap** — an upstream doc states something the downstream doc should reflect but doesn't (a goal not reflected in architecture; a Current status not reflected in PROGRESS).
- **Alignment-only-needed** — both docs are technically correct but their phrasing or framing differs in ways that could confuse an agent reading them together.

---

## Resolving Conflicts

Resolution always begins with the question: *which doc is canonical for this claim?*

| Claim type | Canonical doc |
|---|---|
| Identity, goals, anti-goals, pillars | NORTH_STAR.md |
| Technical decisions, system shape, invariants | architecture.md |
| Current implementation status (what's running now) | architecture.md status labels |
| Current work state, blockers, next focus | PROGRESS.md |
| Routes, commands, hard rules for agents | AGENTS.md |
| Durable decisions with rationale | `docs/decisions/` (referenced from architecture.md) |

Once you know which doc is canonical, the resolution is mechanical: update the downstream doc to match.

If the canonical doc is wrong (the project has genuinely changed and the upstream doc is out of date), the user makes that call. The skill surfaces the finding; it does not silently rewrite the upstream doc.

---

## Common Authority-Flow Findings

**The architectural drift.** architecture.md says the system is local-first; PROGRESS.md is actively integrating an external API. Either architecture.md is stale (Current was wrong) or the project is drifting from architecture (and NORTH_STAR may be next). Surface it; ask the user which.

**The buried decision.** PROGRESS.md "Recently Changed" mentions "switched from Redis to SQLite." This is an ADR-level decision sitting in handoff state. Move it to `docs/decisions/` and add to architecture.md's ADR Index.

**The route gap.** AGENTS.md's decision tree has no branch for "writing documentation." Then the user invokes the project-docs skill, and the tree should have routed there. Add the branch.

**The label mismatch.** architecture.md labels the Guardian runtime "Deferred." PROGRESS.md's Active Work table lists "Guardian implementation: in review." One of the labels is wrong. Resolve.

**The doctrine leak.** AGENTS.md inlines a paragraph explaining the project's goals. NORTH_STAR.md already says this. Remove the inline; the tree's first branch already routes to NORTH_STAR.

**The CLAUDE.md regression.** CLAUDE.md has accreted a header and a few "Claude-specific notes." Reduce to `@AGENTS.md`. If those notes are genuinely Claude-specific, they belong in `.claude/CLAUDE-notes.md` or similar, with AGENTS.md as the source of doctrine.

---

## What the Pass Outputs

A short report:

```
## Authority-Flow Findings

### Conflicts
- (between doc A and doc B): canonical is [doc]; suggested fix: [edit]

### Gaps
- (upstream doc says X; downstream doc should reflect): suggested addition: [edit]

### Alignment notes
- (both correct but inconsistent framing): suggested rewording: [edit]
```

The user decides what to apply. The skill does not silently rewrite multiple docs to resolve one finding.

---

## When To Run the Pass

- After any single-doc edit, to catch propagation needs.
- Before declaring a new repo's documentation pattern complete.
- As a periodic check on a mature repo (monthly is reasonable).
- When the user asks "are my docs in sync?"

The pass is cheap: it reads four files and asks five questions. Run it generously.
