# 3D Printing Tips Index

Symptom lookup for the troubleshooting skill. Grep this file first, then read the linked source.

**Printer context:** `printers/anycubic-vyper.md`

---

## Bed adhesion / warping

| Symptom | Source | Section |
|---------|--------|---------|
| Part won't stick to bed | `reference/alexandre-chappel.md` | Tips 3, 4, 5 |
| Corner lifting (large flat parts) | `reference/alexandre-chappel.md` | Tip 27 (dog ears) |
| Small part won't stick | `reference/alexandre-chappel.md` | Tip 26 (brim) |
| Brim hard to remove | `reference/alexandre-chappel.md` | Tip 27, 28 (deburring tool) |
| Room too cold / drafts | `reference/alexandre-chappel.md` | Tip 29 |
| Vyper: mesh/adhesion after move | `printers/anycubic-vyper.md` | Troubleshooting shortcuts |

## Print failure mid-job

| Symptom | Source | Section |
|---------|--------|---------|
| Spaghetti / print in midair | `reference/alexandre-chappel.md` | Tip 31 |
| Print knocked over | `reference/alexandre-chappel.md` | Tip 31 |
| Missing supports | `reference/alexandre-chappel.md` | Tips 19, 21, 42 |

## Layer quality / extrusion

| Symptom | Source | Section |
|---------|--------|---------|
| Gaps, under-extrusion, poor infill | `reference/alexandre-chappel.md` | Tip 32 |
| Clogged nozzle | `reference/alexandre-chappel.md` | Tip 32 (cold pull / replace) |
| Stringing (PETG) | `printers/anycubic-vyper.md` | Dry filament; PETG row |
| Unknown quality issue | `reference/alexandre-chappel.md` | Tip 30 (print Benchy) |

## Supports & bridging

| Symptom | Source | Section |
|---------|--------|---------|
| Support type choice | `reference/alexandre-chappel.md` | Tip 19 |
| Bridge failing | `reference/alexandre-chappel.md` | Tips 20, 24 |
| Too many supports | `reference/alexandre-chappel.md` | Tips 21, 42 |

## Slicer settings (OrcaSlicer)

| Symptom | Source | Section |
|---------|--------|---------|
| Print too slow | `reference/alexandre-chappel.md` | Tips 11, 12, 14, 25 |
| Part not strong enough | `reference/alexandre-chappel.md` | Tip 13 (perimeters) |
| Creator settings not applying | `reference/alexandre-chappel.md` | Tip 15 (advanced mode) |
| Wrong temperatures / speeds | `reference/alexandre-chappel.md` | Tips 8, 9 |
| PETG/TPU too fast (Vyper) | `printers/anycubic-vyper.md` | Known quirks |

## Design for printing

| Symptom | Source | Section |
|---------|--------|---------|
| Weak part / snapped handle | `reference/alexandre-chappel.md` | Tip 54 (orientation) |
| Holes wrong size | `reference/alexandre-chappel.md` | Tips 44, 55–57 |
| Part weaker than expected | `reference/alexandre-chappel.md` | Tip 41 (blocky > ribs) |

## Lessons learned (project-specific)

| Symptom | Source | Section |
|---------|--------|---------|
| *(none yet)* | `lessons-learned/` | Add entries as you solve problems |

---

## How to add a lesson

1. Create `lessons-learned/YYYY-MM-DD-short-name.md` from `_template.md`
2. Add a row above under the matching symptom category
3. Set `verified: true` in the lesson frontmatter
