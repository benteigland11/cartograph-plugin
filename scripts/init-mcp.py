"""SessionStart hook: ensure cartograph_mcp is importable.

Cross-platform bootstrap. If cartograph_mcp is already importable
(e.g. user ran `pip install cartograph-mcp` globally), exit fast.
Otherwise pip-install into the plugin's data dir so the MCP server
can launch.

Idempotent. Uses os.pathsep so PYTHONPATH separator is correct on
both POSIX (`:`) and Windows (`;`).
"""

import importlib.util
import os
import subprocess
import sys


def _data_dir() -> str:
    return os.environ.get(
        "CLAUDE_PLUGIN_DATA",
        os.path.join(os.path.expanduser("~"), ".cartograph-plugin-data"),
    )


def main() -> int:
    lib_dir = os.path.join(_data_dir(), "lib")

    existing = os.environ.get("PYTHONPATH", "")
    parts = [lib_dir] + ([existing] if existing else [])
    os.environ["PYTHONPATH"] = os.pathsep.join(parts)
    if lib_dir not in sys.path:
        sys.path.insert(0, lib_dir)

    if importlib.util.find_spec("cartograph_mcp") is not None:
        return 0

    print(
        f"[cartograph-plugin] Installing cartograph-mcp into {lib_dir}...",
        file=sys.stderr,
    )
    os.makedirs(lib_dir, exist_ok=True)

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet",
             "--target", lib_dir, "cartograph-mcp"],
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(
            "[cartograph-plugin] ERROR: failed to install cartograph-mcp.\n"
            "\n"
            "To finish setup manually, run:\n"
            "\n"
            "    pip install cartograph-mcp\n"
            "\n"
            "Then restart Claude Code.",
            file=sys.stderr,
        )
        return 1

    print(
        "[cartograph-plugin] Done. cartograph-mcp installed to plugin data dir.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
