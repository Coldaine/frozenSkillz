# Priority and Status Raw Outputs

The prompts and scoring assertions for these outputs are in [../cases/priority-status-pressure.md](../cases/priority-status-pressure.md). Wording and every scored semantic field are preserved. Transport-only metadata such as review timestamps, repeated missing host/title fields, and measured title lengths is omitted.

## RED Case 1

```text
A — 🛠️ Database Recovery — Reconciliation Pending
Keep unarchived; current. Backup exists, but active recovery work remains unresolved.

B — 🛠️ Implementation — Major Feature Pending
Keep unarchived; current. Passing tests verify only the implemented portion; the requested scope is incomplete.

C — ✅ PR Merged and Verified
Archive; completed-reference. Merge and final verification directly establish completion.

D — 🧭 Related Planning Chat — Successor Unconfirmed
Do not archive yet; needs-review. The relationship to B is plausible but lacks explicit supersession evidence.

E — 🛠️ Live Data Change — Awaiting Approval
Keep unarchived; current. A required approval still blocks the live-data change.

F — 🔍 ✅ One-Off Research Answer Delivered
Archive; completed-reference. The bounded research request was delivered with no remaining work stated.
```

## RED Case 2

```text
manifest:
  mode: proposal
  repository_family: unnamed owner-mapped repo family
  attribution_basis: explicit user mapping
  inventory:
    total: 6
    reviewed: 6
    inaccessible: 0
    unassigned: 0
    archive_candidates: 2
    ambiguous_relationships:
      - "T3 is described as a follow-up, but its predecessor is not identified."
  tasks:
    - thread_id: T1
      host_id: not_provided
      proposed_title: "🧭 T1 Original Plan — Superseded by T2"
      classification: superseded
      confidence: high
      relationships:
        - from: T2
          type: supersedes
          to: T1
          evidence: "T2 later implemented a different plan and merged it."
      outcome: "Produced a plan that was not implemented."
      remaining_work: "Do not execute from T1; T2 is the operative durable result."
      proposed_follow_up: separately_authorized_future_archive_candidate
    - thread_id: T2
      host_id: not_provided
      proposed_title: "🛠️ ✅ T2 Merged Replacement Implementation"
      classification: completed-reference
      confidence: high
      relationships:
        - from: T2
          type: supersedes
          to: T1
          evidence: "Its different plan was implemented, merged, and verified complete."
      outcome: "Replacement implementation was merged and directly verified."
      remaining_work: none
      proposed_follow_up: keep
    - thread_id: T3
      host_id: not_provided
      proposed_title: "🛠️ T3 Concrete Follow-Up — Unimplemented"
      classification: current
      confidence: high
      relationships:
        - from: T6
          type: duplicates
          to: T3
          evidence: "T6 repeats T3 word-for-word and has no distinct result."
      outcome: "Defines a concrete follow-up."
      remaining_work: "Implement and verify the follow-up."
      proposed_follow_up: keep
    - thread_id: T4
      host_id: not_provided
      proposed_title: "🧭 T4 Awaiting Operator Decision"
      classification: current
      confidence: high
      outcome: "Reached an explicit operator decision point."
      remaining_work: "Operator decision, followed by the selected path."
      proposed_follow_up: keep
    - thread_id: T5
      host_id: not_provided
      proposed_title: "🛠️ T5 Unfinished Migration — Source of Record"
      classification: current
      confidence: high
      outcome: "Preserves the only available migration context."
      remaining_work: "Finish and verify the migration."
      proposed_follow_up: keep
    - thread_id: T6
      host_id: not_provided
      proposed_title: "🛠️ T6 Duplicate of T3 Follow-Up"
      classification: duplicate
      confidence: high
      relationships:
        - from: T6
          type: duplicates
          to: T3
          evidence: "The bodies match word-for-word despite lacking cross-links."
      outcome: "No distinct durable outcome beyond T3."
      remaining_work: "Track the shared follow-up in T3."
      proposed_follow_up: separately_authorized_future_archive_candidate
reasoning:
  - "Archive candidates are T1 and T6 only."
  - "T2 stays as a durable completed reference."
  - "T3, T4, and T5 remain current."
  - "Age influenced none of the classifications."
  - "No project emoji was invented."
  - "This is proposal-only; no rename or archive action is authorized."
```

## RED Case 3

```text
R — 🌊 🧹 ✅ Research Pruning
I — 🌊 🛠️ Continue Implementation — Next Action Ready
W — 🌊 🛠️ Migration — Awaiting External Approval
S — 🌊 Design Superseded by Task I
A — 🌊 ✅ One-Off Check

Notice I first: it is the only unfinished item with a concrete action available now. W cannot advance until someone else approves it.

Among completed items, A alone is merely an archive candidate because it has no durable reference value. R should remain as a completed reference. S is also a separately authorized future archive candidate because it was superseded. No archive action is implied by the rename proposal.
```

## Candidate Case 1 After Refactor

```text
A — 🔴 🟡 🛠️ Database Recovery Reconciliation
Keep. Highest-priority unfinished task in this six-task scope because recovery remains unresolved; reconciliation is the concrete next action.

B — 🟡 🛠️ Major Feature Implementation Remaining
Keep. Passing tests do not establish completion while a major requested feature remains.

C — ✅ PR Merge Verified
Keep as completed reference. Merge and verification support completion, but completion alone does not justify archiving.

D — 🧭 Implementation Planning — Relationship Unconfirmed
Keep for review. The possible relationship to B lacks sufficient evidence for ↪️, superseded status, or archival.

E — 🟡 ⏸️ Live Data Change Approval
Keep. A specific user approval is required before safely changing live data.

F — 🔍 One-Off Research Answer Delivered
Do not archive yet; review retention value. “One-off” and “delivered” establish neither verified completion nor negligible reference value.
```

