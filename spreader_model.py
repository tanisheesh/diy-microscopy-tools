"""
Blood smear slide spreader - parametric CadQuery model.

All dimensions are in mm. Change only the PARAMETERS section, then run:
    py -3.14 spreader_model.py

Output: base.stl, carriage.stl (print orientation), params.json (for the viewer).

Coordinate system (assembly):
    X = slide length / push direction, Y = width (centred on 0), Z = up.
    Bottom of the base is at z = 0.
The spreader's glass contact point is at carriage-local X = 0.

The carriage is captive: its dovetail-T tongues are trapped in undercut grooves
in the rails, so it cannot lift off. The grooves are closed at the front (end
stop) and open at the back so the carriage can be slid in; a removable pin
(a short piece of 1.75 mm filament) then stops it from sliding out the back.
"""
import json
import math
from pathlib import Path

import cadquery as cq

# ============================== PARAMETERS ==============================
# Glass slides (used for fit only - these are not printed)
SLIDE_L, SLIDE_W, SLIDE_T = 75.0, 25.0, 1.0        # base microscope slide (ISO/DIN)
SPREADER_L, SPREADER_W, SPREADER_T = 75.0, 25.0, 1.0  # spreader slide
SPREADER_ANGLE = 45.0       # degrees, between spreader and base slide

# Print tolerances
CLR_SLIDE = 0.30            # slide bed and spreader slot, per side
CLR_RAIL = 0.25             # carriage tongue <-> rail groove, per side
MIN_WALL = 1.6              # used by the wall-thickness checks

# Base plate
BASE_L, BASE_W = 100.0, 44.0
PLATE_TOP = 4.0             # height of the plate's top surface
SLIDE_PROUD = 0.2           # how far the slide sits above the plate (so the spreader rides on glass)
NOTCH_R, NOTCH_EXTRA_DEPTH = 6.0, 1.5   # finger notches for lifting the slide out

# Rails (both sides) + captive dovetail-T groove
RAIL_W = 8.6
RAIL_H = 5.0                # above the plate top
GROOVE_NECK_W = 2.6         # open top part of the groove
GROOVE_NECK_H = 1.6         # thickness of the rail lip (above the undercut)
GROOVE_W = 5.4              # max inner width after the 45 deg flare
FRONT_STOP = 4.0            # groove is closed for this length at the front (end stop)

# Retaining pin (rear stop) - a piece of 1.75 mm filament
PIN_D = 1.75
PIN_HOLE_D = 1.8            # snug: printed holes come out ~0.1 mm small -> light press fit
PIN_X = 4.0                 # distance from the rear end of the base
PIN_HOLE_DEPTH = 3.0        # below the groove floor (deeper = firmer grip)
PIN_LEN = 11.0              # leaves ~5 mm above the rail top to grab and pull

# Carriage
CARRIAGE_H = 14.0           # body height above the rail top
CARRIAGE_LEN = 32.0         # footprint length on the rails
FOOT_H = 4.0                # rear stabilising foot
RAMP_T = 3.0                # material behind the slot (perpendicular to it)
FRONT_WALL = 4.0            # material in front of the slot at the bottom
KNOB_R = 5.5                # full-width finger grip (side-print friendly)
KNOB_LIFT = 2.5             # knob centre height above the body top
KNOB_SETBACK = 8.0          # knob centre distance from the front face

STL_TOL, STL_ANG_TOL = 0.02, 0.1
# =======================================================================

a = math.radians(SPREADER_ANGLE)
OUT = Path(__file__).resolve().parent
SQ2 = math.sqrt(2)

# ---- derived ----
RECESS_L = SLIDE_L + 2 * CLR_SLIDE
RECESS_W = SLIDE_W + 2 * CLR_SLIDE
RECESS_DEPTH = SLIDE_T - SLIDE_PROUD
RECESS_X0 = (BASE_L - RECESS_L) / 2
SLIDE_X0 = RECESS_X0 + CLR_SLIDE
SLIDE_TOP_Z = PLATE_TOP - RECESS_DEPTH + SLIDE_T
RAIL_TOP = PLATE_TOP + RAIL_H
RAIL_INNER_Y = BASE_W / 2 - RAIL_W
GROOVE_Y = BASE_W / 2 - RAIL_W / 2
FLARE = (GROOVE_W - GROOVE_NECK_W) / 2          # 45 deg flare: height = width
GROOVE_DEPTH = GROOVE_NECK_H + FLARE
GROOVE_FLOOR = RAIL_TOP - GROOVE_DEPTH
SLOT_W = SPREADER_W + 2 * CLR_SLIDE
T_LO, T_HI = -CLR_SLIDE, SPREADER_T + CLR_SLIDE   # slot faces (glass occupies t in [0, T])
T_BACK = T_LO - RAMP_T

