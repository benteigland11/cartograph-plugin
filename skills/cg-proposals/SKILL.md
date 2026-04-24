---
name: cg-proposals
description: Invoke when the user wants to review, accept, or reject pending proposals on widgets they own. Fires on "review my proposals", "walk through pending proposals", "someone proposed a change to my widget", "accept this proposal", "reject this proposal", "show me the diff for proposal X". Does NOT fire on questions about what proposals or governance are — that's cg-cloud. Does NOT fire on one-off agent MCP calls made as part of another task. Does NOT fire on changing governance defaults — that's cg-config.
---

# cg-proposals — walk the proposal queue

This skill walks the owner through their pending proposals one at a
time. It is action-shaped, not orientation-shaped. The user invoked
it because they have decisions to make, not because they want to
learn the model.

If the user asks what governance is, what a proposal does
structurally, or how the cloud layer works, hand to cg-cloud and
stop.

## Opening reads

In parallel:
- `cartograph whoami` — auth gate
- `cartograph cloud proposals` (no args) — the queue across every
  widget the user owns, with diff summaries inline per proposal

## Gate on state

1. **Not logged in** → tell the user, hand to `cartograph login`,
   exit. Don't try to walk a queue without auth.
2. **Queue empty** → *"Nothing pending. You're caught up."* Exit
   cleanly. Don't editorialize.
3. **Queue has items** → proceed.

## Framing the work

Before the first proposal, one sentence on scope: *"You have 3
proposals across 2 widgets."* Group by widget — less context
switching when multiple proposals target the same one.

## For each proposal, surface the signal

The proposals response already carries everything needed to triage.
For each one, present a compact card — not a dump:

- **who**: submitter handle
- **what**: widget_id and proposed version (e.g. `v0.3.0` → `v0.4.0`
  — tells you patch/minor/major)
- **why**: the submitter's free-form reason
- **scope**: from `diff_summary`: file count, `+N/-M` lines,
  widget.json-changed flag
- **flags**: any `violations` from the submitter's validation run
- **time pressure**: days remaining before 30-day expiry, if under 7

Present it as a short block, not a bulleted list the user has to
parse.

### What the signal means

- **widget.json changed** = meta edit (tags, description, contributors
  list, dependencies). Deserves closer look — metadata affects
  discovery and compatibility.
- **violations present** = the submitter's zip failed one or more
  validation checks on the way in. Significant signal; the reason
  explains what tripped.
- **large +/- counts** relative to the widget = structural change.
  Small diffs with widget.json changed = metadata-only PR.
- **near expiry** = user should decide soon or it auto-closes.

Don't recommend accept or reject. Surface the signal, let the user
decide.

## The decision prompt

After presenting each proposal, ask for one of:

- **accept** → `cartograph cloud proposals <widget_id> <id> --accept`
- **reject** → requires a reason. Prompt if not supplied. Then
  `cartograph cloud proposals <widget_id> <id> --reject --reason "..."`
- **view diff** → `cartograph cloud proposals <widget_id> <id>
  --diff`, show the unified diff, re-prompt for accept/reject/skip
- **skip** → leave it queued, move on

Never pass `--reject` without `--reason`. Proposers learn from the
reason; skipping it wastes the feedback loop.

Never batch. One proposal, one decision, confirm, next.

## After each decision

Short confirmation, then move on:
*"Accepted. 2 remaining."*
*"Rejected with reason. 2 remaining."*
*"Skipped. Still queued, 2 remaining."*

Don't restate the proposal you just handled. Don't preview the next
one before the user is ready.

## Exit

- When queue is exhausted: *"Done. 0 pending."*
- When user says stop: *"Stopping. Remaining proposals stay queued."*

Don't suggest more work (don't drift into "while we're here, want to
also...").

## Common friction points

- **Large diffs**: if `--diff` returns hundreds of lines, acknowledge
  it's a lot and ask if the user wants to narrow to specific files
  (the current CLI prints the whole thing; offer to scroll or save to
  a file if the user asks).
- **Proposal on a deleted widget**: shouldn't happen; if it does,
  flag and skip.
- **Proposal expired mid-walk**: the cloud returns 410. Move on.
- **User wants to amend the proposal rather than accept/reject**:
  out of scope. Direct them to ask the submitter to resubmit.

## Scope

This skill only walks pending proposals. It does not:
- teach what proposals or governance are (cg-cloud)
- change governance defaults (cg-config)
- publish, unpublish, or adopt widgets (cg-cloud for the concepts,
  direct MCP calls for the actions)
- edit widget code (that's a different workflow entirely)

If the conversation moves off proposal review, let this skill end.

## What not to do

- Don't walk the queue without gating on auth first.
- Don't recommend accept or reject. Surface signal; user decides.
- Don't accept `--reject` without a reason.
- Don't batch decisions to save time.
- Don't summarize decisions in aggregate at the end — the per-item
  confirmations already did that.
- Don't teach governance concepts here. Hand to cg-cloud.
