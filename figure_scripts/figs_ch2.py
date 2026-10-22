"""Chapter 2 figure for the STRATA thesis: classical vs post-quantum artefact sizes.

Drawn at print size (7.5 in wide). Bold labels, 3D extruded bars with sharp
edges, coloured header panels, matching figs_ch1.py. Bars are drawn on a log10
axis because post-quantum artefacts are one to two orders of magnitude larger.
Sizes in bytes from FIPS 203/204/205 and the classical scheme definitions.
Usage: python figs_ch2.py <output_dir>
"""
import sys, os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from matplotlib.colors import to_rgb

OUT = sys.argv[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.weight": "bold",
                     "axes.labelweight": "bold"})

def shade(c, f):
    r, g, b = to_rgb(c)
    if f < 1:
        return (r * f, g * f, b * f)
    return (r + (1 - r) * (f - 1), g + (1 - g) * (f - 1), b + (1 - b) * (f - 1))

def hbar3d(ax, y, hgt, x0, x1, color, dx, dy):
    ax.add_patch(Rectangle((x0, y), x1 - x0, hgt, fc=color, ec=shade(color, 0.55), lw=0.8, zorder=3))
    ax.add_patch(Polygon([(x0, y + hgt), (x0 + dx, y + hgt + dy), (x1 + dx, y + hgt + dy), (x1, y + hgt)], closed=True,
                         fc=shade(color, 1.35), ec=shade(color, 0.55), lw=0.7, zorder=3))
    ax.add_patch(Polygon([(x1, y), (x1 + dx, y + dy), (x1 + dx, y + hgt + dy), (x1, y + hgt)], closed=True,
                         fc=shade(color, 0.62), ec=shade(color, 0.45), lw=0.7, zorder=3))

def panel(fig, rect, title, color):
    x, y, w, h = rect
    hb = 0.085
    bg = fig.add_axes([x, y, w, h], zorder=0)
    bg.set_xlim(0, 1); bg.set_ylim(0, 1); bg.axis("off")
    bg.add_patch(Rectangle((0.012, -0.012), 0.988, 0.988, fc="#9aa3ad", ec="none", zorder=0))
    bg.add_patch(Rectangle((0, 0), 0.988, 0.988, fc="white", ec=color, lw=1.6, zorder=1))
    bg.add_patch(Rectangle((0, 0.988 - hb), 0.988, hb, fc=color, ec=color, lw=1.6, zorder=2))
    bg.text(0.494, 0.988 - hb / 2, title, ha="center", va="center", color="white", fontsize=8.8, fontweight="bold", zorder=3)

CLASSIC, KEM, SIG = "#607d8b", "#159a9c", "#e0620d"
# (label, public key bytes, ciphertext-or-signature bytes, colour)
SCHEMES = [
    ("X25519", 32, 32, CLASSIC),
    ("ECDSA P-256", 64, 64, CLASSIC),
    ("RSA-2048", 256, 256, CLASSIC),
    ("ML-KEM-512", 800, 768, KEM),
    ("ML-KEM-768", 1184, 1088, KEM),
    ("ML-DSA-44", 1312, 2420, SIG),
    ("SLH-DSA-128s", 32, 7856, SIG),
]

def draw(ax, idx, xmax_log):
    n = len(SCHEMES)
    for i, s in enumerate(SCHEMES):
        v = s[idx]
        y = (n - 1 - i) + 0.2
        hbar3d(ax, y, 0.55, 1.0, math.log10(v), s[3], 0.05, 0.1)
        ax.text(math.log10(v) + 0.1, y + 0.27, f"{v:,} B", va="center", fontsize=7.6, fontweight="bold", color="#16202b")
    ax.set_xlim(1.0, xmax_log); ax.set_ylim(0, n + 0.05)
    ax.set_yticks([(n - 1 - i) + 0.47 for i in range(n)])
    ax.set_yticklabels([s[0] for s in SCHEMES], fontsize=7.6, fontweight="bold")
    ticks = [1, 2, 3, 4]
    ax.set_xticks(ticks); ax.set_xticklabels(["10", "100", "1,000", "10,000"], fontsize=7.4, fontweight="bold")
    ax.set_xlabel("Size in bytes (log scale)", fontsize=7.6)
    ax.grid(axis="x", ls="--", lw=0.4, alpha=0.5, zorder=0)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_linewidth(1.0)
    ax.axhline(n - 3 + 0.0, color="#37474f", lw=1.0, ls=(0, (4, 2)), zorder=4)

fig = plt.figure(figsize=(7.5, 3.6), dpi=400)
panel(fig, (0.005, 0.10, 0.49, 0.89), "(a) Public-key size", "#1f6fd1")
draw(fig.add_axes([0.14, 0.22, 0.33, 0.66]), 1, 4.55)
panel(fig, (0.505, 0.10, 0.49, 0.89), "(b) Ciphertext or signature size", "#6a1b9a")
draw(fig.add_axes([0.64, 0.22, 0.33, 0.66]), 2, 4.55)

leg = fig.add_axes([0, 0, 1, 0.09]); leg.axis("off"); leg.set_xlim(0, 1); leg.set_ylim(0, 1)
for x, c, t in [(0.05, CLASSIC, "Classical (quantum-vulnerable)"), (0.335, KEM, "Post-quantum KEM (FIPS 203)"),
                (0.61, SIG, "Post-quantum signature (FIPS 204/205)")]:
    leg.add_patch(Rectangle((x, 0.3), 0.022, 0.42, fc=c, ec=shade(c, 0.55), lw=0.8))
    leg.text(x + 0.03, 0.51, t, va="center", fontsize=7.6, fontweight="bold", color="#16202b")
fig.savefig(os.path.join(OUT, "Fig2_pqc_sizes.png"), dpi=400, facecolor="white")
print("done")
