r"""fig02_geom.py -- geometry of fig02: the LEFT part (x <= XC) of the fig01
body as a free body -- loads q1, q2 (identical to fig01), the cut face x = XC
with the internal forces, the area element Delta A with its zoom callout and
the enlarged detail (axes x, y, z and the components Delta F_x, _y, _z).
House camera az 35 / el 20.4, 29 pt per model unit (= fig01).
Writes fig02_geom.tex next to this file: \def macros in PAGE POINTS, used by
fig02_body.tex inside \begin{scope}[x=1pt,y=1pt].

Run:  python fig02_geom.py      (deterministic; needs ../style/v3/fsgeom.py)

fig02 is drawn at 42 pt per model unit (1.45 x fig01) so that the cut face has
room for a dense, collision-free field of internal forces.

Internal forces: the traction t = (sigma, tau_y, tau_z) on the +x face, all
arrows leaving the face (tail on the face):
  sigma = 0.90 + 0.10 u   (tension everywhere, slightly larger at the top)
  tau_y = 0.12 + 0.16 u,  tau_z = 0.05 + 0.04 v   (a gentle fan)
with (u, v) = ((y - yc)/ry, (z - zc)/rz). The roots form a staggered lattice
(rows du = 0.27, pitch dv = 0.38); each row's phase was chosen by a layout
search so that every arrowhead keeps clear of the rim, no arrow touches the
Delta A circle, the zoom tangents or the inside of the zoom cone, and no two arrows come closer than 3.5 pt.
The lattice points skipped are those next to Delta A and inside the zoom cone.
All of this is asserted below.
"""
import os
import sys

import numpy as np
from shapely.geometry import Point, Polygon

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'style', 'v3'))
import fsgeom as G  # noqa: E402

BODY, XC = G.course_potato()   # the body of fig01/fig02/fig03; cut x = XC
SCALE = 42.0                   # pt per model unit (1.45 x fig01)
S29 = SCALE / 29.0             # load rows and Delta A were designed at 29 pt per unit
CAM = G.HOUSE
LOAD = 13.0                    # pt, arrow length of the area loads (= fig01)
EX, EY, EZ = CAM.EX, CAM.EY, CAM.EZ
out = []


def P(name, p):
    G.tex_def(out, name, G.fmt(p))


def unit(v):
    return v / np.hypot(*v)


def segdist(a, b, c, d, n=60):
    """smallest distance between the segments a-b and c-d (sampled)"""
    s = np.linspace(0, 1, n)[:, None]
    P1, P2 = a + s * (b - a), c + s * (d - c)
    return np.hypot(*(P1[:, None, :] - P2[None, :, :]).transpose(2, 0, 1)).min()


# ---- q1, q2 exactly as in fig01 (same ring, same calls) -------------------------
ring = G.orient_cw(G.smooth_ring(BODY.outline(CAM, SCALE), n=900, tol=0.02))
xr = ring[:, 0].min() + 0.62 * np.ptp(ring[:, 0])
k0 = int(np.argmin(np.where(np.abs(ring[:, 0] - xr) < 1.5, -ring[:, 1], 9e9)))
ring = np.roll(ring, -k0, 0)
xL, W = ring[:, 0].min(), np.ptp(ring[:, 0])
quad = CAM.page(G.plane_quad_x(BODY, XC, 1.30), SCALE)
xFT = quad[1][0]
q1 = G.load_row(ring, G.s_at_x(ring, xL + 8.0 * S29, 'top'), G.s_at_x(ring, xFT - 7.0 * S29, 'top'),
                7, LOAD)
q2 = G.load_row(ring, G.s_at_x(ring, xL + 40.0 * S29, 'bottom'), G.s_at_x(ring, xL + 17.0 * S29, 'bottom'),
                4, LOAD)
for nm, q in (('one', q1), ('two', q2)):
    out.append(r'\def\Gq%sarrows#1{%s}' % (nm, ' '.join(
        r'\draw[#1] %s -- %s;' % (G.fmt(a), G.fmt(b)) for a, b in q['arrows'])))
    G.tex_def(out, 'Gq%senv' % nm, G.tex_path(q['envelope']))
    G.tex_def(out, 'Gq%sblock' % nm, G.tex_path(q['block'], cycle=True))

# ---- the left part x <= XC ---------------------------------------------------------
lring = G.orient_cw(G.smooth_ring(BODY.outline(CAM, SCALE, clips=[((1.0, 0, 0), XC)]),
                                  n=900, tol=0.02))
lring = np.roll(lring, -int(np.argmax(lring[:, 0])), 0)      # seam on the cut face
G.tex_def(out, 'Gbody', G.tex_path(lring, cycle=True))

# ---- cut face: the section x = XC (outward normal +x, it faces the viewer) --------
face = CAM.page(BODY.section(XC, 720), SCALE)
G.tex_def(out, 'Gface', G.tex_path(face[::2], cycle=True))
ry, rz, yc, zc = BODY.radii(XC)


