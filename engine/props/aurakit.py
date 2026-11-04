"""Episode kit for «Aura Dad» (US): worlds from the xAI backgrounds with local Arizona signs (decals), hero light per location, the
holographic title style (lilac -> aqua -> mint stepped letters, dark violet outline, white sparkle), the AURA SCAN PRO phone screen,
the AR jaw-scan box, MIRRA's glass panels (bathroom mirror / smart-fridge screen), the app-badge cover plate and the overlay pass."""
import math, os
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import Chars, Light
from scene import Layer, sm, lerp
import overlays as O
import paths as PATHS
from props import decals as D
from props import auracast as A

SLUG = 'aura-dad'
BG = PATHS.series(SLUG) / 'bg'
COL = dict(doug=(255, 226, 70), kayden=(170, 255, 90), tammy=(255, 150, 200), mirra=(90, 240, 230), lily=(220, 170, 255),
           skylar=(255, 190, 120), brett=(255, 140, 60), kid=(200, 230, 255), jaxon=(120, 200, 255))
INK, VIOLET, LILAC, AQUA, MINT = (30, 22, 40), (44, 18, 70), (214, 186, 255), (110, 230, 240), (150, 250, 190)
RED, GREEN, CREAM, WOOD = (226, 46, 70), (60, 200, 110), (252, 246, 232), (120, 76, 44)

# ---------------------------------------------------------------- kitchen (native px of bg/kitchen.png 1280x720)
K_FLOOR = 650.0
K_LAMPS = [(420.0, 135.0), (925.0, 135.0)]
K_WINDOW = (470, 92, 840, 360)
K_FRIDGE_SCREEN = (48, 196, 112, 262)        # MIRRA hub screen on the fridge's left door (world px box)
K_MUG = (1062.0, 448.0)
# ---------------------------------------------------------------- bathroom
B_MIRROR = (633.0, 200.0, 128.0, 148.0)       # centre + radii of the oval glass
B_SCONCES = [(352.0, 160.0), (896.0, 160.0)]
B_FLOOR = 640.0


def q(im, colors=110):
    return np.array(im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))


NAMES = ['kitchen', 'bathroom']


def build(force=False, names=None):
    global NAMES
    if names: NAMES = list(names)
    cache = PATHS.build('props', 'auradad_' + '_'.join(NAMES) + '.npz')
    if os.path.exists(cache) and not force:
        d = np.load(cache); return {k: d[k] for k in d.files}
    out = {n: q(Image.open(BG / f'{n}.png').convert('RGB')) for n in NAMES}
    np.savez_compressed(cache, **out)
    return out


