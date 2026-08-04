# Lessons Corpus

A human-gated, git-versioned corpus of **operational lessons** — distilled,
ratified "don't do it that way again" records. This is deliberately **not** an
autonomous memory layer: the files are inert markdown. All reasoning over the
corpus (capture, corroboration, promotion, supersede) happens in-session, at
the human's explicit direction, with diffs reviewed before they land.

Automatic capture systems (kcap, control-plane stores, measurement databases)
already exist below this corpus as raw material. This directory is the thin
curated layer on top: nothing enters except through a reasoning session, and
every claim is one hop away from its raw evidence in those systems.

## Record format

One file per lesson: `L-YYYY-NNN-short-slug.md`.

```markdown
---
id: L-2026-NNN
title: <short imperative>
status: hypothesis | corroborated | settled
recorded: YYYY-MM-DD
---
## Trigger       <- when this lesson applies; plain text; the retrieval key
## Lesson        <- one short imperative paragraph
## Evidence      <- bullets tagged [direct] / [inference]; pointers (session ids,
                    doc paths, run ids), not copied content
## Guard         <- mechanically checkable form, or "none yet"
## Recurrences   <- dated list; first entry is the origin episode
## Superseded by <- empty until superseded; supersession is never silent deletion
```

Status vocabulary matches the retrospective skill's Proposal scale:
- **hypothesis** — one observation.
- **corroborated** — two or more independent observations.
- **settled** — human-confirmed or structurally verified.

## Lifecycle

1. **Capture** — only on explicit request ("persist this lesson"). The agent
   drafts the record, the human ratifies, the file lands in git. No automatic
   extraction, no hooks, no background jobs.
2. **Corroborate** — when a lesson recurs, a reasoning session adds a
   Recurrences entry and may raise status.
3. **Promote** — settled lessons with a mechanically checkable guard can be
   promoted into a target repo's own machinery (e.g. LocalLargeLanguageModels
   `docs/failure-catalog.md` + rubric guard). Promotion is a manual, per-repo
   act; this corpus does not push itself anywhere.
4. **Supersede** — a wrong or stale lesson gets a `Superseded by` pointer and
   stays in history. Never silent deletion; git history is the audit trail for
   the reasoning itself.

## Retrieval

`index.md` is the retrieval surface: one line per lesson with its trigger
summary. Agent prompts (e.g. LocalLargeLanguageModels investigator/examiner)
are instructed to read the index at planning time. A lesson applies when its
Trigger matches the planned work; applied lessons must be cited in the plan
artifact, so what influenced a decision is always visible.

## Relationships

- **retrospective skill** (`_incubator/personal-skills/retrospective`): keeps
  writing per-project Learnings to agent-control-plane on the Windows machine.
  This corpus is cross-project and machine-local. Cross-pollination is manual.
- **failure-catalog.md** (LocalLargeLanguageModels): lessons promote *into* it
  once they recur and have a checkable guard. The catalog stays that repo's
  authority.
- **kcap / control-plane / measurement stores**: evidence pointers reference
  these systems of record instead of duplicating their content.

## Durability

- Source of truth is **git, pushed to the GitHub remote**
  (`MooseGooseConsulting/frozenSkillz`). A lesson is not considered persisted
  until committed and pushed; capture sessions end with a commit, not dirty
  files.
- Stretch goal (someday): a database mirror (Postgres/control-plane) for query
  and retrieval scoring. The DB is always a **derived index, rebuildable from
  git at any time** — never the primary store, so losing the DB loses nothing.
  The frontmatter format is chosen so a loader stays trivial.
