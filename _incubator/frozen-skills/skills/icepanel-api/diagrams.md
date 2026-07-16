# Diagrams — layout, connectors, verification

> **The #1 IcePanel pitfall:** model objects exist in the database; the **canvas only renders diagrams**. Zero diagrams = blank UI.

---

## Mental model

```
ModelObject (id: pf-sys-k8s)     ← import / CRUD
        ↓ referenced by modelId
DiagramObject (id: do-k8s)       ← positioned on canvas (x, y, width, height)
        ↓ originId / targetId
DiagramConnection (id: dc-1)     ← visual edge between diagram objects
```

Diagram object **map keys** (`do-k8s`) are independent from model ids (`pf-sys-k8s`). Connections reference diagram object ids, not model ids.

---

## Create diagram

```http
POST /landscapes/{landscapeId}/versions/{versionId}/diagrams
Content-Type: application/json
```

Body: `DiagramCreate` = metadata (`DiagramRequired`) + canvas (`DiagramContentRequired`).

### DiagramRequired

| Field | Req | Notes |
|-------|-----|-------|
| `name` | ✓ | Human label |
| `type` | ✓ | See C4 table below |
| `modelId` | ✓ | Scope: domain, system, app, or store model id |
| `index` | ✓ | 0-based sort among siblings |
| `handleId` | | Stable URL slug |
| `groupId` | | DiagramGroup membership |
| `description` | | |
| `pinned` | | Pin in sidebar |
| `labels` | | Key-value metadata |

Response: `{ diagram, diagramContent }` — save `diagram.id`.

---

## C4 diagram type selection

Official mapping ([Core Concepts — Diagrams](https://developer.icepanel.io/core-concepts/diagrams)):

| type | C4 level | modelId points to | Place on canvas |
|------|----------|-------------------|-----------------|
| `context-diagram` | **Level 1** | `domain` or scoped `system` | actors, systems, external systems |
| `app-diagram` | **Level 2** | `system` | apps, stores, groups |
| `component-diagram` | **Level 3** | `app` or `store` | components |

> Diagrams are *views* — the same model object may appear on multiple diagrams.

One **context-diagram** minimum per landscape. Add **app-diagram** per major system. Add **component-diagram** only when component depth matters.

---

## DiagramObject

| Field | Req | Notes |
|-------|-----|-------|
| `id` | ✓ | Canvas-local id |
| `modelId` | ✓ | Existing ModelObject id |
| `type` | ✓ | Must match model: `actor`, `app`, `group`, `component`, `store`, `system` |
| `shape` | ✓ | `box` or `area` |
| `x`, `y` | ✓ | Top-left position (px) |
| `width`, `height` | ✓ | Size (px) |

Optional: `parentId` (nest inside area), `collapsed`, `color` overrides are UI-only in some contexts — prefer tag colors on model.

### Shapes

| shape | type | Visual |
|-------|------|--------|
| `box` | actor, app, system, store, component | Standard node |
| `area` | group | Dashed boundary — place children inside bounds |

---

## DiagramConnection

| Field | Req | Notes |
|-------|-----|-------|
| `id` | ✓ | Canvas-local id |
| `modelId` | ✓ | ModelConnection id |
| `originId` | ✓ | DiagramObject id (source) |
| `targetId` | ✓ | DiagramObject id (target) |
| `lineShape` | ✓ | `curved`, `straight`, `square` |
| `originConnector` | ✓ | See connector grid |
| `targetConnector` | ✓ | See connector grid |
| `labelPosition` | ✓ | 0.0–1.0 along edge |
| `points` | ✓ | Array (often `[]`; API fills if empty) |

---

## Connector grid (12 anchors)

```
top-left    top-center    top-right
left-top                  right-top
left-middle               right-middle
left-bottom               right-bottom
bottom-left bottom-center bottom-right
```

**Heuristic:** left column objects use `right-middle` out, `left-middle` in. Top-to-bottom flows: `bottom-center` → `top-center`.

---

## Layout algorithms

### Grid (default — fast, good enough)

```
Constants:
  ORIGIN = (80, 80)
  COL_W  = 320
  ROW_H  = 160
  BOX    = 280 × 120
  AREA   = 600 × 400

Column 0 (x=80):   actors
Column 1 (x=400):  primary systems / apps
Column 2 (x=720):  external / downstream

Row i: y = 80 + i * ROW_H
```

### Context diagram template

```
[Actor]  ----→  [System A]
               [System B]
               [System C]
```

Place actor at (80, 200). Stack systems vertically at x=400.

### App diagram with area

1. Create `area` for each `group` model object first (large bounds)
2. Place child apps/stores inside area coordinates
3. Add connections last (so labels don't overlap nodes)

### Dense graphs

- Switch `lineShape` to `square`
- Increase `labelPosition` offset on parallel edges (0.3 vs 0.7)
- Split into two diagrams rather than overcrowding one

---

## Update layout (incremental)

```http
PATCH .../diagrams/{diagramId}/content
```

```json
{
  "objects": {
    "$add": { "do-new": { "...": "..." } },
    "$update": { "do-k8s": { "x": 420, "y": 140 } },
    "$remove": ["do-old"],
    "$replace": {}
  },
  "connections": {
    "$add": {},
    "$update": {},
    "$remove": [],
    "$replace": {}
  }
}
```

Prefer `$update` for repositioning; `$add` for new nodes; `$remove` for cleanup.

---

## Anti-patterns

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Import only, no diagrams | Blank canvas | `POST .../diagrams` |
| `modelId` on diagram object wrong type | 422 on create | Match ModelObject.type |
| Connection uses model ids for origin/target | Broken edges | Use diagram object ids |
| Empty `objects` map | Blank diagram tab | Add at least one object |
| Share link without handle | 404 | Append `/{optionsHandle}` |
| Components on context diagram | Clutter | Use app/component diagram types |

---

## Verification sequence

```bash
# 1. Diagram count
GET .../diagrams
# expect: diagrams.length >= 1

# 2. Canvas populated
GET .../diagrams/{diagramId}/content
# expect: Object.keys(objects).length >= 1

# 3. Visual proof
POST .../diagrams/{diagramId}/export/image
# poll → fileUrls.png

# 4. Thumbnail (fast check)
GET .../diagrams/{diagramId}/thumbnail
```

Debug script: see consuming project overlay (e.g. `icepanel-ui-debug.ps1`).

Automation patterns: [scripts/README.md](scripts/README.md)

---

## Export and share

**PNG/SVG job:**
```http
POST .../diagrams/{diagramId}/export/image
{ "theme": "light", "maxWidth": 2048 }
GET .../export/image/{diagramExportImageId}
```

**Share link:** See [reference/visuals.md](reference/visuals.md). App URL:

```
https://app.icepanel.io/landscapes/{landscapeId}/versions/latest
```

---

## AI-assisted description

```http
POST .../diagrams/{diagramId}/content/generate-description
POST .../model/objects/{id}/generate-description
POST .../model/connections/{id}/generate-description
```

Useful after layout is stable — not a substitute for diagram creation.

---

## Related

- Full payloads: [examples.md](examples.md)
- Tag/color semantics: [reference/visuals.md](reference/visuals.md)
- Flows on diagrams: [reference/flows-adrs-drafts.md](reference/flows-adrs-drafts.md)
