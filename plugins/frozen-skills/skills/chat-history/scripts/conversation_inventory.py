#!/usr/bin/env python3
"""Read-only, deterministic inventory of local AI conversation records."""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


class SessionRecord:
    def __init__(
        self,
        *,
        tool: str,
        native_id: str,
        kind: str,
        started_at: datetime,
        last_activity: datetime,
        parent_id: str | None = None,
        terminal_at: datetime | None = None,
        title: str = "",
        workspace: str = "",
        source_files: Sequence[str] | None = None,
        evidence: Sequence[str] | None = None,
        user_prompts: Sequence[tuple[datetime, str]] | None = None,
    ) -> None:
        self.tool = tool
        self.native_id = native_id
        self.kind = kind
        self.started_at = started_at
        self.last_activity = last_activity
        self.parent_id = parent_id
        self.terminal_at = terminal_at
        self.title = title
        self.workspace = workspace
        self.source_files = list(source_files or [])
        self.evidence = list(evidence or [])
        self.user_prompts = list(user_prompts or [])


def parse_timestamp(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, (int, float)):
        scale = 1000 if value > 10_000_000_000 else 1
        return datetime.fromtimestamp(value / scale, tz=timezone.utc)
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    item = json.loads(line)
                except (json.JSONDecodeError, UnicodeError):
                    continue
                if isinstance(item, dict):
                    yield item
    except (OSError, PermissionError):
        return


