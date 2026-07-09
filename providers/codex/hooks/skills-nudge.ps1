$ErrorActionPreference = "Stop"

# Codex Windows UserPromptSubmit content hook.
# Do not drain stdin; some harnesses keep the pipe open until timeout.
$msg = "Before acting on this request, review available Cartograph (cg-*) skills and use any that apply."

$payload = [ordered]@{
  systemMessage = $msg
  hookSpecificOutput = [ordered]@{
    hookEventName = "UserPromptSubmit"
    additionalContext = $msg
  }
}

$payload | ConvertTo-Json -Depth 5 -Compress
exit 0
