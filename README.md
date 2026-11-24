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

### 2. 📱 Smartphone Microscope Eyepiece Adapter (v3 — Dual-Side Adjustable)
A symmetrical dual-side adjustable smartphone adapter for light microscopes (compound, monocular, binocular, stereo). Both left and right jaws slide and lock independently so any smartphone (**56 mm – 100 mm wide**, bare or thick cased up to 13.5 mm thick) sits centered and balanced on twin bottom anti-drop ledges over the microscope's eyepiece (**Ø27.5 mm – Ø30.5 mm**).

- **Dual-Side Phone Adjusters:** Mirror-twin left + right sliding jaws with bottom anti-drop support ledges, self-wedging tapered grip faces, full-width captive dovetail-T track, and independent flush M5 lock knobs.
- **Centered 2-Axis Optical Alignment:** 56 mm symmetric horizontal travel (`-28` to `+28 mm`) + 50 mm vertical travel (`111–161 mm` above phone bottom) fits left-corner, center, and right-corner cameras.
- **Open Optical Tunnel:** Ø30.5 mm ID full-length split-clamp collar with 100% open Ø22 mm through-tunnel and exact 12 mm eye-relief stop.
- **Flush Single-Size Hardware:** 4× `M5 × 20 mm` hex bolts + 4× `M5` hex nuts (all heads & bolt tips sit completely recessed — zero protrusion!).
- **Zero Supports:** 100% 3D-printable with pre-oriented flat bed planes (print `thumb_knob.stl` 3×).
- **Folder:** `microscope-adapter/`
- **Files:** `adapter_model.py`, `phone_base.stl`, `clamp_jaw_left.stl`, `clamp_jaw_right.stl`, `eyepiece_arm.stl`, `thumb_knob.stl`, `params.json`.

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
