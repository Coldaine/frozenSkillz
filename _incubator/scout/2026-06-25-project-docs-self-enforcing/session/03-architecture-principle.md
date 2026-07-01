# 03 — architecture.md: approach, not inventory

## The one sentence that has to make it

> **architecture.md is a description of the approach we have chosen to succeed at the
> goals, and why — NOT an inventory of the things in the project.**

The load-bearing words are **approach** and **why**. A list of components has neither.
An approach statement is "we chose X to serve goal Y / solve problem Z, accepting cost W."
That's the only thing that makes architecture.md self-enforcing: an agent reading "we
chose a CLI-first core reusable across service/API/MCP *because* the goal is one stable
surface with flexible execution" can make consistent downstream decisions. An agent
reading "Components: CLI, service, API, MCP, cache, logger" cannot — it has nothing to
weigh against.

## Where the current skill half-knows this and contradicts itself

The skill's `architecture-md-guide.md` names the exact failure:

> **The code inventory creep.** architecture.md grows into a description of every file.
> The diff between architecture.md and a `tree` of the repo shrinks toward zero. The fix
> is to push detail down into `docs/components/` and keep the top-level architecture doc
> strategic.

So it *sees* the problem. Then it mandates the structure that causes it. Its prescribed
sections include a **System Shape Table** (5–12 rows) and a **Major Components Table**
(Component / Status / Responsibility / Detail-link). Two inventory tables.

**The contradiction:** the guide warns against code-inventory creep and then hands you the
table template to do it with. "Keep it strategic, push detail to docs/components/" is a
principle; "fill in this 5–12 row component table" is an instruction that produces the
opposite. Agents follow the instruction, not the principle.

## The reframe — thesis-first, not inventory-first

Flip the center of gravity. **The Architecture Thesis (approach + why) IS the document.**
Everything else exists only insofar as it instantiates or evidences the thesis.

| Current skill (inventory-first) | Reframed (thesis-first) |
|---|---|
| Thesis is one section among ~10 | Thesis is the doc; everything else supports it |
| System Shape table (5–12 rows) required | Mention areas only as needed to explain the approach — prose, not a mandated table |
| Major Components table required | Name a component only when load-bearing for the approach |
| Status labels on every row | Status labels stay — they're approach-implementation state |
| Deep rationale lives in ADRs | Unchanged — ADRs hold per-decision why; architecture.md holds the strategic why |

## The rule of thumb

Parallel to the In/Out rule: **if a component or area doesn't have a "because" tying it
to a goal or the problem, it doesn't belong in architecture.md.** It belongs in
`docs/components/` or nowhere. The "because" is what stops it being a list.

## Where In/Out/Shape lands when it moves here

When Shape (and Caller) get exiled from NORTH_STAR, architecture.md is where they go —
and they fit naturally, because **Shape is part of the chosen approach.**

"CLI-first core, reusable across service/API/MCP, config at X" is an approach statement
with a why ("one stable surface, flexible execution"). That's no longer prescription
leaking into identity — it's prescription *properly seated* in the doc whose job is the
chosen approach.

In/Out stay in NORTH_STAR (conditional, when caller + Out are concrete) — that's the
scope filter, identity-level. Shape comes here. Clean split:

- **Identity holds scope.** (NORTH_STAR: In/Out)
- **Architecture holds approach + delivery.** (architecture.md: Shape/Caller + thesis)

## Implementation detail vs approach

The *shape decision* (CLI-first, one core, multi-entrypoint) belongs in architecture. The
*config path* and the *alias migration* are still too low-level even for architecture —
those are implementation, living in a conventions doc or the relevant component doc.
**Architecture holds the approach; it doesn't hold the file paths.**

## Status labels stay

Current/Planned/Candidate/Deferred survive the reframe. They're about approach
implementation state, so they belong on the thesis and its load-bearing pieces. The
"unlabeled aspiration" failure (future-state written as Current) is real and the labels
fix it — that part of the skill is correct and stays.
