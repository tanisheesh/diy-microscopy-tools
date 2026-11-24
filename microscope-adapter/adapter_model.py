"""
Universal Smartphone Microscope Eyepiece Adapter (v4 - Smooth Dual-Slider + Screwless Flex Collet)
Parametric CadQuery Model.

All dimensions are in mm. Change parameters in PARAMETERS section, then run:
    py -3.14 adapter_model.py

Hardware required (minimal, super light & 100% flush!):
    1x M5 x 20 mm standard hex bolt (DIN 933)  [ONLY for locking X-Y camera center!]
    1x M5 hex nut (DIN 934)
    1-2x standard rubber bands                 [drives BOTH left & right phone sliders!]
    2x 10 mm pieces of 1.75 mm filament        [optional end-stop pins in rail ends]

Outputs (all pre-oriented for 0% support 3D printing):
    phone_base.stl       (1x - Compact symmetrical open-top base, chamfered 5.8mm X-slot, flush hex rail, smooth dovetail)
    clamp_jaw_left.stl   (1x - Left sliding jaw + bottom anti-drop ledge + rear rubber-band T-hook + finger grip)
    clamp_jaw_right.stl  (1x - Right sliding jaw + bottom anti-drop ledge + rear rubber-band T-hook + finger grip)
    eyepiece_arm.stl     (1x - Screwless 6-petal flexible friction collet + 100% open Ø22 mm through-tunnel + 5.8mm Y-slot)
    thumb_knob.stl       (1x - Smooth 14.5 mm tall recessed-cup M5 knob that completely hides bolt tip)
    params.json          (Derived dimensions & transforms for the interactive Three.js 3D viewer)
"""
import json
import math
import struct
from collections import Counter
from pathlib import Path

import cadquery as cq

# ============================== PARAMETERS ==============================
# --- Smartphone Dimensions & Symmetrical Dual-Side Clamping Range ---
PHONE_W_MIN = 56.0          # min phone width (compact bare phone)
PHONE_W_NOM = 76.0          # nominal smartphone width (centered on X = 0)
PHONE_W_MAX = 100.0         # max phone width (Pro Max / Ultra + thick rugged case)
PHONE_T_MAX = 13.5          # max phone thickness with case
PHONE_L_REF = 158.0         # reference phone length (for viewer & checks)

# --- Symmetrical Cradle Geometry (Centered on X = 0) ---
JAW_X_MIN = PHONE_W_MIN / 2          # 28.0 mm
JAW_X_NOM = PHONE_W_NOM / 2          # 38.0 mm
JAW_X_MAX = PHONE_W_MAX / 2 + 1.5    # 51.5 mm

PHONE_BOT_Y = -65.0         # inner contact face of twin bottom anti-drop ledges
BASE_TOP_Y = 26.0           # top of cradle backplate (above this is 100% open camera zone!)
BASE_BOT_Y = -51.0          # bottom edge of compact base rail (clear above rear rubber-band hooks!)
JAW_BOT_Y = PHONE_BOT_Y - 4.5  # -69.5 mm (bottom outer face of anti-drop ledges on jaws)
BASE_T = 7.0                # backplate thickness (4.5 mm deep hex rail + 2.5 mm solid web)
JAW_WALL = 8.0              # slim, lightweight sliding jaw wall (no bulky clamp bolts!)
JAW_H = 14.5                # jaw height above phone backplate (Z = 0 to 14.5)
JAW_TAPER = 1.5             # gentle ~11 deg inward wedge (Z = 7.0 -> 14.5) pulls phone flat onto Z=0
JAW_LIP = 0.5               # extra top bezel retention bead
BOT_LEDGE_H = 13.0          # bottom anti-drop ledge forward height
BOT_LEDGE_W = 16.0          # inward span of each bottom ledge (24 mm center USB-C gap at min width)
BOT_LEDGE_LIP = 1.5         # front anti-slip lip on bottom ledges

# --- Buttery-Smooth Captive Dovetail-T Track & Rear Rubber-Band Hooks ---
TRACK_Y = -36.0             # Y center of captive dovetail-T guide track
TRACK_DEPTH = 4.0           # groove depth into base plate (solid floor web = 7.0 - 4.0 = 3.0 mm)
TRACK_NECK_W = 10.0         # dovetail neck opening width
TRACK_NECK_H = 1.6          # rail overhang lip thickness (>= MIN_WALL 1.6 mm)
TRACK_FLARE = 2.4           # 45 deg flare per side (max inner width = 14.8 mm)
TONGUE_INWARD = 23.0        # long 31 mm total tongue (prevents drawer-binding; 10 mm center gap at min width!)
RAIL_TOP_Y = -22.0          # top edge of lower rail
RAIL_X_HALF = 65.0          # compact symmetric rail half-width (X = -65 to +65 mm)
PIN_X = 62.5                # optional 1.75 mm filament end-stop pin holes near rail ends
PIN_HOLE_D = 1.85           # snug press-fit for standard 1.75 mm printer filament
JAW_TOP_Y = 12.0            # top edge of both left & right sliding jaws (81.5 mm tall symmetric grip!)
HOOK_Y = -59.5              # Y center of rear rubber-band T-hooks (clear below base & arm!)

