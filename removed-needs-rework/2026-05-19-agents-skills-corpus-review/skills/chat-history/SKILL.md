---
name: chat-history
description: Extract and organize AI CLI session history from Codex, Codex CLI, Opencode, Kimi CLI, and other tools into project .chats directory. Use when users want to document their AI assistant sessions, export conversation inputs, or maintain a log of instructions.
user_invocable: true
---

# Chat History Extractor

Extract user inputs from AI CLI session history (Codex, Codex CLI, Opencode, Kimi CLI, Aider, Gemini CLI, Goose) and organize them into a project's `.chats` directory with daily markdown files.

## Supported CLI Tools

| Tool | Format | Location Pattern |
|------|--------|------------------|
| **Codex** | JSONL | `~/.Codex/projects/{encoded-path}/` |
| **Codex CLI** | JSONL | `~/.codex/history.jsonl` + `~/.codex/sessions/YYYY/MM/DD/*.jsonl` |
| **Opencode** | JSON/SQLite | `~/.local/share/opencode/storage/session/` |
| **Kimi CLI** | JSONL | `~/.kimi/sessions/{hash}/{session}/context.jsonl` |
| **Aider** | Markdown | Configurable (default: `~/.aider.chat.history.md`) |
| **Gemini CLI** | JSON | `~/.gemini/tmp/{hash}/chats/` |
| **Goose** | JSONL | `~/.local/share/goose/sessions/` |

## When to Use This Skill

Use this skill when the user wants to:
- **Extract session history** from AI CLI sessions
- **Document conversations** for future reference
- **Create instruction logs** organized by date
- **Export user inputs** from various AI assistant sessions
- **Maintain a changelog** of AI interactions across tools
- **Consolidate history** from multiple CLI tools into one place

## How It Works

Each AI CLI tool stores session data differently. This skill detects which tools are available, extracts user messages from each, and consolidates them into unified `.chats/{YYYYMMDD}.md` files organized by date.

### Tool-Specific Formats

#### Codex
- **Storage**: `~/.Codex/projects/{project-path-encoded}/`
- **Files**: `.jsonl` files with UUID names
- **User detection**: `.type == "user"` AND `.userType == "external"`
- **Content field**: `.message.content`

#### Codex CLI
- **Storage**: `~/.codex/history.jsonl` + `~/.codex/sessions/YYYY/MM/DD/`
- **Files**: `rollout-{timestamp}-{uuid}.jsonl`
- **User detection**: `.type == "event_msg"` AND `.payload.type == "user_message"`
- **Content field**: `.payload.message`

#### Opencode
- **Storage**: `~/.local/share/opencode/storage/session/`
- **Files**: Session JSON + message JSON files
- **User detection**: `.role == "user"`
- **Content field**: `.content`
- **Note**: Recent versions use SQLite (`opencode.db`)

#### Kimi CLI
- **Storage**: `~/.kimi/sessions/{work_dir_hash}/{session_id}/`
- **Files**: `context.jsonl`
- **User detection**: `.role == "user"`
- **Content field**: `.content` (string or array of parts)

#### Aider
- **Storage**: Configurable (default `~/.aider.chat.history.md`)
- **Files**: Markdown files
- **Format**: Simple text log

#### Gemini CLI
- **Storage**: `~/.gemini/tmp/{project_hash}/chats/`
- **Files**: JSON files
- **Retention**: Configurable (default 30 days)

#### Goose
- **Storage**: `~/.local/share/goose/sessions/`
- **Files**: `{timestamp}.jsonl`
- **Includes**: Metadata (tokens, model, working dir)

## Instructions

### Step 1: Detect Available CLI Tools

Check which AI CLI tools have session data available:

```bash
# Check for each tool's session directory
echo "Checking for AI CLI session data..."

# Codex
if [ -d "$HOME/.Codex/projects" ]; then
    echo "✓ Codex: Found"
fi

# Codex CLI
if [ -d "$HOME/.codex" ]; then
    echo "✓ Codex CLI: Found"
fi

# Opencode
if [ -d "$HOME/.local/share/opencode/storage" ]; then
    echo "✓ Opencode: Found"
fi

# Kimi CLI
if [ -d "$HOME/.kimi/sessions" ]; then
    echo "✓ Kimi CLI: Found"
fi

# Aider
if [ -f "$HOME/.aider.chat.history.md" ]; then
    echo "✓ Aider: Found"
fi

# Gemini CLI
if [ -d "$HOME/.gemini" ]; then
    echo "✓ Gemini CLI: Found"
fi

# Goose
if [ -d "$HOME/.local/share/goose/sessions" ]; then
    echo "✓ Goose: Found"
fi
```