def decorate(W):
    """local Arizona signs and labels (rule 10.10.2026: 5–10 per location, every inscription fitted inside its plate)"""
    D.attach(W['kitchen'], [
        (D.plate(132, 96, ['LIVE', 'LAUGH', 'LATTE'], bg=CREAM, colors=[VIOLET, (200, 90, 150), VIOLET], border=None, pad=2.5), 999, 184),
        (D.plate(54, 22, ["WORLD'S", 'OKAYEST DAD'], bg=(255, 220, 90), colors=[INK, RED], border=INK, pad=1.0, tilt=-4), 136, 300),
        (D.plate(48, 30, ['BOAT DAY!', 'LAKE', 'PLEASANT'], bg=(250, 250, 240), colors=[(40, 110, 200), INK, INK], border=(150, 150, 160),
                 weights=[1, 0.7, 0.7], pad=1.2, tilt=3), 150, 214),
        (D.plate(52, 14, ['COST-GO MEMBER 2004'], bg=(214, 40, 50), colors=[(255, 255, 255)], border=(120, 20, 30), pad=0.8), 140, 352),
        (D.plate(34, 34, ['112', 'F'], bg=(255, 250, 240), colors=[RED, INK], border=(90, 90, 100), weights=[1, 0.6], pad=1.5, round_=6),
         772, 128),
        (D.plate(56, 18, ['SCORPION', 'SEASON!'], bg=(255, 196, 60), colors=[INK, RED], border=INK, pad=1.0, tilt=-3), 604, 290),
        (D.plate(70, 14, ['HOME IS WHERE THE WIFI IS'], bg=(214, 186, 255), colors=[VIOLET], border=VIOLET, pad=0.8), 280, 250),
        (D.plate(40, 16, ['DECAF =', 'BETRAYAL'], bg=(250, 240, 220), colors=[WOOD, RED], border=WOOD, pad=1.0, tilt=5), 334, 300),
        (D.plate(66, 66, [' '], bg=(18, 24, 38), border=(70, 74, 90), bw=1.5, round_=5), K_FRIDGE_SCREEN[0], K_FRIDGE_SCREEN[1]),
    ])
    D.attach(W['kitchen'], [                                                       # more set dressing (owner 04.11: denser antourage)
        (D.plate(40, 30, ['MY DAD', '(BALD)', 'BY LILY 3RD'], bg=(255, 255, 250), colors=[(60, 120, 220), RED, INK], border=(200, 200, 210),
                 weights=[1, 1, 0.55], pad=1.2, tilt=-5), 64, 300),
        (D.plate(42, 26, ['CHORES:', 'KAYDEN: TRASH', 'DOUG: VIBES'], bg=(250, 250, 240), colors=[INK, (60, 140, 90), RED],
                 border=(160, 160, 170), weights=[1, 0.7, 0.7], pad=1.0, tilt=2), 160, 262),
        (D.plate(30, 10, ['NO SUGAR'], bg=(255, 255, 255), colors=[RED], border=RED, pad=0.6), 333, 336),
        (D.plate(26, 12, ['HOT AF'], bg=(230, 60, 50), colors=[(255, 240, 200)], border=None, pad=0.8, tilt=-8), 780, 300),
        (D.plate(36, 18, ['MONSOON', 'SALE!'], bg=(120, 200, 230), colors=[INK, RED], border=INK, pad=1.0, tilt=4), 870, 232),
    ])
    D.attach(W['bathroom'], [
        (D.plate(40, 22, ['SCALE', 'LIES'], bg=(255, 255, 255), colors=[INK, RED], border=INK, pad=1.2, tilt=-3), 1010, 560),
        (D.plate(46, 14, ['MEWMASTER 3000'], bg=(170, 255, 90), colors=[INK], border=INK, pad=0.8), 450, 386),
        (D.plate(58, 30, ['DOUG:', 'ONE PUMP OF', 'COLOGNE. ONE.'], bg=(255, 240, 130), colors=[RED, INK, INK], border=None,
                 weights=[1, 0.7, 0.7], pad=1.5, tilt=6), 714, 240),
        (D.plate(50, 12, ['MIRRA SMART MIRROR'], bg=(60, 64, 80), colors=[AQUA], border=(30, 32, 40), pad=0.8), 608, 356),
        (D.plate(36, 14, ['HERS'], bg=(255, 255, 255), colors=[(60, 160, 170)], border=None, pad=1.5), 1128, 400),
        (D.plate(26, 12, ['HIS'], bg=(250, 250, 250), colors=[(40, 110, 200)], border=None, pad=1.2), 372, 360),
        (D.plate(50, 22, ['SPF 100', 'ARIZONA', 'STRENGTH'], bg=(255, 160, 60), colors=[INK, INK, RED], border=INK,
                 weights=[1, 0.6, 0.6], pad=1.0), 840, 360),
        (D.plate(44, 20, ['TIPSY RHINO', '$84'], bg=(255, 200, 220), colors=[VIOLET, RED], border=VIOLET, pad=1.0), 250, 396),
    ])


# ---------------------------------------------------------------- lights
def light_kitchen(v, k_sun=1.0):
    keys = [(*v.opt(x, y), 900, (255, 214, 150), 0.35) for x, y in K_LAMPS]
    keys.append((*v.opt(650.0, 230.0), 1300, (255, 236, 200), 0.25 * k_sun))
    return Light(amb=(0.98, 0.95, 0.93), keys=keys, rim=(-1, -0.3, (255, 240, 210), 0.35), grad=(1.04, 0.92))


