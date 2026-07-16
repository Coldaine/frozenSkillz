---
title: project-docs North Star
date: 2026-05-19
author: Patrick MacLyman
status: living
last_confirmed: 2026-07-16
---

# project-docs North Star

## Opener

Agents drift fastest when no document tells them what a project refuses to be, and the ones that do exist are authored by the agent rather than the owner. `project-docs` is a skill that creates, reviews, reconciles, and migrates a project's authority documents (NORTH_STAR, architecture, AGENTS) from the owner's own words, so the next agent reads the same intent the last one wrote.

## In / Out

- **In:** an agent task — create / review / reconcile / migrate a project's authority documents.
- **Out:** a draft, an edit plan, a review report, an authority-flow summary, or a migration recommendation.

*(Delivery Shape and Caller — a Claude / Codex / Cursor skill loaded by an agent harness at task time — live in `architecture.md`, not here.)*

## Goals

- **G1.** Surface the documentation pattern's authority hierarchy so agents read upstream before downstream.
- **G2.** Keep authoring interview-driven, not template-driven, so documents carry the owner's words rather than plausible defaults.
- **G3.** Separate authoring-time concerns (drafting, reviewing, reconciling) from runtime enforcement, which belongs to a future Guardian.
- **G4.** Preserve owner authorship: every claim traces to something the owner said, not something the skill inferred.

## Anti-Goals

*(Each earned — a real, recurring "mistaken-for" case for this skill.)*

- **AG1.** Not a markdown linter. It does not enforce frontmatter syntax, heading hierarchy, or formatting.
- **AG2.** Not the Guardian runtime. It does not block PRs, run in CI, or assign severities.
- **AG3.** Not a templating engine. The agent interviews the owner and writes from their words; it does not fill in blank fields.
- **AG4.** Not a documentation completeness checker. A project with only AGENTS.md is valid; the minimum stack is small.

## Pillars

**Owner authorship over agent fabrication.** We accept slower authoring in exchange for documents that reflect what the owner actually said. The reasonable opposite — let the agent fill in plausible defaults to save time — is faster but produces constraints the owner never chose.

**Authority-flow over local correctness.** We accept that a locally well-formed doc that contradicts an upstream doc is still a finding. The reasonable opposite — "if it looks fine on its own, it is fine" — is faster to review but lets drift accrete between docs.

**Authoring-time clarity over runtime enforcement.** We accept that the skill can only surface findings, not block changes. The reasonable opposite — build enforcement into the skill — would catch more but conflate authoring with PR-time concerns and make the skill brittle as the Guardian evolves separately.
