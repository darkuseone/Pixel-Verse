"""«Grim Ride» episode kit: speaker colours, moonlit night lights, worlds (xAI backgrounds), the series hook title (pumpkin -> neon
yellow stepped fill, violet-black outline, acid-green halo), overlays pass (Show), Halloween FX (falling leaves, ground fog, lightning,
speed streaks), full-frame inserts drawn in code (the e-bike display, the DoomDash app).
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
from props import bytfx as B
from props import chikit as CK
from props import grimpix as GX
from props import grimcast as GC

SLUG = 'grim-ride'
COL = dict(grim=(200, 170, 255), edgar=(170, 255, 90), harold=(255, 160, 60), todd=(90, 225, 255), kayden=(255, 100, 190),
           dashley=(255, 210, 90), grimph=(200, 170, 255), mom=(255, 140, 140), judge=(90, 225, 255))
INK = GX.INK
PUMP = ((255, 244, 120), (255, 196, 60), (255, 140, 40))          # hook title fill: neon yellow -> pumpkin
HALO = (150, 255, 110)
shot = CK.shot
J, hit = CK.J, CK.hit
SP = 2.0                                                            # people: output px per sprite px at Z = 1


def A(fn, wx, wy, s, flip=False, pin=None, **kw):
    return GX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, **kw)


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


# ---------------------------------------------------------------- lights: cold moonlit ambient, warm lantern pools, moon rim from above-left
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_night(v, lamps=(), amb=(0.86, 0.84, 1.06)):
    return Light(amb=amb, keys=_keys(v, lamps), rim=(-1, -1, (160, 196, 255), 0.55), grad=(1.0, 1.08))


STREET_LAMPS = ((570, 330, 520, (255, 190, 110), 0.35), (920, 330, 520, (255, 190, 110), 0.35), (240, 420, 380, (255, 140, 60), 0.3))
YARD_LAMPS = ((650, 380, 600, (255, 170, 90), 0.35), (180, 520, 360, (200, 120, 255), 0.35), (930, 520, 360, (200, 120, 255), 0.35))
PORCH_LAMPS = ((222, 190, 640, (255, 200, 120), 0.5), (600, 440, 380, (255, 140, 50), 0.45))
def light_street(v): return light_night(v, STREET_LAMPS)
def light_yard(v): return light_night(v, YARD_LAMPS)
def light_porch(v): return light_night(v, PORCH_LAMPS, amb=(0.92, 0.86, 1.0))
GANG_LAMPS = ((290, 175, 520, (255, 200, 120), 0.4), (640, 520, 620, (230, 240, 255), 0.4), (210, 570, 300, (255, 140, 50), 0.35))
HILL_LAMPS = ((1060, 250, 700, (255, 240, 200), 0.3), (820, 580, 300, (255, 140, 50), 0.35), (80, 540, 300, (255, 140, 50), 0.35))
def light_gang(v): return light_night(v, GANG_LAMPS, amb=(0.84, 0.86, 1.08))
def light_hill(v): return light_night(v, HILL_LAMPS, amb=(0.9, 0.86, 1.06))


# ---------------------------------------------------------------- worlds
_W = {}


def world(name):
    if name not in _W:
        _W[name] = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png')
    return _W[name]


# ---------------------------------------------------------------- FX
def leaves(big, t, n=26, seed=1, wind=1.0, speed=1.0):
    """orange autumn leaves tumbling across the frame (screen space)"""
    r = np.random.default_rng(seed)
    cols = [(230, 120, 40), (200, 80, 30), (250, 170, 60), (150, 60, 30)]
    for i in range(n):
        x0 = r.random() * (OUT_W + 600); y0 = r.random() * OUT_H; vx = (300 + r.random() * 500) * wind * speed; vy = 80 + r.random() * 120
        ph = r.random() * 6
        x = (x0 - t * vx) % (OUT_W + 600) - 300
        y = (y0 + t * vy + 40 * math.sin(t * 3 + ph)) % (OUT_H + 100) - 50
        s = 12 + int(r.random() * 10)
        w = int(s * (0.4 + 0.6 * abs(math.sin(t * 5 + ph))))
        xi, yi = int(x), int(y)
        if 0 <= xi < OUT_W - s and 0 <= yi < OUT_H - s:
            big[yi:yi + s // 2, xi:xi + max(4, w)] = cols[i % 4]
            big[yi + s // 2:yi + s, xi + 2:xi + 2 + max(4, w - 4)] = cols[(i + 1) % 4]


def fog(big, t, y0=1300, y1=OUT_H, a=0.30, col=(150, 120, 210), speed=40):
    """low drifting ground fog: soft horizontal bands"""
    h = y1 - y0
    if h <= 0: return
    xs = np.arange(OUT_W, dtype=np.float32)
    ys = np.arange(h, dtype=np.float32)[:, None]
    k = (0.5 + 0.25 * np.sin(xs / 140.0 + t * speed / 140.0) + 0.25 * np.sin(xs / 61.0 - t * speed / 90.0 + ys / 40.0))
    v = np.clip(k * np.clip(ys / h * 1.4, 0, 1), 0, 1)
    v = np.floor(v * 4) / 4 * a                                       # stepped, pixel-art bands
    reg = big[y0:y1].astype(np.float32)
    big[y0:y1] = (reg * (1 - v[..., None]) + np.array(col, np.float32) * v[..., None]).astype(np.uint8)


def lightning(big, t, t0, seed=3):
    """a forked bolt + screen flash at t0 (lasts 0.25 s)"""
    u = t - t0
    if not (0 <= u < 0.28): return
    k = 1 - u / 0.28
    O.flash(big, 0.45 * k if u > 0.06 else 0.75)
    r = np.random.default_rng(seed)
    x = 200 + r.random() * 680; y = 0
    while y < 700:
        nx = x + (r.random() - 0.5) * 120; ny = y + 40 + r.random() * 50
        n = int(max(abs(nx - x), abs(ny - y)) / 6) + 1
        for q in range(n + 1):
            px, py = int(x + (nx - x) * q / n), int(y + (ny - y) * q / n)
            if 0 <= px < OUT_W - 12 and 0 <= py < OUT_H - 12:
                big[py:py + 12, px:px + 12] = (240, 236, 255)
        x, y = nx, ny


def speed_streaks(big, t, k=1.0, n=34, seed=0, col=(200, 190, 255), dirn=-1):
    r = np.random.default_rng(seed)
    for i in range(int(n * k)):
        y = int(r.random() * OUT_H); sp = 2400 + r.random() * 1800; ln = int(120 + r.random() * 300)
        x = int(((t * sp + r.random() * 4000) % (OUT_W + 600)) - 300)
        if dirn < 0: x = OUT_W - x
        a, b = max(0, x), min(OUT_W, x + ln)
        if a < b: big[y:y + 6, a:b] = (big[y:y + 6, a:b] * 0.4 + np.array(col) * 0.6).astype(np.uint8)


def dof(big, r=6):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


def glow_ring(big, cx, cy, r, col, a):
    fx.glow(big, cx, cy, r, col, a)


# ---------------------------------------------------------------- hook title + overlays
def _dil(m, r, step=2):
    d = m.copy()
    for dx in range(-r, r + 1, step):
        for dy in range(-r, r + 1, step):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def hook_title(lines, size=64, width=OUT_W):
    """Press Start 2P, neon-yellow -> pumpkin stepped fill, thick violet-black outline, thin acid-green halo, white top highlight"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 56) + 60, width, 4), np.uint8)
    y = 24
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 56), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 20 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        ol = _dil(m, 11)
        halo = _dil(ol, 6) & ~ol
        reg = out[y:y + m.shape[0]]
        reg[halo] = HALO + (255,)
        reg[ol] = INK + (255,)
        rows = np.where(m.any(1))[0]; r0, r1 = rows[0], rows[-1]
        for yy in range(m.shape[0]):
            k = (yy - r0) / max(1, r1 - r0)
            col = PUMP[0] if k < 0.34 else PUMP[1] if k < 0.67 else PUMP[2]
            reg[yy][m[yy]] = col + (255,)
        reg[m & ~np.roll(m, 7, 0)] = (255, 255, 236, 255)
        y += th + 56
    return out


