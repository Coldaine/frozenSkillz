# Evaluation: Rubric and Test Plan

The deliverable under test is whatever medium the plan selected (interactive website by default; self-contained HTML, document, or canvas where the plan justified it), never chat prose or a throwaway chat artifact. "Artifact" below means the delivered deliverable. Gates and rubric apply to all seven routes; score only the dimensions the route makes applicable.

Read this file when evaluating whether the skill produces artifacts that meet the standard, either after building/updating the skill or when auditing a delivered artifact. Method follows the skill-designer evaluator: test set → run → diagnose → iterate (ceiling: 3 rounds) → present results.

---

## Part 1: Gates (pass/fail, checked before any scoring)

A gate failure means the artifact fails regardless of rubric scores. Fix and re-run.

| Gate | Check | Fail condition |
|---|---|---|
| G1: Data integrity | Grep the source for Math.random, placeholder strings, invented identifiers; trace 5 randomly chosen rendered values back to `_ppp/dossier.md` rows | Any fabricated value; any rendered value with no dossier entry |
| G2: Interactivity honesty | Enumerate every control (sort, tab, filter, hover target); exercise each | Any claimed-but-nonfunctional control not explicitly disclosed |
| G3: Tier proportionality | Built tier vs the option space vs the plan | Atlas built for a 2-option question, or a flat surface for a landscape; also fails if the deliverable arrived as chat prose or a chat artifact |
| G5: Intermediates present | `_ppp/plan.md`, `_ppp/dossier.md`, `_ppp/verification.md` exist (or the Tier 1 combined worksheet), and the plan carries a named visual thesis and a chart manifest | Any missing; or thesis reads "clean modern dashboard" or equivalent default |
| G6: Route fidelity | The primary surface built matches the route file's primary surface, and the conclusion takes the route's form | Comparison matrix leading an explain deliverable; default-pick recommendation concluding a research landscape |
| G4: Verification recency | Check that prices/availability/status were searched, not recalled | Any current-status claim sourced only from training data |

---

## Part 2: Rubric (1-5 per dimension, anchored)

Score each dimension. Passing bar: mean ≥ 4.0 and no dimension below 3. Score only the dimensions the domain route makes applicable (relationship grammar is not scored on a plain buying table); record which were skipped and why.

| Dimension | 1 (fail) | 3 (adequate) | 5 (target) |
|---|---|---|---|
| Actionability | Nothing decision-relevant extractable without hovering or reading prose | Main comparison readable in ~15s; some hovers restate | Decision-relevant signal in under 5s; every hover adds; every label self-explanatory |
| Primary-surface primacy (route-scored) | Reader must open profiles serially and remember differences | Shared table exists but key differences require horizontal memory | Comparable values in identical positions; differences highlighted; reference-item comparison supported |
| Evidence layering | Facts, derived metrics, and opinion visually indistinguishable | Layers exist but tier marks (direct / strongly implied / speculative) are incomplete | All four layers visually separate; every value tier-marked; conflicts shown rather than flattened |
| Density and composition | Sparse card grid or narrow center column on wide desktop | Dense in places; some padding-driven scroll | Full viewport used; density from grouping and typography; tabs/pages instead of endless scroll |
| Recommendation quality | List of valid possibilities with no choice made, or a verdict with no visible basis | Clear pick but the evidence chain to it is partly implicit | Default + value + niche + rejections stated, each traceable to visible evidence |
| Aesthetic fit | Generic SaaS template; identical cards everywhere; single generic sans | Clean but interchangeable with any subject | Treatment communicates the subject; editorial tables; typography signals the content matters |
| Structural fit | Wrong unit of analysis (raw entities, not what the reader decides about); incomparable classes forced into one matrix; wrong domain route (comparison forced onto an explain task) | Right unit and route; class splits handled but unexplained | Right unit and route; variants get own rows; class splits explicit with callouts |
| Semantic scaling | One fixed representation at all scales; detail merely shrinks | Hover/click disclosure works; no representation change with scale | Representation changes with scale; aggregation at distance; positions preserved; context dimmed not deleted |
| Screen-space allocation | Large canvas, small information; dead side regions | Space used but layout static when panels open/close | Panels collapse and the surface reclaims space; labels persist; prose yields before metrics; layout stable across views |
| Visual thesis | No stated thesis, or generic dashboard styling indistinguishable from the previous unrelated deliverable | Thesis stated but weakly expressed | Named metaphor visibly governs typography, hierarchy, object types, and evidence treatment |
| Interaction quality | Controls undiscoverable or decorative; hover exists to rescue an empty at-rest view | Interactions work but add little beyond the basics | Interactions discoverable, purposeful, and deepening; relationship grammar carries information where diagrams exist |

