r"""ch9g_couette_geom.py -- geometry of Figure G of Chapter 9: the steady
profiles of Problem 6(a),

    v1/V = xi + Pi xi (1 - xi),   xi = x2/d,   Pi = -P d^2 / (2 mu V),

between a fixed wall (x2 = 0) and a wall moving with speed V (x2 = d), for
Pi = -2, 0, 2, 4.  Asserted: every profile meets the no-slip conditions,
the slope at the fixed wall is (V/d)(1 + Pi), and backflow occurs exactly
for Pi < -1.  Walls carry the support hatch of the course figures.
Writes ch9g_couette_geom.tex.
"""
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, 'common'))
import fsgeom as G  # noqa: E402

SV = 64.0            # pt per V
SD = 74.0            # pt per d
XL, XR = -46.0, 112.0
HATCH_STEP, HATCH_LEN = 2.9, 5.0
PIS = (-2.0, 0.0, 2.0, 4.0)

out = G.Out()
xi = np.linspace(0.0, 1.0, 81)
curves = []
for k, Pi in enumerate(PIS):
    v = xi + Pi * xi * (1 - xi)
    assert abs(v[0]) < 1e-12 and abs(v[-1] - 1.0) < 1e-12
    h = xi[1] - xi[0]
    assert abs((v[1] - v[0]) / h - (1.0 + Pi * (1.0 - h))) < 1e-12
    assert (v.min() < 0) == (Pi < -1)
    P = np.column_stack([SV * v, SD * xi])
    curves.append(P)
    out.raw('Gc' + 'abcd'[k], G.path(P))
out.seg('Gwallb', G.vec(XL, 0), G.vec(XR, 0))
out.seg('Gwallt', G.vec(XL, SD), G.vec(XR, SD))
strokes = []
for x in np.arange(XL + 1.0, XR - 1.0, HATCH_STEP):
    strokes.append('%s -- %s' % (G.fmt(G.vec(x, 0)),
                                 G.fmt(G.vec(x - HATCH_LEN * 0.7071, -HATCH_LEN * 0.7071))))
    strokes.append('%s -- %s' % (G.fmt(G.vec(x, SD)),
                                 G.fmt(G.vec(x + HATCH_LEN * 0.7071, SD + HATCH_LEN * 0.7071))))
out.raw('Ghatch', ' '.join(strokes))
out.seg('Gaxis', G.vec(0, 0), G.vec(0, SD + 20.0))
out.pt('Gaxislab', G.vec(2.2, SD + 18.5))
out.seg('Gguide', G.vec(SV, 0), G.vec(SV, SD))
out.seg('GV', G.vec(SV - 24.0, SD + 12.0), G.vec(SV, SD + 12.0))
out.pt('GVlab', G.vec(SV + 2.5, SD + 12.0))
out.seg('Gdim', G.vec(XL + 8.0, 0.8), G.vec(XL + 8.0, SD - 0.8))
out.pt('Gdimlab', G.vec(XL + 5.0, SD / 2.0))
out.pt('Gzero', G.vec(0, -HATCH_LEN - 3.0))
out.pt('Gone', G.vec(SV, -HATCH_LEN - 3.0))
for k, Pi in zip('abcd', PIS):
    P = curves['abcd'.index(k)]
    if Pi == 0.0:
        i = int(round(0.62 * (len(xi) - 1)))
        out.pt('Gl' + k, P[i] + G.vec(-5.5, -1.5))
    elif Pi < 0:
        i = int(np.argmin(P[:, 0]))
        out.pt('Gl' + k, P[i] + G.vec(-3.0, 0))
    else:
        i = int(np.argmax(P[:, 0]))
        out.pt('Gl' + k, P[i] + G.vec(3.0, 0))
out.pt('Gpanel', G.vec(XL, -HATCH_LEN - 20.0))
out.write(os.path.join(HERE, 'ch9g_couette_geom.tex'))
print('ch9g_couette: backflow minimum at Pi = -2: v1/V = %.3f'
      % min(xi - 2 * xi * (1 - xi)))