# --- Single Flush M5 x 20 mm Optical Lock (Extra-Smooth Clearances!) ---
SLOT_W = 5.8                # generous +0.8 mm clearance over 5.0 mm M5 bolt -> threads NEVER bite plastic!
M5_HEX_CHAN_W = 8.6         # straight flat anti-rotation channel (8.0 mm hex flat + 0.6 mm smooth glide!)
M5_HEX_POCKET_D = 4.5       # deep front channel so 3.5 mm M5 hex head sits 1.0 mm below phone!
M5_NUT_AF = 8.5             # clean square press-fit for M5 hex nut inside thumb knob
M5_NUT_THICK = 4.2          # M5 hex nut pocket depth

# --- Centered 2-Axis Optical Alignment ---
OPT_SLOT_Y = 14.0           # Y center of horizontal optical X-slot on base plate
OPT_X_HALF = 28.0           # symmetric horizontal travel (-28 to +28 mm = 56 mm total travel!)
OPT_Y_TRAVEL = 50.0         # vertical slot travel (+/- 25 mm)
EP_CENTER_NOM_Y = 72.0      # nominal eyepiece Y (137 mm above phone bottom; range 112 - 162 mm!)
BASE_UPPER_X_HALF = OPT_X_HALF + 12.0  # 40.0 mm (X = -40 to +40 mm upper crossbar)

# --- Screwless 6-Petal Flexible Friction-Fit Eyepiece Collet ---
EYEPIECE_ID = 30.2          # nominal inner bore for standard 28.0 - 30.5 mm light microscope eyepieces
EYEPIECE_GRIP_BULGE = 0.7   # gentle inward friction rib on each petal (effective Ø28.8 mm flex grip!)
EYEPIECE_WALL = 2.4         # elastic flexing wall thickness (35.0 mm OD)
EYEPIECE_OD = EYEPIECE_ID + 2 * EYEPIECE_WALL  # 35.0 mm
EYEPIECE_SOCKET_LEN = 22.0  # depth of eyepiece grip socket
EYEPIECE_STOP_D = 22.0      # 100% open optical through-tunnel aperture diameter
EYEPIECE_STOP_Z = -12.0     # internal stop ring Z (exact 12.0 mm eye relief from phone back Z=0!)
PETAL_COUNT = 6             # 6 symmetric springy collet fingers (uniform 360 deg gentle grip!)
PETAL_SLIT_W = 2.2          # flex slit width between petals
PETAL_SLIT_LEN = 18.5       # long flexible cantilever length (stops 3.5 mm before rigid front flange)

# --- Eyepiece Arm & Single Ergonomic Thumb Knob ---
ARM_W = 24.0                # vertical arm plate width
ARM_T = 5.0                 # vertical arm plate thickness
KNOB_D = 24.0               # comfortable ergonomic thumb knob (only 1 knob!)
KNOB_H = 14.5               # tall recessed-cup knob (completely hides M5x20 bolt tip!)
KNOB_FLOOR = 3.5            # solid clamping floor between arm and M5 nut

# --- Smooth Sliding Tolerances & Export ---
CLR_SLIDE = 0.30            # buttery-smooth 0.30 mm clearance per dovetail face for rubber-band glide!
MIN_WALL = 1.6              # minimum printable wall thickness
STL_TOL = 0.02
STL_ANG_TOL = 0.1
# =======================================================================

OUT = Path(__file__).resolve().parent
SQ2 = math.sqrt(2)

# Derived symmetric geometry
OPT_X_TRAVEL = 2 * OPT_X_HALF                # 56.0 mm
ARM_Z_FRONT = -BASE_T                        # -7.0 mm
ARM_Z_BACK = ARM_Z_FRONT - ARM_T             # -12.0 mm
TUBE_Z_BOT = EYEPIECE_STOP_Z - EYEPIECE_SOCKET_LEN  # -34.0 mm


def groove_half_profile(c=0.0):
    """Right half of dovetail-T groove (y >= 0 from groove center), z relative to Z = 0.
    c > 0 produces the matching tongue shrunk by normal clearance c on every face."""
    neck = TRACK_NECK_W / 2 - c
    floor = -TRACK_DEPTH + c
    k = TRACK_NECK_W / 2 - TRACK_NECK_H - c * SQ2
    z_flare_top = k - neck
    y_bottom = k - floor
    return neck, z_flare_top, floor, y_bottom


def mirrored_profile(gy, z0, half, top_z):
    """Full YZ polygon from groove_half_profile centered on gy."""
    neck, zft, floor, yb = half
    right = [(neck, top_z), (neck, zft), (yb, floor)]
    pts = right + [(-y, z) for y, z in reversed(right)]
    return [(gy + y, z0 + z) for y, z in pts]


