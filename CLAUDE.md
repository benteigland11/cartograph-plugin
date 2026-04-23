# Cartograph

Cartograph is a widget library manager. Widgets are reusable code modules
with tests, examples, and metadata. Installed widgets live under
`cg/<widget_id>/` in the project root.

## Mentality: widget-first

Before writing new logic, search the library. If existing code can be
improved to cover the need, improve the widget and check it in. Only
write fresh glue code after confirming no widget covers the capability.

A widget is anything that would be written for another project. Most
"project-specific" code is actually reusable once you strip the wiring.

## Widget identity

widget_id format: `<domain>-<name>-<language>`
Example: `backend-retry-backoff-python`

When calling `create_widget`, pass only the `<name>`. Domain and language
are prepended/appended automatically.

**Domains:** backend, frontend, data, ml, security, infra, modeling,
rtl, universal. Domain is required — no silent default.

**Languages:** python, javascript, typescript, nim, openscad,
systemverilog, php, css.

## Canonical flow

1. Search the registry for widgets that cover the need.
2. Install the ones that fit. Write glue code to wire them together.
3. If you edit widget source, do it because the widget needs a general
   improvement — not to fit this project's shape. Then validate and
   check it in.
4. `validate_widget` runs tests, contamination scan, and custom rules.
   Must pass before checkin.
5. `checkin_widget` saves the improved version back to the library.
   Use `--bump patch|minor|major`. Never hand-edit the version field.
6. `cloud publish` shares the widget with the registry. Visibility and
   governance are meaningful choices — see the cg-cloud skill.

## Common MCP tools

- `registry_widget` — search and inspect registry widgets
- `installed_widget` — search and inspect locally installed widgets
- `create_widget` — scaffold a new widget with correct structure
- `validate_widget` — run the full validation pipeline
- `checkin_widget` — push improvements back to the library
- `widget_status` — check drift / outdated state for installed widgets
- `cartograph_config` — inspect or change settings

## Skills

- `cg-plan` — invoke when planning an implementation. Teaches
  widget-first decomposition.
- `cg-config` — invoke when the user expresses configuration intent
  ("set up Cartograph", "use my registry", "keep widgets private").
- `cg-cloud` — invoke around publishing, visibility, governance,
  proposals, and unpublishing.

## Non-negotiables

- Validation opinions (80% coverage, timeouts, contamination rules)
  are not user-configurable. Custom rules only add on top.
- Never hand-edit widget `version` fields. Cartograph manages versions.
- `cg/` is a PEP 420 namespace package. Never create `cg/__init__.py`
  in any project — it shadows every other contributor.
