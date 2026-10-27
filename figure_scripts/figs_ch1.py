"""Chapter 1 figures for the STRATA thesis: landscape indicators and thesis roadmap.

Drawn at print size (7.5 in wide = full text width) so font sizes are the
printed sizes. Style matches the author's figures: bold sans labels, 3D
extruded bars and blocks with sharp edges, coloured header panels.
Usage: python figs_ch1.py <output_dir>
"""
import sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch
from matplotlib.colors import to_rgb

OUT = sys.argv[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.weight": "bold",
                     "axes.labelweight": "bold", "axes.titleweight": "bold"})

def shade(c, f):
    r, g, b = to_rgb(c)
    if f < 1:
        return (r * f, g * f, b * f)
    return (r + (1 - r) * (f - 1), g + (1 - g) * (f - 1), b + (1 - b) * (f - 1))

def bar3d(ax, x, w, h, color, dx, dy):
    ax.add_patch(Rectangle((x, 0), w, h, fc=color, ec=shade(color, 0.55), lw=0.8, zorder=3))
    ax.add_patch(Polygon([(x + w, 0), (x + w + dx, dy), (x + w + dx, h + dy), (x + w, h)], closed=True,
                         fc=shade(color, 0.62), ec=shade(color, 0.45), lw=0.7, zorder=3))
    ax.add_patch(Polygon([(x, h), (x + dx, h + dy), (x + w + dx, h + dy), (x + w, h)], closed=True,
                         fc=shade(color, 1.35), ec=shade(color, 0.55), lw=0.7, zorder=3))

def hbar3d(ax, y, hgt, length, color, dx, dy):
    ax.add_patch(Rectangle((0, y), length, hgt, fc=color, ec=shade(color, 0.55), lw=0.8, zorder=3))
    ax.add_patch(Polygon([(0, y + hgt), (dx, y + hgt + dy), (length + dx, y + hgt + dy), (length, y + hgt)], closed=True,
                         fc=shade(color, 1.35), ec=shade(color, 0.55), lw=0.7, zorder=3))
    ax.add_patch(Polygon([(length, y), (length + dx, y + dy), (length + dx, y + hgt + dy), (length, y + hgt)], closed=True,
                         fc=shade(color, 0.62), ec=shade(color, 0.45), lw=0.7, zorder=3))

def panel(fig, rect, title, color, fs=8.6):
    x, y, w, h = rect
    hb = 0.11
    bg = fig.add_axes([x, y, w, h], zorder=0)
    bg.set_xlim(0, 1); bg.set_ylim(0, 1); bg.axis("off")
    bg.add_patch(Rectangle((0.014, -0.014), 0.986, 0.986, fc="#9aa3ad", ec="none", zorder=0))
    bg.add_patch(Rectangle((0, 0), 0.986, 0.986, fc="white", ec=color, lw=1.6, zorder=1))
    bg.add_patch(Rectangle((0, 0.986 - hb), 0.986, hb, fc=color, ec=color, lw=1.6, zorder=2))
    bg.text(0.493, 0.986 - hb / 2, title, ha="center", va="center", color="white", fontsize=fs, fontweight="bold", zorder=3)

