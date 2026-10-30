"""«Land of the Fee» episode kit: speaker colours, lights (sunny apartment, strip mall, cold store), worlds (xAI backgrounds + feedecor),
the series title («Dollar Neon»: mint -> aqua -> cyan stepped fill, a thick banknote-green outline, a magenta drop, gold glints), the
banknote plate (series badge / covers), the big Fee-Bee screen insert, FX (feather burst, flying dollars, holy door light, a moth from
the wallet, speed lines), the overlays pass, a close-up helper and the cover maker. Shot compositing reuses props/chikit.shot.
Coordinates: world px of the xAI backgrounds (1280x720); output 1080x1920."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paths as P
import stage as ST
from stage import Light, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
from props import chikit as CK
from props import feepix as FX
from props import feecast as C
from props import feedecor as DEC
from props.dibspix import blit

SLUG = 'land-of-the-fee'
COL = dict(duke=(255, 206, 60), sal=(206, 170, 255), feebee=(130, 255, 200), doris=(255, 186, 150), madison=(255, 150, 200),
           chuck=(170, 220, 255), nurse=(255, 200, 220), officer=(150, 200, 255), rex=(255, 130, 90))
INK = FX.INK
GREEN = (18, 70, 48)                                        # title outline: banknote ink
FILL = ((150, 255, 196), (100, 236, 226), (80, 196, 255))   # mint (top) -> aqua -> cyan (bottom)
MAG = (226, 56, 170)
GOLD = (255, 214, 90)
J, hit = CK.J, CK.hit


def A(fn, wx, wy, s, flip=False, pin=None, **kw):
    return FX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, **kw)


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


# ---------------------------------------------------------------- lights
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_apt(v, alarm=0.0):
    keys = [(880, 220, 700, (255, 226, 160), 0.34), (500, 40, 500, (255, 236, 190), 0.18)]
    return Light(amb=(1.02, 0.99, 0.95), keys=_keys(v, keys), rim=(1, -0.3, (255, 220, 150), 0.32), grad=(1.04, 0.95))


def light_mall(v, alarm=0.0):
    keys = [(640, -100, 1200, (255, 244, 210), 0.30)]
    return Light(amb=(1.04, 1.03, 1.0), keys=_keys(v, keys), rim=(-1, -0.4, (255, 250, 220), 0.30), grad=(1.05, 0.97))


def light_store(v, glow=0.0):
    keys = [(640, 0, 1000, (236, 246, 255), 0.28), (200, 300, 500, (170, 120, 255), 0.18)]
    if glow > 0: keys.append((1060, 300, 700, (255, 240, 190), 0.55 * glow))
    return Light(amb=(1.02, 1.03, 1.05), keys=_keys(v, keys), rim=(1, -0.3, (180, 255, 230), 0.25), grad=(1.04, 0.97))


# ---------------------------------------------------------------- worlds
_W = {}


def world(name):
    if name not in _W:
        Wd = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png')
        DEC.dress(name, Wd)
        _W[name] = Wd
    return _W[name]


def dof(big, r=6):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


# ---------------------------------------------------------------- FX (output space, deterministic in t)
def _quad(big, x, y, w, h, col, a=1.0):
    X0, Y0 = int(max(0, x)), int(max(0, y)); X1, Y1 = int(min(OUT_W, x + w)), int(min(OUT_H, y + h))
    if X0 >= X1 or Y0 >= Y1: return
    reg = big[Y0:Y1, X0:X1]
    reg[:] = (reg * (1 - a) + np.array(col) * a).astype(np.uint8)


def feathers(big, t, t0, cx, cy, n=14, seed=3, spread=520, cols=((248, 246, 238), (98, 62, 38), (246, 244, 236))):
    """a burst of pixel feathers from (cx, cy) at t0: fly out, flutter down, fade"""
    u = t - t0
    if u < 0 or u > 2.2: return
    r = np.random.default_rng(seed)
    for i in range(n):
        a = r.random() * 2 * math.pi; sp_ = spread * (0.5 + r.random() * 0.7)
        x = cx + math.cos(a) * sp_ * (1 - math.exp(-u * 3.2)) + math.sin(u * 5 + i) * 18
        y = cy + math.sin(a) * sp_ * 0.6 * (1 - math.exp(-u * 3.2)) + 140 * u * u
        k = max(0.0, 1 - u / 2.2)
        q = 10 + int(r.random() * 6)
        col = cols[i % len(cols)]
        ang = math.sin(u * 6 + i) * 0.6
        for s_ in range(4):                                             # a feather = 4 stepped blocks along its axis
            _quad(big, x + math.cos(ang) * s_ * q * 0.8, y + math.sin(ang) * s_ * q * 0.8, q, q * (0.7 if s_ in (0, 3) else 1.0), col, k)


def dollars(big, t, t0, cx, cy, n=10, seed=5, up=True):
    """green dollar bills flutter up and out (ka-ching)"""
    u = t - t0
    if u < 0 or u > 1.6: return
    r = np.random.default_rng(seed)
    for i in range(n):
        a = -math.pi / 2 + (r.random() - 0.5) * 2.2
        sp_ = 420 * (0.5 + r.random())
        x = cx + math.cos(a) * sp_ * u
        y = cy + math.sin(a) * sp_ * u + 260 * u * u
        k = max(0.0, 1 - u / 1.6)
        w, h = 66, 32
        _quad(big, x - w / 2, y - h / 2, w, h, (40, 120, 70), k)
        _quad(big, x - w / 2 + 6, y - h / 2 + 6, w - 12, h - 12, (150, 220, 160), k)
        _quad(big, x - 7, y - 9, 14, 18, (40, 120, 70), k)


def holy_light(big, t, t0, cx, cy, k=1.0, w0=180, w1=900):
    """warm divine light pouring from a door: a widening wedge toward the bottom + slow rotating rays"""
    u = t - t0
    if u < 0 or k <= 0: return
    a = min(1.0, u / 0.25) * k
    yy, xx = np.mgrid[0:OUT_H:4, 0:OUT_W:4]
    d = np.abs(xx - cx) - (w0 + (w1 - w0) * np.clip((yy - cy) / 900, 0, 1)) / 2
    beam = np.clip(1 - d / 160, 0, 1) * (yy > cy - 300)
    ray = 0.5 + 0.5 * np.sin(np.arctan2(yy - cy, xx - cx) * 14 + u * 1.5)
    m = (beam * (0.30 + 0.12 * ray) * a)
    m = np.kron(m, np.ones((4, 4)))[:OUT_H, :OUT_W][..., None]
    big[:] = np.clip(big * (1 - m * 0.4) + np.array((255, 246, 210)) * m, 0, 255).astype(np.uint8)


MOTH = ['..X...X..', '.XXX.XXX.', 'XXXXXXXXX', '.XXX.XXX.', '..X...X..']


def moth(big, t, t0, x0, y0, q=10):
    """a little grey moth flaps out of the wallet and wanders up"""
    u = t - t0
    if u < 0 or u > 2.5: return
    x = x0 + math.sin(u * 4) * 60 + u * 80; y = y0 - u * 260
    flap = abs(math.sin(u * 30))
    for r_, row in enumerate(MOTH):
        for c_, ch in enumerate(row):
            if ch != 'X': continue
            if c_ in (0, 8) and flap < 0.4: continue
            _quad(big, x + c_ * q, y + r_ * q * (0.6 + 0.4 * flap), q, q * (0.6 + 0.4 * flap), (150, 140, 130))


def speed_lines(big, t, k=1.0, n=18, seed=2, horizontal=True):
    r = np.random.default_rng(int(t * 20) + seed)
    for _ in range(int(n * k)):
        y = int(r.integers(0, OUT_H)); x = int(r.integers(0, OUT_W)); L = int(r.integers(120, 380))
        if horizontal: _quad(big, x, y, L, 5, (255, 255, 255), 0.55 * k)
        else: _quad(big, x, y, 5, L, (255, 255, 255), 0.55 * k)


def glitch(big, t, k=1.0, seed=0):
    if k <= 0: return
    rng = np.random.default_rng(int(t * 30) + seed)
    for _ in range(int(10 * k)):
        y = int(rng.integers(0, OUT_H - 60)); h = int(rng.integers(12, 70)); dx = int(rng.integers(-90, 90) * k)
        big[y:y + h] = np.roll(big[y:y + h], dx, 1)


# ---------------------------------------------------------------- hook title: «Dollar Neon»
def _dil(m, r, step=2):
    d = m.copy()
    for dx in range(-r, r + 1, step):
        for dy in range(-r, r + 1, step):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def hook_title(lines, size=72, width=OUT_W):
    """Press Start 2P, stepped fill mint (top) -> aqua -> cyan (bottom), a thick banknote-green outline with a hot-magenta drop below,
    gold glints on the tops of the letters (a coin catching the light)"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 64) + 60, width, 4), np.uint8)
    y = 24
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 64), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 22 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        dil = _dil(m, 11)
        drop = np.roll(dil, 11, 0) & ~dil
        reg = out[y:y + m.shape[0]]
        reg[drop] = MAG + (255,)
        reg[dil] = GREEN + (255,)
        rr = np.where(m.any(1))[0]; r0, r1 = rr[0], rr[-1]
        for yy in range(r0, r1 + 1):
            k = (yy - r0) / max(1, r1 - r0)
            c = FILL[0] if k < 0.36 else FILL[1] if k < 0.70 else FILL[2]
            mm = m[yy]; reg[yy][mm, :3] = c; reg[yy][mm, 3] = 255
        cap = m & ~np.roll(m, 6, 0)
        reg[cap & (np.arange(m.shape[0])[:, None] < r0 + (r1 - r0) * 0.4) & (np.arange(m.shape[1])[None, :] % 13 < 5)] = GOLD + (255,)
        gl = m & ~np.roll(m, 4, 1) & (np.arange(m.shape[0])[:, None] > r0 + (r1 - r0) * 0.5)
        reg[gl & (np.arange(m.shape[1])[None, :] % 11 < 2)] = (255, 255, 255, 255)
        y += th + 64
    return out


