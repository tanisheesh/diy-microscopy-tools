# DIY Microscopy Tools

A collection of 100% 3D-printable, open-hardware precision laboratory tools designed in parametric CadQuery.

**Live 3D Interactive Web Viewer:** https://tanisheesh.github.io/diy-microscopy-tools/

---

## Included Tools

### 1. 🔬 Blood Smear Slide Spreader
A captive 3D-printable jig for making consistent, reproducible blood smears. The base slide (75 × 25 × 1 mm) sits in a recessed bed. A captive carriage runs along rails and holds a glass spreader slide at **45°**. Push the carriage forward and it makes the smear.

- **Captive Fit:** Dovetail-T tongues trapped in undercut grooves (cannot lift off).
- **End Stops:** Closed front end stop + removable rear 1.75 mm filament stop pins.
- **Smear Travel:** ~48 mm smooth stroke.
- **Folder:** `smear-spreader/`
- **Files:** `spreader_model.py`, `base.stl`, `carriage.stl`, `params.json`.

---

### 2. 📱 Smartphone Microscope Eyepiece Adapter (v4 — 1-Screw Smooth Dual-Slider + Flex Collet)
A lightweight, buttery-smooth smartphone adapter for light microscopes (compound, monocular, binocular, stereo) requiring **only 1 metal screw** (`1× M5 × 20 mm` bolt + nut):

- **Screwless 6-Petal Flex Eyepiece Collet:** Slips safely onto Ø28–30.5 mm light microscope eyepieces with gentle 360° friction ribs and an optional outer rubber-band groove — zero risk of cracking eyepiece or PLA!
- **Screwless Dual-Side Mobile Sliders (`56 – 100 mm`):** Mirror-twin left + right sliding jaws (`0.30 mm` smooth dovetail glide) auto-centered by 1–2 rubber bands on rear mushroom T-hooks, with twin bottom anti-drop ledges, self-wedging tapered grip, and optional `1.75 mm` filament end-stop pins.
- **Smooth 1-Screw X-Y Optical Lock:** Chamfered `5.8 mm` slots + `8.6 mm × 4.5 mm` flush anti-rotation hex channel + recessed-cup `thumb_knob.stl` (1×) — zero thread-binding, zero protrusion, `56 mm × 50 mm` travel (`112–162 mm` camera height).
- **100% Open Ø22 mm Optical Tunnel:** Verified `0.000 mm³` ray-probe blockage with exact 12 mm eye-relief stop.
- **Zero Supports:** All 5 STLs pre-oriented flat on bed (`phone_base.stl`, `clamp_jaw_left.stl`, `clamp_jaw_right.stl`, `eyepiece_arm.stl`, `thumb_knob.stl` 1×).
- **Folder:** `microscope-adapter/`

---

## Running the 3D Viewer Locally

```powershell
cd C:\Users\Tanish-Poddar\Downloads\smear-spreader
python -m http.server 8000
```

Then open **http://localhost:8000** in any browser.

- Use the top tab buttons (`🔬 Smear Spreader` / `📱 Microscope Adapter`) or URL hash (`#spreader`, `#adapter`) to switch models.
- Responsive on all devices (mobile portrait bottom-sheet, landscape compact card, desktop glassmorphic panel).

---

## Regenerating the CAD Models

Run with 64-bit Python 3.14 (CadQuery 2.8):

```powershell
# 1. Regenerate Smear Spreader
cd smear-spreader
py -3.14 spreader_model.py

# 2. Regenerate Microscope Adapter
cd ..\microscope-adapter
py -3.14 adapter_model.py
```

All models pass pre-flight wall checks (≥ 1.6 mm), clearance checks (0.25 mm), and post-export STL watertight manifold checks (0 non-manifold edges).