def style_axes(ax, grid_axis):
    ax.grid(axis=grid_axis, ls="--", lw=0.4, alpha=0.5, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(1.0)
    ax.tick_params(labelsize=7.4, width=0.9, length=3)
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_fontweight("bold")

# ------------------------------------------------------------- landscape figure
def fig_landscape():
    fig = plt.figure(figsize=(7.5, 3.3), dpi=400)
    BLUE, TEAL, ORANGE = "#1f6fd1", "#159a9c", "#f07f13"

    panel(fig, (0.005, 0.02, 0.305, 0.96), "(a) Connected IoT devices", BLUE)
    ax = fig.add_axes([0.075, 0.15, 0.215, 0.66])
    vals = [("2024", 18.5, "#4a90e2"), ("2025", 21.1, "#1f6fd1"), ("2030\n(proj.)", 39.0, "#0d47a1")]
    for i, (lab, v, c) in enumerate(vals):
        bar3d(ax, i + 0.2, 0.55, v, c, 0.13, 1.5)
        ax.text(i + 0.475, v + 2.6, f"{v:.1f}", ha="center", fontsize=8.4, fontweight="bold", color="#10243e")
    ax.set_xlim(0, 3.0); ax.set_ylim(0, 48)
    ax.set_xticks([i + 0.475 for i in range(3)]); ax.set_xticklabels([v[0] for v in vals])
    ax.set_ylabel("Devices (billions)", fontsize=7.6)
    ax.text(0.12, 43, "CAGR ≈ 13.2%", fontsize=7.8, fontweight="bold", color=BLUE,
            bbox=dict(boxstyle="square,pad=0.3", fc="white", ec=BLUE, lw=1.1))
    style_axes(ax, "y")

    panel(fig, (0.325, 0.02, 0.37, 0.96), "(b) Ransomware against industrial sites", TEAL)
    ax = fig.add_axes([0.505, 0.15, 0.165, 0.66])
    rows = [("Rise in attacks on\nindustrial organisations", 87, "#0b7a7c"),
            ("Rise in ransomware\ngroups (now 80)", 60, "#159a9c"),
            ("Incidents forcing a\nfull OT shutdown", 25, "#4cc3c4")]
    for i, (lab, v, c) in enumerate(rows):
        y = (len(rows) - 1 - i) + 0.22
        hbar3d(ax, y, 0.52, v, c, 2.6, 0.1)
        ax.text(v + 5, y + 0.26, (f"≈{v}%" if v == 25 else f"{v}%"), va="center", fontsize=8.4, fontweight="bold", color="#0b3b3c")
    ax.set_xlim(0, 112); ax.set_ylim(0, 3.05)
    ax.set_yticks([(len(rows) - 1 - i) + 0.48 for i in range(len(rows))])
    ax.set_yticklabels([r_[0] for r_ in rows])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Percent (%)", fontsize=7.6)
    style_axes(ax, "x")
    for t in ax.get_yticklabels():
        t.set_fontsize(6.4)

    panel(fig, (0.71, 0.02, 0.285, 0.96), "(c) Average data-breach cost", ORANGE)
    ax = fig.add_axes([0.79, 0.15, 0.19, 0.66])
    vals = [("Global", 4.44, "#f6a04d"), ("United\nStates", 10.22, "#e0620d")]
    for i, (lab, v, c) in enumerate(vals):
        bar3d(ax, i + 0.22, 0.52, v, c, 0.12, 0.4)
        ax.text(i + 0.48, v + 0.8, f"USD {v:.2f} M", ha="center", fontsize=8.0, fontweight="bold", color="#5a2a05")
    ax.set_xlim(-0.25, 2.05); ax.set_ylim(0, 12.8)
    ax.set_xticks([i + 0.48 for i in range(2)]); ax.set_xticklabels([v[0] for v in vals])
    ax.set_ylabel("USD (millions)", fontsize=7.6)
    style_axes(ax, "y")

    fig.savefig(os.path.join(OUT, "Fig1_2_landscape.png"), dpi=400, facecolor="white")
    plt.close(fig)

# --------------------------------------------------------------- roadmap figure
# Drawn at the 5.9 in text width in Arial Black, compact, no caption in the image.
def fit_text(ax, fig, x, y, s, maxw, fs, minfs=6.0, **kw):
    t = ax.text(x, y, s, fontsize=fs, **kw)
    r = fig.canvas.get_renderer()
    while fs > minfs and t.get_window_extent(r).width / fig.dpi > maxw:
        fs -= 0.1
        t.set_fontsize(fs)
    return t

def _block(ax, fig, x, y, w, h, color, header, lines, tags, d=0.05):
    hh = 0.32
    ax.add_patch(Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                         fc=shade(color, 0.55), ec=shade(color, 0.40), lw=0.7, zorder=2))
    ax.add_patch(Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                         fc=shade(color, 1.30), ec=shade(color, 0.50), lw=0.7, zorder=2))
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.6, zorder=3))
    ax.add_patch(Rectangle((x, y + h - hh), w, hh, fc=color, ec=color, lw=1.6, zorder=4))
    fit_text(ax, fig, x + w / 2, y + h - hh / 2, header, w - 0.12, 8.8, ha="center", va="center", color="white", zorder=5)
    ty = y + h - hh - 0.2
    for ln in lines:
        ax.add_patch(Rectangle((x + 0.09, ty - 0.035), 0.07, 0.07, fc=color, ec=color, zorder=5))
        fit_text(ax, fig, x + 0.22, ty, ln, w - 0.3, 7.6, ha="left", va="center", color="#151515", zorder=5)
        ty -= 0.235
    tx = x + 0.09
    for t in tags:
        tw = 0.68
        ax.add_patch(Rectangle((tx, y + 0.07), tw, 0.21, fc="#151515", ec="#151515", lw=0.8, zorder=5))
        ax.text(tx + tw / 2, y + 0.175, t, ha="center", va="center", color="white", fontsize=7.0, zorder=6)
        tx += tw + 0.06

