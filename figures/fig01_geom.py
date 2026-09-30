r"""fig01_geom.py -- geometry of fig01 (potato body under distributed loads,
crossed by a transverse cutting plane), house camera az 35 / el 20.4.
Writes fig01_geom.tex next to this file: \def macros in PAGE POINTS, used
by fig01_body.tex inside \begin{scope}[x=1pt,y=1pt].

Run:  python fig01_geom.py      (deterministic; needs ../style/v3/fsgeom.py)

Body: fsgeom.course_potato() (the body of fig01-fig03: pear along x, small
round lobe left, big lobe right, concave neck; organic but calm), 29 pt per
model unit.  Plane x = XC through the neck, overhang 1.30.
Loads (as sketched): q1 on top of the small lobe (5 arrows, pressure),
q2 on its lower-left flank (3 arrows, pressure), q3 under the big lobe
(4 arrows, tension).  Support: hatch along the right end.

Finalised from the v3.1 specimen (FIGS/specimens/figs/fig01_geom.py):
- the glass in front of the small lobe now covers the whole outline stroke
  of the part behind the plane and stops 0.26 pt short of the outline of the
  part in front of it (the specimen ended it on the stroke centre: half-grey
  outlines at 1200 dpi);
- the hidden (far) rim arc drops the ends that run within 1.1 pt of the
  outline, and its dash pattern is stretched by < 5 % so that it starts and
  ends with a whole dash (the specimen had a dash lying on the silhouette at
  the top and a dot-sized dash at the bottom).
"""
import os
import sys

import numpy as np
from shapely.geometry import Polygon

sys.dont_write_bytecode = True                        # no __pycache__ in style/v3
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'style', 'v3'))
import fsgeom as G  # noqa: E402

BODY, XC = G.course_potato()   # the one body shared by fig01/fig02/fig03; plane x = XC
SCALE = 29.0        # pt per model unit -> body about 5.6 cm wide
CAM = G.HOUSE
LOAD = 13.0         # pt, arrow length of the area loads
out = []

# ---- body outline ---------------------------------------------------------
ring = G.orient_cw(G.smooth_ring(BODY.outline(CAM, SCALE), n=900, tol=0.02))
xr = ring[:, 0].min() + 0.62 * np.ptp(ring[:, 0])          # seam on the unloaded top
k0 = int(np.argmin(np.where(np.abs(ring[:, 0] - xr) < 1.5, -ring[:, 1], 9e9)))
ring = np.roll(ring, -k0, 0)
G.tex_def(out, 'Fbody', G.tex_path(ring, cycle=True))
xL, W = ring[:, 0].min(), np.ptp(ring[:, 0])

# ---- cutting plane ----------------------------------------------------------
quad3 = G.plane_quad_x(BODY, XC, 1.30)
quad = CAM.page(quad3, SCALE)
parts = G.plane_parts(BODY, CAM, quad3, XC, SCALE)
G.tex_def(out, 'Fquad', G.tex_path(quad, cycle=True))
# glass in front of the small lobe: it covers the WHOLE outline stroke of the part
# behind the plane and stops short of the outline of the part in front of it
# (fsgeom's 'front' ends on the stroke centre: half-grey outlines at 1200 dpi)
front = (Polygon(quad).intersection(parts['whole'].buffer(0.35, join_style=1))
         .difference(parts['occ'].buffer(0.26, join_style=1)))
G.tex_def(out, 'Fplanefront', G.tex_poly(front))
G.tex_def(out, 'Fplaneedges', G.tex_poly(parts['edges']))
vis, hid, rim = G.rim_runs(BODY, CAM, XC, SCALE)
# the hidden arc meets the outline tangentially: drop its ends that run within
# 1.1 pt of the outline (a dash lying on the outline reads as a blob)
dense = G.resample(ring, 4000)
near = lambda r: np.hypot(*(dense[None, :, :] - r[:, None, :]).transpose(2, 0, 1)).min(axis=1) < 1.1
trimmed = []
for r in hid:
    k = np.nonzero(~near(r))[0]
    if len(k) > 3:
        trimmed.append(r[k[0]:k[-1] + 1])
