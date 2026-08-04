---
id: L-2026-003
title: Harnesses must retain HTTP error bodies
status: hypothesis
recorded: 2026-08-04
---

## Trigger

Writing or modifying a test harness, runner, or HTTP helper that talks to a
serving endpoint.

## Lesson

On any non-2xx response, retain the full response body in the run record, not
just the status line. "HTTP 400: Bad Request" is the least useful form of the
evidence; the server's error body was what actually explained the rejection
(structured outputs unsupported for diffusion models) and had to be recovered
by patching the runner after the fact. The failure body is often the entire
payload of a negative result — treat capturing it as a first-class harness
requirement, not an afterthought.

## Evidence

- [direct] LocalLargeLanguageModels `investigations/20260803_diffusiongemma_native_aider_examiner_critique.md:350-353`
  — documents the error-body loss and the post-hoc runner patch.
- [direct] Origin session: first runner recorded only "HTTP 400: Bad Request";
  a hardening pass added a test ensuring HTTP error bodies are retained
  (suite 20/20 after the fix).

## Guard

None yet. Candidate: a shared `post_json()` helper that raises/returns with
the body attached, plus a unit test asserting error bodies survive — required
for any new runner in the serving tooling.

## Recurrences

- 2026-08-04 — DiffusionGemma native Aider canary runner (origin episode).

## Superseded by

—
