#!/usr/bin/env python3
"""
Master build script for Vigneshwar's GitHub Profile README assets.

Generates:
  1. header.svg           (Technical Founder hero with Problem -> System -> Build -> Ship)
  2. vignesh-ascii.svg    (Animated SMIL ASCII portrait, 840x900)
  3. info-card.svg        (Terminal info & focus tree card, 840x900)
  4. data/contributions.json (Scraped public contributions & profile facts)
  5. contrib-heatmap.svg  (53-week animated blue-gradient heatmap with signals)

Usage:
    python scripts/build_all.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

def run(cmd, desc):
    print(f"==> {desc}...")
    res = subprocess.run([sys.executable] + cmd, cwd=ROOT)
    if res.returncode != 0:
        print(f"Error running {' '.join(cmd)}", file=sys.stderr)
        sys.exit(res.returncode)

def main():
    print("Building all profile assets for Vigneshwar Ramadoss...")
    
    # 1. Header
    run(["scripts/make_header.py", "header.svg"], "Generating header.svg")

    # 2. ASCII Portrait (if prepped image exists)
    prepped = os.path.join(ROOT, "assets", "portrait-prepped.png")
    if os.path.exists(prepped):
        run(["scripts/make_ascii_svg.py", "assets/portrait-prepped.png", "vignesh-ascii.svg"], "Generating vignesh-ascii.svg")
    else:
        print(f"Skipping ASCII portrait (run prep_photo.py first to create {prepped})")

    # 3. Contributions JSON
    run(["scripts/fetch_contributions.py"], "Fetching latest GitHub contributions")

    # 4. Info Card
    run(["scripts/make_info_card.py", "data/contributions.json", "info-card.svg"], "Generating info-card.svg")

    # 5. Contribution Heatmap
    run(["scripts/render_heatmap_svg.py", "data/contributions.json", "contrib-heatmap.svg"], "Generating contrib-heatmap.svg")

    print("\n[OK] All assets generated successfully!")

if __name__ == "__main__":
    main()
