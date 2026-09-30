r"""fig10_geom.py -- geometry of fig10 (inclined face ABC, traction p) -> fig10_geom.tex

The tetrahedron is fsgeom.cauchy_tetra(), identical to fig09 (b).  Here ABC
is the OPAQUE cut face (it carries p); EXACT visibility (fsgeom.visible_pieces,
occluders = ABC and the three coordinate faces):
  - p_x, p_y, p_z and n start at the centroid G of ABC and point to the
    outward side of ABC (n = (1/a, 1/b, 1/c)/|..| has only positive
    components): fully visible, solid, solid heads;
  - the creases QA, QB, QC lie behind ABC: fully hidden -> dashed (house
    hidden edges, knocked out around the arrows and labels by \FigTetra).
The generator checks both and writes the keys /fs/tetra/fig10 (geometry and
lengths, x 1.22 of v3.1 like the tetrahedron).
"""
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'style', 'v3')))
import fsgeom as G  # noqa: E402

CAM = G.HOUSE
a, b, c = G.cauchy_tetra()
Q3, A3, B3, C3 = np.zeros(3), np.array([a, 0, 0]), np.array([0, b, 0]), np.array([0, 0, c])
OCC = [G.Occluder([A3, B3, C3], 'ABC'), G.Occluder([Q3, B3, C3], 'x'), G.Occluder([Q3, C3, A3], 'y'),
       G.Occluder([Q3, A3, B3], 'z')]
TRACTION, NLEN, FLOOR = 34.0, 115.0, 13.5
PC = np.array([44.0, 24.0, 22.0])    # v3.4: drawn p_x, p_y, p_z (model), all above FLOOR; p = their sum


def fmt(v):
    return ('%.2f' % v).rstrip('0').rstrip('.')


def main():
    Gc = (A3 + B3 + C3) / 3
    nn = np.array([1 / a, 1 / b, 1 / c]); nn /= np.linalg.norm(nn)
    lines = ['fig10_geom.py -> fig10_geom.tex  (tetrahedron %s:%s:%s, n = (%.3f, %.3f, %.3f))'
             % (fmt(a), fmt(b), fmt(c), *nn)]
    pv = PC.copy()
    for name, u, L in (('p_x', (1, 0, 0), PC[0]), ('p_y', (0, 1, 0), PC[1]), ('p_z', (0, 0, 1), PC[2]),
                       ('n', nn, NLEN), ('p', pv / np.linalg.norm(pv), np.linalg.norm(pv))):
        E = G.arrow_end(Gc, u, L, FLOOR)
        pcs = G.visible_pieces(Gc, E, OCC)
        assert pcs == [(0.0, 1.0, True)], (name, pcs)
        lines.append('   %s: page %.1f pt, %s (visible)' % (name, np.linalg.norm(CAM.page(E - Gc)),
                                                          G.tex_pieces(pcs)))
    for name, P in (('QA', A3), ('QB', B3), ('QC', C3)):
        pcs = G.visible_pieces(Q3, P, OCC)
        assert pcs == [(0.0, 1.0, False)], (name, pcs)
        lines.append('   %s: %s (hidden behind ABC: dashed)' % (name, G.tex_pieces(pcs)))
    keys = ['a=%s, b=%s, c=%s' % (fmt(a), fmt(b), fmt(c)),
            'stresses=traction, axes=false, traction length=%s, n length=%s' % (fmt(TRACTION), fmt(NLEN)),
            'length px=%s, length py=%s, length pz=%s' % tuple(fmt(v) for v in PC)]
    ex = np.eye(3)
    Pt = Gc + PC
    for i in range(3):
        assert np.allclose(G.arrow_end(Gc, ex[i], PC[i], FLOOR), Gc + PC[i] * ex[i]), i
        assert PC[i] * np.linalg.norm(CAM.page(ex[i])) > FLOOR + 0.5, i
    assert np.allclose(CAM.page(Pt - Gc), sum(CAM.page(PC[i] * ex[i]) for i in range(3)))
    V = {'x': Gc + PC[0] * ex[0], 'y': Gc + PC[1] * ex[1], 'z': Gc + PC[2] * ex[2],
         'xy': Gc + PC[0] * ex[0] + PC[1] * ex[1], 'xz': Gc + PC[0] * ex[0] + PC[2] * ex[2],
         'yz': Gc + PC[1] * ex[1] + PC[2] * ex[2]}
    for p0, p1 in (('x', 'xy'), ('x', 'xz'), ('y', 'xy'), ('y', 'yz'), ('z', 'xz'), ('z', 'yz')):
        pcs = G.visible_pieces(V[p0], V[p1], OCC)
        assert pcs == [(0.0, 1.0, True)], (p0, p1, pcs)
    for k in ('xy', 'xz', 'yz'):
        pcs = G.visible_pieces(V[k], Pt, OCC)
        assert pcs == [(0.0, 1.0, True)], (k, pcs)
    c3 = lambda v: '(%s,%s,%s)' % tuple(fmt(x) for x in v)
    open(os.path.join(HERE, 'fig10_geom.tex'), 'w').write(
        '\\pgfkeys{/fs/tetra/fig10/.style={%s}}\n' % ', '.join(keys)
        + '\def\FtenG{%s}\def\FtenP{%s}\def\FtenPx{%s}\def\FtenPy{%s}\def\FtenPz{%s}\def\FtenPxy{%s}\def\FtenPxz{%s}\def\FtenPyz{%s}\n'
        % (c3(Gc), c3(Pt), c3(V['x']), c3(V['y']), c3(V['z']), c3(V['xy']), c3(V['xz']), c3(V['yz'])))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