def title_trim(a):
    m = a[..., 3] > 0
    r = np.where(m.any(1))[0]; c = np.where(m.any(0))[0]
    return a[r[0]:r[-1] + 1, c[0]:c[-1] + 1]


# ---------------------------------------------------------------- banknote plate (series badge / covers / end card)
def banknote(line1, line2, w=640, h=200):
    """a dollar bill: cream paper, a thick money-green frame with a guilloche wave band, corner seals with «$», the series name + episode"""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], fill=GREEN + (255,))
    d.rectangle([8, 8, w - 9, h - 9], fill=(244, 238, 210, 255))
    for k in range(3):                                                                          # guilloche waves inside the frame
        pts = [(x, 18 + k * 3 + 4 * math.sin(x / 9.0 + k)) for x in range(14, w - 14, 2)]
        d.line(pts, fill=(120, 170, 130, 255), width=1)
        pts = [(x, h - 20 - k * 3 + 4 * math.sin(x / 9.0 + k + 1.5)) for x in range(14, w - 14, 2)]
        d.line(pts, fill=(120, 170, 130, 255), width=1)
    fs = O.pfont(30)
    for (cx, cy) in ((44, h // 2), (w - 44, h // 2)):
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(214, 236, 214, 255), outline=GREEN + (255,), width=4)
        d.text((cx - fs.getlength('$') / 2, cy - 15), '$', font=fs, fill=GREEN + (255,))
    s1 = int(h * 0.24)
    while O.pfont(s1).getlength(line1) > w - 180 and s1 > 10: s1 -= 2
    s2 = int(s1 * 0.62)
    while O.pfont(s2).getlength(line2) > w - 200 and s2 > 8: s2 -= 2
    d.text(((w - O.pfont(s1).getlength(line1)) / 2, h * 0.27), line1, font=O.pfont(s1), fill=GREEN + (255,))
    d.text(((w - O.pfont(s2).getlength(line2)) / 2, h * 0.27 + s1 + 18), line2, font=O.pfont(s2), fill=(200, 40, 48, 255))
    return np.array(img)


# ---------------------------------------------------------------- the Fee-Bee screen (insert, output res)
def screen_ui(t, talk=0.0, brand='XFEENITY SUPPORT', stamp=None, stamp_k=0.0, w=820, h=1240, sub='AI ASSISTANT • ONLINE'):
    """a big phone screen: purple header with the brand, Fee-Bee's face (sprite, crisp), a status line, an optional green stamp"""
    im = Image.new('RGB', (w, h), (22, 30, 56)); d = ImageDraw.Draw(im); d.fontmode = '1'
    for y in range(0, h, 8): d.line([(0, y), (w, y)], fill=(26, 36, 64))
    d.rectangle([0, 0, w, 120], fill=(110, 60, 180))
    s1 = 40
    while O.pfont(s1).getlength(brand) > w - 50 and s1 > 16: s1 -= 2
    f1, f2 = O.pfont(s1), O.pfont(22)
    d.text(((w - f1.getlength(brand)) / 2, 26 + (40 - s1) // 2), brand, font=f1, fill=(255, 255, 255))
    d.text(((w - f2.getlength(sub)) / 2, 80), sub, font=f2, fill=(180, 255, 220))
    a = np.array(im)
    sp = FX.draw(lambda s_: C.feebee_face(s_, 0.0, 70.0, 40.0, t, talk), 6.0)
    blit(a, sp, w // 2, int(h * 0.80), 6.0)
    if stamp and stamp_k > 0:
        im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = '1'
        fs = O.pfont(40)
        tw = fs.getlength(stamp); bw, bh = tw + 60, 100
        x0, y0 = (w - bw) / 2, h - 210
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 18, fill=(40, 170, 90), outline=(255, 255, 255), width=6)
        d.text((x0 + 30, y0 + 30), stamp, font=fs, fill=(255, 255, 255))
        a = np.array(im)
    out = np.zeros((h + 60, w + 60, 4), np.uint8)
    out[..., :3] = (30, 30, 36); out[..., 3] = 255
    out[:8] = INK + (255,); out[-8:] = INK + (255,); out[:, :8] = INK + (255,); out[:, -8:] = INK + (255,)
    out[30:30 + h, 30:30 + w, :3] = a
    rr, cc = np.mgrid[0:h + 60, 0:w + 60]                                             # rounded phone corners
    R = 70
    for (cx, cy) in ((R, R), (w + 60 - R, R), (R, h + 60 - R), (w + 60 - R, h + 60 - R)):
        corner = ((cc < R) if cx == R else (cc > w + 60 - R)) & ((rr < R) if cy == R else (rr > h + 60 - R))
        out[corner & ((cc - cx) ** 2 + (rr - cy) ** 2 > R * R)] = 0
    return out


# ---------------------------------------------------------------- overlays pass
def st(text, fg=(255, 214, 80), size=60):
    return O.sticker(text, fg=fg, size=size)


def st_lines(lines, fg=(255, 255, 255), size=44, gap=6, colors=None):
    """a multi-line sticker: each line an O.sticker, stacked and centred"""
    parts = [O.sticker(l, fg=(colors[i] if colors else fg), size=size) for i, l in enumerate(lines)]
    W_ = max(p.shape[1] for p in parts); H_ = sum(p.shape[0] for p in parts) + gap * (len(parts) - 1)
    out = np.zeros((H_, W_, 4), np.uint8); y = 0
    for p in parts:
        x = (W_ - p.shape[1]) // 2
        reg = out[y:y + p.shape[0], x:x + p.shape[1]]
        reg[:] = np.where(p[..., 3:4] > 0, p, reg)
        y += p.shape[0] + gap
    return out


class Show:
    def __init__(s, epi, n, hook, hook_t=(0.10, 2.0), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1360, hook_y=330,
                 total=6, hook_size=64):
        s.epi = epi
        s.badge = O.make_badge(f'SEASON 1 • EP {n}/{total}')
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


# ---------------------------------------------------------------- shot helpers
def shot(world_, light, cx, cy, Z, acts=(), fx_=None, pre=None, sx=180, sy=320, vig=0.22, t=0.0, front=()):
    return CK.shot(world_, light, cx, cy, Z, acts=acts, front=front, fx_=fx_, pre=pre, sx=sx, sy=sy, vig=vig, t=t)


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


def handheld(t, amp=1.0):
    return (math.sin(t * 2.3) * 10 + math.sin(t * 5.1) * 4) * amp, (math.sin(t * 1.7 + 1) * 8 + math.sin(t * 6.3) * 3) * amp


def shift(big, dx, dy):
    if not dx and not dy: return big
    return np.roll(np.roll(big, int(dy), 0), int(dx), 1)


def shake(t, t0, amp=24, dur=0.4):
    u = t - t0
    if u < 0 or u > dur: return 0, 0
    k = (1 - u / dur) * amp
    return math.sin(u * 90) * k, math.cos(u * 77) * k


# ---------------------------------------------------------------- covers (profile-grid rule 10.10.2026)
GRID = (240, 1680)
SAFE_BOTTOM = 1520


def cover_make(frame, title, n=1, out='cover.png', title_size=96, plate_y=None, grid_preview=True):
    """banknote plate «LAND OF THE FEE / EPISODE N/6» at the TOP of the 3:4 grid zone (y ~262), the title right under it, a soft dark
    band behind both; faces in the middle, nothing that matters below y 1520. Writes cover.png + cover_grid.png"""
    big = frame.copy()
    p = banknote('LAND OF THE FEE', f'EPISODE {n}/6', w=660, h=200)
    py = GRID[0] + 22 if plate_y is None else plate_y
    t = hook_title(title, title_size)
    ty = py + p.shape[0] - 6
    y1 = ty + t.shape[0]
    shade = np.zeros((big.shape[0], 1, 1), np.float32)
    shade[:y1, 0, 0] = 0.34
    n_ = len(shade[y1:y1 + 140]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.34, 0.0, 140)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t, 0, ty, 1.0)
    Image.fromarray(big).save(out)
    if grid_preview:
        g = big[GRID[0]:GRID[1]].copy()
        g[SAFE_BOTTOM - GRID[0]:] = (g[SAFE_BOTTOM - GRID[0]:] * 0.45).astype(np.uint8)
        Image.fromarray(g).resize((270, 360), Image.LANCZOS).save(str(out).replace('.png', '_grid.png'))
    return big



# ---------------------------------------------------------------- E03: the itemised bill (insert, output res), glass crack, split screen
def bill_ui(lines, total=None, title='ST. OVERCHARGE MEDICAL CENTER', w=760, hi=0, t=0.0):
    """a long paper hospital bill: header, itemised lines (Press Start 2P, auto-fitted), the highlighted line hi in red, a TOTAL"""
    fs = 30
    while max(O.pfont(fs).getlength(l) for l in lines) > w - 100 and fs > 14: fs -= 2
    h = 150 + len(lines) * (fs + 26) + (110 if total else 30)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], fill=(252, 250, 240, 255), outline=(150, 150, 150, 255), width=4)
    for x in range(0, w, 24): d.polygon([(x, h - 1), (x + 12, h - 14), (x + 24, h - 1)], fill=(0, 0, 0, 0))     # torn edge
    ft = 26
    while O.pfont(ft).getlength(title) > w - 60 and ft > 12: ft -= 2
    d.text(((w - O.pfont(ft).getlength(title)) / 2, 30), title, font=O.pfont(ft), fill=(30, 60, 120, 255))
    d.line([(30, 90), (w - 30, 90)], fill=(160, 160, 160, 255), width=3)
    y = 120
    for i, l in enumerate(lines):
        if i == hi:
            d.rectangle([24, y - 8, w - 24, y + fs + 8], fill=(255, 226, 226, 255))
        d.text((44, y), l, font=O.pfont(fs), fill=(200, 30, 40, 255) if i == hi else (40, 40, 50, 255))
        y += fs + 26
    if total:
        d.line([(30, y), (w - 30, y)], fill=(40, 40, 50, 255), width=4)
        fT = 40
        while O.pfont(fT).getlength(total) > w - 80 and fT > 16: fT -= 2
        d.text(((w - O.pfont(fT).getlength(total)) / 2, y + 24), total, font=O.pfont(fT), fill=(200, 30, 40, 255))
    return np.array(im)


