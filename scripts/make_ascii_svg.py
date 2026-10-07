#!/usr/bin/env python3
"""
Turn the prepped light map into an animated ASCII portrait SVG.

Rendering
  * One <text> per row, a single gradient ink (cool white -> accent blue
    toward the shoulders) instead of per-character colours, so the file
    stays small and the portrait stays clean.
  * Positive mapping: brighter pixel -> denser glyph (light on dark).

Animation (SMIL -- runs inside GitHub's <img> rendering, JS never does)
  1. A faint "ghost" of the full portrait is visible immediately (7% opacity),
     so the frame never looks empty.
  2. A single clip rect grows top -> bottom while a soft scanline rides its
     edge, "developing" the portrait at full brightness in ~3.4s.
  3. The scanline fades, the status bar flips from `rendering…` to the final
     line and a cursor blinks. Then everything holds -- no looping motion.
  Only a handful of animated elements (vs one clip per row), so the SVG is
  light and smooth.

    python scripts/make_ascii_svg.py [prepped.png] [out.svg] [--preview out.png]
    STATIC=1 python scripts/make_ascii_svg.py    # frozen frame, no animation
"""
import os
import sys

import numpy as np
from PIL import Image, ImageEnhance

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme as T  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
PREVIEW = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
if PREVIEW in args:
    args.remove(PREVIEW)
SRC = args[0] if len(args) > 0 else os.path.join(T.ROOT, "assets", "portrait-prepped.png")
OUT = args[1] if len(args) > 1 else "vignesh-ascii.svg"
STATIC = bool(os.environ.get("STATIC"))

# ---- grid ------------------------------------------------------------------
W, H = T.PAIR_W, T.PAIR_H
SIDE = 20
STATUS_H = 38
COLS = int(os.environ.get("COLS", 140))
ART_W = W - SIDE * 2
CELL_W = ART_W / COLS
CELL_H = CELL_W * 1.875                       # typical monospace aspect
ART_TOP = T.TITLEBAR_H + 10
ROWS = int((H - ART_TOP - STATUS_H - 8) // CELL_H)
ART_H = ROWS * CELL_H
FONT = CELL_W / 0.6                           # mono glyph advance ~0.6em

RAMP = os.environ.get("RAMP", " .`-:=+*#%@")   # sparse -> dense
CUTOFF = float(os.environ.get("CUTOFF", 0.06))  # below this -> blank terminal
GAMMA = float(os.environ.get("GAMMA", 1.0))     # >1 keeps only highlights dense
CONTRAST = float(os.environ.get("CONTRAST", 1.08))
EQ = float(os.environ.get("EQ", 0.7))            # 0 = linear, 1 = fully equalised
DETAIL = float(os.environ.get("DETAIL", 0.8))    # grid-scale sharpening

# ---- timing ----------------------------------------------------------------
BEGIN = 0.35
REVEAL = 3.4


def sample():
    """Sample to the character grid, then equalise *at grid resolution*.

    A lit face is mostly bright, so a plain linear mapping saturates it into a
    block of '@' and the features (eyes, brows, beard) become barely-visible
    holes. Rank-equalising the subject's cells spreads them evenly over the
    ramp, and a small unsharp pass at grid scale re-draws the features.
    """
    im = Image.open(SRC).convert("L")
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)
    a = np.asarray(im.resize((COLS, ROWS), Image.LANCZOS), dtype=np.float32) / 255.0
    mask = a >= CUTOFF
    vals = a[mask]
    eq = a.copy()
    eq[mask] = vals.argsort().argsort() / max(len(vals) - 1, 1)
    v = EQ * eq + (1 - EQ) * a
    pad = np.pad(v, 1, mode="edge")
    blur = sum(pad[dy:dy + ROWS, dx:dx + COLS] for dy in range(3) for dx in range(3)) / 9
    v = np.clip(v + DETAIL * (v - blur), 0, 1) ** GAMMA
    n = len(RAMP) - 1
    rows = []
    for y in range(ROWS):
        line = []
        for x in range(COLS):
            if not mask[y, x]:
                line.append(" ")
            else:
                line.append(RAMP[1 + min(n - 1, int(v[y, x] * n))])
        rows.append("".join(line).rstrip())
    return rows


