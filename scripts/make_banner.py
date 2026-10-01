"""プロフィール冒頭のバナー SVG (assets/banner.svg) を生成する。

星空の上を音声波形が描かれていくアニメーション。外部フォント・外部参照なし。
    python3 scripts/make_banner.py
"""
import math
import random
from pathlib import Path

W, H = 1280, 340
OUT = Path(__file__).resolve().parent.parent / "assets" / "banner.svg"
rnd = random.Random(727)

# --- 星 ---------------------------------------------------------------
stars = []
for i in range(150):
    x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.92)
    r = rnd.choice([0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.6])
    o = rnd.uniform(0.25, 0.9)
    if r >= 1.2 and rnd.random() < 0.7:
        dur, delay = rnd.uniform(2.5, 6.0), rnd.uniform(0, 5)
        stars.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" opacity="{o:.2f}">'
            f'<animate attributeName="opacity" values="{o:.2f};0.15;{o:.2f}" '
            f'dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/></circle>'
        )
    else:
        stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" opacity="{o:.2f}"/>')

# --- 波形(演奏会の録音のように、静かな区間と盛り上がる区間が交互に来る) -----
def envelope(t):
    return (0.18 + 0.82 * (0.5 + 0.5 * math.sin(t * 2 * math.pi * 2.3 - 1.2)) ** 2) * (
        0.75 + 0.25 * math.sin(t * 2 * math.pi * 7.1)
    )


y0, amp, n = 268, 46, 420
top, bot = [], []
for i in range(n + 1):
    t = i / n
    x = 40 + t * (W - 80)
    a = amp * envelope(t) * (0.55 + 0.45 * rnd.random())
    top.append((x, y0 - a))
    bot.append((x, y0 + a * 0.9))
wave = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in top) + " L" + " L".join(
    f"{x:.1f},{y:.1f}" for x, y in reversed(bot)
) + " Z"
mid = "M" + " L".join(f"{x:.1f},{y0 + (yt - y0) * 0.35:.1f}" for x, yt in top)

# チャプターの区切り(縦線)
chapters = [0.40, 0.62, 0.84]
marks = "".join(
    f'<line x1="{40 + c * (W - 80):.1f}" y1="{y0 - 54}" x2="{40 + c * (W - 80):.1f}" y2="{y0 + 58}" '
    f'stroke="#f5c76b" stroke-width="1.4" stroke-dasharray="3 4"/>'
    f'<circle cx="{40 + c * (W - 80):.1f}" cy="{y0 - 58}" r="3.2" fill="#f5c76b"/>'
    for c in chapters
)

# 再生ヘッド: 左から右へ流れ続ける。アニメーション非対応なら左端に留まるだけ
playhead = (
    f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{W - 80} 0" '
    f'dur="14s" repeatCount="indefinite"/>'
    f'<rect x="{40 - 60}" y="{y0 - 60}" width="60" height="120" fill="url(#trail)"/>'
    f'<line x1="40" y1="{y0 - 60}" x2="40" y2="{y0 + 60}" stroke="#ffffff" stroke-width="2" opacity="0.9"/></g>'
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Massy — tools for media, documents and measurement">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#070b1a"/><stop offset="0.65" stop-color="#121a3a"/><stop offset="1" stop-color="#1c1340"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.72" cy="0.18" r="0.6">
    <stop offset="0" stop-color="#5b6cff" stop-opacity="0.35"/><stop offset="1" stop-color="#5b6cff" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="trail" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.18"/>
  </linearGradient>
  <linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#38d6ff"/><stop offset="0.5" stop-color="#8b7bff"/><stop offset="1" stop-color="#ff7ad9"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
{''.join(stars)}
<g>
  <path d="{wave}" fill="url(#wave)" opacity="0.42"/>
  <path d="{mid}" fill="none" stroke="url(#wave)" stroke-width="1.8" opacity="1"/>
</g>
{marks}
{playhead}
<g font-family="'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif" fill="#f4f1ff">
  <text x="64" y="128" font-size="88" letter-spacing="2">Massy</text>
</g>
<g font-family="-apple-system,'Segoe UI',Helvetica,Arial,sans-serif" fill="#b9c0e8">
  <text x="68" y="168" font-size="21" letter-spacing="0.5">Tools that finish the work where it starts.</text>
  <text x="68" y="198" font-size="14" letter-spacing="3.2" fill="#7f88b8">MEDIA · DOCUMENTS · MEASUREMENT</text>
</g>
</svg>
'''
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(svg, encoding="utf-8")
print("wrote", OUT, len(svg), "bytes")
