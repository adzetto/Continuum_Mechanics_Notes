r"""fig03_geom.py -- geometry of fig03 (cutting planes of different orientation)
and of the "octant piece" shared with fig04.  House camera az 35 / el 20.4.
Writes fig03_geom.tex next to this file: \def macros in PAGE POINTS, used by
fig03_body.tex inside \begin{scope}[x=1pt,y=1pt].   Run:  python fig03_geom.py

Body: fsgeom.course_potato() (the one body of fig01-fig03), left part x <= XC
= the free body of fig02; its cut face is the end section x = XC (normal +x).
Q = (XC, YQ, ZQ), YQ and ZQ = middle of the end section (bounding box).
(a) the left part built into a wall x = XW (y-z plane) and cut by the
    horizontal plane y = YQ (normal y) through the middle of the end section;
(b) its lower part y <= YQ cut by the longitudinal plane z = ZQ (normal z):
    the retained piece x <= XC, y <= YQ, z <= ZQ has three plane cut faces
    (+x end, +y top, +z front) meeting at the corner Q -- the body of fig04.
The whole skin of that piece faces away from the camera, so the piece is seen
as its three cut faces only (as in the professor's sketch of fig04).
"""
import os
import sys

import numpy as np
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'style', 'v3'))
import fsgeom as G  # noqa: E402

BODY, XC = G.course_potato()
CAM = G.HOUSE
SEC = BODY.section(XC, 1440)                             # end section (cut face of fig02)
YQ = 0.5 * (SEC[:, 1].min() + SEC[:, 1].max())
ZQ = 0.5 * (SEC[:, 2].min() + SEC[:, 2].max())
Q3 = np.array([XC, YQ, ZQ])
X0 = BODY.x0                                             # left tip of the potato


# ---------------------------------------------------------------------------
# slices of the body by coordinate planes
# ---------------------------------------------------------------------------
def chord(x, axis, c, n=720):
    """interval of the free coordinate where the section x = const meets the
    plane {axis} = c (axis 1: y = c -> z-interval; axis 2: z = c -> y-interval)"""
    s = BODY.section(x, n)
    pg = Polygon(s[:, 1:3]).buffer(0)
    ln = LineString([(c, -9), (c, 9)]) if axis == 1 else LineString([(-9, c), (9, c)])
    g = pg.intersection(ln)
    if g.is_empty:
        return None
    co = np.array([p for gg in G.geoms(g) for p in gg.coords])
    k = 1 if axis == 1 else 0
    return co[:, k].min(), co[:, k].max()


def inside_part(P, xa, xb):
    P = np.atleast_2d(P)
    return BODY.inside(P) & (P[:, 0] >= xa) & (P[:, 0] <= xb)


def hidden_part(P, xa, xb, ds=0.004, smax=6.0):
    """ray test toward the viewer against the body part xa <= x <= xb"""
    hid = np.zeros(len(P), bool)
    for s in np.arange(4 * ds, smax, ds):
        hid |= inside_part(P + s * CAM.D, xa, xb)
    return hid


def page(P, scale, off):
    return CAM.page(P, scale) + np.asarray(off, float)


# ---------------------------------------------------------------------------
# the octant piece  x <= XC, y <= YQ, z <= ZQ   (fig03 b, fig04)
# ---------------------------------------------------------------------------
def octant(n=260):
    """3-D corners Q, L, R, B and boundary curves of the three cut faces:
    top  (+y) = Q-L, Ctop (L->R on the skin), R-Q
    front(+z) = Q-L, Cfront (L->B on the skin), B-Q
    end  (+x) = Q-R, Cend (R->B, rim of the end section), B-Q"""
    lo, hi = X0, XC                                      # L: edge y = YQ, z = ZQ leaves the skin
    for _ in range(50):
        m = 0.5 * (lo + hi)
        if BODY.inside(np.array([[m, YQ, ZQ]]))[0]:
            hi = m
        else:
            lo = m
    xL = hi
    xs = xL + (XC - xL) * np.linspace(0, 1, n) ** 2      # dense near the blunt tip
    ctop = np.array([(x, YQ, chord(x, 1, YQ)[0]) for x in xs[1:]])
    cfront = np.array([(x, chord(x, 2, ZQ)[0], ZQ) for x in xs[1:]])
    L = np.array([xL, YQ, ZQ])
    R, B = ctop[-1].copy(), cfront[-1].copy()
    k = np.nonzero((SEC[:, 1] <= YQ) & (SEC[:, 2] <= ZQ))[0]
    run = max(np.split(k, np.nonzero(np.diff(k) > 1)[0] + 1), key=len)   # contiguous arc
    cend = np.r_[[R], SEC[run], [B]]
    if np.hypot(*(cend[1, 1:] - R[1:])) > np.hypot(*(cend[-2, 1:] - R[1:])):
        cend = np.r_[[R], SEC[run][::-1], [B]]
    ctop = np.r_[[L], ctop]
    cfront = np.r_[[L], cfront]
    return dict(Q=Q3.copy(), L=L, R=R, B=B, ctop=ctop, cfront=cfront, cend=cend,
                FY=np.r_[[Q3], ctop], FZ=np.r_[[Q3], cfront], FX=np.r_[[Q3], cend])


