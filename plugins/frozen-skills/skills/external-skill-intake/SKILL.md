---
name: external-skill-intake
description: Evaluate external skill, plugin, agent, command, hook, configuration, template, evaluation, or documentation-pattern repositories for possible frozenSkillz adoption using live or forensic evidence before promotion.
---

# External Skill Intake

Use this skill when evaluating an external skill, plugin, agent, command, hook, config, template, eval, or documentation-pattern repo for possible frozenSkillz adoption.

Do not use this for ordinary local skill authoring, direct promotion of already-reviewed repo content, or generic documentation cleanup that does not involve external source intake.

## Rules

- Follow the bundled workflow below in order; repo-local documentation may add placement or
  governance constraints when it is available.
- Keep external source read-only under `_incubator/scout/<YYYY-MM-DD>-<repo>/source/`.
- Inventory before scoring.
- Score scoped artifacts before packaging decisions.
- Run and persist live or forensic evaluations before recommending promotion of a large pattern.
- Never promote directly from scout source. Adapt the idea into frozenSkillz-owned files.

## Workflow

1. Create or inspect the scout sandbox described in `references/scout-sandbox-layout.md`.
2. Create or update scout metadata outside `source/`: `README.md`, `inventory.md`, `analysis.md`, and `decisions.md` from `templates/decision-log.md` when needed.
3. Select a narrow evaluation scope.
4. Score artifacts with `references/artifact-rubrics.md` and record results in `templates/analysis.md`.
5. Evaluate with `references/evaluation-protocol.md` and the applicable live or forensic template.
6. Decide packaging with `references/packaging-decision-gate.md` and `templates/decision-log.md`.
7. Update `docs/skill-review/tracker.md` if status changes.

## References

- `references/artifact-rubrics.md`
- `references/scout-sandbox-layout.md`
- `references/evaluation-protocol.md`
- `references/packaging-decision-gate.md`

## Templates

- `templates/inventory.md`
- `templates/analysis.md`
- `templates/eval-case.md`
- `templates/forensic-evaluation.md`
- `templates/decision-log.md`