def checks():
    """Pre-flight wall-thickness, smooth-clearance, flush-bolt, and collision checks."""
    neck, zft, floor, yb = groove_half_profile(CLR_SLIDE)
    walls = {
        "base floor under dovetail groove": BASE_T - TRACK_DEPTH,
        "base web under optical hex channel": BASE_T - M5_HEX_POCKET_D,
        "base top wall above optical slot": BASE_TOP_Y - (OPT_SLOT_Y + M5_HEX_CHAN_W / 2),
        "base side wall past optical hex channel": BASE_UPPER_X_HALF - (OPT_X_HALF + M5_HEX_CHAN_W / 2 + 0.6),
        "base wall below dovetail groove": abs(BASE_BOT_Y - (TRACK_Y - (TRACK_NECK_W / 2 + TRACK_FLARE))),
        "eyepiece collet wall": EYEPIECE_WALL,
        "eyepiece optical flange wall": (EYEPIECE_OD - EYEPIECE_STOP_D) / 2,
        "eyepiece flange thickness": abs(EYEPIECE_STOP_Z - ARM_Z_FRONT),
        "thumb knob solid floor": KNOB_FLOOR,
        "dovetail rail lip": TRACK_NECK_H,
        "dovetail tongue neck": 2 * neck,
        "arm wall beside vertical slot": (ARM_W - SLOT_W) / 2,
    }
    for name, v in walls.items():
        assert v >= MIN_WALL - 1e-9, f"{name} = {v:.2f} mm < {MIN_WALL}"

    assert 0.25 <= CLR_SLIDE <= 0.45, f"CLR_SLIDE = {CLR_SLIDE} should be in smooth range 0.25-0.45 mm"
    assert SLOT_W >= 5.6, "M5 slot must be >= 5.6 mm for smooth non-binding glide!"
    assert M5_HEX_CHAN_W >= 8.5, "M5 hex channel must be >= 8.5 mm for smooth non-binding glide!"
    assert yb > TRACK_NECK_W / 2 + 0.5, "Tongue undercut too small for captive retention"

    # Verify single M5 x 20 mm bolt engages 100% of nut AND stays hidden inside knob cup!
    bolt_len = 20.0
    opt_stack = (BASE_T - M5_HEX_POCKET_D) + ARM_T + KNOB_FLOOR + M5_NUT_THICK
    max_hidden_len = (BASE_T - M5_HEX_POCKET_D) + ARM_T + KNOB_H
    assert opt_stack <= bolt_len <= max_hidden_len, \
        f"Optical M5x20 bolt fit error: engage={opt_stack:.1f}, max_hidden={max_hidden_len:.1f}"

    # Verify Optical Knob never hits eyepiece collet at lowest Y position
    ep_lowest_outer_y = (EP_CENTER_NOM_Y - OPT_Y_TRAVEL / 2) - EYEPIECE_OD / 2
    knob_top_y = OPT_SLOT_Y + KNOB_D / 2
    assert ep_lowest_outer_y > knob_top_y + 2.5, \
        f"Optical Knob ({knob_top_y:.1f}) too close to eyepiece collet ({ep_lowest_outer_y:.1f})"

    # Verify Eyepiece Arm lowest edge stays well above rear rubber-band hooks (HOOK_Y = -59.5)
    arm_bot_nom_y = OPT_SLOT_Y - OPT_Y_TRAVEL / 2 - SLOT_W / 2 - 4.8
    arm_lowest_y = arm_bot_nom_y - OPT_Y_TRAVEL / 2
    hook_top_y = HOOK_Y + 5.5
    assert arm_lowest_y > hook_top_y + 5.0, \
        f"Arm lowest edge ({arm_lowest_y:.1f}) too close to rubber-band hooks ({hook_top_y:.1f})"

    # Verify dual jaws, bottom ledges, and tongues clear at min phone width
    assert 2 * (JAW_X_MIN - BOT_LEDGE_W) >= 18.0, "Bottom ledges too close at min width"
    assert 2 * (JAW_X_MIN - TONGUE_INWARD) >= 8.0, "Dovetail tongues too close at min width"
    assert JAW_X_MAX + JAW_WALL < PIN_X - 1.5, "Jaw outer wall collides with filament end-stop pin at max width"

    return walls


def make_phone_base():
    """Compact, lightweight, 100% symmetrical open-top cradle backplate (centered on X = 0):
    - Full-width smooth captive dovetail-T groove (0.30 mm clearance + chamfered entries!)
    - Two optional 1.75 mm filament end-stop pin holes at X = +/-62.5 mm
    - Centered 5.8 mm wide chamfered horizontal M5 optical slot + 8.6 mm smooth anti-rotation hex channel
    - Ends cleanly at Y = -51.0 mm so rear rubber-band hooks glide freely below with zero friction!
    - 100% flat rear face (Z = -BASE_T) for zero-support 3D printing
    """
    outline = [
        (-RAIL_X_HALF, BASE_BOT_Y),
        (RAIL_X_HALF, BASE_BOT_Y),
        (RAIL_X_HALF, RAIL_TOP_Y),
        (BASE_UPPER_X_HALF, RAIL_TOP_Y),
        (BASE_UPPER_X_HALF, BASE_TOP_Y),
        (-BASE_UPPER_X_HALF, BASE_TOP_Y),
        (-BASE_UPPER_X_HALF, RAIL_TOP_Y),
        (-RAIL_X_HALF, RAIL_TOP_Y),
    ]
    base = (cq.Workplane("XY", origin=(0, 0, -BASE_T))
            .polyline(outline).close().extrude(BASE_T))
    base = base.edges("|Z").fillet(3.0)

    # 1. Full-width Captive Dovetail-T Track Groove (open at both ends for left & right sliding jaws)
    track_pts = mirrored_profile(TRACK_Y, 0.0, groove_half_profile(0.0), 0.5)
    track_cut = (cq.Workplane("YZ", origin=(-RAIL_X_HALF - 2.0, 0, 0))
                 .polyline(track_pts).close().extrude(2 * RAIL_X_HALF + 4.0))
    base = base.cut(track_cut)

    # 2. Optional 1.75 mm Filament End-Stop Pin Holes near outer rail ends (keeps jaws permanently captive!)
    for side in (-1, 1):
        pin_hole = (cq.Workplane("XY", origin=(side * PIN_X, TRACK_Y, -BASE_T - 1))
                    .circle(PIN_HOLE_D / 2).extrude(BASE_T + 2))
        base = base.cut(pin_hole)

    # 3. Centered 5.8 mm Wide Smooth Horizontal Optical X-Slot (Y = +14.0 mm)
    opt_through = (cq.Workplane("XY", origin=(0, OPT_SLOT_Y, -BASE_T - 1))
                   .slot2D(OPT_X_TRAVEL + SLOT_W, SLOT_W)
                   .extrude(BASE_T + 2))
    base = base.cut(opt_through)

    # 0.5 mm lead-in bevel on rear exit of X-slot (eliminates bed elephant-foot roughness!)
    rear_bevel = (cq.Workplane("XY", origin=(0, OPT_SLOT_Y, -BASE_T - 0.1))
                  .slot2D(OPT_X_TRAVEL + SLOT_W + 1.0, SLOT_W + 1.0)
                  .extrude(0.6))
    base = base.cut(rear_bevel)

    # 4. Smooth Anti-Rotation M5 Hex Bolt Channel (8.6 mm wide x 4.5 mm deep -> 1.0 mm below phone!)
    opt_hex_len = OPT_X_TRAVEL + M5_HEX_CHAN_W + 1.2
    opt_hex = (cq.Workplane("XY", origin=(0, OPT_SLOT_Y, -M5_HEX_POCKET_D))
               .box(opt_hex_len, M5_HEX_CHAN_W, M5_HEX_POCKET_D + 0.5, centered=(True, True, False)))
    base = base.cut(opt_hex)

    return base


