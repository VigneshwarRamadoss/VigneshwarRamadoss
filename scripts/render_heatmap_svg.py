#!/usr/bin/env python3
"""
Render data/contributions.json as a custom, animated contribution heatmap.

Different from GitHub's default graph:
  * monochrome-blue ramp from the shared theme (no green)
  * intensity uses GitHub's own relative `data-level`, so a 250/year graph has
    as much contrast as a 9,000/year one
  * a single headline number, then a quiet metrics strip underneath:
    active days, current / longest streak, best day, most active weekday
  * reveal: cells fade in along a diagonal (CSS keyframes, once), the metrics
    follow, and today's cell keeps a slow, low-contrast pulse so the graph
    reads as "live" without being busy

    python scripts/render_heatmap_svg.py [data.json] [out.svg]
"""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme as T  # noqa: E402

SRC = sys.argv[1] if len(sys.argv) > 1 else T.DATA_PATH
OUT = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"

CELL, GAP = 13, 3
STEP = CELL + GAP
SIDE = 34
LABEL_W = 34
HEAD_H = 78          # headline block under the title bar
MONTH_H = 18
FOOT_H = 104

COL_T, ROW_T, CELL_DUR = 0.02, 0.05, 0.5


def fmt_date(s, year=False):
    d = dt.date.fromisoformat(s)
    return f"{d.strftime('%b')} {d.day}" + (f", {d.year}" if year else "")


def grid_of(days):
    first = dt.date.fromisoformat(days[0]["date"])
    col = [None] * ((first.weekday() + 1) % 7)          # sunday-first rows
    grid = []
    for d in days:
        col.append(d)
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        grid.append(col + [None] * (7 - len(col)))
    return grid


