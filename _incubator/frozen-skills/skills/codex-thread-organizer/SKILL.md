---
name: codex-thread-organizer
description: >-
  Use when reviewing or maintaining Codex task history: inventorying related tasks,
  proposing body-derived sidebar titles, assessing same-repository supersession, or
  running a periodic organization pass. Codex-only; do not use for ChatGPT web
  conversations or other agent clients.
---

# Codex Thread Organizer

Organize the native Codex task surface from conversation evidence. Treat the skill as the decision workflow; an on-demand request or periodic Codex automation invokes it.

## Platform and Packaging Boundary

- This is **Codex-only** at this point.
- Do not apply it to ChatGPT web conversations, Claude Code, Cursor, Gemini, browser tabs, or another client's history.
- Do not assume repository presence means installation. The frozenSkillz copy is gated; installation and automation creation are separate, explicit operator actions.
- This is not a daemon. “Running all the time” means a periodic Codex automation invokes the skill.

## Choose the Mode

| Mode | Use when | Allowed effects |
|---|---|---|
| Proposal | The user asks to review, organize, classify, or preview changes | Read tasks and produce a manifest only |
| Authorized title batch | The user approves a batch or explicitly asks to rename the scoped tasks | Set titles, then read them back |
| Cross-task relevance review | The user asks whether older work is still relevant or was superseded | Read and compare related task bodies; propose relationships only |
| Periodic run | A Codex automation invokes this skill | Follow the automation's explicit mutation boundary; otherwise remain proposal-only |

Archive, pin, or other state changes require their own explicit scope. Authorization to rename is not authorization to archive.

## Workflow

1. **Inventory the accessible scope.** Use native Codex task operations. Record task ID, host ID, current title, timestamps, working directory, and other routing metadata.
2. **Read the actual work.** Read enough of each body to understand the opening request, later changes of direction, substantive outcome, remaining work, and references to later tasks or durable artifacts. A title, preview, or first message is not enough.
3. **Group only with evidence.** Attribute a repository or project family from the working directory, repository identity, transcript evidence, or an explicit user mapping. Leave uncertain tasks unassigned.
4. **Compare related tasks when relevant.** If the scope includes relevance, age, duplication, or supersession, read the accessible bodies in the same family together. Follow [references/cross-task-review.md](references/cross-task-review.md).
5. **Draft the semantic title.** Apply the sparse symbol grammar in [references/title-grammar.md](references/title-grammar.md), then critique and revise the title once.
6. **Produce a frozen manifest.** Include IDs, old and proposed titles, confidence, body-derived rationale, relationship evidence, and the proposed action. Record inaccessible and ambiguous tasks.
7. **Apply only an authorized frozen batch.** Recheck each current title immediately before mutation. Skip and report concurrent changes. Use the native Codex title operation.
8. **Verify independently.** Re-inventory or read back every target and require an exact match before reporting success. A mutation acknowledgement is provisional.

## Title Rules

- Use **one to five** leading semantic symbols, never five by default. Most titles should use one to three.
- Prefer one project or domain symbol, then an optional work-type symbol, then an optional lifecycle symbol.
- A fourth or fifth symbol is exceptional and must add a stable distinction. Never pad a title with decoration.
- Keep the words specific and recognizable, normally about 5–12 words.
- Preserve exact product, repository, issue, pull request, and artifact names when they aid recognition.
- Enforce the native limit of 60 UTF-16 code units before mutation; prefer a lower ordinary ceiling so later edits have room.
- Use `✅` only when the scoped outcome is directly verified. An assistant saying “done” is not verification.

Examples:

```text
🌊 Crest Research Pruning
🌊 🧹 Crest Research Pruning
🌊 🧹 ✅ Crest Research Pruning
```

The third form is valid only when the pruning's final state was checked. See [references/title-grammar.md](references/title-grammar.md) for the evidence test.

## Cross-Task Safety

- Age may prioritize review; it never proves irrelevance, duplication, supersession, or archive eligibility.
- `current` does not mean newest.
- Preserve an old task as `completed-reference` when it has a durable result worth retaining.
- A `superseded` or `duplicate` result must name the later related task or repository artifact and summarize the evidence.
- Weak or conflicting evidence becomes `needs-review`.
- Report inaccessible tasks as coverage gaps, not as irrelevant.

## Mutation Safety

- Prefer supported Codex operations; do not edit internal state stores during ordinary runs.
- Freeze IDs and old titles in the proposal manifest.
- Recheck live state before every write.
- Keep title, archive, pin, and deletion scopes separate.
- Never alter conversation content.
- If a supported operation is unavailable, stop and report the limitation. Direct metadata editing requires a separately designed, backed-up, explicitly authorized procedure.

## Periodic Automation

Read [references/periodic-automation.md](references/periodic-automation.md) when defining or running an automation. The automation should invoke `$codex-thread-organizer` explicitly, scan incrementally where possible, and emit an auditable report each run.
