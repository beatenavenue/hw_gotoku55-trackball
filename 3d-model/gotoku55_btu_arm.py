"""GOTOKU-55 BTU arm (Rexroth KU-B8 compatible), CadQuery.

Parts of the arm
  base     : plate of the split metal arm, cut at its top face (z = 33.5)
  cup      : holds the BTU. The BTU hangs on the top face (seat) by its flange.
             The body of the BTU does not touch the floor of the cup.
  support  : joins the cup to the base. A ruled loft from the footprint (from the plan
             by the user) up to the lower edge of the seat. The sides lean inward,
             never outward.

All dimensions in mm. Coordinates are the same as the GOTOKU repository.
"""
import math
import numpy as np
import shapely.geometry as sg
import cadquery as cq
from cadquery import Vector

GOTOKU = "../hw_gotoku55-trackball/3d-model/"

# ---- ball (fixed by the case and the sensor) ----
BALL_D = 55.0
BALL_AXIS = (0.0, -11.07)        # xy of the ball center
BALL_Z = 59.0

# ---- supports ----
CONTACT_DEG = 65.0               # BTU axis from the downward vertical
AZIMUTHS = (30.0, 150.0, 270.0)

# ---- Rexroth KU-B8 ----
BTU_BALL_TOP_TO_SEAT = 4.8       # h
BTU_BODY_D = 12.6                # D
BTU_BODY_LEN = 6.4               # H - h, below the seat

# ---- cup ----
BORE_D = 12.7                    # same as the official v4 STL (Rexroth body 12.6 + 0.1)
CUP_D = 17.2                     # flange recess of v4. The flange is flush with the cup
BODY_GAP = 0.5                   # gap between the end of the body and the floor
FLOOR_T = 1.5
PUSH_HOLE_D = 3.0                # to push the BTU out from behind
CUP_LEN = BTU_BODY_LEN + BODY_GAP + FLOOR_T
BACK_FILLET = 1.5                # round edge at the back of the cup (max with a 1.5 mm wall to the bore)

# ---- support ----
BASE_TOP_Z = 33.5
# footprint in local coordinates (u: from the ball axis outward, v: sideways)
FP_TIP_U = 14.0                  # inner end
FP_TIP_SIDE = (14.66, 4.0)       # where the inner arc meets the straight sides
FP_WIDE = (24.08, 8.2)           # widest point
FP_OUTER_SIDE = (34.58, 3.44)    # where the straight sides meet the outer arc
FP_OUTER_R = 34.77               # outer arc, centered on the ball axis
FP_FILLET_WIDE = 3.0
FP_FILLET_OTHER = 1.5
DRAFT_DEG = 3.0                  # side walls under the cup lean inward by this angle
GUSSET_HALF_WIDTH = 6.4          # the gusset meets the edge of the seat up to this far sideways
GUSSET_POINTS = 61

# ---- derived ----
T = math.radians(CONTACT_DEG)
SEAT_R = BALL_D / 2 + BTU_BALL_TOP_TO_SEAT       # ball center to seat, along the axis
# local frame: x = u (outward), y = v, z = global z. Ball center at (0, 0, BALL_Z)
D_LOCAL = Vector(math.sin(T), 0, -math.cos(T))    # BTU axis, away from the ball
SEAT_LOCAL = Vector(0, 0, BALL_Z) + D_LOCAL * SEAT_R


def to_global(shape, az):
    shape = shape.rotate(Vector(0, 0, 0), Vector(0, 0, 1), az)
    return shape.translate(Vector(BALL_AXIS[0], BALL_AXIS[1], 0))


def along_axis(solid, start):
    """Place a solid built along +z at local `start` (distance from the seat, along D)."""
    # +z of the solid -> D_LOCAL. Rotate about y.
    ang = math.degrees(math.atan2(D_LOCAL.x, D_LOCAL.z))
    s = solid.rotate(Vector(0, 0, 0), Vector(0, 1, 0), ang)
    return s.translate(SEAT_LOCAL + D_LOCAL * start)


