# Live or Forensic Evaluation Protocol

Complete an evaluation before recommending promotion of a large external pattern. Choose the mode
that matches the available evidence and the claim being decided.

## Mode Selection

Use a **live evaluation** when you must execute candidate behavior, compare alternative outputs, or
establish improvement over a baseline.

Use a **forensic evaluation** when real agents or users have already exercised the behavior and the
question can be answered from durable evidence such as transcripts, issue reproductions, code
history, maintainer confirmations, tests, or release notes.

Do not require a synthetic run merely because the evidence was produced outside the current intake.
Do not describe source review or anecdotes as measured comparative performance.

## Live Evaluation

Each live case compares three outputs:

1. Baseline: agent output without candidate material.
2. Candidate-inspired: output using the external pattern or instructions.
3. frozenSkillz-adapted: output using an adapted repo-owned version of the idea.

Each case records:

- user task prompt;
- target artifact paths;
- baseline, candidate-inspired, and frozenSkillz-adapted instructions;
- expected output contract;
- scoring rubric;
- environment notes and tool restrictions.

Persist each run under `evals/runs/<YYYY-MM-DD>-<case-slug>/` with:

- `prompt.md`;
- `inputs.md` or linked fixture paths;
- `baseline-output.md`;
- `candidate-output.md`;
- `adapted-output.md`;
- `scorer-notes.md`;
- environment notes and tool restrictions.

Score task completion, usefulness, safety, portability, maintainability, output-contract compliance,
and improvement over baseline from 1 to 5 with rationale.

## Forensic Evaluation

Store each finding in `evals/forensic/<YYYY-MM-DD>-<finding-slug>.md`. Record:

- the precise claim being evaluated;
- source URL or repository path;
- source type and capture date;
- affected artifact, version, harness, model, and operating system when known;
- observed behavior and reproduction details;
- status: `current`, `fixed`, `historical`, `unresolved`, or `unclear`;
- corroborating and contradicting evidence;
- confidence: `strong`, `moderate`, or `limited`;
- the decision this evidence can and cannot support.

Prefer evidence in this order:

1. Direct transcript, reproducible artifact, or executable test tied to a version.
2. Reproduction corroborated by code history, a maintainer, or a fix commit.
3. Multiple independent reports describing the same behavior.
4. A single uncorroborated report or interpretation.

Lower-ranked evidence remains useful when labeled honestly. A fixed historical defect is evidence of
past behavior and maintenance response, not proof that the current version still fails.

## Claim Standard

- Comparative improvement claims require live comparative evidence.
- Intent, actual behavior, regressions, failure modes, maintenance response, and unresolved risk may
  be established forensically.
- Every conclusion must stay within the versions, harnesses, and conditions supported by its sources.
- Conflicting evidence stays visible; do not average disagreement into false certainty.