### Step 2: Identify Project-Specific Sessions

For project-scoped tools (Codex, Opencode, Kimi, Gemini), compute the project identifier:

**Codex path encoding**:
```bash
# Example: /Users/tchen/projects/tubi/titc
# Becomes: -Users-tchen-projects-tubi-titc
PROJECT_PATH=$(pwd | sed 's|/|-|g' | sed 's|^|/|' | sed 's|^/|-|')
CLAUDE_DIR="$HOME/.Codex/projects/$PROJECT_PATH"
```

**Opencode project hash**:
```bash
# Project hash from git repo path or global storage
# Located at: ~/.local/share/opencode/storage/session/{projectHash}/
```

**Kimi CLI work directory hash**:
```bash
# MD5 hash of the absolute project path
WORK_DIR_HASH=$(echo -n "$(pwd)" | md5sum | cut -d' ' -f1)
KIMI_DIR="$HOME/.kimi/sessions/$WORK_DIR_HASH"
```

**Gemini CLI project hash**:
```bash
# Hash of the absolute project path
GEMINI_DIR="$HOME/.gemini/tmp/{hash}/chats"
```

### Step 3: Extract User Inputs by Tool

#### Codex

```bash
cat {session-file}.jsonl | jq -r '
  select(.type == "user" and .userType == "external" and (.isMeta | not)) |
  .message.content |
  if type == "string" then . else empty end
' | grep -v "^Caveat:" \
  | grep -v "^<command" \
  | grep -v "^<local-command" \
  | grep -v "^This session is being continued" \
  | grep -v "^<user-prompt-submit-hook>" \
  | grep -v "^Analysis:" \
  | grep -v "^$"
```

#### Codex CLI

```bash
# From history.jsonl
cat ~/.codex/history.jsonl | jq -r '.text // empty'

# From session files
cat {session-file}.jsonl | jq -r '
  select(.type == "event_msg" and .payload.type == "user_message") |
  .payload.message
' | grep -v "^$"
```

#### Opencode

```bash
# From session directory
for msg_file in ~/.local/share/opencode/storage/message/{sessionID}/msg_*.json; do
    jq -r 'select(.role == "user") | .content' "$msg_file"
done

# Or use opencode export
opencode export {sessionID} --format json | jq -r '.messages[] | select(.role == "user") | .content'
```

#### Kimi CLI

```bash
cat {session_dir}/context.jsonl | jq -r '
  select(.role == "user") |
  .content |
  if type == "string" then . else
    [.[] | select(.type == "text") | .text] | join("")
  end
'
```

#### Aider

```bash
# Extract user messages from markdown history
cat ~/.aider.chat.history.md | grep "^####" | sed 's/^#### //'
```

#### Gemini CLI

```bash
# Extract from JSON files
for chat_file in ~/.gemini/tmp/{hash}/chats/*.json; do
    jq -r '.messages[] | select(.role == "user") | .content' "$chat_file"
done
```

#### Goose

```bash
cat ~/.local/share/goose/sessions/{session}.jsonl | jq -r '
  select(.role == "user") | .content
'
```

### Step 4: Create/Update .chats Files

Create markdown files in `.chats/` directory with format:

```markdown
# Instructions

## {source}: {task title}

{user instruction}

## {source}: {another task title}

{another user instruction}
```

Include source indicator (e.g., `Codex:`, `codex:`, `opencode:`) to identify which CLI tool the instruction came from.

### Step 5: Commit Changes

```bash
git add .chats/*.md
git commit -m "docs(chats): add session history for {date range}"
```

## File Format

Each `.chats/{YYYYMMDD}.md` file should:
- Start with `# Instructions` header
- Use `##` for each major task/instruction
- Include source prefix (e.g., `Codex:`, `codex:`) to identify the CLI tool
- Include the actual user input text
- Group related instructions under the same heading
- Preserve code blocks and formatting

## Example Output

`.chats/20251225.md`:
```markdown
# Instructions

## Codex: implement feature X

based on @specs/feature-x.md implement all phases entirely

commit the code and test

## codex: refactor auth module

refactor the authentication module to use JWT tokens

## opencode: fix bug Y

investigate why component Z is not working

use sub agents to analyze the issue in parallel
```

## Filtering Rules

**Include:**
- Direct user instructions and requests
- Questions about the codebase
- Task specifications and requirements

**Exclude (all tools):**
- System commands (`<command-name>`, `<local-command-stdout>`)
- Session continuation messages
- Tool results and agent responses
- Hook notifications (`<user-prompt-submit-hook>`)
- Empty lines and caveat messages
- Assistant/model responses

