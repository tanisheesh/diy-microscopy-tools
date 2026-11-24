# Universal Smartphone Microscope Eyepiece Adapter (v2)

A 100% 3D-printable (0% supports), 2-axis adjustable smartphone adapter for compound and stereo **light microscopes**. It securely cradles any smartphone (**58 mm – 95 mm wide**, bare or with thick protective case up to 13.5 mm thick) on bottom anti-drop ledges with self-wedging tapered jaws, and locks the phone's primary camera directly over the microscope's eyepiece (**Ø27.5 mm – Ø30.5 mm**).

---

## Live 3D Interactive Viewer

- **Unified Hub:** https://tanisheesh.github.io/diy-microscopy-tools/#adapter
- **Standalone Page:** https://tanisheesh.github.io/diy-microscopy-tools/microscope-adapter/

---

## Key Features (v2 Engineering Improvements)

1. **Rock-Solid Phone Stability (58 mm – 95 mm Width, 7 – 13.5 mm Thickness):**
   - **Bottom Anti-Drop Ledges:** Symmetric left + right bottom support feet (with center charging-port gap) hold the phone's weight securely even on **45° tilted microscopes**.
   - **Self-Wedging Tapered Jaws:** Full-height side jaws (75–95 mm tall) with vertical lower contact and a gentle ~11° inward upper wedge pull both thin bare phones and thick cased phones flat against the backplate — zero forward flop!
   - **Positive Mechanical Clamp Lock (Thumb Knob #2):** Dedicated M5 locking knob locks the sliding right jaw dead-tight at your phone's exact width, while the closed horizontal rail slot prevents the jaw from ever sliding off the track.

2. **Open-Top Camera Zone + Full 2-Axis Optical Reach:**
   - **Zero Camera Obstruction:** The phone cradle grips the lower-middle body of the phone, leaving the entire upper camera region 100% open (fits triple/quad camera islands, corner iPhone/Samsung lenses, and center Pixel/Xiaomi lenses).
   - **Horizontal Travel:** 46 mm (`X = -26` to `+20 mm`, reaches corner cameras 14 mm from the phone edge).
   - **Vertical Travel:** 50 mm (`111 mm` to `161 mm` above the bottom support ledges — covers compact 130 mm phones up to 170 mm Pro Max / Ultra phones).
   - **100% Open Ø22 mm Optical Through-Tunnel:** Clear, unobstructed light path verified by automated CAD ray-probe checks (`0.000 mm³` blockage) with exact **12.0 mm eye-relief stop** for a full, bright circular field of view.

3. **Flush Recessed Hardware — ZERO Protrusion (Single Bolt Size!):**
   - Uses **3× standard `M5 × 20 mm` hex bolts (DIN 933) + 3× `M5` hex nuts (DIN 934)** across the entire adapter:
     - **Front (Phone Side):** `4.3 mm` deep anti-rotation hex channels keep M5 bolt heads `0.8 mm` **below** the phone resting surface — impossible to scratch or lift the phone.
     - **Back (Knob Side):** Tall `14 mm` recessed-cup `thumb_knob.stl` (print 2×) pulls the M5 nut into a `3.5 mm` solid floor and completely hides the end of the `M5 × 20 mm` bolt inside a `6.3 mm` internal cup.
     - **Eyepiece Collar Ears:** `24 mm` span with `4.0 mm` head counterbore and `5.0 mm` captive hex nut pocket keeps the clamping bolt completely flush.

4. **100% Support-Free 3D Printing:**
   - All 4 STL files are pre-oriented with large flat bed contact areas and **0% floating overhangs**.

---

## Files & Print Quantities

| File | Qty | Print Orientation (Pre-oriented) | Supports | Bed Area |
|---|---|---|---|---|
| `phone_base.stl` | **1×** | Flat rear face on bed | **None (0%)** | 8,691 mm² |
| `clamp_jaw.stl` | **1×** | Outer right cheek flat on bed | **None (0%)** | 1,074 mm² |
| `eyepiece_arm.stl` | **1×** | Flat front face on bed, collar up | **None (0%)** | 2,317 mm² |
| `thumb_knob.stl` | **2×** | Flat clamping floor on bed, cup up | **None (0%)** | 218 mm² |
| `adapter_model.py` | — | Parametric CadQuery 2.8 script with full CAD/STL verification | — | — |
| `params.json` | — | Derived dimensions & transforms for Three.js viewer | — | — |

---

## Recommended Print Settings

- **Material:** PLA or PETG (Matte black PLA is ideal to reduce internal light reflections!)
- **Layer Height:** `0.20 mm` (use `0.16 mm` on `clamp_jaw.stl` for silky dovetail motion)
- **Walls / Perimeters:** `3–4` (≥ 1.2–1.6 mm)
- **Infill:** `25%` Gyroid
- **Supports:** **OFF (0%)** for all 4 parts
- **Brim:** Not needed (optional 3 mm brim on `thumb_knob.stl`)

---

## Assembly (3 × `M5 × 20 mm` Hex Bolts + 3 × `M5` Hex Nuts)

1. **Press M5 Nuts into Both Thumb Knobs:**
   - Push one M5 hex nut firmly into the internal hexagonal pocket of each `thumb_knob.stl` (2×).
2. **Assemble the Sliding Phone Clamp:**
   - Slide `clamp_jaw`'s dovetail tongue into the right end of `phone_base`'s horizontal track.
   - Drop **Bolt #1 (`M5 × 20 mm`)** into the recessed hex pocket on the lower-right jaw wall (through the lower base rail slot).
   - Thread **Thumb Knob #1** onto the back of Bolt #1 — the jaw is now permanently captive and locks dead-tight at any width from 58 to 95 mm!
3. **Attach the Eyepiece Arm:**
   - Drop **Bolt #2 (`M5 × 20 mm`)** into the upper horizontal hex channel on the front of `phone_base` (the hex head sits flush below the phone surface and won't spin!).
   - Place `eyepiece_arm` flat against the back of `phone_base` so Bolt #2 passes through the arm's vertical slot.
   - Thread **Thumb Knob #2** onto the back of Bolt #2.
4. **Install Eyepiece Collar Clamp Bolt:**
   - Insert **Bolt #3 (`M5 × 20 mm`)** into the recessed counterbore on the left clamping ear and press the 3rd **M5 hex nut** into the right ear pocket.

---

## How to Use on a Light Microscope

1. Slip the split collar (`eyepiece_arm`) straight over your light microscope's eyepiece barrel (`Ø27.5–30.5 mm`) until it rests against the internal 12 mm stop ring, and snug Bolt #3.
2. Loosen **Clamp Knob #1**, place your smartphone flat onto the bottom anti-drop ledges against the left jaw, push the right sliding jaw snug against your phone, and tighten **Clamp Knob #1**.
3. Open your phone's **1× Main Camera**, loosen **Optical Knob #2** half a turn, slide the holder in X and Y until the bright circular microscope field of view is dead-center on your screen, and tighten **Optical Knob #2**.
4. Focus with the microscope's fine focus knob and capture sharp photos/videos!

---

## Regenerating the Model

```powershell
cd C:\Users\Tanish-Poddar\Downloads\smear-spreader\microscope-adapter
py -3.14 adapter_model.py
```

The script automatically verifies all wall thicknesses (`≥ 1.6 mm`), flush `M5 × 20 mm` bolt engagement, zero interference across all phone widths (thin & thick) and 2-axis optical travel, captive dovetail lock, `0.000 mm³` optical tunnel blockage, and watertight STL mesh integrity before writing output files.