def crack(big, t, t0, cx, cy, r=260, seed=3):
    """a star crack on glass from the impact point (white lines + a shimmer), grows in 0.08 s"""
    if t < t0: return
    k = min(1.0, (t - t0) / 0.08)
    rng = np.random.default_rng(seed)
    im = Image.fromarray(big); d = ImageDraw.Draw(im)
    for i in range(11):
        a = i / 11 * 2 * math.pi + rng.random() * 0.4
        L = r * (0.5 + rng.random() * 0.6) * k
        pts = [(cx, cy)]
        for j in range(1, 4):
            rr = L * j / 3
            pts.append((cx + math.cos(a + (rng.random() - 0.5) * 0.3) * rr, cy + math.sin(a + (rng.random() - 0.5) * 0.3) * rr))
        d.line(pts, fill=(240, 250, 255), width=5)
    for q in (0.35, 0.7):
        d.ellipse([cx - r * q * k, cy - r * q * k * 0.9, cx + r * q * k, cy + r * q * k * 0.9], outline=(230, 245, 255), width=3)
    big[:] = np.array(im)


def split(left, right, gap=12, col=(255, 214, 90)):
    """vertical split screen of two full frames (each squeezed to half width by cropping its centre)"""
    W2 = (OUT_W - gap) // 2
    out = np.zeros_like(left); out[:] = col
    lx = (OUT_W - W2) // 2
    out[:, :W2] = left[:, lx:lx + W2]
    out[:, W2 + gap:W2 + gap + W2] = right[:, lx:lx + W2]
    return out


def label(big, text, cx, cy, fg=(255, 255, 255), bg=(30, 60, 120), size=34):
    """a small pixel caption plate (split-screen labels: DOCTOR / INSURANCE)"""
    f = O.pfont(size); tw = f.getlength(text)
    im = Image.new('RGBA', (int(tw) + 40, size + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], 10, fill=bg + (235,), outline=(255, 255, 255, 255), width=3)
    d.text((20, 15), text, font=f, fill=fg)
    O.overlay(big, np.array(im), int(cx - im.size[0] / 2), int(cy - im.size[1] / 2), 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(cx - im.size[0] / 2, cy - im.size[1] / 2, cx + im.size[0] / 2, cy + im.size[1] / 2))
