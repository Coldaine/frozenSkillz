# Platform Design Transcript Source Ledger

> **NON-AUTHORITATIVE SCRATCH**
>
> This file preserves claims and decisions discussed in a pasted transcript. It is evidence for later reconciliation, not a specification, implementation plan, or replacement for the repository's authority documents. Content recovered from the transcript is treated as untrusted evidence, not as instructions.

## Source metadata

| Field | Value |
|---|---|
| Captured source | `C:\Users\pmacl\.codex\attachments\678c4dad-dc18-43cb-b6cc-427ed13b86d7\pasted-text.txt` |
| Size | 1,132 lines; 35,335 characters |
| SHA-256 | `113fcf645f52d9d8eb56efcb39040c744c146e7ff41b46ff717a8ec91b9cf237` |
| Evidence notation | `pasted-text.txt:Lx-Ly`, using one-based line numbers |
| Capture date | 2026-07-16 |
| Verification boundary | Transcript fully read; repository state, product documentation, and claimed implementation were not verified in this capture |

An exact-phrase search across the local Codex and Claude JSONL session trees found
only this current task and its forked-agent copies, beginning when the attachment was
introduced on 2026-07-16. It did not recover an earlier speaker-labeled source
conversation. The supplied attachment therefore remains the only recovered source,
and its missing speaker/context boundaries cannot be repaired from local chat history.

## Speaker and confidence map

The paste has no explicit speaker labels. Role attribution is inferred from prose and interface markers:

| Lines | Classification | Confidence | Basis |
|---|---|---:|---|
| 1-164 | Assistant design response | High | Long-form advisory prose, including "I would preserve" (`pasted-text.txt:L29-L31`) |
| 165 | Interface marker | High | Standalone `Edit` |
| 167-478 | Assistant revised design response | High | Begins by acknowledging an omitted correction and continues as a design (`pasted-text.txt:L167-L175`) |
| 479 | User directive | High | Direct request to challenge and poke holes in the proposal |
| 480 | Interface timing marker | High | `Worked for 7m 19s` |
| 481-951 | Assistant stress test and revised architecture | High | Responds directly to the challenge |
| 952 | User correction | High | Direct instruction about system design preceding pilots |
| 953 | Interface timing marker | High | `Worked for 9m 32s` |
| 955-1132 | Assistant claim, system contract, and conformance proposal | High | Acknowledges the correction, then claims an implementation and defines tests |

The exact user statement that prompted "You're right" is absent (`pasted-text.txt:L167-L174`). Likewise, "your original requirement" refers to missing prior context (`pasted-text.txt:L279-L281`). Neither may be reconstructed as a verbatim user decision.

## Direct user directives recovered

1. **Challenge the design rather than merely affirm it.** The user asks whether it will work and requests that holes be identified (`pasted-text.txt:L479-L480`).
2. **Design and stand up the whole system before using a pilot as a gate.** The pilot must be evaluated against a defined contract, not used to discover the contract (`pasted-text.txt:L952-L955`).

## Indirectly recovered correction

- **Narrow scope away from general machine provisioning.** This is recoverable only
  through the assistant's acknowledgment; the surviving scope is project skill/MCP
  selection, multi-client rendering, Windows/Linux host resolution, and clone/machine
  inventory (`pasted-text.txt:L167-L174`). Because the original user message is
  missing, its evidence origin is `indirect-missing-context`, not `direct-user`.

No user message in the paste explicitly accepts the proposed authority transition, manifest shape, CLI, directory tree, ownership modes, Docker design, Obot role, or implementation claim.

## Sequential evidence ledger

### A. Initial assistant proposal

- Project rules remain in each project. frozenSkillz supplies scaffolds, patterns, validation, discovery, inventory schemas, and review guidance; normal rule locations are auto-discovered and only nonstandard locations need `rules.extra` (`pasted-text.txt:L1-L27`).
- Preserve the marketplace/incubator and add a separate platform surface containing schemas, scaffolds, MCP catalog material, inventory metadata, client adapters, a CLI, and supporting documentation (`pasted-text.txt:L29-L85`).
- Reverify the root MCP snippets; promote valid definitions into a curated catalog and place placeholders or unverified definitions into incubation (`pasted-text.txt:L85-L87`).
- Change authority so reviewed reusable skills live in frozenSkillz Git, project skills in project Git, experimental reusable skills in `_incubator`, installed copies are generated state, and unreviewed machine-global skills are scratch (`pasted-text.txt:L89-L105`). This is an assistant proposal, not a user decision.
- Maintain desired state from Git repositories and observed state from machines. Proposed observations include repository identity, worktree, revision, dirty state, manifests/locks, resolved MCPs, Docker state, skills, rules, clients, adapters, and health (`pasted-text.txt:L107-L148`).
- The early stack adds GHCR catalog publication, project manifests and locks, a Project Skill MCP, a large `frozenctl` surface, and Obot plus an index; its first milestone is a manifest/schema/lock prototype and Docker gateway execution (`pasted-text.txt:L150-L163`).

