---
description: Invoke when the user is planning a new feature, starting implementation, or breaking down a problem into components. Teaches widget-first decomposition before any code is written. Triggers on phrases like "I want to build", "let's implement", "how should I structure", "new project", "add capability", or any planning conversation that precedes writing code.
---

# cg-plan — plan implementations widget-first

Your job is to keep the user from writing logic that already exists in
the Cartograph library, and to keep them from burying reusable logic
inside project-specific code.

## Before any code is written

1. **Name the capabilities.** Break the feature into 3-8 named
   capabilities. Each is a verb phrase: "retry a failed HTTP call",
   "parse a CSV into typed rows", "render a hex grid in OpenSCAD".

2. **Search for each capability.** Use `registry_widget` (search mode)
   for each capability. Don't batch into one fuzzy query — each
   capability deserves its own search.

3. **Classify the results:**
   - **Exact match:** install it and plan the glue code around it.
   - **Close match:** install it, note the gap. If the gap is a general
     improvement (not project-specific), plan to improve the widget
     and check it back in.
   - **No match:** decide whether this capability belongs as a new
     widget, or as project-specific glue. See decomposition heuristics.

## Decomposition heuristics

**Belongs as a widget:**
- You can describe it without naming the project.
- Another project (hypothetical or real) would use it.
- It has a clean input/output contract.
- It can be tested without mocking the entire project.

**Belongs as glue (not a widget):**
- It wires specific widgets to specific widgets in a specific order.
- It encodes a product decision ("our app shows the banner on Tuesdays").
- It configures a widget for this project's data shape.

**Red flags:**
- Widget is too large: it does more than one capability.
  Split it. A good widget fits in one screen of code.
- Widget is too small: it's a one-line wrapper. Don't widget-ize it;
  the wrapper belongs in glue.
- Leaky boundary: the widget imports project-specific config or
  knows the name of another widget. Decouple it.

## Picking domain and language

- Domain is required at creation time. Use the taxonomy in CLAUDE.md.
- If the domain feels ambiguous, the widget is probably mis-scoped —
  split it.
- Language follows the caller. Python widgets for Python glue, etc.
  Don't cross languages inside one widget.

## Output shape of the planning conversation

End the conversation with a plan the user can act on:
- List of widgets to install (with widget_ids).
- List of widgets to improve (with the planned change, one line each).
- List of new widgets to create (with proposed `<name>` — remember
  create_widget only needs the name, not the full widget_id).
- List of glue files the project needs, one line each.

Only then start coding.
