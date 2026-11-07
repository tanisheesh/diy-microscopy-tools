# Open Laboratory 3D Tools

A collection of 100% 3D-printable, open-hardware precision laboratory jigs designed in parametric CadQuery.

**Live 3D Interactive Web Viewer:** https://tanisheesh.github.io/smear-spreader/

---

## Included Tools

### 1. 🔬 Blood Smear Slide Spreader
A captive 3D-printable jig for making consistent, reproducible blood smears. The base slide (75 × 25 × 1 mm) sits in a recessed bed. A captive carriage runs along rails and holds a glass spreader slide at **45°**. Push the carriage forward and it makes the smear.

- **Captive Fit:** Dovetail-T tongues trapped in undercut grooves (cannot lift off).
- **End Stops:** Closed front end stop + removable rear 1.75 mm filament stop pins.
- **Smear Travel:** ~48 mm smooth stroke.
- **Files:** `spreader_model.py`, `base.stl`, `carriage.stl`, `params.json`.

---

### 2. 📱 Smartphone Microscope Eyepiece Adapter
A universal 2-axis adjustable smartphone adapter for light microscopes (compound, monocular, binocular, stereo). Clamps any phone (60 mm to 92 mm wide) and locks the camera over the microscope's eyepiece (Ø28.0 mm to Ø30.5 mm) for microphotography and group viewing.

- **Universal Clamp:** Captive dovetail-T sliding jaw + ergonomic D-ring finger pull handle.
- **2-Axis Cross-Slotted Alignment (X: ±16 mm, Y: ±21 mm):** Fits all smartphone camera locations (corner or center).
- **Stepped Eyepiece Collar:** Ø30.0 mm ID split clamp with Ø21 mm internal eye-relief aperture stop.
- **Zero Supports:** 100% 3D-printable with pre-oriented flat bed planes.
- **Folder:** `microscope-adapter/`
- **Files:** `adapter_model.py`, `phone_base.stl`, `clamp_jaw.stl`, `eyepiece_arm.stl`, `thumb_knob.stl`, `params.json`.

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
py -3.14 spreader_model.py

# 2. Regenerate Microscope Adapter
cd microscope-adapter
py -3.14 adapter_model.py
```

All models pass pre-flight wall checks (≥ 1.6 mm), clearance checks (0.25 mm), and post-export STL watertight manifold checks (0 non-manifold edges).
