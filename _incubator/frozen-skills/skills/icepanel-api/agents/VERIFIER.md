# Verifier agent brief

You confirm an IcePanel landscape is **visible and shareable** after model import and diagram push.

Skill reference: [diagrams.md](../diagrams.md) § Verification · [workflows.md](../workflows.md)

---

## Inputs

- `{landscapeId}`, `{versionId}` (or `latest`)
- Optional: expected object/diagram counts from project overlay

---

## Checks (run in order)

### 1. Model layer

```http
GET /landscapes/{landscapeId}/versions/{versionId}/model/objects
GET /landscapes/{landscapeId}/versions/{versionId}/model/connections
```

```
[ ] objects.length > 0
[ ] connections present (if model has edges)
```

### 2. Diagram layer

```http
GET /landscapes/{landscapeId}/versions/{versionId}/diagrams
GET .../diagrams/{diagramId}/content
```

```
[ ] diagrams.length >= 1
[ ] context-diagram exists (type=context-diagram)
[ ] content.objects non-empty
[ ] actors left / externals right (visual spot-check or export PNG)
```

### 3. Export proof

```http
POST .../diagrams/{diagramId}/export/image
{ "theme": "light", "maxWidth": 2400 }
GET .../export/image/{diagramExportImageId}
```

```
[ ] fileUrls.png present
[ ] save to reports/diagrams/{slug}-context.png (project convention)
```

### 4. Share link

```http
GET .../share-link
POST .../share-link  (body: ShareLinkOptions — mode: diagram, diagramId)
```

```
[ ] URL format: https://s.icepanel.io/{shortId}/{handle}
[ ] handle suffix present (404 without it)
```

### 5. Flows (if phase 3 ran)

```http
GET .../flows
```

```
[ ] flows.length >= 0 (optional phase)
```

---

## Failure report template

| Check | Status | Evidence |
|-------|--------|----------|
| diagram count | pass/fail | GET response snippet |
| canvas objects | pass/fail | object key count |
| PNG export | pass/fail | file path or HTTP code |
| share link | pass/fail | full URL |

Write report to `reports/diagram-verify.md` when working in Scratch portfolio project.

---

## Common failures

| Symptom | Fix |
|---------|-----|
| diagram count = 0 | Run diagrammer + push script |
| objects empty on content GET | DiagramCreate missing objects map |
| broken edges | originId/targetId use model ids instead of diagram object ids |
| share 404 | Append options handle to base URL |
