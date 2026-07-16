# Current Work and Document Lifecycle

How this skill treats **current work**, **finished work**, and **temporary docs**.

This replaces the old PROGRESS + `docs/history/` pattern.

---

## Load-Bearing Principle

> Current work lives in Issues and/or `docs/plans/`. Lasting truth is promoted into living homes. Temporary docs are deleted. Git is the archive.

Do not create `PROGRESS.md`, `HANDOFF.md`, `STATUS.md`, or a rolling `docs/history/` tree to park finished notes.

---

## Current Work

Pick one or both (project chooses; AGENTS routes there):

| Home | Best for |
|---|---|
| GitHub Issues (or Linear, etc.) | Blockers, decisions needed, small tasks, discussion |
| `docs/plans/` | Multi-step executable plans with a Status block |

Rules:

- Plans are **active** documents. When the plan is done, promote any lasting facts, then **delete the plan file** (or close the issue). Do not roll it into history prose.
- Do not invent a fourth primary authority doc for handoff.
- If the repo already uses Issues well, do not force `docs/plans/`.

---

## Promote, Then Delete

When temporary content finishes (plan complete, scratch notes obsolete, session dump done):

1. **Promote** anything that must survive into its living home:
   - intent / goals / anti-goals → `NORTH_STAR.md`
   - technical shape / invariants → `architecture.md`
   - durable decision + why → `docs/decisions/`
   - deep subsystem truth → `docs/components/` or topic living docs
   - repeatable procedure → `docs/workflows/`
2. **Delete** the temporary file (plan, scratch, superseded merge note, leftover PROGRESS section).
3. Do **not** copy the temporary file into `docs/history/` “for safekeeping.” Git already has it.

If nothing lasting remains, delete without promoting. That is success, not loss.

---

## Optional: Topic Living Docs

Some repos keep long-lived truth in topic files (e.g. `systems/<topic>.md`) instead of one giant `architecture.md` + `docs/components/`. That is allowed when:

- AGENTS (or a short find-table) routes agents to the right topic
- Each topic owns one concern
- Merges into topics are heading-audited for zero-loss; then source scratch/plans are deleted

Do not force this shape on every repo. Homelab DOC_GUIDE-style layouts may stay project-specific.

---

## Legacy PROGRESS.md

If you find `PROGRESS.md`:

1. Move still-active items to Issues and/or `docs/plans/`.
2. Promote buried decisions / architecture notes to their living homes.
3. Delete `PROGRESS.md`.
4. Update AGENTS routes that pointed at it.

See `progress-md-guide.md` only for migration mechanics — not for how to write a new PROGRESS.

---

## Anti-Patterns

- Dated-record sprawl: `docs/history/YYYY-MM.md`, weekly status dumps, “movement not deletion”
- Meta-indexes: `docs/README.md` that only lists other docs
- Governance-about-governance docs that restate this skill
- Renaming PROGRESS to HANDOFF/STATUS and keeping the diary behavior
- Forcing four-primary + PROGRESS + history onto every repo
