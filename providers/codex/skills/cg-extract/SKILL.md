---
name: cg-extract
description: >
  REQUIRED when turning existing project code into Cartograph widgets — onboarding
  ("cartograph flavor", "widgetize this codebase"), extracting glue/modules already
  in the app, or recovering freehand code that should have been a widget. Decompose
  into domain APIs vs thin glue; search before create; strip contamination; scaffold;
  read library_notes; tests/examples; validate; checkin; rewire and delete old code.
  Bias against under-extraction: coupling is contamination, not a reason to keep logic
  in the app. Fires on "/cg-extract", "extract widget", "widgetize", "cartograph-ify",
  "pull into a widget", "this should have been a widget". Does NOT fire for greenfield
  planning (cg-plan), empty-scaffold fill (cg-create), composing a multi-widget
  feature blueprint (cg-blueprint), or cloud/config/proposals.
---

# cg-extract

Lift **existing** app code into widgets. One API at a time. Prefer MCP
(`cg_registry`, `cg_create`, `cg_validate`, `cg_checkin`); CLI for the rest.

**Onboard whole project:** survey → rank candidates → extract one pass at a time → backlog the rest.

## 1. Classify

Read the target. Split into pieces. **Default bias: extract.**

| Widget | Glue only |
| --- | --- |
| Domain API you’d re-derive later, or that should be stable (policy, parse, transform, retry, shapes, …) even if today’s call site is coupled | Thin sequencing + product wiring (IDs, paths, names) |

Project imports/env/paths ≠ glue — that’s contamination (step 3).  
Names: kebab capability (`retry-backoff`), never project names.  
Too small → leave; too big → split. Show candidates (API, domain, language, slug) before scaffolding.

## 2. Search

Per candidate: project `cg/` then `cg_registry` search (multiple terms). Show hits.

- exact → install  
- partial → prefer install+extend  
- none → create  

## 3. Contamination → public API

Map deps; plan the clean surface:

- third-party → `tech_stack.dependencies`  
- project imports / env / hardcodes / product types → params, Protocols, or widget-local types  

Present contamination plan + public API; then scaffold.

## 4. Scaffold + implement

1. `cg_create` / `cartograph create <slug> --domain … --language …` (slug only).  
2. **Read `library_notes` first** (general/language/domain). Do not edit them. Follow while coding.  
3. `src/` — domain-shaped API, no project names, strip contamination.  
4. tests/examples — isolated, fake data, no network; follow language notes.

## 5. Validate → checkin → rewire

1. `cg_validate` — fix real failures (stop after two hard loops).  
2. `cg_checkin` with reason + bump (minor for new). Publish only if user asks.  
3. Wire consumer imports; **delete** old inline code; pass project values at call site; run consumer tests.  
4. Note remaining extract candidates if any.
