# Eval cases

- `probe.py` — passive `PreToolUse` instrument. Logs `{tool, chars, subagent_type}` per spawn to
  `$PROBE_LOG`, never denies. Used as the uncensored control instrument in
  `../runs/2026-07-31-spawn-prompt-richness.md`.

Note for future runs: install `probe.py` in **every** arm, including arms where a guard hook is
also active. A guard's own metrics output is not a substitute — `ledger_guard_spawn.py` emits
nothing for prompts at or below its threshold, so its log cannot measure prompt length.
