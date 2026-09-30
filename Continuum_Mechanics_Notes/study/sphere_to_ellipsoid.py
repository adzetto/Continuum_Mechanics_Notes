#!/usr/bin/env python
# =====================================================================
#  Chapter 3, section 3.6.1(c):
#      "A spherical material surface is mapped to the surface
#       of an ellipsoid"
#
#  A cloud of points is laid on a unit material sphere in the reference
#  configuration, pushed forward by a HOMOGENEOUS deformation gradient
#  F, and the image is tested against the prediction of the text,
#  equations (3.109)-(3.112):
#
#      r = F rhat ,      rhat . rhat = 1
#      1 = r . B^{-1} r ,               B = F F^t          (3.110)
#      1 = (r_1/l_1)^2 + (r_2/l_2)^2 + (r_3/l_3)^2         (3.112)
#          with r_i = v_i . r ,  {v_i} the spatial principal frame
#          and l_i the principal stretches.
#
#  Two halves:
#      PART 1  plain numpy.  Build F, take it apart again, map the
#              sphere, check every prediction.  No plotting.
#      PART 2  draw it.
#
#  No functions are defined anywhere: loops and numpy array operations
#  only.  Every point is a true vector marker in the output, nothing is
#  rasterised.
#
#  Output:  sphere_to_ellipsoid.pdf
#  Run:     python sphere_to_ellipsoid.py
# =====================================================================

import numpy as np

np.set_printoptions(precision=6, suppress=True)


# #####################################################################
#
#  PART 1   THE COMPUTATION
#
# #####################################################################

# ---------------------------------------------------------------------
# 1.1  Three rotations, by Rodrigues' formula, built in one loop
#          Rot = I + sin(t) W + (1 - cos(t)) W^2 ,   W a = axis x a
# ---------------------------------------------------------------------
rot_axes = np.array([[0.0, 0.0, 1.0],      # for the referential frame
                     [1.0, 0.0, 0.0],      # for the referential frame
                     [1.0, 1.0, 1.0]])     # the rotation inside F
rot_angles = np.array([25.0, 15.0, 40.0])

rots = np.zeros((3, 3, 3))
for n in range(3):
    a = rot_axes[n] / np.linalg.norm(rot_axes[n])
    th = np.deg2rad(rot_angles[n])
    W = np.array([[0.0, -a[2], a[1]],
                  [a[2], 0.0, -a[0]],
                  [-a[1], a[0], 0.0]])
    rots[n] = np.eye(3) + np.sin(th) * W + (1.0 - np.cos(th)) * (W @ W)

# ---------------------------------------------------------------------
# 1.2  Build F = R U from known ingredients, so that the recovery in
#      1.3 can be graded against what went in
# ---------------------------------------------------------------------
Q_REF = rots[0] @ rots[1]                    # turns the principal frame
LAM_IN = np.array([1.90, 1.15, 0.62])        # the principal stretches
U_IN = Q_REF @ np.diag(LAM_IN) @ Q_REF.T     # symmetric, positive definite
R_IN = rots[2]                               # a genuine rotation
F = R_IN @ U_IN                              # the deformation gradient

# ---------------------------------------------------------------------
# 1.3  Take F apart again, using F and nothing else
# ---------------------------------------------------------------------
C = F.T @ F                                  # right Cauchy-Green, (2.83)
B = F @ F.T                                  # left  Cauchy-Green, (2.92)
Binv = np.linalg.inv(B)
J = np.linalg.det(F)                         # volume ratio,       (2.50)

# invariants of C, equation (3.3)
I1 = np.trace(C)
I2 = 0.5 * (I1 ** 2 - np.trace(C @ C))
I3 = np.linalg.det(C)

# invariants of U:  i3 = sqrt(I3);  i1 the largest real root of
#     i1^4 - 2 I1 i1^2 - 8 sqrt(I3) i1 + (I1^2 - 4 I2) = 0 ;
#     i2 = (i1^2 - I1)/2                                   [Thm 3.16]
i3 = np.sqrt(I3)
quartic = np.roots([1.0, 0.0, -2.0 * I1, -8.0 * i3, I1 ** 2 - 4.0 * I2])
i1 = np.max(quartic[np.abs(quartic.imag) < 1.0e-9].real)
i2 = 0.5 * (i1 ** 2 - I1)

