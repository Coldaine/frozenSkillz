# How to Write an AGENTS.md

AGENTS.md is the file every agent in your repo reads first, every session. It is the universal entry point: Codex CLI reads it, Cursor reads it, OpenCode reads it, and Claude Code reads it through a small `CLAUDE.md` stub that eager-loads it alongside NORTH_STAR.md.

Because AGENTS.md is always loaded, every line in it pays a token cost on every session and competes for the model's limited instruction-following capacity. The discipline of this document is *not* "what could be useful to know about this project." It is "what does the agent absolutely need in active context to start working correctly, and where does it find everything else."

A good AGENTS.md does two things: it tells the agent *what this project is*, and it routes the agent to *what to read next based on what they're about to do*. Anything beyond those two jobs is drift.

---

## The Load-Bearing Principle

> Inline nothing. AGENTS.md is a pure router: authority order, task routes, a stop rule, and commands. The project's identity is not restated here; it is eager-loaded from NORTH_STAR.md so the owner's actual opener and anti-goals sit in context with zero duplication. Everything else loads lazily via bare paths.

This rule prevents the document's two primary failure modes (enumeration drift and a drifting second copy of the identity) and exploits the agent harness mechanics correctly:

- `@` references in Claude Code resolve **eagerly and recursively** at session start, pulling referenced files into the active context window before the first user prompt.
- Bare paths (`See docs/architecture.md`) read as instructions, not imports; the agent's Read tool resolves them **lazily** only when the agent decides the file is relevant to the task at hand.

If you put `@` references on architecture, PROGRESS, decisions, or components, every linked file enters active context on every session whether or not the work needs them. That defeats the router. Bare paths preserve selection.

Eager loading is correct for exactly two files: AGENTS.md (the router) and NORTH_STAR.md (the frame). Both are small and relevant to every task; everything else is larger and task-specific, so it stays lazy. The eager-load is a Claude Code mechanic, so it lives in the Claude-specific `CLAUDE.md` stub, which is exactly two lines:

```
@AGENTS.md
@NORTH_STAR.md
```

No header. No prose. Those two `@` references are the only ones in the system. Re-stating NORTH_STAR's identity inside AGENTS.md as prose, or `@`-referencing any third file, is a violation.

## The 60-Line Cap

AGENTS.md is hard-capped at 60 lines. With NORTH_STAR it is one of only two always-loaded documents, so every line competes for the model's limited instruction-following budget on every session. The cap is deliberately generous enough for a large repo to route every task category, list its real commands, and point at its exception process; it is not generous enough to let AGENTS.md inline content that belongs in another doc.

The cap governs routes, commands, and hard rules, never prose. AGENTS.md growing toward 60 lines because it is accumulating one-line routes and commands is the document working as intended. AGENTS.md growing toward 60 lines because it is inlining identity, decisions, procedures, or status is the cap defeated: that content is in the wrong home, and identity belongs in NORTH_STAR, decisions in architecture.md or `docs/decisions/`, procedures in `docs/workflows/`, status in PROGRESS.md.

The cap is a forcing function, not a style preference: a line earns its slot only if it is a route, a command, or a hard rule that is needed on most tasks, costly to get wrong, and cannot be safely deferred to a lazy read. When a line is anything other than a route, a command, or a hard rule, it does not belong in AGENTS.md; route to it instead.

---

## Order of Operations

AGENTS.md sits at the bottom of the authority chain. It derives from everything above it.

1. NORTH_STAR.md (identity, goals, anti-goals, pillars)
2. architecture.md (technical decisions and rationale)
3. PROGRESS.md (current status and phase)
4. AGENTS.md (the route)

Write AGENTS.md last. NORTH_STAR.md must exist first, because AGENTS.md eager-loads it and routes to it; AGENTS.md no longer restates identity.

---

## What AGENTS.md Owns and Does Not Own

AGENTS.md owns:
- agent onboarding
- authority routing (the decision tree)
- essential commands
- hard working rules
- handoff format
- compatibility notes for tool-specific files

