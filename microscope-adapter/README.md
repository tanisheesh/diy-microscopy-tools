# Universal Smartphone Microscope Eyepiece Adapter (v3 — Dual-Side Adjustable)

A 100% 3D-printable (0% supports), **symmetrical dual-side adjustable** smartphone adapter for compound and stereo **light microscopes**. Both the left and right jaws slide and lock independently on a centered rail so any smartphone (**56 mm – 100 mm wide**, bare or thick cased up to 13.5 mm thick) stays perfectly balanced over the microscope eyepiece (**Ø27.5 mm – Ø30.5 mm**).

---

## Live 3D Interactive Viewer

- **Unified Hub:** https://tanisheesh.github.io/diy-microscopy-tools/#adapter
- **Standalone Page:** https://tanisheesh.github.io/diy-microscopy-tools/microscope-adapter/

---

## Key Features (v3 Dual-Side Adjustable)

1. **Symmetrical Dual-Side Phone Clamp (56 mm – 100 mm Width, 7 – 13.5 mm Thickness):**
   - **Both Left & Right Jaws Adjust Independently:** Centers any smartphone symmetrically over the microscope eyepiece for ideal weight balance (zero sideways twisting on 45° microscopes!), OR shifts the phone left/right to help align edge cameras.
   - **Twin Bottom Anti-Drop Ledges:** Both left and right jaws carry sturdy bottom support feet (leaving a 24+ mm center USB-C gap) so the phone can never slide downward on tilted microscopes.
   - **Self-Wedging Tapered Side Jaws:** Full-height (`79.5 mm`) mirror-twin jaws with vertical lower walls and a gentle ~11° inward upper wedge pull both thin bare phones and thick cased phones flat against the backplate — zero forward wobble.
   - **Positive Dual Mechanical Locks:** Dedicated left + right flush M5 locking thumb knobs lock both jaws rock-solid inside closed rail slots (jaws can never fall off the track).

2. **Open-Top Camera Zone + Centered 2-Axis Optical Reach:**
   - **Zero Camera Obstruction:** Cradle holds the lower-middle body of the phone, leaving the entire upper camera region 100% open.
   - **Symmetric Horizontal Travel:** 56 mm (`-28` to `+28 mm`) reaches left-corner, center, and right-corner cameras effortlessly.
   - **Vertical Travel:** 50 mm (`111 mm` to `161 mm` above the bottom ledges — covers compact 130 mm phones up to 170 mm Pro Max / Ultra phones).
   - **100% Open Ø22 mm Optical Through-Tunnel:** Clear, unobstructed light path verified by automated CAD ray-probe checks (`0.000 mm³` blockage) with exact **12.0 mm eye-relief stop**.

3. **Flush Recessed Hardware — ZERO Protrusion (Single Bolt Size!):**
   - Uses **4× standard `M5 × 20 mm` hex bolts (DIN 933) + 4× `M5` hex nuts (DIN 934)** across the entire adapter:
     - **Phone side:** `4.3 mm` deep anti-rotation hex channel keeps the optical M5 bolt head `0.8 mm` **below** the phone surface.
     - **Both sliding jaws:** Rotated flush M5 hex pockets with `2.3 mm` solid walls on both sides keep the clamp bolt heads recessed outside the phone envelope.
     - **Back side (3× Knobs):** Tall `14 mm` recessed-cup `thumb_knob.stl` completely hides the tip of every `M5 × 20 mm` bolt inside a `6.3 mm` internal cup.
     - **Eyepiece collar ears:** `24 mm` span with recessed head counterbore and captive hex nut pocket sits 100% flush.

4. **100% Support-Free 3D Printing:**
   - All 5 STL files are pre-oriented with flat bed planes and **0% floating overhangs**.

---

## Files & Print Quantities

| File | Qty | Print Orientation (Pre-oriented) | Supports | Bed Area |
|---|---|---|---|---|
| `phone_base.stl` | **1×** | Flat rear face on bed (`6.8 mm` flat plate) | **None (0%)** | 9,602 mm² |
| `clamp_jaw_left.stl` | **1×** | Outer left cheek flat on bed | **None (0%)** | 1,074 mm² |
| `clamp_jaw_right.stl` | **1×** | Outer right cheek flat on bed | **None (0%)** | 1,074 mm² |
| `eyepiece_arm.stl` | **1×** | Flat front face on bed, collar up | **None (0%)** | 2,317 mm² |
| `thumb_knob.stl` | **3×** | Flat clamping floor on bed, cup up | **None (0%)** | 218 mm² |
| `adapter_model.py` | — | Parametric CadQuery 2.8 script with full CAD/STL checks | — | — |
| `params.json` | — | Derived dimensions & transforms for Three.js viewer | — | — |

---

## Recommended Print Settings

- **Material:** PLA or PETG (Matte black PLA minimizes stray optical reflections)
- **Layer Height:** `0.20 mm` (`0.16 mm` recommended on both sliding jaws for smooth dovetail glide)
- **Walls / Perimeters:** `3–4` (≥ 1.2–1.6 mm)
- **Infill:** `25%` Gyroid
- **Supports:** **OFF (0%)** for every part

---

## Assembly (4 × `M5 × 20 mm` Hex Bolts + 4 × `M5` Hex Nuts)

1. **Press M5 Nuts into All 3 Thumb Knobs:**
   - Seat one M5 hex nut firmly inside each of the 3 printed `thumb_knob.stl` pieces.
2. **Assemble Left & Right Sliding Jaws:**
   - Slide `clamp_jaw_left` into the left end and `clamp_jaw_right` into the right end of `phone_base`'s dovetail track.
   - Drop **Bolt #1 & Bolt #2 (`M5 × 20 mm`)** into the recessed hex pockets on the lower jaw walls and thread **Thumb Knobs #1 & #2** onto the rear. Both jaws are now captive and lock rock-solid at any width from 56 to 100 mm!
3. **Attach the Eyepiece Arm:**
   - Drop **Bolt #3 (`M5 × 20 mm`)** into the upper horizontal hex channel on the front of `phone_base` (sits flush below phone surface).
   - Place `eyepiece_arm` against the back of `phone_base` over Bolt #3 and thread **Thumb Knob #3** onto the rear.
4. **Install Eyepiece Collar Clamp Bolt:**
   - Insert **Bolt #4 (`M5 × 20 mm`)** into the left ear counterbore and seat the 4th **M5 hex nut** in the right ear hex pocket.

---

## Regenerating the Model

```powershell
cd C:\Users\Tanish-Poddar\Downloads\smear-spreader\microscope-adapter
py -3.14 adapter_model.py
```
