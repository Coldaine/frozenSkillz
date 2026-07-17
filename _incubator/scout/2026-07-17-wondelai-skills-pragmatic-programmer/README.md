# Scout: WondelAI skills pragmatic-programmer

Status: scout, incubated, and not installable from any frozenSkillz manifest.

## Provenance

- Source: https://github.com/wondelai/skills
- Upstream commit: ed2930cf8496336641441eef513ad2ad857b65a1
- Upstream commit date: 2026-07-16T17:25:36Z
- Upstream target: pragmatic-programmer
- Imported: 2026-07-17
- License: MIT, copyright 2025 Wondel.ai sp. z o.o.; preserved in source/LICENSE
- Reviewer: Codex planning_skill_intake

The repository exposes the candidate through symlinks under .agents, .claude,
.cursor, .pi, .windsurf, and a plugin. The canonical root directory
pragmatic-programmer is the actual file tree and is the only skill tree
snapshotted here.

## Snapshot Scope

The immutable source snapshot contains the canonical target directory with one
SKILL.md and six routed references, plus the root license. The upstream catalog,
other skills, plugins, host symlinks, and generated marketplace material were
excluded.

- source/pragmatic-programmer/SKILL.md SHA-256:
  7bd0a042aa2dd559f0327916f8d4f2dcf7d21e5f2343a193eaafee932f0f85a3
- source/pragmatic-programmer/references/tracer-bullets.md SHA-256:
  1ecc782fa53ba364a8d4766a38d551ce696d29583bebfc0710d680270e587fa2

Do not edit source/. Notes, evals, and future adaptations belong beside it.

## Evaluation Focus

The narrow focus is the tracer-bullet versus disposable-prototype decision
described in SKILL.md and references/tracer-bullets.md. The broader DRY,
contracts, broken-windows, reversibility, estimation, and knowledge-portfolio
material is inventoried but deferred.

## Installation Caveats

- The entry skill is broad and forces a 10/10 diagnostic score even when the
  user only needs a narrow tracer-bullet or prototype decision.
- SKILL.md is 16.5 KB and the complete candidate is roughly 93 KB, so loading
  the whole skill has meaningful context and maintenance cost.
- The description can over-trigger on general best-practice, technical-debt,
  estimation, build-versus-buy, and architecture questions.
- The content explicitly derives its framework from The Pragmatic Programmer
  and links to an affiliate-tagged book page. The repository declares MIT, but
  a provenance/license review should still distinguish the repository license
  from the separately copyrighted book before frozenSkillz adapts distinctive
  wording.

No active packaging or installation decision is made by this scout.