AGENTS.md does not own:
- project purpose, goals, anti-goals → `NORTH_STAR.md`
- technical strategy and system shape → `architecture.md`
- current task handoff state → `PROGRESS.md`
- durable decisions → `docs/decisions/`
- detailed subsystem documentation → `docs/components/`
- long procedures → `docs/workflows/`
- archived progress → `docs/history/`

The trap is not just *people dump every doc into AGENTS.md*. The trap is *whatever does not fit cleanly into AGENTS.md gets shoved into architecture.md or PROGRESS.md, and then those become junk drawers*. The decision tree must route to the overflow destinations as well as the primary docs.

---

## What Goes In, What's Optional, What Accretes

| Section | When to include | When to skip or defer |
|---|---|---|
| NORTH_STAR pointer (first line) | Always. | Never skip. |
| Decision tree | Always, once the project has more than one kind of agent task. | A brand-new project with one task category may begin with one or two bare pointers and grow the tree as new task categories emerge. |
| Commands | When the project has commands an agent needs to run (install, test, lint, build). | Pure documentation projects. Research-only repositories. |
| Working rules | When the project has hard rules that apply project-wide to all work. | If your only rules are linter-enforced or already covered by NORTH_STAR's anti-goals, skip. Vague rules don't belong here at all. |
| Handoff format | When PROGRESS.md exists and the project spans sessions. | Single-session projects. |
| Compatibility note | When CLAUDE.md or other tool-specific files exist. | If no tool-specific files exist. |
| Operational negative space | If the agent harness keeps drifting into a specific failure mode that NORTH_STAR's anti-goals don't catch at the operational level. | Default: skip. NORTH_STAR usually covers this. |

**Minimum viable AGENTS.md: the NORTH_STAR pointer (first line) + the route-by-task + the authority line + the stop rule.**

Commands and working rules accrete as the project grows the surface that needs them.

---

## No Inline Identity

AGENTS.md does not contain an identity statement. Identity lives in NORTH_STAR.md's opener (one sentence) and its anti-goals (what the project is mistaken for), and it reaches the agent's context by being eager-loaded through the CLAUDE.md stub, not by being copied here.

AGENTS.md's first line is a pointer, not a paraphrase:

```
Read NORTH_STAR.md first. Do not infer intent from code.
```

### Rules

- **No restatement.** Do not summarize, distill, or "frame" the opener. The eager-loaded NORTH_STAR is already in context; a second version only creates a thing that can drift.
- **The pointer is one line.** It names NORTH_STAR and states the one operating rule that the eager-load cannot enforce by itself: do not infer intent from code.
- **No goals, no anti-goals, no pillars, no commands, no status in the pointer.** Each lives in its own home and reaches the agent through the eager-load or the route-by-task.

### Failure mode

Re-adding an identity paragraph "so the agent sees it without opening NORTH_STAR." If NORTH_STAR is eager-loaded, the agent already sees the real opener; a second copy buys nothing and rots. The first of the two to drift wins, unpredictably. The fix when you find one is deletion, not reconciliation.

---

## The Decision Tree

The body of AGENTS.md. The agent walks the tree before doing anything else; the leaves route to the files and skills relevant to that task.

The ASCII form below is the teaching form: it shows the full routing logic. The production form, under the 60-line cap, is a compressed list of one-line routes (see `examples/AGENTS.md`). Same routes and same rules, no box-drawing.

### Structure

```
What are you about to do?
│
├─ Understand the project's intent, scope, boundaries
│  → docs/NORTH_STAR.md
│
├─ Make a technical or architectural decision
│  → docs/NORTH_STAR.md (goals and anti-goals)
│  → docs/architecture.md (technical strategy, current shape, invariants)
│  → docs/decisions/ (existing ADRs; if your decision is durable, add one)
│
├─ Implement, fix, refactor, pick up active work
│  → docs/PROGRESS.md (current handoff, blockers, next focus)
│  → docs/architecture.md (the subsystem you're touching)
│  → docs/components/ (deep detail on the subsystem if needed)
│
├─ Write or review documentation
│  → Invoke the project-docs skill
│
├─ Run a long procedure
│  → docs/workflows/[procedure].md
│
├─ Look up historical context (completed work, prior milestones)
│  → docs/history/
│
├─ Operate the build, run commands, work with CI
│  → See Commands below
│
└─ Anything that crosses a goal, anti-goal, pillar, or invariant
   → Stop. Surface the conflict. Discuss with maintainer.
```

