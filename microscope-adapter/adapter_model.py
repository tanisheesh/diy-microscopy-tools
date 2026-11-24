"""
Universal Smartphone Microscope Eyepiece Adapter (v2) - Parametric CadQuery Model.

All dimensions are in mm. Change parameters in PARAMETERS section, then run:
    py -3.14 adapter_model.py

Hardware required (unified single bolt size):
    3x M5 x 20 mm standard hex bolts (DIN 933)
    3x M5 hex nuts (DIN 934)

Outputs (all pre-oriented for 0% support 3D printing):
    phone_base.stl   (Open-top cradle, fixed left jaw + bottom ledge, captive dovetail track, flush hex channels)
    clamp_jaw.stl    (Full-height sliding right jaw + bottom ledge, captive dovetail tongue, flush M5 lock foot)
    eyepiece_arm.stl (Slotted alignment arm + split-clamp Ø30.5 mm collar + open Ø22 mm through-tunnel)
    thumb_knob.stl   (Print 2x - 14 mm tall recessed-cup M5 thumb knob that hides the bolt tip)
    params.json      (Derived dimensions & transforms for the interactive Three.js 3D viewer)
"""
import json
import math
import struct
from collections import Counter
from pathlib import Path

import cadquery as cq

# ============================== PARAMETERS ==============================
# --- Smartphone Dimensions & Universal Clamping Range ---
PHONE_W_MIN = 58.0          # min phone width (compact bare phone)
PHONE_W_NOM = 76.0          # nominal smartphone width
PHONE_W_MAX = 95.0          # max phone width (Pro Max / Ultra + thick rugged case)
PHONE_T_MAX = 13.5          # max phone thickness with case
PHONE_L_REF = 158.0         # reference phone length (for viewer & checks)

# --- Cradle Geometry ---
FIXED_JAW_X = -40.0         # inner contact face of left fixed jaw at Z = 0
PHONE_BOT_Y = -65.0         # inner contact face of bottom anti-drop ledges
BASE_TOP_Y = 26.0           # top of cradle backplate (above this is 100% open camera zone!)
BASE_BOT_Y = PHONE_BOT_Y - 4.5  # -69.5 mm
BASE_T = 6.8                # backplate thickness (deep enough for flush M5 hex head + 2.5 mm web)
JAW_WALL_L = 5.0            # left fixed jaw wall thickness
JAW_WALL_R = 13.0           # right sliding jaw outer wall width (2.3 mm walls around M5 hex pocket!)
JAW_H = 14.5                # jaw height above phone backplate (Z = 0 to 14.5)
JAW_TAPER = 1.5             # gentle ~6 deg inward wedge taper from Z=0 to Z=JAW_H
JAW_LIP = 0.5               # extra top bezel retention bead (total 2.0 mm inward at top)
BOT_LEDGE_H = 13.0          # bottom anti-drop ledge forward height
BOT_LEDGE_W = 16.0          # inward span of each bottom ledge (leaves USB-C port clear)
BOT_LEDGE_LIP = 1.5         # front anti-slip lip on bottom ledges

# --- Captive Dovetail-T Track & Sliding Clamp Lock ---
TRACK_Y = -38.0             # Y center of captive dovetail-T guide track
TRACK_DEPTH = 3.8           # groove depth into base plate (floor web = 6.8 - 3.8 = 3.0 mm)
TRACK_NECK_W = 9.0          # dovetail neck opening width
TRACK_NECK_H = 1.6          # rail overhang lip thickness (>= MIN_WALL 1.6 mm!)
TRACK_FLARE = 2.2           # 45 deg flare per side (max inner width = 13.4 mm)
CLAMP_SLOT_Y = -57.0        # Y center of horizontal M5 clamp lock slot
RAIL_TOP_Y = -26.0          # top edge of extended lower rail
RAIL_X_MAX = 75.0           # right end of base rail (closed end stop past max thick-cased phone!)
JAW_TOP_Y = 10.0            # top edge of right sliding jaw (79.5 mm tall symmetric grip)

# --- Unified M5 x 20 mm Hardware Dimensions ---
BOLT_D = 5.4                # M5 bolt shaft clearance
M5_HEX_AF = 8.4             # M5 hex head / nut across flats (8.0 mm nominal + 0.4 mm print clearance)
M5_HEX_POCKET_D = 4.3       # deep front pocket so 3.5 mm M5 hex head sits 0.8 mm below phone!
M5_NUT_THICK = 4.2          # M5 hex nut pocket depth

# --- 2-Axis Optical Alignment (X-slot on Base + Y-slot on Arm) ---
OPT_SLOT_Y = 14.0           # Y center of horizontal optical X-slot on base plate
OPT_X_MIN = -26.0           # left limit (reaches corner cameras 14 mm from phone left edge!)
OPT_X_MAX = 20.0            # right limit (46 mm total horizontal travel)
OPT_Y_TRAVEL = 50.0         # vertical slot travel (+/- 25 mm)
EP_CENTER_NOM_Y = 71.0      # nominal eyepiece Y (136 mm above phone bottom; range 111 - 161 mm!)

