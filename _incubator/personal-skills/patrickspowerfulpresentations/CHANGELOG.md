# Changelog

History lives in this file, not in a repo, so it survives wherever the skill is installed. Append an entry on every change; state what changed and what drove it.

## 2026-07-23 (built in one session, six revisions)

**v1** (2 files, 621 lines). Built from Patrick's written Visual Style Brief plus corrections recovered from past chats (zero fabricated data, actionability test, attack-don't-retreat revisions, interactivity honesty, three-tier evidence strength, aesthetic matched to subject, unit of analysis). Named `visual-research-artifacts`. SKILL.md 143 lines; style-brief.md 478 lines (Patrick's document, verbatim, unchanged in every version since).

**v2** Renamed to `broadsheet`. Added `references/evaluation.md`: four pass/fail gates, anchored rubric, eight-prompt test set, run protocol with mandatory vision audit, and Part 5 (every real critique becomes a new test case).

**v3** Corrected a fundamental misread: the deliverable is a **standalone interactive website**, not a chat artifact. Added environment branch (full toolchain vs constrained) and split the domain into research / comparison / buying considerations. Added `ROADMAP.md`.

**v4** Restructured from a preference list into a **workflow**, on Patrick's instruction that skills encode reasoning steps and written intermediates. Introduced the three mandatory intermediates in `_ppp/`: plan.md, dossier.md, verification.md. Added the chart-manifest forcing function and removed two invented rules (TCO; tier boundaries now marked as defaults needing written justification to override).

**v5** Widened in response to an external critique that the skill had narrowed to comparison and was pretending to be the whole category. Trigger became deliverable-based rather than subject-based; medium selection by capability need replaced the fixed Next.js mandate; tiers set scope rather than page templates. Added `references/domains.md` (seven routes) and `references/visual-language.md` (visual thesis workflow, semantic scaling and the five render densities, screen-space allocation, relationship grammar). Rubric gained semantic scaling, screen-space allocation, visual thesis, and interaction quality.

**v6** Fixed a stale mermaid branch label left by the v5 rewrite. Rewrote the roadmap's template-library item with its canonical lineage: the May 25 2026 pattern-library doctrine (five design languages: editorial, subway, blueprint, terminal, cockpit; one skill per language), the "Primitives, not UI" sibling card, and the ReportCanvas kit as the one realized instance plus its portability lesson. Recorded the decision that design languages ARE named visual theses, resolving the thesis-versus-reuse tension.

### Known open issues (from self-audit, not yet fixed)

1. Intermediates are still comparison-shaped; the dossier schema and chart manifest have no per-route form for explain, topology, plans/results, or narrative.
2. The eval test set exercises only research/comparison/buying and negatives; four routes are unevaluated.
3. The conversational-answer path in the trigger gate reopens a bypass; likely needs a written proportionality call when an agent declines the visual path.
4. Ceremony is not tiered; Tier 1 pays the full ritual and may need a combined worksheet plus inherited thesis.
5. "Does not resemble the previous deliverable" is unenforceable without a delivered-artifacts index.
6. Verification is written by the builder; a fresh-context critic pass is the honest fix.
7. style-brief.md's matrix-centric doctrine versus domains.md's route-specific surfaces has no stated precedence line.

## 2026-07-23 later

**v7** Renamed `broadsheet` → `patrickspowerfulpresentations` (the old name collided with Patrick's Broadside project, and a broadsheet is the editorial design language specifically, which is wrong for a language-neutral skill). Intermediates directory `_broadsheet/` → `_ppp/`. Added this changelog to the package. Added four route-coverage test prompts (explain, topology, plans/results, narrative), closing the gap where four of seven routes were unevaluated. Added a precedence line: `domains.md` governs which surface leads; `style-brief.md`'s matrix-centric passages apply only to the comparison and buying routes.

**Note on a package-version mismatch (2026-07-23):** an external review inspected a `.skill` containing 4 files and a 222-line SKILL.md. That is v3, before the widening. Any review should confirm it is reading a package whose `references/` contains `domains.md` and `visual-language.md`; if those are absent, the package predates the widening and its findings about "missing routes" are about the old file.

**v8** Restructured into router + conditionally-loaded depth, on Patrick's instruction that content volume and hot-path size are different problems. SKILL.md cut from 162 to 118 lines and given an explicit read-path table. `visual-language.md` and `domains.md` were dissolved into thirteen files: `references/techniques/` (visual-thesis, semantic-scaling, screen-allocation, relationship-grammar, evidence, charts) and `references/domains/` (research, comparison, buying, explain, topology, plans-results, narrative), each with page archetypes, mandatory mechanics, conclusion form, intermediates delta, and anti-patterns. Added `references/intermediates.md`: full schemas for plan/dossier/verification with per-route variants (closing open issue 1) and a Tier 1 lite path allowing the three files to combine and the thesis to be inherited (closing open issue 4). Trigger gate now requires a one-line written record when an agent declines the visual path (closing open issue 3). Total content roughly doubled while the always-loaded path shrank.

**v9 (final pass)** Reference-integrity audit found and fixed two dangling pointers in ROADMAP.md to files dissolved in v8 (`domains.md`, `visual-language.md`), plus one roadmap item made obsolete by v8 and rewritten as "deepen the routes against real deliverables." Generalized `evaluation.md` past its website-and-comparison framing: the deliverable under test is now whatever medium the plan justified, G1 traces rendered values to dossier rows rather than to a vague "recorded source," "comparison primacy" became route-scored "primary-surface primacy," and two gates were added: **G5 intermediates present** (all three files exist, plan carries a named thesis and chart manifest, a default thesis fails) and **G6 route fidelity** (built primary surface matches the route; conclusion takes the route's form). Replaced the style-brief addenda, which v8 had duplicated across the technique files, with a pointer table plus the precedence rule, removing the second source of truth while leaving Patrick's authored brief verbatim above it.

### Still open

- No route has governed a real build; the seven routes and six techniques are written but untested.
- Verification is still written by the builder; a fresh-context critic pass remains the honest fix.
- "Does not resemble the previous deliverable" needs a delivered-artifacts index or per-project profiles to be enforceable.
- Template library unbuilt; the editorial pattern library is extractable from the ReportCanvas kit and is the obvious first entry.
