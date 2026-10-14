"""Shared helpers for the brand-asset generator (fonts, glows, tracked text, text fitting).
Run make_brand_assets.py, not this file."""
import math
import os

from PIL import Image, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = f"{HERE}/fonts"   # Manrope + Playfair Display Italic (variable TTFs from google/fonts, OFL)

W, H = 1200, 630
CREAM = (250, 247, 242)   # #faf7f2
BLUSH = (243, 217, 204)   # #f3d9cc
SAGE = (227, 237, 231)    # #e3ede7
GREEN = (15, 61, 51)      # #0f3d33
CLAY = (200, 103, 75)     # #c8674b
MUTED = (91, 102, 97)     # #5b6661
LINE = (228, 221, 208)    # #e4ddd0
INK = (22, 32, 28)        # #16201c
WHITE = (255, 255, 255)


def manrope(size, weight):
    f = ImageFont.truetype(f"{FONTS}/Manrope-wght.ttf", size)
    f.set_variation_by_axes([weight])
    return f


def playfair_italic(size, weight):
    f = ImageFont.truetype(f"{FONTS}/PlayfairDisplay-Italic-wght.ttf", size)
    f.set_variation_by_axes([weight])
    return f


def radial_glow(base, center, radii, color, stop, scale=2):
    """CSS-like radial-gradient(rx ry at cx cy, color, transparent stop) composited onto base."""
    cx, cy = center
    rx, ry = radii
    w, h = base.size
    sw, sh = w // scale, h // scale
    buf = bytearray(sw * sh)
    i = 0
    for y in range(sh):
        dy = ((y + 0.5) * scale - cy) / ry
        dy2 = dy * dy
        for x in range(sw):
            dx = ((x + 0.5) * scale - cx) / rx
            a = 1.0 - math.sqrt(dx * dx + dy2) / stop
            buf[i] = int(a * 255 + 0.5) if a > 0 else 0
            i += 1
    mask = Image.frombytes("L", (sw, sh), bytes(buf)).resize((w, h), Image.BICUBIC)
    return Image.composite(Image.new("RGB", (w, h), color), base, mask)


def draw_tracked(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += font.getlength(ch) + tracking
    return x


def fit(maker, text, max_size, min_size, max_width):
    for s in range(max_size, min_size - 1, -1):
        f = maker(s)
        if f.getlength(text) <= max_width:
            return f, s
    return maker(min_size), min_size
