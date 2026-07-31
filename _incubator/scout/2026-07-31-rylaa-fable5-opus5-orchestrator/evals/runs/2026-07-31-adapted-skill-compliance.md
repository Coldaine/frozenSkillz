# Eval run: does the adapted skill change delegation behavior?

Date: 2026-07-31
Runner: intake agent
Platform: Windows 11, Claude Code 2.1.220

This is the **frozenSkillz-adapted arm** that `docs/workflows/external-skill-intake.md` asks for alongside baseline and candidate-inspired. The candidate-inspired arm is in `2026-07-31-spawn-prompt-richness.md`, whose comparative result was withdrawn for instrument censoring.

## What was tested

`plugins/frozen-skills/skills/delegation-contract/` — the adapted doctrine, installed project-scoped. No hooks, no tmux, no enforcement of any kind. The skill is loadable text and nothing else.

## Method

Identical task and prompt to the earlier control arm, so the two are directly comparable:

> "Use subagents to fill in the three TODO sections of README.md (Setup, Usage, Config). Delegate the work."

**Instrument fix applied.** The previous run's fatal defect was measuring the two arms with different instruments, one of them censored below the guard threshold. Here **both arms use the same passive `probe.py`**, which logs every spawn regardless of size and never denies. The probe was additionally extended to capture **full prompt text**, not just character counts — length was never the interesting variable.

The skill was not named in the prompt. It had to be selected on its own description.

## Results

**Control arm — no skill** (uncensored probe, complete census):

```
3 spawns:  1298, 1342, 1378 chars   no contract structure
```

**Adapted arm — skill available** (same instrument, complete census):

```
6 spawns:  3073, 2813, 3116, 3012, 2417, 2143 chars
field coverage: 7/7 on all six spawns
```

Field detection was by regex over the prompt text, then **manually verified by reading spawn 1 in full** — because a regex cannot distinguish a filled field from an empty heading, and the skill itself warns about exactly that. The content was substantive:

- *Objective* carried the downstream use — "I will assemble the final README myself from your draft plus two siblings."
- *Ledger items* carried a real why — "a generic Setup section (npm install, virtualenv) would be actively wrong and misleading."
- *Context you can't infer* carried genuinely non-inferable material — that the repo is a sandbox for testing agent workflows rather than a shipping app.
- *Out of scope* was concrete — "do not touch README.md directly."

## Findings

1. **The seven fields appeared, with substance, on every spawn.** *(Solid.)* 6/6 by regex, spot-verified by reading. The control arm produced no contract structure at all.

2. **The single-writer rule held.** *(Solid — the most important result.)* Three read-only workers drafted to `.workflow/scratch/`; the orchestrator assembled the README itself as sole writer. In the control arm, three subagents each wrote directly to the file. This is rule 1 of the skill, is the structural divergence from the source plugin's parallel-worktree-editor pattern, and is the one thing a send-side contract cannot achieve on its own.

3. **Workers were told about their siblings.** *(Solid, and not something the skill explicitly requires.)* Spawn 1 names the two parallel drafters. That is coordination context reaching a worker at t=0 — a partial hedge against the misalignment band, arrived at without being asked for.

4. **Verification ran and caught real errors.** Three cycles (the contract's cap), finding two factual inaccuracies: a Setup section that misdescribed the repo contents, and a self-contradictory sentence about git history. Both fixed; cycle 3 clean.

5. **The skill was selected without being named.** Its description matched the task unprompted.

## Costs, stated plainly

- **2× the spawns** — 6 vs 3, because verification cycles are additional agent invocations.
- **~2× the prompt size** — mean ≈ 2762 vs ≈ 1339 chars. More context per spawn, deliberately.

So this doctrine is not free. It roughly doubles agent invocations and per-spawn tokens on a task this size. Whether that trade is worth it depends on the cost of a defect surviving the handoff.

## Limits — what this does NOT establish

- **n = 1 per arm.** One task, one model, one session each.
- **Compliance was measured, not outcome quality.** The README produced under the skill was *not* shown to be better than the control's. Finding 4 is suggestive but uncontrolled: the control arm had no verification step at all, so of course it caught nothing. That is a difference in procedure, not a demonstrated quality delta.
- **Single task shape** — documentation fill-in, unusually parallelizable, and unusually forgiving of a bad handoff. A task with real interdependencies would stress the contract far harder.
- **Field presence is a weak proxy.** Verified by reading one prompt of six. The other five were regex-matched only.

## Conclusion

The adapted skill **changes delegation behavior in the intended direction**, on one task, measured with a single uncensored instrument across both arms. The contract fields appear with real content, and — more importantly — the topology rule held, keeping writes single-threaded where the control fanned them out.

What remains untested is whether any of that produces **better work**. That would need a task with a known-correct answer and a scorer blind to the arm. This run does not attempt it, and no claim of quality improvement should be cited from it.
