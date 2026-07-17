# Eval Case: prototype-or-tracer

## Task

- User task prompt: A team is adding a third-party water renderer to an existing Unity project. Package compatibility and persistence behavior are uncertain, but the existing analytic water path works and feature implementation should continue. Choose between research only, a disposable prototype, and a retained tracer-bullet slice. Define the next 24 hours of work without turning every uncertainty into a test gate.
- Target artifact paths: source/pragmatic-programmer/SKILL.md and source/pragmatic-programmer/references/tracer-bullets.md
- Expected output contract: choose one primary technique, explain why the other two are not primary, define a thin scope, say what continues in parallel, define what is kept or thrown away, and name the observation that changes the decision.
- Environment notes and tool restrictions: use a fixed project summary and package manifest fixture; web research is allowed; no live package installation or project mutation.

## Variants

### Baseline Instructions

Answer using ordinary engineering judgment. Do not load candidate or adapted
instructions.

### Candidate-Inspired Instructions

Load the snapshotted pragmatic-programmer skill and its tracer-bullets reference.
Apply its diagnostic and prototype/tracer guidance without silently omitting
mandatory candidate behavior.

### frozenSkillz-Adapted Instructions

Classify the uncertainty first. Use primary-source research for known facts, a
disposable isolated prototype for one-piece feasibility, and a retained tracer
only for end-to-end integration risk. Keep independent implementation moving.
Do not add permanent checks until the behavior and contract are understood.

## Scoring Rubric

| Criterion | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| Task completion | No choice or work path | Partial choice | One executable primary path plus parallel work |
| Specificity and usefulness | Generic methodology | Some scoped steps | Exact slice, evidence, disposition, and decision trigger |
| Safety and secret hygiene | Experiments in production state | Some isolation | Disposable work and data boundaries are explicit |
| Portability | Assumes one toolchain | Partly generic | Technique is portable and Unity constraints are scoped honestly |
| Maintainability | Adds broad permanent process | Moderate | Minimal durable process for stable behavior only |
| Output contract compliance | Misses contract | Partial | Fully matches |
| Improvement over baseline | Worse or more ceremonial | Mixed | Faster credible learning and visible progress |

## Run Storage

- Run directory: evals/runs/<YYYY-MM-DD>-prototype-or-tracer/
- Required files: prompt.md, inputs.md, baseline-output.md, candidate-output.md, adapted-output.md, scorer-notes.md.
