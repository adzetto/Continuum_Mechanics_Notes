r"""ch9d_coaxial_geom.py -- geometry of Figure D of Chapter 9: the stretching D
and the stress G(D) share their principal axes (Part 2 of Section 9.1.1).

Panel a: a rectangular element with sides along nu1, nu2 (the triad at its
lower left corner); the faces normal to nu1 move apart (eta1 > 0), those
normal to nu2 move together (eta2 < 0).  Panel b: the same element; the
tractions on its faces are normal to them (beta1, beta2), no shear traction
acts on them (tau = 0).  Arrows sit at the face centres, as in the course
figures; the principal directions are shown by a triad clear of the arrows.
Writes ch9d_coaxial_geom.tex.
"""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, 'common'))
import fsgeom as G  # noqa: E402

HX, HY = 22.0, 14.0      # pt, half-sides of the element
TRI = 14.0               # pt, triad arrows
VEL = 11.0               # pt, velocity arrows
STR = 15.0               # pt, traction arrows
GAPF = 0.6               # pt, gap between a face and an arrow that starts on it
XB = 172.0               # pt, centre of panel b

out = G.Out()
for tag, c in (('a', 0.0), ('b', XB)):
    o = G.vec(c, 0)
    out.raw('Del' + tag, G.path([o + G.vec(-HX, -HY), o + G.vec(HX, -HY),
                                 o + G.vec(HX, HY), o + G.vec(-HX, HY)],
                                cycle=True))
    t = o + G.vec(-HX - 20.0, -HY - 14.0)
    out.seg('Dtrione' + tag, t, t + G.vec(TRI, 0))
    out.seg('Dtritwo' + tag, t, t + G.vec(0, TRI))
    out.pt('Dnuone' + tag, t + G.vec(TRI + 1.8, 0))
    out.pt('Dnutwo' + tag, t + G.vec(0, TRI + 1.8))
o = G.vec(0, 0)
out.seg('Dvr', o + G.vec(HX + GAPF, 0), o + G.vec(HX + GAPF + VEL, 0))
out.seg('Dvl', o + G.vec(-HX - GAPF, 0), o + G.vec(-HX - GAPF - VEL, 0))
out.seg('Dvt', o + G.vec(0, HY + GAPF + VEL), o + G.vec(0, HY + GAPF))
out.seg('Dvb', o + G.vec(0, -HY - GAPF - VEL), o + G.vec(0, -HY - GAPF))
out.pt('Detaone', o + G.vec(HX + GAPF + VEL + 2.0, 0))
out.pt('Detatwo', o + G.vec(3.0, HY + GAPF + VEL - 1.0))
o = G.vec(XB, 0)
out.seg('Dsr', o + G.vec(HX + GAPF, 0), o + G.vec(HX + GAPF + STR, 0))
out.seg('Dsl', o + G.vec(-HX - GAPF, 0), o + G.vec(-HX - GAPF - STR, 0))
out.seg('Dst', o + G.vec(0, HY + GAPF), o + G.vec(0, HY + GAPF + STR))
out.seg('Dsb', o + G.vec(0, -HY - GAPF), o + G.vec(0, -HY - GAPF - STR))
out.pt('Dbetaone', o + G.vec(HX + GAPF + STR + 2.0, 0))
out.pt('Dbetatwo', o + G.vec(3.5, HY + GAPF + STR - 1.0))
out.pt('Dtau', o + G.vec(HX + 3.5, -5.5))
m0, m1 = HX + GAPF + VEL + 34.0, XB - HX - GAPF - STR - 10.0
out.seg('Dmap', G.vec(m0, 0), G.vec(m1, 0))
out.pt('Dmaplab', G.vec((m0 + m1) / 2.0, 4.5))
out.pt('Dpanela', G.vec(-HX - 24.0, -HY - 34.0))
out.pt('Dpanelb', G.vec(XB - HX - 24.0, -HY - 34.0))
out.write(os.path.join(HERE, 'ch9d_coaxial_geom.tex'))
print('ch9d_coaxial: element %.0f x %.0f pt, map arrow %.0f pt' % (2 * HX, 2 * HY, m1 - m0))