Z_BOT = RAIL_TOP
Z_TOP = Z_BOT + CARRIAGE_H
Z_FOOT = Z_BOT + FOOT_H


def glass_xz(s, t):
    """Glass frame -> carriage-local XZ. s = along the glass (up and back), t = through its thickness."""
    return (-math.cos(a) * s + math.sin(a) * t,
            SLIDE_TOP_Z + math.sin(a) * s + math.cos(a) * t)


def x_on_face(z, t):
    s = (z - SLIDE_TOP_Z - math.cos(a) * t) / math.sin(a)
    return glass_xz(s, t)[0]


X_FRONT = x_on_face(Z_BOT, T_HI) + FRONT_WALL
X_BACK = X_FRONT - CARRIAGE_LEN


def groove_half_profile(c=0.0):
    """Right half of the groove (y >= 0 from the groove centre), z relative to the rail top.
    c > 0 => tongue: the groove shrunk by c (normal clearance on every face)."""
    neck = GROOVE_NECK_W / 2 - c
    floor = -GROOVE_DEPTH + c
    # 45 deg flare line: y + z = k ; offsetting inward lowers k
    k = GROOVE_NECK_W / 2 - GROOVE_NECK_H - c * SQ2
    z_flare_top = k - neck
    y_bottom = k - floor
    return neck, z_flare_top, floor, y_bottom


def checks():
    neck, zft, floor, yb = groove_half_profile(CLR_RAIL)
    walls = {
        "plate floor under slide bed": PLATE_TOP - RECESS_DEPTH,
        "floor under finger notch": PLATE_TOP - RECESS_DEPTH - NOTCH_EXTRA_DEPTH,
        "rail wall beside groove": (RAIL_W - GROOVE_W) / 2,
        "rail lip over undercut": GROOVE_NECK_H,
        "material under pin hole": GROOVE_FLOOR - PIN_HOLE_DEPTH,
        "front end stop": FRONT_STOP,
        "slot side wall (cheek)": (BASE_W - SLOT_W) / 2,
        "ramp behind slot": RAMP_T,
        "tongue neck": 2 * neck,
    }
    for name, v in walls.items():
        assert v >= MIN_WALL - 1e-9, f"{name} = {v:.2f} mm < {MIN_WALL}"
    assert PIN_HOLE_D < GROOVE_NECK_W, "pin won't pass through the groove neck"
    assert yb > neck + 0.5, "tongue undercut too small - carriage won't stay captive"
    assert RAIL_INNER_Y > SPREADER_W / 2, "spreader doesn't fit between the rails"
    assert RAIL_INNER_Y >= RECESS_W / 2, "slide bed cuts into the rails"
    assert x_on_face(Z_FOOT, T_BACK) > X_BACK, "foot too short"
    walls["undercut grip per side"] = yb - GROOVE_NECK_W / 2
    return walls


def xz_prism(points, width):
    """Extrude an XZ polygon symmetrically along Y."""
    return cq.Workplane("XZ").polyline(points).close().extrude(width / 2, both=True)


def yz_prism(points, x0, length):
    """Extrude a YZ polygon from X = x0 to x0 + length."""
    return (cq.Workplane("YZ", origin=(x0, 0, 0))
            .polyline(points).close().extrude(length))


def mirrored_profile(gy, z0, half, top_extra):
    """Build the full polygon from groove_half_profile, centred on groove centre gy."""
    neck, zft, floor, yb = half
    right = [(neck, top_extra), (neck, zft), (yb, floor)]
    pts = right + [(-y, z) for y, z in reversed(right)]
    return [(gy + y, z0 + z) for y, z in pts]


