"""Redrawn thesis figures replacing user figures that carried errors.

- Fig2_cnn_lstm.png      (replaces Picture5.png: legend belonged to the FL figure)
- Fig2_trust_flow.png    (replaces Picture62.PNG: flag threshold is delta)
- Fig3_review_stats.png  (replaces Picture122.png: first year bar is 2020 and 2025)
- Fig4_engine.png        (replaces Picture 15.PNG: per-window score is q_i)
- Fig4_train_flow.png    (replaces Picture14.PNG: per-window score is q_i)

Drawn at the printed text width (5.9 in, 400 dpi) so labels print at their
true size, in Arial Black on a white background. Each figure has its own
palette and block style so the set does not read as one template.
Usage: python figs_redraw.py <output_dir>
"""
import sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch
from matplotlib.colors import to_rgb

OUT = sys.argv[1]
fm.fontManager.addfont("C:/Windows/Fonts/ariblk.ttf")
plt.rcParams.update({
    "font.family": ["Arial", "DejaVu Sans"], "font.weight": 900, "axes.labelweight": 900,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial:weight=900", "mathtext.it": "Arial:weight=900",
    "mathtext.bf": "Arial:weight=900", "mathtext.default": "regular", "mathtext.fallback": "stixsans",
})
W = 5.9
INK, SUB = "#1a1a1a", "#3d3d3d"


def shade(c, f):
    r, g, b = to_rgb(c)
    if f < 1:
        return (r * f, g * f, b * f)
    return (r + (1 - r) * (f - 1), g + (1 - g) * (f - 1), b + (1 - b) * (f - 1))


def canvas(h):
    fig = plt.figure(figsize=(W, h), dpi=400)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, h); ax.axis("off")
    return fig, ax


def block(ax, x, y, w, h, color, header=None, lines=(), style="3d", d=0.05, hh=0.27, fs=8.3, lfs=7.6,
          fill="white", z=3, lcolor=INK):
    """style: '3d' extruded edges, 'shadow' flat with offset grey shadow, 'flat' plain outline."""
    if style == "3d":
        ax.add_patch(Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                             fc=shade(color, 0.55), ec=shade(color, 0.40), lw=0.7, zorder=z - 1))
        ax.add_patch(Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                             fc=shade(color, 1.30), ec=shade(color, 0.50), lw=0.7, zorder=z - 1))
    elif style == "shadow":
        ax.add_patch(Rectangle((x + 0.04, y - 0.04), w, h, fc="#b5b5b5", ec="none", zorder=z - 1))
    ax.add_patch(Rectangle((x, y), w, h, fc=fill, ec=color, lw=1.5, zorder=z))
    top = y + h
    if header:
        ax.add_patch(Rectangle((x, y + h - hh), w, hh, fc=color, ec=color, lw=1.5, zorder=z + 1))
        ax.text(x + w / 2, y + h - hh / 2, header, ha="center", va="center", color="white",
                fontsize=fs, zorder=z + 2)
        top = y + h - hh
    n = len(lines)
    for k, ln in enumerate(lines):
        yy = top - (top - y) * (k + 0.5) / n
        ax.text(x + w / 2, yy, ln, ha="center", va="center", color=lcolor, fontsize=lfs, zorder=z + 2)


def diamond(ax, cx, cy, w, h, color, text, fs=7.6, fill="white", shadow=True, z=3):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    if shadow:
        ax.add_patch(Polygon([(px + 0.04, py - 0.04) for px, py in pts], closed=True, fc="#b5b5b5", ec="none", zorder=z - 1))
    ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=color, lw=1.6, zorder=z))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=INK, zorder=z + 1, linespacing=1.15)


def arrow(ax, p, q, color="#2b2b2b", lw=1.5, ls="-", z=2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=0.42,head_width=0.22", mutation_scale=10,
                                 lw=lw, color=color, linestyle=ls, zorder=z, shrinkA=0, shrinkB=0))


