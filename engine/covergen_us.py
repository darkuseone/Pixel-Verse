"""Cover pipeline for the US channel («Sunny Palms HOA»): code-rendered reference frame -> xAI edit (grok-imagine-image-2.0, medium, 1k)
-> pixelize 540x960 / 110 colours -> neon-motel plank + BIG neon title (white->pink stepped gradient, purple outline, aqua offset shadow).
Deliberately different from the Russian channel's yellow/orange look: brighter, bigger text, other palette."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P
import xai
from covergen2 import pixelize, W, H

PROMPT_BASE = (
    "Redraw this image as a highly detailed, vivid, saturated HD pixel art scene from a modern indie pixel-art adventure game "
    "(crisp visible pixels, rich environment detail, warm tropical Florida sunlight). Keep the same vertical composition, the same background "
    "and exactly the same cartoon characters with their colors and outfits: ")
PROMPT_END = (" Funny, very expressive cartoon faces, faces large and clear in the middle of the image. Keep the top third of the image calm "
              "and simple (sky) for a title. No text, no letters, no numbers, no watermark.")
PINK, PINK_HI, AQUA, PURPLE, PURPLE_SH = (255, 72, 176), (255, 150, 214), (0, 214, 232), (40, 10, 88), (18, 4, 44)
FILL = ((255, 255, 255), (255, 176, 236), (255, 72, 176))


def ai(ref_png, raw_png, characters):
    return xai.generate(PROMPT_BASE + characters + PROMPT_END, [raw_png], aspect='9:16', ref_png=ref_png)


def _font(size):
    return ImageFont.truetype(P.FONT_PX, size)


def neon_plank(F, text, y, size=22, gap=10):
    """motel neon sign: hot-pink plank, aqua rim, white pixel text; '\n' = rows. Returns bottom y."""
    f = _font(size)
    rows = text.split('\n')
    bbs = [f.getbbox(r) for r in rows]
    tw = max(b[2] - b[0] for b in bbs); th = max(b[3] - b[1] for b in bbs)
    pw, ph = tw + 52, th * len(rows) + gap * (len(rows) - 1) + 32
    x0 = (W - pw) // 2
    F[y - 6:y + ph + 6, x0 - 6:x0 + pw + 6] = PURPLE_SH
    F[y - 3:y + ph + 3, x0 - 3:x0 + pw + 3] = AQUA                        # aqua neon rim
    F[y:y + ph, x0:x0 + pw] = PURPLE
    F[y + 4:y + ph - 4, x0 + 4:x0 + pw - 4] = PINK
    F[y + 4:y + 8, x0 + 4:x0 + pw - 4] = PINK_HI                          # shine
    img = Image.new('L', (W, ph), 0)
    d = ImageDraw.Draw(img); d.fontmode = '1'
    for i, (r, bb) in enumerate(zip(rows, bbs)):
        rw = bb[2] - bb[0]
        d.text(((W - rw) // 2 - bb[0], 16 + i * (th + gap) - bb[1]), r, font=f, fill=255)
    m = np.array(img) > 127
    reg = F[y:y + ph]
    reg[np.roll(np.roll(m, 3, 0), 2, 1) & ~m] = PURPLE
    reg[m] = (255, 255, 255)
    return y + ph


def title(F, lines, top, sizes, max_w=528, gap=6):
    """big neon title; sizes = per-line font size (auto-shrinks to fit max_w)"""
    y = top
    for line, size in zip(lines, sizes):
        fsz = size
        while True:
            f = _font(fsz); bb = f.getbbox(line)
            if bb[2] - bb[0] <= max_w or fsz <= 16: break
            fsz -= 4
        img = Image.new('L', (W, fsz * 2), 0)
        d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], -bb[1] + 8), line, font=f, fill=255)
        m = np.array(img) > 127
        rows = np.where(m.any(1))[0]
        if len(rows) == 0: continue
        m = m[:rows[-1] + 16]
        dil = m.copy()
        for dx in range(-4, 5):
            for dy in range(-4, 5): dil |= np.roll(np.roll(m, dy, 0), dx, 1)
        sh = np.roll(np.roll(dil, 5, 0), 4, 1)                            # aqua offset shadow
        reg = F[y:y + m.shape[0]]
        hh = reg.shape[0]; m, dil, sh = m[:hh], dil[:hh], sh[:hh]
        reg[sh] = AQUA; reg[dil] = PURPLE
        r0, r1 = rows[0], rows[-1]
        for yy in range(hh):
            k = (yy - r0) / max(1, r1 - r0)
            reg[yy][m[yy]] = FILL[0] if k < 0.30 else FILL[1] if k < 0.62 else FILL[2]
        reg[m & ~np.roll(m, 4, 0)] = (255, 255, 255)
        y += (r1 - r0) + gap + 16
    return y


def make(raw_png, src_jpg, out_pngs, n, title_lines, sizes, series='SUNNY PALMS HOA', extra=None, total=6):
    Image.open(raw_png).convert('RGB').save(src_jpg, quality=93)
    F = pixelize(Image.open(src_jpg))
    for i, yy in enumerate(range(0, 130, 22)):                              # darken the very top slightly for text contrast
        F[yy:yy + 22] = (F[yy:yy + 22].astype(np.float32) * (0.70 + 0.06 * i)).clip(0, 255).astype(np.uint8)
    yb = neon_plank(F, f'{series}\nEPISODE {n}/{total}', 128, 22)            # just below the 3:4 grid crop line
    title(F, title_lines, yb + 18, sizes)
    if extra: extra(F)
    img = Image.fromarray(F).resize((1080, 1920), Image.NEAREST)
    for o in out_pngs: img.save(o)
    return img