def text_content(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                candidate = item.get("text") or item.get("input_text") or item.get("content")
                if isinstance(candidate, str):
                    parts.append(candidate)
        return " ".join(parts).strip()
    if isinstance(value, dict):
        return text_content(value.get("content") or value.get("text") or "")
    return ""


def clean_title(text: str, limit: int = 100) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    command_args = re.search(r"<command-args>(.*?)</command-args>", text, flags=re.IGNORECASE)
    if command_args and command_args.group(1).strip():
        text = command_args.group(1).strip()
    elif text.startswith("<") and ">" in text:
        return ""
    lowered = text.lower()
    if lowered.startswith(("# agents.md instructions", "<recommended_plugins", "<environment_context")):
        return ""
    if text.startswith(("{", "[")) and len(text) > 200:
        return ""
    return text[:limit]


def is_human_claude_user(item: dict[str, Any]) -> bool:
    if item.get("type") != "user" or item.get("isMeta") or item.get("toolUseResult") is not None:
        return False
    message = item.get("message") if isinstance(item.get("message"), dict) else {}
    content = message.get("content")
    if isinstance(content, list) and any(isinstance(part, dict) and part.get("type") == "tool_result" for part in content):
        return False
    return True


def parse_codex_file(path: Path) -> SessionRecord | None:
    native_id = path.stem
    parent_id = None
    workspace = ""
    kind = "conversation"
    title = ""
    event_title = ""
    timestamps: list[datetime] = []
    terminal_at = None
    evidence: list[str] = []
    user_prompts: list[tuple[datetime, str]] = []

    for item in iter_jsonl(path):
        timestamp = parse_timestamp(item.get("timestamp"))
        if timestamp:
            timestamps.append(timestamp)
        record_type = item.get("type")
        payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
        if record_type == "session_meta":
            native_id = str(payload.get("id") or payload.get("session_id") or native_id)
            raw_parent_id = payload.get("parent_thread_id") or payload.get("forked_from_id")
            workspace = str(payload.get("cwd") or "")
            source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
            is_subagent = payload.get("thread_source") == "subagent" or isinstance(source.get("subagent"), dict)
            if is_subagent:
                parent_id = raw_parent_id
                kind = "subagent"
        elif record_type == "event_msg":
            event_type = payload.get("type")
            if event_type in {"task_complete", "turn_complete", "thread_complete"} and timestamp:
                terminal_at = timestamp
                evidence.append(str(event_type))
            if not event_title and event_type == "user_message":
                event_title = clean_title(text_content(payload.get("message")))
            if event_type == "user_message" and timestamp:
                prompt = clean_title(text_content(payload.get("message")), limit=240)
                if prompt:
                    user_prompts.append((timestamp, prompt))
        elif record_type == "response_item" and not title:
            if payload.get("type") == "message" and payload.get("role") == "user":
                title = clean_title(text_content(payload.get("content")))
        if record_type == "response_item" and payload.get("type") == "message" and payload.get("role") == "user" and timestamp:
            prompt = clean_title(text_content(payload.get("content")), limit=240)
            if prompt:
                user_prompts.append((timestamp, prompt))

    if not timestamps:
        try:
            modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        except OSError:
            return None
        timestamps = [modified]
    return SessionRecord(
        tool="codex",
        native_id=native_id,
        parent_id=str(parent_id) if parent_id else None,
        kind=kind,
        title=event_title or title,
        workspace=workspace,
        started_at=min(timestamps),
        last_activity=max(timestamps),
        terminal_at=terminal_at,
        source_files=[str(path)],
        evidence=evidence,
        user_prompts=user_prompts,
    )


def parse_codex_files(paths: Iterable[Path]) -> list[SessionRecord]:
    return [record for path in paths if (record := parse_codex_file(Path(path))) is not None]


def parse_claude_file(path: Path) -> SessionRecord | None:
    is_child = "subagents" in {part.lower() for part in path.parts}
    native_id = path.stem
    parent_id = None
    workspace = ""
    title = ""
    timestamps: list[datetime] = []
    terminal_at = None
    evidence: list[str] = []
    user_prompts: list[tuple[datetime, str]] = []

    for item in iter_jsonl(path):
        timestamp = parse_timestamp(item.get("timestamp"))
        if timestamp:
            timestamps.append(timestamp)
        session_id = item.get("sessionId") or item.get("session_id")
        if is_child:
            parent_id = str(session_id or parent_id or "") or None
            native_id = str(item.get("agentId") or item.get("agent_id") or native_id)
        elif session_id:
            native_id = str(session_id)
        workspace = str(item.get("cwd") or workspace)
        if is_human_claude_user(item) and not title:
            title = clean_title(text_content(item.get("message")))
        if is_human_claude_user(item) and timestamp:
            prompt = clean_title(text_content(item.get("message")), limit=240)
            if prompt:
                user_prompts.append((timestamp, prompt))
        subtype = item.get("subtype")
        if subtype in {"success", "error", "interrupted"} and timestamp:
            terminal_at = timestamp
            evidence.append(str(subtype))

    if not timestamps:
        try:
            modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        except OSError:
            return None
        timestamps = [modified]
    return SessionRecord(
        tool="claude-code",
        native_id=native_id,
        parent_id=parent_id,
        kind="subagent" if is_child else "conversation",
        title=title,
        workspace=workspace,
        started_at=min(timestamps),
        last_activity=max(timestamps),
        terminal_at=terminal_at,
        source_files=[str(path)],
        evidence=evidence,
        user_prompts=user_prompts,
    )


def parse_claude_files(paths: Iterable[Path]) -> list[SessionRecord]:
    return [record for path in paths if (record := parse_claude_file(Path(path))) is not None]


def parse_antigravity_database(path: Path) -> list[SessionRecord]:
    """Probe Antigravity SQLite read-only without assuming one unstable schema."""
    records: list[SessionRecord] = []
    try:
        # mode=ro preserves WAL visibility; immutable=1 can hide the newest live rows.
        uri = path.resolve().as_uri() + "?mode=ro"
        connection = sqlite3.connect(uri, uri=True)
    except (sqlite3.Error, OSError, ValueError):
        return records
    try:
        tables = [row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        candidate = next((name for name in tables if name.lower() in {"conversations", "sessions", "chats"}), None)
        if not candidate:
            modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            records.append(SessionRecord(tool="antigravity", native_id=path.stem, kind="event", started_at=modified, last_activity=modified, source_files=[str(path)], evidence=["sqlite_schema_unrecognized"]))
            return records
        quote = lambda name: '"' + str(name).replace('"', '""') + '"'
        columns = [row[1] for row in connection.execute(f"PRAGMA table_info({quote(candidate)})")]
        id_col = next((c for c in columns if c.lower() in {"id", "session_id", "conversation_id"}), columns[0])
        title_col = next((c for c in columns if c.lower() in {"title", "name", "summary"}), None)
        time_col = next((c for c in columns if c.lower() in {"updated_at", "last_activity", "created_at", "timestamp"}), None)
        selected = [id_col] + ([title_col] if title_col else []) + ([time_col] if time_col else [])
        query = "SELECT " + ", ".join(quote(col) for col in selected) + f" FROM {quote(candidate)}"
        fallback = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        for row in connection.execute(query):
            values = dict(zip(selected, row))
            timestamp = parse_timestamp(values.get(time_col)) if time_col else fallback
            timestamp = timestamp or fallback
            records.append(SessionRecord(tool="antigravity", native_id=str(values[id_col]), kind="conversation", title=clean_title(str(values.get(title_col) or "")), started_at=timestamp, last_activity=timestamp, source_files=[str(path)], evidence=[f"sqlite:{candidate}"]))
    except (sqlite3.Error, OSError):
        pass
    finally:
        connection.close()
    return records


def state_at(record: SessionRecord, cutoff: datetime | None) -> str:
    if cutoff is None:
        return "completed" if record.terminal_at else "active_or_interrupted"
    cutoff = cutoff.astimezone(timezone.utc)
    if record.started_at > cutoff:
        return "not_started"
    if record.terminal_at and record.terminal_at <= cutoff:
        return "completed"
    if (record.terminal_at and record.terminal_at > cutoff) or record.last_activity > cutoff:
        return "active"
    return "active_or_interrupted"


def build_report(records: Sequence[SessionRecord], at: datetime | None = None, window_start: datetime | None = None) -> dict[str, Any]:
    conversations = [record for record in records if record.kind == "conversation"]
    children = [record for record in records if record.kind == "subagent"]
    evidence = [record for record in records if record.kind not in {"conversation", "subagent"}]
    children_by_parent: dict[str, list[SessionRecord]] = {}
    for child in children:
        if child.parent_id:
            children_by_parent.setdefault(child.parent_id, []).append(child)

    rendered = []
    for record in sorted(conversations, key=lambda item: item.last_activity, reverse=True):
        attached = children_by_parent.get(record.native_id, [])
        prompt_cutoff = at.astimezone(timezone.utc) if at else None
        eligible_prompts = [item for item in record.user_prompts if prompt_cutoff is None or item[0] <= prompt_cutoff]
        last_user = max(eligible_prompts, key=lambda item: item[0])[1] if eligible_prompts else ""
        recent_prompts = [item for item in eligible_prompts if window_start is None or item[0] >= window_start.astimezone(timezone.utc)]
        recent_prompts = list({text: (timestamp, text) for timestamp, text in recent_prompts}.values())
        rendered.append({
            "tool": record.tool,
            "id": record.native_id,
            "title": record.title or "(untitled)",
            "workspace": record.workspace,
            "started_at": record.started_at.isoformat(),
            "last_activity": record.last_activity.isoformat(),
            "state_at_cutoff": state_at(record, at),
            "current_state": state_at(record, None),
            "child_count": len(attached),
            "children": [{"id": child.native_id, "last_activity": child.last_activity.isoformat(), "state_at_cutoff": state_at(child, at), "current_state": state_at(child, None), "source_files": child.source_files} for child in attached],
            "source_files": record.source_files,
            "evidence": record.evidence,
            "last_user_at_cutoff": last_user,
            "incident_window_prompts": [{"timestamp": timestamp.isoformat(), "text": text} for timestamp, text in recent_prompts[-20:]],
        })
    root_ids = {root.native_id for root in conversations}
    unattached = [child for child in children if not child.parent_id or child.parent_id not in root_ids]
    return {
        "cutoff": at.isoformat() if at else None,
        "user_conversation_count": len(conversations),
        "execution_record_count": len(conversations) + len(children),
        "evidence_record_count": len(evidence),
        "unattached_child_count": len(unattached),
        "unattached_children": [{"id": child.native_id, "parent_id": child.parent_id, "tool": child.tool, "source_files": child.source_files} for child in unattached],
        "conversations": rendered,
        "evidence_records": [{"tool": item.tool, "id": item.native_id, "kind": item.kind, "source_files": item.source_files} for item in evidence],
    }


def parse_duration(value: str) -> timedelta:
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([mhd])\s*", value.lower())
    if not match:
        raise argparse.ArgumentTypeError("duration must look like 30m, 2h, or 1d")
    amount = float(match.group(1))
    return {"m": timedelta(minutes=amount), "h": timedelta(hours=amount), "d": timedelta(days=amount)}[match.group(2)]


def default_paths(home: Path) -> dict[str, list[Path]]:
    appdata = Path(os.environ.get("APPDATA", str(home / ".config")))
    return {
        "codex": [home / ".codex/sessions", home / ".codex/archived_sessions"],
        "claude-code": [home / ".claude/projects"],
        "antigravity": [home / ".gemini/antigravity-cli/conversations", home / ".gemini/antigravity", appdata / "Antigravity/User"],
    }


def discover(tool: str, roots: Sequence[Path]) -> tuple[list[Path], str]:
    existing = [root for root in roots if root.exists()]
    if not existing:
        return [], "missing"
    patterns = ["*.db", "*.vscdb", "*.pb"] if tool == "antigravity" else ["*.jsonl"]
    files = [path for root in existing for pattern in patterns for path in root.rglob(pattern)]
    return files, "searched" if files else "present-empty"


def render_markdown(report: dict[str, Any], coverage: dict[str, dict[str, Any]], explain: bool = False) -> str:
    lines = [
        "# Conversation recovery inventory",
        "",
        f"- User conversations: **{report['user_conversation_count']}**",
        f"- Execution records: **{report['execution_record_count']}**",
        f"- Evidence-only records: **{report['evidence_record_count']}**",
        f"- Unattached children: **{report['unattached_child_count']}**",
        "",
        "| Tool | Conversation / last user request at cutoff | State at cutoff | Current state | Children | Last activity |",
        "|---|---|---|---|---:|---|",
    ]
    for item in report["conversations"]:
        label = item["last_user_at_cutoff"] or item["title"]
        lines.append(f"| {item['tool']} | {label.replace('|', '\\|')} | {item['state_at_cutoff']} | {item['current_state']} | {item['child_count']} | {item['last_activity']} |")
        if explain and item["children"]:
            # Keep CLI output ASCII-safe because Windows PowerShell can still use CP-1252.
            lines.append(f"| child evidence | {len(item['children'])} child workers attached to `{item['id']}` |  |  |  |  |")
        if explain:
            for prompt in item["incident_window_prompts"]:
                prompt_text = prompt["text"].replace("|", "\\|")
                lines.append(f"| prompt evidence | {prompt_text} |  |  |  | {prompt['timestamp']} |")
    lines.extend(["", "## Coverage", "", "| Surface | Status | Files |", "|---|---|---:|"])
    for tool, details in coverage.items():
        lines.append(f"| {tool} | {details['status']} | {details['files']} |")
    if report["unattached_children"]:
        lines.extend(["", "## Unattached child evidence", ""])
        for child in report["unattached_children"]:
            lines.append(f"- `{child['tool']}:{child['id']}` expected parent `{child['parent_id'] or 'unknown'}`; inspect `{child['source_files'][0] if child['source_files'] else 'unknown source'}`")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--at", help="incident cutoff as ISO-8601, including offset")
    parser.add_argument("--window-before", type=parse_duration, default=timedelta(hours=1))
    parser.add_argument("--tool", action="append", choices=["codex", "claude-code", "antigravity"])
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--explain", action="store_true")
    args = parser.parse_args(argv)

    cutoff = parse_timestamp(args.at) if args.at else datetime.now(timezone.utc)
    if args.at and cutoff is None:
        parser.error("--at must be a valid ISO-8601 timestamp")
    start = cutoff - args.window_before
    selected = args.tool or ["codex", "claude-code", "antigravity"]
    roots = default_paths(args.home)
    records: list[SessionRecord] = []
    coverage: dict[str, dict[str, Any]] = {}
    for tool in selected:
        files, status = discover(tool, roots[tool])
        coverage[tool] = {"status": status, "files": len(files)}
        # File mtime is a safe prefilter: a transcript with activity in the
        # incident window cannot have an older final modification time.
        candidate_files = []
        for path in files:
            try:
                if path.stat().st_mtime >= start.timestamp():
                    candidate_files.append(path)
            except OSError:
                continue
        if tool == "codex":
            parsed = parse_codex_files(candidate_files)
        elif tool == "claude-code":
            parsed = parse_claude_files(candidate_files)
        else:
            parsed = []
            for path in candidate_files:
                if path.suffix.lower() in {".db", ".vscdb"}:
                    parsed.extend(parse_antigravity_database(path))
                else:
                    try:
                        modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
                    except OSError:
                        continue
                    parsed.append(SessionRecord(tool="antigravity", native_id=path.stem, kind="event", started_at=modified, last_activity=modified, source_files=[str(path)], evidence=["unsupported:protobuf"]))
        window_records = [record for record in parsed if record.last_activity >= start and record.started_at <= cutoff]
        missing_parents = {record.parent_id for record in window_records if record.kind == "subagent" and record.parent_id}
        present_ids = {record.native_id for record in window_records}
        missing_parents -= present_ids
        if missing_parents and tool in {"codex", "claude-code"}:
            if tool == "codex":
                parent_paths = [path for path in files if any(parent_id in path.name for parent_id in missing_parents)]
                parent_records = parse_codex_files(parent_paths)
            else:
                parent_paths = [path for path in files if path.stem in missing_parents and "subagents" not in {part.lower() for part in path.parts}]
                parent_records = parse_claude_files(parent_paths)
            window_records.extend(record for record in parent_records if record.kind == "conversation" and record.native_id in missing_parents)
        deduplicated = {f"{record.tool}:{record.native_id}:{record.kind}": record for record in window_records}
        records.extend(deduplicated.values())
    report = build_report(records, at=cutoff, window_start=start)
    report["window_start"] = start.isoformat()
    report["coverage"] = coverage
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render_markdown(report, coverage, args.explain), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