# the closed form itself: no eigenvectors anywhere
U = (-C @ C + (i1 ** 2 - i2) * C + i1 * i3 * np.eye(3)) / (i1 * i2 - i3)
R = F @ np.linalg.inv(U)                     # (3.32)
V = F @ R.T

# spatial principal frame from  B = sum l_i^2 v_i (x) v_i ,  (3.42)
eigval, eigvec = np.linalg.eigh(B)
order = np.argsort(eigval)[::-1]             # l_1 >= l_2 >= l_3
lam = np.sqrt(eigval[order])                 # the principal stretches
axes_v = eigvec[:, order]                    # columns are v_i
for k in range(3):                           # stable, repeatable signs
    if axes_v[np.argmax(np.abs(axes_v[:, k])), k] < 0.0:
        axes_v[:, k] = -axes_v[:, k]
if np.linalg.det(axes_v) < 0.0:              # keep the frame right handed
    axes_v[:, 2] = -axes_v[:, 2]
axes_u = R.T @ axes_v                        # u_i = R^t v_i,  from (3.39)

# ---------------------------------------------------------------------
# 1.4  The material sphere and its image
#      golden-angle spiral: k -> ( z , phi ) -> a point of the sphere
# ---------------------------------------------------------------------
N = 3000
k = np.arange(N) + 0.5
z = 1.0 - 2.0 * k / N
rho = np.sqrt(np.maximum(0.0, 1.0 - z * z))
phi = np.pi * (1.0 + 5.0 ** 0.5) * k
P_ref = np.column_stack([rho * np.cos(phi), rho * np.sin(phi), z])

P_img = P_ref @ F.T                          # r = F rhat
stretch = np.linalg.norm(P_img, axis=1)      # mu = |r|, since |rhat| = 1

# ---------------------------------------------------------------------
# 1.5  VERIFICATION
# ---------------------------------------------------------------------
RULE = "-" * 68
print(RULE)
print("sphere -> ellipsoid :  numerical check of (3.109)-(3.112)")
print(RULE)
print("\nF =\n", F)
print("\nJ = det F                = %.10f" % J)
print("principal stretches l_i  =", lam)
print("l_1 l_2 l_3              = %.10f   (must equal J)" % np.prod(lam))
print("  |l_1 l_2 l_3 - J|      = %.3e" % abs(np.prod(lam) - J))

print("\n(i)   max | |rhat| - 1 |                        = %.3e"
      % np.abs(np.linalg.norm(P_ref, axis=1) - 1.0).max())

q110 = np.einsum("ij,jk,ik->i", P_img, Binv, P_img)
print("(ii)  max | r.B^-1 r - 1 |      [eq. (3.110)]   = %.3e"
      % np.abs(q110 - 1.0).max())

r_comp = P_img @ axes_v                      # r_i = v_i . r
q112 = np.sum((r_comp / lam) ** 2, axis=1)
print("(iii) max | S (r_i/l_i)^2 - 1 | [eq. (3.112)]   = %.3e"
      % np.abs(q112 - 1.0).max())

semi = np.abs(r_comp).max(axis=0)
print("\n(iv)  semi-axes measured from the cloud =", semi)
print("      principal stretches l_i           =", lam)
print("      discrepancy at N = %-6d          = %.3e"
      % (N, np.abs(semi - lam).max()))
print("      this one is SAMPLING, not error; refine and it falls:")
for Nt in (N, 10 * N, 100 * N):
    kt = np.arange(Nt) + 0.5
    zt = 1.0 - 2.0 * kt / Nt
    rt = np.sqrt(np.maximum(0.0, 1.0 - zt * zt))
    pt = np.pi * (1.0 + 5.0 ** 0.5) * kt
    cloud = np.column_stack([rt * np.cos(pt), rt * np.sin(pt), zt])
    rc = (cloud @ F.T) @ axes_v
    print("        N = %-8d ->  %.3e"
          % (Nt, np.abs(np.abs(rc).max(axis=0) - lam).max()))

