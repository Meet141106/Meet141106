#!/usr/bin/env python3
"""Convert data/source-prepped.png into a self-revealing monochrome SVG."""
from pathlib import Path
import sys

from PIL import Image
import numpy as np

RAMP = " .`:-=+*cs#%@"
OUT = Path("avi-ascii.svg")


def main():
    src = Path("data/source-prepped.png")
    if not src.exists():
        raise SystemExit("Missing data/source-prepped.png. Run prep_photo.py first.")
    cols = int(sys.argv[1]) if len(sys.argv) > 1 else 70
    rows = int(sys.argv[2]) if len(sys.argv) > 2 else 46
    image = Image.open(src).convert("L").resize((cols, rows), Image.Resampling.LANCZOS)
    pixels = np.asarray(image)
    lines = []
    for row in pixels:
        line = "".join(RAMP[min(len(RAMP)-1, int(v / 256 * len(RAMP)))] for v in row).rstrip()
        lines.append(line)

    svg_lines = []
    for i, line in enumerate(lines):
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_lines.append(f'<text class="row" style="--d:{i*0.03:.2f}s" x="22" y="{42+i*10}">{safe}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="430" height="520" viewBox="0 0 430 520">
<defs><style>@keyframes rowIn{{from{{opacity:0;transform:translateX(-14px)}}to{{opacity:1;transform:translateX(0)}}}}text{{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:7px;letter-spacing:.2px;fill:#b1bac4}}.row{{animation:rowIn .28s ease-out var(--d) both}}</style></defs>
<rect width="430" height="520" rx="12" fill="#0d1117" stroke="#30363d"/>
<text x="20" y="22" fill="#69f0a0" font-size="11">meet@github:~$ portrait --animate</text>
{''.join(svg_lines)}
<text x="22" y="505" fill="#6e7681" font-size="9">monochrome ASCII · one-shot reveal</text>
</svg>'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
