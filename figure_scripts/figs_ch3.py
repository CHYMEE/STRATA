"""Chapter 3 figure for the STRATA thesis: research gaps G1-G4 mapped to RQ1-RQ5.

Drawn at the printed text width (5.9 in) in Arial Black, with black tag blocks
and no caption inside the image (the caption is set in LaTeX).
Usage: python figs_ch3.py <output_dir>
"""
import sys, os, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch

OUT = sys.argv[1]
fm.fontManager.addfont("C:/Windows/Fonts/ariblk.ttf")
plt.rcParams.update({"font.family": ["Arial", "DejaVu Sans"], "font.weight": 900})
INK, SUB, TAG, EDGE = "#151515", "#3a3a3a", "#151515", "#2b2b2b"

W, H = 5.9, 4.75
fig = plt.figure(figsize=(W, H), dpi=400)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
R = fig.canvas.get_renderer()


def fit(x, y, s, maxw, fs, minfs=6.2, **kw):
    """Place text at (x, y), shrinking the font until it fits within maxw inches."""
    t = ax.text(x, y, s, fontsize=fs, **kw)
    while fs > minfs and t.get_window_extent(R).width / fig.dpi > maxw:
        fs -= 0.1
        t.set_fontsize(fs)
    return t


def block(x, y, w, h, tag, title, sub, tw, d=0.05):
    ax.add_patch(Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                         fc="#6e6e6e", ec="#4a4a4a", lw=0.7, zorder=2))
    ax.add_patch(Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                         fc="#9a9a9a", ec="#4a4a4a", lw=0.7, zorder=2))
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=EDGE, lw=1.5, zorder=3))
    ax.add_patch(Rectangle((x, y), tw, h, fc=TAG, ec=TAG, lw=1.5, zorder=4))
    fit(x + tw / 2, y + h / 2, tag, tw - 0.06, 11.0, ha="center", va="center", color="white", zorder=5)
    room = w - tw - 0.14
    fit(x + tw + 0.08, y + h * 0.70, title, room, 7.8, ha="left", va="center", color=INK, zorder=5)
    lines = textwrap.wrap(sub, 30)
    fit(x + tw + 0.08, y + h * 0.33, "\n".join(lines), room, 6.6, ha="left", va="center", color=SUB,
        zorder=5, linespacing=1.15)


GAPS = [
    ("G1", "Mutable trust verdict", "Detection output alterable by its host", "#8b1e3f"),
    ("G2", "Placement dilemma", "Fast ledgers not public; public ledgers not fast", "#c46a10"),
    ("G3", "Durability and its cost", "Bridge risk; post-quantum vs device budget", "#2f6b3b"),
    ("G4", "No composed, portable system", "Single implementation; no joint evaluation", "#1f4e79"),
]
RQS = [
    ("RQ1", "Trust partitioning", "Hybrid ledger within device budgets"),
    ("RQ2", "Lightweight behavioural trust", "AI scoring inside device budgets"),
    ("RQ3", "Quantum-resilient identity", "PQC credentials without prohibitive cost"),
    ("RQ4", "Substrate independence", "Partition holds across ledgers"),
    ("RQ5", "Adversarial robustness", "Isolate a misbehaving node"),
]
gw, gh, gx, gtw = 2.62, 0.86, 0.06, 0.5
rw, rh, rx, rtw = 2.62, 0.64, 3.2, 0.6
gy = [3.3, 2.32, 1.34, 0.36]
ry = [3.42, 2.66, 1.9, 1.14, 0.38]

ax.text(gx + gw / 2, 4.47, "RESEARCH GAPS", ha="center", va="center", fontsize=9.6, color=INK)
ax.text(rx + rw / 2, 4.47, "RESEARCH QUESTIONS", ha="center", va="center", fontsize=9.6, color=INK)
for (t, a, b, c), y in zip(GAPS, gy):
    block(gx, y, gw, gh, t, a, b, gtw)
for (t, a, b), y in zip(RQS, ry):
    block(rx, y, rw, rh, t, a, b, rtw)

# gap index -> RQ indices (from the gap-to-question reasoning of Section 3.4)
LINKS = {0: [1, 4], 1: [0, 4], 2: [0, 2, 4], 3: [3, 4]}
for gi, targets in LINKS.items():
    c = GAPS[gi][3]
    n = len(targets)
    for k, ri in enumerate(targets):
        y0 = gy[gi] + gh * (0.25 + 0.5 * (k + 0.5) / n)
        y1 = ry[ri] + rh / 2 + (gi - 1.5) * (0.12 if ri == 4 else 0.07)
        ax.add_patch(FancyArrowPatch((gx + gw + 0.07, y0), (rx - 0.02, y1),
                                     arrowstyle="-|>,head_length=0.42,head_width=0.22", mutation_scale=10,
                                     lw=1.5, color=c, zorder=1, shrinkA=0, shrinkB=0))

fig.savefig(os.path.join(OUT, "Fig3_gaps_rq.png"), dpi=400, facecolor="white")
print("done")
