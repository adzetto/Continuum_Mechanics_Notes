r"""fig06_geom.py -- exact visibility of the hidden-face tripods of fig06 -> fig06_geom.tex

The cube [0,a]^3 of fig05/fig06 (a = 66, house camera) is shown CUT OPEN
(language of fig09 b): its three negative faces x = 0, y = 0, z = 0 are the
cut faces, opaque, seen from inside; the positive faces are glass (outline
only).  Every tripod arrow of \FigStressCube[faces=negative] is split exactly
(fsgeom.visible_pieces, occluders = the three negative faces):
  - the six shear stresses lie on their own cut face: visible, solid;
  - the three normal stresses point away from the cube, behind it: dotted
    until they leave the silhouette, then solid with a solid head.  Their
    model lengths are set so that the solid shaft before the head is 9 pt
    (v3.3: 11 pt; lengths 36 / 21 as fig05).
Roots, shear length, floor and tip exactly as in fig06_body.tex.  Writes the
keys /fs/cube/fig06 (length <kk>, vis <kk>) and prints the pieces.
"""
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'style', 'v3')))
import fsgeom as G  # noqa: E402

CAM = G.HOUSE
S = 66.0                                    # \FigStressCube size (core default)
NORMAL, SHEAR, FLOOR, TIP, SOLID = 36.0, 21.0, 16.0, 6.6, 11.0
ROOT = {'x': (0.55, 0.65), 'y': (0.62, 0.62), 'z': (0.88, 0.45)}   # fig06_body.tex
OCC = [f for f in G.box_faces((0, 0, 0), (S, S, S)) if f.name in ('-x', '-y', '-z')]  # cut faces opaque, +faces glass
COMP = {'x': [('xx', 'x'), ('xy', 'y'), ('xz', 'z')],
        'y': [('yy', 'y'), ('yx', 'x'), ('yz', 'z')],
        'z': [('zz', 'z'), ('zx', 'x'), ('zy', 'y')]}
E3 = {'x': np.array([1., 0, 0]), 'y': np.array([0, 1., 0]), 'z': np.array([0, 0, 1.])}


def root3(k):
    u, v = ROOT[k]
    return {'x': np.array([0, u * S, v * S]), 'y': np.array([u * S, 0, v * S]),
            'z': np.array([u * S, v * S, 0])}[k]


def fmt(v):
    return ('%.2f' % v).rstrip('0').rstrip('.')


def main():
    keys, lines = [], ['fig06_geom.py -> fig06_geom.tex  (cube %s cut open: cut faces x=0, y=0, z=0 opaque, + faces glass)' % fmt(S)]
    for k in 'xyz':
        R = root3(k)
        for comp, dk in COMP[k]:
            u = -E3[dk]
            p = float(np.linalg.norm(CAM.page(u)))
            if comp[0] == comp[1]:
                # hidden up to the silhouette: find the exit parameter on a long probe
                far = R + 400 * u
                t_exit = G.hidden_intervals(R, far, OCC)[0][1]
                L = max(NORMAL, round((t_exit * 400 * p + SOLID + TIP) / p, 2))
                if L > NORMAL:
                    keys.append('length %s=%s' % (comp, fmt(L)))
            else:
                L = SHEAR
            E = G.arrow_end(R, u, L, FLOOR)
            pcs = G.visible_pieces(R, E, OCC)
            page = float(np.linalg.norm(CAM.page(E - R)))
            keys.append('vis %s={%s}' % (comp, G.tex_pieces(pcs)))
            head = 'visible' if pcs[-1][2] else 'hidden'
            solid = (pcs[-1][1] - pcs[-1][0]) * page - TIP if pcs[-1][2] else 0.0
            lines.append('   %s: page %.1f pt, %s, head %s%s' % (comp, page, G.tex_pieces(pcs), head,
                                                               ', solid shaft %.1f pt' % solid if solid else ''))
            if comp[0] == comp[1]:
                assert pcs[-1][2] and solid > SOLID - 0.05, (comp, pcs, solid)
            else:
                assert pcs == [(0.0, 1.0, True)], (comp, pcs)
    open(os.path.join(HERE, 'fig06_geom.tex'), 'w').write(
        '\\pgfkeys{/fs/cube/fig06/.style={%\n  ' + ',\n  '.join(keys) + '}}\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
