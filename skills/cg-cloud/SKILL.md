---
description: Invoke when the user wants to publish a widget, change its visibility, manage proposals from the community, unpublish, or work with a non-default registry. Explains the publishing workflow, visibility tradeoffs, governance model, and proposal review. Triggers on "publish this", "share my widget", "make this public", "community submitted a change", "review proposal", "unpublish", "add registry", or "publish to my company's registry".
---

# cg-cloud — publish, share, and govern widgets

Publishing is a meaningful decision. Your job is to make sure the user
understands what they're agreeing to before bits leave their machine.

## How publishing works

Two paths:

**Auto-publish on checkin.** With `auto-publish=true` (see cg-config),
every successful `checkin_widget` pushes the new version to the
registry in `publish-registry`. Fast, but assumes the user wants
everything shared.

**Manual publish.** With `auto-publish=false`, checkin stays local.
The user runs `cloud publish <widget_id>` explicitly when ready.
Recommended default — separates "working draft" from "shared."

## Visibility: public vs private

- **public**: anyone who installs the registry prefix can install the
  widget. Search ranking is global. Community members can propose
  changes if `governance=open`.
- **private**: only the user and invited collaborators see it. Does
  not appear in community search. Use for proprietary logic or
  work-in-progress.

**Before flipping to public, ask:**
- Does the widget contain anything project-specific (API keys,
  internal URLs, domain-specific names)? If yes, don't publish.
- Is the widget fully tested and stamped? Unstamped widgets are
  filtered from search — a stamp regression hides the widget from
  users without warning.
- Would you be comfortable showing this to a senior engineer at
  another company? If no, keep it private.

Public is permanent in spirit. Unpublishing removes listings but
anyone who installed before still has the code.

## Governance and proposals

**governance=open** (default): community members can submit proposals
to improve a widget. Owners review and accept or reject. Good default
for healthy public widgets.

**governance=closed**: only the owner edits. Use for widgets with
strong opinions or security boundaries.

**Reviewing proposals:**

1. `cloud proposals <widget_id>` lists pending submissions.
2. Read the diff and the proposer's reason.
3. If you like it: `cloud proposals <widget_id> --accept`.
4. If you don't: `cloud proposals <widget_id> --reject --reason "..."`.
   Always give a reason — proposers learn from it.

## Multi-registry

Registries are identified by a prefix. `cg` is the public registry.
Companies run their own with custom prefixes.

- `registry add <url>` — prefix is fetched from `/info` automatically.
- `registry remove <prefix>` — stop using a registry.
- A widget's registry is determined by its prefix in the widget_id
  (e.g. `acme-backend-retry-python` publishes to the `acme` registry).

## Adopt: linking a local widget to an existing cloud one

If a widget exists locally and on the cloud but isn't yet linked
(e.g. imported from a colleague), use:

    cloud adopt <local-id> <@owner/prefix-widget-id>

This verifies source identity and writes a `.cartograph_source`
sidecar so future `checkin --publish` routes correctly.

## Unpublishing

`cloud unpublish <widget_id> --confirm` removes the widget from
registry listings. Warn the user that:
- Users who already installed still have the code.
- Search will no longer surface it.
- The user can republish later with the same widget_id.

Always require `--confirm`. Don't pass it silently.
