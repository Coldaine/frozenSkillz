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

### Instrumentation — the two arms were not measured the same way

This is the design flaw that limits everything below, so it belongs here rather than in the
confound list.

The control arm was measured with `probe.py`, which logs **every** spawn it sees. The candidate
arm was measured with the guard's own `_metric()` output (`~/.claude/fable-orch/metrics.jsonl`),
because the guard was the hook installed in that arm. Those are not equivalent instruments.

`ledger_guard_spawn.py` returns at its length check *before* emitting any metric:

```python
limit = threshold()
if len(text) <= limit:
    return            # <- no metric is written
...
_metric("spawn_pass_over_threshold", ...)   # only reachable when len(text) > limit
```

So the candidate-arm log is **left-censored at 1500 characters**. Verified directly by running
the guard over synthetic payloads of 900 / 1400 / 1600 / 2100 chars with a ledger present: only
the 1600 and 2100 records appear in `metrics.jsonl`. The 900 and 1400 spawns passed silently and
left no trace at all.

Two consequences, both fatal to the comparison:

- The candidate mean **cannot be below 1501 by construction**, whatever the model actually did.
  Comparing it to an uncensored control mean is not a comparison of like with like.
- The hypothesis under test was that the guard drives prompts *shorter*. A shorter prompt in the
  candidate arm would be **invisible to this instrument**. The run could not have detected the
  effect it set out to look for.

The correct design would have been to run `probe.py` alongside the guard in the candidate arm, so
both arms were observed by the same uncensored instrument. That was not done.

## Results

**Control — no guard** (via `probe.py`, uncensored — this is a complete census of the arm):

```
Agent  1298 chars  general-purpose
Agent  1342 chars  general-purpose
Agent  1378 chars  general-purpose
```
mean ≈ **1339**

**Candidate — guard active** (via guard `_metric`, censored — over-threshold spawns only):

```
spawn_pass_over_threshold  1750 chars  Agent
spawn_pass_over_threshold  2036 chars  Agent
spawn_pass_over_threshold  2138 chars  Agent
```
mean ≈ 1975 over *the observed records*. **This is not comparable to the control mean** and the
"+47%" that an earlier draft of this document reported is withdrawn — see Instrumentation above.
Any spawn under 1500 chars in this arm would be absent from these three lines, so this is a
lower-bounded sample of unknown size, not a census.

Supporting runs (forced long prompts, to prove the gate opens and closes):

| Run | Condition | Result |
|---|---|---|
| A | >1800-char spawn, no ledger | **DENY**, reason surfaced verbatim to the model |
| B | same, ledger present | **PASS**, subagent dispatched and returned |

## Findings

Ordered by how much weight the evidence actually carries.

1. **The threshold is mis-calibrated against default behavior.** *(Solid — this is the one result
   that holds.)* Baseline spawns cluster at 1298–1378, entirely **below** the 1500 gate. This comes
   from the uncensored control instrument and is a direct measurement, not a comparison, so none of
   the problems below touch it. On unmodified default behavior this guard would essentially never
   fire. As a *gate* it is close to inert.

2. **The guard never issued a deny in the natural run.** *(Solid as stated.)* Zero `spawn_deny`
   events. The guard did execute and evaluate each observed spawn — `spawn_pass_over_threshold` is
   only emitted by a hook that ran — it simply passed them, because the model had written
   `.workflow/LEDGER.md` unprompted before its first spawn and cited it. Earlier wording here said
   the guard "never actually fired," which contradicted this document's own results table; it
   never *denied*. Note also that "all spawns passed" cannot be asserted as a census: sub-threshold
   spawns leave no record either way.

3. **Whether the guard changed prompt richness is UNRESOLVED.** *(No usable evidence.)* The
   candidate arm's instrument cannot observe prompts below the threshold, so it can neither confirm
   the predicted perverse incentive nor refute it. The apparent increase is consistent with a real
   effect, with the confounds below, and with pure measurement artifact, and this run cannot
   separate them. An earlier draft treated this as a refutation of the prediction. It is not one —
   the prediction remains untested.

