"""«Ключевой сотрудник» episode kit: speaker colours, worlds (xAI office + ksdecor) with depth maps (depth25), real scale on the office
floor (door 355 px = 2.1 m -> hero 1.75 m ≈ 296 px at the back wall), office lights (evening tubes / night lamp / grey morning),
the 2.5D shot wrapper (parallax, depth of field, bloom, dust, juice grade), the «sticky-note» title letters, the lanyard badge
(series plate, no «N/6» — test 22.11.2026), the overlay pass and the cover maker.
Coordinates: world px of the 1280x720 backgrounds; output 1080x1920."""
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
from props import kspix as KX
from props import kscast as C
from props import ksdecor as DEC

SLUG = 'klyuchevoy'
COL = dict(edik=(255, 214, 90), fikus=(130, 236, 140), shef=(255, 130, 120), lyuda=(214, 176, 255))
INK = KX.INK
FLOOR_Y0, WS0, WS_K = 510.0, 3.75, 0.0095        # hero scale on the floor: world px per sprite px at the back wall, growth per px of y


def ws_at(wy):
    """world px per hero sprite px for feet at floor row wy (perspective of the office floor)"""
    return WS0 + max(0.0, wy - FLOOR_Y0) * WS_K


def A(fn, wx, wy, s, flip=False, pin=None, rim=(KX.LAMP, KX.MONI), **kw):
    return KX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, rim=rim, **kw)


def wpt(v, ox, oy):
    """output px -> world px"""
    return v.X0 + ox / (3 * v.Z), v.Y0 + (oy / 3 - v.oy) / v.Z


def aout(act, v, name):
    sp = act.last
    px, py = sp.anchors[name]
    ox, oy = v.opt(act.wx, act.wy)
    sc = act.scale(v)
    if act.pin:
        qx, qy = sp.anchors[act.pin]
        ox -= (-qx if act.flip else qx) * sc; oy += qy * sc
    return ox + (-px if act.flip else px) * sc, oy - py * sc


def at(fn, v, ox, oy, s, flip=False, pin=None, near=None, **kw):
    """actor placed by OUTPUT px of its feet (or of the pin anchor) at an explicit on-screen scale s (output px per sprite px)"""
    wx, wy = wpt(v, ox, oy)
    a = A(fn, wx, wy, s, flip=flip, pin=pin, **kw)
    if near is not None: a.near = near
    return a


# ---------------------------------------------------------------- worlds + depth
_W = {}


def world(name):
    if name not in _W:
        Wd = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png', colors=128)
        DEC.dress(name, Wd)
        _W[name] = Wd
    return _W[name]


def depth(name):
    return D25.of(world(name), P.series(SLUG) / 'bg' / f'{name}.png')


def V(name, cx, cy, Z):
    return view_at(world(name), cx, cy, Z, 180, 320)


# ---------------------------------------------------------------- lights
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_evening(v, t=0.0):
    fl = 1.0 - 0.06 * (math.sin(t * 37) > 0.93)                                 # a tube that flickers now and then
    return Light(amb=(1.00 * fl, 1.03 * fl, 0.96 * fl), keys=_keys(v, [(610, 410, 260, (255, 200, 120), 0.30),
                                                                        (1000, 220, 420, (150, 150, 255), 0.12)]), grad=(1.04, 0.94))


def light_night(v, t=0.0):
    return Light(amb=(0.62, 0.66, 0.92), keys=_keys(v, [(610, 410, 330, (255, 190, 110), 0.62), (1000, 220, 380, (120, 140, 255), 0.18)]),
                 grad=(0.96, 0.84))


def light_morning(v, t=0.0):
    return Light(amb=(1.04, 1.04, 1.06), keys=_keys(v, [(1000, 220, 520, (220, 230, 255), 0.22)]), grad=(1.04, 0.96))


LIGHT = dict(office=light_evening, office_night=light_night, office_morning=light_morning)


