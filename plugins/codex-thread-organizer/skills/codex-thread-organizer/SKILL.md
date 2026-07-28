---
name: codex-thread-organizer
description: >-
  Use when reviewing or maintaining chats and Codex task history from the Codex app:
  inventorying sidebar conversations, proposing body-derived titles, assessing
  same-repository supersession, or running a periodic organization pass.
---

# Codex Thread Organizer

Organize every accessible sidebar conversation from conversation evidence. Treat the skill as the decision workflow; an on-demand request or periodic Codex automation invokes it.

## Platform and Packaging Boundary

- This is a **Codex-app skill**: use it from Codex's native sidebar surface, including any ChatGPT conversations the app exposes there.
- Do not organize history owned by another client when it is not accessible in the Codex app (for example, Claude Code, Cursor, Gemini, or browser tabs).
- Do not assume repository presence means installation. This skill is active only in frozenSkillz's dedicated Codex package; installation and automation creation are separate, explicit operator actions.
- When installing from frozenSkillz, select the Codex consumer. Do not place this skill in a shared cross-client skill root.
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

1. **Inventory every accessible sidebar conversation.** Use the native list operation before filtering by kind. Record task ID, kind, host ID, current title, timestamps, working directory, and other routing metadata. Never exclude ChatGPT conversations, pinned conversations, or another returned kind merely because it is not a Codex task. If the operation has a page, cursor, or load-more control, exhaust it. If its maximum result count prevents that, record a `bounded inventory` with `partial coverage`, state the exact limit, and never describe the result as “all chats.”
2. **Classify title capability.** For each inventoried conversation, determine whether the native title operation supports its kind. Mark supported targets `title-mutable`; mark unsupported targets `not title-mutable` with the exact failed operation or missing capability. A user request to organize or rename “all chats” scopes every accessible conversation; it does not authorize silently shrinking that scope.
3. **Read the actual work.** Read enough of each body to understand the opening request, later changes of direction, substantive outcome, remaining work, and references to later tasks or durable artifacts. A title, preview, or first message is not enough.
4. **Group only with evidence.** Attribute a repository or project family from the working directory, repository identity, transcript evidence, or an explicit user mapping. Leave uncertain tasks unassigned.
5. **Compare related tasks when relevant.** If the scope includes relevance, age, duplication, or supersession, read the accessible bodies in the same family together. Follow [references/cross-task-review.md](references/cross-task-review.md).
6. **Draft the semantic title.** Apply the sparse symbol grammar in [references/title-grammar.md](references/title-grammar.md), then critique and revise the title once.
7. **Produce a frozen manifest.** Always include IDs, kinds, title capability, old and proposed titles, confidence, body-derived rationale, and proposed action. For cross-task reviews, include every field required by [references/cross-task-review.md](references/cross-task-review.md): repository family and attribution basis, classification, related task IDs and directed relationships, outcome and remaining work, plus inventory and coverage totals. Record inaccessible, unassigned, ambiguous, and not-title-mutable conversations.
8. **Apply only an authorized frozen batch.** Recheck each `title-mutable` target immediately before mutation. Skip and report concurrent changes. Use the native title operation that supports that conversation kind. Do not write an internal state store or pretend an unsupported kind was renamed.
9. **Verify independently.** Re-inventory or read back every mutated target and require an exact match before reporting success. A mutation acknowledgement is provisional. Report the full inventory total and separate mutated, already-correct, skipped, and not-title-mutable totals.

## Title Rules

- Use **one to five** leading semantic symbols, never five by default. Most titles should use one to three.
- Prefer one project or domain symbol, then an optional work-type symbol, then an optional lifecycle symbol.
- A fourth or fifth symbol is exceptional and must add a stable distinction. Never pad a title with decoration.
- Keep the words specific and recognizable, normally about 5–12 words.
- Preserve exact product, repository, issue, pull request, and artifact names when they aid recognition.
- Treat 60 UTF-16 code units as the empirically observed ceiling of Codex's native title operation. Enforce that ceiling only for `title-mutable` Codex targets; document a different verified limit before applying it to another conversation kind.
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