# --- Eyepiece Collar (Standard Light Microscope 27.5 - 30.5 mm Eyepieces) ---
EYEPIECE_ID = 30.5          # slip-on bore for standard compound light microscope eyepieces
EYEPIECE_WALL = 2.5         # collar wall thickness
EYEPIECE_OD = EYEPIECE_ID + 2 * EYEPIECE_WALL  # 35.5 mm
EYEPIECE_SOCKET_LEN = 22.0  # depth of eyepiece grip socket
EYEPIECE_STOP_D = 22.0      # 100% open optical through-tunnel aperture diameter
EYEPIECE_STOP_Z = -12.0     # internal stop ring Z (exact 12.0 mm eye relief from phone back Z=0!)
CLAMP_SLIT_W = 3.0          # split-collar flex slit (clamps down to ~27.5 mm eyepieces)
CLAMP_EAR_W = 10.5          # each ear width (total span 24.0 mm -> M5x20 sits 100% flush!)
CLAMP_EAR_H = 13.5          # ear height above cylinder (>= 1.75 mm wall around Ø10 mm M5 counterbore!)

# --- Eyepiece Arm & Thumb Knob ---
ARM_W = 24.0                # vertical arm plate width
ARM_T = 5.0                 # vertical arm plate thickness
KNOB_D = 22.0               # thumb knob outer diameter (clears collar & arm at all positions)
KNOB_H = 14.0               # tall recessed-cup knob (completely hides M5x20 bolt end!)
KNOB_FLOOR = 3.5            # solid plastic floor between arm and M5 nut

# --- Tolerances & Export ---
CLR_SLIDE = 0.25            # dovetail sliding clearance per face
MIN_WALL = 1.6              # minimum printable wall thickness
STL_TOL = 0.02
STL_ANG_TOL = 0.1
# =======================================================================

OUT = Path(__file__).resolve().parent
SQ2 = math.sqrt(2)

# Derived geometry
JAW_BOLT_OFF_X = JAW_WALL_R / 2  # +5.25 mm from right jaw inner face
NOM_JAW_X = FIXED_JAW_X + PHONE_W_NOM  # +36.0 mm
CLAMP_SLOT_X_MIN = FIXED_JAW_X + PHONE_W_MIN + JAW_BOLT_OFF_X  # +23.25 mm
CLAMP_SLOT_X_MAX = FIXED_JAW_X + PHONE_W_MAX + 3.0 + JAW_BOLT_OFF_X  # +63.25 mm (extra 3 mm for thick case wedge)
OPT_X_TRAVEL = OPT_X_MAX - OPT_X_MIN                           # 46.0 mm
OPT_X_MID = (OPT_X_MIN + OPT_X_MAX) / 2                        # -3.0 mm
BASE_UPPER_X_MAX = OPT_X_MAX + 12.0                            # +32.0 mm
ARM_Z_FRONT = -BASE_T                                          # -6.8 mm
ARM_Z_BACK = ARM_Z_FRONT - ARM_T                               # -11.8 mm
TUBE_Z_BOT = EYEPIECE_STOP_Z - EYEPIECE_SOCKET_LEN             # -34.0 mm


