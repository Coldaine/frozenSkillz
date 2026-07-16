# Modeler agent brief

You read source repos and produce **LandscapeImportData JSON** for IcePanel import. You do NOT call IcePanel.

For diagram layout after import, see [DIAGRAMMER.md](DIAGRAMMER.md).

---

## Outputs

```
imports/<slug>.json          → LandscapeImportData
imports/<slug>-adrs.json     → ADR array (optional, separate push)
```

Consuming projects may extend this contract (e.g. Scratch `AGENT_BRIEF.md`).

---

## Schema essentials

`LandscapeImportData`: `modelObjects`, `modelConnections`, `tags`, `tagGroups`

### Hierarchy (enforced)

| type | parent |
|------|--------|
| domain | — |
| actor, system | domain |
| group | domain or group |
| app, store | system |
| component | app or store |

### IDs

Stable lowercase kebab-case, prefixed with slug: `{slug}-{name}`

### Status and tags

- Status: `live`, `future`, `deprecated`, `removed`
- Tag colors: see [SKILL.md](../SKILL.md) § Tag colors
- `external: true` for systems outside your control

### ASCII only

No em-dashes, smart quotes, or non-ASCII in any string.

---

## Modeling guidance

- 15–40 objects per landscape (adjust by scope)
- Name connections with protocol/action
- Add `description` on important objects (powers search and AI descriptions)
- Use tag groups for Status, Layer, Provider, etc.

---

## Return summary

Object count, connection count, ADR count, surprises from repo review.
