---
name: external-skill-intake
description: Evaluate external skill, plugin, agent, command, hook, configuration, template, evaluation, or documentation-pattern repositories for possible frozenSkillz adoption. Use for external source intake, inventory, scoring, live evaluation, and packaging decisions before promotion.
---

# External Skill Intake

Do not use this for ordinary local skill authoring, direct promotion of already-reviewed repo content, or generic documentation cleanup that does not involve external source intake.

## Rules

- Follow `references/intake-workflow.md` in order.
- Keep external source read-only under `_incubator/scout/<YYYY-MM-DD>-<repo>/source/`.
- Inventory before scoring.
- Score scoped artifacts before packaging decisions.
- Run and persist live evals before recommending promotion of a large pattern.
- Never promote directly from scout source. Adapt the idea into frozenSkillz-owned files.

## Workflow

1. Create or inspect the scout sandbox described in `references/scout-sandbox-layout.md`.
2. Create or update scout metadata outside `source/`: `README.md`, `inventory.md`, `analysis.md`, and `decisions.md` from `templates/decision-log.md` when needed.
3. Select a narrow evaluation scope.
4. Score artifacts with `references/artifact-rubrics.md` and record results in `templates/analysis.md`.
5. Run evals with `references/live-eval-protocol.md` and `templates/eval-case.md`.
6. Decide packaging with `references/packaging-decision-gate.md` and `templates/decision-log.md`.
7. Update `docs/skill-review/tracker.md` if status changes.

## References

- `references/intake-workflow.md`
- `references/artifact-rubrics.md`
- `references/scout-sandbox-layout.md`
- `references/live-eval-protocol.md`
- `references/packaging-decision-gate.md`

## Templates

- `templates/inventory.md`
- `templates/analysis.md`
- `templates/eval-case.md`
- `templates/decision-log.md`
