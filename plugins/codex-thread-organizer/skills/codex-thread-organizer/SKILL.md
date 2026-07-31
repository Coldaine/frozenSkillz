---
name: codex-thread-organizer
description: >-
  Use when Codex task titles are unclear, recent related tasks need completion or
  supersession review, important unfinished work is hard to find, or a periodic
  Codex task-organization pass is requested. Codex-only; do not use for ChatGPT
  web conversations or other agent clients.
---

# Codex Thread Organizer

Organize native Codex tasks from their actual conversation bodies. When this skill is invoked, review the selected task surface, rename the tasks through native Codex operations, read the resulting titles back, and summarize the important unfinished work.

## Boundary

- This skill is Codex-only at this point.
- Its source lives in frozenSkillz's dedicated Codex package and is not auto-installed with every skill.
- A periodic Codex automation is the mechanism for recurring organization; the skill is not a background daemon.

## Workflow

1. **Inventory recent tasks.** Record task ID, host ID, current title, update time, working directory, project ID, and summary or preview.
2. **Form tentative workstream clusters.** Use repository identity, project, branch, pull request, issue, artifact, and semantic goal. A working directory is a routing clue, not proof that tasks belong together.
3. **Read the actual conversation bodies.** For every task being classified or renamed, identify the opening request, later changes of scope, delivered outcome, concrete required action, user acceptance or dispute, and references to successor tasks or durable artifacts.
4. **Cross-read related tasks.** Compare every recent relevant task in the workstream before deciding which task owns unfinished work. Follow [references/cross-task-review.md](references/cross-task-review.md).
5. **Classify and title.** Determine whether each task is `done`, `active-remaining`, `continued-elsewhere`, or `parked-unclear`, then apply [references/title-grammar.md](references/title-grammar.md).
6. **Rename the reviewed tasks.** Use the native Codex title operation. Re-read every resulting title and correct any mismatch or truncation.
7. **Report the result.** List renamed tasks, the current owner of each unfinished workstream, important concrete remaining actions, tasks continued elsewhere, parked uncertainties, and archive candidates.

When several project clusters can be reviewed independently, dispatch one subagent per cluster. Give each subagent the task IDs and require it to read the actual conversation bodies. The main agent reconciles relationships and titles across the returned clusters.

## Title Contract

- Use one to five leading semantic symbols, never five by default. Most titles need one to three.
- Keep the words specific and recognizable, normally about 5–12 words.
- Preserve exact product, repository, issue, pull request, and artifact names when they aid recognition.
- Keep the final title within 60 UTF-16 code units, the empirically observed native Codex title ceiling.
- `✅` means the latest relevant user request was satisfied and no concrete required action remains in that task. It does not claim that the broader project is finished.
- `🟡` means a concrete required action remains in the current owner task.
- Use `🔴` sparingly on the clearest highest-priority unfinished task; omit it when the comparison is unclear.
- `⏸️` means a named user or external response is the next required event; `🚧` means a specific obstacle blocks the required outcome.
- `🗄️` marks a reasonable archive candidate. It may accompany `✅`, or identify an older unfinished task whose work clearly continued elsewhere.
- Use `📌` and `↪️` only when cross-reading establishes a canonical task or a named successor.

Examples:

```text
🌊 🧹 Crest Research Pruning
🌊 🧹 ✅ Crest Research Pruning
🟡 🌊 🛠️ Broadside Implementation Continuation
🗄️ ↪️ 🧛 Vampire Survivors Continuation
🗄️ ✅ Techdeals PR #84 Review
```

## Completion Check

Before adding `✅`, answer these questions from the task body:

1. What was the latest relevant user request?
2. Did the answer, artifact, change, test, publication, or other requested outcome actually satisfy it?
3. Does any required execution, verification, recovery, decision, or user input remain?
4. Did a later user turn extend the scope or dispute the claimed result?

Optional ideas, recommendations, and explicitly deferred future phases do not block completion. A bounded task can be complete while its broader project remains unfinished. A planning task is complete when the requested plan was delivered; a request to implement that plan is not complete merely because the plan exists.

## Periodic Automation

Read [references/periodic-automation.md](references/periodic-automation.md) when defining or running recurring organization. Each run uses the same inventory, body-reading, cross-task classification, rename, read-back, and unfinished-work report workflow.
