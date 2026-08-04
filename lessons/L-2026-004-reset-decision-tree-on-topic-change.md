---
id: L-2026-004
title: Reset the decision tree when the session topic changes
status: hypothesis
recorded: 2026-08-04
---

## Trigger

Session scope shifts across models, runtimes, or investigation targets
mid-conversation.

## Lesson

When the topic moves (in the origin episode: Nanbeige serving → KV-cache math
→ Qwen comparisons → DiffusionGemma), explicitly reset the decision tree:
state the new question, re-derive *its* decisive blocker, and drop assumptions
carried forward from the previous topic. Stale context from an earlier
sub-investigation silently shapes the next one — generic Gemma4 assumptions
survived into DiffusionGemma planning, and KV/context questions were revisited
repeatedly before being anchored to the exact artifact and runtime. A topic
change is a cheap moment to say "what is the question now, and what single
check decides it?"

## Evidence

- [inference] Origin session timeline: scope expanded across four topics
  without a decision-tree reset; repeated re-explanation of KV/context
  reasoning and transfer of Gemma4 structured-output assumptions to
  DiffusionGemma followed.
- [direct] Consequence measured in L-2026-001: carried-forward assumptions
  were exactly what the unchecked `is_diffusion` guard invalidated.

## Guard

None yet. Candidate: on a detected topic change, the agent restates the
current question and its decisive check in one or two lines before proceeding.

## Recurrences

- 2026-08-03/04 — Nanbeige → DiffusionGemma session (origin episode).

## Superseded by

—