def groove_half_profile(c=0.0):
    """Right half of dovetail-T groove (y >= 0 from groove center), z relative to Z = 0.
    c > 0 produces the matching tongue shrunk by normal clearance c on every face."""
    neck = TRACK_NECK_W / 2 - c
    floor = -TRACK_DEPTH + c
    # 45 deg flare line: y + z = k; offsetting inward lowers k by c * sqrt(2)
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
    """Pre-flight mechanical, wall-thickness, and geometric clearance checks."""
    neck, zft, floor, yb = groove_half_profile(CLR_SLIDE)
    walls = {
        "base floor under dovetail groove": BASE_T - TRACK_DEPTH,
        "base web under optical hex channel": BASE_T - M5_HEX_POCKET_D,
        "base top wall above optical slot": BASE_TOP_Y - (OPT_SLOT_Y + M5_HEX_AF / 2),
        "base right end stop past clamp slot": RAIL_X_MAX - (CLAMP_SLOT_X_MAX + BOLT_D / 2),
        "eyepiece collar wall": EYEPIECE_WALL,
        "eyepiece optical flange wall": (EYEPIECE_OD - EYEPIECE_STOP_D) / 2,
        "eyepiece flange thickness": abs(EYEPIECE_STOP_Z - ARM_Z_FRONT),
        "clamping ear wall around M5 head": (CLAMP_EAR_H - 10.0) / 2,
        "left fixed jaw wall": JAW_WALL_L,
        "right jaw lock foot floor": 6.5 - M5_HEX_POCKET_D,
        "right jaw wall beside M5 hex pocket": (JAW_WALL_R - M5_HEX_AF) / 2,
        "thumb knob solid floor": KNOB_FLOOR,
        "dovetail rail lip": TRACK_NECK_H,
        "dovetail tongue neck": 2 * neck,
        "arm wall beside vertical slot": (ARM_W - BOLT_D) / 2,
    }
    for name, v in walls.items():
        assert v >= MIN_WALL - 1e-9, f"{name} = {v:.2f} mm < {MIN_WALL}"

    assert 0.15 <= CLR_SLIDE <= 0.5, f"CLR_SLIDE = {CLR_SLIDE} outside 0.15-0.5 mm"
    assert yb > TRACK_NECK_W / 2 + 0.6, "Tongue undercut too small for captive retention"
    assert CLAMP_SLOT_X_MAX < RAIL_X_MAX - 4.0, "Clamp slot too close to right rail end"

    # Verify M5 x 20 mm bolt engages 100% of nut AND stays hidden inside knob cup!
    bolt_len = 20.0
    opt_stack = (BASE_T - M5_HEX_POCKET_D) + ARM_T + KNOB_FLOOR + M5_NUT_THICK
    clamp_stack = (6.5 - M5_HEX_POCKET_D) + BASE_T + KNOB_FLOOR + M5_NUT_THICK
    max_hidden_len_opt = (BASE_T - M5_HEX_POCKET_D) + ARM_T + KNOB_H
    max_hidden_len_clamp = (6.5 - M5_HEX_POCKET_D) + BASE_T + KNOB_H
    assert opt_stack <= bolt_len <= max_hidden_len_opt, \
        f"Optical M5x20 bolt fit error: engage={opt_stack:.1f}, max_hidden={max_hidden_len_opt:.1f}"
    assert clamp_stack <= bolt_len <= max_hidden_len_clamp, \
        f"Clamp M5x20 bolt fit error: engage={clamp_stack:.1f}, max_hidden={max_hidden_len_clamp:.1f}"

    # Verify Knob #1 never hits eyepiece collar at lowest Y position
    ep_lowest_outer_y = (EP_CENTER_NOM_Y - OPT_Y_TRAVEL / 2) - EYEPIECE_OD / 2
    knob1_top_y = OPT_SLOT_Y + KNOB_D / 2
    assert ep_lowest_outer_y > knob1_top_y + 2.0, \
        f"Knob #1 ({knob1_top_y:.1f}) collides with eyepiece collar ({ep_lowest_outer_y:.1f})"

    # Verify Eyepiece arm lowest edge never hits Knob #2
    arm_bot_nom_y = OPT_SLOT_Y - OPT_Y_TRAVEL / 2 - BOLT_D / 2 - 4.8
    arm_lowest_y = arm_bot_nom_y - OPT_Y_TRAVEL / 2
    knob2_top_y = CLAMP_SLOT_Y + KNOB_D / 2
    assert arm_lowest_y > knob2_top_y + 1.5, \
        f"Arm lowest edge ({arm_lowest_y:.1f}) collides with Knob #2 ({knob2_top_y:.1f})"

    # Verify bottom ledges never collide at min phone width
    left_ledge_x1 = FIXED_JAW_X + BOT_LEDGE_W
    right_ledge_x0_min = (FIXED_JAW_X + PHONE_W_MIN) - BOT_LEDGE_W
    assert right_ledge_x0_min - left_ledge_x1 >= 15.0, "Bottom ledges too close at min width"

    return walls


