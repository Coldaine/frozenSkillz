# Packaging Decision Gate

Every scoped artifact must receive one packaging decision before promotion, deferment, or discard.

## Decision Options

### Whole Import

Use only when the artifact is already portable, safe, well-scoped, licensed for reuse, and fits the active plugin shape. Record why adaptation is not needed.

### Adapt Concept Only

Use when the idea is valuable but the source is too project-specific, verbose, unsafe, stale, or tool-specific. This is the default preferred outcome.

### Merge Into Existing Skill

Use when the concept strengthens an existing skill, reference, workflow, or template without needing a new active skill.

### Incubate For Later

Use when the idea may be useful but needs more evals, upstream verification, license review, or product direction.

### Discard

Use when the artifact is low quality, unsafe, duplicative, stale, out of scope, or not worth maintaining.

## Required Rationale

Each decision must include:

- Artifact paths.
- Decision option.
- Evidence from inventory.
- Rubric score summary.
- Evaluation evidence and mode, if applicable.
- Safety and maintenance notes.
- Affected frozenSkillz paths.
- Follow-up owner or `none`.

## Promotion Checklist

- Adapted files are outside scout `source/`.
- Active `SKILL.md` remains lean.
- Heavy detail lives in `references/`, `templates/`, or `docs/workflows/`.
- Manifest versions and `skills[].path` entries are updated if a skill becomes active.
- `docs/skill-review/tracker.md` reflects the state change.
