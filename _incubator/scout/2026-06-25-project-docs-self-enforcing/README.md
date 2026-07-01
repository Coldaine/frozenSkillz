# project-docs self-enforcing redesign — scout incubator

Design exploration for redesigning the `project-docs` skill so it is **self-enforcing**:
an agent following it literally produces the same behavior as the agent that wrote it,
and the docs get updated in the same act as the work. "If it isn't written down, it
didn't happen, and we don't know why."

- Origin session: 2026-06-25 chat in MooseGooseWebsite workspace
- Source skill under critique: `C:\Users\pmacl\.agents\skills\project-docs\`
- Sample NORTH_STAR evaluated + rewritten: `ColdSearch/docs/NORTH_STAR.md`

This is an incubated scout snapshot — design notes and a worked example, not active
plugin content. The skill+CLI split and the bmad/spec-kit research are **exploratory**,
not settled. The NORTH_STAR and architecture.md principles are the load-bearing output.

## Contents

- `README.md` — this file
- `OVERVIEW.md` — conversation overview + reflection + persistence checklist (read this first to orient)
- `session/` — the full session writeup, split by topic
  - `01-the-bar.md` — the self-enforcing principle and what the current skill gets wrong
  - `02-north-star-redesign.md` — opener, goals, conditional In/Out, inverted anti-goals, pillars, deletions
  - `03-architecture-principle.md` — "approach not inventory"; where Shape lands
  - `04-in-out-shape-stress-test.md` — 12 real projects graded (7 HOLDS / 1 THIN / 1 DEGRADES / 3 COLLAPSES)
  - `05-coldsearch-evaluation.md` — per-section grade of the ColdSearch NORTH_STAR + the corrected version
  - `06-skill-cli-exploration.md` — spec-kit + bmad-method research (EXPLORATORY, not settled)
- `examples/`
  - `coldsearch-north-star.corrected.md` — **the resume point**: ColdSearch NORTH_STAR with Patrick's edits applied
- `canvases/`
  - `north-star-shape.canvas.tsx` — the visual canvas artifact from the session

## What is settled vs exploratory

> **Honesty note (added after review):** the adjective "self-enforcing" is the *aspiration*
> for the whole redesign, but the **settled output (sessions 02–03 + the corrected example)
> is self-*persuading*, not self-enforcing.** Content discipline produces a better doc, not a
> converging one. The only mechanism in this work that would actually produce convergence
> under a loop is the `scripts:` gate + `after_*` hook + content-aware validator in
> session/06 — which is explicitly exploratory. So "self-enforcing" describes the goal the
> redesign reaches for; the settled output delivers "self-persuading," and the enforcement
> mechanism is unbuilt. Resume with that distinction in hand.

**Settled (load-bearing output — self-persuading):**
- NORTH_STAR = identity + the problem + 1–2 anti-goals (default zero, earned only). No Requirements, no Shape, no goal backlog.
- Opener default = Problem → Solution. "The Bet" renamed to "The Hypothesis", spike-only.
- Goals = guiding light, not validation. Real shape guidance with examples.
- In/Out conditional, gated on a Caller test (specific caller + contract-shaped Out).
- architecture.md = the approach we've chosen to succeed at the goals, and why — NOT an inventory. With a known limitation (below).
- Shape/Caller exiled from NORTH_STAR to architecture.md.

**Known limitation on the architecture principle (added after review):**
session/03's rule "if a component has no 'because' tying it to a goal, it doesn't belong"
was promoted to settled **without being tested against a real architecture.md.** When run
against ColdSearch's real `docs/architecture.md`, the rule would reject the Major
Components index (the most useful navigation surface in the doc) because its rows have
status + responsibility but no "because." When run against coldaine-k8cluster, it passes
— but that's the platform/DEGRADES case, so the principle is implicitly platform-flavored
and over-rejects on product repos. **The rule needs a carve-out for status-labeled
orientation indexes** (indexed components with a Status column whose job is agent
orientation, not justification) vs unjustified prose inventory. Revise and re-test against
ColdSearch's real architecture.md before treating session/03 as final.

**Exploratory (explored, NOT settled — and the only path to actual self-enforcement):**
- The skill+CLI split as the distribution/enforcement architecture.
- Steals from spec-kit (CLI-scaffolds-skill, `scripts:` gate, constitution-as-input) and bmad-method (CSV routing graph, status-YAML, TOML override layer, correct-course triage).
- These informed the design but the user explicitly flagged "we might have tried to learn too much from bmad/spec-kit — that's not settled." Treat as research input, not a decision.
- **This is the only layer that could move the output from self-persuading to self-enforcing.**
