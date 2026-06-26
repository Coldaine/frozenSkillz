---
title: North Star
date: 2026-06-22
author: Patrick MacLyman
status: living
---

# North Star

## Why This Exists

Search providers expose overlapping tools and provider-specific interfaces. The problem is not only that callers can choose the wrong vendor — the larger opportunity is to make those tools comparable, reusable, cacheable, and observable from one place.

ColdSearch exists so a user or agent can ask for web/search/extract/crawl-style work once, then let the runtime use multiple provider tools, compare their effectiveness, spread requests across available keys and free quotas, and preserve what happened for later inspection.

## In / Out

> Goals are a guiding light, not a checklist. These are aspirations, not a reflection of the current codebase.

**In:** A query, URL, provider-tool request, or batch of requests.

**Out:** Provider results, normalized common views where useful, raw provider detail where needed, searchable recent cache items, rich logs, and enough provenance to understand how the answer was produced.

## What This Is Not

> Anti-goals default to zero. These are earned — each names a real, recurring case of ColdSearch being mistaken for the wrong thing. Identity-level only.

- **Not a pile of disconnected provider wrappers.** Provider tools should be reachable, but through one audited ColdSearch surface with shared config, logging, key handling, and cache behavior.
- **Not blind model-directed routing.** The model or caller may request a provider tool when that is intentional, but default routing should be controlled, observable, and comparable.
- **Not obligated to expose every niche vertical.** Broadly useful provider tools should be available; narrow surfaces such as specialized academic/legal verticals can stay deferred until there is a real workflow.
- **Not lossy normalization.** Common views are convenience layers; raw provider detail stays reachable when it matters.

## Goals

**G1: Unified Access To Provider Tools.** One ColdSearch surface should reach the useful tools from Tavily, Brave, Exa, Serper, Jina, Firecrawl, SearXNG, and future providers.

**G2: Compare Provider Effectiveness.** ColdSearch should make it practical to run comparable work across providers, inspect the results, and learn which tools work best for which jobs.

**G3: Use Keys And Quotas Efficiently.** Key pools, provider pools, cache hits, and batch execution should spread usage across available keys and reduce avoidable paid calls — including alternating between keys to double free-tier usage.

**G4: Search And Reuse Prior Work.** ColdSearch should build a searchable local memory of recent search/extract/tool results so later calls can surface relevant prior items before paying providers again. Reuse should prefer retrieval over blind replay; exact response replay is only acceptable when it is painless, explicit, and freshness policy allows it.

**G5: Preserve Useful Provider Detail.** Common outputs should be easy to consume, but raw provider details should remain accessible when they matter.

## Pillars

> Pillars are earned tradeoffs, stated as "accept cost X for benefit Y." Zero pillars is better than three plausible-sounding ones the owner didn't choose.

**Audit First.** Important calls should leave inspectable traces — logging is a primary product surface, not an afterthought or debug-only aid. We accept the cost and complexity of rich durable logging in exchange for comparability, trust, free-quota/key tracking, and the ability to explain agent behavior after the fact.

**Comparable Execution.** The runtime should make it easy to compare provider/tool performance instead of hiding every execution choice behind an opaque answer. We accept the overhead of comparable runs in exchange for learning which tools work best for which jobs.

**Searchable Cache, Not Blind Replay.** Cached work should become a searchable recent-results corpus that can be inspected and reused. We accept a lighter cache (prefer surfacing relevant prior items over silently replaying old responses; avoid a heavy bespoke cache layer unless a package or simple local store makes it painless) in exchange for reuse that the caller can trust and inspect.

**Config Over Code.** We accept a bit more config complexity in exchange for defaults that are over-writable: routing, provider pools, keys, and endpoint choices should be configurable rather than hardcoded, with sensible defaults.

**Fail Visible.** When something breaks, the error should make it obvious whether the issue is config, credentials, provider reachability, quota/rate limits, unsupported capability, or provider-specific behavior. We accept the effort of structured error classification in exchange for failures that diagnose themselves.
