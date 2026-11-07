"""
Universal Smartphone Microscope Eyepiece Adapter - Parametric CadQuery Model.

All dimensions are in mm. Change parameters in PARAMETERS section, then run:
    py -3.14 adapter_model.py

Outputs:
    phone_base.stl (Base plate + fixed left jaw + camera window + sliding track)
    clamp_jaw.stl (Sliding right jaw + D-ring pull handle + dovetail tongue)
    eyepiece_arm.stl (Vertical slotted bracket + stepped 30mm eyepiece collar)
    thumb_knob.stl (Ergonomic M5 knurled thumb knob with hex nut pocket)
    params.json (Derived dimensions for Three.js interactive 3D viewer)
"""
import json
import math
import struct
from collections import Counter
from pathlib import Path

import cadquery as cq

# ============================== PARAMETERS ==============================
# --- Smartphone Dimensions & Clearances ---
PHONE_W_MIN = 60.0          # min phone width (e.g. compact phone / iPhone SE/mini)
PHONE_W_NOM = 74.0          # nominal smartphone width
PHONE_W_MAX = 92.0          # max phone width (large phone / rugged case)
PHONE_T_MAX = 13.0          # max phone thickness with case
PHONE_L_REF = 155.0         # nominal phone length (for reference & viewer)

# --- Eyepiece Collar (Microscope Side) ---
EYEPIECE_ID = 30.0          # internal diameter for standard 28.0 - 30.5 mm eyepieces
EYEPIECE_WALL = 2.4         # sleeve wall thickness
EYEPIECE_OD = EYEPIECE_ID + 2 * EYEPIECE_WALL  # 34.8 mm
EYEPIECE_LEN = 26.0         # length of eyepiece sleeve
EYEPIECE_STOP_D = 21.0      # internal aperture stop diameter
EYEPIECE_RELIEF = 12.0      # distance from phone camera face to eyepiece shoulder
CLAMP_SLIT_W = 2.0          # split-collar flex slit width
CLAMP_EAR_W = 6.5           # clamping ear width
CLAMP_EAR_H = 8.0           # clamping ear height
CLAMP_BOLT_D = 4.3          # M4 tightening bolt hole
CLAMP_NUT_AF = 7.2          # M4 hex nut across flats
CLAMP_NUT_D = 3.2           # M4 hex nut pocket depth

# --- 2-Axis Alignment Travel ---
ADJUST_X_TRAVEL = 32.0      # horizontal adjustment travel (+/- 16 mm from center)
ADJUST_Y_TRAVEL = 42.0      # vertical adjustment travel (42 mm slot length)
SLOT_BOLT_D = 5.4           # M5 bolt clearance
M5_HEX_AF = 8.2             # M5 hex nut / bolt head across flats
M5_HEX_DEPTH = 3.2          # M5 hex head pocket depth

# --- Base Plate ---
BASE_W = 72.0               # width of phone cradle backplate
BASE_H = 104.0              # height of phone cradle backplate
BASE_T = 5.2                # thickness of backplate
JAW_H = 14.0                # jaw height above phone backplate (Z=0 to Z=14)
JAW_LIP = 1.8               # inward phone retention lip overhang
JAW_WALL = 4.5              # jaw outer wall thickness

# --- Track & Tongue (Dovetail-T) ---
TRACK_Y = -24.0             # Y center of the horizontal clamp track
TRACK_H = 24.0              # track height in Y
TRACK_DEPTH = 3.2           # track groove depth into base backplate
TRACK_NECK_W = 10.0         # neck width of dovetail
TRACK_FLARE = 3.0           # 45 deg flare on each side (total width = 16.0 mm)

# --- Tolerances ---
CLR_SLIDE = 0.25            # sliding tongue clearance per side
MIN_WALL = 1.6              # minimum printable wall check
STL_TOL = 0.02
STL_ANG_TOL = 0.1
# =======================================================================

