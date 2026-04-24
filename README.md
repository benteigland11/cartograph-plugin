# cartograph-plugin

A Claude Code plugin for [Cartograph](https://github.com/benteigland11/Cartograph),
the widget library manager for AI agents.

Installing this plugin gives Claude Code the Cartograph MCP server
(auto-registered and auto-installed on first session) plus four skills
that teach Claude to use widgets well.

## What ships

**Skills**

- `cg-plan` drives widget-first decomposition for a feature.
- `cg-config` interprets the current Cartograph setup and recommends
  named profiles when the user wants to change defaults.
- `cg-cloud` explains the cloud layer: publishing, governance,
  adopt, sync, and what the available choices mean.
- `cg-proposals` walks the pending proposals queue on widgets the
  user owns, one proposal at a time.

**MCP server**

Claude Code auto-registers the Cartograph MCP server on install. No
manual `claude mcp add` step. No manual `pip install`. The plugin
handles setup the first time a session starts.

**CLAUDE.md**

An always-on instructions layer describing the Cartograph mentality
(search the library before writing new logic), the widget identity
format, domain and language taxonomy, and the canonical flow for
creating and checking in widgets.

## Prerequisites

Claude Code, plus Python 3.10 or newer with `pip` on the PATH. That
is everything the plugin needs. On first session it installs
`cartograph-mcp` into its own data directory, so no separate `pip
install` step is required.

If you already use Cartograph from the command line outside of Claude
Code, or if you simply want to install the package system-wide, run:

    pip install cartograph-mcp

The plugin detects the existing install and skips its own bootstrap.

## How the auto-install works

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

## Install

### From the Claude Code marketplace

Coming soon. While the plugin is in development, use the local
install below.

### Local development install

Clone the repo and point Claude Code at it:

    git clone https://github.com/benteigland11/cartograph-plugin
    claude --plugin-dir ./cartograph-plugin

Skills appear as `/cartograph:cg-plan`, `/cartograph:cg-config`,
`/cartograph:cg-cloud`, and `/cartograph:cg-proposals`. They also
auto-trigger based on natural language matching their descriptions,
so in practice you usually just say what you want and Claude picks
the right skill.

After editing any SKILL.md, plugin.json, or the hook script, run
`/reload-plugins` to pick up the change without restarting Claude
Code.

## Quick start

Once the plugin is loaded, any of these prompts will invoke a skill:

> "I want to build a retry wrapper for HTTP calls. What parts should
> be widgets?"

Claude invokes `cg-plan` and walks the feature through widget
identification.

> "How should Cartograph be set up if I want to keep widgets
> private?"

Claude invokes `cg-config` and recommends a named profile.

> "Someone proposed a change to one of my widgets. Help me review
> it."

Claude invokes `cg-proposals` and walks the queue, showing the
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
