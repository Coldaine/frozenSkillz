#!/usr/bin/env python3
"""frozenSkillz — Swappable LLM backend for classification hooks.

This module isolates the "call a small/fast LLM and get text back" concern so
that hooks (skill_classifier, prompt_quality_gate, ...) do not care which model
or transport is used.

Backends
--------
- ``ollama`` (default): local Ollama REST API. Stays resident, so there is no
  per-call process startup cost. Pure stdlib (``urllib``), no extra packages.
- ``gemini``: Gemini Flash via the ``gemini`` CLI (the original backend). Kept
  as a fallback so existing GEMINI_API_KEY setups keep working.

Selection
---------
``SKILL_CLASSIFIER_BACKEND`` env var: ``ollama`` | ``gemini`` | ``auto``
(default ``auto``). In ``auto`` mode the backends are tried in order
(ollama, then gemini) and the first one that returns a non-empty completion
wins. An explicitly named backend is tried first, then the remaining ones are
used as fallback so a misconfigured primary still degrades gracefully.

Configuration env vars
-----------------------
- ``SKILL_CLASSIFIER_BACKEND``  backend selector (see above)
- ``OLLAMA_HOST``               Ollama base URL or host:port (default
  ``http://localhost:11434``)
- ``SKILL_CLASSIFIER_MODEL``    Ollama model tag (default ``llama3.2:3b``)
- ``GEMINI_MODEL``              Gemini CLI model (default
  ``gemini-3-flash-preview``)
- ``SKILL_CLASSIFIER_TIMEOUT``  per-call timeout seconds (default ``10``)

Failure policy
--------------
Every public function returns ``""`` on any failure. Callers rely on this for
silent passthrough — the LLM is best-effort guidance, never a hard dependency.
"""

import json
import os
import socket
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime
from urllib.parse import urlparse

IS_WINDOWS = sys.platform == "win32"

# --- Defaults (all overridable via env) ---

DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "llama3.2:3b"
DEFAULT_GEMINI_MODEL = "gemini-3-flash-preview"
DEFAULT_TIMEOUT_SECONDS = 10
# Fast reachability guard. When Ollama is down, some OSes (notably Windows with
# its firewall) silently drop the SYN instead of refusing, so a normal connect
# blocks for the full request timeout — twice, once per resolved address of
# ``localhost`` (::1 and 127.0.0.1). A tight pre-check keeps a per-prompt hook
# snappy when Ollama is not running.
DEFAULT_CONNECT_TIMEOUT_SECONDS = 0.5


def log(msg: str) -> None:
    """Log to stderr (visible in debug, invisible to the hook consumer)."""
    stamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[frozenSkillz/llm {stamp}] {msg}", file=sys.stderr)


def _timeout() -> float:
    try:
        return float(os.environ.get("SKILL_CLASSIFIER_TIMEOUT", DEFAULT_TIMEOUT_SECONDS))
    except (TypeError, ValueError):
        return DEFAULT_TIMEOUT_SECONDS


def _connect_timeout() -> float:
    try:
        return float(os.environ.get(
            "SKILL_CLASSIFIER_CONNECT_TIMEOUT", DEFAULT_CONNECT_TIMEOUT_SECONDS))
    except (TypeError, ValueError):
        return DEFAULT_CONNECT_TIMEOUT_SECONDS


def _ollama_base_url() -> str:
    host = os.environ.get("OLLAMA_HOST", DEFAULT_OLLAMA_HOST).strip()
    if not host:
        host = DEFAULT_OLLAMA_HOST
    if not host.startswith(("http://", "https://")):
        host = f"http://{host}"
    return host.rstrip("/")


