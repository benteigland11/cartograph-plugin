---
name: cg-rules
description: >
  REQUIRED when encoding durable conventions into Cartograph custom validation
  rules — the highest-leverage harness control for agents. Custom rules are
  scripts that run on every `validate` and `checkin` and can only *tighten* the
  bar (blocks hard-fail; warnings soft). Prefer rules over hoping AGENTS.md or
  chat memory sticks. Fire when: user names a convention to enforce, a repeated
  freehand mistake should never ship again, a project/team standard is real but
  not in the engine floor, "add a validation rule", "ban X on checkin",
  "/cg-rules", or after create/plan/extract when a durable quality bar is clear.
  Also fire proactively when you notice the same correction twice — propose a
  rule. Scope: project (.cartograph/rules/, repo-shared) vs global (machine) vs
  org ($CARTOGRAPH_ORG_RULES). Does NOT fire for one-off widget fixes (edit the
  widget), engine library_notes (read-only floor), config defaults (cg-config),
  or cloud/governance (cg-cloud).
---

# cg-rules — turn judgment into enforced guarantees

Custom rules are how Cartograph lets **local opinion ride above the universal
floor**. The built-in pipeline (coverage, contamination, tests, timeouts) cannot
be lowered. Rules only add checks. Once a rule is in force, every validate and
checkin runs it — no special invoke step.

For agents this is the difference between:

| Soft (forgets) | Hard (enforces) |
| -------------- | --------------- |
| Note in AGENTS.md / chat | Script on validate/checkin |
| "Remember we don't use pickle" | `blocks` if pickle appears in `src/` |
| Style nit every PR | Automatic warning or block |

**Bias: when a convention is real and durable, encode it as a rule.** Do not
only fix the one widget and move on if the same class of bug will recur.

## When this skill applies

- User wants to enforce / ban / require something on all (or language-scoped)
  widgets going forward
- You or the user corrected the same class of issue more than once
- Onboarding a repo: "how do we keep quality without re-explaining every time?"
- After plan/create/extract, a **project-wide** standard is obvious (API shape,
  banned APIs, required tags, domain constraints)

Skip when the issue is one widget's bug (fix that widget), or when the check
belongs in Cartograph's universal floor (that's a product request, not a rule).

## Mental model

1. **Floor** — engine validation + `library_notes` on the widget. Non-negotiable.
2. **Custom rules** — your additive layer. Project / global / org scripts.
3. **Prompt text** — AGENTS.md, skills. Useful for *intent*; rules for *enforcement*.

Rules **cannot** waive coverage, contamination, or any built-in check. There is
no "exception below the floor."

Adding a rule is **not retroactive**: already-checked-in widgets keep their
stamp. The new bar applies on the next validate/checkin of something you touch.

## Scope (choose deliberately)

| Scope | Where | Who it binds | When to use |
| ----- | ----- | ------------ | ----------- |
| **Project** | `.cartograph/rules/` (checked into the repo) | Everyone on this project | Team/repo conventions |
| **Global** | user data dir rules (e.g. `~/.local/share/cartograph/rules/`) | This machine / your agent | Personal agent standards across projects |
| **Org** | `$CARTOGRAPH_ORG_RULES` paths | Org-pushed | Company-wide; agents rarely author these |

Default for shared product work: **project** rules. Default for "I never want
my agent to ship X anywhere": **global**. Confirm before writing global.

One rules **file per language** (e.g. `rules.py` for Python). Language-scoped
checks stay in that file — do not invent cross-language magic in one script.

## Tool boundary

| Action | How |
| ------ | --- |
| List active rules | MCP `cg_rules` list / `cartograph rules` |
| Init project (or global) template | MCP `cg_rules` init / `cartograph rules init --language <lang> [--global]` |
| Read current script | `cartograph rules get --language <lang> [--global]` |
| Write full file | `cartograph rules write --language <lang> [--global] --from-file path` or `--content` (use `--confirm` when overwriting) |
| Reset to template | MCP/CLI reset + `--confirm` (destructive) |

