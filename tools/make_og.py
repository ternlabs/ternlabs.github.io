"""Render site/assets/og.png (1200x630), the link-preview image.

Usage: python3 tools/make_og.py <logo-reversed.png> [tagline]
The logo PNG comes from the brand kit (png/ternlabs-logo-reversed.png);
the font is the one the site serves.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "site/assets/fonts/SpaceGrotesk.ttf"
OUT = ROOT / "site/assets/og.png"
INK, SHOOT = (0x1E, 0x3A, 0x2A), (0x8C, 0xC0, 0x63)
W, H, SS = 1200, 630, 2

logo_png = sys.argv[1]
tag = sys.argv[2] if len(sys.argv) > 2 else "Robots over private 5G  ·  Edge AI  ·  Vietnamese OCR"

bg = Image.new("RGBA", (W * SS, H * SS), INK + (255,))
rings = Image.new("RGBA", bg.size, (0, 0, 0, 0))
d = ImageDraw.Draw(rings)
cx, cy = 1010 * SS, 315 * SS
for i, r in enumerate(range(40, 900, 34)):
    rr = r * SS
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=SHOOT + (max(14, 60 - i * 2),), width=2 * SS)
bg = Image.alpha_composite(bg, rings).resize((W, H), Image.LANCZOS)

logo = Image.open(logo_png).convert("RGBA")
logo = logo.crop(logo.getchannel("A").getbbox())
lw = 620
logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)

font = ImageFont.truetype(str(FONT), 30)
try:
    font.set_variation_by_name("Regular")
except Exception:
    pass
draw = ImageDraw.Draw(bg)
tb = draw.textbbox((0, 0), tag, font=font)
tw, th = tb[2] - tb[0], tb[3] - tb[1]
gap = 36
y0 = (H - (logo.height + gap + th)) // 2
bg.alpha_composite(logo, ((W - lw) // 2, y0))
draw.text(((W - tw) // 2 - tb[0], y0 + logo.height + gap - tb[1]), tag, font=font, fill=SHOOT)
bg.convert("RGB").save(OUT, optimize=True)
print(f"wrote {OUT}")
