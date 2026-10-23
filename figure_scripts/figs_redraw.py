"""Redrawn thesis figures replacing user figures that carried errors.

- Fig2_cnn_lstm.png      (replaces Picture5.png: legend belonged to the FL figure)
- Fig3_review_stats.png  (replaces Picture122.png: first year bar is 2020 and 2025)
- Fig4_engine.png        (replaces Picture 15.PNG: per-window score is q_i)
- Fig4_train_flow.png    (replaces Picture14.PNG: per-window score is q_i)

Drawn at print size (7.5 in wide, 400 dpi) in the thesis figure style: bold
labels, 3D extruded blocks with sharp edges, coloured header bands.
Usage: python figs_redraw.py <output_dir>
"""
import sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch
from matplotlib.colors import to_rgb

OUT = sys.argv[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.weight": "bold",
                     "axes.labelweight": "bold", "mathtext.fontset": "dejavusans",
                     "mathtext.default": "bf"})
INK, SUB = "#16202b", "#37474f"

def shade(c, f):
    r, g, b = to_rgb(c)
    if f < 1:
        return (r * f, g * f, b * f)
    return (r + (1 - r) * (f - 1), g + (1 - g) * (f - 1), b + (1 - b) * (f - 1))

def box3d(ax, x, y, w, h, color, header=None, lines=(), d=0.06, hh=0.26, fs=8.2, lfs=7.0, fill="white", z=3):
    ax.add_patch(Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                         fc=shade(color, 0.55), ec=shade(color, 0.40), lw=0.8, zorder=z - 1))
    ax.add_patch(Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                         fc=shade(color, 1.30), ec=shade(color, 0.50), lw=0.8, zorder=z - 1))
    ax.add_patch(Rectangle((x, y), w, h, fc=fill, ec=color, lw=1.6, zorder=z))
    top = y + h
    if header:
        ax.add_patch(Rectangle((x, y + h - hh), w, hh, fc=color, ec=color, lw=1.6, zorder=z + 1))
        ax.text(x + w / 2, y + h - hh / 2, header, ha="center", va="center", color="white",
                fontsize=fs, fontweight="bold", zorder=z + 2)
        top = y + h - hh
    n = len(lines)
    if n:
        span = top - y
        for k, ln in enumerate(lines):
            yy = top - span * (k + 0.5) / n
            ax.text(x + w / 2, yy, ln, ha="center", va="center", color=INK, fontsize=lfs, fontweight="bold", zorder=z + 2)

def diamond(ax, cx, cy, w, h, color, text, fs=7.2, z=3):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    off = [(px + 0.05, py - 0.05) for px, py in pts]
    ax.add_patch(Polygon(off, closed=True, fc="#9aa3ad", ec="none", zorder=z - 1))
    ax.add_patch(Polygon(pts, closed=True, fc=shade(color, 1.75), ec=color, lw=1.6, zorder=z))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=INK, fontweight="bold", zorder=z + 1)

def arrow(ax, p, q, color="#2b3a4a", lw=1.6, style="-|>", ls="-", rad=0.0, z=2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"{style},head_length=0.45,head_width=0.25", mutation_scale=10,
                                 lw=lw, color=color, linestyle=ls, zorder=z,
                                 connectionstyle=f"arc3,rad={rad}"))

def label(ax, x, y, t, fs=6.8, color=SUB, ha="center", va="center", **kw):
    ax.text(x, y, t, ha=ha, va=va, fontsize=fs, color=color, fontweight="bold", **kw)

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=400, facecolor="white")
    plt.close(fig)