# ---------------------------------------------------------------- the 2.5D shot
def shot(name, cx, cy, Z, acts=(), par=(0.0, 0.0), fx_=None, pre=None, t=0.0, kick=(0, 0), focus=None, dof_k=30.0, haze=None,
         motes=True, juice=True, rays=None, front=(), bloom=(226, 22, 0.34), vig=0.22, emit=None, clock='17:59'):
    DEC.CLOCK[0] = clock
    W_ = world(name)
    v = V(name, cx, cy, Z)
    big = D25.shot25(W_, lambda v_: LIGHT[name](v_, t), cx, cy, Z, depth(name), acts=acts, front=front, par=par, focus=focus, dof_k=dof_k, haze_=haze,
                     bloom_=bloom, rays_=rays, pre=pre, emit=emit, fx_=None, sx=ST.W // 2, sy=ST.H // 2, vig=0, t=t, kick=(0, 0))
    if motes:
        col = (255, 236, 190) if name != 'office_night' else (190, 210, 255)
        AT.motes(big, t, n=22, col=col, seed=int(cx * 3) % 11, par=par[0] * 3)
    if fx_: fx_(big, v)
    if juice: AT.juice(big, 1.26, 1.10)
    if vig: fx.vignette(big, vig)
    if kick[0] or kick[1]:
        dx, dy = int(round(kick[0])), int(round(kick[1]))
        big[:] = np.roll(np.roll(big, dy, 0), dx, 1)
    return big


def blur(big, r=8):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


# ---------------------------------------------------------------- titles: «sticky-note» letters
def _dil(m, r, step=2):
    d = m.copy()
    for dx in range(-r, r + 1, step):
        for dy in range(-r, r + 1, step):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


TOP, BOT = np.array((255, 232, 110)), np.array((246, 140, 40))
EDGE, OUTL = (255, 250, 226), (70, 40, 24)


def note_title(lines, size=80, width=OUT_W, tape=True):
    """sticky-note letters: mustard-yellow (top) -> orange (bottom) in 4 steps, a cream inner edge, a thick coffee-brown
    «cardboard» outline + drop, two strips of translucent tape on the first line's corners"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 56) + 60, width, 4), np.uint8)
    y = 28
    for li, line in enumerate(lines):
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 64), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 22 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        o1 = _dil(m, 5, 1); o2 = _dil(m, 13)
        drop = np.roll(np.roll(o2, 10, 0), 6, 1) & ~o2
        reg = out[y:y + m.shape[0]]
        reg[drop] = (30, 18, 10, 230); reg[o2] = OUTL + (255,); reg[o1 & ~m] = EDGE + (255,)
        rr = np.where(m.any(1))[0]; r0, r1 = rr[0], rr[-1]
        for yy in range(r0, r1 + 1):
            k = (yy - r0) / max(1, r1 - r0)
            k = math.floor(k * 4) / 3.0
            c = TOP * (1 - k) + BOT * k
            mm = m[yy]; reg[yy][mm, :3] = c.astype(np.uint8); reg[yy][mm, 3] = 255
        if tape and li == 0:
            cc = np.where(m.any(0))[0]; c0, c1 = cc[0], cc[-1]
            for (xx, ang) in ((c0 - 10, 1), (c1 - 70, -1)):
                for q in range(26):
                    yy0 = r0 - 22 + q
                    x0 = int(xx + ang * q * 0.6)
                    if 0 <= yy0 < reg.shape[0]:
                        seg = reg[yy0, max(0, x0):max(0, x0) + 84]
                        seg[:, :3] = (seg[:, :3].astype(np.float32) * 0.45 + np.array((255, 250, 230)) * 0.55).astype(np.uint8)
                        seg[:, 3] = np.maximum(seg[:, 3], 170)
        y += th + 56
    return out


def title_trim(a):
    m = a[..., 3] > 0
    r = np.where(m.any(1))[0]; c = np.where(m.any(0))[0]
    return a[r[0]:r[-1] + 1, c[0]:c[-1] + 1]


def hook_title(lines, size=80, width=OUT_W):
    return note_title(lines, size, width)


# ---------------------------------------------------------------- the lanyard badge (series plate + cover plate)
def lanyard_badge(w=560, h=190, line1='КЛЮЧЕВОЙ', line2='СОТРУДНИК', strap=True):
    """an office pass on a blue lanyard: white card, a blue header strip «ПРОПУСК», a photo square with a tiny pixel face,
    two big lines; the strap goes up out of the top"""
    sh = 70 if strap else 0
    im = Image.new('RGBA', (w, h + sh), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    if strap:
        d.polygon([(w // 2 - 70, 0), (w // 2 - 40, 0), (w // 2 - 6, sh + 8), (w // 2 - 30, sh + 8)], fill=(52, 96, 200, 255))
        d.polygon([(w // 2 + 40, 0), (w // 2 + 70, 0), (w // 2 + 30, sh + 8), (w // 2 + 6, sh + 8)], fill=(40, 76, 170, 255))
        d.rectangle([w // 2 - 22, sh - 2, w // 2 + 22, sh + 16], fill=(190, 190, 196, 255))
    y0 = sh + 10
    d.rounded_rectangle([0, y0, w - 1, y0 + h - 11], 16, fill=(40, 30, 26, 255))
    d.rounded_rectangle([6, y0 + 6, w - 7, y0 + h - 17], 12, fill=(250, 250, 244, 255))
    d.rectangle([6, y0 + 22, w - 7, y0 + 50], fill=(52, 96, 200, 255))
    d.text((24, y0 + 28), 'ПРОПУСК • ВЕКТОР-СНАБ-СБЫТ', font=O.pfont(14), fill=(250, 250, 244))
    ps = h - 86
    px0, py0 = 22, y0 + 60
    d.rectangle([px0, py0, px0 + ps, py0 + ps - 8], fill=(150, 180, 220, 255), outline=(40, 30, 26, 255), width=3)
    cx, cy = px0 + ps // 2, py0 + ps // 2                                                   # tiny pixel Эдик
    d.ellipse([cx - 22, cy - 26, cx + 22, cy + 22], fill=(238, 188, 152, 255))
    d.rectangle([cx - 12, cy - 6, cx - 6, cy], fill=(40, 30, 26)); d.rectangle([cx + 6, cy - 6, cx + 12, cy], fill=(40, 30, 26))
    d.rectangle([cx - 8, cy + 10, cx + 8, cy + 13], fill=(160, 80, 70))
    for q in range(3): d.line([(cx - 20, cy - 20 + q * 5), (cx + 14, cy - 26 + q * 5)], fill=(120, 92, 62), width=3)
    tx0 = px0 + ps + 22
    avail = w - tx0 - 22
    s1 = 46
    while O.pfont(s1).getlength(line1) > avail and s1 > 12: s1 -= 2
    d.text((tx0, py0 + 4), line1, font=O.pfont(s1), fill=(40, 30, 26))
    s2 = s1
    while O.pfont(s2).getlength(line2) > avail and s2 > 12: s2 -= 2
    d.text((tx0, py0 + 14 + s1), line2, font=O.pfont(s2), fill=(178, 72, 54))
    return np.array(im)


def badge():
    im = Image.new('RGBA', (430, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, 429, 63], 12, fill=(40, 30, 26, 215))
    d.rectangle([12, 12, 22, 51], fill=(52, 96, 200, 255))
    d.rounded_rectangle([30, 14, 60, 50], 4, fill=(250, 250, 244, 255))
    d.rectangle([35, 20, 55, 32], fill=(150, 180, 220, 255))
    d.text((74, 21), 'КЛЮЧЕВОЙ СОТРУДНИК', font=O.pfont(20), fill=(255, 232, 110))
    return np.array(im)


# ---------------------------------------------------------------- the per-episode overlay pass
class Show:
    def __init__(s, epi, hook, hook_t=(0.10, 2.4), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1240, hook_y=280,
                 hook_size=78):
        s.epi = epi
        s.badge = badge()
        s.hook = note_title(hook, hook_size) if hook else None
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


def st(text, fg=(255, 232, 110), size=58):
    return O.sticker(text, fg=fg, size=size)


# ---------------------------------------------------------------- covers (profile grid rule 10.10.2026)
GRID = (240, 1680)
SAFE_BOTTOM = 1520


def cover_make(frame, title, out='cover.png', title_size=96):
    big = frame.copy()
    p = lanyard_badge(560, 170)
    py = GRID[0] - 40
    t = note_title(title, title_size)
    ty = py + p.shape[0] - 18
    y1 = ty + t.shape[0]
    shade = np.zeros((big.shape[0], 1, 1), np.float32); shade[:y1, 0, 0] = 0.28
    n_ = len(shade[y1:y1 + 140]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.28, 0.0, 140)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t, 0, ty, 1.0)
    Image.fromarray(big).save(out)
    g = big[GRID[0]:GRID[1]].copy()
    g[SAFE_BOTTOM - GRID[0]:] = (g[SAFE_BOTTOM - GRID[0]:] * 0.45).astype(np.uint8)
    Image.fromarray(g).resize((270, 360), Image.LANCZOS).save(str(out).replace('.png', '_grid.png'))
    return big


# ---------------------------------------------------------------- inserts
def clock_insert(t, hhmm, w=OUT_W, h=OUT_H, bg=(232, 220, 180)):
    """a full-frame close-up of the wall clock (time jump), the second hand runs fast"""
    big = np.zeros((h, w, 3), np.uint8); big[:] = bg
    yy = np.linspace(0, 1, h)[:, None, None]; big[:] = (big * (1.0 - 0.25 * yy)).astype(np.uint8)
    hh, mm = (int(x) for x in hhmm.split(':'))
    cx, cy, R_ = w // 2, int(h * 0.45), int(w * 0.40)
    Y, X = np.mgrid[0:h, 0:w]; d = np.hypot(X - cx, Y - cy)
    big[d < R_ + 26] = (40, 36, 34); big[d < R_] = (240, 236, 222)
    for k in range(60):
        a = k / 60 * 2 * math.pi; r0 = R_ * (0.82 if k % 5 == 0 else 0.90)
        for i in range(int(r0), int(R_ * 0.95)):
            x, y = int(cx + math.sin(a) * i), int(cy - math.cos(a) * i); q = 9 if k % 5 == 0 else 4
            big[y - q:y + q, x - q:x + q] = (40, 36, 34)
    def hand(ang, ln, wd, c):
        a = ang * 2 * math.pi
        for i in range(-int(R_ * 0.1), int(R_ * ln)):
            x, y = int(cx + math.sin(a) * i), int(cy - math.cos(a) * i)
            big[y - wd:y + wd, x - wd:x + wd] = c
    hand((hh % 12 + mm / 60) / 12, 0.52, 16, (30, 26, 24)); hand(mm / 60, 0.78, 10, (30, 26, 24))
    hand((t * 6.0) % 1.0, 0.82, 4, (200, 40, 40))
    big[cy - 20:cy + 20, cx - 20:cx + 20] = (200, 40, 40)
    return big
