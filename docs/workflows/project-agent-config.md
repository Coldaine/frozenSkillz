# Project Agent Configuration (v1 convention)

> **Status:** proposed workflow (pairs with [REFINED-V1](../platform/REFINED-V1.md)).
> Does not replace [skill-authority-and-frozen-sync.md](skill-authority-and-frozen-sync.md).

## Purpose

Persist agent configuration **in each GitHub project** so a clone is usable without a
central renderer rewriting the tree.

## Rules

1. **Commit native files** the clients for this repo actually load
   (`AGENTS.md`, `.cursor/`, `.claude/`, `.codex/`, client MCP JSON, project-local
   skills under the paths those clients discover).
2. **Shared reviewed skills** come from frozenSkillz via
   `scripts/sync_frozen_skills.py` into `~/.agents/skills` — not by inventing a
   parallel project manifest that re-lists the whole catalog.
3. **Project-specific skills** live in the project (or as an explicit fork/vendor
   copy the project owns). Do not silently overwrite them from frozenSkillz.
4. **Rules stay project-owned.** Do not transpile or continually overwrite them from
   a central pack.
5. **Secrets stay out of git.** Reference Doppler or environment names only.
6. **No required `.agents/config.yaml` in v1.** If a project later wants a thin
   inventory file for humans, it must not become a second source of truth that
   agents reconcile against native files.

## Relationship to frozenSkillz sync

| Need | Mechanism |
|---|---|
| Same reviewed skill on every machine | `python scripts/sync_frozen_skills.py --check` / `--apply` after pull |
| This repo’s operating contract | Commit native files in **this** repo |
| Experimental personal skill | Author under `~/.agents/skills`; mirror to `_incubator/` when tracked |

## Done when

- A new clone of the project has the committed agent files agents need for that repo.
- Shared skills on the machine match the frozenSkillz allowlist (`--check` exits 0).
- No meta-manifest is required to explain what the native files already say.
