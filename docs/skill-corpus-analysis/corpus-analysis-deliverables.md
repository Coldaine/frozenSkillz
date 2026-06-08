# Agent Skill Corpus Analysis — Design Pattern Reference

> Built from actual skill directory analysis, March 2026. Corpus: Tier 1 official sources (Vercel, Google ADK, Supabase, Anthropic). See `/corpus/` for collected skills.

---

## Deliverable 1: Corpus Summary Table

| Skill Name | Source Tier | Primary Pattern | Secondary Pattern(s) | Disclosure (1-5) | Description (1-5) | Structure (1-5) | Gates (1-5) | Quality Tier | Notable Feature |
|---|---|---|---|---|---|---|---|---|---|---|
| vercel-composition-patterns | Tier 1 (Vercel) | tool-wrapper | — | 5 | 5 | 5 | N/A | **Exemplar** | Lean SKILL.md (89 lines) + rich `rules/` folder with 8 rule files + AGENTS.md compiled doc. Progressive disclosure at its finest. |
| vercel-react-best-practices | Tier 1 (Vercel) | tool-wrapper | — | 5 | 5 | 5 | N/A | **Exemplar** | 65 rules across 8 priority categories. SKILL.md is routing doc; full rules in AGENTS.md + `rules/`. |
| supabase-postgres-best-practices | Tier 1 (Supabase) | tool-wrapper | — | 5 | 4 | 5 | N/A | **Strong** | 8 reference categories with prefix-based lookup. SKILL.md (64 lines) + `references/` folder. Good trigger coverage. |
| google-adk-dev-guide | Tier 1 (Google) | pipeline | tool-wrapper | 4 | 4 | 4 | 5 | **Strong** | Explicit 4-phase pipeline (Understand → Build → Evaluate → Deploy) with gates. "MANDATORY" language. References other skills. |
| anthropic-pdf | Tier 1 (Anthropic) | tool-wrapper | — | 1 | 2 | 1 | N/A | **Anti-pattern** | 314-line monolithic SKILL.md. No progressive disclosure. All content inline. Zero `references/`, `assets/`, or `scripts/`. |

**Key Finding:** The Vercel and Supabase skills demonstrate what progressive disclosure looks like in practice: SKILL.md is a lean routing document (<100 lines), while the actual domain knowledge lives in `references/`, `rules/`, or `AGENTS.md`. The Anthropic PDF skill demonstrates the anti-pattern.

---

## Deliverable 2: Pattern Exemplar Reports

### Exemplar 1: Tool Wrapper — `vercel-composition-patterns`

**Why it's the best example:** This skill demonstrates textbook progressive disclosure. The SKILL.md is 89 lines and acts purely as a routing document. All 8 composition rules live in `rules/`, and the full expanded guide is in `AGENTS.md`.

**Full directory listing:**

```
vercel-composition-patterns/
├── SKILL.md           # 89 lines — routing only
├── AGENTS.md          # 22,627 bytes — full compiled guide
├── README.md          # 2,140 bytes
├── metadata.json      # 530 bytes
└── rules/
    ├── architecture-avoid-boolean-props.md
    ├── architecture-compound-components.md
    ├── state-decouple-implementation.md
    ├── state-context-interface.md
    ├── state-lift-state.md
    ├── patterns-explicit-variants.md
    ├── patterns-children-over-render-props.md
    └── react19-no-forwardref.md
```

**SKILL.md analysis:**

- **Trigger semantics:** Description includes specific contexts: "boolean prop proliferation", "compound components", "context providers", "component architecture". Clear activation criteria.
- **Body vs. references:** Body is 89 lines. References directory holds 8 detailed rule files (~2-5KB each). Agent loads SKILL.md first; `rules/` files load on demand.
- **Token budget:** L1 (metadata): ~50 tokens. L2 (SKILL.md body): ~200 tokens. L3 (rule files): ~2-5KB each, loaded as needed.

**Control flow:** This is a pure Tool Wrapper — no gates. The skill packages domain knowledge that the agent consumes on demand.

**What makes it "large without being monolithic":**

- SKILL.md doesn't repeat content from rule files — it indexes them.
- The `rules/` directory allows rule-level granularity: agent can load just "compound components" without loading "avoid boolean props."
- AGENTS.md provides a single merged view for agents that prefer one document.

**What I would steal:**

1. The prefix-based rule naming (`architecture-`, `state-`, `patterns-`, `react19-`) for predictable lookup
2. The priority table in SKILL.md showing impact levels (CRITICAL → HIGH → MEDIUM)
3. The "When to Apply" section with specific trigger contexts
4. The separation of `rules/` from AGENTS.md — two consumption modes

---

### Exemplar 2: Pipeline — `google-adk-dev-guide`

