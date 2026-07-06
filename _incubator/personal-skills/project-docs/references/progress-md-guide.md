# How to Write a PROGRESS.md

`PROGRESS.md` is the session continuity document. It owns the current handoff window: what's happening now, what's blocked, and what the next session should focus on.

It is *not* a permanent diary, a full project history, a roadmap, architecture doctrine, a place to bury durable decisions, or a dumping ground for chat summaries.

A PROGRESS.md that has not been rolled in three months will be longer than `architecture.md` and less useful than `git log`. The discipline of this document is staying small.

---

## The Load-Bearing Principle

> PROGRESS.md is a rolling handoff window, not a project history. Anything that's no longer load-bearing for the next session has a different home.

The handoff window is what the next session needs to pick up work. Everything older rolls off:

- Completed items older than the window → `docs/history/YYYY-MM.md`
- Durable decisions made along the way → `docs/decisions/`
- Architecture notes that emerged → `architecture.md` or `docs/components/`
- Long procedures that crystallized → `docs/workflows/`

---

## What PROGRESS.md Owns and Does Not Own

PROGRESS.md owns:

- current state
- active work
- blockers
- next-session focus
- unresolved decisions
- recently changed context that affects next work

PROGRESS.md does not own:

- project intent → `NORTH_STAR.md`
- technical strategy → `architecture.md`
- durable decisions → `docs/decisions/`
- detailed implementation notes → `docs/components/`
- long procedures → `docs/workflows/`
- old completed work → `docs/history/`

---

## What Goes In, What's Optional, What Accretes

| Section | When to include | When to skip or defer |
|---|---|---|
| Current State | Always. | Never skip. |
| Active Work (table) | Always once work spans more than one item. | Single-task projects can collapse into Current State. |
| Blockers / Decisions Needed | When something is genuinely blocked or waiting. | If nothing is blocked, the section is empty. Do not list "potential" blockers. |
| Next Session Focus | Always. | Never skip. |
| Recently Changed | When the last session changed context that affects the next session. | If nothing notable changed, the section is empty. |
| Roll-Off / Archive note | Always. The discipline of rolling off needs to be visible in the file itself. | Never skip. |

**Minimum viable PROGRESS.md: Current State + Next Session Focus.**

---

## Current State

One short paragraph. Where the project stands right now, in plain language. Three to five sentences.

### Rules

- **Present tense.** "The skill is drafted; reviews are pending." Not "We have been drafting..."
- **No history.** Where things stand, not how they got there. History belongs in `docs/history/`.
- **No roadmap.** Where things stand, not where they're going. Direction belongs in NORTH_STAR.md.

### Failure mode

A Current State section that has grown into a paragraph-per-month timeline. That's history, not state.

---

## Active Work

A table of in-flight workstreams:

| Workstream | Status | Next Action |
|---|---|---|
| (name) | (drafting / in review / blocked / etc.) | (the immediate next step) |

### Rules

- **Status uses short verbs or adjectives.** "drafting," "in review," "blocked," "merging." Not paragraphs of explanation.
- **Next Action is one line.** If the next action is a multi-step procedure, the procedure belongs in `docs/workflows/` and Next Action says "follow X workflow."
- **No completed rows.** Move them to `docs/history/`.
- **Three to seven rows.** More than seven and the project is over-committed; some rows are stale.

### Failure mode

Active Work that hasn't been touched in weeks. If a row's status hasn't changed in a month, either it's actually a blocker (move it to Blockers) or it's abandoned (move it to history or remove).

---

## Blockers / Decisions Needed

A table of things waiting on input:

| Decision | Needed From | Link |
|---|---|---|
| (what needs deciding) | (whom, or what condition) | (link to context if relevant) |

### Rules

- **Decisions only.** If a thing is blocked on a build failure or a network outage, it's not a decision; it's an issue. Use the issue tracker.
- **Needed From is concrete.** A name, a role, or a condition. Not "TBD."
- **Resolved decisions move to `docs/decisions/`.** Do not leave resolved entries sitting in this table.

### Failure mode

A Blockers list that fills up with things nobody owns. The table becomes a graveyard of "someone should think about this." Each row needs a real owner or it gets removed.

---

## Next Session Focus

A numbered list of the next one to five concrete actions.

### Rules

