"""Cover pipeline for the US series «Agent Dibs»: code-rendered reference frame -> xAI edit (grok-imagine-image-2.0, medium, 1k)
-> pixelize 540x960 / 110 colours -> Chicago-flag plaque (white field, two sky-blue stripes, four red six-pointed stars)
+ BIG italic title: ice-white -> cyan stepped gradient, Chicago-red outline, navy offset shadow, a few icicles.
Family: US channel (neon / night), series look: icy blue + Chicago red + sodium-lamp orange (Sunny Palms is pink/aqua)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P
import xai
from covergen2 import pixelize, W, H

PROMPT_BASE = (
    "Redraw this image as a highly detailed, vivid HD pixel art scene from a modern indie pixel-art adventure game "
    "(crisp visible pixels, rich environment detail, cold deep-blue Chicago winter night, warm orange sodium streetlamp glow, falling snow). "
    "Keep the same vertical composition, the same background and exactly the same cartoon characters with their colors and outfits: ")
PROMPT_END = (" Funny, very expressive cartoon faces, faces large and clear in the middle of the image. Keep the top third of the image calm "
              "and simple (dark night sky with a few snowflakes) for a title. No text, no letters, no numbers, no watermark.")
RED, RED_DK = (226, 40, 60), (120, 12, 30)
NAVY, NAVY_SH = (16, 30, 72), (6, 12, 34)
SKY = (104, 186, 240)
FILL = ((255, 255, 255), (170, 232, 255), (70, 194, 250))


def ai(ref_png, raw_png, characters):
    return xai.generate(PROMPT_BASE + characters + PROMPT_END, [raw_png], aspect='9:16', ref_png=ref_png)


def _font(size):
    return ImageFont.truetype(P.FONT_PX, size)


def _star6(F, cx, cy, r, col):
    """red six-pointed star (two triangles) centred at (cx, cy) on the 540x960 canvas"""
    img = Image.new('L', (2 * r + 6, 2 * r + 6), 0); d = ImageDraw.Draw(img); c = r + 3
    k = 0.866
    d.polygon([(c, c - r), (c + r * k, c + r * 0.5), (c - r * k, c + r * 0.5)], fill=255)
    d.polygon([(c, c + r), (c + r * k, c - r * 0.5), (c - r * k, c - r * 0.5)], fill=255)
    m = np.array(img) > 127
    y0, x0 = cy - c, cx - c
    reg = F[y0:y0 + m.shape[0], x0:x0 + m.shape[1]]
    reg[m] = col


def flag_plank(F, text, y, size=20, gap=8):
    """Chicago-flag plaque: white field, two sky-blue stripes, 2 + 2 red stars around the text rows ('\n' = rows). Returns bottom y."""
    f = _font(size)
    rows = text.split('\n')
    bbs = [f.getbbox(r) for r in rows]
    tw = max(b[2] - b[0] for b in bbs); th = max(b[3] - b[1] for b in bbs)
    ph = th * len(rows) + gap * (len(rows) - 1) + 52
    pw = tw + 150
    x0 = (W - pw) // 2
    F[y - 6:y + ph + 6, x0 - 6:x0 + pw + 6] = NAVY_SH
    F[y - 3:y + ph + 3, x0 - 3:x0 + pw + 3] = NAVY
    F[y:y + ph, x0:x0 + pw] = (250, 252, 255)
    F[y + 6:y + 16, x0:x0 + pw] = SKY                                        # the two stripes of the Chicago flag
    F[y + ph - 16:y + ph - 6, x0:x0 + pw] = SKY
    F[y + 6:y + 8, x0:x0 + pw] = (190, 226, 250); F[y + ph - 16:y + ph - 14, x0:x0 + pw] = (190, 226, 250)
    cy = y + ph // 2
    for sx in (x0 + 30, x0 + 62, x0 + pw - 62, x0 + pw - 30):
        _star6(F, sx, cy, 11, RED)
    img = Image.new('L', (W, ph), 0)
    d = ImageDraw.Draw(img); d.fontmode = '1'
    for i, (r, bb) in enumerate(zip(rows, bbs)):
        rw = bb[2] - bb[0]
        d.text(((W - rw) // 2 - bb[0], 26 + i * (th + gap) - bb[1]), r, font=f, fill=255)
    m = np.array(img) > 127
    reg = F[y:y + ph]
    reg[np.roll(np.roll(m, 2, 0), 2, 1) & ~m] = (150, 176, 214)
    reg[m] = NAVY
    return y + ph


def _icicles(reg, dil, seed):
    """a few icicles hanging from the bottom edge of the outlined letters"""
    rng = np.random.default_rng(seed)
    edge = dil & ~np.roll(dil, -1, 0)
    cols = np.where(edge.any(0))[0]
    for x in cols[::5]:
        if rng.random() > 0.45: continue
        ys = np.where(edge[:, x])[0]
        if len(ys) == 0: continue
        y = ys[-1] + 1; ln = int(rng.integers(7, 19))
        for k in range(ln):
            w = max(1, 4 - (4 * k) // ln)
            xx0 = x - w // 2
            if y + k >= reg.shape[0] or xx0 < 0: break
            reg[y + k, xx0:xx0 + w] = (214, 242, 255) if k < ln - 3 else (255, 255, 255)
            reg[y + k, xx0] = (120, 200, 246)


def title(F, lines, top, sizes, max_w=500, gap=4, slant=0.16, icicles=True):
    """big italic title; sizes = per-line font size (auto-shrinks to fit max_w)"""
    y = top
    for li, (line, size) in enumerate(zip(lines, sizes)):
        fsz = size
        while True:
            f = _font(fsz); bb = f.getbbox(line)
            if bb[2] - bb[0] <= max_w or fsz <= 16: break
            fsz -= 4
        img = Image.new('L', (W, fsz * 2), 0)
        d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((W - (bb[2] - bb[0])) // 2 - bb[0] - 8, -bb[1] + 14), line, font=f, fill=255)
        m0 = np.array(img) > 127
        rows = np.where(m0.any(1))[0]
        if len(rows) == 0: continue
        m0 = m0[:rows[-1] + 24]
        m = np.zeros_like(m0)                                                    # italic shear: top rows lean right
        for yy in range(m0.shape[0]):
            m[yy] = np.roll(m0[yy], int((rows[-1] - yy) * slant))
        dil = m.copy()
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                if dx * dx + dy * dy <= 30: dil |= np.roll(np.roll(m, dy, 0), dx, 1)
        sh = np.roll(np.roll(dil, 6, 0), 5, 1)                                   # navy offset shadow
        reg = F[y:y + m.shape[0]]
        hh = reg.shape[0]; m, dil, sh = m[:hh], dil[:hh], sh[:hh]
        reg[sh] = NAVY_SH; reg[dil] = RED
        reg[dil & ~np.roll(dil, 3, 0)] = RED_DK                                  # darker rim on top of the outline
        r0, r1 = rows[0], rows[-1]
        for yy in range(hh):
            k = (yy - r0) / max(1, r1 - r0)
            reg[yy][m[yy]] = FILL[0] if k < 0.30 else FILL[1] if k < 0.62 else FILL[2]
        reg[m & ~np.roll(m, 4, 0)] = (255, 255, 255)
        if icicles and li == len(lines) - 1: _icicles(reg, dil, 11)
        y += (r1 - r0) + gap + 20
    return y


def make(raw_png, src_jpg, out_pngs, n, title_lines, sizes, series='AGENT DIBS', extra=None, total=6):
    Image.open(raw_png).convert('RGB').save(src_jpg, quality=93)
    F = pixelize(Image.open(src_jpg))
    for yy in range(0, 132, 4):                                                  # darken the very top slightly for text contrast
        F[yy:yy + 4] = (F[yy:yy + 4].astype(np.float32) * (0.72 + 0.28 * yy / 132)).clip(0, 255).astype(np.uint8)
    yb = flag_plank(F, f'{series}\nEPISODE {n}/{total}', 126, 20)                # just below the 3:4 grid crop line
    title(F, title_lines, yb + 20, sizes)
    if extra: extra(F)
    img = Image.fromarray(F).resize((1080, 1920), Image.NEAREST)
    for o in out_pngs: img.save(o)
    return img


def calm_night(big):
    """paint a calm dark night sky with a few chunky snowflakes over the top of a 1080x1920 reference frame (the title goes there)"""
    ys = np.arange(1920)[:, None].astype(np.float32)
    a = np.clip(1.0 - (ys - 440) / 470.0, 0, 1) ** 0.7
    sky = np.zeros((1920, 1, 3), np.float32)
    for c, (top, bot) in enumerate(((14, 52), (24, 74), (60, 128))): sky[:, 0, c] = top + (bot - top) * np.clip(ys[:, 0] / 900, 0, 1)
    big[:] = (big * (1 - a[..., None]) + sky * a[..., None]).astype(np.uint8)
    rng = np.random.default_rng(7)
    for i in range(60):
        x = int(rng.integers(0, 1068)); y = int(rng.integers(0, 760)); s = int(rng.choice((6, 9, 12)))
        big[y:y + s, x:x + s] = (240, 246, 255)
    return big
