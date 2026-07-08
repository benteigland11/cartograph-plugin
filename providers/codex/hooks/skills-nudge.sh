#!/usr/bin/env bash
# UserPromptSubmit: one-line nudge into Cartograph skills.
# Compatible with Claude Code, Grok, and Codex plugin hooks.
# Reads (and discards) the hook envelope on stdin so the pipe never blocks.
set -euo pipefail
cat >/dev/null || true

# Shared inject shape:
# - Claude Code / Grok: hookSpecificOutput.additionalContext
# - Codex: same field as extra developer context on UserPromptSubmit
MSG='Before acting on this request, review available Cartograph (cg-*) skills and use any that apply.'

printf '%s\n' "{
  \"hookSpecificOutput\": {
    \"hookEventName\": \"UserPromptSubmit\",
    \"additionalContext\": \"${MSG}\"
  }
}"