OUT = Path(__file__).resolve().parent
SQ2 = math.sqrt(2)
FIXED_JAW_X = -PHONE_W_NOM / 2  # -37.0 mm (inner contact face of left jaw)


def checks():
    """Verify wall thicknesses and printable tolerances before generation."""
    walls = {
        "base floor under dovetail track": BASE_T - TRACK_DEPTH,
        "eyepiece collar wall": EYEPIECE_WALL,
        "fixed jaw wall": JAW_WALL,
        "base plate thickness": BASE_T,
        "clamping ear thickness": CLAMP_EAR_W,
        "jaw retention lip": JAW_LIP,
    }
    for name, v in walls.items():
        assert v >= MIN_WALL - 1e-9, f"{name} = {v:.2f} mm < {MIN_WALL}"

    assert 0.15 <= CLR_SLIDE <= 0.6, f"CLR_SLIDE = {CLR_SLIDE} mm is outside printable range 0.15 - 0.6"
    assert PHONE_W_MAX > PHONE_W_MIN, "Invalid phone width range"
    assert ADJUST_X_TRAVEL >= 20.0, "X travel too small for camera alignment"
    assert ADJUST_Y_TRAVEL >= 25.0, "Y travel too small for camera alignment"
    assert EYEPIECE_ID >= 25.0, "Eyepiece diameter too small for standard microscopes"
    return walls


def make_phone_base():
    """Main phone cradle backplate with fixed left jaw, X-adjustment slot,
    camera window, and horizontal dovetail-T track for the sliding jaw.
    
    Origin: Z=0 is the front face where the phone back rests.
    Base plate extends from Z = -BASE_T to Z = 0.
    Rear face at Z = -BASE_T is 100% flat for bed adhesion.
    """
    jaw_x0 = FIXED_JAW_X - JAW_WALL  # -41.5 mm
    jaw_x1 = FIXED_JAW_X             # -37.0 mm
    plate_x_max = PHONE_W_NOM / 2    # +37.0 mm
    total_w = plate_x_max - jaw_x0   # 78.5 mm
    plate_center_x = (jaw_x0 + plate_x_max) / 2

    # 1. Base plate
    base = (cq.Workplane("XY", origin=(plate_center_x, 0, -BASE_T))
            .box(total_w, BASE_H, BASE_T, centered=(True, True, False)))
    base = base.edges("|Z").fillet(3.0)

    # 2. Left Fixed Jaw (stands in +Z from Z=0 to Z=JAW_H)
    jaw_center_x = (jaw_x0 + jaw_x1) / 2
    jaw_box = (cq.Workplane("XY", origin=(jaw_center_x, 0, -0.01))
               .box(JAW_WALL + 0.02, BASE_H - 12.0, JAW_H + 0.01, centered=(True, True, False)))

    # Inward retention lip at Z = JAW_H with 45 deg chamfer for support-free print
    lip_pts = [
        (jaw_x1, JAW_H - JAW_LIP),
        (jaw_x1 + JAW_LIP, JAW_H),
        (jaw_x0, JAW_H),
        (jaw_x0, JAW_H - JAW_LIP)
    ]
    lip = (cq.Workplane("XZ", origin=(0, 0, 0))
           .polyline(lip_pts).close().extrude((BASE_H - 12.0) / 2, both=True))
    base = base.union(jaw_box).union(lip)

    # 3. Camera Viewing Window (upper area)
    cam_win = (cq.Workplane("XY", origin=(0, 24.0, -BASE_T - 1))
               .box(40.0, 32.0, BASE_T + JAW_H + 2, centered=(True, True, False)))
    cam_win = cam_win.edges("|Z").fillet(3.0)
    base = base.cut(cam_win)

    # 4. Horizontal X-Adjustment Slot (for M5 lock bolt)
    slot_y = 0.0
    slot_len = ADJUST_X_TRAVEL
    slot_through = (cq.Workplane("XY", origin=(0, slot_y, -BASE_T - 1))
                    .slot2D(slot_len, SLOT_BOLT_D)
                    .extrude(BASE_T + 2))
    base = base.cut(slot_through)

    # Front recessed pocket for M5 bolt head (so bolt is flush with Z=0)
    hex_pocket = (cq.Workplane("XY", origin=(0, slot_y, -M5_HEX_DEPTH))
                  .slot2D(slot_len + 4.0, M5_HEX_AF + 0.6)
                  .extrude(M5_HEX_DEPTH + 1.0))
    base = base.cut(hex_pocket)

    # 5. Horizontal Dovetail-T Track for Sliding Clamp Jaw
    track_neck = TRACK_NECK_W
    track_max_w = TRACK_NECK_W + 2 * TRACK_FLARE
    z_floor = -BASE_T + TRACK_DEPTH
    z_neck_top = -BASE_T + 1.2

    track_pts = [
        (TRACK_Y - track_neck / 2, -BASE_T - 0.5),
        (TRACK_Y - track_neck / 2, z_neck_top),
        (TRACK_Y - track_max_w / 2, z_floor),
        (TRACK_Y + track_max_w / 2, z_floor),
        (TRACK_Y + track_neck / 2, z_neck_top),
        (TRACK_Y + track_neck / 2, -BASE_T - 0.5)
    ]
    track_len = (plate_x_max + 2) - (-28.0)
    track_solid = (cq.Workplane("YZ", origin=(-28.0, 0, 0))
                   .polyline(track_pts).close().extrude(track_len))
    base = base.cut(track_solid)

    # 6. Elastic band anchor eyelet hole in the lower-left corner (stays flush with bed)
    eyelet = (cq.Workplane("XY", origin=(-24.0, -42.0, -BASE_T - 1))
              .circle(2.2).extrude(BASE_T + 2))
    base = base.cut(eyelet)

    return base


