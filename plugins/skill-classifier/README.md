# skill-classifier (experimental)

A `UserPromptSubmit` hook that classifies your intent against your installed
skill catalog using a small, fast LLM, then injects a targeted suggestion so the
right skill gets loaded automatically.

**Two-layer architecture:**

1. **Layer 1 (hook):** fast LLM classification — *"what category of task is this?"*
2. **Layer 2 (skills):** detailed guidance from the loaded skill — *"here's how to do it."*

> **Status:** experimental / WIP (`v0.2.0`).

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
| `SKILL_CLASSIFIER_TIMEOUT` | `10` | Per-call request timeout (seconds). |
| `SKILL_CLASSIFIER_CONNECT_TIMEOUT` | `0.5` | TCP reachability pre-check timeout (seconds). |
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

With Ollama resident, classification round-trip is typically well under 2s. When
Ollama is **not** running, a fast TCP pre-check (~1s, bounded) short-circuits the
call so a per-prompt hook never stalls — it then falls back to Gemini (in `auto`)
or silently passes through.

## Failure policy

Classification is best-effort guidance, never a hard dependency. On **any**
failure — backend unreachable, timeout, malformed output, no skills found — the
hook prints nothing and exits 0 (silent passthrough). It never blocks your
prompt.

## Testing

```bash
# Backend unit tests (no live model needed — uses a local HTTP stub):
python plugins/skill-classifier/test_llm_backend.py

# Manual end-to-end harness (uses whatever backend is configured):
python plugins/skill-classifier/test_classifier.py            # interactive
RUN_LATENCY=1 python plugins/skill-classifier/test_classifier.py   # headless + latency
```

## Files

| Path | Purpose |
| --- | --- |
| `scripts/skill_classifier.py` | The `UserPromptSubmit` hook entry point. |
| `scripts/llm_backend.py` | Swappable LLM backend (Ollama / Gemini). |
| `hooks/hooks.json` | Hook registration. |
| `skills/skill-classifier/SKILL.md` | User-facing skill documentation. |
| `docs/decisions/` | Architecture Decision Records (ADRs 001–006). |
| `test_llm_backend.py` | Automated backend tests. |
| `test_classifier.py` | Manual classifier harness. |

See [`docs/decisions/`](docs/decisions/) for the design rationale (ADR 002 covers
the original Gemini-CLI MVP; the swappable backend introduced in `v0.2.0`
supersedes its single-backend assumption).
