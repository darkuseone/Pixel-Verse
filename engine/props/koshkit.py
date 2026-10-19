"""«Кощей из панельки» episode kit: speaker colours, bulb lights, worlds (xAI backgrounds + koshdecor), the series title
(«хохломское золото»: stepped gold fill, black-lacquer outline, cinnabar line, green ghost-glow halo), the overlays pass, close-ups,
green «кощеев огонь», glowing eyes in the dark, candles, steam.
Shot compositing reuses props/chikit.shot (world view + direct actors + fx + vignette); generic helpers come from props/taigakit.
Coordinates: world px of the xAI backgrounds (1280x720); output 1080x1920."""
import math
import numpy as np
from PIL import Image, ImageDraw
import paths as P
import stage as ST
from stage import Light, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from props import chikit as CK
from props import koshpix as KX
from props import koshdecor as DEC
from props.taigakit import wpt, aout, dof, puff, handheld, shift, phone_card, title_trim

SLUG = 'koshchei'
COL = dict(koshchei=(120, 255, 140), yaga=(255, 96, 80), kuzmich=(255, 214, 90), galina=(200, 190, 255), gorynych=(170, 236, 110),
           student=(255, 160, 220))
INK = KX.INK
GOLD3 = ((255, 236, 150), (240, 190, 60), (190, 130, 30))      # title fill: light gold (top) -> gold -> dark gold (bottom)
J, hit = CK.J, CK.hit
GREEN = (120, 255, 150)


def A(fn, wx, wy, s, flip=False, pin=None, **kw):
    return KX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, **kw)


# ---------------------------------------------------------------- lights: bare 40 W bulbs, warm; green moon/ghost rim
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_office(v, k=1.0):
    return Light(amb=(1.0, 1.0, 0.96), keys=_keys(v, ((640, 40, 900, (255, 236, 190), 0.30 * k),)), rim=(1, -0.3, (150, 255, 170), 0.25),
                 grad=(1.03, 0.92))


def light_flat(v, k=1.0):
    return Light(amb=(1.0, 0.94, 0.86), keys=_keys(v, ((640, 60, 760, (255, 210, 130), 0.40 * k),)), rim=(-1, -0.3, (150, 255, 170), 0.30),
                 grad=(1.02, 0.88))


def light_stairs(v, k=1.0):
    return Light(amb=(0.98, 0.94, 0.84), keys=_keys(v, ((640, 90, 620, (255, 214, 130), 0.45 * k),)), rim=(1, -0.3, (150, 255, 170), 0.30),
                 grad=(1.0, 0.86))


def light_dark(v, k=0.0):
    """power cut: almost black, the green ghost rim stays"""
    return Light(amb=(0.32 + 0.6 * k, 0.36 + 0.58 * k, 0.34 + 0.5 * k), keys=[], rim=(1, -0.3, (120, 255, 150), 0.55), grad=(1.0, 0.9))


def light_yard(v, k=1.0):
    return Light(amb=(0.92, 0.90, 1.02), keys=_keys(v, ((200, 260, 520, (255, 210, 130), 0.40 * k),)), rim=(1, -0.35, (150, 255, 170), 0.35),
                 grad=(1.02, 0.86))


def light_facade(v, k=1.0):
    return Light(amb=(0.90, 0.92, 1.05), keys=_keys(v, ((640, 300, 700, (255, 220, 140), 0.25 * k),)), rim=(1, -0.3, (150, 255, 170), 0.35),
                 grad=(1.0, 0.9))


# ---------------------------------------------------------------- worlds
_W = {}


def world(name):
    if name not in _W:
        W = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png')
        DEC.dress(name, W)
        _W[name] = W
    return _W[name]


# ---------------------------------------------------------------- FX
def green_fire(big, x, y, t, r=120, k=1.0, seed=0):
    """«кощеев огонь»: a green flickering glow with chunky rising sparks (output px centre)"""
    if k <= 0: return
    fx.glow(big, x, y, r * 2.2, (120, 255, 150), 0.45 * k)
    rng = np.random.default_rng(int(t * 20) + seed)
    for i in range(int(16 * k)):
        ph = (t * 2.4 + i * 0.13) % 1.0
        px = x + (rng.random() - 0.5) * r * 1.4 * (1 - 0.5 * ph); py = y - ph * r * 1.8 + r * 0.4
        q = int(10 + 12 * (1 - ph))
        col = (230, 255, 230) if ph < 0.3 else (120, 255, 150) if ph < 0.7 else (40, 160, 80)
        ix, iy = int(px) // 6 * 6, int(py) // 6 * 6
        if 0 <= ix < OUT_W - q and 0 <= iy < OUT_H - q: big[iy:iy + q, ix:ix + q] = col


def eyes_glow(big, pts, k=1.0, r=26, col=(140, 255, 160)):
    """glowing eyes in the dark: pairs of chunky green dots with a soft glow (output px)"""
    for (x, y) in pts:
        fx.glow(big, x, y, r * 4, col, 0.55 * k)
        q = r // 2 * 2
        big[int(y - q / 2):int(y + q / 2), int(x - q / 2):int(x + q / 2)] = (230, 255, 230)


def darken(big, k):
    """power cut: crush the frame towards black lacquer, keep a hint of green"""
    if k <= 0: return
    big[:] = (big.astype(np.float32) * (1 - 0.86 * k) + np.array((6, 14, 8)) * k).astype(np.uint8)


def candles(big, pts, t, k=1.0):
    """tiny candle flames (output px tips)"""
    rng = np.random.default_rng(int(t * 18))
    for i, (x, y) in enumerate(pts):
        h = 22 + 8 * rng.random()
        fx.glow(big, x, y, 70, (255, 200, 90), 0.22 * k)
        big[int(y - h):int(y), int(x - 5):int(x + 5)] = (255, 200, 80)
        big[int(y - h * 0.6):int(y), int(x - 3):int(x + 3)] = (255, 250, 210)


