#!/usr/bin/env python3
"""Regenerate the codex provider tree from root sources + codex overrides.

Layout:
  skills/                              canonical, hand-edited
  .mcp.json                            canonical mcp config
  providers/codex/skills/              generated, committed (do not hand-edit)
  providers/codex/.mcp.json            generated, committed (do not hand-edit)
  providers/codex/skills.overrides/    optional per-file overrides for codex

Run with no args to regenerate. Run with --check to verify the committed
generated tree matches what would be produced (used in CI).
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT_SKILLS = REPO / "skills"
ROOT_MCP = REPO / ".mcp.json"
CODEX_DIR = REPO / "providers" / "codex"
CODEX_SKILLS = CODEX_DIR / "skills"
CODEX_MCP = CODEX_DIR / ".mcp.json"
CODEX_OVERRIDES = CODEX_DIR / "skills.overrides"


def build_skills(target: Path) -> tuple[int, int]:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(ROOT_SKILLS, target)
    copied = sum(1 for p in target.rglob("*") if p.is_file())

    overridden = 0
    if CODEX_OVERRIDES.exists():
        for src in CODEX_OVERRIDES.rglob("*"):
            if not src.is_file():
                continue
            rel = src.relative_to(CODEX_OVERRIDES)
            dst = target / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            overridden += 1
    return copied, overridden


def build_mcp(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT_MCP, target)


def trees_equal(a: Path, b: Path) -> bool:
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
        help="Verify committed codex tree matches generator output. Exit 1 on drift.",
    )
    args = ap.parse_args()

    for required in (ROOT_SKILLS, ROOT_MCP):
        if not required.exists():
            print(f"error: {required} not found", file=sys.stderr)
            return 2

    if args.check:
        scratch_skills = REPO / ".sync-codex.skills.check"
        scratch_mcp = REPO / ".sync-codex.mcp.check"
        try:
            copied, overridden = build_skills(scratch_skills)
            build_mcp(scratch_mcp)
            skills_ok = CODEX_SKILLS.is_dir() and trees_equal(scratch_skills, CODEX_SKILLS)
            mcp_ok = files_equal(scratch_mcp, CODEX_MCP)
        finally:
            if scratch_skills.exists():
                shutil.rmtree(scratch_skills)
            if scratch_mcp.exists():
                scratch_mcp.unlink()
        if not (skills_ok and mcp_ok):
            drifted = []
            if not skills_ok:
                drifted.append("providers/codex/skills/")
            if not mcp_ok:
                drifted.append("providers/codex/.mcp.json")
            print(
                "drift: " + ", ".join(drifted) + " does not match generator output. "
                "Run scripts/sync-codex.py and commit the result.",
                file=sys.stderr,
            )
            return 1
        print(f"ok: {copied} skill files, {overridden} overrides, mcp synced")
        return 0

    copied, overridden = build_skills(CODEX_SKILLS)
    build_mcp(CODEX_MCP)
    print(
        f"synced providers/codex/: skills={copied} files, overrides={overridden}, "
        f".mcp.json mirrored from root"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