def path(ax, pts, color="#2b2b2b", lw=1.5, ls="-", z=2):
    xs, ys = zip(*pts[:-1])
    ax.plot(list(xs) + [pts[-2][0]], list(ys) + [pts[-2][1]], color=color, lw=lw, ls=ls, zorder=z)
    arrow(ax, pts[-2], pts[-1], color=color, lw=lw, ls=ls, z=z)


def label(ax, x, y, t, fs=7.6, color=SUB, ha="center", va="center", **kw):
    ax.text(x, y, t, ha=ha, va=va, fontsize=fs, color=color, **kw)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=400, facecolor="white")
    plt.close(fig)


# --------------------------------------------------------------------------
# Fig2_cnn_lstm.png: generic hybrid CNN-LSTM detection engine (Chapter 2)
# palette: slate, teal, ochre, brick, charcoal; 3D blocks
# --------------------------------------------------------------------------
def fig_cnn_lstm():
    H = 2.45
    fig, ax = canvas(H)
    stages = [
        ("Input", "#3b5b7a", ["Flow", "features", r"$x \in R^{T\times d}$"]),
        ("1D Conv", "#2a7f7a", ["Learnable", "filters", "Local motifs"]),
        ("Pooling", "#a87a1c", ["Max pooling", "Keeps peak", "responses"]),
        ("LSTM", "#9c3f2c", ["Gated", "memory", "Long-range"]),
        ("Classifier", "#454545", ["Dense +", "softmax", r"$\hat{y}$"]),
    ]
    bw, bh, gap, x0, y0 = 0.98, 1.3, 0.2, 0.1, 0.9
    for k, (t, c, ls) in enumerate(stages):
        x = x0 + k * (bw + gap)
        block(ax, x, y0, bw, bh, c, t, ls, style="3d", hh=0.32)
        if k:
            arrow(ax, (x - gap + 0.06, y0 + bh / 2), (x - 0.02, y0 + bh / 2), lw=1.8)

    def brace(xa, xb, text, color):
        yb = y0 - 0.12
        ax.plot([xa, xa, xb, xb], [yb + 0.07, yb, yb, yb + 0.07], color=color, lw=1.5)
        label(ax, (xa + xb) / 2, yb - 0.18, text, fs=7.6, color=color)
    brace(x0 + (bw + gap), x0 + 2 * (bw + gap) + bw, "Feature compression", "#2a7f7a")
    brace(x0 + 3 * (bw + gap), x0 + 3 * (bw + gap) + bw, "Temporal modelling", "#9c3f2c")
    arrow(ax, (0.15, 0.17), (0.55, 0.17), lw=1.8)
    label(ax, 0.62, 0.17, "Data flow", fs=7.2, ha="left")
    ax.add_patch(Rectangle((2.55, 0.09), 0.26, 0.16, fc="#454545", ec="#454545"))
    label(ax, 2.88, 0.17, "Header: stage function", fs=7.2, ha="left")
    save(fig, "Fig2_cnn_lstm.png")


