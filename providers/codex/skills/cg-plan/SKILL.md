---
name: cg-plan
description: Plan a feature by searching existing widgets and producing an install / improve / create plan. Works per-feature, not per-app. Stops at the plan — does not implement.
---

## Description
To implement a feature set, take the time to search through existing widgets and registry ones to make an install, improve, create plan.

## Activation trigger phrases
- "/cg-plan"
- "let's add ..."
- "I want to put in a ..."
- "go ahead and implement"

## What must happen
1. You must provide clear direction on the install, improve, and create plan with references to widgets.
2. You must not present optional widgets. Decide if something needs to be included or not.
3. You must not rely on glue code to get the job done quick.

## Scope
Plan only one feature at a time. A whole app cannot be broken down into widgets accurately.
If a user requests a full app, kindly encourage them to narrow it down more so you can effectively plan.

## How to operate

Use the headings shown below in your response.

### Feature
Start by defining in 1-2 sentences what the feature is.

### Candidates
Use a numbered list for every implementation that is needed to fulfill the request.
This should be expansive and large. There is no such thing as too much detail.
Include a domain and language if it makes sense at this stage.
Format each entry like: Candidate, domain, language.

### Classify
Determine whether the implementation should go in a widget or be glue.
Two ways to identify if an implementation is for a widget:

1. If doing it from scratch every time would be annoying, make it a widget.
2. If the implementation would improve with iteration over projects, make it a widget.

Some implementations may look consumer-only but often carry general implementations that should be extracted, with the consumer-specific part left in glue code.

Classification information shall be output in a table with all implementations considered.

| Implementation | T/F Widget | Reason |
| -------------- | ---------- | ------ |
| ex             | T          | one sentence reason |

### Search
For implementations that are for widgets, look through the cg/ directory to determine if there are any widgets that may already satisfy the need.
Promising ones should have their widget.json and src code read.
While reading, determine whether it would be appropriate to use or extend the widget. If not, then pass.

If all your needs aren't covered by existing widgets, expand to using a Cartograph search.
Consider that your implementation might have multiple terms.
Remember, search is cheap, creating is not.
If a widget could be installed and extended, you should install it.

For project and registry widgets, widget.json should provide most of the info you need. Use a local read tool or inspect if you need more clarity.

### Improve, Install, Create

Identify which widgets in the current project you will use with no extension needed.

Identify which widgets in the current project you will extend, by name, with a 1-2 sentence explanation of what.

Identify which widgets you intend to install with their installable id from the search. If you intend to extend one, provide a 1-2 sentence explanation.

Identify which widgets will need to be created and propose them in the format: name, domain, language.