def make_clamp_jaw_right():
    """Slim, lightweight, buttery-smooth sliding RIGHT phone clamp jaw (zero screws!):
    - 81.5 mm tall self-wedging tapered jaw wall (vertical 0->7 mm, ~11 deg wedge 7->14.5 mm)
    - Bottom right anti-drop ledge (16 mm inward, glides 0.25 mm above base)
    - Long 31 mm captive dovetail-T tongue (0.30 mm smooth clearance, recessed 0.25 mm below phone!)
    - Rear rubber-band T-hook below base plate (Y = -59.5 mm) for effortless self-centering tension!
    - Sculpted side finger-pull ridge for easy 1-handed phone insertion
    - Print orientation: rotated +90 deg around Y (outer right cheek flat on bed -> 0% overhangs!)
    """
    x_in = JAW_X_NOM                     # +38.0 mm
    x_out = x_in + JAW_WALL              # +46.0 mm (flat print bed plane!)
    jaw_len = JAW_TOP_Y - JAW_BOT_Y      # 81.5 mm
    jaw_mid_y = (JAW_TOP_Y + JAW_BOT_Y) / 2

    # 1. Main Right Jaw Wall (slim 8.0 mm wide, self-wedging tapered inner grip)
    jaw_pts = [
        (x_out, 0.0),
        (x_in, 0.0),
        (x_in, 7.0),
        (x_in - JAW_TAPER, JAW_H - 1.2),
        (x_in - JAW_TAPER - JAW_LIP, JAW_H),
        (x_out, JAW_H),
    ]
    jaw = (cq.Workplane("XZ", origin=(0, jaw_mid_y, 0))
           .polyline(jaw_pts).close().extrude(jaw_len / 2, both=True))

    # 2. Bottom Right Anti-Drop Ledge (holds phone weight on 45 deg tilted microscopes!)
    ledge_x0 = x_in - BOT_LEDGE_W
    ledge_pts = [
        (JAW_BOT_Y, 0.25),
        (PHONE_BOT_Y, 0.25),
        (PHONE_BOT_Y, BOT_LEDGE_H - BOT_LEDGE_LIP),
        (PHONE_BOT_Y + BOT_LEDGE_LIP, BOT_LEDGE_H),
        (JAW_BOT_Y, BOT_LEDGE_H),
    ]
    right_ledge = (cq.Workplane("YZ", origin=(ledge_x0, 0, 0))
                   .polyline(ledge_pts).close().extrude(x_out - ledge_x0))
    jaw = jaw.union(right_ledge)

    # 3. Long 31 mm Smooth Captive Dovetail-T Tongue (centered at TRACK_Y = -36.0 mm)
    tongue_x0 = x_in - TONGUE_INWARD
    half_t = groove_half_profile(CLR_SLIDE)
    tongue_under_phone = (cq.Workplane("YZ", origin=(tongue_x0, 0, 0))
                          .polyline(mirrored_profile(TRACK_Y, 0.0, half_t, -0.25))
                          .close().extrude(x_in - tongue_x0 + 0.5))
    tongue_under_jaw = (cq.Workplane("YZ", origin=(x_in, 0, 0))
                        .polyline(mirrored_profile(TRACK_Y, 0.0, half_t, 1.0))
                        .close().extrude(x_out - x_in))
    jaw = jaw.union(tongue_under_phone).union(tongue_under_jaw)

    # 4. Rear Rubber-Band Mushroom T-Hook (Y = -59.5 mm, Z = -10.5 to 0.0 mm, clear below phone_base!)
    # Flared +/-2.0 mm in Y at 45 deg so rubber bands NEVER slip off, prints 100% flat on bed!
    hook_yz = [
        (HOOK_Y - 3.5, 1.0),
        (HOOK_Y - 3.5, -6.5),
        (HOOK_Y - 5.5, -8.5),
        (HOOK_Y - 5.5, -10.5),
        (HOOK_Y + 5.5, -10.5),
        (HOOK_Y + 5.5, -8.5),
        (HOOK_Y + 3.5, -6.5),
        (HOOK_Y + 3.5, 1.0),
    ]
    hook = (cq.Workplane("YZ", origin=(x_in, 0, 0))
            .polyline(hook_yz).close().extrude(x_out - x_in))
    jaw = jaw.union(hook)

    # 5. Ergonomic Finger Pull Wing (front-outer grip ridge on +Z, Y = -42 to -12 mm, flush with x_out!)
    grip_yz = [
        (-42.0, JAW_H - 0.5),
        (-38.0, JAW_H + 3.2),
        (-16.0, JAW_H + 3.2),
        (-12.0, JAW_H - 0.5),
    ]
    grip = (cq.Workplane("YZ", origin=(x_out - 4.5, 0, 0))
            .polyline(grip_yz).close().extrude(4.5))
    jaw = jaw.union(grip)

    return jaw