def make_clamp_jaw():
    """Adjustable Right Phone Clamp Jaw with captive dovetail-T tongue,
    ergonomic D-ring pull handle, and elastic band hook.
    
    Default position: nominal clamp width = 74 mm (inner face at X = +37 mm).
    Rear face at Z = -BASE_T is flat for bed adhesion.
    """
    nom_x = PHONE_W_NOM / 2  # +37.0 mm (inner contact face of right jaw)
    jaw_len_y = 38.0
    jaw_w_x = JAW_WALL

    # 1. Main Jaw Body (rises from Z = -BASE_T to Z = JAW_H)
    jaw_body = (cq.Workplane("XY", origin=(nom_x + jaw_w_x / 2, TRACK_Y, -BASE_T))
                .box(jaw_w_x, jaw_len_y, BASE_T + JAW_H, centered=(True, True, False)))

    # Inward retention lip at Z = JAW_H
    lip_pts = [
        (nom_x, JAW_H - JAW_LIP),
        (nom_x - JAW_LIP, JAW_H),
        (nom_x + jaw_w_x, JAW_H),
        (nom_x + jaw_w_x, JAW_H - JAW_LIP)
    ]
    lip = (cq.Workplane("XZ", origin=(0, TRACK_Y, 0))
           .polyline(lip_pts).close().extrude(jaw_len_y / 2, both=True))
    jaw = jaw_body.union(lip)

    # 2. Dovetail-T Tongue (shrunk by CLR_SLIDE)
    c = CLR_SLIDE
    track_neck = TRACK_NECK_W - 2 * c
    track_max_w = (TRACK_NECK_W + 2 * TRACK_FLARE) - 2 * c
    z_floor = -BASE_T + TRACK_DEPTH - c
    z_neck_top = -BASE_T + 1.2 - c * (SQ2 - 1)

    tongue_pts = [
        (TRACK_Y - track_neck / 2, -BASE_T + c),
        (TRACK_Y - track_neck / 2, z_neck_top),
        (TRACK_Y - track_max_w / 2, z_floor),
        (TRACK_Y + track_max_w / 2, z_floor),
        (TRACK_Y + track_neck / 2, z_neck_top),
        (TRACK_Y + track_neck / 2, -BASE_T + c)
    ]
    tongue_len = 34.0
    tongue = (cq.Workplane("YZ", origin=(nom_x + jaw_w_x - tongue_len, 0, 0))
              .polyline(tongue_pts).close().extrude(tongue_len))
    jaw = jaw.union(tongue)

    # 3. D-Ring Pull Handle (Photo 1 style) on outer right side
    handle_x0 = nom_x + jaw_w_x
    handle_pts = [
        (handle_x0, TRACK_Y - 14.0),
        (handle_x0 + 12.0, TRACK_Y - 10.0),
        (handle_x0 + 12.0, TRACK_Y + 10.0),
        (handle_x0, TRACK_Y + 14.0),
        (handle_x0, TRACK_Y + 9.0),
        (handle_x0 + 7.5, TRACK_Y + 6.0),
        (handle_x0 + 7.5, TRACK_Y - 6.0),
        (handle_x0, TRACK_Y - 9.0)
    ]
    handle = (cq.Workplane("XY", origin=(0, 0, -BASE_T))
              .polyline(handle_pts).close().extrude(BASE_T + 4.0))
    handle = handle.edges("|Z").fillet(1.5)
    jaw = jaw.union(handle)

    # 4. Elastic Band Eyelet Hole through D-handle (for spring / elastic loop)
    eyelet = (cq.Workplane("XY", origin=(nom_x + 6.0, TRACK_Y, -BASE_T - 1))
              .circle(2.2).extrude(BASE_T + 6.0))
    jaw = jaw.cut(eyelet)

    return jaw


