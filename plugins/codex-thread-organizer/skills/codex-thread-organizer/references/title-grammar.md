# Sparse Codex Title Grammar

## Purpose

Make adjacent Codex tasks recognizable in a narrow sidebar. Symbols are compact semantics, not a completeness checklist. A symbol earns a place only when it communicates a distinct, evidence-backed dimension faster than the words alone.

## Prefix Shape

Use between one and five leading symbols, but never aim for five. Most good titles use one to three.

Build an ordinary semantic base in this order:

1. **Project or domain** — the stable family marker when the mapping is known.
2. **Work type** — optional; add it when neighboring tasks in the family need differentiation.
3. **Lifecycle** — optional; add it only when the body contains clear state evidence.

When cross-task review establishes an attention, relationship, or retention state, put its marker before that base so it remains visible at the left edge. Use the precedence below when the five-symbol ceiling forces an omission:

1. `🔴` global highest priority;
2. `🟡` concrete follow-up;
3. one relationship or retention marker;
4. lifecycle;
5. project or domain;
6. work type.

Omit the least useful lower-precedence marker instead of exceeding five. Do not invent a project-symbol mapping from a single ambiguous task. Reuse a stable mapping already present in the reviewed cohort or propose the mapping for owner review.

## Global Attention Markers

| Symbol | Meaning | Evidence test |
|---|---|---|
| `🔴` | Single highest-priority unfinished task | Use on exactly zero or one task across the frozen audited scope, and only after comparing all eligible current unfinished tasks |
| `🟡` | Concrete remaining action | Use when the body supports a specific next action, decision, or follow-up; several tasks may qualify |

`🔴` is a global comparison, not a synonym for “important.” Select it after classification using, in order: explicit owner urgency, safety or loss risk, downstream blocking impact, time sensitivity, then action readiness. Recency and dramatic subject matter do not establish priority. Use zero red markers when coverage is too incomplete for a credible comparison or when no unfinished current task clearly leads.

`🔴` and `🟡` may coexist because they answer different questions: “Which one matters most?” and “Does it have a concrete remaining action?” Yellow does not require the agent itself to be able to act: a named owner approval or external decision is a concrete follow-up and normally earns `🟡` alongside `⏸️`. A blocked task without a defined remediation, decision, or other specific next step does not automatically receive yellow.

## Relationship and Retention Markers

| Symbol | Meaning | Evidence test |
|---|---|---|
| `📌` | Current canonical task or durable reference | Cross-task comparison identifies it as the task to retain or continue for that workstream |
| `↪️` | Superseded task | A named later task or durable artifact replaces its operative plan, decision, or outcome |
| `🗄️` | Archive candidate | Cross-task review supports a proposal to archive after separate authorization |

Do not put `📌` on every current task. Use it only when distinguishing a canonical task from related tasks adds real value. `↪️` belongs on the older replaced task, not its successor. `🗄️` records a recommendation in a frozen proposal; it never authorizes or proves that an archive mutation occurred.

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

## Lifecycle Markers

| Symbol | Meaning | Evidence test |
|---|---|---|
| `⏸️` | Waiting | Progress requires a named user or external decision, response, or event |
| `🚧` | Blocked | A specific technical or operational blocker prevents safe progress |
| `✅` | Verified complete | The scoped requested outcome reached its final state and that state was directly checked |

Use at most one lifecycle marker. Prefer `⏸️` for a decision or external response and `🚧` for an obstacle that requires diagnosis or remediation; `✅` is mutually exclusive with both. None of these markers means abandoned, stale, or safe to archive.

Use `✅` only when completion evidence includes one or more of the following:

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

## Construction Pass

1. Read and classify the task before choosing any marker.
2. Write a plain title from the dominant final work and put its distinctive words early.
3. Add the known project or domain symbol.
4. Add one work-type symbol only if it speeds recognition.
5. Add a lifecycle marker only after its evidence test passes.
6. After the full related inventory is classified, add relationship, retention, and global attention markers.
7. Confirm the frozen manifest contains zero or one `🔴`, and that every `🟡` names a concrete remaining action in the rationale.
8. Critique the result for ambiguity, redundancy, decoration, and truncation.
9. Revise once and measure the final title in UTF-16 code units. Treat 60 units as an empirical Codex title-operation ceiling, observed when longer titles persisted with a literal trailing ellipsis in a verified 2026-07-20 batch, rather than as a documented API guarantee.

## Examples

| Evidence | Title |
|---|---|
| Project known; action already clear | `🌊 Crest Research Pruning` |
| Cleanup distinction helps | `🌊 🧹 Crest Research Pruning` |
| Cleanup completed and final state verified | `🌊 🧹 ✅ Crest Research Pruning` |
| Single top priority with a concrete next action | `🔴 🟡 🌊 Broadside Implementation Continuation` |
| Concrete follow-up waiting for owner approval | `🟡 ⏸️ Techdeals Future-State Migration` |
| Canonical completed reference | `📌 🌊 ✅ Legacy Broadside Systems Preservation` |
| Named later work replaced this task | `↪️ ❄️ Platform Branch Purpose` |
| Verified one-off result proposed for archive | `🗄️ ✅ Techdeals PR #84 Review` |

The sparse examples are intentional. Do not add five symbols when two or three already make the task recognizable.
