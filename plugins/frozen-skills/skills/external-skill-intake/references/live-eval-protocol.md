# Live Eval Protocol

Run a live eval before recommending promotion of any large external pattern.

## Eval Variants

Each eval case compares three outputs:

1. Baseline: agent output without candidate material.
2. Candidate-inspired: output using the external pattern or instructions.
3. frozenSkillz-adapted: output using an adapted repo-owned version of the idea.

## Required Case Fields

- User task prompt.
- Target artifact paths.
- Baseline instructions.
- Candidate-inspired instructions.
- frozenSkillz-adapted instructions.
- Expected output contract.
- Scoring rubric.
- Environment notes and tool restrictions.

## Required Run Artifacts

Persist each run under `evals/runs/<YYYY-MM-DD>-<case-slug>/` with:

- `prompt.md`.
- `inputs.md` or linked fixture paths.
- `baseline-output.md`.
- `candidate-output.md`.
- `adapted-output.md`.
- `scorer-notes.md`.

## Scoring Criteria

Score 1 to 5 with rationale:

- Task completion.
- Specificity and usefulness.
- Safety and secret hygiene.
- Portability.
- Maintainability.
- Output contract compliance.
- Improvement over baseline.

## Claim Standard

Only claim an external pattern improves outcomes when the adapted output beats baseline on meaningful dimensions and does not introduce unacceptable safety or maintenance risk.
