# cartograph-plugin

A Claude Code plugin for [Cartograph](https://github.com/benteigland11/Cartograph),
a widget library manager for AI agents.

Installing this plugin gives Claude Code:

- The Cartograph MCP server (auto-registered, no manual config).
- Three skills that teach Claude to use widgets well:
  - **cg-plan** — widget-first decomposition before writing code.
  - **cg-config** — walking the user through configuration choices.
  - **cg-cloud** — publishing, visibility, and governance guidance.
- An always-on `CLAUDE.md` with the Cartograph mentality, widget
  identity format, and canonical workflow.

## Prerequisites

- Claude Code
- Python 3.10+
- `cartograph-cli` and `cartograph-mcp` installed:

      pip install cartograph-cli cartograph-mcp

## Install

### From the Claude Code marketplace

*(Coming soon — while the plugin is in development, use the local
install path below.)*

### Local development install

    git clone https://github.com/benteigland11/cartograph-plugin
    claude --plugin-dir ./cartograph-plugin

Skills appear namespaced as `/cartograph:cg-plan`, `/cartograph:cg-config`,
`/cartograph:cg-cloud`. The MCP server registers automatically.

Run `/reload-plugins` to pick up changes without restarting Claude Code.

## Quick start

Once installed, ask Claude something that triggers a skill:

> "I want to build a retry wrapper for HTTP calls. Where should I start?"

Claude invokes `cg-plan`, searches the registry, and walks you through
widget-first decomposition.

> "How do I set up Cartograph to keep my widgets private?"

Claude invokes `cg-config` and walks you through the relevant settings.

## What Cartograph is

Widgets are reusable code modules with tests, examples, and metadata.
Installed widgets live under `cg/<widget_id>/`. Search, install, validate,
and publish across languages and domains.

Widget identity: `<domain>-<name>-<language>` (e.g. `backend-retry-backoff-python`).

See the main repo for the full CLI surface and engine list.

## License

MIT
