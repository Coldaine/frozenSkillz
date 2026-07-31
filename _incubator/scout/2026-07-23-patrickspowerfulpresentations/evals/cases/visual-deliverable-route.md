# Eval Case: visual-deliverable-route

Optional scout case only — **not** a three-way promotion eval. Use when manually checking Phase 0–1 routing.

## Task

- User task prompt: "Build me an interactive explorer comparing three Kubernetes MCP servers for local agent use — I need to pick one."
- Target artifact paths: `source/patrickspowerfulpresentations/SKILL.md`, `references/domains/comparison.md`, `references/domains/buying.md`, `references/techniques/charts.md`, `references/techniques/evidence.md`
- Expected output contract: Phase 0 qualifies as visual deliverable; Phase 1 writes `_ppp/plan.md` naming route (comparison or buying), medium, tier, unit of analysis, page map, chart manifest, visual thesis — **no layout code before dossier**
- Environment notes and tool restrictions: no need to complete full build for this case; stop after plan (or plan+dossier schema check). Do not run promotion baseline/candidate/adapted triad.

## Variants

### Baseline Instructions

Answer the comparison in chat prose or a short markdown table without invoking the skill phases.

### Candidate-Inspired Instructions

Follow the scout `SKILL.md` read path: load comparison (+ buying if decision), evidence, visual-thesis; write `_ppp/plan.md` only.

### frozenSkillz-Adapted Instructions

Same as candidate after personal-lane landing (`~/.agents/skills/patrickspowerfulpresentations/`); adaptation this pass is identical tree, not a rewrite.

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

- Run directory: `evals/runs/<YYYY-MM-DD>-visual-deliverable-route/` (create when executed)
- Required files if run: `prompt.md`, `inputs.md`, `baseline-output.md`, `candidate-output.md`, `adapted-output.md`, `scorer-notes.md`
- Status: **case defined; run not required for this intake**
