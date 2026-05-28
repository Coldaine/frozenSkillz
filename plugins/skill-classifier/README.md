# skill-classifier (experimental)

Two small-LLM-backed hooks that share one swappable backend:

1. **Skill classifier** (`UserPromptSubmit`) — classifies your intent against
   your installed skill catalog and injects a targeted suggestion so the right
   skill gets loaded automatically.
2. **Subagent prompt quality gate** (`PreToolUse` on `Agent`/`Task`) — reviews
   the prompt you are about to send to a subagent against a quality checklist
   and injects *advisory, non-blocking* feedback. See
   [Subagent prompt quality gate](#subagent-prompt-quality-gate-pretooluse).

The classifier follows a **two-layer architecture:**

1. **Layer 1 (hook):** fast LLM classification — *"what category of task is this?"*
2. **Layer 2 (skills):** detailed guidance from the loaded skill — *"here's how to do it."*

> **Status:** experimental / WIP (`v0.3.0`).

## LLM backend

The backend that does the classification is **swappable**. All transport logic
lives in [`scripts/llm_backend.py`](scripts/llm_backend.py); the classifier only
owns the prompt and parsing.

| Backend | Notes |
| --- | --- |
| **`ollama`** (default) | Local [Ollama](https://ollama.com) REST API. Stays resident, so there is no per-call process-startup cost. Uses only the Python standard library (`urllib`) — no extra packages, no API key. |
| **`gemini`** (fallback) | Gemini Flash via the `gemini` CLI. Requires the CLI on `PATH` and `GEMINI_API_KEY`. |

### Configuration

All configuration is via environment variables — nothing is hard-coded.

| Env var | Default | Purpose |
| --- | --- | --- |
| `SKILL_CLASSIFIER_BACKEND` | `auto` | `ollama`, `gemini`, or `auto`. In `auto` the backends are tried in order (Ollama → Gemini); the first non-empty result wins. A named backend is tried first, then the others act as fallback. |
| `SKILL_CLASSIFIER_MODEL` | `llama3.2:3b` | Ollama model tag. Use any small model you have pulled. |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama base URL (or `host:port`). |
| `SKILL_CLASSIFIER_TIMEOUT` | `3` | Per-call request timeout (seconds). Deliberately tight — this is a per-prompt hook. |
| `SKILL_CLASSIFIER_CONNECT_TIMEOUT` | `0.5` | TCP reachability pre-check timeout (seconds). |
| `SKILL_CLASSIFIER_KEEP_ALIVE` | `10m` | How long Ollama keeps the model resident after a call (avoids cold starts). |
| `GEMINI_MODEL` | `gemini-3-flash-preview` | Gemini CLI model. |
| `GEMINI_API_KEY` | — | Required only for the Gemini backend. |
| `SKILL_CLASSIFIER_SKILL_DIRS` | — | `os.pathsep`-separated dirs to scan for `SKILL.md`. Overrides the default (this plugin's `skills/` + sibling `frozen-skills/skills`). |

### Quick start (Ollama, recommended)

```bash
# 1. Install Ollama from https://ollama.com, then pull a small model:
ollama pull llama3.2:3b
# 2. Ensure the server is running (ollama serve, or the desktop app).
# 3. Nothing else — the hook uses Ollama by default.
```

### Using the Gemini fallback

```bash
export SKILL_CLASSIFIER_BACKEND=gemini      # or leave as 'auto'
export GEMINI_API_KEY="your-api-key-here"
```

### Performance

With Ollama resident, classification round-trip is typically well under 2s, and
`keep_alive` (default `10m`) keeps the model loaded between prompts so you don't
pay a cold start each time. When Ollama is **not** running, a fast TCP pre-check
(~1s, bounded) short-circuits the call so a per-prompt hook never stalls — it
then falls back to Gemini (in `auto`) or silently passes through.

**Cold start:** the *first* call after Ollama evicts the model from memory still
has to reload it, which can exceed the 3s `SKILL_CLASSIFIER_TIMEOUT`. In that
case the hook silently passes through (no suggestion that turn) rather than
blocking your prompt; the next prompt is warm. Raise `SKILL_CLASSIFIER_TIMEOUT`
if you prefer to wait for the cold call.

## Subagent prompt quality gate (PreToolUse)

A second hook (`scripts/prompt_quality_gate.py`) fires *before* the `Agent`/`Task`
tool dispatches a subagent. It sends the subagent prompt to the same LLM backend,
which checks it against a quality checklist distilled from a real failure where a
vague 6-question research prompt produced 2000+ words of fabricated specifics:

- one focused ask vs a wishlist (>2 distinct questions)
- says what **not** to do / not to guess; report "unknown" instead of estimating
- constrains response length / format
- provides context about what is already known
- does not mix lookup (*"what exists"*) with speculation (*"how fast is it"*)

When the prompt looks fine the model returns `OK` and the hook is silent.
Otherwise it injects up to three short suggestions as **advisory, non-blocking**
context (`hookSpecificOutput.additionalContext`) — it never denies the dispatch:

```
<agent-prompt-review>
Advisory on the subagent prompt you are about to dispatch (non-blocking — apply your judgment):
- Split the five questions into separate focused lookups.
- Tell the subagent to report "unknown" rather than estimate latency numbers.
</agent-prompt-review>
```

### Gate configuration

| Env var | Default | Purpose |
| --- | --- | --- |
| `SUBAGENT_PROMPT_GATE` | on | Set `0`/`off`/`false` to disable the gate entirely. |
| `SUBAGENT_PROMPT_GATE_MIN_CHARS` | `200` | Skip prompts shorter than this (trivial dispatches), bounding added latency. |

The gate reuses the backend env vars above (`SKILL_CLASSIFIER_BACKEND`, model,
timeouts). Because it adds one LLM round-trip per agent dispatch, it is gated on a
minimum prompt length and fast-fails (or silently passes through) when the backend
is unavailable. Disable it if you do not want any per-dispatch latency.

## Failure policy

Both hooks are best-effort guidance, never a hard dependency. On **any** failure —
backend unreachable, timeout, malformed output, no skills found, non-agent tool —
the hook prints nothing and exits 0 (silent passthrough). The classifier never
blocks your prompt and the gate never blocks an agent dispatch.

## Testing

```bash
# Backend unit tests (no live model needed — uses a local HTTP stub):
python plugins/skill-classifier/test_llm_backend.py

# Prompt quality gate tests (deterministic — stubbed backend, no network):
python plugins/skill-classifier/test_prompt_quality_gate.py

# Manual end-to-end harness (uses whatever backend is configured):
python plugins/skill-classifier/test_classifier.py            # interactive
RUN_LATENCY=1 python plugins/skill-classifier/test_classifier.py   # headless + latency
```

## Files

| Path | Purpose |
| --- | --- |
| `scripts/skill_classifier.py` | The `UserPromptSubmit` classifier hook entry point. |
| `scripts/prompt_quality_gate.py` | The `PreToolUse` subagent-prompt quality gate hook. |
| `scripts/llm_backend.py` | Swappable LLM backend (Ollama / Gemini), shared by both hooks. |
| `hooks/hooks.json` | Hook registration (both events). |
| `skills/skill-classifier/SKILL.md` | User-facing skill documentation. |
| `docs/decisions/` | Architecture Decision Records (ADRs 001–008). |
| `test_llm_backend.py` | Automated backend tests. |
| `test_prompt_quality_gate.py` | Automated quality-gate tests. |
| `test_classifier.py` | Manual classifier harness. |

See [`docs/decisions/`](docs/decisions/) for the design rationale: ADR-002 covers
the original Gemini-CLI MVP, ADR-007 the swappable backend (supersedes 002's
single-backend assumption, `v0.2.0`), and ADR-008 the subagent prompt quality
gate (`v0.3.0`).
