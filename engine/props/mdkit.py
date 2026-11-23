"""«MOTION DETECTED» episode kit (US): speaker colours, worlds (xAI porch / hall + mddecor) with depth maps, real scale (porch door
405 world px = 2.03 m -> Glenn 1.88 m; hall door 480 px), lights (porch at dusk / hall morning sun), the 2.5D shot wrapper — the same
pipeline as kskit («Ключевой сотрудник», owner 23.11.2026: drawing like the last RU season), the NEON-NOTIFICATION title letters,
the «● MOTION DETECTED» series plate (no «N/6» — test 22.11.2026), the overlay pass, the camera-footage look and the cover maker."""
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
from props import mdcast as C
from props import mddecor as DEC
from props.kskit import wpt, aout, _dil, title_trim, blur

SLUG = 'motion-detected'
COL = dict(glenn=(255, 196, 70), doris=(110, 230, 255), trent=(180, 255, 120), marcy=(255, 140, 200), clerk=(200, 200, 210), mom=(255, 190, 150))
INK = KX.INK
RIM = ((255, 190, 110), (170, 120, 255))                # porch lamp amber / dusk violet
FLOOR = {'porch': (520.0, 3.65, 0.010), 'hall': (560.0, 4.30, 0.012), 'breakroom': (690.0, 3.10, 0.008),
         'postoffice': (690.0, 2.90, 0.008), 'momporch': (528.0, 2.90, 0.010)}


def ws_at(wy, name='porch'):
    key = next((k_ for k_ in FLOOR if name.startswith(k_)), 'porch')
    y0, w0, k = FLOOR[key]
    return w0 + (wy - y0) * k


def A(fn, wx, wy, s, flip=False, pin=None, rim=RIM, **kw):
    return KX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, rim=rim, **kw)


def at(fn, v, ox, oy, s, flip=False, pin=None, near=None, **kw):
    wx, wy = wpt(v, ox, oy)
    a = A(fn, wx, wy, s, flip=flip, pin=pin, **kw)
    if near is not None: a.near = near
    return a


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


def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_porch(v, t=0.0):
    fl = 1.0 - 0.04 * (math.sin(t * 23) > 0.95)
    return Light(amb=(0.98, 0.90, 1.02), keys=_keys(v, [(390, 175, 300 * fl, (255, 196, 110), 0.45),
                                                       (900, 120, 520, (255, 120, 170), 0.16)]), grad=(1.02, 0.90))


def light_hall(v, t=0.0):
    return Light(amb=(1.04, 1.00, 0.94), keys=_keys(v, [(520, 300, 420, (255, 214, 150), 0.36)]), grad=(1.04, 0.96))


LGLOW = [0.0]                                            # E02: Glenn's own lights (0 off .. 1 blazing) light the porch


def light_porch_night(v, t=0.0):
    out = DEC.BLACKOUT[0]
    keys = [(390, 175, 260, (255, 196, 110), 0.55)]
    if out < 0.5:
        keys += [(800, 290, 320, (255, 150, 120), 0.30), (1185, 160, 200, (255, 200, 120), 0.35)]
    if LGLOW[0] > 0: keys += [(560, 120, 520, (255, 236, 170), 0.9 * LGLOW[0])]
    a = 0.62 - 0.22 * out
    return Light(amb=(a, a + 0.03, a + 0.30), keys=_keys(v, keys), grad=(0.98, 0.86))


def light_office(v, t=0.0):
    return Light(amb=(1.02, 1.03, 1.00), keys=_keys(v, [(450, 300, 380, (255, 200, 140), 0.28), (1000, 200, 420, (255, 140, 170), 0.16)]),
                 grad=(1.04, 0.94))


def light_momporch(v, t=0.0):
    tv = 0.30 + 0.08 * math.sin(t * 9) * (math.sin(t * 2.3) > 0)
    return Light(amb=(0.58, 0.62, 0.92), keys=_keys(v, [(380, 240, 240, (255, 196, 110), 0.55), (600, 320, 300, (140, 180, 255), tv)]),
                 grad=(0.98, 0.86))


LIGHT = dict(porch=light_porch, hall=light_hall, porch_night=light_porch_night, breakroom=light_office, postoffice=light_office,
             momporch=light_momporch)


