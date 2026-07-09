---
name: cg-plan
description: >
  REQUIRED before implementing a feature. Do not freehand domain logic in the app.
  Decompose one feature into a decisive install / improve / create plan for Cartograph
  widgets and, when the composition itself is a reusable feature, blueprints; leave only
  thin product wiring as glue. Search project cg/ and the registry before proposing
  anything new. Bias hard against under-extraction: if future work would re-derive a
  capability, it owns a widget API; if the valuable unit is a multi-widget feature API
  others would install, it owns a blueprint — ordinary multi-widget call sites stay glue.
  Stops at the plan — does not implement. Fires on add/implement/build/feature work,
  "use cartograph", "cartograph plan", "/cg-plan", and any request that would otherwise
  invent helpers, services, or domain code from scratch. Does NOT fire for pure docs/chat,
  cloud/account (cg-cloud), config defaults (cg-config), proposal review (cg-proposals),
  filling an already-scaffolded widget (cg-create), composing an agreed blueprint
  (cg-blueprint), extracting an existing in-tree chunk into a widget (cg-extract),
  or authoring custom validation rules (cg-rules).
---

## Description

Plan how a feature is built with Cartograph **before any implementation**.
Search first. Decide install / improve / create for **leaves** and, when
warranted, **blueprint** for a reusable multi-widget feature. Glue is last
resort for product-specific sequencing only.

## Activation trigger phrases

- "/cg-plan"
- "use cartograph" / "cartograph plan"
- "let's add …" / "I want to put in a …"
- "implement …" / "build …" / "go ahead and implement"
- any feature request that would invent domain code from scratch

## What must happen

1. Clear install / improve / create / blueprint plan with concrete ids or slugs.
2. No optional widgets. Include or exclude — decide.
3. No "glue it all in the app for speed." Domain atoms → widgets; reusable
   multi-widget **features** → blueprints; only product sequencing stays glue.
4. Actually run search (project `cg/` then Cartograph registry). "I don't think
   anything exists" is not a substitute.

## Scope

Plan **one feature** at a time. A whole app cannot be broken into widgets
accurately. If the user asks for a full app, ask them to narrow to a single
feature.

## How to operate

Use the headings shown below in your response.

### Feature

Define the feature in 1–2 sentences.

### Candidates

Numbered list of every implementation piece needed. Expansive detail.
Format: `Candidate, domain, language` when known. Call out if a piece is a
**composition** (feature façade over other pieces) vs an **atom**.

### Classify

Three-way: **widget** | **blueprint** | **glue**. Default bias: extract domain
work upward. Under-extraction is the failure mode.

**Widget (leaf)** when:

1. Re-deriving it from scratch next time would be annoying, **or**
2. It would improve with iteration across projects, **or**
3. It is domain capability that should be called through a stable API (policy,
   parser, transform, retry, auth decision, shape builders, etc.) even if
   *today's* call site is coupled.

**Blueprint (compose feature)** when **all** of:

1. The valuable unit is a **named multi-widget feature API**, not the leaves
   alone, **and**
2. Another project would want **this assembly** as one installable thing, **and**
3. Re-deriving this orchestration later would be annoying

Blueprints are **not** "we use two widgets." Ordinary multi-widget call sites
in the app are **glue** unless the composition itself is the feature.

**Glue** when:

- Thin product sequencing, IDs, paths, names, env, deploy
- One-off wiring of widgets with no reusable feature façade

**Coupling is not glue.** Project imports, env vars, hardcoded paths, and
product types are contamination to strip when extracting — not proof the logic
should stay in the consumer. Leave only sequencing and product names in glue.

| Implementation | Kind (widget / blueprint / glue) | Reason |
| -------------- | -------------------------------- | ------ |
| ex             | widget                           | one sentence: what API this owns |

### Search

For every widget-classified piece **and** any proposed blueprint:

1. Read promising `cg/` installs (`widget.json` / `blueprint.json` + source).
2. Cartograph search (multiple query terms) — leaves **and** existing
   blueprints (`bp-*` / compose features). Search is cheap; create is not.
3. Prefer install + extend over create when something covers ≥ a meaningful
   share of need.

Show what you searched and what you found. Do not invent widget or blueprint IDs.

### Improve, Install, Create, Blueprint

State each bucket with names/ids:

- **Use as-is** — installed or to-install leaf or blueprint, no changes
- **Improve/extend** — which leaf or blueprint, what changes, why general
- **Install** — exact installable id from search
- **Create leaf** — `name, domain, language` only when search fails for an atom
- **Create / extend blueprint** — when classify said blueprint: proposed
  `bp-<name>-<language>` (or installable id), which leaves it composes, one-line
  feature API. Leaves must be install/create first; composition work is
  **cg-blueprint**, not app glue
- **Rules (optional)** — if this feature reveals a **durable** convention that
  should block or warn on every future validate/checkin (not a one-widget fix),
  list it here and hand authoring to **cg-rules**. Prefer rules over hoping the
  next session remembers AGENTS.md.

## Stop

End at the plan. Do not scaffold, install, or write feature code unless the user
explicitly says to execute the plan next. On execute: leaves via create/extract
as needed; **composition only under cg-blueprint**; durable bars via **cg-rules**.
