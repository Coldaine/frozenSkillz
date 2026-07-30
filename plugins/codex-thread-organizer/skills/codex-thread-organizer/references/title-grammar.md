# Sparse Codex Title Grammar

## Purpose

Make adjacent Codex tasks recognizable in a narrow sidebar. Symbols communicate useful state; they are not a checklist and do not need to fill five positions.

## Prefix Shape

Use one to five leading symbols, normally one to three. Build the prefix in this order:

1. left-edge markers: attention, then retention, then relationship when present;
2. project or domain;
3. optional work type;
4. lifecycle marker last.

Attention is `🔴` or `🟡`; retention is `🗄️` or `📌`; relationship is `↪️`. This keeps the actionable state visible at the left edge while preserving forms such as `🌊 🧹 ✅` and `🗄️ ↪️ 🧛`. Omit a symbol when the words already communicate it or the evidence is uncertain.

## Status and Relationship Markers

| Symbol | Meaning | Use when |
|---|---|---|
| `✅` | Done | The latest relevant user request was satisfied and no concrete required action remains in that task |
| `🟡` | Concrete follow-up | A specific required action remains in the current owner task |
| `🔴` | Highest-priority unfinished task | Use sparingly on the clearest priority after comparing relevant current owners; omit when unclear |
| `⏸️` | Waiting | A named user or external response is the next required event |
| `🚧` | Blocked | A specific obstacle prevents the required outcome |
| `📌` | Canonical task or durable reference | Cross-reading identifies the task to retain or continue |
| `↪️` | Continued or superseded elsewhere | A named successor carries the older task's unfinished work or replaces its operative result |
| `🗄️` | Archive candidate | The task is done with little continuing value, duplicated, or fully carried by a named successor |

`✅` and `🗄️` can coexist: one says the task is finished, the other says it is a reasonable archive candidate. A `continued-elsewhere` task can receive `↪️` and `🗄️` without receiving `✅`.

## Definition of Done

Add `✅` when the latest relevant user request has been satisfied with adequate evidence from the conversation or resulting state and no concrete required action remains.

Completion evidence depends on what the user asked for:

- an explanation or review covers the requested question;
- a requested artifact or change was delivered;
- requested tests, publication, merge, cleanup, or real-world operation occurred when those were part of the scope;
- the user accepted or confirmed a result when their observation was needed;
- later turns did not extend the task or leave a dispute unresolved.

Judge the task, not the broader project. Optional recommendations and deferred future phases do not block `✅`. A requested plan may be complete while implementation remains future work. If implementation was requested, producing only the plan is incomplete.

An explicit remaining statement such as “next I need to push,” “C-05 through C-08 remain,” or “waiting for the user's answer” blocks `✅` when that action belongs to the current request.

## Work-Type Symbols

| Symbol | Meaning | Use when |
|---|---|---|
| `🧹` | Cleanup or pruning | The dominant work removes, consolidates, or retires clutter |
| `🔍` | Research, audit, or investigation | The outcome is primarily findings or diagnosis |
| `🛠️` | Implementation or repair | The task materially changes a system or artifact |
| `🧭` | Planning or orientation | The durable outcome is a plan, scope, or decision frame |
| `📝` | Documentation | Documentation is the primary deliverable |

Treat these as defaults rather than an exhaustive taxonomy. Use other clear project or domain symbols when they are easier to recognize.

## Construction Pass

1. Read and cross-task classify the task.
2. Write a plain title from the dominant final work.
3. Add the known project or domain symbol.
4. Add a work-type symbol only when it distinguishes nearby tasks.
5. Add attention, relationship, and archive markers at the left edge, and the lifecycle marker last.
6. Keep one to five symbols, normally one to three.
7. Revise once for ambiguity, decoration, and truncation.
8. Measure the final title in UTF-16 code units and keep it within the empirical 60-unit Codex ceiling.

## Examples

| Evidence | Title |
|---|---|
| Project known; cleanup underway | `🌊 🧹 Crest Research Pruning` |
| Latest pruning request finished; nothing required remains | `🌊 🧹 ✅ Crest Research Pruning` |
| Current implementation owner has a concrete next action | `🟡 🌊 🛠️ Broadside Implementation Continuation` |
| Older unfinished task is fully carried by a successor | `🗄️ ↪️ 🧛 Vampire Survivors Continuation` |
| Completed one-off is an archive candidate | `🗄️ ✅ Techdeals PR #84 Review` |

The sparse examples are intentional. Do not add five symbols when two or three make the task recognizable.
