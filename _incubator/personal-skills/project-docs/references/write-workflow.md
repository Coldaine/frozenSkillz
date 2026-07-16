# Writing a New Authority Doc

Generation workflow for a primary document that does not yet exist. Applies to NORTH_STAR.md, architecture.md, and AGENTS.md. Doc-specific guides own section definitions.

For current-work homes (Issues / `docs/plans/`), see `current-work-and-lifecycle.md` — those are not authority primaries.

Two on-ramps: interview (greenfield) vs review + reconcile (docs already in motion). Use the interview for what is truly new.

<interview>

## Step 1: Interview the Owner

Do not open a template. Ask open-ended questions.

| Doc | Questions |
|---|---|
| NORTH_STAR.md | "What is this thing?" / "Why are you building it?" / "What will people assume this is that it isn't?" / "Where is this going?" / "Hard tradeoffs so far?" |
| architecture.md | "What technical approach and why?" / "What is Current vs Planned vs still open?" / "Major components?" / "Choices that would invalidate the project if reversed?" |
| AGENTS.md | "What does an agent need on first entry?" / "What commands actually work?" / "Hard rules on every PR?" / "Where does current work live (Issues vs plans)?" |

Listen for the owner's phrasing. Do not invent constraints they did not state.

Exit when you can describe the doc without them correcting you.

</interview>

<draft>

## Step 2: Draft from the Owner's Words

| Doc | Minimum viable |
|---|---|
| NORTH_STAR.md | Opener + Goals + at least one Anti-Goal |
| architecture.md | Architecture Thesis + Status Legend + System Shape table |
| AGENTS.md | NORTH_STAR pointer + route-by-task + stop rule (≤60 lines) |

Rules:

- Use the owner's phrasing.
- Mark unknowns `[OPEN]`.
- Do not invent constraints.

</draft>

<provenance>

## Step 3: Tag Provenance

- `[OWNER]` — direct words or faithful paraphrase
- `[INFERRED]` — synthesized; flag for review
- `[OPEN]` — not decided

High-authority elements (pillars, invariants, hard rules) must be `[OWNER]` or deleted / asked.

</provenance>

<review>

## Step 4: Review with the Owner

Confirm every `[INFERRED]` and `[OPEN]`, omitted sections, and the opener / thesis / first-line pointer.

</review>

<finalize>

## Step 5: Finalize

Remove provenance tags. Optional frontmatter:

```yaml
---
title: [Project Name] [Doc Name]
date: [today]
author: [owner]
status: living
last_confirmed: [today]
---
```

| Doc | Path |
|---|---|
| NORTH_STAR.md | `docs/NORTH_STAR.md` or root `NORTH_STAR.md` |
| architecture.md | `docs/architecture.md` or root `architecture.md` |
| AGENTS.md | Root `AGENTS.md` (always) |
| CLAUDE.md | Root stub: one-line pointer to AGENTS |

Do not create PROGRESS.md.

</finalize>

<revision>

## Revising an Existing Doc

1. Run `review-checklist.md`.
2. Fix only what needs changing.
3. Update `last_confirmed` if used.
4. Run `authority-flow.md`.
5. For finished temporary docs: promote then delete (`current-work-and-lifecycle.md`).

</revision>
