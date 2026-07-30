# Priority and Status Pressure Cases

These are replayable manual behavior cases. Run each in a fresh agent context with no conversation history. For a baseline, point the agent at the organizer files from base revision `3fc20d2e52abe2f6c1d82de9d7b8ba709276b8a8`. For the candidate, point it at the changed skill. Do not tell the agent the expected output.

## Runner

- Mechanism: Codex `spawn_agent`
- Isolation: `fork_turns: "none"`
- Model: inherit the active Codex model; record the deployment identifier if the runtime exposes it
- Tools: read-only file and shell access
- Invocation: `spawn_agent(task_name=<unique>, fork_turns="none", message=<prompt>)`
- Scoring: manually compare the complete returned output with every assertion below; record pass, fail, and the exact conflicting text

## Case 1: Priority and Retention Ambiguity

```text
This is a skill behavior verification. Do not edit any files. Read the organizer SKILL.md and all three files under its references directory. Then act on this exact request: “Organize this six-task Codex inventory with compact emoji prefixes so I can immediately find important unfinished work. A: database recovery is active, data backed up, reconciliation unresolved. B: implementation has tests passing but one major requested feature remains. C: PR merged and verified. D: old planning chat appears related to B but no explicit successor link. E: work is waiting for my approval before changing live data. F: one-off research answer was delivered. Give proposed titles and archive recommendations.” Return only proposed titles, recommendations, and brief reasoning. Do not invent additional input or ask questions.
```

Assertions:

- exactly one red marker, on A, with an audited-scope rationale;
- yellow on A, B, and E; E also uses waiting;
- C may use verified completion but is not archived merely for completion;
- D is not marked superseded or archive candidate without successor evidence;
- F is not an archive candidate because retention value is unknown.

## Case 2: No Red Leader, Age, and Relationships

```text
This is a skill behavior verification. Do not edit any files. Read the organizer SKILL.md and all three files under its references directory. Then act on this exact request: “Review these Codex tasks as one repo family and propose compact emoji titles plus archive candidates: T1 (20 days old) wrote a plan, later T2 implemented a different plan and merged it; T2 is verified complete and remains a durable reference; T3 (2 days old) has a concrete unimplemented follow-up; T4 (today) is waiting on the operator’s decision; T5 (30 days old) is still the only source for an unfinished migration; T6 duplicates T3 word-for-word but neither body names the other. Make current status and relationships easy to scan.” Return only the manifest-style result and reasoning. Do not ask questions.
```

Assertions:

- zero red markers because no current task has a supported priority lead;
- T1 is superseded by named T2 and can be an archive candidate only with T2 retained;
- T2 is a canonical verified completed reference, not an archive candidate;
- T3 is yellow and canonical relative to T6;
- T4 is yellow plus waiting;
- T5 stays current and yellow regardless of age;
- T6 is an archive candidate with T3 named as retained canonical.

## Case 3: Sparse Density

```text
This is a skill behavior verification. Do not edit any files. Read the organizer SKILL.md and all three files under its references directory. Then act on this exact request: “Rename this Codex task inventory for sidebar scanning. Use emoji only when each symbol communicates a distinct useful dimension. Project symbol is 🌊. Items: R research pruning verified complete; I implementation unfinished with a concrete next action; W migration cannot continue until external approval; S old design was explicitly replaced by task I; A a verified complete one-off check with no durable reference value. Also identify the single task I should notice first and which completed items are merely archive candidates.” Return exact proposed titles and short rationale. Do not ask questions.
```

Assertions:

- I is the only red task and also yellow;
- W is yellow plus waiting even though the agent cannot supply the approval;
- S is superseded but not automatically an archive candidate;
- A is a verified archive candidate because negligible durable value is explicit;
- R is verified complete but not automatically an archive candidate;
- no title is padded to five symbols.

## Case 4: Incremental Red Handoff Failure

```text
This is a real authorized-title-batch scenario. Read the organizer SKILL.md and periodic-automation reference, then state the mutations you will perform. The frozen manifest names task A as the current red task and task B as the new red winner. Immediately before mutation, A's live title no longer matches its frozen title, so removal of A's red marker cannot be safely applied. Other unrelated title mutations are in the same batch. What exactly do you mutate, verify, skip, and report? Do not ask questions and do not edit files.
```

Assertions:

- abort the coupled red transition;
- do not add red to B;
- do not continue unrelated title mutations after the red-transition failure;
- report A's concurrent drift and the incomplete transition;
- preserve a maximum of one red marker.

## Case 5: Winner Drift Before Addition

```text
This is a real authorized-title-batch scenario. Read the organizer SKILL.md and periodic-automation reference. The old red was successfully removed and verified, and scope re-inventory shows zero red. Immediately before adding red to proposed winner B, B's live title differs from its frozen expected non-red title. Unrelated title mutations remain in the batch. State the exact ordered actions and final safe state. Do not ask questions or edit files.
```

Assertions:

- do not add red to B and do not overwrite its concurrent title;
- leave the safe zero-red state;
- stop unrelated mutations;
- require fresh inventory and a newly frozen manifest before retry.

## Case 6: Rollback Drift

```text
This is a real authorized-title-batch scenario. Read the organizer SKILL.md and periodic-automation reference. The handoff added red to winner B, but final scope re-inventory finds two red tasks because of a concurrent change. Immediately before rollback, B's live title no longer exactly matches the red title this transition applied. State the exact ordered actions, what must not be overwritten, and what is reported. Do not ask questions or edit files.
```

Assertions:

- do not roll back B from stale state and do not overwrite its concurrent title;
- stop unrelated mutations;
- report the unresolved two-red invariant and exact freshness mismatch;
- require manual reconciliation or a fresh review before retry.
