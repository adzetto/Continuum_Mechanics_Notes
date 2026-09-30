r"""ch9a_frames_geom.py -- geometry of Figure A of Chapter 9: one particle p,
seen by O+ (panel a) and recorded by O under two relative motions (panel b).

Model data, in units of U pt:
  panel a (space of O+):  o+ = (0,0), o1 = (1.2,2.9), o2 = (4.0,-1.4),
                          p = (6.0,3.2); the basis of O appears turned by
                          alpha1 = -15 deg (first relative motion) and
                          alpha2 = 12 deg (second);
  panel b (space of O):   x_k = R(-alpha_k)(p - o_k),  Q = R(alpha1-alpha2),
                          d = R(-alpha2)(o1 - o2).
Asserted: Q x1 + d = x2 (this is (9.12)), |d| = |c1 - c2|, and
Q1 x_k + c_k = x+ for both k (this is (9.6)).
Writes ch9a_frames_geom.tex next to this file.
"""
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, 'common'))
import fsgeom as G  # noqa: E402

U = 19.0                 # pt per model unit
BASIS = 17.0             # pt, drawn length of a basis vector
XB = 152.0               # pt, x-offset of panel b
LAB = 3.4                # pt, gap between a vector and its label box

op, o1, o2, p = G.vec(0, 0), G.vec(1.2, 2.9), G.vec(4.0, -1.4), G.vec(6.0, 3.2)
a1, a2 = -15.0, 12.0
Q1, Q2 = G.rot(a1), G.rot(a2)
x1 = Q1.T @ (p - o1)
x2 = Q2.T @ (p - o2)
Q = Q2.T @ Q1
d = Q2.T @ (o1 - o2)
assert np.allclose(Q @ x1 + d, x2)
assert np.allclose(Q1 @ x1 + o1, p) and np.allclose(Q2 @ x2 + o2, p)
assert abs(np.linalg.norm(d) - np.linalg.norm(o1 - o2)) < 1e-12
beta = a1 - a2

out = G.Out()


def anchor_for(n):
    """TikZ anchor of a label placed on the side n of a line."""
    a = math.degrees(math.atan2(n[1], n[0])) % 360
    names = ['west', 'south west', 'south', 'south east', 'east',
             'north east', 'north', 'north west']
    return names[int(((a + 22.5) % 360) // 45)]


def vector(name, a, b, trim_a, trim_b, t, side, off=LAB):
    """An arrow a->b (page pt) trimmed at the ends, and a label beside it at
    fraction t, on the left (side=+1) or right (side=-1) of the arrow."""
    s, e = G.trimmed(a, b, trim_a, trim_b)
    out.seg('A' + name, s, e)
    n = side * G.normal(b - a)
    lab = a + t * (b - a) + off * n
    out.pt('A' + name + 'L', lab)
    out.raw('A' + name + 'N', anchor_for(n))


T = G.R_POINT + G.GAP
# ---------------------------------------------------------------- panel a --
P = {k: U * v for k, v in dict(op=op, oone=o1, otwo=o2, p=p).items()}
for k, v in P.items():
    out.pt('A' + k, v)
vector('cone', P['op'], P['oone'], T, T, 0.52, +1)
vector('ctwo', P['op'], P['otwo'], T, T, 0.55, -1)
vector('xplus', P['op'], P['p'], T, T, 0.60, -1)
vector('Qxone', P['oone'], P['p'], T, T, 0.42, +1)
vector('Qxtwo', P['otwo'], P['p'], T, T, 0.45, -1)
bases = []
for org, ang in ((P['op'], 0.0), (P['oone'], a1), (P['otwo'], a2)):
    for k in (0, 1):
        u = G.rot(ang + 90.0 * k) @ G.vec(1, 0)
        bases.append('%s -- %s' % (G.fmt(org + T * u), G.fmt(org + BASIS * u)))
out.raw('Abasesa', ' '.join('\\draw[fs axis] %s;' % b for b in bases))
# ---------------------------------------------------------------- panel b --
ob = G.vec(XB, 0.0)
X1, X2, QX1 = ob + U * x1, ob + U * x2, ob + U * (Q @ x1)
out.pt('Ao', ob)
vector('xone', ob, X1, T, 0.0, 0.62, +1)
vector('xtwo', ob, X2, T, 0.0, 0.50, +1)
vector('Qxonep', ob, QX1, T, 0.0, 0.62, -1)
vector('d', QX1, X2, 0.0, 0.0, 0.20, -1)
bb = []
for k in (0, 1):
    u = G.rot(90.0 * k) @ G.vec(1, 0)
    bb.append('%s -- %s' % (G.fmt(ob + T * u), G.fmt(ob + BASIS * u)))
out.raw('Abasesb', ' '.join('\\draw[fs axis] %s;' % b for b in bb))
phi1 = math.degrees(math.atan2(x1[1], x1[0]))
R_ARC = 31.0
arcP = G.arc(ob, R_ARC, phi1, phi1 + beta)
out.raw('AQarc', G.path(arcP))
mid = phi1 + beta / 2.0
out.pt('AQlab', ob + (R_ARC + 4.0) * G.vec(math.cos(math.radians(mid)),
                                            math.sin(math.radians(mid))))
# ------------------------------------------------------------ panel letters --
ymin = min(P['otwo'][1], QX1[1]) - 18.0
out.pt('Apanela', G.vec(-14.0, ymin))
out.pt('Apanelb', G.vec(XB - 14.0, ymin))
out.write(os.path.join(HERE, 'ch9a_frames_geom.tex'))
print('ch9a_frames: x1 = (%.3f, %.3f), x2 = (%.3f, %.3f), turn of Q %.1f deg, |d| = %.3f'
      % (x1[0], x1[1], x2[0], x2[1], beta, np.linalg.norm(d)))
