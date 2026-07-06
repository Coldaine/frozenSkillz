#!/usr/bin/env python3
"""
Find likely locations for a remembered artifact across local transcripts,
workspace files, and Chrome history.

This is deliberately deterministic. It does not call MCP servers or LLMs; use it
to create the first candidate table before a semantic Pieces/Drive/Chrome pass.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
from urllib.parse import urlsplit, urlunsplit


CHROME_EPOCH = dt.datetime(1601, 1, 1, tzinfo=dt.timezone.utc)


@dataclass
class Hit:
    source: str
    when: str
    kind: str
    location: str
    score: int
    evidence: str
    matched_terms: list[str]


def parse_date(value: str | None, end_of_day: bool = False) -> dt.datetime | None:
    if not value:
        return None
    text = value.strip()
    if re.fullmatch(r"\d{8}", text):
        base = dt.datetime.strptime(text, "%Y%m%d").replace(tzinfo=dt.timezone.utc)
        if end_of_day:
            return base + dt.timedelta(days=1)
        return base
    parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def chrome_time_to_iso(value: int) -> str:
    try:
        return (CHROME_EPOCH + dt.timedelta(microseconds=int(value))).isoformat()
    except Exception:
        return ""


def in_window(iso_text: str, start: dt.datetime | None, end: dt.datetime | None) -> bool:
    if not iso_text:
        return True
    try:
        when = dt.datetime.fromisoformat(iso_text.replace("Z", "+00:00"))
    except Exception:
        return True
    if when.tzinfo is None:
        when = when.replace(tzinfo=dt.timezone.utc)
    when = when.astimezone(dt.timezone.utc)
    return (start is None or when >= start) and (end is None or when < end)


def term_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(term.strip())
    escaped = re.sub(r"\\\s+", r"\\s+", escaped)
    return re.compile(rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])", re.IGNORECASE)


def find_terms(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term_pattern(term).search(text)]


def term_score(text: str, terms: list[str], require_all: bool) -> int:
    hits = find_terms(text, terms)
    if require_all and len(hits) != len(terms):
        return 0
    return len(hits)


def match_score(text: str, terms: list[str], must_terms: list[str], require_all: bool) -> int:
    if must_terms and any(not term_pattern(term).search(text) for term in must_terms):
        return 0
    score = term_score(text, terms, require_all)
    if not score and not must_terms:
        return 0
    return (10 * len(must_terms)) + score


def snippet(text: str, terms: list[str], width: int = 320) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    positions = []
    for term in terms:
        match = term_pattern(term).search(compact)
        if match:
            positions.append(match.start())
    if not positions:
        return compact[:width]
    center = max(0, min(positions) - width // 4)
    return compact[center : center + width]


def iter_jsonl_records(path: Path, include_tool_outputs: bool) -> Iterator[tuple[str, str, str, str]]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for lineno, line in enumerate(handle, 1):
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                timestamp = obj.get("timestamp") or obj.get("created_at") or ""
                payload = obj.get("payload", obj)
                ptype = payload.get("type") or obj.get("type") or "jsonl"
                if not include_tool_outputs and ptype in {
                    "function_call_output",
                    "mcp_tool_call_end",
                    "tool_search_output",
                    "patch_apply_end",
                }:
                    continue
                text_parts: list[str] = []

                if ptype == "message":
                    role = payload.get("role", "")
                    for item in payload.get("content", []) or []:
                        if isinstance(item, dict):
                            text_parts.append(str(item.get("text") or item.get("input_text") or ""))
                        else:
                            text_parts.append(str(item))
                    kind = f"message:{role}" if role else "message"
                elif ptype == "function_call":
                    kind = "function_call"
                    text_parts.extend(
                        [
                            str(payload.get("namespace") or ""),
                            str(payload.get("name") or ""),
                            str(payload.get("arguments") or ""),
                        ]
                    )
                elif ptype == "function_call_output":
                    kind = "function_output"
                    text_parts.append(str(payload.get("output") or ""))
                elif ptype == "event_msg":
                    kind = "event_msg"
                    text_parts.append(json.dumps(payload, ensure_ascii=False))
                else:
                    kind = ptype
                    text_parts.append(json.dumps(payload, ensure_ascii=False))

                text = " ".join(part for part in text_parts if part)
                if text:
                    yield timestamp, kind, f"{path}:{lineno}", text
    except OSError:
        return


def transcript_paths() -> Iterator[Path]:
    home = Path.home()
    roots = [
        home / ".codex" / "sessions",
        home / ".claude" / "projects",
        home / ".cursor" / "projects",
        home / ".opencode",
    ]
    history = home / ".codex" / "history.jsonl"
    if history.exists():
        yield history
    for root in roots:
        if root.exists():
            yield from root.rglob("*.jsonl")


def search_transcripts(
    terms: list[str],
    must_terms: list[str],
    start: dt.datetime | None,
    end: dt.datetime | None,
    require_all: bool,
    include_tool_outputs: bool,
) -> Iterator[Hit]:
    for path in transcript_paths():
        for timestamp, kind, location, text in iter_jsonl_records(path, include_tool_outputs):
            if not in_window(timestamp, start, end):
                continue
            score = match_score(text, terms, must_terms, require_all)
            if score:
                all_terms = must_terms + terms
                yield Hit("transcript", timestamp, kind, location, score, snippet(text, all_terms), find_terms(text, all_terms))


def search_chrome_history(
    terms: list[str],
    must_terms: list[str],
    start: dt.datetime | None,
    end: dt.datetime | None,
    require_all: bool,
) -> Iterator[Hit]:
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data"
    if not base.exists():
        return

    for history in base.glob("*/History"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tmp:
            tmp_path = Path(tmp.name)
        try:
            shutil.copy2(history, tmp_path)
            con = sqlite3.connect(tmp_path)
            try:
                rows = con.execute(
                    "select url, title, last_visit_time from urls order by last_visit_time desc"
                ).fetchall()
            finally:
                con.close()
        except Exception:
            continue
        finally:
            try:
                tmp_path.unlink()
            except OSError:
                pass

        for url, title, last_visit_time in rows:
            when = chrome_time_to_iso(last_visit_time)
            if not in_window(when, start, end):
                continue
            text = f"{title or ''} {url or ''}"
            score = match_score(text, terms, must_terms, require_all)
            if score:
                profile = history.parent.name
                all_terms = must_terms + terms
                yield Hit("chrome-history", when, "url-title", f"{profile}: {url}", score, snippet(text, all_terms), find_terms(text, all_terms))


def search_files_with_rg(
    roots: list[Path],
    terms: list[str],
    must_terms: list[str],
    require_all: bool,
    max_bytes: int,
) -> Iterator[Hit]:
    rg = shutil.which("rg")
    existing_roots = [str(root) for root in roots if root.exists()]
    if not rg or not existing_roots:
        return

    pattern_terms = list(dict.fromkeys(must_terms + terms))
    pattern = "|".join(re.escape(term) for term in pattern_terms)
    cmd = [rg, "--json", "--ignore-case", "--max-filesize", str(max_bytes), pattern, *existing_roots]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    except Exception:
        return

    for line in proc.stdout.splitlines():
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get("type") != "match":
            continue
        data = obj.get("data", {})
        lines = data.get("lines", {}).get("text", "")
        path = data.get("path", {}).get("text", "")
        line_number = data.get("line_number", "")
        score = match_score(lines, terms, must_terms, require_all)
        if score:
            yield Hit("file", "", "rg-match", f"{path}:{line_number}", score, snippet(lines, pattern_terms), find_terms(lines, pattern_terms))


def redact_text(value: str) -> str:
    home = str(Path.home())
    redacted = value.replace(home, "%USERPROFILE%")

    def repl_url(match: re.Match[str]) -> str:
        raw = match.group(0)
        try:
            parts = urlsplit(raw)
            return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
        except Exception:
            return "[url]"

    redacted = re.sub(r"https?://[^\s|)>\"]+", repl_url, redacted)
    redacted = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[email]", redacted)
    return redacted


def hit_record(hit: Hit, redact: bool, no_snippets: bool) -> dict[str, object]:
    location = redact_text(hit.location) if redact else hit.location
    evidence = "" if no_snippets else hit.evidence
    if redact and evidence:
        evidence = redact_text(evidence)
    return {
        "surface": hit.source,
        "timestamp": hit.when,
        "kind": hit.kind,
        "score": hit.score,
        "location": location,
        "matched_terms": hit.matched_terms,
        "direct_evidence": evidence,
        "inference": "candidate match only; verify against source before citing",
        "confidence": "weak",
        "needs_followup": "open source record/page and classify as direct hit, adjacent, or false positive",
    }


def sorted_hits(hits: list[Hit], limit: int) -> list[Hit]:
    return sorted(hits, key=lambda h: (h.score, h.when), reverse=True)[:limit]


def render_markdown(hits: list[Hit], limit: int, redact: bool, no_snippets: bool) -> str:
    hits = sorted_hits(hits, limit)
    hits = sorted(hits, key=lambda h: (h.score, h.when), reverse=True)[:limit]
    out = [
        "| Source | When | Kind | Score | Matched Terms | Location | Evidence |",
        "|---|---:|---|---:|---|---|---|",
    ]
    for hit in hits:
        record = hit_record(hit, redact, no_snippets)
        evidence = str(record["direct_evidence"]).replace("|", "\\|")
        location = str(record["location"]).replace("|", "\\|")
        matched = ", ".join(str(term) for term in record["matched_terms"])
        out.append(f"| {hit.source} | {hit.when} | {hit.kind} | {hit.score} | {matched} | `{location}` | {evidence} |")
    return "\n".join(out)


def render_json(hits: list[Hit], limit: int, redact: bool, no_snippets: bool) -> str:
    records = [hit_record(hit, redact, no_snippets) for hit in sorted_hits(hits, limit)]
    return json.dumps(records, ensure_ascii=False, indent=2)


def render_jsonl(hits: list[Hit], limit: int, redact: bool, no_snippets: bool) -> str:
    return "\n".join(
        json.dumps(hit_record(hit, redact, no_snippets), ensure_ascii=False)
        for hit in sorted_hits(hits, limit)
    )


def render_csv(hits: list[Hit], limit: int, redact: bool, no_snippets: bool) -> str:
    import io

    output = io.StringIO()
    fieldnames = [
        "surface",
        "timestamp",
        "kind",
        "score",
        "location",
        "matched_terms",
        "direct_evidence",
        "inference",
        "confidence",
        "needs_followup",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for hit in sorted_hits(hits, limit):
        record = hit_record(hit, redact, no_snippets)
        record["matched_terms"] = ",".join(str(term) for term in record["matched_terms"])
        writer.writerow(record)
    return output.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic historical artifact hunt.")
    parser.add_argument("--terms", required=True, help="Comma-separated terms or variants to score, e.g. 'Orin,flash,JetPack'.")
    parser.add_argument("--must", default="", help="Comma-separated anchor terms every result must contain, e.g. 'Jetson'.")
    parser.add_argument("--from-date", dest="from_date", help="UTC date/window start, YYYYMMDD or ISO timestamp.")
    parser.add_argument("--to-date", dest="to_date", help="UTC date/window end, YYYYMMDD or ISO timestamp. YYYYMMDD is exclusive next-day.")
    parser.add_argument("--all-terms", action="store_true", help="Require every term to appear in a record.")
    parser.add_argument("--root", action="append", default=[], help="Additional local roots to search with rg. Repeatable.")
    parser.add_argument("--skip-transcripts", action="store_true")
    parser.add_argument("--skip-chrome", action="store_true")
    parser.add_argument("--skip-files", action="store_true")
    parser.add_argument("--include-tool-outputs", action="store_true", help="Also search large tool-output records. Noisy, but useful when the output itself is the source.")
    parser.add_argument("--max-file-bytes", type=int, default=2_000_000)
    parser.add_argument("--limit", type=int, default=80)
    parser.add_argument("--format", choices=["markdown", "json", "jsonl", "csv"], default="markdown", help="Output format. Use jsonl for subagent collector lanes.")
    parser.add_argument("--no-redact", dest="redact", action="store_false", help="Do not redact URL query strings, emails, or the home directory prefix.")
    parser.add_argument("--no-snippets", action="store_true", help="Omit evidence snippets from output. Useful before saving to durable docs.")
    parser.set_defaults(redact=True)
    args = parser.parse_args()

    terms = [term.strip() for term in args.terms.split(",") if term.strip()]
    must_terms = [term.strip() for term in args.must.split(",") if term.strip()]
    if not terms and not must_terms:
        parser.error("--terms or --must must include at least one non-empty term")

    start = parse_date(args.from_date)
    end = parse_date(args.to_date, end_of_day=bool(args.to_date and re.fullmatch(r"\d{8}", args.to_date)))

    hits: list[Hit] = []
    if not args.skip_transcripts:
        hits.extend(search_transcripts(terms, must_terms, start, end, args.all_terms, args.include_tool_outputs))
    if not args.skip_chrome:
        hits.extend(search_chrome_history(terms, must_terms, start, end, args.all_terms))
    if not args.skip_files and args.root:
        roots = [Path(root) for root in args.root]
        hits.extend(search_files_with_rg(roots, terms, must_terms, args.all_terms, args.max_file_bytes))

    if args.format == "json":
        print(render_json(hits, args.limit, args.redact, args.no_snippets))
    elif args.format == "jsonl":
        print(render_jsonl(hits, args.limit, args.redact, args.no_snippets))
    elif args.format == "csv":
        print(render_csv(hits, args.limit, args.redact, args.no_snippets), end="")
    else:
        print(render_markdown(hits, args.limit, args.redact, args.no_snippets))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
