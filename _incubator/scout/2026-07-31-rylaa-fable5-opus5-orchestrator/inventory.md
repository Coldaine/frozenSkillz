# Inventory: fable5-opus5-orchestrator

## Provenance

- Source URL: https://github.com/Rylaa/fable5-opus5-orchestrator
- Commit or version: `828974b4998a6f24b0a56c635e3e090309a417a7` / plugin v0.15.0
- Import date: 2026-07-31
- License: MIT
- Reviewer: intake agent
- Scout path: `_incubator/scout/2026-07-31-rylaa-fable5-opus5-orchestrator/`

## Artifact Counts

| Type | Count | Notable paths |
|---|---:|---|
| skill | 1 | `skills/playbook/SKILL.md` (89 lines, frontmatter name+description only) |
| agent | 0 | — |
| command | 0 | — |
| hook | 4 | `hooks/hooks.json` → SessionStart, PreToolUse(`^(Agent\|Task\|Workflow\|TaskCreate)$`), Stop, SessionEnd |
| config | 3 | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.github/workflows/ci.yml` |
| template | 1 | `LEDGER.md` checkbox grammar (documented in README, not shipped as a file) |
| eval-case | 0 | no eval corpus; `tests/` are unit/integration tests, not model evals |
| documentation-pattern | 3 | README "Honest limitations"; ASCII routing/decision diagrams; progressive-disclosure split (slim core → on-demand playbook skill) |

Supporting code: 5 Python hook scripts (~1790 LOC) and 4 test modules (~2160 LOC). Test-to-source ratio > 1:1.

## Useful / risky / duplicate / stale paths

**Useful**
- `skills/playbook/SKILL.md` — the only self-contained, platform-independent artifact. Delegation contract: research pipeline, subagent output contract, spawn economics, forks, teammate lifecycle, verification procedure.
- `scripts/ledger_guard_spawn.py` — pure-Python gate (no subprocess). Denies >1500-char spawns when no active ledger exists; exempts `subagent_type: "fork"`; stale-complete ledger detection.
- Progressive-disclosure pattern — slim always-injected core + heavy detail deferred to an on-demand skill, with the core's size budget asserted in tests.
- README "Honest limitations" section — candidly enumerates 7 known weaknesses including a case where the guard was observed to fail.

**Risky**
- `scripts/cleanup_session_cache.py`, `scripts/ledger_guard_stop.py` — issue `tmux kill-pane` / `kill-server` and reap processes by CPU-rate heuristic. Destructive by design.
- Idle-reaping heuristic can kill a teammate blocked in a long quiet external wait (author documents this).
- SessionStart injector prepends a profile into *every* chair session — broad, ambient behavior change.

**Project-specific / not portable**
- Whole tmux teammate lifecycle layer (agent-teams backend assumption).
- Model-tier routing hardcoded to a Fable-chair economy.

**Stale**
- README badge and install instructions point at `Rylaa/fable5-orchestrator`; actual repo is `Rylaa/fable5-opus5-orchestrator`. Install snippet as published would fail.

## Risks

- **Secret surfaces:** none. No network calls, no credential reads. Metrics log at `~/.claude/fable-orch/metrics.jsonl` records events only, explicitly never prompt content; opt-out via `FABLE_ORCH_METRICS=0`.
- **Tool or platform assumptions:** POSIX-only. Requires `python3` on PATH, `tmux`, `ps`, `/tmp/tmux-$UID` sockets, `os.getuid`. Upstream README states "macOS and Linux only... Windows is not supported."
- **External dependencies:** none at runtime beyond stdlib + system `tmux`/`ps`. `pytest` for tests only.
- **License or provenance concerns:** none. MIT, single named author, clean history.
- **Generated or low-quality material:** none evident. Code is commented with rationale; failure modes documented rather than hidden.

### Safety audit (read-only review of `scripts/`)

| Check | Result |
|---|---|
| `shell=True` | none — all `subprocess.run` calls use list args |
| `eval` / `exec` / `__import__` / `pickle` | none |
| Network calls (`urllib`, `requests`, `socket`) | none |
| `tmux kill-server` scope | only on sockets whose basename starts with `claude-swarm-`; a non-swarm/default server is never killed |
| `tmux kill-pane` scope | requires `--agent-id` in the pane command **and** an exact `--parent-session-id` ownership match; prefix-collision test exists |
| Failure mode | wrapped in broad `except Exception` → hooks fail open, never block the session |

Conclusion: destructive surface is real but narrowly scoped and defensively written. No malicious or obfuscated behavior found.

### Windows portability probe (2026-07-31)

Upstream declares Windows unsupported; this operator is on Windows 11. Probe run against a scratchpad copy (never `source/`) with Python 3.13.14 / pytest 9.1.1:

| Module | Result | Dominant failure cause |
|---|---|---|
| `test_hooks_manifest.py` | 3 passed / 0 failed | — |
| `test_spawn_guard.py` | 40 passed / 2 failed | `$HOME`-boundary path semantics; metrics temp path |
| `test_stop_guard.py` | 35 passed / 12 failed | `os.getuid` (tmux reaping) |
| `test_inject_and_cleanup.py` | 40 passed / 20 failed | `os.getuid` (tmux reaping) |
| **Total** | **118 passed / 34 failed** | 21 of 34 = `os.getuid`/`geteuid` |

Findings:
1. `python3` is **not** on this machine's PATH (only `python`). `hooks/hooks.json` hardcodes `python3`, so the plugin as shipped would fail to fire here at all — a hard blocker independent of the POSIX issues.
2. The failure mass is confined to the tmux/reaping layer, which is exactly the part with no Windows analogue and no value on this platform.
3. The **ledger gate — the core idea — is already substantially portable** (40/42). `ledger_guard_spawn.py` imports no `subprocess` and degrades deliberately: `except ImportError: fcntl = None  # non-POSIX: run unlocked, best effort`. `cleanup_session_cache.py:333` likewise carries `# no tmux, or no os.getuid (Windows) — never fail the hook`.

So "Windows is not supported" is accurate for the plugin as a whole, and too pessimistic for the ledger-guard concept specifically.

## Initial Scope Recommendation

- **Evaluate:** (a) the Requirements-Ledger discipline — ledger-before-delegation, `V.` fresh-eyes verification item, `- [~] deferred` grammar; (b) the progressive-disclosure packaging pattern (slim core + on-demand playbook, size budget asserted in tests); (c) the playbook's subagent output contract (≤40-line reports, >10-line verbatim spills to disk with a path).
- **Defer:** `ledger_guard_spawn.py` as a possible Windows-portable hook. Attractive but requires porting work and a `python3`→`python` resolution; needs its own decision.
- **Discard:** the entire tmux teammate-reaping layer (`cleanup_session_cache.py`, the reaping half of `ledger_guard_stop.py`), the SessionStart profile injector, and the Fable-chair model-routing economics. POSIX-bound, host-backend-bound, or specific to an economy this repo does not share.
- **Needs more evidence:** whether the ledger discipline actually improves outcomes versus baseline. Upstream ships zero model evals — its own README concedes the hooks check "existence and checkbox state, not fidelity." Per `docs/workflows/external-skill-intake.md`, no promotion of this pattern is allowed without a persisted live eval.

## Notes for the scoring pass

The candidate's strongest contribution is conceptual, not executable: it takes soft orchestration advice and mechanizes the three failure points it claims are skipped most (task→plan translation, closing with unaddressed items, and never delegating at all). That framing is transferable to this repo regardless of platform. The code that implements it largely is not.