def shot(name, cx, cy, Z, acts=(), par=(0.0, 0.0), fx_=None, pre=None, t=0.0, kick=(0, 0), focus=None, dof_k=0.0, haze=None,
         motes=True, juice=True, rays=None, front=(), bloom=(226, 22, 0.34), vig=0.22, emit=None):
    W_ = world(name)
    v = V(name, cx, cy, Z)
    big = D25.shot25(W_, lambda v_: LIGHT[name](v_, t), cx, cy, Z, depth(name), acts=acts, front=front, par=par, focus=focus, dof_k=dof_k,
                     haze_=haze, bloom_=bloom, rays_=rays, pre=pre, emit=emit, fx_=None, sx=ST.W // 2, sy=ST.H // 2, vig=0, t=t, kick=(0, 0))
    if motes:
        AT.motes(big, t, n=18, col=(255, 230, 190), seed=int(cx * 3) % 11, par=par[0] * 3)
    if fx_: fx_(big, v)
    if juice: AT.juice(big, 1.28, 1.10)
    if vig: fx.vignette(big, vig)
    if kick[0] or kick[1]:
        dx, dy = int(round(kick[0])), int(round(kick[1]))
        big[:] = np.roll(np.roll(big, dy, 0), dx, 1)
    return big


# ---------------------------------------------------------------- titles: neon-notification letters
FILL, GLOW, OUTL = np.array((255, 255, 255)), (90, 220, 255), (14, 20, 44)


def neon_title(lines, size=80, width=OUT_W, colors=None):
    """thick white letters (a faint cyan bottom half), a cyan neon tube edge, a navy outline + drop and a soft cyan glow"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 56) + 60, width, 4), np.uint8)
    y = 28
    for li, line in enumerate(lines):
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 64), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 22 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        o1 = _dil(m, 5, 1); o2 = _dil(m, 12); o3 = _dil(m, 22, 3)
        drop = np.roll(np.roll(o2, 9, 0), 5, 1) & ~o2
        reg = out[y:y + m.shape[0]]
        reg[o3 & ~o2] = GLOW + (90,)
        reg[drop] = (6, 8, 20, 230); reg[o2] = OUTL + (255,); reg[o1 & ~m] = GLOW + (255,)
        rr = np.where(m.any(1))[0]; r0, r1 = rr[0], rr[-1]
        top = np.array(colors[li]) if colors else FILL
        for yy in range(r0, r1 + 1):
            k = (yy - r0) / max(1, r1 - r0)
            c = top * (1 - 0.25 * (k > 0.55)) + np.array((200, 240, 255)) * 0.25 * (k > 0.55)
            mm = m[yy]; reg[yy][mm, :3] = c.astype(np.uint8); reg[yy][mm, 3] = 255
        y += th + 56
    return out


def hook_title(lines, size=80, width=OUT_W):
    return neon_title(lines, size, width)


# ---------------------------------------------------------------- the notification plate (series plate + cover plate)
def notif(w=600, h=120, line1='MOTION DETECTED', line2='Front Door • KNOCKR Pro'):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=(14, 20, 44, 240), outline=(90, 220, 255, 255), width=4)
    r = h // 2 - 22
    cx, cy = 22 + r, h // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(34, 36, 42, 255), outline=(90, 220, 255, 255), width=5)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2], fill=(40, 70, 110, 255))
    d.ellipse([cx - r // 5, cy - r // 5, cx + r // 5, cy + r // 5], fill=(8, 8, 12, 255))
    d.rectangle([cx + r // 4, cy - r // 2, cx + r // 4 + 5, cy - r // 2 + 5], fill=(255, 255, 255, 255))
    tx = cx + r + 22; avail = w - tx - 20
    s1 = int(h * 0.36)
    while O.pfont(s1).getlength(line1) > avail and s1 > 12: s1 -= 2
    d.text((tx, int(h * 0.14)), line1, font=O.pfont(s1), fill=(255, 255, 255))
    s2 = int(h * 0.20)
    while O.pfont(s2).getlength(line2) > avail and s2 > 10: s2 -= 1
    d.text((tx, int(h * 0.62)), line2, font=O.pfont(s2), fill=(120, 220, 255))
    return np.array(im)


def badge():
    return notif(430, 70)


class Show:
    def __init__(s, epi, hook, hook_t=(0.10, 2.4), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1240, hook_y=280,
                 hook_size=78, badge_until=None):
        s.epi = epi
        s.badge = badge()
        s.hook = neon_title(hook, hook_size) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default
        s.badge_until = badge_until

    def apply(s, big, t, shot_):
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        if s.badge_until is None or t < s.badge_until: O.overlay(big, s.badge, 36, 96, 1.0)
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


def st(text, fg=(110, 230, 255), size=58):
    return O.sticker(text, fg=fg, size=size)


# ---------------------------------------------------------------- the doorbell-camera look (fisheye, desaturated, REC, timestamp)
def cam_look(big, t, stamp='11/23  2:14:07 PM', label='FRONT DOOR'):
    h, w = big.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = (xx - w / 2) / (w / 2); ny = (yy - h / 2) / (h / 2)
    r2 = nx * nx * 0.55 + ny * ny * 0.30
    sx = np.clip((w / 2 + nx * (w / 2) * (1 - 0.22 * r2)), 0, w - 1).astype(np.int32)
    sy = np.clip((h / 2 + ny * (h / 2) * (1 - 0.22 * r2)), 0, h - 1).astype(np.int32)
    img = big[sy, sx].astype(np.float32)
    g = img.mean(axis=2, keepdims=True)
    img = img * 0.55 + g * 0.45
    img = img * np.array((0.92, 1.02, 1.04)) + 6
    rng = np.random.default_rng(int(t * 30))
    img += rng.normal(0, 7, (h, w, 1))
    img[(yy.astype(int) % 6) < 1] *= 0.9
    big[:] = np.clip(img, 0, 255).astype(np.uint8)
    fx.vignette(big, 0.6)
    st_ = O.sticker(stamp, fg=(255, 255, 255), size=34)
    O.overlay(big, st_, 40, h - 300, 1.0)
    lb = O.sticker(label, fg=(120, 220, 255), size=34)
    O.overlay(big, lb, w - lb.shape[1] - 40, 220, 1.0)
    if int(t * 2) % 2 == 0:
        Y, X = np.mgrid[0:h, 0:w]
        big[np.hypot(X - 70, Y - 240) < 16] = (240, 40, 40)
    rec = O.sticker('REC', fg=(240, 60, 60), size=34)
    O.overlay(big, rec, 96, 220, 1.0)
    return big


# ---------------------------------------------------------------- covers (profile grid rule 10.10.2026)
GRID = (240, 1680)
SAFE_BOTTOM = 1520


def cover_make(frame, title, out='cover.png', title_size=96):
    big = frame.copy()
    p = notif(620, 120)
    py = GRID[0] + 10
    t = neon_title(title, title_size)
    ty = py + p.shape[0] - 6
    y1 = ty + t.shape[0]
    shade = np.zeros((big.shape[0], 1, 1), np.float32); shade[:y1, 0, 0] = 0.30
    n_ = len(shade[y1:y1 + 140]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.30, 0.0, 140)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t, 0, ty, 1.0)
    Image.fromarray(big).save(out)
    g = big[GRID[0]:GRID[1]].copy()
    g[SAFE_BOTTOM - GRID[0]:] = (g[SAFE_BOTTOM - GRID[0]:] * 0.45).astype(np.uint8)
    Image.fromarray(g).resize((270, 360), Image.LANCZOS).save(str(out).replace('.png', '_grid.png'))
    return big


def phone_insert(t, lines=('PARCELZ', 'SIGNATURE REQUIRED', 'Delivery TODAY', '8 AM – 9 PM'), bg=(30, 36, 60)):
    """full-frame phone screen: the delivery app"""
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = bg
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([90, 180, OUT_W - 90, OUT_H - 180], 60, fill=(20, 20, 24), outline=(90, 90, 100), width=10)
    d.rounded_rectangle([120, 240, OUT_W - 120, OUT_H - 240], 30, fill=(240, 244, 250))
    d.rectangle([120, 240, OUT_W - 120, 420], fill=(30, 160, 160))
    d.text((170, 290), lines[0], font=O.pfont(80), fill=(255, 255, 255))
    y = 520
    for i, ln in enumerate(lines[1:]):
        sz = (40, 52, 70)[i % 3]
        col = ((200, 40, 40), (40, 40, 50), (30, 60, 140))[i % 3]
        d.text((170, y), ln, font=O.pfont(sz), fill=col); y += sz + 50
    d.rounded_rectangle([170, y + 40, OUT_W - 170, y + 180], 24, fill=(246, 128, 40))
    d.text((215, y + 88), 'OUT FOR DELIVERY', font=O.pfont(34), fill=(255, 255, 255))
    return np.array(im)
