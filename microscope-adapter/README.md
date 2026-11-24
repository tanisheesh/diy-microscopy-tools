# Universal Smartphone Microscope Eyepiece Adapter (v4 — 1-Screw Smooth Dual-Slider + Flex Collet)

A lightweight, 100% support-free 3D-printable smartphone adapter for **light microscopes** (compound, monocular, binocular, stereo). Designed for effortless, buttery-smooth operation with **ONLY ONE metal screw** across the entire assembly:

- **0 screws on the eyepiece:** Screwless **6-petal flexible friction-fit collet** slips safely over Ø28–30.5 mm microscope eyepieces — zero risk of cracking the eyepiece or PLA!
- **0 screws on the phone clamp:** Normal **symmetrical dual-side smooth sliders** (`56 – 100 mm`) auto-centered by 1–2 regular rubber bands!
- **Only 1 flush `M5 × 20 mm` bolt + nut:** Locks X-Y camera center rock-solid once — bolt head sits `1.0 mm` below the phone surface and bolt tip hides completely inside the tall recessed thumb knob!

---

## Live 3D Interactive Viewer

- **Unified Hub:** https://tanisheesh.github.io/diy-microscopy-tools/#adapter
- **Standalone Page:** https://tanisheesh.github.io/diy-microscopy-tools/microscope-adapter/

---

## Key Engineering Features (v4)

1. **Buttery-Smooth Sliding Execution:**
   - **5.8 mm wide chamfered M5 slots** (`+0.8 mm` clearance over M5 threads -> steel threads NEVER bite or jam into plastic!).
   - **8.6 mm × 4.5 mm straight flat anti-rotation hex channel** (`+0.6 mm` side glide clearance, `1.0 mm` recessed below phone -> bolt glides smoothly along X without spinning or wedging!).
   - **0.30 mm dovetail slider clearance** + long `31 mm` guide tongues -> zero drawer-binding, silky smooth rubber-band gliding!
   - **5.8 mm knob floor bore + 8.5 mm square nut pocket** -> knob spins effortlessly on the metal nut with zero plastic drag!

2. **Self-Centering Dual-Side Phone Clamp (56 – 100 mm Width, 7 – 13.5 mm Thickness):**
   - Left + right mirror-twin sliders move smoothly on a compact centered rail.
   - **Rear Mushroom T-Hooks:** Stretch 1–2 standard rubber bands straight between left & right rear hooks — equal tension automatically centers your phone over the eyepiece for perfect weight balance!
   - **Twin Bottom Anti-Drop Ledges + Self-Wedging Tapered Jaws:** Phone sits solidly on bottom support ledges with a 24+ mm center USB-C gap and never slips or tips forward on 45° tilted microscopes.
   - **Filament End-Stop Pins:** Push two 10 mm pieces of `1.75 mm` filament into the outer rail holes (`±62.5 mm`) so jaws can never slide off the track.

3. **Screwless 6-Petal Flexible Eyepiece Collet + 100% Open Optical Tunnel:**
   - 6 symmetric springy fingers with smooth `45°` lead-in funnel, gentle `0.7 mm` internal friction ribs, round stress-relief holes at each root, and an external optional rubber-band groove for extra grip on slim `27.5 mm` eyepieces.
   - **100% Open Ø22 mm Optical Through-Tunnel:** Verified by automated CAD ray-probe (`0.000 mm³` blockage) with exact **12.0 mm eye-relief stop**.
   - **Open-Top Camera Zone + Full 2-Axis Travel:** `56 mm` horizontal (`-28` to `+28 mm`) × `50 mm` vertical (`112 – 162 mm` above phone bottom).

---

## Files & Print Quantities (All 0% Supports!)

| File | Qty | Size (Print Orient.) | Supports | Bed Contact |
|---|---|---|---|---|
| `phone_base.stl` | **1×** | `130.0 × 77.0 × 7.0 mm` | **None (0%)** | 7,180 mm² |
| `clamp_jaw_left.stl` | **1×** | `28.2 × 81.5 × 31.0 mm` | **None (0%)** | 1,387 mm² |
| `clamp_jaw_right.stl` | **1×** | `28.2 × 81.5 × 31.0 mm` | **None (0%)** | 1,387 mm² |
| `eyepiece_arm.stl` | **1×** | `35.0 × 108.2 × 27.0 mm` | **None (0%)** | 1,994 mm² |
| `thumb_knob.stl` | **1×** | `23.3 × 24.0 × 14.5 mm` | **None (0%)** | 218 mm² |

---

## Hardware Needed (Minimal & Ultra-Light!)

- **1× `M5 × 20 mm` Hex Bolt (DIN 933) + 1× `M5` Hex Nut (DIN 934)** *(ONLY for the single optical X-Y lock!)*
- **1–2× Standard Stationery Rubber Bands** *(double-looped between the left & right rear T-hooks)*
- **2× `10 mm` pieces of `1.75 mm` 3D-printer filament** *(optional end-stop pins in outer rail holes)*

---

## Recommended Print Settings

- **Material:** PLA or PETG (Matte black PLA is best to prevent internal glare)
- **Layer Height:** `0.20 mm` (`0.16 mm` recommended on both sliding jaws for silky dovetail glide)
- **Walls / Perimeters:** `3` (`1.2 mm` — gives ideal elastic flex on the 6 collet petals!)
- **Infill:** `20–25%` Gyroid
- **Supports:** **OFF (0%)** for every part

---

## Quick 30-Second Assembly

1. Slide `clamp_jaw_left` into the left end and `clamp_jaw_right` into the right end of `phone_base`'s dovetail track.
2. *(Optional)* Push two short `10 mm` pieces of `1.75 mm` filament into the outer rail holes (`±62.5 mm`) as end stops.
3. Loop 1–2 rubber bands across the **Left & Right Rear Mushroom T-Hooks** underneath the base plate.
4. Drop the single **`M5 × 20 mm` bolt** into the recessed hex channel on the front of `phone_base`, place `eyepiece_arm` flat on the back over the bolt, press the **M5 hex nut** into `thumb_knob`, and thread the knob onto the bolt.
5. Slip the 6-petal flex collet gently onto your light microscope's eyepiece, pull both jaws open to snap your phone onto the bottom ledges, slide X/Y until the bright microscope circle is dead-center on screen, and snug the single knob!

---

## Regenerating the Model

```powershell
cd C:\Users\Tanish-Poddar\Downloads\smear-spreader\microscope-adapter
py -3.14 adapter_model.py
```
