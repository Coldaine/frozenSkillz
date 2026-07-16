#!/usr/bin/env python3
"""
Unified AI CLI Session Extractor
Extracts user messages from Claude Code, Codex CLI, Opencode, Kimi CLI, and other AI CLI tools.

Usage:
    python extract_chat_history.py [--date YYYYMMDD] [--output-dir .chats] [--tool claude,codex,kimi]

Supported tools:
    - claude:   Claude Code (JSONL at ~/.claude/projects/)
    - codex:    Codex CLI (JSONL at ~/.codex/)
    - opencode: Opencode (JSON/SQLite at ~/.local/share/opencode/)
    - kimi:     Kimi CLI (JSONL at ~/.kimi/sessions/)
    - aider:    Aider (Markdown at ~/.aider.chat.history.md)
    - goose:    Goose (JSONL at ~/.local/share/goose/sessions/)

Gemini and Antigravity are intentionally handled by the deterministic inventory's
coverage/probe layer until their live schemas are verified; this legacy message
extractor does not claim support for them.
"""

import json
import os
import re
import sys
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Iterator, Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ChatMessage:
    """Represents a single user message from any CLI tool."""

    tool: str
    content: str
    timestamp: Optional[str] = None
    session_id: Optional[str] = None

    def __str__(self) -> str:
        ts = f" [{self.timestamp}]" if self.timestamp else ""
        return f"[{self.tool}{ts}] {self.content[:100]}..."