def make_clamp_jaw_left():
    """Exact mirror-image sliding LEFT phone clamp jaw (assembly frame at -JAW_X_NOM = -38 mm).
    Print orientation: rotated -90 deg around Y (outer left cheek flat on bed -> 0% overhangs!).
    """
    return make_clamp_jaw_right().mirror("YZ")


def make_eyepiece_arm():
    """Smooth 2-Axis Vertical Alignment Arm + Screwless 6-Petal Flexible Friction Eyepiece Collet:
    - ZERO screws on the eyepiece -> 0% risk of cracking eyepiece or PLA!
    - 6 springy collet petals with gentle internal 0.7 mm friction grip beads & 45 deg lead-in bevel
    - External optional rubber-band groove on collet for extra grip on very slim (27.5 mm) eyepieces
    - 100% OPEN Ø22.0 mm through-tunnel (cut LAST & verified by automated ray-probe!)
    - 5.8 mm wide chamfered vertical M5 slot (buttery-smooth non-binding slide!)
    - 100% flat front face on bed (rotated 180 deg around X -> 0% overhangs!)
    """
    slot_bot_y = OPT_SLOT_Y - OPT_Y_TRAVEL / 2 - SLOT_W / 2
    arm_bot_y = slot_bot_y - 4.8
    arm_top_y = EP_CENTER_NOM_Y
    arm_h = arm_top_y - arm_bot_y
    arm_mid_y = (arm_top_y + arm_bot_y) / 2

    # 1. Vertical Arm Plate (Z = -12.0 to -7.0 mm)
    arm = (cq.Workplane("XY", origin=(0, arm_mid_y, ARM_Z_BACK))
           .box(ARM_W, arm_h, ARM_T, centered=(True, True, False)))
    arm = arm.edges("|Z").fillet(3.0)

    # 2. Revolved Screwless 6-Petal Collet Profile (includes 45 deg entry bevel, gentle internal
    # friction grip bead, internal 12.0 mm eye-relief stop, and external optional rubber-band groove!)
    # Profile in (R, Z) coordinates around optical axis (X = 0, Y = EP_CENTER_NOM_Y):
    r_out = EYEPIECE_OD / 2            # 17.5 mm
    r_groove = r_out - 1.2             # 16.3 mm (outer optional rubber-band groove)
    r_in = EYEPIECE_ID / 2             # 15.1 mm (nominal bore)
    r_grip = r_in - EYEPIECE_GRIP_BULGE  # 14.4 mm (gentle friction bead -> Ø28.8 mm elastic grip!)
    r_hole = EYEPIECE_STOP_D / 2       # 11.0 mm (100% open Ø22 mm through-tunnel!)

    collet_rz = [
        (r_hole, ARM_Z_FRONT),         # Front flat face on bed (Z = -7.0)
        (r_out,  ARM_Z_FRONT),         # Outer edge on bed
        (r_out,  -22.5),               # Solid outer wall up to outer groove
        (r_groove, -23.7),             # 45 deg chamfer into optional rubber-band groove
        (r_groove, -27.5),             # Groove floor
        (r_out,  -28.7),               # 45 deg chamfer back out
        (r_out,  TUBE_Z_BOT),          # Bottom lip of collet (Z = -34.0)
        (r_in + 0.6, TUBE_Z_BOT),      # Wide 45 deg entry funnel for effortless slip-on!
        (r_grip, TUBE_Z_BOT + 2.2),    # Smooth gentle friction grip ridge peak
        (r_grip, TUBE_Z_BOT + 4.8),    # Smooth contact band (2.6 mm wide)
        (r_in,   TUBE_Z_BOT + 6.5),    # Smooth taper back to 30.2 mm bore
        (r_in,   EYEPIECE_STOP_Z),     # Straight bore up to internal 12.0 mm eye-relief stop!
        (r_hole, EYEPIECE_STOP_Z),     # Internal stop shoulder
    ]
    # Build revolved collet centered at (0, EP_CENTER_NOM_Y, 0)
    collet = (cq.Workplane("XZ", origin=(0, EP_CENTER_NOM_Y, 0))
              .polyline(collet_rz).close()
              .revolve(360, (0, 0, 0), (0, 1, 0)))

    # Union arm plate + collet FIRST before cutting through-tunnel, flex slits & vertical slot!
    arm = arm.union(collet)

    # 3. 5.8 mm Wide Smooth Vertical M5 Adjustment Slot + Lead-in Chamfers
    v_slot = (cq.Workplane("XY", origin=(0, OPT_SLOT_Y, ARM_Z_BACK - 1))
              .slot2D(OPT_Y_TRAVEL + SLOT_W, SLOT_W, 90)
              .extrude(ARM_T + 2))
    arm = arm.cut(v_slot)

    # 0.5 mm chamfer on BOTH faces of vertical slot -> zero burrs, silky slide!
    v_bev_front = (cq.Workplane("XY", origin=(0, OPT_SLOT_Y, ARM_Z_FRONT - 0.5))
                   .slot2D(OPT_Y_TRAVEL + SLOT_W + 1.0, SLOT_W + 1.0, 90)
                   .extrude(0.6))
    v_bev_back = (cq.Workplane("XY", origin=(0, OPT_SLOT_Y, ARM_Z_BACK - 0.1))
                  .slot2D(OPT_Y_TRAVEL + SLOT_W + 1.0, SLOT_W + 1.0, 90)
                  .extrude(0.6))
    arm = arm.cut(v_bev_front).cut(v_bev_back)

    # 4. 100% OPEN Optical Through-Tunnel (Ø22.0 mm ALL THE WAY THROUGH!)
    optical_tunnel = (cq.Workplane("XY", origin=(0, EP_CENTER_NOM_Y, TUBE_Z_BOT - 2))
                      .circle(EYEPIECE_STOP_D / 2)
                      .extrude(ARM_Z_FRONT - TUBE_Z_BOT + 6))
    arm = arm.cut(optical_tunnel)

    # 5. 6 Symmetric Collet Flex Slits (30 deg offset so slits sit symmetrically off the arm spine!)
    slit_top_z = TUBE_Z_BOT + PETAL_SLIT_LEN  # -15.5 mm (leaves 3.5 mm rigid flange ring!)
    for i in range(PETAL_COUNT):
        ang_deg = 30.0 + i * (360.0 / PETAL_COUNT)
        slit = (cq.Workplane("XY", origin=(0, EP_CENTER_NOM_Y, TUBE_Z_BOT - 1))
                .box(PETAL_SLIT_W, EYEPIECE_OD, PETAL_SLIT_LEN + 1.0, centered=(True, False, False))
                .rotate((0, EP_CENTER_NOM_Y, 0), (0, EP_CENTER_NOM_Y, 1), ang_deg))
        arm = arm.cut(slit)
        # Round stress-relief hole at top of each flex slit (prevents cracking!)
        relief = (cq.Workplane("XZ", origin=(0, EP_CENTER_NOM_Y, 0))
                  .center(0, slit_top_z)
                  .circle(1.3).extrude(EYEPIECE_OD)
                  .rotate((0, EP_CENTER_NOM_Y, 0), (0, EP_CENTER_NOM_Y, 1), ang_deg + 180))
        arm = arm.cut(relief)

    return arm


