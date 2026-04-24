#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$ROOT" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])

def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        raise SystemExit(f"invalid JSON: {path.relative_to(root)}: {exc}")

codex = load_json(root / ".codex-plugin" / "plugin.json")
load_json(root / ".mcp.json")
claude = load_json(root / ".claude-plugin" / "plugin.json")
marketplace = load_json(root / ".agents" / "plugins" / "marketplace.json")

for key in ("name", "version", "description", "homepage", "repository", "license"):
    if codex.get(key) != claude.get(key):
        raise SystemExit(
            f"metadata drift for {key}: "
            f"codex={codex.get(key)!r} claude={claude.get(key)!r}"
        )

for field in ("skills", "mcpServers", "interface"):
    if field not in codex:
        raise SystemExit(f"missing Codex plugin field: {field}")

if marketplace.get("name") != "cartograph-marketplace":
    raise SystemExit("Codex marketplace name must be cartograph-marketplace")
plugins = marketplace.get("plugins")
if not isinstance(plugins, list) or not plugins:
    raise SystemExit("Codex marketplace must include at least one plugin")

cartograph_entries = [entry for entry in plugins if entry.get("name") == "cartograph"]
if len(cartograph_entries) != 1:
    raise SystemExit("Codex marketplace must include exactly one cartograph plugin entry")

entry = cartograph_entries[0]
source = entry.get("source") or {}
if source.get("source") != "local":
    raise SystemExit("Codex cartograph plugin source must be local")
if "policy" not in entry or "category" not in entry:
    raise SystemExit("Codex marketplace entry must include policy and category")

plugin_path = (root / source.get("path", "")).resolve()
try:
    plugin_path.relative_to(root.resolve())
except ValueError:
    raise SystemExit("Codex marketplace plugin path must stay inside the repo")
if not (plugin_path / ".codex-plugin" / "plugin.json").is_file():
    raise SystemExit("Codex marketplace plugin path does not contain .codex-plugin/plugin.json")

skills_dir = root / "skills"
if not skills_dir.is_dir():
    raise SystemExit("missing skills directory")

for skill in sorted(skills_dir.glob("*/SKILL.md")):
    text = skill.read_text()
    if not text.startswith("---\n"):
        raise SystemExit(f"missing frontmatter: {skill.relative_to(root)}")
    try:
        frontmatter = text.split("---\n", 2)[1]
    except IndexError:
        raise SystemExit(f"malformed frontmatter: {skill.relative_to(root)}")
    fields = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    if not fields.get("name"):
        raise SystemExit(f"missing skill name: {skill.relative_to(root)}")
    if not fields.get("description"):
        raise SystemExit(f"missing skill description: {skill.relative_to(root)}")
    if fields["name"] != skill.parent.name:
        raise SystemExit(
            f"skill name does not match folder: {skill.relative_to(root)} "
            f"has {fields['name']!r}"
        )

print("codex plugin metadata ok")
PY

if ! command -v cartograph-mcp >/dev/null 2>&1; then
    echo "missing cartograph-mcp executable; run: pip install cartograph-mcp" >&2
    exit 1
fi

echo "cartograph-mcp entrypoint found: $(command -v cartograph-mcp)"
