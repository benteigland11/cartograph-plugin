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

for key in ("name", "version", "description", "homepage", "repository", "license"):
    if codex.get(key) != claude.get(key):
        raise SystemExit(
            f"metadata drift for {key}: "
            f"codex={codex.get(key)!r} claude={claude.get(key)!r}"
        )

for field in ("skills", "mcpServers", "interface"):
    if field not in codex:
        raise SystemExit(f"missing Codex plugin field: {field}")

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
