# Scout Sandbox Layout

External repositories belong under `_incubator/scout/` until a recorded decision says otherwise.

## Required Shape

```text
_incubator/scout/<YYYY-MM-DD>-<repo>/
  README.md
  source/
  inventory.md
  analysis.md
  decisions.md
  evals/
    cases/
    runs/
  extracted-patterns/
```

## Path Rules

- `source/` contains the external snapshot and is read-only after import.
- `README.md` records provenance, source URL, commit, license, import date, and warnings.
- `inventory.md` lists artifacts and initial scope recommendations.
- `analysis.md` holds rubric scores and evaluator notes.
- `decisions.md` records packaging decisions and affected frozenSkillz paths; create it from `templates/decision-log.md` when starting a new scout.
- `evals/cases/` holds reusable eval case definitions.
- `evals/runs/` holds prompts, inputs, outputs, and scorer notes from executed evals.
- `extracted-patterns/` holds small adapted ideas, never raw wholesale source dumps.

## Naming

Use a stable, readable slug: `_incubator/scout/2026-07-01-owner-repo/`.

## Guardrails

- Do not put scout snapshots in `plugins/`.
- Do not edit files under `source/` to make them look better.
- Do not treat `extracted-patterns/` as active content.
- Do not delete provenance files when a pattern is promoted.
