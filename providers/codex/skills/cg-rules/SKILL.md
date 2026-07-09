---
name: cg-rules
description: >
  REQUIRED when encoding durable conventions into Cartograph custom validation
  rules — the highest-leverage harness control for agents. Custom rules are
  per-language scripts that run on every validate/checkin and can only *tighten*
  the bar (blocks hard-fail; warnings soft). Prefer rules over AGENTS.md/chat
  memory for anything that must not ship again. Fire when: user names a
  convention to enforce, a repeated freehand mistake should never recur, a
  project/team standard is real but not in the engine floor, "add a validation
  rule", "ban X on checkin", "/cg-rules", or after plan/create/extract when a
  durable bar is clear. Also fire proactively when the same correction appears
  twice — propose a rule. Layers: project + global + org all run if present
  (merged). Does NOT fire for one-off widget fixes, engine library_notes,
  config keys (cg-config), or cloud/governance (cg-cloud).
---

# cg-rules — turn judgment into enforced guarantees

Custom rules sit **above** Cartograph’s universal validation floor (coverage,
contamination, tests, timeouts). The floor cannot be lowered. Rules only add
checks. Once present, they run automatically on `cartograph validate` and
`cartograph checkin` — nothing special to invoke.

For agents this is the hard harness:

| Soft (forgets) | Hard (enforces) |
| -------------- | --------------- |
| AGENTS.md / chat | Script on every validate/checkin |
| “Remember we don’t use pickle” | `blocks` when pickle appears in `src/` |

**Bias:** if a convention is real and durable, encode it as a rule. Do not only
fix one widget and hope the next session remembers.

Rules are **not retroactive**: already-stamped widgets keep their stamp. The new
bar applies the next time something is validated or checked in.

---

## Layers (all run if present — they stack)

Discovery order and run order for a given **widget language**:

1. **project** — `<cwd>/.cartograph/rules/<filename>`
2. **global** — `<user_data_dir>/rules/<filename>` (platform data dir)
3. **org** — each path in `$CARTOGRAPH_ORG_RULES` (pathsep-separated)

Every existing file is **executed**. Results **merge**. Messages are tagged
`[project]`, `[global]`, or `[org]`. Project does **not** replace global; all
active layers fire.

| Layer | Path (conceptually) | Lifecycle |
| ----- | ------------------- | --------- |
| **project** | `.cartograph/rules/` in the **current working directory** (repo) | Created by `rules init` / `rules write`. Checked into git with the project. Binds everyone who validates from that repo. |
| **global** | User data dir `rules/` (e.g. `~/.local/share/cartograph/rules/` on Linux) | **Auto-seeded** for every language the first time Cartograph resolves its library (`_ensure_global_rules`). Templates already exist even if empty of real checks. Binds this machine / this user’s Cartograph. |
| **org** | `$CARTOGRAPH_ORG_RULES` = file(s) and/or director(ies) | Org-pushed. Each entry: if **directory**, use `<dir>/<filename>` for the language; if **file**, only if basename matches that language’s filename. Agents almost never author these; list may show them. |

**cwd matters for project rules:** paths are resolved from process cwd, not from
the widget path. Run validate/checkin (and rules CLI) from the **project root**.

### Choosing a layer

- **Repo / team convention** → **project** (default for product work).
- **Personal agent bar on every project on this machine** → **global** (confirm
  with the user; affects all local work).
- **Org** → do not invent; environment owns it.

Adding a project rule does not turn off global/org. Read **all** layers for that
language before duplicating checks.

---

## Fixed filename + runner per language

Not free-form names. One script per language key:

| Language | Filename | Runner |
| -------- | -------- | ------ |
| python | `rules.py` | `python` |
| javascript | `rules.js` | `node` |
| typescript | `rules.typescript.js` | `node` |
| nim | `rules.nim` | `nim r --hints:off` |
| angular | `rules.angular.js` | `node` |
| php | `rules.php` | `php` |
| openscad | `rules.openscad.py` | `python` |
| systemverilog | `rules.sv.py` | `python` |
| css | `rules.css.js` | `node` |
| terraform | `rules.terraform.py` | `python` |
| go | `rules.go.py` | `python` |
| spice | `rules.spice.py` | `python` |
| rust | `rules.rust.py` | `python` |
| gdscript | `rules.gdscript.py` | `python` |
| java | `rules.java.py` | `python` |

Several non-Python languages still use a **Python** rules script (filename
suffix `.py`). Write checks in the language the **runner** executes, not
necessarily the widget language.

Unknown language → no custom rules file for that widget.

---

## How a rules script is actually run

From the validator, after built-in checks:

```text
run_all_rules(widget_path, language)
  → for each existing layer file in order project, global, org:
       runner [rules_file, abspath(widget_path)]
       cwd = widget_path
       timeout 30s
```

**Contract:**

- Process **exit 0** if the script itself is healthy.
- **Stdout:** one JSON object  
  `{"blocks": ["..."], "warnings": ["..."]}`  
  Empty arrays **or empty stdout** = pass for that file.
- **blocks** — hard fail; checkin rejected; no override.
- **warnings** — soft; user may pass with  
  `--override-warnings --override-reason "…"`.
- Non-zero exit, timeout, or invalid JSON → **block** explaining the script
  failure (broken rules break checkin — treat rules as production code).
- Cartograph prefixes each message with `[project]` / `[global]` / `[org]`.

`widget_path` is the widget (or blueprint) directory under validation. Inspect
with normal FS/AST tools:

- `widget.json` or `blueprint.json`
- `src/`, `tests/`, `examples/`

No special Cartograph API inside the script.

---

## How rules files are actually written (template shape)

`cartograph rules init` writes a **language template**. For Python the durable
pattern is:

