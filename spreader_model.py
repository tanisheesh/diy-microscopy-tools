"""
Blood smear slide spreader - parametric CadQuery model.

Saare dimensions mm mein. Sirf PARAMETERS section badlo, phir chalao:
    py -3.14 spreader_model.py

Output: base.stl, carriage.stl (print orientation), params.json (viewer ke liye).

Coordinate system (assembly):
    X = slide ki lambai / push direction, Y = width (centre 0), Z = upar.
    Base ka bottom z = 0.
Spreader ka glass contact point carriage ke local X = 0 pe hota hai.

Carriage captive hai: uske dovetail-T tongues rails ki undercut grooves mein
phanse rehte hain (upar nahi uth sakta). Groove aage se band hai (end stop),
peeche se khuli hai taaki carriage andar daal sako; wahan ek removable pin
(1.75 mm filament ka tukda) carriage ko bahar nikalne se rokta hai.
"""
import json
import math
from pathlib import Path

import cadquery as cq

# ============================== PARAMETERS ==============================
# Glass slides (sirf fit ke liye - print nahi hoti)
SLIDE_L, SLIDE_W, SLIDE_T = 75.0, 25.0, 1.0        # base microscope slide
SPREADER_L, SPREADER_W, SPREADER_T = 75.0, 25.0, 1.0  # spreader slide
SPREADER_ANGLE = 45.0       # degrees, spreader aur base slide ke beech

# Print tolerances
CLR_SLIDE = 0.30            # slide bed aur spreader slot, har taraf
CLR_RAIL = 0.25             # carriage tongue <-> rail groove, har taraf
MIN_WALL = 1.6              # check ke liye

# Base plate
BASE_L, BASE_W = 100.0, 44.0
PLATE_TOP = 4.0             # plate top surface ki height
SLIDE_PROUD = 0.2           # slide plate se kitni upar rahe (spreader glass pe chale)
NOTCH_R, NOTCH_EXTRA_DEPTH = 6.0, 1.5   # slide nikalne ke finger notch

# Rails (dono taraf) + captive dovetail-T groove
RAIL_W = 8.6
RAIL_H = 5.0                # plate top ke upar
GROOVE_NECK_W = 2.6         # groove ka upar wala khula hissa
GROOVE_NECK_H = 1.6         # rail ke lip ki motai (undercut ke upar)
GROOVE_W = 5.4              # 45 deg flare ke baad andar ki max width
FRONT_STOP = 4.0            # groove aage se itni band (end stop)

# Retaining pin (peeche ka stop) - 1.75 mm filament ka tukda
PIN_D = 1.75
PIN_HOLE_D = 1.8           # snug: printed hole ~0.1 chhota aata hai -> halka press-fit
PIN_X = 4.0                 # base ke peeche wale end se
PIN_HOLE_DEPTH = 3.0        # groove floor ke neeche (jitna gehra, utna pakka pakad)
PIN_LEN = 11.0              # rail top se ~5 mm bahar rahe, pakad ke kheenchne ke liye

# Carriage
CARRIAGE_H = 14.0           # rail top ke upar body height
CARRIAGE_LEN = 32.0         # rails pe footprint length
FOOT_H = 4.0                # pichhla stabilising foot
RAMP_T = 3.0                # slot ke peeche ki material (perpendicular)
FRONT_WALL = 4.0            # slot ke aage bottom pe material
KNOB_R = 5.5                # full-width finger grip (side-print friendly)
KNOB_LIFT = 2.5             # knob centre body top se kitna upar
KNOB_SETBACK = 8.0          # front face se knob centre

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
FLARE = (GROOVE_W - GROOVE_NECK_W) / 2          # 45 deg flare ki height = width
GROOVE_DEPTH = GROOVE_NECK_H + FLARE
GROOVE_FLOOR = RAIL_TOP - GROOVE_DEPTH
SLOT_W = SPREADER_W + 2 * CLR_SLIDE
T_LO, T_HI = -CLR_SLIDE, SPREADER_T + CLR_SLIDE   # slot faces (glass t in [0, T])
T_BACK = T_LO - RAMP_T

Z_BOT = RAIL_TOP
Z_TOP = Z_BOT + CARRIAGE_H
Z_FOOT = Z_BOT + FOOT_H


def glass_xz(s, t):
    """Glass frame -> carriage-local XZ. s = glass ke along (upar-peeche), t = thickness."""
    return (-math.cos(a) * s + math.sin(a) * t,
            SLIDE_TOP_Z + math.sin(a) * s + math.cos(a) * t)


def x_on_face(z, t):
    s = (z - SLIDE_TOP_Z - math.cos(a) * t) / math.sin(a)
    return glass_xz(s, t)[0]


