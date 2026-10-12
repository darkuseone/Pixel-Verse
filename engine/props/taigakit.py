"""«Прохор. Таёжные лайфхаки» episode kit: speaker colours, winter lights, worlds (xAI backgrounds + taigadecor), the series title
(«костёр» fill + snow caps + icicles), the blog-camera frame, breath steam, fire, the overlays pass and a close-up helper.
Shot compositing reuses props/chikit.shot (world view + direct actors + fx + vignette).
Coordinates: world px of the xAI backgrounds (1280x720); output 1080x1920."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paths as P
import stage as ST
from stage import Light, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from props import chikit as CK
from props import taigapix as TX
from props import taigacast as C
from props import taigadecor as DEC
from props import decals as D

SLUG = 'prokhor'
COL = dict(prokhor=(255, 128, 96), bear=(150, 220, 255))
INK = TX.INK
FIRE = ((255, 236, 110), (255, 150, 40), (226, 50, 40))       # title fill: yellow (top) -> orange -> red (bottom)
J, hit = CK.J, CK.hit


def A(fn, wx, wy, s, flip=False, pin=None, **kw):
    return TX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, **kw)


def wpt(v, ox, oy):
    """output px -> world px"""
    return v.X0 + ox / (3 * v.Z), v.Y0 + (oy / 3 - v.oy) / v.Z


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


# ---------------------------------------------------------------- lights (low sun + cold ambience)
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_izba(v):
    return Light(amb=(0.92, 0.96, 1.08), keys=_keys(v, ((870, 260, 620, (255, 180, 110), 0.40),)), rim=(1, -0.3, (255, 170, 100), 0.40),
                 grad=(1.02, 0.92))


def light_taiga(v):
    return Light(amb=(1.00, 0.96, 1.04), keys=_keys(v, ((950, 200, 900, (255, 170, 110), 0.30),)), rim=(1, -0.35, (255, 180, 120), 0.45),
                 grad=(1.04, 0.94))


def light_taiga2(v):
    return Light(amb=(1.00, 0.96, 1.04), keys=_keys(v, ((370, 280, 900, (255, 176, 110), 0.32),)), rim=(-1, -0.35, (255, 186, 120), 0.45),
                 grad=(1.04, 0.94))


def light_porch(v):
    return Light(amb=(1.0, 0.96, 1.02), keys=_keys(v, ((930, 300, 900, (255, 176, 110), 0.30), (210, 240, 400, (255, 200, 120), 0.25))),
                 rim=(1, -0.35, (255, 186, 120), 0.45), grad=(1.04, 0.94))


def light_den2(v, k=0.0):
    keys = [(700, 60, 520, (255, 210, 140), 0.40)]
    return Light(amb=(1.02, 0.92, 0.82), keys=_keys(v, keys), rim=(-1, -0.3, (150, 190, 255), 0.25), grad=(1.0, 0.88))


def light_den(v, lamp=0.0):
    keys = [(790, 120, 380, (170, 200, 255), 0.25)]
    if lamp > 0: keys.append((930, 520, 520, (255, 220, 140), 0.45 * lamp))
    return Light(amb=(1.02, 0.90, 0.80), keys=_keys(v, keys), rim=(-1, -0.3, (150, 190, 255), 0.30), grad=(1.0, 0.86))


# ---------------------------------------------------------------- worlds
_W = {}


def world(name):
    if name not in _W:
        W = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png')
        DEC.dress(name, W)
        _W[name] = W
    return _W[name]


def dof(big, r=6):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


# ---------------------------------------------------------------- FX
def puff(big, cx, cy, r, a, col=(236, 244, 255), q=9):
    """a chunky round puff (square pixels of q output px)"""
    x0, x1, y0, y1 = int(max(0, cx - r)), int(min(OUT_W, cx + r)), int(max(0, cy - r)), int(min(OUT_H, cy + r))
    if x0 >= x1 or y0 >= y1 or a <= 0: return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    m = (((xx // q) * q + q / 2 - cx) ** 2 + ((yy // q) * q + q / 2 - cy) ** 2) <= r * r
    reg = big[y0:y1, x0:x1]
    reg[m] = (reg[m] * (1 - a) + np.array(col) * a).astype(np.uint8)


def breath(big, x, y, t, k=1.0, dirx=1.0, scale=1.0, period=1.6):
    """breath steam in the frost: puffs out of the mouth (output px), drifting up and forward"""
    for i in range(3):
        ph = (t / period + i / 3) % 1.0
        r = (14 + 50 * ph) * scale
        puff(big, x + dirx * (20 + 120 * ph) * scale, y - 30 * ph * scale, r, 0.55 * k * (1 - ph), q=max(6, int(8 * scale)))


def fire(big, x, y, t, w=120, h=200, k=1.0, seed=0):
    """a small living flame (output px base centre)"""
    fx.glow(big, x, y - h * 0.3, h * 1.6, (255, 150, 60), 0.45 * k)
    rng = np.random.default_rng(int(t * 24) + seed)
    for i in range(int(18 * k)):
        ph = (t * 3.2 + i * 0.11) % 1.0
        px = x + (rng.random() - 0.5) * w * (1 - ph * 0.6)
        py = y - ph * h
        rr = (1 - ph) * w * 0.22 + 6
        col = (255, 244, 170) if ph < 0.25 else (255, 170, 60) if ph < 0.6 else (220, 70, 40)
        s = 12
        x0, x1, y0, y1 = int(max(0, px - rr)), int(min(OUT_W, px + rr)), int(max(0, py - rr)), int(min(OUT_H, py + rr))
        if x0 < x1 and y0 < y1: big[y0 - y0 % s:y1 - y1 % s, x0 - x0 % s:x1 - x1 % s] = col


def sweat_glow(big, k):
    """warm sauna tint over the whole frame (bliss in the den)"""
    if k <= 0: return
    big[:] = np.clip(big * np.array([1 + 0.10 * k, 1 + 0.02 * k, 1 - 0.10 * k]) + np.array([14, 4, 0]) * k, 0, 255).astype(np.uint8)


def frost_edges(big, k=1.0, seed=1):
    """hoarfrost creeping in from the frame edges (cold shots)"""
    if k <= 0: return
    h, w = big.shape[:2]
    yy, xx = np.mgrid[0:h:12, 0:w:12]
    d = np.minimum(np.minimum(xx, w - xx), np.minimum(yy, h - yy)).astype(np.float32)
    rng = np.random.default_rng(seed)
    n = rng.random(d.shape)
    m = d < (90 + 90 * n) * k
    for (r, c) in zip(*np.nonzero(m)):
        y, x = r * 12, c * 12
        big[y:y + 12, x:x + 12] = (big[y:y + 12, x:x + 12] * 0.35 + np.array((230, 242, 255)) * 0.65).astype(np.uint8)


def snow_burst(big, x, y, t, t0, n=40, seed=3, col=(240, 246, 255)):
    """a snow splash (someone lands in a drift) at output (x, y) from t0"""
    u = t - t0
    if u < 0 or u > 1.2: return
    r = np.random.default_rng(seed)
    for i in range(n):
        a = -math.pi * r.random(); sp = 500 + 900 * r.random()
        px = x + math.cos(a) * sp * u; py = y + math.sin(a) * sp * u + 1400 * u * u
        q = 14 + int(r.random() * 14)
        if 0 <= px < OUT_W - q and 0 <= py < OUT_H - q: big[int(py):int(py) + q, int(px):int(px) + q] = col


# ---------------------------------------------------------------- hook title: «костёр» fill, snow caps, icicles
def _dil(m, r, step=2):
    d = m.copy()
    for dx in range(-r, r + 1, step):
        for dy in range(-r, r + 1, step):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def hook_title(lines, size=72, width=OUT_W):
    """Press Start 2P, campfire stepped gradient (yellow top -> orange -> red bottom), thick spruce ink outline,
    white snow caps on the tops of the letters, icicles hanging from the outline"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 64) + 70, width, 4), np.uint8)
    y = 26
    rng = np.random.default_rng(11)
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 60), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 22 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        dil = _dil(m, 11)
        rows = np.where(dil.any(1))[0]; yb = rows[-1]
        cols = np.where(dil[yb])[0]
        ice = np.zeros_like(dil)
        for c in cols[::max(1, len(cols) // 9)][1:-1]:                   # icicles: tapering spikes under the outline
            ln = int(10 + rng.random() * 26)
            for k in range(ln):
                hw = max(1, int(5 * (1 - k / ln)))
                if yb + k < ice.shape[0]: ice[yb + k, c - hw:c + hw] = True
        reg = out[y:y + m.shape[0]]
        reg[dil] = INK + (255,)
        reg[ice] = (200, 230, 255, 255)
        rr = np.where(m.any(1))[0]; r0, r1 = rr[0], rr[-1]
        for yy in range(r0, r1 + 1):
            k = (yy - r0) / max(1, r1 - r0)
            c = FIRE[0] if k < 0.36 else FIRE[1] if k < 0.70 else FIRE[2]
            mm = m[yy]; reg[yy][mm, :3] = c; reg[yy][mm, 3] = 255
        cap = m & ~np.roll(m, 8, 0)                                      # snow caps on the tops of the strokes
        cap = _dil(cap, 3, 1) & (dil | m)
        reg[cap & (np.arange(m.shape[0])[:, None] < r0 + (r1 - r0) * 0.5)] = (250, 252, 255, 255)
        y += th + 64
    return out


def title_trim(a):
    m = a[..., 3] > 0
    r = np.where(m.any(1))[0]; c = np.where(m.any(0))[0]
    return a[r[0]:r[-1] + 1, c[0]:c[-1] + 1]


# ---------------------------------------------------------------- the blog camera frame (his phone on a ski pole)
def blog_frame(big, t, k=1.0, label='ТАЙГА-ЛАЙФХАК', n=None):
    """phone-camera UI over the frame: corner brackets, blinking ● REC + timer, the channel name, a dying battery"""
    if k <= 0: return
    W_, H_ = big.shape[1], big.shape[0]
    c = (255, 255, 255)
    L, T = 70, 180
    for (x, y, sx, sy) in ((L, T + 120, 1, 1), (W_ - L, T + 120, -1, 1), (L, H_ - 300, 1, -1), (W_ - L, H_ - 300, -1, -1)):
        big[min(y, y + sy * 80):max(y, y + sy * 80), min(x, x + sx * 12):max(x, x + sx * 12)] = c
        big[min(y, y + sy * 12):max(y, y + sy * 12), min(x, x + sx * 80):max(x, x + sx * 80)] = c
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    f = O.pfont(30)
    if int(t * 2) % 2 == 0: d.ellipse([L + 10, T + 150, L + 46, T + 186], fill=(240, 40, 40))
    d.text((L + 60, T + 154), f'REC 00:{int(t) % 60:02d}', font=f, fill=c, stroke_width=3, stroke_fill=(0, 0, 0))
    big[:] = np.array(im)
    bx, by = W_ - L - 120, T + 150                                       # a dying battery: one red bar of four
    big[by - 4:by + 40, bx - 4:bx + 104] = (0, 0, 0); big[by:by + 36, bx:bx + 100] = (255, 255, 255)
    big[by + 4:by + 32, bx + 4:bx + 96] = (0, 0, 0); big[by + 8:by + 28, bx + 8:bx + 26] = (255, 70, 60)
    big[by + 10:by + 26, bx + 104:bx + 114] = (255, 255, 255)


# ---------------------------------------------------------------- overlays pass
class Show:
    def __init__(s, epi, n, hook, hook_t=(0.10, 2.2), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330, hook_y=330,
                 total=6, hook_size=76):
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
            if ST.LOG[0] is not None:
                ST.log('title', bbox=(0, s.hook_y, OUT_W, s.hook_y + s.hook.shape[0]))
        s.epi.captions.draw(big, t, s.cap_y.get(shot_, s.cap_default))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


def st(text, fg=(255, 236, 120), size=60):
    return O.sticker(text, fg=fg, size=size)


# ---------------------------------------------------------------- shot helpers
def shot(world_, light, cx, cy, Z, acts=(), fx_=None, pre=None, sx=180, sy=320, vig=0.26, t=0.0):
    return CK.shot(world_, light, cx, cy, Z, acts=acts, fx_=fx_, pre=pre, sx=sx, sy=sy, vig=vig, t=t)


def cu(fn, t, world_, cx, cy, Z, sz, head=(540, 960), light=None, blur=0, extra_fx=None, pre_fx=None, acts_before=(), acts_after=(),
       flip=False, **kw):
    """close-up of any hero: head pinned at an output point (sz output px per sprite px); the world behind is zoomed less (CU rule)
    and optionally soft (blur)"""
    v0 = view_at(world_, cx, cy, Z, 180, 320)
    hx, hy = wpt(v0, head[0], head[1])
    a = A(fn, hx, hy, sz, pin='head', t=t, flip=flip, **kw)
    def pre(big, v):
        if pre_fx: pre_fx(big, v)
        if blur: big[:] = dof(big, blur)
    def f(big, v):
        if extra_fx: extra_fx(big, v, a)
    big = shot(world_, light, cx, cy, Z, acts=list(acts_before) + [a] + list(acts_after), pre=pre, fx_=f)
    return big, a


# ---------------------------------------------------------------- blogger / phone helpers (E02+)
def handheld(t, amp=1.0):
    """selfie camera wobble (output px)"""
    return (math.sin(t * 2.3) * 10 + math.sin(t * 5.1) * 4) * amp, (math.sin(t * 1.7 + 1) * 8 + math.sin(t * 6.3) * 3) * amp


def shift(big, dx, dy):
    if not dx and not dy: return big
    return np.roll(np.roll(big, int(dy), 0), int(dx), 1)


def _star(d, cx, cy, r, fill, outline):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=fill, outline=outline)
    if fill is None:
        for k in range(len(pts)): d.line([pts[k], pts[(k + 1) % len(pts)]], fill=outline, width=5)


def phone_card(big, t, t0, t1, lines, icon='ДЯ', icon_col=(150, 40, 150), y=640, stars=None, colors=None):
    """a phone notification card popping in (t0..t1): app icon + fitted text lines (+ optional star rating, filled = stars)"""
    if not (t0 <= t < t1): return
    k = min(1.0, (t - t0) / 0.15) * (1 - sm((t - (t1 - 0.15)) / 0.15))
    W_, H_ = 940, 150 + 40 * (len(lines) - 1) + (110 if stars is not None else 0)
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 36, fill=(250, 250, 252, 245), outline=(30, 30, 40, 255), width=6)
    d.rounded_rectangle([28, 28, 128, 128], 24, fill=icon_col + (255,))
    f = O.pfont(34); bb = f.getbbox(icon)
    d.text((78 - (bb[2] - bb[0]) / 2 - bb[0], 78 - (bb[3] - bb[1]) / 2 - bb[1]), icon, font=f, fill=(255, 255, 255))
    y_ = 34
    for i, ln in enumerate(lines):
        sz = 30 if i == 0 else 24
        f = O.pfont(sz)
        while f.getlength(ln) > W_ - 190 and sz > 12: sz -= 2; f = O.pfont(sz)
        d.text((156, y_), ln, font=f, fill=(colors[i] if colors else ((30, 30, 40) if i == 0 else (90, 90, 100))))
        y_ += sz + 18
    if stars is not None:
        for i in range(5):
            _star(d, 230 + i * 120, H_ - 66, 44, (255, 196, 40) if i < stars else None, (60, 60, 70))
    a = np.array(im)
    if k < 1:
        s = 0.6 + 0.4 * k
        a = np.array(Image.fromarray(a).resize((max(1, int(W_ * s)), max(1, int(H_ * s))), Image.NEAREST))
    O.overlay(big, a, (OUT_W - a.shape[1]) // 2, int(y - a.shape[0] / 2), 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=((OUT_W - a.shape[1]) // 2, int(y - a.shape[0] / 2), (OUT_W + a.shape[1]) // 2, int(y + a.shape[0] / 2)))
