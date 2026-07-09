# Cartograph plugin

Agent plugin for [Cartograph](https://github.com/benteigland11/Cartograph) — reusable, validated widgets for AI coding agents.

**Version:** 0.1.8  
**Hosts:** Claude Code · Grok · Codex · Gemini CLI · OpenClaw

---

## What you get

| Piece | Purpose |
| --- | --- |
| **MCP server** | Search, install, create, validate, checkin widgets |
| **Skills** | Judgment workflows (`cg-plan`, `cg-create`, `cg-extract`, …) |
| **Hooks** | Nudge the agent toward those skills on every prompt |

### Skills

| Skill | When to use it |
| --- | --- |
| **cg-plan** | Before implementing a feature — install / improve / create plan |
| **cg-create** | After `create` scaffolds a widget — design API, fill, validate |
| **cg-extract** | Existing or freehanded app code → widgets (onboard / recover) |
| **cg-config** | Defaults, profiles, “how should I set Cartograph up?” |
| **cg-cloud** | Publish, governance, registries, login, adopt/sync |
| **cg-proposals** | Review / accept / reject proposals on widgets you own |

### Hooks

| Event | What it does |
| --- | --- |
| **UserPromptSubmit** | Injects: *review available Cartograph (`cg-*`) skills and use any that apply* |
| **SessionStart** (Claude) | Optionally `pip install`s `cartograph-mcp` into plugin data if missing |

**Trust plugin hooks** when the host asks (Grok / Codex `/hooks`). Without trust, hooks do not run.

---

## Prerequisites

1. **Python 3.10+** with `pip` on your `PATH`
2. **Cartograph MCP** (once, any host except Claude auto-bootstrap):

```bash
pip install -U cartograph-mcp
```

Confirm:

```bash
cartograph-mcp --help   # or: python -m cartograph_mcp.server
cartograph doctor       # optional: language engines
```

---

## Install

### Claude Code

```text
/plugin marketplace add benteigland11/cartograph-plugin
/plugin install cartograph@cartograph-marketplace
```

Local dev:

```bash
git clone https://github.com/benteigland11/cartograph-plugin
claude --plugin-dir ./cartograph-plugin
```

After edits: `/reload-plugins`.

Claude starts the MCP server as `python -m cartograph_mcp.server` (with plugin data `PYTHONPATH`). First session can auto-install the package via `SessionStart` if it is missing.

### Grok

Grok uses a **native** package (`.grok-plugin/` + `providers/grok/`), not the Claude layout.

```bash
pip install -U cartograph-mcp

# Preferred: install the Grok provider package from this monorepo
grok plugin install benteigland11/cartograph-plugin#providers/grok --trust

# Or whole-repo install (root also has .grok-plugin/plugin.json)
grok plugin install benteigland11/cartograph-plugin --trust
```

Marketplace (reads `.grok-plugin/marketplace.json` → `providers/grok`):

```bash
grok plugin marketplace add benteigland11/cartograph-plugin
grok plugin marketplace update
# then install cartograph from the marketplace UI / CLI and trust hooks
```

Confirm hooks registered:

```text
/hooks   → look for Plugin source, UserPromptSubmit / skills-nudge
```

If hooks are missing after install, reinstall with `--trust` and reload (`/hooks` → `r` or new session).

MCP: `cartograph-mcp` on `PATH` (or the plugin `.mcp.json`).

### Codex

```bash
pip install -U cartograph-mcp

codex plugin marketplace add https://github.com/benteigland11/cartograph-plugin
# Then install/enable "cartograph" from the plugin picker

# Refresh after we ship updates:
codex plugin marketplace upgrade cartograph-marketplace
```

MCP (if not auto-wired from the plugin):

```bash
codex mcp add cartograph -- cartograph-mcp
codex mcp list
```

Trust the plugin’s **UserPromptSubmit** hook in `/hooks` after install.

Codex loads `providers/codex/` (skills, hooks, `.mcp.json`).

### Gemini CLI

```bash
pip install -U cartograph-mcp
gemini extensions install https://github.com/benteigland11/cartograph-plugin
```

Registers MCP + skills + `GEMINI.md`.

### OpenClaw

```bash
pip install -U cartograph-mcp
openclaw plugins install ./cartograph-plugin   # or clone path / published package
openclaw plugins list
openclaw gateway restart
```

Expect bundle format; MCP from root `.mcp.json`.

---

## Quick start (after install)

Try:

> I want to add HTTP retries with backoff. What should be widgets?

→ **cg-plan** (search → install / improve / create)

> Widgetize this module — give the project Cartograph flavor.

→ **cg-extract**

> Finish the scaffold I just created under `cg/…`.

→ **cg-create**

Every prompt also gets a short reminder to check `cg-*` skills (if hooks are trusted).

---

## What Cartograph is

Widgets are proven modules: code + tests + examples + metadata.  
Layout: `cg/<domain>-<name>-<language>/` (e.g. `backend-retry-backoff-python`).

Agents should **search → install/extend → glue**, and only **create** when nothing fits.  
CLI reference: [Cartograph](https://github.com/benteigland11/Cartograph).

---

## Repo layout

```text
skills/                 Shared skill bodies (canonical)
hooks/                  UserPromptSubmit nudge (Grok + shared)
.claude-plugin/         Claude marketplace + plugin.json (+ SessionStart)
providers/codex/        Codex package (skills, hooks, .mcp.json)
.mcp.json               MCP: cartograph-mcp
gemini-extension.json   Gemini
openclaw.plugin.json    OpenClaw
scripts/                sync-codex, init-mcp, validators
```

Codex tree is generated from root:

```bash
python3 scripts/sync-codex.py
python3 scripts/sync-codex.py --check
```

---

## Validate packaging

```bash
scripts/validate-codex-plugin.sh
scripts/validate-openclaw-bundle.sh
```

---

## License

MIT
