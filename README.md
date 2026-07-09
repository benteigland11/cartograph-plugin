# Cartograph plugin

Agent plugin for [Cartograph](https://github.com/benteigland11/Cartograph) — reusable, validated widgets for AI coding agents.

**Version:** 0.1.16  
**Hosts:** Claude Code · Grok · Codex · Gemini CLI · OpenClaw

---

## What you get

| Piece | Purpose |
| --- | --- |
| **MCP server** | Search, install, create, validate, checkin widgets and blueprints |
| **Skills** | Always-on skill menu + workflows (`cg-plan`, `cg-create`, `cg-blueprint`, `cg-rules`, …) |
| **Hooks** | **Claude / Codex only** — per-prompt skills reminder (where inject works) |

### Skills (every host — primary “Cartograph mode” surface)

Skill **descriptions** are listed every turn. That is how Grok (and all hosts) stay in widget-first mode without freehand free-for-all.

| Skill | When to use it |
| --- | --- |
| **cg-plan** | Before implementing a feature — leaves + optional blueprint; install / improve / create |
| **cg-create** | After `create` scaffolds a **widget** — design API, fill, validate |
| **cg-blueprint** | Compose widgets into a reusable multi-widget **feature** (`bp-…`) |
| **cg-extract** | Existing or freehanded app code → widgets (onboard / recover) |
| **cg-rules** | Encode durable conventions as custom validate/checkin rules (project/global) |
| **cg-config** | Defaults, profiles, “how should I set Cartograph up?” |
| **cg-cloud** | Publish, governance, registries, login, adopt/sync |
| **cg-proposals** | Review / accept / reject proposals on widgets you own |

### Hooks (host-dependent)

| Host | UserPromptSubmit inject |
| --- | --- |
| **Claude Code** | Yes — `additionalContext` / structured JSON via `skills-nudge.sh` |
| **Codex** | Yes if the host applies hook stdout (ships same Claude-shaped nudge) |
| **Grok Build** | **No** — harness runs the hook but **ignores stdout** on passive events (official docs). Grok package ships **no hooks** so we don’t fake success. |

**Claude SessionStart** may `pip install` `cartograph-mcp` into plugin data if missing.

---

## Grok: how “always Cartograph” works without inject

Grok’s public hooks contract: only `PreToolUse` uses stdout for decisions; for passive events (including `UserPromptSubmit`), **stdout is ignored**. Probes confirmed `systemMessage`, plain text, and `hookSpecificOutput.additionalContext` all fire successfully and **do not** reach the model.

So the Grok package is **MCP + skills only**:

1. **Strong skill descriptions** (always in the skills menu) — mode gate.
2. **MCP tools** — daily driver for search/install/create/validate/checkin.
3. **Optional project rules** (not in the plugin) — for local max, add `.grok/rules/cartograph-mode.md` or a short block in `AGENTS.md` so instructions co-exist with every session in that repo.

Do **not** rely on UserPromptSubmit for Grok mode pressure.

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

After edits: `/reload-plugins`. Trust hooks when asked (inject works here).

### Grok

```bash
pip install -U cartograph-mcp

# Preferred: Grok package only (skills + MCP, no hooks)
grok plugin install benteigland11/cartograph-plugin#providers/grok --trust
```

Marketplace:

```bash
grok plugin marketplace add benteigland11/cartograph-plugin
grok plugin marketplace update
# install cartograph from marketplace UI / CLI
```

Confirm:

```text
/plugins  → cartograph enabled, skills listed, hooks count 0
/skills   → cg-plan, cg-create, cg-extract, …
/mcps     → cartograph
```

If an older install still shows a UserPromptSubmit cartograph hook: uninstall, reinstall **0.1.11+**, `/hooks` → `r` or new session.

### Codex

```bash
pip install -U cartograph-mcp

codex plugin marketplace add https://github.com/benteigland11/cartograph-plugin
# Then install/enable "cartograph" from the plugin picker

codex plugin marketplace upgrade cartograph-marketplace
```

Trust hooks after install if the host prompts (nudge may inject depending on Codex version).

### Gemini CLI

```bash
pip install -U cartograph-mcp
gemini extensions install https://github.com/benteigland11/cartograph-plugin
```

### OpenClaw

```bash
pip install -U cartograph-mcp
openclaw plugins install ./cartograph-plugin
openclaw plugins list
openclaw gateway restart
```

---

## Quick start (after install)

> I want to add HTTP retries with backoff. What should be widgets?

→ **cg-plan** (search → install / improve / create)

> Widgetize this module — give the project Cartograph flavor.

→ **cg-extract**

> Finish the scaffold I just created under `cg/…`.

→ **cg-create**

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
hooks/                  Claude/Codex UserPromptSubmit: skills-nudge.sh
.claude-plugin/         Claude marketplace + SessionStart + nudge
.grok-plugin/           Grok root manifest (skills + MCP only)
providers/grok/         Grok package (no hooks/)
providers/codex/        Codex package (skills, hooks, .mcp.json)
.mcp.json               MCP: cartograph-mcp
scripts/                sync-grok, sync-codex, versions, validators
```

```bash
python3 scripts/sync-grok.py
python3 scripts/sync-codex.py
python3 scripts/versions.py --check
```

---

## License

MIT
