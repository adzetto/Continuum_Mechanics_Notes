r"""ch9e_rays_geom.py -- geometry of Figure E of Chapter 9: the two uses of
"for all" in Section 9.3.

Panel a: along the ray w = delta a(z) the left side of (9.64) is the affine
function delta |a|^2 + b; drawn for |a|^2 = 1, b = 0.8 (a != 0) and for
a = 0.  Panel b: along the ray D = s dD the function f of (9.71); a curve
with zero slope at s = 0 (0.8 s^2) and one with non-zero slope
(0.75 s + 0.25 s^2).  Negative values, which the inequalities forbid, are
shaded.  Unit U pt per unit on both axes.
Writes ch9e_rays_geom.tex.
"""
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, 'common'))
import fsgeom as G  # noqa: E402

U = 22.0
XB = 150.0
B = 0.8
out = G.Out()
# ------------------------------------------------------------------ a ------
x0, x1, y0, y1 = -2.3, 1.55, -1.45, 2.15
out.raw('Eregiona', G.path([G.vec(x0, 0) * U, G.vec(x1, 0) * U,
                            G.vec(x1, y0) * U, G.vec(x0, y0) * U], cycle=True))
out.seg('Eaxda', G.vec(x0 - 0.1, 0) * U, G.vec(x1 + 0.35, 0) * U)
out.seg('Eaxfa', G.vec(0, y0 - 0.05) * U, G.vec(0, y1 + 0.25) * U)
d = np.array([x0, y1 - B])
XE = 1.0
out.seg('Eline', G.vec(x0, x0 + B) * U, G.vec(XE, XE + B) * U)
out.seg('Eflat', G.vec(x0, B) * U, G.vec(x1, B) * U)
out.pt('Ecross', G.vec(-B, 0) * U)
out.pt('Elinelab', G.vec(XE, XE + B) * U + G.vec(2.5, -2.0))
out.pt('Eflatlab', G.vec(x1, B) * U + G.vec(2.5, 0))
out.pt('Eblab', G.vec(0, B) * U + G.vec(-2.5, 3.0))
out.pt('Ecrosslab', G.vec(-B, 0) * U + G.vec(-3.5, 3.0))
out.pt('Edlab', G.vec(x1 + 0.35, 0) * U + G.vec(2.0, 0))
out.pt('Eflab', G.vec(0, y1 + 0.25) * U + G.vec(2.5, -1.0))
# ------------------------------------------------------------------ b ------
o = G.vec(XB, 0)
s0, s1 = -2.0, 2.0
out.raw('Eregionb', G.path([o + G.vec(s0 - 0.2, 0) * U, o + G.vec(s1 + 0.2, 0) * U,
                            o + G.vec(s1 + 0.2, y0) * U, o + G.vec(s0 - 0.2, y0) * U],
                           cycle=True))
out.seg('Eaxsb', o + G.vec(s0 - 0.3, 0) * U, o + G.vec(s1 + 0.45, 0) * U)
out.seg('Eaxfb', o + G.vec(0, y0 - 0.05) * U, o + G.vec(0, y1 + 0.25) * U)
sa = np.linspace(-1.6, 1.6, 61)
out.raw('Eallowed', G.path([o + G.vec(s, 0.8 * s * s) * U for s in sa]))
se = np.linspace(-2.0, 1.25, 61)
out.raw('Eexcluded', G.path([o + G.vec(s, 0.75 * s + 0.25 * s * s) * U
                             for s in se]))
out.pt('Eallowedlab', o + G.vec(1.6, 0.8 * 1.6 ** 2) * U + G.vec(2.5, -1.5))
out.pt('Eexcludedlab', o + G.vec(1.25, 0.75 * 1.25 + 0.25 * 1.5625) * U
       + G.vec(2.5, -1.5))
out.pt('Eslab', o + G.vec(s1 + 0.45, 0) * U + G.vec(2.0, 0))
out.pt('Eflabb', o + G.vec(0, y1 + 0.25) * U + G.vec(2.5, -1.0))
out.pt('Eo', o)
out.pt('Epanela', G.vec(x0 * U - 6.0, y0 * U - 14.0))
out.pt('Epanelb', o + G.vec((s0 - 0.3) * U - 4.0, y0 * U - 14.0))
out.write(os.path.join(HERE, 'ch9e_rays_geom.tex'))
print('ch9e_rays: crossing at delta = -b/|a|^2 = %.2f' % (-B))
