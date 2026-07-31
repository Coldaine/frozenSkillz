# Analysis: audio-producer

## Scope

- Selected artifacts: whole skill tree `source/audio-producer/` (SKILL.md + references + assets)
- Reason this scope is narrow enough: one Unity SFX production skill; Broadside files are examples inside the same skill, not a second product
- Out-of-scope artifacts: music/score generation, TTS, marketplace promotion, de-Broadside rewrite this pass

## Rubric Scores

| Artifact | Type | Average | Recommendation |
|---|---|---:|---|
| `source/audio-producer/` (whole skill) | skill | 4.36 | Incubate personal / stay gated |

## Detailed Notes

### source/audio-producer/ (whole skill)

| Dimension | Score | Rationale |
|---|---:|---|
| Purpose clarity | 5 | Moment-first SFX production; reasoning record before generate; music/TTS excluded |
| Activation or invocation clarity | 5 | ALWAYS for design/generate/audit/wire SFX; `/audio-producer` and phrase triggers |
| Output contract | 5 | Master Log + Review Checklist + run report; 1:1:1 disk↔log↔checklist verify |
| Reuse value | 4 | Strong for Unity+MCP operators; portable core + Broadside worked evidence pattern |
| Progressive disclosure or structure | 5 | Lean loop in SKILL; phase refs + asset templates routed by phase |
| Safety/security risk | 4 | Credits, compile halt, no overwrite of non-placeholder clips; MCP write gated by preflight |
| Portability | 3 | Honestly Unity + ElevenLabs MCP locked; project path conventions (`docs/audio/`, `Assets/Audio/`) |
| Testability/evaluability | 3 | Self-audit steps exist; needs live Unity project to prove; no promotion evals this pass |
| Maintenance burden | 3 | Multi-ref pipeline + MCP discovery; Broadside examples need labeling as evidence (done in decisions) |
| Fit with frozenSkillz scope | 4 | Matches personal/gated Unity lane (alongside `unity-editor-mcp` incubating notes); not catalog |
| Artifact-specific: Trigger clarity | 5 | Sound pass / missing sounds / wire audio / slash command |
| Artifact-specific: Negative triggers | 5 | Music, voice/TTS, mix/master of existing clips |
| Artifact-specific: Reference and template routing | 5 | Table maps phases → refs/assets |
| Artifact-specific: Gate quality before action | 5 | Incomplete six-field → checklist only, never generate |

**Average:** (5+5+5+4+5+4+3+3+3+4+5+5+5+5) / 14 = **4.36** → band 3.5–4.4

### Broadside examples (worked evidence note)

`assets/example-walk-broadside.md`, `example-profile-broadside.md`, and `example-sound-design-broadside.md` are **worked evidence** from Project Broadside (same operator pattern as `unity-editor-mcp`’s Broadside example). They are not stripped this pass; they demonstrate the reasoning/profile/design-doc shapes. Broader reuse later would keep them under assets/examples and lift portable rules only.

## Summary Recommendation

- Recommended outcome: **incubate personal / stay gated** — personal lane only; do **not** place under `_incubator/frozen-skills/`
- Evidence: high gate quality + MCP-honest scope; Broadside coupling and Unity lock argue personal, not marketplace
- Open questions: live eval on a second Unity project before any de-personalization; confirm ElevenLabs MCP tool names still match discovery notes
