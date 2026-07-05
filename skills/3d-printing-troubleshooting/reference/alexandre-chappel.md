# 3D Printing Tips & Recommendations

**Source:** [It took me 16 Years to learn this... (tips & tricks)](https://www.youtube.com/watch?v=gPW_mitgosw)  
**Creator:** Alexandre Chappel  
**Duration:** 32:18  
**Published:** June 30, 2026

Alexandre Chappel shares 63 tips gathered over 16 years of 3D printing and design — from choosing your first printer to slicer settings, troubleshooting, and designing parts for FDM printing.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Printer & Build Plate](#printer--build-plate)
3. [Filament & Materials](#filament--materials)
4. [Slicers & Profiles](#slicers--profiles)
5. [Slicer Settings That Matter](#slicer-settings-that-matter)
6. [Supports, Bridging & Multi-Color](#supports-bridging--multi-color)
7. [Advanced Slicer Tricks](#advanced-slicer-tricks)
8. [Troubleshooting Common Issues](#troubleshooting-common-issues)
9. [3D Modeling Software](#3d-modeling-software)
10. [Design Philosophy](#design-philosophy)
11. [Designing for FDM](#designing-for-fdm)
12. [Hardware Integration](#hardware-integration)
13. [Print Orientation & Strength](#print-orientation--strength)
14. [Geometry, Tolerances & Holes](#geometry-tolerances--holes)
15. [Text & Labels](#text--labels)
16. [Resources Mentioned](#resources-mentioned)

---

## Getting Started

### Tip 1 — Start with an FDM printer
Your first 3D printer should be one that **melts plastic** (FDM/FFF). It works like a glue gun: a hot nozzle melts filament (a thin string of plastic) fed from the back. FDM is the **cheapest, safest, and least messy** option.

**What you need to get started:**
- The printer
- Filament (plastic)
- A way to send models to the printer — usually a computer + **slicer** software, though some manufacturers offer phone apps

### Tip 2 — You don't need to 3D model to print cool things
Many talented designers share models online. You can download and print without any modeling experience.

**Where to find models:**
- Personal sites like [alch.shop](https://www.alch.shop/)
- Free platforms: **Printables**, **MakerWorld** (often printable directly from your phone)

---

## Printer & Build Plate

### Tip 3 — Keep the build plate clean
Whether your printer is big or small, the hot nozzle deposits melted plastic onto the **build plate**. A dirty plate means prints won't stick.

- Clean with **regular dish soap and water**, then wipe dry
- **Don't touch** the plate with your fingers — skin oils prevent adhesion

### Tip 4 — Use a glue stick before every print
A coat of regular glue stick:
- Helps prints stick firmly during printing
- Makes removal easier when the print is done

The liquid adhesive versions do the same job but are less sticky and cost more.

### Tip 5 — Check bed adhesion first when something goes wrong
Before troubleshooting anything else, verify the part (or a corner/section) didn't **lift or come loose** during printing. Most print failures trace back to adhesion.

---

## Filament & Materials

### Tip 6 — PLA is the default; PETG for tougher conditions
| Material | Best for |
|----------|----------|
| **PLA** | Cheapest, easiest, strong enough for most projects (organizers, camera arms, boxes) |
| **PETG** | Outdoor use, UV resistance, ~70°C heat tolerance. Easiest material after PLA. Slightly less stiff, more brittle — **must be dried** before printing |

**Rule:** Anything other than PLA should be **properly dried and stored in a dry place**.

**Drying options:**
- Dedicated filament dryers
- AMS units on modern printers (some have high-temp drying)
- For PETG/ABS: crank up build plate heat, place spool on plate, cover it

### Tip 7 — Fancy materials = more hassle
Carbon- or glass-filled filaments:
- Are **abrasive** and wear out standard nozzles → need hardened nozzles (more expensive)
- Require higher temperatures, enclosures, heated chambers → expensive printers

If PLA can build a camera arm, you need a **good reason** to buy $100/spool exotic filament.

---

## Slicers & Profiles

### Tip 8 — Use your manufacturer's recommended slicer
If unsure which slicer to pick, download the one your printer maker recommends.

### Tip 9 — Always select the correct material profile
Whether you have generic PETG or branded PLA, picking the right profile sets correct temperatures and speeds — leading to much better results.

### Tip 10 — Match brand filament to brand printer
For printers from **Prusa, Creality, Bambu Lab**, using their name-brand filament gives properly tuned profiles for better results **and faster print times**.

---

## Slicer Settings That Matter

### Tip 11 — Layer height has the biggest impact on print time
| Setting | Result |
|---------|--------|
| **Higher layer height** | Faster, rougher surface |
| **Lower layer height** | Slower, smoother surface |

On straight-sided objects (like boxes), the visual difference is minimal — a coarse box took **40 min** vs. **3.5 hours** for fine layers with little visible difference. On curved models (like a figurine), the difference is obvious.

### Tip 12 — Use adaptive layers
Adaptive layers give the best of both worlds: thinner layers only where needed (e.g., top of a curved head), thicker layers on flat areas. Example: a Pikachu went from 52 min (coarse) / 3.5 hr (fine) to **1 hr 8 min** looking nearly identical to the fine version.

### Tip 13 — Increase perimeters, not infill, for strength
- **5% infill** is enough for decorative parts
- **15–20% infill** is usually plenty for functional parts
- For more strength, **increase wall perimeters** rather than infill

### Tip 14 — Larger nozzles speed up older/slower printers
On older printers that can't move fast, swap the standard **0.4 mm nozzle** for **0.6 or 0.8 mm** — similar quality, much faster. Less relevant on modern fast printers.

### Tip 15 — Turn on Advanced Mode in your slicer
Even if you never touch advanced settings, turn Advanced Mode **on**. Creators often bundle tuned print settings in project files that only apply when advanced mode is enabled. Just flip the switch — no other action needed.

### Tip 16 — Split multi-object files in the slicer
Downloaded files sometimes contain multiple objects stuck together. Split them into separate objects (in Bambu Studio: **Split → Objects** in the top menu).

### Tip 17 — Chop oversized models and add alignment connectors
If a model is too big for your printer, cut it into pieces in the slicer and add **connectors** on cut surfaces for easier gluing alignment.

### Tip 18 — Use modifiers for localized infill
Increase infill only in areas that need it (e.g., where bolts pass through) instead of raising infill globally.

---

## Supports, Bridging & Multi-Color

### Tip 19 — Choose the right support type
| Type | When to use |
|------|-------------|
| **Normal supports** | Only when the supported area is completely flat and supports can go straight from the build plate |
| **Tree supports** | Almost everything else — stick with defaults |
| **Normal supports setting** | Set to **Snug** if you must use them |

### Tip 20 — Test your printer's bridging ability
Printers can bridge surprisingly large gaps without supports. Print test models to find your acceptable bridging distance. **PLA bridges best.**

### Tip 21 — Manually select support areas
You don't have to support the entire model — manually mark only the key areas that need it in the slicer.

### Tip 22 — Be strategic with multi-color text placement
Adding contrasting-color text in the slicer has a huge time impact:
- **Top of model:** ~12 extra minutes (one color switch)
- **Side of model:** ~68 extra minutes on a small box (color switch every layer + purge tower waste)

Place accent colors where the printer switches **fewest times**.

### Tip 23 — Manual filament swap for multi-color (single-nozzle printers)
Add a **pause at a specific layer** in the slicer, manually change filament, and resume — works without an automatic multi-material system.

### Tip 24 — Dissolvable supports via incompatible filaments (multi-nozzle only)
Use **PETG as support for PLA** or **PLA as support for PETG** — but **only on multi-nozzle printers**. Single-nozzle machines leave residue that creates weak layer lines at the transition, causing bridges to fail.

---

## Advanced Slicer Tricks

### Tip 25 — Override line width for faster, precise walls
Manually set line width in the slicer independent of nozzle size. Example: with a **0.4 mm nozzle**, set line width to **0.75 mm** on uniformly **1.5 mm thick** walls → prints in **2 passes instead of 3**. Despite slower extrusion per line, total time drops significantly (e.g., a box from 40 min → **32 min**).

This is a core technique behind Chappel's fast, precise MotorBox print profiles.

---

## Troubleshooting Common Issues

### Tip 26 — Use a brim for small-footprint parts
If the plate is clean and glued but small parts still won't stick, add a **brim**.

### Tip 27 — Use dog ears instead of brims on large flat parts
For large models where only corners lift, apply **dog ears** at corners — same adhesion benefit, much easier cleanup than a full brim.

### Tip 28 — Use a deburring tool to remove brims
The easiest brim removal method is a **deburring tool** (Stefan from CNC Kitchen sells one — link in video description).

### Tip 29 — Control ambient temperature
Keep the print room around **20–25°C (68–77°F)**. Temperature swings contribute to adhesion and warping issues.

### Tip 30 — Print a Benchy to isolate the problem
When print quality is off:
- If the **Benchy shows the same issue** → something is wrong with the **printer**
- If the **Benchy prints fine** → something is wrong with your **settings**

Benchy files usually come preloaded on new printers.

### Tip 31 — Diagnose spaghetti failures
Spaghetti (prints in midair) usually means:
1. Part didn't stick to the build plate (full or partial)
2. Missing supports on an overhang
3. Warping lifted a corner → print head knocked the part over

**How to diagnose:**
- Failed at the start → bed adhesion
- Failed at a specific height → check supports at that height
- Random mid-print failure → part got heavy enough to shake loose, or corner lifted and caused a collision

### Tip 32 — Gaps and under-extrusion = clog or too-fast printing
If surfaces look like this or infill didn't fill properly:
- Check print speeds first
- If speeds look fine → **clogged nozzle**
- **Fix:** replace the nozzle (easiest) or do a **cold pull** to clean it

### Tip 33 — Deep calibration is a rabbit hole
For advanced printer/filament/profile calibration beyond basic troubleshooting, see the **Factorian Designs** video linked in the description.

---

## 3D Modeling Software

### Tip 34 — Pick software based on what you want to model

| Goal | Recommended software |
|------|---------------------|
| **Parametric / mechanical / industrial design** | **Fusion** (formerly Fusion 360 — free tier, tons of tutorials), **OnShape**, or SolidWorks if you already know it |
| **Organic / freeform sculpting** | **Blender** (free, steep learning curve) |

Chappel primarily uses SolidWorks (learned in design school 16 years ago) for mechanical work.

---

## Design Philosophy

### Tip 35 — Think beyond the printed part
3D printing can be the **tool**, not just the final product:
- **3D-printed molds** for casting materials like Jesmonite
- **Router templates** for shaping wood handles
- Use printing to achieve results that aren't plastic themselves

---

## Designing for FDM

### Tip 36 — Chamfer the bottom, never fillet it
Fillets on the bottom edge create bad overhangs at the start of the radius. A **chamfer** gives a consistent **45° overhang** that prints cleanly at any scale.

### Tip 37 — Combine chamfer + fillet for smooth edges
Apply a **chamfer first**, then a **fillet** on top — you get a fillet-like shape without the bottom overhang problem because it starts at 45°.

### Tip 38 — Finish edges with micro-fillets and chamfers
Add small **fillets to all edges** and small **chamfers to tops and bottoms**. Subtle but makes parts look and feel much more finished.

**Order matters:** fillets first, then chamfers, for the smoothest transitions.

### Tip 39 — Use wooden dowels for alignment
Model holes sized for **wooden dowels** (IKEA-style) to align large multi-part assemblies. Dowels are cheap, grip well, and are made for this purpose.

### Tip 40 — Print only the section you're iterating
For large designs, print just the **changed section** instead of the whole part — saves time and material during development.

### Tip 41 — Don't design like injection molding
Weight-saving ribs and thin walls that make sense for injection molding often produce **weaker, slower** FDM prints:
- Infill naturally stiffens the interior
- Ribs reduce effective infill and add more slow-printing perimeters
- A **solid blocky design** can be **stronger, faster, and use the same amount of material**

### Tip 42 — Minimize supports through design
- Plan which face sits on the build plate
- Keep overhangs at **45–60° maximum**
- Sometimes **rotate the entire part** to eliminate supports (e.g., stool joints printed on their side instead of upright)

### Tip 43 — Print calibration models for your limits
Don't guess — print test models for:
- **Overhang angles** (how far beyond 45° your printer can go)
- **Bridge spans**
- **Tolerances and hole clearances**

Test in the **actual material** you plan to use.

### Tip 44 — Use teardrop/T-rock holes for precision
Circular holes on vertical walls create bad overhangs on some layers. Replace the problematic arc with **two 60° chamfered flats** forming a **teardrop (T-rock) shape** — precise holes at any size, no supports needed. Especially useful where supports can't be removed easily.

### Tip 45 — Bridge-support embedded nut holes
When embedding a nut in the bottom surface with a through-hole for a bolt, the hole interior prints unsupported and looks terrible. Fix: add **two 0.2 mm thick bridge surfaces** (one in each direction) so the printer bridges first, then prints the hole on top of that foundation.

### Tip 46 — Vertical faces for side-inserted nuts
When inserting a nut into the side of a part, make **two parallel nut faces vertical** so the remaining surfaces don't need supports.

### Tip 47 — Design living hinges and snap mechanisms
Model flexible geometry that prints as one piece with no moving parts:
- Living-hinge clamps
- Snap-lock lids
- Click mechanisms in drawer bottoms

### Tip 48 — Model breakaway supports for tricky geometry
For large thin sections (e.g., a go-kart seat) that struggle to stick, **model your own breakaway supports** in CAD. Snap them off after printing for more consistent results than slicer-generated supports.

---

## Hardware Integration

### Tip 49 — Combine 3D printing with off-the-shelf hardware
Nuts, bolts, and standard fasteners are far easier and stronger than trying to 3D-print complex mechanical joints.

### Tip 50 — Square nut trap when you lack back access
Create a **rectangular pocket** on the side of the part for a **square nut** to slide into — gives you metal threads without needing access from behind.

### Tip 51 — Use design boards for standard hardware dimensions
Download free **design boards** from [alch.shop](https://www.alch.shop/) with exact dimensions for standard hardware (M6 counterbore bolts, etc.) — enter those numbers directly into your CAD software.

### Tip 52 — Back-side nut insertion is the preferred threading method
Inserting a regular nut from the back of the part is Chappel's **favorite** way to add threads.

### Tip 53 — Heat inserts as an alternative
**Heat-set inserts** (heated and pressed into printed holes) work well for many people when you can't expose a nut or lack back access.

---

## Print Orientation & Strength

### Tip 54 — Orient parts for layer strength
FDM parts are **weak between layers** and **strong along layers**. Example: a handle printed flat on the bed (layers running along the handle) is very strong. The same handle printed standing upright (layers perpendicular to stress) snaps easily.

Always orient functional parts so the **layer lines run along the direction of expected force**.

---

## Geometry, Tolerances & Holes

### Tip 55 — Start with ~0.2 mm gap for snug moving fits
For parts that should move freely but fit snugly, leave about **0.2 mm** clearance in the CAD model. This varies by printer, filament, settings, and print orientation.

**General rules:**
- **Side surfaces** need more gap than top/bottom mating surfaces
- Small screw holes in side walls tend to print **slightly undersized** due to overhang effects

### Tip 56 — Use hole calibration boards
Free **hole calibration boards** on [alch.shop](https://www.alch.shop/) — grids of holes in three orientations to find which CAD hole size prints to the real-world dimension you need.

### Tip 57 — Ream holes for precision
Buy inexpensive **reamers**, print holes **~0.5 mm undersized**, then ream to final size for precise fit and smoother hole walls.

### Tip 58 — Print-in-place interlocking assemblies
Design geometry that prints as one piece but creates interlocked moving parts after printing — not just toys. Example: **ball bearings printed in one go** with their cage, eliminating post-assembly.

---

## Text & Labels

### Tip 59 — Add text directly in the slicer
You can add inset or extruded text in the slicer and assign contrasting colors — useful for labels and markings without remodeling.

### Tip 60 — Print the background, not the text (best text quality)
For the **cleanest small text**, don't print the letters — print **everything around them**:

1. Orient the face **down on the build plate**
2. **First layer** = background/contrast color surrounding the text
3. **Second layer** = fill color

The printer's minimum line width limits how thin text strokes can be, but the **gap between two adjacent lines** can be much narrower — creating crisp letterforms.

**Trade-offs:**
| Approach | Pros | Cons |
|----------|------|------|
| **Background method** | Crisper small details, best texture when face-down | More print time on large models |
| **Direct text extrusion** | More durable (more printed surface), faster on large parts | Less crisp on fine details |

Works face-up too (e.g., inverted label option) but looks best face-down.

### Tip 61 — Split models before assigning text colors
When using the background-text technique, **split the model first** in the slicer so small parts keep one color and you only assign the contrasting color to the remaining background piece — saves significant time.

---

## Resources Mentioned

| Resource | Link | Notes |
|----------|------|-------|
| Alexandre Chappel's shop (files, design boards, hole calibration) | [alch.shop](https://www.alch.shop/) | Free design boards; paid project files |
| Label generator (MotorBox labels) | [label.alch.shop](https://label.alch.shop/) | Free; outputs STL/3MF with colors |
| Model repositories | Printables, MakerWorld | Free downloadable models |
| Deburring tool | CNC Kitchen store | Stefan's deburring tool for brim removal |
| Cold pull nozzle cleaning | Link in video description | Nozzle maintenance |
| Deep printer calibration | Factorian Designs (YouTube) | Advanced calibration guide |
| Recommended first printer type | FDM/FFF | Melts plastic filament |

---

## Quick Reference Checklist

**Before every print:**
- [ ] Build plate clean (soap + water, no finger oils)
- [ ] Glue stick applied
- [ ] Correct material profile selected
- [ ] Advanced mode enabled (if using creator-provided settings)

**When something fails:**
- [ ] Check bed adhesion first
- [ ] Print a Benchy to isolate printer vs. settings
- [ ] Check room temperature (20–25°C)
- [ ] For spaghetti: check supports and warping

**When designing:**
- [ ] Chamfer bottoms, not fillet
- [ ] Orient for layer strength
- [ ] Keep overhangs ≤ 45–60°
- [ ] Prefer blocky geometry over injection-molding-style ribs
- [ ] Use teardrop holes for precision side holes
- [ ] Leave ~0.2 mm gap for snug fits
- [ ] Print only the section you're testing

---

*Extracted from the video transcript. Some promotional segments (Squarespace sponsorship, product announcements) were omitted to keep this focused on actionable tips.*