def light_bath(v):
    keys = [(*v.opt(x, y), 800, (255, 214, 160), 0.45) for x, y in B_SCONCES]
    keys.append((*v.opt(*B_MIRROR[:2]), 700, (150, 240, 240), 0.25))
    return Light(amb=(1.02, 1.0, 1.04), keys=keys, rim=(1, -0.3, (200, 250, 255), 0.4), grad=(1.03, 0.92))


def begin():
    """heroes always at PX=1: one hero pixel = 3 output px (rule: <= 3.75 px), background zoom <= 1.45"""
    ST.set_px(1)
    return Chars(), Chars()


def logface(v, cam, head, r_units):
    x, y = cam.p(*head)
    ST.log('sprite', face=(x * ST.UP * ST.PX[0], y * ST.UP * ST.PX[0], r_units * cam.sc * ST.UP * ST.PX[0]))


# ---------------------------------------------------------------- holographic title
def hook_title(lines, size=72, width=O.OUT_W):
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 52) + 46, width, 4), np.uint8)
    y = 26
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 46), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 20 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        dil = O._dilate(m, 10)
        shd = np.roll(np.roll(dil, 12, 0), 8, 1)
        reg = out[y:y + m.shape[0]]
        reg[shd] = (22, 8, 38, 255); reg[dil] = VIOLET + (255,)
        rows = np.where(m.any(1))[0]; r0, r1 = rows[0], rows[-1]
        cols = np.where(m.any(0))[0]; c0, c1 = cols[0], cols[-1]
        xx = np.arange(m.shape[1])
        for yy in range(m.shape[0]):
            k = (yy - r0) / max(1, r1 - r0)
            dk = (xx - c0) / max(1, c1 - c0) * 0.25                       # holographic diagonal shift
            kk = k + dk
            col = np.where(kk[:, None] < 0.38, np.array(LILAC), np.where(kk[:, None] < 0.75, np.array(AQUA), np.array(MINT)))
            rm = m[yy]
            reg[yy, rm, :3] = col[rm]; reg[yy, rm, 3] = 255
        top = m & ~np.roll(m, 7, 0)
        reg[top] = (255, 255, 255, 255)
        y += th + 52
    return out


def title_trim(a):
    ys, xs = np.nonzero(a[..., 3])
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1] if len(ys) else a


def _fit(a, maxw):
    if a.shape[1] <= maxw: return a
    f = maxw / a.shape[1]
    return np.array(Image.fromarray(a).resize((int(a.shape[1] * f), int(a.shape[0] * f)), Image.NEAREST))


# ---------------------------------------------------------------- AURA SCAN PRO phone screen (output px, RGBA)
_UI = {}


def _txt(d, xy, s, size, col, anchor='mm'):
    d.text(xy, s, font=O.pfont(size), fill=col, anchor=anchor)