## Tool-Specific Exclusions

### Codex
- Lines starting with: `Caveat:`, `<command`, `<local-command`, `This session is being continued`, `<user-prompt-submit-hook>`, `Analysis:`

### Codex CLI
- Empty lines after jq extraction
- Tool output blocks

### Opencode
- System messages (`.role == "system"`)
- Tool call results (`.role == "tool"`)

### Kimi CLI
- Internal metadata: `_system_prompt`, `_usage`, `_checkpoint`
- Tool messages: `.role == "tool"`
- System messages: `.role == "system"`

### Aider
- Assistant responses (marked differently in markdown)
- File content blocks

## Workflow Summary

1. Detect which AI CLI tools have session data available
2. For project-scoped tools, compute the project identifier (path encoding/hash)
3. For each tool with data:
   - Find session files for the target date(s)
   - Extract user inputs using tool-specific jq/python filters
   - Apply tool-specific filtering rules
4. Consolidate all extracted inputs by date
5. Create `.chats/{YYYYMMDD}.md` with source prefixes
6. Create `.chats/` directory if it doesn't exist
7. Optionally commit the changes

## Advanced: Unified Python Script

For complex extraction, use this Python template:

```python
#!/usr/bin/env python3
"""
Unified AI CLI Session Extractor
Extracts user messages from multiple AI CLI tools.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Iterator, Dict, Any

class ClaudeCodeExtractor:
    """Extract user messages from Codex sessions."""
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.home() / ".Codex" / "projects"
    
    def get_project_dir(self, cwd: str) -> Path:
        """Compute encoded project path."""
        encoded = cwd.replace("/", "-").replace("\\", "-")
        if not encoded.startswith("-"):
            encoded = "-" + encoded
        return self.base_dir / encoded
    
    def extract_messages(self, session_file: Path) -> Iterator[Dict[str, Any]]:
        """Extract user messages from a session file."""
        with open(session_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    msg = json.loads(line)
                    if (msg.get("type") == "user" and 
                        msg.get("userType") == "external" and
                        not msg.get("isMeta", False)):
                        content = msg.get("message", {}).get("content")
                        if isinstance(content, str):
                            yield {
                                "tool": "Codex",
                                "timestamp": msg.get("timestamp"),
                                "content": content
                            }
                except json.JSONDecodeError:
                    continue

class CodexCLIExtractor:
    """Extract user messages from Codex CLI sessions."""
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.home() / ".codex"
    
    def extract_from_history(self) -> Iterator[Dict[str, Any]]:
        """Extract from history.jsonl."""
        history_file = self.base_dir / "history.jsonl"
        if not history_file.exists():
            return
        
        with open(history_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if text := entry.get("text"):
                        yield {
                            "tool": "codex",
                            "timestamp": entry.get("timestamp"),
                            "content": text
                        }
                except json.JSONDecodeError:
                    continue
    
    def extract_from_session(self, session_file: Path) -> Iterator[Dict[str, Any]]:
        """Extract from a session file."""
        with open(session_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    msg = json.loads(line)
                    if (msg.get("type") == "event_msg" and
                        msg.get("payload", {}).get("type") == "user_message"):
                        content = msg["payload"].get("message")
                        if content:
                            yield {
                                "tool": "codex",
                                "timestamp": msg.get("timestamp"),
                                "content": content
                            }
                except json.JSONDecodeError:
                    continue

class KimiCLIExtractor:
    """Extract user messages from Kimi CLI sessions."""
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.home() / ".kimi" / "sessions"
    
    def get_project_dir(self, cwd: str) -> Path:
        """Compute work directory hash."""
        import hashlib
        work_hash = hashlib.md5(cwd.encode()).hexdigest()
        return self.base_dir / work_hash
    
    def extract_messages(self, context_file: Path) -> Iterator[Dict[str, Any]]:
        """Extract user messages from context.jsonl."""
        with open(context_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    msg = json.loads(line)
                    if msg.get("role") == "user":
                        content = msg.get("content", "")
                        # Handle both string and array content
                        if isinstance(content, list):
                            text_parts = [
                                part.get("text", "") 
                                for part in content 
                                if part.get("type") == "text"
                            ]
                            content = "".join(text_parts)
                        
                        if content:
                            yield {
                                "tool": "kimi",
                                "content": content
                            }
                except json.JSONDecodeError:
                    continue

def main():
    """Main extraction function."""
    cwd = os.getcwd()
    
    # Detect and extract from all available tools
    messages = []
    
    # Codex
    Codex = ClaudeCodeExtractor()
    claude_dir = Codex.get_project_dir(cwd)
    if claude_dir.exists():
        for session_file in claude_dir.glob("*.jsonl"):
            if "agent-" not in session_file.name:
                messages.extend(Codex.extract_messages(session_file))
    
    # Codex CLI
    codex = CodexCLIExtractor()
    messages.extend(codex.extract_from_history())
    for session_file in (codex.base_dir / "sessions").rglob("rollout-*.jsonl"):
        messages.extend(codex.extract_from_session(session_file))
    
    # Kimi CLI
    kimi = KimiCLIExtractor()
    kimi_dir = kimi.get_project_dir(cwd)
    if kimi_dir.exists():
        for session_dir in kimi_dir.iterdir():
            context_file = session_dir / "context.jsonl"
            if context_file.exists():
                messages.extend(kimi.extract_messages(context_file))
    
    # Sort by timestamp if available
    messages.sort(key=lambda x: x.get("timestamp", ""))
    
    # Output
    for msg in messages:
        print(f"[{msg['tool']}] {msg['content'][:100]}...")

if __name__ == "__main__":
    main()
```

