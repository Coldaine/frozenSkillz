# Technique: Evidence and Sourcing

Read in Phase 2 for every deliverable. These rules are the highest-priority non-negotiables; when constraints force a trade-off, everything else yields first.

## Tiers

| Tier | Means |
|---|---|
| direct | measured, filed, or vendor-stated with a source |
| strongly implied | multiple corroborating signals, no single direct statement |
| speculative | plausible but unsourced; flag explicitly or omit, and prefer omit |

Inference is labeled as inference, distinctly from sources. Where a claim connects sourced facts, say so and show the reasoning.

## Rules

1. Search-verify every price, availability claim, and current-status fact. Anchor searches to the current year. Training data is fallback, never primary.
2. A value that cannot be found renders as **unknown**. Never an invented number, a placeholder name, an interpolated score, or a fabricated identifier; this includes loading states, empty states, and demos.
3. Every rendered value traces to a dossier entry. A rendered value with no entry is fabrication by definition.
4. Conflicting sources: record both, show both. Never silently flatten into one confident number.
5. Thin data reduces columns; it does not soften numbers. Cutting a dimension is honest; filling it with inference is not.
6. Distinguish measured values, manufacturer claims, community reports, estimates, inferred values, and unknowns in the rendered output, not only in the dossier.

## Rendering sourcing

Make sourcing visible without drowning the presentation: inline source indicators, hover citations, a methodology panel, source-quality labels, and a dedicated sources page for Tier 2/3 builds. Margin or sidenote treatment suits verification status well.

## Completion claims (plans/results route)

An agent's claim that something was done is a claim, not evidence. It traces to an artifact: a commit, a file, a test run, an output. "Done" with no artifact renders as unverified, visibly.
