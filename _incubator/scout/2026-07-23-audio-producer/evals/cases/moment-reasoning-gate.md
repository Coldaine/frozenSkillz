# Eval Case: moment-reasoning-gate

Optional scout case only — **not** a three-way promotion eval. Use when manually checking the no-generate-without-record gate.

## Task

- User task prompt: "Do a sound pass on UI button clicks and one cannon fire moment in this Unity project."
- Target artifact paths: `source/audio-producer/SKILL.md`, `references/reasoning-record.md`, `references/generation.md`, `assets/example-walk-broadside.md` (worked evidence only)
- Expected output contract: Preflight notes; inventory entries; **six-field reasoning records complete before any ElevenLabs call**; silence proposals allowed; Master Log / checklist shapes if generation proceeds
- Environment notes and tool restrictions: may stub MCP if unavailable — then assert HALT/degrade behavior. Do not run promotion baseline/candidate/adapted triad.

## Variants

### Baseline Instructions

Generate two SFX prompts ad hoc and "attach later" without a reasoning record or master log.

### Candidate-Inspired Instructions

Follow scout skill: complete six-field records for each moment; reject generation on blank fields; use Broadside walk example only as shape reference.

### frozenSkillz-Adapted Instructions

Same as candidate after personal-lane landing (`~/.agents/skills/audio-producer/`); Broadside examples remain worked evidence.

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

- Run directory: `evals/runs/<YYYY-MM-DD>-moment-reasoning-gate/` (create when executed)
- Required files if run: `prompt.md`, `inputs.md`, `baseline-output.md`, `candidate-output.md`, `adapted-output.md`, `scorer-notes.md`
- Status: **case defined; run not required for this intake**
