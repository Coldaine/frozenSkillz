# Inventory: audio-producer

## Provenance

- Source URL: local package `local Downloads/audio-producer.skill` (ZIP handoff; no public git URL in package)
- Commit or version: package SHA256 `FF25FF85760E3474BE9B978C0E218B3BCCD5049A8C87B5861AF965A4A62A53FC`
- Import date: 2026-07-23
- License: undeclared
- Reviewer: intake agent (operator-approved plan)
- Scout path: `_incubator/scout/2026-07-23-audio-producer/`

## Artifact Counts

| Type | Count | Notable paths |
|---|---:|---|
| skill | 1 | `source/audio-producer/SKILL.md` |
| agent | 0 | — |
| command | 0 | slash trigger `/audio-producer` documented in prose only |
| hook | 0 | — |
| config | 0 | expects project `docs/audio/PROFILE.md`, `Sound_Design.md`, Master Log |
| template | 2 | `assets/master-log-entry.md`, `assets/review-checklist-entry.md` |
| eval-case | 1 | `evals/cases/moment-reasoning-gate.md` |
| documentation-pattern | 1 | phase loop + reference routing; Broadside worked examples in `assets/` |

## Useful / Risky / Project-Specific

| Path | Note |
|---|---|
| `SKILL.md` | Act-first SFX loop; six-field reasoning gate; hard constraints; MCP preflight |
| `references/detection-catalog.md` | Lane A (imagine) + Lane B (repo signal families) |
| `references/reasoning-record.md` | Core quality gate — no generate without complete record |
| `references/generation.md` | ElevenLabs-oriented generation + self-audit |
| `references/engine-wiring.md` | Unity MCP attach ladder + `[AUDIO:id]` tags |
| `references/aesthetic-direction.md`, `profile-authoring.md` | Design-doc / profile contracts |
| `assets/example-*-broadside.md` | **Worked evidence** from Project Broadside — keep as examples, do not treat as portable defaults |
| `assets/*-entry.md` | Log/checklist shapes for Phase 6 |

## Risks

- Secret surfaces: ElevenLabs credits/API via MCP; no secrets in package files
- Tool or platform assumptions: Unity editor + Unity MCP write path; ElevenLabs `text_to_sound_effects` (5.0s cap noted); project paths under `docs/audio/` and `Assets/Audio/`
- External dependencies: MCP servers must be present; credit exhaustion is a halt
- License or provenance concerns: undeclared license; Broadside coupling in example assets (honest, intentional)
- Generated or low-quality material: none in package; skill exists specifically to prevent generate-without-reason slop

## Initial Scope Recommendation

- Evaluate: whole skill as one scoped artifact (personal Unity SFX producer)
- Defer: de-Broadside rewrite, marketplace / `_incubator/frozen-skills/` lane, promotion evals
- Discard: nothing this pass
- Needs more evidence: optional one case file only; live Unity+ElevenLabs run later if considering broader reuse
