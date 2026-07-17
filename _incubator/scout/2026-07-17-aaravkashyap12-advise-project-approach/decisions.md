# Decision Log: AaravKashyap12 advise-project-approach

## Decision

- Date: 2026-07-17
- Reviewer: Codex planning_skill_intake
- Artifact paths: source/skills/advise-project-approach/SKILL.md and source/skills/advise-project-approach/agents/openai.yaml
- Outcome: incubate for later
- Affected frozenSkillz paths: this scout directory and docs/skill-review/tracker.md only

## Evidence

- Inventory summary: one comprehensive 21.9 KB skill and one small OpenAI interface config.
- Rubric score summary: 4.1/5 for the skill; config retained as unscored packaging metadata.
- Eval run paths: none; only evals/cases/mid-build-research-scope.md is defined.
- Safety notes: strong read-only and secret boundaries; mutation permission language may duplicate higher-level authorization.
- Maintenance notes: monolithic time-sensitive research and pricing guidance needs progressive disclosure.

## Rationale

This is the strongest complete research workflow of the three candidates, but
its breadth can turn one implementation uncertainty into a project-wide review.
Without a live eval there is no basis for promotion, and its large entrypoint
does not meet frozenSkillz progressive-disclosure expectations.

## Follow-Up

- Owner: unassigned evaluator
- Due date or trigger: before adapting a general project-research skill
- Required validation: run the three-variant mid-build eval with browsing, score source quality and scope control, then prototype a lean router plus routed research and output references.
