# Plan 3: Conformance, Integrations, and Pilot

> **Status:** draft and blocked on Plan 2 completion.

## Outcome

Turn the approved contract and completed local implementation into reproducible
system-level evidence, add only the retained central/update integrations, and then run
the pilot as a conformance exercise rather than a design exercise.

## Entry gates

- [Plan 1](01-design-closure-authority-and-distribution.md) is approved.
- [Plan 2](02-local-control-plane-and-client-runtime.md) is complete on deterministic
  Windows/Linux and exact-client-version fixtures.
- Required acceptance/failure cases have fixed expected outcomes.
- Evidence format, environment snapshot, pass aggregation, waiver policy, and
  retention are approved before any pilot run.

## Phase 3A: Full conformance harness

1. Assemble the repository, client, platform, runtime, inventory, security, update,
   and failure catalogs into one versioned harness.
2. Record fixture/project commits, frozenSkillz commit, OS/architecture, client
   versions, input digests, commands, exit codes, changed-file digests, observed
   states, and evidence paths for every run.
3. Require all approved happy-path and fault cases; a blocked/not-runnable case is not
   a pass.
4. Build bounded golden inventories and independently reproduce the results.
5. Define agent-effectiveness benchmarks before making effectiveness claims: corpus,
   baseline, model/version controls, repetitions, intended-tool metric, wrong-tool
   rate, tool/context cost, latency budget, and thresholds.
6. For every retained managed-proxy capability, include its adversarial cases: direct
   disallowed tool calls, paginated/list-changed discovery, identical concurrent
   request IDs, capability/root/auth separation, callbacks, cancellation, disconnect,
   daemon peer access, redaction, dynamic root narrowing, and canonicalized
   runtime-root escape.

**Exit gate:** the harness produces deterministic, independently interpretable
evidence and no successful connection is mistaken for full correctness.

## Phase 3B: Optional central observation integration

Only if retained by the approved v1 design:

1. Implement submission as a separate consumer of complete local scan output.
2. Add authentication, privacy classification, payload limits, idempotency, retries,
   offline queueing, schema negotiation, retention/deletion, and device-identity
   collision handling.
3. Test sink absence, timeout, auth failure, duplicate acknowledgement, stale
   observation, and schema rejection without degrading local scan correctness.
4. Keep desired project/publication state authoritative in Git; the index remains an
   observation and comparison surface.

**Exit gate:** central failure cannot corrupt local state, lose required evidence, or
silently redefine authority.

## Phase 3C: Cross-repository update integration

Only after local sync/update semantics pass conformance:

1. Discover actual consumers from committed desired state and verify the consumer
   index against a golden repository set.
2. Use least-privilege automation to create ordinary reviewable branches/PRs; never
   write directly to consumer default branches.
3. Generate deterministic diffs that preserve unmanaged settings and fork/local
   artifacts and refuse ambiguous overwrite.
4. Record per-repository selection and outcome, handle rate limits/branch collisions,
   and retry partial runs without duplicate PRs or false global completion.
5. Prove that reverting a generated project PR reverses the managed update without
   out-of-band machine repair.

**Exit gate:** real update automation passes consumer selection, deterministic diff,
partial-failure, review, and rollback cases.

## Phase 3D: Pilot declaration

Freeze the pilot contract before deployment:

- exact frozenSkillz and fixture repository commits;
- proposed minimum topology of one Python repository and one infrastructure
  repository, subject to explicit approval;
- one declared Windows 11 machine and one declared Linux machine;
- exact supported client versions rather than the phrase "all five clients";
- one portable MCP and one host-bound MCP with pinned versions;
- required local and integration acceptance/failure IDs;
- operator procedure, expected duration/resource budgets, cleanup, rollback, waiver,
  evidence-retention, and abort rules.

The transcript's two-repository/two-machine/five-client composition remains a
candidate until the supported-client matrix and repositories are explicitly approved.

## Phase 3E: Pilot execution and evaluation

1. Snapshot the declared environments without importing secret values into evidence.
2. Install/materialize from the approved source and run the exact committed procedure.
3. Execute all required conformance and failure cases, including cross-scope collision,
   approval-pending state, drift, rollback, and Windows/Linux logical equivalence;
   when retained by the approved design, also run authorized root containment,
   tool-call enforcement, per-client session isolation, and gateway concurrency.
4. Compare observations with the hand-built golden result.
5. Run the predeclared agent-effectiveness benchmark only after configuration and
   runtime correctness pass.
6. Classify every failure as contract defect, implementation defect, fixture defect,
   environment defect, or unsupported behavior. Do not redesign silently during the
   run.
7. Retain evidence and produce a go/no-go decision with remaining risks and rollback
   state.

**Plan 3 complete when:** every required case passes under the predeclared aggregation
rule, all evidence is retained and reproducible, and the approved rollout decision is
based on the contract rather than anecdotal connectivity.

## Explicit non-actions

- No pilot before the system contract, local implementation, and deterministic
  conformance harness are complete.
- No Obot or other sink becomes the scanner or desired-state authority.
- No cross-repository automation bypasses review or ownership boundaries.
- No effectiveness claim is made without a controlled benchmark and threshold.
- No failed case is waived by editing the contract after seeing the result without a
  new reviewed contract version and rerun.