MCP today: **list / init / reset**. Prefer CLI **get / write** for read-modify-write
of the script body. For non-trivial edits: get → edit carefully → write with
confirm; do not `reset` unless the user wants a wipe.

Prefer editing the rules file in-repo under `.cartograph/rules/` when the project
already has one (git-friendly).

## Contract every rules script must honor

Cartograph runs: `runner rules_file <absolute_widget_or_blueprint_path>`

- **Exit 0** always when the script itself is healthy
- **Stdout**: one JSON object  
  `{"blocks": ["..."], "warnings": ["..."]}`  
  Empty arrays (or empty stdout) = pass
- **blocks** — hard fail; checkin rejected; no override
- **warnings** — soft; user may `--override-warnings` with a reason
- Timeout ~30s; keep checks fast
- Inspect `widget_path` (or blueprint path) with normal filesystem/AST tools —
  `widget.json` / `blueprint.json`, `src/`, `tests/`, `examples/`

A broken rules script (non-zero exit, invalid JSON) becomes a **block** with a
fix-the-script message. Treat rules code as production: test it.

## How to operate

### 1. Discover what is already enforced

```text
cartograph rules
cartograph rules get --language <lang>
# project vs global paths in the list
```

Read existing checks before adding duplicates. Merge into the same language file.

### 2. Name the convention

State in one sentence:

- **What** must never (or should rarely) ship
- **block vs warning** (never ship → block; usually wrong → warning)
- **project vs global**
- **language**

Get user agreement on block-level and scope before writing, unless they already
mandated it.

### 3. Init if missing

Project:

```text
cartograph rules init --language python
```

Then edit `.cartograph/rules/rules.py` (or language-specific filename).

### 4. Implement the check

Pattern:

1. Walk/read `src/` (and metadata if needed)
2. Detect the forbidden or required condition
3. `blocks.append("clear message + where")` or `warnings.append(...)`
4. Print JSON at the end (template already does this)

Good rules:

- Deterministic, local (no network)
- Messages tell the agent **what to fix**
- Target the convention, not one widget's id
- Prefer AST/structure over brittle full-file string bans when possible

Bad rules:

- Trying to disable built-in validation
- Project-name hardcodes that block legitimate reuse (unless truly required)
- Slow full test re-runs unless the user asked for extra test policy
- One-off "fix this widget" logic

### 5. Prove it

1. Run `cg_validate` / `cartograph validate` on a widget that **should pass**
2. If possible, temporarily violate the rule on a scratch path or show the
   condition would block — without leaving the library broken
3. Confirm the rule file is the one you think (project vs global)

### 6. Hand back to the workflow

Rules now apply on every later create/extract/checkin. When validating widgets,
if a **[project]** or **[global]** block fires, fix the widget **or** refine the
rule if the rule was wrong — do not teach the user to override casually.

## Proactive use (agents should want this)

During **cg-plan / cg-create / cg-extract / cg-blueprint**, if you learn:

- "We never allow dependency X in leaf widgets"
- "Every security-domain widget must document threat notes in custom_notes"
- "No raw SQL strings outside the db widget"
- "Examples must not import pytest"

…then **propose a rule** in the same breath as the fix. Ask to encode it. That
is taking advantage of the harness: the next session and the next agent inherit
the bar without re-deriving it.

Do not spam rules for taste. Spam for **recurring, enforceable, durable** bars.

## Handoffs

| Need | Skill |
| ---- | ----- |
| Defaults: publish, visibility, registries | **cg-config** |
| Fill one widget scaffold | **cg-create** (obey rules when they fire on validate) |
| Feature plan | **cg-plan** (may list "add project rule for …") |
| Cloud publish | **cg-cloud** |

## What not to do

- Do not use rules to lower the Cartograph floor (impossible; don't pretend)
- Do not reset rules without explicit confirm
- Do not write only to global when the convention is this repo's
- Do not leave conventions solely in chat when they should block checkin
- Do not invent a second rules system outside `.cartograph/rules` / global paths
