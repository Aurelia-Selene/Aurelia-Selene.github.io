# Rig Case Layouts — Rulebook

How component placements are stored and how to add new ones.
The single source of truth for the encoding is this file plus `seed_to_layouts.py`.

**File map (keep all in the same folder):**
- `rigs-data.js` — the **data**: `const D=[…]` (every rig) + `const LAYOUTS={…}` (all placements). Edit layouts **here**.
- `index.html` — the app; loads `rigs-data.js` via `<script src>` and `images/` via relative paths.
- `seed_to_layouts.py` — seed/JSON → `LAYOUTS` converter.

## 1. The grid

- Every case is a **5×5 board**: 5 columns (`x`, left→right, 0–4) × 5 rows (`y`, top→bottom, 0–4).
- Reading order is **row-major**: index `i → row = i//5, col = i%5`.
- A **PSU occupies 2 adjacent cells**; everything else is 1×1.

## 2. Seed format (from slw.io/rig)

- **25 chars per case × N cases**, then a **1–2 char tail** encoding rig state (not placement):
  - optional `C` = CMT2570 education on, then a digit **0–5** = OC level (digit × 10%).
  - `C3` = CMT2570 + 30% OC · `3` = no education + 30% OC · `0` = base, no OC.
- Char → component (grid ID):

| Char | Component    | ID |
|------|--------------|----|
| `e`  | eCPU         | 1  |
| `c`  | CPU          | 2  |
| `h`  | HPCU         | 3  |
| `f`  | Fan          | 4  |
| `w`  | Water Block  | 5  |
| `s`  | Heat Sink    | 6  |
| `b`  | Empty        | 0  |
| `p`  | PSU half-left   | 7 |
| `P`  | PSU half-right  | 7 |
| `v`  | PSU vert-top    | 7 |
| `V`  | PSU vert-bottom | 7 |

- PSU pairing: `p`+`P` = **horizontal** (left/right), `v`+`V` = **vertical** (top/bottom).
- The **anchor** is the `p` cell (horizontal) or the `v` cell (vertical) — the partner `P`/`V` is the second cell.
- **PSU count = (number of `p/P/v/V` cells) ÷ 2.**

## 3. JSON format (export)

`{"rig-case.N": [ {x, y, item, [x2, y2]}, ... ]}`
- `x,y` = position (0-indexed), `item` = component ID (0–7).
- PSU: `{x,y,item:7,x2,y2}` — `x2,y2` is the second cell (horizontal if same row, vertical if same column).

## 4. Simulator LAYOUTS format (stored format)

```js
LAYOUTS["<tier>|<cases>|<MIPS>"] = [ case0, case1, ... ];
// each case:
//   [ {t:type, r:row, c:col}, ... {t:"PSU", r:anchorRow, c:anchorCol, o:"h"|"v"}, ... ]
```
- `t` = component name (`"eCPU"`, `"CPU"`, `"HPCU"`, `"Fan"`, `"Water Block"`, `"Heat Sink"`, `"PSU"`).
- `r` = row 0–4, `c` = col 0–4 (top-left origin).
- PSU only: `o:"h"` = 2 across (anchor = left cell), `o:"v"` = 2 down (anchor = top cell).
- Unfilled slots render as empty cells automatically — you only list placed parts.

## 5. Adding a rig (workflow)

1. Get the **seed** (or JSON) for the rig.
2. Convert it:
   ```
   python seed_to_layouts.py --seed "<seed>" --cases <N> --grid          # preview
   python seed_to_layouts.py --seed "<seed>" --cases <N> --key "<tier>|<N>|<MIPS>"
   python seed_to_layouts.py --json <file.json> --key "<tier>|<N>|<MIPS>"
   ```
3. Add the printed entry to `LAYOUTS` in **`rigs-data.js`** (not the HTML).
4. Refresh the HTML — the rig's case(s) now render the real component images.

## 6. Worked example — NO Educations · 550,000 MIPS

Seed (case 1): `hceehewewcpPcpPcweweheech`

```
 HPCU  CPU   eCPU  eCPU  HPCU
 eCPU  Water eCPU  Water CPU
 [PSU] [PSU] CPU   [PSU] [PSU]      <- 2 horizontal PSUs (cols 0-1 and 3-4)
 CPU   Water eCPU  Water eCPU
 HPCU  eCPU  eCPU  CPU   HPCU
```
Counts: eCPU 8 · CPU 5 · HPCU 4 · Water Block 4 · PSU 2 (23 parts, full grid).

## 7. MIPS per component

OC step `s` = 0–5 (one step = 10%): `30% OC` → s=3, `50% OC` → s=5.

| Component | base (s=0) | per step |
|-----------|------------|----------|
| eCPU      | 25,000     | +1,250   |
| CPU       | 30,000     | +2,250   |
| HPCU      | 50,000     | +5,000   |
| Fan / Water Block / Heat Sink / PSU | 0 | — |

Rig MIPS = sum over the compute parts.

## 8. Power

| Component | base (s=0) | per step |
|-----------|------------|----------|
| eCPU      | 30 W       | +3 W     |
| CPU       | 70 W       | +7 W     |
| HPCU      | 150 W      | +15 W    |
| Fan       | 5 W        | —        |
| Water Block / Heat Sink | 0 W | — |
| PSU       | 750 W each (budget) | — |

- Rig draw = sum over parts; budget = PSUs × 750 W.
- **Over budget → MIPS throttle.** The simulator does not reject the rig: MIPS scales by `budget ÷ draw`, shown rounded to the nearest 10.
  - Example: 1 eCPU + 35 HPCU at 0% OC = 5,280 W draw vs 7 × 750 W = 5,250 W budget → 1,775,000 × 5250/5280 = **1,764,910 MIPS**.
- So a MIPS value that is not a multiple of 5,000 is a throttled rig, not a data error.
