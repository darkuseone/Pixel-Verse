"""Shared episode kit for «Agent Dibs»: speaker colours, night scene lights, hook title (ice gradient + Chicago-red outline),
the standard overlay pass (badge, hook, stickers, karaoke captions, flashes, mosaic) and a generic shot helper.
Same conventions as props/uskit.py (E01 of Sunny Palms), different look."""
import math
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import Chars, Light, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from props import bytfx as B

COL = dict(dibs=(255, 150, 40), deb=(80, 230, 255), marty=(150, 255, 80), brad=(60, 225, 170), terry=(255, 100, 100),
           gary=(190, 150, 255), mrs_w=(255, 238, 200), chief=(255, 214, 74), operator=(205, 210, 220), cabbie=(255, 220, 60))
RED = (226, 40, 60)
ICE = ((255, 255, 255), (170, 232, 255), (70, 194, 250))


# ---------------------------------------------------------------- lights (world lamp positions -> output px)
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z * 3 / 3.0, c, a) for (x, y, r, c, a) in lamps]


def light_night(v, lamps=(), amb=(0.84, 0.91, 1.10), rim=(-1, -0.45, (255, 206, 150), 0.42), grad=(1.04, 0.90)):
    return Light(amb=amb, keys=_keys(v, lamps), rim=rim, grad=grad)


STREET_LAMPS = ((400, 70, 640, (255, 190, 110), 0.55), (700, 460, 520, (255, 206, 140), 0.40))
AVENUE_LAMPS = ((470, 215, 640, (255, 190, 110), 0.55), (1560, 215, 560, (255, 190, 110), 0.45), (1010, 190, 560, (255, 180, 100), 0.35))
STAND_LAMPS = ((520, 390, 760, (255, 214, 130), 0.80), (1000, 140, 640, (150, 190, 255), 0.30))


def light_street(v): return light_night(v, STREET_LAMPS)
def light_avenue(v): return light_night(v, AVENUE_LAMPS)
def light_stand(v): return light_night(v, STAND_LAMPS)
def light_lobby(v):
    return Light(amb=(0.96, 0.98, 1.10), keys=_keys(v, ((640, 260, 900, (110, 235, 255), 0.35), (240, 330, 600, (255, 90, 230), 0.30))),
                 rim=(1, -0.3, (255, 96, 226), 0.40), grad=(1.05, 0.90))
def light_river(v):
    return Light(amb=(0.86, 0.93, 1.16), keys=_keys(v, ((250, 90, 900, (200, 220, 255), 0.30), (820, 420, 560, (255, 196, 120), 0.35))),
                 rim=(-1, -0.4, (190, 214, 255), 0.45), grad=(1.04, 0.88))
def light_bean(v):
    return Light(amb=(0.90, 0.95, 1.12), keys=_keys(v, ((640, 280, 900, (150, 200, 255), 0.30), (180, 420, 560, (255, 190, 120), 0.35))),
                 rim=(-1, -0.4, (220, 232, 255), 0.42), grad=(1.04, 0.90))


