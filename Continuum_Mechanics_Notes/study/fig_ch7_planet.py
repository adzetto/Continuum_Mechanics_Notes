#!/usr/bin/env python
# =====================================================================
#  Chapter 7, Problem 3:  "An observer standing on a spinning planet"
#  Figure J of the notes  (label fig:ch7planet).
#
#  PART 1  sympy.   The moving triad, the spin of the frame and
#                   the centrifugal term of the solution are re-derived
#                   symbolically and every identity used in the text is
#                   checked to be exactly zero.
#  PART 2  numpy.   Earth numbers, and the coordinates of every stroke
#                   and every label of the figure, all derived from the
#                   same formulas.  A bounding-box pass proves that no
#                   label overlaps another label or crosses a stroke.
#  PART 3  output.  fig_ch7_planet.tex, a pgfplots picture with three
#                   panels: (a) the planet, (b) the station, (c) the
#                   centrifugal term against latitude.
#
#      python fig_ch7_planet.py          ->  fig_ch7_planet.tex
# =====================================================================
import io
import os

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'fig_ch7_planet.tex')
OUT3D = os.path.join(HERE, 'fig_ch7_planet3d.tex')


# =====================================================================
#  PART 1 -- sympy: the identities of Steps 1, 3 and 5
# =====================================================================
th, ph, w, R, g = sp.symbols('theta varphi omega R g', real=True)
e1, e2, e3 = [sp.Matrix(c) for c in np.eye(3, dtype=int)]

# Step 1: the moving triad
f_rho = sp.cos(th) * e1 + sp.sin(th) * e2
f_E = -sp.sin(th) * e1 + sp.cos(th) * e2
f_N = -sp.sin(ph) * f_rho + sp.cos(ph) * e3
f_U = sp.cos(ph) * f_rho + sp.sin(ph) * e3
triad = (f_E, f_N, f_U)

G = sp.Matrix(3, 3, lambda i, j: (triad[i].T * triad[j])[0])
assert sp.simplify(G - sp.eye(3)) == sp.zeros(3), 'triad not orthonormal'
assert sp.simplify(f_E.dot(f_N.cross(f_U))) == 1, 'triad not right-handed'
# the inverse relations used twice in the text
assert sp.simplify(f_rho - (sp.cos(ph) * f_U - sp.sin(ph) * f_N)) == sp.zeros(3, 1)
assert sp.simplify(e3 - (sp.sin(ph) * f_U + sp.cos(ph) * f_N)) == sp.zeros(3, 1)

# Step 3: theta = omega t + theta_0, so d/dt = omega d/dtheta
dot = lambda v: sp.simplify(w * sp.diff(v, th))
Om = sp.Matrix(3, 3, lambda i, j: sp.simplify(dot(triad[i]).dot(triad[j])))
Om_text = w * sp.Matrix([[0, sp.sin(ph), -sp.cos(ph)],
                         [-sp.sin(ph), 0, 0],
                         [sp.cos(ph), 0, 0]])
assert sp.simplify(Om - Om_text) == sp.zeros(3), 'Omega differs from the text'
assert sp.simplify(Om + Om.T) == sp.zeros(3), 'Omega not skew'
# axial vector:  Omega_ab = -eps_abc w_c   ->   w = (-Om[1,2], Om[0,2], -Om[0,1])
w_vec = sp.Matrix([-Om[1, 2], Om[0, 2], -Om[0, 1]])          # components (E,N,U)
assert sp.simplify(w_vec - sp.Matrix([0, -w * sp.cos(ph), -w * sp.sin(ph)])) == sp.zeros(3, 1)
# Omega s = w x s  for every s, hence  Omega s = -omega x s  with  omega = -w
s = sp.Matrix(sp.symbols('s_E s_N s_U', real=True))
assert sp.simplify(Om * s - w_vec.cross(s)) == sp.zeros(3, 1)
omega_plus = -w_vec                                          # (0, w cos, w sin)

# Step 5: centrifugal term at the station, s+ = R e_U+
s_station = R * sp.Matrix([0, 0, 1])
cf = sp.simplify(-omega_plus.cross(omega_plus.cross(s_station)))
cf_text = w**2 * R * sp.cos(ph) * sp.Matrix([0, -sp.sin(ph), sp.cos(ph)])
assert sp.simplify(cf - cf_text) == sp.zeros(3, 1), 'centrifugal term differs'
assert sp.simplify(cf.norm()**2 - (w**2 * R * sp.cos(ph))**2) == 0
assert sp.simplify(cf.dot(omega_plus)) == 0, 'not perpendicular to the axis'

# effective gravity and the tilt of the plumb line,  eps = omega^2 R / g
eps = sp.symbols('epsilon', positive=True)
g_eff = -g * sp.Matrix([0, 0, 1]) + cf
tan_delta = sp.simplify((-g_eff[1] / (-g_eff[2])).subs(w**2 * R, eps * g))
# where is the tilt largest?  numerator of d(tan delta)/d phi, to first order in eps
num = sp.numer(sp.together(sp.simplify(sp.diff(tan_delta, ph))))
lead = sp.factor(sp.simplify(sp.series(num, eps, 0, 2).removeO()))
print('PART 1  sympy: every identity of Steps 1, 3, 5 checks.')
print('        tan(delta) =', tan_delta)
print('        d tan(delta)/d phi = 0  to O(eps):', lead, '= 0')


