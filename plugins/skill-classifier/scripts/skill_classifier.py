#!/usr/bin/env python3
"""frozenSkillz — LLM-Powered Skill Classifier Hook.

UserPromptSubmit hook that classifies user intent against available skills
and injects targeted suggestions. Silent passthrough on any failure.

Backend: pluggable via ``llm_backend`` (Ollama by default, Gemini CLI
fallback). See ``llm_backend.py`` and the plugin README for configuration.
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import llm_backend

# --- Configuration ---

SCRIPT_DIR = Path(__file__).resolve().parent
# Plugin root: ``${CLAUDE_PLUGIN_ROOT}`` at runtime, else the dir above scripts/.
PLUGIN_ROOT = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", SCRIPT_DIR.parent)).resolve()
# ``plugins/`` dir of the marketplace (sibling-plugin lookups work in-repo and
# when the marketplace is installed flat).
PLUGINS_DIR = PLUGIN_ROOT.parent

CACHE_FILE = SCRIPT_DIR / ".skills_cache.json"
CACHE_TTL_SECONDS = 300  # 5 minutes
MAX_TRANSCRIPT_MESSAGES = 10
MAX_CONTENT_LENGTH = 500


def skill_dirs() -> list[Path]:
    """Resolve directories to scan for SKILL.md files.

    Order of precedence:
    1. ``SKILL_CLASSIFIER_SKILL_DIRS`` (os.pathsep-separated) — explicit override.
    2. This plugin's own ``skills/`` and the sibling ``frozen-skills/skills``.
    """
    override = os.environ.get("SKILL_CLASSIFIER_SKILL_DIRS", "").strip()
    if override:
        return [Path(p).expanduser() for p in override.split(os.pathsep) if p.strip()]
    return [
        PLUGIN_ROOT / "skills",
        PLUGINS_DIR / "frozen-skills" / "skills",
    ]


def log(msg: str) -> None:
    """Log to stderr (visible in debug, invisible to hook consumer)."""
    print(f"[frozenSkillz {datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {msg}", file=sys.stderr)


# --- Skill Catalog ---

def scan_skills(dirs: list[Path]) -> list[dict]:
    """Scan directories for SKILL.md files and extract name + description."""
    skills = []
    for base_dir in dirs:
        if not base_dir.exists():
            continue
        for skill_file in base_dir.rglob("SKILL.md"):
            try:
                content = skill_file.read_text(encoding="utf-8")
                name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
                desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
                if name_match:
                    skills.append({
                        "name": name_match.group(1).strip().strip('"'),
                        "description": (
                            desc_match.group(1).strip().strip('"')
                            if desc_match else "No description"
                        ),
                    })
            except Exception as e:
                log(f"Error reading {skill_file}: {e}")
    return skills


def get_skills() -> list[dict]:
    """Return skill catalog, using disk cache with TTL."""
    if CACHE_FILE.exists():
        try:
            data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            cached_at = datetime.fromisoformat(data["timestamp"])
            if datetime.now() - cached_at < timedelta(seconds=CACHE_TTL_SECONDS):
                return data["skills"]
        except Exception:
            pass

    skills = scan_skills(skill_dirs())
    try:
        CACHE_FILE.write_text(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "skills": skills,
        }), encoding="utf-8")
    except Exception as e:
        log(f"Cache write failed: {e}")
    return skills


# --- Transcript Loading ---

def extract_content_text(content) -> str:
    """Extract plain text from message content (string or content-block list)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "tool_use":
                    parts.append(f"[tool: {block.get('name', '?')}]")
                elif block.get("type") == "tool_result":
                    parts.append("[tool result]")
            elif isinstance(block, str):
                parts.append(block)
        return " ".join(parts)
    return str(content)


def load_transcript(transcript_path: str) -> str:
    """Load last N messages from JSONL transcript, formatted for context."""
    if not transcript_path:
        return ""
    p = Path(transcript_path)
    if not p.exists():
        return ""

    try:
        messages = []
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Only process actual conversation messages
            msg = entry.get("message", {})
            role = msg.get("role")
            if role not in ("user", "assistant"):
                continue
            # Skip meta messages
            if entry.get("isMeta"):
                continue

            content_raw = msg.get("content", "")
            text = extract_content_text(content_raw)
            if not text.strip():
                continue

            # Truncate long content
            if len(text) > MAX_CONTENT_LENGTH:
                text = text[:MAX_CONTENT_LENGTH] + "..."

            messages.append(f"{role.upper()}: {text}")

        # Return last N messages
        return "\n".join(messages[-MAX_TRANSCRIPT_MESSAGES:])
    except Exception as e:
        log(f"Transcript load failed: {e}")
        return ""


# --- LLM Backend (Swappable) ---

def classify(prompt: str, context: str, skills: list[dict]) -> list[str]:
    """Classify user intent against skills using the configured LLM backend.

    Backend selection/transport lives in ``llm_backend`` (Ollama by default,
    Gemini CLI fallback). This function owns only the prompt and parsing.

    Returns list of relevant skill names, or empty list.
    """
    skills_text = "\n".join(f"- {s['name']}: {s['description']}" for s in skills)

    classification_prompt = f"""You are a skill routing classifier. Given a conversation and available skills, decide which skills (if any) are relevant to what the user is currently working on.

AVAILABLE SKILLS:
{skills_text}

RECENT CONVERSATION:
{context}

CURRENT USER MESSAGE: "{prompt}"

RULES:
1. Only suggest skills that are CLEARLY relevant (>80% confidence).
2. If a skill is already actively being followed in the conversation, do NOT re-suggest it.
3. If the user is chatting, asking a question, or the task is trivial, suggest nothing.
4. Return ONLY a valid JSON array of skill names. Example: ["systematic-debugging"] or []
5. Never suggest more than 3 skills.
6. Do NOT explain your reasoning. Output ONLY the JSON array."""

    output = llm_backend.complete(classification_prompt)
    return _parse_skill_array(output)


def _parse_skill_array(output: str) -> list[str]:
    """Parse a JSON array of skill-name strings from raw LLM output."""
    if not output:
        return []
    output = output.strip()

    # Direct parse
    try:
        parsed = json.loads(output)
        if isinstance(parsed, list):
            return [s for s in parsed if isinstance(s, str)]
    except json.JSONDecodeError:
        pass

    # Fallback: extract the first JSON array from surrounding text
    match = re.search(r"\[.*?\]", output, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, list):
                return [s for s in parsed if isinstance(s, str)]
        except json.JSONDecodeError:
            pass

    return []


# --- Hook Entry Point ---

def main():
    # 1. Read hook payload from stdin
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            return
        payload = json.loads(raw)
    except Exception:
        return

    prompt = payload.get("prompt", "").strip()
    transcript_path = payload.get("transcript_path", "")

    if not prompt:
        return

    # 2. Load skills catalog
    skills = get_skills()
    if not skills:
        log("No skills found")
        return

    # 3. Load conversation context
    context = load_transcript(transcript_path)

    # 4. Classify
    suggested = classify(prompt, context, skills)

    # Validate suggestions against known skill names
    known_names = {s["name"] for s in skills}
    suggested = [s for s in suggested if s in known_names]

    if not suggested:
        return

    # 5. Build output
    skill_mentions = ", ".join(f"`{s}`" for s in suggested)
    hint = (
        f"<user-prompt-submit-hook>\n"
        f"Skill match detected: {skill_mentions}. "
        f"You MUST invoke these using the Skill tool before responding.\n"
        f"</user-prompt-submit-hook>"
    )

    output = {"additionalContext": hint}
    json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
