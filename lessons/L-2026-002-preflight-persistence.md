---
id: L-2026-002
title: Preflight the persistence path before the run
status: hypothesis
recorded: 2026-08-04
---

## Trigger

Any run whose results must be persisted to graph or relational stores.

## Lesson

Validate the entire write path *before* executing the experiment: graph edge
and node vocabulary from the actual importer/schema (not invented — the origin
episode generated `RUN_EXECUTED_WORKLOAD` where the schema defines
`RUN_ON_WORKLOAD`), Python dependencies through the repo's own environment
(repo `uv` env, not system Python — which lacked `psycopg`), and store
credentials/endpoints with a dry run. A GPU run followed by interactive
persistence debugging inverts the cost order: the cheap checks should gate the
expensive one, and a run whose record cannot be written did not happen.

## Evidence

- [direct] Graph dry-run failed on the invented edge type
  `RUN_EXECUTED_WORKLOAD`; schema requires `RUN_ON_WORKLOAD` (origin session,
  2026-08-04).
- [direct] First live importer invocation used system Python without
  `psycopg`; succeeded only after switching to the repository's uv dependency
  path.
- [direct] LocalLargeLanguageModels `prompts/investigator.md` step 6 already
  states the same-session persistence rule; the failure was not preflighting
  the mechanics that rule depends on.

## Guard

None yet. Candidate: a pre-run checklist item that runs the importer in
dry-run mode against the planned record before the experiment starts.

## Recurrences

- 2026-08-04 — DiffusionGemma native Aider run persistence (origin episode).

## Superseded by

—