# =====================================================================
#  PART 2 -- numpy: Earth numbers and the figure geometry
# =====================================================================
OMEGA = 7.292115e-5        # sidereal rate, 1/s
RADIUS = 6.371e6           # mean radius, m
G0 = 9.80665               # m/s^2
EPS = OMEGA**2 * RADIUS / G0
tan_delta_f = sp.lambdify((ph, eps), tan_delta, 'numpy')
phis = np.linspace(0.0, np.pi / 2, 90001)
tilt = np.degrees(np.arctan(tan_delta_f(phis, EPS)))
i_max = int(np.argmax(tilt))
phi_max_deg = np.degrees(phis[i_max])
tilt_max_arcmin = 60.0 * tilt[i_max]
print('PART 2  Earth:  omega^2 R = %.4f m/s^2 = %.2f mm/s^2,  eps = %.5f'
      % (OMEGA**2 * RADIUS, 1e3 * OMEGA**2 * RADIUS, EPS))
print('        plumb-line tilt largest at phi = %.2f deg: delta = %.2f arcmin'
      % (phi_max_deg, tilt_max_arcmin))

# ---- the drawing latitude and the exaggeration used in panel (b) -----
PHI = 35.0                            # degrees
EXAG = 0.55                           # omega^2 R / g drawn in panel (b)
SCALE = 1.2                           # cm per paper unit in panels (a), (b)
BOUNDS = {'a': ((-2.55, 3.55), (-3.35, 3.85)),   # (xmin,xmax),(ymin,ymax)
          'b': ((-2.50, 2.60), (-3.35, 3.85)),
          'd': ((-8.0, 8.0), (-7.0, 7.0))}          # cm on paper, 3-d panel
c, s_ = np.cos(np.radians(PHI)), np.sin(np.radians(PHI))
unit = lambda deg: np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg))])

# ---------------- panel (a): the meridional section --------------------
#  x = f_rho (to the right), y = e_3 (up); f_E into the page.
RA = 2.0                              # planet radius on paper
P = RA * unit(PHI)                    # the station
r_sym = 0.15                          # radius of the "into the page" symbol
a = {
    'axis_lo': (0.0, -2.55), 'axis_hi': (0.0, 2.40), 'axis_tip': (0.0, 3.15),
    'frho_tip': 1.30 * unit(0.0),
    'phi_arc_r': 0.72,
    'P': P,
    'R_line_end': P - r_sym * unit(PHI),            # stop at the symbol
    'foot': np.array([0.0, P[1]]),                  # foot on the axis
    'cos_line_end': P - r_sym * unit(0.0),          # stop at the symbol
    'fU_tip': P + 1.05 * unit(PHI),
    'fU_tail': P + r_sym * unit(PHI),
    'fN_tip': P + 0.85 * unit(PHI + 90.0),
    'fN_tail': P + r_sym * unit(PHI + 90.0),
    'spin_c': (0.0, 2.62), 'spin_ab': (0.62, 0.22),
}
assert abs(np.dot(a['fU_tip'] - P, a['fN_tip'] - P)) < 1e-12
assert abs(a['foot'][1] - RA * s_) < 1e-12           # height R sin phi
assert abs((P - a['foot'])[0] - RA * c) < 1e-12      # distance R cos phi from axis

# ---------------- panel (b): as O+ draws it ----------------------------
#  x = -e_N+ (north to the LEFT), y = e_U+ (up); e_E+ into the page.
#  A vector with components (v_N, v_U) is drawn at paper point (-v_N, v_U).
paper = lambda vN, vU: np.array([-vN, vU])
LG = 1.55                                            # |g| on paper
om_dir = paper(c, s_)                                # omega/|omega| = (cos, sin) in (N,U)
cf_vec = EXAG * LG * c * paper(-s_, c)               # exaggerated centrifugal term
g_vec = paper(0.0, -LG)
geff = g_vec + cf_vec
delta_draw = np.degrees(np.arctan2(geff[0], -geff[1]))
assert abs(np.dot(cf_vec, om_dir)) < 1e-12           # perpendicular to the axis
assert abs(np.linalg.norm(cf_vec) - EXAG * LG * c) < 1e-12
b = {
    'hz_l': (-2.25, 0.0), 'hz_r': (2.15, 0.0),
    'ticks': np.arange(-2.05, 2.06, 0.41),
    'N_tip': paper(1.65, 0.0), 'N_tail': paper(r_sym, 0.0),
    'U_tip': paper(0.0, 1.65), 'U_tail': paper(0.0, r_sym),
    'om_tip': 2.05 * om_dir, 'om_tail': r_sym * om_dir,
    'phi_arc_r': 0.90,
    'g_tip': g_vec, 'g_tail': paper(0.0, -r_sym),
    'cf_tail': g_vec, 'cf_tip': geff,
    'geff_tip': geff, 'geff_tail': r_sym * geff / np.linalg.norm(geff),
    'delta_arc_r': 0.70,
}
print('        panel (b) drawn with omega^2 R / g = %.2f (Earth: %.4f); '
      'tilt on paper %.1f deg' % (EXAG, EPS, delta_draw))

# ---------------- panel (c): the centrifugal term against latitude -----
phi_c = np.linspace(0.0, 90.0, 181)
cc = np.cos(np.radians(phi_c))
ss = np.sin(np.radians(phi_c))
curves = {
    'mag': cc,            # |centrifugal| / omega^2 R
    'vert': cc * cc,      # component along e_U+, / omega^2 R
    'horz': ss * cc,      # component along -e_N+ (towards the equator)
}
assert np.allclose(curves['vert']**2 + curves['horz']**2, curves['mag']**2)
assert abs(phi_c[np.argmax(curves['horz'])] - 45.0) < 0.5

