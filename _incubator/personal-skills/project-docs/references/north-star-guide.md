# How to Write a North Star

A North Star is the most authoritative document in a project. It defines what the project is, where it is going, and what it refuses to be. Agents and contributors read it first and weigh everything else against it. The Guardian enforces it.

Because of that authority, every word matters. A wrong sentence in a North Star will be enforced as if the owner chose it. This guide exists to prevent that.

---

## What Goes In, What's Optional, What Accretes

A North Star is not a form to fill out. Not every section belongs in every project, and not every section belongs on day one.

| Section | When to include | When to skip or defer |
|---|---|---|
| Opener | Always. No exceptions. | Never skip. |
| In/Out/Shape | When the project has clear boundaries: something goes in, something comes out, there is a delivery mechanism. | Research projects, exploratory tools, creative works, or any project where the architectural shape has not been earned yet. A premature In/Out/Shape locks in design decisions that agents will treat as requirements. Better to omit than to guess. |
| Goals | Always. No exceptions. | Never skip. |
| Requirements | When you know how you will recognize progress toward a goal. | A new project may have goals with no requirements yet. Empty requirements under a goal is a valid signal: "I know where I'm going but haven't decided how I'll know I'm getting there." Flag for revisit; do not leave empty for months. |
| Anti-Goals | Include at least one from day one. Every project has at least one thing it will be mistaken for. More will accrete as agents and contributors misunderstand the project. | Do not force a long list upfront. One or two real ones are worth more than five hypothetical ones. |
| Pillars | Only when the owner has hit a real tradeoff and made a real choice. | If the owner has no strong tradeoff preferences yet, the section should not exist. Zero pillars is better than three plausible-sounding ones the owner didn't actually choose. |

**Minimum viable North Star: Opener + Goals + at least one Anti-Goal.**

Everything else accretes as the project matures.

---

## The Opener

Pick exactly one. Delete the other two.

**"The Bet"** — The project rests on an unproven assumption. If the bet is wrong, the project was a mistake. Use this when you are building something speculative.

**"Why This Exists"** — The problem is known and understood. No hypothesis; just a gap to close. Use this when the situation is clear and the goal is to fix it.

**"The Goal"** — The mission is self-evidently worth pursuing. Rare. Most projects are bets or gap-closers, not missions.

### Rules

- One sentence. If you cannot say it in one sentence, you do not know your bet yet.
- No hedging. "We believe that maybe..." is not an opener; it is a committee trying not to commit.
- The opener type sets the tone for the entire document. A "Bet" North Star expects to be invalidated. A "Why This Exists" North Star expects to be completed. A "The Goal" North Star expects to be pursued indefinitely. The guardian reasons differently against each.

---

## In / Out / Shape

Four one-liners:

- **In:** What goes into the system.
- **Out:** What comes out.
- **Shape:** How it is delivered.
- **Caller:** Who or what initiates interaction.

### Rules

- An agent that reads only these four lines should be able to answer "does feature X belong here?" about 70% of the time. That is the bar.
- Prose invites softening. "The system primarily ingests X, though it may also accept..." is how scope creep starts. Constrained one-liners force blunt answers.
- If you cannot fill one out, leave it blank and mark it open. A blank line is better than a vague one. A vague line is better than a fabricated one.
- If filling out this section feels forced or produces misleading constraints, omit the entire section. It is better to have no In/Out/Shape than a wrong one, because agents will enforce what you write here.

### The Caller Trap

"Caller" is the most commonly fabricated field. An agent filling out this template will confidently write something like "The project owner, directly. No API consumers, no integrations, no plugins" because it sounds like a reasonable scope limiter. If the owner never said that, the agent just created a constraint that will be enforced as if the owner chose it. Reviewers will praise it because it sounds crisp and decisive.

If you do not know who or what calls this system yet, write "Open" and move on. Do not let an agent decide for you.

---

## Goals

Goals describe where you are going. They do not describe how you measure arrival. That is what requirements are for.

