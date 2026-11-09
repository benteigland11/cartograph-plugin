# cartograph-plugin

The Cartograph agent plugin (github.com/benteigland11/cartograph-plugin):
the `cartograph` MCP server plus the cg-* skills, packaged for Claude Code,
Grok, Codex, Gemini, OpenClaw, and Antigravity. Current version 0.1.19.

## Layout

    skills/<cg-*>/SKILL.md          canonical skills (edit these only)
    providers/grok/skills/          mirrored copies for Grok
    providers/codex/skills/         mirrored copies for Codex
    .claude-plugin/ .grok-plugin/ .agents/   host manifests + marketplaces
    GEMINI.md                       context file shipped to Gemini users
    scripts/versions.py             bumps and checks every host version

## Skills (shipped product, not agent instructions for this repo)

cg-plan (plan before implementing), cg-create (fill a scaffolded widget),
cg-extract (pull in-tree code into a widget), cg-blueprint (compose a feature),
cg-cloud (registry/account questions), cg-config (setup and defaults),
cg-proposals (review proposal queue), cg-rules (author custom validation rules).
Each skill's frontmatter description defines when it fires and which
sibling skill owns the neighboring case.

## Rules

- **Skills track the CLI.** When a CLI command, flag, or default changes, update
  the affected SKILL.md in the same change. Stale skills mislead every agent
  that loads them.
- **Edit the canonical `skills/` copy**, then copy that one file into
  `providers/grok/skills/<name>/` and `providers/codex/skills/<name>/`. Prefer
  the single-file copy when other skills have WIP; the full sync scripts
  rebuild every skill and would mix WIP in.
- **Bump every host together:** `python3 scripts/versions.py --bump patch`, then
  `python3 scripts/versions.py --check`. Set README **Version:** to the same
  number (it has drifted before).
- Don't bump cartograph-mcp for a skill-only change.
- Stage only release files (canonical skill, provider copies, manifests,
  README). Leave unrelated modified skills unstaged.
- Feature branch, PR, squash-merge to `main`. Only Ben merges.
- No em dashes in skills or docs. No `git reset --hard` over others' work.