class ClaudeCodeExtractor:
    """Extract user messages from Claude Code sessions."""

    TOOL_NAME = "claude"
    EXCLUSION_PATTERNS = [
        r"^Caveat:",
        r"^<command",
        r"^<local-command",
        r"^This session is being continued",
        r"^<user-prompt-submit-hook>",
        r"^Analysis:",
        r"^\s*$",
    ]

    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or Path.home() / ".claude" / "projects"

    def is_available(self) -> bool:
        """Check if Claude Code session data exists."""
        return self.base_dir.exists()

    def encode_project_path(self, cwd: str) -> str:
        """Compute encoded project path for Claude Code.

        Claude Code replaces path separators with '-' and prefixes with '-'.
        Example: /Users/tchen/projects/foo -> -Users-tchen-projects-foo
        """
        # Normalize path separators
        encoded = cwd.replace("/", "-").replace("\\", "-")
        # Remove drive letter colon on Windows (D: -> D)
        encoded = re.sub(r"^([A-Za-z]):", r"\1", encoded)
        # Prefix with -
        if not encoded.startswith("-"):
            encoded = "-" + encoded
        return encoded

    def get_project_dir(self, cwd: str) -> Optional[Path]:
        """Get the project-specific session directory."""
        encoded = self.encode_project_path(cwd)
        project_dir = self.base_dir / encoded
        return project_dir if project_dir.exists() else None

    def get_all_project_dirs(self) -> Iterator[Path]:
        """Get all project directories."""
        if self.base_dir.exists():
            for item in self.base_dir.iterdir():
                if item.is_dir():
                    yield item

    def extract_from_session(self, session_file: Path) -> Iterator[ChatMessage]:
        """Extract user messages from a single session file."""
        with open(session_file, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    # Check if this is a user message
                    if (
                        msg.get("type") == "user"
                        and msg.get("userType") == "external"
                        and not msg.get("isMeta", False)
                    ):
                        content = msg.get("message", {}).get("content")
                        if isinstance(content, str):
                            # Apply exclusion filters
                            if not any(
                                re.match(pattern, content)
                                for pattern in self.EXCLUSION_PATTERNS
                            ):
                                yield ChatMessage(
                                    tool=self.TOOL_NAME,
                                    content=content,
                                    timestamp=msg.get("timestamp"),
                                    session_id=session_file.stem,
                                )
                except (json.JSONDecodeError, KeyError):
                    continue

    def extract_for_project(self, cwd: str) -> Iterator[ChatMessage]:
        """Extract all user messages for a specific project."""
        project_dir = self.get_project_dir(cwd)
        if not project_dir:
            return

        for session_file in project_dir.glob("*.jsonl"):
            # Skip agent sessions
            if "agent-" in session_file.name:
                continue
            yield from self.extract_from_session(session_file)

    def extract_all(self) -> Iterator[ChatMessage]:
        """Extract all user messages from all projects."""
        for project_dir in self.get_all_project_dirs():
            for session_file in project_dir.glob("*.jsonl"):
                if "agent-" not in session_file.name:
                    yield from self.extract_from_session(session_file)


class CodexCLIExtractor:
    """Extract user messages from Codex CLI sessions."""

    TOOL_NAME = "codex"

    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or Path.home() / ".codex"

    def is_available(self) -> bool:
        """Check if Codex CLI session data exists."""
        return self.base_dir.exists()

    def extract_from_history(self) -> Iterator[ChatMessage]:
        """Extract from ~/.codex/history.jsonl."""
        history_file = self.base_dir / "history.jsonl"
        if not history_file.exists():
            return

        with open(history_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if text := entry.get("text"):
                        text = text.strip()
                        if text:
                            yield ChatMessage(
                                tool=self.TOOL_NAME,
                                content=text,
                                timestamp=entry.get("timestamp"),
                                session_id="history",
                            )
                except (json.JSONDecodeError, AttributeError):
                    continue

    def extract_from_session(self, session_file: Path) -> Iterator[ChatMessage]:
        """Extract from a rollout session file."""
        with open(session_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    if (
                        msg.get("type") == "event_msg"
                        and msg.get("payload", {}).get("type") == "user_message"
                    ):
                        content = msg["payload"].get("message", "").strip()
                        if content:
                            yield ChatMessage(
                                tool=self.TOOL_NAME,
                                content=content,
                                timestamp=msg.get("timestamp"),
                                session_id=session_file.stem,
                            )
                except (json.JSONDecodeError, KeyError, AttributeError):
                    continue

    def extract_all(self) -> Iterator[ChatMessage]:
        """Extract from both history and all session files."""
        # From history.jsonl
        yield from self.extract_from_history()

        # From session files
        sessions_dir = self.base_dir / "sessions"
        if sessions_dir.exists():
            for session_file in sessions_dir.rglob("rollout-*.jsonl"):
                yield from self.extract_from_session(session_file)


class KimiCLIExtractor:
    """Extract user messages from Kimi CLI sessions."""

    TOOL_NAME = "kimi"

    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or Path.home() / ".kimi" / "sessions"

    def is_available(self) -> bool:
        """Check if Kimi CLI session data exists."""
        return self.base_dir.exists()

    def get_work_dir_hash(self, cwd: str) -> str:
        """Compute MD5 hash of the absolute working directory path."""
        return hashlib.md5(cwd.encode("utf-8")).hexdigest()

    def get_project_dir(self, cwd: str) -> Optional[Path]:
        """Get the project-specific session directory."""
        work_hash = self.get_work_dir_hash(cwd)
        project_dir = self.base_dir / work_hash
        return project_dir if project_dir.exists() else None

    def get_all_project_dirs(self) -> Iterator[Path]:
        """Get all project directories."""
        if self.base_dir.exists():
            for item in self.base_dir.iterdir():
                if item.is_dir() and len(item.name) == 32:  # MD5 hash length
                    yield item

    def extract_from_context(self, context_file: Path) -> Iterator[ChatMessage]:
        """Extract user messages from a context.jsonl file."""
        with open(context_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    if msg.get("role") == "user":
                        content = msg.get("content", "")

                        # Handle both string and array content
                        if isinstance(content, list):
                            text_parts = [
                                part.get("text", "")
                                for part in content
                                if isinstance(part, dict) and part.get("type") == "text"
                            ]
                            content = "".join(text_parts)

                        content = content.strip()
                        if content:
                            yield ChatMessage(
                                tool=self.TOOL_NAME,
                                content=content,
                                session_id=context_file.parent.name,
                            )
                except (json.JSONDecodeError, AttributeError):
                    continue

    def extract_for_project(self, cwd: str) -> Iterator[ChatMessage]:
        """Extract all user messages for a specific project."""
        project_dir = self.get_project_dir(cwd)
        if not project_dir:
            return

        for session_dir in project_dir.iterdir():
            if session_dir.is_dir():
                context_file = session_dir / "context.jsonl"
                if context_file.exists():
                    yield from self.extract_from_context(context_file)

    def extract_all(self) -> Iterator[ChatMessage]:
        """Extract all user messages from all projects."""
        for project_dir in self.get_all_project_dirs():
            for session_dir in project_dir.iterdir():
                if session_dir.is_dir():
                    context_file = session_dir / "context.jsonl"
                    if context_file.exists():
                        yield from self.extract_from_context(context_file)


class OpencodeExtractor:
    """Extract user messages from Opencode sessions."""

    TOOL_NAME = "opencode"

    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or Path.home() / ".local" / "share" / "opencode"

    def is_available(self) -> bool:
        """Check if Opencode session data exists."""
        session_dir = self.base_dir / "storage" / "session"
        return session_dir.exists()

    def get_session_dirs(self) -> Iterator[Path]:
        """Get all session directories."""
        session_base = self.base_dir / "storage" / "session"
        if session_base.exists():
            for project_dir in session_base.iterdir():
                if project_dir.is_dir():
                    for session_file in project_dir.glob("ses_*.json"):
                        yield session_file

    def get_messages_dir(self, session_id: str) -> Optional[Path]:
        """Get the messages directory for a session."""
        msg_dir = self.base_dir / "storage" / "message" / session_id
        return msg_dir if msg_dir.exists() else None

    def extract_from_session(self, session_file: Path) -> Iterator[ChatMessage]:
        """Extract user messages from a session and its message files."""
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)

            session_id = session_data.get("id")
            if not session_id:
                return

            # Get messages from individual message files
            msg_dir = self.get_messages_dir(session_id)
            if msg_dir and msg_dir.exists():
                for msg_file in sorted(msg_dir.glob("msg_*.json")):
                    try:
                        with open(msg_file, "r", encoding="utf-8") as f:
                            msg = json.load(f)

                        if msg.get("role") == "user":
                            content = msg.get("content", "")
                            if isinstance(content, str) and content.strip():
                                yield ChatMessage(
                                    tool=self.TOOL_NAME,
                                    content=content.strip(),
                                    timestamp=msg.get("createdAt"),
                                    session_id=session_id,
                                )
                    except (json.JSONDecodeError, IOError):
                        continue

        except (json.JSONDecodeError, IOError):
            pass

    def extract_all(self) -> Iterator[ChatMessage]:
        """Extract all user messages from all sessions."""
        for session_file in self.get_session_dirs():
            yield from self.extract_from_session(session_file)


class AiderExtractor:
    """Extract user messages from Aider chat history."""

    TOOL_NAME = "aider"

    def __init__(self, history_file: Path | None = None):
        self.history_file = history_file or Path.home() / ".aider.chat.history.md"

    def is_available(self) -> bool:
        """Check if Aider history file exists."""
        return self.history_file.exists()

    def extract_all(self) -> Iterator[ChatMessage]:
        """Extract user messages from markdown history."""
        with open(self.history_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Aider uses #### headers for messages
        # User messages typically follow the pattern
        lines = content.split("\n")
        for i, line in enumerate(lines):
            line = line.strip()
            # Look for user message headers
            if line.startswith("####") and "user" in line.lower():
                # Next lines until next header are the message
                message_lines = []
                for j in range(i + 1, len(lines)):
                    next_line = lines[j]
                    if next_line.startswith("#"):
                        break
                    message_lines.append(next_line)

                message = "\n".join(message_lines).strip()
                if message:
                    yield ChatMessage(tool=self.TOOL_NAME, content=message)


class GooseExtractor:
    """Extract user messages from Goose sessions."""

    TOOL_NAME = "goose"

    def __init__(self, base_dir: Path = None):
        self.base_dir = (
            base_dir or Path.home() / ".local" / "share" / "goose" / "sessions"
        )

    def is_available(self) -> bool:
        """Check if Goose session data exists."""
        return self.base_dir.exists()

    def extract_from_session(self, session_file: Path) -> Iterator[ChatMessage]:
        """Extract user messages from a session file."""
        with open(session_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    if msg.get("role") == "user":
                        content = msg.get("content", [])

                        # Handle array of content parts
                        if isinstance(content, list):
                            text_parts = []
                            for part in content:
                                if isinstance(part, dict):
                                    if part.get("type") == "text":
                                        text_parts.append(part.get("text", ""))
                                    elif "text" in part:
                                        text_parts.append(part["text"])
                            content = "".join(text_parts)

                        content = str(content).strip()
                        if content:
                            yield ChatMessage(
                                tool=self.TOOL_NAME,
                                content=content,
                                timestamp=msg.get("created"),
                                session_id=session_file.stem,
                            )
                except (json.JSONDecodeError, AttributeError):
                    continue

    def extract_all(self) -> Iterator[ChatMessage]:
        """Extract all user messages from all sessions."""
        if self.base_dir.exists():
            for session_file in self.base_dir.glob("*.jsonl"):
                yield from self.extract_from_session(session_file)


class ChatHistoryExtractor:
    """Main class that orchestrates extraction from all available tools."""

    EXTRACTORS = [
        ClaudeCodeExtractor,
        CodexCLIExtractor,
        KimiCLIExtractor,
        OpencodeExtractor,
        AiderExtractor,
        GooseExtractor,
    ]

    def __init__(self, cwd: str = None, selected_tools: List[str] = None):
        self.cwd = cwd or os.getcwd()
        self.selected_tools = selected_tools
        self.extractors: List[Any] = []

        # Initialize available extractors
        for extractor_class in self.EXTRACTORS:
            try:
                extractor = extractor_class()
                if extractor.is_available():
                    if not selected_tools or extractor.TOOL_NAME in selected_tools:
                        self.extractors.append(extractor)
            except Exception:
                continue

    def detect_tools(self) -> List[str]:
        """Detect which tools have session data available."""
        return [ex.TOOL_NAME for ex in self.extractors]

    def extract_all(self, project_scoped_only: bool = False) -> Iterator[ChatMessage]:
        """Extract messages from all available tools."""
        for extractor in self.extractors:
            try:
                if project_scoped_only and hasattr(extractor, "extract_for_project"):
                    yield from extractor.extract_for_project(self.cwd)
                else:
                    yield from extractor.extract_all()
            except Exception as e:
                print(
                    f"Warning: Failed to extract from {extractor.TOOL_NAME}: {e}",
                    file=sys.stderr,
                )

    def extract_for_project(self) -> Iterator[ChatMessage]:
        """Extract messages for the current project only."""
        for extractor in self.extractors:
            try:
                if hasattr(extractor, "extract_for_project"):
                    yield from extractor.extract_for_project(self.cwd)
                elif hasattr(extractor, "extract_all"):
                    # Global tools - include all messages
                    yield from extractor.extract_all()
            except Exception as e:
                print(
                    f"Warning: Failed to extract from {extractor.TOOL_NAME}: {e}",
                    file=sys.stderr,
                )

    def export_to_markdown(self, output_dir: Path, group_by_date: bool = True) -> None:
        """Export extracted messages to markdown files."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Collect all messages
        messages = list(self.extract_for_project())

        if not messages:
            print("No messages found.")
            return

        # Sort by timestamp if available
        messages.sort(key=lambda m: m.timestamp or "")

        if group_by_date:
            # Group by date
            by_date: Dict[str, List[ChatMessage]] = {}
            for msg in messages:
                date_key = "unknown"
                if msg.timestamp:
                    try:
                        # Try to parse various timestamp formats
                        if "T" in msg.timestamp:
                            date_key = msg.timestamp.split("T")[0].replace("-", "")
                        elif " " in msg.timestamp:
                            date_key = msg.timestamp.split(" ")[0].replace("-", "")
                    except:
                        pass

                by_date.setdefault(date_key, []).append(msg)

            # Write files by date
            for date_key, msgs in sorted(by_date.items()):
                if date_key == "unknown":
                    filename = "unknown_date.md"
                else:
                    filename = f"{date_key}.md"

                filepath = output_dir / filename
                self._write_markdown_file(filepath, msgs, date_key)
        else:
            # Single file
            filepath = output_dir / "chat_history.md"
            self._write_markdown_file(filepath, messages, "all")

    def _write_markdown_file(
        self, filepath: Path, messages: List[ChatMessage], date_label: str
    ) -> None:
        """Write messages to a markdown file."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# Instructions\n\n")

            for i, msg in enumerate(messages):
                # Create a brief title from first line
                title = msg.content.split("\n")[0][:50]
                if len(title) == 50:
                    title += "..."

                f.write(f"## {msg.tool}: {title}\n\n")
                f.write(f"{msg.content}\n\n")

                # Add separator between messages (except last)
                if i < len(messages) - 1:
                    f.write("---\n\n")

        print(f"Wrote {len(messages)} messages to {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract user messages from AI CLI session history"
    )
    parser.add_argument("--date", help="Filter by date (YYYYMMDD)")
    parser.add_argument(
        "--output-dir",
        default=".chats",
        help="Output directory for markdown files (default: .chats)",
    )
    parser.add_argument(
        "--tool",
        help="Comma-separated list of tools to extract from (claude,codex,kimi,opencode,aider,goose)",
    )
    parser.add_argument(
        "--detect",
        action="store_true",
        help="Only detect which tools have session data",
    )
    parser.add_argument(
        "--project-only",
        action="store_true",
        help="Only extract project-scoped sessions (for tools that support it)",
    )
    parser.add_argument(
        "--cwd",
        default=os.getcwd(),
        help="Current working directory (for project-scoped extraction)",
    )

    args = parser.parse_args()

    # Parse tool selection
    selected_tools = None
    if args.tool:
        selected_tools = [t.strip() for t in args.tool.split(",")]

    # Initialize extractor
    extractor = ChatHistoryExtractor(cwd=args.cwd, selected_tools=selected_tools)

    # Detect mode
    if args.detect:
        available = extractor.detect_tools()
        if available:
            print("Available tools with session data:")
            for tool in available:
                print(f"  - {tool}")
        else:
            print("No AI CLI session data found.")
        return

    # Export to markdown
    extractor.export_to_markdown(output_dir=Path(args.output_dir), group_by_date=True)


if __name__ == "__main__":
    main()