### Rules

- **Directional, not testable.** "Surface ideas the owner didn't know they had" is a goal. "Cluster 90% of entries within 30 seconds" is a requirement. Goals survive pivots; if you change your algorithm, the goal is still the goal. If your goal WAS your test, changing the test destabilizes the entire document.
- **Numbered: G1, G2, G3.** So agents and humans can cite them precisely. "This PR conflicts with G2" is actionable. "This PR conflicts with the goal about evolution" forces the reader to go find which goal you mean.
- **Three to five.** Fewer than three usually means you have not separated concerns. More than five usually means you have not prioritized. If you have eight goals, some of them are requirements wearing a goal's clothing. Push them down.
- **Start with a verb that implies direction, not completion.** "Surface," "show," "separate," "enable," "reduce." Avoid verbs that imply a finish line: "implement," "build," "deliver," "complete." A goal you can finish is a task, not a goal.

---

## Requirements

Requirements live under goals, not in a separate section. A requirement without a parent goal is an orphan: it may be valid, but no one can reason about why it exists.

### Rules

- **Testable: yes or no.** Can someone look at the system and say whether this requirement is satisfied? If the answer requires judgment or interpretation, it is still a goal. Push it up or sharpen it.
- **Numbered with parent: G1-R1, G1-R2, G2-R1.** The prefix ties the requirement to its goal mechanically. An agent does not need to read surrounding prose to know which goal a requirement serves. Orphaned requirements (any R without a corresponding G) are suspect.
- **Requirements are the guardian's actual reasoning anchor.** Goals give direction. Anti-goals define identity. Pillars inform judgment. But requirements are what the guardian checks PRs against. A PR that moves away from a requirement gets cited with the specific requirement number. Everything else in the document gives that citation context.
- **No algorithmic prescription unless it is genuinely part of the goal.** "Semantic clustering produces named idea groups" is a valid requirement. "Uses HDBSCAN for clustering" is an implementation choice that does not belong here unless the owner has a specific reason to mandate it.
- **Beware underspecified verbs.** Words like "learns," "adapts," "understands," and "intelligently" are dangerous in requirements. An agent will interpret them as requiring sophisticated mechanisms (training loops, fine-tuning, model updates) when the owner may mean something simple (persisted labels, a lookup table, a bias term). Say what you mean mechanically.

---

## Anti-Goals

Anti-goals define identity through exclusion. They answer: "What will agents and contributors assume we are building, because it looks similar, that we are NOT building?"

### How Anti-Goals Differ from Anti-Patterns

Anti-patterns are retrospective: "we tried X, it failed." They require experience.

Anti-goals are definitional: "you will assume we are building X because it looks like X; we are not building X." They require self-awareness about what the project resembles from the outside.

A project with no anti-patterns is young. A project with no anti-goals has not defined itself.

### Rules

- **At least one from day one.** Every project looks like something it is not. If you cannot name one thing your project will be mistaken for, you have not thought about it enough.
- **Name the attractor.** "This is not a note-taking app" is not just a boundary; it names the specific thing agents will drift toward. LLMs are especially susceptible to attractor drift: if your project description contains "text," "corpus," and "user," every LLM will try to add a text editor.
- **Ban the intent, not the mechanism.** "No text input fields" bans search boxes and date pickers along with editors. "The user does not compose ideas into this system" bans the intent while leaving the mechanism open. An agent enforcing the first version will flag legitimate UI. An agent enforcing the second version will flag actual scope violations.
- **More will accrete.** If you have corrected an agent or contributor more than once on the same misunderstanding, that misunderstanding is an anti-goal. Write it down. The list grows through lived experience.
- **The guardian treats anti-goal violations like requirement violations.** A PR that crosses an anti-goal is not a judgment call; it is a boundary violation. The guardian soft-blocks with a citation to the specific anti-goal.

---

## Pillars

Pillars are how the project prefers to make tradeoff decisions. Each pillar has a name, a statement, and a "Why" that names the cost.