def cup_local():
    outer = cq.Workplane("XY").circle(CUP_D / 2).extrude(CUP_LEN)
    outer = outer.faces(">Z").edges().fillet(BACK_FILLET)
    return along_axis(outer.val(), 0)


def cup_cuts_local():
    bore = cq.Solid.makeCylinder(BORE_D / 2, BTU_BODY_LEN + BODY_GAP + 20, Vector(0, 0, -20))
    hole = cq.Solid.makeCylinder(PUSH_HOLE_D / 2, 40, Vector(0, 0, 0))
    # room for the flange and the ball of the BTU, and the way it goes in
    # (same diameter as the cup: the flange is 17 mm, so 0.1 mm per side)
    flange = cq.Solid.makeCylinder(CUP_D / 2, 30, Vector(0, 0, -30))
    return [along_axis(s, 0) for s in (bore, hole, flange)]


def footprint_face():
    (tu, tv), (wu, wv), (ou, ov) = FP_TIP_SIDE, FP_WIDE, FP_OUTER_SIDE
    f = (
        cq.Sketch()
        .arc((tu, -tv), (FP_TIP_U, 0), (tu, tv))
        .segment((tu, tv), (wu, wv))
        .segment((wu, wv), (ou, ov))
        .arc((ou, ov), (FP_OUTER_R, 0), (ou, -ov))
        .segment((ou, -ov), (wu, -wv))
        .segment((wu, -wv), (tu, -tv))
        .assemble()
    )._faces.Faces()[0]

    def pick(face, pts):
        return [v for v in face.Vertices()
                if any(abs(v.X - p[0]) < 0.01 and abs(v.Y - p[1]) < 0.01 for p in pts)]

    f = f.fillet2D(FP_FILLET_WIDE, pick(f, [(wu, wv), (wu, -wv)]))
    f = f.fillet2D(FP_FILLET_OTHER, pick(f, [(ou, ov), (ou, -ov)]))
    f = f.fillet2D(FP_FILLET_OTHER, pick(f, [(tu, tv), (tu, -tv)]))
    return f.translate(Vector(0, 0, BASE_TOP_Z))


def _resample(pts, n):
    """n points spaced evenly along a polyline (the last point is left out)."""
    pts = np.asarray(pts, float)
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    t = np.linspace(0, d[-1], n, endpoint=False)
    return np.array([np.interp(t, d, pts[:, k]) for k in range(3)]).T


def _pair_by_angle(curve, center, ax_x, ax_y, angles):
    """Points on an open curve (polyline) at the given polar angles around `center`.
    Angle 0 is along ax_x and grows toward ax_y. The curve must turn monotonically."""
    q = curve - center
    ang = np.unwrap(np.arctan2(q @ ax_y, q @ ax_x))
    if ang[-1] < ang[0]:
        curve, ang = curve[::-1], ang[::-1]
    return np.array([np.interp(angles, ang, curve[:, k]) for k in range(3)]).T


def _spline(pts):
    return cq.Edge.makeSpline([Vector(*p) for p in pts],
                              parameters=list(np.linspace(0, 1, len(pts))))