class Show:
    def __init__(s, epi, n, hook, hook_t=(0.10, 2.6), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330, hook_y=150, total=6,
                 hook_size=62):
        s.epi = epi
        s.badge = O.make_badge(f'SEASON 1 • EPISODE {n}/{total}')
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


# ---------------------------------------------------------------- full-frame inserts
def _font(sz): return O.pfont(sz)


def _bold(sz): return ImageFont.truetype(P.FONT_BOLD, sz)


def display_insert(big, t, pct=13, dead=False, blink=True, y0=0, y1=OUT_H, label='PALE HORSE 2', mph=None, banner=None):
    """the e-bike handlebar display filling the frame: battery % blinking, «PALE HORSE 2», speed; black when dead"""
    reg = big[y0:y1]
    h = y1 - y0
    reg[:] = (reg * 0.35).astype(np.uint8)
    bx0, by0, bx1, by1 = 110, int(h * 0.22), OUT_W - 110, int(h * 0.78)
    reg[by0 - 18:by1 + 18, bx0 - 18:bx1 + 18] = (20, 20, 26)
    reg[by0:by1, bx0:bx1] = (16, 34, 26) if not dead else (6, 6, 8)
    if dead:
        mid = (by0 + by1) // 2
        reg[mid - 4:mid + 4, OUT_W // 2 - 60:OUT_W // 2 + 60] = (200, 210, 220)
        return
    yy = np.arange(by0, by1)[:, None]
    scan = ((yy - by0) % 10 < 2).repeat(bx1 - bx0, 1)
    reg[by0:by1, bx0:bx1][scan] = (10, 26, 20)
    on = (int(t * 4) % 2 == 0) or not blink
    low = pct < 20
    col = ((255, 70, 60) if on else (140, 40, 36)) if low else GC.LIME
    img = Image.fromarray(reg[by0:by1, bx0:bx1]); d = ImageDraw.Draw(img); d.fontmode = '1'
    W_, H_ = img.size
    # battery icon + %
    d.rectangle([60, H_ // 2 - 120, 420, H_ // 2 + 40], outline=col, width=14)
    d.rectangle([420, H_ // 2 - 70, 450, H_ // 2 - 10], fill=col)
    w = int(330 * max(0.0, min(1.0, pct / 100)))
    if w > 0: d.rectangle([75, H_ // 2 - 105, 75 + w, H_ // 2 + 25], fill=col)
    d.text((500, H_ // 2 - 120), f'{pct}%', font=_font(130), fill=col)
    d.text((60, 40), label, font=_font(34), fill=(120, 200, 150))
    d.text((60, H_ - 90), 'MPH', font=_font(30), fill=(120, 200, 150))
    d.text((200, H_ - 110), mph if mph is not None else ('28' if pct > 5 else '03'), font=_font(60), fill=(200, 255, 220))
    if low and banner is None: d.text((W_ - 380, 40), 'LOW BATT', font=_font(34), fill=col)
    if banner:
        on2 = int(t * 3) % 2 == 0
        d.rectangle([W_ - 470, 24, W_ - 40, 100], fill=(255, 200, 60) if on2 else (200, 140, 40))
        d.text((W_ - 255, 62), banner, font=_font(34), fill=(30, 16, 40), anchor='mm')
    reg[by0:by1, bx0:bx1] = np.array(img)


def phone_app(big, t, mode='pickup', u=0.0, thumb=True, **kw):
    """the DoomDash courier app, full frame. mode 'pickup' (new pickup: HAROLD, 97) or 'rated' (★ «Too slow.», rating drops)"""
    big[:] = (18, 10, 30)
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    # phone body
    d.rounded_rectangle([90, 120, OUT_W - 90, OUT_H - 80], 70, fill=(10, 8, 14), outline=(70, 60, 90), width=10)
    sx0, sy0, sx1, sy1 = 130, 200, OUT_W - 130, OUT_H - 140
    d.rectangle([sx0, sy0, sx1, sy1], fill=(36, 18, 54))
    d.rectangle([sx0, sy0, sx1, sy0 + 150], fill=(150, 60, 220))
    d.text((sx0 + 40, sy0 + 50), 'DOOMDASH', font=_font(56), fill=(255, 255, 255))
    d.ellipse([sx1 - 120, sy0 + 35, sx1 - 40, sy0 + 115], fill=(236, 226, 198))          # tiny skull logo
    d.ellipse([sx1 - 105, sy0 + 60, sx1 - 88, sy0 + 78], fill=(36, 18, 54)); d.ellipse([sx1 - 72, sy0 + 60, sx1 - 55, sy0 + 78], fill=(36, 18, 54))
    if mode == 'pickup':
        d.rounded_rectangle([sx0 + 30, sy0 + 300, sx1 - 30, sy0 + 900], 30, fill=(56, 30, 80))
        d.text((sx0 + 70, sy0 + 640), 'HAROLD, 97', font=_font(52), fill=(255, 255, 255))
        d.text((sx0 + 70, sy0 + 720), 'Maple Hollow Ct.', font=_bold(46), fill=(200, 180, 240))
        d.text((sx0 + 70, sy0 + 790), 'PAYOUT: 1 SOUL', font=_font(32), fill=(255, 200, 80))
        d.text((sx0 + 40, sy0 + 960), 'YOUR RATING  4.2', font=_font(36), fill=(255, 255, 255))
        d.text((sx0 + 40, sy0 + 1030), '★★★★☆', font=_bold(80), fill=(255, 210, 60))
        d.rounded_rectangle([sx0 + 30, sy1 - 220, sx1 - 30, sy1 - 60], 40, fill=(150, 255, 110))
        d.text((OUT_W // 2, sy1 - 140), 'ACCEPT', font=_font(56), fill=(20, 10, 30), anchor='mm')
        big[:] = np.array(im)
        # Harold's mugshot on the card (head only, cropped into a frame)
        from props.dibspix import blit
        sc = 9.0
        sp = GX.draw(GC.harold, sc, t=t, pose='stand', expr='bored', hires=2)
        hx, hy = sp.anchors['head']
        tmp = np.zeros((360, 360, 3), np.uint8); tmp[:] = (90, 60, 120)
        blit(tmp, sp, 180 - hx * sc, 200 + hy * sc, sc)
        x0 = OUT_W // 2 - 150; y0 = sy0 + 320
        big[y0:y0 + 300, x0:x0 + 300] = tmp[40:340, 30:330]
        big[y0 - 6:y0, x0 - 6:x0 + 306] = (150, 255, 110); big[y0 + 300:y0 + 306, x0 - 6:x0 + 306] = (150, 255, 110)
        big[y0:y0 + 300, x0 - 6:x0] = (150, 255, 110); big[y0:y0 + 300, x0 + 300:x0 + 306] = (150, 255, 110)
    elif mode == 'captcha':
        big[:] = np.array(im)
        captcha(big, t, u, kw.get('taps', ()), (sx0, sy0, sx1, sy1))
        im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
        big[:] = np.array(im)
    elif mode == 'chat':
        msgs = kw.get('msgs', [])
        d.text((sx0 + 40, sy0 + 170), 'SUPPORT CHAT', font=_font(34), fill=(200, 170, 255))
        y = sy0 + 250
        for who, txt_, t0 in msgs:
            if u < t0: continue
            k = min(1.0, (u - t0) / 0.15)
            bot = who == 'bot'
            f = _bold(48)
            lines_ = _wrap(d, txt_, f, sx1 - sx0 - 200)
            h = 70 * len(lines_) + 40
            x0 = sx0 + 30 if bot else sx0 + 170
            x1 = sx1 - 170 if bot else sx1 - 30
            d.rounded_rectangle([x0, y, x1, y + h], 34, fill=(255, 200, 90) if bot else (150, 60, 220))
            for i, ln in enumerate(lines_):
                d.text((x0 + 30, y + 22 + 70 * i), ln, font=f, fill=(30, 16, 40) if bot else (255, 255, 255))
            if bot: d.text((x0, y - 44), 'DASHLEY', font=_font(24), fill=(255, 200, 90))
            y += h + 70
        big[:] = np.array(im)
    elif mode == 'transfer' or mode == 'wait':
        d.text((OUT_W // 2, sy0 + 330), 'PLEASE HOLD', font=_font(56), fill=(255, 255, 255), anchor='mm')
        cx, cy = OUT_W // 2, sy0 + 640
        for i in range(12):                                                     # pixel spinner
            a = i / 12 * 2 * math.pi
            on = (int(t * 12) - i) % 12 < 4
            x, y = cx + math.cos(a) * 140, cy + math.sin(a) * 140
            d.rectangle([x - 18, y - 18, x + 18, y + 18], fill=(200, 170, 255) if on else (70, 50, 100))
        if mode == 'transfer':
            d.text((OUT_W // 2, sy0 + 930), 'Transferring you to', font=_bold(52), fill=(220, 210, 240), anchor='mm')
            d.text((OUT_W // 2, sy0 + 1010), 'a SPECIALIST...', font=_bold(52), fill=(255, 200, 90), anchor='mm')
        else:
            d.text((OUT_W // 2, sy0 + 900), 'ESTIMATED WAIT:', font=_font(40), fill=(220, 210, 240), anchor='mm')
            k = min(1.0, u / 0.6)
            d.text((OUT_W // 2, sy0 + 1010), 'ETERNITY', font=_font(int(40 + 40 * k)), fill=(255, 90, 80), anchor='mm')
            d.text((OUT_W // 2, sy0 + 1110), 'Your call is important to us', font=_bold(40), fill=(160, 140, 190), anchor='mm')
        big[:] = np.array(im)
    elif mode == 'incoming':
        d.rectangle([sx0, sy0, sx1, sy1], fill=(20, 12, 34))
        d.text((OUT_W // 2, sy0 + 260), 'INCOMING CALL', font=_font(40), fill=(200, 170, 255), anchor='mm')
        r = 150 + 18 * math.sin(t * 18)
        d.ellipse([OUT_W // 2 - r, sy0 + 560 - r, OUT_W // 2 + r, sy0 + 560 + r], outline=(150, 255, 110), width=10)
        d.ellipse([OUT_W // 2 - 120, sy0 + 440, OUT_W // 2 + 120, sy0 + 680], fill=(150, 60, 220))
        d.text((OUT_W // 2, sy0 + 560), 'DD', font=_font(80), fill=(255, 255, 255), anchor='mm')
        d.text((OUT_W // 2, sy0 + 800), 'DOOMDASH', font=_font(52), fill=(255, 255, 255), anchor='mm')
        d.text((OUT_W // 2, sy0 + 880), 'SUPPORT', font=_font(52), fill=(255, 200, 90), anchor='mm')
        d.text((OUT_W // 2, sy0 + 960), 'calling you, the specialist', font=_bold(40), fill=(160, 140, 190), anchor='mm')
        for x, c in ((OUT_W // 2 - 200, (255, 80, 80)), (OUT_W // 2 + 200, (120, 230, 120))):
            d.ellipse([x - 80, sy1 - 260, x + 80, sy1 - 100], fill=c)
        big[:] = np.array(im)
    elif mode == 'deadline':
        d.text((sx0 + 40, sy0 + 210), 'FINAL PICKUP', font=_font(48), fill=(255, 200, 90))
        d.text((sx0 + 40, sy0 + 300), 'HAROLD, 97', font=_font(52), fill=(255, 255, 255))
        sec = max(0, 59 - int(u * 6))
        d.text((OUT_W // 2, sy0 + 560), f'0:{sec:02d}', font=_font(150), fill=(255, 90, 80) if int(t * 4) % 2 else (255, 160, 140), anchor='mm')
        d.text((OUT_W // 2, sy0 + 700), 'DEACTIVATION', font=_font(44), fill=(255, 90, 80), anchor='mm')
        d.text((sx0 + 40, sy0 + 900), 'YOUR RATING  3.5', font=_font(40), fill=(255, 90, 80))
        d.text((sx0 + 40, sy0 + 980), '★★★½☆', font=_bold(90), fill=(255, 210, 60))
        big[:] = np.array(im)
    elif mode == 'resched':
        d.text((sx0 + 40, sy0 + 210), 'PICKUP', font=_font(48), fill=(150, 255, 110))
        d.text((sx0 + 40, sy0 + 280), 'RESCHEDULED:', font=_font(48), fill=(150, 255, 110))
        d.text((sx0 + 40, sy0 + 370), 'NEXT HALLOWEEN', font=_font(48), fill=(255, 200, 90))
        k = min(1.0, max(0.0, (u - 0.8) / 0.6))
        if k > 0:
            d.text((sx0 + 40, sy0 + 520), 'HAROLD RATED YOU:', font=_font(40), fill=(255, 255, 255))
            n = int(1 + 4 * k)
            d.text((sx0 + 40, sy0 + 600), '★' * n + '☆' * (5 - n), font=_bold(130), fill=(255, 210, 60))
            d.rounded_rectangle([sx0 + 30, sy0 + 800, sx1 - 30, sy0 + 960], 30, fill=(56, 30, 80))
            d.text((sx0 + 70, sy0 + 850), '"Great ride."', font=_bold(64), fill=(255, 255, 255))
            d.text((sx0 + 40, sy0 + 1040), 'YOUR RATING  5.0', font=_font(40), fill=(150, 255, 110))
        big[:] = np.array(im)
    else:
        d.text((sx0 + 40, sy0 + 210), 'PICKUP FAILED', font=_font(48), fill=(255, 90, 80))
        d.text((sx0 + 40, sy0 + 330), 'HAROLD RATED', font=_font(44), fill=(255, 255, 255))
        d.text((sx0 + 40, sy0 + 400), 'YOUR PICKUP:', font=_font(44), fill=(255, 255, 255))
        d.text((sx0 + 40, sy0 + 500), '★☆☆☆☆', font=_bold(130), fill=(255, 210, 60))
        d.rounded_rectangle([sx0 + 30, sy0 + 700, sx1 - 30, sy0 + 860], 30, fill=(56, 30, 80))
        d.text((sx0 + 70, sy0 + 750), '"Too slow."', font=_bold(64), fill=(255, 255, 255))
        k = sm(min(1.0, u / 0.5))
        r = 4.2 - 0.3 * k
        d.text((sx0 + 40, sy0 + 960), f'YOUR RATING  {r:.1f}', font=_font(40), fill=(255, 90, 80) if k > 0.5 else (255, 255, 255))
        d.text((sx0 + 40, sy0 + 1040), 'DEACTIVATION BELOW 3.5', font=_font(28), fill=(200, 160, 220))
        big[:] = np.array(im)
    if thumb:                                                                              # a bony thumb on the screen edge
        sp = GX.draw(GC.bony_hand, 22.0, x=0.0, y=0.0, d=-1.0, grip=False)
        from props.dibspix import blit
        blit(big, sp, OUT_W - 160, OUT_H - 120 + 6 * math.sin(t * 3), 22.0)


def _wrap(d, txt, f, w):
    out, cur = [], ''
    for word in txt.split():
        nxt = (cur + ' ' + word).strip()
        if d.textlength(nxt, font=f) > w and cur: out.append(cur); cur = word
        else: cur = nxt
    if cur: out.append(cur)
    return out


_ICONS = {}


def _icon(key, size):
    """a captcha tile picture: one of the cast (head close-up) or a prop, drawn by the series' own sprites"""
    if (key, size) in _ICONS: return _ICONS[(key, size)]
    from props.dibspix import blit
    tile = np.zeros((size, size, 3), np.uint8)
    tile[:] = {'todd': (90, 140, 200), 'kevin': (60, 50, 90), 'harold': (200, 150, 90), 'pumpkin': (40, 90, 60), 'kayden': (150, 80, 140),
               'edgar': (120, 160, 120), 'grim': (90, 70, 120), 'sign': (60, 100, 140), 'moon': (20, 20, 50)}[key]
    spec = {'todd': (GC.todd, 'head', 9.0, dict(phone=False, expr='hype')), 'harold': (GC.harold, 'head', 9.0, dict(pose='stand', expr='bored')),
            'kayden': (GC.kayden, 'head', 9.0, dict(bike=False)), 'edgar': (GC.edgar, 'head', 9.0, dict(perch=False, cam=True)),
            'grim': (GC.grim, 'head', 7.0, dict(ride=False, scythe=False, expr='bored')), 'kevin': (GC.kevin, 'head', 6.5, {}),
            'pumpkin': (GC.pumpkin_inflatable, None, 7.0, {}), 'sign': (GC.countdown_sign, None, 6.0, dict(days=4)), 'moon': (None, None, 0, {})}[key]
    fn, pin, sc, kw = spec
    if fn is not None:
        sp = GX.draw(fn, sc, t=0.3, hires=1, **kw) if fn not in (GC.countdown_sign,) else GX.draw(fn, sc, hires=1, **kw)
        if pin:
            hx, hy = sp.anchors[pin]
            blit(tile, sp, size / 2 - hx * sc, size / 2 + 20 + hy * sc, sc)
        else:
            blit(tile, sp, size / 2, size - 20, sc)
    else:
        yy, xx = np.mgrid[0:size, 0:size]
        tile[(xx - size / 2) ** 2 + (yy - size / 2) ** 2 < (size * 0.32) ** 2] = (236, 230, 200)
    _ICONS[(key, size)] = tile
    return tile


CAPTCHA = ['todd', 'kevin', 'harold', 'pumpkin', 'kayden', 'edgar', 'grim', 'sign', 'moon']
ALIVE = {'todd', 'harold', 'kayden', 'edgar'}


def captcha(big, t, u, taps, box):
    """«SELECT ALL SQUARES WITH A PULSE»: 3x3 tiles of the cast, heartbeat lines under the living ones; a tapped tile flatlines
    (red line + X) — except Harold's, which keeps beating (ERROR). taps = [(tile_index, u_tap), ...]"""
    sx0, sy0, sx1, sy1 = box
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([sx0 + 20, sy0 + 170, sx1 - 20, sy0 + 330], fill=(60, 120, 230))
    d.text((sx0 + 50, sy0 + 195), 'Select all squares', font=_bold(46), fill=(255, 255, 255))
    d.text((sx0 + 50, sy0 + 255), 'with a PULSE', font=_bold(52), fill=(255, 255, 255))
    big[:] = np.array(im)
    size = (sx1 - sx0 - 80) // 3
    tapped = {i: ut for i, ut in taps if u >= ut}
    for i, key in enumerate(CAPTCHA):
        x0 = sx0 + 30 + (i % 3) * (size + 10); y0 = sy0 + 360 + (i // 3) * (size + 10)
        big[y0:y0 + size, x0:x0 + size] = _icon(key, size)
        if key in ALIVE:
            dead = i in tapped and key != 'harold'
            ly = y0 + size - 40
            big[ly - 34:ly + 34, x0:x0 + size] = (big[ly - 34:ly + 34, x0:x0 + size] * 0.35).astype(np.uint8)
            col = (255, 70, 60) if dead else (120, 255, 120)
            for x in range(0, size, 6):
                ph = (x / size * 3 - t * 2.5) % 1.0
                yv = 0 if dead else (-26 if 0.45 < ph < 0.5 else (20 if 0.5 <= ph < 0.55 else 0))
                big[ly + yv - 3:ly + yv + 3, x0 + x:x0 + x + 6] = col
            if dead:
                k = min(1.0, (u - tapped[i]) / 0.12)
                for q in range(int(size * 0.8 * k)):
                    for (a, b) in ((q, q), (q, size * 0.8 - q)):
                        xa, ya = int(x0 + size * 0.1 + a), int(y0 + size * 0.1 + b)
                        big[ya:ya + 10, xa:xa + 10] = (255, 60, 60)
            elif i in tapped:
                if int(t * 8) % 2: big[y0:y0 + 8, x0:x0 + size] = (255, 200, 60); big[y0 + size - 8:y0 + size, x0:x0 + size] = (255, 200, 60)
        if i in tapped:
            big[y0:y0 + 6, x0:x0 + size] = (60, 120, 230); big[y0:y0 + size, x0:x0 + 6] = (60, 120, 230)


def confetti(big, t, t0, n=160, seed=4):
    """Halloween confetti burst (orange / violet / lime / bone) falling from t0"""
    if t < t0: return
    r = np.random.default_rng(seed)
    cols = [(255, 140, 40), (180, 120, 255), (150, 255, 110), (236, 226, 198), (255, 90, 80)]
    u = t - t0
    for i in range(n):
        x0 = r.random() * OUT_W; vy = 260 + r.random() * 380; ph = r.random() * 6
        x = x0 + math.sin(u * 3 + ph) * 60
        y = -60 + (u * vy + r.random() * 300) - 300
        if 0 <= y < OUT_H - 16 and 0 <= x < OUT_W - 16:
            w = 18 if int((u * 8 + ph) % 2) else 8
            big[int(y):int(y) + 14, int(x):int(x) + w] = cols[i % len(cols)]


def clock(big, txt, sub=None, k=1.0, col=(255, 90, 80), y=760, size=190):
    """a big digital clock over the frame (pixel font), optional caption under it"""
    img = Image.new('RGBA', (OUT_W, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rounded_rectangle([60, 40, OUT_W - 60, 340], 40, fill=(10, 6, 18, 230), outline=col + (255,), width=10)
    d.text((OUT_W // 2, 190), txt, font=_font(size), fill=col + (255,), anchor='mm')
    for i, ln in enumerate((sub or '').split('\n')):                  # sub lines: white with an ink outline, stacked under the box
        if ln: d.text((OUT_W // 2, 410 + i * 56), ln, font=_font(44), fill=(255, 255, 255, 255), anchor='mm', stroke_width=5, stroke_fill=(10, 6, 18, 255))
    O.overlay(big, np.array(img), 0, y - 190, k)


def rope_line(big, a, b, sag=60, w=10, col=(206, 172, 110)):
    (x0, y0), (x1, y1) = a, b
    n = int(max(abs(x1 - x0), abs(y1 - y0)) / 4) + 2
    pts = [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n + sag * 4 * (i / n) * (1 - i / n)) for i in range(n + 1)]
    for pad, cf in ((3, lambda i: INK), (0, lambda i: col if (i // 3) % 2 else (176, 140, 84))):
        for i, (x, y) in enumerate(pts):
            xa, ya = int(x - w / 2) - pad, int(y - w / 2) - pad
            xb, yb = xa + w + 2 * pad, ya + w + 2 * pad
            if xb > 0 and yb > 0 and xa < OUT_W and ya < OUT_H:
                big[max(0, ya):min(OUT_H, yb), max(0, xa):min(OUT_W, xb)] = cf(i)


def fireworks(big, t, t0, bursts=((300, 400), (780, 300), (540, 520)), cols=((255, 140, 40), (180, 120, 255), (150, 255, 110))):
    for i, (x, y) in enumerate(bursts):
        u = (t - t0 - i * 0.5) % 1.6
        if u < 0 or u > 1.2: continue
        r = 40 + 260 * u; a = 1 - u / 1.2
        for j in range(16):
            ang = j / 16 * 2 * math.pi
            px, py = int(x + math.cos(ang) * r), int(y + math.sin(ang) * r + 60 * u * u)
            if 0 <= px < OUT_W - 14 and 0 <= py < OUT_H - 14:
                c = np.array(cols[i % len(cols)]) * a + big[py, px] * (1 - a)
                big[py:py + 14, px:px + 14] = c.astype(np.uint8)