# =====================================================================
#  Labels: position, anchor, and an estimated box for the overlap test.
#  Sizes: the document is 17pt, so \small = 14pt, \footnotesize = 12pt.
#  A box is (width, height) in cm; widths are counted in em of the font.
# =====================================================================
PT = 1.0 / 28.4527                                   # cm per pt
FONT = {'small': 14.0, 'footnotesize': 12.0}


PANEL_SCALE = {'a': SCALE, 'b': SCALE, 'd': 1.0}    # cm per paper unit


def box(em, font, panel):
    """estimated (width, height) of a label, in paper units of its panel"""
    fs = FONT[font] * PT / PANEL_SCALE[panel]
    return (em * fs, 1.15 * fs)


def anchor_shift(anchor, wdt, hgt):
    """lower-left corner of a box relative to its anchor point"""
    dx = {'west': 0.0, 'east': -wdt, 'center': -wdt / 2}
    dy = {'south': 0.0, 'north': -hgt, 'center': -hgt / 2}
    v = 'south' if 'south' in anchor else 'north' if 'north' in anchor else 'center'
    h = 'west' if 'west' in anchor else 'east' if 'east' in anchor else 'center'
    return dx[h], dy[v]


class Label:
    def __init__(self, panel, text, xy, anchor, em, font='small',
                 color=None, sep=0.06, xyz=None, off=(0.0, 0.0)):
        # xy: position on paper (panel units) used by the overlap test.
        # 3-d panels anchor the node at the data point xyz and shift it by
        # off (cm) on paper; xy must then be the projected point plus off.
        self.panel, self.text, self.xy = panel, text, np.asarray(xy, float)
        self.anchor, self.font, self.color = anchor, font, color
        self.xyz, self.off = xyz, off
        self.w, self.h = box(em, font, panel)
        dx, dy = anchor_shift(anchor, self.w, self.h)
        lo = self.xy + (dx, dy) - sep
        self.lo, self.hi = lo, lo + (self.w, self.h) + 2 * sep

    def tex(self):
        opts = ['font=\\%s' % self.font, 'anchor=%s' % self.anchor,
                'inner sep=1pt']
        if self.color:
            opts.append('text=%s' % self.color)
        if self.xyz is None:
            return '\\node[%s] at (axis cs:%.3f,%.3f) {%s};' % (
                ', '.join(opts), self.xy[0], self.xy[1], self.text)
        opts.append('shift={(%.2fcm,%.2fcm)}' % tuple(self.off))
        return '\\node[%s] at (axis cs:%.3f,%.3f,%.3f) {%s};' % (
            ', '.join(opts), self.xyz[0], self.xyz[1], self.xyz[2], self.text)


RED, BLUE, GRAY = 'red!65!black', 'blue!55!black', 'gray!85'
labels = [
    # ---- panel (a) ----
    Label('a', r'$\be_{3}$', (0.10, 3.20), 'south west', 1.3),
    Label('a', r'$\omega$', (0.78, 2.80), 'west', 1.1, color=RED),
    Label('a', r'$\bff_{\rho}$', (0.65, -0.12), 'north', 1.3, color=GRAY),
    Label('a', r'$\varphi$', (1.05, 0.33), 'west', 0.9),
    Label('a', r'$R$', 0.45 * P + 0.12 * unit(PHI + 90.0), 'south east', 1.0),
    Label('a', r'$R\cos\varphi$', (0.53, P[1] + 0.09), 'south', 2.5,
          font='footnotesize', color=GRAY),
    Label('a', r'$\bff_{U}$', a['fU_tip'] + 0.08 * unit(PHI), 'west', 1.4, color=BLUE),
    Label('a', r'$\bff_{N}$', a['fN_tip'] + 0.08 * unit(PHI + 90.0) + (0.12, 0.0),
          'south', 1.4, color=BLUE),
    Label('a', r'$\bff_{E}$', P + 0.45 * unit(-10.0), 'west', 1.4, color=GRAY),
    Label('a', r'(a) the local triad at the station', (0.5, -2.78), 'north', 14.2),
    # ---- panel (b) ----
    Label('b', r'$\be^{+}_{N}$', (-1.62, -0.10), 'north', 1.6),
    Label('b', r'$\be^{+}_{U}$', (0.10, 1.60), 'west', 1.6),
    Label('b', r'$\be^{+}_{E}$', (r_sym + 0.07, 0.34), 'west', 1.6, color=GRAY),
    Label('b', r'$\bom$', b['om_tip'] + 0.12 * om_dir + (-0.05, 0.05), 'south east',
          1.2, color=RED),
    Label('b', r'$\varphi$', 1.10 * unit(180.0 - PHI / 2), 'east', 0.9),
    Label('b', r'$-g\,\be^{+}_{U}$', (-0.10, -1.25), 'east', 3.0),
    Label('b', r'$\omega^{2}R\cos\varphi$', (0.55, -1.82), 'west', 4.6,
          font='footnotesize', color=RED),
    Label('b', r'$\bg_{\mathrm{eff}}$', (0.55, -1.16), 'west', 1.7, color=BLUE),
    Label('b', r'$\delta$', 0.70 * unit(-50.0), 'west', 0.9, color=BLUE),
    Label('b', r'(b) as $O^{+}$ draws it', (-0.05, -2.78), 'north', 10.0),
]