def make_base():
    base = cq.Workplane("XY").box(BASE_L, BASE_W, PLATE_TOP, centered=(False, True, False))
    for side in (1, -1):
        y_in, y_out = side * RAIL_INNER_Y, side * BASE_W / 2
        rail = yz_prism([(y_in, PLATE_TOP - 0.01), (y_out, PLATE_TOP - 0.01),
                         (y_out, RAIL_TOP), (y_in, RAIL_TOP)], 0, BASE_L)
        base = base.union(rail)
        gy = side * GROOVE_Y
        # groove: open at the rear (x = 0), closed FRONT_STOP from the front
        groove = yz_prism(mirrored_profile(gy, RAIL_TOP, groove_half_profile(0.0), 1.0),
                          -1, BASE_L - FRONT_STOP + 1)
        base = base.cut(groove)
        pin_hole = (cq.Workplane("XY", origin=(PIN_X, gy, GROOVE_FLOOR - PIN_HOLE_DEPTH))
                    .circle(PIN_HOLE_D / 2).extrude(PIN_HOLE_DEPTH + 0.5))
        base = base.cut(pin_hole)
    recess_z0 = PLATE_TOP - RECESS_DEPTH
    recess = (cq.Workplane("XY", origin=(RECESS_X0, 0, recess_z0))
              .box(RECESS_L, RECESS_W, RECESS_DEPTH + 1, centered=(False, True, False)))
    base = base.cut(recess)
    for nx in (RECESS_X0, RECESS_X0 + RECESS_L):
        notch = (cq.Workplane("XY", origin=(nx, 0, recess_z0 - NOTCH_EXTRA_DEPTH))
                 .circle(NOTCH_R).extrude(RECESS_DEPTH + NOTCH_EXTRA_DEPTH + 1))
        base = base.cut(notch)
    return base


def make_pins():
    pins = None
    for side in (1, -1):
        p = (cq.Workplane("XY", origin=(PIN_X, side * GROOVE_Y, GROOVE_FLOOR - PIN_HOLE_DEPTH))
             .circle(PIN_D / 2).extrude(PIN_LEN))
        pins = p if pins is None else pins.union(p)
    return pins


def make_carriage():
    """Carriage-local frame: spreader contact at X = 0, Z at assembly height."""
    back_top = x_on_face(Z_TOP, T_BACK)
    back_foot = x_on_face(Z_FOOT, T_BACK)
    profile = [(X_FRONT, Z_BOT), (X_FRONT, Z_TOP), (back_top, Z_TOP),
               (back_foot, Z_FOOT), (X_BACK, Z_FOOT), (X_BACK, Z_BOT)]
    body = xz_prism(profile, BASE_W)

    knob_x = X_FRONT - KNOB_SETBACK
    knob = (cq.Workplane("XZ").center(knob_x, Z_TOP + KNOB_LIFT)
            .circle(KNOB_R).extrude(BASE_W / 2, both=True))
    body = body.union(knob)

    # Dovetail-T tongues: the groove shrunk by CLR_RAIL
    for side in (1, -1):
        tongue = yz_prism(mirrored_profile(side * GROOVE_Y, Z_BOT, groove_half_profile(CLR_RAIL), 0.01),
                          X_BACK, X_FRONT - X_BACK)
        body = body.union(tongue)

    s0, s1 = -10.0, SPREADER_L + 20
    slot = xz_prism([glass_xz(s0, T_LO), glass_xz(s1, T_LO),
                     glass_xz(s1, T_HI), glass_xz(s0, T_HI)], SLOT_W)
    return body.cut(slot)


def glass_solids(contact_x):
    slide = (cq.Workplane("XY", origin=(SLIDE_X0, 0, SLIDE_TOP_Z - SLIDE_T))
             .box(SLIDE_L, SLIDE_W, SLIDE_T, centered=(False, True, False)))
    spreader = xz_prism([glass_xz(0, 0), glass_xz(SPREADER_L, 0),
                         glass_xz(SPREADER_L, SPREADER_T), glass_xz(0, SPREADER_T)],
                        SPREADER_W).translate((contact_x, 0, 0))
    return slide, spreader


def interference(p, q):
    r = p.intersect(q)
    return r.val().Volume() if r.vals() else 0.0


