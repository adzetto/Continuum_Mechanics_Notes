r"""ch9h_annulus_geom.py -- geometry of Figure H of Chapter 9: circular Couette
flow, Problem 8.

Panel a: cross-section of the annulus, inner cylinder of radius a turning at
omega_a, outer cylinder of radius b turning at omega_b; the fluid between.
Panel b: v_theta = r f(r) = A r + B/r for b = 2a, omega_a fixed and three
rates of the outer cylinder: omega_b = omega_a (rigid, B = 0),
omega_b = omega_a a^2/b^2 = omega_a/4 (potential vortex, A = 0) and
omega_b = 0.  Asserted: the no-slip values at r = a, b, and that A = 0
exactly for omega_b/omega_a = a^2/b^2 (Problem 8(c)).
Writes ch9h_annulus_geom.tex.
"""
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fs9geom as G  # noqa: E402

RA, RB = 24.0, 48.0          # pt, radii in panel a
HATCH_STEP, HATCH_LEN = 2.9, 5.0
XB = 96.0                    # pt, origin (r = a, v = 0) of panel b
SX, SY = 72.0, 30.0          # pt per unit of r/a and of v/(a omega_a)

out = G.Out()
# ---------------------------------------------------------------- panel a --
c = G.vec(0, 0)
out.raw('Houter', G.path(G.arc(c, RB, 0, 360, 181)[:-1], cycle=True))
out.raw('Hinner', G.path(G.arc(c, RA, 0, 360, 121)[:-1], cycle=True))
strokes = []
n = int(2 * math.pi * RB / HATCH_STEP)
for k in range(n):
    t = 2 * math.pi * k / n
    p = c + RB * G.vec(math.cos(t), math.sin(t))
    nrm = G.vec(math.cos(t), math.sin(t))
    d = G.rot(45.0) @ nrm
    strokes.append('%s -- %s' % (G.fmt(p), G.fmt(p + HATCH_LEN * d)))
out.raw('Hhatch', ' '.join(strokes))
out.raw('Hwa', G.path(G.arc(c, 15.0, 35.0, 145.0)))
out.pt('Hwalab', c + G.vec(0, 8.2))
out.raw('Hwb', G.path(G.arc(c, RB + HATCH_LEN + 7.0, 40.0, 88.0)))
t = math.radians(64.0)
out.pt('Hwblab', c + (RB + HATCH_LEN + 10.0) * G.vec(math.cos(t), math.sin(t)))
T = G.R_POINT + G.GAP
ua, ub = G.rot(-40.0) @ G.vec(1, 0), G.rot(-140.0) @ G.vec(1, 0)
out.seg('Hda', c + T * ua, c + RA * ua)
out.seg('Hdb', c + T * ub, c + RB * ub)
out.pt('Hdalab', c + 0.52 * RA * ua + 5.0 * G.normal(ua))
out.pt('Hdblab', c + 0.72 * RB * ub - 5.0 * G.normal(ub))
out.pt('Hc', c)
out.pt('Hpanela', G.vec(-RB - 12.0, -RB - 18.0))
# ---------------------------------------------------------------- panel b --
a, b, wa = 1.0, 2.0, 1.0
o = G.vec(XB, -26.0)
cases = [('rigid', 1.0), ('vortex', a * a / (b * b)), ('rest', 0.0)]
r = np.linspace(a, b, 81)
for name, wb in cases:
    A = (b * b * wb - a * a * wa) / (b * b - a * a)
    B = a * a * b * b * (wa - wb) / (b * b - a * a)
    v = A * r + B / r
    assert abs(v[0] - a * wa) < 1e-12 and abs(v[-1] - b * wb) < 1e-12
    if name == 'vortex':
        assert abs(A) < 1e-12
    P = np.column_stack([o[0] + SX * (r - 1.0), o[1] + SY * v])
    out.raw('Hc' + name, G.path(P))
    dy = {'rigid': 0.0, 'vortex': 3.0, 'rest': 6.5}[name]
    out.pt('Hl' + name, P[-1] + G.vec(3.0, dy))
out.seg('Hax', o, o + G.vec(SX * 1.18, 0))
out.seg('Hay', o, o + G.vec(0, SY * 2.35))
out.pt('Haxlab', o + G.vec(SX * 1.18 + 1.0, -2.5))
out.pt('Haylab', o + G.vec(2.5, SY * 2.35 - 1.0))
ticks = []
for x in (1.0, 1.5, 2.0):
    p = o + G.vec(SX * (x - 1.0), 0)
    ticks.append('%s -- %s' % (G.fmt(p), G.fmt(p + G.vec(0, -2.5))))
    out.pt('Htx' + {1.0: 'a', 1.5: 'b', 2.0: 'c'}[x], p + G.vec(0, -4.5))
for y in (1.0, 2.0):
    p = o + G.vec(0, SY * y)
    ticks.append('%s -- %s' % (G.fmt(p), G.fmt(p + G.vec(-2.5, 0))))
    out.pt('Hty' + {1.0: 'a', 2.0: 'b'}[y], p + G.vec(-4.5, 0))
out.raw('Hticks', ' '.join(ticks))
out.pt('Hpanelb', G.vec(XB - 18.0, -RB - 18.0))
out.write(os.path.join(HERE, 'ch9h_annulus_geom.tex'))
print('ch9h_annulus: b = 2a; irrotational for omega_b/omega_a = %.3f' % (a * a / (b * b)))
