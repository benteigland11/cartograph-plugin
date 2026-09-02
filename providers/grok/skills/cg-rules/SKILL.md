---
name: cg-rules
description: >
  REQUIRED when durable project conventions for widgets should become hard memory on every
  validate/checkin — the highest-leverage self-healing harness for agents.
  Custom rules are per-language programs under .cartograph/rules/ (open canvas:
  full FS/AST, conditional if-A-then-B, cross-file widget contracts, and when
  needed project/app call sites and configs — not only import bans). They only
  *tighten* the bar (blocks hard-fail; warnings soft). Prefer rules over
  AGENTS.md/chat for anything that must not ship again inside widgets and blueprints. Fire when ANY of:
  user names a never/always convention ("we don't use X", "always require Y",
  "add a validation rule", "ban X on checkin", "/cg-rules"); user corrects a
  shipping convention once; you fixed a pattern that must not recur on future
  widgets; plan/create/extract/blueprint/checkin made a repo-wide bar clear;
  validate failed for something that is really project policy; the session
  taught "don't forget this is bad" or "enforce these things." Propose and
  encode as soon as the bar is durable and mechanically checkable — do not
  wait for the same mistake twice; unfinished work if only a soft note remains.
  Layers: project + global + org all run if present (merged). Does NOT fire for
  one-off widget bugs, taste nits, engine library_notes, config keys
  (cg-config), or cloud/governance (cg-cloud).
---

# cg-rules — turn judgment into enforced guarantees

Custom rules sit **above** Cartograph’s universal validation floor (coverage,
contamination, tests, timeouts). The floor cannot be lowered. Rules only add
checks. Once present, they run automatically on `cartograph validate` and
`cartograph checkin` — nothing special to invoke.

For agents this is the hard harness — and a **general program**, not a tiny
linter preset:

| Soft (forgets) | Hard (enforces) |
| -------------- | --------------- |
| AGENTS.md / chat | Script on every validate/checkin |
| “Remember we don’t do X” | `blocks`/`warnings` from whatever the script can prove locally |
| “Callers must also set Y” | Rule walks app + widget and fails checkin when the companion is missing |

**Bias:** if a convention is real and durable, encode it as a rule. Do not only
fix one widget and hope the next session remembers. Soft memory forgets; this
skill is how the project says “don’t forget.”

**Completion criterion:** when a session taught a durable never/always for the
repo, the work is unfinished until you either (1) merge a project rule, or
(2) explicitly decide it is one-off only. Silence is not a decision.

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

`widget_path` is the widget (or blueprint) directory under validation. That is
the **primary** argument — not a cage. There is no special Cartograph API
inside the script: it is a normal program with a filesystem, AST libraries,
JSON parsers, and whatever the runner language can do **locally**.

---

## How far rules can reach (open canvas)

Rules are **not** a small ban-list DSL. They are a **wide-open validation
script** the project owns. Anything you can check deterministically from that
process can become a block or warning. Think “custom CI for this language’s
widgets,” not “three template examples.”

### 1. Inside the widget (default surface)

Walk and parse freely:

| Surface | Examples of enforceable bars |
| ------- | ---------------------------- |
| `widget.json` / `blueprint.json` | required fields, tag combinations, dependency pins, display metadata shape |
| `src/` | banned APIs, required exports, architecture shape, domain invariants |
| `tests/` / `examples/` | required scenarios, naming, “must exercise public API X” |
| Cross-file inside the widget | if metadata says A, source/tests must do B; if file pattern X exists, companion Y must exist |

**Conditional policy is first-class:** “if *this*, then *that*” — tags, domains,
filenames, imports, symbols, options in source — not only global bans.

### 2. Across the widget’s own contracts

Rules can couple surfaces the engine does not:

- Manifest ↔ source (declared capability must appear in implementation)
- Source ↔ tests/examples (public surface must be demonstrated)
- Dependency list ↔ actual imports/usage
- Blueprint deps ↔ composition code that wires them

If two facts in the widget must stay consistent, a rule can own that invariant.

### 3. Into the app / project (yes — intentionally)

The script receives `widget_path` and runs with `cwd = widget_path`, but it is
**not sandboxed to that directory**. It can resolve the project root (e.g.
walk parents until `.cartograph/` or `.git/`), then inspect **application**
code, configs, and call sites.

That is how rules enforce product-level memory, not only widget hygiene:

