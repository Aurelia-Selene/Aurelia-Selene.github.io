# Changelog

## [1.7.0] — 2026-10-16
### Added
- **12 rig layouts** for the Only Heat Reduction tier (590k–2.65m MIPS, 1–3 cases). All validated against D-data component counts.

## [1.6.2] — 2026-10-16
### Changed
- **Footer author** name contrast improved: bolder weight, brighter color, stronger glow.

## [1.6.1] — 2026-10-16
### Changed
- **Footer author** name now has a subtle green glow for readability.

## [1.6.0] — 2026-10-16
### Changed
- **Colored tier tabs**: Each tab button now uses its tier's accent color (red, amber, cyan, green) on hover and active states.
- **Tab labels** updated for clarity: "Heat Reduction" → "Only Heat Reduction", "30% OC" → "30% Overclock", "50% OC" → "50% Overclock".
- **Tier badges** on rig cards now match tab labels exactly.

## [1.5.0] — 2026-10-16
### Added
- **Tier tabs**: Tier selector is now 4 tab buttons (No Educations, Heat Reduction, 30% OC, 50% OC) that filter the rig list.
### Changed
- **Centered** the search bar, tier tabs, and sort bar.
- **Default sort** is now MIPS ascending (was: original order).
- **Removed** "Tier" and "Original" from sort options (tier is now the tab filter).
- Search placeholder simplified to "Search MIPS, component...".

## [1.4.0] — 2026-10-16

### Added
- **18 new layout entries** — case-by-case component placements for rigs from 555,000 MIPS through 2,650,000 MIPS (NO Educations tier, 1–3 cases). All entries validated against their D-data component counts (PSU, HPCU, eCPU, CPU, WaterBlock).

### Fixed
- **730k / 750k WaterBlock data** — D-row field 11 corrected from `0` → `4` to match the 4 WaterBlock objects actually placed in those layouts.
- **Vertical PSU rendering** — the rotated PSU image now fills its 1×2 cell (`width:200%;height:100%` before rotation).

## [1.3.0] — 2026-10-16

### Added
- **External data file** — all rig data now lives in `rigs-data.js` (single source of truth): `const D=[…]` (every rig definition) + `const LAYOUTS={…}` (all case placements). Adding a new rig's layout now means editing just this one file.

### Changed
- **HTML is now a thin app shell** — it loads the data via `<script src="rigs-data.js"></script>` instead of embedding the ~96 rig rows inline. The app still opens by double-click (data file sits in the same folder).

## [1.2.0] — 2026-10-16

### Added
- **In-rig component placement** — rig case grids can now show the actual component images placed exactly where they sit in-game, instead of empty slots. Component art is pulled from the new `images/` folder (`eCPU`, `CPU`, `HPCPU`, `Computer_Fan`, `Water-Block`, `Heat-Sink`, `PSU`).
- **PSU is 2-wide** — the PSU spans two slots and can be placed **horizontally** (2 across, `o:"h"`) or **vertically** (2 down, `o:"v"`, image auto-rotated). Every other component is a single 1×1 slot.
- **Per-rig layout data** — a `LAYOUTS` map keyed by `tier|cases|MIPS`. Each case is a list of placed parts `{t:type, r:row, c:col, o:orientation}` (row 0 = top, col 0 = left); empty slots are auto-filled. Rigs with no entry yet still render as empty grids.
- **Hover tooltip** — hovering a placed component shows its name.
- **Seed / JSON → layout tooling** — `seed_to_layouts.py` converts an in-game **seed** or **JSON export** into the `LAYOUTS` snippet (handles multi-case rigs, PSU pairing, and a `--grid` preview). `LAYOUTS.md` is the permanent rulebook documenting the seed char map, JSON schema, PSU pairing, and the stored `LAYOUTS` format.
- First example laid out: **NO EDUCATIONS · 550,000 MIPS** (8 eCPU, 5 CPU, 4 HPCU, 4 Water Block, 2 PSU = full 5×5), **verified against the in-game seed** `hceehewewcpPcpPcweweheech`.

### Changed
- **Case grid geometry** — the 5×5 board is now a true square (`aspect-ratio:1` + `repeat(5,1fr)` rows) so 2-wide/2-tall components and the slot cells all stay geometrically consistent.

### Fixed
- **Case slots are square again** — cells use `aspect-ratio:1` (true square, as in-game) instead of stretching to fill the column. The **case** now scales with a relative `clamp(9.5rem,15vw,12.5rem)` width, so slots stay square while the whole case still scales with the viewport. Columns are vertically centered (`align-items:center`) rather than stretched, removing the earlier fill-rectangles trade-off.

