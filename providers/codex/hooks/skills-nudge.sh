#!/usr/bin/env bash
# Claude / Codex UserPromptSubmit content hook.
# Reads (and discards) the hook envelope on stdin so the pipe never blocks.
set -euo pipefail
cat >/dev/null || true

MSG='Before acting on this request, review available Cartograph (cg-*) skills and use any that apply.'

# Claude Code / Codex: structured inject
printf '%s\n' "{
  \"systemMessage\": $(python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$MSG"),
  \"hookSpecificOutput\": {
    \"hookEventName\": \"UserPromptSubmit\",
    \"additionalContext\": $(python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$MSG")
  }
}"