**Why it's the best example:** This skill demonstrates explicit phase gating with strict language. The skill is "ALWAYS ACTIVE" but enforces a sequential workflow through 4 phases with mandatory checkpoints.

**Full directory listing:**

```
google-adk-dev-guide/
└── SKILL.md           # 197 lines — contains full workflow
```

(Note: This skill lives in a monorepo where other ADK skills provide the referenced content — `adk-cheatsheet`, `adk-eval-guide`, `adk-deploy-guide`, `adk-scaffold`.)

**SKILL.md analysis:**

- **Trigger semantics:** "ALWAYS ACTIVE — read at the start of any ADK agent development session." Unusual — it doesn't deactivate.
- **Body content:** Phase 1 (Understand Spec), Phase 2 (Build), Phase 3 (Evaluate), Phase 4 (Deploy). Each phase has numbered steps.
- **Gate language:**
  - "MANDATORY: Activate `/adk-eval-guide` before running evaluation."
  - "IMPORTANT: If `DESIGN_SPEC.md` exists... it is your primary source of truth."
  - "Never deploy without explicit human approval."
  - "Phase 3 is the most important phase."

**Control flow analysis:**

| Phase | Gate | Enforcement |
|---|---|---|
| Phase 1 | Read DESIGN_SPEC.md first | "If DESIGN_SPEC.md exists, it is your primary source of truth" |
| Phase 2 | Use `/adk-cheatsheet` before writing code | Named reference to sibling skill |
| Phase 3 | Activate `/adk-eval-guide` before eval | "MANDATORY" language, explicit |
| Phase 4 | Get human approval before deploy | "Never deploy without explicit human approval" |

**What makes this skill "large without being monolithic":**

- It delegates to sibling skills for detailed content (`/adk-cheatsheet`, `/adk-eval-guide`)
- Each phase is self-contained with clear entry/exit criteria
- The skill doesn't contain the domain knowledge — it orchestrates access to it

**What I would steal:**

1. The "ALWAYS ACTIVE" pattern for skills that govern a session lifecycle
2. The explicit phase numbering with "re-read relevant skill before each phase" guidance
3. The "re-read at L1" pattern for long sessions where context compaction may drop skill content
4. The mandatory gate language ("MANDATORY:", "IMPORTANT:", "Never deploy without...")

---

## Deliverable 3: Composite Pattern Analysis

**Composite 1: Pipeline + Tool Wrapper — `google-adk-dev-guide`**

- **Pipeline aspect:** 4-phase sequential workflow with explicit gates between phases
- **Tool Wrapper aspect:** Delegates to `/adk-cheatsheet`, `/adk-eval-guide`, `/adk-deploy-guide`, `/adk-scaffold` for domain knowledge
- **Handoff:** Phase 2 says "For ADK API patterns... use `/adk-cheatsheet`." Phase 3 says "MANDATORY: Activate `/adk-eval-guide`."
- **Composition is explicit:** The skill explicitly names which sibling skills to activate at each phase.

**Composite 2: Tool Wrapper + Generator (emergent in some skills)**

- Several Vercel skills could compose with a hypothetical "code generator" skill that takes the rule output and produces code
- The pattern isn't explicit in collected skills but is a natural extension

---

## Deliverable 4: Anti-Pattern Gallery

### Anti-Pattern 1: Monolithic Blob — `anthropic-pdf`

**What's wrong:** 314-line SKILL.md with all content inline. No progressive disclosure. Agent pays full token cost even for simple queries.

**File evidence:** `/corpus/tier1-official/../skills/pdf/SKILL.md` — 314 lines, no `references/` directory.

**How to fix:** Apply Tool Wrapper pattern — extract library references to `references/pypdf.md`, `references/reportlab.md`, etc. Keep SKILL.md as a 60-line index.

### Anti-Pattern 2: Thin Wrapper / Zero Delta — (inferred from marketplace skills)

**What's wrong:** Skills that duplicate what the model already knows. Example: A "JavaScript" skill that explains what `const` does.

**How to fix:** Only encode knowledge the model doesn't have: organization-specific conventions, internal tooling, framework quirks not in mainstream docs.

### Anti-Pattern 3: Generic Description — (observed in some skills)

**What's wrong:** Description says "Helps with X" without specific triggers. Agent can't reliably activate.

**Example:** `description: "Database best practices."` — triggers on any database mention, including databases the skill doesn't cover.

**How to fix:** Include specific activation contexts: "Use when writing PostgreSQL queries for Supabase, configuring RLS policies, or optimizing database performance."

### Anti-Pattern 4: Pipeline with No Gates — (observed in community skills)