# --------------------------------------------------------------------------
# Fig2_trust_flow.png: detection to enforcement (Chapter 2)
# palette: navy, steel, gold, moss, crimson, violet, copper, pine; flat with shadow, grey bodies
# --------------------------------------------------------------------------
def fig_trust_flow():
    H = 3.5
    fig, ax = canvas(H)
    G = "#efefef"
    OK, BAD = "#4f7f3a", "#b03a2e"
    y0, bh = 2.05, 0.98
    block(ax, 0.08, y0, 1.2, bh, "#22356f", "1. Engine", ["Class", "probabilities"], style="shadow", fill=G, hh=0.3)
    block(ax, 1.52, y0, 1.15, bh, "#3e6f8e", "2. Score", ["Trust score", r"in [0, 1]"], style="shadow", fill=G, hh=0.3)
    arrow(ax, (1.3, y0 + bh / 2), (1.5, y0 + bh / 2), lw=1.8)
    cx, cy = 3.48, y0 + bh / 2
    arrow(ax, (2.69, cy), (2.8, cy), lw=1.8)
    diamond(ax, cx, cy, 1.32, 1.0, "#b8901c", "3. Is score\n" + r"$\geq \delta$ ?", fs=7.6, fill=G)
    block(ax, 4.45, 2.15, 1.38, 0.86, OK, "4A. Trusted", ["Interactions", "proceed"], style="shadow", fill=G, hh=0.3)
    arrow(ax, (cx + 0.66, cy), (4.43, cy), color=OK, lw=1.7)
    label(ax, 4.27, cy + 0.15, "Yes", fs=7.6, color=OK)
    bw, by, bhh, gap = 1.31, 0.6, 0.86, 0.16
    stages = [("4B. Flagged", BAD, [r"Score $< \delta$", "flag device"]),
              ("5. Isolate", "#5e4a8c", ["Restrict or", "quarantine"]),
              ("6. Ledger", "#a8611d", ["Revocation", "recorded"]),
              ("7. Propagate", "#2e6b66", ["Broadcast;", "nodes update"])]
    for k, (h_, c, ln) in enumerate(stages):
        x = 0.1 + k * (bw + gap)
        block(ax, x, by, bw, bhh, c, h_, ln, style="shadow", fill=G, hh=0.3)
        if k:
            arrow(ax, (x - gap + 0.03, by + 0.3), (x - 0.01, by + 0.3), color=BAD, lw=1.6, ls="--")
    path(ax, [(cx, cy - 0.5), (cx, 1.72), (0.1 + bw / 2, 1.72), (0.1 + bw / 2, by + bhh + 0.01)], color=BAD, lw=1.6, ls="--")
    label(ax, cx + 0.1, 1.84, "No", fs=7.6, color=BAD, ha="left")
    arrow(ax, (0.12, 0.2), (0.52, 0.2), color=OK, lw=1.7)
    label(ax, 0.58, 0.2, r"Trusted path (score $\geq \delta$)", fs=7.0, ha="left")
    arrow(ax, (3.1, 0.2), (3.5, 0.2), color=BAD, lw=1.7, ls="--")
    label(ax, 3.56, 0.2, r"Anomalous path (score $< \delta$)", fs=7.0, ha="left")
    save(fig, "Fig2_trust_flow.png")


# --------------------------------------------------------------------------
# Fig3_review_stats.png: corpus distribution (Chapter 3)
# palette: teal shades (a), earthy mix (b); charcoal header bands
# --------------------------------------------------------------------------
def bar3d(ax, x, w, h, color, dx, dy):
    ax.add_patch(Rectangle((x, 0), w, h, fc=color, ec=shade(color, 0.55), lw=0.8, zorder=3))
    ax.add_patch(Polygon([(x + w, 0), (x + w + dx, dy), (x + w + dx, h + dy), (x + w, h)], closed=True,
                         fc=shade(color, 0.62), ec=shade(color, 0.45), lw=0.7, zorder=3))
    ax.add_patch(Polygon([(x, h), (x + dx, h + dy), (x + w + dx, h + dy), (x + w, h)], closed=True,
                         fc=shade(color, 1.35), ec=shade(color, 0.55), lw=0.7, zorder=3))


def hbar(ax, y, hgt, length, color):
    ax.add_patch(Rectangle((0, y), length, hgt, fc=color, ec=shade(color, 0.6), lw=0.8, zorder=3))


def panel(fig, rect, title):
    x, y, w, h = rect
    hb = 0.11
    bg = fig.add_axes([x, y, w, h], zorder=0)
    bg.set_xlim(0, 1); bg.set_ylim(0, 1); bg.axis("off")
    bg.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec="#555555", lw=1.2, zorder=1))
    bg.add_patch(Rectangle((0, 1 - hb), 1, hb, fc="#2f2f2f", ec="#2f2f2f", lw=1.2, zorder=2))
    bg.text(0.5, 1 - hb / 2, title, ha="center", va="center", color="white", fontsize=8.0, zorder=3)


