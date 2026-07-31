# Intermediates: Schemas

Read in Phase 1. The three written intermediates live in `_ppp/` in the workspace. They are forcing functions, not paperwork: the plan prevents template-first building, the dossier makes fabrication structurally impossible, and the verification record prevents self-certification. Skipping one is a workflow violation even if the deliverable looks right.

Each route adds fields; see the route's "Intermediates delta" section.

---

## `_ppp/plan.md`

Written before any data collection or layout code.

```markdown
# Plan: <deliverable>

## Question
<one sentence: what decision or understanding must this enable?>

## Route
<research | comparison | buying | explain | topology | plans-results | narrative>
Primary surface: <what leads, per the route file>
Secondary route (if mixed): <route> adds pages: <which>

## Medium and stack
<web app | fixed artifact | canvas | designed document>
Capability justification: <why this medium, not a lighter one>

## Tier
<1 | 2 | 3> ; default boundaries overridden? <no | yes, because ...>

## Unit of analysis
<what the reader decides about / reasons about>
Class splits: <none | list, with why axes cannot be shared>

## Page map
| Page | Question it answers | Visual form | Visible at rest | On hover/select | Evidence kept inspectable |

## Dimensions / columns
<name, unit, why it distinguishes>

## Chart & diagram manifest
| Artifact | The one sentence: what structure this reveals that a table/prose cannot |
(no sentence → cut it)

## Visual thesis
References examined (verified, not assumed): <3+>
What they do structurally: <notes>
Metaphor: <named>
Derived: typography / hierarchy / object types / evidence treatment
Differs from last unrelated deliverable how: <...>

## Data requirements
<every value the deliverable will display>
```

---

## `_ppp/dossier.md`

Written before any layout code. One entry per value from the plan's data requirements.

```markdown
| Subject | Field | Value | Tier | Source | Retrieved |
```

- Tier: direct / strongly implied / speculative.
- Not found → value is `unknown`; it renders as unknown.
- Conflicts → two rows, both sources, both shown in the deliverable.
- **Every rendered value must exist here.** A rendered value with no entry is fabrication by definition.

Route variants:
- **topology:** edges get entries too (medium, capacity, certainty), not only nodes.
- **plans-results:** the dossier is an artifact ledger; the artifact reference (commit, file, run) stands where the source would.
- **narrative:** each junction carries the source artifact it opens onto.
- **explain:** each asserted relationship carries its basis (documented / observed / inferred).

---

## `_ppp/verification.md`

Written after building and rendering, from screenshots.

```markdown
# Verification

## Build
Command: <...> ; clean: <yes/no> ; pages rendered and screenshotted: <list>

## Gates
G1 Data integrity: grep result for fabricated patterns; 5 sampled rendered values traced to dossier rows: <list them>
G2 Interactivity honesty: every control enumerated and exercised: <list>; visual-only controls and where disclosed: <list>
G3 Proportionality: tier built vs option space vs plan
G4 Recency: current-status claims and their retrieval dates

## Actionability, per page
For each page, answer by NAMING the element that satisfies it. A bare "yes" is a fail.
1. Decision-relevant info in <5s: <element>
2. Every hover adds beyond the overview: <element>
3. Labels self-explanatory to a first-time viewer: <element>
4. Every data point traces to the dossier: <sample>

## Acceptance questions
<answers from screenshots; see style-brief.md final section>

## Failures found and fixed
<list; if none, say so and explain why that is credible>
```

---

## Tier 1 lite path

For Tier 1 (a single dense surface, few options, one question), the three files may be combined into one `_ppp/worksheet.md` with the same sections, and the visual thesis may be inherited from a prior deliverable in the same subject area by reference rather than re-derived. The dossier table and the verification gates are never skipped, only co-located. Ceremony scales with the deliverable; the evidence discipline does not.
