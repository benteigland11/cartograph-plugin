---
name: cg-create
description: >
  REQUIRED immediately after a successful Cartograph scaffold — MCP cg_create
  or CLI `cartograph create` — when a brand-new widget directory exists under cg/
  and still needs to become a real, validatable widget. Before writing code, read
  widget.json library_notes (general, language, and domain if present) — these are
  the language-engine rules validation will enforce; adhere to them while filling
  the scaffold. Then design the public API, fill TODOs/src/tests/examples, and run
  cg_validate before any checkin. Greenfield fill only, not planning or extraction.
  Fires on: right after create succeeds, "finish this widget", "fill in the scaffold",
  "shape this new widget", "what should this widget's API be", "/cg-create". Does NOT
  fire before scaffold exists (run create first). Does NOT fire for feature triage
  (cg-plan), extracting existing app code (cg-extract), or patching a checked-in
  library widget.
---

# cg-create — guide a brand-new widget

This skill starts **after** scaffold succeeds. `cartograph create` / MCP
`cg_create` has produced `cg/<widget_id>/`. The directory and manifest exist;
most of it is TODOs and placeholders. Your job is to turn that skeleton into a
widget that will pass validation and is worth calling from other projects —
not just something that compiles.

This is design work, not typing work. Filling TODOs in order without locking
the public surface first is how bad widgets ship.

## When this skill applies

- `cg_create` or `cartograph create` just succeeded, **or**
- A fresh scaffold is on disk and the user wants it finished

If the widget directory does not exist yet, stop: run create first, then
continue here. Do not improvise extraction of existing app code — that is
`cg-extract`.

## Scope

**One** brand-new widget. Finish it before starting another. Do not expand into
unrelated features or "while we're here" siblings.

## What to read first

Before suggesting anything, read the scaffold:

1. **`widget.json` → `library_notes` (required, first).** Cartograph injects
   engine rules here: `general`, `language`, and sometimes `domain`. These are
   the constraints validation will enforce (coverage, tests, contamination,
   examples, deps, language-specific bans). **Read them fully and design/implement
   to comply before you write code.** Do not edit `library_notes` — it is managed
   by Cartograph and restored on checkin. Put agent/project notes in
   `custom_notes` if needed.
2. Rest of `widget.json` — every `[TODO: ...]` is a real decision (tags, description, etc.).
3. `src/` — including scaffold guidance comments.
4. Tests — what shape the scaffolder set up.
5. Examples — what the scaffolder expects demonstrated.
6. Any NOTES/README stubs the scaffolder dropped.

Skipping `library_notes` is how widgets fail validation for rules the engine
already told you about.

## The design pass (before any implementation)

Force these four answers, in order, before writing real code:

1. **One-line purpose.** "This widget does X and only X." If you need "and" or
   "for cases where", you are designing two widgets.
2. **Public surface.** Exact consumer-facing signatures: names, args, return shapes.
   No internals yet.
3. **Won't do.** Two or three explicit non-goals — blocks scope creep.
4. **What the example proves.** One concrete consumer scenario (the widget's pitch).

Surface the design and get agreement before filling source. Redesign is cheap;
post-validation rewrites are not.

**API bias:** Prefer a clean domain API over mirroring one project's call site.
Hardcoded paths, product names, and env reads do not belong in `src/` — they
become parameters.

## Filling the scaffold

Once design is agreed, in this order — still bound by `library_notes`:

1. `widget.json` TODOs (tags, description) — must match the design; placeholder tags fail validate.
2. `src/` — only what the public surface promised; match language/general notes
   (deps declared, no contamination, no project names, etc.).
3. Tests — pin the public surface; follow language-note test rules (e.g. pytest
   only, coverage expectations, isolation).
4. Example — design-pass scenario; must run under the example rules in
   `library_notes` (no network, no secrets, exits cleanly).

After each file, briefly note what changed and what remains.

## Validating

When filled, run **`cg_validate`** (not checkin). Treat failures as design feedback:
fix code or rethink the surface. Do not suppress warnings to pass.

Only suggest **`cg_checkin`** when validation is clean and the user confirms the
widget is what they wanted. Checkin is a commitment.

## Tool boundary

- Scaffold: already done (`cg_create` / `cartograph create`)
- Dry run: `cg_validate`
- Commit to library: `cg_checkin` only at the end, with user intent
- CLI for anything outside MCP

Do not edit the widget to bypass a validation rule — fix the cause.