# ---- strokes, for the label-crosses-a-line test (paper coordinates) ---
def arc_pts(cx, cy, rx, ry, d0, d1, n=40):
    tt = np.radians(np.linspace(d0, d1, n))
    return np.c_[cx + rx * np.cos(tt), cy + ry * np.sin(tt)]


strokes = {
    'a': [
        arc_pts(0, 0, RA, RA, 0, 360, 181),
        np.array([(-RA, 0.0), (RA, 0.0)]),            # the equator
        np.array([a['axis_lo'], a['axis_tip']]),
        np.array([(0, 0), a['frho_tip']]),
        arc_pts(0, 0, a['phi_arc_r'], a['phi_arc_r'], 0, PHI),
        np.array([(0, 0), a['R_line_end']]),
        np.array([a['foot'], a['cos_line_end']]),
        np.array([a['fU_tail'], a['fU_tip']]),
        np.array([a['fN_tail'], a['fN_tip']]),
        arc_pts(*a['spin_c'], *a['spin_ab'], -15, 200),
        arc_pts(*P, r_sym, r_sym, 0, 360, 37),
    ],
    'b': [
        np.array([b['hz_l'], b['hz_r']]),
        np.array([b['N_tail'], b['N_tip']]),
        np.array([b['U_tail'], b['U_tip']]),
        np.array([b['om_tail'], b['om_tip']]),
        arc_pts(0, 0, b['phi_arc_r'], b['phi_arc_r'], 180 - PHI, 180),
        np.array([b['g_tail'], b['g_tip']]),
        np.array([b['cf_tail'], b['cf_tip']]),
        np.array([b['geff_tail'], b['geff_tip']]),
        arc_pts(0, 0, b['delta_arc_r'], b['delta_arc_r'], -90, -90 + delta_draw),
        arc_pts(0, 0, r_sym, r_sym, 0, 360, 37),
    ],
}


# =====================================================================
#  Panel (d): the same geometry in three dimensions, R = 1.
#  pgfplots is given explicit unit vectors, so the orthographic
#  projection is known exactly and the overlap test can run on paper
#  coordinates (cm).  View: azimuth AZ about e_3, elevation EL.
# =====================================================================
AZ, EL, S3 = 100.0, 22.0, 4.2                         # degrees, degrees, cm per R
THETA = 40.0                                          # longitude drawn, degrees
_ca, _sa = np.cos(np.radians(AZ)), np.sin(np.radians(AZ))
_ce, _se = np.cos(np.radians(EL)), np.sin(np.radians(EL))
U3 = np.array([_ca, _sa, 0.0])                        # paper x, in data space
W3 = np.array([-_sa * _se, _ca * _se, _ce])           # paper y
V3 = np.cross(U3, W3)                                 # towards the viewer
assert abs(np.dot(U3, W3)) < 1e-12 and abs(np.linalg.norm(V3) - 1) < 1e-12


def proj(p):
    """data point -> paper point in cm"""
    p = np.asarray(p, float)
    return S3 * np.array([p @ U3, p @ W3])


def visible(p):
    return np.asarray(p, float) @ V3 >= 0.0


ct, st = np.cos(np.radians(THETA)), np.sin(np.radians(THETA))
E1, E2, E3 = np.eye(3)
FRHO = np.array([ct, st, 0.0])                        # f_rho
FE = np.array([-st, ct, 0.0])                         # f_E
FN = -s_ * FRHO + c * E3                              # f_N
FU = c * FRHO + s_ * E3                               # f_U
P3 = FU                                               # the station, R = 1
F3 = np.array([0.0, 0.0, s_])                         # foot on the axis
assert np.allclose(np.cross(FE, FN), FU)              # right-handed
assert np.allclose([FE @ FN, FN @ FU, FU @ FE], 0)
assert abs(np.linalg.norm(P3 - F3) - c) < 1e-12       # R cos(phi) from the axis
assert visible(P3) and visible(FRHO) and visible(E1) and visible(E2)


def circle3(center, a, b, d0, d1, n=181):
    """points center + cos(t) a + sin(t) b for t from d0 to d1 degrees"""
    tt = np.radians(np.linspace(d0, d1, n))
    return np.asarray(center)[None, :] + np.outer(np.cos(tt), a) + np.outer(np.sin(tt), b)


curves3 = {                                           # name: (points, style)
    'equator': (circle3([0, 0, 0], E1, E2, 0, 360), 'thin,gray!70'),
    'meridian': (circle3([0, 0, 0], FRHO, E3, 0, 360), 'thin,gray!70'),
    'parallel': (circle3([0, 0, 0], c * E1, c * E2, 0, 360)
                 + np.array([0, 0, s_]), 'thin,gray!70'),
    'theta_arc': (circle3([0, 0, 0], 0.42 * E1, 0.42 * E2, 0, THETA, 25), 'guide'),
    'phi_arc': (circle3([0, 0, 0], 0.32 * FRHO, 0.32 * E3, 0, PHI, 25), 'guide'),
    'spin': (circle3([0, 0, 1.22], 0.26 * E1, 0.26 * E2, 130, 430, 40),
             'sm,red!65!black'),
}
arrows3 = {                                           # name: (tail, tip, style)
    'e1': (0 * E1, 1.45 * E1, 'ar'),
    'e2': (0 * E2, 1.45 * E2, 'ar'),
    'e3': (0 * E3, 1.50 * E3, 'ar'),
    'frho': (0 * E1, FRHO, 'ar,gray!70'),
    'fE': (P3, P3 + 0.45 * FE, 'ar,blue!55!black'),
    'fN': (P3, P3 + 0.45 * FN, 'ar,blue!55!black'),
    'fU': (P3, P3 + 0.45 * FU, 'ar,blue!55!black'),
}
lines3 = {
    'R': (0 * E1, P3, 'thick'),
    'Rcos': (F3, P3, 'guide'),
    'axis': (-1.0 * E3, 0 * E3, 'guide'),
}


