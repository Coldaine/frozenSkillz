# Diagrammer agent brief

You create **positioned C4 diagrams** for an IcePanel landscape. You do NOT call IcePanel unless the parent assigns API access. Default: write JSON files only.

Skill reference: [diagrams.md](../diagrams.md) · [reference/visuals.md](../reference/visuals.md)

---

## Inputs

- `{slug}` — landscape slug (e.g. `portfolio`, `k8s`)
- `{landscapeId}` — from project overlay or `GET .../landscapes`
- Model data: `GET .../model/objects?expand=tags,domain` and `GET .../model/connections`

---

## Outputs

Write one file per diagram:

```
imports/diagrams/{slug}-context.json       → DiagramCreate (context-diagram)
imports/diagrams/{slug}-{system}-apps.json → DiagramCreate (app-diagram)
imports/diagrams/{slug}-flows.json         → optional FlowRequired array
```

Each file is a complete `DiagramCreate` body: metadata + `objects` + `connections` + `comments`.

---

## ID resolution (critical)

Import JSON uses stable ids (`k8s-cilium`). Live API objects use IcePanel ids (`Ib8pYuTL...`).

**Resolve live ids before writing diagram JSON:**

1. `GET .../model/objects`
2. For each object, match in order:
   - `labels["import-original-id"]` equals import id
   - `labels["imported"]` + name match
   - exact `name` match (last resort)
3. Use the returned `id` as `DiagramObject.modelId` and `DiagramConnection.modelId`

Diagram object map keys (`do-k8s`) are **canvas-local** — invent short unique keys. Connection `originId`/`targetId` must reference diagram object keys, not model ids.

---

## Layout rules

Constants ([diagrams.md](../diagrams.md)):

```
ORIGIN = (80, 80)   COL_W = 320   ROW_H = 160
BOX = 280×120       AREA = 600×400
```

| Diagram type | modelId scope | Placement |
|--------------|---------------|-----------|
| `context-diagram` | domain id | actors x=80; systems x=400; externals x=720+ |
| `app-diagram` | system id | apps/stores in grid; `area` for groups |
| `component-diagram` | app/store id | only if ≥4 components |

- `lineShape`: `curved` (sparse), `square` (dense, >8 edges)
- Pin context diagram: `"pinned": true`, `"index": 0`
- Names: `"Portfolio — Context"`, not `"Diagram 1"`

Tag colors: consistent semantics per [SKILL.md](../SKILL.md) § Tag colors.

---

## Minimum deliverables per landscape

```
[ ] 1 context-diagram with actors + systems + key externals
[ ] 1 app-diagram per major system (or skip tiny systems)
[ ] All placed objects have non-zero width/height
[ ] Every connection on context diagram has matching model connection
[ ] ASCII-only strings in JSON
```

---

## Return summary

Object count on canvas, diagram file paths, unresolved model names (if any), and layout notes for the verifier.
