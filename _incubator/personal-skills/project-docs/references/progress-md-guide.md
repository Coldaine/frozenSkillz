# Legacy PROGRESS.md — Migrate Away

`PROGRESS.md` is **not** part of the recommended authority stack.

Do not create a new PROGRESS.md. Do not rename it to HANDOFF.md or STATUS.md and keep the diary.

If a repo still has one, this guide is only for **migrating content out and deleting the file**.

---

## Why It Was Retired

PROGRESS was meant as a rolling handoff window. In practice it became:

- a permanent diary
- a second roadmap
- a burial ground for durable decisions
- paired with `docs/history/` roll-off (“movement, not deletion”) — the dated-record sprawl machine

Settled preference: Issues and/or `docs/plans/` for current work; promote lasting facts; delete temporary docs; git is the archive.

See `current-work-and-lifecycle.md`.

---

## Migration Steps

1. **Active items** → open GitHub Issues and/or a Status block on the relevant `docs/plans/` file.
2. **Buried decisions** → `docs/decisions/` (ADR) + reference from architecture if needed.
3. **Architecture notes** → `architecture.md` or topic/component docs.
4. **Procedures** → `docs/workflows/`.
5. **Completed diary entries** → delete (recoverable from git). Do not create `docs/history/YYYY-MM.md`.
6. **Delete** `PROGRESS.md`.
7. **Update AGENTS.md** routes and remove handoff-to-PROGRESS sections.
8. **Run** `authority-flow.md` pass.

---

## Review Questions (legacy file still present)

- Are active items already tracked in Issues/plans?
- Are durable decisions still only in PROGRESS?
- Does AGENTS still route here?
- Can the file be deleted this session?

If content still matters, the fix is **promote then delete**, not “roll into history.”

---

## Guardian Note

A future Guardian may flag “PROGRESS.md exists” or “AGENTS routes to PROGRESS” as drift against this skill’s rules — not as a request to refresh the diary.
