# ADR-002: Gemini Flash 3 via CLI as MVP Backend

**Status:** Accepted (temporary — will be superseded by REST API)
**Date:** 2026-02-08
**Deciders:** pmacl

## Context

The classifier needs an LLM backend. We evaluated three options available on this machine today:

| Backend | Auth | Latency | Cost | Setup Required |
|---------|------|---------|------|---------------|
| Gemini CLI (v0.27.3) | Pre-configured (Google account) | ~10s on Windows | Free (Flash tier) | None — already installed |
| Gemini REST API | Needs `GEMINI_API_KEY` | ~300ms | Free (Flash tier) | API key provisioning |
| Anthropic SDK (Haiku 4.5) | `ANTHROPIC_API_KEY` in env | ~300-500ms | ~$0.001/call | pip install anthropic |

## Decision

Gemini Flash 3 via CLI for MVP. The `classify()` function is isolated so swapping to REST API or Anthropic SDK later requires changing one function.

## Rationale

### Zero setup gets us to validation faster

The gemini CLI is already installed and authenticated. We can validate the entire hook architecture — stdin parsing, transcript loading, skill scanning, output injection — without provisioning API keys or installing SDKs. The backend is the least important part to get right first.

### The latency problem is known and bounded

The ~10s CLI startup is Node.js bootstrap + credential loading + hook registry initialization. This is inherent to the CLI tool and independent of prompt complexity. We measured it:

```
Simple prompt ("Return exactly: []"):  ~9s
Full classification prompt (14 skills + context): ~10s
```

This confirms the overhead is fixed cost, not prompt-dependent. The REST API eliminates it entirely.

### Swappable backend architecture

The `classify(prompt, context, skills) -> list[str]` function signature is deliberately generic:
- Input: the user's prompt, formatted conversation context, and skill catalog
- Output: list of skill names (or empty)

The function internally builds the classification prompt and calls the LLM. Swapping backends means replacing `_call_gemini_cli()` with `_call_gemini_rest()` or `_call_anthropic_haiku()`. Nothing else changes.

## Windows-Specific Implementation Notes

### npm CLI shim resolution

On Windows, `npm install -g gemini` creates `gemini.cmd` (not `gemini.exe`). Python's `subprocess.run(["gemini", ...])` calls `CreateProcess` which only resolves `.exe` files. Fix: `shell=True` on Windows, which invokes `cmd.exe /c gemini ...`.

```python
IS_WINDOWS = sys.platform == "win32"
subprocess.run([...], shell=IS_WINDOWS)
```

### Long prompt argument escaping

Passing the classification prompt (~2KB, multi-line, contains quotes and brackets) as a `-p` argument with `shell=True` causes cmd.exe to hang indefinitely. The shell can't escape the content.

Fix: write prompt to a temp file, pipe via stdin, cleanup in `finally` block.

```python
tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
tmp.write(prompt)
tmp.close()
try:
    with open(tmp.name) as f:
        result = subprocess.run(["gemini", "--model", "...", "--output-format", "text"],
                                stdin=f, shell=IS_WINDOWS, ...)
finally:
    os.unlink(tmp.name)
```

This pattern is documented in the project's auto memory (`windows-subprocess.md`) for future reference.

## Upgrade Path

1. **Phase 2:** Switch to Gemini REST API via `urllib.request`. Same model (Flash 3), ~300ms latency, no CLI overhead. Requires provisioning `GEMINI_API_KEY` in Bitwarden Secrets Manager.
2. **Alternative:** Anthropic Haiku 4.5 via SDK. Better classification quality (hypothesis), but costs money per call. Good for accuracy comparison testing.

## Consequences

- **Positive:** MVP works today with zero setup. Architecture is validated end-to-end.
- **Negative:** 10s latency makes the hook blocking and noticeable. Users will feel a pause before Claude responds. Acceptable for validation, not for daily use.
- **Negative:** Temp file I/O adds ~5ms overhead and a cleanup obligation. Trivial cost.
