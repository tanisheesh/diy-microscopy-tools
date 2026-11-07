# Universal Smartphone Microscope Eyepiece Adapter

A 3D-printable, 2-axis adjustable smartphone adapter for compound and stereo microscopes. It clamps any standard smartphone (60 mm to 92 mm wide) and locks the phone's primary camera directly over the microscope's eyepiece (ocular lens) for sharp microphotography, video recording, and live group viewing.

Inspired by laboratory microscope phone mounts (e.g. Sajid Shaikh's adapter design).

---

## 3D Interactive Viewer

Open `index.html` in a web browser via local HTTP server to interactively test phone clamping width, 2-axis camera alignment, and exploded assembly views.

```powershell
cd C:\Users\Tanish-Poddar\Downloads\smear-spreader\microscope-adapter
python -m http.server 8000
```
Then open **http://localhost:8000** in your browser.

---

## Key Features

1. **Universal Phone Clamp (60 mm – 92 mm):**
   - Captive dovetail-T slider accommodates compact phones (e.g. iPhone mini/SE) up to large smartphones with thick protective cases.
   - Inward retention lips (45° chamfered) securely hold the phone without scratching.
   - Integrated **D-ring finger pull handle** for quick one-handed phone insertion.
   - Rear elastic band eyelets for instant spring-tensioned auto-clamping.

2. **2-Axis Cross-Slotted Optical Alignment (X: ±16 mm, Y: ±21 mm):**
   - Horizontal slot in the base plate crosses with the vertical slot in the eyepiece arm.
   - Tightening a single M5 thumb knob from the rear locks both X and Y alignment simultaneously.
   - Fits all camera configurations: corner multi-lens clusters (iPhone/Samsung S-series) or center cameras (Google Pixel, Xiaomi, OnePlus).

3. **Standard Microscope Eyepiece Collar (Ø30 mm ID with Split Clamp):**
   - Outer diameter fits over standard lab compound microscope eyepieces (Ø28.0 mm to Ø30.5 mm).
   - Built-in **Ø21 mm eye-relief aperture stop** keeps the eyepiece glass at the optimal focal distance (~12 mm from phone camera sensor) and prevents metal-to-lens scratching.
   - Split-collar flex ears with captive M4 nut pocket for tightening clamp screw.

4. **100% 3D Printable (Zero Supports Needed):**
   - All 4 parts are pre-oriented with 45° overhangs and flat bed planes.
   - Compatible with 100% printed thumb knobs or standard M5 bolt + wingnut hardware.

---

## Files

| File | Description |
|---|---|
| `adapter_model.py` | Parametric CadQuery 2.8 CAD script with automated printability checks |
| `phone_base.stl` | Main phone cradle backplate with fixed left jaw, X-slot, and camera window |
| `clamp_jaw.stl` | Sliding right jaw with dovetail-T tongue and D-ring pull handle |
| `eyepiece_arm.stl` | Vertical slotted bracket with stepped Ø30 mm eyepiece collar |
| `thumb_knob.stl` | Ergonomic 6-flute knurled M5 thumb knob with captive hex nut socket |
| `params.json` | Derived dimensions and transforms for the web viewer |
| `index.html` | Interactive Three.js 3D viewer with animations & downloads |

---

## Regenerating the Model

Run the CadQuery script using 64-bit Python 3.14:

```powershell
cd C:\Users\Tanish-Poddar\Downloads\smear-spreader\microscope-adapter
py -3.14 adapter_model.py
```

### Pre-flight & Post-export Automated Checks:
- **Wall Thickness:** All structural walls ≥ 1.6 mm.
- **Printable Clearances:** Sliding dovetail-T clearance = 0.25 mm.
- **Watertight Manifold Check:** 0 non-manifold edges across all exported STLs.
- **Normal Verification:** Outward facing normals (positive volume).
- **Bed Contact Area:** Large flat base (> 250 mm² on bed) for 100% reliable adhesion.

---

## Recommended Print Settings

| Setting | `phone_base` | `clamp_jaw` | `eyepiece_arm` | `thumb_knob` |
|---|---|---|---|---|
| Material | PLA or PETG | PLA or PETG | PLA or PETG | PLA or PETG |
| Layer Height | 0.20 mm | 0.16–0.20 mm | 0.20 mm | 0.20 mm |
| Perimeters / Walls | 3–4 (1.2–1.6 mm) | 3–4 | 4 (strength for collar) | 3 |
| Infill | 20–25% Gyroid | 25% Gyroid | 30% Gyroid | 30% Gyroid |
| Supports | **None (0%)** | **None (0%)** | **None (0%)** | **None (0%)** |
| Print Orientation | Flat back on bed | Flat back on bed | Flat front arm on bed | Flat base on bed |

---

## Hardware & Assembly

### Option A: Standard Hardware (Recommended)
- **1× M5 × 20 mm or 25 mm Bolt:** Insert from the front of `phone_base` through the horizontal slot. (Bolt head sits flush in front recess so phone rests flat).
- **1× M5 Hex Nut:** Press into `thumb_knob.stl`.
- **1× M4 × 20 mm Bolt & Nut:** For clamping the eyepiece collar onto the microscope.
- **1× Standard Rubber Band:** (Optional) Loop between the base eyelet and jaw eyelet for automatic spring tension.

### Option B: 100% 3D-Printed Assembly
- Use `thumb_knob.stl` as a captive thumb nut directly with printed M5 studs or pins.

---

## How to Use

1. **Mount on Microscope:** Slide the cylindrical collar of `eyepiece_arm` over the microscope's eyepiece and lightly tighten the M4 clamp screw.
2. **Insert Phone:** Pull the sliding jaw outward using the D-ring handle and snap your smartphone into the cradle.
3. **Align Camera:**
   - Open your phone's Camera app.
   - Loosen the rear M5 thumb knob.
   - Slide the phone holder in X and Y until the circular microscope field of view is centered on the phone screen.
   - Tighten the M5 thumb knob to lock alignment.
4. **Focus & Capture:** Use the microscope's fine focus knob to achieve a crisp view on the screen, pinch-to-zoom slightly to fill the screen, and take photos or record videos!
