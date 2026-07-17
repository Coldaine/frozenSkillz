# Decision Log: GitHub awesome-copilot create-technical-spike

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
