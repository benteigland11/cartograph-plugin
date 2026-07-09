#!/usr/bin/env bash
# Claude / Codex UserPromptSubmit content hook.
#
# Do NOT drain stdin with `cat` — some harnesses leave the pipe open after
# writing the event JSON, so `cat` blocks until the hook timeout.
# We ignore the envelope; exiting closes our end of the pipe.
set -uo pipefail

MSG='Before acting on this request, review available Cartograph (cg-*) skills and use any that apply.'

# Fixed JSON — no python3 (avoids PATH issues under minimal plugin env).
# Claude: systemMessage + additionalContext.
# Codex: additionalContext (plain text also injects as developer context).
printf '%s\n' "{
  \"systemMessage\": \"${MSG//\"/\\\"}\",
  \"hookSpecificOutput\": {
    \"hookEventName\": \"UserPromptSubmit\",
    \"additionalContext\": \"${MSG//\"/\\\"}\"
  }
}"
exit 0