def style(ax, grid):
    ax.grid(axis=grid, ls=":", lw=0.5, color="#999999", zorder=0)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    ax.tick_params(labelsize=7.2, width=0.9, length=3)


def fig_review_stats():
    fig = plt.figure(figsize=(W, 3.2), dpi=400)
    panel(fig, (0.004, 0.01, 0.405, 0.98), "(a) Publication year (n = 116)")
    ax = fig.add_axes([0.105, 0.2, 0.28, 0.6])
    vals = [("2020 &\n2025", 25, "#8fbcb9"), ("2021\u2013\n2022", 29, "#4a9590"), ("2023\u2013\n2024", 62, "#1d5e5a")]
    for i, (lab, v, c) in enumerate(vals):
        bar3d(ax, i + 0.2, 0.58, v, c, 0.12, 1.6)
        ax.text(i + 0.49, v + 3.2, str(v), ha="center", fontsize=8.2, color=INK)
    ax.set_xlim(0, 3); ax.set_ylim(0, 72)
    ax.set_xticks([i + 0.49 for i in range(3)]); ax.set_xticklabels([v[0] for v in vals])
    ax.set_ylabel("Number of studies", fontsize=7.4)
    style(ax, "y")

    panel(fig, (0.418, 0.01, 0.578, 0.98), "(b) Application domain")
    ax = fig.add_axes([0.62, 0.17, 0.34, 0.65])
    doms = [("Multi-domain", 68), ("Healthcare/IoMT", 12), ("Industrial/CPS", 10), ("Transport/IoV", 8),
            ("Energy", 8), ("Construction", 5), ("Supply chain", 3), ("Civic/e-voting", 2)]
    cols = ["#7a2e1d", "#c1666b", "#6b705c", "#d4a373", "#457b9d", "#a5a58d", "#1d3557", "#e07a5f"]
    n = len(doms)
    for i, ((lab, v), c) in enumerate(zip(doms, cols)):
        y = (n - 1 - i) + 0.18
        hbar(ax, y, 0.64, v, c)
        ax.text(v + 2.0, y + 0.32, str(v), va="center", fontsize=7.6, color=INK)
    ax.set_xlim(0, 80); ax.set_ylim(0, n)
    ax.set_yticks([(n - 1 - i) + 0.5 for i in range(n)]); ax.set_yticklabels([d[0] for d in doms])
    ax.set_xlabel("Number of studies", fontsize=7.4)
    style(ax, "x")
    for t in ax.get_yticklabels():
        t.set_fontsize(6.9)
    save(fig, "Fig3_review_stats.png")


