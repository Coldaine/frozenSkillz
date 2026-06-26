# 06 — skill + CLI exploration (EXPLORATORY, not settled)

> **Status: EXPLORATORY.** This is research input from spec-kit and bmad-method, not a
> decision. The user explicitly flagged: "I feel like we might have tried to learn a
> little too much from the bmad method and spec-kit. That's not settled. That's just
> something we were exploring." The load-bearing output of this work is the NORTH_STAR
> and architecture.md principles (sessions 02 and 03). Treat this file as research that
> informed the design, not as a committed architecture.

## The headline both repos agree on

**Neither spec-kit nor bmad-method actually solves self-enforcement.** Both build the
*architecture* for it and stop short of wiring the gate. We can't copy either one and be
done — we'd have to build the part both left unfinished.

| | spec-kit | bmad-method |
|---|---|---|
| Built | CLI-scaffolds-skill + `scripts:` prerequisite gate + hook rail + workflow `gate` steps | CSV routing graph + artifact-glob completion + status-YAML + 3-layer TOML override |
| Did NOT build | Content-aware validation wired into a gate; `*(mandatory)*` markers can be written away | The runtime gate that blocks novel work missing its doc artifact ("Dev Loop Automation" = roadmap) |
| Self-enforcement | Shallow — existence-gating + human approval only | D — explicitly "soft suggestions, not hard gates" |

Both have the seam. Neither wires it to content.

## What was explored as stealable from spec-kit

- **CLI-scaffolds-skill inversion** — SKILL.md as a generated projection of a CLI, not
  hand-maintained. Force-include templates in the wheel so scaffolded files match CLI
  version.
- **`scripts:` front-matter prerequisite gate** — shell/PS script that `exit 1`s before
  the agent's prompt body runs. spec-kit uses it for "no `implement` without `tasks.md`."
- **Constitution-as-input + detect-empty-template** — instead of pretending a Guardian
  will enforce, detect the constitution is still an unfilled template and degrade
  gracefully. Kills the "Guardian runtime doesn't exist" ceremony.
- **The hook rail, wired to a validator** — spec-kit built `after_*` hooks and used them
  for git auto-commit. The idea: wire ours to a doc-drift validator.
- **`unrequested` finding type from `converge`** — flags code not called for by any doc.
  The "novel work without a doc update" smell. Pair it with a block, not the advisory
  spec-kit ships.
- **"Unit tests for English" checklist framing** — stops a doc-quality checklist decaying
  into a code-test checklist.

## What was explored as stealable from bmad-method

- **CSV routing-table schema** (`phase / preceded-by / followed-by / required / outputs`)
  as the workflow graph declaration.
- **Artifact-glob completion detection** — infer "done" from files on disk, not chat
  history. Session-independent by construction.
- **`*-status.yaml` state file + enum-validated statuses** — drives "what doc work is
  pending / stale / orphaned."
- **`correct-course` Minor/Moderate/Major triage** — the Loop 3 side-quest mechanism:
  triage drift into severity buckets that route to different handlers, rather than
  "don't drift."
- **Three-layer TOML override (base → team → user)** — the strongest candidate mechanism
  for the "non-negotiable lines don't survive agent rewrites" problem. Fixed commentary
  lives in a structured override file the agent never touches as prose, injected at
  generate/validate time. **Beats HTML-comment markers** because the override file is
  structurally unreachable by the agent's prose edits.

## What to avoid from both (these ARE settled as avoid)

- **spec-kit:** the SDD methodology and nine-articles constitution (the "too generic"
  part), heavy template ceremony (`tasks-template.md`'s multi-phase `[P]` parallel
  structure — same inventory-table disease already diagnosed, worse), `analyze` as
  enforcement (read-only/non-blocking by design), `converge` as the *only* drift defense.
- **bmad-method:** persona-as-enforcement ("You are Winston" is a prompt costume, not a
  constraint), checklist-as-gate when it's really a prompt (`bmad-create-story/checklist.md`'s
  14KB "competitive excellence" theater), the `required=true` illusion (in bmad it's a
  recommendation label, not a block — if we label something required, a CLI must
  actually refuse), the "competitive excellence" / "scale-adaptive intelligence" rhetoric.

## The architecture that was sketched (NOT committed)

```
CLI (source of truth + the gate)
  - generates the SKILL.md projection
  - carries the mechanical enforcement
  - owns the override layer (non-negotiables)
        │ generates                    │ enforces
        ▼                              ▼
  Skill layer (generated)        Declaration + state files
  - the reasoning                - docs-workflow.csv (graph)
  - guides, anti-patterns        - docs-status.yaml (state)
  - "approach not inventory"     - override.toml (fixed lines)
  Agent reads mid-task           - constitution.md (input)
                                       │
                                       ▼
                                 scripts: gate (the seam)
                                 - check-doc-state.sh/ps1
                                 - exit 1 if docs stale
                                 - exit 1 if novel work has
                                   no doc update (unrequested)
                                 - after_* hooks wired to it
```

**Why the split might be necessary, not just convenient:** the skill layer can only
*persuade* — an agent reads it and might follow it. The CLI layer *enforces* — it exits
non-zero, blocks the step, fails the PR. Every failure diagnosed in this work traces to
making the skill layer do enforcement work it structurally cannot do. spec-kit and bmad
both prove the split ships; neither proves it enforces, because neither wired the gate.

## The four problems, graded against the sketched architecture

| Problem | spec-kit alone | bmad alone | Sketched skill+CLI |
|---|---|---|---|
| Self-enforcement | D | D | A — `scripts:` gate + `after_*` hook wired to content-aware validator |
| Ideas-not-now shelf | F | C+ | A — `candidates/` row in docs-workflow.csv, status `shelved` |
| Side-quest prevention | C | B | A — correct-course triage made mechanical, invoked from the gate |
| Session/agent handoff | B | B+ | A — status-YAML + artifact-glob, agent orients from files alone |

## Open questions when resuming

- Is the skill+CLI split actually worth the build cost, or does a lighter enforcement
  mechanism (a single validator script + a fixed-lines override file, no full CLI)
  capture 80% of the value?
- Is the CSV routing graph overkill for a docs methodology, or is it the right
  declarative backbone?
- The TOML override layer is the strongest candidate for the non-negotiable-lines
  problem — but is it worth a separate file + resolver vs. a simpler scaffold with
  CLI-validated fixed regions?
- These were not decided. They were being explored when the session paused.
