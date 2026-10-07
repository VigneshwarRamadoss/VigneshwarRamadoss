"""
Shared design tokens for every generated SVG, so the header, portrait, info
card and heatmap read as one system. Change a colour here, re-run
`python scripts/build_all.py`, and all assets update together.
"""
import os

USERNAME = os.environ.get("GH_PROFILE_USER", "VigneshwarRamadoss")
PROMPT_USER = "vigneshwar"
PROMPT_HOST = "thedot"


def prompt(cmd=""):
    """Terminal prompt string used in title bars / labels."""
    return f"{PROMPT_USER}@{PROMPT_HOST}:~$ {cmd}".rstrip()


# ---- palette: monochrome + a single accent (no rainbow) -------------------
BG = "#0d1117"        # github dark canvas
BG2 = "#10161f"       # top of the subtle vertical gradient
PANEL = "#161b22"     # inner tiles / empty heatmap cell
FRAME = "#30363d"     # window border
RULE = "#21262d"      # hairlines
DIM = "#484f58"       # tertiary text
MUTED = "#7d8590"     # secondary text
INK = "#c9d1d9"       # primary text / ascii ink
BRIGHT = "#f0f6fc"    # emphasis
ACCENT = "#58a6ff"    # the one accent colour
ACCENT_DEEP = "#1f6feb"
OK = "#3fb950"        # status dot only

# heatmap ramp: empty -> brightest, all in the accent hue
HEAT = ["#161b22", "#0c2d4f", "#0f4c81", "#1f6feb", "#58a6ff"]

MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

RADIUS = 12
TITLEBAR_H = 34
PAD = 22

# portrait + info card share this canvas so they pair at equal widths
PAIR_W = 840
PAIR_H = 900

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DATA_PATH = os.path.join(ROOT, "data", "contributions.json")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def window(w, h, title, gid="bg"):
    """Common terminal window chrome: gradient body, border, title bar.

    Deliberately not the macOS traffic lights: three muted dots plus a
    left-aligned path label keeps the frame quiet.
    """
    parts = [
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
        f'</linearGradient></defs>',
        f'<rect width="{w}" height="{h}" rx="{RADIUS}" fill="url(#{gid})"/>',
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{RADIUS-0.5}" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{w}" y2="{TITLEBAR_H}" stroke="{RULE}"/>',
    ]
    for i in range(3):
        parts.append(f'<circle cx="{PAD + i*14}" cy="{TITLEBAR_H/2}" r="4" fill="{DIM if i else ACCENT}" '
                     f'fill-opacity="{1 if i == 0 else 0.6}"/>')
    parts.append(f'<text x="{PAD + 50}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'font-family="{MONO}">{esc(title)}</text>')
    return parts


def svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(label)}" font-family="{MONO}">'
            f'<title>{esc(label)}</title>')


def write(path, svg):
    full = os.path.join(ROOT, path)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {path} ({len(svg):,} bytes)")
