# Guardian Relationship

The Guardian is downstream of the documentation skill. The documentation skill comes first; it produces and repairs the authority documents the Guardian may later consume.

The Guardian should not invent documentation rules. It consumes the same branch guides and review checklists the skill uses, but executes them in PR, repo-monitoring, drift-review, or variance contexts.

---

## What the Guardian Is

A future runtime that may inspect repo changes, PRs, branches, or agent activity against the project authority docs.

It may eventually detect:

- project drift (active work crosses NORTH_STAR anti-goals)
- architecture drift (current implementation diverges from architecture.md Current claims)
- undocumented decisions (architecturally significant choices made without ADRs)
- stale progress state (PROGRESS.md no longer reflects reality)
- AGENTS.md bloat (inlined doctrine, enumeration drift, `@` references)
- North Star conflicts (a PR crosses a goal or anti-goal)
- variance from intentional tradeoffs (a PR departs from a pillar without acknowledgment)

---

## What the Guardian Is Not

The Guardian is not the project-docs skill.

The skill:
- creates docs
- reviews docs
- reconciles docs
- proposes edits
- surfaces conflicts as findings

The Guardian:
- watches activity
- compares changes against authority
- reports drift
- may comment in PRs
- may run in hooks, GitHub Actions, or CI

The skill operates at *authoring time*. The Guardian operates at *PR time* and *runtime*. They share the same rules and the same authority documents; they differ in when and how they enforce.

---

## Why the Separation Matters

If the skill absorbs Guardian semantics, two failure modes appear:

1. **The skill starts blocking.** A skill that returns "VIOLATION: this is a hard block" turns the authoring experience into a CI workflow. Authoring needs to be conversational and exploratory; blocking belongs at the PR boundary, not the author's desk.

2. **The Guardian starts inventing rules.** A Guardian that doesn't defer to the skill's branch guides will produce its own interpretations of "what good looks like." Those interpretations drift from the skill's interpretations. The agent gets two different sets of feedback for the same work.

The clean separation is: **the skill defines the rules; the Guardian executes them at PR time.**

---

## Reserved Vocabulary

Use Guardian vocabulary only for the future runtime:

- enforcement
- violation
- blocker
- severity
- CI failure
- PR gate
- policy engine

Inside the skill, use:

- finding
- review note
- conflict
- alignment issue
- authority-flow check
- suggested edit

When a skill response uses Guardian vocabulary, that is a signal the skill is overstepping its scope. Watch for it.

---

## What the Guardian Consumes

The Guardian consumes the four primary documents:

```
NORTH_STAR.md     — project intent and boundaries
architecture.md   — technical strategy and shape
PROGRESS.md       — current handoff state
AGENTS.md         — agent operating contract
```

It also consumes the four overflow destinations:

```
docs/decisions/   — durable decisions (ADRs)
docs/components/  — subsystem detail
docs/workflows/   — long procedures
docs/history/     — archived progress
```

The Guardian does not define any of these. It reads them, compares repo behavior against them, and reports drift.

---

## How the Guardian Uses Each Doc

| Doc | Guardian's question on a PR |
|---|---|
| NORTH_STAR.md | Does this PR cross a goal, anti-goal, or pillar? Does the bet/why/goal still hold? |
| architecture.md | Does this PR violate an invariant? Does it advance a Planned item to Current without updating the label? Does it make an architecturally significant decision without an ADR? |
| PROGRESS.md | Does this PR end substantial work without updating handoff state? Are completed items rolled out? |
| AGENTS.md | Does this PR add a new task category that the decision tree doesn't cover? Does it change commands without updating the section? Does it leak doctrine into a tool-specific file? |
| `docs/decisions/` | Does this PR contain a decision that should be an ADR? |

---

## Open Guardian Questions

The Guardian runtime is not yet built. Open design questions, captured here so they don't get answered implicitly by the skill:

- Should the Guardian mirror authority docs into an orphan branch, a separate repo, or an external store?
- Does the Guardian run as a CLI, GitHub Action, local hook, or all three?
- Should findings be advisory only, or can they become blocking in PR contexts?
- How does the Guardian avoid false positives?
- How does it capture multi-agent provenance (which agent made which change)?
- How does it record intentional variance (a PR that crosses a pillar with acknowledged justification)?

These are *runtime* design questions. They are not skill design questions. The skill should not answer them implicitly through how it phrases findings or how it suggests edits.

---

## When the Skill Should Mention the Guardian

The skill mentions the Guardian only when:

1. The user asks about runtime enforcement.
2. The skill is being asked to do something that is the Guardian's job (block a PR, fail a build, assign severity), and the skill needs to redirect.
3. A doc is being authored that requires a route to "where boundaries get enforced." That route should say "the future Guardian" rather than naming a system that doesn't exist yet.

Otherwise, the skill operates as if the Guardian doesn't exist. The skill is sufficient on its own at authoring time.
