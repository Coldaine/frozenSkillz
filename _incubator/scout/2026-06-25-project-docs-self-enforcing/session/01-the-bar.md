# 01 — The bar a project-docs skill has to meet

## The principle

The only reliable channel to a future agent is a doc that `AGENTS.md` forces it to read.
Commits, PRs, and issues are *reconstructable*, not *read*. No agent reads all of them
reliably mid-task. Therefore:

> A doc is only doing its job if an agent that follows it literally produces the same
> behavior as the agent that wrote it — and if the doc gets updated **in the same act**
> as the work, so the doc *is* the running state. If it isn't written down, it didn't
> happen, and we don't know why.

This is the **self-enforcing** bar. Test every part of the skill against it.

## What the current skill gets wrong (against this bar)

Most of the skill fails the bar not by being wrong, but by being **descriptive instead of
prescriptive**. It describes what good docs look like; it does not force the agent to
*maintain* them.

| Component | Tries to do | Shortcoming |
|---|---|---|
| NORTH_STAR guide | Identity, goals, anti-goals, pillars | Has a Requirements section = goals-as-validation. Accretes 6 sections; no size discipline. |
| architecture guide | Technical shape + status labels | Status labels are the best idea. But "5–12 rows, one line each" can't hold a real build plan — offloads plans to nowhere. |
| PROGRESS guide | Rolling handoff window | Doomed by its own admission (becomes a diary / `git log` wins). Competes with GitHub. Not self-enforcing — nothing forces the roll-off. |
| AGENTS guide | Router, 20-line cap, lazy paths | Router idea right. But 20-line cap + Handoff Format section fight each other; `@`-eager-load mechanics are Claude-specific dressed as universal. |
| Overflow folders (decisions/components/workflows/history) | Homes for expelled content | `history/` is pure ritual. **No `plans/` bucket** — the one doc type written most. Boundaries between folders overlap. |
| authority-flow | Cross-doc conflict detection | Good concept. "Downstream is always wrong" too rigid — sometimes upstream is stale. |
| write-workflow (interview→draft→provenance→review) | Authoring process | Provenance tags `[OWNER]/[INFERRED]/[OPEN]` vanish on finalize — can't help the *next* agent. Self-enforcing needs persistent markers, not throwaway ones. |
| review-checklist (structural/drift/style) | Critique existing docs | Findings are advisory; nothing forces action. Drift findings require a human to run the checklist. |
| guardian-relationship | Future runtime separation | Every guide has "What the Guardian Does" tables for a system that doesn't exist. Pure ceremony today. |

## The pattern across all of them

They tell you what good looks like, but **nothing makes the agent keep it good.** That's
the gap the redesign fills.

## The test the redesign has to pass

Run an agent in a loop adding features over and over. Watch whether the system
**converges** (later agents, reading only the docs, do it the same way) or **drifts**
(each agent re-infers and the conventions rot).

The money result: **a self-enforcing doc set eventually reaches a state where the agent
changes only code because the conventions are already written.** If it never stops
needing doc edits, the docs aren't self-enforcing — they're a treadmill.

## Three loops the redesign has to serve

### Loop 1 — Project over time (lifecycle)

Questions that live here: "great idea but not now → where?", "what do I need to know
about the project right now?"

- No "shelf" doc type in the current skill → ideas get smuggled into NORTH_STAR (bloat)
  or PROGRESS (roadmap smuggle) or lost.
- "What do I need to know right now" has no home — PROGRESS is a handoff window, not an
  orientation doc.
- Archive step undefined — completed work piles up and rots.

### Loop 2 — Scoping what we want vs what exists

- The steady-state node ("docs already prescribe this; no doc edit needed") is the whole
  point — and the current skill never names it.
- "What exists today" is split across architecture labels + code + PROGRESS with no
  reconciliation rule an agent will run.
- Novelty → WriteDoc is not enforced. The self-enforcing seam is missing.

### Loop 3 — Preventing the top failure patterns

Two named failures:
1. **Minor rule explodes into a major rule** — what NORTH_STAR anti-goals were supposed
   to prevent. A minor constraint becomes major by being written into a high-authority
   doc. The current skill has no guard against this.
2. **NORTH_STAR bloat + prescription creep + goals-as-validation** — agents infer
   implementation from goals ("goal says fast search → use Meilisearch") and write it
   into NORTH_STAR. No "no prescriptions" rule. No "permissive default, one or two
   anti-goals" rule. Requirements section is the checking-off mechanism we reject.

## Overall grade of the current skill

**C−** — good essay, incomplete system, not battle-tested. Ambitious theory, weak as
something you'd actually live in. Not "terrible" end-to-end — real thinking in it — but
over-specified in places that don't matter (Guardian tables, provenance ceremony) and
under-specified in the places that make it self-enforcing.

> User note: "over-specified" was the wrong frame. The problem is the opposite — it's
> under-specified in the places that make it self-enforcing, and over-specified in the
> places that don't matter. Detailed documentation is the whole point; agents can only
> infer otherwise.
