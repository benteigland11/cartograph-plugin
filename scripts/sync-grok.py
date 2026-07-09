#!/usr/bin/env python3
"""Regenerate the Grok provider tree from root sources.

Layout:
  skills/                         canonical
  .mcp.json                       canonical
  .grok-plugin/plugin.json        Grok root manifest (no hooks)
  providers/grok/                 generated, committed

Grok Build does not apply UserPromptSubmit stdout to the model (passive
hooks: exit 0 only). Do not ship fake inject hooks — mode pressure is
skill descriptions + MCP.

Install:
  grok plugin install benteigland11/cartograph-plugin#providers/grok --trust
"""
from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT_SKILLS = REPO / "skills"
ROOT_MCP = REPO / ".mcp.json"
ROOT_MANIFEST = REPO / ".grok-plugin" / "plugin.json"
GROK_DIR = REPO / "providers" / "grok"
GROK_SKILLS = GROK_DIR / "skills"
GROK_HOOKS = GROK_DIR / "hooks"
GROK_MCP = GROK_DIR / ".mcp.json"
GROK_MANIFEST_DIR = GROK_DIR / ".grok-plugin"
GROK_MANIFEST = GROK_MANIFEST_DIR / "plugin.json"


def build_skills(target: Path) -> int:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(ROOT_SKILLS, target)
    return sum(1 for p in target.rglob("*") if p.is_file())


def build_mcp(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT_MCP, target)


def build_manifest(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT_MANIFEST, target)
    # Grok package: never register hooks (convention dir can still load them).
    data = json.loads(target.read_text())
    data.pop("hooks", None)
    # Prefer relative paths under providers/grok
    data["skills"] = "./skills/"
    data["mcpServers"] = "./.mcp.json"
    target.write_text(json.dumps(data, indent=2) + "\n")


def remove_hooks_dir() -> None:
    if GROK_HOOKS.exists():
        shutil.rmtree(GROK_HOOKS)


def trees_equal(a: Path, b: Path) -> bool:
    if not a.is_dir() and not b.is_dir():
        return True
    if not a.is_dir() or not b.is_dir():
        return False
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    for sub in cmp.common_dirs:
        if not trees_equal(a / sub, b / sub):
            return False
    return True


def files_equal(a: Path, b: Path) -> bool:
    return a.is_file() and b.is_file() and filecmp.cmp(a, b, shallow=False)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--check",
        action="store_true",
        help="Verify committed grok tree matches generator. Exit 1 on drift.",
    )
    args = ap.parse_args()

    for required in (ROOT_SKILLS, ROOT_MCP, ROOT_MANIFEST):
        if not required.exists():
            print(f"error: {required} not found", file=sys.stderr)
            return 2

    if args.check:
        scratch = REPO / ".sync-grok.check"
        try:
            if scratch.exists():
                shutil.rmtree(scratch)
            scratch.mkdir()
            n_skills = build_skills(scratch / "skills")
            build_mcp(scratch / ".mcp.json")
            build_manifest(scratch / ".grok-plugin" / "plugin.json")
            ok = (
                trees_equal(scratch / "skills", GROK_SKILLS)
                and files_equal(scratch / ".mcp.json", GROK_MCP)
                and files_equal(
                    scratch / ".grok-plugin" / "plugin.json", GROK_MANIFEST
                )
                and not GROK_HOOKS.exists()
            )
        finally:
            if scratch.exists():
                shutil.rmtree(scratch)
        if not ok:
            print(
                "drift: providers/grok/ does not match generator output. "
                "Run scripts/sync-grok.py and commit.",
                file=sys.stderr,
            )
            return 1
        print(f"ok: skills={n_skills} mcp+manifest, no hooks/")
        return 0

    n_skills = build_skills(GROK_SKILLS)
    build_mcp(GROK_MCP)
    build_manifest(GROK_MANIFEST)
    remove_hooks_dir()
    print(
        f"synced providers/grok/: skills={n_skills}, .mcp.json + "
        f".grok-plugin/plugin.json, hooks removed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
