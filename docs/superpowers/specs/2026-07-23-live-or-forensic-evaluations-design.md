# Live or Forensic Evaluations

## Purpose

External-skill intake must accept two valid evidence modes instead of treating synthetic or
sandboxed execution as the only evaluation path:

- **Live evaluation** exercises a candidate or adaptation and preserves the prompt, inputs,
  outputs, environment, and scorer notes.
- **Forensic evaluation** reconstructs behavior from evidence produced by real agents and users,
  including transcripts, issue reproductions, code history, maintainer confirmations, tests, and
  release notes.

The mode must be named explicitly. Neither mode may be presented as the other.

## Evidence Contract

Every material finding records its source, affected version and harness when known, status
(`current`, `fixed`, `historical`, `unresolved`, or `unclear`), and confidence. Forensic evaluation ranks
direct transcripts and reproducible artifacts above corroborated issue reports, and ranks isolated
anecdotes below both. Absence of a live run does not invalidate a well-supported forensic finding.

Claims that a candidate improves outcomes still require comparative live evidence. Forensic
evidence can establish intent, actual behavior, regressions, failure modes, maintenance response,
and current unresolved risk without manufacturing a benchmark.

## Repository Shape

The active `external-skill-intake` skill will route both modes through one evaluation protocol and
separate templates. Existing `evals/cases/` and `evals/runs/` paths remain valid for compatibility;
forensic findings may be stored under `evals/forensic/`.

The initial consumer is a pinned Superpowers v6.1.1 scout dossier containing provenance,
repository and skill inventory, a per-skill forensic analysis, and a decision log. The first
completed review is `brainstorming`; later skills can be appended one at a time.

## Verification

A repository test will assert that the active skill and workflow expose both modes and that the
forensic template exists. Existing manifest validation and unit tests remain green. The scout
snapshot will be checked against the recorded upstream commit and tag.