def tip_label(name, text, em, dist=0.30, color=None, font='small'):
    """label just beyond an arrow tip, anchored against the arrow direction"""
    tail, tip, _ = arrows3[name]
    d = proj(tip) - proj(tail)
    d = d / np.linalg.norm(d)
    off = dist * d
    ax = 'west' if d[0] > 0.35 else 'east' if d[0] < -0.35 else ''
    ay = 'south' if d[1] > 0.35 else 'north' if d[1] < -0.35 else ''
    anchor = (ay + ' ' + ax).strip() or 'center'
    return Label('d', text, proj(tip) + off, anchor, em, font=font,
                 color=color, xyz=tip, off=off)


def at_label(xyz, off, text, anchor, em, color=None, font='small'):
    off = np.asarray(off, float)
    return Label('d', text, proj(xyz) + off, anchor, em, font=font,
                 color=color, xyz=np.asarray(xyz, float), off=off)


def on_circle(a, b, deg, center=(0, 0, 0)):
    return circle3(center, a, b, deg, deg, 1)[0]


# the front-most point of the equator, for a label that sits under it
_t_low = np.degrees(np.arctan2(-W3[1], -W3[0]))      # minimises y of (cos t, sin t, 0)
_eq_low = on_circle(E1, E2, _t_low if visible(on_circle(E1, E2, _t_low)) else _t_low + 180)
# the lowest visible point of the meridian, for a label below the globe
_mer = curves3['meridian'][0]
_mer_low = min((p for p in _mer if visible(p)), key=lambda p: proj(p)[1])

labels += [
    tip_label('e1', r'$\be_{1}$', 1.3),
    tip_label('e2', r'$\be_{2}$', 1.3),
    tip_label('e3', r'$\be_{3}$', 1.3),
    tip_label('frho', r'$\bff_{\rho}$', 1.3, color=GRAY),
    tip_label('fE', r'$\bff_{E}$', 1.4, color=BLUE),
    at_label(arrows3['fN'][1], (0.45, 0.15), r'$\bff_{N}$', 'west', 1.4, color=BLUE),
    at_label(arrows3['fU'][1], (-0.15, 0.35), r'$\bff_{U}$', 'south', 1.4, color=BLUE),
    at_label(on_circle(0.68 * E1, 0.68 * E2, THETA / 2), (0.0, 0.0), r'$\theta$',
             'center', 0.9, font='footnotesize'),
    # phi sits beside the lower end of its arc, between f_rho and e_2
    at_label([0, 0, 0], (1.64, -0.44), r'$\varphi$', 'center', 0.9,
             font='footnotesize'),
    # R sits under the line O-P, between it and e_2
    at_label([0, 0, 0], (1.32, 0.70), r'$R$', 'north west', 1.0,
             font='footnotesize'),
    at_label(F3, (-0.12, 0.0), r'$R\cos\varphi$', 'east', 2.5,
             font='footnotesize', color=GRAY),
    at_label([0, 0, 1.22], (1.30, 0.0), r'$\omega$', 'west', 1.1, color=RED),
    at_label([0, 0, 0], (-0.20, 0.10), r'$O$', 'east', 0.9),
    at_label(_eq_low, (0.9, -0.12), r'equator', 'north', 3.4,
             font='footnotesize', color=GRAY),
    at_label(on_circle(c * E1, c * E2, -45.0, [0, 0, s_]), (-0.10, -0.15),
             r'parallel $\varphi$', 'north east', 4.2, font='footnotesize',
             color=GRAY),
    at_label(_mer_low, (0.3, -0.28), r'meridian $\theta$', 'north', 4.6,
             font='footnotesize', color=GRAY),
]
HIDDEN_DRAWN = set()                  # curves whose far side is drawn dotted (none)


def visible_runs(pts):
    """the maximal runs of front-side points of a polyline"""
    out, cur = [], []
    for p in pts:
        if visible(p):
            cur.append(p)
        elif cur:
            out.append(np.array(cur))
            cur = []
    if cur:
        out.append(np.array(cur))
    return out
strokes['d'] = (
    [np.array([proj(p) for p in pts]) for k, (pts, _) in curves3.items()
     if k in HIDDEN_DRAWN or k in ('theta_arc', 'phi_arc', 'spin')]
    + [np.array([proj(p) for p in run]) for k, (pts, _) in curves3.items()
       if k in ('equator', 'meridian', 'parallel') and k not in HIDDEN_DRAWN
       for run in visible_runs(pts)]
    + [np.array([proj(t0), proj(t1)]) for t0, t1, _ in arrows3.values()]
    + [np.array([proj(t0), proj(t1)]) for t0, t1, _ in lines3.values()]
)


def seg_hits_box(p, q, lo, hi):
    """Liang-Barsky: does the segment p-q enter the box [lo, hi]?"""
    d = q - p
    t0, t1 = 0.0, 1.0
    for k in range(2):
        for sign, bound in ((-1.0, lo[k]), (1.0, hi[k])):
            den = sign * d[k]
            num_ = sign * (bound - p[k])
            if abs(den) < 1e-15:
                if num_ < 0:
                    return False
                continue
            tt = num_ / den
            if den < 0:
                t0 = max(t0, tt)
            else:
                t1 = min(t1, tt)
            if t0 > t1:
                return False
    return True