## Helper Commands

### Find sessions for current project

```bash
#!/bin/bash
# find-sessions.sh - Find AI CLI sessions for current directory

CWD=$(pwd)
echo "Finding sessions for: $CWD"
echo ""

# Codex
CLAUDE_ENCODED=$(echo "$CWD" | sed 's|/|-|g' | sed 's|^|/|' | sed 's|^/|-|')
CLAUDE_DIR="$HOME/.Codex/projects/$CLAUDE_ENCODED"
if [ -d "$CLAUDE_DIR" ]; then
    echo "Codex: $CLAUDE_DIR"
    ls -la "$CLAUDE_DIR"/*.jsonl 2>/dev/null | grep -v agent- | wc -l | xargs echo "  Sessions:"
fi

# Kimi CLI (requires md5)
if command -v md5sum &> /dev/null; then
    KIMI_HASH=$(echo -n "$CWD" | md5sum | cut -d' ' -f1)
    KIMI_DIR="$HOME/.kimi/sessions/$KIMI_HASH"
    if [ -d "$KIMI_DIR" ]; then
        echo "Kimi CLI: $KIMI_DIR"
        echo "  Sessions: $(ls -1 "$KIMI_DIR" | wc -l)"
    fi
fi

# Opencode
if [ -d "$HOME/.local/share/opencode/storage/session" ]; then
    echo "Opencode: ~/.local/share/opencode/storage/session/"
    # Project hash requires git
    if [ -d ".git" ]; then
        echo "  (In git repo - check for project-specific hash)"
    fi
fi

echo ""
echo "Global tools (not project-scoped):"

# Codex CLI
if [ -d "$HOME/.codex" ]; then
    echo "  Codex CLI: ~/.codex/"
fi

# Aider
if [ -f "$HOME/.aider.chat.history.md" ]; then
    echo "  Aider: ~/.aider.chat.history.md"
fi

# Goose
if [ -d "$HOME/.local/share/goose/sessions" ]; then
    echo "  Goose: ~/.local/share/goose/sessions/"
fi
```

## Notes

- **Session files named `agent-*.jsonl`** (Codex) or with `parentID` (Opencode) are sub-agent sessions and typically don't contain direct user input
- **Main session files** have UUID-style names (e.g., `01e78099-de0e-4424-845c-518638c8241e.jsonl`)
- **Opencode recent versions** store messages in SQLite (`~/.local/share/opencode/opencode.db`) - use `opencode export` command instead
- **Kimi CLI** uses MD5 hash of absolute path - moving projects breaks the link
- **Gemini CLI** sessions auto-expire (default 30 days)
- **Aider** history file is global by default but configurable per-project
- **Goose** sessions are global but include working directory metadata

## References

- [ai-hist](https://github.com/khaliqgant/ai-hist) - Existing tool that syncs Codex and Codex CLI history to SQLite
- [Codex](https://Codex.ai/code) - Anthropic's AI coding assistant
- [Codex CLI](https://github.com/openai/codex) - OpenAI's CLI coding agent
- [Opencode](https://opencode.ai) - Open-source AI coding assistant
- [Kimi CLI](https://github.com/MoonshotAI/kimi-cli) - Moonshot AI's CLI agent
- [Aider](https://aider.chat) - AI pair programming tool
- [Gemini CLI](https://geminicli.com) - Google's AI CLI tool
- [Goose](https://block.github.io/goose) - Block's AI agent framework