# --------------------------------------------------------------------------
# Fig2_cnn_lstm.png: generic hybrid CNN-LSTM detection engine (Chapter 2)
# --------------------------------------------------------------------------
def fig_cnn_lstm():
    W, H = 7.5, 2.95
    fig = plt.figure(figsize=(W, H), dpi=400)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    stages = [
        ("Input", "#1565c0", ["Flow-feature", "sequence", r"$\mathbf{x}\in\mathbb{R}^{T\times d}$"]),
        ("1D convolution", "#00838f", ["Learnable filters", "slide over time", "Local patterns"]),
        ("Pooling", "#2e7d32", ["Max pooling", "Keeps strongest", "responses"]),
        ("LSTM", "#ef6c00", ["Gated memory", "Long-range", "temporal context"]),
        ("Classification", "#c62828", ["Dense + softmax", "Class probabilities", r"$\hat{\mathbf{y}}$"]),
    ]
    bw, bh, gap, x0, y0 = 1.22, 1.75, 0.27, 0.12, 0.95
    for k, (t, c, ls) in enumerate(stages):
        x = x0 + k * (bw + gap)
        box3d(ax, x, y0, bw, bh, c, t, ls, fs=8.0, lfs=7.0)
        if k:
            arrow(ax, (x - gap + 0.07, y0 + bh / 2 - 0.05), (x - 0.03, y0 + bh / 2 - 0.05), lw=2.0)
    # feature-compression and temporal-modelling braces
    def brace(xa, xb, text, color):
        yb = y0 - 0.12
        ax.plot([xa, xa, xb, xb], [yb + 0.08, yb, yb, yb + 0.08], color=color, lw=1.6)
        label(ax, (xa + xb) / 2, yb - 0.17, text, fs=7.4, color=color)
    brace(x0 + (bw + gap), x0 + 2 * (bw + gap) + bw, "Feature extraction and compression", "#00695c")
    brace(x0 + 3 * (bw + gap), x0 + 3 * (bw + gap) + bw, "Temporal modelling", "#e65100")
    # legend
    lx, ly = 0.55, 0.22
    arrow(ax, (lx, ly), (lx + 0.45, ly), lw=2.0)
    label(ax, lx + 0.55, ly, "Data flow through the engine", fs=7.0, ha="left")
    ax.add_patch(Rectangle((3.95, ly - 0.09), 0.3, 0.18, fc="#00838f", ec=shade("#00838f", 0.6)))
    label(ax, 4.33, ly, "Stage header: function performed", fs=7.0, ha="left")
    save(fig, "Fig2_cnn_lstm.png")

# --------------------------------------------------------------------------
# Fig3_review_stats.png: corpus distribution (Chapter 3)
# --------------------------------------------------------------------------
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

def panel(fig, rect, title, color):
    x, y, w, h = rect
    hb = 0.10
    bg = fig.add_axes([x, y, w, h], zorder=0)
    bg.set_xlim(0, 1); bg.set_ylim(0, 1); bg.axis("off")
    bg.add_patch(Rectangle((0.012, -0.012), 0.988, 0.988, fc="#9aa3ad", ec="none", zorder=0))
    bg.add_patch(Rectangle((0, 0), 0.988, 0.988, fc="white", ec=color, lw=1.6, zorder=1))
    bg.add_patch(Rectangle((0, 0.988 - hb), 0.988, hb, fc=color, ec=color, lw=1.6, zorder=2))
    bg.text(0.494, 0.988 - hb / 2, title, ha="center", va="center", color="white", fontsize=8.8, fontweight="bold", zorder=3)

def style(ax, grid):
    ax.grid(axis=grid, ls="--", lw=0.4, alpha=0.5, zorder=0)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    for s_ in ("left", "bottom"):
        ax.spines[s_].set_linewidth(1.0)
    ax.tick_params(labelsize=7.2, width=0.9, length=3)
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_fontweight("bold")

