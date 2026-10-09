"""«Florida Man: Allegedly» episode kit: speaker colours, noon-sun / freezer / jail lights, worlds (xAI backgrounds), the series hook
title («Greetings from Florida» postcard letters: yellow -> coral -> magenta, teal 3D extrusion, white outline), the overlay pass (Show)
with the BREAKING chyron, the FREQUENT GUEST punch card, the mugshot wall and booking board, heat haze, cold blast, smoke, frost.
Shot compositing reuses props/chikit.shot (world view + direct actors + fx + vignette)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import paths as P
import stage as ST
from stage import Light, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from props import chikit as CK
from props import bytfx as B
from props import fmpix as FX
from props import fmcast as C
from props.dibspix import blit

SLUG = 'florida-man'
COL = dict(fm=(255, 132, 110), mort=(90, 230, 225), darlene=(255, 214, 80), tanner=(170, 255, 110))
INK = FX.INK
SUNSET = ((255, 236, 96), (255, 150, 90), (246, 76, 150))          # title fill: yellow -> coral -> magenta
EXTR = (20, 150, 160)                                               # teal 3D extrusion
shot = CK.shot
J, hit = CK.J, CK.hit


def A(fn, wx, wy, s, flip=False, pin=None, **kw):
    return FX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, **kw)


def wpt(v, ox, oy):
    """output px -> world px"""
    return v.X0 + ox / (3 * v.Z), v.Y0 + (oy / 3 - v.oy) / v.Z


def put(v, fn, ox, oy, s, **kw):
    """an actor whose feet anchor lands on output point (ox, oy) of view v"""
    return A(fn, *wpt(v, ox, oy), s, **kw)


def aout(act, v, name):
    """output px of a named sprite anchor of an actor that has been drawn"""
    sp = act.last
    px, py = sp.anchors[name]
    ox, oy = v.opt(act.wx, act.wy)
    sc = act.scale(v)
    if act.pin:
        qx, qy = sp.anchors[act.pin]
        ox -= (-qx if act.flip else qx) * sc; oy += qy * sc
    return ox + (-px if act.flip else px) * sc, oy - py * sc


# ---------------------------------------------------------------- lights
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_sun(v, keys=((380, -200, 900, (255, 236, 170), 0.35),)):
    """noon sun: warm ambient, a hot top rim on every head and shoulder"""
    return Light(amb=(1.06, 1.02, 0.94), keys=_keys(v, keys), rim=(0, -1, (255, 250, 222), 0.55), grad=(1.06, 0.96))


def light_store(v):
    return light_sun(v, ((640, -100, 900, (255, 236, 170), 0.3),))


def light_aisle(v):
    """freezer aisle: cold blue-white light from the cases, fluorescent top rim"""
    return Light(amb=(0.94, 1.0, 1.10), keys=_keys(v, ((640, 360, 900, (190, 230, 255), 0.35),)), rim=(0, -1, (230, 246, 255), 0.5),
                 grad=(1.06, 0.94))


def light_deli(v):
    """deli counter: warm fluorescent ceiling, a bit of window sun from the left"""
    return Light(amb=(1.02, 1.01, 0.98), keys=_keys(v, ((120, 200, 700, (255, 236, 190), 0.3),)), rim=(0, -1, (255, 250, 236), 0.5),
                 grad=(1.04, 0.95))


def light_cell(v):
    return Light(amb=(0.94, 0.98, 0.90), keys=_keys(v, ((540, 140, 520, (255, 220, 140), 0.45),)), rim=(1, -1, (255, 236, 180), 0.4),
                 grad=(1.04, 0.92))


# ---------------------------------------------------------------- worlds
_W = {}


def world(name):
    if name not in _W:
        _W[name] = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png')
    return _W[name]


# ---------------------------------------------------------------- FX
def heat_haze(big, t, y0=0, y1=OUT_H, amp=6, speed=3.0, band=24):
    """shimmering rows (hot air): every `band` output px row-block is shifted sideways by a sine"""
    for y in range(y0, y1, band):
        dx = int(amp * math.sin(t * speed * 2 + y * 0.045))
        if dx: big[y:y + band] = np.roll(big[y:y + band], dx, 1)


def cold_blast(big, t, k=1.0, n=46, seed=2, dirn=-1):
    """white-blue wind streaks + snow flecks blowing out of the store / freezer"""
    r = np.random.default_rng(seed)
    for i in range(int(n * k)):
        y = int(r.random() * OUT_H); sp_ = 1800 + r.random() * 1600; ln = int(80 + r.random() * 260)
        x = int(((t * sp_ + r.random() * 4000) % (OUT_W + 600)) - 300)
        if dirn < 0: x = OUT_W - x
        a, b = max(0, x), min(OUT_W, x + ln)
        if a < b: big[y:y + 6, a:b] = (big[y:y + 6, a:b] * 0.35 + np.array((236, 248, 255)) * 0.65).astype(np.uint8)
        fx_ = (x + ln + 30) % OUT_W
        big[y - 9:y - 3, fx_:fx_ + 6] = (250, 254, 255)


def smoke(big, x, y, t, n=7, rise=320, size=60, a=0.55, col=(90, 90, 96), seed=0):
    """dark stepped smoke puffs rising from a dead machine (output px)"""
    r = np.random.default_rng(seed)
    for i in range(n):
        ph = (t * 0.9 + i / n) % 1.0
        cx = x + 50 * math.sin(i * 2.1 + t * 1.5) + 40 * ph * (r.random() - 0.3)
        cy = y - rise * ph
        rr = size * (0.5 + ph)
        B.puff(big, cx, cy, rr, a * (1 - ph), col)


def frost_edges(big, k=1.0):
    """frosty white corners/edges of the frame (freezer cold), stepped"""
    h, w = big.shape[:2]
    yy, xx = np.ogrid[0:h, 0:w]
    d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)).astype(np.float32)
    noise = (np.sin(xx * 0.09) * np.cos(yy * 0.07) + 1) * 30
    v = np.clip(1 - (d - noise) / (160 * k + 1), 0, 1)
    v = np.floor(v * 4) / 4 * 0.8
    big[:] = (big * (1 - v[..., None]) + np.array((236, 248, 255)) * v[..., None]).astype(np.uint8)


def sparkle(big, x, y, t, col=(255, 255, 255), n=4, r=60):
    for i in range(n):
        a = i * 1.57 + t * 3
        cx, cy = int(x + math.cos(a) * r), int(y + math.sin(a) * r * 0.6)
        s = int(8 + 6 * abs(math.sin(t * 7 + i)))
        if 0 <= cx < OUT_W - s and 0 <= cy < OUT_H - s:
            big[cy - s:cy + s, cx - 2:cx + 2] = col; big[cy - 2:cy + 2, cx - s:cx + s] = col


def dof(big, r=6):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


# ---------------------------------------------------------------- hook title («Greetings from Florida» postcard letters)
def _dil(m, r, step=2):
    d = m.copy()
    for dx in range(-r, r + 1, step):
        for dy in range(-r, r + 1, step):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def hook_title(lines, size=72, width=OUT_W, depth=14):
    """Press Start 2P, yellow -> coral -> magenta stepped fill, white outline, a thick teal 3D extrusion down-right, dark teal edge"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 64) + 70, width, 4), np.uint8)
    y = 26
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 70), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0] - depth // 2, 22 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        wh = _dil(m, 7)                                                  # white outline
        ext = np.zeros_like(m)
        for k in range(1, depth + 1): ext |= np.roll(np.roll(wh, k, 0), k, 1)
        edge = _dil(wh | ext, 5) & ~(wh | ext)
        reg = out[y:y + m.shape[0]]
        reg[edge] = INK + (255,)
        reg[ext & ~wh] = EXTR + (255,)
        sh = ext & ~wh & np.roll(np.roll(ext & ~wh, -3, 0), -3, 1)
        reg[ext & ~wh & ~sh] = (10, 100, 112, 255)
        reg[wh] = (255, 255, 250, 255)
        rows = np.where(m.any(1))[0]; r0, r1 = rows[0], rows[-1]
        for yy in range(m.shape[0]):
            k = (yy - r0) / max(1, r1 - r0)
            col = SUNSET[0] if k < 0.34 else SUNSET[1] if k < 0.67 else SUNSET[2]
            reg[yy][m[yy]] = col + (255,)
        reg[m & ~np.roll(m, 7, 0)] = (255, 255, 236, 255)
        y += th + 64
    return out


