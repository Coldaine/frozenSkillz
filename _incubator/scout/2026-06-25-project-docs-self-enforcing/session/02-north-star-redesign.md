# 02 — NORTH_STAR redesign

The current skill's NORTH_STAR has six sections: Opener + In/Out/Shape + Goals +
Requirements + Anti-Goals + Pillars. The redesign keeps three, demotes one, deletes one,
and reworks the opener and goals.

## The Opener — reworked

### The bug the current skill has

The skill offers three opener shapes — Bet / Why-This-Exists / The-Goal — as peers.
Agents glom onto "The Bet" because it sounds dramatic, apply it to everything, and
misread it as a commercial get-rich-quick framing. But **The Bet is the least common
shape**, valid only for spike/experimental repos.

### The fix

**Default shape = Problem → Solution.** "I have problem Y. This is X to solve Y."

This does two jobs the current skill underplays:
1. **States the problem explicitly** — the "why it exists" that NORTH_STAR currently leaves
   implied. The problem is the most load-bearing piece of identity: it's what makes the
   side-quest gate answerable ("does this serve solving problem Y?"). If the problem is
   only implied, the gate gets answered by inference.
2. **Names the thing.** Two lines, both earning their place.

### The three opener shapes, renamed and ranked by actual frequency

| Shape | Rank | Form |
|---|---|---|
| Problem → Solution | default | "I have problem Y. This is X to solve Y." |
| Why This Exists | gap-closer | "No good X exists for Y. This fills that gap." Implies the problem less directly; use when the pain is an absence in the world, not personal. |
| The Hypothesis (was "The Bet") | spike-only | "We suspect X produces Y without Z. This tests that." Renamed to drop the commercial-wager baggage; restricted, not default. |

### MooseGoose example

"Patrick's technical life is scattered across home-app, refs, and half-finished tools,
none reachable in one place. MooseGoose Studio is a single-owner private console that
consolidates it behind one gate."

## Goals — guiding light, not validation

### The principle

Goals are a compass bearing, not a destination. They shape every decision an agent
makes; they are never a test suite. **The skill's "Requirements" section (how you'll
recognize progress) is goals-as-validation and gets deleted.**

### What goals are NOT

- Not requirements. No "how you'll recognize progress." That's validation.
- Not a backlog. A goal that needs more than a sentence is a plan; plans live in
  `docs/plans/`.
- Not implementation. "Use Postgres" is architecture, not a goal.
- Not a checklist item. If you can tick it off, it was a task, not a guiding light.

### Goal shapes — examples of what a one-line goal can be

| Shape | Example |
|---|---|
| Direction | "Make MooseGoose the one place Patrick's technical life lives." Compass bearing, never done. Most common. |
| Problem-echo | "Consolidate scattered tools behind one owner gate." Restates the opener's problem as the standing thing to solve. |
| Quality-bar | "Every owner-only route is reachable, or has a documented reason it's hidden." A bar to clear on every piece of work, ongoing by design. |
| User-outcome | "Patrick can run his day from one authenticated surface." Names the caller and what they get. |

### Refusal goals belong in Anti-Goals

"Not X, not Y" is a goal shape, but it lives in the Anti-Goals section, not here — and
only when earned. Don't duplicate a refusal as a goal and an anti-goal.

### How many goals?

Not "one or two" as a rigid rule. **The real test is: does each goal shape a real
decision an agent would otherwise get wrong?** Five can be fine if each earns its place
and they don't duplicate without intent. Seven is usually a backlog wearing a goal suit.
The distinction is sharper than count.

## In / Out / Shape — conditional, demote Shape

The skill bundles four one-liners. Split them.

### In / Out — keep in NORTH_STAR, conditional

- **What:** Scope filters. "In: owner's work + tools. Out: a thin public portfolio, nothing else."
- **Conditional rule:** Include In/Out ONLY when the project has a clear caller and a
  clear delivered Out. For platforms, infra, languages, or abstract-caller systems,
  In/Out degrade into tautology — omit rather than force filler.
- **Empirical backing:** the 12-project stress test (see `04-in-out-shape-stress-test.md`)
  produced 7 HOLDS / 1 THIN / 1 DEGRADES / 3 COLLAPSES = 58% genuine holds, below the
  skill's claimed ~70%. The framework fits products with a specific caller and a
  contract-shaped Out; it breaks on platforms, umbrella repos, scheduler-initiated
  pipelines, configurations, and empty scaffolds.

