r"""fs9geom.py -- small geometry helpers shared by the ch9*_geom.py generators.

Everything is computed here in page points and written to ch9*_geom.tex as
\def macros; the bodies only style what the generators computed.
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