def make_thumb_knob():
    """Single ultra-smooth 14.5 mm tall ergonomic 6-flute M5 thumb knob (Print 1x!):
    - 5.8 mm central floor hole -> bolt threads NEVER touch plastic, ONLY the metal M5 nut!
    - 8.5 mm AF square hex nut pocket -> smooth press-fit, zero crooked thread binding!
    - 6.8 mm deep recessed bolt-tip cup -> completely hides M5 x 20 mm bolt end!
    - 1.5 mm bottom chamfer -> clean, low-friction clamping contact on arm!
    """
    knob = cq.Workplane("XY").circle(KNOB_D / 2).extrude(KNOB_H)

    flute_r = 3.0
    for i in range(6):
        ang = i * (2 * math.pi / 6)
        fx = (KNOB_D / 2) * math.cos(ang)
        fy = (KNOB_D / 2) * math.sin(ang)
        flute = (cq.Workplane("XY", origin=(fx, fy, -1))
                 .circle(flute_r).extrude(KNOB_H + 2))
        knob = knob.cut(flute)

    # Smooth 5.8 mm shaft bore (threads never bind on plastic!)
    hole = cq.Workplane("XY", origin=(0, 0, -1)).circle(SLOT_W / 2).extrude(KNOB_H + 2)
    knob = knob.cut(hole)

    # Captive M5 hex nut pocket (8.5 mm AF)
    hex_r = M5_NUT_AF / math.cos(math.pi / 6) / 2
    hex_nut = (cq.Workplane("XY", origin=(0, 0, KNOB_FLOOR))
               .polygon(6, hex_r * 2).extrude(M5_NUT_THICK + 1.0))
    knob = knob.cut(hex_nut)

    # Recessed bolt-tip shield cup (completely hides M5 x 20 mm bolt end!)
    cup = (cq.Workplane("XY", origin=(0, 0, KNOB_FLOOR + M5_NUT_THICK))
           .circle(5.75).extrude(KNOB_H))
    knob = knob.cut(cup)

    knob = knob.edges(">Z").chamfer(1.0).edges("<Z").chamfer(1.2)
    return knob


