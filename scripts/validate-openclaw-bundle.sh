#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$ROOT" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])

def rel(path: pathlib.Path) -> str:
    return str(path.relative_to(root))

def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        raise SystemExit(f"invalid JSON: {rel(path)}: {exc}")

def require_file(path: pathlib.Path, message: str):
    if not path.is_file():
        raise SystemExit(message)

def require_dir(path: pathlib.Path, message: str):
    if not path.is_dir():
        raise SystemExit(message)

require_file(root / "openclaw.plugin.json", "missing ClawHub package manifest: openclaw.plugin.json")
require_file(root / ".claude-plugin" / "plugin.json", "missing Claude bundle marker: .claude-plugin/plugin.json")
require_file(root / ".mcp.json", "missing bundle MCP config: .mcp.json")
require_dir(root / "skills", "missing root skill bundle: skills/")

openclaw = load_json(root / "openclaw.plugin.json")
claude = load_json(root / ".claude-plugin" / "plugin.json")
root_mcp = load_json(root / ".mcp.json")

if openclaw.get("id") != "cartograph":
    raise SystemExit("openclaw.plugin.json id must be cartograph")
if openclaw.get("skills") != ["./skills"]:
    raise SystemExit("openclaw.plugin.json must expose ./skills")
schema = openclaw.get("configSchema")
if not isinstance(schema, dict):
    raise SystemExit("openclaw.plugin.json must include configSchema")

servers = root_mcp.get("mcpServers")
if not isinstance(servers, dict) or "cartograph" not in servers:
    raise SystemExit(".mcp.json must declare mcpServers.cartograph")
server = servers["cartograph"]
if server.get("command") != "cartograph-mcp":
    raise SystemExit(".mcp.json mcpServers.cartograph.command must be cartograph-mcp")
if "url" in server:
    raise SystemExit(".mcp.json must use stdio command transport, not url transport")

codex_root = root / "providers" / "codex"
require_file(codex_root / ".codex-plugin" / "plugin.json", "missing Codex bundle marker: providers/codex/.codex-plugin/plugin.json")
require_file(codex_root / ".mcp.json", "missing Codex bundle MCP config: providers/codex/.mcp.json")
require_dir(codex_root / "skills", "missing Codex skill bundle: providers/codex/skills/")

codex = load_json(codex_root / ".codex-plugin" / "plugin.json")
codex_mcp = load_json(codex_root / ".mcp.json")

if codex_mcp != root_mcp:
    raise SystemExit("Codex .mcp.json drifted from root .mcp.json")

if codex.get("mcpServers") != "./.mcp.json":
    raise SystemExit("Codex manifest must point mcpServers at ./.mcp.json")
if codex.get("skills") != "./skills/":
    raise SystemExit("Codex manifest must point skills at ./skills/")

for key in ("name", "description", "homepage", "repository", "license"):
    if codex.get(key) != claude.get(key):
        raise SystemExit(
            f"metadata drift for {key}: codex={codex.get(key)!r} claude={claude.get(key)!r}"
        )

if openclaw.get("version") != claude.get("version"):
    raise SystemExit(
        f"metadata drift for version: openclaw={openclaw.get('version')!r} claude={claude.get('version')!r}"
    )
for key in ("description",):
    if openclaw.get(key) != claude.get(key):
        raise SystemExit(
            f"metadata drift for {key}: openclaw={openclaw.get(key)!r} claude={claude.get(key)!r}"
        )

root_skills = sorted(path.parent.name for path in (root / "skills").glob("*/SKILL.md"))
codex_skills = sorted(path.parent.name for path in (codex_root / "skills").glob("*/SKILL.md"))
if root_skills != codex_skills:
    raise SystemExit(
        "root and Codex skill sets differ: "
        f"root={root_skills!r} codex={codex_skills!r}"
    )

for skill_path in sorted((root / "skills").glob("*/SKILL.md")):
    text = skill_path.read_text()
    if not text.startswith("---\n"):
        raise SystemExit(f"missing skill frontmatter: {rel(skill_path)}")
    frontmatter = text.split("---\n", 2)[1]
    fields = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    if fields.get("name") != skill_path.parent.name:
        raise SystemExit(f"skill name must match folder: {rel(skill_path)}")
    if not fields.get("description"):
        raise SystemExit(f"missing skill description: {rel(skill_path)}")

print("openclaw bundle metadata ok")
PY

if command -v openclaw >/dev/null 2>&1; then
    OPENCLAW_VERSION="$(openclaw --version 2>/dev/null || true)"
    if openclaw plugins --help 2>/dev/null | grep -Eq '(^|[[:space:]])inspect([[:space:]]|$)'; then
        echo "openclaw inspect command available"
    else
        echo "openclaw inspect command unavailable in local CLI (${OPENCLAW_VERSION:-unknown}); use a current OpenClaw CLI for bundle install inspection" >&2
    fi
else
    echo "openclaw executable not found; install OpenClaw to run live bundle inspection" >&2
fi

if command -v clawhub >/dev/null 2>&1; then
    if clawhub --help 2>/dev/null | grep -Eq '(^|[[:space:]])package([[:space:]]|$)'; then
        echo "clawhub package publish command available"
    else
        CLAWHUB_VERSION="$(clawhub --cli-version 2>/dev/null || true)"
        echo "clawhub package publish unavailable in local CLI (${CLAWHUB_VERSION:-unknown}); update clawhub before publishing to ClawHub" >&2
    fi
else
    echo "clawhub executable not found; install with: npm i -g clawhub" >&2
fi
