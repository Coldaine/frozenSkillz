# Delegation Handoff Contract

Adapted pattern, not active content. Mirrors the candidate's *return* contract with the *send* contract it never wrote.

The candidate defines rigorously what a worker owes the chair (five parts, ≤40 lines, rejected and re-run if violated) and says almost nothing about what the chair owes a worker — "phases cite item numbers," and send "workers with specs" without ever defining a spec. This is that definition.

## First principle: you are briefing an agent, not calling a function

Everything below follows from this, and the fields are worthless without it. A spawn prompt is not an argument list. The thing receiving it reasons, chooses, and will encounter your task differently than you imagined it.

Seven consequences, each of which is why one of the fields exists:

- **It needs intent, not just instructions.** An agent that knows *why* adapts when reality contradicts your assumption. One that knows only *what* executes your plan off a cliff and reports success. Give it the reasoning and it can defend the goal when the steps stop applying.
- **You cannot enumerate the branches.** It will hit situations you did not foresee — that is the normal case, not the failure case. What it needs is not more steps but a rule for the unforeseen: proceed on judgment, or come back and ask.
- **It can tell you it doesn't know — if you invite it.** The candidate's return contract already asks for "uncertain because X." That only works if uncertainty is treated as a valid deliverable. A worker that never reports doubt is not confident, it is guessing quietly.
- **Over-scripting destroys the thing you're paying for.** Listing steps it could derive wastes its judgment and makes it brittle the moment a step doesn't fit. Specify the destination and the constraints; let it choose the route.
- **It cannot ask about what it cannot see.** Absence is invisible. It will never think to ask about the approach you rejected last month, because nothing in the repo hints that a decision was ever made.
- **Competence expands into any space you leave unbounded.** A good agent that notices adjacent breakage will helpfully fix it — into another worker's files, or into a decision that was yours.
- **It is not deterministic.** Run the same prompt twice and you get different work, both plausibly correct. So the prompt must carry the *invariants* — what has to be true regardless of which path it takes — rather than a path you expect it to reproduce.

The test for a spawn prompt is not "does it have all seven sections." It is: **if this worker makes a reasonable decision I did not anticipate, does it have what it needs to make a good one?**

## The rule

Every spawn of a substantive worker carries all seven fields below — not as a form, but because each closes one of the gaps above. A spawn missing any of them is underspecified: fix it before sending, don't hope the worker infers.

Sub-minute lookups — one grep, one read, one fetch — are exempt. They are not delegations, they are remote-controlled tool calls, and the distinction matters: the exemption exists precisely because nothing is being *judged*.

## The seven fields

**1 · Objective, and what you'll do with the result.** One sentence, the finished state, not the activity. "Auth middleware rejects expired tokens with 401 and a structured body" — not "look at the auth middleware." A worker that cannot tell when it is done will either stop early or never stop.

State the downstream use too: *"Find where auth is implemented; I need the pattern to add OAuth"* beats *"search for auth files."* Knowing what the answer feeds lets the worker judge what counts as relevant — a judgment you cannot pre-encode as a step.

**2 · Ledger items, with the why.** Cite the item numbers this worker owns *and* restate the reasoning behind them. Ledger lines are one-line checkboxes; they carry the WHAT and almost never the WHY. The item says "reject expired tokens." The why — "a prior incident let 30-day-stale tokens through and we chose explicit rejection over silent refresh" — is what stops the worker from solving it the wrong way. **This is the field most often dropped and the one that most often causes rework.**

**3 · Context the worker cannot infer.** Anything decided in conversation, rejected earlier, or true-but-unwritten. Constraints that exist for reasons not visible in the code. Approaches already tried and abandoned, and why. A worker starts with the repo and your prompt — nothing else. Everything you know that the repo does not say is invisible to it unless you write it here.

**4 · Where to look — and what to skip.** Concrete entry points: paths, symbols, commands, URLs, the ledger path, prior work-product paths. Not "the auth code" but `src/middleware/auth.ts` and `tests/auth/expiry.test.ts`. Save the worker the rediscovery you have already paid for.

Name the dead ends too — the source that looks authoritative and is stale, the tool that will time out, the directory that is vendored. Steering *away* is as cheap to write and saves as much as steering toward.

**5 · Out of scope.** State explicitly what NOT to touch. Adjacent code that looks broken but is deliberate. Refactors that are someone else's phase. Files another parallel worker owns right now. Without this, a capable worker will helpfully expand until it collides with a sibling or with a decision you already made.

**6 · Expected output, with a size bound.** What you need back to make the next decision — a diff, a brief, a verdict, a path. Point at the return contract rather than restating it. If the shape is unusual, say so here.

Bound it: *"return only the failing tests with their error messages"* beats *"report the test run."* Say who consumes it, and that it is not addressing the user — a worker unsure of its audience writes a status update instead of a deliverable.

**7 · Authority.** What the worker may decide alone versus what it must return for a ruling. "Pick the error-message wording; do not change the status code without asking." Silence here produces one of two failures: a worker that stalls on trivia, or one that quietly makes a call that was yours.

## Why this and not a length rule

The candidate gates spawns on prompt length — over 1500 characters and it demands a ledger. To be fair to it, this is not a limit on verbosity: length is being used as a cheap proxy for *"is this a serious delegation?"* Nobody is arguing that long prompts are bad.