def make_eyepiece_arm():
    """Adjustable Vertical Arm with M5 alignment slot and integrated
    Microscope Eyepiece Sleeve / Collar with split clamp and eye-relief stop.
    """
    arm_w = 24.0
    arm_h = 78.0
    arm_t = 4.8
    slot_len = ADJUST_Y_TRAVEL
    
    # 1. Vertical Arm Plate (centered at X=0, Y=14.0)
    arm = (cq.Workplane("XY", origin=(0, 14.0, -BASE_T - arm_t))
           .box(arm_w, arm_h, arm_t, centered=(True, True, False)))
    arm = arm.edges("|Z").fillet(3.0)

    # Vertical M5 Adjustment Slot
    slot_through = (cq.Workplane("XY", origin=(0, 0, -BASE_T - arm_t - 1))
                    .slot2D(slot_len, SLOT_BOLT_D, 90)
                    .extrude(arm_t + 2))
    arm = arm.cut(slot_through)

    # 2. Eyepiece Collar / Sleeve (Y = 38.0 mm)
    tube_center_y = 38.0
    tube_z_top = -BASE_T - arm_t
    tube_z_bot = tube_z_top - EYEPIECE_LEN

    tube_outer = (cq.Workplane("XY", origin=(0, tube_center_y, tube_z_bot))
                  .circle(EYEPIECE_OD / 2)
                  .extrude(EYEPIECE_LEN))

    tube_bore = (cq.Workplane("XY", origin=(0, tube_center_y, tube_z_bot - 1))
                 .circle(EYEPIECE_ID / 2)
                 .extrude(EYEPIECE_LEN - EYEPIECE_RELIEF + 1))

    cam_bore = (cq.Workplane("XY", origin=(0, tube_center_y, tube_z_top - EYEPIECE_RELIEF - 1))
                .circle(EYEPIECE_STOP_D / 2)
                .extrude(EYEPIECE_RELIEF + arm_t + 2))

    sleeve = tube_outer.cut(tube_bore).cut(cam_bore)

    # 3. Split Collar Clamping Ears (+Y side of sleeve)
    ear_y0 = tube_center_y + EYEPIECE_OD / 2 - 1.0
    ear_y1 = ear_y0 + CLAMP_EAR_H
    ear_box = (cq.Workplane("XY", origin=(0, (ear_y0 + ear_y1) / 2, tube_z_bot + 4.0))
               .box(CLAMP_EAR_W * 2 + CLAMP_SLIT_W, CLAMP_EAR_H, EYEPIECE_LEN - 8.0, centered=(True, True, False)))
    
    slit = (cq.Workplane("XY", origin=(0, tube_center_y, tube_z_bot - 1))
            .box(CLAMP_SLIT_W, EYEPIECE_OD, EYEPIECE_LEN + 2, centered=(True, False, False)))

    ear_mid_y = (ear_y0 + ear_y1) / 2
    ear_mid_z = tube_z_bot + EYEPIECE_LEN / 2
    bolt_hole = (cq.Workplane("YZ", origin=(-15.0, ear_mid_y, ear_mid_z))
                 .circle(CLAMP_BOLT_D / 2)
                 .extrude(30.0))

    nut_pocket = (cq.Workplane("YZ", origin=(CLAMP_SLIT_W / 2 + CLAMP_EAR_W - CLAMP_NUT_D, ear_mid_y, ear_mid_z))
                  .polygon(6, CLAMP_NUT_AF / math.cos(math.pi / 6))
                  .extrude(CLAMP_NUT_D + 2.0))

    clamping_lugs = ear_box.cut(slit).cut(bolt_hole).cut(nut_pocket)
    sleeve = sleeve.union(clamping_lugs).cut(slit)

    arm = arm.union(sleeve)
    return arm


