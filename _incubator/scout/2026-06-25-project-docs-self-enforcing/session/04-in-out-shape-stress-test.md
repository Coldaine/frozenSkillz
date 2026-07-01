# 04 — In/Out/Shape stress test against 12 real projects

A subagent read each project's top-level evidence (NORTH_STAR, README, AGENTS.md,
manifests) and attempted In/Out/Shape/Caller, then graded where the framework holds vs
collapses. Grounded in actual docs, not invented. Harsh mode: where a line would be
generic or tautological, the honest generic version was written and marked as a failure.

## Tally

**7 HOLDS / 1 THIN / 1 DEGRADES / 3 COLLAPSES** = 58% genuine holds, below the skill's
claimed ~70%.

## Per-project verdicts

| # | Project | Verdict | Why it held / broke |
|---|---|---|---|
| 1 | MooseGooseWebsite | HOLDS | Single owner, one gate, crisp In/Out + public/private boundary |
| 2 | coldaine-k8cluster | DEGRADES | GitOps platform: "repo is source of truth" is Shape; rest is tautology or architecture |
| 3 | ColdSearch | HOLDS | Clear caller + distinctive Out (normalized + raw + cache + provenance) |
| 4 | ColdVault | HOLDS | Crisp In→Out contract: govern access, never hold values |
| 5 | ColdTools | COLLAPSES | Umbrella monorepo, no caller, no Out beyond "tools in one place" |
| 6 | llm-archiver | THIN | Scheduler/cron is the real caller = "every process" anti-pattern |
| 7 | TokenRouter | HOLDS | Specific caller + contract-shaped Out |
| 8 | NorthStarGuardian | HOLDS | Specific caller + contract-shaped Out |
| 9 | agent-control-plane | COLLAPSES | Empty scaffold, no product yet |
| 10 | HermesStart | COLLAPSES | Configuration/starter, not a product |
| 11 | ComfyUI | HOLDS | Specific caller + contract-shaped Out |
| 12 | WoWshipExport | HOLDS | Specific caller + contract-shaped Out |

## Patterns

**Fits:** products with a specific caller and a contract-shaped Out — MooseGoose,
ColdSearch, ColdVault, TokenRouter, WoWshipExport, ComfyUI, NorthStarGuardian.

**Breaks on:**
- Platforms/infrastructure (coldaine-k8cluster) — identity is "source of truth," which
  is Shape; the other three lines collapse to tautology or architecture.
- Umbrella/consolidation repos (ColdTools) — no caller, no Out beyond "the tools in one
  place." Identity lives one level down in each tool's own NORTH_STAR.
- Scheduler-initiated pipelines (llm-archiver) — the real caller is a cron job, which is
  the "every process" anti-pattern. Shape carries it.
- Configurations/starters (HermesStart) — not a product.
- Empty scaffolds (agent-control-plane) — nothing to identify yet.

## Recommendation

Make In/Out/Shape/Caller a **conditional** NORTH_STAR section, gated on a Caller test:
*is there a specific caller, and is the Out a contract-shaped thing the caller receives?*
If no, omit — don't force filler.

For platforms/infra, defer to "source-of-truth" or "one-line test" framing instead of
the four-liner.

Repurpose the four-liner as a **per-epic scoping tool** in `docs/plans/` — that's where
"can you fill it out concretely?" is the right gate for whether an epic is well-defined.
Being unable to fill it out is a *signal the epic isn't well-defined* — not a mandatory
section of every identity doc.

## The rule of thumb

If you can't fill out In/Out/Shape concretely, that's a signal the thing you're
describing isn't a product with a caller — it's a platform, a spec, or a layer, and it
needs a different identity shape, not a forced one.
