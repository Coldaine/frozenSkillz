---
title: project-docs North Star
date: 2026-05-19
author: Patrick MacLyman
status: living
last_confirmed: 2026-05-19
---

# project-docs North Star

## The Bet

Agents drift fastest when no document tells them what the project refuses to be, and the cheapest defense against that drift is a small set of authority documents authored from the owner's words and routed through a decision tree the agent walks before working.

## In / Out / Shape

- **In:** an agent task ("create / review / reconcile / migrate the project authority documents")
- **Out:** a draft, an edit plan, a review report, an authority-flow summary, or a migration recommendation
- **Shape:** a Claude skill (`SKILL.md` + `references/` + `examples/`) loaded by an agent harness at task time
- **Caller:** an agent harness (Claude Code, Codex CLI, Cursor, OpenCode) invoking the skill on behalf of a project owner

## Goals

- **G1.** Surface the documentation pattern's authority hierarchy so agents read upstream before downstream.
- **G2.** Reduce the cost of authoring authority documents by routing the agent through an interview-driven workflow, not a template.
- **G3.** Separate authoring-time concerns (drafting, reviewing, reconciling) from runtime concerns (PR-time enforcement, drift detection), which belong to a future Guardian.
- **G4.** Preserve owner authorship: every claim in every authority document is traceable to something the owner said, not something the skill inferred.

### Requirements

- **G1-R1.** The skill's router exposes the four primary documents and the four overflow destinations as distinct task targets.
- **G1-R2.** The skill produces an authority-flow finding when a downstream doc contradicts an upstream doc.
- **G2-R1.** The skill's generation workflow opens with open-ended interview questions, not a template.
- **G2-R2.** The skill records provenance tags (`[OWNER]`, `[INFERRED]`, `[OPEN]`) on every draft before review.
- **G3-R1.** The skill uses authoring vocabulary (finding, suggested edit) and not Guardian vocabulary (violation, blocker, severity).
- **G4-R1.** The skill refuses to silently rewrite neighboring docs as a side effect of working on one doc.

## Anti-Goals

- **AG1.** This is not a markdown linter. It does not enforce frontmatter syntax, heading hierarchy, or formatting rules. Those are linter concerns.
- **AG2.** This is not the Guardian runtime. It does not block PRs, run in CI, or assign severities. PR-time enforcement is a separate, downstream system.
- **AG3.** This is not a templating engine. The agent does not fill in fields; the agent interviews the owner and writes from the owner's words.
- **AG4.** This is not a documentation completeness checker. A project with only AGENTS.md is a valid project. The minimum viable stack is small.

## Pillars

**Owner authorship over agent fabrication.** We accept slower authoring in exchange for documents that reflect what the owner actually said. The reasonable opposite is "let the agent fill in plausible defaults to save time," which faster but produces constraints the owner never chose.

**Authority-flow over local correctness.** We accept that a doc that is locally well-formed but contradicts an upstream doc is still a finding. The reasonable opposite is "if the doc looks fine on its own, it is fine," which is faster to review but lets drift accrete between docs.

**Authoring-time clarity over runtime enforcement.** We accept that the skill cannot block bad changes; it can only surface findings. The reasonable opposite is "build enforcement into the skill," which would catch more problems but conflate authoring concerns with PR-time concerns and make the skill brittle as the Guardian evolves separately.

## Open Questions

- Should the skill bootstrap the overflow subdirectories (`docs/decisions/`, `docs/components/`, etc.) when it bootstraps the primary docs, or only when it detects a need for them?
- How does the skill detect "this content should be moved out of doc X into overflow destination Y" without rewriting doc X?
- When the skill is invoked on a repo that already has CLAUDE.md, .cursorrules, and copilot-instructions.md, what is the migration workflow's order of operations?