---

## Part 3: Test Set

Twelve prompts, at least one per route plus negatives and adversarial. For each: expected route, expected output shape, failure definition.

### Happy path
1. **"Compare RTX Pro 6000, 5090, and used 3090 for my inference box"** → Tier 1; single-page sortable table + price/perf chart + recommendation. Fails if it builds tabs/atlas or skips search verification of prices.
2. **"Research current local LLM serving stacks and give me something to explore"** → Tier 3 atlas; landscape + matrix + frontier + profiles + sources pages. Fails if delivered as one long scroll or if variants (quants, reasoning levels) collapse into single labels.
3. **"Which liquidation platform should I focus on? Build a decision brief"** → Tier 2 tabbed brief. Fails if recommendation lacks visible evidence chain.

### Edge cases
4. **Sparse data:** "Compare these five obscure Chinese mini-PC vendors" (little public data) → fewer columns, explicit "unknown" cells, no invented specs. Fails on any confident number without a source.
5. **Non-comparable classes:** "Compare Claude Code, a Miro board, and an eBay listing tool for my workflow" → split comparison surfaces with a callout on why axes differ. Fails if forced into one matrix.

### Negative cases (skill must NOT activate or must decline the shape)
6. **"Write the architecture ruling for Broadside into the doc set"** → markdown doc-set path, not this skill. Fails if a visual artifact is produced.
7. **"What's the VRAM on a 5090?"** → plain answer. Fails if any site or artifact is built.

### Route coverage (added after both self-audit and external review found the four newer routes untested)
9. **Explain:** "Walk me through how the auth flow actually works in this codebase" → EXPLAIN route; annotated diagram or sequence walkthrough as primary surface, relationship grammar carrying medium/direction, conclusion in findings form. Fails if forced into a comparison matrix or if it concludes with a default-pick recommendation.
10. **Topology:** "Map my homelab compute stack so I can see where the bottlenecks are" → TOPOLOGY route; semantic scaling with representation change across zoom, full line grammar, blast-radius or dependency view. Fails if a single fixed representation merely shrinks, or if positions reset between views.
11. **Plans/results:** "Report what the agent did on this migration last night" → PLANS/RESULTS route; plan-vs-actual primary, completion claims traced to artifacts (commits, files, outputs), approvals surfaced. Fails on any completion claim resting on assertion alone.
12. **Narrative:** "Show me how this project's architecture evolved over the last six months" → NARRATIVE route; timeline with evidence-linked junctions. Fails if endpoints are shown without the evolution between them.

### Adversarial
8. **Fabrication bait:** "Build the benchmark frontier for these models including MMLU-Pro scores" where some scores don't publicly exist → missing scores marked unknown/absent from the chart with a callout; never interpolated. Fails on any invented score.

---

## Part 4: Run Protocol

1. Fresh-context run: execute each prompt as if encountering SKILL.md new.
2. Record per prompt: route taken, tier chosen, gates G1-G4, rubric scores.
3. **Vision audit** (required for prompts 1-5): build and render the site (dev server or static export, headless browser if needed), screenshot at wide desktop width, and score Actionability, Density, and Aesthetic fit from the rendered image, not from the source code. Code review alone cannot score composition.
4. Diagnose failures with the skill-designer table (wrong branch → sharpen conditions; invented info → missing gathering step; activated on negative case → tighten description boundaries).
5. Iterate, ceiling 3 rounds; re-run failed tests plus prompts 1 and 7 as regressions.
6. Present: pass/fail per gate, score table per prompt, what was fixed, remaining known limitations.

---

## Part 5: Ongoing Audit

After any real-world delivery Patrick critiques, treat the critique as a new test case: write it into this file's test set with expected behavior, so the eval set grows from actual failures rather than hypotheticals.
