"""Episode kit for «Тёща на недельку»: the series title style («тёщин халат»: raspberry -> pink stepped letters, plum outline, gold
shine on top), the doily plate for covers, worlds from the xAI backgrounds with local signs (decals), hero light per location,
face logging for the machine critic, and the standard overlay pass (badge, hook, stickers, captions, flashes, mosaic)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import Chars, Light
from scene import sm, lerp
import overlays as O
import paths as PATHS
from props import decals as D
from props import rusigns as R

SLUG = 'teshcha'
BG = PATHS.series(SLUG) / 'bg'
COL = dict(tolik=(90, 225, 215), raisa=(255, 110, 175), pusya=(255, 222, 80), sveta=(175, 235, 110))
INK, RED, BLUE, PAPER = (34, 28, 30), (184, 30, 40), (40, 60, 150), (242, 236, 218)
PLUM = (58, 16, 40)

# ---------------------------------------------------------------- landing (native px of bg/landing.png)
L_FLOOR = 560.0          # Tolik's feet on the threshold of the open door
L_DOOR_X = 962.0
L_LIFT = (232, 80, 418, 540)
L_BULB = (640.0, 60.0)
L_STAIRS = (150.0, 690.0)
# ---------------------------------------------------------------- room
R_FLOOR = 640.0
R_CHAIR = (600.0, 650.0)  # floor point under the armchair seat front
R_LAMP = (905.0, 200.0)
R_TV = (1210.0, 420.0)
# ---------------------------------------------------------------- balcony
B_DOOR = (40, 120, 200, 640)
B_BED = (338.0, 668.0)


def q(im, colors=110):
    return np.array(im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))


def glow_map(shape, pts, r):
    Hh, Ww = shape
    yy, xx = np.mgrid[0:Hh, 0:Ww].astype(np.float32)
    g = np.zeros(shape, np.float32)
    for (x, y) in pts:
        g += np.clip(1 - np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / r, 0, 1) ** 1.6
    return g


def build(force=False):
    cache = PATHS.build('props', 'teshcha.npz')
    if os.path.exists(cache) and not force:
        d = np.load(cache); return {k: d[k] for k in d.files}
    out = {n: q(Image.open(BG / f'{n}.png').convert('RGB')) for n in ('landing', 'room', 'balcony')}
    np.savez_compressed(cache, **out)
    return out


def decorate(W, day=1):
    """local signs and labels (rule 10.10.2026: 5–10 per location, every inscription fitted inside its plate)"""
    D.attach(W['landing'], [
        (R.plate(38, 16, ['КВ. 33'], bg=(236, 206, 120), colors=[INK], border=(120, 84, 30), pad=1.5), 1150, 128),
        (R.plate(40, 30, ['НЕ ХЛОПАТЬ', 'ДВЕРЬЮ!', 'ЛИФТ ОБИЖАЕТСЯ'], bg=PAPER, colors=[RED, RED, INK], border=(150, 140, 120),
                 weights=[1, 1, 0.7], pad=1.5, tilt=-2), 712, 168),
        (R.plate(36, 34, ['ПРОДАМ', 'ГАРАЖ', '8-916-...'], bg=(250, 250, 240), colors=[INK, BLUE, INK], border=(170, 160, 140),
                 weights=[1, 1, 0.6], pad=1.5, tilt=3), 790, 172),
        (R.plate(30, 30, ['ПРОПАЛА', 'СОБАКА', 'НЕ ИЩИТЕ.', 'ОНА У ЗИНЫ'], bg=(255, 244, 170), colors=[RED, INK, INK, INK],
                 border=(170, 150, 90), weights=[1, 1, 0.7, 0.7], pad=1.2, tilt=-3), 742, 222),
        (R.plate(36, 22, ['ЛИФТ', 'ПО ЧЁТНЫМ'], bg=(236, 236, 230), colors=[INK, RED], border=(90, 90, 96), pad=1.5), 432, 236),
        (R.plate(28, 12, ['4 ЭТАЖ'], bg=(60, 110, 70), colors=[(244, 240, 220)], border=(30, 50, 34), pad=1.2), 560, 120),
        (R.plate(44, 18, ['ВЫТИРАЙТЕ', 'НОГИ!'], bg=(200, 60, 50), colors=[(255, 240, 220), (255, 240, 220)], border=(90, 24, 20),
                 pad=1.5), 930, 600),
    ])
    D.attach(W['room'], [
        (R.plate(42, 16, ['СОЧИ-2009'], bg=(70, 160, 210), colors=[(255, 250, 220)], border=(30, 60, 90), pad=1.2, tilt=-4), 1150, 330),
        (R.plate(26, 34, ['ДЕНЬ', str(day)], bg=(250, 248, 240), colors=[RED, INK], border=(120, 110, 100), weights=[0.55, 1],
                 stripe=((200, 40, 40), 0.3), pad=1.2), 470, 102),
        (R.plate(40, 14, ['НЕ ВКЛЮЧАТЬ!'], bg=(255, 244, 170), colors=[RED], border=(150, 130, 70), pad=1.0, tilt=3), 1180, 470),
        (R.plate(46, 20, ['ХРУСТАЛЬ', 'НЕ ТРОГАТЬ'], bg=PAPER, colors=[INK, RED], border=(140, 120, 90), pad=1.5, tilt=-2), 270, 455),
    ])
    D.attach(W['balcony'], [
        (R.plate(30, 13, ['КАБАЧКИ 19'], bg=(250, 246, 230), colors=[INK], border=(120, 110, 90), pad=0.8), 1110, 126),
        (R.plate(30, 13, ['ОГУРЦЫ 21'], bg=(250, 246, 230), colors=[INK], border=(120, 110, 90), pad=0.8), 1110, 228),
        (R.plate(36, 16, ['ЛЫЖИ ТОЛИКА'], bg=(240, 230, 210), colors=[BLUE], border=(110, 90, 70), pad=0.9, tilt=-6), 940, 452),
        (R.plate(34, 16, ['РАССАДА', 'НЕ ТРОГАТЬ'], bg=(255, 244, 170), colors=[RED, INK], border=(150, 130, 70), pad=1.0), 1080, 506),
        (R.plate(44, 18, ['ЗАКАЛЯЙСЯ!'], bg=(210, 60, 60), colors=[(255, 244, 230)], border=(90, 24, 20), pad=1.5, tilt=4), 560, 452),
    ])


# ---------------------------------------------------------------- lights
def light_landing(v):
    bx, by = v.opt(*L_BULB); dx, dy = v.opt(960.0, 300.0)
    return Light(amb=(1.0, 0.96, 0.9), keys=[(bx, by, 1300, (255, 210, 140), 0.55), (dx, dy, 900, (255, 200, 120), 0.45)],
                 rim=(1, -0.3, (255, 226, 170), 0.35), grad=(1.04, 0.9))


def light_room(v, tv=0.0):
    lx, ly = v.opt(*R_LAMP)
    keys = [(lx, ly, 1400, (255, 190, 110), 0.7)]
    if tv > 0:
        tx, ty = v.opt(*R_TV); keys.append((tx, ty, 900, (150, 190, 255), 0.5 * tv))
    return Light(amb=(1.02, 0.95, 0.88), keys=keys, rim=(1, -0.4, (255, 214, 160), 0.35), grad=(1.03, 0.9))


def light_balcony(v):
    dx, dy = v.opt(120.0, 380.0)
    return Light(amb=(0.8, 0.9, 1.14), keys=[(dx, dy, 1100, (255, 196, 110), 0.65)], rim=(1, -0.3, (190, 214, 255), 0.5),
                 grad=(1.05, 0.88))


def begin():
    """heroes always at PX=1: one hero pixel = 3 output px (rule: <= 3.75 px), background zoom <= 1.45"""
    ST.set_px(1)
    return Chars(), Chars()


def logface(v, cam, head, r_units):
    """machine critic: where a face is on the output frame (centre + radius in output px)"""
    x, y = cam.p(*head)
    ST.log('sprite', face=(x * ST.UP * ST.PX[0], y * ST.UP * ST.PX[0], r_units * cam.sc * ST.UP * ST.PX[0]))


# ---------------------------------------------------------------- title style «тёщин халат»
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
        shd = np.roll(np.roll(dil, 11, 0), 7, 1)
        reg = out[y:y + m.shape[0]]
        reg[shd] = (24, 6, 18, 255); reg[dil] = PLUM + (255,)
        rows = np.where(m.any(1))[0]; r0, r1 = rows[0], rows[-1]
        for yy in range(m.shape[0]):
            k = (yy - r0) / max(1, r1 - r0)
            col = (255, 186, 214) if k < 0.3 else (255, 110, 170) if k < 0.62 else (214, 36, 104)
            reg[yy][m[yy]] = col + (255,)
        top = m & ~np.roll(m, 7, 0)                                       # gold-tooth shine on the top edges
        reg[top] = (255, 214, 90, 255)
        reg[top & np.roll(top, 3, 1)] = (255, 246, 190, 255)
        y += th + 50
    return out


def title_trim(a):
    ys, xs = np.nonzero(a[..., 3])
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1] if len(ys) else a


def doily(w, h, lines):
    """embroidered white doily plate with a lace edge: «ТЁЩА НА НЕДЕЛЬКУ / СЕРИЯ N/6» (covers)"""
    S = 4
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    r = 14
    for i in range(0, w, 2 * r):                                          # scalloped lace edge
        d.ellipse([i - 2, -r + 8, i + 2 * r + 2, r + 8], fill=(250, 246, 236, 255))
        d.ellipse([i - 2, h - r - 8, i + 2 * r + 2, h + r - 8], fill=(250, 246, 236, 255))
    for j in range(0, h, 2 * r):
        d.ellipse([-r + 8, j - 2, r + 8, j + 2 * r + 2], fill=(250, 246, 236, 255))
        d.ellipse([w - r - 8, j - 2, w + r - 8, j + 2 * r + 2], fill=(250, 246, 236, 255))
    d.rectangle([12, 12, w - 13, h - 13], fill=(252, 248, 240, 255))
    for i in range(0, w, 2 * r):                                          # lace holes
        d.ellipse([i + r - 3, 6, i + r + 3, 12], fill=(0, 0, 0, 0))
        d.ellipse([i + r - 3, h - 12, i + r + 3, h - 6], fill=(0, 0, 0, 0))
    d.rectangle([24, 24, w - 25, h - 25], outline=(214, 60, 120, 255), width=4)
    for k in range(0, w - 60, 22):                                        # cross-stitch border
        x = 34 + k
        d.line([(x, 30), (x + 8, 38)], fill=(214, 60, 120, 255), width=2); d.line([(x + 8, 30), (x, 38)], fill=(214, 60, 120, 255), width=2)
        d.line([(x, h - 38), (x + 8, h - 30)], fill=(214, 60, 120, 255), width=2); d.line([(x + 8, h - 38), (x, h - 30)], fill=(214, 60, 120, 255), width=2)
    a = np.array(im)
    pl = R.plate(w / 4 - 16, h / 4 - 20, lines, bg=(252, 248, 240), colors=[PLUM, (214, 40, 104)], border=None, weights=[1, 0.7], pad=1.0)
    ph, pw = pl.shape[:2]
    y0, x0 = (h - ph) // 2, (w - pw) // 2
    m = pl[..., 3] > 0
    a[y0:y0 + ph, x0:x0 + pw][m] = pl[m]
    return a


# ---------------------------------------------------------------- overlay pass
class Show:
    def __init__(s, epi, season, n, hook, hook_t=(0.06, 2.4), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330,
                 hook_y=300):
        s.epi = epi
        s.badge = O.make_badge(f'СЕЗОН {season} • СЕРИЯ {n}/6')
        s.hook = hook_title(hook, 70) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default

    def apply(s, big, t, shot):
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
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
    a = O.sticker(top, fg=(255, 186, 214), size=48)
    b = O.sticker(bottom, fg=(255, 255, 255), size=38)
    w = max(a.shape[1], b.shape[1])
    out = np.zeros((a.shape[0] + b.shape[0] - 30, w, 4), np.uint8)
    out[:a.shape[0], (w - a.shape[1]) // 2:(w - a.shape[1]) // 2 + a.shape[1]] = a
    sub = out[a.shape[0] - 30:, (w - b.shape[1]) // 2:(w - b.shape[1]) // 2 + b.shape[1]]
    m = b[..., 3] > sub[..., 3]
    sub[m] = b[m]
    return out


def decal_layer(L, v, img, wx, wy, ws=4):
    """paint a decal (RGBA, ws px per world px) into a character-canvas Layer at world (wx, wy), so heroes drawn later cover it"""
    import scene as S
    k = ST.PX[0]
    h, w = img.shape[:2]
    x0, y0 = v.pt(wx, wy); x1, y1 = v.pt(wx + w / ws, wy + h / ws)
    win = S.win(x0, x1, y0, y1)
    if win is None: return
    X = S.XX[win]; Y = S.YY[win]
    u = ((X - x0) / max(1e-6, x1 - x0) * w).astype(int).clip(0, w - 1)
    q_ = ((Y - y0) / max(1e-6, y1 - y0) * h).astype(int).clip(0, h - 1)
    sub = img[q_, u]
    m = sub[..., 3] > 127
    L.set(win, m, (0, 0, 0))
    L.col[win][m] = sub[..., :3][m]
