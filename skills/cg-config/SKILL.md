---
description: Invoke when the user expresses configuration intent, asks how to set up Cartograph, or mentions preferences like private widgets, company registries, auto-publish, or binary paths. Walks the user through current settings and translates intent into config changes. Triggers on "how do I set up", "configure Cartograph", "change my settings", "keep widgets private", "use my company registry", "turn off auto-publish", or "where does Cartograph look for nim/iverilog/openscad".
---

# cg-config — walk the user through configuration choices

Cartograph has a small set of settings that encode important decisions.
The user rarely reads them all on their own. Your job is to surface
the ones that matter, explain the tradeoff, and apply the choice.

## The settings that matter

**auto-publish** (default: false)
Controls whether `checkin` automatically pushes the new version to
the cloud registry. `true` is convenient for solo devs with public
widgets. `false` is safer if the user is working on private code
or hasn't decided what's shareable yet. Ask before flipping.

**visibility** (default: private)
The default visibility for widgets the user publishes. `public` means
anyone on the registry can install it. `private` means only the user
and invited collaborators. If the user sets `public` casually, double
-check — "public" means "the world, forever." Publishing proprietary
logic as public is hard to take back.

**governance** (default: open)
Controls who can propose changes to published widgets. `open` lets
community members submit proposals. `closed` means only the owner
edits. Open is the default for healthy widgets.

**show-unavailable** (default: false)
When `true`, search results include widgets whose language engine
isn't installed on this machine. Useful for browsing. Defaults to
`false` because installing an unavailable widget fails.

**publish-registry** (default: cg)
The registry prefix that receives checkin/publish calls. `cg` is the
public community registry. Companies run their own with custom
prefixes (e.g. `acme-`) for internal widgets.

**paths.\<binary\>** (default: auto-detect)
Override where Cartograph looks for language engines (nim, iverilog,
openscad, composer, ng, etc). Only set when auto-detection fails.

## Conversation pattern

1. **Start with `cartograph_config`** (list mode) to show the current
   state. Render it in prose — group by theme (visibility, publishing,
   paths), not alphabetically.

2. **Ask what the user actually wants.** Don't walk them through every
   setting. Common intents:
   - "I want to keep my widgets private" → set `visibility=private`,
     confirm `auto-publish=false` unless they want their own private
     cloud workflow.
   - "I want to publish to my company registry" → walk through
     `registry add` first, then set `publish-registry=<prefix>`.
   - "I want to auto-publish" → confirm `visibility` matches the
     intent (public defaults to community-visible), then flip.
   - "Nim isn't found" → set `paths.nim` to the binary location.

3. **Show the diff before applying.** State current value → new
   value in one sentence per change. Wait for confirmation.

4. **Apply with `cartograph_config`** (set mode), one key at a time.

## Safety reminders

- Never set `visibility=public` without naming the widgets affected.
- Never change `publish-registry` without confirming the prefix
  matches an added registry.
- `paths.<binary>` values should be absolute paths. Relative paths
  break across projects.