def phone_ui(value, t=0.0, mode='score', w=520, h=920, label=None):
    """the son's app: mode 'score' (big AURA number, red if negative, green if positive), 'scan' (scan line over a face outline),
    'jaw' (JAWLINE: NOT FOUND + spinner). value: int. Returns RGBA."""
    key = (value, mode, w, h, label, int(t * 8) if mode in ('scan', 'jaw') else 0)
    if key in _UI: return _UI[key]
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 54, fill=(22, 20, 30, 255))
    d.rounded_rectangle([14, 14, w - 15, h - 15], 44, fill=(36, 26, 60, 255))
    for i in range(h - 60):                                                       # lilac -> aqua screen gradient
        k = i / (h - 60)
        c = tuple(int(a + (b - a) * k) for a, b in zip((70, 40, 120), (30, 110, 130)))
        d.line([(24, 30 + i), (w - 25, 30 + i)], fill=c + (255,))
    d.rounded_rectangle([w // 2 - 70, 34, w // 2 + 70, 62], 14, fill=(14, 12, 20, 255))  # notch
    _txt(d, (w // 2, 112), 'AURA SCAN', 36, (255, 255, 255, 255))
    _txt(d, (w // 2, 156), 'PRO  $9.99/WK', 18, LILAC + (255,))
    cy = 380
    d.ellipse([w // 2 - 150, cy - 170, w // 2 + 150, cy + 170], outline=(255, 255, 255, 120), width=6)   # face outline
    if mode == 'score':
        neg = value < 0
        col = (255, 80, 100, 255) if neg else (90, 255, 150, 255)
        s = f'{value:+d}'.replace('+', '+') if value else '0'
        _txt(d, (w // 2, cy - 10), s, 92 if len(s) <= 4 else 74, col)
        _txt(d, (w // 2, cy + 90), 'AURA', 40, (255, 255, 255, 255))
        bars = [('JAWLINE', 0.05 if neg else 0.2), ('RIZZ', 0.1 if neg else 0.9), ('SILENCE', 0.15 if neg else 1.0)]
    elif mode == 'video':                                                          # viral clip: big view counter
        d.rectangle([40, cy - 170, w - 40, cy + 110], fill=(14, 12, 20, 255))
        d.polygon([(w // 2 - 40, cy - 90), (w // 2 - 40, cy + 10), (w // 2 + 50, cy - 40)], fill=(255, 255, 255, 230))
        _txt(d, (w // 2, cy + 150), label or 'GRILL DAD', 30, (255, 255, 255, 255))
        _txt(d, (w // 2, cy + 200), 'FALLS IN', 30, (255, 255, 255, 255))
        s_ = f'{value / 1e6:.1f}M VIEWS'
        _txt(d, (w // 2, cy + 270), s_, 40, (255, 90, 110, 255))
        bars = []
        label = None
    elif mode == 'jaw':
        a = t * 6.0
        for i in range(8):                                                        # loading spinner
            ang = a + i * math.pi / 4
            r = 46
            x, y = w // 2 + r * math.cos(ang), cy - 20 + r * math.sin(ang)
            al = int(60 + 195 * (i / 7))
            d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(255, 255, 255, al))
        _txt(d, (w // 2, cy + 90), 'SEARCHING', 32, (255, 255, 255, 255))
        bars = [('JAWLINE', 0.0), ('CHIN', 0.0), ('NECK', 1.0)]
    else:
        yy = cy - 170 + int((math.sin(t * 5) * 0.5 + 0.5) * 340)
        d.line([(w // 2 - 160, yy), (w // 2 + 160, yy)], fill=(120, 255, 220, 255), width=6)
        _txt(d, (w // 2, cy), 'SCANNING', 34, (255, 255, 255, 255))
        bars = [('JAWLINE', 0.3), ('RIZZ', 0.3), ('SILENCE', 0.3)]
    y = 610
    for name, k in bars:
        _txt(d, (54, y), name, 22, (255, 255, 255, 255), 'lm')
        d.rounded_rectangle([54, y + 22, w - 54, y + 44], 10, fill=(20, 16, 34, 255))
        if k > 0: d.rounded_rectangle([54, y + 22, 54 + int((w - 108) * k), y + 44], 10, fill=(MINT if k > 0.5 else (255, 90, 110)) + (255,))
        y += 82
    if label:
        _txt(d, (w // 2, h - 70), label, 24, (255, 230, 120, 255))
    a = np.array(im)
    _UI[key] = a
    return a


def ar_scan(big, cx, cy, r, t, label='JAWLINE: NOT FOUND'):
    """AR scan brackets over a body part (output px) with a spinner and a red label underneath"""
    im = Image.new('RGBA', (int(r * 2 + 40), int(r * 2 + 150)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 20, 20, 20 + 2 * r, 20 + 2 * r
    L_ = r * 0.4
    for (ax, ay, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(ax, ay), (ax + sx * L_, ay)], fill=(90, 255, 220, 255), width=8)
        d.line([(ax, ay), (ax, ay + sy * L_)], fill=(90, 255, 220, 255), width=8)
    a = t * 7.0
    for i in range(8):
        ang = a + i * math.pi / 4
        x, y = 20 + r + 26 * math.cos(ang), 20 + r + 26 * math.sin(ang)
        al = int(60 + 195 * (i / 7))
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(255, 255, 255, al))
    lab = O.sticker(label, fg=(255, 90, 110), size=40)
    arr = np.array(im)
    O.overlay(big, arr, int(cx - r - 20), int(cy - r - 20), 1.0)
    lx = int(min(max(cx - lab.shape[1] / 2, 10), big.shape[1] - 10 - lab.shape[1]))
    O.overlay(big, lab, lx, int(cy + r + 16), 1.0)
    ST.log('sticker', bbox=(lx, int(cy + r + 16), lx + lab.shape[1], int(cy + r + 16 + lab.shape[0])))


def mirra_panel(L, box, t, talk, expr='calm', score=None):
    """MIRRA on a dark screen in world px box = (x0, y0, x1, y1): face + optional score line drawn by the caller as a decal"""
    x0, y0, x1, y1 = box
    s = (x1 - x0) / 11.0
    A.mirra(L, (x0 + x1) / 2, (y0 + y1) / 2 + 0.2 * s, s, t, talk, expr)


def mirra_glass(L, t, talk, expr='calm', scale=1.0):
    cx, cy, rx, ry = B_MIRROR
    A.mirra(L, cx, cy + 6, rx / 6.2 * scale, t, talk, expr)


def glass_glow(big, v, t, k=1.0):
    import fx
    fx.glow(big, *v.opt(*B_MIRROR[:2]), B_MIRROR[2] * v.Z * 3 * 1.1, (120, 250, 240), 0.10 * k * (0.85 + 0.15 * math.sin(t * 3)))


_SC = {}


def score_plate(value, w=60, h=16):
    key = (value, w, h)
    if key not in _SC:
        neg = value < 0
        _SC[key] = D.plate(w, h, [f'AURA {value:+d}'], bg=(18, 24, 38), colors=[(255, 90, 110) if neg else MINT], border=AQUA, pad=1.0)
    return _SC[key]


# ---------------------------------------------------------------- cover plate: app badge «AURA DAD / EPISODE N/6»
def app_badge(n, w=760, h=200):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 14, w - 1, h - 1], 48, fill=(22, 8, 38, 255))                   # shadow
    d.rounded_rectangle([0, 0, w - 9, h - 15], 48, fill=VIOLET + (255,))
    d.rounded_rectangle([10, 10, w - 19, h - 25], 40, fill=(70, 40, 120, 255))
    for i in range(h - 45):
        k = i / (h - 45)
        c = tuple(int(a + (b - a) * k) for a, b in zip((120, 80, 200), (40, 150, 170)))
        d.line([(30, 18 + i), (w - 40, 18 + i)], fill=c + (255,))
    cx = 104
    d.ellipse([cx - 66, 22, cx + 66, h - 37], fill=(18, 12, 30, 255), outline=MINT + (255,), width=6)
    _txt(d, (cx, (h - 15) // 2), '-400', 30, (255, 90, 110, 255))
    _txt(d, (cx + 70 + (w - cx - 110) // 2, 70), 'AURA DAD', 50, (255, 255, 255, 255))
    _txt(d, (cx + 70 + (w - cx - 110) // 2, 132), f'EPISODE {n}/6', 28, MINT + (255,))
    return np.array(im)


GRID = (240, 1680)
SAFE_BOTTOM = 1520


def cover_make(frame, title, n=1, out='cover.png', title_size=96, grid_preview=True):
    big = frame.copy()
    p = app_badge(n)
    py = GRID[0] + 22
    t_ = _fit(title_trim(hook_title(title, title_size, width=1500)), 1040)
    ty = py + p.shape[0] + 12
    y1 = ty + t_.shape[0]
    shade = np.zeros((big.shape[0], 1, 1), np.float32)
    shade[:y1, 0, 0] = 0.34
    n_ = len(shade[y1:y1 + 140]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.34, 0.0, 140)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t_, (big.shape[1] - t_.shape[1]) // 2, ty, 1.0)
    Image.fromarray(big).save(out)
    if grid_preview:
        g = big[GRID[0]:GRID[1]].copy()
        g[SAFE_BOTTOM - GRID[0]:] = (g[SAFE_BOTTOM - GRID[0]:] * 0.45).astype(np.uint8)
        Image.fromarray(g).resize((270, 360), Image.LANCZOS).save(str(out).replace('.png', '_grid.png'))
    return big


# ---------------------------------------------------------------- overlay pass
class Show:
    def __init__(s, epi, season, n, hook, hook_t=(0.06, 2.4), stickers=(), flashes=(), mosaics=(), inserts=(), cap_y=None,
                 cap_default=1330, hook_y=300):
        s.epi = epi
        s.badge = O.make_badge(f'SEASON {season} • EP {n}/6')
        s.hook = _fit(title_trim(hook_title(hook, 84, width=1400)), 1020) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics); s.inserts = list(inserts)
        s.cap_y = cap_y or {}; s.cap_default = cap_default

    def apply(s, big, t, shot):
        for fn, t0, t1 in s.inserts:
            if t0 <= t < t1: fn(big, t, t - t0)
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        O.overlay(big, s.badge, 36, 96, 1.0)
        if s.hook is not None and s.hook_t[0] <= t < s.hook_t[1]:
            k = min(1.0, (t - s.hook_t[0]) / 0.1) * (1 - sm((t - (s.hook_t[1] - 0.2)) / 0.2))
            O.overlay(big, s.hook, (big.shape[1] - s.hook.shape[1]) // 2, s.hook_y, k)
        s.epi.captions.draw(big, t, s.cap_y.get(shot, s.cap_default))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


# ---------------------------------------------------------------- SEPHORIA store (bg/sephoria.png 1280x720)
S_FLOOR = 640.0
S_COUNTER = [(866, 414), (1135, 414), (1280, 436), (1280, 720), (1104, 720), (1098, 640), (896, 560), (874, 560)]   # front occluder
S_RINGS = [(515.0, 45.0), (992.0, 40.0)]


def decorate_store(Wd):
    D.attach(Wd, [
        (D.plate(150, 30, ['SEPHORIA'], bg=(20, 20, 24), colors=[(255, 255, 255)], border=(255, 150, 200), bw=1.5, pad=2.0), 590, 96),
        (D.plate(70, 24, ['GLOW UP', 'OR GO HOME'], bg=(255, 182, 214), colors=[VIOLET, VIOLET], border=VIOLET, pad=1.2), 1170, 186),
        (D.plate(46, 20, ['AGES 8+', 'ANTI-AGING'], bg=(255, 255, 255), colors=[INK, RED], border=INK, pad=1.0, tilt=-3), 470, 410),
        (D.plate(44, 16, ['TIPSY RHINO', '$84'], bg=(255, 220, 230), colors=[VIOLET, RED], border=VIOLET, pad=0.8), 236, 152),
        (D.plate(40, 16, ['GLOWY', 'RECIPE $68'], bg=(200, 255, 220), colors=[(30, 120, 80), RED], border=(30, 120, 80), pad=0.8), 236, 266),
        (D.plate(46, 18, ['RETINOL', 'FOR KIDS?'], bg=(255, 250, 200), colors=[INK, RED], border=INK, pad=0.8, tilt=2), 380, 230),
        (D.plate(52, 18, ['LIMIT 40', 'PER CHILD'], bg=(255, 255, 255), colors=[RED, INK], border=RED, pad=1.0), 60, 380),
        (D.plate(50, 14, ['NO STANLEES', 'ON TESTERS'], bg=(40, 40, 46), colors=[(255, 220, 120), (255, 255, 255)], border=None, pad=0.8),
         900, 470),
        (D.plate(44, 16, ['PAY HERE', ':('], bg=(255, 150, 200), colors=[INK, INK], border=INK, pad=0.8), 1170, 300),
        (D.plate(36, 14, ['REWARDS: 0'], bg=(20, 20, 24), colors=[(150, 250, 190)], border=None, pad=0.8), 960, 386),
    ])


def light_store(v):
    keys = [(*v.opt(x, y), 1000, (255, 170, 220), 0.35) for x, y in S_RINGS]
    keys.append((*v.opt(700.0, 300.0), 1400, (255, 250, 240), 0.3))
    return Light(amb=(1.0, 0.98, 1.02), keys=keys, rim=(1, -0.3, (255, 200, 236), 0.4), grad=(1.03, 0.94))


# ---------------------------------------------------------------- layers: occluders from the background + parallax foreground
_OCC = {}


def occluder(world, poly, key):
    """RGBA sprite (world px) cut from the background inside poly: drawn AFTER the heroes so a counter / table / doorframe stands
    in front of them (a second layer of the same painting)"""
    if key in _OCC: return _OCC[key]
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    x0, y0 = int(min(xs)), int(min(ys)); x1, y1 = int(max(xs)), int(max(ys))
    x1 = min(x1, world.shape[1]); y1 = min(y1, world.shape[0])
    m = Image.new('L', (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(m).polygon([(x - x0, y - y0) for x, y in poly], fill=255)
    spr = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    spr[..., :3] = world[y0:y1, x0:x1]
    spr[..., 3] = np.array(m)
    _OCC[key] = (spr, x0, y0)
    return _OCC[key]


def draw_occluder(big, v, occ):
    spr, x0, y0 = occ
    ST.blit_world(big, v, spr, x0, y0)


def fgcam(v, par=0.35, xref=640.0):
    """camera for a foreground layer (closer than the heroes): it slides faster than the background when the camera pans"""
    from stage import ACam
    k = ST.PX[0]
    X0 = v.X0 + (v.X0 - (xref - 180 / v.Z)) * par
    return ACam(0.0, 0.0, -X0 * v.Z / k, (-v.Y0 * v.Z + v.oy) / k, v.Z / k)


def fg_plant(L, x, y, s=1.0, pot=(214, 110, 70)):
    """potted desert plant (agave) in the foreground, world px"""
    from props.folk import cap as fcap, ell as fell, poly as fpoly
    for i, a in enumerate((-1.1, -0.6, -0.15, 0.3, 0.75, 1.2)):
        ln = (70 + 25 * ((i + 1) % 3)) * s
        tip = (x + math.sin(a) * ln, y - 40 * s - math.cos(a) * ln)
        fcap(L, (x, y - 36 * s), tip, 9 * s, 2 * s, (90, 160, 110), (140, 210, 150), (60, 120, 80))
    fpoly(L, [(x - 34 * s, y - 40 * s), (x + 34 * s, y - 40 * s), (x + 26 * s, y + 20 * s), (x - 26 * s, y + 20 * s)], pot)
    fcap(L, (x - 36 * s, y - 40 * s), (x + 36 * s, y - 40 * s), 6 * s, 6 * s, (236, 140, 96))


def fg_bags(L, x, y, s=1.0):
    """a pile of SEPHORIA shopping bags (foreground)"""
    from props.folk import cap as fcap, poly as fpoly
    for i, col in enumerate([(255, 182, 214), (214, 186, 255), (150, 250, 190)]):
        bx = x + i * 46 * s; by = y + (i % 2) * 10 * s
        fpoly(L, [(bx - 26 * s, by - 70 * s), (bx + 26 * s, by - 70 * s), (bx + 30 * s, by), (bx - 30 * s, by)], col)
        fcap(L, (bx - 12 * s, by - 70 * s), (bx - 4 * s, by - 92 * s), 2.5 * s, 2.5 * s, (40, 30, 40))
        fcap(L, (bx - 4 * s, by - 92 * s), (bx + 12 * s, by - 70 * s), 2.5 * s, 2.5 * s, (40, 30, 40))


# ---------------------------------------------------------------- backyard (bg/backyard.png 1280x720)
Y_CAM = (1095.0, 182.0)                         # the neighbour's security camera (clue of E03)
Y_GRILL = (110.0, 330.0)
Y_SPEAKER = (250.0, 398.0)                      # MIRRA's patio speaker on the cooler


def decorate_yard(Wd):
    D.attach(Wd, [
        (D.plate(66, 36, ['POOL RULES', 'NO RUNNING', 'NO DAD DIVES'], bg=(255, 255, 255), colors=[(40, 110, 200), INK, RED],
                 border=(40, 110, 200), weights=[1, 0.7, 0.7], pad=1.2), 592, 290),
        (D.plate(54, 22, ['SMILE!', "YOU'RE ON CAMERA"], bg=(255, 220, 60), colors=[INK, INK], border=INK, weights=[1, 0.6], pad=1.0),
         1062, 224),
        (D.plate(54, 22, ['BEWARE OF DOG', "(HE'S LAZY)"], bg=(250, 250, 240), colors=[RED, INK], border=INK, weights=[1, 0.7], pad=1.0,
                 tilt=-3), 455, 296),
        (D.plate(40, 14, ['GRILL SARGE'], bg=(30, 30, 36), colors=[(255, 200, 80)], border=(120, 120, 130), pad=0.8), 92, 350),
        (D.plate(56, 16, ['NO LIFEGUARD. EVER.'], bg=(214, 40, 50), colors=[(255, 255, 255)], border=None, pad=0.8), 1110, 434),
        (D.plate(26, 12, ['93 F'], bg=(255, 255, 255), colors=[(40, 110, 200)], border=(40, 110, 200), pad=0.8, round_=3), 470, 452),
        (D.plate(44, 16, ['SCORPION', 'XING'], bg=(255, 214, 60), colors=[INK, INK], border=INK, pad=0.8, tilt=6), 1180, 300),
        (D.plate(40, 14, ['KEEP OFF', 'CACTUS'], bg=(250, 250, 240), colors=[(60, 140, 90), INK], border=(60, 140, 90), pad=0.8), 770, 330),
    ])


def light_yard(v, k=1.0):
    keys = [(*v.opt(900.0, 60.0), 1600, (255, 200, 130), 0.4 * k), (*v.opt(150.0, 100.0), 800, (255, 220, 150), 0.2)]
    return Light(amb=(1.04, 0.98, 0.9), keys=keys, rim=(1, -0.5, (255, 210, 140), 0.45), grad=(1.04, 0.94))


def cam_blink(big, v, t, k=1.0):
    import fx
    if (t * 2.2) % 1.0 < 0.55:
        fx.glow(big, *v.opt(Y_CAM[0] - 6, Y_CAM[1] + 2), 18 * v.Z * 3, (255, 40, 40), 0.9 * k)


# ---------------------------------------------------------------- cul-de-sac (bg/culdesac.png 1280x720)
C_MAIL = [(605.0, 565.0), (678.0, 565.0)]
C_DOOR_P = (180.0, 360.0)                        # Pruitt front door (left house)
C_BELL = (206.0, 286.0, 244.0, 332.0)            # smart doorbell screen box
C_BOX = (812.0, 372.0)                           # empty «+6 IN» box on Brett's porch (clue)


def decorate_cul(Wd):
    D.attach(Wd, [
        (D.plate(40, 12, ['THE PRUITTS'], bg=(250, 250, 240), colors=[INK], border=None, pad=0.8), 584, 430),
        (D.plate(40, 12, ['KOWALSKI'], bg=(255, 140, 60), colors=[INK], border=None, pad=0.8), 658, 430),
        (D.plate(56, 30, ['SLOW', 'DADS AT', 'PLAY'], bg=(255, 220, 60), colors=[INK, INK, INK], border=INK, pad=1.2), 30, 470),
        (D.plate(60, 24, ['WE BELIEVE', 'IN GAINS'], bg=(255, 255, 255), colors=[(220, 80, 50), INK], border=(220, 80, 50), pad=1.2,
                 tilt=-3), 1100, 452),
        (D.plate(62, 14, ["BRETT'S GYM"], bg=(30, 30, 36), colors=[(255, 140, 60)], border=None, pad=0.8), 1012, 266),
        (D.plate(44, 18, ['HOA: GRAVEL', 'ONLY'], bg=(255, 255, 255), colors=[RED, INK], border=RED, pad=1.0), 410, 470),
        (D.plate(40, 14, ['NO SOLICITING'], bg=(250, 250, 240), colors=[RED], border=INK, pad=0.8), 140, 300),
        (D.plate(30, 18, ['+6 IN', 'LIFTS'], bg=(200, 160, 110), colors=[INK, RED], border=(120, 90, 60), pad=1.0), C_BOX[0], C_BOX[1]),
        (D.plate(42, 50, [' '], bg=(18, 24, 38), border=(90, 90, 100), round_=4), C_BELL[0] - 2, C_BELL[1] - 2),
    ])


def light_cul(v):
    keys = [(*v.opt(1000.0, 40.0), 1800, (255, 236, 200), 0.35)]
    return Light(amb=(1.03, 1.0, 0.95), keys=keys, rim=(1, -0.5, (255, 236, 200), 0.4), grad=(1.04, 0.94))