**What's wrong:** Numbered steps but no enforcement. Agent can skip Phase 3 (evaluation) entirely and go straight to deploy.

**How to fix:** Use mandatory language: "DO NOT proceed to Phase 4 until Phase 3 evaluation thresholds are met."

---

## Deliverable 5: Gap Analysis

### Missing Patterns

- **Inversion:** No collected skill demonstrates the "agent interviews user before acting" pattern. This is the rarest pattern — likely only appears in skills for high-stakes tasks (security audits, legal document review).
- **Reviewer:** No collected skill has a explicit checklist-based evaluation with scored output. This pattern may exist in code-review skills from Sentry or similar.

### Underrepresented Patterns

| Pattern | Exemplars Found | Notes |
|---|---|---|
| Tool Wrapper | 4 (Vercel x2, Supabase, Google ADK) | Well-represented in official sources |
| Pipeline | 1 (Google ADK) | Rare — requires strict phase discipline |
| Generator | 0 | Not found in Tier 1 |
| Reviewer | 0 | Not found in Tier 1 |
| Inversion | 0 | Not found in Tier 1 |

### Domain Gaps

Based on collected sources:

| Domain | Status |
|---|---|
| Actuarial modeling | No skills found |
| Multi-agent orchestration governance | Google ADK touches this but not explicit |
| Repository health monitoring | Not in Tier 1 |
| Document generation pipelines | Anthropic has docx/pdf but as monolithic blobs |
| Infrastructure-as-code | Not in Tier 1 |
| Legal/compliance | Not found |

---

## Deliverable 6: Skill Authoring Cheatsheet

### Decision Tree: Which Pattern?

| I want to build... | Use Pattern |
|---|---|
| On-demand domain knowledge the agent consumes as reference | **Tool Wrapper** |
| Structured output from a reusable template | **Generator** |
| Scored evaluation against a checklist | **Reviewer** |
| Agent gathers context before producing output | **Inversion** |
| Sequential workflow with explicit gates | **Pipeline** |

### Token Budget Guidelines

| Pattern | SKILL.md | References/Assets/Scripts |
|---|---|---|
| Tool Wrapper | <100 lines (routing index) | Primary knowledge location |
| Generator | ~100 lines (orchestration) | `assets/` for template, `references/` for style guide |
| Reviewer | ~100 lines (protocol) | `references/` for checklist |
| Inversion | ~150 lines (question phases) | Optional `references/` for phase templates |
| Pipeline | ~200 lines (workflow + gates) | Can delegate to sibling skills |

### Description Field Template

```yaml
description: >
  [What the skill does]. Use when [specific trigger contexts].
  Triggers on tasks involving [keywords].
  Do NOT use when [exclusions].
```

**Example:**
```yaml
description: >
  React composition patterns for scalable components.
  Use when refactoring components with boolean prop proliferation,
  building flexible component libraries, or designing reusable APIs.
  Triggers on compound components, context providers, or component architecture.
  Do NOT use when working with Vue or Angular.
```

### Gate Condition Templates

**Pipeline Gates:**
```
## Phase N: [Name]

[Steps...]

**GATE:** Do NOT proceed to Phase N+1 until [condition].
```

**Example:**
```
**GATE:** Do NOT proceed to Phase 4 (Deploy) until:
- Phase 3 evaluation thresholds are met (see /adk-eval-guide)
- You have received explicit human approval
```

### The Three Most Common Structural Mistakes

1. **Monolithic SKILL.md** — Put all domain knowledge in `references/`, keep SKILL.md as routing (<100 lines)
2. **Vague triggers** — Include specific activation contexts in description, not generic "helps with X"
3. **No enforcement** — Use mandatory language ("MANDATORY:", "DO NOT proceed until") for critical gates

---

## Provenance

All skills collected from publicly accessible GitHub repositories:

| Skill | Source Repo | Commit | License |
|---|---|---|---|
| vercel-composition-patterns | github.com/vercel-labs/agent-skills | 64484e9a6022c81e3af59f5dcee6fb6d631bf53e | MIT |
| vercel-react-best-practices | github.com/vercel-labs/agent-skills | 64484e9a6022c81e3af59f5dcee6fb6d631bf53e | MIT |
| supabase-postgres-best-practices | github.com/supabase/agent-skills | 760460c221d30d0db904ff28e8fa52af85672255 | MIT |
| google-adk-dev-guide | github.com/google/adk-docs | 50732c99da53c723591adb8056783ac6a294b3f3 | Apache 2.0 |
| anthropic-pdf | github.com/anthropics/skills | 887114fd09f8f24a7e6c907f9ee505348498ab6a | Proprietary (per skill) |

**Security screening:** All skills passed security review. No prompt injection, exfiltration, or suspicious network calls detected.