### Shape / Caller — demote to architecture.md

- **What:** Delivery mechanism. "Next.js pod on K8s behind Cloudflare Tunnel."
- **Why demote:** Prescription masquerading as identity. If delivery changes, NORTH_STAR
  changes — but NORTH_STAR should be the slowest-moving doc. Invites the agent to infer
  implementation ("K8s → reach for Helm"), the prescription-creep failure.

### The split rule

In/Out answer "does this belong here?" (scope, permissive). Shape/Caller answer "how is
it delivered?" (prescription, downstream). **Identity holds scope; architecture holds
approach + delivery.** If you can't fill In/Out concretely, that signals the thing isn't
a product with a caller — it's a platform/spec/layer needing a different identity shape.

### In/Out/Shape as a full four-liner is a plan/epic-scoping tool

Not a universal identity section. When scoping an epic, being unable to fill out
In/Out/Shape concretely is a signal the epic isn't well-defined. That's where the
four-liner earns its keep.

## Anti-Goals — inverted: default is zero

### The bug the current skill has

The skill says "at least one from day one, more accrete over time." That rule invites
agents to **fabricate anti-goals out of thin air** to feel thorough — "must not become a
framework," "must not depend on cloud services" — that the owner never chose and that
aren't real mistaken-for cases.

### The inverted rule

- **Default is ZERO anti-goals.** Absence is the healthy state, not a gap to fill.
- **An anti-goal is earned, not invented.** Write one only when you can point to a
  specific, observed, recurring case of the project being mistaken for X. No evidence,
  no anti-goal.
- **The guard is against fabrication, not against absence.** If you cannot point to a
  real time this project was actually mistaken for X, do not write an anti-goal about X.

### Identity-level only

"Not a marketing site. Not a multi-user SaaS." Good — identity drift. "Must not use
Redis" is a prescription hiding in an anti-goal — it belongs in conventions, where it
can change without touching identity.

### The minor-rule-explosion guard (the rule the current skill is missing)

Fabricated anti-goals are the **primary way minor rules become major ones** — they get
written into the highest-authority doc on a hunch. The guard: an anti-goal must be
identity-level ("not a SaaS"), never implementation-level ("must not use Redis").

## Pillars — keep, conditional

The current skill's rule is correct: "only when the owner has hit a real tradeoff, stated
as 'accept cost X for benefit Y,' not a directive. Zero pillars is better than three
plausible-sounding ones the owner didn't choose."

This is the **one place prescription-adjacent content is allowed**, and only as a
tradeoff. It survives the self-enforcing test: a future agent reads "we accept slower
builds for reproducibility" and makes consistent downstream choices.

## What gets deleted

- **Requirements (Goals-as-validation).** Goals are a guiding light — read every
  session, shape decisions, never checked off. Requirements turns NORTH_STAR into a
  test suite.
- **Goals-as-backlog.** Goals are the opener's shadow — at most one or two guiding-light
  statements. A goal needing more than a sentence is a plan; plans live in `docs/plans/`.

## Resulting shape

1. **Opener** — one or two lines, Problem→Solution default. States the problem, names the thing.
2. **Goals** — one or two (sometimes a few) guiding-light lines. Direction / problem-echo / quality-bar / user-outcome. Never validation.
3. **In / Out** — conditional, only if caller + Out are concrete. Omit rather than force filler.
4. **Anti-Goals** — default zero. Earned only by observed mistaken-for cases. Identity-level only.
5. **Pillars** — only if a real tradeoff has been made.

No Requirements. No Shape. No Caller. No goal backlog. No fabricated anti-goals. Small
enough to be read by every agent every session — enforced by content discipline, not a
line count.

## The template / non-negotiable-lines problem (exploratory)

The current skill is anti-template ("interview, don't fill in blanks"). That avoids
fill-in slop but means non-negotiable commentary lines like "these goals are
aspirations" don't survive agent rewrites — nothing forces re-emission.

Hybrid resolution (sketched, not settled):
- A scaffold with **fixed commentary lines** the agent cannot remove + **fill regions**
  for owner-derived content.
- The fixed lines are the self-enforcing part. The fill regions preserve the no-template
  insight (interview, don't fabricate).
- See `06-skill-cli-exploration.md` for the stronger mechanism (structured override
  layer) — but treat that as research input, not a settled decision.