def make_thumb_knob():
    """Ergonomic 6-flute Knurled M5 Thumb Knob with captive hex nut pocket."""
    knob_d = 24.0
    knob_h = 8.5
    
    knob = cq.Workplane("XY").circle(knob_d / 2).extrude(knob_h)

    flute_r = 2.8
    for i in range(6):
        ang = i * (2 * math.pi / 6)
        fx = (knob_d / 2) * math.cos(ang)
        fy = (knob_d / 2) * math.sin(ang)
        flute = (cq.Workplane("XY", origin=(fx, fy, -1))
                 .circle(flute_r).extrude(knob_h + 2))
        knob = knob.cut(flute)

    hole = cq.Workplane("XY", origin=(0, 0, -1)).circle(SLOT_BOLT_D / 2).extrude(knob_h + 2)
    knob = knob.cut(hole)

    hex_r = M5_HEX_AF / math.cos(math.pi / 6) / 2
    hex_nut = (cq.Workplane("XY", origin=(0, 0, knob_h - 4.2))
               .polygon(6, hex_r * 2).extrude(5.0))
    knob = knob.cut(hex_nut)
    # Chamfer top and bottom edges for smooth tactile grip
    knob = knob.edges(">Z").chamfer(0.8).edges("<Z").chamfer(0.8)
    return knob


