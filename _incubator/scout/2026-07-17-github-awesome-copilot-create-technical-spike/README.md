# Scout: GitHub awesome-copilot create-technical-spike

Status: scout, incubated, and not installable from any frozenSkillz manifest.

## Provenance

- Source: https://github.com/github/awesome-copilot
- Upstream commit: cf04ddde790008b3cf01dcdbb1f7213cd6e55a71
- Upstream commit date: 2026-07-17T14:22:35+10:00
- Upstream target: skills/create-technical-spike
- Imported: 2026-07-17
- License: MIT, copyright GitHub, Inc.; preserved in source/LICENSE
- Reviewer: Codex planning_skill_intake

## Snapshot Scope

The immutable source snapshot contains only the target skill and the repository
license. The 90 KB upstream catalog README and unrelated skills, plugins,
extensions, hooks, and examples were deliberately excluded.

Source files were copied byte-for-byte from a depth-one sparse checkout. The
SHA-256 of source/skills/create-technical-spike/SKILL.md is
2cac…26 tokens truncated…echnical-spike

## Decision

- Date: 2026-07-17
- Reviewer: Codex planning_skill_intake
- Artifact paths: source/skills/create-technical-spike/SKILL.md
- Outcome: incubate for later
- Affected frozenSkillz paths: this scout directory and docs/skill-review/tracker.md only

## Evidence

- Inventory summary: one narrowly scoped skill with a strong document template and explicit research phases.
- Rubric score summary: 3.5/5; useful but tool-specific, monolithic, and weak on negative triggers and safety.
- Eval run paths: none; only evals/cases/technical-unknown-to-decision.md is defined.
- Safety notes: candidate names mutating tools but provides no permission, secret, or rollback guidance.
- Maintenance notes: input interpolation and named Copilot/VS Code tools must be adapted for each host.

## Rationale

The core technical-spike pattern is worth evaluating, especially its explicit
external-research and focused-prototype phases. Promotion would be premature:
there is no live eval, and installing the source unchanged could turn a quick
unknown into a mandatory planning document while exposing host-specific syntax.

## Follow-Up

- Owner: unassigned evaluator
- Due date or trigger: before any active planning or spike skill is added
- Required validation: execute the three-variant eval, compare decision quality and time-to-action, then choose adapt concept only, merge into an existing planning skill, or discard.