def octant_tex(out, pre, scale, off):
    """write the octant piece (page pt) as \\def macros with prefix `pre`"""
    F = octant()
    for k in ('Q', 'L', 'R', 'B'):
        G.tex_def(out, pre + k, G.fmt(page(F[k], scale, off)))
    for k in ('ctop', 'cfront', 'cend'):
        G.tex_def(out, pre + k, G.tex_path(page(F[k], scale, off)))
    for k in ('FY', 'FZ', 'FX'):
        G.tex_def(out, pre + k, G.tex_path(page(F[k], scale, off), cycle=True))
    sil = np.r_[page(F['ctop'], scale, off), page(F['cend'], scale, off)[1:],
                page(F['cfront'], scale, off)[::-1][1:-1]]
    G.tex_def(out, pre + 'outline', G.tex_path(sil, cycle=True))
    return F, Polygon(sil).buffer(0)


# ---------------------------------------------------------------------------
# fig03 composition
# ---------------------------------------------------------------------------
SCALE = 28.0          # pt per model unit (fig01: 29)
XW = -2.78            # wall face x = XW: the blunt left end is built into the wall
OVH = 1.22            # overhang of the planes (x the half extent of the body)


def panel_a(scale, off, out):
    """(a): left part built into the wall x = XW, end section at XC, plane y = YQ"""
    clips = [((1.0, 0, 0), XC), ((-1.0, 0, 0), -XW)]
    ring = G.orient_cw(G.smooth_ring(BODY.outline(CAM, scale, clips), n=900, tol=0.02)) + off
    G.tex_def(out, 'Abody', G.tex_path(ring, cycle=True))
    G.tex_def(out, 'Aend', G.tex_path(page(SEC[::4], scale, off), cycle=True))
    # horizontal plane y = YQ from the wall to XC + ox; beyond the body in z
    zz = np.array([chord(x, 1, YQ) for x in np.linspace(XW, XC, 60)])
    zc, hz = 0.5 * (zz.min() + zz.max()), 0.5 * (zz.max() - zz.min())
    zlo, zhi = zc - OVH * hz, zc + OVH * hz
    ox = 0.50
    quad3 = np.array([(XW, YQ, zhi), (XC + ox, YQ, zhi), (XC + ox, YQ, zlo), (XW, YQ, zlo)])  # FL FR BR BL
    quadp = page(quad3, scale, off)
    quad = Polygon(quadp)
    sh = lambda g: G._largest(g.buffer(0))
    whole = Polygon(np.array(sh(BODY.solid(CAM, scale, clips)).exterior.coords) + off)
    occ = Polygon(np.array(sh(BODY.solid(CAM, scale, clips + [((0, -1.0, 0), -YQ)])).exterior.coords) + off)
    # wall face x = XW (y-z plane): around the built-in end, and in front far
    # enough to hold the visible front corner of the plane; at the back it
    # stops just behind the built-in end (the wall behind the body is not drawn)
    sw = BODY.section(XW, 720)
    wy0, wy1 = sw[:, 1].min() - 0.30, sw[:, 1].max() + 0.22
    wz0, wz1 = sw[:, 2].min() - 0.06, zhi + 0.28
    wall3 = np.array([(XW, wy0, wz1), (XW, wy1, wz1), (XW, wy1, wz0), (XW, wy0, wz0)])  # FB FT BT BB
    wall = page(wall3, scale, off)
    # glass = plane parts in front of the lower half and of the wall; grown by
    # 0.6 pt so that lines under the glass are tinted over their full width
    # (over the bare plane the glass changes nothing: same colour)
    front = quad.intersection(whole.union(Polygon(wall)).buffer(0.6, join_style=2)).difference(occ)
    edges = quad.buffer(0.8, join_style=2).difference(occ)
    G.tex_def(out, 'Aquad', G.tex_path(quadp, cycle=True))
    G.tex_def(out, 'Afront', G.tex_poly(front))
    G.tex_def(out, 'Aedges', G.tex_poly(edges))
    G.tex_def(out, 'Awall', G.tex_path(wall, cycle=True))
    for nm, p in zip(('FB', 'FT', 'BT', 'BB'), wall):
        G.tex_def(out, 'Aw' + nm, G.fmt(p))
    for nm, p in zip(('FL', 'FR', 'BR', 'BL'), quadp):
        G.tex_def(out, 'Aq' + nm, G.fmt(p))
    # traces of the plane: front arc on the skin (visible), back arc (hidden),
    # chord on the end section (A = front end, R = back end = corner R of (b))
    xs = np.linspace(XW, XC, 300)
    ch = np.array([chord(x, 1, YQ) for x in xs])
    front3 = np.c_[xs, np.full(len(xs), YQ), ch[:, 1]]
    back3 = np.c_[xs, np.full(len(xs), YQ), ch[:, 0]]
    hf, hb = hidden_part(front3, XW, XC).mean(), hidden_part(back3, XW, XC).mean()
    G.tex_def(out, 'Arimfront', G.tex_path(page(front3, scale, off)))
    G.tex_def(out, 'Arimback', G.tex_path(page(back3, scale, off)))
    G.tex_def(out, 'AA', G.fmt(page(front3[-1], scale, off)))
    G.tex_def(out, 'AR', G.fmt(page(back3[-1], scale, off)))
    bb = unary_union([Polygon(ring), quad, Polygon(wall)]).bounds
    return dict(bbox=bb, hf=hf, hb=hb, quad=quadp, wall=wall)