- **One to five items.** More than five and the next session is over-committed.
- **Numbered, not bulleted.** Order matters; the first item is what gets picked up first.
- **Concrete.** "Draft `docs/guides/agents-md.md`" is concrete. "Continue working on docs" is not.
- **Actions, not aspirations.** "Get sign-off from owner" is fine. "Eventually finish the skill" is not.

### Failure mode

Next Session Focus that lists every item from a roadmap. The agent reads it and tries to do everything at once.

---

## Recently Changed

Short list of context changes from the last session that affect the next one.

### Rules

- **Recent only.** If a change is older than the handoff window, it doesn't belong here.
- **Affecting next work only.** "We finished phase 1" is fine if phase 2 starts next session. "We had a long discussion about Redis" is not, unless the conclusion affects next work.
- **One-line entries.** If something needs paragraphs, it should be in `docs/decisions/` or `architecture.md`.

### Failure mode

Recently Changed that becomes a dumping ground for "things I discussed in chat." The agent gets context that doesn't help, and the useful changes get lost.

---

## Roll-Off / Archive

A short standing note in the file:

```
Completed items older than the current handoff window move to:
- docs/history/YYYY-MM.md
- docs/decisions/
- release notes
- issue tracker
```

### Rule

This note is not just documentation; it is the convention. When the file gets pruned, this section explains where things went.

---

## What Piles Up in Bad PROGRESS.md

The pattern of decay looks like this:

- every completed task ever
- long chat summaries
- stale todo lists
- abandoned plans
- unresolved questions that were later resolved (but never moved out)
- running commentary
- version history
- roadmap material
- architecture notes
- "next steps" from six sessions ago

The result: the agent opens it and cannot tell what matters now.

---

## What the Guardian Does with Each Section

| Section | Guardian asks | On violation |
|---|---|---|
| Current State | "Is this state, or is this history?" | Suggest rolling history items to `docs/history/`. |
| Active Work | "Are completed rows still present? Are stale rows lingering?" | Suggest archival. |
| Blockers / Decisions Needed | "Are resolved decisions still here? Are open ones owned?" | Suggest moving resolved entries to `docs/decisions/`. |
| Next Session Focus | "Is this actionable, or aspirational?" | Soft-block PRs that change this without removing yesterday's items. |
| Recently Changed | "Is this affecting next work, or is this commentary?" | Suggest moving non-actionable items out. |
| File-level | "Has this file been pruned in the last handoff window?" | Surface staleness. |

---

## Review Questions

When reviewing PROGRESS.md, walk these:

- Is this a handoff window, or a permanent diary?
- Are completed items rolled into `docs/history/`?
- Are decisions moved to `docs/decisions/`?
- Are blockers current and owned?
- Is next-session focus still actionable?
- Is roadmap material being smuggled into progress?
- Is architecture being rewritten in progress notes?

If any answer is wrong, the fix is movement, not deletion. The content goes somewhere; it just doesn't stay in PROGRESS.md.

---

## Common Failure Modes

**The accreting diary.** Every session appends; nothing rolls off. After three months, PROGRESS.md is 3000 lines. Nobody reads it. The agent gives up and infers state from `git log` instead.

**The buried decision.** A consequential choice gets written into a Recently Changed bullet and never makes it to `docs/decisions/`. Two months later, no one remembers why the choice was made.

**The roadmap smuggle.** Future plans creep into Next Session Focus. The list grows to twenty items. The agent reads them as committed work.

**The dead blocker.** A blocker sits there for weeks because nobody owns the resolution. The list of blockers stops being a working tool and becomes a wall of stuck items.

**The architecture rewrite.** A subsystem decision gets explained in PROGRESS.md instead of `architecture.md`. The explanation grows; architecture.md never gets updated. Two sources of truth, both partial.

---

## When PROGRESS.md and Downstream Docs Disagree

PROGRESS.md is downstream of NORTH_STAR.md and architecture.md.

- If PROGRESS.md's Active Work conflicts with NORTH_STAR's anti-goals (the project is drifting from its stated identity), **the conflict is a finding**, not just a PROGRESS update. Surface it.
- If PROGRESS.md's Current State disagrees with architecture.md's Current status labels, **architecture.md wins for technical truth**; PROGRESS.md is updated.
- If PROGRESS.md contains durable decisions that should be ADRs, they move to `docs/decisions/`. The ADR is referenced from PROGRESS.md, not duplicated.

PROGRESS.md is the most volatile of the four primary docs. Its disagreement with upstream docs is almost always resolved by updating PROGRESS.md or by moving its contents to their proper home.