def fmt_box(L):
    return '[%.2f..%.2f]x[%.2f..%.2f]' % (L.lo[0], L.hi[0], L.lo[1], L.hi[1])


problems = []
for i, L in enumerate(labels):
    (x0, x1), (y0, y1) = BOUNDS[L.panel]
    if not (x0 <= L.lo[0] and L.hi[0] <= x1 and y0 <= L.lo[1] and L.hi[1] <= y1):
        problems.append('label/bounds %s %s  (panel %s)' % (L.text, fmt_box(L), L.panel))
    for M in labels[i + 1:]:
        if L.panel == M.panel and np.all(L.lo < M.hi) and np.all(M.lo < L.hi):
            problems.append('label/label  %s %s  vs  %s %s'
                            % (L.text, fmt_box(L), M.text, fmt_box(M)))
    for j, poly in enumerate(strokes[L.panel]):
        hits = [k for k in range(len(poly) - 1)
                if seg_hits_box(poly[k], poly[k + 1], L.lo, L.hi)]
        if hits:
            k = hits[0]
            problems.append('label/stroke %s %s  (panel %s, stroke %d near (%.2f,%.2f))'
                            % (L.text, fmt_box(L), L.panel, j, *poly[k]))
            break
if problems:
    print('OVERLAPS FOUND:')
    for p_ in problems:
        print('   ', p_)
    if not os.environ.get('FIG_DRAFT'):          # FIG_DRAFT=1: write anyway, to look
        raise SystemExit(1)
print('        overlap test: %d labels, %d strokes, no collisions'
      % (len(labels), sum(len(v) for v in strokes.values())))


# =====================================================================
#  PART 3 -- the pgfplots source
# =====================================================================
def f3(x):
    return '%.3f' % x


def coords(*pts):
    return ' '.join('(%s,%s)' % (f3(p[0]), f3(p[1])) for p in pts)


def into_page(cx, cy, r, col='gray!75'):
    """a circled cross at (cx,cy): a direction into the page"""
    d = r / np.sqrt(2)
    return '\n'.join([
        '\\addplot[semithick,%s,domain=0:360,samples=37] '
        '({%s+%s*cos(x)},{%s+%s*sin(x)});' % (col, f3(cx), f3(r), f3(cy), f3(r)),
        '\\addplot[semithick,%s] coordinates {%s};'
        % (col, coords((cx - d, cy - d), (cx + d, cy + d))),
        '\\addplot[semithick,%s] coordinates {%s};'
        % (col, coords((cx - d, cy + d), (cx + d, cy - d))),
    ])


def nodes(panel):
    return '\n'.join(L.tex() for L in labels if L.panel == panel)


tex = []
tex.append(r'''%% ---------------------------------------------------------------------
%%  GENERATED by fig_ch7_planet.py -- do not edit; edit the script.
%%  Figure J of Chapter 7: the geometry of Problem 3.
%%  Panels (a),(b): latitude %(phi).0f deg; panel (b) draws omega^2 R / g = %(exag).2f
%%  (Earth: %(eps).4f) so that the tilt of the plumb line is visible.
%% ---------------------------------------------------------------------
\begin{tikzpicture}[
   ar/.style={-{Stealth[length=2.4mm]},thick},
   sm/.style={-{Stealth[length=1.9mm]},semithick},
   guide/.style={gray!65,densely dashed,thin}]
\pgfplotsset{
   panel/.style={axis lines=none, x=%(sc).2fcm, y=%(sc).2fcm, clip=false,
                 every axis plot/.append style={no markers, line join=round}}}
''' % dict(phi=PHI, exag=EXAG, eps=EPS, sc=SCALE))


def bounds(panel):
    (x0, x1), (y0, y1) = BOUNDS[panel]
    return 'xmin=%s, xmax=%s, ymin=%s, ymax=%s' % tuple(map(f3, (x0, x1, y0, y1)))

# ------------------------------- panel (a) ----------------------------
tex.append(r'''%% ======================= (a) the planet =======================
\begin{axis}[panel, name=pa, %(bounds)s]
%% the planet in the meridional section through the station, and its equator
\addplot[thick,gray!55,fill=blue!4,domain=0:360,samples=181,smooth]
   ({%(RA)s*cos(x)},{%(RA)s*sin(x)});
\addplot[guide] coordinates {(-%(RA)s,0) (%(RA)s,0)};
%% the axis  e_3  and the spin about it
\addplot[guide] coordinates {%(axis)s};
\addplot[ar] coordinates {%(axistip)s};
\addplot[{Stealth[length=1.9mm]}-,semithick,red!65!black,domain=-15:200,samples=40]
   ({%(sx)s*cos(x)},{%(scy)s+%(sy)s*sin(x)});
\addplot[only marks,mark=*,mark size=1.4pt,black] coordinates {(0,0)};
%% the equatorial radial direction at the station's longitude, and the latitude
\addplot[ar,gray!70] coordinates {%(frho)s};
\addplot[guide,domain=0:%(phi)s,samples=20]
   ({%(phr)s*cos(x)},{%(phr)s*sin(x)});
%% the station: distance R from the centre, R cos(phi) from the axis
\addplot[thick] coordinates {%(Rline)s};
\addplot[guide] coordinates {%(cosline)s};
%% the local triad:  f_U outward, f_N along the meridian, f_E into the page
\addplot[ar,blue!55!black] coordinates {%(fU)s};
\addplot[ar,blue!55!black] coordinates {%(fN)s};
%(fE)s
%(nodes)s
\end{axis}
''' % dict(
    RA=f3(RA), bounds=bounds('a'),
    axis=coords(a['axis_lo'], a['axis_hi']),
    axistip=coords(a['axis_hi'], a['axis_tip']),
    sx=f3(a['spin_ab'][0]), sy=f3(a['spin_ab'][1]), scy=f3(a['spin_c'][1]),
    frho=coords((0, 0), a['frho_tip']),
    phi=f3(PHI), phr=f3(a['phi_arc_r']),
    Rline=coords((0, 0), a['R_line_end']),
    cosline=coords(a['foot'], a['cos_line_end']),
    fU=coords(a['fU_tail'], a['fU_tip']),
    fN=coords(a['fN_tail'], a['fN_tip']),
    fE=into_page(P[0], P[1], r_sym),
    nodes=nodes('a')))

