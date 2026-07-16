# Integrator agent brief

You wire **cross-landscape relationships** into a portfolio or hub landscape after per-landscape model imports complete.

Skill reference: [workflows.md](../workflows.md) § Phase 4 · [workflows.md](../workflows.md) § Merge

---

## Inputs

- Portfolio/hub `{landscapeId}`
- Detail landscapes (each with own model)
- Share URLs or system names for cross-links

---

## Outputs

- Updated `LandscapeImportData` patch OR individual `POST .../model/connections`
- Optional: `links` on model objects pointing to detail-landscape share URLs
- Trigger diagrammer to **rebuild portfolio context-diagram** after integration

---

## Patterns

### Cross-landscape links (no merge)

On portfolio system objects, set `links` in import JSON or `PUT .../model/objects/{id}`:

```json
{
  "links": {
    "detail": {
      "name": "Open K8s detail landscape",
      "url": "https://s.icepanel.io/{shortId}/{handle}"
    }
  }
}
```

### Connection naming

Use action verbs: `depends on`, `deploys to`, `governed by`, `searches via`, `syncs secrets from`

Tag cross-cutting concerns: purple for agents, blue for platform, green for live.

### Merge strategies

| Strategy | When |
|----------|------|
| Copy API | Single source → portfolio shell, same org |
| Export → remap → import | Multiple sources, id prefix required |
| Duplicate | Fork experiment, not portfolio merge |

After any merge: **recreate diagrams** on target — import does not preserve canvas layout.

---

## Exit criteria

```
[ ] Portfolio systems represent all detail landscapes
[ ] Cross-links or connections document dependencies
[ ] Context diagram updated to show integrated systems
[ ] Search finds shared concerns (e.g. Doppler) in expected landscapes only
```