def _ollama_reachable(base_url: str, connect_timeout: float) -> bool:
    """Tight TCP pre-check so a down Ollama never stalls the hook.

    Tries each resolved address with a short per-address timeout (at most two,
    to bound worst-case time when ``localhost`` resolves to both ::1 and
    127.0.0.1). Returns True on the first successful connect.
    """
    parsed = urlparse(base_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 11434
    try:
        infos = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except OSError as e:
        log(f"Ollama DNS resolve failed ({host}:{port}): {e}")
        return False
    for af, socktype, proto, _canon, sockaddr in infos[:2]:
        s = socket.socket(af, socktype, proto)
        s.settimeout(connect_timeout)
        try:
            s.connect(sockaddr)
            return True
        except OSError:
            continue
        finally:
            s.close()
    return False


# --- Backends ---

def _ollama_complete(prompt: str, timeout: float) -> str:
    """Call the local Ollama REST API. Returns completion text or ""."""
    base = _ollama_base_url()
    if not _ollama_reachable(base, _connect_timeout()):
        log(f"Ollama not reachable at {base} - skipping")
        return ""
    url = f"{base}/api/generate"
    model = os.environ.get("SKILL_CLASSIFIER_MODEL", DEFAULT_OLLAMA_MODEL).strip() or DEFAULT_OLLAMA_MODEL
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        # Deterministic, short output — this is a classification task.
        "options": {"temperature": 0},
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        return (data.get("response") or "").strip()
    except urllib.error.URLError as e:
        log(f"Ollama unreachable ({url}): {e}")
        return ""
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        log(f"Ollama bad response: {e}")
        return ""
    except Exception as e:  # noqa: BLE001 — best-effort, never raise to caller
        log(f"Ollama failed: {e}")
        return ""


def _gemini_complete(prompt: str, timeout: float) -> str:
    """Call Gemini via the CLI subprocess. Returns completion text or "".

    Uses a temp file piped on stdin to avoid shell quoting issues on Windows
    with long multi-line prompts containing special characters.
    """
    model = os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL
    tmp = None
    try:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        tmp.write(prompt)
        tmp.close()

        with open(tmp.name, "r", encoding="utf-8") as f:
            result = subprocess.run(
                ["gemini", "--model", model, "--output-format", "text"],
                stdin=f,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=IS_WINDOWS,
            )
        if result.returncode != 0:
            log(f"Gemini CLI error: {result.stderr.strip()}")
            return ""
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        log("Gemini CLI timed out")
        return ""
    except FileNotFoundError:
        log("Gemini CLI not found")
        return ""
    except Exception as e:  # noqa: BLE001
        log(f"Gemini CLI failed: {e}")
        return ""
    finally:
        if tmp is not None:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass


_BACKENDS = {
    "ollama": _ollama_complete,
    "gemini": _gemini_complete,
}

# Order tried in "auto" mode and as fallback after an explicit primary.
_DEFAULT_ORDER = ["ollama", "gemini"]


def _backend_order() -> list:
    """Resolve the ordered list of backends to attempt."""
    choice = os.environ.get("SKILL_CLASSIFIER_BACKEND", "auto").strip().lower()
    if choice in ("", "auto"):
        return list(_DEFAULT_ORDER)
    if choice not in _BACKENDS:
        log(f"Unknown backend '{choice}', falling back to auto order")
        return list(_DEFAULT_ORDER)
    # Named primary first, then the rest as graceful fallback.
    return [choice] + [b for b in _DEFAULT_ORDER if b != choice]


def complete(prompt: str, timeout: float = None) -> str:
    """Return an LLM completion for ``prompt`` as text, or "" on failure.

    Tries each configured backend in order until one returns non-empty text.
    Never raises — failure is reported as an empty string so callers can
    silently pass through.
    """
    if not prompt or not prompt.strip():
        return ""
    if timeout is None:
        timeout = _timeout()
    for name in _backend_order():
        fn = _BACKENDS[name]
        text = fn(prompt, timeout)
        if text:
            log(f"backend '{name}' returned {len(text)} chars")
            return text
    return ""


def active_backend_label() -> str:
    """Human-readable description of the configured backend (for docs/debug)."""
    order = _backend_order()
    if order == _DEFAULT_ORDER:
        return f"auto ({' -> '.join(order)})"
    return f"{order[0]} (fallback: {', '.join(order[1:]) or 'none'})"
