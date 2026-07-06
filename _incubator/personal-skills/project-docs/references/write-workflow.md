# Writing a New Authority Doc

This is the generation workflow for a primary document that does not yet exist. It applies to NORTH_STAR.md, architecture.md, PROGRESS.md, and AGENTS.md. The doc-specific guide (`references/<doc>-guide.md`) is the source of truth for section definitions, rules, and failure modes. What follows is the process across all four.

In environments with subagents, generation may be delegated to a document-generation subagent. Otherwise, run the interview workflow directly.

Two on-ramps. The interview below is the greenfield path, for a doc that does not yet exist and whose content lives only in the owner's head. For repos where the docs co-evolve with the code (the owner iterates with agents rather than sitting for an interview), the primary loop is instead review + reconcile: run `review-checklist.md` against what already exists, then `authority-flow.md` to propagate, and draft only the genuinely missing pieces. Use the interview for what is truly new; use the review/reconcile loop for everything already in motion.

<interview>

## Step 1: Interview the Owner

Do not open a template. Do not present section options. Ask open-ended questions and listen.

The questions vary by document:

| Doc | Open-ended questions to ask |
|---|---|
| NORTH_STAR.md | "What is this thing?" / "Why are you building it?" / "What will people assume this is that it isn't?" / "Where is this going?" / "Have you had to make any hard tradeoffs yet?" |
| architecture.md | "What technical approach are you taking and why?" / "What is implemented today vs. planned vs. still being decided?" / "What are the major components?" / "What architectural choices, if reversed, would invalidate the project?" |
| PROGRESS.md | "Where does the project stand right now?" / "What's actively being worked on?" / "What's blocking the next move?" / "What does the next session need to know?" |
| AGENTS.md | "What does an agent walking into this repo for the first time need to know?" / "What commands actually work?" / "What hard rules apply to every PR?" / "What gets mistaken for project scope that isn't?" |

### How to listen

- If the owner rambles, that is signal. Capture their exact words.
- Their phrasing is almost always better than whatever you would rewrite it into.
- Do not lead: "Is this a Bet or a Why This Exists?" biases the answer. "Why are you building this?" does not.
- If the owner says something that sounds like a section element, confirm: "It sounds like you'd accept [cost] in exchange for [benefit]. Is that a real tradeoff you've made, or am I reading into it?"

### Exit condition

You can describe the document's content without the owner correcting you.

</interview>

<draft>

## Step 2: Draft from the Owner's Words

Open the doc-specific guide and write the minimum viable shape:

| Doc | Minimum viable |
|---|---|
| NORTH_STAR.md | Opener + Goals + at least one Anti-Goal |
| architecture.md | Architecture Thesis + Status Legend + System Shape table (with status labels) |
| PROGRESS.md | Current State + Active Work + Next Session Focus |
| AGENTS.md | NORTH_STAR pointer + route-by-task + stop rule (≤60 lines) |

Only include sections the interview gave you material for. The doc guide tells you what goes in each section, when to include it, and when to skip it.

### Rules across all four

- **Use the owner's phrasing, not your synthesis.** If the owner said "this is a bet that observation produces insight without classification," that is the opener. Do not rewrite it into "We hypothesize that..."
- **Mark unknowns explicitly.** "Open" is a valid value for a field. A fabricated value is not.
- **Do not invent constraints the owner did not state.** This is the single most important rule. Agents confidently fabricate reasonable-sounding constraints. The interview step exists to prevent this.

</draft>

<provenance>

## Step 3: Tag Provenance

Every claim in the draft gets one tag:

- `[OWNER]` — the owner's direct words or a faithful paraphrase
- `[INFERRED]` — you synthesized this from what they said; flag for explicit review
- `[OPEN]` — not yet decided; marked as a gap

If you are writing `[INFERRED]` on a high-authority element (a NORTH_STAR pillar, an architecture invariant, an AGENTS.md hard rule), stop. These must come from the owner. Delete the element or ask the owner directly.

</provenance>

<review>

## Step 4: Review with the Owner

Present the draft. Direct the owner's attention to:

1. Every `[INFERRED]` tag: "Did you mean this, or did I misread you?"
2. Every `[OPEN]` tag: "Do you have an answer, or should this stay open?"
3. Any section you omitted: "I left out [section] because you didn't mention it. Is that right?"
4. The opener / thesis / first-line pointer: "Does this one sentence (or paragraph) capture what this is?"

</review>

<finalize>

## Step 5: Finalize

Remove provenance tags. The final document reads clean.

Add frontmatter:

```yaml
---
title: [Project Name] [Doc Name]
date: [today]
author: [owner]
status: living
last_confirmed: [today]
---
```

Place the file at the conventional path:

| Doc | Path |
|---|---|
| NORTH_STAR.md | `docs/NORTH_STAR.md` or root `NORTH_STAR.md` |
| architecture.md | `docs/architecture.md` or root `architecture.md` |
| PROGRESS.md | `docs/PROGRESS.md` or root `PROGRESS.md` |
| AGENTS.md | Root `AGENTS.md` (always root; this is the cross-tool convention) |

</finalize>

<revision>

## Revising an Existing Doc

Run the review checklist first (`review-checklist.md`). Then:

1. For each finding the checklist identified, discuss with the owner whether to fix, defer, or accept.
2. Apply fixes using the same provenance tagging from Step 3.
3. Do not rewrite sections the owner is satisfied with. Touch only what needs changing.
4. Update the `last_confirmed` date in frontmatter.
5. After the revision, run the authority-flow pass (`authority-flow.md`) to surface any new conflicts the revision created with neighboring docs.

</revision>
