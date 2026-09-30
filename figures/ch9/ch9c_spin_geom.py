r"""ch9c_spin_geom.py -- geometry of Figure C of Chapter 9: a square material
element with sides along the principal axes nu1, nu2 of D_*, and its image a
short time dt later (exaggerated), in the two descriptions of (9.18)-(9.20).

To first order in dt the image of the square [-A,A]^2 under I + dt L is the
rectangle of half-sides (1+e)A, (1-e)A turned through w dt, where
dt D_* = diag(e,-e) and dt W_* is the turn w dt; here e = 0.25 and
w dt = 20 deg.  In the second description Q-hat = I and Omega-hat = -W_*,
so the turn is removed and the stretch is kept.
Writes ch9c_spin_geom.tex.
"""
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, 'common'))
import fsgeom as G  # noqa: E402

A = 18.0              # pt, half-side of the square
E = 0.25              # stretch dt*eta, exaggerated
TURN = 20.0           # deg, w dt, exaggerated
AX = 37.0             # pt, half-length of the principal axes
XB = 176.0            # pt, centre of panel b

out = G.Out()
sq = np.array([[-A, -A], [A, -A], [A, A], [-A, A]])
rect = np.array([[-(1 + E) * A, -(1 - E) * A], [(1 + E) * A, -(1 - E) * A],
                 [(1 + E) * A, (1 - E) * A], [-(1 + E) * A, (1 - E) * A]])
turned = rect @ G.rot(TURN).T
for name, P, c in (('Csqa', sq, 0.0), ('Crecta', turned, 0.0),
                   ('Csqb', sq, XB), ('Crectb', rect, XB)):
    out.raw(name, G.path(P + G.vec(c, 0), cycle=True))
for tag, c in (('a', 0.0), ('b', XB)):
    o = G.vec(c, 0)
    out.seg('Caxone' + tag, o + G.vec(-AX, 0), o + G.vec(AX, 0))
    out.seg('Caxtwo' + tag, o + G.vec(0, -AX), o + G.vec(0, AX))
    out.pt('Cnuone' + tag, o + G.vec(AX + 2.0, 0))
    out.pt('Cnutwo' + tag, o + G.vec(2.5, AX - 1.0))
    out.pt('Cunder' + tag, o + G.vec(0, -AX - 5.0))
fibre = G.rot(TURN) @ G.vec(1, 0)
out.seg('Cfibre', -44.0 * fibre, 44.0 * fibre)
R = 31.0
out.raw('Cturn', G.path(G.arc(G.vec(0, 0), R, 180.0, 180.0 + TURN)))
mid = math.radians(180.0 + TURN / 2)
out.pt('Cturnlab', (R + 3.5) * G.vec(math.cos(mid), math.sin(mid)))
out.seg('Cmap', G.vec(56.0, 0), G.vec(XB - 54.0, 0))
out.pt('Cmaplab', G.vec((56.0 + XB - 54.0) / 2.0, 4.5))
out.pt('Cpanela', G.vec(-AX - 10.0, -AX - 26.0))
out.pt('Cpanelb', G.vec(XB - AX - 10.0, -AX - 26.0))
out.write(os.path.join(HERE, 'ch9c_spin_geom.tex'))
print('ch9c_spin: element %.0f pt, stretch %.2f, turn %.0f deg' % (2 * A, E, TURN))
