r"""fig09_geom.py -- geometry of fig09 (Cauchy tetrahedron) -> fig09_geom.tex

House camera (az 35 / el 20.4), model unit = 1 pt.  The tetrahedron is
fsgeom.cauchy_tetra() (the same one as fig10): Q = (0,0,0), A = (a,0,0),
B = (0,b,0), C = (0,0,c).

(b) coordinate faces x = 0 (QBC), y = 0 (QCA), z = 0 (QAB) are OPAQUE and
    seen from inside through the GLASS face ABC (\FigTetra[look=shaded]).
    EXACT visibility of every arrow (fsgeom.visible_pieces, occluders = the
    three coordinate faces):
      - shear stresses lie on their own face, inside it: visible, solid;
      - a normal stress points away from the tetrahedron, i.e. BEHIND its own
        face: hidden (dotted) until it leaves the face's projection at the
        silhouette edge (BC, CA, AB), then solid; its head is visible.
    Roots and label directions come from a layout search (scratchpad
    tetra/layout.py + optroot.py): every tau label lies inside its own face
    (5 pt from the creases was a soft penalty of the search; measured:
    >= 3.7 pt, tau_yx-QC 3.8 pt, all others >= 5.5 pt), never nearer to
    another face's arrow than to its own; every sigma label outside the
    silhouette; fscheck >= 1.5 pt.
    Normal lengths: exit distance to the silhouette + 9 pt solid + 6.6 pt tip
    (page), so each sigma shows a 9 pt solid shaft behind its visible head.
(a) the same tetrahedron at k = 0.36 (b' = 0.36 b = 38.2) inside the cube [0,S]^3 whose
    hidden corner is Q.  The cube is a glass element drawn as a wireframe:
    9 visible edges thin; its 3 hidden edges from Q dashed (house convention,
    the cube's own faces taken as opaque for its own edges) -- except where
    they are the tetrahedron's creases QA, QB, QC, which are visible through
    the glass face ABC (tetrahedron faces opaque): solid, as in (b).
    Dashes fitted to each hidden piece (whole dashes at both ends).
Writes \pgfkeys{/fs/tetra/fig09b/.style={...}} and the (a) coordinates /
hidden pieces; prints the visibility of every arrow and edge.
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
FACES = {'x': [Q3, B3, C3], 'y': [Q3, C3, A3], 'z': [Q3, A3, B3]}
OCC = [G.Occluder(FACES[k], k) for k in 'xyz']          # ABC is glass: not an occluder
TIP, SOLID, FLOOR, SHEAR = 6.6, 13.0, 13.5, 24.0

# tripod roots (model, on x = 0: (y, z); on y = 0: (x, z); on z = 0: (x, y))
ROOT = {'x': (34.79, 41.77), 'y': (36.0, 26.0), 'z': (34.18, 35.96)}
# label directions (absolute page direction tip -> label, deg)
DIR = {'xx': 85, 'xy': 215, 'xz': 105, 'yy': 210, 'yx': 225, 'yz': 315,
       'zz': 330, 'zx': 85, 'zy': 330}
DIR_Q = 40
COMP = {'x': [('xx', 'x'), ('xy', 'y'), ('xz', 'z')],
        'y': [('yy', 'y'), ('yx', 'x'), ('yz', 'z')],
        'z': [('zz', 'z'), ('zx', 'x'), ('zy', 'y')]}
E3 = {'x': np.array([1., 0, 0]), 'y': np.array([0, 1., 0]), 'z': np.array([0, 0, 1.])}


def root3(k):
    u, v = ROOT[k]
    return {'x': np.array([0, u, v]), 'y': np.array([u, 0, v]), 'z': np.array([u, v, 0])}[k]


def exit_distance(k, R, u):
    """page distance from the root along the page image of u to the boundary of face k"""
    from shapely.geometry import LineString, Polygon
    q, d = CAM.page(R), CAM.page(u)
    d = d / np.linalg.norm(d)
    pg = Polygon(CAM.page(np.array(FACES[k])))
    hit = LineString([q, q + 500 * d]).intersection(pg.boundary)
    pts = [np.array(p.coords[0]) for p in getattr(hit, 'geoms', [hit])]
    return min(np.linalg.norm(p - q) for p in pts if np.linalg.norm(p - q) > 1e-6)


def tripods():
    out = {}
    for k in 'xyz':
        R = root3(k)
        for comp, dk in COMP[k]:
            u = -E3[dk]
            p = float(np.linalg.norm(CAM.page(u)))
            if comp[0] == comp[1]:                     # normal stress: 9 pt solid behind the head
                L = round((exit_distance(k, R, u) + SOLID + TIP) / p, 2)
            else:
                L = SHEAR
            E = G.arrow_end(R, u, L, FLOOR)
            pcs = G.visible_pieces(R, E, OCC)
            out[comp] = dict(R=R, E=E, L=L, pieces=pcs, page=float(np.linalg.norm(CAM.page(E - R))))
    return out


# ------------------------------------------------------------------ panel (a)
S = 56.0                        # cube edge
K = 0.36                        # tetrahedron scale in (a): b' = 38.2 = 0.68 S


def fitted_dash(p0, p1, on=2.6, off=1.9):
    """dash pattern with whole dashes at both ends of the page segment p0-p1"""
    L = float(np.linalg.norm(p1 - p0))
    n = max(1, round((L + off) / (on + off)))
    f = L / (n * on + (n - 1) * off)
    return on * f, off * f


def panel_a():
    a2, b2, c2 = K * a, K * b, K * c
    P = {'Q': (0, 0, 0), 'X': (S, 0, 0), 'Y': (0, S, 0), 'Z': (0, 0, S), 'XY': (S, S, 0),
         'XZ': (S, 0, S), 'YZ': (0, S, S), 'XYZ': (S, S, S), 'A': (a2, 0, 0), 'B': (0, b2, 0),
         'C': (0, 0, c2)}
    P = {k: np.array(v, float) for k, v in P.items()}
    cube_occ = G.box_faces((0, 0, 0), (S, S, S))
    tet_occ = [G.Occluder([P['Q'], P['B'], P['C']]), G.Occluder([P['Q'], P['C'], P['A']]),
               G.Occluder([P['Q'], P['A'], P['B']])]
    report = []
    # cube edges against the cube's own faces
    edges = [('Y', 'XY'), ('XY', 'X'), ('X', 'XZ'), ('XZ', 'Z'), ('Z', 'YZ'), ('YZ', 'Y'),
             ('XYZ', 'XY'), ('XYZ', 'XZ'), ('XYZ', 'YZ'), ('Q', 'X'), ('Q', 'Y'), ('Q', 'Z')]
    vis_cube, hid_cube = [], []
    for e0, e1 in edges:
        pcs = G.visible_pieces(P[e0], P[e1], cube_occ)
        report.append('   cube %s-%s: %s' % (e0, e1, G.tex_pieces(pcs)))
        (vis_cube if pcs == [(0.0, 1.0, True)] else hid_cube).append((e0, e1, pcs))
    # the tetrahedron against its own opaque faces (glass ABC): creases and ABC visible
    for e0, e1 in (('Q', 'A'), ('Q', 'B'), ('Q', 'C'), ('A', 'B'), ('B', 'C'), ('C', 'A')):
        pcs = G.visible_pieces(P[e0], P[e1], tet_occ)
        report.append('   tetra %s-%s: %s' % (e0, e1, G.tex_pieces(pcs)))
        assert pcs == [(0.0, 1.0, True)]
    # hidden cube edges minus the (visible) creases: Q-X -> A-X, Q-Y -> B-Y, Q-Z -> C-Z
    hidden = []
    for e0, e1, pcs in hid_cube:
        assert pcs == [(0.0, 1.0, False)], pcs
        start = {'X': 'A', 'Y': 'B', 'Z': 'C'}[e1]
        p0, p1 = CAM.page(P[start]), CAM.page(P[e1])
        hidden.append((start, e1, fitted_dash(p0, p1)))
    pg = {k: CAM.page(v) for k, v in P.items()}
    return pg, hidden, report


def fmt(v):
    return ('%.2f' % v).rstrip('0').rstrip('.')


def main():
    tri = tripods()
    keys = ['a=%s, b=%s, c=%s' % (fmt(a), fmt(b), fmt(c)),
            'look=shaded, stresses=coordinate, axes=false, shear length=%s' % fmt(SHEAR),
            'root x={%s,%s}, root y={%s,%s}, root z={%s,%s}' % tuple(fmt(v) for k in 'xyz' for v in ROOT[k]),
            'dir Q=%d' % DIR_Q]
    for comp in ('xx', 'yy', 'zz'):
        keys.append('length %s=%s' % (comp, fmt(tri[comp]['L'])))
    for comp in ('xx', 'xy', 'xz', 'yy', 'yx', 'yz', 'zz', 'zx', 'zy'):
        keys.append('dir %s=%d, vis %s={%s}' % (comp, DIR[comp], comp, G.tex_pieces(tri[comp]['pieces'])))
    pg, hidden, report = panel_a()
    L = ['\\pgfkeys{/fs/tetra/fig09b/.style={%', '  ' + ',\n  '.join(keys) + '}}',
         '\\def\\FnineAcoords{\\path ' + ' '.join('(%.3f,%.3f) coordinate (f9a%s)' % (v[0], v[1], k)
                                                 for k, v in sorted(pg.items())) + ';}',
         '\\def\\FnineAhidden{%']
    for e0, e1, (on, off) in hidden:
        L.append('  \\draw[fs hidden, dash pattern=on %.3fpt off %.3fpt] (f9a%s) -- (f9a%s);' % (on, off, e0, e1))
    L.append('}')
    open(os.path.join(HERE, 'fig09_geom.tex'), 'w').write('\n'.join(L) + '\n')
    lines = ['fig09_geom.py -> fig09_geom.tex  (tetrahedron %s:%s:%s)' % (fmt(a), fmt(b), fmt(c))]
    for comp in ('xx', 'xy', 'xz', 'yy', 'yx', 'yz', 'zz', 'zx', 'zy'):
        t = tri[comp]
        hid = sum((t1 - t0) for t0, t1, v in t['pieces'] if not v) * t['page']
        solid = (t['pieces'][-1][1] - t['pieces'][-1][0]) * t['page'] - TIP if t['pieces'][-1][2] else -1
        lines.append('   %s: page %.1f pt, hidden %.1f pt, solid shaft before the head %.1f pt, head %s'
                     % (comp, t['page'], hid, solid, 'visible' if t['pieces'][-1][2] else 'HIDDEN'))
        # shears on their own face: fully visible; normals: hidden, then visible with the head
        if comp[0] == comp[1]:
            assert len(t['pieces']) == 2 and not t['pieces'][0][2] and t['pieces'][1][2] and solid > SOLID - 0.05
        else:
            assert t['pieces'] == [(0.0, 1.0, True)]
    # (b) edges and axes against the opaque coordinate faces (glass ABC): all visible
    ends = {'Q': Q3, 'A': A3, 'B': B3, 'C': C3}
    for e0, e1 in (('Q', 'A'), ('Q', 'B'), ('Q', 'C'), ('A', 'B'), ('B', 'C'), ('C', 'A')):
        pcs = G.visible_pieces(ends[e0], ends[e1], OCC)
        assert pcs == [(0.0, 1.0, True)], (e0, e1, pcs)
        lines.append('   (b) edge %s-%s: %s (visible%s)' % (e0, e1, G.tex_pieces(pcs),
                     ': crease, seen through the glass face ABC' if e0 == 'Q' else ''))
    for name, P0, u in (('x', A3, E3['x']), ('y', B3, E3['y']), ('z', C3, E3['z'])):
        pcs = G.visible_pieces(P0 + 1 * u, P0 + 20 * u, OCC)
        assert pcs == [(0.0, 1.0, True)], (name, pcs)
        lines.append('   (b) axis %s: %s (visible)' % (name, G.tex_pieces(pcs)))
    print('\n'.join(lines + report))


if __name__ == '__main__':
    main()
