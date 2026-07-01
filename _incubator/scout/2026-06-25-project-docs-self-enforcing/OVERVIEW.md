# Conversation overview — project-docs self-enforcing redesign

> An index and reflection over the 2026-06-25 session that produced this scout snapshot.
> Read this first to orient; then dive into `session/` for the detail.

## The question that opened it

The session started with a mundane orientation question (open PRs, what's in flight) and
a challenge to a documentation habit: "Is `PROGRESS.md` actually how we're tracking
things? I don't like that." That surfaced two facts:

1. The MooseGoose repo doesn't use `PROGRESS.md` — it uses `docs/north_star.md` + `docs/plans/*`.
2. The `project-docs` skill at `~/.agents/skills/project-docs/` *does* prescribe PROGRESS.md
   as part of a four-doc authority stack.

That mismatch kicked off a critique of the skill, which became the design session.

## The thesis that emerged

> The only reliable channel to a future agent is a doc that `AGENTS.md` forces it to read.
> Commits, PRs, and issues are *reconstructable*, not *read*. So a doc is only doing its
> job if an agent that follows it literally produces the same behavior as the agent that
> wrote it — and if the doc gets updated **in the same act** as the work.
> **If it isn't written down, it didn't happen, and we don't know why.**

The current skill describes what good docs look like but nothing forces agents to
*maintain* them. The redesign's bar is **self-enforcement**: run an agent in a loop and
watch whether the system converges (later agents do it the same way) or drifts (each agent
re-infers). The money result — a self-enforcing doc set eventually reaches a state where
the agent changes only code because the conventions are already written.

## The arc of the conversation, in order

### 1. Critique the skill → C−
Read the full skill (`SKILL.md` + all `references/`). Graded it C−: good essay,
incomplete system, not battle-tested. Over-specified in places that don't matter
(Guardian tables for a runtime that doesn't exist, provenance ceremony that vanishes on
finalize), under-specified in the places that make it self-enforcing.

The user corrected one frame: **"over-specified" was wrong.** Detailed documentation is
the whole point — agents can only infer otherwise. The real problem is the opposite:
under-specified where self-enforcement lives.

### 2. The three loops
Before redesigning any single doc, sketched the three loops the redesign has to serve:
- **Loop 1 — lifecycle:** "great idea but not now → where?", "what do I need to know right now?"
- **Loop 2 — scoping:** want vs exists, with the steady-state node ("docs already prescribe this; no edit needed") the skill never names.
- **Loop 3 — guardrails:** the two top failure patterns — minor-rule-explosion and NORTH_STAR bloat/prescription-creep/goals-as-validation.

### 3. NORTH_STAR redesign
Worked section by section. Key moves:
- **Opener:** Problem→Solution as default. "The Bet" renamed to "The Hypothesis," restricted to spikes (agents glom onto "The Bet" and misread it as a get-rich-quick framing).
- **Goals:** guiding light not validation. Delete the Requirements section. Real shape guidance with four example shapes (direction / problem-echo / quality-bar / user-outcome).
- **In/Out/Shape:** split it. In/Out conditional in NORTH_STAR; Shape/Caller demoted to architecture.
- **Anti-goals:** **inverted.** Default is zero. Earned only by observed mistaken-for cases. Identity-level only. This is where the minor-rule-explosion guard lives.
- **Pillars:** keep, conditional. The one place prescription-adjacent content is allowed, as a tradeoff ("accept cost X for benefit Y").
- **Deletions:** Requirements (goals-as-validation), goals-as-backlog.

### 4. The In/Out/Shape debate — abstract test, then empirical
The user was skeptical of In/Out/Shape as a universal section. First tested it abstractly
against five big pieces of software (Git, Postgres, VS Code, Linux, Python): holds for
Git/Postgres, thins for VS Code, degrades for Linux, **collapses for Python** (a language
has no Shape; the framework forces a prescription the spec refuses).

That established "conditional, not universal." Then ran a subagent to test it empirically
against 12 of the user's real projects. Result: **7 HOLDS / 1 THIN / 1 DEGRADES / 3
COLLAPSES = 58%**, below the skill's claimed ~70%. Confirmed: the framework fits products
with a specific caller and a contract-shaped Out; it breaks on platforms, umbrella repos,
scheduler-initiated pipelines, configurations, empty scaffolds.

### 5. The ColdSearch NORTH_STAR evaluation
The user supplied their ColdSearch `docs/NORTH_STAR.md` for grading. Per-section grades
(frontmatter A, Why This Exists A−, In/Out/Shape C+, What This Is Not B+, Goals B−,
Pillars B). Overall B−: strong identity pulled down by prescription leak in Shape, a
7-item goals backlog with heavy duplication, one anti-goal dissolving into draft-note
prose, an orphan LLM-endpoint line.

Then the goal-by-goal corrections — and the user pushed back on three of my cuts:
- **G3 (key/quota efficiency):** I said "requirement not goal"; user corrected — free-tier
  key-pool swapping is load-bearing *design intent*, not generic optimization. **Keep.**
- **G6 (preserve provider detail):** I said "duplicates Out + anti-goal"; user said the
  duplication is *intentional reinforcement* of the biggest failure mode. **Keep.**
- **G5 (log and audit):** agreed → move to the Audit First pillar.
- **G7 (stable surface):** agreed → move to architecture (it's a best practice, not a guiding light).

The refinement on reinforcement: **duplication for reinforcement should escalate in
specificity, not just repeat.** Three different angles on one idea (contract / failure
mode / standing decision) is reinforcement; the same idea near-verbatim four times is noise.

### 6. The architecture.md principle
User nailed the one sentence: **"architecture.md is a description of the approach we have
chosen to succeed at the goals, and why — NOT an inventory of the things in the project."**

Named the skill's self-contradiction: it warns against "code inventory creep" and then
mandates the inventory tables that cause it (System Shape table, Major Components table).
Agents follow the instruction, not the principle.

Reframe: thesis-first, not inventory-first. The Architecture Thesis (approach + why) IS
the document. Rule of thumb: **if a component has no "because" tying it to a goal or the
problem, it doesn't belong.** Shape/Caller exiled from NORTH_STAR land here — they're the
chosen approach, properly seated.

### 7. The skill + CLI exploration (EXPLORATORY — flagged not settled)
User raised offering the redesign as both a skill and a CLI, citing spec-kit (pattern,
not guardrails) and bmad-method (passionate commentary, real machinery underneath). Two
subagents researched both repos in parallel.

**Headline both agreed on:** neither spec-kit nor bmad actually solves self-enforcement.
Both build the architecture for it and stop short of wiring the gate.

- **Stealable from spec-kit:** CLI-scaffolds-skill inversion, `scripts:` front-matter
  prerequisite gate (the one real mechanical enforcement), constitution-as-input +
  detect-empty-template (kills Guardian ceremony), the hook rail wired to a validator,
  the `unrequested` finding type.
- **Stealable from bmad:** CSV routing-table schema, artifact-glob completion detection,
  status-YAML state, correct-course Minor/Moderate/Major triage, three-layer TOML
  override (the strongest candidate for the non-negotiable-lines problem).
- **Avoid from both:** spec-kit's SDD methodology and heavy template ceremony; bmad's
  persona-as-enforcement, checklist theater, the `required=true` illusion.

**User flag at the end:** "we might have tried to learn too much from bmad and spec-kit —
that's not settled, that's just something we were exploring." This is recorded as
EXPLORATORY in `session/06`, the canvas, and the README. The settled output stands on
its own without it.

### 8. Persist everything
Final move: move the whole session into the frozenSkillz repo as a dated scout snapshot,
make the canvas and the corrected ColdSearch example survive, open a PR, call a review
agent. (This is the step this overview is part of.)

## What is settled vs exploratory

**Settled (the load-bearing output):**
- NORTH_STAR = identity + the problem + 1–2 earned anti-goals. No Requirements, no Shape,
  no goal backlog. Opener default Problem→Solution; The Hypothesis spike-only.
- Goals = guiding light, not validation. Real shape guidance.
- In/Out conditional, gated on a Caller test (specific caller + contract-shaped Out).
- Anti-goals inverted: default zero, earned only, identity-level only. Minor-rule-explosion guard.
- architecture.md = the chosen approach + why, NOT an inventory. Shape/Caller land here.
- The corrected ColdSearch NORTH_STAR as the worked example / resume point.

**Exploratory (explored, NOT settled):**
- The skill+CLI split as distribution/enforcement architecture.
- All spec-kit and bmad-method steals.
- The TOML override layer as the non-negotiable-lines mechanism (strongest candidate, but
  the lighter "validator script + fixed-lines file, no full CLI" option is open).
- These informed the design; they are not decisions.

## Persistence checklist — what survived, what didn't, what was almost lost

| Item | Persisted? | Where |
|---|---|---|
| The self-enforcing principle + C− critique | yes | `session/01-the-bar.md` |
| The three loops | yes | `session/01-the-bar.md` |
| NORTH_STAR redesign (all sections) | yes | `session/02-north-star-redesign.md` |
| Goals shape guidance (4 examples) | yes | `session/02` + canvas |
| **Abstract big-software In/Out/Shape test (Git/Postgres/VS Code/Linux/Python)** | **added during this overview** — was missing, now in `session/02` | `session/02-north-star-redesign.md` |
| 12-project empirical stress test | yes | `session/04-in-out-shape-stress-test.md` |
| ColdSearch per-section grades | yes | `session/05-coldsearch-evaluation.md` |
| Goal-by-goal corrections + user's pushbacks | yes | `session/05` |
| The "reinforcement vs noise" refinement | yes | `session/05` |
| architecture.md principle + skill's self-contradiction | yes | `session/03-architecture-principle.md` |
| spec-kit research (full) | yes | `session/06` + subagent transcript |
| bmad research (full) | yes | `session/06` + subagent transcript |
| **The corrected ColdSearch NORTH_STAR (resume point)** | yes — and notably this was NOT written during the session, only evaluated; it was written for the first time during persistence | `examples/coldsearch-north-star.corrected.md` |
| The canvas artifact | yes | `canvases/north-star-shape.canvas.tsx` |
| EXPLORATORY framing on skill+CLI | yes | `session/06` header, canvas callout, README |
| Open questions for resuming | yes | `session/06` tail |
| This overview | yes | `OVERVIEW.md` (this file) |
| Orientation chatter (open PRs, PROGRESS.md question) | intentionally not persisted | — (not design content) |

**One gap caught and fixed during this overview:** the abstract big-software test that
*motivated* launching the 12-project empirical test was not in the persisted files — only
the empirical result was. That argument is load-bearing (it's the reasoning that
established "conditional, not universal" before there was data), so it's been added to
`session/02-north-star-redesign.md` under "The abstract test that motivated the
conditional rule."

## Where to resume

1. **`examples/coldsearch-north-star.corrected.md`** — the worked example. Read it
   against the original `d:\_projects\ColdSearch\docs\NORTH_STAR.md` to confirm the
   deletions-and-demotion edits read as an improvement.
2. **`session/02`** for the NORTH_STAR rules and **`session/03`** for the architecture
   principle — these are the settled design. The next concrete move is either:
   - rewrite the actual `~/.agents/skills/project-docs/references/north-star-guide.md`
     to this shape, or
   - pressure-test the architecture principle against a real architecture doc
     (ColdVault or coldaine-k8cluster) before committing it.
3. **`session/06`** for the exploratory skill+CLI material and its open questions — to
   revisit *only* when deciding whether to build enforcement machinery, not before.

## The PR

https://github.com/Coldaine/frozenSkillz/pull/32 — branch
`claude/project-docs-self-enforcing-design`.

## The review pass (after persistence)

A review subagent read all the writeups plus the original skill, the original ColdSearch
NORTH_STAR, and the real `architecture.md` files in ColdSearch and coldaine-k8cluster.
It found real defects. The most important:

1. **The "self-enforcing" overclaim (biggest).** The settled output (sessions 02–03 +
   the corrected example) is self-*persuading*, not self-enforcing. Content discipline
   produces a better doc, not a converging one. The only mechanism that would actually
   produce convergence is the exploratory `scripts:` gate + hook + validator in
   session/06. The adjective was smeared across both halves. **Fix applied:** README and
   this overview now state plainly that settled = self-persuading, enforcement = unbuilt
   exploratory.

2. **The architecture principle was never tested against a real architecture.md.** When
   run against ColdSearch's real `docs/architecture.md`, session/03's "no component
   without a because" rule would reject the Major Components index — the most useful
   navigation surface in the doc. When run against coldaine-k8cluster, it passes — but
   that's the platform/DEGRADES case, so the principle is implicitly platform-flavored
   and over-rejects on products. **Fix applied:** README records this as a known
   limitation; session/03 needs a carve-out for status-labeled orientation indexes before
   it's treated as final.

3. **The aspirations line was in the wrong section** in the corrected example (under
   In/Out, not Goals). **Fixed** in the example.

4. **G3 smuggled implementation into a goal** ("including alternating between keys to
   double free-tier usage" — a mechanism, not a compass bearing, violating session/02's
   own "Not implementation" rule). **Fixed:** the clause is removed; the key-pool
   tradeoff can become a real pillar if a genuine opposing position emerges.

5. **"Config Over Code" still failed the reasonable-opposite test** (no one would argue
   for hardcoded routing; it's a default dressed as a tradeoff). **Fixed:** removed from
   the example, with a note explaining why and how it could return as a real tradeoff.

6. **Goal renumbering broke downstream architecture.md cross-references.** The original
   correction renumbered G1–G7 to G1–G5, which silently invalidated four citations in
   ColdSearch's real `docs/architecture.md` (lines 13, 62, 63, 64). **Fixed:** goals keep
   their original numbers; G5 and G7 are marked "(moved)" rather than renumbered, so the
   architecture cross-references stay resolvable. This is itself a small instantiation of
   the self-enforcement problem — the doc edit created downstream drift that nothing
   forced to be reconciled.

The review's overall verdict was "needs fixes first" — the eight concrete fixes it
listed. The four applied here (1–6 above; some bundle multiple review items) are the
ones that could be fixed in the artifacts without re-opening design questions. The
remaining two (reconcile session/02 and session/04 on the platform case; resolve the
fixed-commentary-line leak between the exploratory scaffold and the settled example) are
recorded as open and are the natural first items when resuming.

## Where to resume

1. **`examples/coldsearch-north-star.corrected.md`** — the worked example, now with the
   review's concrete defects fixed (aspirations line moved to Goals, G3 implementation
   clause removed, Config Over Code removed, goal numbers kept stable so architecture
   cross-refs survive). Read against the original `d:\_projects\ColdSearch\docs\NORTH_STAR.md`.
2. **`session/02`** for the NORTH_STAR rules and **`session/03`** for the architecture
   principle — with the known limitation on session/03 noted in the README. The next
   concrete moves, in priority order:
   - revise session/03's "no component without a because" rule with a carve-out for
     status-labeled orientation indexes, then re-test against ColdSearch's real
     `docs/architecture.md`;
   - reconcile session/02 and session/04 on the platform case (add a third identity
     shape — "source-of-truth framing" — to session/02's Resulting shape);
   - resolve the fixed-commentary-line leak (the blockquote preambles in the corrected
     example are an unflagged instance of the exploratory hybrid scaffold);
   - then either rewrite the real `north-star-guide.md` to this shape, or decide
     whether to build the enforcement mechanism (session/06) that would move the
     output from self-persuading to actually self-enforcing.
3. **`session/06`** for the exploratory skill+CLI material — revisit only when deciding
   whether to build enforcement machinery. Until then, the settled output is
   self-persuading, and that's the honest framing.