def verify_stl(path, cad_volume):
    """Re-read exported binary STL and verify printability."""
    p = Path(path)
    data = p.read_bytes()
    n = struct.unpack_from("<I", data, 80)[0]
    assert len(data) == 84 + 50 * n, f"{p.name}: not a valid binary STL"
    key = lambda v: tuple(round(c, 4) for c in v)
    edges, vol, zmin, bed_area = Counter(), 0.0, math.inf, 0.0
    for i in range(n):
        f = struct.unpack_from("<12f", data, 84 + 50 * i)
        v = [f[3:6], f[6:9], f[9:12]]
        ks = [key(p_) for p_ in v]
        for j in range(3):
            a_, b_ = ks[j], ks[(j + 1) % 3]
            edges[(a_, b_) if a_ < b_ else (b_, a_)] += 1
        (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = v
        vol += (x1 * (y2 * z3 - y3 * z2) - x2 * (y1 * z3 - y3 * z1) + x3 * (y1 * z2 - y2 * z1)) / 6
        zmin = min(zmin, z1, z2, z3)
        if max(z1, z2, z3) < 1e-4:
            bed_area += abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2
    bad = sum(1 for c in edges.values() if c != 2)
    assert bad == 0, f"{p.name}: {bad} non-manifold / open edges"
    assert vol > 0, f"{p.name}: inverted normals"
    assert abs(vol - cad_volume) / cad_volume < 0.015, \
        f"{p.name}: volume {vol:.0f} vs CAD {cad_volume:.0f} mm^3"
    assert abs(zmin) < 1e-4, f"{p.name}: not sitting on the bed (z min = {zmin:.3f})"
    assert bed_area > 150, f"{p.name}: only {bed_area:.0f} mm^2 touching the bed"
    return n, vol, bed_area


def vol_inter(a, b):
    inter = a.intersect(b)
    return inter.val().Volume() if inter.vals() else 0.0


def main():
    walls = checks()
    print("Pre-flight wall checks:", {k: round(v, 2) for k, v in walls.items()})

    base = make_phone_base()
    jaw_r = make_clamp_jaw_right()
    jaw_l = make_clamp_jaw_left()
    arm = make_eyepiece_arm()
    knob = make_thumb_knob()

    knob_opt_asm = knob.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, OPT_SLOT_Y, ARM_Z_BACK))

    # 1. Interference checks across full symmetric dual-side phone clamping (56 - 100 mm)
    for w in (PHONE_W_MIN, 66.0, PHONE_W_NOM, 88.0, PHONE_W_MAX):
        half_delta = w / 2 - JAW_X_NOM
        jl = jaw_l.translate((-half_delta, 0, 0))
        jr = jaw_r.translate((+half_delta, 0, 0))
        assert vol_inter(base, jl) < 1e-3, f"Base-LeftJaw collision at width {w} mm"
        assert vol_inter(base, jr) < 1e-3, f"Base-RightJaw collision at width {w} mm"
        assert vol_inter(jl, jr) < 1e-3, f"LeftJaw-RightJaw collision at width {w} mm"

        # Thin bare phone (7.0 mm)
        phone_thin = (cq.Workplane("XY", origin=(-w / 2 + 0.2, PHONE_BOT_Y + 0.2, 0.2))
                      .box(w - 0.4, PHONE_L_REF, 6.8, centered=(False, False, False)))
        assert vol_inter(base, phone_thin) < 1e-3, f"Base collides with thin {w} mm phone"
        assert vol_inter(jl, phone_thin) < 1e-3 and vol_inter(jr, phone_thin) < 1e-3, f"Jaw collides with thin {w} mm phone"

        # Thick cased phone (12.0 mm)
        jl_t = jaw_l.translate((-half_delta - 1.4, 0, 0))
        jr_t = jaw_r.translate((+half_delta + 1.4, 0, 0))
        assert vol_inter(base, jl_t) < 1e-3 and vol_inter(base, jr_t) < 1e-3, f"Base-Jaw collision at thick {w} mm"
        phone_thick = (cq.Workplane("XY", origin=(-w / 2, PHONE_BOT_Y + 0.4, 0.2))
                       .box(w, PHONE_L_REF, 11.2, centered=(False, False, False)))
        assert vol_inter(jl_t, phone_thick) < 1e-3 and vol_inter(jr_t, phone_thick) < 1e-3, f"Jaw collides with thick {w} mm phone"

    # 2. Captive dovetail retention checks on BOTH Left & Right jaws
    lift = CLR_SLIDE * SQ2 + 0.4
    assert vol_inter(base, jaw_l.translate((0, 0, lift))) > 5.0, "Left jaw is not captive!"
    assert vol_inter(base, jaw_r.translate((0, 0, lift))) > 5.0, "Right jaw is not captive!"

    # 3. Full 2-axis optical travel + Single Knob vs Flex Collet + Arm vs Jaws/Hooks
    for ax in (-OPT_X_HALF, 0.0, OPT_X_HALF):
        for ay in (-OPT_Y_TRAVEL / 2, 0.0, OPT_Y_TRAVEL / 2):
            a_s = arm.translate((ax, ay, 0))
            k_s = knob_opt_asm.translate((ax, 0, 0))
            assert vol_inter(base, a_s) < 1e-3, f"Base-Arm collision at ({ax}, {ay})"
            assert vol_inter(a_s, k_s) < 1e-3, f"Arm-Knob collision at ({ax}, {ay})"
            assert vol_inter(a_s, jaw_l) < 1e-3 and vol_inter(a_s, jaw_r) < 1e-3, f"Arm-Jaw collision at ({ax}, {ay})"

    # 4. Optical through-tunnel ray probe test (100% open Ø22 mm light path!)
    optical_probe = (cq.Workplane("XY", origin=(0, EP_CENTER_NOM_Y, -50.0))
                     .circle(EYEPIECE_STOP_D / 2 - 0.2)
                     .extrude(60.0))
    probe_vol = vol_inter(arm, optical_probe)
    assert probe_vol < 1e-3, f"Optical tunnel is blocked by {probe_vol:.2f} mm^3 plastic!"

    # 5. Export all 5 STLs pre-oriented for 0% support printing
    parts_spec = [
        ("phone_base.stl",      base,  None, 0),
        ("clamp_jaw_left.stl",  jaw_l, "Y", -90),  # Outer left cheek flat on bed -> 0% overhangs!
        ("clamp_jaw_right.stl", jaw_r, "Y",  90),  # Outer right cheek flat on bed -> 0% overhangs!
        ("eyepiece_arm.stl",    arm,   "X", 180),  # Flat front arm face on bed, flex collet up -> 0% overhangs!
        ("thumb_knob.stl",      knob,  None, 0),   # Flat clamping floor on bed, cup up -> 0% overhangs!
    ]

    transforms = {}
    for fname, raw_solid, rot_axis, rot_deg in parts_spec:
        assert raw_solid.val().isValid(), f"{fname} solid is invalid"
        assert len(raw_solid.solids().vals()) == 1, f"{fname} has {len(raw_solid.solids().vals())} solids"

        p = raw_solid
        if rot_axis == "X":
            p = p.rotate((0, 0, 0), (1, 0, 0), rot_deg)
        elif rot_axis == "Y":
            p = p.rotate((0, 0, 0), (0, 1, 0), rot_deg)

        bb = p.val().BoundingBox()
        print_shift = [-bb.xmin, -bb.ymin, -bb.zmin]
        print_solid = p.translate(print_shift)
        transforms[fname] = {
            "printShift": print_shift,
            "rotAxis": rot_axis or "",
            "rotDeg": rot_deg,
        }

        out_path = OUT / fname
        cq.exporters.export(print_solid, str(out_path), tolerance=STL_TOL, angularTolerance=STL_ANG_TOL)
        n, vol, bed = verify_stl(out_path, print_solid.val().Volume())
        pb = print_solid.val().BoundingBox()
        print(f"{fname}: {n} tris, watertight, {pb.xlen:.1f}x{pb.ylen:.1f}x{pb.zlen:.1f} mm, "
              f"vol {vol/1000:.2f} cm^3, {bed:.0f} mm^2 on bed")

    params = {
        "version": 4,
        "phone": {
            "wMin": PHONE_W_MIN,
            "wNom": PHONE_W_NOM,
            "wMax": PHONE_W_MAX,
            "tMax": PHONE_T_MAX,
            "lRef": PHONE_L_REF,
            "jawXMin": JAW_X_MIN,
            "jawXNom": JAW_X_NOM,
            "jawXMax": JAW_X_MAX,
            "jawWall": JAW_WALL,
            "botY": PHONE_BOT_Y,
            "hookY": HOOK_Y,
            "pinX": PIN_X,
            "trackY": TRACK_Y,
        },
        "eyepiece": {
            "id": EYEPIECE_ID,
            "od": EYEPIECE_OD,
            "socketLen": EYEPIECE_SOCKET_LEN,
            "stopD": EYEPIECE_STOP_D,
            "stopZ": EYEPIECE_STOP_Z,
            "tubeZBot": TUBE_Z_BOT,
            "centerNomY": EP_CENTER_NOM_Y,
        },
        "adjust": {
            "xMin": -OPT_X_HALF,
            "xMax": OPT_X_HALF,
            "xNom": 0.0,
            "yMin": -OPT_Y_TRAVEL / 2,
            "yMax": OPT_Y_TRAVEL / 2,
            "yNom": 0.0,
            "optSlotY": OPT_SLOT_Y,
        },
        "base": {
            "t": BASE_T,
            "armT": ARM_T,
            "armZBack": ARM_Z_BACK,
            "knobH": KNOB_H,
            "jawH": JAW_H,
        },
        "transforms": transforms,
    }
    (OUT / "params.json").write_text(json.dumps(params, indent=2))
    print(f"\nGenerated v4 (1-Screw Smooth Dual-Slider + Flex Collet) params.json:")
    print(f"  Phone width range : {PHONE_W_MIN:.0f} -> {PHONE_W_MAX:.0f} mm (rubber-band self-centering dual sliders)")
    print(f"  Smooth clearances : slots = {SLOT_W} mm, hex channel = {M5_HEX_CHAN_W} mm, dovetail = {CLR_SLIDE} mm")
    print(f"  Camera X travel   : -{OPT_X_HALF:.0f} -> +{OPT_X_HALF:.0f} mm ({OPT_X_TRAVEL:.0f} mm symmetric)")
    print(f"  Camera Y height   : {EP_CENTER_NOM_Y - OPT_Y_TRAVEL/2 - PHONE_BOT_Y:.0f} -> "
          f"{EP_CENTER_NOM_Y + OPT_Y_TRAVEL/2 - PHONE_BOT_Y:.0f} mm above phone bottom")
    print(f"  Eyepiece grip     : Screwless 6-petal flexible friction collet (Ø28-30.5 mm, 0% crack risk!)")
    print(f"  Optical tunnel    : Ø{EYEPIECE_STOP_D:.0f} mm 100% OPEN (probe blockage = 0.000 mm^3)")
    print(f"  Total Hardware    : ONLY 1x M5 x 20 mm hex bolt + 1x M5 nut + 1-2 rubber bands!")
    print("ALL v4 CAD, SMOOTH-CLEARANCE, CAPTIVE, OPTICAL & STL CHECKS PASSED!")


if __name__ == "__main__":
    main()
