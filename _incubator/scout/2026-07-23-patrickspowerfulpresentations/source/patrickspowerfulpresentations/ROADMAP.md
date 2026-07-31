# Roadmap

Improvement queue for this skill, in Patrick's words where possible. Read when asked to improve or extend the skill. Items are specified here so a future session can build them without re-deriving intent.

## 1. Confirm the plans/results route with Patrick

The route now exists (references/domains/plans-results.md) with a working reading: plan-vs-actual as primary surface, completion claims tracing to artifacts not assertion, approvals surfaced. The considerations are marked unconfirmed in the route itself; review with Patrick and remove the caveat once settled.

## 2. Template library of composable pre-approved pieces

A `templates/` capability of richly styled, pre-approved **components**; pieces that agents compose per deliverable, with good examples of each. Candidate pieces: sortable comparison matrix, frontier scatter with annotation layer, evidence-tier badge system, hover citation panel, profile card variants per subject type, recommendation block, sources/methodology page, atlas navigation shell.

**Canonical lineage (do not re-derive this doctrine; it already exists):**
- **Pattern-library doctrine, May 25 2026**, AnchorMarks `land-stack-then-rename` Claude Code session. Locked there: pattern library = hand-curated pre-made design pieces agents draw from; distinct from token libraries, component libraries/UI kits, and standardized catalogs (A2UI); thesis "pattern libraries are upstream of The Bet; no patterns, no artifact, no markup, no loop." Five design languages, each needing its own library: **editorial, subway, blueprint, terminal, cockpit** (editorial partially realized; cockpit never existed even as a theme). **Packaging decision: one Claude Code skill per design language**, static resources pulled only when invoked. Durable artifacts: branch `docs/pattern-libraries`, PR #11 on the repo, `docs/PATTERN_LIBRARIES.md` in-repo, `~/.claude/PATTERN_LIBRARIES.md` global, project memory `pattern-library-doctrine.md`. Read those before building anything here.
- **"Primitives, not UI"** (Orb/OmniLink, April 2026): the sibling card; emission vocabulary composed by watcher LLMs, designed once, picked forever; recorded conflicts apply verbatim: component-library-plus-Figma thinking, LLM-authored CSS, boring-corporate-button framing. Five render densities (micro, compact, standard, full, atmospheric) are each piece's density axis.
- **ReportCanvas kit (Jun 8-10 2026)**: the one realized instance and the working model for piece structure: content contract (`data.js`) separated from a fixed renderer, archetypes chosen per section, draft `pattern-library/SKILL.md` + `CONTENT-SCHEMA.md` exist in that package. **Portability lesson from its review:** pieces must build in the target environment; the multi-file in-browser Babel loading pattern requires a server and fails standalone. Pieces ship as buildable source, never as served-loader assemblies.

**Integration with this skill:** the five design languages ARE named visual theses. Phase 1's visual-thesis step, once the libraries exist, selects a design language, which selects that language's pattern-library skill. This resolves the thesis-vs-reuse tension: polyphony across subjects is preserved by language choice; reuse happens within a language. Provenance of each piece (which approved deliverable it came from, when, what changed in genericizing) is recorded with the piece; Patrick flagged provenance tracking as a requirement.

**Sourcing rule (hard):** pieces are extracted from delivered artifacts Patrick has approved (ReportCanvas's editorial kit is the first candidate), then genericized. Never authored speculatively; the last attempt at that produced generic output and was rejected.

**Anti-goal (hard):** NOT the pre-rendered-artifact pattern (Google generative-UI style: model selects pre-baked whole artifacts and throws them into chat). Whole pre-made artifacts cannot anticipate what a specific deliverable needs. Composable pieces with usage examples; assembly and content are always per-deliverable.

## 3. Growing evaluation test set

Already wired (references/evaluation.md, Part 5): every real critique of a delivered site becomes a new test case. Standing task: actually append them.

## 4. Deepen routes against real deliverables

The seven route files and six technique files are written but untested; none has yet governed a real build. As deliverables get made, deepen the routes that prove thin. Two known-shallow spots: topology (the infrastructure-atlas line grammar and zoom behaviors have more depth in past sessions than the file currently carries) and narrative (StoryFlow junction and thread patterns from the Idea Emergence work).

## 5. Per-project profile docs

Genericize further per Patrick's skill philosophy: the skill holds the reusable process; recurring subject areas (e.g., GPU hardware, local models, liquidation lots) get thin profile docs capturing their specific columns, evidence sources, and units, so repeat deliverables in a domain don't re-derive structure.