def panel_b(scale, off, out):
    """(b): the octant piece framed by the longitudinal plane z = ZQ"""
    F, sil = octant_tex(out, 'B', scale, off)
    # glass over the faces behind the plane (top +y, end +x): one region, grown
    # by 0.6 pt so that their outlines are tinted over the full line width
    gl = unary_union([Polygon(page(F[k], scale, off)).buffer(0.6, join_style=2) for k in ('FY', 'FX')])
    G.tex_def(out, 'Bglass', G.tex_poly(gl))
    x0p, x1p = F['L'][0] - 0.36, XC + 0.92
    y0p, y1p = F['cfront'][:, 1].min() - 0.34, YQ + 0.60
    quad3 = np.array([(x0p, y0p, ZQ), (x1p, y0p, ZQ), (x1p, y1p, ZQ), (x0p, y1p, ZQ)])  # BL BR TR TL
    quadp = page(quad3, scale, off)
    G.tex_def(out, 'Bquad', G.tex_path(quadp, cycle=True))
    for nm, p in zip(('BL', 'BR', 'TR', 'TL'), quadp):
        G.tex_def(out, 'Bq' + nm, G.fmt(p))
    bb = unary_union([sil, Polygon(quadp)]).bounds
    return dict(bbox=bb, F=F, quad=quadp)


# label "cutting plane" (10 pt, fs label: inner sep 1.1 pt, outer sep 1 pt)
LAB_W, LAB_H = 61.1, 13.1           # outer box of the node, pt
LAB_A = np.array([-10.0, 14.0])     # (a): south west corner = back-right plane corner + LAB_A
LAB_B = np.array([4.0, 17.0])       # (b): south east corner = top-right plane corner + LAB_B
GAP = 18.0                          # between the (a) label and the (b) plane
HATCH = 5.2 * np.sqrt(0.5)          # \FigWall strokes (5.2 pt at 135 deg) reach this far


if __name__ == '__main__':
    out = []
    A = panel_a(SCALE, (0, 0), out)
    qa, wa = A['quad'], A['wall']
    la = qa[2] + LAB_A                                    # BR + offset
    a_right = max(A['bbox'][2], la[0] + LAB_W)
    a_left = wa[:, 0].min() - HATCH
    a_top = max(wa[:, 1].max() + HATCH, la[1] + LAB_H)
    a_bot = A['bbox'][1]
    B0 = panel_b(SCALE, (0, 0), [])                       # extents only
    b_left, b_top = B0['quad'][0][0], B0['quad'][2][1] + LAB_B[1] + LAB_H
    shift = np.array([a_right + GAP - b_left, a_top - b_top])
    Bb = panel_b(SCALE, shift, out)
    lb = Bb['quad'][2] + LAB_B                            # TR + offset
    base = min(a_bot, Bb['bbox'][1])
    G.tex_def(out, 'Alabel', G.fmt(la))
    G.tex_def(out, 'Blabel', G.fmt(lb))
    G.tex_def(out, 'Apanel', G.fmt((a_left, base)))
    G.tex_def(out, 'Bpanel', G.fmt((Bb['quad'][0][0], base)))
    open(os.path.join(HERE, 'fig03_geom.tex'), 'w').write('\n'.join(out) + '\n')
    w = max(Bb['bbox'][2], lb[0]) - a_left
    print('fig03: Q = (%.3f, %.3f, %.3f); scale %.0f pt; plane trace hidden: front %.2f back %.2f;'
          ' width %.1f mm, (b) shifted by (%.1f, %.1f) pt'
          % (XC, YQ, ZQ, SCALE, A['hf'], A['hb'], w / 72.27 * 25.4, shift[0], shift[1]))
