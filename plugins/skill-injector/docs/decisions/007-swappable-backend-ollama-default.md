# ADR-007: Swappable LLM Backend with Ollama as Default

**Status:** Accepted (supersedes the single-backend assumption of [ADR-002](002-gemini-flash-cli-mvp.md))
**Date:** 2026-05-28
**Deciders:** pmacl
**Issue:** [#5 — Replace Gemini Flash backend with faster lightweight LLM](https://github.com/Coldaine/frozenSkillz/issues/5)

## Context

ADR-002 chose the Gemini CLI as the MVP backend, explicitly flagging its ~8–10s
process-startup latency on Windows as "acceptable for validation, not for daily
use" and naming a swap as the upgrade path. For a hook that fires on **every**
`UserPromptSubmit`, that fixed startup cost is the dominant problem: the CLI must
boot Node.js, load credentials, and initialize its registry before inference even
begins.

The classification task itself is small (a ~50–500 token prompt, a ~1k token
skill catalog, ~2k tokens of recent context) and well within reach of a 1–3B
local model.

## Decision

Introduce a dedicated backend module, `scripts/llm_backend.py`, and make the
backend selectable at runtime:

- **`ollama` (default):** the local Ollama REST API (`/api/generate`), called
  with the Python **standard library only** (`urllib`). Ollama stays resident,
  so there is no per-call startup cost.
- **`gemini` (fallback):** the original Gemini CLI path, preserved verbatim
  (temp-file-over-stdin, `shell=True` on Windows) so existing setups keep working.

Selection is via `SKILL_CLASSIFIER_BACKEND` (`ollama` | `gemini` | `auto`,
default `auto`). In `auto` mode backends are tried in order (Ollama → Gemini) and
the first non-empty result wins.

`classify()` no longer talks to a CLI directly — it builds the prompt and calls
`llm_backend.complete()`, then parses the JSON array. This realizes the
"swappable backend" the original `classify()` signature was designed for.

## Rationale

### Latency

With Ollama resident, round-trip is well under the issue's 3s target. The remaining
risk was the *down* case: on Windows, a closed port silently drops the SYN rather
than refusing it, and `localhost` resolves to both `::1` and `127.0.0.1`, so a
naive request blocks for the full timeout twice (~4s measured). A tight TCP
reachability pre-check (`SKILL_CLASSIFIER_CONNECT_TIMEOUT`, default 0.5s, bounded
to two addresses) short-circuits this to ~1s.

### No new dependencies

The Ollama path uses only `urllib` and `socket`. The plugin's `requirements` drop
`google-generativeai` and the mandatory `GEMINI_API_KEY`; both become optional and
relevant only to the Gemini fallback.

### Graceful degradation preserved (ADR-004)

Every backend returns `""` on any failure, so the hook's silent-passthrough
guarantee is unchanged: backend down, timeout, bad output, or no skills → print
nothing, exit 0.

## Configuration

See the plugin [`README.md`](../../README.md#configuration) for the full env-var
table. Key knobs: `SKILL_CLASSIFIER_BACKEND`, `SKILL_CLASSIFIER_MODEL`,
`OLLAMA_HOST`.

## Consequences

- **Positive:** Default path is fast, key-free, and dependency-free. The hook is
  viable for daily use, not just validation.
- **Positive:** The backend is genuinely pluggable — a third backend (e.g.
  Anthropic Haiku) is a single function plus a registry entry.
- **Positive:** Path resolution for the skill catalog moved off the hard-coded
  `/app/...` POSIX paths to `CLAUDE_PLUGIN_ROOT`-relative resolution, so the hook
  actually finds skills on Windows and in-repo.
- **Negative:** Two backends to maintain. Mitigated by isolating both behind one
  `complete()` entry point and covering them with `test_llm_backend.py` (Ollama
  exercised against a local HTTP stub, no live model required).
- **Neutral:** The default model tag (`llama3.2:3b`) is a guess at what users will
  have pulled; it is fully overridable via `SKILL_CLASSIFIER_MODEL`.
