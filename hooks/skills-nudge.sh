#!/usr/bin/env bash
# Claude / Codex UserPromptSubmit content hook.
# Reads (and discards) the hook envelope on stdin so the pipe never blocks.
# Exit 0 always on success — exit 1 from a broken path/env is what Codex surfaces.
set -uo pipefail
cat >/dev/null || true

MSG='Before acting on this request, review available Cartograph (cg-*) skills and use any that apply.'

# Fixed string — no python3 (avoids PATH/set -e exit 1 when python is missing).
# Claude: systemMessage + additionalContext. Codex: additionalContext (and plain text also injects).
printf '%s\n' "{
  \"systemMessage\": \"${MSG//\"/\\\"}\",
  \"hookSpecificOutput\": {
    \"hookEventName\": \"UserPromptSubmit\",
    \"additionalContext\": \"${MSG//\"/\\\"}\"
  }
}"
exit 0
