#!/usr/bin/env python3
"""
Generate the terminal info card SVG (info-card.svg).

Neofetch / CLI style info card designed to pair with vignesh-ascii.svg (840 x 900).
Prioritizes technical founder identity, focus hierarchy, and live GitHub signals.

    python scripts/make_info_card.py [data.json] [out.svg]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme as T

SRC = sys.argv[1] if len(sys.argv) > 1 else T.DATA_PATH
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(T.ROOT, "info-card.svg")

W, H = T.PAIR_W, T.PAIR_H
PAD = 32

def generate_info_card(data=None):
    if data is None and os.path.exists(SRC):
        try:
            with open(SRC, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = None
            
    if data is None:
        data = {
            "total_contributions": 254,
            "active_days": 56,
            "current_streak": {"length": 1},
            "longest_streak": {"length": 6},
            "profile": {"public_repos": 47}
        }

    total_contribs = data.get("total_contributions", 0)
    active_days = data.get("active_days", 0)
    current_streak = data.get("current_streak", {}).get("length", 0)
    longest_streak = data.get("longest_streak", {}).get("length", 0)
    repos = data.get("profile", {}).get("public_repos", 47) or 47

    css = f"""
      .mono {{ font-family: {T.MONO}; }}
      .sans {{ font-family: {T.SANS}; }}
      .row-fade {{ opacity: 0; animation: rowIn 0.4s ease-out forwards; }}
      .d1 {{ animation-delay: 0.2s; }}
      .d2 {{ animation-delay: 0.5s; }}
      .d3 {{ animation-delay: 0.8s; }}
      .d4 {{ animation-delay: 1.1s; }}
      .d5 {{ animation-delay: 1.4s; }}
      .d6 {{ animation-delay: 1.7s; }}
      .d7 {{ animation-delay: 2.0s; }}
      .d8 {{ animation-delay: 2.3s; }}
      .cursor-blink {{ opacity: 0; animation: blinkCur 1.1s ease-in-out 2.5s infinite; }}
      
      @keyframes rowIn {{
        from {{ opacity: 0; transform: translateY(4px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes blinkCur {{
        0%, 49% {{ opacity: 0.9; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .row-fade, .cursor-blink {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
      }}
    """

    parts = [
        T.svg_open(W, H, "Vigneshwar Ramadoss - Terminal Info Card"),
        f"<style>{css}</style>",
    ]
    parts += T.window(W, H, "~/identity  ·  neofetch --system", gid="ibg")

    # Command Line 1: whoami
    y = T.TITLEBAR_H + 38
    parts.append(f'<g class="row-fade d1 mono" font-size="14">')
    parts.append(f'<text x="{PAD}" y="{y}" fill="{T.MUTED}">{T.esc(T.prompt("whoami"))}</text>')
    parts.append(f'</g>')

    # Output 1: Name & Title Block
    y += 34
    parts.append(f'<g class="row-fade d2">')
    # Name banner
    parts.append(f'<rect x="{PAD}" y="{y-18}" width="{W - PAD*2}" height="76" rx="8" fill="{T.PANEL}" stroke="{T.RULE}"/>')
    parts.append(f'<text class="sans" x="{PAD+20}" y="{y+16}" font-size="24" font-weight="700" fill="{T.BRIGHT}">{T.esc("Vigneshwar Ramadoss")}</text>')
    parts.append(f'<text class="mono" x="{PAD+20}" y="{y+42}" font-size="13" fill="{T.ACCENT}">{T.esc("Co-Founder @ The Dot")}</text>')
    parts.append(f'<text class="mono" x="{W - PAD - 20}" y="{y+42}" font-size="12" fill="{T.DIM}" text-anchor="end">SYS: CO-FOUNDER</text>')
    parts.append(f'</g>')

    # Command Line 2: focus
    y += 104
    parts.append(f'<g class="row-fade d3 mono" font-size="14">')
    parts.append(f'<text x="{PAD}" y="{y}" fill="{T.MUTED}">{T.esc(T.prompt("cat focus.tree"))}</text>')
    parts.append(f'</g>')

    # Output 2: Focus Tree
    y += 28
    focus_items = [
        ("Product Engineering", "From idea to scalable production systems"),
        ("Intelligent Systems", "Autonomous workflows, applied AI leverage"),
        ("Interaction Engineering", "High-craft digital interfaces & UX"),
        ("Digital Transformation", "Modernizing legacy operations & workflows"),
        ("Automation Architecture", "End-to-end tooling & operations pipelines"),
    ]

    parts.append(f'<g class="row-fade d4 mono" font-size="13.5">')
    parts.append(f'<rect x="{PAD}" y="{y-16}" width="{W - PAD*2}" height="194" rx="8" fill="{T.PANEL}" stroke="{T.RULE}"/>')
    
    tree_y = y + 14
    for i, (title, subtitle) in enumerate(focus_items):
        is_last = (i == len(focus_items) - 1)
        branch = "└── " if is_last else "├── "
        parts.append(f'<text x="{PAD+18}" y="{tree_y}" fill="{T.ACCENT}">{branch}<tspan fill="{T.BRIGHT}" font-weight="600">{T.esc(title)}</tspan></text>')
        parts.append(f'<text x="{PAD+280}" y="{tree_y}" font-size="12" fill="{T.MUTED}">// {T.esc(subtitle)}</text>')
        tree_y += 34
    parts.append(f'</g>')

    # Command Line 3: building
    y += 224
    parts.append(f'<g class="row-fade d5 mono" font-size="14">')
    parts.append(f'<text x="{PAD}" y="{y}" fill="{T.MUTED}">{T.esc(T.prompt("cat organisation.info"))}</text>')
    parts.append(f'</g>')

    # Output 3: Organization Details
    y += 26
    parts.append(f'<g class="row-fade d6 mono" font-size="13">')
    parts.append(f'<rect x="{PAD}" y="{y-16}" width="{W - PAD*2}" height="76" rx="8" fill="{T.PANEL}" stroke="{T.RULE}"/>')
    parts.append(f'<text x="{PAD+20}" y="{y+14}" fill="{T.DIM}">COMPANY    <tspan fill="{T.BRIGHT}" font-weight="600">The Dot</tspan> <tspan fill="{T.MUTED}">(thedotco.in)</tspan></text>')
    parts.append(f'<text x="{PAD+20}" y="{y+42}" fill="{T.DIM}">MISSION    <tspan fill="{T.INK}">Digital Transformation &amp; Product Engineering Studio</tspan></text>')
    parts.append(f'</g>')

    # Command Line 4: live signals
    y += 104
    parts.append(f'<g class="row-fade d7 mono" font-size="14">')
    parts.append(f'<text x="{PAD}" y="{y}" fill="{T.MUTED}">{T.esc(T.prompt("git status --summary"))}</text>')
    parts.append(f'</g>')

    # Output 4: Live GitHub Signals
    y += 26
    tile_w = (W - PAD * 2 - 24) / 3
    signals = [
        ("CONTRIBUTIONS", f"{total_contribs:,}", "in the last year"),
        ("ACTIVE DAYS", f"{active_days}", "active commit days"),
        ("STREAK (DAYS)", f"{current_streak}", f"longest: {longest_streak}d"),
    ]

    parts.append(f'<g class="row-fade d8 mono">')
    for i, (label, val, sub) in enumerate(signals):
        tx = PAD + i * (tile_w + 12)
        parts.append(f'<rect x="{tx}" y="{y-14}" width="{tile_w}" height="76" rx="8" fill="{T.PANEL}" stroke="{T.RULE}"/>')
        parts.append(f'<text x="{tx+16}" y="{y+10}" font-size="10.5" fill="{T.DIM}" letter-spacing="1.2">{label}</text>')
        parts.append(f'<text class="sans" x="{tx+16}" y="{y+40}" font-size="22" font-weight="700" fill="{T.ACCENT if i == 0 else T.BRIGHT}">{val}</text>')
        parts.append(f'<text x="{tx+16 + len(val)*14 + 10}" y="{y+38}" font-size="11" fill="{T.MUTED}">{sub}</text>')
    parts.append(f'</g>')

    # Bottom Terminal Prompt with blinking cursor
    foot_y = H - 24
    parts.append(f'<line x1="0" y1="{H - 46}" x2="{W}" y2="{H - 46}" stroke="{T.RULE}"/>')
    prompt_txt = T.prompt("")
    parts.append(f'<text class="mono" x="{PAD}" y="{foot_y}" font-size="13" fill="{T.MUTED}">{T.esc(prompt_txt)}</text>')
    cur_x = PAD + len(prompt_txt) * 7.8 + 6
    parts.append(f'<rect class="cursor-blink" x="{cur_x:.1f}" y="{foot_y-11}" width="7.5" height="14" fill="{T.ACCENT}"/>')
    parts.append(f'<text class="mono" x="{W - PAD}" y="{foot_y}" font-size="11" fill="{T.DIM}" text-anchor="end">VIGNESHWAR // THE DOT</text>')

    parts.append("</svg>")
    return "".join(parts)

if __name__ == "__main__":
    svg = generate_info_card()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg):,} bytes)")