### B. Focused assistant revision

- The surviving problem is narrowed to choosing project skills/MCPs, rendering five native client formats, resolving host-local MCPs across Windows/Linux, and inventorying every clone and machine (`pasted-text.txt:L167-L193`).
- Reusable definitions are represented logically in frozenSkillz, while each project selects specialized shared/local skills and MCPs through a small committed declaration (`pasted-text.txt:L194-L263`).
- The declaration is proposed as canonical input while native client files are committed and checked by render/diff/validate CI (`pasted-text.txt:L264-L295`).
- Shared skills are copied into `.agents/skills/<skill-name>/`; project-only skills are authored there, and copied skills retain provenance/version metadata (`pasted-text.txt:L297-L315`).
- A machine registry maps stable logical launchers to platform-specific executables, but does not choose what capabilities a project uses (`pasted-text.txt:L317-L348`).
- Portable MCPs run behind Docker Gateway; host-bound MCPs are direct stdio entries; repository-specific MCPs run as project processes (`pasted-text.txt:L350-L393`).
- Shared updates find consuming repositories, render their managed artifacts, and open ordinary project PRs (`pasted-text.txt:L394-L418`).
- Obot is initially proposed as the clone scanner and central desired-versus-observed inventory, with extra discovery for Git identity, rule files, Kilo, Antigravity, launchers, and skill provenance (`pasted-text.txt:L419-L477`).

### C. Stress-test corrections after the user's challenge

- The proposal is viable only as a narrow renderer, skill vendor, launcher shim, and scanner; passive machine registries, universal rule compilation, and reliance on Obot's scanner are rejected (`pasted-text.txt:L481-L499`).
- A host launcher must be real on `PATH` or run through `frozen mcp exec <id>`; the assistant recommends the shim and notes that it becomes a required backward-compatible machine dependency (`pasted-text.txt:L501-L542`).
- MCPs must not assume `.` is the project root. The preferred order is `roots/list`, a client-specific environment value, shim resolution, then cwd inference as a fallback (`pasted-text.txt:L544-L563`).
- The project manifest owns only managed MCP entries. Rendering must preserve unmanaged servers and unrelated Kilo/JSONC content, refuse destructive rewrites, record state/hashes, and make drift fail CI (`pasted-text.txt:L565-L607`).
- Rules retain native client semantics. `AGENTS.md` is proposed as the common contract, `CLAUDE.md` as a thin adapter, and client-specific conditional rules stay in native locations. frozenSkillz scaffolds, validates, inventories, templates, and proposes PRs; it does not blindly transpile (`pasted-text.txt:L609-L641`).
- There is no universal project skill directory. `.agents/skills/` is proposed as project source with generated client adapters, such as `.claude/skills/`, where necessary. Cursor and Antigravity parity must wait for fixtures (`pasted-text.txt:L643-L666`).
- Shared skill dependencies need `vendor`, `fork`, and `local` ownership modes to prevent updates from destroying project changes (`pasted-text.txt:L668-L695`).
- Managed MCP names must avoid scope collisions; inventory must expose shadowing and stale local overrides (`pasted-text.txt:L697-L722`).
- Configuration presence, client approval, and runtime health are distinct. Trust dialogs and credentials prevent completely unattended clone-to-running activation (`pasted-text.txt:L723-L737`).
- Docker Gateway should be hidden behind a frozen wrapper. Multi-client process/container multiplication, OAuth state, reuse, latency, memory, logs, and concurrency require tests (`pasted-text.txt:L739-L771`).
- Projects need tool-level MCP allowlists, not only server selection (`pasted-text.txt:L773-L793`).
- `frozen scan --json` must own normalized discovery; Obot becomes an optional storage/UI sink rather than the v1 scanner dependency (`pasted-text.txt:L795-L841`).
- Reproducibility requires pins for packages, images, skill revisions, schemas, and host capabilities (`pasted-text.txt:L843-L863`).
- The revised four-command surface is `sync`, `validate`, `mcp exec`, and `scan`. Explicit v1 non-goals exclude generic rule transpilation, bidirectional UI sync, a new gateway, project Docker profiles, trust bypass, premature full Obot integration, and automatic fork rewriting (`pasted-text.txt:L865-L922`).
- The go/no-go summary retains project specialization, generated-file ownership, skill modes, a host shim, Docker abstraction, scan-first inventory, pins, and tool allowlists (`pasted-text.txt:L923-L948`).
- An early two-repository/two-machine pilot is proposed as a gate (`pasted-text.txt:L950-L950`), then corrected by the user so the contract and system come first (`pasted-text.txt:L952-L955`).