def verify_stl(path, cad_volume):
    """Re-read exported binary STL and verify printability."""
    data = Path(path).read_bytes()
    n = struct.unpack_from("<I", data, 80)[0]
    assert len(data) == 84 + 50 * n, f"{path.name}: not a valid binary STL"
    key = lambda v: tuple(round(c, 4) for c in v)
    edges, vol, zmin, bed_area = Counter(), 0.0, math.inf, 0.0
    for i in range(n):
        f = struct.unpack_from("<12f", data, 84 + 50 * i)
        v = [f[3:6], f[6:9], f[9:12]]
        ks = [key(p) for p in v]
        for j in range(3):
            a_, b_ = ks[j], ks[(j + 1) % 3]
            edges[(a_, b_) if a_ < b_ else (b_, a_)] += 1
        (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = v
        vol += (x1 * (y2 * z3 - y3 * z2) - x2 * (y1 * z3 - y3 * z1) + x3 * (y1 * z2 - y2 * z1)) / 6
        zmin = min(zmin, z1, z2, z3)
        if max(z1, z2, z3) < 1e-4:   # triangle touching print bed
            bed_area += abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2
    bad = sum(1 for c in edges.values() if c != 2)
    assert bad == 0, f"{path.name}: {bad} non-manifold / open edges"
    assert vol > 0, f"{path.name}: inverted normals"
    assert abs(vol - cad_volume) / cad_volume < 0.015, \
        f"{path.name}: volume {vol:.0f} vs CAD {cad_volume:.0f} mm^3"
    assert abs(zmin) < 1e-4, f"{path.name}: not sitting on the bed (z min = {zmin:.3f})"
    assert bed_area > 30, f"{path.name}: only {bed_area:.0f} mm^2 touching the bed"
    return n, vol, bed_area


def main():
    walls = checks()
    print("Pre-flight wall checks:", {k: round(v, 2) for k, v in walls.items()})

    base = make_phone_base()
    jaw = make_clamp_jaw()
    arm = make_eyepiece_arm()
    knob = make_thumb_knob()

    parts_dict = {
        "phone_base.stl": base,
        "clamp_jaw.stl": jaw,
        "eyepiece_arm.stl": arm,
        "thumb_knob.stl": knob
    }

    transforms = {}
    for fname, raw_solid in parts_dict.items():
        assert raw_solid.val().isValid(), f"{fname} solid is invalid"
        assert len(raw_solid.solids().vals()) == 1, f"{fname} has multiple solids"
        
        # Prepare print-oriented solid
        p = raw_solid
        rot_x = 0
        if fname == "eyepiece_arm.stl":
            p = p.rotate((0, 0, 0), (1, 0, 0), 180)
            rot_x = 180
            
        bb = p.val().BoundingBox()
        print_shift = [-bb.xmin, -bb.ymin, -bb.zmin]
        print_solid = p.translate(print_shift)
        transforms[fname] = {"printShift": print_shift, "rotX": rot_x}

        out_path = OUT / fname
        cq.exporters.export(print_solid, str(out_path), tolerance=STL_TOL, angularTolerance=STL_ANG_TOL)
        n, vol, bed = verify_stl(out_path, print_solid.val().Volume())
        print(f"{fname}: {n} triangles, watertight, volume {vol/1000:.2f} cm^3, {bed:.0f} mm^2 on bed")

    # Export params for Three.js viewer
    params = {
        "phone": {
            "wMin": PHONE_W_MIN,
            "wNom": PHONE_W_NOM,
            "wMax": PHONE_W_MAX,
            "tMax": PHONE_T_MAX,
            "lRef": PHONE_L_REF
        },
        "eyepiece": {
            "id": EYEPIECE_ID,
            "od": EYEPIECE_OD,
            "len": EYEPIECE_LEN,
            "stopD": EYEPIECE_STOP_D,
            "relief": EYEPIECE_RELIEF,
            "centerNomY": 38.0
        },
        "adjust": {
            "xTravel": ADJUST_X_TRAVEL,
            "yTravel": ADJUST_Y_TRAVEL,
            "xMin": -ADJUST_X_TRAVEL / 2,
            "xMax": ADJUST_X_TRAVEL / 2,
            "yMin": -ADJUST_Y_TRAVEL / 2,
            "yMax": ADJUST_Y_TRAVEL / 2
        },
        "base": {
            "w": BASE_W,
            "h": BASE_H,
            "t": BASE_T,
            "jawH": JAW_H,
            "fixedJawX": FIXED_JAW_X
        },
        "transforms": transforms
    }
    (OUT / "params.json").write_text(json.dumps(params, indent=2))
    print(f"Generated params.json with 2-axis travel: X +/-{ADJUST_X_TRAVEL/2}mm, Y +/-{ADJUST_Y_TRAVEL/2}mm")
    print(f"Clamping width range: {PHONE_W_MIN} mm -> {PHONE_W_MAX} mm")


if __name__ == "__main__":
    main()