```python
def validate(widget_path):
    blocks = []
    warnings = []
    # inspect widget_path/src, tests, examples, widget.json
    # blocks.append("what's wrong and where")
    # warnings.append("what looks off")
    return {"blocks": blocks, "warnings": warnings}

if __name__ == "__main__":
    import json, sys
    print(json.dumps(validate(sys.argv[1])))
```

Any script that honors argv + JSON stdout works; prefer keeping the template’s
`validate()` + `__main__` shape so humans and agents share one style.

Templates include commented examples (banned imports, line-count warnings,
extra pytest). Prefer **uncomment/adapt** and add clear messages over inventing
a new structure.

---

## CLI surface (source of truth for agents)

```text
cartograph rules                         # list all languages × scopes that exist
cartograph rules init  --language L [--global]
cartograph rules get   --language L [--global]
cartograph rules write --language L [--global] --content '…' | --from-file PATH | stdin
                       # existing file requires --confirm (full overwrite)
cartograph rules reset --language L [--global] --confirm   # wipe back to template
```

Default scope is **project**. Pass `--global` for the machine-wide file.

| Action | Behavior |
| ------ | -------- |
| **list** (no action) | Every rules file that exists (project + global + org), with paths |
| **init** | If missing: write template. If exists: **no overwrite** — only reports path |
| **get** | Read full file content (JSON with `--json`) |
| **write** | Write **entire** file body. Create dirs as needed. If file already exists, **requires `--confirm`**. Content: `--content`, `--from-file`, or stdin |
| **reset** | Overwrite with stock template; **requires `--confirm`** |

There is **no patch API**. Authoring is always:

1. `get` (or read the path from `list`)
2. Edit the full script locally (merge new checks into existing `validate`)
3. `write --confirm` with the **complete** new body

Never `reset` unless the user wants a wipe. Never drop existing checks when
adding one.

### MCP vs CLI

MCP `cg_rules` today: **list / init / reset** only.  
**get / write are CLI** — use shell for real authoring. Prefer:

```text
cartograph rules get --language python --json
# …edit…
cartograph rules write --language python --from-file /tmp/rules.py --confirm
```

For project rules, writing into `.cartograph/rules/` via CLI is git-friendly and
what teammates will load.

---

## When this skill applies

- User wants to enforce / ban / require something on future widgets
- Same class of mistake corrected more than once
- Onboarding: “keep quality without re-explaining every session”
- After plan/create/extract/blueprint, a **durable** bar is clear

Skip: one widget bug (fix that widget); changing engine floor (not a rule);
config keys (**cg-config**); org policy files you don’t own.

---

## How to operate

### 1. List what already runs

```text
cartograph rules
```

Note every path for the target language (project **and** global **and** org).
Open each relevant body:

```text
cartograph rules get --language python
cartograph rules get --language python --global
```

Do not add a check that already exists on another layer unless you intend
redundancy.

### 2. Name the convention

Before writing:

- **What** must not (or should rarely) ship
- **block vs warning**
- **language** (filename/runner)
- **layer** (project vs global; org only if instructed)

Confirm scope with the user when ambiguous. Default product work → **project**.

### 3. Ensure a file exists

**Project** (usually):

```text
cartograph rules init --language python
```

Creates `.cartograph/rules/rules.py` from template if missing.

**Global:** files are usually **already** there from engine bootstrap. Prefer
`get --global` then `write --global --confirm`. `init --global` only if listing
shows nothing (rare).

### 4. Implement (merge into the full file)

1. `get` full content.
2. Keep the template I/O contract.
3. Add checks inside `validate` (or equivalent) **alongside** existing ones.
4. Messages: what failed and where; actionable for the next agent.
5. Deterministic, local, fast (≤30s total). No network.
6. Prefer AST/structure over fragile whole-file string bans when practical.
7. `write` **full** file with `--confirm` if overwriting.

Good targets: banned imports/APIs, required metadata fields, domain-specific
shape, example constraints, “never freehand pattern X again.”

Bad targets: waiving coverage/contamination; one-off widget_id checks; pure
taste spam; slow full re-test harnesses unless the user asked for that policy.

### 5. Prove it

From **project root**:

1. `cartograph validate <widget>` (or MCP `cg_validate`) on something that
   should still pass.
2. Confirm failure path if safe (or reason about the condition) — do not leave
   the library broken.
3. Re-list and confirm the path you wrote (project vs global).

### 6. Ongoing

When validate prints `[project]` / `[global]` / `[org]` failures: fix the widget
**or** refine the rule if the rule was wrong. Do not normalize casual
`--override-warnings` for durable bars.

---

## Proactive use

During **cg-plan / cg-create / cg-extract / cg-blueprint**, if you learn a
recurring standard, **propose a rule in the same breath as the fix**. Ask to
encode it. That is using the harness: the next session inherits the bar without
re-deriving it.

Do not spam rules for taste. Use them for **recurring, enforceable, durable**
bars.

---

## Handoffs

| Need | Skill |
| ---- | ----- |
| Config keys (publish, visibility, …) | **cg-config** |
| One widget scaffold | **cg-create** (obey rules when validate fires) |
| Feature triage | **cg-plan** (may list “add project rule for …”) |
| Cloud | **cg-cloud** |

---

## What not to do

- Do not claim rules can lower the engine floor
- Do not assume only one layer runs — **list and get all layers** for the language
- Do not partial-patch via imaginary APIs — **full-file write** only
- Do not `write` over an existing file without `--confirm`
- Do not `reset` without explicit user intent
- Do not put repo conventions only in **global** (or only in chat)
- Do not author **org** paths unless the user owns that environment
- Do not invent rules outside project/global/org paths Cartograph loads
