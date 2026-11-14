"""«Замело» episode kit: speaker colours, worlds (xAI backgrounds + zamdecor) with depth maps (depth25), the procedural SNOW SHAFT
along the facade (dug down 9 floors, windows of the neighbours pass by), frosty morning lights, falling snow / sparkles, the 2.5D shot
wrapper (parallax, depth of field, bloom, snowfall, juicy grade), the «аляска» title letters half-buried in a snowdrift, the road-sign
badge / cover plate, the ОЗНОБ phone screens (push notification, rating), stickers.
Coordinates: world px of the 1280x720 backgrounds; output 1080x1920. WS[name] = world px per hero sprite px in that world."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paths as P
import stage as ST
from stage import Light, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
import atmos as AT
import depth25 as D25
from props import zampix as ZX
from props import zamcast as C
from props import zamdecor as DEC

SLUG = 'zamelo'
COL = dict(zhora=(255, 170, 60), chayka=(200, 235, 255), ira=(255, 130, 180), vitek=(150, 240, 110), nina=(215, 175, 255))
WS = dict(facade=4.0, yard=1.4, door=3.4, landing=4.4, kitchen=3.6, cutaway=1.0, slope=0.62, school=5.6, carfield=1.15, port=1.35, flood=2.75)
GULL = 0.55                      # seagull sprite scale vs the hero sprite scale (real ~0.35 m standing vs 1.8 m man)
ORANGE, NAVY, SNOW = (255, 140, 30), (24, 32, 80), (240, 246, 255)
INK = ZX.INK


def A(fn, wx, wy, s, flip=False, pin=None, rim=(ZX.SNOWRIM, ZX.SUN), **kw):
    return ZX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, rim=rim, **kw)


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


# ---------------------------------------------------------------- worlds + depth
_W = {}
DAY = 150                         # the «ДО ВЕСНЫ: N ДНЕЙ» counter of the season (set by the episode before the first world() call)


def world(name):
    if name not in _W:
        Wd = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png', colors=128)
        DEC.dress(name, Wd, day=DAY)
        _W[name] = Wd
    return _W[name]


def depth(name):
    return D25.of(world(name), P.series(SLUG) / 'bg' / f'{name}.png')


def V(name, cx, cy, Z):
    return view_at(world(name), cx, cy, Z, ST.W // 2, ST.H // 2)


def S_of(v, name, z=1.0):
    """output px per hero sprite px for world `name` at depth scale z"""
    return WS[name] * 3 * v.Z * z


# ---------------------------------------------------------------- lights (frosty morning; heroes sit in the painted light)
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_morning(v):
    return Light(amb=(1.04, 1.0, 1.04), keys=_keys(v, [(200, 120, 900, (255, 180, 120), 0.22)]), grad=(1.04, 0.98))


def light_window(v):
    """Жора in the open window: warm lamp from the kitchen behind, cold snow light from the front"""
    return Light(amb=(0.98, 0.98, 1.06), keys=_keys(v, [(700, 330, 300, (255, 190, 110), 0.30), (620, 600, 600, (200, 230, 255), 0.18)]),
                 grad=(1.02, 1.0))


def light_pit(v):
    return Light(amb=(0.82, 0.90, 1.10), keys=_keys(v, [(640, 0, 700, (220, 236, 255), 0.30)]), grad=(1.08, 0.86))


def light_cut(v):
    return Light(amb=(1.02, 1.0, 1.04), keys=_keys(v, [(150, 600, 700, (255, 196, 130), 0.18)]), grad=(1.02, 0.98))


SHAFT_X = (362.0, 424.0)          # the shaft along the outer wall in the cutaway (world px)
SNOW_TOP = 132.0


def shaft_cut(big, v, depth_y, t, seed=1):
    """the shaft dug down along the wall in the cutaway world: from the snow surface to depth_y (world px); jagged walls,
    shovel marks, a dark-blue inside going lighter at the bottom where the lamp of the phone shines"""
    x0, x1 = SHAFT_X
    y0, y1 = SNOW_TOP - 6, depth_y
    if y1 <= y0: return
    ox0, oy0 = v.opt(x0, y0); ox1, oy1 = v.opt(x1, y1)
    H_, W_ = big.shape[:2]
    ya, yb = max(0, int(oy0)), min(H_, int(oy1))
    if ya >= yb: return
    yy = np.arange(ya, yb)[:, None]; xx = np.arange(W_)[None, :]
    wy = (yy / (3 * v.Z)) + v.Y0
    jag_r = ox1 + (np.sin(wy / 9.0 + seed) * 4 + np.sin(wy / 3.7) * 2) * 3 * v.Z
    m = (xx >= ox0) & (xx < jag_r)
    k = np.clip((wy - y0) / max(1.0, y1 - y0), 0, 1)
    col = (np.array((48, 62, 120), np.float32) * (1 - 0.35 * k) + np.array((120, 150, 210), np.float32) * 0.35 * k).reshape(-1, 3)
    reg = big[ya:yb]
    shade = 1.0 - 0.25 * np.clip((xx - ox0) / max(1.0, float(jag_r.mean()) - ox0), 0, 1)       # (1, W)
    c = col[:, None, :] * shade[..., None]                                                    # (n, W, 3) via broadcast
    c = np.broadcast_to(c, (yb - ya, W_, 3))
    reg[m] = np.clip(c[m], 0, 255).astype(np.uint8)
    edge = (xx >= jag_r - 3 * v.Z) & (xx < jag_r + 2 * v.Z)
    reg[edge] = (210, 226, 252)
    for q in range(int(y0) + 18, int(y1) - 6, 22):                         # shovel marks on the snow wall
        _, sy = v.opt(x0, q)
        if ya <= sy < yb - 3:
            sx = int(jag_r[int(sy) - ya, 0] - 6 * v.Z)
            big[int(sy):int(sy) + 3, max(0, sx - int(10 * v.Z)):sx] = (90, 110, 170)


def light_landing(v):
    return Light(amb=(0.92, 0.92, 1.0), keys=_keys(v, [(1040, 60, 520, (255, 196, 140), 0.32), (160, 230, 400, (150, 200, 255), 0.25)]),
                 grad=(1.0, 0.95))


# ---------------------------------------------------------------- snow
def snowfall(big, t, n=70, seed=3, speed=1.0, wind=0.3, par=0.0, a=1.0, box=None):
    """falling snowflakes in 3 depth layers: far = tiny square, near = big soft flake; fixed seeds (no boiling)"""
    H_, W_ = big.shape[:2]
    x0, y0, x1, y1 = box or (0, 0, W_, H_)
    r = np.random.default_rng(seed)
    P_ = r.random((n, 4))
    for u, w, ph, d in P_:
        layer = 0 if d < 0.55 else (1 if d < 0.88 else 2)
        sp = (60.0, 120.0, 260.0)[layer] * speed
        x = x0 + ((u * (x1 - x0) + t * sp * wind + math.sin(t * 1.3 + ph * 7) * (8, 16, 30)[layer] + par * (layer - 1)) % (x1 - x0))
        y = y0 + ((w * (y1 - y0) + t * sp) % (y1 - y0))
        q = (5, 8, 14)[layer]
        ix, iy = int(x), int(y)
        if not (0 <= ix < W_ - q and 0 <= iy < H_ - q): continue
        reg = big[iy:iy + q, ix:ix + q].astype(np.float32)
        k = (0.75, 0.9, 0.7)[layer] * a
        if layer == 2:
            yy, xx = np.mgrid[0:q, 0:q]
            m = ((xx - q / 2 + 0.5) ** 2 + (yy - q / 2 + 0.5) ** 2) <= (q / 2) ** 2
            reg[m] = reg[m] * (1 - k) + np.array(SNOW, np.float32) * k
        else:
            reg[:] = reg * (1 - k) + np.array(SNOW, np.float32) * k
        big[iy:iy + q, ix:ix + q] = reg.astype(np.uint8)
    return big


def sparkle(big, t, box, n=18, seed=5):
    """glints on the snow surface: tiny 4-point stars twinkling"""
    r = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    for i in range(n):
        x, y, ph = r.uniform(x0, x1), r.uniform(y0, y1), r.random() * 6.28
        k = max(0.0, math.sin(t * 2.4 + ph)) ** 6
        if k < 0.1: continue
        L = int(4 + 10 * k); ix, iy = int(x), int(y)
        if 12 <= ix < big.shape[1] - 12 and 12 <= iy < big.shape[0] - 12:
            c = np.array((255, 255, 255), np.float32)
            for dx, dy in ((1, 0), (0, 1)):
                for s_ in range(-L, L + 1, 3):
                    yy, xx = iy + s_ * dy, ix + s_ * dx
                    big[yy:yy + 3, xx:xx + 3] = np.clip(big[yy:yy + 3, xx:xx + 3] * (1 - k) + c * k, 0, 255).astype(np.uint8)


def puff(big, x, y, t, t0, n=10, col=SNOW, seed=2, life=0.6, speed=420.0, px=10):
    """a burst of snow chunks (a dive into the drift, a shovel hit)"""
    if t < t0 or t > t0 + life: return
    u = (t - t0) / life
    r = np.random.default_rng(seed)
    for i in range(n):
        a = r.uniform(-math.pi, 0.0); v_ = r.uniform(0.4, 1.0) * speed
        xx = x + math.cos(a) * v_ * u * life; yy = y + math.sin(a) * v_ * u * life + 900 * (u * life) ** 2
        q = int(px * (1.0 - 0.5 * u)) + 2
        ix, iy = int(xx), int(yy)
        if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q: big[iy:iy + q, ix:ix + q] = col


# ---------------------------------------------------------------- the 2.5D shot
def shot(name, light, cx, cy, Z, acts=(), par=(0.0, 0.0), fx_=None, pre=None, t=0.0, kick=(0, 0), focus=None, dof_k=30.0, haze=None,
         snow=True, snow_n=60, juice=True, rays=None, front=(), bloom=(236, 18, 0.30), vig=0.16, emit=None, glints=None):
    """depth25.shot25 on a «Замело» world + falling snow, glints, the juicy grade (owner 12.11.2026)"""
    W_ = world(name)
    big = D25.shot25(W_, light, cx, cy, Z, depth(name), acts=acts, front=front, par=par, focus=focus, dof_k=dof_k, haze_=haze,
                     bloom_=bloom, rays_=rays, pre=pre, emit=emit, fx_=None, sx=ST.W // 2, sy=ST.H // 2, vig=0, t=t, kick=(0, 0))
    if glints: sparkle(big, t, glints, seed=int(cx) % 9)
    if snow: snowfall(big, t, n=snow_n, seed=int(cx * 3) % 13, par=par[0] * 3)
    if fx_: fx_(big, None)
    if juice: AT.juice(big, 1.24, 1.08)
    if vig: fx.vignette(big, vig)
    if kick[0] or kick[1]:
        dx, dy = int(round(kick[0])), int(round(kick[1]))
        big[:] = np.roll(np.roll(big, dy, 0), dx, 1)
    return big


def blur(big, r=8):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


# ---------------------------------------------------------------- the SNOW SHAFT (procedural: dug down along the facade)
FLOOR_H = 520                     # output px per floor in the shaft at scale 1
_SH = {}


def _shaft_tex():
    """one floor of the facade (low-res pixel art): concrete panels with joints + a window; tiled vertically"""
    if 'tex' in _SH: return _SH['tex']
    w, h = 270, 130                                                     # low-res px (x4 = output)
    im = Image.new('RGB', (w, h), (150, 146, 140)); d = ImageDraw.Draw(im)
    g = np.random.default_rng(3)
    for y in range(h):
        for x in range(0, w, 1):
            pass
    a = np.array(im).astype(np.int32)
    a += (g.normal(0, 5, a.shape[:2])[..., None]).astype(np.int32)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    for x0, c in ((0, (156, 150, 142)), (90, (146, 142, 136)), (200, (152, 148, 140))):     # concrete panels, slightly different
        d.rectangle([x0, 0, x0 + 110, h], fill=c)
    a2 = np.array(im).astype(np.int32) + (np.random.default_rng(5).normal(0, 4, (h, w))[..., None]).astype(np.int32)
    im = Image.fromarray(np.clip(a2, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    d.line([(0, h - 1), (w, h - 1)], fill=(90, 86, 84), width=2)        # floor slab joint
    for x0 in (90, 200): d.line([(x0, 0), (x0, h)], fill=(100, 96, 92), width=1)
    _SH['tex'] = np.array(im)
    return _SH['tex']


def shaft(t, depth_floors, scenes=None, w=OUT_W, h=OUT_H, snow_k=1.0):
    """the facade wall in the shaft, camera descending: depth_floors = how many floors down the camera has gone (float).
    scenes(floor) -> fn(img, x0, y0, x1, y1, t) draws what is inside that floor's window. Returns RGB output frame (no heroes)."""
    tex = _shaft_tex()
    th, tw = tex.shape[:2]
    S = 4
    big = np.zeros((h, w, 3), np.uint8)
    off = depth_floors * th * S
    y = -int(off % (th * S)) - th * S
    fl = 9 - int(off // (th * S)) + 1
    while y < h:
        tile = np.repeat(np.repeat(tex, S, 0), S, 1)[:, :w]
        y0, y1 = max(0, y), min(h, y + th * S)
        if y1 > y0: big[y0:y1, :tile.shape[1]] = tile[y0 - y:y1 - y]
        wx0, wy0, wx1, wy1 = 250, y + 120, 780, y + 400                  # the window of this floor
        if wy1 > 0 and wy0 < h:
            yy0, yy1 = max(0, wy0), min(h, wy1)
            big[yy0:yy1, wx0 - 18:wx1 + 18] = (238, 236, 228)           # white frame
            inner = (wx0, wy0, wx1, wy1)
            big[max(0, wy0 + 12):max(0, min(h, wy1 - 12)), wx0:wx1] = (40, 46, 70)
            if scenes and fl in scenes and wy1 - 12 > 0:
                sub = np.zeros((wy1 - wy0 - 24, wx1 - wx0, 3), np.uint8); sub[:] = (60, 66, 96)
                scenes[fl](sub, t)
                a0 = max(0, -(wy0 + 12)); a1 = sub.shape[0] - max(0, (wy1 - 12) - h)
                if a1 > a0: big[wy0 + 12 + a0:wy0 + 12 + a1, wx0:wx1] = sub[a0:a1]
            big[max(0, wy0 + (wy1 - wy0) // 2 - 6):max(0, min(h, wy0 + (wy1 - wy0) // 2 + 6)), wx0:wx1] = (238, 236, 228)   # transom bar
            big[max(0, wy1 - 14):max(0, min(h, wy1 + 14)), wx0 - 30:wx1 + 30] = (210, 214, 224)      # sill with snow
            n_img = O.sticker(f'{fl} ЭТ.', fg=(255, 214, 80), size=30)
            O.overlay(big, n_img, wx1 + 40, wy1 - 150, 1.0)
        y += th * S
        fl -= 1
    # snow walls on both sides of the shaft (the pit is narrow), with shovel marks
    for side in (0, 1):
        x0, x1 = (0, 150) if side == 0 else (w - 170, w)
        col = np.array((214, 228, 250), np.float32)
        reg = big[:, x0:x1].astype(np.float32)
        xx = np.linspace(0, 1, x1 - x0)[None, :, None] if side == 0 else np.linspace(1, 0, x1 - x0)[None, :, None]
        reg = reg * 0 + col * (0.82 + 0.18 * xx)
        big[:, x0:x1] = reg.astype(np.uint8)
        for k in range(0, h, 90):
            yy = int((k + off * 1.0) % h)
            big[yy:yy + 8, x0 + 20:x1 - 20] = (180, 196, 230)
    return big


# ---------------------------------------------------------------- titles: «аляска» letters half-buried in a snowdrift
def hook_title(lines, size=80, width=OUT_W, drift=0.16):
    """Press Start 2P, fill yellow -> orange -> dark orange steps (Жора's alaska), thick navy outline + drop; the bottom third of every
    line is buried in a bumpy snowdrift (white with blue shade, glints) — not snow caps on top (that is «Прохор»)"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 64) + 60, width, 4), np.uint8)
    y = 26
    for li, line in enumerate(lines):
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 70), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 24 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        o1 = O._dilate(m, 11)
        drop = np.roll(np.roll(o1, 10, 0), 6, 1) & ~o1
        reg = out[y:y + m.shape[0]]
        reg[drop] = (10, 12, 36, 255); reg[o1] = NAVY + (255,)
        rows = np.where(m.any(1))[0]; r0, r1 = rows[0], rows[-1]
        for yy in range(r0, r1 + 1):
            k = (yy - r0) / max(1, r1 - r0)
            c = (255, 222, 90) if k < 0.30 else (255, 150, 40) if k < 0.62 else (226, 96, 20)
            reg[yy][m[yy]] = c + (255,)
        top = m & ~np.roll(m, 6, 0)
        reg[top] = (255, 246, 200, 255)
        # the snowdrift over the lower part of the letters
        cols = np.where(o1.any(0))[0]
        if len(cols):
            ys = r1 - int((r1 - r0) * drift)
            g = np.random.default_rng(li + 3)
            xs = np.arange(cols[0] - 10, cols[-1] + 11)
            bump = ys + np.round(np.sin(xs / 23.0 + li) * 7 + np.sin(xs / 9.0) * 3 + g.normal(0, 0.6, len(xs))).astype(int)
            for x_, b in zip(xs, bump):
                if not (0 <= x_ < width): continue
                b = int(b // 4 * 4)
                y_end = min(m.shape[0], r1 + 14)
                if b < y_end:
                    reg[b:y_end, x_] = (240, 246, 255, 255)
                    reg[b + 8:y_end, x_] = (196, 214, 246, 255)
        y += th + 64
    return out


def title_trim(a):
    m = a[..., 3] > 0
    r = np.where(m.any(1))[0]; c = np.where(m.any(0))[0]
    return a[r[0]:r[-1] + 1, c[0]:c[-1] + 1]


# ---------------------------------------------------------------- road-sign plate: badge / cover plate
def road_sign(line1, line2, w=640, h=170, icicles=True):
    """a blue-white Russian road sign sticking out of a drift: white border, «ЗАМЕЛО!» big + «СЕРИЯ N/6» small, a drift on the bottom
    edge and icicles hanging from it"""
    img = Image.new('RGBA', (w, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rounded_rectangle([0, 0, w - 1, h - 1], 16, fill=(250, 250, 250, 255))
    d.rounded_rectangle([10, 10, w - 11, h - 11], 10, fill=(32, 84, 176, 255))
    s1 = int(h * 0.36)
    while O.pfont(s1).getlength(line1) > w - 60 and s1 > 10: s1 -= 2
    d.text(((w - O.pfont(s1).getlength(line1)) / 2, 24), line1, font=O.pfont(s1), fill=(255, 255, 255))
    s2 = int(s1 * 0.46)
    while O.pfont(s2).getlength(line2) > w - 60 and s2 > 8: s2 -= 2
    d.text(((w - O.pfont(s2).getlength(line2)) / 2, 34 + s1 + 10), line2, font=O.pfont(s2), fill=(255, 214, 80))
    for x in range(0, w, 6):                                              # the drift on the bottom edge
        b = int(h - 26 + math.sin(x / 31.0) * 7 + math.sin(x / 11.0) * 3)
        d.rectangle([x, b, x + 5, h + 2], fill=(240, 246, 255, 255))
        d.rectangle([x, b + 12, x + 5, h + 2], fill=(200, 216, 246, 255))
    if icicles:
        g = np.random.default_rng(2)
        for x in range(30, w - 30, 46):
            L = int(g.uniform(12, 36))
            d.polygon([(x, h), (x + 10, h), (x + 5, h + L)], fill=(214, 236, 255, 255))
    return np.array(img)


def badge(n, total=6):
    im = Image.new('RGBA', (470, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, 469, 63], 12, fill=(250, 250, 250, 235))
    d.rounded_rectangle([5, 5, 464, 58], 9, fill=(32, 84, 176, 235))
    d.text((22, 21), f'ЗАМЕЛО! • СЕРИЯ {n}/{total}', font=O.pfont(20), fill=(255, 255, 255))
    return np.array(im)


# ---------------------------------------------------------------- the per-episode overlay pass
class Show:
    def __init__(s, epi, n, hook, hook_t=(0.10, 2.6), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1180, hook_y=300,
                 hook_size=78):
        s.epi = epi
        s.badge = badge(n)
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
            if ST.LOG[0] is not None: ST.log('title', bbox=(0, s.hook_y, OUT_W, s.hook_y + s.hook.shape[0]))
        s.epi.captions.draw(big, t, s.cap_y.get(shot_, s.cap_default))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


def st(text, fg=(255, 214, 80), size=58):
    return O.sticker(text, fg=fg, size=size)


# ---------------------------------------------------------------- covers (profile grid rule 10.10.2026)
GRID = (240, 1680)
SAFE_BOTTOM = 1520


def cover_make(frame, title, n=1, out='cover.png', title_size=96):
    big = frame.copy()
    p = road_sign('ЗАМЕЛО!', f'СЕРИЯ {n}/6', w=600, h=160)
    py = GRID[0] + 22
    t = hook_title(title, title_size)
    ty = py + p.shape[0] - 30
    y1 = ty + t.shape[0]
    shade = np.zeros((big.shape[0], 1, 1), np.float32); shade[:y1, 0, 0] = 0.26
    n_ = len(shade[y1:y1 + 140]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.26, 0.0, 140)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t, 0, ty, 1.0)
    Image.fromarray(big).save(out)
    g = big[GRID[0]:GRID[1]].copy()
    g[SAFE_BOTTOM - GRID[0]:] = (g[SAFE_BOTTOM - GRID[0]:] * 0.45).astype(np.uint8)
    Image.fromarray(g).resize((270, 360), Image.LANCZOS).save(str(out).replace('.png', '_grid.png'))
    return big


# ---------------------------------------------------------------- phone screens
def _phone(w, h, S=4):
    wl, hl = w // S, h // S
    im = Image.new('RGBA', (wl, hl), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, wl - 1, hl - 1], 16, fill=(30, 30, 40, 255), outline=(14, 14, 24, 255), width=2)
    d.rounded_rectangle([6, 14, wl - 7, hl - 14], 8, fill=(236, 240, 248, 255))
    d.rounded_rectangle([wl // 2 - 14, 5, wl // 2 + 14, 9], 2, fill=(70, 70, 84, 255))
    return im, d, wl, hl


def _fit_text(d, x0, x1, y, txt, size, col, center=True):
    s = size
    while O.pfont(s).getlength(txt) > (x1 - x0) and s > 5: s -= 1
    f = O.pfont(s)
    x = x0 + ((x1 - x0) - f.getlength(txt)) / 2 if center else x0
    d.text((x, y), txt, font=f, fill=col)
    return s


def push_screen(t, w=600, h=980, t_push=0.0):
    """the phone: lock screen with a big violet ОЗНОБ push «Заказ доставлен ✓ Оставлен у двери» sliding in"""
    S = 4
    im, d, wl, hl = _phone(w, h, S)
    d.rectangle([6, 14, wl - 7, hl - 14], fill=(110, 150, 220, 255))
    _fit_text(d, 6, wl - 7, 40, '07:12', 22, (255, 255, 255))
    _fit_text(d, 6, wl - 7, 70, 'ЧЕТВЕРГ, 14 ЯНВАРЯ', 6, (230, 240, 255))
    k = min(1.0, max(0.0, (t - t_push) / 0.18))
    py = int(lerp(-80, 60, 1 - (1 - k) ** 3))
    d.rounded_rectangle([12, py, wl - 13, py + 96], 8, fill=(250, 250, 255, 255), outline=(120, 60, 200, 255), width=2)
    d.rounded_rectangle([18, py + 8, 34, py + 24], 4, fill=(120, 60, 200, 255))
    d.text((21, py + 12), 'О', font=O.pfont(9), fill=(255, 255, 255))
    d.text((40, py + 12), 'ОЗНОБ', font=O.pfont(8), fill=(120, 60, 200))
    _fit_text(d, 18, wl - 19, py + 32, 'ЗАКАЗ ДОСТАВЛЕН', 8, (30, 30, 40), center=False)
    _fit_text(d, 18, wl - 19, py + 50, 'ОСТАВЛЕН', 9, (200, 40, 40), center=False)
    _fit_text(d, 18, wl - 19, py + 66, 'У ДВЕРИ', 9, (200, 40, 40), center=False)
    return np.array(im.resize((wl * S, hl * S), Image.NEAREST))


def rating_screen(t, stars=1, t_star=0.3, w=600, h=760):
    """«Оцените доставку»: five stars, `stars` light up one by one from t_star"""
    S = 4
    im, d, wl, hl = _phone(w, h, S)
    d.rectangle([6, 14, wl - 7, 40], fill=(120, 60, 200, 255))
    _fit_text(d, 6, wl - 7, 22, 'ОЗНОБ', 9, (255, 255, 255))
    _fit_text(d, 14, wl - 15, 60, 'ОЦЕНИТЕ ДОСТАВКУ', 9, (30, 30, 40))
    n = int(max(0, (t - t_star) / 0.15) + 1) if t >= t_star else 0
    n = min(n, stars)
    for i in range(5):
        cx, cy, r = 24 + i * ((wl - 48) // 4), 110, 11
        pts = []
        for j in range(10):
            a = -math.pi / 2 + j * math.pi / 5
            rr = r if j % 2 == 0 else r * 0.45
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        d.polygon(pts, fill=(255, 196, 40, 255) if i < n else (210, 214, 226, 255), outline=(40, 40, 60, 255))
    return np.array(im.resize((wl * S, hl * S), Image.NEAREST))
