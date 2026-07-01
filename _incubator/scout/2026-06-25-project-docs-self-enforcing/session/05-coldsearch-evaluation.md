# 05 — ColdSearch NORTH_STAR evaluation + corrected version

Evaluated the ColdSearch `docs/NORTH_STAR.md` against the redesign bar. Overall grade:
**B−**. Strong identity, real problem statement, earned anti-goals, mostly real pillars.
Pulled down by prescription leak in Shape, a 7-item goals backlog with heavy duplication,
one anti-goal dissolving into draft-note prose, and an orphan LLM-endpoint line.

## Per-section grades

| Section | Grade | Notes |
|---|---|---|
| Frontmatter | A | Clean, correct, minimal. `status: living` + `date` is the right amount. |
| Why This Exists | A− | Genuinely good — states the problem explicitly (the thing the skill misses). Two fat paragraphs where the opener principle says one or two lines; content right, compression isn't. Last sentence is anti-goal work smuggled into the opener. |
| In / Out / Shape | C+ | Out is genuinely strong (contract-shaped). In is honest but generic. Shape is prescription leak (config path, alias migration = architecture, not identity). Orphan "LLM endpoint rule" has no home. ColdSearch IS a HOLDS case so In/Out belong; Shape doesn't. |
| What This Is Not | B+ | Three real earned anti-goals. "Not lossy normalization" is four sentences of draft-note prose ("really, the optimal approach would be a balance of both") — stops being self-enforcing. Borderline on minor-rule-explosion guard. |
| Goals | B− | 7 goals is a backlog wearing a goal suit. G5 is a feature spec (lists exactly what to log). G6 duplicates Out + anti-goal. G7 duplicates Shape. G1/G4 are real guiding lights. |
| Pillars | B | Mostly real tradeoffs. "Config Over Code" is a process instruction, not a tradeoff statement. Several pillars contain implementation hints. "Fail Visible" is the best. |

## Goal-by-goal (with Patrick's corrections applied)

- **G1 (unified access)** — keep. Real guiding light.
- **G2 (compare provider effectiveness)** — keep; it's the opener's core intent restated, fine as reinforcement.
- **G3 (key/quota efficiency)** — keep. **Patrick corrected this:** free-tier key-pool swapping (alternating between two keys to double free usage) is a load-bearing *design intent* of ColdSearch, not generic optimization. The "requirement not goal" framing was the skill's validation lens, which we're rejecting.
- **G4 (search and reuse prior work)** — keep. Real guiding light.
- **G5 (log and audit everything)** — **move to a pillar.** "Logging is a primary product surface, not an afterthought" is a tradeoff (accept cost/complexity of rich durable logging for comparability + trust + auditability). Merges with the existing "Audit First" pillar.
- **G6 (preserve useful provider detail)** — keep, as **intentional reinforcement** of the biggest failure mode. Patrick's reasoning: this is the biggest problem actually faced (lossy normalization burying raw detail), so hammering it across Out + anti-goal + G6 is intentional, not accidental duplication. The minor-rule-explosion guard doesn't apply — this is an observed recurring failure, which is exactly the "earned" bar.
- **G7 (stable surface, flexible execution)** — **move to architecture.md.** "Same core supports CLI + service/API/MCP + daemonization + async without duplicating logic" is a best practice, not a guiding light for this product specifically. It belongs in the architecture approach statement as the "why" for the CLI-first core.

## On intentional reinforcement vs noise

Duplication for reinforcement should **escalate in specificity, not just repeat:**
- Out line: "raw provider detail where needed" — the contract.
- Anti-goal: "not lossy normalization" — the failure mode to avoid.
- G6: "common outputs easy to consume, raw detail stays accessible when it matters" — the standing decision.

Three different angles on one idea, each doing different work. That's reinforcement. The
ColdSearch doc's actual problem was the *same idea restated near-verbatim four times
including as a feature-spec list in G5* — that's noise. **The rule: repeat the
load-bearing idea across sections, but each occurrence must do a different job. If two
occurrences do the same job, one is noise.**

## The corrected version

See `examples/coldsearch-north-star.corrected.md` — the resume point. Changes applied:

| Section | Change |
|---|---|
| Why This Exists | Keep both paragraphs' content, compress. Drop last sentence (anti-goal work). |
| In / Out / Shape | Keep In (accept thin) and Out (strong). Delete Shape — move to architecture. Delete orphan LLM endpoint rule. |
| What This Is Not | Cut "Not lossy normalization" to one line. Delete the four-sentence draft note. |
| Goals | Cut from 7 to 5: keep G1, G2, G3, G4, G6. Move G5 → Audit First pillar. Move G7 → architecture. |
| Pillars | Rewrite "Config Over Code" as a tradeoff statement, not a process instruction. Strip implementation hints. Merge G5's "logging is a primary surface" into Audit First. |

The fix is mostly deletion and demotion, not rewriting — usually the sign of a North Star
that started good and accreted.