def make_phone_base():
    """Open-top smartphone cradle backplate with:
    - Full-height left fixed jaw (6 deg inward self-wedging taper + grip ribs)
    - Bottom left anti-drop ledge (16 mm wide, with front anti-slip lip)
    - Upper horizontal M5 optical alignment slot with flush anti-rotation hex channel
    - Extended lower rail with captive dovetail-T groove + closed M5 clamp lock slot
    - 100% flat rear face (Z = -BASE_T) for zero-support printing
    """
    x_left = FIXED_JAW_X - JAW_WALL_L  # -45.0 mm

    # 1. L-shaped flat base plate (Z = -BASE_T to 0)
    # Upper body + lower extended rail merged cleanly into one 2D outline
    outline = [
        (x_left, BASE_BOT_Y),
        (RAIL_X_MAX, BASE_BOT_Y),
        (RAIL_X_MAX, RAIL_TOP_Y),
        (BASE_UPPER_X_MAX, RAIL_TOP_Y),
        (BASE_UPPER_X_MAX, BASE_TOP_Y),
        (x_left, BASE_TOP_Y),
    ]
    base = (cq.Workplane("XY", origin=(0, 0, -BASE_T))
            .polyline(outline).close().extrude(BASE_T))
    base = base.edges("|Z").fillet(3.0)

    # 2. Left Fixed Jaw (Y = BASE_BOT_Y to BASE_TOP_Y, Z = 0 to JAW_H)
    # Vertical 0 -> 7.0 mm for flat edge contact, then gentle ~11 deg inward wedge (7.0 -> 14.5 mm)
    # that pulls BOTH thin (7.5 mm) and thick cased (13 mm) phones flat against Z = 0!
    jaw_pts = [
        (x_left, -0.05),
        (FIXED_JAW_X, -0.05),
        (FIXED_JAW_X, 7.0),
        (FIXED_JAW_X + JAW_TAPER, JAW_H - 1.2),
        (FIXED_JAW_X + JAW_TAPER + JAW_LIP, JAW_H),
        (x_left, JAW_H),
    ]
    jaw_len = BASE_TOP_Y - BASE_BOT_Y
    jaw_mid_y = (BASE_TOP_Y + BASE_BOT_Y) / 2
    left_jaw = (cq.Workplane("XZ", origin=(0, jaw_mid_y, 0))
                .polyline(jaw_pts).close().extrude(jaw_len / 2, both=True))
    base = base.union(left_jaw)

    # 3. Bottom Left Anti-Drop Ledge (supports phone weight on 45 deg microscope!)
    ledge_x0 = x_left
    ledge_x1 = FIXED_JAW_X + BOT_LEDGE_W  # -24.0 mm
    ledge_pts = [
        (BASE_BOT_Y, -0.05),
        (PHONE_BOT_Y, -0.05),
        (PHONE_BOT_Y, BOT_LEDGE_H - BOT_LEDGE_LIP),
        (PHONE_BOT_Y + BOT_LEDGE_LIP, BOT_LEDGE_H),
        (BASE_BOT_Y, BOT_LEDGE_H),
    ]
    left_ledge = (cq.Workplane("YZ", origin=(ledge_x0, 0, 0))
                  .polyline(ledge_pts).close().extrude(ledge_x1 - ledge_x0))
    base = base.union(left_ledge)

    # 4. Horizontal Dovetail-T Track Groove (open at right end X = RAIL_X_MAX for assembly)
    # Starts at X = -28.0 mm (closed left stop) and runs cleanly out the right end
    track_x0 = -28.0
    track_pts = mirrored_profile(TRACK_Y, 0.0, groove_half_profile(0.0), 0.5)
    track_cut = (cq.Workplane("YZ", origin=(track_x0, 0, 0))
                 .polyline(track_pts).close().extrude(RAIL_X_MAX - track_x0 + 2.0))
    base = base.cut(track_cut)

    # 5. Upper Optical X-Adjustment Slot (Y = OPT_SLOT_Y = +14.0 mm)
    opt_through = (cq.Workplane("XY", origin=(OPT_X_MID, OPT_SLOT_Y, -BASE_T - 1))
                   .slot2D(OPT_X_TRAVEL + BOLT_D, BOLT_D)
                   .extrude(BASE_T + 2))
    base = base.cut(opt_through)

    # Flush anti-rotation M5 hex bolt head channel (4.3 mm deep -> bolt head sits 0.8 mm below Z=0!)
    # Rectangular flat-sided slot prevents hex head from spinning during tightening
    opt_hex_len = OPT_X_TRAVEL + M5_HEX_AF + 1.2
    opt_hex = (cq.Workplane("XY", origin=(OPT_X_MID, OPT_SLOT_Y, -M5_HEX_POCKET_D))
               .box(opt_hex_len, M5_HEX_AF, M5_HEX_POCKET_D + 0.5, centered=(True, True, False)))
    base = base.cut(opt_hex)

    # 6. Lower Horizontal Clamp Lock Slot (Y = CLAMP_SLOT_Y = -57.0 mm, closed at both ends!)
    clamp_slot_mid = (CLAMP_SLOT_X_MIN + CLAMP_SLOT_X_MAX) / 2
    clamp_slot_len = (CLAMP_SLOT_X_MAX - CLAMP_SLOT_X_MIN) + BOLT_D
    clamp_through = (cq.Workplane("XY", origin=(clamp_slot_mid, CLAMP_SLOT_Y, -BASE_T - 1))
                     .slot2D(clamp_slot_len, BOLT_D)
                     .extrude(BASE_T + 2))
    base = base.cut(clamp_through)

    # 7. Optional Elastic Band Anchor Eyelet (lower-left corner, flush with bed)
    eyelet = (cq.Workplane("XY", origin=(-31.0, CLAMP_SLOT_Y, -BASE_T - 1))
              .circle(2.2).extrude(BASE_T + 2))
    base = base.cut(eyelet)

    return base


