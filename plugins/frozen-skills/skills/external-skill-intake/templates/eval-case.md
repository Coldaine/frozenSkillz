# Eval Case: <case-slug>

## Task

- User task prompt:
- Target artifact paths:
- Expected output contract:

## Variants

### Baseline Instructions

<instructions without candidate material>

### Candidate-Inspired Instructions

<instructions using candidate material>

### frozenSkillz-Adapted Instructions

<instructions using adapted repo-owned material>

## Scoring Rubric

| Criterion | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| Task completion | Fails core task | Partial | Complete |
| Specificity and usefulness | Generic | Some useful detail | Directly actionable |
| Safety and secret hygiene | Unsafe | Some gaps | Safe by default |
| Portability | Locked | Partly portable | Portable or scoped honestly |
| Maintainability | Hard to maintain | Moderate | Low burden |
| Output contract compliance | Misses contract | Partial | Fully matches |
| Improvement over baseline | Worse | Mixed | Clear improvement |

## Run Storage

- Run directory: `evals/runs/<YYYY-MM-DD>-<case-slug>/`
- Required files: `prompt.md`, `inputs.md`, `baseline-output.md`, `candidate-output.md`, `adapted-output.md`, `scorer-notes.md`.
