#!/usr/bin/env bash
#
# SessionStart hook: ensure cartograph_mcp is importable.
#
# If the user already has cartograph-mcp installed globally (e.g. via
# `pip install cartograph-mcp`), this exits fast as a no-op. Otherwise
# it pip-installs into the plugin's data dir so `python -m
# cartograph_mcp.server` works when Claude Code launches the MCP
# server.
#
# Idempotent: subsequent sessions skip the install once the package is
# present.

set -e

DATA_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.cartograph-plugin-data}"
LIB_DIR="${DATA_DIR}/lib"

export PYTHONPATH="${LIB_DIR}:${PYTHONPATH:-}"

if python3 -c "import cartograph_mcp" 2>/dev/null; then
    exit 0
fi

echo "[cartograph-plugin] Installing cartograph-mcp into ${LIB_DIR}..." >&2

mkdir -p "${LIB_DIR}"

if ! pip install --quiet --target "${LIB_DIR}" cartograph-mcp 2>&1; then
    cat >&2 <<EOF
[cartograph-plugin] ERROR: failed to install cartograph-mcp automatically.

To finish setup manually, run:

    pip install cartograph-mcp

Then restart Claude Code.
EOF
    exit 1
fi

echo "[cartograph-plugin] Done. cartograph-mcp installed to plugin data dir." >&2
