"""Condense AgentsView sessions into reviewer input-contract JSON.

Selects skill-firing sessions (tagged skill_name plus the codex SKILL.md-read
channel), builds one trajectory JSON per session sized for a single judge call.

Usage:
  python condense.py --sessions "id1,id2"        # explicit (calibration)
  python condense.py --new --cap 25              # ungraded skill-firing sessions, newest first
"""
import argparse
import json
import re
import sqlite3
from pathlib import Path

import skill_versions

DB = Path.home() / ".agentsview" / "sessions.db"
HERE = Path(__file__).parent
WORK = HERE / ".work"
STATE = HERE / "state.json"

LOOP_REPROMPT = "Briefly inform the user about the task result"
CLAIM_RE = re.compile(r"\b(done|completed?|passed|merged|landed|fixed|green|success)\b", re.I)
OFFLINE_RE = re.compile(r"\boffline\b|MCP.{0,20}down|\bunavailable\b|\bquota\b|rate.?limit", re.I)
CODEX_SKILL_RE = re.compile(r"skills[\\/]([^\\/\"']+)[\\/]SKILL\.md")


def clip(s, n):
    s = (s or "").strip()
    return s if len(s) <= n else s[:n] + " …[truncated]"


def skill_fires(cx, sid, agent):
    fires = {}
    for (name,) in cx.execute(
            "SELECT DISTINCT skill_name FROM tool_calls WHERE session_id=? AND skill_name IS NOT NULL", (sid,)):
        fires.setdefault(name, "tagged")
    if agent == "codex":
        for (ij,) in cx.execute(
                "SELECT input_json FROM tool_calls WHERE session_id=? AND input_json LIKE '%SKILL.md%'", (sid,)):
            for m in CODEX_SKILL_RE.finditer((ij or "").replace("\\\\", "\\")):
                fires.setdefault(m.group(1), "skillmd-read")
    return [{"name": n, "channel": ch, "version_hash": skill_versions.current_hash(n)}
            for n, ch in sorted(fires.items())]


def condense(cx, sid):
    srow = cx.execute(
        "SELECT agent, started_at, cwd, message_count, tool_failure_signal_count,"
        " edit_churn_count, health_score, is_automated FROM sessions WHERE id=?", (sid,)).fetchone()
    if not srow:
        return None
    agent, started, cwd, msgs, fails, churn, health, automated = srow

    rows = cx.execute(
        "SELECT ordinal, role, content FROM messages WHERE session_id=? AND role IN ('user','assistant')"
        " AND content IS NOT NULL AND length(content) > 0 ORDER BY ordinal", (sid,)).fetchall()

    user_msgs, claims, offline_hits, opening = [], [], 0, None
    for ordn, role, content in rows:
        if role == "user":
            if content.startswith("<"):
                continue
            if LOOP_REPROMPT in content:
                user_msgs.append({"ordinal": ordn, "text": "[loop-reprompt]"})
                continue
            entry = {"ordinal": ordn, "text": clip(content, 280)}
            if opening is None:
                opening = clip(content, 800)
            user_msgs.append(entry)
        else:
            if OFFLINE_RE.search(content):
                offline_hits += 1
            if CLAIM_RE.search(content) and len(claims) < 8:
                claims.append({"ordinal": ordn, "text": clip(content, 300)})
    if len(user_msgs) > 40:
        user_msgs = user_msgs[:20] + [{"ordinal": -1, "text": f"[…{len(user_msgs)-40} messages elided…]"}] + user_msgs[-20:]

    closing = [{"ordinal": o, "role": r, "text": clip(c, 500)} for o, r, c in rows[-10:]]
    (ncalls,) = cx.execute("SELECT COUNT(*) FROM tool_calls WHERE session_id=?", (sid,)).fetchone()

    return {
        "session_id": sid, "agent": agent, "date": (started or "")[:10], "cwd": cwd or "",
        "is_automated": bool(automated),
        "opening_ask": opening or "[no genuine user message found]",
        "user_messages": user_msgs,
        "assistant_claims": claims,
        "closing_window": closing,
        "tool_stats": {"messages": msgs, "tool_calls": ncalls, "tool_failures": fails,
                       "edit_churn": churn, "agentsview_health_thrash_score": health},
        "skills_fired": skill_fires(cx, sid, agent),
        "resource_flags": {"offline_or_quota_mentions": offline_hits},
    }


def pick_new(cx, cap, graded):
    ids = [r[0] for r in cx.execute(
        "SELECT DISTINCT s.id FROM sessions s JOIN tool_calls tc ON tc.session_id = s.id"
        " WHERE (tc.skill_name IS NOT NULL OR (s.agent='codex' AND tc.input_json LIKE '%SKILL.md%'))"
        " AND s.ended_at IS NOT NULL ORDER BY s.started_at DESC")]
    return [i for i in ids if i not in graded][:cap]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions")
    ap.add_argument("--new", action="store_true")
    ap.add_argument("--cap", type=int, default=25)
    args = ap.parse_args()

    state = json.loads(STATE.read_text()) if STATE.exists() else {"graded": {}}
    cx = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    ids = ([s.strip() for s in args.sessions.split(",") if s.strip()] if args.sessions
           else pick_new(cx, args.cap, state["graded"]))

    WORK.mkdir(exist_ok=True)
    out = []
    for sid in ids:
        t = condense(cx, sid)
        if t is None:
            print(f"skip (not found): {sid}")
            continue
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", sid)
        p = WORK / f"{safe}.json"
        p.write_text(json.dumps(t, indent=1), encoding="utf-8")
        out.append(str(p))
        print(p)
    if not out:
        print("nothing to grade")


if __name__ == "__main__":
    main()
