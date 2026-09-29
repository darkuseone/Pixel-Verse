"""Cover pipeline for newer series: code-rendered reference frame -> xAI edit (grok-imagine-image-2.0, medium, 1k)
-> pixelize 540x960 / 110 colours -> series plank + big title.
«Валера и кот»: blue enamel house-number style plank («ВАЛЕРА И КОТ» / «СЕРИЯ N/6»), title in the proven
yellow->orange gradient with a navy outline and snow caps (same look as overlays.winter_title)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P
import xai

PROMPT_BASE = (
    "Redraw this image as a highly detailed HD pixel art scene from a modern indie pixel-art adventure game "
    "(crisp visible pixels, rich environment detail, soft light). Keep the same vertical composition, the same background "
    "and exactly the same cartoon characters with their colors and outfits: ")
PROMPT_END = (" Funny, very expressive cartoon faces. Keep the top third of the image calm and simple for a title. "
              "No text, no letters, no numbers, no watermark.")
W, H = 540, 960
NAVY, NAVY_SH = (18, 24, 52), (8, 10, 26)


def ai(ref_png, raw_png, characters):
    return xai.generate(PROMPT_BASE + characters + PROMPT_END, [raw_png], aspect='9:16', ref_png=ref_png)


def pixelize(im):
    im = im.convert('RGB')
    w, h = im.size; tw = h * 9 / 16
    if abs(w - tw) > 2: x0 = int((w - tw) / 2); im = im.crop((x0, 0, x0 + int(tw), h))
    small = im.resize((W, H), Image.BOX)
    return np.array(small.quantize(colors=110, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))


def _font(size):
    return ImageFont.truetype(P.FONT_PX, size)


def enamel_plank(F, text, y, size=24, gap=10):
    """blue enamel street-sign plank with a white rim and white pixel text; '\n' = rows. Returns bottom y."""
    f = _font(size)
    rows = text.split('\n')
    bbs = [f.getbbox(r) for r in rows]
    tw = max(b[2] - b[0] for b in bbs); th = max(b[3] - b[1] for b in bbs)
    pw, ph = tw + 48, th * len(rows) + gap * (len(rows) - 1) + 30
    x0 = (W - pw) // 2
    F[y - 4:y + ph + 4, x0 - 4:x0 + pw + 4] = NAVY
    F[y:y + ph, x0:x0 + pw] = (34, 78, 150)
    F[y + 4:y + ph - 4, x0 + 4:x0 + pw - 4] = (244, 246, 250)                 # white rim
    F[y + 8:y + ph - 8, x0 + 8:x0 + pw - 8] = (36, 84, 162)
    F[y + 8:y + 12, x0 + 8:x0 + pw - 8] = (70, 120, 196)                     # enamel shine
    for nx in (x0 + 14, x0 + pw - 18):                                        # screws
        F[y + ph // 2 - 2:y + ph // 2 + 2, nx:nx + 4] = (200, 206, 214)
    img = Image.new('L', (W, ph), 0)
    d = ImageDraw.Draw(img); d.fontmode = '1'
    for i, (r, bb) in enumerate(zip(rows, bbs)):
        rw = bb[2] - bb[0]
        d.text(((W - rw) // 2 - bb[0], 15 + i * (th + gap) - bb[1]), r, font=f, fill=255)
    m = np.array(img) > 127
    reg = F[y:y + ph]
    reg[np.roll(np.roll(m, 3, 0), 2, 1) & ~m] = (16, 40, 88)
    reg[m] = (250, 250, 255)
    return y + ph


def title(F, lines, top, size=64, max_w=520, gap=12):
    """big title: yellow->orange steps, 4px navy outline + shadow, snow on the top edges"""
    y = top
    for line in lines:
        fsz = size
        while True:
            f = _font(fsz); bb = f.getbbox(line)
            if bb[2] - bb[0] <= max_w or fsz <= 16: break
            fsz -= 8
        img = Image.new('L', (W, fsz * 2), 0)
        d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], -bb[1] + 8), line, font=f, fill=255)
        m = np.array(img) > 127
        rows = np.where(m.any(1))[0]
        if len(rows) == 0: continue
        m = m[:rows[-1] + 14]
        dil = m.copy()
        for dx in range(-4, 5):
            for dy in range(-4, 5): dil |= np.roll(np.roll(m, dy, 0), dx, 1)
        sh = np.roll(np.roll(dil, 5, 0), 3, 1)
        reg = F[y:y + m.shape[0]]
        hh = reg.shape[0]; m, dil, sh = m[:hh], dil[:hh], sh[:hh]
        reg[sh] = NAVY_SH; reg[dil] = NAVY
        r0, r1 = rows[0], rows[-1]
        for yy in range(hh):
            k = (yy - r0) / max(1, r1 - r0)
            reg[yy][m[yy]] = (255, 236, 120) if k < 0.34 else (255, 200, 70) if k < 0.67 else (255, 150, 50)
        cap = m & ~np.roll(m, 5, 0)
        reg[cap] = (250, 252, 255)
        reg[np.roll(cap, -3, 0) & ~m & dil] = (236, 244, 255)
        y += (r1 - r0) + gap + 14
    return y


def make(raw_png, src_jpg, out_pngs, n, title_lines, series='ВАЛЕРА И КОТ', extra=None):
    Image.open(raw_png).convert('RGB').save(src_jpg, quality=93)
    F = pixelize(Image.open(src_jpg))
    for i, yy in enumerate(range(0, 110, 22)):
        F[yy:yy + 22] = (F[yy:yy + 22].astype(np.float32) * (0.62 + 0.07 * i)).astype(np.uint8)
    yb = enamel_plank(F, f'{series}\nСЕРИЯ {n}/6', 136, 24)                 # below the 3:4 grid crop line
    title(F, title_lines, yb + 22, 64, max_w=524, gap=10)
    if extra: extra(F)
    img = Image.fromarray(F).resize((1080, 1920), Image.NEAREST)
    for o in out_pngs: img.save(o)
    return img


def lcd(F, txt, cx, cy, size=40, col=(120, 255, 140)):
    """green LCD price display box drawn onto the 540x960 cover canvas"""
    f = _font(size)
    bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    w, h = tw + 36, th + 30
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    F[y0 - 4:y0 + h + 4, x0 - 4:x0 + w + 4] = NAVY
    F[y0:y0 + h, x0:x0 + w] = (34, 36, 40)
    F[y0 + 5:y0 + h - 5, x0 + 5:x0 + w - 5] = (12, 34, 18)
    img = Image.new('L', (w, h), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text(((w - tw) // 2 - bb[0], (h - th) // 2 - bb[1]), txt, font=f, fill=255)
    m = np.array(img) > 127
    reg = F[y0:y0 + h, x0:x0 + w]
    reg[m] = col