X_FRONT = x_on_face(Z_BOT, T_HI) + FRONT_WALL
X_BACK = X_FRONT - CARRIAGE_LEN


def groove_half_profile(c=0.0):
    """Groove ka right-half (y >= 0, groove centre se), z rail top se relative.
    c > 0 => tongue: groove ko c se andar shrink kiya (har face pe normal clearance)."""
    neck = GROOVE_NECK_W / 2 - c
    floor = -GROOVE_DEPTH + c
    # 45 deg flare line: y + z = k ; erosion se k chhota hota hai
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
    assert PIN_HOLE_D < GROOVE_NECK_W, "pin groove ke neck se andar nahi jaayega"
    assert yb > neck + 0.5, "tongue ka undercut bahut chhota - captive nahi rahega"
    assert RAIL_INNER_Y > SPREADER_W / 2, "spreader rails ke beech fit nahi hota"
    assert RAIL_INNER_Y >= RECESS_W / 2, "slide bed rails mein ghus raha hai"
    assert x_on_face(Z_FOOT, T_BACK) > X_BACK, "foot too short"
    walls["undercut grip per side"] = yb - GROOVE_NECK_W / 2
    return walls


def xz_prism(points, width):
    """XZ polygon ko Y mein symmetric extrude."""
    return cq.Workplane("XZ").polyline(points).close().extrude(width / 2, both=True)


def yz_prism(points, x0, length):
    """YZ polygon ko X = x0 .. x0+length extrude."""
    return (cq.Workplane("YZ", origin=(x0, 0, 0))
            .polyline(points).close().extrude(length))


def mirrored_profile(gy, z0, half, top_extra):
    """groove_half_profile ko groove centre gy pe poora polygon banao."""
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
        # groove: peeche (x=0) se khuli, aage FRONT_STOP pe band
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
    """Carriage-local frame: spreader contact X = 0, Z assembly height wala."""
    back_top = x_on_face(Z_TOP, T_BACK)
    back_foot = x_on_face(Z_FOOT, T_BACK)
    profile = [(X_FRONT, Z_BOT), (X_FRONT, Z_TOP), (back_top, Z_TOP),
               (back_foot, Z_FOOT), (X_BACK, Z_FOOT), (X_BACK, Z_BOT)]
    body = xz_prism(profile, BASE_W)

    knob_x = X_FRONT - KNOB_SETBACK
    knob = (cq.Workplane("XZ").center(knob_x, Z_TOP + KNOB_LIFT)
            .circle(KNOB_R).extrude(BASE_W / 2, both=True))
    body = body.union(knob)

    # Dovetail-T tongues: groove ko CLR_RAIL se shrink kiya
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

    # Travel: peeche pin tak, aage end stop tak (aur slide ke end se pehle)
    contact_min = (PIN_X + PIN_D / 2 + 0.5) - X_BACK
    contact_max = min(BASE_L - FRONT_STOP - 0.5 - X_FRONT, SLIDE_X0 + SLIDE_L - 3)
    assert contact_max > contact_min + 30, "smear travel 30 mm se kam hai"

    # Fit / interference checks (dono travel ends pe)
    for cx in (contact_min, contact_max):
        c = carriage.translate((cx, 0, 0))
        slide, spreader = glass_solids(cx)
        for name, (p, q) in {"carriage-base": (c, base), "carriage-pins": (c, pins),
                             "carriage-spreader": (c, spreader), "base-slide": (base, slide),
                             "base-spreader": (base, spreader), "base-pins": (base, pins)}.items():
            v = interference(p, q)
            assert v < 1e-3, f"interference {name} @x={cx:.1f}: {v:.4f} mm^3"

    # Captive checks: carriage upar uthe, ya travel ke bahar jaaye, to takkar honi chahiye
    mid = (contact_min + contact_max) / 2
    lift = CLR_RAIL * SQ2 + 0.3
    assert interference(carriage.translate((mid, 0, lift)), base) > 1, "carriage upar uth jaata hai!"
    assert interference(carriage.translate((contact_min - 1.5, 0, 0)), pins) > 0.1, "pin carriage ko nahi rokta"
    assert interference(carriage.translate((BASE_L - FRONT_STOP - X_FRONT + 1, 0, 0)), base) > 0.1, \
        "front end stop carriage ko nahi rokta"

    for name, part in (("base", base), ("carriage", carriage)):
        assert part.val().isValid(), f"{name} solid invalid"
        assert len(part.solids().vals()) == 1, f"{name} ek solid nahi hai"

    # Print orientation
    cq.exporters.export(base, str(OUT / "base.stl"), tolerance=STL_TOL, angularTolerance=STL_ANG_TOL)
    # Carriage side pe (Y -> Z): slot, knob, tongues sab bina support
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
