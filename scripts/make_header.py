#!/usr/bin/env python3
"""
Generate the responsive editorial header SVG (header.svg).

Clean, static, editorial composition.
Strict two-column architecture:
  Left: x=64..650 (Identity, positioning, focus)
  Right: x=760..1136 (Problem -> System -> Build -> Ship typographic system)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme as T

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(T.ROOT, "header.svg")

W = 1200
H = 440

def generate_header():
    # Palette
    BG = "#0D1117"
    PRIMARY = "#F0F6FC"
    SECONDARY = "#B1BAC4"
    MUTED = "#6E7681"
    SUBTLE = "#484F58"
    RULE = "#30363D"
    ACCENT = "#58A6FF"

    SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
    MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', Menlo, Consolas, monospace"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Vigneshwar Ramadoss — Co-Founder · The Dot</title>
  <desc id="desc">Vigneshwar Ramadoss, Co-Founder at The Dot. Product Engineering, AI + Automation, and Interaction Systems.</desc>

  <defs>
    <radialGradient id="rightGlow" cx="950" cy="220" r="380" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <style>
      .sans {{ font-family: {SANS}; }}
      .mono {{ font-family: {MONO}; }}
    </style>
  </defs>

  <!-- Background Canvas -->
  <rect width="{W}" height="{H}" rx="12" fill="{BG}"/>
  <rect width="{W}" height="{H}" rx="12" fill="url(#rightGlow)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="{RULE}" stroke-opacity="0.35"/>

  <!-- ======================================================== -->
  <!-- LEFT REGION: IDENTITY, POSITIONING, FOCUS (x=64..650)    -->
  <!-- ======================================================== -->

  <!-- 01 Name -->
  <text class="sans" x="64" y="112" fill="{PRIMARY}" font-size="46" font-weight="700" letter-spacing="-0.025em">Vigneshwar Ramadoss</text>

  <!-- 02 Role & Company -->
  <text class="sans" x="64" y="152" font-size="15" font-weight="500" letter-spacing="0.01em">
    <tspan fill="{MUTED}">Co-Founder</tspan>
    <tspan fill="{SUBTLE}"> · </tspan>
    <tspan fill="{ACCENT}" font-weight="600">The Dot</tspan>
  </text>

  <!-- 03 Positioning Statement -->
  <text class="sans" x="64" y="218" fill="{PRIMARY}" font-size="19" font-weight="400" letter-spacing="-0.01em">
    <tspan x="64" dy="0">Turning business problems into</tspan>
    <tspan x="64" dy="28">digital products, systems</tspan>
    <tspan x="64" dy="28" fill="{SECONDARY}">and high-performance experiences.</tspan>
  </text>

  <!-- 04 Focus Disciplines (Quiet Typographic Stack) -->
  <g transform="translate(64, 340)">
    <!-- Item 01 -->
    <text class="mono" x="0" y="0" fill="{MUTED}" font-size="11" font-weight="500">01</text>
    <text class="mono" x="24" y="0" fill="{SUBTLE}" font-size="11">·</text>
    <text class="sans" x="38" y="0" fill="{SECONDARY}" font-size="12" font-weight="600" letter-spacing="0.06em">PRODUCT ENGINEERING</text>

    <!-- Item 02 -->
    <text class="mono" x="0" y="22" fill="{MUTED}" font-size="11" font-weight="500">02</text>
    <text class="mono" x="24" y="22" fill="{SUBTLE}" font-size="11">·</text>
    <text class="sans" x="38" y="22" fill="{SECONDARY}" font-size="12" font-weight="600" letter-spacing="0.06em">AI + AUTOMATION</text>

    <!-- Item 03 -->
    <text class="mono" x="0" y="44" fill="{MUTED}" font-size="11" font-weight="500">03</text>
    <text class="mono" x="24" y="44" fill="{SUBTLE}" font-size="11">·</text>
    <text class="sans" x="38" y="44" fill="{SECONDARY}" font-size="12" font-weight="600" letter-spacing="0.06em">INTERACTION SYSTEMS</text>
  </g>

  <!-- ======================================================== -->
  <!-- RIGHT REGION: ARCHITECTURAL INDEX SYSTEM (x=760..1136)   -->
  <!-- ======================================================== -->

  <!-- Row 01: PROBLEM -->
  <g transform="translate(760, 112)">
    <text class="mono" x="0" y="0" fill="{MUTED}" font-size="12" font-weight="500">01</text>
    <text class="sans" x="42" y="0" fill="{SECONDARY}" font-size="20" font-weight="600" letter-spacing="0.08em">PROBLEM</text>
    <line x1="184" y1="-6" x2="376" y2="-6" stroke="{RULE}" stroke-opacity="0.6" stroke-width="1"/>
  </g>

  <!-- Row 02: SYSTEM -->
  <g transform="translate(760, 180)">
    <text class="mono" x="0" y="0" fill="{MUTED}" font-size="12" font-weight="500">02</text>
    <text class="sans" x="42" y="0" fill="{SECONDARY}" font-size="20" font-weight="600" letter-spacing="0.08em">SYSTEM</text>
    <line x1="184" y1="-6" x2="376" y2="-6" stroke="{RULE}" stroke-opacity="0.6" stroke-width="1"/>
  </g>

  <!-- Row 03: BUILD (Active / Primary Accent) -->
  <g transform="translate(760, 248)">
    <text class="mono" x="0" y="0" fill="{ACCENT}" font-size="12" font-weight="600">03</text>
    <text class="sans" x="42" y="0" fill="{ACCENT}" font-size="20" font-weight="700" letter-spacing="0.08em">BUILD</text>
    <line x1="184" y1="-6" x2="376" y2="-6" stroke="{ACCENT}" stroke-opacity="0.9" stroke-width="1.5"/>
  </g>

  <!-- Row 04: SHIP -->
  <g transform="translate(760, 316)">
    <text class="mono" x="0" y="0" fill="{MUTED}" font-size="12" font-weight="500">04</text>
    <text class="sans" x="42" y="0" fill="{SECONDARY}" font-size="20" font-weight="600" letter-spacing="0.08em">SHIP</text>
    <line x1="184" y1="-6" x2="376" y2="-6" stroke="{RULE}" stroke-opacity="0.6" stroke-width="1"/>
  </g>

  <!-- Operating Signature (Bottom Right) -->
  <text class="mono" x="760" y="384" fill="{MUTED}" font-size="11" letter-spacing="0.1em">Problem → System → Build → Ship</text>

</svg>"""
    return svg

if __name__ == "__main__":
    svg = generate_header()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg):,} bytes)")