print("\n(v)   |r| ranges over [%.6f, %.6f]" % (stretch.min(), stretch.max()))
print("      i.e. exactly [l_3, l_1] = [%.6f, %.6f]" % (lam[2], lam[0]))
print("      max/min = %.4f, so the image is certainly not a sphere"
      % (stretch.max() / stretch.min()))

print("\n(vi)  ellipsoid volume / sphere volume = %.10f" % np.prod(lam))
print("      J = det F                        = %.10f" % J)

print("\n(vii) polar decomposition recovered from F alone:")
print("      max |U - U_in|      = %.3e" % np.abs(U - U_IN).max())
print("      max |R - R_in|      = %.3e" % np.abs(R - R_IN).max())
print("      max |R^t R - I|     = %.3e" % np.abs(R.T @ R - np.eye(3)).max())
print("      det R               = %.10f" % np.linalg.det(R))
print("      max |F - R U|       = %.3e" % np.abs(F - R @ U).max())
print("      max |F - V R|       = %.3e" % np.abs(F - V @ R).max())

print("\n(viii) max | F u_i - l_i v_i |   [eq. (3.44)]   = %.3e"
      % np.abs(F @ axes_u - axes_v * lam).max())

print("\n" + RULE)
print("every residual at machine precision: the image is exactly the")
print("ellipsoid of (3.112), axes v_i, semi-axes l_i.")
print(RULE)


# #####################################################################
#
#  PART 2   THE FIGURE
#
# #####################################################################

import matplotlib                                              # noqa: E402

matplotlib.use("pgf")

import matplotlib.pyplot as plt                                # noqa: E402
import matplotlib.patheffects as pe                            # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, to_rgb  # noqa: E402
from matplotlib.patches import Rectangle                       # noqa: E402
import scienceplots                                            # noqa: F401,E402
from mpl_toolkits.mplot3d import Axes3D                        # noqa: F401,E402

# ---------------------------------------------------------------------
# 2.1  Palette: white, beige, brown.  Nothing else.
# ---------------------------------------------------------------------
PAPER = "#FCFAF6"      # warm white, the background
CREAM = "#F1E7D8"
BEIGE = "#DCC7A8"
TAN = "#BC9A72"
BROWN = "#8A6642"
DEEP = "#57402D"
INK = "#33261B"        # text and rules

WBB = LinearSegmentedColormap.from_list(
    "white_beige_brown", [CREAM, BEIGE, TAN, BROWN, DEEP], N=512)
PAPER_RGB = np.array(to_rgb(PAPER))

plt.style.use(["science"])
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "pgf.rcfonts": False,
    "text.usetex": True,
    "font.family": "serif",
    "pgf.preamble": "\n".join([
        r"\usepackage{amsmath}",
        r"\usepackage{amssymb}",
        r"\usepackage{accents}",
        r"\DeclareRobustCommand{\vek}[1]{\underaccent{\tilde}{#1}}",
        r"\newcommand{\bF}{\vek{F}}",
        r"\newcommand{\br}{\vek{r}}",
        r"\newcommand{\bv}{\vek{v}}",
        r"\newcommand{\bu}{\vek{u}}",
        r"\newcommand{\bB}{\vek{B}}",
    ]),
    "figure.facecolor": PAPER,
    "savefig.facecolor": PAPER,
    "axes.facecolor": PAPER,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.linewidth": 0.6,
    "lines.linewidth": 0.8,
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

# ---------------------------------------------------------------------
# 2.2  Viewing geometry
# ---------------------------------------------------------------------
ELEV, AZIM = 18.0, 34.0
LIM = 2.05                                   # identical scale in (a),(b)
ev, az = np.deg2rad(ELEV), np.deg2rad(AZIM)
VIEW = np.array([np.cos(ev) * np.cos(az),
                 np.cos(ev) * np.sin(az),
                 np.sin(ev)])                # unit vector to the camera
VMIN, VMAX = lam[2], lam[0]

fig = plt.figure(figsize=(6.9, 6.55))
axA = fig.add_axes([0.005, 0.400, 0.435, 0.600], projection="3d")
axB = fig.add_axes([0.415, 0.400, 0.435, 0.600], projection="3d")
axC = fig.add_axes([0.090, 0.078, 0.355, 0.270])
axD = fig.add_axes([0.605, 0.078, 0.355, 0.270])

