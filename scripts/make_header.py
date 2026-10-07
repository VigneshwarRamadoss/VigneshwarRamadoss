#!/usr/bin/env python3
"""
Generate the responsive header SVG (header.svg).

Establishes:
  - Vigneshwar Ramadoss
  - Co-Founder @ The Dot
  - "Problem → System → Build → Ship" engineering workflow
  - Product Development · Digital Transformation · Applied AI · Automation
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
  <title id="title">Vigneshwar Ramadoss — Co-Founder @ The Dot | Digital Transformation &amp; Product Development</title>
  <desc id="desc">Technical Founder profile hero displaying Vigneshwar Ramadoss, Co-Founder @ The Dot, and the Problem to System to Build to Ship workflow.</desc>

  <defs>
    <pattern id="headerGrid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#8b949e" stroke-opacity="0.04" stroke-width="1"/>
    </pattern>
    <linearGradient id="headerFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{T.BG}"/>
      <stop offset="0.6" stop-color="{T.BG}" stop-opacity="0.3"/>
      <stop offset="1" stop-color="{T.BG}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="glowLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{T.ACCENT}" stop-opacity="0.8"/>
      <stop offset="1" stop-color="{T.ACCENT_DEEP}" stop-opacity="0.2"/>
    </linearGradient>
    <style>
      .sans {{ font-family: {T.SANS}; }}
      .mono {{ font-family: {T.MONO}; }}
      .h-in {{ opacity: 0; transform: translateY(4px); animation: hIn 0.5s ease-out 0.05s forwards; }}
      .fade-up {{ opacity: 0; animation: fUp 0.45s ease-out forwards; }}
      .delay-1 {{ animation-delay: 0.25s; }}
      .delay-2 {{ animation-delay: 0.5s; }}
      .delay-3 {{ animation-delay: 0.75s; }}
      .delay-4 {{ animation-delay: 1.0s; }}
      .line-draw {{ stroke-dasharray: 90; stroke-dashoffset: 90; animation: drawL 0.6s cubic-bezier(.2,.8,.2,1) 0.6s forwards; }}
      .node-pulse {{ opacity: 0; animation: pulseNode 2.2s ease-in-out 1.2s infinite; }}
      
      @keyframes hIn {{ to {{ opacity: 1; transform: translateY(0); }} }}
      @keyframes fUp {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
      @keyframes drawL {{ to {{ stroke-dashoffset: 0; }} }}
      @keyframes pulseNode {{ 0%, 100% {{ r: 4; opacity: 0.4; }} 50% {{ r: 8; opacity: 0.9; }} }}
      
      @media (prefers-reduced-motion: reduce) {{
        .h-in, .fade-up, .line-draw, .node-pulse {{ animation: none !important; opacity: 1 !important; transform: none !important; stroke-dashoffset: 0 !important; }}
      }}
    </style>
  </defs>

  <!-- Container -->
  <rect width="{W}" height="{H}" rx="{T.RADIUS}" fill="{T.BG}"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="{T.RADIUS-0.5}" fill="none" stroke="{T.FRAME}"/>
  
  <!-- Subtle technical grid on the right -->
  <rect x="640" y="1" width="559" height="{H-2}" rx="{T.RADIUS-1}" fill="url(#headerGrid)"/>
  <rect x="540" y="1" width="380" height="{H-2}" fill="url(#headerFade)"/>

  <!-- Left Identity Block -->
  <g class="h-in">
    <!-- Main Name -->
    <text class="sans" x="54" y="98" fill="{T.BRIGHT}" font-size="52" font-weight="700" letter-spacing="-1.8">Vigneshwar Ramadoss</text>
    
    <!-- Role & Company -->
    <g class="fade-up delay-1 mono" font-size="13" letter-spacing="1.8">
      <text x="54" y="142" fill="{T.ACCENT}" font-weight="600">CO-FOUNDER @ THE DOT</text>
      <text x="315" y="142" fill="{T.DIM}">/</text>
      <text x="338" y="142" fill="{T.MUTED}">TECHNICAL FOUNDER</text>
    </g>
    
    <line class="fade-up delay-1" x1="54" y1="162" x2="520" y2="162" stroke="{T.FRAME}" stroke-opacity="0.8"/>

    <!-- Positioning Statement -->
    <text class="sans fade-up delay-2" x="54" y="206" fill="{T.INK}" font-size="18" font-weight="400">
      <tspan x="54" dy="0">Building digital systems that turn ideas into working products.</tspan>
      <tspan x="54" dy="28" fill="{T.MUTED}" font-size="15">Focusing on product engineering, automation and applied AI.</tspan>
    </text>

    <!-- Meta / Focus Badges (quiet style) -->
    <g class="mono fade-up delay-3" font-size="11.5" letter-spacing="1.1">
      <text x="54" y="300" fill="{T.MUTED}">FOCUS</text>
      <circle cx="116" cy="296" r="2" fill="{T.DIM}"/>
      <text x="130" y="300" fill="{T.INK}">PRODUCT DEV</text>
      <circle cx="258" cy="296" r="2" fill="{T.DIM}"/>
      <text x="272" y="300" fill="{T.INK}">DIGITAL TRANSFORMATION</text>
      <circle cx="498" cy="296" r="2" fill="{T.DIM}"/>
      <text x="512" y="300" fill="{T.INK}">APPLIED AI</text>
    </g>

    <!-- Terminal Status Tag -->
    <g class="mono fade-up delay-4" font-size="11">
      <rect x="54" y="324" width="220" height="26" rx="5" fill="{T.PANEL}" stroke="{T.RULE}"/>
      <circle cx="70" cy="337" r="3.5" fill="{T.OK}"/>
      <text x="82" y="341" fill="{T.MUTED}">STATUS <tspan fill="{T.BRIGHT}">SHIPPING &amp; ACTIVE</tspan></text>
    </g>
  </g>

  <!-- Right Workflow Block: Problem -> System -> Build -> Ship -->
  <g class="fade-up delay-2">
    <!-- Header info in right corner -->
    <text class="mono" x="720" y="64" fill="{T.DIM}" font-size="11" letter-spacing="1.6">ENGINEERING SYSTEM / 01</text>
    <text class="mono" x="1130" y="64" fill="{T.DIM}" font-size="11" text-anchor="end">SYS: PROD</text>
    <line x1="720" y1="78" x2="1130" y2="78" stroke="{T.RULE}"/>

    <!-- Workflow connector lines -->
    <line class="line-draw" x1="772" y1="185" x2="862" y2="185" stroke="{T.FRAME}" stroke-width="1.5"/>
    <line class="line-draw" x1="886" y1="185" x2="976" y2="185" stroke="{T.ACCENT}" stroke-width="1.5"/>
    <line class="line-draw" x1="1000" y1="185" x2="1080" y2="185" stroke="{T.FRAME}" stroke-width="1.5"/>

    <!-- 01 PROBLEM -->
    <g class="node">
      <circle cx="750" cy="185" r="22" fill="{T.PANEL}" stroke="{T.FRAME}" stroke-width="1.2"/>
      <circle cx="750" cy="185" r="4" fill="{T.MUTED}"/>
      <text class="mono" x="750" y="228" fill="{T.DIM}" font-size="10" text-anchor="middle">01</text>
      <text class="mono" x="750" y="246" fill="{T.MUTED}" font-size="11" font-weight="600" letter-spacing="1.2" text-anchor="middle">PROBLEM</text>
    </g>

    <!-- 02 SYSTEM -->
    <g class="node">
      <circle cx="874" cy="185" r="22" fill="{T.PANEL}" stroke="{T.FRAME}" stroke-width="1.2"/>
      <circle cx="874" cy="185" r="4" fill="{T.MUTED}"/>
      <text class="mono" x="874" y="228" fill="{T.DIM}" font-size="10" text-anchor="middle">02</text>
      <text class="mono" x="874" y="246" fill="{T.MUTED}" font-size="11" font-weight="600" letter-spacing="1.2" text-anchor="middle">SYSTEM</text>
    </g>

    <!-- 03 BUILD (Primary Active Stage) -->
    <g class="node">
      <circle cx="988" cy="185" r="24" fill="{T.PANEL}" stroke="{T.ACCENT}" stroke-width="1.8"/>
      <circle cx="988" cy="185" r="4.5" fill="{T.ACCENT}"/>
      <circle class="node-pulse" cx="988" cy="185" r="4.5" fill="none" stroke="{T.ACCENT}" stroke-width="1.5"/>
      <text class="mono" x="988" y="228" fill="{T.ACCENT}" font-size="10" font-weight="600" text-anchor="middle">03</text>
      <text class="mono" x="988" y="246" fill="{T.BRIGHT}" font-size="11" font-weight="600" letter-spacing="1.2" text-anchor="middle">BUILD</text>
    </g>

    <!-- 04 SHIP -->
    <g class="node">
      <circle cx="1102" cy="185" r="22" fill="{T.PANEL}" stroke="{T.FRAME}" stroke-width="1.2"/>
      <circle cx="1102" cy="185" r="4" fill="{T.MUTED}"/>
      <text class="mono" x="1102" y="228" fill="{T.DIM}" font-size="10" text-anchor="middle">04</text>
      <text class="mono" x="1102" y="246" fill="{T.MUTED}" font-size="11" font-weight="600" letter-spacing="1.2" text-anchor="middle">SHIP</text>
    </g>

    <!-- Workflow Execution Bar -->
    <g class="mono" font-size="11">
      <rect x="720" y="294" width="410" height="36" rx="6" fill="{T.PANEL}" stroke="{T.RULE}"/>
      <text x="742" y="316" fill="{T.MUTED}">SYSTEM</text>
      <text x="806" y="316" fill="{T.ACCENT}">EXECUTION</text>
      <text x="906" y="316" fill="{T.DIM}">|</text>
      <text x="926" y="316" fill="{T.INK}">END-TO-END DELIVERY</text>
      <text x="1112" y="316" fill="{T.DIM}" text-anchor="end">LIVE</text>
    </g>
  </g>
</svg>"""
    return svg

if __name__ == "__main__":
    svg = generate_header()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg):,} bytes)")
