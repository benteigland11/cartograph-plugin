#!/usr/bin/env python3
"""Inspect or bump plugin versions across host manifests.

Manifests:
  claude   → .claude-plugin/plugin.json
  grok     → .grok-plugin/plugin.json (+ providers/grok/.grok-plugin/plugin.json)
  codex    → providers/codex/.codex-plugin/plugin.json
  gemini   → gemini-extension.json
  openclaw → openclaw.plugin.json

Usage:
  versions.py                              print a table of current versions
  versions.py --check                      exit 1 if versions are out of sync
  versions.py --bump patch [--only ...]    bump versions in place
  versions.py --set 1.2.3 [--only ...]     set explicit version
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

MANIFESTS = {
    "claude": REPO / ".claude-plugin" / "plugin.json",
    "grok": REPO / ".grok-plugin" / "plugin.json",
    "codex": REPO / "providers" / "codex" / ".codex-plugin" / "plugin.json",
    "gemini": REPO / "gemini-extension.json",
    "openclaw": REPO / "openclaw.plugin.json",
}

# Secondary copies kept in sync with grok when present
GROK_PROVIDER_MANIFEST = (
    REPO / "providers" / "grok" / ".grok-plugin" / "plugin.json"
)


def read(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    return json.loads(text), text


def get_version(path: Path) -> str:
    data, _ = read(path)
    return data.get("version", "?")


def write_version(path: Path, new_version: str) -> None:
    data, original = read(path)
    data["version"] = new_version
    rendered = json.dumps(data, indent=2) + ("\n" if original.endswith("\n") else "")
    path.write_text(rendered)


def bump(version: str, level: str) -> str:
    parts = version.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"cannot bump non-semver version: {version!r}")
    major, minor, patch = (int(p) for p in parts)
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    if level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"unknown bump level: {level}")


def parse_only(value: str | None) -> list[str]:
    if not value:
        return list(MANIFESTS)
    requested = [p.strip() for p in value.split(",") if p.strip()]
    unknown = [p for p in requested if p not in MANIFESTS]
    if unknown:
        raise SystemExit(
            f"unknown host(s): {', '.join(unknown)}. valid: {', '.join(MANIFESTS)}"
        )
    return requested


def print_table() -> dict[str, str]:
    versions = {host: get_version(path) for host, path in MANIFESTS.items()}
    width = max(len(h) for h in versions)
    for host, ver in versions.items():
        print(f"{host.ljust(width)}  {ver}")
    return versions


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit 1 if hosts disagree on version")
    ap.add_argument("--bump", choices=("patch", "minor", "major"), help="bump semver level")
    ap.add_argument("--set", dest="set_version", metavar="X.Y.Z", help="set explicit version")
    ap.add_argument(
        "--only",
        metavar="claude,grok,codex,gemini,openclaw",
        help="comma-separated subset of hosts to bump/set (default: all)",
    )
    args = ap.parse_args()

    if args.bump and args.set_version:
        ap.error("--bump and --set are mutually exclusive")

    if not (args.bump or args.set_version):
        versions = print_table()
        if args.check:
            unique = set(versions.values())
            if len(unique) > 1:
                print(f"\ndrift: hosts disagree ({sorted(unique)})", file=sys.stderr)
                return 1
            print("\nok: all hosts in sync")
        return 0

    targets = parse_only(args.only)

    for host in targets:
        path = MANIFESTS[host]
        current = get_version(path)
        if args.set_version:
            new = args.set_version
        else:
            new = bump(current, args.bump)
        write_version(path, new)
        print(f"{host}: {current} -> {new}")
        if host == "grok" and GROK_PROVIDER_MANIFEST.is_file():
            write_version(GROK_PROVIDER_MANIFEST, new)
            print(f"grok-provider: -> {new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