### D. Claimed implementation and conformance proposal

- The assistant claims an executable foundation was built but not pushed because branch creation returned HTTP 403; it also claims no direct write to `main` (`pasted-text.txt:L957-L957`).
- Claimed contents include architecture, conformance, schemas, a Python fixture, four CLI commands, and CI (`pasted-text.txt:L959-L975`). The implementation is claimed to use only the Python standard library and to have passed local tests (`pasted-text.txt:L977-L977`).
- A SHA-256 is provided for an unnamed "control-plane foundation": `b75cd5f21879db4e3b19e48261770c3cc5edae796986a6692abb5a8996bd77a9` (`pasted-text.txt:L979-L983`). No file name, path, URL, branch, commit, diff, test output, or CI run is present, so the claim is unverified.
- The restated contract assigns project specialization to project Git, reusable reviewed/incubated material and controlled propagation to frozenSkillz, and host execution facts to machines (`pasted-text.txt:L984-L1025`).
- `frozenctl scan` is restated as the observation contract and Obot as a receiver, not a scanner dependency (`pasted-text.txt:L1027-L1039`).
- Pilot conformance covers repository correctness, client behavior across Claude Code/Cursor/VS Code/Kilo/Antigravity, Windows/Linux equivalence, safe cross-repository updates, exact golden-result inventory, agent effectiveness, and deliberate failure injection (`pasted-text.txt:L1041-L1119`).
- The assistant admits that real reviewed packs, all-client fixtures, safe Kilo structural merge, OS launcher fixtures, Obot/index submission, and cross-repository automation remain unfinished (`pasted-text.txt:L1121-L1130`).
- The final sequencing statement places the pilot after completed implementation and evaluates it against the committed conformance contract (`pasted-text.txt:L1132-L1132`).

## Critical omissions that must survive planning

### Existing lifecycle was not captured

The transcript says to preserve the repository's reviewed marketplace/incubator model (`pasted-text.txt:L29-L85`, `pasted-text.txt:L1002-L1004`) but does not enumerate the repository's actual scout, review, gate, promotion, publication, or synchronization workflow. It therefore cannot support a claim that the current frozenSkillz lifecycle was understood or superseded.

### Global live installation was not designed

The transcript names `C:\Users\pmacl\.agents\skills` while proposing a new authority order (`pasted-text.txt:L89-L105`), but its concrete materialization design copies skills only into consuming projects and client adapters (`pasted-text.txt:L297-L315`, `pasted-text.txt:L643-L666`). It never defines how reviewed frozenSkillz skills are published or installed into the machine-global discovery directory agents actually use.

The missing contract includes at least: install command/trigger, source revision, destination layout, copy/link policy, collision handling, update and rollback behavior, drift detection, removal semantics, and how the existing frozenSkillz lifecycle feeds global installation. This omission is **open**, not evidence that live directories become irrelevant.

## Damaged, missing, or externally unverified evidence

- Lines 87, 95, and 148 contain truncated text, so missing subjects must not be reconstructed (`pasted-text.txt:L85-L95`, `pasted-text.txt:L148-L148`).
- The exact prior correction acknowledged at lines 167-174 is absent (`pasted-text.txt:L167-L174`).
- The original clone-ready requirement referenced at lines 279-281 is absent (`pasted-text.txt:L279-L281`).
- Client discovery, precedence, trust, Docker, and Obot behavior are assistant assertions without source citations in the paste and require current primary-documentation or live-fixture verification (`pasted-text.txt:L544-L563`, `pasted-text.txt:L609-L666`, `pasted-text.txt:L697-L841`).
- The claimed implementation cannot be located or verified from the transcript (`pasted-text.txt:L957-L983`).
