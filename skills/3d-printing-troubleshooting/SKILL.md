---
name: 3d-printing-troubleshooting
description: Use when FDM 3D prints fail or show quality issues — warping, bed adhesion, spaghetti, layer gaps, stringing, supports, bridging, or OrcaSlicer tuning — on the Anycubic Vyper or similar printers.
---

# 3D Printing Troubleshooting

**Skill root:** `/home/gregoire/.agents/skills/3d-printing-troubleshooting`

## Overview

Diagnose FDM print failures using a searchable tips knowledge base, your printer context, and the OrcaSlicer MCP server.

## When to use

- Print failed, warped, or poor surface quality
- Bed adhesion, spaghetti, layer gaps, stringing
- OrcaSlicer profile or setting questions
- After fixing an issue — capture a lesson learned

## Workflow

1. **Load printer context** — read `/home/gregoire/.agents/skills/3d-printing-troubleshooting/printers/anycubic-vyper.md` (or the active printer file).
2. **Extract symptoms** from the user's description.
3. **Search** `/home/gregoire/.agents/skills/3d-printing-troubleshooting/tips-index.md` for matching symptoms; read linked reference and `lessons-learned/` entries.
4. **Query OrcaSlicer MCP** for current profile/settings; compare against tips and printer context.
5. **Apply tips in priority order:** bed adhesion → supports → material/temperature → nozzle/clog → calibration.
6. **Propose fixes** — specific Orca setting changes when possible.
7. **On confirmed fix** — append a new file in `lessons-learned/` using `_template.md` and add a row to `tips-index.md`.

## Knowledge base layout

All paths relative to `/home/gregoire/.agents/skills/3d-printing-troubleshooting/`:

| Path | Contents |
|------|----------|
| `printers/anycubic-vyper.md` | Machine specs, your filaments, Orca profiles, quirks |
| `tips-index.md` | Symptom → tip lookup table |
| `reference/` | Curated external tips (videos, guides) |
| `lessons-learned/` | Your resolved problems (grows over time) |

## Active printer

**Anycubic Vyper** — see `printers/anycubic-vyper.md`.

## Saving a lesson learned

Only after the user confirms the fix worked:

1. Copy `lessons-learned/_template.md` → `lessons-learned/YYYY-MM-DD-short-description.md`
2. Fill frontmatter (`symptoms`, `material`, `tags`, `verified: true`)
3. Add one row to `tips-index.md` under the matching symptom category

All files live under `/home/gregoire/.agents/skills/3d-printing-troubleshooting/` — not in project repos.