def gusset_local():
    """Ruled loft from the part of the footprint on the ball side of the seat plane
    up to the lower edge of the seat. Its back face lies in the seat plane."""
    e_up = np.array([math.cos(T), 0, math.sin(T)])        # in the seat plane, upward
    e_v = np.array([0.0, 1.0, 0.0])
    seat = np.array(SEAT_LOCAL.toTuple())
    r = CUP_D / 2
    # where the seat plane meets the top of the base
    u_cut = seat[0] - (seat[2] - BASE_TOP_Z) / math.tan(T)
    fp = sg.Polygon([footprint_face().outerWire().positionAt(t, mode="length").toTuple()[:2]
                     for t in np.linspace(0, 1, 4000, endpoint=False)])
    part = fp.intersection(sg.box(0, -50, u_cut, 50))
    ring = np.array(part.exterior.coords)[:-1]
    # boundary from the +v end of the cut line, around the tip, to the -v end
    on_cut = np.abs(ring[:, 0] - u_cut) < 1e-6
    i_p = np.where(on_cut)[0][np.argmax(ring[on_cut, 1])]
    i_m = np.where(on_cut)[0][np.argmin(ring[on_cut, 1])]
    ring = np.roll(ring, -i_p, axis=0)
    i_m = (i_m - i_p) % len(ring)
    if i_m == 1:            # walked along the cut line, go the other way
        ring = np.r_[ring[:1], ring[1:][::-1]]
        i_m = len(ring) - 1
    side = np.c_[ring[:i_m + 1], np.full(i_m + 1, BASE_TOP_Z)]
    # dense resample, then pair by angle
    side = _resample(np.r_[side, side[-1:]], 2000)
    side = np.r_[side, [np.r_[ring[i_m], BASE_TOP_Z]]]
    a_end = math.asin(GUSSET_HALF_WIDTH / r)
    arc = np.array([seat + e_v * (r * math.sin(a)) - e_up * (r * math.cos(a))
                    for a in np.linspace(a_end, -a_end, 2000)])
    n = GUSSET_POINTS
    # pair by angle: bottom around the middle of the cut line, top around the middle of the chord
    cb = np.array([u_cut, 0, BASE_TOP_Z])
    ct = seat - e_up * (r * math.cos(a_end))          # middle of the chord
    ab = np.linspace(-math.pi / 2, math.pi / 2, n)
    pb = _pair_by_angle(side, cb, np.array([-1.0, 0, 0]), -e_v, ab)
    pt = _pair_by_angle(arc, ct, -e_up, -e_v, ab)
    pb[0], pb[-1] = side[0], side[-1]
    pt[0], pt[-1] = arc[0], arc[-1]
    bottom = cq.Wire.assembleEdges([cq.Edge.makeLine(Vector(*pb[-1]), Vector(*pb[0])), _spline(pb)])
    top = cq.Wire.assembleEdges([cq.Edge.makeLine(Vector(*pt[-1]), Vector(*pt[0])), _spline(pt)])
    return cq.Solid.makeLoft([bottom, top], True)


def under_cup_local():
    """Below the cup: the footprint extruded up (sides lean inward by DRAFT_DEG), kept on the
    outer side of the seat plane and below the plane through the cup axis."""
    prism = cq.Solid.extrudeLinear(footprint_face(), Vector(0, 0, 30), taper=DRAFT_DEG)
    outer_of_seat = halfspace_below(SEAT_LOCAL, -D_LOCAL)
    below_mid = halfspace_below(SEAT_LOCAL, Vector(math.cos(T), 0, math.sin(T)))
    return prism.intersect(outer_of_seat).intersect(below_mid)


def halfspace_below(point, normal):
    """Solid of the points p with normal . (p - point) <= 0 (inside a 400 mm box)."""
    n = normal.normalized()
    box = cq.Solid.makeBox(400, 400, 400, Vector(-200, -200, -400))
    z = Vector(0, 0, 1)
    ax = z.cross(n)
    if ax.Length > 1e-9:
        box = box.rotate(Vector(0, 0, 0), ax, math.degrees(math.acos(max(-1, min(1, z.dot(n))))))
    return box.translate(point)


def arm_local():
    body = under_cup_local().fuse(gusset_local()).fuse(cup_local())
    for c in cup_cuts_local():
        body = body.cut(c)
    return body


def make_base():
    arm = cq.importers.importStep(GOTOKU + "gotoku55-arm-split-metal.step").val()
    keep = cq.Solid.makeBox(200, 200, BASE_TOP_Z, Vector(-100, -100, 0))
    return arm.intersect(keep).clean()


def make_arm():
    base = make_base()
    parts = [to_global(arm_local(), a) for a in AZIMUTHS]
    arm = base
    for p in parts:
        arm = arm.fuse(p)
    return arm, parts


if __name__ == "__main__":
    arm, parts = make_arm()
    print("valid", arm.isValid(), "solids", len(arm.Solids()), "volume %.1f" % arm.Volume())
    cq.exporters.export(arm, "gotoku55-btu-arm.step")
    cq.exporters.export(arm, "gotoku55-btu-arm.stl", tolerance=0.01, angularTolerance=0.1)
    print("cup length %.1f" % CUP_LEN)
