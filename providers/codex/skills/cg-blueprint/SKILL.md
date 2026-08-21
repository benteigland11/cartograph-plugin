---
name: cg-blueprint
description: >
  REQUIRED when composing Cartograph widgets into a reusable multi-widget
  *feature* with its own sealed API — not for ordinary multi-widget call sites
  in app code. A blueprint is a higher-order widget (id bp-<name>-<language>,
  blueprint.json): leaves stay widgets; the composition is the installable unit.
  Search existing blueprints first; ensure leaf widgets exist (install/create/
  checkin); scaffold via MCP cg_blueprint or create with is_blueprint; pin deps
  with add-dep; implement only composition in blueprint src/; tests/examples hit
  that API only; cg_validate then checkin. Fires on "/cg-blueprint", "compose
  into a blueprint", "this should be a blueprint", "feature composition",
  "higher-order widget", multi-widget feature façade, or after cg-plan names a
  blueprint. Does NOT fire for wiring two widgets once in the app with no
  reusable feature API (that's glue). Does NOT fire for single-widget scaffolds
  (cg-create), feature triage alone (cg-plan), or leaf extraction (cg-extract).
---

# cg-blueprint — compose widgets into a feature

Blueprints are the **compose layer**. Widgets are atoms. A blueprint is a
named, versioned, validated **feature** built from those atoms — same install
root (`cg/`), own API surface, pinned leaf deps.

**Not a blueprint:** calling two widgets from a route/screen once. That is
product glue. **Is a blueprint:** the composition *is* the feature other
projects would install (auth flow, ingest pipeline, checkout orchestration).

## When this skill applies

- Plan (or user) decided a **reusable multi-widget feature** needs its own API
- User asks to compose widgets into a blueprint / higher-order package
- You are about to freehand multi-widget orchestration in the app that should
  be a library feature instead

If only one leaf is needed, use **cg-create** / install — not this skill.
If you are still triaging a feature, run **cg-plan** first.

## Decision test (before scaffolding)

Blueprint when **all** of:

1. The valuable unit is a **named feature API**, not the leaves alone, **and**
2. Another project would want **this assembly** as one installable thing, **and**
3. Re-deriving this orchestration later would be annoying

Stay **app glue** when:

- One-off product sequencing, env, deploy, brand names
- Widgets are called independently with no shared façade worth publishing

## Tool boundary

Prefer MCP when available:

| Step | MCP / CLI |
| ---- | --------- |
| Search leaves & blueprints | registry search / `cartograph search` |
| Scaffold blueprint | `cg_blueprint` action create, or `cg_create` with `is_blueprint=true` / `cartograph blueprint create <slug> --language …` |
| Pin a leaf | `cg_blueprint` add-dep (`widget_id`, `blueprint_path`) / `cartograph blueprint add-dep <widget_id> --path <blueprint_dir>`. Widget must be installed. Pin-only; no extra flags. |
| Unpin | remove-dep |
| Validate / checkin | `cg_validate` / `cg_checkin` (same as widgets) |

ID shape: local `bp-<name>-<language>`; published often `cg-bp-<name>-<language>`.
v0.7: **single language**; deps are **leaf widgets only** (no blueprint-in-blueprint).
Strict pins — exact versions on add-dep / checkin.

## How to operate

### 1. Feature API (design first)

Before scaffolding:

1. **One-line feature purpose** — what the composition does end-to-end.
2. **Public surface** — consumer-facing signatures of the *blueprint* (not the leaves).
3. **Leaf list** — which widgets it composes and why each is needed.
4. **Won't do** — product env, deploy, one-off UI; those stay in the app.

Get agreement on the façade. Redesign is cheaper than re-pinning after checkin.

### 2. Search

1. Project `cg/` for existing `blueprint.json` / `bp-*` installs.
2. Registry search for blueprints and for each leaf (multiple terms).
3. Prefer **install/improve an existing blueprint** over creating one.
4. Prefer **install/improve leaves** over creating leaves.

Show what you searched. Do not invent ids.

### 3. Leaves ready

Every dependency must exist as an installable leaf (installed in this project
for `add-dep`, or created + validated + checked in first via **cg-create** /
extract — not half-finished placeholders).

Do not put leaf implementation inside the blueprint `src/`. Leaves own atoms;
the blueprint only wires them.

### 4. Scaffold

```text
cartograph blueprint create <slug> --language <lang>
# or MCP: cg_blueprint create / cg_create is_blueprint
```

Produces `cg/bp_<…>/` with `blueprint.json`, `src/`, tests, examples.
Read the scaffold fully (including any notes). Fill description/tags seriously —
placeholder tags fail validation.

### 5. Pin dependencies

For each leaf, ensure it is installed under `cg/`, then from the **project
root**:

```text
cartograph blueprint add-dep <widget_id> --path <blueprint_dir>
```

Pins the **installed** version. No ranges. Does **not** run the full
blueprint validator (`cg_validate` / checkin does). MCP add-dep needs
no extra flags. Pin every leaf before writing composition imports;
contamination blocks undeclared `cg/` imports in `src/`. If a leaf is
missing, install or create it first — do not skip pins. CLI `--validate`
re-proves a finished blueprint and reverts on failure; do not use it on
a scaffold.

### 6. Implement composition only

- **`src/`** — the sealed feature API; may import declared deps under `cg/`.
- **Tests / examples** — import **only** the blueprint public API. Never reach
  past it into leaves.
- No project names, env reads, or product types in `src/` — parameters instead
  (same contamination rules as widgets).
- Do not reimplement leaf logic; call leaf APIs.

### 7. Validate → checkin

1. `cg_validate` on the blueprint path — fix real failures.
2. `cg_checkin` only when green and the user wants it committed.
3. App code should call the **blueprint** API; leave only product-specific
   sequencing outside.

## Stop / handoff

- Still choosing install vs create leaves vs compose → **cg-plan**
- Filling a single new **widget** scaffold → **cg-create**
- Lifting existing app modules into **leaves** → **cg-extract**
- Cloud publish / adopt of a blueprint → **cg-cloud** after local checkin
- Durable project conventions on what compositions may do → **cg-rules**

Do not freehand a multi-widget feature façade in the app when this skill applies.
