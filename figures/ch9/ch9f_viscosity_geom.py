r"""ch9f_viscosity_geom.py -- geometry of Figure F of Chapter 9: the two test
motions of (9.79) and the viscous tractions they call for.

Panel a: pure dilatation, D = (1/3)(tr D) I.  The square element and,
dashed, its image a moment later (uniformly larger); on every face the
viscous traction kappa (tr D) n, normal and outward.
Panel b: pure shear, D = Dev D.  The element and, dashed, its sheared image;
on the faces the shear tractions 2 mu D12, parallel to the faces and
3.9 pt outside them, as the shear stresses of the course figures.
The tractions are those that act on the element: they point the way the
faces move, so that they do positive work, which is the dissipation.
Writes ch9f_viscosity_geom.tex.
"""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fs9geom as G  # noqa: E402

H = 18.0              # pt, half-side of the element
GROW = 5.0            # pt, growth of the half-side in panel a (exaggerated)
SHIFT = 5.0           # pt, shift of the top face in panel b (exaggerated)
NRM = 16.0            # pt, normal tractions
SH = 16.0             # pt, shear tractions (shaft + tip)
OUT = 3.9             # pt, shear arrows outside their faces
GAPF = 0.6
XB = 142.0
out = G.Out()


def square(c, h):
    return [c + G.vec(-h, -h), c + G.vec(h, -h), c + G.vec(h, h), c + G.vec(-h, h)]


o = G.vec(0, 0)
out.raw('Fela', G.path(square(o, H), cycle=True))
out.raw('Fgrow', G.path(square(o, H + GROW), cycle=True))
for nm, u in (('r', G.vec(1, 0)), ('l', G.vec(-1, 0)), ('t', G.vec(0, 1)),
              ('b', G.vec(0, -1))):
    out.seg('Fn' + nm, o + (H + GAPF) * u, o + (H + GAPF + NRM) * u)
out.pt('Fnlab', o + G.vec(H + GAPF + NRM + 2.0, 0.0))
out.pt('Funda', o + G.vec(0, -H - GAPF - NRM - 9.0))
ob = G.vec(XB, 0)
out.raw('Felb', G.path(square(ob, H), cycle=True))
sh = [ob + G.vec(-H - SHIFT, -H), ob + G.vec(H - SHIFT, -H),
      ob + G.vec(H + SHIFT, H), ob + G.vec(-H + SHIFT, H)]
out.raw('Fshear', G.path(sh, cycle=True))
out.seg('Fst', ob + G.vec(-SH / 2, H + OUT), ob + G.vec(SH / 2, H + OUT))
out.seg('Fsb', ob + G.vec(SH / 2, -H - OUT), ob + G.vec(-SH / 2, -H - OUT))
out.seg('Fsr', ob + G.vec(H + OUT, -SH / 2), ob + G.vec(H + OUT, SH / 2))
out.seg('Fsl', ob + G.vec(-H - OUT, SH / 2), ob + G.vec(-H - OUT, -SH / 2))
out.pt('Fslab', ob + G.vec(0, H + OUT + 3.0))
out.pt('Fundb', ob + G.vec(0, -H - GAPF - NRM - 9.0))
out.pt('Fpanela', G.vec(-H - NRM - 10.0, -H - NRM - 38.0))
out.pt('Fpanelb', G.vec(XB - H - NRM - 10.0, -H - NRM - 38.0))
out.write(os.path.join(HERE, 'ch9f_viscosity_geom.tex'))
print('ch9f_viscosity: element %.0f pt' % (2 * H))