# ------------------------------- panel (b) ----------------------------
ticks = ','.join(f3(x) for x in b['ticks'])
tex.append(r'''%% ======================= (b) the station ======================
\begin{axis}[panel, name=pb, %(bounds)s, at={(pa.east)}, anchor=west, xshift=4mm]
%% the horizon, with the ground hatched beneath it
\addplot[thick,gray!60] coordinates {%(hz)s};
\pgfplotsinvokeforeach{%(ticks)s}{
   \addplot[gray!45,thin] coordinates {(#1,0) (#1-0.16,-0.20)};}
%% the observer's fixed triad:  north to the left, up, east into the page
\addplot[ar] coordinates {%(N)s};
\addplot[ar] coordinates {%(U)s};
%(E)s
%% the angular velocity, at elevation phi above the northern horizon
\addplot[ar,red!65!black] coordinates {%(om)s};
\addplot[guide,domain=%(phi0)s:180,samples=20]
   ({%(phr)s*cos(x)},{%(phr)s*sin(x)});
%% gravity, the centrifugal term (perpendicular to the axis) and their sum
\addplot[ar,gray!70] coordinates {%(g)s};
\addplot[sm,red!65!black] coordinates {%(cf)s};
\addplot[ar,blue!55!black] coordinates {%(geff)s};
\addplot[guide,domain=-90:%(d1)s,samples=12]
   ({%(dr)s*cos(x)},{%(dr)s*sin(x)});
%(nodes)s
\end{axis}
''' % dict(
    bounds=bounds('b'), hz=coords(b['hz_l'], b['hz_r']), ticks=ticks,
    N=coords(b['N_tail'], b['N_tip']), U=coords(b['U_tail'], b['U_tip']),
    E=into_page(0.0, 0.0, r_sym),
    om=coords(b['om_tail'], b['om_tip']),
    phi0=f3(180.0 - PHI), phr=f3(b['phi_arc_r']),
    g=coords(b['g_tail'], b['g_tip']),
    cf=coords(b['cf_tail'], b['cf_tip']),
    geff=coords(b['geff_tail'], b['geff_tip']),
    d1=f3(-90.0 + delta_draw), dr=f3(b['delta_arc_r']),
    nodes=nodes('b')))


# ------------------------------- panel (c) ----------------------------
WAB = SCALE * sum(BOUNDS[k][0][1] - BOUNDS[k][0][0] for k in 'ab') + 0.4  # cm, (a)+(b)
WC = round(WAB, 1)                                                     # cm, (c)
assert WAB <= 17.4, 'panels (a)+(b) wider than the text block: %.1f cm' % WAB


def table(y):
    return '\n'.join('%.1f %.5f' % (x_, y_) for x_, y_ in zip(phi_c, y))


tex.append(r'''%% ============ (c) the centrifugal term against latitude ===========
%%  Earth: omega^2 R = %(w2R).1f mm/s^2; the plumb line tilts most, by
%%  %(dmax).1f arcmin, at phi = %(pmax).1f deg  (quoted in the caption).
\begin{axis}[name=pc, at={(pa.south west)}, anchor=outer north west,
   xshift=%(xs).1fmm, yshift=-3mm,
   width=%(wc).1fcm, height=4.9cm,
   xmin=0, xmax=90, ymin=0, ymax=1.05,
   xtick={0,15,...,90}, ytick={0,0.25,0.5,0.75,1},
   xticklabel={$\pgfmathprintnumber{\tick}^{\circ}$},
   yticklabel={$\pgfmathprintnumber{\tick}$},
   tick label style={font=\footnotesize},
   xlabel={(c) the centrifugal term against the latitude $\varphi$},
   ylabel={in units of $\omega^{2}R$},
   label style={font=\small},
   axis lines=left, axis line style={thin,gray!70},
   grid=major, grid style={gray!20, thin},
   legend style={font=\footnotesize, draw=none, fill=none,
                 at={(0.5,1.02)}, anchor=south, legend columns=-1,
                 /tikz/every even column/.append style={column sep=0.45cm}},
   legend cell align=left,
   every axis plot/.append style={no markers, line join=round, thick}]
\addplot[red!65!black]  table {
%(mag)s
};
\addlegendentry{$\cos\varphi$, the magnitude}
\addplot[blue!55!black] table {
%(vert)s
};
\addlegendentry{$\cos^{2}\!\varphi$, along $\be^{+}_{U}$}
\addplot[blue!55!black,densely dashed] table {
%(horz)s
};
\addlegendentry{$\sin\varphi\cos\varphi$, along $-\be^{+}_{N}$}
\addplot[guide,forget plot] coordinates {(45,0) (45,0.5)};
\addplot[only marks,mark=*,mark size=1.6pt,blue!55!black,forget plot]
   coordinates {(45,0.5)};
\end{axis}
\end{tikzpicture}
''' % dict(mag=table(curves['mag']), vert=table(curves['vert']),
           horz=table(curves['horz']),
           w2R=1e3 * OMEGA**2 * RADIUS, dmax=tilt_max_arcmin, pmax=phi_max_deg,
           wc=WC, xs=10.0 * (WAB - WC) / 2))