def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


# ---------------------------------------------------------------- BREAKING chyron (local-news lower third)
_CHY = {}


def chyron_img(line1, line2=None):
    key = (line1, line2)
    if key in _CHY: return _CHY[key]
    h = 250 if line2 else 190
    im = Image.new('RGBA', (OUT_W, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 60, OUT_W, h], fill=(250, 250, 246, 255))
    d.rectangle([0, 60, OUT_W, 70], fill=(226, 34, 52, 255))
    d.rectangle([24, 0, 360, 72], fill=(226, 34, 52, 255)); d.rectangle([24, 0, 360, 8], fill=(255, 120, 120, 255))
    d.text((44, 18), 'BREAKING', font=O.pfont(36), fill=(255, 255, 255, 255))
    d.rectangle([380, 14, 640, 60], fill=(14, 44, 54, 255)); d.text((396, 24), 'LIVE', font=O.pfont(26), fill=(255, 236, 96, 255))
    d.ellipse([570, 26, 592, 48], fill=(226, 34, 52, 255))
    d.text((40, 92), line1, font=O.pfont(34), fill=(14, 20, 30, 255))
    if line2: d.text((40, 150), line2, font=O.pfont(34), fill=(14, 20, 30, 255))
    a = np.array(im)
    _CHY[key] = a
    return a


