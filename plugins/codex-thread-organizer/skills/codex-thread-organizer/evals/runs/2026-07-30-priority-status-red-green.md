# Priority and Status Taxonomy RED-GREEN Run

Date: 2026-07-30  
Scope: unchanged versus updated `codex-thread-organizer` instructions  
Method: three fresh-context inventory scenarios, followed by two focused refactor reruns  
Mutation boundary: proposal only; no live Codex task titles or archive state changed

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

The durable semantic cases are in `../semantic-cases.json`; repository assertions enforce the marker vocabulary, sparse-title contract, archive authorization boundary, age rule, and red-count expectation.
