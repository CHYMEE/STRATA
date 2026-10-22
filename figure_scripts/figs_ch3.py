"""Chapter 3 figure for the STRATA thesis: research gaps G1-G4 mapped to RQ1-RQ5.

Drawn at print size (7.5 in wide). Bold labels, 3D extruded blocks with sharp
edges and coloured headers, matching figs_ch1.py.
Usage: python figs_ch3.py <output_dir>
"""
import sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch
from matplotlib.colors import to_rgb

OUT = sys.argv[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.weight": "bold"})

def shade(c, f):
    r, g, b = to_rgb(c)
    if f < 1:
        return (r * f, g * f, b * f)
    return (r + (1 - r) * (f - 1), g + (1 - g) * (f - 1), b + (1 - b) * (f - 1))

def block(ax, x, y, w, h, color, tag, title, sub, d=0.06):
    ax.add_patch(Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                         fc=shade(color, 0.55), ec=shade(color, 0.40), lw=0.8, zorder=2))
    ax.add_patch(Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                         fc=shade(color, 1.30), ec=shade(color, 0.50), lw=0.8, zorder=2))
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.8, zorder=3))
    tw = 0.52
    ax.add_patch(Rectangle((x, y), tw, h, fc=color, ec=color, lw=1.8, zorder=4))
    ax.text(x + tw / 2, y + h / 2, tag, ha="center", va="center", color="white", fontsize=10.5, fontweight="bold", zorder=5)
    ax.text(x + tw + 0.10, y + h * 0.66, title, ha="left", va="center", color="#16202b", fontsize=8.4, fontweight="bold", zorder=5)
    ax.text(x + tw + 0.10, y + h * 0.30, sub, ha="left", va="center", color="#37474f", fontsize=6.8, fontweight="bold", zorder=5)

W, H = 7.5, 4.9
fig = plt.figure(figsize=(W, H), dpi=400)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

ax.text(1.62, 4.62, "RESEARCH GAPS (Section 3.4)", ha="center", fontsize=9.4, fontweight="bold", color="#10243e")
ax.text(5.88, 4.62, "RESEARCH QUESTIONS", ha="center", fontsize=9.4, fontweight="bold", color="#10243e")

GAPS = [
    ("G1", "Mutable trust verdict", "Detection output alterable by its host", "#c62828"),
    ("G2", "Placement dilemma", "Fast ledgers not public; public ledgers not fast", "#ef6c00"),
    ("G3", "Durability and its cost", "Bridge risk; post-quantum vs device budget", "#2e7d32"),
    ("G4", "No composed, portable system", "Single implementation; no joint evaluation", "#1565c0"),
]
RQS = [
    ("RQ1", "Trust partitioning", "Hybrid ledger within device budgets"),
    ("RQ2", "Lightweight behavioural trust", "AI scoring inside device budgets"),
    ("RQ3", "Quantum-resilient identity", "PQC credentials without prohibitive cost"),
    ("RQ4", "Substrate independence", "Partition holds across ledgers"),
    ("RQ5", "Adversarial robustness", "Isolate a misbehaving node"),
]
gw, gh, gx = 3.15, 0.72, 0.12
rw, rh, rx = 3.05, 0.62, 4.33
gy = [3.55, 2.55, 1.55, 0.55]
ry = [3.62, 2.86, 2.10, 1.34, 0.58]
for (t, a, b, c), y in zip(GAPS, gy):
    block(ax, gx, y, gw, gh, c, t, a, b)
for (t, a, b), y in zip(RQS, ry):
    block(ax, rx, y, rw, rh, "#6a1b9a", t, a, b)

# gap index -> list of RQ indices (from the gap-to-question reasoning of Section 3.4)
LINKS = {0: [1, 4], 1: [0, 4], 2: [0, 2, 4], 3: [3, 4]}
for gi, targets in LINKS.items():
    c = GAPS[gi][3]
    n = len(targets)
    for k, ri in enumerate(targets):
        y0 = gy[gi] + gh * (0.25 + 0.5 * (k + 0.5) / n)
        y1 = ry[ri] + rh / 2 + (gi - 1.5) * (0.12 if ri == 4 else 0.07)
        ax.add_patch(FancyArrowPatch((gx + gw + 0.08, y0), (rx - 0.03, y1),
                                     arrowstyle="-|>,head_length=0.4,head_width=0.22", mutation_scale=10,
                                     lw=1.4, color=c, alpha=0.9, zorder=1, connectionstyle="arc3,rad=0.0"))

ax.text(W / 2, 0.18, "Arrow colour identifies the gap from which each research question follows",
        ha="center", va="center", fontsize=7.2, fontweight="bold", color="#37474f")
fig.savefig(os.path.join(OUT, "Fig3_gaps_rq.png"), dpi=400, facecolor="white")
print("done")
