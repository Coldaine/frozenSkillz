#!/usr/bin/env python3
"""
Extract a compact timeline from a Codex JSONL rollout.

Use this during retrospectives before synthesis so the account can cite actual
messages and tool calls instead of relying on memory or compacted summaries.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class TimelineItem:
    line: int
    timestamp: str
    item_type: str
    actor: str
    name: str
    summary: str


def compact(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)] + "..."


def parse_arguments(value: object) -> object:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except Exception:
        return value


def summarize_arguments(args: object) -> str:
    if isinstance(args, dict):
        for key in ("question", "query", "command", "url", "title", "code"):
            if key in args:
                return str(args[key])
        return json.dumps(args, ensure_ascii=False)
    return str(args)


def message_text(payload: dict) -> str:
    parts: list[str] = []
    for item in payload.get("content", []) or []:
        if isinstance(item, dict):
            parts.append(str(item.get("text") or item.get("input_text") or item.get("output_text") or ""))
        else:
            parts.append(str(item))
    return " ".join(parts)


def iter_timeline(path: Path, include_outputs: bool, limit: int) -> list[TimelineItem]:
    items: list[TimelineItem] = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, 1):
            try:
                obj = json.loads(line)
            except Exception:
                continue

            payload = obj.get("payload", {})
            payload_type = payload.get("type") or obj.get("type") or ""
            timestamp = obj.get("timestamp", "")

            if payload_type == "message":
                role = payload.get("role", "")
                items.append(
                    TimelineItem(
                        line_no,
                        timestamp,
                        "message",
                        role,
                        "",
                        compact(message_text(payload), limit),
                    )
                )
            elif payload_type == "function_call":
                name = payload.get("name", "")
                namespace = payload.get("namespace", "")
                full_name = f"{namespace}.{name}" if namespace else name
                args = parse_arguments(payload.get("arguments", ""))
                items.append(
                    TimelineItem(
                        line_no,
                        timestamp,
                        "tool-call",
                        "assistant",
                        full_name,
                        compact(summarize_arguments(args), limit),
                    )
                )
            elif payload_type == "function_call_output" and include_outputs:
                items.append(
                    TimelineItem(
                        line_no,
                        timestamp,
                        "tool-output",
                        "tool",
                        payload.get("call_id", ""),
                        compact(str(payload.get("output", "")), limit),
                    )
                )
            elif payload_type == "event_msg":
                event_payload = payload.get("payload", {})
                event_type = event_payload.get("type", "")
                if event_type in {"user_message", "mcp_tool_call_end", "thread_compacted"}:
                    items.append(
                        TimelineItem(
                            line_no,
                            timestamp,
                            f"event:{event_type}",
                            "event",
                            "",
                            compact(json.dumps(event_payload, ensure_ascii=False), limit),
                        )
                    )

    return items


def find_sessions(root: Path, phrase: str) -> list[Path]:
    matches: list[tuple[float, Path]] = []
    phrase_lower = phrase.lower()
    for path in root.rglob("*.jsonl"):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if phrase_lower in text.lower():
            matches.append((path.stat().st_mtime, path))
    return [path for _, path in sorted(matches, reverse=True)]


def render_markdown(items: list[TimelineItem]) -> str:
    lines = [
        "| Line | Timestamp | Type | Actor | Name | Summary |",
        "|---:|---|---|---|---|---|",
    ]
    for item in items:
        summary = item.summary.replace("|", "\\|")
        lines.append(
            f"| {item.line} | {item.timestamp} | {item.item_type} | {item.actor} | `{item.name}` | {summary} |"
        )
    return "\n".join(lines)


def render_jsonl(items: list[TimelineItem]) -> str:
    return "\n".join(json.dumps(asdict(item), ensure_ascii=False) for item in items)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract a compact Codex session timeline.")
    parser.add_argument("--session", help="Path to a rollout JSONL file.")
    parser.add_argument("--find", help="Find rollout files containing this exact phrase, then extract the newest match.")
    parser.add_argument("--root", default=str(Path.home() / ".codex" / "sessions"), help="Root used with --find.")
    parser.add_argument("--format", choices=["markdown", "jsonl"], default="markdown")
    parser.add_argument("--include-outputs", action="store_true", help="Include tool output rows. Noisy; off by default.")
    parser.add_argument("--summary-chars", type=int, default=220)
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()

    if args.session:
        session = Path(args.session)
    elif args.find:
        sessions = find_sessions(Path(args.root), args.find)
        if not sessions:
            raise SystemExit(f"No session matched phrase: {args.find}")
        session = sessions[0]
    else:
        parser.error("Provide --session or --find")

    items = iter_timeline(session, args.include_outputs, args.summary_chars)[: args.limit]
    if args.format == "jsonl":
        print(render_jsonl(items))
    else:
        print(render_markdown(items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