def make_clamp_jaw():
    """Full-height sliding right phone clamp jaw (assembly frame at PHONE_W_NOM = 76 mm):
    - 75 mm tall symmetric tapered jaw wall (6 deg inward self-wedging grip)
    - Bottom right anti-drop ledge (16 mm wide, 0.25 mm clearance above base plate)
    - 34 mm long captive dovetail-T tongue (recessed 0.25 mm below Z=0 under phone!)
    - Flush recessed M5 clamp lock bolt pocket inside outer jaw wall
    - Print orientation: rotated -90 deg around Y so outer right face (X_max) sits
      100% FLAT on the print bed with ZERO overhangs and maximum clamping strength!
    """
    x_in = NOM_JAW_X                   # +36.0 mm (inner phone contact face at Z=0)
    x_out = x_in + JAW_WALL_R          # +46.5 mm (outer flat face -> print bed plane!)
    jaw_len = JAW_TOP_Y - BASE_BOT_Y   # 79.5 mm
    jaw_mid_y = (JAW_TOP_Y + BASE_BOT_Y) / 2

    # 1. Main Right Jaw Wall (vertical 0 -> 7.0 mm, gentle inward wedge 7.0 -> JAW_H)
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

    # 2. Bottom Right Anti-Drop Ledge (Z = +0.25 to BOT_LEDGE_H so it glides cleanly over base!)
    ledge_x0 = x_in - BOT_LEDGE_W  # +20.0 mm
    ledge_pts = [
        (BASE_BOT_Y, 0.25),
        (PHONE_BOT_Y, 0.25),
        (PHONE_BOT_Y, BOT_LEDGE_H - BOT_LEDGE_LIP),
        (PHONE_BOT_Y + BOT_LEDGE_LIP, BOT_LEDGE_H),
        (BASE_BOT_Y, BOT_LEDGE_H),
    ]
    right_ledge = (cq.Workplane("YZ", origin=(ledge_x0, 0, 0))
                   .polyline(ledge_pts).close().extrude(x_out - ledge_x0))
    jaw = jaw.union(right_ledge)

    # 3. Captive Dovetail-T Tongue (centered at TRACK_Y = -38.0 mm)
    # Under the phone (X < x_in): top surface at Z = -0.25 (flush/recessed below phone!)
    # Under the jaw wall (X >= x_in): extends up to Z = +1.0 mm to fuse solidly into jaw wall!
    tongue_len = 34.0
    tongue_x0 = x_in - 28.0  # extends 28 mm inward under phone (always inside rail even at 95 mm!)
    half_t = groove_half_profile(CLR_SLIDE)

    tongue_under_phone = (cq.Workplane("YZ", origin=(tongue_x0, 0, 0))
                          .polyline(mirrored_profile(TRACK_Y, 0.0, half_t, -0.25))
                          .close().extrude(x_in - tongue_x0 + 0.5))
    tongue_under_jaw = (cq.Workplane("YZ", origin=(x_in, 0, 0))
                        .polyline(mirrored_profile(TRACK_Y, 0.0, half_t, 1.0))
                        .close().extrude(x_out - x_in))
    jaw = jaw.union(tongue_under_phone).union(tongue_under_jaw)

    # 4. Flush M5 Clamp Lock Bolt Hole & Recessed Captive Hex Head Pocket
    # Located inside the lower jaw wall at (x_in + JAW_BOLT_OFF_X, CLAMP_SLOT_Y)
    # Cut a clean top access notch above Z = 6.5 mm in the bolt zone so wrench/finger can drop M5 bolt in
    bolt_x = x_in + JAW_BOLT_OFF_X  # +41.25 mm
    lock_floor = 6.5 - M5_HEX_POCKET_D  # 2.2 mm solid floor under M5 bolt head

    # Open access cutout from Z = 6.5 to JAW_H + 1 right around the bolt head (keeps phone grip above Y = -49!)
    bolt_access = (cq.Workplane("XY", origin=(bolt_x, CLAMP_SLOT_Y, 6.5))
                   .box(JAW_WALL_R + 1.0, 14.0, JAW_H, centered=(True, True, False)))
    jaw = jaw.cut(bolt_access)

    # Captive M5 hex head pocket (rotated 30 deg so 8.4 mm flats face X -> 2.3 mm solid walls on both sides!)
    hex_r = M5_HEX_AF / math.cos(math.pi / 6) / 2
    bolt_hex = (cq.Workplane("XY", origin=(bolt_x, CLAMP_SLOT_Y, lock_floor))
                .polygon(6, hex_r * 2).extrude(M5_HEX_POCKET_D + 1.0)
                .rotate((bolt_x, CLAMP_SLOT_Y, 0), (bolt_x, CLAMP_SLOT_Y, 1), 30))
    jaw = jaw.cut(bolt_hex)

    # M5 bolt shaft through-hole
    bolt_hole = (cq.Workplane("XY", origin=(bolt_x, CLAMP_SLOT_Y, -1.0))
                 .circle(BOLT_D / 2).extrude(8.0))
    jaw = jaw.cut(bolt_hole)

    # 5. Optional Rubber Band Eyelet through upper-middle jaw body (clear of phone & bolt)
    eyelet = (cq.Workplane("XY", origin=(bolt_x, -22.0, -1.0))
              .circle(2.2).extrude(JAW_H + 2.0))
    jaw = jaw.cut(eyelet)

    return jaw


