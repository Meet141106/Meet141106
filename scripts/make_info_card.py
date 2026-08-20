#!/usr/bin/env python3
from pathlib import Path

OUT = Path("info-card.svg")

ROWS = [
    ("ROLE", "Full-Stack Developer"),
    ("EDU", "B.Tech IT · DJSCE"),
    ("STACK", "React · Node · Python · Flutter"),
    ("DATA", "Supabase · PostgreSQL · MongoDB"),
    ("FOCUS", "AI/ML · FinTech · Blockchain"),
    ("BUILD", "TrustLend · FairSplit · Communica"),
    ("STATUS", "always learning, usually shipping"),
]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def main():
    lines = []
    for i, (key, value) in enumerate(ROWS):
        y = 90 + i * 43
        delay = 0.12 + i * 0.10
        lines.append(f'''<g style="--d:{delay:.2f}s"><text x="28" y="{y}" fill="#69f0a0" font-size="12">{esc(key):<6}</text><text x="112" y="{y}" fill="#c9d1d9" font-size="12">{esc(value)}</text></g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="430" height="460" viewBox="0 0 430 460">
<defs><style>@keyframes lineIn{{from{{opacity:0;transform:translateX(-10px)}}to{{opacity:1;transform:translateX(0)}}}}g{{animation:lineIn .45s ease-out var(--d) both}}text{{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}}</style></defs>
<rect width="430" height="460" rx="12" fill="#0d1117" stroke="#30363d"/>
<rect x="1" y="1" width="428" height="36" rx="11" fill="#161b22"/>
<circle cx="18" cy="19" r="5" fill="#ff6b6b"/><circle cx="34" cy="19" r="5" fill="#ffd166"/><circle cx="50" cy="19" r="5" fill="#69f0a0"/>
<text x="72" y="23" fill="#8b949e" font-size="11">meet@github:~</text>
<text x="28" y="64" fill="#f0f6fc" font-size="18">Meet Patel</text>
<text x="28" y="82" fill="#6e7681" font-size="10">$ neofetch --profile</text>
{''.join(lines)}
<g style="--d:0.85s">
  <text x="28" y="385" fill="#6e7681" font-size="10">$ systemctl status meet.service</text>
</g>
<g style="--d:0.95s">
  <text x="28" y="403" fill="#69f0a0" font-size="10">●</text>
  <text x="42" y="403" fill="#c9d1d9" font-size="10">meet.service - Developer Daemon (Active: running)</text>
</g>
<g style="--d:1.05s">
  <text x="28" y="419" fill="#8b949e" font-size="10">  uptime: 4y 11m 6d | tasks: 200 ok | load: 0.05</text>
</g>
<g style="--d:1.15s">
  <text x="28" y="435" fill="#8b949e" font-size="10">  processes: api [ok] · db [ok] · app [deploying...]</text>
</g>
</svg>'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