hid = trimmed
# dash pattern of fs hidden (2.6 / 1.9 pt) stretched by < 5 % so that the arc
# starts and ends with a whole dash (no dot-sized dash at an end)
L = sum(G.arc_param(r)[-2] for r in hid) if len(hid) == 1 else None
k = L / (round((L - 2.6) / 4.5) * 4.5 + 2.6) if L else 1.0
out.append('\\tikzset{fig01 hidden dash/.style={dash pattern=on %.3fpt off %.3fpt}}' % (2.6 * k, 1.9 * k))
G.tex_def(out, 'Frimvis', ' '.join(G.tex_path(r) for r in vis))
G.tex_def(out, 'Frimhid', ' '.join(G.tex_path(r) for r in hid))
G.tex_def(out, 'Fsection', G.tex_path(rim[::4], cycle=True))
for nm, p in zip(('FB', 'FT', 'BT', 'BB'), quad):
    G.tex_def(out, 'Fq' + nm, G.fmt(p))

# ---- loads -------------------------------------------------------------------
per = G.arc_param(ring)[-1]
xFT = quad[1][0]
q1 = G.load_row(ring, G.s_at_x(ring, xL + 8.0, 'top'), G.s_at_x(ring, xFT - 7.0, 'top'), 5, LOAD)
q2 = G.load_row(ring, G.s_at_x(ring, xL + 40.0, 'bottom'), G.s_at_x(ring, xL + 17.0, 'bottom'), 3, LOAD)
xm = xL + 0.63 * W
q3 = G.load_row(ring, G.s_at_x(ring, xm + 17.5, 'bottom'), G.s_at_x(ring, xm - 17.5, 'bottom'), 4, LOAD,
                tension=True)
for nm, q in (('one', q1), ('two', q2), ('three', q3)):
    out.append('\\def\\Fq%sarrows#1{%s}' % (nm, ' '.join(
        '\\draw[#1] %s -- %s;' % (G.fmt(a), G.fmt(b)) for a, b in q['arrows'])))
    G.tex_def(out, 'Fq%senv' % nm, G.tex_path(q['envelope']))
    G.tex_def(out, 'Fq%sblock' % nm, G.tex_path(q['block'], cycle=True))

# ---- support: hatch along the right end --------------------------------------
S = G.arc_param(ring)
cand = []
for s in np.arange(0, per, 0.5):
    p, u = G.at_arc(ring, s)
    nrm = np.array([-u[1], u[0]])
    a = np.degrees(np.arctan2(nrm[1], nrm[0]))
    if -40 < a < 50 and p[0] > xL + 0.78 * W:
        cand.append(s)
cand = np.array(cand)
run = max(np.split(cand, np.nonzero(np.diff(cand) > 2.0)[0] + 1), key=len)
strokes, sline = G.hatch_along(ring, run[0] + 1.5, run[-1] - 1.5, 2.9, 5.6, 40)
G.tex_def(out, 'Fsupport', ' '.join('%s -- %s' % (G.fmt(a), G.fmt(b)) for a, b in strokes))

# ---- label anchor: next to the back-top corner of the plane --------------------
G.tex_def(out, 'Flabel', G.fmt(quad[2] + np.array([12.0, 1.0])))
G.tex_def(out, 'Flabeltip', G.fmt(quad[2] + 0.16 * (quad[3] - quad[2])))   # the leader touches the plane edge

open(os.path.join(HERE, 'fig01_geom.tex'), 'w').write('\n'.join(out) + '\n')
print('fig01: body %.1f x %.1f pt; plane x = %.2f; rim visible %.0f %%; support %d strokes'
      % (W, np.ptp(ring[:, 1]), XC, 100 * sum(len(r) for r in vis) / len(rim), len(strokes)))
# ---- self-check (numbers for the report) --------------------------------------
_all = len(np.arange(run[0] + 1.5, run[-1] - 1.5, 2.9))
_ang = []
for a, b in strokes:
    s = S[int(np.argmin(np.hypot(*(ring - a).T)))]
    d = (b - a) / np.hypot(*(b - a))
    _ang.append(np.degrees(np.arcsin(np.clip(d @ G.outward_normal(ring, s, 2.0), -1, 1))))
print('  support: %d of %d strokes kept, smallest angle to the outline %.1f deg' % (len(strokes), _all, min(_ang)))
print('  hidden rim arc: %.1f pt, dash pattern stretched x %.3f' % (L, k))
for nm, q in (('q1', q1), ('q2', q2), ('q3', q3)):
    d = np.diff(q['envelope'], axis=0)
    t = np.degrees(np.abs(np.diff(np.unwrap(np.arctan2(d[:, 1], d[:, 0])))))
    print('  %s envelope: fit deviation %.2f pt, max turn %.2f deg/step' % (nm, q['fit_dev'], t.max()))
