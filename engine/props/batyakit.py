"""Episode kit for «Батя сам»: the series title style («вязаный»: cream knitted letters with a zigzag stitch, thick burgundy outline,
dark shadow), the yellow tape-measure plate (covers), worlds from the xAI backgrounds, hero light per location, face logging for the
machine critic, Tyoma's phone UI (REC + viewers counter), and the standard overlay pass (badge, hook, stickers, captions, flashes)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import Chars, Light
from scene import sm, lerp
import overlays as O
import paths as PATHS
from props import rusigns as R

SLUG = 'batya'
BG = PATHS.series(SLUG) / 'bg'
COL = dict(batya=(255, 130, 120), tema=(190, 240, 80), ira=(255, 200, 70))
INK, RED, BLUE, PAPER = (34, 28, 30), (184, 30, 40), (40, 60, 150), (242, 236, 218)
BURG, CREAM, TAPE = (120, 20, 36), (246, 236, 210), (246, 206, 30)


def q(im, colors=110):
    return np.array(im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))


def build(force=False):
    cache = PATHS.build('props', 'batya.npz')
    if os.path.exists(cache) and not force:
        d = np.load(cache); return {k: d[k] for k in d.files}
    out = {n: q(Image.open(BG / f'{n}.png').convert('RGB')) for n in ('bedroom', 'kitchen')}
    np.savez_compressed(cache, **out)
    return out


def begin():
    """heroes always at PX=1: one hero pixel = 3 output px (rule: <= 3.75 px)"""
    ST.set_px(1)
    return Chars(), Chars()


def logface(v, cam, head, r_units):
    x, y = cam.p(*head)
    ST.log('sprite', face=(x * ST.UP * ST.PX[0], y * ST.UP * ST.PX[0], r_units * cam.sc * ST.UP * ST.PX[0]))


# ---------------------------------------------------------------- title style «вязаный»
def hook_title(lines, size=64, width=O.OUT_W):
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 50) + 46, width, 4), np.uint8)
    y = 26
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 46), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 20 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        dil = O._dilate(m, 9)
        shd = np.roll(np.roll(dil, 10, 0), 7, 1)
        reg = out[y:y + m.shape[0]]
        reg[shd] = (40, 8, 18, 255); reg[dil] = BURG + (255,)
        yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
        st = max(4, size // 12)
        zig = (np.abs(((xx % (2 * st)) - st)) == (yy % st))                    # knitted «ёлочка» stitches
        reg[m] = CREAM + (255,)
        reg[m & zig] = (214, 196, 160, 255)
        top = m & ~np.roll(m, 6, 0)
        reg[top] = (255, 255, 255, 255)
        y += th + 50
    return out


def title_trim(a):
    ys, xs = np.nonzero(a[..., 3])
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1] if len(ys) else a


def tape(w, h, lines):
    """yellow tape-measure strip with black ticks and a metal hook tab: «БАТЯ САМ / СЕРИЯ N/6» (covers, endcard)"""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 6, w - 1, h - 7], radius=10, fill=TAPE + (255,), outline=(80, 60, 8, 255), width=5)
    d.rectangle([w - 40, 0, w - 22, h - 1], fill=(170, 176, 186, 255), outline=(70, 74, 84, 255), width=3)    # hook tab
    for i, x in enumerate(range(18, w - 50, 14)):
        ln = 30 if i % 5 == 0 else 16
        d.line([(x, 10), (x, 10 + ln)], fill=(30, 26, 20, 255), width=3)
        d.line([(x, h - 11), (x, h - 11 - ln)], fill=(30, 26, 20, 255), width=3)
    a = np.array(im)
    pl = R.plate(w / 4 - 22, h / 4 - 20, lines, bg=TAPE, colors=[INK, RED], border=None, weights=[1, 0.62], pad=0.8)
    ph, pw = pl.shape[:2]
    y0, x0 = (h - ph) // 2, (w - pw) // 2 - 10
    m = pl[..., 3] > 0
    a[y0:y0 + ph, x0:x0 + pw][m] = pl[m]
    return a


# ---------------------------------------------------------------- Tyoma's phone UI (his selfie / POV shots)
_UI = {}


def _ui_text(s, size, fg):
    k = (s, size, fg)
    if k not in _UI: _UI[k] = O.sticker(s, fg=fg, size=size)
    return _UI[k]


def phone_ui(big, t, viewers, title='БАТЯ VS НОЯБРЬ'):
    """dark phone bezel around the frame, a blinking REC dot + stream title, the viewers counter (the number = a joke)"""
    h, w = big.shape[:2]
    b = 22
    big[:b] = (18, 18, 22); big[-b:] = (18, 18, 22); big[:, :b] = (18, 18, 22); big[:, -b:] = (18, 18, 22)
    for (cy, cx) in ((b, b), (b, w - b), (h - b, b), (h - b, w - b)):                 # rounded inner corners
        yy, xx = np.mgrid[max(0, cy - 30):min(h, cy + 30), max(0, cx - 30):min(w, cx + 30)]
        far = ((yy - cy) * np.sign(h / 2 - cy) < 0) | ((xx - cx) * np.sign(w / 2 - cx) < 0)
        big[max(0, cy - 30):min(h, cy + 30), max(0, cx - 30):min(w, cx + 30)][far & (np.hypot(yy - cy, xx - cx) > 0)] = (18, 18, 22)
    rec = _ui_text('REC  ' + title, 30, (255, 255, 255))
    if (t % 1.0) < 0.6:                                                                        # blinking red dot
        yy, xx = np.mgrid[0:30, 0:30]
        m = (yy - 15) ** 2 + (xx - 15) ** 2 <= 144
        big[214:244, 46:76][m] = (240, 50, 50)
    O.overlay(big, rec, 82, 196, 1.0)
    vw = _ui_text(f'ЗРИТЕЛИ: {viewers}', 30, (255, 255, 255))
    O.overlay(big, vw, w - vw.shape[1] - 40, 252, 1.0)


# ---------------------------------------------------------------- overlay pass
class Show:
    def __init__(s, epi, season, n, hook, hook_t=(0.06, 2.4), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330,
                 hook_y=300, extra=None):
        s.epi = epi
        s.badge = O.make_badge(f'СЕЗОН {season} • СЕРИЯ {n}/6')
        s.hook = hook_title(hook, 70) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default
        s.extra = extra

    def apply(s, big, t, shot):
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        if s.extra: s.extra(big, t, shot)
        O.overlay(big, s.badge, 36, 96, 1.0)
        if s.hook is not None and s.hook_t[0] <= t < s.hook_t[1]:
            k = min(1.0, (t - s.hook_t[0]) / 0.1) * (1 - sm((t - (s.hook_t[1] - 0.2)) / 0.2))
            O.overlay(big, s.hook, 0, s.hook_y, k)
        s.epi.captions.draw(big, t, s.cap_y.get(shot, s.cap_default))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


def question(top, bottom):
    """the silent comment question over the button (rule 08.11.2026: text, not voice)"""
    a = O.sticker(top, fg=(255, 236, 200), size=44)
    b = O.sticker(bottom, fg=(255, 214, 60), size=38)
    w = max(a.shape[1], b.shape[1])
    out = np.zeros((a.shape[0] + b.shape[0] - 30, w, 4), np.uint8)
    out[:a.shape[0], (w - a.shape[1]) // 2:(w - a.shape[1]) // 2 + a.shape[1]] = a
    sub = out[a.shape[0] - 30:, (w - b.shape[1]) // 2:(w - b.shape[1]) // 2 + b.shape[1]]
    m = b[..., 3] > sub[..., 3]
    sub[m] = b[m]
    return out
