r"""fsgeom.py -- small geometry helpers shared by the *_geom.py generators
of the figures of the notes (figures/chN/).

Everything is computed in page points and written to <name>_geom.tex as
\def macros; the figure bodies only style what the generators computed.
"""
import math

import numpy as np

R_POINT = 1.4 + 0.177      # outer radius of an fs point (2.8 pt circle, thin stroke)
GAP = 0.3                  # gap between a point marker and a line that meets it


def vec(*a):
    return np.array(a, dtype=float)


def rot(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return np.array([[c, -s], [s, c]])


def unit(v):
    return v / np.linalg.norm(v)


def normal(v):
    """Left normal of a direction."""
    u = unit(v)
    return np.array([-u[1], u[0]])


def fmt(p):
    return '(%.3f,%.3f)' % (p[0], p[1])


def trimmed(a, b, ta=0.0, tb=0.0):
    """Segment a->b shortened by ta at the start and tb at the end."""
    u = unit(b - a)
    return a + ta * u, b - tb * u


def between_points(a, b):
    """Segment between two point markers, leaving the marker gap at both ends."""
    t = R_POINT + GAP
    return trimmed(a, b, t, t)


def from_point(a, b):
    return trimmed(a, b, R_POINT + GAP, 0.0)


def to_point(a, b):
    return trimmed(a, b, 0.0, R_POINT + GAP)


def arc(center, radius, a0, a1, n=48):
    t = np.radians(np.linspace(a0, a1, n))
    return np.column_stack([center[0] + radius * np.cos(t),
                            center[1] + radius * np.sin(t)])


def path(P, cycle=False):
    s = ' -- '.join(fmt(p) for p in P)
    return s + (' -- cycle' if cycle else '')


class Out:
    def __init__(self):
        self.lines = []

    def pt(self, name, p):
        self.lines.append('\\def\\%s{%s}' % (name, fmt(p)))

    def num(self, name, x):
        self.lines.append('\\def\\%s{%.3f}' % (name, x))

    def raw(self, name, s):
        self.lines.append('\\def\\%s{%s}' % (name, s))

    def seg(self, name, a, b):
        self.lines.append('\\def\\%s{%s -- %s}' % (name, fmt(a), fmt(b)))

    def write(self, fn):
        with open(fn, 'w') as f:
            f.write('\n'.join(self.lines) + '\n')


class Camera:
    """Orthographic trimetric camera of the course figures: azimuth 35.0 deg,
    elevation 20.4 deg; y up, x to the right and down, z towards the viewer
    (left and down).  Unit images on the page:
        e_x = (cos az, -sin az sin el), e_y = (0, cos el),
        e_z = (-sin az, -cos az sin el).
    page(P, scale) maps model points (n x 3) to page points (n x 2);
    toward is the unit vector pointing from the scene to the viewer, so a
    face with outward normal n is seen from outside iff n . toward > 0.
    """

    def __init__(self, az=35.0, el=20.4):
        a, e = math.radians(az), math.radians(el)
        self.ex = np.array([math.cos(a), -math.sin(a) * math.sin(e)])
        self.ey = np.array([0.0, math.cos(e)])
        self.ez = np.array([-math.sin(a), -math.cos(a) * math.sin(e)])
        u = np.array([self.ex[0], self.ey[0], self.ez[0]])
        v = np.array([self.ex[1], self.ey[1], self.ez[1]])
        self.toward = np.cross(u, v)

    def page(self, P, scale=1.0):
        P = np.atleast_2d(np.asarray(P, dtype=float))
        Q = scale * (np.outer(P[:, 0], self.ex) + np.outer(P[:, 1], self.ey)
                     + np.outer(P[:, 2], self.ez))
        return Q[0] if Q.shape[0] == 1 else Q

    def faces_viewer(self, normal):
        return float(np.dot(normal, self.toward)) > 0.0


HOUSE = Camera()
