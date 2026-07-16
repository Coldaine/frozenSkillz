# Guardian Relationship

The Guardian is downstream of the documentation skill. The documentation skill comes first; it produces and repairs the authority documents the Guardian may later consume.

The Guardian should not invent documentation rules. It consumes the same guides and review checklists the skill uses, but executes them in PR, repo-monitoring, drift-review, or variance contexts.

---

## What the Guardian Is

A future runtime that may inspect repo changes, PRs, branches, or agent activity against the project authority docs.

It may eventually detect:

- project drift (active work crosses NORTH_STAR anti-goals)
- architecture drift (implementation diverges from architecture.md Current claims)
- undocumented decisions (architecturally significant choices without ADRs)
- stale current-work homes (open Issues/plans contradict living docs)
- leftover legacy handoff (`PROGRESS.md` or `docs/history/` still present / still routed)
- AGENTS.md bloat (inlined doctrine, enumeration drift, `@` inside AGENTS)
- North Star conflicts (a PR crosses a goal or anti-goal)
- variance from intentional tradeoffs (a PR departs from a pillar without acknowledgment)

---

## What the Guardian Is Not

The Guardian is not the project-docs skill.

The skill creates, reviews, reconciles, proposes edits, and surfaces conflicts as findings.

The Guardian watches activity, compares changes against authority, reports drift, may comment in PRs, may run in hooks/Actions/CI.

Authoring time vs PR/runtime. Same rules; different when/how.

---

## Why the Separation Matters

1. **The skill must not block.** Blocking belongs at the PR boundary.
2. **The Guardian must not invent rules.** It defers to this skill’s guides.

**The skill defines the rules; the Guardian executes them at PR time.**

---

## Reserved Vocabulary

Guardian-only: enforcement, violation, blocker, severity, CI failure, PR gate, policy engine.

Skill: finding, review note, conflict, alignment issue, authority-flow check, suggested edit.

---

## What the Guardian Consumes

Primary authority:

```
NORTH_STAR.md     — intent and boundaries
architecture.md   — technical strategy and shape
AGENTS.md         — agent router / operating contract
```

Living overflow:

```
docs/decisions/              — ADRs
docs/components/ or topics   — subsystem detail
docs/workflows/              — long procedures
docs/plans/ and/or Issues    — current work (not authority rungs)
```

Not recommended inputs: `PROGRESS.md`, `docs/history/` (legacy; flag if present).

---

## How the Guardian Uses Each Doc

| Doc | Guardian's question on a PR |
|---|---|
| NORTH_STAR.md | Does this PR cross a goal, anti-goal, or pillar? |
| architecture.md | Invariant violated? Planned→Current without label update? Decision without ADR? |
| Issues / `docs/plans/` | Does active work contradict living authority? Finished plan left undeleted after promote? |
| AGENTS.md | New task category missing from routes? Commands changed without update? Doctrine in tool stub? |
| `docs/decisions/` | Decision that should be an ADR? |

---

## Open Guardian Questions

Runtime design (not for the skill to answer implicitly):

- Mirror location for authority docs?
- CLI vs Action vs hook?
- Advisory vs blocking?
- False-positive control?
- Multi-agent provenance?
- Intentional variance recording?

---

## When the Skill Should Mention the Guardian

Only when the user asks about runtime enforcement, when asked to block/fail/assign severity (redirect), or when a doc needs a route to “where boundaries get enforced later.”

Otherwise operate as if the Guardian does not exist.
