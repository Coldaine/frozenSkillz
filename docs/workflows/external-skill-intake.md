# External Skill Intake Workflow

Use this workflow when evaluating external skill, plugin, agent, command, hook, config, template, eval, or documentation-pattern repos for possible frozenSkillz adoption.

The goal is to learn from external work without turning active marketplace content into a junk drawer. External source stays sandboxed until a scored decision says what to do with it.

## Required Order

1. Snapshot the candidate into `_incubator/scout/<YYYY-MM-DD>-<repo>/source/` or inspect an existing scout snapshot.
2. Create or update scout metadata outside `source/`: `README.md`, `inventory.md`, `analysis.md`, `decisions.md`, and optional eval files.
3. Inventory artifacts before judging them.
4. Select a narrow scope for evaluation.
5. Score scoped artifacts with artifact-specific rubrics.
6. Complete at least one live or forensic evaluation before recommending any large pattern for promotion.
7. Record packaging decisions with rationale and affected paths.
8. Promote only adapted, reviewed output into `plugins/`, `docs/`, or another active location.

## Non-Negotiables

- Do not import external repos directly into `plugins/`.
- Do not modify files under a scout `source/` directory.
- Match claims to the evaluation mode and its evidence. Comparative improvement claims require persisted live outputs and scorer notes.
- Do not promote directly from scout source. Adapt the concept into frozenSkillz-owned files.
- Do not add scripts for intake v1 unless repeated manual pain has been observed and documented.
- Do not commit secrets, local client caches, or generated runtime state.

## Snapshot

Create a scout directory with this shape:

```text
_incubator/scout/<YYYY-MM-DD>-<repo>/
  README.md
  source/
  inventory.md
  analysis.md
  decisions.md
  evals/cases/
  evals/runs/
  evals/forensic/
  extracted-patterns/
```

`source/` is read-only evidence. Put notes, reductions, adapted snippets, evals, and decisions outside `source/`.

## Inventory

Create `inventory.md` before analysis. Include:

- Source URL, commit, import date, license, and any known provenance concerns.
- Artifact counts by type: skill, agent, command, hook, config, template, eval-case, documentation-pattern.
- Paths that appear useful, risky, duplicate, stale, or project-specific.
- External dependencies, required tools, secret surfaces, and platform assumptions.
- Initial scope recommendation: evaluate, defer, discard, or needs more evidence.

## Scope Selection

Pick a narrow scope before scoring. Good scopes are concrete, such as one agent handoff pattern, one eval format, one hook safety behavior, or one documentation pattern.

Reject broad scopes like "import the whole repo" unless every artifact class has been inventoried, scored, and evaluated.

## Rubric Scoring

Use `plugins/frozen-skills/skills/external-skill-intake/references/artifact-rubrics.md`.

For each scoped artifact, record:

- Artifact path.
- Artifact type.
- Scores from 1 to 5 for each applicable dimension.
- Short rationale for each score.
- `N/A` only where structurally inapplicable.
- Summary recommendation.

## Live or Forensic Evaluations

Use `plugins/frozen-skills/skills/external-skill-intake/references/evaluation-protocol.md`.

Use a **live evaluation** when the decision depends on exercising candidate behavior or comparing
outputs. A live case compares:

- Baseline output without candidate material.
- Candidate-inspired output using the external pattern.
- frozenSkillz-adapted output using a repo-owned adaptation.

Persist prompts, inputs, outputs, and scorer notes under `evals/runs/`.

Use a **forensic evaluation** when real agents or users have already produced relevant evidence.
Inspect transcripts, issue reproductions, code history, maintainer confirmations, tests, and release
notes. Persist findings under `evals/forensic/` with source, version and harness when known,
current-versus-historical status, corroboration, and confidence.

Do not invent a sandbox run when forensic evidence answers the question. Do not use forensic
evidence alone to claim comparative improvement over a baseline.

## Decision Log

Use `decisions.md` or the decision-log template. Each decision must include:

- Date and reviewer.
- Candidate artifact paths.
- Chosen packaging outcome.
- Rationale grounded in inventory, rubric scores, and the applicable evaluations.
- Affected frozenSkillz paths.
- Follow-up work and owner, if any.

## Packaging Outcomes

Use `plugins/frozen-skills/skills/external-skill-intake/references/packaging-decision-gate.md`.

Allowed outcomes:

- Whole import.
- Adapt concept only.
- Merge into existing skill.
- Incubate for later.
- Discard.

Whole import is rare. Prefer adapting concepts into the repo's existing skill, workflow, or reference structure.

## Promotion Path

When a candidate passes the gate:

1. Create frozenSkillz-owned files outside scout `source/`.
2. Keep active `SKILL.md` files lean and route heavy detail to `references/` and `templates/`.
3. Update plugin manifests and versions if adding an active skill.
4. Update `docs/skill-review/tracker.md`.
5. Validate JSON manifests and every `skills[].path`.
6. Run `git diff --check` and any relevant repo validation.

## Related Files

- `AGENTS.md` routes agents to this workflow.
- `docs/skill-review/tracker.md` records active, gated, and scout status.
- `docs/skill-corpus-analysis/corpus-intake-rubric.md` contains the earlier SKILL.md-centered rubric.
- `docs/skill-corpus-analysis/corpus-analysis-deliverables.md` shows scoring/reporting examples.
- `plugins/frozen-skills/skills/external-skill-intake/SKILL.md` is the loadable skill entrypoint.