# --------------------------------------------------------------------------
# Fig4_engine.png: Stratum 1 trust-scoring engine (Chapter 4)
# palette: slate, jade, plum, amber, olive, wine; deeper 3D blocks
# --------------------------------------------------------------------------
def fig_engine():
    H = 3.85
    fig, ax = canvas(H)
    y1, bh, bw, gap = 1.95, 1.35, 1.22, 0.27
    xs = [0.1 + k * (bw + gap) for k in range(4)]
    spec = [("Telemetry", "#2e4057", [r"Flow features $x_t$", "Protocol flags", r"Window $T$"]),
            ("Trimmed 1D-CNN", "#04776f", ["Conv + pooling", "16 / 32 filters", "kernel 3"]),
            ("LSTM", "#54428e", ["32 units", "Temporal", "dependence"]),
            ("Softmax", "#c27c2c", ["Benign", "confidence", r"$q_i$ in [0, 1]"])]
    for x, (t, c, ls) in zip(xs, spec):
        block(ax, x, y1, bw, bh, c, t, ls, style="3d", d=0.07, hh=0.32, fs=7.9, lfs=7.4)
    for a, b in zip(xs[:-1], xs[1:]):
        arrow(ax, (a + bw + 0.09, y1 + bh / 2), (b - 0.02, y1 + bh / 2), lw=1.8)
    yb = y1 + bh + 0.2
    ax.plot([xs[0], xs[0], xs[3] + bw, xs[3] + bw], [yb - 0.07, yb, yb, yb - 0.07], color=INK, lw=1.4)
    label(ax, (xs[0] + xs[3] + bw) / 2, yb + 0.17, "Runs within the edge budget (Stratum 1)", fs=7.8, color=INK)
    cx, cy = 2.95, 0.98
    sx = xs[3] + bw / 2
    path(ax, [(sx, y1), (sx, 1.7), (cx, 1.7), (cx, cy + 0.43)], lw=1.7)
    diamond(ax, cx, cy, 1.25, 0.86, "#c27c2c", r"$q_i < \delta$ ?", fs=8.0)
    block(ax, 0.3, 0.55, 1.55, 0.86, "#7a1f35", "Flag raised", [r"flag$(d_i) = 1$", "to Plane A"],
          style="3d", d=0.07, hh=0.3, fs=7.8, lfs=7.4)
    arrow(ax, (cx - 0.63, cy), (1.87, cy), color="#7a1f35", lw=1.7)
    label(ax, 2.1, cy + 0.14, "Yes", fs=7.6, color="#7a1f35")
    block(ax, 4.05, 0.55, 1.55, 0.86, "#4d6b1f", "Commit", [r"$q_i$ to NSL-L2", "fast layer"],
          style="3d", d=0.07, hh=0.3, fs=7.8, lfs=7.4)
    arrow(ax, (cx + 0.63, cy), (4.03, cy), color="#4d6b1f", lw=1.7)
    label(ax, 3.8, cy + 0.14, "No", fs=7.6, color="#4d6b1f")
    label(ax, W / 2, 0.2, r"$q_i$ feeds the accumulated trust score $s_i$ of Plane A", fs=7.2)
    save(fig, "Fig4_engine.png")