### Rules

- **Bare paths only at leaves.** No `@`. The tree's selectivity depends on lazy loading.
- **Three to seven top-level branches.** Fewer: the tree isn't doing real selection. More: branches are too granular and some are procedures, not categories.
- **Routes to all five legal homes for content.** The four primary docs (NORTH_STAR, architecture, PROGRESS, AGENTS) plus the four overflow destinations (decisions, components, workflows, history). A tree that only points at the primary docs forces overflow back into the primaries.
- **Branches must be mutually distinguishable.** If an agent can plausibly walk two branches for the same task, the agent will pick the wrong one about half the time. Test by asking: for each of the last ten PRs in this repo, which branch would the agent have walked? If any PR fits two branches, the tree needs sharpening.
- **First branch is "understand the project."** Routes to NORTH_STAR.md.
- **Last branch is "boundary crossing."** Routes to "Stop. Surface the conflict." This is the seam where AGENTS.md hands off to the future Guardian runtime: the tree teaches the agent to recognize boundary-crossing at authoring time; the Guardian enforces the same boundary at PR time.
- **Procedures don't live in the tree.** A leaf that says "do X then Y then Z" is a procedure and belongs in `docs/workflows/`. The leaf should route there, not inline the steps.

### Failure modes

- **The shallow tree.** Two branches: "code stuff" and "everything else." The tree does no work; it's a label, not a router.
- **The deep tree.** Twenty branches, each for a micro-task. The tree itself becomes longer than the docs it routes to.
- **The overlapping tree.** Branches that aren't distinguishable. "Implementing a feature" and "Adding new code" route differently. The agent can't pick consistently.
- **The procedural leaf.** A leaf containing the actual steps instead of routing to `docs/workflows/`. The procedure ages poorly; AGENTS.md grows.
- **The dead leaf.** A bare path points at a file that was renamed or deleted. The agent reads the instruction and the Read tool fails. Better than `@` (which would have eagerly failed at load time), but still rot.
- **The missing overflow.** No branches route to `docs/decisions/`, `docs/components/`, `docs/workflows/`, or `docs/history/`. The overflow content has nowhere to go and ends up back in the primary docs.

---

## Commands

Operational commands an agent needs to run: install, build, test, lint, branch policy.

### Rules

- **One line each.** Format: `- Action: command`. Example: `- Test: pytest tests/`.
- **No explanation inline.** If a command needs a paragraph of context, the paragraph belongs in `docs/`, not here. The command stays one line.
- **No aspirational commands.** If `make deploy` doesn't exist yet, don't list it. AGENTS.md describes the current state.
- **Branch policy if non-default.** "Branch from main; PR to main; no direct pushes" is one line.

### Failure mode

Commands that don't actually work. An agent runs them, they fail, the agent now doesn't trust the rest of AGENTS.md.

---

## Working Rules

Hard rules that apply project-wide to all work. The shorter this list, the better; every entry pays a token cost on every session.

### Rules

- **Each rule must be enforceable.** Either by linter, by reviewer, by hook, or by the project-docs skill itself. "Be thoughtful with the codebase" is not a rule. "All Python code must pass `ruff check`" is. "Do not bury architecture decisions in PROGRESS.md" is enforceable by the skill's review checklist. "Documentation lives only in the doc homes; implementation directories hold no prose docs" is enforceable by the skill.
- **No conditional rules.** A rule that only applies in some contexts doesn't belong in always-loaded AGENTS.md. Move it to the relevant tree leaf or to architecture.md.
- **No style nits the linter handles.** Indentation, quote style, trailing commas are configuration, not instruction. Configure the linter and let the linter speak.
- **Five to ten total, hard ceiling.** More than ten and the rules start losing weight.

### Failure mode

Rules that everyone has stopped following but nobody has removed. The list ages into noise.

---

## Handoff Format

When PROGRESS.md exists, the AGENTS.md handoff section tells the agent how to update PROGRESS.md at the end of substantial work. This is a short rule, not a procedure.

Example:

