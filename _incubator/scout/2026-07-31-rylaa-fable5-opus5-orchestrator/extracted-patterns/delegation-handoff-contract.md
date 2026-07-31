# Delegation Handoff Contract

Adapted pattern, not active content. Mirrors the candidate's *return* contract with the *send* contract it never wrote.

The candidate defines rigorously what a worker owes the chair (five parts, ≤40 lines, rejected and re-run if violated) and says almost nothing about what the chair owes a worker — "phases cite item numbers," and send "workers with specs" without ever defining a spec. This is that definition.

## The rule

Every spawn of a substantive worker carries all seven fields below. A spawn missing any of them is underspecified: fix it before sending, don't hope the worker infers.

Sub-minute lookups — one grep, one read, one fetch — are exempt. They are not delegations, they are remote-controlled tool calls.

## The seven fields

**1 · Objective.** One sentence, the finished state, not the activity. "Auth middleware rejects expired tokens with 401 and a structured body" — not "look at the auth middleware." A worker that cannot tell when it is done will either stop early or never stop.

**2 · Ledger items, with the why.** Cite the item numbers this worker owns *and* restate the reasoning behind them. Ledger lines are one-line checkboxes; they carry the WHAT and almost never the WHY. The item says "reject expired tokens." The why — "a prior incident let 30-day-stale tokens through and we chose explicit rejection over silent refresh" — is what stops the worker from solving it the wrong way. **This is the field most often dropped and the one that most often causes rework.**

**3 · Context the worker cannot infer.** Anything decided in conversation, rejected earlier, or true-but-unwritten. Constraints that exist for reasons not visible in the code. Approaches already tried and abandoned, and why. A worker starts with the repo and your prompt — nothing else. Everything you know that the repo does not say is invisible to it unless you write it here.

**4 · Where to look.** Concrete entry points: paths, symbols, commands, URLs, the ledger path, prior work-product paths. Not "the auth code" but `src/middleware/auth.ts` and `tests/auth/expiry.test.ts`. Save the worker the rediscovery you have already paid for.

**5 · Out of scope.** State explicitly what NOT to touch. Adjacent code that looks broken but is deliberate. Refactors that are someone else's phase. Files another parallel worker owns right now. Without this, a capable worker will helpfully expand until it collides with a sibling or with a decision you already made.

**6 · Expected output.** What you need back to make the next decision — a diff, a brief, a verdict, a path. Point at the return contract rather than restating it. If the shape is unusual, say so here.

**7 · Authority.** What the worker may decide alone versus what it must return for a ruling. "Pick the error-message wording; do not change the status code without asking." Silence here produces one of two failures: a worker that stalls on trivia, or one that quietly makes a call that was yours.

## Why this and not a length rule

The candidate gates spawns on prompt length — over 1500 characters and it demands a ledger. Measured against default behavior, spawn prompts land at roughly 1300 characters, under the gate, so it rarely fires; and length was never the thing worth protecting. A 2,000-character prompt that is all restated background and no authority boundary is worse than an 800-character one carrying all seven fields.

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

## Provenance

Derived during intake of `Rylaa/fable5-opus5-orchestrator` (commit `828974b`). Fields 2, 3, 5, and 7 have no counterpart in the candidate; fields 1, 4, and 6 generalize hints scattered across its playbook and profiles. The candidate's return contract is unchanged and worth taking as-is.
