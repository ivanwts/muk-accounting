"""Brand assets from the real logo (images/logo-source.png): mark, wordmark, favicons, touch icon, og.jpg. Run: python3 tools/make_brand_assets.py (needs Pillow)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import make_assets as m
from PIL import Image, ImageDraw, ImageFilter, ImageOps

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{REPO}/images/logo-source.png"
INK = (22, 32, 28)        # site text colour, close to the logo's charcoal
GREEN, WHITE, CLAY, MUTED, LINE = m.GREEN, m.WHITE, m.CLAY, m.MUTED, m.LINE

src = Image.open(SRC).convert("L")
W0, H0 = src.size
print("source", src.size)

def band_boxes(g, gap=8):
    w, h = g.size; px = g.load()
    rows = [y for y in range(h) if any(px[x, y] < 128 for x in range(w))]
    bands = []
    for y in rows:
        if bands and y - bands[-1][1] <= gap: bands[-1][1] = y
        else: bands.append([y, y])
    out = []
    for y0, y1 in bands:
        cols = [x for x in range(w) if any(px[x, y] < 128 for y in range(y0, y1 + 1))]
        out.append((min(cols), y0, max(cols) + 1, y1 + 1))
    return out

boxes = band_boxes(src)
assert len(boxes) == 2, boxes
mark_box, word_box = boxes
print("mark", mark_box, "wordmark", word_box)

def alpha_of(region, scale=2, pad=0, dilate=0):
    """Luminance -> alpha (ink on white), upscaled, optionally thickened; returns an 'L' mask."""
    g = src.crop(region)
    g = ImageOps.invert(g)                          # ink -> bright
    if scale != 1:
        g = g.resize((g.width * scale, g.height * scale), Image.LANCZOS)
    # firm up the edges a little so upscaled lines stay crisp
    g = g.point(lambda v: 0 if v < 40 else (255 if v > 215 else int((v - 40) * 255 / 175)))
    if dilate:
        g = g.filter(ImageFilter.MaxFilter(dilate))
    if pad:
        g = ImageOps.expand(g, pad, fill=0)
    return g

def coloured(mask, rgb):
    out = Image.new("RGBA", mask.size, rgb + (0,))
    out.putalpha(mask)
    return out

# --- mark + wordmark for the pages (transparent PNG, ink colour)
mark_mask = alpha_of(mark_box, scale=3, pad=12)
coloured(mark_mask, INK).save(f"{REPO}/images/logo-mark.png", optimize=True)
# the wordmark in the source reads "M.U.K ACCOUNTING"; the brand is written "M.U.K." — add the dot after K
def wordmark_band():
    g = src.crop(word_box)
    cols = [x for x in range(g.width) if any(g.getpixel((x, y)) < 128 for y in range(g.height))]
    glyphs = []
    for x in cols:
        if glyphs and x - glyphs[-1][1] <= 2: glyphs[-1][1] = x
        else: glyphs.append([x, x])
    # glyphs: M . U . K  A C C O U N T I N G  → dot = glyphs[3], K = glyphs[4], A = glyphs[5]
    dot, k, a = glyphs[3], glyphs[4], glyphs[5]
    gap = dot[0] - glyphs[2][1] - 1                     # letter-to-dot gap, as between U and its dot
    word_gap = a[0] - k[1] - 1                          # the word space before ACCOUNTING
    new_dot_x = k[1] + 1 + gap
    shift = (new_dot_x + (dot[1] - dot[0] + 1) + word_gap) - a[0]
    band = Image.new("L", (g.width + shift, g.height), 255)
    band.paste(g.crop((0, 0, k[1] + 1, g.height)), (0, 0))
    band.paste(g.crop((dot[0], 0, dot[1] + 1, g.height)), (new_dot_x, 0))
    band.paste(g.crop((a[0], 0, g.width, g.height)), (a[0] + shift, 0))
    return band

def alpha_of_image(g, scale=2, pad=6):
    g = ImageOps.invert(g).resize((g.width * scale, g.height * scale), Image.LANCZOS)
    g = g.point(lambda v: 0 if v < 40 else (255 if v > 215 else int((v - 40) * 255 / 175)))
    return ImageOps.expand(g, pad, fill=0)

word_mask = alpha_of_image(wordmark_band())
coloured(word_mask, INK).save(f"{REPO}/images/logo-wordmark.png", optimize=True)
print("logo-mark", mark_mask.size, "logo-wordmark", word_mask.size)

# --- icons: white monogram on the green rounded square
def icon(size, bleed=False, dilate=0):
    ss = 4
    S = size * ss
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if bleed: d.rectangle((0, 0, S - 1, S - 1), fill=GREEN + (255,))
    else: d.rounded_rectangle((0, 0, S - 1, S - 1), radius=round(14 / 64 * S), fill=GREEN + (255,))
    inner = int(S * 0.62)
    mk = alpha_of(mark_box, scale=3, dilate=dilate)
    mk = ImageOps.contain(mk, (inner, inner), Image.LANCZOS)
    glyph = coloured(mk, WHITE)
    layer.alpha_composite(glyph, ((S - mk.width) // 2, (S - mk.height) // 2))
    return layer.resize((size, size), Image.LANCZOS)

icon(32, dilate=5).save(f"{REPO}/images/favicon-32.png", optimize=True)
icon(192, dilate=3).save(f"{REPO}/images/favicon-192.png", optimize=True)
icon(48, dilate=5).save(f"{REPO}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
icon(180, bleed=True, dilate=3).convert("RGB").save(f"{REPO}/images/apple-touch-icon.png", optimize=True)

# --- og.jpg: monogram on the cream card, text on the right (same layout as before)
def make_og(path):
    W, H = m.W, m.H
    canvas = Image.new("RGB", (W, H), m.CREAM)
    canvas = m.radial_glow(canvas, (int(W * 0.88), int(H * 0.18)), (560, 470), m.BLUSH, 0.68)
    canvas = m.radial_glow(canvas, (int(-0.06 * W), H), (520, 420), m.SAGE, 0.70)
    canvas = canvas.convert("RGBA")

    # white rounded card with the monogram
    D, PCX, PCY = 340, 278, 315
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((PCX - D // 2 + 8, PCY - D // 2 + 30, PCX + D // 2 - 8, PCY + D // 2 + 30), radius=48, fill=m.INK + (70,))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    canvas = Image.alpha_composite(canvas, shadow)
    card = Image.new("RGBA", (D * 4, D * 4), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, D * 4 - 1, D * 4 - 1), radius=48 * 4, fill=WHITE + (255,))
    card = card.resize((D, D), Image.LANCZOS)
    canvas.alpha_composite(card, (PCX - D // 2, PCY - D // 2))
    mk = ImageOps.contain(alpha_of(mark_box, scale=3), (int(D * 0.64), int(D * 0.64)), Image.LANCZOS)
    canvas.alpha_composite(coloured(mk, INK), (PCX - mk.width // 2, PCY - mk.height // 2))

    draw = ImageDraw.Draw(canvas)
    X0, XMAX = 556, 1152
    COLW = XMAX - X0
    label = "CERTIFIED PUBLIC ACCOUNTANT · KENT, WA"
    for size in (19, 18, 17, 16):
        label_font = m.manrope(size, 700)
        if sum(label_font.getlength(c) for c in label) + 2.4 * (len(label) - 1) <= COLW: break
    m.draw_tracked(draw, (X0, 122), label, label_font, GREEN, 2.4)
    head_font, head_size = m.fit(lambda s: m.manrope(s, 800), "Accounting", 84, 56, COLW)
    draw.text((X0, 226), "M.U.K.", font=head_font, fill=GREEN, anchor="ls")
    draw.text((X0, 226 + head_size), "Accounting", font=head_font, fill=GREEN, anchor="ls")
    accent = "Taxes & bookkeeping in the U.S."
    accent_font, _ = m.fit(lambda s: m.playfair_italic(s, 600), accent, 38, 28, COLW)
    draw.text((X0, 368), accent, font=accent_font, fill=CLAY, anchor="ls")
    ru = "Бухгалтерия и налоги в США · говорим по-русски"
    ru_font, _ = m.fit(lambda s: m.manrope(s, 500), ru, 26, 20, COLW)
    draw.text((X0, 408), ru, font=ru_font, fill=MUTED, anchor="ls")
    foot_base = PCY + 220
    draw.line((X0, foot_base - 100, XMAX, foot_base - 100), fill=LINE, width=2)
    phone, phone_font = "+1 (564) 999-0089", m.manrope(32, 800)
    draw.text((X0, foot_base - 50), phone, font=phone_font, fill=GREEN, anchor="ls")
    draw.text((X0 + phone_font.getlength(phone) + 16, foot_base - 50), "call or text", font=m.manrope(20, 500), fill=MUTED, anchor="ls")
    f_strong, f_soft = m.manrope(21, 700), m.manrope(21, 500)
    draw.text((X0, foot_base), "mukaccounting.net", font=f_strong, fill=GREEN, anchor="ls")
    draw.text((X0 + f_strong.getlength("mukaccounting.net"), foot_base), "  ·  Kent, WA  ·  online nationwide", font=f_soft, fill=MUTED, anchor="ls")

    out = canvas.convert("RGB")
    for q in (88, 85, 82, 78):
        out.save(path, "JPEG", quality=q, optimize=True, subsampling=0)
        if os.path.getsize(path) < 290_000: break
    print("og.jpg", out.size, os.path.getsize(path), "bytes")

make_og(f"{REPO}/images/og.jpg")
for f in ["images/logo-mark.png", "images/logo-wordmark.png", "images/favicon-32.png", "images/favicon-192.png", "favicon.ico", "images/apple-touch-icon.png"]:
    print(f, os.path.getsize(f"{REPO}/{f}"), "bytes")