def fig_review_stats():
    fig = plt.figure(figsize=(7.5, 3.4), dpi=400)
    panel(fig, (0.005, 0.02, 0.42, 0.96), "(a) By publication year (n = 116)", "#1f6fd1")
    ax = fig.add_axes([0.085, 0.16, 0.31, 0.66])
    vals = [("2020 & 2025", 25, "#4a90e2"), ("2021–2022", 29, "#159a9c"), ("2023–2024", 62, "#f07f13")]
    for i, (lab, v, c) in enumerate(vals):
        bar3d(ax, i + 0.2, 0.55, v, c, 0.13, 1.6)
        ax.text(i + 0.475, v + 3.0, str(v), ha="center", fontsize=8.6, fontweight="bold", color=INK)
    ax.set_xlim(0, 3); ax.set_ylim(0, 72)
    ax.set_xticks([i + 0.475 for i in range(3)]); ax.set_xticklabels([v[0] for v in vals])
    ax.set_ylabel("Number of studies", fontsize=7.6)
    style(ax, "y")

    panel(fig, (0.44, 0.02, 0.555, 0.96), "(b) By application domain", "#ef6c00")
    ax = fig.add_axes([0.6, 0.16, 0.36, 0.66])
    doms = [("Multi-domain / general", 68), ("Healthcare / IoMT", 12), ("Industrial / CPS", 10),
            ("Transport / IoV", 8), ("Energy", 8), ("Construction", 5), ("Supply chain", 3), ("Civic / e-voting", 2)]
    cols = ["#f07f13", "#159a9c", "#2e7d32", "#6a1b9a", "#f9a825", "#c62828", "#1f6fd1", "#d81b60"]
    n = len(doms)
    for i, ((lab, v), c) in enumerate(zip(doms, cols)):
        y = (n - 1 - i) + 0.2
        hbar3d(ax, y, 0.55, v, c, 1.6, 0.1)
        ax.text(v + 3.2, y + 0.28, str(v), va="center", fontsize=8.0, fontweight="bold", color=INK)
    ax.set_xlim(0, 80); ax.set_ylim(0, n + 0.05)
    ax.set_yticks([(n - 1 - i) + 0.47 for i in range(n)]); ax.set_yticklabels([d[0] for d in doms])
    ax.set_xlabel("Number of studies", fontsize=7.6)
    style(ax, "x")
    for t in ax.get_yticklabels():
        t.set_fontsize(6.9)
    save(fig, "Fig3_review_stats.png")

# --------------------------------------------------------------------------
# Fig4_engine.png: Stratum 1 trust-scoring engine (Chapter 4)
# --------------------------------------------------------------------------
def fig_engine():
    W, H = 7.5, 3.6
    fig = plt.figure(figsize=(W, H), dpi=400)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    y0, bh, bw = 1.25, 1.65, 1.0
    xs = [0.10, 1.42, 2.74, 4.06]
    box3d(ax, xs[0], y0, bw, bh, "#1565c0", "Device telemetry",
          [r"Flow features $x_t$", "Protocol flags", "Burst rate", "Window $T$"], fs=7.0, lfs=6.7)
    box3d(ax, xs[1], y0, bw, bh, "#00838f", "Trimmed 1D-CNN",
          ["1D conv + pooling", "16 / 32 filters", "kernel 3", "Compression"], fs=7.0, lfs=6.5)
    box3d(ax, xs[2], y0, bw, bh, "#6a1b9a", "LSTM",
          ["32 units", "Temporal", "dependence"], fs=7.6, lfs=6.7)
    box3d(ax, xs[3], y0, bw, bh, "#ef6c00", "Softmax",
          ["Benign", "confidence", r"$q_i \in [0,1]$"], fs=7.6, lfs=6.9)
    for a, b in zip(xs[:-1], xs[1:]):
        arrow(ax, (a + bw + 0.09, y0 + bh / 2 - 0.05), (b - 0.03, y0 + bh / 2 - 0.05), lw=2.0)
    # brace: runs within edge budget
    yb = y0 + bh + 0.22
    ax.plot([xs[0], xs[0], xs[3] + bw, xs[3] + bw], [yb - 0.08, yb, yb, yb - 0.08], color=INK, lw=1.5)
    label(ax, (xs[0] + xs[3] + bw) / 2, yb + 0.17, "Runs within the edge budget (Stratum 1)", fs=8.0, color=INK)
    # decision
    dx, dy = 5.72, y0 + bh / 2
    arrow(ax, (xs[3] + bw + 0.09, dy - 0.05), (dx - 0.47, dy - 0.02), lw=2.0)
    diamond(ax, dx, dy, 0.92, 0.82, "#f9a825", r"$q_i < \delta$ ?", fs=8.0)
    # no branch -> commit
    box3d(ax, 6.36, 2.35, 1.02, 0.78, "#2e7d32", "Commit", [r"$q_i$ to NSL-L2", "fast layer"], fs=7.4, lfs=6.7, hh=0.24)
    arrow(ax, (dx + 0.2, dy + 0.3), (6.34, 2.7), color="#2e7d32", lw=1.8)
    label(ax, 6.0, 2.75, "No", fs=7.4, color="#2e7d32")
    # yes branch -> flag
    box3d(ax, 6.36, 0.62, 1.02, 0.86, "#c62828", "Flag raised", [r"flag$(d_i)=1$", "to Plane A"], fs=7.4, lfs=6.7, hh=0.24)
    arrow(ax, (dx + 0.2, dy - 0.3), (6.34, 1.05), color="#c62828", lw=1.8)
    label(ax, 6.0, 1.0, "Yes", fs=7.4, color="#c62828")
    # legend
    arrow(ax, (0.2, 0.42), (0.62, 0.42), lw=2.0)
    label(ax, 0.7, 0.42, "Data and inference flow", fs=6.9, ha="left")
    diamond(ax, 2.95, 0.42, 0.34, 0.3, "#f9a825", "", fs=6)
    label(ax, 3.2, 0.42, r"Threshold test against $\delta$", fs=6.9, ha="left")
    label(ax, 3.2, 0.14, r"$q_i$ feeds the accumulated trust score $s_i$ of Plane A", fs=6.9, ha="left")
    save(fig, "Fig4_engine.png")

