---
name: cg-plan
description: >
  REQUIRED before implementing a feature. Do not freehand domain logic in the app.
  Decompose one feature into a decisive install / improve / create plan for Cartograph
  widgets; leave only thin product wiring as glue. Search project cg/ and the registry
  before proposing anything new. Bias hard against under-extraction: if future work would
  re-derive this capability, it owns a widget API — today's tight coupling is usually
  contamination to strip (params, Protocols), not a reason to keep logic in the consumer.
  Stops at the plan — does not implement. Fires on add/implement/build/feature work,
  "use cartograph", "cartograph plan", "/cg-plan", and any request that would otherwise
  invent helpers, services, or domain code from scratch. Does NOT fire for pure docs/chat,
  cloud/account (cg-cloud), config defaults (cg-config), proposal review (cg-proposals),
  filling an already-scaffolded widget (cg-create), or extracting an existing in-tree chunk
  into a widget (cg-extract).
---

## Description

Plan how a feature is built with Cartograph **before any implementation**.
Search first. Decide install / improve / create. Glue is last resort for
product-specific sequencing only.

## Activation trigger phrases

- "/cg-plan"
- "use cartograph" / "cartograph plan"
- "let's add …" / "I want to put in a …"
- "implement …" / "build …" / "go ahead and implement"
- any feature request that would invent domain code from scratch

## What must happen

1. Clear install / improve / create plan with concrete widget references.
2. No optional widgets. Include or exclude — decide.
3. No "glue it all in the app for speed." Domain capability goes up into a widget API.
4. Actually run search (project `cg/` then Cartograph registry). "I don't think anything exists" is not a substitute.

## Scope

Plan **one feature** at a time. A whole app cannot be broken into widgets accurately.
If the user asks for a full app, ask them to narrow to a single feature.

## How to operate

Use the headings shown below in your response.

### Feature

Define the feature in 1–2 sentences.

### Check Architecture If Exists

Look for `architect.py` / architecture diagrams if present. Use them only as context
for how the feature plugs in — architect is not required.

### Candidates

Numbered list of every implementation piece needed. Expansive detail.
Format: `Candidate, domain, language` when known.

### Classify

Widget vs glue. **Default bias: widget.** Under-extraction is the failure mode.

A piece owns a **widget** when:

1. Re-deriving it from scratch next time would be annoying, **or**
2. It would improve with iteration across projects, **or**
3. It is domain capability that should be called through a stable API (policy, parser,
   transform, retry, auth decision, shape builders, etc.) even if *today's* call site is coupled.

**Coupling is not glue.** Project imports, env vars, hardcoded paths, and product types
are contamination to strip when extracting — not proof the logic should stay in the app.
Leave only sequencing and product names in glue.

| Implementation | Widget? | Reason |
| -------------- | ------- | ------ |
| ex             | T       | one sentence: what API this owns |

### Search

For every widget-classified piece:

1. Read promising `cg/` installs (`widget.json` + source).
2. Cartograph search (multiple query terms). Search is cheap; create is not.
3. Prefer install + extend over create when a widget covers ≥ a meaningful share of need.

Show what you searched and what you found. Do not invent widget IDs.

### Improve, Install, Create

State each bucket with names/ids:

- **Use as-is** — installed or to-install, no changes
- **Improve/extend** — which widget, what changes, why general (not product-specific)
- **Install** — exact installable id from search
- **Create** — `name, domain, language` only when search fails

### Edit Architecture

If architecture files exist and the plan changes structure, note required edits.
Do not implement them in this skill unless the user asks.

## Stop

End at the plan. Do not scaffold, install, or write feature code unless the user
explicitly says to execute the plan next.
