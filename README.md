# cartograph-plugin

Agent plugin for [Cartograph](https://github.com/benteigland11/Cartograph),
the widget library manager for AI coding agents.

Ships the Cartograph MCP server plus a set of skills. Designed to work
across hosts. Currently packaged for **Claude Code**, **Codex**, and
**Gemini CLI**, with one shared body of skill content and per-host
manifests in their respective conventions.

## What ships

**MCP server**

The Cartograph MCP server exposes registry search, installed-widget
management, widget status, widget creation, validation, checkin, rules
management, and config. It is published to PyPI as `cartograph-mcp`
and runs through the `cartograph-mcp` console command (or
`python -m cartograph_mcp.server` when invoked as a Python module).

Each host registers the server its own way:
- **Claude Code** — `mcpServers` block in `.claude-plugin/plugin.json`
- **Codex** — `.mcp.json` referenced from `providers/codex/.codex-plugin/plugin.json`
- **Gemini CLI** — `mcpServers` block in `gemini-extension.json`

**Skills**

- `cg-plan` drives widget-first decomposition for a feature.
- `cg-config` interprets the current Cartograph setup and recommends
  named profiles when the user wants to change defaults.
- `cg-cloud` explains the cloud layer: publishing, governance,
  adopt, sync, and what the available choices mean.
- `cg-proposals` walks the pending proposals queue on widgets the
  user owns, one proposal at a time.

How each host surfaces skills depends on the host. See the per-host
sections below.

## Repo layout

- `skills/` — base skill content shared across hosts.
- `.claude-plugin/` — Claude Code plugin manifest + Claude marketplace manifest.
- `gemini-extension.json` — Gemini CLI extension manifest at repo root.
- `.agents/plugins/marketplace.json` + `providers/codex/` — Codex marketplace manifest and provider package. Codex skills may diverge from the base skills when Codex needs provider-specific instructions.
- `scripts/` — bootstrap helpers (cross-platform Python).

## Prerequisites

Python 3.10 or newer with `pip` on the PATH. The Cartograph MCP server
is a Python package, and `python` must resolve to a Python 3 interpreter
on your PATH (true on Windows out of the box, and on modern macOS/Linux).

The cleanest setup on any host:

    pip install cartograph-mcp

Claude Code can also do this for you on first session via a bootstrap
hook (see "Install for Claude Code" below). Codex and Gemini CLI do
not have an equivalent hook, so install once yourself.

## Install for Claude Code

Claude Code treats this repo as a plugin via the manifest at
`.claude-plugin/plugin.json`. The plugin auto-registers the MCP server
and (optionally) installs `cartograph-mcp` on first session.

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

### How the Claude Code bootstrap hook works

The plugin ships a `SessionStart` hook at `scripts/init-mcp.py`
(cross-platform Python — works on Linux, macOS, and Windows). On the
first run it checks whether `cartograph_mcp` is importable. If the
import fails it runs `pip install --target $CLAUDE_PLUGIN_DATA/lib
cartograph-mcp`, which also pulls in `cartograph-cli` as a dependency.
On every later session the check passes instantly and the hook exits
as a no-op.

Claude Code launches the MCP server as `python -m cartograph_mcp.server`
with `PYTHONPATH` set to the plugin data lib, so the auto-installed
package is always found.

If the auto-install fails (no network, restricted environment, a pip
configuration that blocks `--target`), the hook prints a clear fallback
instruction asking you to run `pip install cartograph-mcp` manually and
restart Claude Code. You can also pre-install at any time and the hook
becomes a no-op.

This bootstrap is a Claude-Code-specific convenience because Claude
Code has session-start hooks. The other hosts don't, so on those you
install `cartograph-mcp` once yourself.

## Install for Codex

Codex consumes the marketplace manifest at
`.agents/plugins/marketplace.json` and the plugin manifest at
`providers/codex/.codex-plugin/plugin.json`.

Install `cartograph-mcp` first:

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

The published marketplace entry points Codex at `providers/codex/`.
That provider package contains the Codex manifest, skills, assets, and
`.mcp.json`. The explicit `codex mcp add` step is still needed for
Codex versions that do not auto-register MCP servers from a marketplace
plugin.

`.mcp.json` launches the server with:

    cartograph-mcp

## Install for Gemini CLI

Gemini CLI uses the `gemini-extension.json` manifest at the repo root.

Install `cartograph-mcp` first:

    pip install cartograph-mcp

Then link the plugin locally:

    gemini extensions install https://github.com/benteigland11/cartograph-plugin

This:
1. Registers the Cartograph MCP server.
2. Enables the `cg-plan`, `cg-config`, `cg-cloud`, and `cg-proposals` skills.
3. Loads the `GEMINI.md` context file.

For gallery discoverability, the upstream `cartograph-plugin` repo is
tagged with the `gemini-cli-extension` GitHub topic so the Gemini CLI
crawler can find it.

## Install for OpenClaw

OpenClaw can load this repo as a compatible plugin bundle. The root
package includes the ClawHub-required `openclaw.plugin.json` plus a
Claude-compatible bundle with shared skills and `.mcp.json`;
`providers/codex/` is also a Codex-compatible bundle with the same MCP
server config and Codex-specific skill copies. Current OpenClaw
versions still detect the root package as a bundle and expose the MCP
server from `.mcp.json`.

Install `cartograph-mcp` first:

    pip install cartograph-mcp

For local testing with current OpenClaw versions:

    openclaw plugins install ./cartograph-plugin
    openclaw plugins list
    openclaw plugins inspect cartograph
    openclaw gateway restart

Bundles should show as `Format: bundle`. OpenClaw maps the skill roots
and the stdio MCP server declared in `.mcp.json`; the MCP tools are
exposed with OpenClaw's bundle-safe tool naming.

To publish/register on ClawHub, use the package workflow from a current
`clawhub` CLI:

    npm i -g clawhub
    clawhub login
    clawhub package publish benteigland11/cartograph-plugin --dry-run
    clawhub package publish benteigland11/cartograph-plugin

`clawhub package publish` is newer than the legacy skill-only
`clawhub publish` command. If your local CLI only shows
`clawhub publish`, update `clawhub` before attempting plugin
registration.

## Validate

After editing Codex packaging or shared skill metadata, run:

    scripts/validate-codex-plugin.sh

That checks Codex JSON, required skill frontmatter, the
`cartograph-mcp` entrypoint, shared identity metadata drift between
the Claude and Codex manifests, and reports any intentional Codex skill
variants that differ from the base skills. Provider versions are
independent, so a Codex-only skill change only needs a Codex version
bump.

After editing OpenClaw-facing bundle metadata, run:

    scripts/validate-openclaw-bundle.sh

That checks the ClawHub package manifest, root bundle marker, Codex
bundle marker, MCP stdio config, skill metadata, root/Codex skill
parity, and whether the local OpenClaw and ClawHub CLIs are new enough
to run the documented live inspection and package publish commands.

## Quick start

Once the plugin is loaded on any host, prompts like these will invoke
the relevant skill:

> "I want to build a retry wrapper for HTTP calls. What parts should
> be widgets?"

The agent runs `cg-plan` and walks the feature through widget
identification.

> "How should Cartograph be set up if I want to keep widgets private?"

The agent runs `cg-config` and recommends a named profile.

> "Someone proposed a change to one of my widgets. Help me review it."

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