# ---------------------------------------------------------------- hook title
def _dil(m, r):
    d = m.copy()
    for dx in range(-r, r + 1, 2):
        for dy in range(-r, r + 1, 2):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def hook_title(lines, size=64, width=OUT_W):
    """Press Start 2P, italic skew, ice-white -> cyan stepped gradient with a Chicago-red outline and a navy shadow (RGBA)"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 44) + 40, width, 4), np.uint8)
    y = 20
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 40), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 16 - bb[1]), line, font=f, fill=255)
        m0 = np.array(img) > 127
        m = np.zeros_like(m0)                                                       # italic shear: shift rows by height
        for yy in range(m0.shape[0]):
            m[yy] = np.roll(m0[yy], int((m0.shape[0] - yy) * 0.18))
        dil = _dil(m, 8); shd = np.roll(np.roll(dil, 10, 0), 6, 1)
        reg = out[y:y + m.shape[0]]
        reg[shd] = (8, 18, 48, 255); reg[dil] = RED + (255,)
        rows = np.where(m.any(1))[0]; r0, r1 = rows[0], rows[-1]
        for yy in range(m.shape[0]):
            k = (yy - r0) / max(1, r1 - r0)
            col = ICE[0] if k < 0.30 else ICE[1] if k < 0.62 else ICE[2]
            if (yy // 6) % 2: col = tuple(int(c * 0.93) for c in col)                # faint horizontal stripes
            reg[yy][m[yy]] = col + (255,)
        reg[m & ~np.roll(m, 8, 0)] = (255, 255, 255, 255)
        y += th + 44
    return out


class Show:
    """per-episode overlay config: badge, hook, stickers [(img, t0, t1, cx, cy)], captions, flashes, mosaics, optional teaser"""
    def __init__(s, epi, n, hook, hook_t=(0.15, 2.4), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330, teaser=None,
                 hook_y=150, total=6, hook_size=64):
        s.epi = epi
        s.badge = O.make_badge(f'SEASON 1 • EP {n}/{total}')
        s.hook = hook_title(hook, hook_size) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default
        s.teaser = hook_title([teaser], 40) if teaser else None

    def apply(s, big, t, shot):
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        O.overlay(big, s.badge, 36, 96, 1.0)
        if s.hook is not None and s.hook_t[0] <= t < s.hook_t[1]:
            k = min(1.0, (t - s.hook_t[0]) / 0.1) * (1 - sm((t - (s.hook_t[1] - 0.2)) / 0.2))
            O.overlay(big, s.hook, 0, s.hook_y, k)
        s.epi.captions.draw(big, t, s.cap_y.get(shot, s.cap_default))
        dur = s.epi.dur
        if s.teaser is not None and t >= dur - 0.8:
            O.overlay(big, s.teaser, 0, 1560, min(1.0, (t - (dur - 0.8)) / 0.15))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


# ---------------------------------------------------------------- generic helpers
def J(u, p=1.7, k=0.38):
    """jump-cut punch-in: every other `p` seconds of a long shot is framed tighter"""
    return k if int(u / p) % 2 else 0.0


def hit(t, t0, dur=0.35):
    return max(0.0, 1 - (t - t0) / dur) if t >= t0 else 0.0


def shot(world, light, cx, cy, Z, acts=(), back=(), front=(), fx_=None, sx=180, sy=330, vig=0.26, emit=None, pre=None):
    """render one frame: background view (cx, cy at screen (sx, sy)), back / acts / front groups of callables a(CH, v),
    each group composited with the scene light, then emit(big, v) (unlit overlays), fx_(big, v), vignette"""
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world, cx, cy, Z, sx, sy)
    big = v.bg()
    if pre: pre(big, v)
    lt = light(v) if light else None
    for group in (back, acts, front):
        if not group: continue
        CH = Chars()
        for a in group: a(CH, v)
        CH.comp(big, lt)
    if emit: emit(big, v)
    if fx_: fx_(big, v)
    if vig: fx.vignette(big, vig)
    return big


def snow(big, v, t, n=70, speed=55, wind=0.0):
    """falling snow over the visible world box (emissive)"""
    FX = Chars()
    x0, y0 = v.X0, v.Y0
    x1, y1 = x0 + ST.W * ST.PX[0] / v.Z + 4, y0 + ST.H * ST.PX[0] / v.Z + 4
    B.falling_snow(FX, v, t, x0, y0, x1, y1, n=n, speed=speed)
    FX.comp(big)


def wind_snow(big, t, k=1.0, slant=0.9, n=120):
    """horizontal blizzard streaks across the output frame (E05 wind)"""
    r = np.random.default_rng(int(t * 30) % 100000)
    for i in range(int(n * k)):
        y = int(r.integers(0, OUT_H)); x = int(r.integers(-200, OUT_W)); ln = int(r.integers(60, 220))
        big[y:y + 4, max(0, x):max(0, min(OUT_W, x + ln))] = (236, 244, 255)


def shake(big, t, amp, freq=37.0):
    B.shake(big, t, amp, freq)
    return big


# ---------------------------------------------------------------- worlds (AI backgrounds, quantised once)
import paths as P
from props import chi_cast as C, chi_props as PR
_WORLDS = {}
SLUG = 'agent-dibs'


def world(name):
    if name not in _WORLDS: _WORLDS[name] = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png')
    return _WORLDS[name]


# ---------------------------------------------------------------- Deb at her desk (Field Office)
DEBA = (500.0, 664.0, 14.0)             # anchor x, y, unit
DESK_Y = 548                            # desk top edge in world px: everything below hides Deb's lower body


def light_office(v):
    return Light(amb=(1.0, 1.0, 0.95), keys=_keys(v, ((640, 40, 900, (200, 255, 170), 0.30), (900, 300, 500, (255, 200, 120), 0.25))),
                 rim=(-1, -0.4, (255, 226, 170), 0.38), grad=(1.05, 0.92))


def deb_frame(t, expr='smile', mouth=0.0, Z=2.0, dx=0.0, dy=0.0, zoom=0.05, u=0.0, hand_n=None, prop_n=None, hand_f=None, prop_f=None,
              pose=None, lean=0.0, sweat=0.0, shake_=0.0, fx_=None):
    """full 1080x1920 cutaway of Deb behind her desk (knitting by default); lower body hidden by redrawing the desk from the background"""
    Zt = Z + zoom * u
    ST.set_px(ST.px_for_zoom(Zt))
    W_ = world('field_office')
    ax, ay, un = DEBA
    v = view_at(W_, ax + 1.4 * un + dx, ay - 21.0 * un + dy, Zt, 180, 262)
    big = v.bg(); orig = big.copy()
    CH = Chars()
    pose = pose or C.POSE['hold']
    C.deb(CH, v.cam(ax, ay, un), pose, t, mouth, expr, 0.0, hand_n=hand_n if hand_n is not None else H_(6.0, 14.4),
          hand_f=hand_f if hand_f is not None else H_(5.0, 14.8), prop_n=prop_n or (lambda L, h: PR.knit(L, h, t)), prop_f=prop_f,
          lean=lean, sweat=sweat)
    CH.comp(big, light_office(v))
    xs, ys = v.grid()
    m = (ys[:, None] > DESK_Y) & ((xs >= 20) & (xs <= 955))[None, :]
    big[m] = orig[m]
    if fx_: fx_(big, v)
    fx.vignette(big, 0.26)
    if shake_: B.shake(big, t, shake_, 35)
    return big


def H_(x, h):
    return C.H(x, h)


def deb_window(big, t, expr='smile', mouth=0.0, box=(660, 520, 1040, 900), label='DEB: CONTROL', **kw):
    """picture-in-picture video call window with Deb (cyan frame, blinking REC dot)"""
    fr = deb_frame(t, expr, mouth, Z=2.2, **kw)
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    crop = fr[300:300 + 1000, 40:1040]
    img = Image.fromarray(crop).resize((w, h), Image.NEAREST)
    a = np.array(img)
    big[y0 - 10:y1 + 10, x0 - 10:x1 + 10] = (60, 220, 250)
    big[y0 - 4:y1 + 4, x0 - 4:x1 + 4] = (10, 20, 40)
    big[y0:y1, x0:x1] = a
    d = Image.fromarray(big[y1 + 10:y1 + 70, x0 - 10:x1 + 10]); dd = ImageDraw.Draw(d)
    dd.rectangle([0, 0, d.size[0], 60], fill=(10, 20, 40))
    dd.text((14, 14), label, font=O.pfont(26), fill=(120, 240, 255))
    big[y1 + 10:y1 + 70, x0 - 10:x1 + 10] = np.array(d)
    if int(t * 2) % 2 == 0: big[y0 + 14:y0 + 34, x1 - 40:x1 - 20] = (240, 50, 60)


# ---------------------------------------------------------------- brick wall + window with a nosy lady (curtain twitch)
_BRICK = None


def brick_bg():
    global _BRICK
    if _BRICK is None:
        r = np.random.default_rng(5)
        img = np.zeros((OUT_H, OUT_W, 3), np.uint8)
        bh, bw = 54, 150
        for row in range(OUT_H // bh + 1):
            off = (row % 2) * bw // 2
            for cx in range(-1, OUT_W // bw + 2):
                col = np.array([96, 44, 36]) + r.integers(-14, 14, 3) + np.array([r.integers(0, 10), 0, 0])
                x0 = cx * bw + off; y0 = row * bh
                img[max(0, y0):max(0, y0 + bh - 5), max(0, x0):max(0, x0 + bw - 5)] = np.clip(col, 0, 255)
        img[img.sum(2) == 0] = (40, 30, 28)
        _BRICK = img
    return _BRICK.copy()


def window_cut(t, u, who='mrs_w', open_t=0.12, prop='binoculars', expr='deadpan', flip=False, shift=(0, 0), robe_cur=(214, 70, 96)):
    """full-frame cutaway: moonlit brick wall, lit window, curtains snap open at open_t and a lady leans out (binoculars / popcorn)"""
    wall = (brick_bg() * np.array([0.36, 0.42, 0.62])).astype(np.uint8)
    big = wall.copy()
    x0, y0, x1, y1 = 150 + shift[0], 330 + shift[1], 930 + shift[0], 1250 + shift[1]
    big[y0 - 70:y0, x0 - 90:x1 + 90] = (226, 232, 240)                                              # snow on the lintel
    big[y0 - 22:y1 + 22, x0 - 22:x1 + 22] = (30, 26, 30)                                            # frame
    big[y0:y1, x0:x1] = (255, 206, 120)                                                              # warm light
    k = min(1.0, max(0.0, (t - open_t) / 0.10))
    cw = int((x1 - x0) / 2 * (1.0 - 0.84 * k))
    cur = robe_cur
    big[y0:y1, x0:x0 + cw] = cur; big[y0:y1, x1 - cw:x1] = cur
    for q in range(0, max(cw, 1), 28):
        big[y0:y1, x0 + q:x0 + q + 6] = (170, 40, 68); big[y0:y1, x1 - q - 6:x1 - q] = (170, 40, 68)
    base_below = big.copy()
    if k > 0.02:
        ST.set_px(2)
        pk = ST.PX[0]; f = ST.UP * pk
        unit_out = 58.0
        ax_o, ay_o = (x0 + x1) / 2 + (50 if flip else -50), (y0 + y1) / 2 - 110 + 21.3 * unit_out + 40 * (1 - k)    # head a bit above window centre
        cam = ST.ACam(1000.0, 1000.0, ax_o / f, ay_o / f, unit_out / f, flip)
        CH = Chars()
        pr = None
        if prop == 'binoculars':
            from props.us_props import binoculars
            pr = lambda L, h: binoculars(L, (h[0] - 0.4, h[1] - 4.6))
        elif prop == 'popcorn':
            pr = lambda L, h: popcorn(L, h, t)
        C.lady(CH, cam, who, C.POSE['hold'], t, 0.0, expr, 0.0, legs=False, hand_n=C.H(5.4, 18.6) if prop == 'binoculars' else C.H(5.4, 13.4), prop_n=pr)
        CH.comp(big, Light(amb=(1.08, 1.0, 0.92), rim=(1, -0.3, (255, 230, 180), 0.3)))
        big[y1:] = base_below[y1:]                                                                   # nothing below the sill
    big[y1:y1 + 50, x0 - 70:x1 + 70] = (210, 218, 232)                                              # sill with snow
    big[y0 - 40:y0 - 14, x0 - 22:x1 + 22] = (120, 90, 60)                                           # curtain rod
    fx.vignette(big, 0.3)
    return big


def popcorn(L, h, t=0.0):
    """bucket of popcorn held at h"""
    from props.us_props import rect
    poly_ = PR.poly
    poly_(L, [(h[0] - 1.6, h[1] - 0.6), (h[0] + 1.6, h[1] - 0.6), (h[0] + 1.2, h[1] + 2.6), (h[0] - 1.2, h[1] + 2.6)], (250, 250, 246))
    for k in range(3): PR.cap(L, (h[0] - 1.0 + k * 1.0, h[1] - 0.4), (h[0] - 1.0 + k * 1.0, h[1] + 2.4), 0.3, 0.3, (214, 40, 50))
    for k in range(5): PR.ell(L, (h[0] - 1.4 + k * 0.7, h[1] - 1.2 - 0.3 * (k % 2)), 0.6, 0.6, (255, 244, 200), 0, None, (230, 200, 130))


# ---------------------------------------------------------------- invisibility (ghost composite) and big pixel digits
def ghost_comp(CH, big, light, alpha=0.30, edge=(120, 240, 255), t=0.0):
    """composite a Chars canvas semi-transparent with a shimmering cyan outline (invisibility cloak)"""
    if not CH.m.any():
        CH.col[:] = 0; CH.m[:] = False; return
    col = CH.col.astype(np.float32)
    if light is not None: col = light.apply(col, CH.m, CH.k)
    f = ST.UP * CH.k
    m = np.repeat(np.repeat(CH.m, f, 0), f, 1)
    c = np.repeat(np.repeat(np.clip(col, 0, 255).astype(np.uint8), f, 0), f, 1)
    b = big[m].astype(np.float32)
    big[m] = np.clip(b * (1 - alpha) + c[m].astype(np.float32) * alpha, 0, 255).astype(np.uint8)
    ed = m & ~np.roll(np.roll(m, 6, 0), 6, 1)
    yy, xx = np.nonzero(ed)
    sh = ((xx // 18 + yy // 18 + int(t * 8)) % 2 == 0)
    big[yy[sh], xx[sh]] = edge
    CH.col[:] = 0; CH.m[:] = False


def digits(big, txt, cx=540, cy=700, size=420, col=(255, 236, 110), pulse=1.0):
    """giant pixel countdown digit with a Chicago-red outline"""
    f = O.pfont(int(size * pulse)); bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    img = Image.new('L', (tw + 80, th + 80), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((40 - bb[0], 40 - bb[1]), txt, font=f, fill=255)
    m = np.array(img) > 127
    dil = _dil(m, 16)
    out = np.zeros((m.shape[0], m.shape[1], 4), np.uint8)
    out[dil] = RED + (255,); out[m] = col + (255,)
    O.overlay(big, out, int(cx - out.shape[1] / 2), int(cy - out.shape[0] / 2), 1.0)
