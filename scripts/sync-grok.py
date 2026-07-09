#!/usr/bin/env python3
"""Regenerate the Grok provider tree from root sources.

Layout (mirrors providers/codex):
  skills/                         canonical
  hooks/                          canonical (Grok-native relative commands)
  .mcp.json                       canonical
  .grok-plugin/plugin.json        Grok root manifest
  providers/grok/                 generated, committed

Grok discovers plugins via .grok-plugin/ first (native). Claude keeps
.claude-plugin/. Install the Grok package with:

  grok plugin install benteigland11/cartograph-plugin#providers/grok --trust

Or add the repo as a marketplace source (reads .grok-plugin/marketplace.json).
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
ROOT_HOOKS = REPO / "hooks"
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


def build_hooks(target: Path) -> int:
    if target.exists():
        shutil.rmtree(target)
    if not ROOT_HOOKS.is_dir():
        return 0
    shutil.copytree(ROOT_HOOKS, target)
    for sh in target.glob("*.sh"):
        sh.chmod(sh.stat().st_mode | 0o111)
    return sum(1 for p in target.rglob("*") if p.is_file())


def build_mcp(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT_MCP, target)


def build_manifest(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT_MANIFEST, target)


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

    for required in (ROOT_SKILLS, ROOT_MCP, ROOT_MANIFEST, ROOT_HOOKS):
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
            n_hooks = build_hooks(scratch / "hooks")
            build_mcp(scratch / ".mcp.json")
            build_manifest(scratch / ".grok-plugin" / "plugin.json")
            ok = (
                trees_equal(scratch / "skills", GROK_SKILLS)
                and trees_equal(scratch / "hooks", GROK_HOOKS)
                and files_equal(scratch / ".mcp.json", GROK_MCP)
                and files_equal(
                    scratch / ".grok-plugin" / "plugin.json", GROK_MANIFEST
                )
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
        print(f"ok: skills={n_skills} hooks={n_hooks} mcp+manifest synced")
        return 0

    n_skills = build_skills(GROK_SKILLS)
    n_hooks = build_hooks(GROK_HOOKS)
    build_mcp(GROK_MCP)
    build_manifest(GROK_MANIFEST)
    # ensure version in generated manifest matches root
    root_ver = json.loads(ROOT_MANIFEST.read_text()).get("version")
    data = json.loads(GROK_MANIFEST.read_text())
    if data.get("version") != root_ver:
        data["version"] = root_ver
        GROK_MANIFEST.write_text(json.dumps(data, indent=2) + "\n")
    print(
        f"synced providers/grok/: skills={n_skills}, hooks={n_hooks}, "
        f".mcp.json + .grok-plugin/plugin.json"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
