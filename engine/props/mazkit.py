"""«Мазутыч» episode kit: speaker colours, dusk lights, worlds (xAI backgrounds + code-painted signs: АЗС «ГАЗПРОПАЛ», «БЕНЗИНА НЕТ»,
the refinery plan banner), the series hook title (oil-slick gradient + crude-oil outline with drips), overlays pass, flare / exhaust FX.
Shot compositing reuses props/chikit.shot (generic: world view + direct actors + fx + vignette)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P
import stage as ST
from stage import Light, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from props import bytfx as B
from props import chikit as CK

SLUG = 'mazutych'
COL = dict(maz=(255, 156, 40), zoya=(255, 120, 200), wheel=(90, 230, 255), boss=(255, 230, 80), tolik=(120, 255, 140), zoyam=(255, 120, 200))
INK = (30, 20, 16)
SLICK = ((210, 90, 230), (90, 220, 230), (255, 214, 90))      # oil-slick: purple -> teal -> gold
def _anchor_out(a, v, name):
    sp = a.last
    px, py = sp.anchors[name]
    ox, oy = v.opt(a.wx, a.wy)
    sc = a.scale(v)
    if a.pin:
        qx, qy = sp.anchors[a.pin]
        ox -= (-qx if a.flip else qx) * sc; oy += qy * sc
    return ox + (-px if a.flip else px) * sc, oy - py * sc, sc


def say_waves(big, x, y, t, k, sc, col=(90, 230, 255)):
    """«it is the wheel who speaks»: pixel sound-wave arcs ))) and ((( flying out of its display, beating with the voice"""
    if k <= 0.05: return
    H, W = big.shape[:2]
    r_max = max(230.0, sc * 30.0)
    r0 = max(44.0, sc * 6.0)
    th = max(12.0, sc * 1.4)
    x0, x1 = int(max(0, x - r_max - th)), int(min(W, x + r_max + th))
    y0, y1 = int(max(0, y - r_max - th)), int(min(H, y + r_max + th))
    if x0 >= x1 or y0 >= y1: return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    dx, dy = xx - x, yy - y
    rr = np.hypot(dx, dy)
    ang = np.arctan2(dy, dx)
    side = (np.abs(ang) < 0.7) | (np.abs(np.abs(ang) - math.pi) < 0.7)
    q = max(4, int(th // 2))                                                   # chunky pixels like the sprites
    blk = ((xx // q) + (yy // q)) % 1 == 0
    reg = big[y0:y1, x0:x1]
    for i in range(3):
        ph = (t * 2.4 + i / 3.0) % 1.0
        r = r0 + (r_max - r0) * ph
        a = (1.0 - ph * 0.85) * min(1.0, 0.55 + k)
        ring = side & blk & (np.abs(rr - r) < th / 2)
        edge = side & (np.abs(rr - r) < th / 2 + 4) & ~ring
        reg[edge] = (reg[edge] * (1 - 0.6 * a) + np.array(INK) * 0.6 * a).astype(np.uint8)
        reg[ring] = (reg[ring] * (1 - a) + np.array(col) * a).astype(np.uint8)


def wheel_says(big, v, acts, t):
    """for every actor with a talking monowheel (maz(wheel_talk=..) / monowheel_solo(talk=..)) draw the sound waves"""
    from props import mazcast as MC
    for a in acts:
        P = getattr(a, 'P', None)
        if not P or not hasattr(a, 'last'): continue
        k = P.get('wheel_talk', 0.0) if a.fn is MC.maz else P.get('talk', 0.0) if a.fn is MC.monowheel_solo else 0.0
        if k <= 0.05 or P.get('dead') or P.get('face') == 'dead' or (a.fn is MC.maz and not P.get('ride', True)): continue
        if 'screen' not in a.last.anchors: continue
        x, y, sc = _anchor_out(a, v, 'screen')
        say_waves(big, x, y, t, k, sc)


def shot(world, light, cx, cy, Z, acts=(), fx_=None, t=0.0, **kw):
    """chikit.shot + the talking-wheel waves (drawn after the actors, before the episode's own fx)"""
    def f(big, v):
        tt = t
        for a in acts:
            if getattr(a, 'P', None) and 't' in a.P: tt = a.P['t']; break
        wheel_says(big, v, acts, tt)
        if fx_: fx_(big, v)
    return CK.shot(world, light, cx, cy, Z, acts=acts, fx_=f, t=t, **kw)
J, hit = CK.J, CK.hit

# ---------------------------------------------------------------- lights: dusk, the flare is the key (upper right)
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_dusk(v, lamps=()):
    return Light(amb=(1.02, 0.90, 0.96), keys=_keys(v, lamps), rim=(1, -0.45, (255, 168, 90), 0.45), grad=(1.06, 0.88))


HW_LAMPS = ((665, 200, 700, (255, 150, 70), 0.35), (1000, 380, 420, (255, 214, 140), 0.35))
GATE_LAMPS = ((1110, 60, 900, (255, 150, 60), 0.45), (300, 420, 420, (255, 200, 120), 0.40), (1140, 330, 380, (255, 200, 120), 0.35))
def light_hw(v): return light_dusk(v, HW_LAMPS)
def light_gate(v): return light_dusk(v, GATE_LAMPS)
def light_win(v):
    return Light(amb=(1.05, 0.96, 0.86), keys=_keys(v, ((640, 200, 700, (255, 210, 130), 0.35),)), rim=(1, -0.3, (255, 190, 120), 0.35),
                 grad=(1.04, 0.92))


# ---------------------------------------------------------------- worlds
_W = {}


def _font(sz): return ImageFont.truetype(P.FONT_PX, sz)


def _text(d, xy, txt, sz, fill, anchor='mm', stroke=0, sfill=INK):
    d.text(xy, txt, font=_font(sz), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)


def world(name):
    if name in _W: return _W[name]
    arr = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png')
    im = Image.fromarray(arr); d = ImageDraw.Draw(im); d.fontmode = '1'
    if name == 'highway_azs':
        # cardboard «БЕНЗИНА НЕТ» taped over the empty price board
        d.polygon([(1156, 118), (1240, 114), (1238, 204), (1158, 207)], fill=(196, 160, 112))
        d.line([(1156, 118), (1240, 114), (1238, 204), (1158, 207), (1156, 118)], fill=(120, 90, 60), width=2)
        for x, y in ((1160, 116), (1232, 112)): d.rectangle([x, y, x + 10, y + 4], fill=(220, 220, 200))   # tape
        _text(d, (1198, 146), 'БЕНЗИНА', 11, (196, 30, 36))
        _text(d, (1198, 176), 'НЕТ', 22, (196, 30, 36))
        d.line([(1168, 194), (1228, 191)], fill=(196, 30, 36), width=2)
        # canopy fascia «ГАЗПРОПАЛ» with a gone-out blue flame
        d.rectangle([944, 254, 1124, 282], fill=(236, 236, 230)); d.rectangle([944, 254, 1124, 282], outline=(40, 90, 200), width=2)
        _text(d, (1042, 268), 'ГАЗПРОПАЛ', 12, (40, 90, 200))
        d.polygon([(950, 278), (962, 278), (959, 268), (956, 262), (952, 269)], fill=(60, 120, 230))
        d.line([(957, 260), (955, 256), (958, 252)], fill=(170, 170, 176), width=1)
        # pump screens: «---»
        for x in (905, 985): _text(d, (x, 409), '---', 7, (255, 80, 60))
    if name == 'refinery_gate':
        d.rectangle([462, 116, 838, 238], fill=(232, 226, 206))
        d.rectangle([462, 116, 838, 238], outline=(180, 40, 40), width=4)
        _text(d, (650, 140), 'ПЛАН ПО БЕНЗИНУ', 18, (180, 30, 34))
        _text(d, (650, 224), 'ЗАВОД «ФАКЕЛ ТРУДА»', 9, (60, 50, 60))
        # factory loudspeaker horn on the banner frame
        d.polygon([(860, 92), (896, 76), (900, 112), (862, 104)], fill=(150, 150, 140), outline=INK)
        d.rectangle([852, 90, 864, 106], fill=(110, 110, 104), outline=INK)
        # checkpoint sign
        d.rectangle([150, 372, 330, 386], fill=(40, 60, 120)); _text(d, (240, 379), 'ПРОХОДНАЯ', 9, (240, 240, 230))
    if name == 'assembly_hall':
        _text(d, (692, 112), 'СЛАВА НЕФТЯНИКАМ!', 16, (120, 20, 24))
        d.rectangle([1162, 312, 1244, 404], fill=(150, 30, 34))                     # «Доска почёта»
        _text(d, (1203, 324), 'ДОСКА', 8, (250, 220, 120)); _text(d, (1203, 336), 'ПОЧЁТА', 8, (250, 220, 120))
        for i in range(3):
            for j in range(2):
                x, y = 1170 + i * 25, 348 + j * 27
                d.rectangle([x, y, x + 17, y + 21], fill=(220, 214, 196), outline=(250, 220, 120))
                d.ellipse([x + 4, y + 3, x + 13, y + 13], fill=(120, 100, 90))
        d.rectangle([494, 404, 560, 426], fill=(236, 236, 230), outline=(40, 90, 200))   # podium plate
        _text(d, (527, 415), 'ГАЗПРОПАЛ', 7, (40, 90, 200))
    _W[name] = np.array(im)
    return _W[name]


def plan_banner(big, v, pct, flip=None):
    """the plan number on the gate banner, a split-flap flip (flip 0..1) between pct-1 and pct"""
    img = Image.new('RGBA', (240, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    k = 1.0 if flip is None else flip
    txt = f'{pct - 1}%' if k <= 0 else f'{pct}%' if k >= 1 else (f'{pct - 1}%' if k < 0.5 else f'{pct}%')
    _text(d, (120, 36), txt, 44, (200, 30, 36), stroke=0)
    a = np.array(img)
    if 0 < k < 1:                                                       # squash vertically mid-flip
        s = abs(math.cos(k * math.pi))
        h = max(2, int(70 * s)); a = np.array(Image.fromarray(a).resize((240, h), Image.NEAREST))
        pad = (70 - h) // 2; full = np.zeros((70, 240, 4), np.uint8); full[pad:pad + h] = a; a = full
    rgb = np.zeros((70, 240, 4), np.uint8); rgb[..., :3] = a[..., :3]; rgb[..., 3] = (a[..., 3] > 127) * 255
    ST.blit_world(big, v, rgb, 530, 152)


# ---------------------------------------------------------------- FX
def flare(big, v, t, x, y, k=1.0, r=1.0):
    """the refinery flare: a living flame + glow above the stack top (world x, y)"""
    ox, oy = v.opt(x, y)
    fx.glow(big, ox, oy - 20 * v.Z * r, 260 * v.Z * k * r, (255, 140, 50), 0.55 * k)
    rng = np.random.default_rng(int(t * 24))
    for i in range(int(14 * k)):
        ph = (t * 3.0 + i * 0.13) % 1.0
        px = ox + (rng.random() - 0.5) * 18 * v.Z * r + math.sin(t * 7 + i) * 6 * v.Z * r
        py = oy - ph * 90 * v.Z * k * r
        rr = (1 - ph) * 16 * v.Z * r * k + 3
        col = (255, 240, 160) if ph < 0.25 else (255, 170, 60) if ph < 0.6 else (220, 80, 40)
        x0, x1, y0, y1 = int(px - rr), int(px + rr), int(py - rr), int(py + rr)
        x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(OUT_W, x1), min(OUT_H, y1)
        if x0 < x1 and y0 < y1:
            s = 9                                                          # chunky square pixels
            big[y0 - y0 % s:y1 - y1 % s, x0 - x0 % s:x1 - x1 % s] = col


def exhaust(big, v, t, x, y, n=5, col=(70, 64, 70), rise=60):
    for i in range(n):
        ph = (t * 1.6 + i / n) % 1.0
        ox, oy = v.opt(x - ph * 40, y - ph * rise)
        B.puff(big, ox, oy, (10 + 26 * ph) * 3 * v.Z, 0.55 * (1 - ph), col)


def dust_trail(big, v, t, x, y, n=6, col=(176, 150, 120)):
    for i in range(n):
        ph = (t * 3.0 + i / n) % 1.0
        ox, oy = v.opt(x - ph * 60, y - ph * 14)
        B.puff(big, ox, oy, (6 + 20 * ph) * 3 * v.Z, 0.5 * (1 - ph), col)


def confetti(big, t, t0, n=160, seed=4):
    if t < t0: return
    r = np.random.default_rng(seed)
    cols = [(255, 60, 80), (255, 220, 60), (80, 220, 255), (120, 255, 120), (255, 140, 220)]
    u = t - t0
    for i in range(n):
        x0 = r.random() * OUT_W; vy = 260 + r.random() * 380; ph = r.random() * 6
        x = x0 + math.sin(u * 3 + ph) * 60
        y = -60 + (u * vy + r.random() * 300) - 300
        if 0 <= y < OUT_H - 16 and 0 <= x < OUT_W - 16:
            w = 18 if int((u * 8 + ph) % 2) else 8
            big[int(y):int(y) + 14, int(x):int(x) + w] = cols[i % len(cols)]


def wind_lines(big, t, k=1.0, n=26, seed=0):
    """horizontal wind streaks (riding): thin light lines streaming to the left"""
    r = np.random.default_rng(seed)
    for i in range(int(n * k)):
        y = int(r.random() * OUT_H); sp = 1800 + r.random() * 1500; ln = int(80 + r.random() * 260)
        x = int(OUT_W - ((t * sp + r.random() * 4000) % (OUT_W + 600)))
        a, b = max(0, x), min(OUT_W, x + ln)
        if a < b: big[y:y + 5, a:b] = (big[y:y + 5, a:b] * 0.45 + 140).astype(np.uint8)


# ---------------------------------------------------------------- hook title + overlays
def _dil(m, r):
    d = m.copy()
    for dx in range(-r, r + 1, 2):
        for dy in range(-r, r + 1, 2):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def hook_title(lines, size=64, width=OUT_W, drips=True):
    """Press Start 2P, oil-slick stepped gradient (purple -> teal -> gold), thick crude-oil outline with drips"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 52) + 60, width, 4), np.uint8)
    y = 20
    rng = np.random.default_rng(7)
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 50), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 16 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        dil = _dil(m, 10)
        if drips:                                                         # oil drips from the bottom of the outline
            rows = np.where(dil.any(1))[0]; yb = rows[-1]
            cols = np.where(dil[yb])[0]
            for c in cols[::max(1, len(cols) // 6)][1:-1]:
                ln = int(8 + rng.random() * 22)
                dil[yb:min(dil.shape[0], yb + ln), c - 4:c + 5] = True
        reg = out[y:y + m.shape[0]]
        reg[dil] = INK + (255,)
        rows = np.where(m.any(1))[0]; r0, r1 = rows[0], rows[-1]
        xs = np.arange(width)
        for yy in range(m.shape[0]):
            k = (yy - r0) / max(1, r1 - r0)
            band = (k * 3 + (xs / width) * 1.2) % 3                         # diagonal iridescent bands
            colsrow = np.where(band[:, None] < 1, SLICK[0], np.where(band[:, None] < 2, SLICK[1], SLICK[2]))
            mm = m[yy]
            reg[yy][mm, :3] = colsrow[mm]; reg[yy][mm, 3] = 255
        reg[m & ~np.roll(m, 6, 0)] = (255, 255, 240, 255)
        y += th + 52
    return out


class Show:
    def __init__(s, epi, n, hook, hook_t=(0.10, 2.6), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330, hook_y=150, total=6,
                 hook_size=60):
        s.epi = epi
        s.badge = O.make_badge(f'СЕЗОН 1 • СЕРИЯ {n}/{total}')
        s.hook = hook_title(hook, hook_size) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default

    def apply(s, big, t, shot_):
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        O.overlay(big, s.badge, 36, 96, 1.0)
        if s.hook is not None and s.hook_t[0] <= t < s.hook_t[1]:
            k = min(1.0, (t - s.hook_t[0]) / 0.1) * (1 - sm((t - (s.hook_t[1] - 0.2)) / 0.2))
            O.overlay(big, s.hook, 0, s.hook_y, k)
        s.epi.captions.draw(big, t, s.cap_y.get(shot_, s.cap_default))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)