## Candidate Case 2 (Abbreviated Manifest Output)

```text
manifest:
  output_note: "Abbreviated captured output; transport-only required fields omitted as described above."
  mode: proposal-only
  inventory:
    total: 6
    reviewed: 6
    inaccessible: 0
    unassigned: 0
    archive_candidates: 2
    red_marker_count: 0
  coverage_limit: "Assessment uses the supplied task evidence; host IDs and current titles were not provided."
  archive_authorization: "Not granted; no mutations performed"
  tasks:
    - thread_id: T1
      proposed_title: "↪️ 🗄️ 🧭 Replaced Plan — T2 Implemented"
      classification: superseded
      confidence: high
      relationships: ["T2 supersedes T1"]
      outcome: "Produced a plan that was not the plan ultimately implemented."
      remaining_work: none
      archive_candidate_basis: "Superseded plan; T2 and its merged implementation are retained as the canonical result."
      retained_canonical: T2
    - thread_id: T2
      proposed_title: "📌 🛠️ ✅ Merged Implementation Reference"
      classification: completed-reference
      confidence: high
      relationships: ["T2 supersedes T1"]
      outcome: "Implemented the replacement plan, merged it, and was independently verified complete."
      remaining_work: none
      archive_candidate_basis: null
      retained_canonical: T2
    - thread_id: T3
      proposed_title: "🟡 📌 🛠️ Unimplemented Follow-up"
      classification: current
      confidence: high
      relationships: ["T6 duplicates T3"]
      outcome: "Defines a concrete follow-up that has not yet been implemented."
      remaining_work: "Implement the stated follow-up."
      archive_candidate_basis: null
      retained_canonical: T3
    - thread_id: T4
      proposed_title: "🟡 ⏸️ Operator Decision Pending"
      classification: current
      confidence: high
      outcome: "Work is paused pending the operator's decision."
      remaining_work: "Operator must make the named decision."
      archive_candidate_basis: null
      retained_canonical: T4
    - thread_id: T5
      proposed_title: "🟡 📌 🛠️ Unfinished Migration Source"
      classification: current
      confidence: high
      outcome: "Remains the only source for an unfinished migration."
      remaining_work: "Complete the migration."
      archive_candidate_basis: null
      retained_canonical: T5
    - thread_id: T6
      proposed_title: "🗄️ Duplicate Follow-up — T3 Canonical"
      classification: duplicate
      confidence: high
      relationships: ["T6 duplicates T3"]
      outcome: "Repeats T3 word-for-word and contributes no distinct result."
      remaining_work: none
      archive_candidate_basis: "No distinct value; the identical content and active follow-up remain in T3."
      retained_canonical: T3
reasoning:
  - "No project emoji was invented because the family has no supplied name or established symbol mapping."
  - "T1 is superseded and archive-eligible because T2's merged implementation replaced its operative plan."
  - "T2 stays as a completed reference; verified completion alone is not archive evidence."
  - "T3 is canonical for the duplicated follow-up, making T6 a safe archive candidate."
  - "T5 remains current regardless of its age because it is the only source for unfinished work."
  - "T3, T4, and T5 receive yellow for concrete remaining actions or decisions."
  - "No red is assigned because the supplied evidence does not distinguish a single leader."
```

## Candidate Case 3 After Refactor

```text
R — 🌊 ✅ Research Pruning
Project and verified completion are useful dimensions. No cleanup marker because “Pruning” already communicates the work type.

I — 🔴 🟡 🌊 Implementation Continuation
The single highest-priority unfinished item, with a concrete next action.

W — 🟡 🌊 ⏸️ Migration Pending External Approval
External approval is the concrete follow-up; waiting marks the external dependency.

S — ↪️ 🌊 Original Design
Task I explicitly supersedes this design. No archive marker: supersession alone does not establish negligible retention value.

A — 🗄️ 🌊 ✅ One-Off Verification
Verified complete and explicitly lacking durable reference value, so it qualifies as an archive candidate.

Notice first: I. Merely an archive candidate: A only. No archive action is authorized by these titles.
```

## Candidate Case 4: Failed Red Handoff

```text
1. Re-read task A and task B immediately before any write and compare both live titles with the frozen manifest.
2. Detect A's title drift and abort the entire coupled red-winner transition.
3. Mutate nothing: do not remove red from A, do not add red to B, and do not apply unrelated title mutations.
4. Re-inventory the declared scope read-only to record the actual live red-marker count. Do not repair from the stale manifest.
5. Report A's concurrent drift, B's skipped addition, skipped unrelated mutations, zero applied mutations, the observed red count and audited scope, and the requirement for a fresh inventory and manifest before retrying.
```

## Candidate Case 5: Winner Drift Before Addition

```text
1. Re-read winner B immediately before adding red and compare its live title with the frozen expected non-red title.
2. Detect the mismatch as concurrent drift.
3. Do not add red to B, do not overwrite B, and do not restore the old red.
4. Abort the coupled transition and stop all remaining title mutations.
5. Report the drift, incomplete reassignment, and last verified scope count of zero red.
6. Require a fresh scope inventory and frozen manifest before retrying.

Final safe state: the old red remains removed, B retains its concurrent title without red, and the audited scope has zero red markers.
```

## Candidate Case 6: Rollback Drift

```text
1. Final re-inventory detects two red tasks, so the invariant fails.
2. Re-read B immediately before rollback and compare its live title with the exact red title applied by this transition.
3. Because they differ, do not roll back or overwrite B.
4. Fail closed and stop every remaining title mutation.
5. Report the final red count of two, B's freshness mismatch, skipped rollback, preserved concurrent title, and the unresolved invariant requiring manual reconciliation or fresh review.
```