It is still the wrong instrument, for two reasons. Measured against default behavior, spawn prompts land at roughly 1300 characters — under the gate — so it rarely fires at all (`../evals/runs/2026-07-31-spawn-prompt-richness.md`, control arm: 1298 / 1342 / 1378). And more fundamentally, size tells you nothing about whether the recipient can exercise judgment well. A 2,000-character prompt that is all restated background with no authority boundary leaves an agent *less* able to handle surprise than an 800-character one carrying all seven fields. The question is never how much you wrote; it is whether what you wrote survives the worker doing something you didn't script.

If any of this is ever mechanized, check for the fields, not the size. Note the honest limit of doing so: presence of a heading is not presence of content, and the candidate's own author warned that mechanizing further "invites ritual compliance." A field check is a floor on effort, not a quality bar. It is still worth having, because it is checked when the prompt is written rather than self-marked afterward, and filling a field honestly costs barely more than faking it.

## Worked example

> **Objective.** `POST /sessions` rejects expired refresh tokens with 401 and `{error:"token_expired"}`; unexpired behavior unchanged.
>
> **Ledger items.** Covers 4 and 5. Why: incident 2026-06-11 — stale tokens up to 30 days old were silently refreshed. We chose explicit rejection over silent refresh so clients see the failure and re-auth; silent refresh hid the problem for six weeks.
>
> **Context you can't infer.** We tried a sliding-window refresh in June and reverted it — it made session length unpredictable for the mobile client. Don't reintroduce it. The 30-day figure comes from the incident, not from config.
>
> **Where to look.** `src/middleware/auth.ts` (`verifyRefresh`), tests in `tests/auth/expiry.test.ts`. Ledger at `.workflow/LEDGER.md`.
>
> **Out of scope.** Don't touch access-token TTL — that's phase 3, another worker holds it. `src/legacy/session_v1.ts` looks wrong and is deliberately frozen.
>
> **Expected output.** Diff plus the standard return contract. Note any call site that assumed refresh never fails.
>
> **Authority.** Yours: error wording, test structure, where the check sits in the middleware chain. Mine: the status code, the error key, anything touching token TTL.

## Evidence

### The failure data says specification is the biggest single category

[Cemri et al., *Why Do Multi-Agent LLM Systems Fail?*](https://arxiv.org/abs/2503.13657) (NeurIPS 2025, Datasets & Benchmarks) is the strongest empirical grounding available: 1,600+ annotated execution traces across 7 multi-agent frameworks, taxonomy built from 150 traces with κ = 0.88 inter-annotator agreement. It produces 14 failure modes in 3 categories:

| Category | Share | Addressed by |
|---|---:|---|
| Specification & system design | **41.8%** | this contract |
| Inter-agent misalignment | **36.9%** | **not this contract** — see below |
| Task verification | **21.3%** | the candidate's fresh-eyes verifier + `V.` item |

Their headline conclusion is that failures "stem from poor system design, not model performance" — agents operating on incorrect assumptions, ignoring peer input, failing to verify. Roughly **79% traces to bad specification plus broken coordination.** That is direct empirical support for treating the send-side briefing as load-bearing rather than incidental, and it is the reason this document exists.

### Vendor guidance converges on the same fields

Anthropic's [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) writeup reports **objective + output format + tool guidance + task boundaries** as their largest single quality lift, with vague instructions causing duplication and silent gaps. Those map to fields 1, 6, 4, 5. Fields **2 (the why), 3 (non-inferable context), 7 (authority)** are additions here.

Field 7 is corroborated independently: give subordinates "autonomy within clear boundaries, only escalating on failures or ambiguous requirements" ([Osmani](https://addyosmani.com/blog/code-agent-orchestra/)); a micromanaging supervisor becomes the bottleneck.

The mechanical justification for field 3: a subagent begins with a **fresh, isolated context window** — no conversation history, no prior reads, no earlier tool results. The delegation string is its entire briefing.

## What this contract does NOT fix

The strongest objection comes from [Cognition, *Don't Build Multi-Agents*](https://cognition.com/blog/dont-build-multi-agents), and it lands squarely on the limits of this document:

> Even if you give each sub-agent the full initial task description, they won't have each other's ongoing intermediate decisions or assumptions.

That is correct, and no send-side contract can fix it. **This contract is a briefing at t=0.** Inter-agent misalignment — the 36.9% band above — happens at t>0, when parallel workers make assumptions their siblings never see. A perfect prompt does not transfer a decision that has not been made yet.

So: writing all seven fields well should reduce the 41.8% specification band. It will do close to nothing for the 36.9% misalignment band. Claiming otherwise would be the same overreach as claiming a ledger's existence proves its fidelity.

Cognition's answer is architectural, not prompt-level — share full agent traces rather than individual messages, and keep **writes single-threaded** while letting multiple agents contribute intelligence. That is worth reading against the candidate, which does both shapes:

- Its **research pipeline** — many readers fan out, one synthesizer writes — is exactly the endorsed shape.
- Its **parallel editors with `isolation: "worktree"`** is exactly the shape Cognition warns about: concurrent writers, each blind to the others' intermediate decisions, reconciled only at merge.

If you adopt one pattern from the candidate and reject another, that is the line to draw it on — and it is an architecture decision, not something a better spawn prompt reaches.

## Provenance

Derived during intake of `Rylaa/fable5-opus5-orchestrator` (commit `828974b`). Fields 2, 3, 5, and 7 have no counterpart in the candidate; fields 1, 4, and 6 generalize hints scattered across its playbook and profiles, then were refined against the prior art above. The candidate's return contract is unchanged and worth taking as-is.
