# Priority and Status Taxonomy RED-GREEN Run

- Date: 2026-07-30
- Scope: unchanged versus updated `codex-thread-organizer` instructions
- Method: three fresh-context inventory scenarios, followed by two focused refactor reruns
- Mutation boundary: proposal only; no live Codex task titles or archive state changed

## Reproduction Metadata

- Runner: Codex `spawn_agent` with `fork_turns: "none"`
- Invocation: `spawn_agent(task_name=<unique>, fork_turns="none", message=<case prompt>)`
- Model: inherited active Codex model; the exact deployment identifier and sampling parameters were not exposed by the runner
- Source revisions: base `3fc20d2e52abe2f6c1d82de9d7b8ba709276b8a8`; candidate is the reviewed PR diff from that base
- Complete replay prompts and scoring assertions: [../cases/priority-status-pressure.md](../cases/priority-status-pressure.md)
- Raw baseline and candidate outputs: [2026-07-30-priority-status-raw-outputs.md](2026-07-30-priority-status-raw-outputs.md)
- Scoring: manual, assertion by assertion; this is replayable pressure-test evidence, not an automated semantic test runner

## RED: Unchanged Skill

The unchanged skill correctly recovered outcomes and remaining work but did not make the agreed states visually scannable:

- Priority scenario: proposed `🛠️ Database Recovery — Reconciliation Pending` and no red or yellow attention markers.
- Relationship scenario: rendered supersession, waiting, and duplicates only in words; no `↪️`, `⏸️`, `📌`, or `🗄️` markers.
- Density scenario: stated that a blocked state must stay in words because “no approved blocked-lifecycle symbol exists.”
- One baseline classified a verified merged PR as both a completed reference and an archive recommendation, showing that completion and retention value were not separated tightly enough.

## GREEN: Initial Updated Skill

All three scenarios used the new attention, lifecycle, and relationship vocabulary and preserved zero-or-one red selection. The initial pass exposed two wording gaps:

- a waiting task omitted `🟡` because the agent treated yellow as requiring an agent-executable action;
- a delivered “one-off” answer received `🗄️` without an explicit retention-value judgment.

## REFACTOR: Wording Tightened

The grammar now states that a named owner or external decision is a concrete follow-up even when the agent cannot perform it. The archive review now states that “one-off,” “delivered,” and “no remaining work” establish outcome state, not retention value.

Fresh-context reruns then produced:

- `🟡 ⏸️ Live Data Change Approval` for the named owner decision;
- `🟡 🌊 ⏸️ Migration Pending External Approval` for the external wait;
- no archive marker for the delivered research answer when retention value was unknown;
- `🗄️ 🌊 ✅ One-Off Verification` only when negligible durable value was explicit;
- exactly one `🔴` in each scope with a credible priority leader, and zero when no leader was supported.

## Raw Final Outputs

Case 1 final rerun:

```text
A — 🔴 🟡 🛠️ Database Recovery Reconciliation — Keep. Highest-priority unfinished task in this six-task scope; reconciliation is the concrete next action.
B — 🟡 🛠️ Major Feature Implementation Remaining — Keep. Passing tests do not establish completion while a major requested feature remains.
C — ✅ PR Merge Verified — Keep as completed reference. Completion alone does not justify archiving.
D — 🧭 Implementation Planning — Relationship Unconfirmed — Keep for review; no successor evidence supports supersession or archive.
E — 🟡 ⏸️ Live Data Change Approval — Keep. A specific user approval is required.
F — 🔍 One-Off Research Answer Delivered — Do not archive yet; “one-off” and “delivered” establish neither verified completion nor negligible reference value.
```

Case 2 final output assigned zero red, `↪️ 🗄️` to T1 with T2 retained, `📌 🛠️ ✅` to T2, `🟡 📌 🛠️` to T3, `🟡 ⏸️` to T4, `🟡 📌 🛠️` to the thirty-day-old T5, and `🗄️` to duplicate T6 with T3 retained.

Case 3 final rerun:

```text
R — 🌊 ✅ Research Pruning
I — 🔴 🟡 🌊 Implementation Continuation
W — 🟡 🌊 ⏸️ Migration Pending External Approval
S — ↪️ 🌊 Original Design
A — 🗄️ 🌊 ✅ One-Off Verification
```

Case 4 aborted the entire coupled transition after detecting drift on the old red task: it removed no old red, added no new red, skipped unrelated mutations, re-inventoried read-only, and required a fresh manifest before retry.

Cases 5 and 6 exercised later concurrency windows. Winner drift immediately before addition left the verified zero-red state untouched. Winner drift immediately before rollback preserved the concurrent title, stopped all mutations, and escalated the unresolved two-red state for manual reconciliation instead of overwriting from stale state.

The durable structured expectations are in `../semantic-cases.json`. Repository unit tests validate documentation and fixture invariants; they do not execute or score model behavior.
