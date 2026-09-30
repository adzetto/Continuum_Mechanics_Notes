r"""fig04_geom.py -- geometry of fig04: the course body cut by the three
orthogonal planes x = XC, y = YQ, z = ZQ through Q (the octant piece of
fig03 b: same body, same Q), with a small cube element at the corner Q.
House camera az 35 / el 20.4 (= fig05).  Writes fig04_geom.tex (page pt).
Run:  python fig04_geom.py      (imports fig03_geom.py from this folder)
"""
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fig03_geom as F3  # noqa: E402
G = F3.G

SCALE = 56.0          # pt per model unit (fig03 b: 28 -> the same piece enlarged 2x)
EDGE = 0.25           # element edge (model units) = 14 pt, 13 % of the body width
TRIAD = (22.0, 13.0)  # triad origin: right of the tip L, above the lowest point B (pt)

if __name__ == '__main__':
    out = []
    F, sil = F3.octant_tex(out, 'D', SCALE, (0, 0))
    Q = F['Q']
    ex, ey, ez = np.eye(3) * EDGE
    V = {'Q': Q, 'X': Q - ex, 'Y': Q - ey, 'Z': Q - ez,
         'XY': Q - ex - ey, 'XZ': Q - ex - ez, 'YZ': Q - ey - ez}
    for k, P in V.items():
        G.tex_def(out, 'E' + k, G.fmt(F3.page(P, SCALE, (0, 0))))
    x0, y0, x1, y1 = sil.bounds
    Lp, Qp = F3.page(F['L'], SCALE, (0, 0)), F3.page(Q, SCALE, (0, 0))
    G.tex_def(out, 'Dtriad', G.fmt((Lp[0] + TRIAD[0], y0 + TRIAD[1])))
    open(os.path.join(HERE, 'fig04_geom.tex'), 'w').write('\n'.join(out) + '\n')
    print('fig04: body %.1f x %.1f pt (aspect %.2f), Q at %.0f %% of the width, %.0f %% from the top;'
          ' element edge %.1f pt (%.0f %% of the body width)'
          % (x1 - x0, y1 - y0, (x1 - x0) / (y1 - y0), 100 * (Qp[0] - x0) / (x1 - x0),
             100 * (y1 - Qp[1]) / (y1 - y0), EDGE * SCALE, 100 * EDGE * SCALE * 1.393 / (x1 - x0)))