# --------------------------------------------------------------------------
# Fig4_train_flow.png: federated training and behavioural commitment (Chapter 4)
# palette: deep blue, forest, brick, dark gold; flat flowchart, black phase bars
# --------------------------------------------------------------------------
def fig_train_flow():
    H = 8.1
    fig, ax = canvas(H)
    C1, C2, C3, DG = "#1f4e79", "#2f6b3b", "#9c3d2e", "#8a6d1d"
    phases = [("Training rounds", 4.85, 7.98), ("Validation &\naggregation", 3.08, 4.85), ("Trust evaluation", 0.12, 3.08)]
    for t, ya, yb in phases:
        ax.add_patch(Rectangle((0.05, ya + 0.03), 0.34, yb - ya - 0.06, fc="#262626", ec="#262626", zorder=2))
        ax.text(0.22, (ya + yb) / 2, t, rotation=90, ha="center", va="center", color="white",
                fontsize=8.2, zorder=3, linespacing=1.1)
    for yline in (4.85, 3.08):
        ax.plot([0.48, W - 0.05], [yline, yline], color="#9a9a9a", lw=0.9, ls="--", zorder=1)
    cx, bw, bh = 2.6, 3.4, 0.42

    def step(y, text, color, w=bw):
        block(ax, cx - w / 2, y, w, bh, color, None, [text], style="flat", lfs=7.6)

    def term(y, text, w):
        ax.add_patch(Rectangle((cx - w / 2, y), w, 0.3, fc="#262626", ec="#262626", zorder=3))
        label(ax, cx, y + 0.15, text, fs=7.6, color="white")

    term(7.6, "START", 1.0)
    step(7.0, r"Initialise $w^{(0)}$; register clients", C1)
    arrow(ax, (cx, 7.6), (cx, 7.43))
    diamond(ax, cx, 6.42, 2.3, 0.64, DG, "Rounds left?\n(t < R)", fs=7.2, shadow=False)
    arrow(ax, (cx, 7.0), (cx, 6.75))
    step(5.5, r"Client $i$: LocalTrain($w^{(t)}$, $E_{loc}$)", C1)
    arrow(ax, (cx, 6.1), (cx, 5.93)); label(ax, cx + 0.12, 6.02, "Yes", fs=7.0, color=C2, ha="left")
    step(4.95, "Send update, round ID, timestamp", C1)
    arrow(ax, (cx, 5.5), (cx, 5.38))
    diamond(ax, cx, 4.22, 2.5, 0.7, DG, "Registered client and\nvalid metadata?", fs=7.0, shadow=False)
    arrow(ax, (cx, 4.95), (cx, 4.58))
    block(ax, 4.5, 4.01, 1.3, 0.42, C3, None, ["Reject update"], style="flat", lfs=7.4)
    arrow(ax, (cx + 1.25, 4.22), (4.48, 4.22), color=C3); label(ax, 4.05, 4.36, "No", fs=7.0, color=C3)
    step(3.3, r"FedAvg: $w^{(t+1)}$ = weighted mean", C2)
    arrow(ax, (cx, 3.86), (cx, 3.73)); label(ax, cx + 0.12, 3.8, "Yes", fs=7.0, color=C2, ha="left")
    # loop back to the round test
    path(ax, [(cx - bw / 2, 3.51), (0.62, 3.51), (0.62, 6.42), (cx - 1.16, 6.42)], color=C1, lw=1.4)
    label(ax, 0.68, 4.0, r"$t \leftarrow t+1$", fs=7.0, color=C1, ha="left")
    # exit of the loop
    block(ax, 4.5, 6.15, 1.3, 0.55, C2, None, [r"$w^* \leftarrow w^{(R)}$", "commit model"], style="flat", lfs=7.2)
    arrow(ax, (cx + 1.15, 6.42), (4.48, 6.42), color=C2); label(ax, 4.1, 6.56, "No", fs=7.0, color=SUB)
    path(ax, [(5.8, 6.42), (5.86, 6.42), (5.86, 2.78), (cx + bw / 2 + 0.02, 2.78)], color=C2, lw=1.4)
    # trust evaluation
    step(2.57, r"Each device $d_i$: $\hat{y}_i = F(x_i; w^*)$", C3)
    step(1.97, r"Compute benign confidence $q_i$", C3)
    arrow(ax, (cx, 2.57), (cx, 2.4))
    diamond(ax, cx, 1.3, 1.35, 0.66, DG, r"$q_i < \delta$ ?", fs=7.8, shadow=False)
    arrow(ax, (cx, 1.97), (cx, 1.64))
    block(ax, 0.55, 0.95, 1.33, 0.55, C3, None, [r"flag$(d_i) = 1$", "raise to Plane A"], style="flat", lfs=7.0)
    arrow(ax, (cx - 0.68, 1.3), (1.9, 1.3), color=C3); label(ax, 2.05, 1.44, "Yes", fs=7.0, color=C3)
    block(ax, 3.4, 0.95, 1.6, 0.55, C2, None, [r"Commit $q_i$ as", "validated score"], style="flat", lfs=7.0)
    arrow(ax, (cx + 0.68, 1.3), (3.38, 1.3), color=C2); label(ax, 3.15, 1.44, "No", fs=7.0, color=C2)
    term(0.3, r"END: return $w^*$ and flags", 2.6)
    arrow(ax, (1.2, 0.95), (1.75, 0.62), color=SUB, lw=1.3)
    arrow(ax, (4.2, 0.95), (3.65, 0.62), color=SUB, lw=1.3)
    save(fig, "Fig4_train_flow.png")


fig_trust_flow()
fig_cnn_lstm()
fig_review_stats()
fig_engine()
fig_train_flow()
print("done")
