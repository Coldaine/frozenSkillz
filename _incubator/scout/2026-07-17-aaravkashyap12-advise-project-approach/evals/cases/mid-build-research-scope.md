# Eval Case: mid-build-research-scope

## Task

- User task prompt: A small team is midway through a Unity naval tactics prototype. It must choose how to automate editor screenshots and scene verification while implementation continues. Inspect the supplied project fixture and research current official or primary-source approaches. Recommend the smallest credible path and state when that recommendation becomes wrong.
- Target artifact paths: source/skills/advise-project-approach/SKILL.md and source/skills/advise-project-approach/agents/openai.yaml
- Expected output contract: state evidence status and inspection scope; identify the consequential unknown; compare two or three credible approaches with primary sources; distinguish transferable and non-transferable patterns; recommend one next action, parallel work, and failure conditions. Avoid an unrelated whole-project review.
- Environment notes and tool restrictions: use a fixed medium-repository fixture; browsing is available; sources and observations must be dated; no file mutation, installation, or paid agent sessions.

## Variants

### Baseline Instructions

Answer using ordinary engineering judgment. Do not load candidate or adapted
instructions.

### Candidate-Inspired Instructions

Apply the snapshotted advise-project-approach skill exactly in mid-build mode,
including its evidence, comparable, freshness, tradeoff, and output rules.

### frozenSkillz-Adapted Instructions

Use a lean mid-build research router: map the local constraint, fan out primary
source and comparable research, stop when evidence discriminates between
candidates, recommend the smallest path, and keep independent implementation
moving. Load pricing, security, or full project-review references only if the
question actually depends on them.

## Scoring Rubric

| Criterion | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| Task completion | No credible recommendation | Partial | Evidence-backed next action and parallel path |
| Specificity and usefulness | Generic stack advice | Some concrete evidence | Exact local facts, sources, tradeoffs, and failure conditions |
| Safety and secret hygiene | Reads or mutates sensitive state | Some gaps | Read-only and secret boundaries are respected |
| Portability | Assumes one host | Partly portable | Host/tool assumptions are explicit and separable |
| Maintainability | Full-review ceremony for one unknown | Moderate | Progressive disclosure and bounded research |
| Output contract compliance | Misses contract | Partial | Fully matches without scope spill |
| Improvement over baseline | Worse or much slower | Mixed | Better decision with proportionate effort |

## Run Storage

- Run directory: evals/runs/<YYYY-MM-DD>-mid-build-research-scope/
- Required files: prompt.md, inputs.md, baseline-output.md, candidate-output.md, adapted-output.md, scorer-notes.md.