def render(data):
    days = data["days"]
    grid = grid_of(days)
    gw = len(grid) * STEP - GAP
    W = SIDE * 2 + LABEL_W + gw
    grid_top = T.TITLEBAR_H + HEAD_H + MONTH_H
    grid_left = SIDE + LABEL_W
    grid_bottom = grid_top + 7 * STEP - GAP
    H = grid_bottom + 30 + FOOT_H
    grid_done = (len(grid) - 1) * COL_T + 6 * ROW_T + CELL_DUR

    css = (
        "@keyframes c{from{opacity:0}to{opacity:1}}"
        f".c{{opacity:0;animation:c {CELL_DUR}s ease-out both}}"
        "@keyframes up{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}"
        ".m{opacity:0;animation:up .5s ease-out both}"
        "@keyframes p{0%,100%{stroke-opacity:0}50%{stroke-opacity:.9}}"
        f".today{{stroke-opacity:0;animation:p 2.6s ease-in-out {grid_done:.2f}s infinite}}"
        "@media (prefers-reduced-motion:reduce){.c,.m{opacity:1!important;animation:none!important;transform:none!important}.today{animation:none;stroke-opacity:.9}}"
    )
    p = [T.svg_open(W, H, f"{data['username']} - contribution activity, last 12 months"),
         f"<style>{css}</style>"]
    p += T.window(W, H, '~/activity  ·  git log --all --since="1 year" --graph', gid="hbg")

    # ---- headline -----------------------------------------------------------
    total = data["total_contributions"]
    hy = T.TITLEBAR_H + 46
    p.append(f'<text x="{SIDE}" y="{hy}" font-size="30" font-weight="600" fill="{T.BRIGHT}" '
             f'font-family="{T.SANS}" letter-spacing="-0.5">{total:,}</text>')
    num_w = len(f"{total:,}") * 17.5 + 12
    p.append(f'<text x="{SIDE + num_w:.0f}" y="{hy}" font-size="13" fill="{T.MUTED}">contributions in the last year</text>')
    rng = data["range"]
    l30, p30 = data.get("last_30_days", 0), data.get("previous_30_days", 0)
    trend = "↑" if l30 > p30 else ("↓" if l30 < p30 else "→")
    p.append(f'<text x="{W - SIDE}" y="{hy - 14}" font-size="11" fill="{T.DIM}" text-anchor="end">'
             f'{fmt_date(rng["start"], True)}  →  {fmt_date(rng["end"], True)}</text>')
    p.append(f'<text x="{W - SIDE}" y="{hy + 4}" font-size="12" fill="{T.MUTED}" text-anchor="end">last 30 days '
             f'<tspan fill="{T.ACCENT}">{l30:,} {trend}</tspan></text>')

    # ---- labels -------------------------------------------------------------
    seen = set()
    last_x = -99
    for ci, col in enumerate(grid):
        d = next((c for c in col if c), None)
        if not d:
            continue
        date = dt.date.fromisoformat(d["date"])
        key = (date.year, date.month)
        if key not in seen and date.day <= 7:
            seen.add(key)
            x = grid_left + ci * STEP
            if x - last_x > 30:
                p.append(f'<text x="{x}" y="{grid_top - 7}" font-size="10" fill="{T.MUTED}">{date.strftime("%b")}</text>')
                last_x = x
    for ri, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        p.append(f'<text x="{SIDE}" y="{grid_top + ri * STEP + CELL - 3}" font-size="9.5" fill="{T.DIM}">{name}</text>')

    # ---- cells --------------------------------------------------------------
    today = days[-1]["date"]
    today_xy = None
    for ci, col in enumerate(grid):
        for ri, d in enumerate(col):
            if not d:
                continue
            x, y = grid_left + ci * STEP, grid_top + ri * STEP
            lvl = max(0, min(4, d["level"]))
            delay = ci * COL_T + ri * ROW_T
            s = "" if d["count"] == 1 else "s"
            p.append(f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{T.HEAT[lvl]}" '
                     f'style="animation-delay:{delay:.2f}s"><title>{d["count"]} contribution{s} · {fmt_date(d["date"], True)}</title></rect>')
            if d["date"] == today:
                today_xy = (x, y)
    if today_xy:
        x, y = today_xy
        p.append(f'<rect class="today" x="{x - 2.5}" y="{y - 2.5}" width="{CELL + 5}" height="{CELL + 5}" rx="4.5" '
                 f'fill="none" stroke="{T.ACCENT}" stroke-width="1.2"/>')

    # ---- legend -------------------------------------------------------------
    ly = grid_bottom + 12
    lx = W - SIDE - len(T.HEAT) * (CELL - 2 + 3) - 34
    p.append(f'<text x="{lx - 8}" y="{ly + 9}" font-size="10" fill="{T.DIM}" text-anchor="end">less</text>')
    for i, c in enumerate(T.HEAT):
        p.append(f'<rect x="{lx + i * (CELL + 1)}" y="{ly}" width="{CELL - 2}" height="{CELL - 2}" rx="2.5" fill="{c}"/>')
    p.append(f'<text x="{lx + len(T.HEAT) * (CELL + 1) + 6}" y="{ly + 9}" font-size="10" fill="{T.DIM}">more</text>')
    if today_xy:
        p.append(f'<rect x="{grid_left}" y="{ly + 0.5}" width="9" height="9" rx="2.5" fill="none" stroke="{T.ACCENT}"/>'
                 f'<text x="{grid_left + 15}" y="{ly + 9}" font-size="10" fill="{T.DIM}">today</text>')

    # ---- metrics strip --------------------------------------------------------
    fy = H - FOOT_H
    p.append(f'<line x1="0" y1="{fy}" x2="{W}" y2="{fy}" stroke="{T.RULE}"/>')
    cur, lng, best = data["current_streak"], data["longest_streak"], data["best_day"]
    n_days = len(days)
    metrics = [
        ("active days", f'{data["active_days"]}', f'/ {n_days}  ·  {data["active_days"] / n_days:.0%}'),
        ("current streak", f'{cur["length"]}', "day" + ("" if cur["length"] == 1 else "s")),
        ("longest streak", f'{lng["length"]}', f'days  ·  {fmt_date(lng["start"])}' if lng["start"] else "days"),
        ("best day", f'{best["count"]}', fmt_date(best["date"])),
        ("most active", (data.get("most_active_weekday") or "—")[:3], "weekday"),
    ]
    colw = (W - SIDE * 2) / len(metrics)
    for i, (label, value, sub) in enumerate(metrics):
        x = SIDE + i * colw
        delay = grid_done + 0.08 * i
        if i:
            p.append(f'<line x1="{x - 14:.0f}" y1="{fy + 26}" x2="{x - 14:.0f}" y2="{fy + FOOT_H - 24}" stroke="{T.RULE}"/>')
        p.append(f'<g class="m" style="animation-delay:{delay:.2f}s">'
                 f'<text x="{x:.0f}" y="{fy + 34}" font-size="10" fill="{T.DIM}" letter-spacing="1.4">{label.upper()}</text>'
                 f'<text x="{x:.0f}" y="{fy + 66}" font-size="24" font-weight="600" font-family="{T.SANS}" '
                 f'fill="{T.ACCENT if i == 1 else T.BRIGHT}">{T.esc(value)}</text>'
                 f'<text x="{x + len(value) * 14 + 8:.0f}" y="{fy + 66}" font-size="11" fill="{T.MUTED}">{T.esc(sub)}</text>'
                 f'</g>')
    p.append("</svg>")
    return "".join(p), W, H


if __name__ == "__main__":
    data = json.load(open(SRC, encoding="utf-8"))
    svg, w, h = render(data)
    T.write(OUT, svg)
    print(f"canvas {w}x{h}")