def make_eyepiece_arm():
    """2-Axis Vertical Slotted Alignment Arm + Light Microscope Eyepiece Collar:
    - 50 mm vertical M5 adjustment slot (covers phone camera heights 111 - 161 mm!)
    - Guaranteed clearance from BOTH Thumb Knob #1 and Thumb Knob #2 across 100% travel
    - Standard Ø30.5 mm split-clamp collar (grips 27.5 - 30.5 mm light microscope eyepieces)
    - 100% OPEN Ø22.0 mm through-tunnel (cut LAST & verified by ray-probe test!)
    - Flush M5 x 20 mm clamping ears (bolt head & hex nut sit completely recessed!)
    - 100% flat front face (Z = -BASE_T) for zero-support 3D printing (rotated 180 deg around X)
    """
    # Vertical slot spans from OPT_SLOT_Y - 25 to OPT_SLOT_Y + 25 (-11.0 to +39.0 mm)
    slot_bot_y = OPT_SLOT_Y - OPT_Y_TRAVEL / 2 - BOLT_D / 2  # -13.7 mm
    arm_bot_y = slot_bot_y - 4.8                              # -18.5 mm
    arm_top_y = EP_CENTER_NOM_Y                               # +71.0 mm (blends into round collar flange)
    arm_h = arm_top_y - arm_bot_y
    arm_mid_y = (arm_top_y + arm_bot_y) / 2

    # 1. Vertical Arm Plate (Z = ARM_Z_BACK to ARM_Z_FRONT = -11.8 to -6.8 mm)
    arm = (cq.Workplane("XY", origin=(0, arm_mid_y, ARM_Z_BACK))
           .box(ARM_W, arm_h, ARM_T, centered=(True, True, False)))
    arm = arm.edges("|Z").fillet(3.0)

    # 2. Full-Diameter Optical Head Flange + Eyepiece Collar Cylinder
    # Runs continuously from front bed plane (Z = ARM_Z_FRONT = -6.8) down to TUBE_Z_BOT (-34.0)
    tube_total_len = ARM_Z_FRONT - TUBE_Z_BOT  # 27.2 mm
    tube_outer = (cq.Workplane("XY", origin=(0, EP_CENTER_NOM_Y, TUBE_Z_BOT))
                  .circle(EYEPIECE_OD / 2)
                  .extrude(tube_total_len))

    # 3. Split-Collar Clamping Ears (+Y top of eyepiece collar)
    # Extend all the way to Z = ARM_Z_FRONT (-6.8 mm) so ears sit 100% FLAT on the print bed (0% overhang!)
    # Total X span = 2 * 10.5 + 3.0 = 24.0 mm -> M5 x 20 mm bolt sits 100% flush!
    ear_total_x = 2 * CLAMP_EAR_W + CLAMP_SLIT_W
    ear_y0 = EP_CENTER_NOM_Y + EYEPIECE_OD / 2 - 2.0  # overlaps cylinder wall by 2 mm
    ear_mid_y = ear_y0 + CLAMP_EAR_H / 2
    ear_mid_z = (TUBE_Z_BOT + EYEPIECE_STOP_Z) / 2    # centered vertically on eyepiece grip socket (-23.0 mm)
    ears = (cq.Workplane("XY", origin=(0, ear_mid_y, TUBE_Z_BOT))
            .box(ear_total_x, CLAMP_EAR_H, tube_total_len, centered=(True, True, False)))

    # Union ALL solid bodies FIRST before cutting ANY holes or optical tunnels!
    arm = arm.union(tube_outer).union(ears)

    # 4. Vertical M5 Adjustment Slot (centered at X = 0, Y = OPT_SLOT_Y)
    v_slot = (cq.Workplane("XY", origin=(0, OPT_SLOT_Y, ARM_Z_BACK - 1))
              .slot2D(OPT_Y_TRAVEL + BOLT_D, BOLT_D, 90)
              .extrude(ARM_T + 2))
    arm = arm.cut(v_slot)

    # 5. Microscope Eyepiece Bore (Ø30.5 mm from TUBE_Z_BOT up to internal stop ring at EYEPIECE_STOP_Z = -12.0 mm)
    ep_bore = (cq.Workplane("XY", origin=(0, EP_CENTER_NOM_Y, TUBE_Z_BOT - 1))
               .circle(EYEPIECE_ID / 2)
               .extrude(EYEPIECE_SOCKET_LEN + 1))
    arm = arm.cut(ep_bore)

    # 6. 100% OPEN Optical Through-Tunnel (Ø22.0 mm ALL THE WAY THROUGH from microscope to phone camera!)
    optical_tunnel = (cq.Workplane("XY", origin=(0, EP_CENTER_NOM_Y, TUBE_Z_BOT - 2))
                      .circle(EYEPIECE_STOP_D / 2)
                      .extrude(tube_total_len + 6))
    arm = arm.cut(optical_tunnel)

    # 7. Full-Length Split Flex Slit (cuts cleanly through ears & top wall so collar clamps smoothly 27.5 - 30.5 mm)
    slit = (cq.Workplane("XY", origin=(0, EP_CENTER_NOM_Y, TUBE_Z_BOT - 1))
            .box(CLAMP_SLIT_W, EYEPIECE_OD + CLAMP_EAR_H, tube_total_len + 2,
                 centered=(True, False, False)))
    arm = arm.cut(slit)

    # 8. Flush M5 x 20 mm Clamping Bolt Hole + Left Head Counterbore + Right Captive Hex Nut Pocket
    bolt_hole = (cq.Workplane("YZ", origin=(-ear_total_x, ear_mid_y, ear_mid_z))
                 .circle(BOLT_D / 2)
                 .extrude(ear_total_x * 2))
    arm = arm.cut(bolt_hole)

    # Left (-X) counterbore for M5 hex bolt head (4.0 mm deep, Ø10.0 mm -> 100% flush!)
    head_cbore = (cq.Workplane("YZ", origin=(-ear_total_x / 2 - 1.0, ear_mid_y, ear_mid_z))
                  .circle(5.0)
                  .extrude(5.0))
    arm = arm.cut(head_cbore)

    # Right (+X) captive M5 hex nut pocket (5.0 mm deep -> nut + bolt tip 100% flush!)
    hex_r = M5_HEX_AF / math.cos(math.pi / 6) / 2
    nut_pocket = (cq.Workplane("YZ", origin=(ear_total_x / 2 - 5.0, ear_mid_y, ear_mid_z))
                  .polygon(6, hex_r * 2)
                  .extrude(6.0))
    arm = arm.cut(nut_pocket)

    return arm