def build(rows):
    p = [T.svg_open(W, H, "Vigneshwar Ramadoss - animated ASCII portrait")]
    p += T.window(W, H, "~/portrait  ·  ascii --render vigneshwar.png", gid="pbg")
    p.append(
        f'<defs><linearGradient id="ink" gradientUnits="userSpaceOnUse" x1="0" y1="{ART_TOP}" x2="0" y2="{ART_TOP + ART_H}">'
        f'<stop offset="0" stop-color="{T.BRIGHT}"/><stop offset="0.55" stop-color="{T.INK}"/>'
        f'<stop offset="1" stop-color="{T.ACCENT}"/></linearGradient>'
        f'<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{T.ACCENT}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{T.ACCENT}" stop-opacity="0.35"/></linearGradient></defs>'
    )

    lines = []
    for r, line in enumerate(rows):
        if not line:
            continue
        y = ART_TOP + r * CELL_H + CELL_H * 0.78
        n = len(line)
        lines.append(f'<text x="{SIDE}" y="{y:.1f}" textLength="{n * CELL_W:.1f}" lengthAdjust="spacing" '
                     f'xml:space="preserve">{T.esc(line)}</text>')
    # no id: the group is emitted twice (ghost + revealed copy)
    art = (f'<g fill="url(#ink)" font-size="{FONT:.2f}">' + "".join(lines) + "</g>")

    status_y = H - STATUS_H / 2 + 4
    p.append(f'<line x1="0" y1="{H - STATUS_H}" x2="{W}" y2="{H - STATUS_H}" stroke="{T.RULE}"/>')
    left = (f'<tspan fill="{T.MUTED}">{T.esc(T.prompt())} </tspan>'
            f'<tspan fill="{T.INK}">whoami</tspan>')
    final = f'<tspan fill="{T.DIM}">  →  </tspan><tspan fill="{T.BRIGHT}">Vigneshwar Ramadoss</tspan>'
    right_txt = f"{COLS}×{ROWS}"

    if STATIC:
        p.append(art)
        p.append(f'<text x="{SIDE}" y="{status_y:.1f}" font-size="13">{left}{final}</text>')
    else:
        end = BEGIN + REVEAL
        p.append(f'<g opacity="0.07">{art}</g>')
        p.append(
            f'<clipPath id="reveal"><rect x="0" y="{ART_TOP}" width="{W}" height="0">'
            f'<animate attributeName="height" values="0;{ART_H + 4:.1f}" keyTimes="0;1" calcMode="spline" '
            f'keySplines="0.45 0 0.25 1" begin="{BEGIN}s" dur="{REVEAL}s" fill="freeze"/></rect></clipPath>'
        )
        p.append(f'<g clip-path="url(#reveal)">{art}</g>')
        p.append(
            f'<rect x="{SIDE - 6}" y="{ART_TOP - 22}" width="{ART_W + 12}" height="22" fill="url(#scan)" opacity="0">'
            f'<animate attributeName="y" values="{ART_TOP - 22};{ART_TOP + ART_H - 18:.1f}" keyTimes="0;1" calcMode="spline" '
            f'keySplines="0.45 0 0.25 1" begin="{BEGIN}s" dur="{REVEAL}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="1" begin="{BEGIN}s"/>'
            f'<animate attributeName="opacity" to="0" begin="{end}s" dur="0.5s" fill="freeze"/></rect>'
        )
        # status: "rendering…" then the final answer
        p.append(f'<text x="{SIDE}" y="{status_y:.1f}" font-size="13">{left}'
                 f'<tspan fill="{T.DIM}">  rendering…</tspan>'
                 f'<set attributeName="opacity" to="0" begin="{end}s" fill="freeze"/></text>')
        p.append(f'<text x="{SIDE}" y="{status_y:.1f}" font-size="13" opacity="0">{left}{final}'
                 f'<set attributeName="opacity" to="1" begin="{end}s" fill="freeze"/></text>')
        # blinking block cursor after the name
        cur_x = SIDE + len(T.prompt() + " whoami  →  Vigneshwar Ramadoss ") * 13 * 0.6
        p.append(f'<rect x="{cur_x:.1f}" y="{status_y - 11:.1f}" width="7.5" height="14" fill="{T.ACCENT}" opacity="0">'
                 f'<animate attributeName="opacity" values="0.9;0.9;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" '
                 f'begin="{end}s" repeatCount="indefinite"/></rect>')

    p.append(f'<text x="{W - SIDE}" y="{status_y:.1f}" font-size="11" fill="{T.DIM}" text-anchor="end">{right_txt}</text>')
    p.append("</svg>")
    return "".join(p)


def preview(rows, path):
    """Rasterise the final frame with PIL so the portrait can be checked locally."""
    from PIL import ImageDraw, ImageFont
    scale = 2
    img = Image.new("RGB", (W * scale, H * scale), T.BG)
    d = ImageDraw.Draw(img)
    font = None
    for name in ("consola.ttf", "DejaVuSansMono.ttf", "Menlo.ttc"):
        try:
            font = ImageFont.truetype(name, int(FONT * scale))
            break
        except OSError:
            pass
    font = font or ImageFont.load_default()
    for r, line in enumerate(rows):
        t = r / max(ROWS - 1, 1)
        col = tuple(int(a + (b - a) * max(0, (t - 0.55) / 0.45)) for a, b in ((201, 88), (209, 166), (217, 255)))
        for c, ch in enumerate(line):
            if ch != " ":
                d.text(((SIDE + c * CELL_W) * scale, (ART_TOP + r * CELL_H) * scale), ch, fill=col, font=font)
    img.save(path)
    print("preview", path)


if __name__ == "__main__":
    rows = sample()
    T.write(OUT, build(rows))
    print(f"grid {COLS}x{ROWS}, cell {CELL_W:.2f}x{CELL_H:.2f}px, canvas {W}x{H}")
    if PREVIEW:
        preview(rows, PREVIEW)
