# cartograph-plugin

Agent plugin for [Cartograph](https://github.com/benteigland11/Cartograph),
the widget library manager for AI coding agents.

Ships the Cartograph MCP server plus a set of skills. Supported
agents so far: Claude Code and Codex.

## What ships

**MCP server**

The Cartograph MCP server exposes registry search, installed-widget
management, widget status, widget creation, validation, checkin,
rules management, and config. It is published to PyPI as
`cartograph-mcp` and runs through the `cartograph-mcp` console
command.

Agents pick it up via the standard `.mcp.json` at the repo root when
their plugin loader supports it, or via an agent-specific registration
if the agent prefers that path.

**Skills**

- `cg-plan` drives widget-first decomposition for a feature.
- `cg-config` interprets the current Cartograph setup and recommends
  named profiles when the user wants to change defaults.
- `cg-cloud` explains the cloud layer: publishing, governance,
  adopt, sync, and what the available choices mean.
- `cg-proposals` walks the pending proposals queue on widgets the
  user owns, one proposal at a time.

How each agent surfaces skills depends on the agent. See the
per-agent sections below.

## Prerequisites

Python 3.10 or newer with `pip` on the PATH. The Cartograph MCP
server is a Python package.

If you want `cartograph-mcp` available system-wide:

    pip install cartograph-mcp

Claude Code can install it automatically on first session, so this
step is optional for Claude Code users. For Codex, install it
yourself before starting a session.

## Install for Claude Code

Claude Code treats this repo as a plugin via the manifest at
`.claude-plugin/plugin.json`. The plugin auto-registers the MCP
server and installs `cartograph-mcp` on first session, so there is
no separate `claude mcp add` or `pip install` step.

### From the Claude Code marketplace

    /plugin marketplace add benteigland11/cartograph-plugin
    /plugin install cartograph@cartograph-marketplace

Skills appear as `/cartograph:cg-plan`, `/cartograph:cg-config`,
`/cartograph:cg-cloud`, and `/cartograph:cg-proposals`, and also
auto-trigger based on natural language matching their descriptions.

### Local development install

    git clone https://github.com/benteigland11/cartograph-plugin
    claude --plugin-dir ./cartograph-plugin

After editing any SKILL.md, plugin.json, or the hook script, run
`/reload-plugins` to pick up the change without restarting Claude
Code.

## Install for Gemini CLI

Gemini CLI uses the `gemini-extension.json` manifest. Gemini does not
run the Claude Code `SessionStart` hook, so install the MCP server
yourself first:

    pip install cartograph-mcp

Then link the plugin locally:

    gemini extensions link ./cartograph-plugin

This will:
1.  Register the Cartograph MCP server.
2.  Enable the `cg-plan`, `cg-config`, `cg-cloud`, and `cg-proposals` skills.
3.  Inject the "Project-to-Project Contribution" mindset via `GEMINI.md`.

### How the Claude Code auto-install works

The plugin ships a `SessionStart` hook at `scripts/init-mcp.sh` that
runs when Claude Code starts a session. On the first run it checks
whether `cartograph_mcp` is importable. If the import fails it runs
`pip install --target ${CLAUDE_PLUGIN_DATA}/lib cartograph-mcp`, which
also pulls in `cartograph-cli` as a dependency. On every later
session the check passes instantly and the hook exits as a no-op.

Claude Code launches the MCP server as `python3 -m
cartograph_mcp.server` with `PYTHONPATH` set to the plugin data lib,
so the auto-installed package is always found.

If the auto-install ever fails (no network, restricted environment,
a pip configuration that blocks `--target`), the hook prints a clear
fallback instruction asking the user to run `pip install
cartograph-mcp` manually and restart Claude Code.

## Install for Codex

Codex consumes the marketplace manifest at
`.agents/plugins/marketplace.json` and the plugin manifest at
`plugins/cartograph/.codex-plugin/plugin.json`. Codex does not
currently run the Claude Code `SessionStart` hook, so install the MCP
server yourself first:

    pip install cartograph-mcp

Then add this plugin marketplace to Codex:

    codex plugin marketplace add https://github.com/benteigland11/cartograph-plugin

Open Codex's slash plugin picker, select `cartograph`, and press Enter
to install/enable it for the current Codex setup. Adding the marketplace
only makes the plugin available; this picker step is what installs it.

If you already added the marketplace before an update, refresh it with:

    codex plugin marketplace upgrade cartograph-marketplace

Then register the MCP server with Codex:

    codex mcp add cartograph -- cartograph-mcp

Confirm Codex can see it:

    codex mcp list

You should see `cartograph` with command `cartograph-mcp` and status
`enabled`.

The published marketplace entry points Codex at
`plugins/cartograph/`. That nested plugin contains the Codex manifest,
skills, and `.mcp.json`. The explicit `codex mcp add` step is still
needed for Codex versions that do not auto-register MCP servers from a
marketplace plugin.

`.mcp.json` launches the server with:

    cartograph-mcp

## Validate

After editing Codex packaging or shared skill metadata, run:

    scripts/validate-codex-plugin.sh

That checks Codex JSON, required skill frontmatter, the
`cartograph-mcp` entrypoint, and shared metadata drift between the
Claude and Codex manifests.

## Quick start

Once the plugin is loaded, any of these prompts will invoke the
relevant skill:

> "I want to build a retry wrapper for HTTP calls. What parts should
> be widgets?"

The agent runs `cg-plan` and walks the feature through widget
identification.

> "How should Cartograph be set up if I want to keep widgets
> private?"

The agent runs `cg-config` and recommends a named profile.

> "Someone proposed a change to one of my widgets. Help me review
> it."

The agent runs `cg-proposals` and walks the queue, showing the
inline diff summary for each proposal.

## What Cartograph is

Widgets are reusable code modules with tests, examples, and metadata.
Installed widgets live under `cg/<widget_id>/` in the project root.
Cartograph searches, installs, validates, and publishes them across
languages and domains.

Widget identity follows the pattern `<domain>-<name>-<language>`, for
example `backend-retry-backoff-python`.

See the main repo for the full CLI surface and the list of language
engines Cartograph supports.

## License

MIT
