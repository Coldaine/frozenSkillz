# Decision Log: WondelAI skills pragmatic-programmer

## Decision

- Date: 2026-07-17
- Reviewer: Codex planning_skill_intake
- Artifact paths: source/pragmatic-programmer/SKILL.md and source/pragmatic-programmer/references/tracer-bullets.md
- Outcome: incubate for later
- Affected frozenSkillz paths: this scout directory and docs/skill-review/tracker.md only

## Evidence

- Inventory summary: one broad skill and six long references; the selected value is the tracer-bullet/prototype reference.
- Rubric score summary: parent skill 3.9/5; selected reference 4.0/5.
- Eval run paths: none; only evals/cases/prototype-or-tracer.md is defined.
- Safety notes: prototype guidance needs explicit isolation, secret, and non-production-data rules.
- Maintenance notes: whole-skill context cost and broad triggering are disproportionate to the narrow desired behavior.

## Rationale

The tracer-bullet distinction is a strong candidate for a small, independently
worded frozenSkillz pattern. The complete skill should not be installed or
promoted solely for that fragment. No live comparison exists, and adaptation
must review the repository-versus-book provenance boundary.

## Follow-Up

- Owner: unassigned evaluator
- Due date or trigger: before adding a progress-oriented implementation skill
- Required validation: execute the three-variant eval, perform provenance review, and decide whether to merge a narrow concept into an existing planning skill or create a separately scoped adaptation.
