# Sparse Codex Title Grammar

## Purpose

Make adjacent Codex tasks recognizable in a narrow sidebar. Symbols are compact semantics, not a completeness checklist.

## Prefix Shape

Use between one and five leading symbols:

1. **Project or domain** — the stable family marker when the mapping is known.
2. **Work type** — optional; add it when neighboring tasks in the family need differentiation.
3. **Lifecycle** — optional; add it only when the body contains clear state evidence.
4. **Subsystem or exception** — rare; use only when it prevents a real collision.
5. **Additional exception** — very rare; never add it merely because five are allowed.

Most good titles use one or two symbols. A verified lifecycle marker commonly makes three.

Do not invent a project-symbol mapping from a single ambiguous task. Reuse a stable mapping already present in the reviewed cohort or propose the mapping for owner review.

## Work-Type Symbols

Treat these as defaults, not an exhaustive universal taxonomy:

| Symbol | Meaning | Use when |
|---|---|---|
| `🧹` | Cleanup or pruning | The dominant work removes, consolidates, or retires clutter |
| `🔍` | Research, audit, or investigation | The outcome is primarily findings or diagnosis |
| `🛠️` | Implementation or repair | The task materially changes a system or artifact |
| `🧭` | Planning or orientation | The durable outcome is a plan, scope, or decision frame |
| `📝` | Documentation | Documentation is the primary deliverable, not a side effect |

Omit the work-type symbol when the natural-language title already distinguishes the task or the classification is uncertain.

## Verified Completion

Use `✅` only when the scoped outcome has direct completion evidence, such as:

- the requested artifact exists in its final location and was read back;
- relevant tests or verification commands passed against the final state;
- a commit, push, merge, issue state, or pull request state was checked when that was part of the requested outcome;
- a native Codex mutation was independently read back exactly;
- the user explicitly confirmed that the scoped outcome is complete.

Do not use `✅` merely because:

- the assistant used “done,” “completed,” or similar language;
- a plan was written but not executed;
- files were changed but required validation, publication, review, or cleanup remains;
- one intermediate command succeeded;
- a newer task exists.

If the task reached a clear non-completion final state, describe that state in words unless the owner has approved a stable lifecycle symbol for it. Do not improvise a lifecycle vocabulary during a batch.

## Construction Pass

1. Write a plain title from the dominant final work.
2. Put the most distinctive words early.
3. Add the known project or domain symbol.
4. Add one work-type symbol only if it speeds recognition.
5. Add `✅` only after the completion test above.
6. Critique the result for ambiguity, redundancy, decoration, and truncation.
7. Revise once and measure the final title in UTF-16 code units. Treat 60 units as an empirical Codex title-operation ceiling, observed when longer titles persisted with a literal trailing ellipsis in a verified 2026-07-20 batch, rather than as a documented API guarantee.

Examples:

| Evidence | Title |
|---|---|
| Project known; action already clear | `🌊 Crest Research Pruning` |
| Cleanup distinction helps | `🌊 🧹 Crest Research Pruning` |
| Cleanup completed and final state verified | `🌊 🧹 ✅ Crest Research Pruning` |
| Work still pending verification | `🌊 🧹 Crest Research Pruning` |