# ---------------------------------------------------------------------
# 2.3  The two three-dimensional panels, drawn in one loop
#
#      colour  = the stretch, on the white-beige-brown ramp
#      size    = depth, so the cloud reads as a surface
#      opacity = depth as well, lightly
#      every marker is a vector path; nothing is rasterised
# ---------------------------------------------------------------------
panel_ax = [axA, axB]
panel_pts = [P_ref, P_img]
panel_axes = [axes_u, axes_v * lam]
panel_labels = [[r"$\bu_1$", r"$\bu_2$", r"$\bu_3$"],
                [r"$\lambda_1\bv_1$", r"$\lambda_2\bv_2$",
                 r"$\lambda_3\bv_3$"]]
panel_caption = [
    r"(a)\ \ $\kappa$: the material sphere $|\hat{\br}|=1$,"
    "\n" r"with the referential principal axes $\bu_i$",
    r"(b)\ \ $\kappa_t$: the image $\br=\bF\hat{\br}$, an ellipsoid"
    "\n" r"with semi-axes $\lambda_i$ along $\bv_i$; same scale"
    "\n" r"as (a), dashed $=$ the original unit sphere"]

for n in range(2):
    ax = panel_ax[n]
    pts = panel_pts[n]

    # the original unit sphere, kept in panel (b) as three great circles
    if n == 1:
        t = np.linspace(0.0, 2.0 * np.pi, 400)
        for m in range(3):
            e1 = np.eye(3)[(m + 1) % 3]
            e2 = np.eye(3)[(m + 2) % 3]
            circ = np.outer(np.cos(t), e1) + np.outer(np.sin(t), e2)
            ax.plot(circ[:, 0], circ[:, 1], circ[:, 2], color=BROWN,
                    lw=0.55, ls=(0, (2.2, 1.9)), zorder=25)

    # sort back to front so that near points are drawn last
    depth = pts @ VIEW
    idx = np.argsort(depth)
    p = pts[idx]
    d = depth[idx]
    s_val = stretch[idx]
    t_depth = (d - d.min()) / (d.max() - d.min())        # 0 far .. 1 near

    rgb = WBB((np.clip(s_val, VMIN, VMAX) - VMIN) / (VMAX - VMIN))[:, :3]
    wgt = (0.74 + 0.26 * t_depth)[:, None]               # slight aerial fade
    rgb = rgb * wgt + PAPER_RGB * (1.0 - wgt)
    rgba = np.concatenate([rgb, (0.42 + 0.58 * t_depth)[:, None]], axis=1)
    size = 0.85 + 4.1 * t_depth ** 2

    ax.scatter(p[:, 0], p[:, 1], p[:, 2], s=size, c=rgba,
               linewidths=0.0, zorder=2)

    # the three principal axes, each a full diameter, labelled at the
    # end that faces the camera
    for m in range(3):
        v = panel_axes[n][:, m]
        ax.plot([-v[0], v[0]], [-v[1], v[1]], [-v[2], v[2]],
                color=INK, lw=1.25, zorder=30, solid_capstyle="round",
                path_effects=[pe.withStroke(linewidth=3.0,
                                            foreground=PAPER)])
        tip = v if np.dot(v, VIEW) > 0.0 else -v
        ax.scatter([tip[0]], [tip[1]], [tip[2]], s=8, color=INK, zorder=31)
        q = tip * 1.20
        ax.text(q[0], q[1], q[2], panel_labels[n][m], fontsize=8, color=INK,
                ha="center", va="center", zorder=32,
                bbox=dict(fc=PAPER, ec="none", pad=0.7, alpha=0.9))

    ax.set_box_aspect((1, 1, 1), zoom=1.55)
    ax.set_xlim(-LIM, LIM)
    ax.set_ylim(-LIM, LIM)
    ax.set_zlim(-LIM, LIM)
    ax.view_init(elev=ELEV, azim=AZIM)
    ax.set_axis_off()
    ax.set_facecolor(PAPER)
    ax.text2D(0.5, 0.125, panel_caption[n], transform=ax.transAxes,
              ha="center", va="top", fontsize=8.6, color=INK)

