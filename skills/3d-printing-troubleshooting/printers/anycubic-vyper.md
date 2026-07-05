# Anycubic Vyper — Printer Context

> **Purpose:** Machine-specific facts for the 3D printing troubleshooting skill.  
> The agent reads this file to apply general tips to *this* printer.  
> Update the **Your setup** sections as you dial in profiles and learn quirks.

**Status:** Active (primary printer)  
**Last updated:** 2026-07-01

---

## Printer overview

| Field | Value |
|-------|-------|
| Make / model | Anycubic Vyper |
| Technology | FDM (single extruder) |
| Build volume | 245 × 245 × 260 mm (L × W × H) |
| Nozzle (stock) | 0.4 mm |
| Hotend | Volcano-style |
| Filament diameter | 1.75 mm |
| Frame | Open (no enclosure) |
| Bed leveling | Automatic — 16-point probe (strain gauge on nozzle) |
| UI | 4.3" color touchscreen |

---

## Temperature limits

| Component | Max | Notes |
|-----------|-----|-------|
| Nozzle | 260°C | Enough for PLA, PETG, TPU, ABS |
| Heated bed | 110°C | Magnetic flex plate |
| Ambient | 8–40°C | Open frame — drafts and cold rooms affect warping |

**Not ideal without enclosure:** nylon, polycarbonate, and other high-temp engineering filaments.

**Heating behavior:** The bed reaches target temperature **before** the nozzle starts heating. Printing begins only after both are at target.

---

## Build plate

| Field | Value |
|-------|-------|
| Type | Magnetic, flexible spring steel sheet |
| Surface | Textured PEI (not Ultrabase) |
| Removal | Flex the plate to pop prints off — wait for bed to cool first |

### Bed care (from general tips + Vyper notes)

- Clean with **dish soap and water**; avoid touching the surface with oily fingers
- Consider a **glue stick** coat before prints if adhesion is inconsistent
- **Wait for the bed to cool** before removing models (hot PEI can bond too strongly)
- Re-run **auto bed leveling** if you move the printer or after nozzle crashes

### Before auto leveling

- Clean the nozzle tip (brass brush while hot) so the probe touches the bed accurately
- Optionally unload filament before leveling to avoid dribble affecting the mesh

---

## Motion & quality

| Field | Value |
|-------|-------|
| Suggested print speed | ~80 mm/s (range 20–100 mm/s per manual) |
| Positioning accuracy | X/Y 0.0125 mm, Z 0.002 mm |
| Print accuracy | ±0.1 mm |

**Vyper note:** Volcano hotend can handle higher flow when tuned, but stock/community profiles may be conservative — verify speeds when switching materials.

---

## Supported materials (manufacturer)

PLA, PETG, TPU, ABS, wood-filled, and similar mid-temp filaments.

| Material | Typical use on this printer | Notes |
|----------|----------------------------|-------|
| PLA | Default / daily driver | Easiest; good starting point |
| PETG | Functional / outdoor parts | Dry filament; watch corner lifting on large flats |
| TPU | Flexible parts | Use slow speeds; may need profile tuning |
| ABS | Higher temp parts | Hard on open frame — expect warping without enclosure |

---

## Your setup

> Fill these in as you dial in OrcaSlicer. The agent uses this to compare live MCP settings against your baselines.

### Nozzle & upgrades

- Current nozzle: `0.4 mm` *(stock — update if changed)*
- Nozzle material: `stock` *(brass / hardened / etc.)*
- Upgrades installed: `none noted` *(fill in: BLTouch tweaks, fan ducts, etc.)*

### Filaments you actually use

| Slot | Brand / material | Color | Dried? | Notes |
|------|------------------|-------|--------|-------|
| 1 | | PLA | | |
| 2 | | PETG | | |
| 3 | | | | |

### OrcaSlicer

| Field | Your value |
|-------|------------|
| Printer profile name | `<!-- e.g. Anycubic Vyper 0.4 nozzle -->` |
| Default layer height | `0.2 mm` *(typical starting point)* |
| Advanced mode | `on` *(recommended)* |
| Typical adhesion aid | `<!-- none / glue stick / brim / dog ears -->` |

**Per-material profiles** *(add rows as you create them):*

| Material | Orca profile name | Nozzle °C | Bed °C | Notes |
|----------|-------------------|-----------|--------|-------|
| PLA | | 200–210 | 60 | |
| PETG | | 230–240 | 70–80 | Dry first |
| TPU | | | | Slow speeds |

### Print environment

- Room temperature: `<!-- e.g. ~22°C -->`
- Drafts / AC nearby: `<!-- yes / no -->`
- Enclosure: `no` (open frame)

---

## Known quirks

> Add entries here (or in `lessons-learned/`) when you solve a problem. The agent checks both.

- Bed heats before nozzle — normal Vyper behavior, not a fault
- Textured PEI can over-stick if you remove prints while the bed is still hot
- Community reports: stock Cura profiles for PETG/TPU may print too fast — tune or use Orca profiles carefully
- Single nozzle — no multi-material dissolvable supports (PLA/PETG as breakaway only)

### Your lessons (quick notes)

<!-- Example:
- **2026-07-01 — PETG corner lift:** Dog ears on corners + bed 70°C fixed large flat boxes.
-->

---

## Troubleshooting shortcuts (Vyper-specific)

| Symptom | Check first on this printer |
|---------|------------------------------|
| First layer won't stick | Clean PEI, glue stick, re-run 16-point leveling, clean nozzle before level |
| Print knocked over mid-job | Adhesion (most common) — see general tips index |
| Mesh seems wrong after crash | Re-run auto bed leveling from touchscreen |
| PETG stringing / poor layers | Filament likely wet — dry before printing |
| ABS warping | Open frame limitation — enclosure or stick to PLA/PETG |
| Gaps / under-extrusion | Clog or speed too high for material profile |

For general FDM troubleshooting, see `tips-index.md` and `reference/alexandre-chappel.md`.

---

## Maintenance log

| Date | Action | Notes |
|------|--------|-------|
| | Nozzle clean / replace | |
| | Bed surface clean | |
| | Re-level | |

---

## Links

- [Anycubic Vyper product page](https://store.anycubic.com/products/anycubic-vyper)
- OrcaSlicer: primary slicer on this machine (use Orca MCP for live settings)
