# Analysis: fable5-opus5-orchestrator

Scored against `plugins/frozen-skills/skills/external-skill-intake/references/artifact-rubrics.md`.

The plugin does not score as one artifact. It is three components with sharply different value, and averaging them would hide the whole finding. Scored separately.

## Component A — Ledger discipline + playbook skill

Paths: `skills/playbook/SKILL.md`, `instructions/dynamic-workflow-fable.md` (Rule 1), the `LEDGER.md` checkbox grammar.
Type: skill / documentation-pattern.

| Dimension | Score | Rationale |
|---|---:|---|
| Purpose clarity | 5 | "Write every requirement to a file before delegating" — explicit, narrow, one job. |
| Activation clarity | 4 | "Load before your first delegation each session" is unambiguous, but depends on the injected core to fire it. |
| Output contract | 5 | Five numbered return fields, ≤40 lines total, >10 lines verbatim spills to disk with a path. Rare specificity. |
| Reuse value | 4 | Concept transfers anywhere; needs de-coupling from Fable-chair tier names. |
| Progressive disclosure | 5 | Exemplary — slim always-injected core, heavy detail deferred to on-demand skill, core size budget asserted in tests. |
| Safety/security risk | 5 | Pure text. No execution surface. |
| Portability | 5 | A markdown checklist file. Platform-independent. |
| Testability/evaluability | 2 | Zero model evals. Content tests assert text is *present*, never that it *works*. Author concedes hooks check "existence and checkbox state, not fidelity." |
| Maintenance burden | 4 | Text-only, low burden; model tier names will drift. |
| Fit with frozenSkillz scope | 5 | Directly supports reusable agent workflows. |

**Average: 4.4** — band: useful pattern, needs focused cleanup or eval proof.

## Component B — Spawn/task guard hook

Path: `scripts/ledger_guard_spawn.py`.
Type: hook.

| Dimension | Score | Rationale |
|---|---:|---|
| Purpose clarity | 5 | Gate spawns over N chars when no active ledger exists. One sentence. |
| Activation clarity | 5 | `PreToolUse` matcher `^(Agent\|Task\|Workflow\|TaskCreate)$`, explicit in `hooks.json`. |
| Output contract | 5 | Standard `permissionDecision` / `hookSpecificOutput`; deny message tells the model what to do instead. |
| Reuse value | 4 | Useful in any repo doing multi-phase agent work. |
| Progressive disclosure | 3 | Single 409-line script, but heavily commented with rationale. |
| Safety/security risk | 5 | No `subprocess`, no network, no `shell=True`. Fails open on every exception. |
| Portability | 3 | 40/42 tests pass on Windows; `fcntl` degrades deliberately. Blocked only by `python3` hardcoded in `hooks.json`. |
| Testability/evaluability | 5 | 42 tests running the hook end-to-end as real subprocesses over stdin/stdout JSON. |
| Maintenance burden | 4 | Couples only to the **public** hook contract (`tool_name`, `tool_input`, `permissionDecision`). Low drift risk. |
| Fit with frozenSkillz scope | 4 | Adjacent-to-direct; enforces a discipline this repo already values. |

**Average: 4.3** — band: useful pattern, needs focused cleanup or eval proof.

## Component C — SessionStart injector + tmux teammate reaper

Paths: `scripts/inject_instructions.py`, `scripts/cleanup_session_cache.py`, reaping half of `scripts/ledger_guard_stop.py`.
Type: hook / config.

| Dimension | Score | Rationale |
|---|---:|---|
| Purpose clarity | 4 | Clear: inject profile, kill orphaned teammates. |
| Activation clarity | 3 | Fires ambiently on every SessionStart/Stop/SessionEnd; detection order is a 4-level fallback chain. |
| Output contract | 3 | Injection is additionalContext; reaping returns only a count. |
| Reuse value | 1 | Locked to POSIX + `tmux` + the agent-teams backend. Zero value on Windows. |
| Progressive disclosure | 3 | Reasonable module separation. |
| Safety/security risk | 2 | Destructive by design. Kills panes on a **CPU-rate heuristic** — a teammate blocked in one long quiet external wait gets killed mid-wait (author documents this). Scoping is careful, but the blast radius is real processes. |
| Portability | 1 | `os.getuid`, `/tmp/tmux-$UID`, `ps`, `tmux`. 21 of 34 Windows failures originate here. |
| Testability/evaluability | 4 | Well tested against a fake `tmux`/`ps` on PATH. |
| Maintenance burden | 1 | Couples to **undocumented** host internals: `--agent-id`, `--parent-session-id`, `claude-swarm-*` socket names, `@session-` pane tags, `settings.json` model field, process-tree walking. This coupling **already broke once** — the README documents the teammate layout moving from dedicated servers to the user's default tmux server between Claude Code versions, forcing version-proofing code. It will break again. |
| Fit with frozenSkillz scope | 1 | Out of scope. This repo does not manage tmux process lifecycles. |

**Average: 2.3** — band: incubate or mine for small ideas only. In practice: discard.

## Verdict

**Is it a good plugin?** For its author's setup, yes — genuinely above average for this ecosystem. The test-to-source ratio exceeds 1:1, hooks fail open, destructive calls are narrowly scoped, and the README's "Honest limitations" section volunteers seven real weaknesses including one where the guard was observed failing outright. That is more intellectual honesty than most plugins in this space show.

**For this repo and this operator, no — it is not adoptable.** Three independent reasons, any one sufficient:

1. **It cannot run here.** `hooks/hooks.json` hardcodes `python3`, absent from this machine's PATH. Upstream declares macOS/Linux only.
2. **Its most complex half is its most fragile half.** The tmux/injector layer carries all the destructive behavior *and* all the undocumented-internals coupling, and has already required rework from upstream drift. That is the worst possible combination to take on as a maintenance dependency.
3. **Its central claim is unevidenced.** The plugin asserts the ledger improves outcomes; it ships no eval demonstrating that, and its own hooks cannot distinguish a faithful ledger from a shallow one.

**But the ideas are worth keeping**, and they are cleanly separable from the code that fails:

- Ledger-before-delegation with a mandatory final `- [ ] V. fresh-eyes verification passed` item that only a fresh verifier may close.
- The `- [~] deferred: <reason>` grammar requiring explicit user approval — a third state between open and done, which most checklists lack.
- The ≤40-line subagent report contract with verbatim spilling to disk plus a path.
- Progressive disclosure with the entrypoint's size budget **asserted in tests** — directly applicable to how this repo splits `SKILL.md` against `references/`.
- Batching mechanical work into one worker because every spawn pays fixed overhead.

## Recommendation

**Adapt concept only.** Discard Component C entirely. Component A's patterns are the prize and are platform-independent. Component B is a defensible future port if repeated manual pain justifies it — not now, and not before an eval exists.

Per `docs/workflows/external-skill-intake.md`, none of Component A may be promoted into `plugins/` until a live eval is persisted under `evals/runs/` comparing baseline / candidate-inspired / frozenSkillz-adapted output. This analysis is a scoring pass only.

A first live eval is now persisted at `evals/runs/2026-07-31-spawn-prompt-richness.md`. It does not
satisfy that promotion gate: it ran two arms rather than three, and its comparative result is
unusable because the candidate arm's instrument could not observe sub-threshold prompts. What it
does establish is that Component B's guard is near-inert at its default threshold and is portable
to Windows with a one-line fix. Component A's promotion gate remains open.