def steam(big, x, y, t, k=1.0, scale=1.0, period=1.8, dx=0.3):
    for i in range(3):
        ph = (t / period + i / 3) % 1.0
        puff(big, x + dx * 120 * ph * scale, y - 220 * ph * scale, (22 + 60 * ph) * scale, 0.45 * k * (1 - ph), col=(236, 236, 228), q=10)


def vhs(big, t, k=1.0):
    """VHS rewind: horizontal tear bands + noise lines"""
    if k <= 0: return
    rng = np.random.default_rng(int(t * 60))
    for _ in range(int(14 * k)):
        y = int(rng.integers(0, OUT_H - 40)); h = int(rng.integers(6, 40)); dx = int(rng.integers(-80, 80))
        big[y:y + h] = np.roll(big[y:y + h], dx, 1)
    for _ in range(int(40 * k)):
        y = int(rng.integers(0, OUT_H)); big[y:y + 3, :] = (230, 230, 230)


def ticker_text(big, txt, y, size=64, col=(255, 236, 150), k=1.0):
    """a centred title card line («ЧЕРЕЗ ГОД») in the hook style"""
    if k <= 0: return
    t = title_trim(hook_title([txt], size))
    O.overlay(big, t, (OUT_W - t.shape[1]) // 2, y, k)


# ---------------------------------------------------------------- hook title: «хохломское золото»
def _dil(m, r, step=2):
    d = m.copy()
    for dx in range(-r, r + 1, step):
        for dy in range(-r, r + 1, step):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def hook_title(lines, size=76, width=OUT_W):
    """Press Start 2P, stepped gold fill (light gold top -> gold -> dark gold bottom), thick black-lacquer outline with a thin cinnabar
    line inside it, a soft green «кощеев огонь» halo outside, white lacquer glints on the tops of the strokes"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 70) + 70, width, 4), np.uint8)
    y = 30
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 70), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 28 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        red = _dil(m, 5)
        ink = _dil(m, 12)
        halo = _dil(ink, 8, 3)
        reg = out[y:y + m.shape[0]]
        reg[halo & ~ink] = (120, 255, 150, 110)
        reg[ink] = INK + (255,)
        reg[red & ~m] = KX.CINNABAR + (255,)
        rr = np.where(m.any(1))[0]; r0, r1 = rr[0], rr[-1]
        for yy in range(r0, r1 + 1):
            k = (yy - r0) / max(1, r1 - r0)
            c = GOLD3[0] if k < 0.34 else GOLD3[1] if k < 0.70 else GOLD3[2]
            mm = m[yy]; reg[yy][mm, :3] = c; reg[yy][mm, 3] = 255
        cap = m & ~np.roll(m, 5, 0)
        reg[cap & (np.arange(m.shape[0])[:, None] < r0 + (r1 - r0) * 0.4)] = (255, 255, 240, 255)
        y += th + 70
    return out


# ---------------------------------------------------------------- overlays pass
class Show:
    def __init__(s, epi, n, hook, hook_t=(0.10, 2.4), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330, hook_y=300,
                 total=6, hook_size=76, extra=None):
        s.epi = epi
        s.badge = O.make_badge(f'СЕЗОН 1 • СЕРИЯ {n}/{total}')
        s.hook = hook_title(hook, hook_size) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default
        s.extra = extra

    def apply(s, big, t, shot_):
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        O.overlay(big, s.badge, 36, 96, 1.0)
        if s.hook is not None and s.hook_t[0] <= t < s.hook_t[1]:
            k = min(1.0, (t - s.hook_t[0]) / 0.1) * (1 - sm((t - (s.hook_t[1] - 0.2)) / 0.2))
            O.overlay(big, s.hook, 0, s.hook_y, k)
            if ST.LOG[0] is not None:
                ST.log('title', bbox=(0, s.hook_y, OUT_W, s.hook_y + s.hook.shape[0]))
        if s.extra: s.extra(big, t, shot_)
        s.epi.captions.draw(big, t, s.cap_y.get(shot_, s.cap_default))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


def st(text, fg=(255, 220, 110), size=60):
    return O.sticker(text, fg=fg, size=size)


# ---------------------------------------------------------------- shot helpers
def shot(world_, light, cx, cy, Z, acts=(), fx_=None, pre=None, sx=180, sy=320, vig=0.30, t=0.0, back=(), front=()):
    return CK.shot(world_, light, cx, cy, Z, acts=acts, back=back, front=front, fx_=fx_, pre=pre, sx=sx, sy=sy, vig=vig, t=t)


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


def calendar(n):
    """the season counter: a tear-off calendar page «ДО ХЭЛЛОУИНА: N» (decal RGBA)"""
    from props import rusigns as R
    if n == 0:
        return R.plate(30, 34, ['31', 'ОКТЯБРЯ'], bg=(250, 248, 236), fg=(30, 28, 30), border=(60, 50, 44), colors=[KX.CINNABAR, (30, 28, 30)],
                       weights=[1.0, 0.45], stripe=((190, 40, 34), 0.18), pad=1.6)
    return R.plate(30, 34, ['ДО', 'ХЭЛЛОУИНА', str(n)], bg=(250, 248, 236), fg=(30, 28, 30), border=(60, 50, 44),
                   colors=[(30, 28, 30), (30, 28, 30), KX.CINNABAR], weights=[0.35, 0.35, 1.0], stripe=((190, 40, 34), 0.14), pad=1.4)
