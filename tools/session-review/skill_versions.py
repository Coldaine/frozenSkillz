"""Nightly SKILL.md version ledger.

Sweeps known skill roots, hashes every SKILL.md, and appends a row the first
time each (skill, content-hash) pair is seen, so grades can attach to the skill
version that was actually live. Run before condense.

The ledger is committed on purpose: `first_seen` for a given content hash is
unreconstructable once that SKILL.md is edited and the old bytes leave disk, and
it is the join key that keeps an old grade attached to the version it graded.

Two properties keep it commit-friendly:

- **Append-only.** Existing rows are never rewritten, so a nightly run with no
  skill changes produces no diff at all. There is deliberately no `last_seen`
  field; it would rewrite all 200+ rows every night to record something nothing
  reads. "Which version is current" is answered by `current_hash`, which reads
  the bytes on disk and falls back to the newest `first_seen`.
- **HOME-relative paths.** Rows store `~/...` posix paths, so the ledger carries
  no local username and stays comparable across machines.
"""
import hashlib
import json
from datetime import date
from pathlib import Path

HOME = Path.home()
ROOTS = [
    HOME / ".agents" / "skills",
    HOME / ".claude" / "skills",
    HOME / ".cursor" / "skills",
    HOME / ".cursor" / "skills-cursor",
    HOME / ".codex" / "skills",
    HOME / ".codex" / "plugins" / "cache",
]
LEDGER = Path(__file__).parent / "skill-versions.jsonl"


def _relative(path: Path) -> str:
    """HOME-relative posix form, so no local username enters the ledger.

    The unresolved path is tried first on purpose. Every sweep root lives under
    HOME, so a skill reached through a symlink or junction keeps its logical
    `~/...` form instead of leaking the absolute target it resolves to.
    """
    for candidate in (path, path.resolve()):
        try:
            return "~/" + candidate.relative_to(HOME).as_posix()
        except ValueError:
            continue
    return path.resolve().as_posix()


def _hash_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    except OSError:
        return None


_rows_cache: tuple | None = None


def _load_rows() -> dict:
    """Ledger as a {(name, sha256): row} map.

    Cached on the ledger's (mtime, size) because condense.py calls
    `current_hash` once per skill per session; re-parsing every row each time
    turns a cheap lookup into the hot path.
    """
    global _rows_cache
    if not LEDGER.exists():
        return {}
    st = LEDGER.stat()
    stamp = (st.st_mtime_ns, st.st_size)
    if _rows_cache is not None and _rows_cache[0] == stamp:
        return _rows_cache[1]
    rows = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        rows[(r["name"], r["sha256"])] = r
    _rows_cache = (stamp, rows)
    return rows


def sweep():
    today = date.today().isoformat()
    known = dict(_load_rows())
    new_rows = []
    found = 0
    for root in ROOTS:
        if not root.exists():
            continue
        for f in root.rglob("SKILL.md"):
            name = f.parent.name
            sha = _hash_file(f)
            if sha is None:
                continue
            found += 1
            key = (name, sha)
            if key in known:
                continue
            row = {"name": name, "sha256": sha, "path": _relative(f),
                   "first_seen": today}
            known[key] = row
            new_rows.append(row)

    if new_rows:
        block = "".join(
            json.dumps(r) + "\n"
            for r in sorted(new_rows, key=lambda r: (r["name"], r["sha256"])))
        # One write of the whole block, so two runs racing on the nightly cron
        # interleave at row-block granularity rather than mid-line.
        with LEDGER.open("a", encoding="utf-8") as fh:
            fh.write(block)

    print(f"swept {found} SKILL.md files, {len(new_rows)} new version(s), "
          f"ledger has {len(known)} (name, version) rows")


def _root_rank(path: str) -> int:
    """Canonicality of the root a ledger path sits under; higher wins.

    Matching is boundary-aware: a bare `startswith` would score
    `~/.cursor/skills-cursor/...` against the earlier `~/.cursor/skills` root
    and hand it that root's rank.
    """
    for i, root in enumerate(ROOTS):
        prefix = "~/" + root.relative_to(HOME).as_posix()
        if path == prefix or path.startswith(prefix + "/"):
            return len(ROOTS) - i
    return 0


def _still_on_disk(row: dict) -> bool:
    """True if the file this row points at still has this row's content hash.

    Existence alone is not enough: the path outlives the bytes, so a skill that
    was edited still has a file sitting at every old row's path.
    """
    path = row["path"]
    target = HOME / path[2:] if path.startswith("~/") else Path(path)
    return _hash_file(target) == row["sha256"]


def current_hash(name: str) -> str:
    """Newest live hash for a skill name, for condense.py.

    The ledger is append-only history, so its newest row is not automatically
    what is on disk — reverting a skill to an earlier version adds no row and
    leaves a newer row still standing. Rows whose bytes are still present win
    for that reason.

    Where nothing verifies (a machine that has none of these skills installed,
    such as CI) the newest ledger row is still returned, so this degrades to a
    pure ledger read rather than reporting everything as `unknown`.

    Ties on first_seen (the same version present in several roots or plugin
    caches) resolve to the most canonical root by ROOTS order, then by hash for
    determinism — never by position in the file.
    """
    rows = [r for r in _load_rows().values() if r["name"] == name]
    if not rows:
        return "unknown"
    live = [r for r in rows if _still_on_disk(r)]
    best = max(live or rows,
               key=lambda r: (r["first_seen"], _root_rank(r["path"]), r["sha256"]))
    return best["sha256"]


if __name__ == "__main__":
    sweep()
