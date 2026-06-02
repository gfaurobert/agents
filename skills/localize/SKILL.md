---
name: localize
description: Use when the user asks to translate or localize content via a /localize command (especially JSON i18n files) and intent, tone, and placeholder/token integrity must be preserved.
---

# Localize

## Overview

`/localize` translates content to a target locale while preserving **intent** and **detected tone**, enforcing strict **token integrity** (placeholders/tags), and validating meaning via **back-translation**.

## When to Use

Use when the user:
- wants to translate/localize copy or i18n resources (JSON string values)
- provides `/localize …` with a target locale (e.g. `DE`, `fr-FR`)
- requires “meaning must not change”, not just fluency

Do not use when:
- the user wants literal word-for-word translation regardless of naturalness
- the content is a legal contract where wording must remain exact (ask for explicit instruction)

## Command Forms (v1)

Supported inputs:
- `/localize @path/to/file.json DE`
- `/localize DE` (pasted content in same message)
- `/localize @path/to/file.json` (ask one follow-up for locale)
- `/localize @file.json DE --glossary @glossary.json`

Reject malformed commands with a short usage hint (no guessing).

## What to Translate (JSON rules)

For JSON:
- Translate **string values only**
- Preserve exactly:
  - JSON structure + key names
  - placeholders and interpolation tokens (`{name}`, `%s`, `{{count}}`, ICU)
  - URLs, IDs/SKUs, code snippets, non-linguistic tokens
  - HTML/Markdown tags (translate surrounding human text)

Fail fast if output JSON is invalid.

## Tone + Intent Requirements

- **Detect tone from source** and preserve it in the target language.
- **Intent must be kept** (no added/removed constraints, negation flips, scope changes, wrong entities/numbers, wrong user actions).

## Glossary (hybrid)

Optional user glossary `--glossary @glossary.json` entries:
- `source_term`, `target_term`, `do_not_translate`, optional `notes`

Agent-managed state (requires explicit approval to promote suggestions → approved):
- `skills/localize/state/glossary-approved.json`
- `skills/localize/state/glossary-suggested.json`
- `skills/localize/state/runs-log.jsonl` (append-only)

## Agent Roster & Orchestration (required)

Parent `/localize` orchestrator runs:
1) Translation Subagent A (parallel)
2) Translation Subagent B (parallel)
3) Merge/Judge agent
4) Back-translation agent (target → source)
5) Comparison agent (source vs back-translated source)
6) Correction agent (patch failed paths only)
7) Re-check changed paths (max 2 rounds)

### Translation Subagent Contract (schema)

Both A and B MUST return the same structure:
- `neutral_source`: culture-agnostic rewrite in source language
- `final_translation`: target-language result (for JSON: per key path)
- `tone_analysis`: detected tone + how preserved
- `intent_checks`: key meaning points preserved
- `terminology_map`: applied glossary + repeated-term decisions
- `integrity_checks`: placeholders/tags/tokens preserved + JSON validity
- `confidence`: 0–1 + rationale
- `issues`: uncertainties/flags

### Merge/Judge Policy (deterministic)

When A and B differ:
- Prefer structurally valid output (JSON valid + placeholders/tags intact)
- Then prefer higher meaning fidelity to the source
- If still tied, judge per key path/segment and merge best parts with brief rationale

## Back-Translation Meaning Gate

### What gets back-translated

- Back-translate **only the merged candidate** (what you would ship)
- For JSON, do it **per key path** (string-by-string), not as one concatenated document

### Integrity gates (hard)

Before meaning comparison (and re-checked after corrections):
- JSON validity (if applicable)
- placeholders/tags/tokens preserved exactly
- structure/keys unchanged
- glossary `do_not_translate` respected

Any integrity break is a `fail` for that path.

### Comparison verdicts (per key path)

Comparison agent returns for each path:
- `path`
- `verdict`: `pass` | `warn` | `fail`
- `reason`, `sourceSnippet`, `backSnippet`

Rules:
- `pass`: same intent, wording drift only
- `warn`: minor ambiguity/tone shift, meaning likely OK (report it)
- `fail`: meaning deviation (negation flip, wrong entity/number, changed constraints, wrong user action)

**Global gate:** any `fail` on critical paths (CTA, pricing, legal/safety, permissions) blocks writing output until fixed.

### Correction loop

If any `fail`:
- Correction agent patches **only failed paths** in target translation (no full re-translate)
- Re-run back-translation + comparison on **changed paths only**
- Max 2 rounds; if `fail` remains → stop, no file write, return `needs human review`

## Output Contract

- Never overwrite source by default.
- `@file.json` + `DE` → write sibling `file.de.json`.
- Always return a QA report including:
  - detected tone + how preserved
  - intent checks
  - adaptations made (dates/numbers/units when user-facing)
  - placeholder/tag/token integrity
  - terminology decisions + suggested glossary entries
  - back-translation rounds used + corrected paths + remaining warnings

## Examples

### File-based JSON

User:
`/localize @app/messages.json DE`

Output:
- `app/messages.de.json`
- QA report (tone, integrity, meaning gate)

### Pasted content + glossary

User:
`/localize fr-FR --glossary @glossary.json`
<pasted content>

Output:
- translated content
- QA report + glossary suggestions (if any)

## Common Mistakes

- Translating JSON keys (never)
- Breaking placeholders/ICU patterns (hard fail)
- Skipping back-translation check (don’t ship without meaning gate passing)
- “Improving” legal/compliance meaning (flag instead of rewriting obligations)

