#!/usr/bin/env python3
"""
Generate the responsive header SVG (header.svg).

Vercel/Linear-inspired aesthetic.
Focuses on strict composition, hierarchy, and whitespace.
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
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{T.BRIGHT}" stroke-opacity="0.03" stroke-width="1"/>
      <circle cx="40" cy="40" r="1.5" fill="{T.BRIGHT}" fill-opacity="0.05"/>
    </pattern>
    
    <linearGradient id="gridFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{T.BG}" stop-opacity="1"/>
      <stop offset="0.3" stop-color="{T.BG}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{T.BG}" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="glow" cx="85%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{T.ACCENT}" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="{T.BG}" stop-opacity="0"/>
    </radialGradient>

    <style>
      .sans {{ font-family: {T.SANS}; }}
      .mono {{ font-family: {T.MONO}; }}
      
      .fade-up {{ opacity: 0; animation: fUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
      .fade-in {{ opacity: 0; animation: fIn 1.2s ease-out forwards; }}
      .line-draw {{ stroke-dasharray: 200; stroke-dashoffset: 200; animation: drawL 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
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
      @keyframes pNode {{ 0%, 100% {{ opacity: 0.4; stroke-width: 1; }} 50% {{ opacity: 1; stroke-width: 1.5; }} }}
      @keyframes stream {{ to {{ stroke-dashoffset: -200; }} }}
      
      @media (prefers-reduced-motion: reduce) {{
        .fade-up, .fade-in, .line-draw, .pulse, .data-stream {{ animation: none !important; opacity: 1 !important; transform: none !important; stroke-dashoffset: 0 !important; }}
      }}
    </style>
  </defs>

  <!-- Base layer -->
  <rect width="{W}" height="{H}" fill="{T.BG}"/>
  
  <!-- Right-side Grid & Glow -->
  <rect x="500" y="0" width="700" height="{H}" fill="url(#grid)"/>
  <rect x="500" y="0" width="700" height="{H}" fill="url(#gridFade)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  
  <!-- Faint Border -->
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{T.RADIUS}" fill="none" stroke="{T.BRIGHT}" stroke-opacity="0.04"/>

  <!-- ==========================================
       LEFT SIDE: IDENTITY (55%)
       ========================================== -->
       
  <!-- Metadata Top -->
  <g class="mono fade-in d-1" font-size="11" letter-spacing="2">
    <text x="80" y="64" fill="{T.MUTED}">ID /</text>
    <text x="120" y="64" fill="{T.INK}">VIGNESHWAR_RAMADOSS</text>
  </g>

  <g class="fade-up d-1">
    <!-- Name -->
    <text class="sans" x="80" y="126" fill="{T.BRIGHT}" font-size="52" font-weight="600" letter-spacing="-1.2">Vigneshwar Ramadoss</text>
    
    <!-- Role -->
    <text class="mono" x="80" y="166" fill="{T.ACCENT}" font-size="12" font-weight="600" letter-spacing="1.5">CO-FOUNDER @ THE DOT</text>

    <!-- Positioning -->
    <text class="sans" x="80" y="222" fill="{T.BRIGHT}" font-size="18" font-weight="400" letter-spacing="-0.1">
      <tspan x="80" dy="0">Turning business problems into products, systems</tspan>
      <tspan x="80" dy="28" fill="{T.INK}">and high-performance digital experiences.</tspan>
    </text>

    <!-- Focus -->
    <g class="mono" font-size="11.5" letter-spacing="1.2">
      <text x="80" y="294" fill="{T.MUTED}">FOCUS /</text>
      <text x="144" y="294" fill="{T.INK}">PRODUCT DEV</text>
      <text x="240" y="294" fill="{T.MUTED}">·</text>
      <text x="256" y="294" fill="{T.INK}">DIGITAL TRANSFORMATION</text>
      <text x="448" y="294" fill="{T.MUTED}">·</text>
      <text x="464" y="294" fill="{T.INK}">APPLIED AI</text>
    </g>
  </g>

  <!-- Status Bottom -->
  <g class="mono fade-in d-2" font-size="11" letter-spacing="1.5">
    <circle cx="84" cy="344" r="3.5" fill="{T.ACCENT}"/>
    <circle class="pulse d-2" cx="84" cy="344" r="5" fill="none" stroke="{T.ACCENT}"/>
    <text x="100" y="348" fill="{T.MUTED}">STATUS:</text>
    <text x="160" y="348" fill="{T.BRIGHT}" font-weight="600">SYSTEM ONLINE</text>
  </g>


  <!-- ==========================================
       RIGHT SIDE: SYSTEM VISUALIZATION (45%)
       ========================================== -->
       
  <g class="fade-up d-3" transform="translate(850, 0)">
    
    <!-- Metadata Top Right -->
    <g class="mono" font-size="11" letter-spacing="2" text-anchor="middle">
      <text x="50" y="64" fill="{T.MUTED}">SYSTEM ARCHITECTURE</text>
    </g>

    <!-- Vertical Lines -->
    <g fill="none" stroke="{T.FRAME}" stroke-width="1.5">
      <path class="line-draw d-3" d="M 50 118 L 50 152"/>
      <path class="line-draw d-4" d="M 50 178 L 50 212"/>
      <path class="line-draw d-5" d="M 50 238 L 50 272"/>
    </g>
    
    <!-- Animated Data Flow -->
    <path class="data-stream" d="M 50 100 L 50 300" fill="none" stroke="{T.ACCENT}" stroke-width="1.5" stroke-opacity="0.3"/>

    <!-- 01 PROBLEM -->
    <g transform="translate(50, 106)">
      <!-- Box/Node container -->
      <rect x="-80" y="-12" width="160" height="24" rx="4" fill="{T.BG}" stroke="{T.FRAME}" stroke-width="1"/>
      <g class="mono" font-size="11" letter-spacing="1.5" text-anchor="middle">
        <text x="-32" y="4" fill="{T.MUTED}">01</text>
        <text x="16" y="4" fill="{T.INK}" font-weight="600">PROBLEM</text>
      </g>
    </g>

    <!-- Down Arrow 1 -->
    <path class="fade-in d-4" d="M 46 148 L 50 153 L 54 148" fill="none" stroke="{T.MUTED}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 02 SYSTEM -->
    <g transform="translate(50, 166)">
      <rect x="-80" y="-12" width="160" height="24" rx="4" fill="{T.BG}" stroke="{T.FRAME}" stroke-width="1"/>
      <g class="mono" font-size="11" letter-spacing="1.5" text-anchor="middle">
        <text x="-32" y="4" fill="{T.MUTED}">02</text>
        <text x="16" y="4" fill="{T.INK}" font-weight="600">SYSTEM</text>
      </g>
    </g>

    <!-- Down Arrow 2 -->
    <path class="fade-in d-5" d="M 46 208 L 50 213 L 54 208" fill="none" stroke="{T.MUTED}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 03 BUILD (Active) -->
    <g transform="translate(50, 226)">
      <!-- Active Glow -->
      <rect x="-80" y="-12" width="160" height="24" rx="4" fill="{T.ACCENT}" fill-opacity="0.08"/>
      <rect x="-80" y="-12" width="160" height="24" rx="4" fill="none" stroke="{T.ACCENT}" stroke-width="1.5"/>
      <g class="mono" font-size="11" letter-spacing="1.5" text-anchor="middle">
        <text x="-32" y="4" fill="{T.ACCENT}">03</text>
        <text x="16" y="4" fill="{T.BRIGHT}" font-weight="700">BUILD</text>
      </g>
      <!-- Pulse dot indicator on the side -->
      <circle cx="-68" cy="0" r="3" fill="{T.ACCENT}"/>
      <circle class="pulse d-5" cx="-68" cy="0" r="4.5" fill="none" stroke="{T.ACCENT}"/>
    </g>

    <!-- Down Arrow 3 -->
    <path class="fade-in d-5" d="M 46 268 L 50 273 L 54 268" fill="none" stroke="{T.MUTED}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 04 SHIP -->
    <g transform="translate(50, 286)">
      <rect x="-80" y="-12" width="160" height="24" rx="4" fill="{T.BG}" stroke="{T.FRAME}" stroke-width="1"/>
      <g class="mono" font-size="11" letter-spacing="1.5" text-anchor="middle">
        <text x="-32" y="4" fill="{T.MUTED}">04</text>
        <text x="16" y="4" fill="{T.INK}" font-weight="600">SHIP</text>
      </g>
    </g>

  </g>
  
</svg>"""
    return svg

if __name__ == "__main__":
    svg = generate_header()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg):,} bytes)")