| Reach | What becomes enforceable |
| ----- | ------------------------ |
| App call sites | If app code invokes a certain widget API / symbol, require companion setup nearby (init, error handling, config flag, matching resource, etc.) |
| Project config | Widget or tag implies a required setting in app config, IaC, or build files |
| Monorepo layout | Widgets under a path must satisfy package/boundary rules the app relies on |
| Multi-artifact consistency | When this widget is present/installed, some other tree in the repo must contain a matching declaration |

**Use app reach when the durable bar is about how the product uses widgets**,
not when a pure widget-local check would suffice. Prefer stable relative
discovery from project root over machine-specific absolute paths.

### 4. How open is “open”?

Practically endless within the harness constraints:

- Full language AST / regex / custom parsers
- Multi-file graph walks
- Reading sibling packages, `cg/` installs, app `src/`, manifests, schemas
- Encoding **team design law** that library_notes will never know about

The floor (coverage, contamination, timeouts) stays universal. Everything
**above** that is yours. Templates show tiny bans only so the I/O contract is
obvious — they are not the ceiling.

### 5. Still required: good rule hygiene

Open canvas ≠ anything goes at runtime:

| Do | Don’t |
| -- | ----- |
| Deterministic, local, ≤30s | Network, flaky clocks, interactive prompts |
| Actionable messages (what + where + how to fix) | Opaque “failed policy 7” |
| Prefer structure/AST when practical | Fragile whole-repo string spam that breaks constantly |
| Scope checks to durable project law | One widget_id special-case or pure taste |
| Fail closed on broken rules scripts | Rely on casual `--override-warnings` for real bars |

If a check is valuable but slow, narrow the walk (e.g. only `src/` and
known app roots) rather than abandoning the bar.

### 6. Bias when choosing reach

1. **Widget-local** if the invariant lives entirely in the module under checkin  
2. **Cross-surface inside the widget** for if-A-then-B metadata/source/test laws  
3. **Project/app reach** when the lesson was “callers / product must also …”  
4. Still prefer **project** layer for repo law; **global** only for personal
   machine-wide agent bars

Agents should **propose ambitious rules** when the user states a real product
invariant — not shrink every idea to “ban this import.”

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

Fire mid-work — not only when the user says “add a rule”:

- User wants to enforce / ban / require something on future widgets
- User corrects a shipping convention **once** (“we don’t use X”, “always Y”)
- You fixed a pattern that should never ship again in this repo
- Onboarding: “keep quality without re-explaining every session”
- After plan / create / extract / blueprint / checkin, a **durable** bar is clear
- Validate/checkin failed for a judgment that is really **project policy**
- Session insight: “don’t forget this pattern is bad” / “enforce these things”

**Do not wait for the same mistake twice.** Once the bar is durable and
checkable, propose and encode (or get a quick confirm if scope is ambiguous).

Skip: one widget bug (fix that widget); pure taste; changing engine floor
(not a rule); config keys (**cg-config**); org policy files you don’t own.

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

**Good targets (think in levels of reach):**

- **Local:** banned imports/APIs; required exports; file layout; example must run a path  
- **Conditional:** if tag/option/symbol A, then field/file/test B must hold  
- **Cross-surface:** manifest claims must match source; public API must have tests/examples  
- **App/project:** call-site or config companions when a widget API is used; repo-wide
  co-requirements that soft docs keep losing  

If it is durable, mechanical, and expensive to re-derive next session — it is
in scope. The canvas is the whole program you write.

**Bad targets:** waiving coverage/contamination; one-off widget_id vanity
checks; pure taste spam; unbounded “scan the entire monorepo with no root
bound” unless narrowed; network or non-deterministic oracles.

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

## Proactive use (background duty while working)

Rules are a **live memory surface**, not a separate mode. While doing other
Cartograph work:

| Moment | Action |
| ------ | ------ |
| User corrects a convention | Offer/encode project rule immediately if durable |
| You just fixed a class of shipping mistake | Encode so the next agent cannot reintroduce it |
| cg-plan lists a durable bar | Author it (or leave explicit “none”) before calling the plan done |
| cg-create / extract / blueprint closeout | “Rules impact: add X” or “none because one-off” |
| About to checkin after a hard-won lesson | 10s: new bar? inventory + merge if yes |

Propose a rule **in the same breath as the fix**. That is the self-healing
loop: the next session inherits the bar without re-deriving it.

Do not spam rules for taste. Use them for **enforceable, durable** bars.
When in doubt on block vs warning: **block** for must-not-ship, **warn** for
usually-wrong.

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