def fp(u, v):
    """page point of the face at local (u, v) = ((y-yc)/ry, (z-zc)/rz)"""
    return CAM.page(np.array([XC, yc + ry * u, zc + rz * v]), SCALE)


# ---- Delta A on the face and the zoom callout ------------------------------------
UM, VM = 0.12, -0.50           # local position of Delta A (right half of the face)
AM, BM = 0.075 / S29, 0.09 / S29   # half sides (fractions of ry, rz): same page size as at 29
pc = [np.array([XC, yc + ry * (UM + sa * AM), zc + rz * (VM + sb * BM)])
      for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
G.tex_def(out, 'Gpatch', G.tex_path(CAM.page(np.array(pc), SCALE), cycle=True))
mark = fp(UM, VM)
RMARK, RZOOM = 4.6, 39.3       # \FigZoom radii (pt)
ZOOM = mark + np.array([95.0, 0.0])        # detail circle at the height of Delta A
P('Gmark', mark)
P('Gzoom', ZOOM)
out.append(r'\def\Grmark{%.2fpt}\def\Grzoom{%.2fpt}\def\Grzoomin{%.2fpt}'
           % (RMARK, RZOOM, RZOOM - 0.2))
dv = ZOOM - mark
phi, al = np.arctan2(dv[1], dv[0]), np.arcsin((RZOOM - RMARK) / np.hypot(*dv))
tang = [(mark + RMARK * np.array([np.cos(a), np.sin(a)]), ZOOM + RZOOM * np.array([np.cos(a), np.sin(a)]))
        for a in (phi + np.pi / 2 + al, phi - np.pi / 2 - al)]

# ---- internal forces: staggered lattice on the face, every arrow leaves the face -----
S0, S1, T0, KY, Z0, KZ = 0.90, 0.10, 0.12, 0.16, 0.05, 0.04
LF = 20.0                      # pt per traction unit
ROOTS = [(-0.54, -0.6321), (-0.54, 0.1279), (-0.54, 0.5079),
         (-0.27, -0.1282), (-0.27, 0.2518), (-0.27, 0.6318),
         (0.00, -0.0800), (0.00, 0.3000), (0.00, 0.6800),
         (0.27, 0.4102), (0.27, 0.7902),
         (0.54, -0.6321), (0.54, 0.1279), (0.54, 0.5079),
         (0.81, 0.0275)]
HEAD, HALF = 5.6, 1.3          # fs tip load: length, half width (pt)


def trac(u, v):
    return np.array([S0 + S1 * u, T0 + KY * u, Z0 + KZ * v])


CONE = Polygon([tang[0][0], tang[0][1], tang[1][1], tang[1][0]]).union(Point(*mark).buffer(RMARK)).buffer(1.8)
arr = []
for u, v in ROOTS:
    t = trac(u, v)
    a = fp(u, v)
    arr.append((a, a + LF * (t[0] * EX + t[1] * EY + t[2] * EZ)))
out.append(r'\def\Gfield#1{%s}' % ' '.join(r'\draw[#1] %s -- %s;' % (G.fmt(a), G.fmt(b))
                                             for a, b in arr))


def ringdist(P):
    return np.hypot(*(np.asarray(P)[:, None, :] - face[None, :, :]).transpose(2, 0, 1)).min(axis=1)


for a, b in arr:
    d = unit(b - a)
    head = b - np.linspace(0, HEAD, 12)[:, None] * d
    assert np.hypot(*(b - a)) >= 2 * HEAD + 0.4, 'arrow shorter than two tips'
    assert ringdist(head).min() >= HALF + 1.2, 'arrowhead too close to the rim'
    assert ringdist([a])[0] >= 2.5, 'root too close to the rim'
    assert min(np.hypot(*(p - mark)) for p in np.linspace(a, b, 60)) >= RMARK + 2.3, 'arrow meets Delta A circle'
    assert min(segdist(a, b, c, e) for c, e in tang) >= 2.5, 'arrow meets a zoom tangent'
    assert not any(CONE.contains(Point(*q)) for q in np.linspace(a, b, 30)), 'arrow inside the zoom cone'
assert min(segdist(*arr[i], *arr[j]) for i in range(len(arr)) for j in range(i + 1, len(arr))) >= 3.5
assert (trac(UM, VM) > 0).all(), 'the detail draws all components of Delta F positive'

# ---- the detail: Delta A enlarged, same camera; O = centroid of Delta A --------------
A_, B_ = 6.0, 6.5              # half sides of the enlarged patch (model pt)
F = np.array([23.0, 17.5, 23.0])   # drawn Delta F_x, _y, _z (model pt), positive senses
AX, GAP = 11.0, 1.5            # axis stub beyond each component tip (page pt), gap
O = ZOOM + np.array([-2.36, 2.69])  # content centred in the circle (fitted to the
                                    # label boxes of the compiled PDF, margin >= 2.4 pt)
dpc = [O + sa * A_ * EY + sb * B_ * EZ for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
P('GO', O)
G.tex_def(out, 'Gdpatch', G.tex_path(np.array(dpc), cycle=True))
tips = {}
for nm, e, f in (('x', EX, F[0]), ('y', EY, F[1]), ('z', EZ, F[2])):
    tip = O + f * e
    tips[nm] = tip
    P('GF%s' % nm, tip)
    P('GA%sa' % nm, tip + GAP * unit(e))
    P('GA%sb' % nm, tip + (GAP + AX) * unit(e))
P('GdAl', O + np.array([B_ * 0.574 + 1.0, 4.6]))   # Delta A: right of the patch (anchor west)
P('GFzl', tips['z'] + np.array([0.6, 1.4]))        # Delta F_z: above-left of its tip (south east)

# ---- label "internal forces": above the face, leader to the top tension arrow --------
LW, LH = 61.0, 7.2             # ink box of the label "internal forces" (pt, from fscheck)


def box_clear(c, pts, gap):
    lo, hi = c - np.array([LW / 2 + gap, LH / 2 + gap]), c + np.array([LW / 2 + gap, LH / 2 + gap])
    return not ((pts >= lo) & (pts <= hi)).all(axis=1).any()


obst = np.vstack([lring, face, q1['block'], q2['block']] +
                 [np.linspace(a, b, 40) for a, b in arr] + [np.linspace(c, e, 120) for c, e in tang])
best = None
for k, (a, b) in enumerate(arr):
    for f in np.linspace(0.45, 0.80, 8):
        tip = a + f * (b - a)
        if ringdist([tip])[0] < 1.8 or Polygon(face).contains(Point(*tip)):
            continue                                  # the leader ends on a part outside the face
        others = np.vstack([np.linspace(c, e, 40) for j, (c, e) in enumerate(arr) if j != k] +
                           [lring, face])
        for dy in np.linspace(11.0, 24.0, 14):
            for dx in np.linspace(-14.0, 14.0, 15):
                c = tip + np.array([dx, dy])
                foot = c - np.array([0.0, LH / 2 + 1.2])
                if not box_clear(c, obst, 2.4):
                    continue
                lead = np.linspace(foot, tip, 50)
                if np.hypot(*(lead[:, None, :] - others[None, :, :]).transpose(2, 0, 1)).min() < 1.6:
                    continue
                cost = np.hypot(dx, dy) + 0.6 * abs(dx)
                if best is None or cost < best[0]:
                    best = (cost, tip, c)
assert best is not None, 'no clean place for the label "internal forces"'
LT, LC = best[1], best[2]
P('Glabtip', LT)
P('Glab', LC)                                     # label centre

# ---- wavy pointer "Delta A" inside the detail: label below the enlarged patch, the
#      squiggle ends on its lower edge
P('GpAtip', O + np.array([1.0, -7.2]))
P('GpAlab', O + np.array([4.0, -21.0]))           # label centre
P('GpAfrom', O + np.array([3.0, -15.0]))          # squiggle start, 1.5 pt off the label

open(os.path.join(HERE, 'fig02_geom.tex'), 'w').write('\n'.join(out) + '\n')

# ---- self-check (numbers for the report) ---------------------------------------------
d = max(np.hypot(*(lring - p).T).min() for q in (q1, q2) for p in q['block'][:90])
aa = min(segdist(*arr[i], *arr[j]) for i in range(len(arr)) for j in range(i + 1, len(arr)))
hr = min(min(np.hypot(*(face - r).T).min() for r in np.linspace(b - 5.6 * unit(b - a), b, 8))
         for a, b in arr)
tg = min(segdist(a, b, c, e) for a, b in arr for c, e in tang)
mk = min(min(np.hypot(*(r - mark)) for r in np.linspace(a, b, 60)) for a, b in arr) - RMARK
print('fig02: left part %.1f x %.1f pt, cut face %.1f x %.1f pt; q1/q2 on its outline within %.2f pt'
      % (np.ptp(lring[:, 0]), np.ptp(lring[:, 1]), np.ptp(face[:, 0]), np.ptp(face[:, 1]), d))
print('  field: %d arrows, lengths %.1f-%.1f pt; arrow-arrow >= %.1f, head-rim >= %.1f, '
      'zoom tangents >= %.1f, Delta A circle >= %.1f pt'
      % (len(arr), min(np.hypot(*(b - a)) for a, b in arr), max(np.hypot(*(b - a)) for a, b in arr),
         aa, hr, tg, mk))
print('  Delta A circle to the rim %.1f pt; traction at Delta A (%.2f, %.2f, %.2f): all positive'
      % (np.hypot(*(face - mark).T).min() - RMARK, *trac(UM, VM)))
print('  detail: Delta F_x/_y/_z %.1f/%.1f/%.1f pt on the page; head bases beyond the patch edge '
      'by %.1f/%.1f pt' % (F[0] * np.hypot(*EX), F[1] * np.hypot(*EY), F[2] * np.hypot(*EZ),
                           F[1] * np.hypot(*EY) - 6.6 - A_ * np.hypot(*EY),
                           F[2] * np.hypot(*EZ) - 6.6 - B_ * np.hypot(*EZ)))
