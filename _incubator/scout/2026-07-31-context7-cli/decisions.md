# Decisions — context7-cli

## 2026-07-31 — adopt-as-external-tool

- **Decision:** Adopt. Install the binary built from this reviewed snapshot
  (`cargo install --path source --locked`); do NOT package the CLI itself as a skill.
- **Consumption:** the `context7-mcp` full rewrite
  ([#71](https://github.com/Coldaine/frozenSkillz/issues/71) survivor maintenance) targets
  this CLI as its transport: skill instructs agents to run
  `context7 docs <id> --query "..." --text`, with `CONTEXT7_API_KEYS` (comma-separated)
  providing rotation. The MCP server is dropped from agent configs when the rewrite lands.
- **Owner setup step (keys are credentials — never handled by agents):** owner adds keys
  themselves via `context7 keys add <key>` or sets `CONTEXT7_API_KEYS`.
- **Version policy:** pinned to v0.5.2 / `e2f1935`. Repo is single-author and young —
  re-review the diff before taking any future update.
- **Trigger to revisit:** if the upstream repo goes stale and the Context7 API drifts, the
  skill falls back to direct REST calls (the API surface is small; see `src/api.rs`).