# --------------------------------------------------------------------------
# Fig4_train_flow.png: federated training and behavioural commitment (Chapter 4)
# --------------------------------------------------------------------------
def fig_train_flow():
    W, H = 7.5, 8.6
    fig = plt.figure(figsize=(W, H), dpi=400)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    PH = [("Training rounds", "#4527a0", 5.15, 8.15), ("Validation &\naggregation", "#00838f", 3.35, 5.15),
          ("Trust evaluation", "#ef6c00", 0.55, 3.35)]
    for t, c, ya, yb in PH:
        ax.add_patch(Rectangle((0.08, ya + 0.03), 0.42, yb - ya - 0.06, fc=c, ec=c, zorder=2))
        ax.text(0.29, (ya + yb) / 2, t, rotation=90, ha="center", va="center", color="white",
                fontsize=8.4, fontweight="bold", zorder=3, linespacing=1.1)
        ax.add_patch(Rectangle((0.58, ya + 0.03), 6.8, yb - ya - 0.06, fc=shade(c, 1.88), ec=shade(c, 1.4), lw=0.8, zorder=0))
    cx, bw, bh = 3.0, 3.0, 0.42
    C1, C2, C3 = "#4527a0", "#00838f", "#ef6c00"

    def step(y, text, color, w=bw, x=None):
        x = cx - w / 2 if x is None else x
        box3d(ax, x, y, w, bh, color, None, [text], d=0.04, lfs=7.2)
        return x, y

    # start
    ax.add_patch(Rectangle((cx - 0.55, 8.22), 1.1, 0.3, fc=C1, ec=C1, zorder=3))
    label(ax, cx, 8.37, "START", fs=8.0, color="white")
    step(7.55, r"Initialise $w^{(0)}$; register clients on the fast layer", C1, w=3.9)
    arrow(ax, (cx, 8.2), (cx, 8.01))
    diamond(ax, cx, 6.95, 2.1, 0.62, "#f9a825", r"Rounds remaining ($t<R$)?", fs=7.0)
    arrow(ax, (cx, 7.53), (cx, 7.28))
    step(6.05, r"Each client $i$: LocalTrain$(w^{(t)}, E)$ on private telemetry", C1, w=3.9)
    arrow(ax, (cx, 6.63), (cx, 6.5)); label(ax, cx + 0.2, 6.57, "Yes", fs=6.8, color="#2e7d32", ha="left")
    step(5.45, "Send update with round ID and timestamp", C1, w=3.9)
    arrow(ax, (cx, 6.03), (cx, 5.9))
    diamond(ax, cx, 4.72, 2.6, 0.66, "#f9a825", "Registered client and\nvalid metadata?", fs=6.6)
    arrow(ax, (cx, 5.43), (cx, 5.05))
    # reject
    box3d(ax, 5.2, 4.5, 1.8, 0.46, "#c62828", None, ["Reject update"], d=0.04, lfs=7.2)
    arrow(ax, (cx + 1.31, 4.72), (5.18, 4.72), color="#c62828"); label(ax, 4.6, 4.85, "No", fs=6.8, color="#c62828")
    step(3.62, r"Federated averaging: $w^{(t+1)}$ = weighted mean of admitted $w_i^{(t)}$", C2, w=3.9)
    arrow(ax, (cx, 4.4), (cx, 4.06)); label(ax, cx + 0.12, 4.22, "Yes", fs=6.8, color="#2e7d32", ha="left")
    # loop back to round decision
    ax.plot([cx - 1.95, 0.75, 0.75], [3.83, 3.83, 6.95], color=C1, lw=1.5, zorder=1)
    arrow(ax, (0.75, 6.95), (cx - 1.07, 6.95), color=C1)
    label(ax, 0.82, 5.55, r"$t \leftarrow t+1$", fs=7.0, color=C1, ha="left")
    # exit of loop
    box3d(ax, 5.2, 6.73, 1.95, 0.46, C2, None, [r"$w^{\star} \leftarrow w^{(R)}$; commit"], d=0.04, lfs=7.0)
    arrow(ax, (cx + 1.06, 6.95), (5.18, 6.95), color=C2); label(ax, 4.6, 7.08, "No", fs=6.8, color=SUB)
    ax.plot([7.27, 7.27], [6.95, 3.2], color=C2, lw=1.5, zorder=1)
    ax.plot([7.22, 7.27], [6.95, 6.95], color=C2, lw=1.5, zorder=1)
    arrow(ax, (7.27, 3.2), (cx + 1.97, 3.2), color=C2)
    # trust evaluation
    step(2.98, r"For each device $d_i$: $\hat{y}_i = F(x_i;\, w^{\star})$", C3, w=3.9)
    step(2.38, r"Compute benign confidence $q_i$", C3, w=3.9)
    arrow(ax, (cx, 2.96), (cx, 2.83))
    diamond(ax, cx, 1.7, 1.5, 0.62, "#f9a825", r"$q_i < \delta$ ?", fs=8.0)
    arrow(ax, (cx, 2.36), (cx, 2.03))
    box3d(ax, 0.78, 0.82, 1.75, 0.55, "#c62828", None, [r"flag$(d_i)=1$;", "raise event to Plane A"], d=0.04, lfs=6.8)
    arrow(ax, (cx - 0.76, 1.7), (1.66, 1.4), color="#c62828"); label(ax, 2.0, 1.78, "Yes", fs=6.8, color="#c62828")
    box3d(ax, 4.45, 0.82, 1.95, 0.55, "#2e7d32", None, [r"Commit $q_i$ as validated", "behavioural trust score"], d=0.04, lfs=6.8)
    arrow(ax, (cx + 0.76, 1.7), (5.4, 1.4), color="#2e7d32"); label(ax, 4.05, 1.78, "No", fs=6.8, color="#2e7d32")
    # end
    ax.add_patch(Rectangle((cx - 1.25, 0.12), 2.5, 0.34, fc=C1, ec=C1, zorder=3))
    label(ax, cx, 0.29, r"END: return $w^{\star}$ and per-device flags", fs=7.4, color="white")
    arrow(ax, (1.66, 0.8), (cx - 0.9, 0.48), color=SUB)
    arrow(ax, (5.4, 0.8), (cx + 0.9, 0.48), color=SUB)
    save(fig, "Fig4_train_flow.png")

fig_cnn_lstm()
fig_review_stats()
fig_engine()
fig_train_flow()
print("done")