def allegedly_stamp(size=30):
    key = ('stamp', size)
    if key in _CHY: return _CHY[key]
    f = O.pfont(size); bb = f.getbbox('(ALLEGEDLY)'); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    im = Image.new('RGBA', (tw + 60, th + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([4, 4, tw + 56, th + 46], outline=(226, 34, 52, 255), width=8)
    d.text((30 - bb[0], 25 - bb[1]), '(ALLEGEDLY)', font=f, fill=(226, 34, 52, 255))
    im = im.rotate(8, resample=Image.NEAREST, expand=True)
    a = np.array(im)
    _CHY[key] = a
    return a


def chyron(big, t, t0, t1, line1, line2=None, y=1500):
    if not (t0 <= t < t1): return
    u = t - t0
    img = chyron_img(line1, line2)
    slide = int((1 - sm(min(1.0, u / 0.18))) * -OUT_W)
    O.overlay(big, img, slide, y, 1.0)
    if u > 0.35:
        k = min(1.0, (u - 0.35) / 0.08)
        stp = allegedly_stamp()
        sc = 1.0 + 0.6 * (1 - k)
        im = Image.fromarray(stp).resize((int(stp.shape[1] * sc), int(stp.shape[0] * sc)), Image.NEAREST)
        a = np.array(im)
        O.overlay(big, a, OUT_W - a.shape[1] - 24, y - a.shape[0] + 40, k)


# ---------------------------------------------------------------- FREQUENT GUEST punch card
def punch_card(big, t, t0, n, cx=540, cy=760, w=760, punch_t=None):
    """the county jail loyalty card: 10 holes, n of them punched; the n-th one gets punched at punch_t (pops in)"""
    h = int(w * 0.56)
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    k = min(1.0, max(0.0, (t - t0) / 0.15))
    if k <= 0: return
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], fill=(14, 44, 54, 255))
    d.rectangle([8, 8, w - 9, h - 9], fill=(255, 244, 214, 255))
    d.rectangle([8, 8, w - 9, 92], fill=(255, 150, 90, 255))
    d.text((30, 28), 'SUNSHINE COUNTY JAIL', font=O.pfont(26), fill=(14, 44, 54, 255))
    d.text((30, 64), 'FREQUENT GUEST', font=O.pfont(20), fill=(255, 255, 255, 255))
    d.text((30, h - 56), '10 STAYS = 1 FREE NIGHT!', font=O.pfont(22), fill=(226, 34, 52, 255))
    r = 34; gx0 = 70; gy0 = 150; gap = (w - 2 * gx0) / 4
    for i in range(10):
        cxh = gx0 + (i % 5) * gap; cyh = gy0 + (i // 5) * 100
        d.ellipse([cxh - r, cyh - r, cxh + r, cyh + r], outline=(14, 44, 54, 255), width=6)
        punched = i < n - 1 or (i == n - 1 and (punch_t is None or t >= punch_t))
        if punched:
            d.ellipse([cxh - r + 10, cyh - r + 10, cxh + r - 10, cyh + r - 10], fill=(0, 0, 0, 0))
            d.ellipse([cxh - r + 10, cyh - r + 10, cxh + r - 10, cyh + r - 10], fill=(40, 40, 46, 255))
    a = np.array(im)
    sc = 0.85 + 0.15 * k
    if sc != 1.0:
        a = np.array(Image.fromarray(a).resize((int(w * sc), int(h * sc)), Image.NEAREST))
    O.overlay(big, a, int(cx - a.shape[1] / 2), int(cy - a.shape[0] / 2), k)
    if punch_t is not None and punch_t <= t < punch_t + 0.2:                           # the punch flash on the new hole
        i = n - 1; cxh = gx0 + (i % 5) * gap; cyh = gy0 + (i // 5) * 100
        fx.glow(big, int(cx - a.shape[1] / 2 + cxh * sc), int(cy - a.shape[0] / 2 + cyh * sc), 110, (255, 255, 230), 0.8)


# ---------------------------------------------------------------- mugshot wall + booking board
_MUG = None


def mug_wall():
    """height-chart wall of the booking room, drawn in code (lines and numbers stay crisp)"""
    global _MUG
    if _MUG is None:
        im = Image.new('RGB', (OUT_W, OUT_H), (176, 196, 204)); d = ImageDraw.Draw(im); d.fontmode = '1'
        for y in range(0, OUT_H, 8): d.line([(0, y), (OUT_W, y)], fill=(170, 190, 198))
        labels = {0: "7'", 2: "6'6", 4: "6'", 6: "5'6", 8: "5'", 10: "4'6", 12: "4'"}
        for i in range(0, 14):
            y = 160 + i * 110
            d.rectangle([0, y, OUT_W, y + 8], fill=(40, 60, 70))
            if i in labels:
                d.text((30, y - 46), labels[i], font=O.pfont(34), fill=(40, 60, 70)); d.text((OUT_W - 150, y - 46), labels[i], font=O.pfont(34), fill=(40, 60, 70))
            else:
                d.rectangle([0, y - 55, 60, y - 51], fill=(80, 100, 110)); d.rectangle([OUT_W - 60, y - 55, OUT_W, y - 51], fill=(80, 100, 110))
        _MUG = np.array(im)
    return _MUG.copy()


def booking_board(big, cx, cy, lines, w=640):
    """black peg letterboard held at chest height: white letters"""
    h = 60 + 64 * len(lines)
    im = Image.new('RGB', (w, h), (18, 20, 24)); d = ImageDraw.Draw(im); d.fontmode = '1'
    for y in range(18, h - 10, 16): d.line([(14, y), (w - 14, y)], fill=(30, 32, 38))
    d.rectangle([0, 0, w - 1, h - 1], outline=(70, 74, 80), width=8)
    for i, ln in enumerate(lines):
        f = O.pfont(34 if i == 0 else 26)
        bb = f.getbbox(ln); tw = bb[2] - bb[0]
        d.text(((w - tw) // 2 - bb[0], 36 + i * 64), ln, font=f, fill=(246, 246, 240))
    a = np.array(im)
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya = max(0, x0), max(0, y0); xb, yb = min(OUT_W, x0 + w), min(OUT_H, y0 + h)
    big[ya:yb, xa:xb] = a[ya - y0:yb - y0, xa - x0:xb - x0]


# ---------------------------------------------------------------- the A/C invoice held up to the camera (screen space)
def invoice_card(big, x, y, w=520, ang=-6.0, amount='$9,000', head='COOL-RITE A/C', lines=('COMPRESSOR...DEAD', 'WAIT.....3 WEEKS'),
                 hc=(40, 120, 200)):
    h = int(w * 0.62)
    hb = int(h * 0.27)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], fill=(14, 44, 54, 255))
    d.rectangle([8, 8, w - 9, h - 9], fill=(252, 252, 244, 255))
    d.rectangle([8, 8, w - 9, hb], fill=hc + (255,))
    fh, fl, ft = O.pfont(max(16, int(w * 0.056))), O.pfont(max(10, int(w * 0.036))), O.pfont(max(12, int(w * 0.044)))
    d.text((int(w * 0.055), int(hb * 0.36)), head, font=fh, fill=(255, 255, 255, 255))
    for i, ln in enumerate(lines[:2]):
        d.text((int(w * 0.055), hb + int(h * (0.07 + 0.10 * i))), ln, font=fl, fill=(70, 70, 80, 255))
    d.text((int(w * 0.055), hb + int(h * 0.30)), 'TOTAL:', font=ft, fill=(70, 70, 80, 255))
    f = O.pfont(int(w * 0.1)); bb = f.getbbox(amount)
    d.text((w - int(w * 0.055) - (bb[2] - bb[0]) - bb[0], h - int(h * 0.09) - (bb[3] - bb[1]) - bb[1]), amount, font=f, fill=(226, 30, 40, 255))
    im = im.rotate(ang, resample=Image.NEAREST, expand=True)
    a = np.array(im)
    O.overlay(big, a, int(x), int(y), 1.0)
    return a.shape[1], a.shape[0]


# ---------------------------------------------------------------- overlay pass
class Show:
    def __init__(s, epi, n, hook, hook_t=(0.10, 2.6), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330, hook_y=150, total=6,
                 hook_size=72, chyrons=(), cards=(), extra=None):
        s.epi = epi
        s.badge = O.make_badge(f'SEASON 1 • EPISODE {n}/{total}')
        s.hook = hook_title(hook, hook_size) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default
        s.chyrons = list(chyrons); s.cards = list(cards); s.extra = extra

    def apply(s, big, t, shot_):
        for (t0, t1, l1, l2, y) in s.chyrons: chyron(big, t, t0, t1, l1, l2, y)
        for (t0, t1, n, pt, cx, cy) in s.cards:
            if t0 <= t < t1: punch_card(big, t, t0, n, cx, cy, punch_t=pt)
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        O.overlay(big, s.badge, 36, 96, 1.0)
        if s.hook is not None and s.hook_t[0] <= t < s.hook_t[1]:
            k = min(1.0, (t - s.hook_t[0]) / 0.1) * (1 - sm((t - (s.hook_t[1] - 0.2)) / 0.2))
            O.overlay(big, s.hook, 0, s.hook_y, k)
        if s.extra: s.extra(big, t, shot_)
        s.epi.captions.draw(big, t, s.cap_y.get(shot_, s.cap_default))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


# ---------------------------------------------------------------- signs baked into the worlds (tiny pixel font at world resolution)
def wtext(arr, s_, x, y, col, k=1):
    """3x5 pixel text straight into a world image (top-left at x, y; k = world px per font px)"""
    cx = x
    for ch in s_:
        g = C.FONT.get(ch.upper(), C.FONT[' '])
        for r, row in enumerate(g):
            for q, b in enumerate(row):
                if b == '1': arr[y + r * k:y + (r + 1) * k, cx + q * k:cx + (q + 1) * k] = col
        cx += (len(g[0]) + 1) * k
    return cx - x


def wtext_w(s_, k=1):
    return C.txt_w(s_) * k


SLOGAN = ["ARRESTED?", "GATOR'D? MELTED?"]           # Mort's billboard slogan: a new one every episode (set before world_baked('yard'))


def bake_yard(Wd):
    """Mort's billboard across the canal: his face + «MORT POUCH, ESQ. / <slogan> / 1-800-POUCH-ME»"""
    x0, y0, x1, y1 = 812, 218, 1002, 312
    Wd[y0:y1, x0:x1] = (250, 248, 238)
    Wd[y0:y0 + 6, x0:x1] = (40, 196, 196)
    with ST_res_guard():
        sp = FX.draw(C.mort, 1.0, t=0.0, expr='smug', look=(0.4, 0.0), lift=0.6, blink=False)
    blit(Wd, sp, x0 + 34, y1 - 3, 1.0)
    tx = x0 + 70
    wtext(Wd, 'MORT POUCH', tx, y0 + 14, (14, 44, 54), 2)
    wtext(Wd, 'ESQ.', tx, y0 + 28, (14, 44, 54), 2)
    wtext(Wd, SLOGAN[0], tx, y0 + 44, (226, 34, 52), 1)
    wtext(Wd, SLOGAN[1], tx, y0 + 52, (226, 34, 52), 1)
    wtext(Wd, '1-800-POUCH-ME', tx, y0 + 66, (20, 140, 150), 1)
    Wd[y1 - 6:y1, x0:x1] = (255, 150, 90)


def bake_store(Wd):
    x0, y0, x1, y1 = 446, 176, 846, 252
    Wd[y0:y1, x0:x1] = (246, 246, 236)
    w = wtext_w('PUBBIX', 6)
    wtext(Wd, 'PUBBIX', (x0 + x1 - w) // 2, y0 + 8, (34, 150, 110), 6)
    t2 = 'WHERE SHOPPING IS A PLEASURE*'
    wtext(Wd, t2, (x0 + x1 - wtext_w(t2, 1)) // 2, y0 + 50, (14, 44, 54), 1)
    t3 = '*PRICES MAY VARY'
    wtext(Wd, t3, (x0 + x1 - wtext_w(t3, 1)) // 2, y0 + 60, (226, 34, 52), 1)


def bake_aisle(Wd):
    x0, y0, x1, y1 = 520, 54, 772, 112
    Wd[y0:y1, x0:x1] = (40, 150, 160)
    t1 = 'AISLE 9'
    wtext(Wd, t1, (x0 + x1 - wtext_w(t1, 3)) // 2, y0 + 8, (255, 255, 250), 3)
    t2 = 'FROZEN FOODS'
    wtext(Wd, t2, (x0 + x1 - wtext_w(t2, 2)) // 2, y0 + 34, (255, 236, 96), 2)


def bake_deli(Wd):
    """the Pubbix deli menu board (prices!) and the scale's LCD showing Mort's weight and price"""
    x0, y0, x1, y1 = 360, 80, 968, 216
    Wd[y0:y1, x0:x1] = (250, 244, 222)
    t = 'PUBBIX DELI'
    wtext(Wd, t, (x0 + x1 - wtext_w(t, 4)) // 2, y0 + 6, (34, 150, 110), 4)
    rows = [('CHICKEN TENDER SUB', '$14.99', (226, 30, 40)), ('ITALIAN SUB', '$15.49', (14, 44, 54)),
            ('HALF A SUB', '$11.99', (14, 44, 54)), ('SUB-SIZED SUB', '$13.99', (14, 44, 54))]
    for i, (a, b, c) in enumerate(rows):
        y = y0 + 34 + i * 20
        wtext(Wd, a, x0 + 22, y, c, 3)
        wb = wtext_w(b, 3)
        wtext(Wd, b, x1 - 22 - wb, y, c, 3)
        xa = x0 + 22 + wtext_w(a, 3) + 8
        for xx in range(xa, x1 - 30 - wb, 9): Wd[y + 11:y + 14, xx:xx + 3] = (150, 150, 140)
    t = '*PRICES MAY VARY. UP.'
    wtext(Wd, t, (x0 + x1 - wtext_w(t, 2)) // 2, y1 - 14, (226, 30, 40), 2)
    sx0, sy0, sx1, sy1 = 929, 262, 996, 286                       # the scale's LCD
    Wd[sy0:sy1, sx0:sx1] = (30, 52, 40)
    wtext(Wd, '18.2LB', sx0 + 4, sy0 + 2, (140, 255, 160), 1)
    wtext(Wd, '$72.80', sx0 + 4, sy0 + 10, (140, 255, 160), 2)


class ST_res_guard:
    def __enter__(s): s.k = ST.PX[0]; return s
    def __exit__(s, *a): ST.set_px(s.k)


def bake_hospital(Wd):
    x0, y0, x1, y1 = 456, 92, 846, 150
    Wd[y0:y1, x0:x1] = (246, 246, 238)
    t = 'BILLING - CASHIER'
    wtext(Wd, t, (x0 + x1 - wtext_w(t, 3)) // 2, y0 + 8, (14, 44, 54), 3)
    t = 'SUNSHINE GENERAL - PAY HERE'
    wtext(Wd, t, (x0 + x1 - wtext_w(t, 2)) // 2, y0 + 34, (226, 34, 52), 2)


def bake_vet(Wd):
    x0, y0, x1, y1 = 634, 92, 888, 258                            # the blank poster: the MICROCHIP SPECIAL (the clue)
    Wd[y0:y1, x0:x1] = (255, 250, 236)
    Wd[y0:y0 + 34, x0:x1] = (255, 140, 60)
    for i, (t, k, c, dy) in enumerate((('MICROCHIP', 4, (255, 255, 255), 6), ('SPECIAL!', 4, (226, 34, 52), 46), ('NEVER LOSE', 2, (14, 44, 54), 84),
                                        ('YOUR BEST', 2, (14, 44, 54), 100), ('FRIEND!', 2, (14, 44, 54), 116), ('$0 TODAY*', 3, (40, 150, 90), 136))):
        wtext(Wd, t, (x0 + x1 - wtext_w(t, k)) // 2, y0 + dy, c, k)
    wtext(Wd, '*SCAN EXTRA', x1 - wtext_w('*SCAN EXTRA', 1) - 6, y1 - 9, (226, 34, 52), 1)
    t = 'DR. PAWS'
    wtext(Wd, t, 1000, 40, (226, 34, 52), 4)


BOOTH_SIGN = ['GATOR JERKY', 'BOILED PEANUTS', 'FIREWORKS']    # E05 turns the booth into the FWC python-bounty window


def bake_booth(Wd):
    x0, y0, x1, y1 = 448, 196, 832, 266
    Wd[y0:y1, x0:x1] = (240, 226, 190)
    for i, t in enumerate(BOOTH_SIGN):
        wtext(Wd, t, (x0 + x1 - wtext_w(t, 3)) // 2, y0 + 6 + i * 21, [(226, 34, 52), (14, 44, 54), (255, 120, 40)][i], 3)


BAKE = dict(yard=bake_yard, store=bake_store, aisle=bake_aisle, deli=bake_deli, hospital=bake_hospital, vet=bake_vet, booth=bake_booth)


def world_baked(name):
    key = name + '+'
    if key not in _W:
        Wd = world(name).copy()
        if name in BAKE: BAKE[name](Wd)
        _W[key] = Wd
    return _W[key]
