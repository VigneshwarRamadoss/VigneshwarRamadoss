#!/usr/bin/env python3
"""
Generate the responsive header SVG (header.svg).

Vercel/Linear-inspired aesthetic.
Establishes:
  - Vigneshwar Ramadoss
  - Co-Founder @ The Dot
  - "Problem → System → Build → Ship" engineering workflow
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme as T

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(T.ROOT, "header.svg")

W = 1200
H = 380

def generate_header():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Vigneshwar Ramadoss — Co-Founder @ The Dot</title>
  <desc id="desc">Technical Founder profile hero displaying Vigneshwar Ramadoss, Co-Founder @ The Dot, and the Problem to System to Build to Ship workflow.</desc>

  <defs>
    <!-- Background Grid -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{T.BRIGHT}" stroke-opacity="0.02" stroke-width="1"/>
      <circle cx="40" cy="40" r="1.5" fill="{T.BRIGHT}" fill-opacity="0.05"/>
    </pattern>

    <!-- Fades and Glows -->
    <radialGradient id="glow" cx="80%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{T.ACCENT}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{T.BG}" stop-opacity="0"/>
    </radialGradient>
    
    <linearGradient id="gridFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{T.BG}"/>
      <stop offset="0.3" stop-color="{T.BG}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{T.BG}" stop-opacity="0"/>
    </linearGradient>

    <style>
      .sans {{ font-family: {T.SANS}; }}
      .mono {{ font-family: {T.MONO}; }}
      
      /* Restrained animations */
      .fade-up {{ opacity: 0; animation: fUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
      .fade-in {{ opacity: 0; animation: fIn 1.2s ease-out forwards; }}
      .line-draw {{ stroke-dasharray: 400; stroke-dashoffset: 400; animation: drawL 2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
      .pulse {{ opacity: 0; animation: pNode 3s ease-in-out infinite; }}
      .data-stream {{ stroke-dasharray: 4 12; stroke-dashoffset: 0; animation: stream 15s linear infinite; }}
      
      .d-1 {{ animation-delay: 0.1s; }}
      .d-2 {{ animation-delay: 0.2s; }}
      .d-3 {{ animation-delay: 0.4s; }}
      .d-4 {{ animation-delay: 0.6s; }}
      .d-5 {{ animation-delay: 0.8s; }}
      
      @keyframes fUp {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: translateY(0); }} }}
      @keyframes fIn {{ to {{ opacity: 1; }} }}
      @keyframes drawL {{ to {{ stroke-dashoffset: 0; }} }}
      @keyframes pNode {{ 0%, 100% {{ r: 3; opacity: 0.3; stroke-width: 1; }} 50% {{ r: 8; opacity: 1; stroke-width: 1.5; }} }}
      @keyframes stream {{ to {{ stroke-dashoffset: -400; }} }}
      
      @media (prefers-reduced-motion: reduce) {{
        .fade-up, .fade-in, .line-draw, .pulse, .data-stream {{ animation: none !important; opacity: 1 !important; transform: none !important; stroke-dashoffset: 0 !important; }}
      }}
    </style>
  </defs>

  <!-- Base layer -->
  <rect width="{W}" height="{H}" fill="{T.BG}"/>
  
  <!-- Subtle Glow & Grid -->
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  <rect x="400" y="0" width="800" height="{H}" fill="url(#grid)"/>
  <rect x="400" y="0" width="800" height="{H}" fill="url(#gridFade)"/>
  
  <!-- Faint Border (Apple/Linear restraint) -->
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{T.RADIUS}" fill="none" stroke="{T.BRIGHT}" stroke-opacity="0.04"/>

  <!-- Top-left microcopy -->
  <g class="mono fade-in d-1" font-size="10" letter-spacing="2">
    <text x="64" y="56" fill="{T.MUTED}">ID /</text>
    <text x="96" y="56" fill="{T.BRIGHT}">VIGNESHWAR_RAMADOSS</text>
  </g>

  <!-- Left Identity Block -->
  <g class="fade-up d-1">
    <text class="sans" x="64" y="150" fill="{T.BRIGHT}" font-size="46" font-weight="600" letter-spacing="-1.2">Vigneshwar Ramadoss</text>
    
    <!-- Role & Company -->
    <g class="mono" font-size="12" letter-spacing="1.5">
      <text x="64" y="188" fill="{T.ACCENT}">CO-FOUNDER — THE DOT</text>
      <text x="248" y="188" fill="{T.DIM}">//</text>
      <text x="274" y="188" fill="{T.MUTED}">TECHNICAL FOUNDER</text>
    </g>

    <!-- Positioning Statement -->
    <text class="sans" x="64" y="244" fill="{T.INK}" font-size="17" font-weight="400" letter-spacing="-0.1">
      <tspan x="64" dy="0">Turning business problems into products, systems</tspan>
      <tspan x="64" dy="26">and high-performance digital experiences.</tspan>
    </text>

    <!-- Focus areas quietly integrated -->
    <g class="mono" font-size="11" letter-spacing="1.2">
      <text x="64" y="306" fill="{T.DIM}">FOCUS /</text>
      <text x="124" y="306" fill="{T.MUTED}">PRODUCT DEV</text>
      <text x="216" y="306" fill="{T.DIM}">·</text>
      <text x="230" y="306" fill="{T.MUTED}">DIGITAL TRANSFORMATION</text>
      <text x="408" y="306" fill="{T.DIM}">·</text>
      <text x="422" y="306" fill="{T.MUTED}">APPLIED AI</text>
    </g>
  </g>

  <!-- Bottom-left Status -->
  <g class="mono fade-in d-2" font-size="10" letter-spacing="1.5">
    <circle cx="68" cy="350" r="3" fill="{T.ACCENT}"/>
    <circle class="pulse d-2" cx="68" cy="350" r="3" fill="none" stroke="{T.ACCENT}"/>
    <text x="82" y="353" fill="{T.DIM}">STATUS:</text>
    <text x="136" y="353" fill="{T.BRIGHT}">SYSTEM ONLINE</text>
  </g>

  <!-- RIGHT SIDE: Architectural System Diagram -->
  <g class="fade-up d-3" transform="translate(680, 0)">
    
    <!-- Top-right microcopy -->
    <g class="mono" font-size="10" letter-spacing="2" text-anchor="end">
      <text x="456" y="56" fill="{T.DIM}">SYS_ARCH / 0.1</text>
    </g>

    <!-- Base Paths -->
    <g fill="none" stroke="{T.FRAME}" stroke-width="1.5" stroke-linejoin="round">
      <path class="line-draw d-3" d="M 40 140 L 80 140 L 120 180 L 160 180 L 280 180 L 320 180 L 360 220 L 400 220"/>
      <path class="line-draw d-4" stroke-opacity="0.4" d="M 40 220 L 80 220 L 120 180"/>
      <path class="line-draw d-5" stroke-opacity="0.4" d="M 280 180 L 320 180 L 360 140 L 440 140"/>
    </g>
    
    <!-- Streaming Data -->
    <path class="data-stream" d="M 40 140 L 80 140 L 120 180 L 160 180 L 280 180 L 320 180 L 360 220 L 400 220" fill="none" stroke="{T.ACCENT}" stroke-width="1.5" stroke-opacity="0.4" stroke-linejoin="round"/>

    <!-- [01] PROBLEM -->
    <g transform="translate(40, 140)">
      <circle cx="0" cy="0" r="12" fill="{T.BG}" stroke="{T.BRIGHT}" stroke-opacity="0.1" stroke-width="1"/>
      <circle cx="0" cy="0" r="3" fill="{T.MUTED}"/>
      <g class="mono" font-size="10" letter-spacing="1.5" text-anchor="middle">
        <text x="0" y="-22" fill="{T.DIM}">01</text>
        <text x="0" y="30" fill="{T.MUTED}">PROBLEM</text>
      </g>
    </g>

    <!-- [02] SYSTEM -->
    <g transform="translate(160, 180)">
      <circle cx="0" cy="0" r="12" fill="{T.BG}" stroke="{T.BRIGHT}" stroke-opacity="0.1" stroke-width="1"/>
      <circle cx="0" cy="0" r="3" fill="{T.MUTED}"/>
      <g class="mono" font-size="10" letter-spacing="1.5" text-anchor="middle">
        <text x="0" y="-22" fill="{T.DIM}">02</text>
        <text x="0" y="30" fill="{T.MUTED}">SYSTEM</text>
      </g>
    </g>

    <!-- [03] BUILD (Active) -->
    <g transform="translate(280, 180)">
      <!-- Aura -->
      <circle cx="0" cy="0" r="24" fill="{T.ACCENT}" fill-opacity="0.04"/>
      <circle cx="0" cy="0" r="16" fill="{T.BG}" stroke="{T.ACCENT}" stroke-width="1.5"/>
      <circle cx="0" cy="0" r="4" fill="{T.ACCENT}"/>
      <circle class="pulse d-4" cx="0" cy="0" r="4" fill="none" stroke="{T.ACCENT}"/>
      <g class="mono" font-size="10" letter-spacing="1.5" text-anchor="middle">
        <text x="0" y="-26" fill="{T.ACCENT}">03</text>
        <text x="0" y="34" fill="{T.BRIGHT}" font-weight="600">BUILD</text>
      </g>
    </g>

    <!-- [04] SHIP -->
    <g transform="translate(400, 220)">
      <circle cx="0" cy="0" r="12" fill="{T.BG}" stroke="{T.BRIGHT}" stroke-opacity="0.1" stroke-width="1"/>
      <circle cx="0" cy="0" r="3" fill="{T.MUTED}"/>
      <g class="mono" font-size="10" letter-spacing="1.5" text-anchor="middle">
        <text x="0" y="-22" fill="{T.DIM}">04</text>
        <text x="0" y="30" fill="{T.MUTED}">SHIP</text>
      </g>
    </g>

    <!-- Terminals/Ports -->
    <g class="mono fade-in d-5" font-size="9" fill="{T.DIM}" letter-spacing="1">
      <text x="445" y="143">OP_A</text>
      <text x="10" y="223">IP_B</text>
    </g>
  </g>
  
</svg>"""
    return svg

if __name__ == "__main__":
    svg = generate_header()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg):,} bytes)")