```
## Handoff Format

Before ending substantial work, update PROGRESS.md with:
- current state
- active work
- blockers
- next-session focus
- links to any new decisions or docs

Roll completed work older than the current handoff window into docs/history/.
```

### Rule

If the handoff format exceeds five or six lines, move it to `docs/workflows/handoff.md` and route to it from the tree.

---

## Compatibility

If `CLAUDE.md`, `.cursorrules`, or similar tool-specific files exist, AGENTS.md should declare the relationship in one line each. Example:

```
## Compatibility

CLAUDE.md must contain only `@AGENTS.md` and `@NORTH_STAR.md`. No prose, no header.
```

### Rule

Tool-specific files do not hold doctrine. They point back to AGENTS.md. If you find yourself writing the same rule in AGENTS.md and a tool-specific file, the tool-specific file should be reduced to a pointer.

---

## What the Guardian Does with Each Section

| Section | Guardian asks | On violation |
|---|---|---|
| NORTH_STAR pointer | "Does this PR change the project's identity?" | Identity lives in NORTH_STAR.md; it must change there. AGENTS.md restates nothing, so nothing follows here. |
| Decision tree | "Does this PR introduce a new category of task not represented in the tree?" | Surface the gap. The tree should grow or the PR should fit an existing branch. |
| Commands | "Does this PR add, remove, or change a runnable command?" | Update the commands section. Hard-block if a new required command is undocumented. |
| Working rules | "Does this PR violate a hard rule?" | Hard-block with citation. |
| Handoff format | "Did this PR end substantial work without updating PROGRESS.md?" | Soft-block. Request handoff update. |
| Compatibility | "Does this PR add doctrine to a tool-specific file?" | Hard-block. Move doctrine to AGENTS.md; reduce tool-specific file to a pointer. |

---

## Common Failure Modes

**Enumeration drift.** The tree starts as a router. Over time, contributors add a new bullet under "Other files to know about." Six months later, AGENTS.md is a flat list of every doc in the repo. The tree is dead. Selection is gone.

**The `@`-inside-AGENTS.md violation.** Someone "improves" the bare paths by adding `@` symbols. The eager loader now pulls every referenced file into context on every session. The router becomes an index that loads everything upfront.

**The duplication trap.** A goal from NORTH_STAR.md feels important enough to "also mention here." A decision from architecture.md gets summarized "for convenience." Two months later, the AGENTS.md copy and the source have drifted. The agent reads both and applies whichever it reads first.

**Tool-specific cruft.** Cursor-specific rules, Claude hook semantics, Copilot instructions all end up in the shared AGENTS.md. Codex reads about Claude hooks that don't exist in its harness. Cursor reads about Copilot extensions.

**The aspirational AGENTS.md.** Commands that don't exist yet. Rules that aspire to be followed. Phases that haven't started. Every aspirational line is a lie the agent will act on.

**The vague rule list.** "Write clean code." "Be respectful of the codebase." These take token budget, contribute nothing actionable, and dilute the rules that are real.

**The missing-overflow tree.** A decision tree that only routes to the four primary docs forces overflow content back into them. architecture.md becomes a code inventory; PROGRESS.md becomes a diary. The fix is in AGENTS.md: route to `docs/decisions/`, `docs/components/`, `docs/workflows/`, `docs/history/`.

---

## When AGENTS.md and Downstream Docs Disagree

The authority order is fixed:

1. NORTH_STAR.md (owns identity, goals, anti-goals, pillars)
2. architecture.md (owns technical decisions; derives from NORTH_STAR)
3. PROGRESS.md (owns current status; derives from phases)
4. AGENTS.md (owns the route; derives from everything above)

AGENTS.md no longer restates identity, so it cannot disagree with NORTH_STAR's opener; it eager-loads and routes to it.
If AGENTS.md's commands disagree with what `make` or `package.json` actually does, the code wins; AGENTS.md is updated.
If AGENTS.md's handoff format disagrees with what PROGRESS.md expects, the convention agreed in NORTH_STAR or `docs/workflows/handoff.md` wins; AGENTS.md is updated.

AGENTS.md never holds authority of its own. It is plumbing: it routes the agent to the documents that hold authority. When AGENTS.md drifts from those documents, AGENTS.md is always the wrong one.
