"""«Thanks, Randy» episode kit: speaker colours, store lights (warm lamps above + cold freezer light), worlds (xAI backgrounds +
randydecor), the series title («Price-Tag Feast»: orange -> cranberry-pink stepped fill, a thick «roast crust» brown outline, an icy
frost cap on the letters), the sitcom day card, the THAW-O-METER, the big self-checkout screen insert, freezer vapour, the overlays pass
and a close-up helper. Shot compositing reuses props/chikit.shot (world view + direct actors + fx + vignette).
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
from props import randypix as RX
from props import randycast as C
from props import randydecor as DEC

SLUG = 'thanks-randy'
COL = dict(randy=(255, 150, 50), tom=(150, 220, 255), joyce=(206, 160, 255), brayden=(170, 255, 90), scandee=(235, 240, 255),
           patty=(255, 120, 120), carol=(255, 200, 120), carol2=(255, 200, 120), dunn=(255, 90, 60), kyle=(200, 200, 200),
           family=(255, 255, 255))
INK = RX.INK
CRUST = (92, 46, 26)                                   # title outline: roast crust brown
FILL = ((255, 186, 60), (255, 120, 60), (240, 70, 110))  # orange (top) -> coral -> cranberry-pink (bottom)
ICE = (206, 238, 255)
J, hit = CK.J, CK.hit


def A(fn, wx, wy, s, flip=False, pin=None, **kw):
    return RX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, **kw)


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


def anchor_world(fn, name, wx, wy, s_world, flip=False, **kw):
    """world position of a sprite anchor (e.g. the kiosk's bagging shelf) for an object standing at (wx, wy), s_world world px / sprite px"""
    sp = RX.draw(fn, 3.0, **kw)
    px, py = sp.anchors[name]
    return wx + (-px if flip else px) * s_world, wy - py * s_world


# ---------------------------------------------------------------- lights
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_store(v, alarm=0.0):
    keys = [(640, 40, 900, (255, 236, 190), 0.30), (160, 420, 520, (150, 210, 255), 0.30)]
    if alarm > 0: keys.append((900, 300, 700, (255, 60, 60), 0.35 * alarm))
    return Light(amb=(1.02, 1.0, 0.98), keys=_keys(v, keys), rim=(-1, -0.3, (170, 220, 255), 0.30), grad=(1.04, 0.95))


def light_store_b(v, alarm=0.0):
    keys = [(640, 40, 900, (255, 236, 190), 0.30), (260, 420, 560, (150, 210, 255), 0.32)]
    if alarm > 0: keys.append((800, 300, 700, (255, 60, 60), 0.35 * alarm))
    return Light(amb=(1.02, 1.0, 0.98), keys=_keys(v, keys), rim=(-1, -0.3, (170, 220, 255), 0.30), grad=(1.04, 0.95))


def light_airport(v, alarm=0.0):
    keys = [(640, 120, 1000, (255, 228, 180), 0.32), (1050, 300, 500, (190, 230, 255), 0.20)]
    if alarm > 0: keys.append((1050, 300, 700, (255, 60, 60), 0.40 * alarm))
    return Light(amb=(1.0, 1.0, 1.02), keys=_keys(v, keys), rim=(1, -0.3, (255, 220, 170), 0.30), grad=(1.04, 0.96))


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


# ---------------------------------------------------------------- FX
def puff(big, cx, cy, r, a, col=(236, 244, 255), q=9):
    x0, x1, y0, y1 = int(max(0, cx - r)), int(min(OUT_W, cx + r)), int(max(0, cy - r)), int(min(OUT_H, cy + r))
    if x0 >= x1 or y0 >= y1 or a <= 0: return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    m = (((xx // q) * q + q / 2 - cx) ** 2 + ((yy // q) * q + q / 2 - cy) ** 2) <= r * r
    reg = big[y0:y1, x0:x1]
    reg[m] = (reg[m] * (1 - a) + np.array(col) * a).astype(np.uint8)


def cold_vapor(big, x, y, t, k=1.0, scale=1.0, w=120):
    """icy vapour curling off Tom (output px of his top centre)"""
    for i in range(4):
        ph = (t / 1.8 + i / 4) % 1.0
        r = (16 + 46 * ph) * scale
        puff(big, x + (i - 1.5) * w * 0.35 * scale + math.sin(t * 1.3 + i) * 12 * scale, y - 160 * ph * scale, r, 0.42 * k * (1 - ph),
             (226, 242, 255), q=max(6, int(8 * scale)))


def alarm_tint(big, t, k=1.0, period=0.5):
    """red pulsing alarm light over the frame"""
    if k <= 0: return
    a = (0.10 + 0.10 * (int(t / period) % 2)) * k
    big[:] = np.clip(big * (1 - a) + np.array((255, 40, 40)) * a, 0, 255).astype(np.uint8)


def glitch(big, t, k=1.0, seed=0):
    """digital glitch: shifted bands + RGB split (a machine breaking down)"""
    if k <= 0: return
    rng = np.random.default_rng(int(t * 30) + seed)
    for _ in range(int(10 * k)):
        y = int(rng.integers(0, OUT_H - 60)); h = int(rng.integers(12, 70)); dx = int(rng.integers(-90, 90) * k)
        big[y:y + h] = np.roll(big[y:y + h], dx, 1)
    s = int(10 * k)
    if s:
        big[..., 0] = np.roll(big[..., 0], s, 1); big[..., 2] = np.roll(big[..., 2], -s, 1)


# ---------------------------------------------------------------- hook title: «Price-Tag Feast»
def _dil(m, r, step=2):
    d = m.copy()
    for dx in range(-r, r + 1, step):
        for dy in range(-r, r + 1, step):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def hook_title(lines, size=72, width=OUT_W):
    """Press Start 2P, stepped fill orange (top) -> coral -> cranberry-pink (bottom), a thick roast-crust brown outline with a darker
    drop below, an icy frost cap on the tops of the letters (frozen turkey), white glints"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 64) + 60, width, 4), np.uint8)
    y = 24
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 64), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 22 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        dil = _dil(m, 11)
        drop = np.roll(dil, 10, 0) & ~dil
        reg = out[y:y + m.shape[0]]
        reg[drop] = (52, 22, 14, 255)
        reg[dil] = CRUST + (255,)
        rr = np.where(m.any(1))[0]; r0, r1 = rr[0], rr[-1]
        for yy in range(r0, r1 + 1):
            k = (yy - r0) / max(1, r1 - r0)
            c = FILL[0] if k < 0.36 else FILL[1] if k < 0.70 else FILL[2]
            mm = m[yy]; reg[yy][mm, :3] = c; reg[yy][mm, 3] = 255
        cap = m & ~np.roll(m, 9, 0)                                      # frost caps on the tops of the strokes
        cap = _dil(cap, 3, 1) & (dil | m)
        reg[cap & (np.arange(m.shape[0])[:, None] < r0 + (r1 - r0) * 0.45)] = ICE + (255,)
        gl = m & ~np.roll(m, 4, 1) & (np.arange(m.shape[0])[:, None] > r0 + (r1 - r0) * 0.5)   # white glints on left edges
        reg[gl & (np.arange(m.shape[1])[None, :] % 11 < 2)] = (255, 255, 255, 255)
        y += th + 64
    return out


def title_trim(a):
    m = a[..., 3] > 0
    r = np.where(m.any(1))[0]; c = np.where(m.any(0))[0]
    return a[r[0]:r[-1] + 1, c[0]:c[-1] + 1]


# ---------------------------------------------------------------- price-tag plate (series badge / covers / end card)
def price_tag(line1, line2, w=600, h=190, price=None):
    """supermarket shelf price label: white label, a barcode strip, a red SALE corner, the series name + episode"""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], fill=INK + (255,))
    d.rectangle([8, 8, w - 9, h - 9], fill=(252, 250, 242, 255))
    d.polygon([(w - 9, 8), (w - 9, 96), (w - 97, 8)], fill=(214, 36, 46, 255))
    fs = O.pfont(20); d.text((w - 70, 22), 'SALE', font=fs, fill=(255, 255, 255, 255))
    for i, x in enumerate(range(26, 170, 7)):                                         # barcode
        if (i * 7) % 5 != 3: d.rectangle([x, h - 54, x + (3 if i % 3 else 1), h - 22], fill=(30, 30, 36, 255))
    s1 = int(h * 0.27)
    while O.pfont(s1).getlength(line1) > w - 150 and s1 > 10: s1 -= 2
    s2 = int(s1 * 0.56)
    while O.pfont(s2).getlength(line2) > w - 230 and s2 > 8: s2 -= 2
    d.text((30, 30), line1, font=O.pfont(s1), fill=(196, 40, 40, 255))
    d.text((200, h - 52), line2, font=O.pfont(s2), fill=(30, 30, 40, 255))
    return np.array(img)


# ---------------------------------------------------------------- sitcom day card + THAW-O-METER
def day_card(big, t, t0, t1, line1, line2=None, y=300):
    """sitcom time card (white pixel caps on a dark pill) that slides in from the left"""
    if not (t0 <= t < t1): return
    k = min(1.0, (t - t0) / 0.18) * (1 - sm((t - (t1 - 0.2)) / 0.2))
    f1, f2 = O.pfont(40), O.pfont(28)
    w = int(max(f1.getlength(line1), f2.getlength(line2) if line2 else 0)) + 70
    h = 76 + (48 if line2 else 0)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=(20, 14, 24, 220), outline=(255, 186, 60, 255), width=4)
    d.text((34, 18), line1, font=f1, fill=(255, 255, 255))
    if line2: d.text((34, 72), line2, font=f2, fill=(255, 186, 60))
    a = np.array(im)
    x = int(lerp(-w, 40, k))
    O.overlay(big, a, x, y, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(max(0, x), y, x + w, y + h))


def thaw_meter(big, t, t0, t1, state='ROCK', x=870, y=520, level=0.08):
    """THAW-O-METER: a pixel thermometer sticker, the needle stuck at «ROCK»"""
    if not (t0 <= t < t1): return
    u = t - t0
    pop = min(1.0, u / 0.12) * (1 - sm((t - (t1 - 0.15)) / 0.15))
    w, h = 150, 430
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([20, 10, w - 20, h - 10], 30, fill=(252, 250, 244, 255), outline=INK + (255,), width=6)
    d.rounded_rectangle([58, 70, 92, 330], 16, fill=(220, 230, 240, 255), outline=INK + (255,), width=4)
    lv = int(330 - (330 - 80) * level)
    d.rectangle([64, lv, 86, 330], fill=(120, 200, 255, 255))
    d.ellipse([46, 316, 104, 374], fill=(120, 200, 255, 255), outline=INK + (255,), width=4)
    f = O.pfont(16)
    d.text(((w - f.getlength('THAW-O')) / 2, 24), 'THAW-O', font=f, fill=(196, 40, 40))
    d.text(((w - f.getlength('METER')) / 2, 46), 'METER', font=f, fill=(196, 40, 40))
    f2 = O.pfont(20 if len(state) <= 5 else 14)
    d.text(((w - f2.getlength(state)) / 2, 384), state, font=f2, fill=(30, 80, 160))
    for q in range(5): d.line([(96, 100 + q * 48), (108, 100 + q * 48)], fill=INK, width=3)
    a = np.array(im)
    if pop < 1:
        s = 0.4 + 0.6 * pop
        a = np.array(Image.fromarray(a).resize((max(1, int(w * s)), max(1, int(h * s))), Image.NEAREST))
    wob = math.sin(u * 9) * 8 * math.exp(-u * 2)
    O.overlay(big, a, int(x - a.shape[1] / 2 + wob), int(y - a.shape[0] / 2), 1.0)
    if ST.LOG[0] is not None: ST.log('sticker', bbox=(x - w // 2, y - h // 2, x + w // 2, y + h // 2))


# ---------------------------------------------------------------- the big self-checkout screen (insert)
def screen_ui(mode, t, w=900, h=640, total='$89.99', weight=None):
    """Shop'n'Weep self-checkout screen at output resolution (crisp pixel text):
    mode 'price' (turkey line + total), 'alarm' (UNEXPECTED ITEM), 'grandma' (GRANDMA DETECTED, price per pound), 'glitch' (broken total)"""
    im = Image.new('RGB', (w, h), (20, 34, 58)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, 70], fill=(196, 40, 36))
    fh = O.pfont(30)
    d.text((24, 20), "SHOP'N'WEEP  SELF-CHECKOUT", font=fh, fill=(255, 255, 255))
    blink = int(t * 4) % 2 == 0
    f = O.pfont(34); fb = O.pfont(56); fs = O.pfont(26)
    if mode in ('price', 'glitch'):
        d.text((40, 110), 'TURKEY 22 LB', font=f, fill=(255, 255, 255))
        d.text((w - 40 - f.getlength('$89.99'), 110), '$89.99', font=f, fill=(255, 255, 255))
        d.text((40, 170), 'GRAVY JAR', font=fs, fill=(170, 190, 220)); d.text((w - 40 - fs.getlength('$7.49'), 170), '$7.49', font=fs, fill=(170, 190, 220))
        d.line([(40, 236), (w - 40, 236)], fill=(90, 110, 150), width=4)
        d.text((40, 270), 'TOTAL', font=fb, fill=(255, 230, 80))
        tt = total
        if mode == 'glitch':
            rng = np.random.default_rng(int(t * 12))
            tt = ''.join(ch if rng.random() > 0.35 else '$%#@?!9'[int(rng.integers(0, 7))] for ch in total)
        d.text((w - 40 - fb.getlength(tt), 270), tt, font=fb, fill=(255, 230, 80))
        d.rounded_rectangle([40, h - 150, w - 40, h - 40], 20, fill=(40, 160, 90))
        d.text(((w - f.getlength('PAY NOW')) / 2, h - 112), 'PAY NOW', font=f, fill=(255, 255, 255))
    elif mode == 'alarm':
        d.rectangle([0, 70, w, h], fill=(200, 30, 40) if blink else (150, 20, 30))
        for i, ln in enumerate(['UNEXPECTED', 'ITEM IN', 'BAGGING AREA']):
            d.text(((w - fb.getlength(ln)) / 2, 150 + i * 90), ln, font=fb, fill=(255, 255, 255))
        d.text(((w - fs.getlength('PLEASE WAIT FOR ASSISTANCE')) / 2, h - 110), 'PLEASE WAIT FOR ASSISTANCE', font=fs, fill=(255, 220, 220))
    elif mode == 'grandma':
        d.rectangle([0, 70, w, h], fill=(200, 30, 40) if blink else (150, 20, 30))
        for i, ln in enumerate(['GRANDMA', 'DETECTED']):
            d.text(((w - fb.getlength(ln)) / 2, 120 + i * 84), ln, font=fb, fill=(255, 255, 255))
        y0 = 300
        d.rectangle([60, y0, w - 60, h - 40], fill=(252, 250, 242))
        st_ = (h - 40 - y0 - 40) / 3
        d.text((90, y0 + 24), weight or 'NANA 98 LB', font=f, fill=(30, 30, 40))
        d.text((90, y0 + 24 + st_), 'x $4.99/LB', font=f, fill=(30, 30, 40))
        d.text((90, y0 + 14 + 2 * st_), '= $489.02', font=fb, fill=(196, 40, 40))
    a = np.array(im)
    if mode == 'glitch':
        rng = np.random.default_rng(int(t * 20))
        for _ in range(8):
            y = int(rng.integers(70, h - 40)); hh = int(rng.integers(8, 40))
            a[y:y + hh] = np.roll(a[y:y + hh], int(rng.integers(-80, 80)), 1)
    # bezel
    out = np.zeros((h + 60, w + 60, 4), np.uint8)
    out[..., :3] = (44, 48, 58); out[..., 3] = 255
    out[:8] = INK + (255,); out[-8:] = INK + (255,); out[:, :8] = INK + (255,); out[:, -8:] = INK + (255,)
    out[30:30 + h, 30:30 + w, :3] = a
    return out


# ---------------------------------------------------------------- overlays pass
class Show:
    def __init__(s, epi, n, hook, hook_t=(0.10, 2.3), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330, hook_y=330,
                 total=6, hook_size=76, day=None):
        s.epi = epi
        s.badge = O.make_badge(f'SEASON 1 • EP {n}/{total}')
        s.hook = hook_title(hook, hook_size) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default
        s.day = day

    def apply(s, big, t, shot_):
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        O.overlay(big, s.badge, 36, 96, 1.0)
        if s.day: day_card(big, t, *s.day)
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


def st(text, fg=(255, 214, 80), size=60):
    return O.sticker(text, fg=fg, size=size)


# ---------------------------------------------------------------- shot helpers
def shot(world_, light, cx, cy, Z, acts=(), fx_=None, pre=None, sx=180, sy=320, vig=0.24, t=0.0, front=()):
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


def live_frame(big, t, viewers=12, k=1.0):
    """Brayden's phone stream UI: LIVE pill, viewer count, floating hearts"""
    if k <= 0: return
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    f = O.pfont(30)
    d.rounded_rectangle([60, 230, 210, 280], 10, fill=(236, 30, 60))
    d.text((80, 240), 'LIVE', font=f, fill=(255, 255, 255))
    d.rounded_rectangle([222, 230, 400, 280], 10, fill=(0, 0, 0))
    d.ellipse([236, 244, 258, 266], fill=(255, 255, 255))
    d.text((270, 240), f'{viewers}', font=f, fill=(255, 255, 255))
    HEART = ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...']
    for i in range(3):
        ph = (t * 0.7 + i / 3) % 1.0
        x, y = 960 + math.sin(t * 2 + i) * 30, 1500 - ph * 500
        for r, row in enumerate(HEART):
            for c, ch in enumerate(row):
                if ch == 'X': d.rectangle([x + c * 7, y + r * 7, x + c * 7 + 6, y + r * 7 + 6], fill=(255, 70, 110))
    big[:] = np.array(im)


# ---------------------------------------------------------------- covers (profile-grid rule 10.10.2026)
GRID = (240, 1680)
SAFE_BOTTOM = 1520


def cover_make(frame, title, n=1, out='cover.png', title_size=104, plate_y=None, grid_preview=True):
    """price-tag plate «THANKS, RANDY / EPISODE N/6» at the TOP of the 3:4 grid zone (y ~262), the title right under it, a soft dark
    band behind both; faces in the middle, nothing that matters below y 1520. Writes cover.png + cover_grid.png"""
    big = frame.copy()
    p = price_tag('THANKS, RANDY', f'EPISODE {n}/6', w=640, h=190)
    py = GRID[0] + 22 if plate_y is None else plate_y
    t = hook_title(title, title_size)
    ty = py + p.shape[0] - 6
    y1 = ty + t.shape[0]
    shade = np.zeros((big.shape[0], 1, 1), np.float32)
    shade[:y1, 0, 0] = 0.36
    n_ = len(shade[y1:y1 + 140]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.36, 0.0, 140)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t, 0, ty, 1.0)
    Image.fromarray(big).save(out)
    if grid_preview:
        g = big[GRID[0]:GRID[1]].copy()
        g[SAFE_BOTTOM - GRID[0]:] = (g[SAFE_BOTTOM - GRID[0]:] * 0.45).astype(np.uint8)
        Image.fromarray(g).resize((270, 360), Image.LANCZOS).save(str(out).replace('.png', '_grid.png'))
    return big


# ---------------------------------------------------------------- E02: airport X-ray monitor + body scanner screens
def _bezel(a, label=None):
    h, w = a.shape[:2]
    out = np.zeros((h + 60, w + 60, 4), np.uint8)
    out[..., :3] = (44, 48, 58); out[..., 3] = 255
    out[:8] = INK + (255,); out[-8:] = INK + (255,); out[:, :8] = INK + (255,); out[:, -8:] = INK + (255,)
    out[30:30 + h, 30:30 + w, :3] = a
    return out


def xray_ui(fn, t, w=860, h=600, s=13.0, label='SOLID FOOD', sub='UNLIMITED', ok=True, rot=0.0, spr=None, at=None):
    """baggage X-ray monitor: the sprite fn rendered in false colours (organics orange, dense blue-black), grid, a verdict label"""
    from props.dibspix import blit
    a = np.zeros((h, w, 3), np.uint8); a[:] = (230, 236, 240)
    for x in range(0, w, 40): a[:, x] = (210, 218, 226)
    for y in range(0, h, 40): a[y] = (210, 218, 226)
    sp = RX.draw(fn, s, rot=rot, t=t, **(spr or {}))
    lum = sp.col.astype(np.float32).mean(2)
    fc = np.zeros_like(sp.col)
    dense = lum < 120
    fc[...] = (236, 150, 60)
    fc[dense] = (40, 60, 150)
    fc[(lum > 200)] = (250, 200, 120)
    c_ = sp.col.astype(int)
    gr = (c_[..., 0] > 95) & (c_[..., 0] < 160) & (c_[..., 1] > 50) & (c_[..., 1] < 100) & (c_[..., 2] < 55)   # gravy = liquid green
    fc[gr] = (90, 190, 110)
    sp.col = fc
    blit(a, sp, *(at or (w // 2, h - 120)), s, None, False)
    im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w, 56], fill=(30, 40, 60))
    d.text((20, 14), 'X-RAY LANE 2', font=O.pfont(26), fill=(200, 220, 255))
    blink = int(t * 3) % 2 == 0
    col = (40, 160, 90) if ok else ((200, 30, 40) if blink else (150, 20, 30))
    d.rectangle([0, h - 92, w, h], fill=col)
    f = O.pfont(40); f2 = O.pfont(24)
    d.text(((w - f.getlength(label)) / 2, h - 84), label, font=f, fill=(255, 255, 255))
    d.text(((w - f2.getlength(sub)) / 2, h - 36), sub, font=f2, fill=(255, 255, 220))
    return _bezel(np.array(im))


def scanner_ui(t, level=0.7, w=700, h=860, slosh=1.0, label='UNEXPECTED LIQUID', sub='128 OZ'):
    """millimetre-wave body scanner screen: a generic yellow outline of a stocky man (arms up), filled with brown gravy to `level`"""
    im = Image.new('RGB', (w, h), (18, 26, 44)); d = ImageDraw.Draw(im)
    for y in range(0, h, 6): d.line([(0, y), (w, y)], fill=(22, 32, 54))
    m = Image.new('L', (w, h), 0); dm = ImageDraw.Draw(m)
    cx = w // 2
    dm.rectangle([cx - 70, 70, cx + 70, 220], fill=255)                       # brick head
    dm.ellipse([cx - 190, 230, cx + 190, 620], fill=255)                      # pear body
    dm.rectangle([cx - 90, 600, cx - 40, 800], fill=255); dm.rectangle([cx + 40, 600, cx + 90, 800], fill=255)   # legs
    dm.polygon([(cx - 150, 300), (cx - 260, 120), (cx - 220, 100), (cx - 110, 260)], fill=255)                  # arms up
    dm.polygon([(cx + 150, 300), (cx + 260, 120), (cx + 220, 100), (cx + 110, 260)], fill=255)
    M = np.array(m) > 127
    a = np.array(im)
    yy, xx = np.mgrid[0:h, 0:w]
    surf = h - level * (h - 120) + np.sin(xx / 40.0 + t * 7.0) * 14 * slosh
    a[M & (yy > surf)] = (150, 90, 40)
    a[M & (yy > surf) & ((xx + yy + int(t * 30)) % 23 < 2)] = (190, 120, 60)
    edge = M & ~(np.roll(M, 4, 0) & np.roll(M, -4, 0) & np.roll(M, 4, 1) & np.roll(M, -4, 1))
    a[edge] = (255, 220, 60)
    im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = '1'
    blink = int(t * 4) % 2 == 0
    d.rectangle([0, 0, w, 64], fill=(200, 30, 40) if blink else (150, 20, 30))
    f = O.pfont(30)
    d.text(((w - f.getlength(label)) / 2, 18), label, font=f, fill=(255, 255, 255))
    f2 = O.pfont(44)
    bw = int(f2.getlength(sub)) + 40
    d.rectangle([w - bw - 20, h - 90, w - 20, h - 20], fill=(252, 246, 226))
    d.text((w - bw, h - 76), sub, font=f2, fill=(160, 40, 30))
    return _bezel(np.array(im))


# ---------------------------------------------------------------- E03: phone call screen + split screen
def phone_ui(t, name='BUTTERBUTT', sub='TURKEY TALK-LINE', number='1-800-GOBBLE', status='ON HOLD', timer=None, w=520, h=900):
    """a big smartphone in-call screen (output res): caller name, number, a hold timer, call buttons"""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, w - 1, h - 1], 60, fill=INK + (255,))
    d.rounded_rectangle([18, 18, w - 19, h - 19], 46, fill=(24, 34, 60, 255))
    d.ellipse([w // 2 - 70, 110, w // 2 + 70, 250], fill=(236, 120, 40, 255))
    for i, c in enumerate(FEATH := ((226, 96, 40), (246, 176, 48), (176, 70, 36), (236, 200, 90))):     # turkey icon
        d.ellipse([w // 2 - 50 + i * 22, 132, w // 2 - 30 + i * 22, 186], fill=c)
    d.ellipse([w // 2 - 30, 160, w // 2 + 30, 220], fill=(150, 92, 46))
    f1, f2, f3 = O.pfont(40), O.pfont(24), O.pfont(30)
    for txt, f, y, c in ((name, f1, 290, (255, 255, 255)), (sub, f2, 350, (200, 220, 255)), (number, f3, 410, (255, 214, 80))):
        d.text(((w - f.getlength(txt)) / 2, y), txt, font=f, fill=c)
    blink = int(t * 2) % 2 == 0
    d.text(((w - f3.getlength(status)) / 2, 500), status, font=f3, fill=(255, 120, 120) if blink else (255, 200, 200))
    if timer:
        d.text(((w - O.pfont(56).getlength(timer)) / 2, 560), timer, font=O.pfont(56), fill=(255, 255, 255))
    for i, (x, c) in enumerate(((w // 2 - 140, (80, 90, 110)), (w // 2, (80, 90, 110)), (w // 2 + 140, (230, 50, 50)))):
        d.ellipse([x - 50, h - 190, x + 50, h - 90], fill=c)
    return np.array(im)


def split(left, right, gap=10, col=(255, 186, 60)):
    """vertical split screen of two full frames (each squeezed to half width by cropping its centre)"""
    W2 = (OUT_W - gap) // 2
    out = np.zeros_like(left); out[:] = col
    lx = (OUT_W - W2) // 2
    out[:, :W2] = left[:, lx:lx + W2]
    out[:, W2 + gap:W2 + gap + W2] = right[:, lx:lx + W2]
    return out


# ---------------------------------------------------------------- E05: the StreamFlix TV screen (paywall recursion)
def tv_ui(mode, t, w=980, h=560, step=0):
    """StreamFlix Ultra+ Max on the big TV: 'paywall' (SUBSCRIBE TO WATCH $29.99/MO + fine print), 'windows' (step 1..4 stacked popups:
    QR / APP / EMAIL / PASSWORD), 'question' (SECURITY QUESTION), 'locked' (WRONG · LOCKED → SUPPORT+ $29.99), 'final' (the game is over)"""
    im = Image.new('RGB', (w, h), (14, 10, 30)); d = ImageDraw.Draw(im); d.fontmode = '1'
    for y in range(0, h, 8): d.line([(0, y), (w, y)], fill=(20, 14, 40))
    d.rectangle([0, 0, w, 64], fill=(120, 20, 200))
    d.text((24, 18), 'STREAMFLIX ULTRA+ MAX', font=O.pfont(30), fill=(255, 255, 255))
    d.text((w - 360, 22), 'MAPLE FALLS vs EVERYBODY', font=O.pfont(18), fill=(230, 210, 255))
    fb, f, fs = O.pfont(52), O.pfont(34), O.pfont(18)
    if mode == 'paywall':
        for i, ln in enumerate(['SUBSCRIBE', 'TO WATCH']):
            d.text(((w - fb.getlength(ln)) / 2, 110 + i * 70), ln, font=fb, fill=(255, 255, 255))
        d.text(((w - O.pfont(64).getlength('$29.99/MO')) / 2, 270), '$29.99/MO', font=O.pfont(64), fill=(255, 214, 60))
        d.text(((w - fs.getlength('*requires app, account, email & patience')) / 2, h - 50), '*requires app, account, email & patience',
               font=fs, fill=(170, 160, 200))
    elif mode == 'windows':
        items = [('SCAN THE QR CODE', (60, 160, 255)), ('DOWNLOAD THE APP', (60, 200, 120)), ('VERIFY YOUR EMAIL', (255, 160, 40)),
                 ('RESET YOUR PASSWORD', (230, 60, 60))]
        for i, (txt, c) in enumerate(items[:max(1, step)]):
            x0, y0 = 60 + i * 60, 100 + i * 80
            d.rectangle([x0, y0, x0 + 620, y0 + 230], fill=(250, 250, 252), outline=c, width=8)
            d.rectangle([x0, y0, x0 + 620, y0 + 44], fill=c)
            d.text((x0 + 16, y0 + 10), 'STEP %d OF 47' % (i + 1), font=O.pfont(20), fill=(255, 255, 255))
            d.text((x0 + 30, y0 + 90), txt, font=O.pfont(30), fill=(30, 30, 40))
            if i == 0:
                for q in range(6):
                    for r_ in range(6):
                        if (q * 7 + r_ * 3) % 5 < 2: d.rectangle([x0 + 470 + q * 18, y0 + 70 + r_ * 18, x0 + 486 + q * 18, y0 + 86 + r_ * 18], fill=(0, 0, 0))
    elif mode == 'question':
        d.rectangle([60, 110, w - 60, h - 60], fill=(250, 250, 252), outline=(230, 60, 60), width=8)
        d.text((100, 140), 'SECURITY QUESTION', font=f, fill=(230, 60, 60))
        d.text((100, 220), 'NAME OF YOUR', font=f, fill=(30, 30, 40))
        d.text((100, 270), 'FIRST PET?', font=f, fill=(30, 30, 40))
        d.rectangle([100, 350, w - 100, 420], outline=(30, 30, 40), width=4)
        if int(t * 3) % 2: d.rectangle([116, 362, 128, 408], fill=(30, 30, 40))
    elif mode == 'locked':
        blink = int(t * 4) % 2 == 0
        d.rectangle([0, 64, w, h], fill=(200, 30, 40) if blink else (150, 20, 30))
        d.text(((w - f.getlength('WRONG. ACCOUNT LOCKED.')) / 2, 100), 'WRONG. ACCOUNT LOCKED.', font=f, fill=(255, 255, 255))
        d.rectangle([80, 170, w - 80, h - 50], fill=(250, 250, 252))
        d.text((110, 196), 'TO SPEAK TO AN AGENT', font=O.pfont(28), fill=(30, 30, 40))
        d.text((110, 246), 'SUBSCRIBE TO', font=O.pfont(28), fill=(30, 30, 40))
        d.text((110, 300), 'SUPPORT+', font=O.pfont(72), fill=(120, 20, 200))
        d.text((110, 400), '$29.99/MO', font=O.pfont(48), fill=(200, 30, 40))
    elif mode == 'final':
        d.text(((w - fb.getlength('FINAL')) / 2, 200), 'FINAL', font=fb, fill=(255, 255, 255))
        d.text(((w - f.getlength('THANKS FOR WATCHING')) / 2, 300), 'THANKS FOR WATCHING', font=f, fill=(255, 214, 60))
    return np.array(im)


def paste_world(big, v, img, rect, log=False):
    """paste an RGB image into a world-space rectangle (x0, y0, x1, y1) of the current view (a TV screen, a phone, a poster)"""
    ox0, oy0 = v.opt(rect[0], rect[1]); ox1, oy1 = v.opt(rect[2], rect[3])
    X0, X1, Y0, Y1 = int(round(ox0)), int(round(ox1)), int(round(oy0)), int(round(oy1))
    if X1 <= X0 or Y1 <= Y0: return
    sub = np.array(Image.fromarray(img[..., :3] if img.shape[2] > 3 else img).resize((X1 - X0, Y1 - Y0), Image.NEAREST))
    cx0, cy0 = max(0, X0), max(0, Y0); cx1, cy1 = min(OUT_W, X1), min(OUT_H, Y1)
    if cx0 >= cx1 or cy0 >= cy1: return
    big[cy0:cy1, cx0:cx1] = sub[cy0 - Y0:cy1 - Y0, cx0 - X0:cx1 - X0]
    if log and ST.LOG[0] is not None: ST.log('card', bbox=(cx0, cy0, cx1, cy1))