def arrow(ax, p, q):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=0.55,head_width=0.32", mutation_scale=13,
                                 lw=2.8, color="#262626", zorder=1, shrinkA=0, shrinkB=0))

def fig_roadmap():
    from matplotlib import font_manager as fm
    fm.fontManager.addfont("C:/Windows/Fonts/ariblk.ttf")
    with plt.rc_context({"font.family": ["Arial", "DejaVu Sans"], "font.weight": 900}):
        _roadmap()

def _roadmap():
    W, H = 5.9, 4.98
    fig = plt.figure(figsize=(W, H), dpi=400)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    w, h = 2.72, 1.43
    xl, xr = 0.05, 3.08
    y1, y2, y3 = 3.47, 1.76, 0.05
    C = ["#2c3e50", "#1b7f79", "#5d7f2f", "#b5651d", "#9e2a2b", "#3c3c6e"]

    def block(ax_, x, y, w_, h_, color, header, lines, tags):
        _block(ax_, fig, x, y, w_, h_, color, header, lines, [t for t, _ in tags])

    RQ = None
    block(ax, xl, y1, w, h, C[0], "Chapter 1: Introduction",
          ["Constrained IIoT and the trilemma", "Quantum threat to device identity", "Research questions, contributions"],
          [("RQ1–RQ5", RQ)])
    block(ax, xr, y1, w, h, C[1], "Chapter 2: Background",
          ["IIoT security landscape", "Federated CNN–LSTM learning", "Ledgers, PoA², hybrid pattern"],
          [])
    block(ax, xr, y2, w, h, C[2], "Chapter 3: Related Works",
          ["PRISMA review of 116 studies", "Defence-gap analysis", "Gaps motivating RQ1–RQ5"],
          [("RQ1–RQ5", RQ)])
    block(ax, xl, y2, w, h, C[3], "Chapter 4: STRATA Architecture",
          ["Behavioural trust stratum", "Consensus and public anchoring", "Identity and post-quantum planes"],
          [("RQ1–RQ5", RQ)])
    block(ax, xl, y3, w, h, C[4], "Chapter 5: Evaluation",
          ["Accuracy 96.84–97.70%", "Finality 0.11 s and ledger cost", "PQC delivery, revocation 1.8 s"],
          [("RQ1–RQ5", RQ)])
    block(ax, xr, y3, w, h, C[5], "Chapter 6: Conclusion",
          ["Answers to RQ1–RQ5", "Practical concerns", "Future research directions"],
          [("RQ1–RQ5", RQ)])

    arrow(ax, (xl + w + 0.07, y1 + h / 2), (xr - 0.02, y1 + h / 2))
    arrow(ax, (xr + w / 2, y1 - 0.01), (xr + w / 2, y2 + h + 0.07))
    arrow(ax, (xr - 0.02, y2 + h / 2), (xl + w + 0.07, y2 + h / 2))
    arrow(ax, (xl + w / 2, y2 - 0.01), (xl + w / 2, y3 + h + 0.07))
    arrow(ax, (xl + w + 0.07, y3 + h / 2), (xr - 0.02, y3 + h / 2))

    fig.savefig(os.path.join(OUT, "Fig1_3_roadmap.png"), dpi=400, facecolor="white")
    plt.close(fig)

fig_landscape()
fig_roadmap()
print("done")
