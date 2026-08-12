#!/usr/bin/env python3
import json
import math
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP = 12, 3
LEFT, TOP = 26, 28
WEEKS = 53
WIDTH = LEFT + WEEKS * (CELL + GAP) + 26
HEIGHT = 7 * (CELL + GAP) + TOP + 54


def main():
    payload = json.loads(DATA.read_text())
    days = payload["days"]
    stats = payload["stats"]
    by_date = {d["date"]: d for d in days}
    dates = sorted(by_date)
    if not dates:
        raise RuntimeError("No contribution data")
    start = __import__("datetime").date.fromisoformat(dates[0])
    # align first column to Sunday
    start = start.fromordinal(start.toordinal() - ((start.weekday() + 1) % 7))

    rects = []
    for i in range(WEEKS * 7):
        day = start.fromordinal(start.toordinal() + i)
        d = by_date.get(day.isoformat(), {"level": 0})
        week = i // 7
        dow = (day.weekday() + 1) % 7
        x = LEFT + week * (CELL + GAP)
        y = TOP + dow * (CELL + GAP)
        delay = (week * 0.035 + dow * 0.012)
        rects.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[min(5, int(d.get("level", 0)))]}" style="--d:{delay:.3f}s"/>')

    total = stats["total"]
    current = stats["current_streak"]
    active = stats["active_days"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<defs><style>
@keyframes reveal {{from{{opacity:0;transform:translateY(-7px)}}to{{opacity:1;transform:translateY(0)}}}}
rect {{animation:reveal .45s ease-out var(--d) both}}
text {{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}}
</style></defs>
<rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d"/>
<text x="{LEFT}" y="17" fill="#8b949e" font-size="10">LESS</text>
<text x="{WIDTH-52}" y="17" fill="#8b949e" font-size="10">MORE</text>
{''.join(rects)}
<text x="{LEFT}" y="{HEIGHT-29}" fill="#c9d1d9" font-size="10">{total:,} contributions · {active} active days · {current} day current streak</text>
<text x="{LEFT}" y="{HEIGHT-13}" fill="#6e7681" font-size="9">Meet141106 · refreshed automatically</text>
</svg>'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