def main():
    walls = checks()
    base = make_base()
    carriage = make_carriage()
    pins = make_pins()

    # Travel: back to the pin, forward to the end stop (and short of the slide's end)
    contact_min = (PIN_X + PIN_D / 2 + 0.5) - X_BACK
    contact_max = min(BASE_L - FRONT_STOP - 0.5 - X_FRONT, SLIDE_X0 + SLIDE_L - 3)
    assert contact_max > contact_min + 30, "smear travel is less than 30 mm"

    # Fit / interference checks (at both ends of travel)
    for cx in (contact_min, contact_max):
        c = carriage.translate((cx, 0, 0))
        slide, spreader = glass_solids(cx)
        for name, (p, q) in {"carriage-base": (c, base), "carriage-pins": (c, pins),
                             "carriage-spreader": (c, spreader), "base-slide": (base, slide),
                             "base-spreader": (base, spreader), "base-pins": (base, pins)}.items():
            v = interference(p, q)
            assert v < 1e-3, f"interference {name} @x={cx:.1f}: {v:.4f} mm^3"

    # Captive checks: lifting the carriage, or moving it past either end, must collide
    mid = (contact_min + contact_max) / 2
    lift = CLR_RAIL * SQ2 + 0.3
    assert interference(carriage.translate((mid, 0, lift)), base) > 1, "carriage can lift off!"
    assert interference(carriage.translate((contact_min - 1.5, 0, 0)), pins) > 0.1, "pin doesn't stop the carriage"
    assert interference(carriage.translate((BASE_L - FRONT_STOP - X_FRONT + 1, 0, 0)), base) > 0.1, \
        "front end stop doesn't stop the carriage"

    for name, part in (("base", base), ("carriage", carriage)):
        assert part.val().isValid(), f"{name} solid is invalid"
        assert len(part.solids().vals()) == 1, f"{name} is not a single solid"

    # Print orientation
    cq.exporters.export(base, str(OUT / "base.stl"), tolerance=STL_TOL, angularTolerance=STL_ANG_TOL)
    # Carriage on its side (Y -> Z): slot, knob and tongues all print without supports
    rot = carriage.rotate((0, 0, 0), (1, 0, 0), 90)
    bb = rot.val().BoundingBox()
    shift = (-bb.xmin, -bb.ymin, -bb.zmin)
    rot = rot.translate(shift)
    cq.exporters.export(rot, str(OUT / "carriage.stl"), tolerance=STL_TOL, angularTolerance=STL_ANG_TOL)

    params = {
        "base": {"L": BASE_L, "W": BASE_W, "plateTop": PLATE_TOP, "railTop": RAIL_TOP},
        "slide": {"L": SLIDE_L, "W": SLIDE_W, "T": SLIDE_T, "x0": SLIDE_X0, "topZ": SLIDE_TOP_Z},
        "spreader": {"L": SPREADER_L, "W": SPREADER_W, "T": SPREADER_T, "angleDeg": SPREADER_ANGLE},
        "carriage": {"printShift": shift, "printRotXDeg": 90,
                     "contactMin": contact_min, "contactMax": contact_max},
        "pin": {"x": PIN_X, "y": GROOVE_Y, "d": PIN_D, "z0": GROOVE_FLOOR - PIN_HOLE_DEPTH, "len": PIN_LEN},
        "tolerances": {"slide": CLR_SLIDE, "rail": CLR_RAIL, "minWall": MIN_WALL},
    }
    (OUT / "params.json").write_text(json.dumps(params, indent=2))

    print("Min walls:", {k: round(v, 2) for k, v in walls.items()})
    for name, part in (("base", base), ("carriage (print orient.)", rot)):
        b = part.val().BoundingBox()
        print(f"{name}: {b.xlen:.1f} x {b.ylen:.1f} x {b.zlen:.1f} mm, "
              f"volume {part.val().Volume() / 1000:.1f} cm^3")
    print(f"Spreader angle: {SPREADER_ANGLE:.0f} deg")
    print(f"Smear travel: contact X {contact_min:.1f} -> {contact_max:.1f} mm "
          f"({contact_max - contact_min:.1f} mm)")
    print("Captive checks OK: lift blocked, pin + front stop block the ends")


if __name__ == "__main__":
    main()