## [1.1.3] — 2026-10-16

### Changed
- **Rig panel now scales fluidly** — case grids use `repeat(5,1fr)` for both axes and fill their column (no more dead space around the cases when the reference panel is open). Cases and stats split the width via relative `flex-grow` instead of fixed pixels.
- **Relative units** — converted the sim card's fixed `px` sizes (padding, gaps, font sizes, `min-width`, stat-card `minmax`) to `rem` / `fr`, so the layout scales with the container and browser zoom. Only `1px` borders and the shadow spread remain in `px` (physical/effect values).

## [1.1.2] — 2026-10-16

### Changed
- **Rig panel layout** — restructured the simulator card into a two-column layout: **case grids on the left**, **stats + component counts on the right** (now big stat cards in an auto-fitting grid), filling the previously empty space. Larger cells, chips, and stat values for readability.

## [1.1.1] — 2026-10-16

### Changed
- **Cleaner reference panel** — dropped the per-line source tags (e.g. "community", "wiki") so the data reads as-is.

## [1.1.0] — 2026-10-16

### Added
- **Targets reference (official wiki)** — all **28** Cracking targets: 13 unencrypted + 15 encrypted, each with unlock skill, encryption layers, and reward range.
- **New mechanics** — ICE encryption, 4–10 char passwords, 1–9 encryption layers, brute-forcing (7 nerve) vs final cracking (5 nerve), 3-guess lockout, jail time on critical failure (3h16m–6h23m), 7–26 jobs/day at midnight TCT.
- **CMT1520** (required course) added to the education list.

### Changed
- **Wider reference sidebar** (370px → 480px) via a `--panel-w` token, shared by the panel, the open-state layout gap, and the footer.

### Fixed (reconciled to the official wiki)
- Rig online threshold: **≥100,000 MIPS + 1 PSU** (was 150,000 MIPS / 1500W budget).
- **CPU heat = High** (was "Low"); **Computer Fan = 5W** (was 50W).
- **OC unlocks** — CMT2128 → 30%, CMT2129 → 50% (was CMT2570→30 / CMT2128→50 / CMT2129→100). CMT2570 is the **−25% heat** course, not an OC unlock.
- **Chassis** unlock at skill **25 / 50 / 75** (was "every 2 levels").
- Passwords are **4–10 chars** (was "25-char"); encryption layers **1–9** (was "1–5").

## [1.0.3] — 2026-10-16

### Added
- **Sticky footer** — the status bar now pins to the bottom of the viewport (like a terminal status line) and stays visible while you scroll; it steps aside when the reference panel is open.

## [1.0.2] — 2026-10-16

### Added
- **Themed scrollbars** — thin green-phosphor track & thumb (WebKit + Firefox) to match the terminal aesthetic.

### Changed
- **Cracking Reference panel** — long content now word-wraps; the horizontal scrollbar is gone.
- **Layout** — the database keeps a consistent right-hand gap when the reference panel is open (matches the collapsed-state padding) instead of crowding the panel edge.

### Fixed
- **Per-case board** — now renders as **5×5** to match in-game (earlier builds drew 6×6).

## [1.0.1] — 2026-10-16

### Fixed
- **Empty database on load + dead Cracking Info button.** Info-panel wiring deferred to `DOMContentLoaded` (guarded by a `document.readyState` check); the 96 rigs render on load and the panel opens/closes.

## [1.0.0] — 2026-10-16

_First tracked release._

### Added
- Collapsible rig panels (accordion) for all **96** rigs, with tier badges and key stats in the header.
- Simulator-style detail card per rig: MIPS, BFS, component counts, rig power (PSU × 750 W), heat gain, uses, component chips, and N empty **6×6** case grids.
- Search box, multi-field sort (Tier / Cases / MIPS / BFS / Heat / Uses, asc/desc), and Expand/Collapse All.
- Retro **terminal** theme (green phosphor / VFD): scanlines, CRT vignette, monospace type, glow, blinking title cursor, ONLINE footer.
- Tier accent colors: 50% OC (green) · 30% OC (cyan) · NO OC (amber) · NO Educations (red).
- Expandable right-side **Cracking Reference** panel summarizing the community guide — core mechanics, components, BFS formula + thresholds, heat & overheating, cooling, overclocking, rig classifications, design patterns, skill-growth paths, honors & merits, enhancers & tools, education, and key formulas.

### Notes
- BFS formula follows the guide: `BFS = 0.0052 × √MIPS − 0.6252` (approximate, ±3%).
- Rig power = PSU count × 750 W.

---
*Author: Frieza [4025189]*
