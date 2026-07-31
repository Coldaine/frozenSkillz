# Eval runs

Must hold prompts, inputs, outputs, and scorer notes.

- `2026-07-31-spawn-prompt-richness.md` — does the ledger guard change spawn prompt richness?
  **Partial.** Establishes that default spawn prompts (1298–1378 chars) fall below the guard's
  1500-char gate, so it is near-inert as shipped, and that the guard is Windows-portable with a
  one-line fix. The comparative question is **unresolved**: the candidate arm was instrumented with
  the guard's own metrics log, which records nothing below the threshold. Two arms, not three; raw
  logs were not persisted. Does not discharge the promotion gate — see its "Status against the
  intake evaluation protocol" section.
