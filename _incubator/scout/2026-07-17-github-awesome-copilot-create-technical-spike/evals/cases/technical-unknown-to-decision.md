# Eval Case: technical-unknown-to-decision

## Task

- User task prompt: A Unity team receives portrait or flat-color images from its editor capture automation even though the camera is composed for 16:9. The team must keep implementing while this uncertainty is investigated. Recommend and, where read-only tools allow, perform the cheapest credible investigation that leads to a concrete next action. Do not change project files.
- Target artifact paths: source/skills/create-technical-spike/SKILL.md
- Expected output contract: state the single consequential question, evidence inspected, at most three candidate approaches, the next discriminating action, a timebox, and whether implementation can continue in parallel. Do not create a document merely to restate the prompt.
- Environment notes and tool restrictions: use a fixed fixture repository and captured tool inventory; web research is allowed; project writes and dependency installation are forbidden.

## Variants

### Baseline Instructions

Answer using ordinary engineering judgment. Do not load candidate or adapted
instructions.

### Candidate-Inspired Instructions

Apply the snapshotted create-technical-spike skill exactly. If its host-specific
tool names are unavailable, record the mismatch rather than silently replacing
them.

### frozenSkillz-Adapted Instructions

Use the candidate's one-question, evidence-first spike idea, but optimize for
time-to-decision: inspect local facts and primary sources in parallel, prototype
only the residual unknown, keep unrelated implementation moving, and create a
durable spike document only when the decision needs a lasting record.

## Scoring Rubric

| Criterion | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| Task completion | No decision path | Partial investigation | Concrete evidence-backed next action |
| Specificity and usefulness | Generic process prose | Some concrete steps | Names exact evidence, candidates, owner, and timebox |
| Safety and secret hygiene | Mutates or exposes data | Some gaps | Read-only boundaries are respected |
| Portability | Requires missing host tools | Workarounds are implicit | Host assumptions are explicit and replaceable |
| Maintainability | Produces needless ceremony | Moderate artifact burden | Durable output only where it earns its cost |
| Output contract compliance | Misses contract | Partial | Fully matches |
| Improvement over baseline | Worse or slower | Mixed | Faster learning with a better decision |

## Run Storage

- Run directory: evals/runs/<YYYY-MM-DD>-technical-unknown-to-decision/
- Required files: prompt.md, inputs.md, baseline-output.md, candidate-output.md, adapted-output.md, scorer-notes.md.