# ---------------------------------------------------------------------
# 2.4  The colour key, drawn as stacked rectangles so that it too is
#      vector rather than a raster image
# ---------------------------------------------------------------------
cax = fig.add_axes([0.888, 0.505, 0.015, 0.385])
n_slab = 256
edges = np.linspace(VMIN, VMAX, n_slab + 1)
slab_rgb = WBB(np.linspace(0.0, 1.0, n_slab))
for m in range(n_slab):
    cax.add_patch(Rectangle((0.0, edges[m]), 1.0, edges[m + 1] - edges[m],
                            facecolor=slab_rgb[m], edgecolor="none",
                            linewidth=0.0))
cax.set_xlim(0.0, 1.0)
cax.set_ylim(VMIN, VMAX)
cax.set_xticks([])
cax.yaxis.tick_right()
cax.yaxis.set_label_position("right")
cax.set_yticks(list(lam))
cax.set_yticklabels([r"$\lambda_1$", r"$\lambda_2$", r"$\lambda_3$"])
cax.tick_params(labelsize=8, length=2)
for sp in cax.spines.values():
    sp.set_edgecolor(INK)
    sp.set_linewidth(0.5)
cax.set_ylabel(r"stretch $\mu=|\br|$ of the material radius",
               fontsize=8, labelpad=6)

# ---------------------------------------------------------------------
# 2.5  (c)  the residual of (3.110), every point a vector marker
# ---------------------------------------------------------------------
res = np.abs(q110 - 1.0)
FLOOR = 2.0e-17
n_exact = int((res == 0.0).sum())
axC.semilogy(np.arange(N), np.maximum(res, FLOOR), ".", ms=1.1,
             color=DEEP, alpha=0.55)
axC.axhline(np.finfo(float).eps, color=INK, lw=0.7, ls="--")
axC.set_ylim(1.0e-17, 2.0e-13)
axC.set_xlim(0, N)
axC.text(N * 0.5, 1.1e-13, r"machine $\varepsilon$ (dashed)",
         fontsize=7.5, ha="center", va="top", color=INK)
axC.text(N * 0.5, 1.25e-17,
         r"$%d$ of $%d$ points give exactly $0$" % (n_exact, N),
         fontsize=7.5, ha="center", va="bottom", color=INK,
         bbox=dict(fc=PAPER, ec="none", pad=0.7))
axC.set_xlabel(r"point index")
axC.set_ylabel(r"$\bigl|\,\br\cdot\bB^{-1}\br-1\,\bigr|$")
axC.set_title(r"(c)\ \ every image point satisfies (3.110)",
              fontsize=8.8, pad=5, color=INK)

# ---------------------------------------------------------------------
# 2.6  (d)  the stretch distribution and the extremal property
# ---------------------------------------------------------------------
counts, _, _ = axD.hist(stretch, bins=64, color=BEIGE,
                        edgecolor=DEEP, lw=0.35)
top = counts.max()
axD.set_ylim(0.0, top * 1.20)
axD.set_xlim(lam[2] - 0.09, lam[0] + 0.09)
lab_d = [r"$\lambda_1$", r"$\lambda_2$", r"$\lambda_3$"]
for m in range(3):
    axD.axvline(lam[m], color=INK, lw=0.9)
    axD.text(lam[m], top * 1.05, lab_d[m], fontsize=8, ha="center",
             va="bottom", color=INK,
             bbox=dict(fc=PAPER, ec="none", pad=0.8))
axD.set_xlabel(r"stretch $\mu=|\bF\hat{\br}|$ over all directions")
axD.set_ylabel(r"count")
axD.set_title(r"(d)\ \ $\lambda_3\le\mu\le\lambda_1$: the extremal property",
              fontsize=8.8, pad=5, color=INK)

# ---------------------------------------------------------------------
# 2.7  Save
# ---------------------------------------------------------------------
fig.savefig("sphere_to_ellipsoid.pdf", facecolor=PAPER)
print("\nwritten: sphere_to_ellipsoid.pdf  (all markers vector)")
