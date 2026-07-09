#!/usr/bin/env bash
# Grok UserPromptSubmit content hook.
#
# Grok applies UserPromptSubmit inject differently from Claude:
# - Prefer plain text on stdout as additional prompt context.
# - Also emit Claude-compatible JSON (additionalContext + systemMessage)
#   so mixed loaders still get something useful.
#
# Drain stdin so the hook pipe never blocks.
set -eu
cat >/dev/null 2>/dev/null || true

MSG='Before acting on this request, review available Cartograph (cg-*) skills and use any that apply.'

# 1) Plain text — primary for Grok UserPromptSubmit
printf '%s\n' "$MSG"

# 2) JSON block (Claude/Codex shape) after a blank line
printf '\n%s\n' "{
  \"systemMessage\": $(python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$MSG"),
  \"hookSpecificOutput\": {
    \"hookEventName\": \"UserPromptSubmit\",
    \"additionalContext\": $(python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$MSG")
  }
}"
