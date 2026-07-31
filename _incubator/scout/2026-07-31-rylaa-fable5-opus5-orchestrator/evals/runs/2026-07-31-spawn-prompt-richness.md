# Eval run: does the ledger guard change spawn prompt richness?

Date: 2026-07-31
Runner: intake agent
Platform: Windows 11, Claude Code 2.1.220, Python 3.13.14 via `py -3`

## Question

Both the intake analysis and a second independent review predicted a **perverse incentive**: the spawn guard denies delegations whose prompt exceeds 1500 chars unless a ledger exists, so the friction gradient should push a model toward *shorter* spawn prompts — the opposite of the desired "say more when you delegate."

Does that happen?

## Method

Two sandbox projects, identical task, identical prompt:

> "Use subagents to fill in the three TODO sections of README.md (Setup, Usage, Config). Delegate the work."

| Arm | Setup |
|---|---|
| **Control** (`ctrl/`) | Passive `probe.py` only. Same `PreToolUse` matcher, logs `chars` per spawn, **never denies**. No `.workflow/`, no guard source in the project. |
| **Candidate** (`proj/`) | Real `ledger_guard_spawn.py` from the snapshot, wired project-scoped. No ledger pre-written. |

`source/` was never modified; hooks were copied to a scratch working copy. The only edit to the candidate was `python3` → `py -3` in the hook command.

## Results

**Control — no guard:**

```
Agent  1298 chars  general-purpose
Agent  1342 chars  general-purpose
Agent  1378 chars  general-purpose
```
mean ≈ **1339**

**Candidate — guard active:**

```
spawn_pass_over_threshold  1750 chars  Agent
spawn_pass_over_threshold  2036 chars  Agent
spawn_pass_over_threshold  2138 chars  Agent
```
mean ≈ **1975** (+47%)

Supporting runs (forced long prompts, to prove the gate opens and closes):

| Run | Condition | Result |
|---|---|---|
| A | >1800-char spawn, no ledger | **DENY**, reason surfaced verbatim to the model |
| B | same, ledger present | **PASS**, subagent dispatched and returned |

## Findings

1. **The predicted perverse incentive did not appear.** With the guard active, prompts got *richer*, not thinner (+47%). The model wrote `.workflow/LEDGER.md` unprompted before its first spawn, then cited it.

2. **The guard never actually fired in the natural run.** Zero `spawn_deny` events. All three spawns passed. The behavior change was *preemptive compliance*, not a response to being blocked.

3. **The threshold is mis-calibrated against default behavior.** Baseline spawns cluster at 1298–1378, entirely **below** the 1500 gate. On unmodified default behavior this guard would essentially never fire. As a *gate* it is close to inert; whatever value it produced here came from the model reading its intent, not from enforcement.

## Confounds — this is not a clean result

- **n = 1 per arm.** Three spawns each, one task, one model. Not statistically meaningful.
- **The candidate project contained more material to describe.** `proj/` held two guard scripts plus `.workflow/`; `ctrl/` held one probe script. Subagents documented the actual repo, so the candidate arm had genuinely more content to write about. This alone could inflate prompt length independent of any discipline effect. **This is the most serious confound and it is not controlled for.**
- **The guard's source was readable by the model** at `.claude/hooks/`. Preemptive compliance may be "model read a convention doc," not "guard imposed discipline." A real plugin install hides the script in a plugin dir, which would weaken the effect.
- Single task shape (documentation fill-in), which is unusually parallelizable.

## Conclusion

The direction of the effect contradicts the prediction, so the "polices verbosity, rewards reticence" critique is **not supported** by this run. But the confounds are large enough that the +47% cannot be attributed to the guard with any confidence.

The finding that *does* hold up, because it is a direct measurement rather than a comparison: **default spawn prompts sit below the guard's threshold**, so the hook as shipped would rarely trigger. That is consistent with the standing recommendation — the doctrine carries the value, the hook is near-inert at default settings — while arriving at it by a different route than predicted.

If this guard were ever adopted, the useful change is not to keep the 1500-char length gate but to invert it: check that a spawn prompt *contains* the required contract sections, rather than that it is short. Length is a poor proxy for the thing being protected.

## Reproduction

Sandboxes under `scratchpad/orch-sandbox/{proj,ctrl}/` (ephemeral). `probe.py` is reproduced below for reuse:

```python
# PreToolUse passive instrument: logs {tool, chars, subagent_type}, never denies.
# Matcher: ^(Agent|Task|Workflow|TaskCreate)$
# Reads hook JSON on stdin; appends one JSON line per spawn to $PROBE_LOG.
```
