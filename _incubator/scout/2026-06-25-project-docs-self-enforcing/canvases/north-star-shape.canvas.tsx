import { Stack, Row, Card, CardHeader, CardBody, H1, H2, H3, Text, Pill, Callout, Divider, Grid, Table, Stat } from "cursor/canvas";
export default function NorthStarShape() {
  return (
    <Stack gap={16}>
      <H1>NORTH_STAR: what stays, what goes</H1>
      <Text tone="secondary">
        The skill prescribes six sections. The thesis here: keep three, demote one, delete one, rework the opener and
        goals. Goal is identity + the problem + side-quest guardrails, read by every agent every session — nothing
        prescriptive.
      </Text>

      <Grid columns={4} gap={10}>
        <Pill tone="success" active>KEEP / REWORK</Pill>
        <Pill tone="warning" active>DEMOTE</Pill>
        <Pill tone="danger" active>DELETE</Pill>
        <Pill tone="info" active>CONDITIONAL</Pill>
      </Grid>

      {/* OPENER — reworked */}
      <H2>1. The Opener — one or two lines, problem first</H2>
      <Callout tone="danger" title="The skill's bug">
        The skill offers three opener shapes — Bet / Why-This-Exists / The-Goal. Agents glom onto "The Bet" because it
        sounds dramatic and apply it to everything. But The Bet is the LEAST common shape, valid only for
        spike/experimental repos. Worse, they misread it as a commercial get-rich-quick framing. The default should be
        Problem → Solution.
      </Callout>

      <Card>
        <CardHeader trailing={<Pill tone="success" size="sm">rework</Pill>}>The default shape: Problem → Solution</CardHeader>
        <CardBody>
          <Text weight="semibold">Form:</Text>
          <Text>"I have problem Y. This is [thing] to solve Y."</Text>
          <Divider />
          <Text weight="semibold">Why this is the default:</Text>
          <Text>It does two jobs the current skill underplays. (1) It states the problem explicitly — the "why it exists" that NORTH_STAR currently leaves implied. The problem is the most load-bearing piece of identity: it's what stops a side quest ("does this serve solving problem Y?"). (2) It names the thing. Two lines, both earning their place.</Text>
          <Divider />
          <Text weight="semibold">MooseGoose example:</Text>
          <Text>"Patrick's technical life is scattered across home-app, refs, and half-finished tools, none reachable in one place. MooseGoose Studio is a single-owner private console that consolidates it behind one gate."</Text>
        </CardBody>
      </Card>

      <H3>The three opener shapes — renamed and ranked by frequency</H3>
      <Grid columns={3} gap={10}>
        <Card>
          <CardHeader trailing={<Pill tone="success" size="sm">default</Pill>}>Problem → Solution</CardHeader>
          <CardBody>
            <Text size="small">"I have problem Y. This is X to solve Y."</Text>
            <Divider />
            <Text size="small" tone="secondary">Most common. States the problem and the thing. Use unless you have a reason not to.</Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader trailing={<Pill tone="warning" size="sm">gap-closer</Pill>}>Why This Exists</CardHeader>
          <CardBody>
            <Text size="small">"No good X exists for Y. This fills that gap."</Text>
            <Divider />
            <Text size="small" tone="secondary">Use when the problem is an absence in the world, not a personal pain. Implies the problem but states it less directly than Problem→Solution.</Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader trailing={<Pill tone="danger" size="sm">spike-only</Pill>}>The Hypothesis (was "The Bet")</CardHeader>
          <CardBody>
            <Text size="small">"We suspect X produces Y without Z. This repo tests that."</Text>
            <Divider />
            <Text size="small" tone="secondary">Rename of "The Bet." Valid ONLY for spike/experimental repos. The old name invited agents to treat every repo as a high-stakes commercial wager. Restricted, not default.</Text>
          </CardBody>
        </Card>
      </Grid>

      {/* GOALS — new guidance */}
      <H2>2. Goals — a guiding light, not validation</H2>
      <Card>
        <CardHeader trailing={<Pill tone="success" size="sm">keep — with guidance</Pill>}>One or two. Read every session. Never checked off.</CardHeader>
        <CardBody>
          <Text weight="semibold">The principle:</Text>
          <Text>Goals are a compass bearing, not a destination. They shape every decision an agent makes; they are never a test suite. The skill's "Requirements" section (how you'll recognize progress) is goals-as-validation and gets deleted. Goals themselves stay, but get real guidance — the skill never explains how to write one.</Text>
          <Divider />
          <Text weight="semibold">What goals are NOT:</Text>
          <Stack gap={4}>
            <Text size="small">— Not requirements. No "how you'll recognize progress." That's validation.</Text>
            <Text size="small">— Not a backlog. A goal that needs more than a sentence is a plan; plans live in docs/plans/.</Text>
            <Text size="small">— Not implementation. "Use Postgres" is architecture, not a goal.</Text>
            <Text size="small">— Not a checklist item. If you can tick it off, it was a task, not a guiding light.</Text>
          </Stack>
        </CardBody>
      </Card>

      <H3>Goal shapes — examples of what a one-line goal can be</H3>
      <Grid columns={2} gap={10}>
        <Card>
          <CardHeader>Direction goal</CardHeader>
          <CardBody>
            <Text size="small" italic>"Make MooseGoose the one place Patrick's technical life lives."</Text>
            <Divider />
            <Text size="small" tone="secondary">A compass bearing. Never "done," always shapes decisions. Most common goal shape.</Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>Problem-echo goal</CardHeader>
          <CardBody>
            <Text size="small" italic>"Consolidate scattered tools behind one owner gate."</Text>
            <Divider />
            <Text size="small" tone="secondary">Restates the opener's problem as the standing thing to solve. Pairs naturally with Problem→Solution opener.</Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>Quality-bar goal</CardHeader>
          <CardBody>
            <Text size="small" italic>"Every owner-only route is reachable, or has a documented reason it's hidden."</Text>
            <Divider />
            <Text size="small" tone="secondary">A bar to clear on every piece of work, not a one-time task. Ongoing by design.</Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>User-outcome goal</CardHeader>
          <CardBody>
            <Text size="small" italic>"Patrick can run his day from one authenticated surface."</Text>
            <Divider />
            <Text size="small" tone="secondary">Names the caller and what they get. Works when the opener's Caller is concrete.</Text>
          </CardBody>
        </Card>
      </Grid>
      <Callout tone="neutral" title="Refusal goals belong in Anti-Goals">
        "Not X, not Y" is a goal shape, but it lives in the Anti-Goals section, not here — and only when earned (see
        section 3). Don't duplicate a refusal as a goal and an anti-goal.
      </Callout>

      {/* IN/OUT/SHAPE */}
      <H2>3. In / Out / Shape — the contested section</H2>
      <Text>The skill bundles four one-liners. Split them: two conditional in NORTH_STAR, two demoted.</Text>
      <Grid columns={2} gap={12}>
        <Card>
          <CardHeader trailing={<Pill tone="info" size="sm">conditional</Pill>}>In / Out — only if caller + Out are concrete</CardHeader>
          <CardBody>
            <Text weight="semibold">What they are:</Text>
            <Text>Scope filters. "In: owner's work + tools. Out: a thin public portfolio, nothing else."</Text>
            <Divider />
            <Text weight="semibold">Conditional rule:</Text>
            <Text>Include In/Out ONLY when the project has a clear caller and a clear delivered Out. For platforms, infra, languages, or abstract-caller systems, In/Out degrade into tautology — omit them rather than force filler. In/Out/Shape as a full four-liner is a plan/epic-scoping tool, not a universal identity section.</Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader trailing={<Pill tone="warning" size="sm">demote to architecture</Pill>}>Shape / Caller</CardHeader>
          <CardBody>
            <Text weight="semibold">What they are:</Text>
            <Text>Delivery mechanism. "Next.js pod on K8s behind Cloudflare Tunnel."</Text>
            <Divider />
            <Text weight="semibold">Why demote:</Text>
            <Text>Prescription masquerading as identity. If delivery changes, NORTH_STAR changes — but NORTH_STAR should be the slowest-moving doc. Invites the agent to infer implementation ("K8s → reach for Helm"), the prescription-creep failure.</Text>
          </CardBody>
        </Card>
      </Grid>
      <Callout tone="info" title="The split rule">
        In/Out answer "does this belong here?" (scope, permissive). Shape/Caller answer "how is it delivered?"
        (prescription, downstream). Identity holds scope; architecture holds delivery. If you can't fill In/Out
        concretely, that signals the thing isn't a product with a caller — it's a platform/spec/layer needing a
        different identity shape.
      </Callout>

      <H3>Empirical test — 12 of your projects, In/Out/Shape/Caller attempted on each</H3>
      <Table
        headers={["Project", "Verdict", "Why it held / broke"]}
        rows={[
          ["MooseGooseWebsite", <Pill tone="success" size="sm">HOLDS</Pill>, "Single owner, one gate, crisp In/Out + public/private boundary"],
          ["coldaine-k8cluster", <Pill tone="warning" size="sm">DEGRADES</Pill>, "GitOps platform: \"repo is source of truth\" is Shape; rest is tautology"],
          ["ColdSearch", <Pill tone="success" size="sm">HOLDS</Pill>, "Clear caller + distinctive Out (normalized + raw + cache + provenance)"],
          ["ColdVault", <Pill tone="success" size="sm">HOLDS</Pill>, "Crisp In→Out contract: govern access, never hold values"],
          ["ColdTools", <Pill tone="danger" size="sm">COLLAPSES</Pill>, "Umbrella monorepo, no caller, no Out beyond \"tools in one place\""],
          ["llm-archiver", <Pill tone="warning" size="sm">THIN</Pill>, "Scheduler/cron is the real caller = \"every process\" anti-pattern"],
          ["TokenRouter", <Pill tone="success" size="sm">HOLDS</Pill>, "Specific caller + contract-shaped Out"],
          ["NorthStarGuardian", <Pill tone="success" size="sm">HOLDS</Pill>, "Specific caller + contract-shaped Out"],
          ["agent-control-plane", <Pill tone="danger" size="sm">COLLAPSES</Pill>, "Empty scaffold, no product yet"],
          ["HermesStart", <Pill tone="danger" size="sm">COLLAPSES</Pill>, "Configuration/starter, not a product"],
          ["ComfyUI", <Pill tone="success" size="sm">HOLDS</Pill>, "Specific caller + contract-shaped Out"],
          ["WoWshipExport", <Pill tone="success" size="sm">HOLDS</Pill>, "Specific caller + contract-shaped Out"],
        ]}
      />
      <Grid columns={4} gap={10}>
        <Stat value="7" label="HOLDS" tone="success" />
        <Stat value="1" label="THIN" tone="info" />
        <Stat value="1" label="DEGRADES" tone="warning" />
        <Stat value="3" label="COLLAPSES" tone="danger" />
      </Grid>
      <Callout tone="success" title="The data confirms the conditional rule">
        7/12 (58%) genuine holds — below the skill's claimed ~70%. The framework fits products with a specific caller
        and a contract-shaped Out. It breaks on platforms (coldaine-k8cluster), umbrella repos (ColdTools),
        scheduler-initiated pipelines (llm-archiver), configurations (HermesStart), and empty scaffolds
        (agent-control-plane). Verdict: make In/Out/Shape/Caller a CONDITIONAL NORTH_STAR section gated on a Caller
        test, not mandatory. For platforms, defer to \"source-of-truth\" / \"one-line test\" framing. Repurpose the
        four-liner as a per-epic scoping tool for ambiguous cases.
      </Callout>

      {/* ANTI-GOALS — inverted */}
      <H2>4. Anti-Goals — inverted: default is zero</H2>
      <Card>
        <CardHeader trailing={<Pill tone="success" size="sm">keep — but invert the rule</Pill>}>What this product must NOT turn into</CardHeader>
        <CardBody>
          <Text weight="semibold">Skill's rule:</Text>
          <Text>"At least one from day one; more accrete." — Inverted. That rule invites agents to fabricate anti-goals out of thin air to feel thorough.</Text>
          <Divider />
          <Text weight="semibold">Inverted rule:</Text>
          <Text>Default is ZERO anti-goals. Absence is the healthy state, not a gap to fill. An anti-goal is EARNED: you write one only when you can point to a specific, observed, recurring case of the project being mistaken for X. No evidence, no anti-goal.</Text>
          <Divider />
          <Text weight="semibold">Identity-level only:</Text>
          <Text>"Not a marketing site. Not a multi-user SaaS." Good — those are identity drift. "Must not use Redis" is a prescription hiding in an anti-goal — it belongs in conventions, where it can change without touching identity.</Text>
        </CardBody>
      </Card>
      <Callout tone="danger" title="The minor-rule-explosion guard (the rule the skill is missing)">
        Fabricated anti-goals are the primary way minor rules become major ones — they get written into the
        highest-authority doc on a hunch. The guard: an anti-goal must be identity-level ("not a SaaS"), never
        implementation-level ("must not use Redis"). If you can't point to a real time this project was mistaken for
        X, do not write an anti-goal about X.
      </Callout>

      {/* PILLARS */}
      <H2>5. Pillars — keep, conditional</H2>
      <Card>
        <CardHeader trailing={<Pill tone="info" size="sm">conditional</Pill>}>Tradeoff statements, earned only</CardHeader>
        <CardBody>
          <Text weight="semibold">Skill's rule:</Text>
          <Text>"Only when the owner has hit a real tradeoff. Zero pillars is better than three plausible-sounding ones the owner didn't choose."</Text>
          <Divider />
          <Text weight="semibold">Why correct:</Text>
          <Text>The ONE place prescription-adjacent content is allowed, and only as a tradeoff ("accept cost X for benefit Y"), not a directive. Survives the self-enforcing test: a future agent reads "we accept slower builds for reproducibility" and makes consistent downstream choices.</Text>
        </CardBody>
      </Card>

      {/* DELETIONS */}
      <H2>What gets deleted from the skill's NORTH_STAR</H2>
      <Grid columns={2} gap={12}>
        <Card>
          <CardHeader trailing={<Pill tone="danger" size="sm">delete</Pill>}>Requirements (Goals-as-validation)</CardHeader>
          <CardBody>
            <Text>The skill pairs Goals with "how you will recognize progress toward a goal." That is validation. Goals are a guiding light — read every session, shape decisions, never checked off. Requirements turns NORTH_STAR into a test suite.</Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader trailing={<Pill tone="danger" size="sm">delete</Pill>}>Goals-as-backlog</CardHeader>
          <CardBody>
            <Text>The skill allows Goals to accrete as a list. Goals are the opener's shadow — at most one or two guiding-light statements. A goal needing more than a sentence is a plan; plans live in docs/plans/.</Text>
          </CardBody>
        </Card>
      </Grid>

      {/* RESULTING SHAPE */}
      <H2>Resulting NORTH_STAR shape</H2>
      <Card>
        <CardHeader>The minimal self-enforcing identity doc</CardHeader>
        <CardBody>
          <Stack gap={10}>
            <Row gap={8} align="center"><Pill tone="success" size="sm">1</Pill><Text><Text weight="semibold">Opener</Text> — one or two lines, Problem→Solution default. States the problem and names the thing.</Text></Row>
            <Row gap={8} align="center"><Pill tone="success" size="sm">2</Pill><Text><Text weight="semibold">Goals</Text> — one or two guiding-light lines. Direction / problem-echo / quality-bar / user-outcome. Never validation.</Text></Row>
            <Row gap={8} align="center"><Pill tone="info" size="sm">opt</Pill><Text><Text weight="semibold">In / Out</Text> — conditional, only if caller + Out are concrete. Omit rather than force filler.</Text></Row>
            <Row gap={8} align="center"><Pill tone="success" size="sm">3</Pill><Text><Text weight="semibold">Anti-Goals</Text> — default zero. Earned only by observed mistaken-for cases. Identity-level only.</Text></Row>
            <Row gap={8} align="center"><Pill tone="info" size="sm">opt</Pill><Text><Text weight="semibold">Pillars</Text> — only if a real tradeoff has been made.</Text></Row>
            <Divider />
            <Text tone="secondary" size="small">No Requirements. No Shape. No Caller. No goal backlog. No implementation. No fabricated anti-goals. Small enough to be read by every agent every session — enforced by content discipline, not a line count.</Text>
          </Stack>
        </CardBody>
      </Card>

      <Callout tone="neutral" title="What this tees up">
        The opener now carries the problem explicitly (the missing "why it exists"), The Bet is renamed to The
        Hypothesis and restricted to spikes, and goals get real shape guidance. Loop 3's identity gate now reads from
        a small, stable, problem-anchored, non-prescriptive NORTH_STAR. Next move: rewrite the north-star-guide.md to
        this shape, then run the same exercise on the architecture + plans layer where Shape/Caller and build
        sequencing belong.
      </Callout>

      {/* ARCHITECTURE — the next layer */}
      <H2>→ architecture.md (next layer)</H2>
      <Card>
        <CardHeader>The one sentence that has to make it</CardHeader>
        <CardBody>
          <Text weight="semibold">architecture.md is a description of the approach we have chosen to succeed at the goals, and why — NOT an inventory of the things in the project.</Text>
          <Divider />
          <Text weight="semibold">Load-bearing words:</Text>
          <Text>approach + why. A list of components has neither. An approach statement is "we chose X to serve goal Y / solve problem Z, accepting cost W." That's the only thing that makes it self-enforcing — an agent can weigh downstream decisions against it. A component list gives nothing to weigh.</Text>
        </CardBody>
      </Card>

      <Callout tone="danger" title="The skill contradicts itself here">
        The skill's architecture guide names "code inventory creep" as a failure ("architecture.md grows into a
        description of every file") and then MANDATES the structure that causes it: a 5–12 row System Shape table and a
        Major Components table. It warns against inventory and hands you the inventory template. Agents follow the
        instruction, not the principle.
      </Callout>

      <Card>
        <CardHeader>The reframe — thesis-first, not inventory-first</CardHeader>
        <CardBody>
          <Stack gap={6}>
            <Text size="small">— Architecture Thesis (approach + why) IS the document. Everything else exists only as it instantiates the thesis.</Text>
            <Text size="small">— Mention areas/components only when load-bearing for the approach. No mandated tables.</Text>
            <Text size="small">— Rule of thumb (parallel to the In/Out rule): if a component has no "because" tying it to a goal or the problem, it doesn't belong here — it goes in docs/components/ or nowhere.</Text>
            <Text size="small">— Status labels (Current/Planned/Candidate/Deferred) stay — they're approach implementation state.</Text>
            <Text size="small">— Deep per-decision rationale stays in ADRs; architecture.md holds the strategic why.</Text>
          </Stack>
        </CardBody>
      </Card>

      <Callout tone="info" title="Where In/Out/Shape lands when it moves here">
        Shape (and Caller) get exiled from NORTH_STAR and come HERE — because Shape is part of the chosen approach.
        "CLI-first core reusable across service/API/MCP, one stable surface with flexible execution" is an approach
        statement with a why. That's prescription properly seated, not leaking into identity. In/Out stay in NORTH_STAR
        (conditional, when caller + Out are concrete) — that's the scope filter. Clean split: identity holds scope;
        architecture holds the approach + delivery.
      </Callout>

      {/* SKILL + CLI — the synthesis (EXPLORATORY) */}
      <H2>→ skill + CLI: the self-enforcement architecture (EXPLORATORY)</H2>
      <Text tone="secondary">
        Research verdict from spec-kit + bmad-method — EXPLORATORY, not settled. Both build the architecture for
        self-enforcement and stop short of wiring the gate. We may steal the declaration/distribution machinery from
        each and build the part both omitted, but this was being explored, not decided.
      </Text>

      <Card>
        <CardHeader>Both repos agree, and both stop short</CardHeader>
        <CardBody>
          <Table
            headers={["", "spec-kit", "bmad-method", "Sketched skill+CLI"]}
            rows={[
              ["Self-enforcement", <Pill tone="danger" size="sm">D</Pill>, <Pill tone="danger" size="sm">D</Pill>, <Pill tone="success" size="sm">A</Pill>],
              ["Ideas-not-now shelf", <Pill tone="danger" size="sm">F</Pill>, <Pill tone="warning" size="sm">C+</Pill>, <Pill tone="success" size="sm">A</Pill>],
              ["Side-quest prevention", <Pill tone="warning" size="sm">C</Pill>, <Pill tone="success" size="sm">B</Pill>, <Pill tone="success" size="sm">A</Pill>],
              ["Session/agent handoff", <Pill tone="success" size="sm">B</Pill>, <Pill tone="success" size="sm">B+</Pill>, <Pill tone="success" size="sm">A</Pill>],
            ]}
          />
          <Divider />
          <Text size="small">spec-kit: existence-gating + human approval only. bmad: explicitly "soft suggestions, not hard gates." Both have the seam; neither wires it to content.</Text>
        </CardBody>
      </Card>

      <Callout tone="warning" title="Exploratory — not settled">
        The skill+CLI split, the CSV routing graph, the TOML override layer, and the correct-course triage were being
        explored as research input. The user explicitly flagged: "we might have tried to learn too much from bmad and
        spec-kit — that's not settled." The load-bearing output is the NORTH_STAR and architecture.md principles above.
        See session/06-skill-cli-exploration.md for the full research and the open questions to revisit.
      </Callout>

      <Card>
        <CardHeader>Non-negotiable lines — candidate mechanism (exploratory)</CardHeader>
        <CardBody>
          <Text weight="semibold">The failure:</Text>
          <Text size="small">spec-kit's *(mandatory)* markers sit in prose, so agents write them away and the CLI never notices. Same as our "aspirations" line disappearing.</Text>
          <Divider />
          <Text weight="semibold">Candidate fix (from bmad's override layer — stronger than HTML-comment markers):</Text>
          <Stack gap={4}>
            <Text size="small">— Fixed commentary lines live in override.toml, injected at generate + validate. The agent cannot reach them as prose.</Text>
            <Text size="small">— Fill regions (owner-derived content) live in the prose doc, written from interview — no-template insight preserved.</Text>
            <Text size="small">— A gate validates fixed lines are present + unmodified after any edit. Re-emission forced mechanically, not by agent goodwill.</Text>
          </Stack>
          <Divider />
          <Text size="small" tone="secondary">Open question when resuming: is the full skill+CLI build worth it, or does a lighter mechanism (a single validator script + a fixed-lines override file, no full CLI) capture 80% of the value?</Text>
        </CardBody>
      </Card>

      <Callout tone="neutral" title="Resume point">
        The edited ColdSearch NORTH_STAR with Patrick's corrections applied lives at
        examples/coldsearch-north-star.corrected.md — that is where to pick up. The next move is either rewriting the
        north-star-guide.md to this shape, or pressure-testing the architecture principle against a real architecture
        doc (ColdVault or coldaine-k8cluster).
      </Callout>
    </Stack>
  );
}