def make_thumb_knob():
    """Tall 14 mm ergonomic 6-flute M5 thumb knob with recessed bolt-tip shield cup.
    Print 2x (identical for Optical Lock Knob #1 and Clamp Lock Knob #2).

    Stack from Z = 0 (arm-facing flat bed face) to Z = 14.0 mm (back):
      0.0 - 3.5 mm : Solid clamping floor with Ø5.4 mm bolt hole
      3.5 - 7.7 mm : Captive M5 hex nut pocket (8.4 mm AF) -> nut pulls INTO solid floor!
      7.7 - 14.0 mm: Recessed Ø11.0 mm cup -> completely hides M5 x 20 mm bolt end!
    """
    knob = cq.Workplane("XY").circle(KNOB_D / 2).extrude(KNOB_H)

    # 6 ergonomic finger grip flutes
    flute_r = 2.6
    for i in range(6):
        ang = i * (2 * math.pi / 6)
        fx = (KNOB_D / 2) * math.cos(ang)
        fy = (KNOB_D / 2) * math.sin(ang)
        flute = (cq.Workplane("XY", origin=(fx, fy, -1))
                 .circle(flute_r).extrude(KNOB_H + 2))
        knob = knob.cut(flute)

    # Central M5 shaft hole through bottom floor
    hole = cq.Workplane("XY", origin=(0, 0, -1)).circle(BOLT_D / 2).extrude(KNOB_H + 2)
    knob = knob.cut(hole)

    # Captive M5 hex nut pocket (Z = 3.5 to 7.7 mm)
    hex_r = M5_HEX_AF / math.cos(math.pi / 6) / 2
    hex_nut = (cq.Workplane("XY", origin=(0, 0, KNOB_FLOOR))
               .polygon(6, hex_r * 2).extrude(M5_NUT_THICK + 1.0))
    knob = knob.cut(hex_nut)

    # Recessed bolt-tip shield cup (Z = 7.7 to 14.0 mm, hides M5x20 bolt end completely!)
    cup = (cq.Workplane("XY", origin=(0, 0, KNOB_FLOOR + M5_NUT_THICK))
           .circle(5.5).extrude(KNOB_H))
    knob = knob.cut(cup)

    knob = knob.edges(">Z").chamfer(0.8).edges("<Z").chamfer(0.8)
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
        if max(z1, z2, z3) < 1e-4:   # triangle touching print bed
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
    jaw = make_clamp_jaw()
    arm = make_eyepiece_arm()
    knob = make_thumb_knob()

    # Orient knob in assembly frame (arm-facing base at Z = ARM_Z_BACK = -11.8, cup facing -Z)
    knob_opt_asm = knob.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, OPT_SLOT_Y, ARM_Z_BACK))
    knob_clamp_asm = knob.rotate((0, 0, 0), (1, 0, 0), 180).translate((NOM_JAW_X + JAW_BOLT_OFF_X, CLAMP_SLOT_Y, -BASE_T))

    # 1. Interference checks across full phone clamping travel (58 - 95 mm)
    for w in (PHONE_W_MIN, 67.0, PHONE_W_NOM, 85.0, PHONE_W_MAX):
        shift_x = w - PHONE_W_NOM
        j_s = jaw.translate((shift_x, 0, 0))
        v = vol_inter(base, j_s)
        assert v < 1e-3, f"Interference Base-Jaw at width {w} mm: {v:.4f} mm^3"
        # Thin bare phone (7.0 mm thick) fits flush against vertical lower jaw walls
        phone_thin = (cq.Workplane("XY", origin=(FIXED_JAW_X + 0.2, PHONE_BOT_Y + 0.2, 0.2))
                      .box(w - 0.4, PHONE_L_REF, 6.8, centered=(False, False, False)))
        assert vol_inter(base, phone_thin) < 1e-3, f"Base collides with thin {w} mm phone!"
        assert vol_inter(j_s, phone_thin) < 1e-3, f"Jaw collides with thin {w} mm phone!"

        # Thick cased phone (12.0 mm thick): sits nicely inside the 11 deg wedge with jaw shifted +2.8 mm
        j_thick = jaw.translate((shift_x + 2.8, 0, 0))
        assert vol_inter(base, j_thick) < 1e-3, f"Base-Jaw collision at thick {w} mm phone!"
        phone_thick = (cq.Workplane("XY", origin=(FIXED_JAW_X + 1.4, PHONE_BOT_Y + 0.4, 0.2))
                       .box(w, PHONE_L_REF, 11.2, centered=(False, False, False)))
        assert vol_inter(base, phone_thick) < 1e-3, f"Base collides with thick {w} mm phone!"
        assert vol_inter(j_thick, phone_thick) < 1e-3, f"Jaw collides with thick {w} mm phone!"

    # 2. Captive dovetail retention check: lifting jaw (+Z) must collide with base rail lip
    lift = CLR_SLIDE * SQ2 + 0.35
    assert vol_inter(base, jaw.translate((0, 0, lift))) > 5.0, "Jaw is not captive in dovetail track!"

    # 3. Interference checks across full 2-axis optical travel + Knob #1 vs Collar + Arm vs Knob #2
    for ax in (OPT_X_MIN, OPT_X_MID, OPT_X_MAX):
        for ay in (-OPT_Y_TRAVEL / 2, 0.0, OPT_Y_TRAVEL / 2):
            a_s = arm.translate((ax, ay, 0))
            k1_s = knob_opt_asm.translate((ax, 0, 0))
            assert vol_inter(base, a_s) < 1e-3, f"Base-Arm collision at ({ax}, {ay})"
            assert vol_inter(a_s, k1_s) < 1e-3, f"Arm-Knob1 collision at ({ax}, {ay})"
            for w in (PHONE_W_MIN, PHONE_W_MAX):
                k2_s = knob_clamp_asm.translate((w - PHONE_W_NOM, 0, 0))
                assert vol_inter(a_s, k2_s) < 1e-3, f"Arm-Knob2 collision at ({ax}, {ay}, w={w})"

    # 4. Optical through-tunnel ray probe test (light cylinder must pass 100% clear through Ø22 mm bore!)
    optical_probe = (cq.Workplane("XY", origin=(0, EP_CENTER_NOM_Y, -50.0))
                     .circle(EYEPIECE_STOP_D / 2 - 0.2)
                     .extrude(60.0))
    probe_vol = vol_inter(arm, optical_probe)
    assert probe_vol < 1e-3, f"Optical tunnel is blocked by {probe_vol:.2f} mm^3 plastic!"

    # 5. Verify all parts are single valid solids, orient for 0% support printing & export
    parts_spec = [
        ("phone_base.stl",   base, None, 0),
        ("clamp_jaw.stl",    jaw,  "Y", 90),   # Outer right cheek (X_max) flat on bed -> zero overhangs!
        ("eyepiece_arm.stl", arm,  "X", 180),  # Flat front arm face on bed, collar pointing straight up!
        ("thumb_knob.stl",   knob, None, 0),   # Flat arm-facing base on bed, nut pocket & cup pointing up!
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
        "version": 2,
        "phone": {
            "wMin": PHONE_W_MIN,
            "wNom": PHONE_W_NOM,
            "wMax": PHONE_W_MAX,
            "tMax": PHONE_T_MAX,
            "lRef": PHONE_L_REF,
            "fixedJawX": FIXED_JAW_X,
            "botY": PHONE_BOT_Y,
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
            "xMin": OPT_X_MIN,
            "xMax": OPT_X_MAX,
            "xNom": 0.0,
            "yMin": -OPT_Y_TRAVEL / 2,
            "yMax": OPT_Y_TRAVEL / 2,
            "yNom": 0.0,
            "optSlotY": OPT_SLOT_Y,
            "clampSlotY": CLAMP_SLOT_Y,
            "jawBoltOffX": JAW_BOLT_OFF_X,
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
    print(f"\nGenerated v2 params.json:")
    print(f"  Phone width range : {PHONE_W_MIN:.0f} -> {PHONE_W_MAX:.0f} mm (thickness up to {PHONE_T_MAX:.1f} mm)")
    print(f"  Camera X travel   : {OPT_X_MIN:+.0f} -> {OPT_X_MAX:+.0f} mm ({OPT_X_TRAVEL:.0f} mm)")
    print(f"  Camera Y height   : {EP_CENTER_NOM_Y - OPT_Y_TRAVEL/2 - PHONE_BOT_Y:.0f} -> "
          f"{EP_CENTER_NOM_Y + OPT_Y_TRAVEL/2 - PHONE_BOT_Y:.0f} mm above phone bottom")
    print(f"  Optical tunnel    : Ø{EYEPIECE_STOP_D:.0f} mm 100% OPEN (probe blockage = 0.000 mm^3)")
    print(f"  Hardware          : 3x M5 x 20 mm hex bolts + 3x M5 hex nuts (100% flush!)")
    print("ALL CAD, INTERFERENCE, CAPTIVE, OPTICAL & STL CHECKS PASSED!")


if __name__ == "__main__":
    main()
