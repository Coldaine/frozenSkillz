---
id: L-2026-001
title: Execute the decisive code path offline before GPU or review
status: hypothesis
recorded: 2026-08-04
---

## Trigger

Planning any GPU run, feasibility test, or Examiner round where one binary
question decides whether the work is viable at all.

## Lesson

Identify the single decisive question first ("does this exact runtime build
permit feature X for this model class?"), then execute that code path offline
— against the pinned source or a local validator with the real config — before
scheduling GPU time, an Examiner round, or integration design. If the decisive
check fails, stop; everything downstream was planning for a world that does
not exist. Three corollaries measured in the origin episode: (1) registration
is not acceptance — a feature present in docs and accepted by the request
schema was still rejected deep in the validator; (2) generic model-family
documentation does not transfer to a variant — Gemma4 structured-output
support said nothing about DiffusionGemma, which the runtime explicitly
rejects; (3) a passing test suite can give false confidence when no test
exercises the real decisive path — 23 tests passed while none ran the actual
validator with the effective ModelConfig.

## Evidence

- [direct] LocalLargeLanguageModels `investigations/20260803_diffusiongemma_native_aider_prerun_plan.md:40-44`
  — the plan believed the capability check was done; it had tested request
  schema and XGrammar compilation, not `SamplingParams._validate_structured_outputs()`.
- [direct] LocalLargeLanguageModels `investigations/20260803_diffusiongemma_native_aider_examiner_critique.md:288-296,341-346`
  — Examiner authorized GPU on insufficient offline gates, then admitted
  post-hoc the `is_diffusion` guard was only checked after the HTTP 400.
- [direct] Run receipt: `/srv/ai-models/runtime-state/model-missions/diffusiongemma-native-aider-20260803/diffusiongemma-native-aider-20260804T000057Z/import_receipt.json`
  — GPU server loaded for ~3 minutes; first structured request returned 400;
  Aider never ran.
- [inference] Most of the 38-minute session cost was Aider-specific planning,
  Examiner iteration, and rework that the early offline check would have
  deleted.

## Guard

None yet. Candidate: a pre-run plan must name its single decisive question and
show the offline execution of that check (or state why none exists) before the
Examiner reviews it.

## Recurrences

- 2026-08-03/04 — DiffusionGemma native Aider feasibility run (origin episode).

## Superseded by

—