### Rules

- **Every pillar names its tradeoff.** A pillar without a cost is a platitude. "We value quality" is not a pillar. "We accept slower velocity in exchange for never shipping demo-only features" is a pillar, because it names what you are giving up. If there is no cost, it is not a tradeoff, and if it is not a tradeoff, it is not a pillar.
- **The "reasonable opposite" test.** Would someone on this project reasonably argue for the opposite? If yes, it is a real pillar. "Corpus-first vs. synthetic-first" is a real tradeoff. "Don't ship broken software" is not a tradeoff. If no one would disagree, it is not a pillar.
- **Pillars are defaults, not mandates.** The guardian's job with pillars is to notice when a PR departs from one and ask whether the departure is intentional and justified. Not to block it. A PR that violates a pillar is not wrong; it is a signal that a tradeoff is being made. The guardian makes sure that tradeoff is conscious, not accidental.
- **Every pillar must come from the owner's mouth.** This is the section most likely to be contaminated by agent assumptions. An agent filling out this template will invent pillars that sound reasonable but were never chosen by the owner. "Local and self-contained" sounds like a reasonable pillar for any desktop app. But if the owner never said it, the agent just created a constraint that will be enforced as if the owner chose it. Two real pillars from the interview are worth more than four plausible ones from the agent.
- **Zero pillars is a valid state.** If the owner has not hit a real tradeoff yet, this section should not exist. Do not fill it in to make the document look complete. The section appears when the owner makes a real choice about what to sacrifice for what. Not before.
- **Temporal scope matters.** If a pillar applies at runtime but not at build-time, say so in the pillar statement, not just in the rationale. An agent reading the statement will enforce it everywhere; an agent reading the rationale might interpret it differently. The statement and the rationale must agree on scope.

---

## What the Guardian Does with Each Section

| Section | Guardian asks | On violation |
|---|---|---|
| Opener | "Does this PR serve the project's reason for existing?" | Rarely invoked directly; provides context for all other checks. |
| In/Out/Shape | "Does this PR introduce something outside the declared boundaries?" | Soft-block with citation. |
| Goals | "Does this PR move toward or away from a goal?" | Provides direction; the guardian reasons about goals but cites requirements. |
| Requirements | "Does this PR satisfy, advance, or contradict a specific requirement?" | Soft-block with requirement number citation. |
| Anti-Goals | "Does this PR cross a declared identity boundary?" | Soft-block with anti-goal citation. Treated same as requirement violation. |
| Pillars | "Does this PR depart from a stated preference? Is the departure acknowledged?" | Surface the tension. Ask the question. Never block. |

---

## Common Failure Modes

**Agent fabrication.** An agent filling out this template will confidently invent constraints the owner never chose. The constraint will sound reasonable. Reviewers will praise it. The guardian will enforce it. The owner will not notice until the constraint blocks something they wanted. Every field in this document should be traceable to something the owner said, not something the agent inferred.

**Pillar contamination.** The most common fabrication target. Agents default to "reasonable-sounding" architectural preferences (local-first, privacy-focused, minimal dependencies) that may or may not reflect the owner's actual values. The interview exists to prevent this.

**Underspecified verbs in requirements.** "Learns," "adapts," "understands," "intelligently handles." Each of these will be interpreted as requiring sophisticated mechanisms. Say what you mean mechanically.

**Anti-goals that ban mechanisms instead of intent.** "No text input fields" vs. "the user does not compose ideas into this system." The first bans legitimate UI. The second bans scope violations.

**Pillars without costs.** If the "Why" does not name what you are sacrificing, the pillar is a platitude and will not help the guardian reason about tradeoffs.

**Premature In/Out/Shape.** Filling this section in before the project's boundaries are earned locks in architectural choices that agents will enforce as requirements.

**Empty sections left for months.** An empty requirements section is fine on day one. An empty requirements section three months in means the owner has not revisited the document. The guardian should flag staleness using the "Last Confirmed" metadata field.
