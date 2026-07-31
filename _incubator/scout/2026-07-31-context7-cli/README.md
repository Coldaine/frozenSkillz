# Scout: danilo-aguiar-br/context7-cli

- **Source:** https://github.com/danilo-aguiar-br/context7-cli
- **Pinned commit:** `e2f19359345880f8cbeb3b8852c2815ebb7e3481` (v0.5.2, pushed 2026-07-15)
- **Captured:** 2026-07-31 (shallow clone, `.git` removed)
- **Why:** Owner-requested intake — the `context7-mcp` skill is being fully rewritten
  ([#71](https://github.com/Coldaine/frozenSkillz/issues/71) survivor maintenance) and its
  standing failure was quota-blocking (10+ sessions). This CLI's multi-key rotation
  (`CONTEXT7_API_KEYS=a,b,c` → shuffle + exponential backoff) directly addresses that.
- **Verdict:** adopt-as-external-tool (binary installed from this reviewed source), not a
  packaged skill. See `analysis.md` and `decisions.md`.