io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(tex))
print('PART 3  wrote', os.path.relpath(OUT, HERE))


# ---------------------------- the 3-d figure --------------------------
def c3(p):
    return '(%s,%s,%s)' % tuple(f3(x) for x in p)


def runs(pts, style, hidden_style=None):
    """split a polyline into front (solid) and back (dotted, or omitted) runs"""
    out = []
    vis = [bool(visible(p)) for p in pts]
    i = 0
    while i < len(pts):
        j = i
        while j + 1 < len(pts) and vis[j + 1] == vis[i]:
            j += 1
        seg = pts[i:j + 2]                        # overlap one point for continuity
        st_ = style if vis[i] else hidden_style
        if st_ is not None:
            out.append('\\addplot3[%s] coordinates {%s};'
                       % (st_, ' '.join(c3(p) for p in seg)))
        i = j + 1
    return '\n'.join(out)


t3 = [r'''%% ---------------------------------------------------------------------
%%  GENERATED by fig_ch7_planet.py -- do not edit; edit the script.
%%  Figure K of Chapter 7: the geometry of Problem 3 in three dimensions,
%%  longitude %(th).0f deg, latitude %(phi).0f deg, R = 1.  Explicit unit vectors
%%  (azimuth %(az).0f, elevation %(el).0f); curves on the far side are dotted.
%% ---------------------------------------------------------------------
\begin{tikzpicture}[
   ar/.style={-{Stealth[length=2.4mm]},thick},
   sm/.style={-{Stealth[length=1.9mm]},semithick},
   guide/.style={gray!65,densely dashed,thin},
   back/.style={gray!45,dotted,thin}]
\begin{axis}[axis lines=none, clip=false,
   x={(%(ux).3fcm,%(wx).3fcm)}, y={(%(uy).3fcm,%(wy).3fcm)}, z={(0cm,%(wz).3fcm)},
   xmin=-1.6, xmax=1.6, ymin=-1.6, ymax=1.6, zmin=-1.2, zmax=1.6,
   every axis plot/.append style={no markers, line join=round}]
%% the sphere, as a translucent surface
\addplot3[surf, shader=flat, draw=gray!35, line width=0.15pt, fill=blue!25,
   opacity=0.13, z buffer=sort, samples=37, samples y=19,
   domain=0:360, y domain=-90:90]
   ({cos(x)*cos(y)},{sin(x)*cos(y)},{sin(y)});
''' % dict(th=THETA, phi=PHI, az=AZ, el=EL,
           ux=S3 * U3[0], wx=S3 * W3[0], uy=S3 * U3[1], wy=S3 * W3[1],
           wz=S3 * W3[2])]
t3.append('% the equator, the meridian of the station and its parallel')
for name in ('equator', 'meridian', 'parallel'):
    pts, sty = curves3[name]
    t3.append(runs(pts, sty, 'back' if name in HIDDEN_DRAWN else None))
t3.append('% the fixed triad and the axis, the radial direction, the angles')
for name in ('axis',):
    t0, t1, sty = lines3[name]
    t3.append('\\addplot3[%s] coordinates {%s %s};' % (sty, c3(t0), c3(t1)))
for name in ('e1', 'e2', 'e3', 'frho'):
    t0, t1, sty = arrows3[name]
    t3.append('\\addplot3[%s] coordinates {%s %s};' % (sty, c3(t0), c3(t1)))
for name in ('theta_arc', 'phi_arc'):
    pts, sty = curves3[name]
    t3.append('\\addplot3[%s] coordinates {%s};' % (sty, ' '.join(c3(p) for p in pts)))
t3.append('% the station, its distances from the centre and from the axis')
for name in ('R', 'Rcos'):
    t0, t1, sty = lines3[name]
    t3.append('\\addplot3[%s] coordinates {%s %s};' % (sty, c3(t0), c3(t1)))
t3.append('\\addplot3[only marks,mark=*,mark size=1.6pt,black] coordinates {%s %s};'
          % (c3(0 * E1), c3(P3)))
t3.append('% the moving triad at the station')
for name in ('fE', 'fN', 'fU'):
    t0, t1, sty = arrows3[name]
    t3.append('\\addplot3[%s] coordinates {%s %s};' % (sty, c3(t0), c3(t1)))
t3.append('% the spin about the axis')
pts, sty = curves3['spin']
t3.append('\\addplot3[%s] coordinates {%s};' % (sty, ' '.join(c3(p) for p in pts)))
t3.append(nodes('d'))
t3.append('\\end{axis}\n\\end{tikzpicture}\n')
io.open(OUT3D, 'w', encoding='utf-8', newline='\n').write('\n'.join(t3))
print('        wrote', os.path.relpath(OUT3D, HERE))