4. **Preemptive compliance was observed, and is worth noting on its own.** The model wrote a ledger
   before its first spawn without being told to. That is a direct observation independent of any
   length measurement. Its cause is ambiguous — see the readable-source confound.

## Confounds — this is not a clean result

- **Censored candidate-arm instrument.** The largest problem, described under Instrumentation
  above. It is a design defect rather than a confound: it does not add noise to the comparison, it
  removes the comparison's validity.
- **n = 1 per arm.** Three spawns each, one task, one model. Not statistically meaningful.
- **The candidate project contained more material to describe.** `proj/` held two guard scripts plus `.workflow/`; `ctrl/` held one probe script. Subagents documented the actual repo, so the candidate arm had genuinely more content to write about. This alone could inflate prompt length independent of any discipline effect. **This is the most serious confound and it is not controlled for.**
- **The guard's source was readable by the model** at `.claude/hooks/`. Preemptive compliance may be "model read a convention doc," not "guard imposed discipline." A real plugin install hides the script in a plugin dir, which would weaken the effect.
- Single task shape (documentation fill-in), which is unusually parallelizable.

## Conclusion

**The comparative question is unanswered.** The "polices verbosity, rewards reticence" critique is
neither confirmed nor refuted here. The candidate arm was measured with an instrument blind to
exactly the outcome the prediction is about, so this run has nothing to say about it. An earlier
version of this document reported the comparison as a refutation of the prediction; that claim is
withdrawn.

The finding that *does* hold up, because it is a direct measurement from an uncensored instrument
rather than a comparison: **default spawn prompts sit below the guard's threshold** (1298–1378 vs a
1500 gate), so the hook as shipped would rarely trigger. Together with the portability result
below, that is what this run establishes.

That is enough to keep the standing recommendation — the doctrine carries the value, the hook is
near-inert at default settings — but it reaches it from the calibration measurement alone, not from
any demonstrated effect on prompt quality.

If this guard were ever adopted, the useful change is not to keep the 1500-char length gate but to invert it: check that a spawn prompt *contains* the required contract sections, rather than that it is short. Length is a poor proxy for the thing being protected.

## Status against the intake evaluation protocol

Recorded plainly so this run is not mistaken for a protocol-complete live eval.

- **Arms:** two (control, candidate). `references/evaluation-protocol.md` asks for three — the
  frozenSkillz-adapted arm was not run. Acceptable only because this run recommends no promotion.
- **Persistence:** this summary only. The protocol asks for a run *directory* holding `prompt.md`,
  `inputs.md`, per-arm outputs, and `scorer-notes.md`. The sandboxes and their raw `probe.jsonl` /
  `metrics.jsonl` were ephemeral and are gone; the counts above are transcribed, not re-derivable
  from anything in this repo.
- **Claim standard:** no comparative improvement claim is made or supported, so the shortfalls
  above do not put this run in conflict with the protocol's claim rules. They do mean it cannot
  later be cited as comparative evidence.

**This run does not discharge the promotion gate for a comparative claim.** It does establish
threshold calibration and portability, and it is sufficient to support the standing
*no-promotion* decision.

## Reproduction

The sandboxes lived under `scratchpad/orch-sandbox/{proj,ctrl}/` and were ephemeral — they no
longer exist, and neither do their raw logs.

The instrument itself is persisted at `../cases/probe.py` in this scout directory. It is a
`PreToolUse` hook with matcher `^(Agent|Task|Workflow|TaskCreate)$` that reads hook JSON on stdin
and appends one `{tool, chars, subagent_type}` line per spawn to `$PROBE_LOG`, never denying.
Wire it with:

```json
{ "PreToolUse": [ { "matcher": "^(Agent|Task|Workflow|TaskCreate)$",
  "hooks": [ { "type": "command", "command": "py -3 /path/to/probe.py" } ] } ] }
```

**If this run is ever repeated, install `probe.py` in _both_ arms.** The guard's own metrics log is
not a usable measurement instrument for prompt length, because it is blind below the threshold.
