"""S01E06 «Naperville» (v2 cast, season finale) — Brad cuts the ribbon on HIS heated parking spot; Dibs slaps the call sheet on the screen:
every villain of the season was the Cul-de-Sac Players, hired by Brad ($400/wk + snacks). Brad flees, but the block is all chairs; Dibs
helpfully points at an «open» spot. Brad moves Mrs. Wozniak's chair — every curtain, every door, every lady with a kitchen weapon.
Brad leaves rolled in a snow burrito. The Chief makes Dibs permanent. A New York cabbie asks if the spot is open.
  python3 ep06.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import view_at, OUT_W, OUT_H, Light
from scene import sm, lerp
import overlays as O
import fx
from episode import Episode
from props import dibspix as DX
from props import dibscast as DC
from props import dibskit as DK
from props import chi_props as PR
from props import chikit as K
from props import bytfx as B
from timeline import DUR, FPS, VOICE, SLUG, TURN_T

HERE = pathlib.Path(__file__).resolve().parent
EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
WORLD = K.world('dibs_row')
GY = 652.0                                   # street line (feet)
SPOT = (640.0, 654.0)                        # the heated spot (steam from the manhole)
SIGN = (790.0, 652.0)                        # RESERVED sign pole
MW = (330.0, 640.0)                          # Mrs. Wozniak's chair
DIBS_CURB = (190.0, 646.0)                   # Dibs on his own chair on the left curb (laps)
CHU = 0.62                                   # chair size relative to a person
L_HIP = (-17.0, 34.0)                        # ladies: free fist on the hip
WEAPON = {'mrs_w': ('rolling_pin', (16.0, 72.0)), 'rose': ('casserole', (16.0, 68.0)), 'dot': ('pan', (16.0, 72.0)), 'bev': ('mop', (14.0, 64.0))}
MW_SIGN = [('MRS. W', 1.7), ('SINCE', 0.8), ('1974', 1.3)]


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def A(fn, wx, wy, un=None, s=None, flip=False, pin=None, **P):
    return DX.Act(fn, wx, wy, s_=s, un=un, flip=flip, pin=pin, **P)


def snow_fx(t, n=70):
    return lambda big, v: K.snow(big, v, t, n)


def street(cx, cy, Z, acts=(), front=(), pre=None, emit=None, fx_=None, sx=180, sy=330, t=0.0, snow=60):
    def fx2(big, v):
        K.snow(big, v, t, snow)
        if fx_: fx_(big, v)
    return K.shot(WORLD, K.light_street, cx, cy, Z, acts=list(acts), front=list(front), pre=pre, emit=emit, fx_=fx2, sx=sx, sy=sy)


CU_BG = 1.45                                 # background zoom behind close-ups (rule 05.10.2026); extreme close-ups capped at 1.7


def cu_bg(Z):
    """background zoom for a close-up framed as if at zoom Z (the hero keeps his own scale)"""
    return min(1.7, CU_BG * Z / 2.3)


def cu(fn, spk, t, u, hx, hy, Z=2.1, s=12.5, zoom=0.06, sx=180, sy=300, flip=False, k=1.8, extra=(), front=(), pre=None, emit=None,
       fx_=None, cdx=0.0, cdy=0.0, near_pre=None, near=None, near_acts=(), **P):
    """close-up: the hero's head pinned at world (hx, hy); camera on the head (slow push); sprite scale follows the zoom.
    The hero is drawn at 2x (3x for extreme close-ups) and the street behind is zoomed less (cu_bg); camera offsets scale with it, so the
    hero sits where he did. near_pre / near(big, v) draw things right next to the hero (ribbon, sign) with the hero-depth view instead,
    near_acts = Chars props f(CH, v) right behind the hero (his chair), also with the hero-depth view"""
    Zt = Z + zoom * u
    zb = cu_bg(Zt); f = Zt / zb
    vh = view_at(WORLD, hx + cdx, hy + 30.0 + cdy, Zt, sx, sy)
    P.setdefault('mouth_', mouth(spk, t, k))
    a = A(fn, hx, hy, s=s * Zt / Z, flip=flip, pin='head', t=t, hires=True, **P)
    def pre2(big, v):
        if pre: pre(big, v)
        if near_pre: near_pre(big, vh)
    def emit2(big, v):
        if emit: emit(big, v)
        if near: near(big, vh)
    class Near:                                                                         # a Chars prop painted with the hero-depth view
        direct = True
        def __init__(s_, f_): s_.f = f_
        def __call__(s_, big, v, lt):
            CH = ST.Chars(); s_.f(CH, vh); CH.comp(big, lt)
    acts = list(extra) + [Near(f_) for f_ in near_acts] + [a]
    return street(hx + cdx * f, hy + (30.0 + cdy) * f, zb, acts=acts, front=front, pre=pre2, emit=emit2, fx_=fx_, sx=sx, sy=sy, t=t, snow=40)


# ================================================================== world-space drawing (signs, ribbon)
def world_text(big, v, text, cx, cy, h, col, outline_=None, glow=0.0):
    """pixel-font text at world coordinates (cx, cy centre, h = text height in world px)"""
    s_ = v.Z * 3.0
    size = max(8, int(h * s_))
    ox, oy = v.opt(cx, cy)
    x0 = max(0, int(ox - len(text) * size * 0.62)); x1 = min(OUT_W, int(ox + len(text) * size * 0.62))
    y0 = max(0, int(oy) - size); y1 = min(OUT_H, int(oy) + size)
    if x1 - x0 < 4 or y1 - y0 < 4: return
    img = Image.fromarray(big[y0:y1, x0:x1])
    d = ImageDraw.Draw(img); d.fontmode = '1'
    f = O.pfont(size)
    xy = (ox - x0, oy - y0)
    if glow > 0:
        for dx in (-3, 0, 3):
            for dy in (-3, 0, 3):
                d.text((xy[0] + dx, xy[1] + dy), text, font=f, fill=tuple(int(c * glow) for c in col), anchor='mm')
    if outline_:
        for dx in (-2, 0, 2):
            for dy in (-2, 0, 2): d.text((xy[0] + dx, xy[1] + dy), text, font=f, fill=outline_, anchor='mm')
    d.text(xy, text, font=f, fill=col, anchor='mm')
    big[y0:y1, x0:x1] = np.array(img)


def wbox(big, v, x0, y0, x1, y1, col):
    a, b = v.opt(x0, y0); c, d = v.opt(x1, y1)
    a, b, c, d = int(a), int(b), int(c), int(d)
    big[max(0, b):max(0, min(OUT_H, d)), max(0, a):max(0, min(OUT_W, c))] = col


def reserved_sign(big, v, x=SIGN[0], y=SIGN[1], steam_t=None):
    """steel pole + blue plate: RESERVED / AGENT OF THE YEAR / (HEATED)"""
    wbox(big, v, x - 2.2, y - 118, x + 2.2, y, (24, 18, 40)); wbox(big, v, x - 1.2, y - 118, x + 1.2, y, (150, 156, 172))
    wbox(big, v, x - 38, y - 160, x + 38, y - 112, (24, 18, 40))
    wbox(big, v, x - 36, y - 158, x + 36, y - 114, (30, 80, 170))
    wbox(big, v, x - 33, y - 155, x + 33, y - 117, (240, 244, 252)); wbox(big, v, x - 31, y - 153, x + 31, y - 119, (30, 80, 170))
    world_text(big, v, 'RESERVED', x, y - 146, 9.5, (255, 255, 255))
    world_text(big, v, 'AGENT OF THE YEAR', x, y - 135, 5.0, (255, 236, 120))
    world_text(big, v, '(HEATED)', x, y - 125, 6.5, (255, 150, 70))


def ribbon(big, v, t, cut=0.0):
    """two gold stanchions and a red ribbon with a bow across the spot; cut = 0..1 the halves drop"""
    xa, xb, h = 548.0, 732.0, 34.0
    for x in (xa, xb):
        wbox(big, v, x - 3, GY - h - 6, x + 3, GY, (24, 18, 40)); wbox(big, v, x - 2, GY - h - 5, x + 2, GY, (226, 180, 60))
        wbox(big, v, x - 5, GY - h - 9, x + 5, GY - h - 4, (250, 214, 90))
    mid = (xa + xb) / 2
    def seg(p0, p1, col, th):
        n = 40
        for k in range(n + 1):
            q = k / n
            wx, wy = p0[0] + (p1[0] - p0[0]) * q, p0[1] + (p1[1] - p0[1]) * q
            ox, oy = v.opt(wx, wy)
            r = int(th * v.Z * 3 / 2)
            big[max(0, int(oy) - r):max(0, int(oy) + r), max(0, int(ox) - r):max(0, int(ox) + r)] = col
    top = GY - h
    if cut <= 0:
        seg((xa, top), (xb, top), (200, 30, 44), 3.2)
        bx, by = v.opt(mid, top)
        r = int(9 * v.Z)
        for dx in (-1, 1):
            big[max(0, int(by) - r):int(by) + r, max(0, int(bx) + (0 if dx > 0 else -2 * r)):max(0, int(bx) + (2 * r if dx > 0 else 0))] = (226, 40, 56)
    else:
        drop = 26.0 * sm(cut)
        seg((xa, top), (mid - 4, top + drop * 0.6 + 14 * cut), (200, 30, 44), 3.2)
        seg((xb, top), (mid + 4, top + drop * 0.6 + 14 * cut), (200, 30, 44), 3.2)


def mrsw_chair(t, un, x=MW[0], y=MW[1], lift=0.0, dx=0.0, rot=0.0):
    def f(CH, v):
        PR.dibs_chair(CH, v.cam(x + dx, y - lift, un * CHU), t=t, sign=MW_SIGN)
        if rot:
            px, py = v.pt(x + dx, y - lift)
            K.rot_chars(CH, rot, px, py)
    return f


def own_chair(t, un, x, y):
    return lambda CH, v: PR.dibs_chair(CH, v.cam(x, y, un * CHU), t=t)


def curb_chairs(t, un=6.6, xs=(470.0, 905.0, 1060.0)):
    """every spot on the block is taken: chairs along the curb"""
    return [own_chair(t + i, un, x, 628.0 + 8 * (i % 2)) for i, x in enumerate(xs)]


def sit_anchor(x, y, un):
    return x + 1.5 * un, y + 0.2 * un


def dibs_sitting(t, x, y, un, expr='smug', mth=0.0, pose='sit', props=None, hands=None, **kw):
    """Dibs sitting on his chair at (x, y); any arm pose (wave / point / hold) keeps the sitting legs"""
    ax, ay = sit_anchor(x, y, un)
    if pose == 'sit' and hands is None: hands = {'R': (17.0, 44.0)}
    props = props if props is not None else {'R': 'thermos'}
    return A(DC.dibs, ax, ay, un=un, pose=DC.P_(pose, sit=True), t=t, mouth_=mth, expr=expr, shades=False, hands=hands, props=props, **kw)


def van_with_brad(t, x, y, un=4.6, pose='wheel', expr='grin', mth=0.0, flip=False, blinker=True, look=-0.6):
    return [lambda CH, v: PR.minivan(CH, v.cam(x, y, un, flip), t, rot=-x * 0.3, driver=False, blinker=blinker),
            A(DC.brad, x + (-5.0 if flip else 5.0) * un, y - 9.6 * un, un=un * 0.62, pin='head', flip=flip, pose=pose, t=t, mouth_=mth, expr=expr,
              legs=False, clip_h=58.0, look=look)]


def lady_act(who, x, y, un, t, expr='glare', flip=True, armed=True, pose='hold', step=0.0, mth=0.0, look=0.0, hands=None):
    w, hand = WEAPON[who]
    hd = hands or ({'L': L_HIP, 'R': hand} if armed else None)
    return A(DC.lady, x, y, un=un, flip=flip, who=who, pose=pose, t=t, expr=expr, legs=True, clip_h=None, hands=hd,
             props={'R': w} if armed else None, step=step, mouth_=mth, look=look, shadow=0.3)


# ================================================================== the call sheet (hook) and the cork board (recap)
_CACHE = {}


def head_shot(fn, w, h, **P):
    sp = DX.Spr(); fn(sp, t=0.4, **P)
    hx, hy = sp.anchors['head']
    img = np.zeros((h, w, 3), np.uint8); img[:] = (196, 206, 222)
    DX.blit(img, sp, w / 2 - hx * 5.0, h * 0.62 + hy * 5.0, 5.0, None, False)
    return img


def callsheet():
    """CUL-DE-SAC PLAYERS call sheet, 760 x 1000 px (drawn at output resolution)"""
    if 'cs' in _CACHE: return _CACHE['cs']
    W_, H_ = 760, 1000
    img = Image.new('RGB', (W_, H_), (248, 242, 224))
    d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([0, 0, W_ - 1, H_ - 1], outline=(70, 56, 44), width=8)
    d.rectangle([8, 8, W_ - 9, 150], fill=(196, 36, 50))
    d.text((W_ // 2, 60), 'CUL-DE-SAC', font=O.pfont(52), fill=(255, 250, 240), anchor='mm')
    d.text((W_ // 2, 118), 'PLAYERS', font=O.pfont(46), fill=(255, 224, 120), anchor='mm')
    for cx in (52, W_ - 52):                                                  # comedy masks
        d.ellipse([cx - 26, 50, cx + 26, 110], fill=(250, 250, 246), outline=(30, 30, 40), width=4)
        d.rectangle([cx - 14, 68, cx - 5, 76], fill=(30, 30, 40)); d.rectangle([cx + 5, 68, cx + 14, 76], fill=(30, 30, 40))
        d.arc([cx - 14, 78, cx + 14, 100], 10, 170, fill=(30, 30, 40), width=4)
    d.text((W_ // 2, 210), 'CALL SHEET', font=O.pfont(58), fill=(30, 34, 70), anchor='mm')
    d.rectangle([90, 252, W_ - 90, 258], fill=(30, 34, 70))
    d.text((W_ // 2, 312), 'ROLE: "THE VILLAIN"', font=O.pfont(36), fill=(30, 34, 70), anchor='mm')
    a = np.array(img)
    for i, (fn, lab, P) in enumerate(((DC.terry, 'T.', dict(expr='nervous')), (DC.gary, 'G.', dict(expr='normal')))):
        x0 = 150 + i * 260
        a[352:352 + 220, x0 - 6:x0 + 206] = (70, 56, 44)
        a[358:358 + 208, x0:x0 + 200] = head_shot(fn, 200, 208, **P)
    img = Image.fromarray(a); d = ImageDraw.Draw(img); d.fontmode = '1'
    for i, lab in enumerate(('T.', 'G.')):
        d.text((250 + i * 260, 610), lab, font=O.pfont(48), fill=(30, 34, 70), anchor='mm')
    d.text((W_ // 2, 702), 'PAY: $400/WK', font=O.pfont(50), fill=(196, 36, 50), anchor='mm')
    d.text((W_ // 2, 778), '+ SNACKS', font=O.pfont(50), fill=(196, 36, 50), anchor='mm')
    d.rectangle([90, 826, W_ - 90, 830], fill=(150, 140, 130))
    d.text((W_ // 2, 880), 'PRODUCER: BRAD', font=O.pfont(46), fill=(30, 34, 70), anchor='mm')
    d.text((W_ // 2, 940), '(NAPERVILLE)  :)', font=O.pfont(34), fill=(90, 96, 120), anchor='mm')
    _CACHE['cs'] = np.array(img)
    return _CACHE['cs']


def paste_rot(big, img, cx, cy, ang=0.0, scale=1.0, alpha=1.0, shadow=True):
    """paste an RGB image centred at (cx, cy), rotated (degrees), scaled (nearest), with a drop shadow"""
    im = Image.fromarray(img).convert('RGBA')
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.NEAREST)
    if ang: im = im.rotate(ang, resample=Image.NEAREST, expand=True)
    a = np.array(im)
    h, w = a.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    for (ox, oy, k, use) in (((18, 22, 0.45, True) if shadow else (0, 0, 0, False)), (0, 0, alpha, True)):
        if not use or k <= 0: continue
        X0, Y0 = max(0, x0 + ox), max(0, y0 + oy); X1, Y1 = min(OUT_W, x0 + ox + w), min(OUT_H, y0 + oy + h)
        if X0 >= X1 or Y0 >= Y1: continue
        sub = a[Y0 - y0 - oy:Y1 - y0 - oy, X0 - x0 - ox:X1 - x0 - ox]
        m = (sub[..., 3:4] > 127).astype(np.float32) * k
        reg = big[Y0:Y1, X0:X1].astype(np.float32)
        src = np.zeros_like(reg) if (ox or oy) else sub[..., :3].astype(np.float32)
        big[Y0:Y1, X0:X1] = (reg * (1 - m) + src * m).astype(np.uint8)


def mitten(big, x, y, s=1.0):
    """Dibs's black mitten pinching the poster edge"""
    r = int(46 * s)
    yy, xx = np.ogrid[max(0, y - r):min(OUT_H, y + r), max(0, x - r):min(OUT_W, x + r)]
    m = ((xx - x) / (r * 0.85)) ** 2 + ((yy - y) / r) ** 2 <= 1.0
    reg = big[max(0, y - r):min(OUT_H, y + r), max(0, x - r):min(OUT_W, x + r)]
    reg[m] = (22, 22, 28)
    m2 = ((xx - x + r * 0.25) / (r * 0.5)) ** 2 + ((yy - y + r * 0.35) / (r * 0.35)) ** 2 <= 1.0
    reg[m2] = (54, 54, 66)
    big[max(0, y - int(0.8 * r)):min(OUT_H, y + int(0.8 * r)), 0:max(0, x - int(0.6 * r))] = (28, 36, 70)          # sleeve from off-screen
    big[max(0, y - int(0.8 * r)):min(OUT_H, y + int(0.8 * r)), max(0, x - int(0.75 * r)):max(0, x - int(0.55 * r))] = (14, 16, 30)


def polaroid(e, label):
    key = 'pol_' + e
    if key in _CACHE: return _CACHE[key]
    ph = np.array(Image.open(HERE / 'recap' / f'{e}.png').convert('RGB'))
    h, w = ph.shape[:2]
    img = Image.new('RGB', (w + 40, h + 110), (250, 250, 244))
    a = np.array(img); a[20:20 + h, 20:20 + w] = ph
    img = Image.fromarray(a); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([0, 0, w + 39, h + 109], outline=(200, 200, 190), width=3)
    d.text(((w + 40) // 2, h + 62), label, font=O.pfont(46), fill=(30, 40, 110), anchor='mm')
    _CACHE[key] = np.array(img)
    return _CACHE[key]


def stamp_img(text='ACTOR', size=96, col=(214, 30, 40)):
    key = 'stamp_' + text
    if key in _CACHE: return _CACHE[key]
    f = O.pfont(size)
    w = int(len(text) * size * 1.02) + 70; h = size + 60
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([4, 4, w - 5, h - 5], outline=col + (255,), width=10)
    d.text((w // 2, h // 2), text, font=f, fill=col + (255,), anchor='mm')
    a = np.array(img)
    rng = np.random.default_rng(4)                                          # worn ink
    holes = rng.random(a.shape[:2]) < 0.12
    a[holes, 3] = 0
    _CACHE[key] = a
    return a


def paste_rgba(big, a, cx, cy, ang=0.0, scale=1.0):
    im = Image.fromarray(a)
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.NEAREST)
    if ang: im = im.rotate(ang, resample=Image.NEAREST, expand=True)
    b = np.array(im); h, w = b.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    X0, Y0 = max(0, x0), max(0, y0); X1, Y1 = min(big.shape[1], x0 + w), min(big.shape[0], y0 + h)
    if X0 >= X1 or Y0 >= Y1: return
    sub = b[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    m = sub[..., 3:4] > 127
    big[Y0:Y1, X0:X1] = np.where(m, sub[..., :3], big[Y0:Y1, X0:X1])


def cork():
    if 'cork' in _CACHE: return _CACHE['cork']
    rng = np.random.default_rng(11)
    b = np.zeros((OUT_H, OUT_W, 3), np.float32); b[:] = (150, 108, 66)
    n = rng.random((OUT_H // 6 + 1, OUT_W // 6 + 1))
    n = np.kron(n, np.ones((6, 6)))[:OUT_H, :OUT_W]
    b += ((n > 0.82) * 26 - (n < 0.18) * 30)[..., None]
    b[:46], b[-46:], b[:, :46], b[:, -46:] = (92, 60, 34), (92, 60, 34), (92, 60, 34), (92, 60, 34)
    _CACHE['cork'] = np.clip(b, 0, 255).astype(np.uint8)
    return _CACHE['cork']


BOARD = [('ep01', 'EP 1', 300.0, 420.0, -6.0, 4.55), ('ep02', 'EP 2', 760.0, 760.0, 5.0, 5.20), ('ep04', 'EP 4', 300.0, 1110.0, 4.0, 5.85)]
POSTER_AT = (770.0, 1330.0, -3.0, 6.50)


def board_canvas(t):
    big = cork().copy()
    pins = []
    for e, lab, x, y, ang, t0 in BOARD:
        if t < t0: continue
        k = sm((t - t0) / 0.12)
        paste_rot(big, polaroid(e, lab), x, y - 60 * (1 - k), ang, 1.0)
        pins.append((int(x), int(y - 200)))
        if t > t0 + 0.2:                                                  # ACTOR stamp slams on
            q = min(1.0, (t - t0 - 0.2) / 0.08)
            paste_rgba(big, stamp_img(), x + 10, y + 80, ang - 14, 0.85 + 0.5 * (1 - q))
    px, py, pang, pt0 = POSTER_AT
    if t >= pt0:
        k = sm((t - pt0) / 0.12)
        paste_rot(big, callsheet(), px, py - 80 * (1 - k), pang, 0.52)
        if t > pt0 + 0.1:
            q = min(1.0, (t - pt0 - 0.1) / 0.3)
            img = Image.fromarray(big); d = ImageDraw.Draw(img)
            for (x, y) in pins:                                           # red strings from each villain to the call sheet
                ex, ey = x + (px - x) * q, (y) + (py - 230 - y) * q
                d.line([(x, y), (ex, ey)], fill=(210, 30, 40), width=7)
            big = np.array(img)
        pins.append((int(px), int(py - 240)))
    for (x, y) in pins:
        big[y - 14:y + 14, x - 14:x + 14] = (24, 18, 30); big[y - 11:y + 11, x - 11:x + 11] = (220, 40, 50); big[y - 9:y - 3, x - 7:x - 1] = (255, 170, 170)
    return big


def r_board(t, u):
    big = board_canvas(t)
    keys = [(0.00, 300.0, 400.0, 1.55), (0.55, 300.0, 400.0, 1.6), (0.65, 760.0, 740.0, 1.55), (1.20, 760.0, 740.0, 1.6),
            (1.30, 300.0, 1090.0, 1.55), (1.85, 300.0, 1090.0, 1.6), (2.05, 540.0, 960.0, 1.0), (3.3, 560.0, 980.0, 1.07)]
    for (a0, x0, y0, z0), (a1, x1, y1, z1) in zip(keys, keys[1:]):
        if a0 <= u <= a1:
            q = sm((u - a0) / (a1 - a0)); cx, cy, z = lerp(x0, x1, q), lerp(y0, y1, q), lerp(z0, z1, q); break
    else:
        cx, cy, z = keys[-1][1:]
    w, h = OUT_W / z, OUT_H / z
    x0 = int(min(max(0, cx - w / 2), OUT_W - w)); y0 = int(min(max(0, cy - h / 2), OUT_H - h))
    crop = big[y0:y0 + int(h), x0:x0 + int(w)]
    out = np.array(Image.fromarray(crop).resize((OUT_W, OUT_H), Image.NEAREST))
    for e, lab, x, y, ang, t0 in BOARD:
        if t0 <= t < t0 + 0.08: O.flash(out, 0.6 * (1 - (t - t0) / 0.08))
        if t0 + 0.2 <= t < t0 + 0.32: B.shake(out, t, 10, 40)
    fx.vignette(out, 0.3)
    return out


# ================================================================== shots
def r_hook(t, u):
    cut = sm((u - 0.05) / 0.2)
    open_ = 0.5 * (1 - cut)
    def front(big, v):
        ribbon(big, v, t, cut)
    big = cu(DC.brad, 'brad', t, u, 640.0, 440.0, Z=2.1, s=12.5, zoom=0.05, pose='hold', hands={'R': (24.0, 60.0)},
             props={'R': lambda sp, h, a, tt: DC.p_scissors(sp, h, a, tt, open_=open_)}, expr='grin', ting=max(0.0, 1 - abs(u - 0.15) / 0.15),
             mouth_=0.0, near_pre=lambda big, v: reserved_sign(big, v, 760.0, 600.0), near=front, cdy=0.0, sy=260)
    if u > 0.30:                                                                         # SLAP: the call sheet
        k = min(1.0, (u - 0.30) / 0.07)
        paste_rot(big, callsheet(), 560, 1420 + 400 * (1 - k), -3.0, 1.0 + 0.25 * (1 - k))
        mitten(big, 168, int(1080 + 400 * (1 - k)), 1.7)
        if u < 0.5: B.shake(big, t, 22 * (1 - (u - 0.30) / 0.2), 40)
        if u < 0.36: O.flash(big, 0.35)
    return big


def r_ope(t, u):
    ex = 'ope' if talk('brad', t) > 0.05 else 'grin'
    return cu(DC.brad, 'brad', t, u, 640.0, 440.0, Z=2.7, s=16.0, zoom=0.08, pose='hold', hands={'R': (20.0, 40.0)},
              props={'R': lambda sp, h, a, tt: DC.p_scissors(sp, h, a, tt, open_=0.1, a=-0.3)}, expr=ex, sweat=1.0, mouth_=mouth('brad', t, 1.2),
              near_pre=lambda big, v: reserved_sign(big, v, 760.0, 600.0), cdy=0.0)


def r_marty(t, u, zoom=0.05, Z=2.0, s=18.0):
    Zt = Z + zoom * u
    zb = cu_bg(Zt); f = Zt / zb
    vh = view_at(WORLD, 812.0, 510.0, Zt, 180, 330)                                     # hero-depth view (his steam)
    def pre(big, v):
        B.steam(big, vh, t, 790.0, 586.0, n=7, rise=170, size=60, a=0.55)
    a = A(DC.marty, 800.0, 598.0, s=s * Zt / Z, t=t, mouth_=mouth('marty', t, 1.7), expr='deadpan', look=0.6, hires=True)
    return street(800.0 + 12.0 * f, 598.0 - 88.0 * f, zb, acts=[a], pre=pre, t=t, snow=40)


def r_d2(t, u):
    big = cu(DC.dibs, 'dibs', t, u, 520.0, 420.0, Z=2.2, s=12.5, zoom=0.1, pose='point', hands={'R': (34.0, 70.0 + 4 * math.sin(t * 30))},
             props={'R': 'paper'}, expr='shout', mouth_=mouth('dibs', t, 1.9), sy=310)
    B.shake(big, t, 9, 38)
    return big


def r_snacks1(t, u):
    return cu(DC.brad, 'brad', t, u, 640.0, 440.0, Z=2.4, s=13.5, zoom=0.06, pose='stand', expr='nervous', sweat=1.0, mouth_=mouth('brad', t, 1.6),
              cdy=30.0)


def r_snacks2(t, u):
    """Terry and Gary behind the CRAFT SERVICES table, munching, waving"""
    def emit(big, v):
        top = GY - 74.0
        wbox(big, v, 556, top, 764, top + 7, (24, 18, 40)); wbox(big, v, 558, top + 1, 762, top + 6, (236, 236, 228))   # folding table top
        wbox(big, v, 558, top + 6, 762, top + 40, (196, 36, 50)); wbox(big, v, 558, top + 6, 762, top + 8, (150, 20, 30))  # red skirt
        for x in (566, 754): wbox(big, v, x - 2, top + 40, x + 2, GY, (60, 60, 70))
        world_text(big, v, 'CRAFT SERVICES', 660, top + 24, 9.0, (255, 244, 220))
        for i, (x, c) in enumerate(((585, (240, 190, 60)), (618, (210, 120, 60)), (700, (250, 220, 120)), (735, (190, 90, 150)))):
            ox, oy = v.opt(x, top); r = int(8 * v.Z * 1.5)
            big[int(oy) - r // 2:int(oy), int(ox) - r:int(ox) + r] = c                                         # chip bowls, donuts
            big[int(oy) - r // 2:int(oy) - r // 2 + 4, int(ox) - r:int(ox) + r] = tuple(min(255, cc + 40) for cc in c)
    chew = 0.5 + 0.5 * math.sin(t * 18)
    acts = [A(DC.terry, 612.0, GY - 6, un=7.6, pose='hold', t=t, expr='smile', mouth_=chew * 0.6, props={'R': 'popcorn'}, hands={'R': (16.0, 62.0)}),
            A(DC.gary, 712.0, GY - 4, un=7.4, flip=True, pose='wave', t=t, expr='grin', mouth_=chew * 0.5, props={'L': 'sandwich'})]
    return street(662.0, 520.0, 1.38 + 0.05 * u, acts=acts, emit=emit, t=t, sy=330)


def r_thing(t, u):
    """Brad backs away to his minivan; the Chief reads the call sheet; Deb shakes her head on the video call"""
    k = sm(u / 2.4)
    bx = lerp(560.0, 470.0, k)
    acts = [lambda CH, v: PR.minivan(CH, v.cam(395.0, 700.0, 5.2), t, driver=False, door=0.6),
            A(DC.brad, bx, GY + 6, un=8.0, flip=True, pose=DC.walk('wave', t, 9.0, 0.35, 0.4), t=t, expr='grin', mouth_=mouth('brad', t, 1.7),
              look=0.7, shadow=0.3),
            A(DC.chief, 650.0, GY, un=7.8, flip=True, pose='hold', hands={'R': (22.0, 76.0)}, props={'R': 'paper'}, t=t,
              expr='shock' if u > 0.9 else 'deadpan', shadow=0.3)]
    big = street(560.0, 520.0, 1.3, acts=acts, pre=lambda big, v: reserved_sign(big, v, 720.0, 640.0), t=t, sy=330)
    DK.deb_window(big, t, 'deadpan', 0.0, box=(650, 200, 1010, 560), look=0.7 * math.sin(t * 9))
    return big


def r_chase(t, u):
    """crossing: Brad's minivan crawls along at 25 mph, Dibs jogs right beside it, sipping coffee"""
    x = 300.0 + 230.0 * u
    acts = van_with_brad(t, x + 60.0, 708.0, 6.6, 'wheel', 'panic', 0.0)
    acts.append(A(DC.dibs, x - 64.0, GY + 30, un=7.0, pose=DC.walk('sip', t, 13.0, 0.6, 0.8), props={'R': 'coffee'}, t=t, expr='smug',
                  shades=True, shadow=0.3))
    big = street(x + 10.0, 520.0, 1.3, acts=acts, t=t, sy=330, fx_=lambda big, v: fx.speed_lines(big, t, 0.25))
    return big


def lap_shot(t, u, state):
    """static wide: Dibs on his chair on the curb; the minivan zooms past (left -> right)"""
    un = 7.6
    acts = curb_chairs(t, 6.4, (300.0, 395.0)) + [own_chair(t, un, *DIBS_CURB)]
    if state == 'wave':
        acts.append(dibs_sitting(t, *DIBS_CURB, un, expr='smile', pose='wave', props={}, hands=None))
    elif state == 'paper':
        acts.append(dibs_sitting(t, *DIBS_CURB, un, expr='content', pose='hold', props={'R': 'newspaper'}, hands={'R': (18.0, 50.0)}))
    else:
        acts.append(dibs_sitting(t, *DIBS_CURB, un, expr='sleepy', props={'R': 'thermos'}))
    x = -150.0 + 1000.0 * (u / 0.9)
    acts += van_with_brad(t, x, 712.0, 6.0, 'wheel', 'panic')
    def fx_(big, v):
        fx.speed_lines(big, t, 0.35)
        if state == 'doze':
            ox, oy = v.opt(DIBS_CURB[0] + 30, DIBS_CURB[1] - 120)
            for k, s_ in enumerate((40, 56, 72)):
                world_text(big, v, 'Z', DIBS_CURB[0] + 24 + k * 12, DIBS_CURB[1] - 110 - k * 14 - 6 * ((t * 2) % 1), 8 + 3 * k, (240, 244, 255))
    return street(285.0, 500.0, 1.15, acts=acts, t=t, sy=330, fx_=fx_)


def r_lap1(t, u): return lap_shot(t, u, 'wave')
def r_lap2(t, u): return lap_shot(t, u + 0.3, 'paper')
def r_lap3(t, u): return lap_shot(t, u + 0.3, 'doze')


def r_park(t, u):
    """Brad in the minivan window, panicking"""
    def emit(big, v):
        big[0:150, :] = (46, 52, 64); big[150:166, :] = (92, 102, 118)
        big[1500:1920, 0:130] = (46, 52, 64); big[1500:1920, 130:146] = (92, 102, 118)
    big = cu(DC.brad, 'brad', t, u, 790.0, 430.0, Z=2.1, s=12.5, flip=True, k=1.7, pose='wheel', expr='panic', legs=False, look=0.8, sweat=1.0,
             emit=emit, extra=curb_chairs(t, 7.0), cdx=-40 * u)
    B.shake(big, t, 4, 30)
    return big


def r_point(t, u):
    """Dibs on his chair points helpfully across the street at Mrs. Wozniak's spot; the minivan rolls up to it"""
    un = 8.2
    k = sm(min(1.0, u / 1.6))
    vx = lerp(-100.0, 470.0, k)
    acts = [own_chair(t, un, 250.0, 666.0), mrsw_chair(t, 7.0)] + van_with_brad(t, vx, 712.0, 5.2, 'wheel', 'grin', look=0.0)
    acts.append(dibs_sitting(t, 250.0, 666.0, un, expr='smile', pose='point', props={'L': 'thermos'}, hands={'R': (44.0, 64.0)},
                             mth=mouth('dibs', t, 1.8)))
    return street(320.0, 520.0, 1.45, acts=acts, t=t, sy=330)


def r_move(t, u):
    """slow motion: Brad lifts Mrs. Wozniak's chair and sets it on the snowbank"""
    q = sm(u / 1.35)
    lift = 26.0 * math.sin(math.pi * min(1.0, q * 1.1))
    acts = [mrsw_chair(t, 8.6, dx=-70.0 * q, lift=lift, rot=-0.15 * math.sin(math.pi * q)),
            A(DC.brad, MW[0] + 46.0 - 40.0 * q, GY + 4, un=8.6, flip=True, pose='reach', hands={'R': (24.0, 40.0 + lift * 0.5)}, t=t,
              expr='grin', look=0.0, shadow=0.3)]
    big = street(MW[0] + 10.0, 540.0, 1.9, acts=acts, t=t, sy=330, snow=30)
    g = big.mean(axis=2, keepdims=True)
    big[:] = (big * 0.7 + g * 0.3).astype(np.uint8)
    if u > 1.38: O.flash(big, 0.3)
    return big


def split4(t, u, open_t=0.05, expr='glare', props=('binoculars', 'popcorn', 'binoculars', 'popcorn'), look=0.0):
    """2 x 2 split: four windows, four ladies, curtains snap open together"""
    out = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    for i, who in enumerate(('mrs_w', 'rose', 'dot', 'bev')):
        fr = DK.window_cut(t, u, who, open_t=open_t + 0.03 * i, prop=props[i], expr=expr, flip=i % 2 == 1, s=15.0, hires=2)   # halved below
        small = fr[::2, ::2]
        y0, x0 = (i // 2) * 960, (i % 2) * 540
        out[y0:y0 + 960, x0:x0 + 540] = small
    out[956:964, :] = (16, 14, 22); out[:, 536:544] = (16, 14, 22)
    return out


def r_curtains(t, u): return split4(t, u)


def r_d4(t, u):
    """Dibs on his chair, sly: the chair is placed under him the way dibs_sitting does it (feet anchor = chair + (1.5, 0.2) un)"""
    hx, hy, Z, zoom, s = 520.0, 430.0, 2.35, 0.05, 13.5
    Zt = Z + zoom * u; sc = s * Zt / Z; un = sc / (Zt * 0.75)
    ax, ay = DX.draw(DC.dibs, 1.0, hires=1, pose='sit', t=t).anchors['head']
    fx_, fy_ = hx - ax * sc / (3 * Zt), hy + ay * sc / (3 * Zt)                           # feet anchor, hero-depth world px
    chair = lambda CH, v: PR.dibs_chair(CH, v.cam(fx_ - 1.5 * un, fy_ - 0.2 * un, un * CHU), t=t)
    return cu(DC.dibs, 'dibs', t, u, hx, hy, Z=Z, s=s, zoom=zoom, pose='sit', hands={'R': (14.0, 52.0)}, props={'R': 'thermos'},
              expr='sly', mouth_=mouth('dibs', t, 1.5), k=1.5, near_acts=[chair])


def r_doors(t, u):
    """the left two-flat: the front door bursts open, warm light spills out, Mrs. Wozniak steps onto the porch with her rolling pin"""
    k = sm(u / 0.12)
    DX_, DY_ = 104.0, 298.0                                                     # doorway bottom centre (porch floor)
    def pre(big, v):
        ox, oy = v.opt(DX_, DY_); s_ = v.Z * 3
        w, h = int(30 * s_), int(64 * s_)
        x0, y0 = int(ox - w / 2), int(oy - h)
        big[max(0, y0 - 8):max(0, int(oy)), max(0, x0 - 8):max(0, x0 + w + 8)] = (40, 26, 22)          # frame
        big[max(0, y0):max(0, int(oy)), max(0, x0):max(0, x0 + w)] = (255, 214, 130)                     # warm light inside
        dw = int(w * (1 - 0.82 * k))                                                                     # the door swings open
        big[max(0, y0):max(0, int(oy)), max(0, x0):max(0, x0 + dw)] = (96, 52, 36)
        big[max(0, y0 + 10):max(0, int(oy) - 10), max(0, x0 + 8):max(0, x0 + max(9, dw - 8))] = (120, 70, 46)
        fx.glow(big, ox, oy - h // 2, 460 * v.Z * k, (255, 200, 120), 0.75 * k)
    acts = [lady_act('mrs_w', DX_ + 2.0, DY_ + 2.0, 7.0, t, expr='glare', flip=True)] if u > 0.06 else []
    def fx_(big, v):
        if u < 0.3:
            ox, oy = v.opt(DX_, DY_)
            for i in range(8):
                B.puff(big, ox - 180 + i * 50, oy - 10 - 40 * (i % 3) * u * 3, 70, 0.6 * (1 - u / 0.3), (240, 244, 252))
    big = street(118.0, 240.0, 1.7, acts=acts, pre=pre, fx_=fx_, t=t, sy=330)
    if u < 0.14: B.shake(big, t, 16, 40)
    return big


def r_lineup(t, u):
    """low angle: four ladies in a row, kitchen weapons up, robes in the wind, backlit by the street lamp"""
    acts = []
    for i, (who, x) in enumerate((('bev', 512.0), ('dot', 582.0), ('mrs_w', 652.0), ('rose', 722.0))):
        acts.append(lady_act(who, x, GY + 6 + 4 * (i % 2), 8.6, t + i * 0.2, expr='glare', flip=x > 620))
    big = street(617.0, 560.0, 1.42 + 0.06 * u, acts=acts, t=t, sy=360, snow=80)
    return big


def r_ope3(t, u):
    """Brad backs off, hands up to his mouth; the ladies advance"""
    k = sm(u / 1.5)
    bx = lerp(540.0, 492.0, k)
    acts = [A(DC.brad, bx, GY + 4, un=8.0, flip=False, pose=DC.walk('cover', t, 10.0, 0.3, 0.3), t=t,
              expr='ope' if talk('brad', t) > 0.05 else 'panic', mouth_=mouth('brad', t, 1.4), sweat=1.0, look=0.6, shadow=0.3)]
    for i, (who, x) in enumerate((('mrs_w', 680.0), ('rose', 735.0), ('dot', 790.0), ('bev', 842.0))):
        acts.append(lady_act(who, x - 60 * k, GY + 2 + 6 * (i % 2), 8.0, t, expr='glare', step=t * 8 + i))
    big = street(lerp(615.0, 590.0, k), 520.0, 1.3 + 0.08 * u, acts=acts, t=t, sy=330)
    if u > 1.1: B.shake(big, t, 6 + 6 * (u - 1.1), 36)
    return big


def r_ope_cu(t, u):
    big = cu(DC.brad, 'brad', t, u, 640.0, 440.0, Z=2.8, s=17.0, zoom=0.25, pose='ears', expr='ope', sweat=1.0, mouth_=0.9, cdy=0.0)
    B.shake(big, t, 12, 40)
    return big


def r_naperville(t, u):
    pin = DC.walk('hold', t, 0.0, 0.0, 0.0)
    tap = 4.0 * max(0.0, math.sin(t * 9))
    return cu(DC.lady, 'mrs_w', t, u, 600.0, 430.0, Z=2.3, s=13.0, zoom=0.05, who='mrs_w', pose='hold',
              hands={'L': (-6.0, 46.0 + tap * 0.3), 'R': (12.0, 50.0 + tap)}, props={'R': 'rolling_pin'}, expr='deadpan', legs=False, clip_h=None,
              k=1.5, flip=True)


def burrito(sp, t=0.0, wave=0.0, **_):
    """Brad rolled up in a snowbank: snow roll, head sticking out at the left, a hand with the trophy waving weakly up top, a dad sneaker"""
    DC.brad(sp, pose='reach', t=t, expr='ope', mouth_=0.35, hands={'R': (26.0, 52.0)}, legs=True, look=0.6)
    DX.rotate(sp, 90.0, pivot=(0.0, 40.0))
    snow = [(150, 166, 196), (196, 210, 232), (228, 236, 248), (250, 252, 255)]
    body = sp.cap((-20.0, 40.0), (44.0, 40.0), 17.0, 17.0, snow, olc=(120, 136, 170))
    rng = np.random.default_rng(3)
    sp.fill(body & (rng.random(body.shape) < 0.06), (176, 190, 220))                   # packed-snow texture
    sp.fill(body & (rng.random(body.shape) < 0.03), (255, 255, 255))
    end = sp.m_ell(52.0, 40.0, 7.0, 16.5)[0]
    sp.paint(end, snow, None, olc=(120, 136, 170))
    for r_ in (12.0, 8.0, 4.0):                                                       # the spiral of the roll
        ring = sp.m_ell(52.0, 40.0, r_ * 0.42, r_)[0]
        sp.fill(ring & ~erode_(ring), (150, 166, 196))
    sp.rect(57, 36, 64, 41, (250, 250, 252)); sp.rect(57, 35, 64, 36, (40, 90, 200))     # dad sneaker poking out
    for k in range(9):                                                                # snow clumps
        sp.dot(-14 + k * 7, 57 + (k % 3), (255, 255, 255)); sp.dot(-12 + k * 7, 23 - (k % 2), (180, 194, 220))
    hx, hy = sp.anchors['handR']
    w = 3.0 * math.sin(t * 7) * wave
    sp.cap((hx - 2, 54.0), (hx + w, hy + 6), 2.6, 2.4, ramp_((60, 190, 180)))
    DC.p_trophy(sp, (hx + w, hy + 6), 0.0, t)
    sp.anchors['roll'] = (12.0, 40.0)
    sp.outline()


def erode_(m): return DX.erode(m)
def ramp_(c): return DX.ramp(c)


def r_burrito(t, u):
    """crossing: four ladies carry the snow burrito down the street like a carpet"""
    p = t - TURN_T
    x = 380.0 + 140.0 * p
    acts = []
    for i, (who, dx) in enumerate((('dot', -46.0), ('mrs_w', -12.0), ('rose', 22.0), ('bev', 56.0))):
        acts.append(A(DC.lady, x + dx, GY + 4 + 3 * (i % 2), un=7.4, flip=False, who=who, pose='arms_up', t=t, expr='deadpan', legs=True,
                      clip_h=None, step=t * 9 + i * 1.3, shadow=0.3))
    acts.append(A(burrito, x + 6.0, GY - 146.0 + 3 * math.sin(t * 9), un=6.8, pin='roll', t=t, wave=1.0))
    big = street(x + 4.0, 500.0, 1.35, acts=acts, t=t, sy=330, fx_=lambda big, v: fx.speed_lines(big, t, 0.15))
    if p < 0.25:                                                                       # the roll-up whirl
        q = p / 0.25
        for k in range(14):
            a = k / 14 * 2 * math.pi + t * 12
            B.puff(big, 540 + math.cos(a) * 300 * (1 - q), 1100 + math.sin(a) * 220 * (1 - q), 120, 0.8 * (1 - q), (240, 244, 252))
    return big


def r_chief(t, u):
    return cu(DC.chief, 'chief', t, u, 700.0, 430.0, Z=2.3, s=12.5, zoom=0.05, flip=True, pose='stand', expr='deadpan', look=-0.5, k=1.5,
              near_pre=lambda big, v: reserved_sign(big, v, 820.0, 610.0))


BADGE = None


def badge_card(cross=0.0):
    """the «22 YRS PROBATIONARY» sticker with a red strike-through"""
    img = O.sticker('22 YRS PROBATIONARY', fg=(255, 120, 120), size=44)
    a = np.array(img).copy()
    if cross > 0:
        h, w = a.shape[:2]
        x1 = int(20 + (w - 40) * cross)
        a[h // 2 - 6:h // 2 + 6, 20:x1, :3] = (220, 30, 40); a[h // 2 - 6:h // 2 + 6, 20:x1, 3] = 255
    return a


def r_cry(t, u):
    big = cu(DC.dibs, 'dibs', t, u, 520.0, 430.0, Z=2.3, s=13.0, zoom=0.07, pose='tears', expr='cry', mouth_=0.25, badge22=True, look=0.3)
    paste_rgba(big, badge_card(sm((u - 0.15) / 0.3)), 540, 1180, -4.0, 1.0)
    if u > 0.55:
        q = min(1.0, (u - 0.55) / 0.08)
        paste_rgba(big, stamp_img('PERMANENT', 84, (40, 200, 110)), 560, 1300, 8.0, 1.0 + 0.6 * (1 - q))
        if u < 0.7: B.shake(big, t, 12, 40)
    return big


def r_heated(t, u):
    """Dibs on his chair on the heated spot, steam rising around him; slow pull back"""
    un = 8.4
    Z = lerp(1.7, 1.35, sm(u / 2.3))
    def pre(big, v):
        reserved_sign(big, v)
        B.steam(big, v, t, SPOT[0] - 40, SPOT[1] - 4, n=6, rise=160, size=50, a=0.45, seed=2)
        B.steam(big, v, t, SPOT[0] + 70, SPOT[1] - 2, n=6, rise=150, size=46, a=0.4, seed=5)
    ex = 'content' if u > 0.4 else 'smile'
    acts = [own_chair(t, un, *SPOT), dibs_sitting(t, *SPOT, un, expr=ex, mth=mouth('dibs', t, 1.6), props={'R': 'coffee'})]
    hx, hy = sit_anchor(*SPOT, un)
    return street(hx + 20.0, hy - 120.0, Z, acts=acts, pre=pre, t=t, sy=330, snow=50)


def taxi_acts(t, x, y=704.0, un=5.2, mth=0.0, arm=True):
    return [lambda CH, v: PR.taxi(CH, v.cam(x, y, un, True), t, driver=False, rot=-x * 0.2),
            DC.driver(DC.cabbie, x, y, un, 4.6, flip=True, pose='rest' if arm else 'stand', t=t, mouth_=mth, expr='deadpan')]


def r_taxi(t, u):
    """the yellow cab rolls up next to Dibs on the heated spot"""
    k = sm(min(1.0, u / 0.35))
    x = lerp(1060.0, 800.0, 1 - (1 - k) ** 2)
    un = 8.0
    acts = [own_chair(t, un, *SPOT), dibs_sitting(t, *SPOT, un, expr='content' if u < 0.35 else 'stunned', props={'R': 'coffee'})]
    acts += taxi_acts(t, x, 716.0, 6.4, mouth('cabbie', t, 1.6))
    big = street(715.0, 520.0, 1.25, acts=acts, pre=lambda big, v: reserved_sign(big, v), t=t, sy=330)
    if u < 0.4: B.shake(big, t, 4, 30)
    return big


def r_cabbie(t, u):
    def emit(big, v):
        big[0:170, :] = (240, 196, 30); big[170:186, :] = (150, 120, 20)                    # yellow roof edge
        big[1480:1920, :] = (240, 196, 30); big[1480:1496, :] = (150, 120, 20)              # door below the window
        for k in range(0, OUT_W, 80): big[1530:1570, k:k + 40] = (20, 20, 26)              # checker stripe
    return cu(DC.cabbie, 'cabbie', t, u, 700.0, 430.0, Z=2.3, s=13.0, zoom=0.05, flip=True, pose='rest', expr='deadpan', look=-0.5, k=1.5,
              emit=emit, cdx=-30.0)


def r_chorus(t, u):
    return split4(t, u, open_t=0.02, expr='glare', props=('rolling_pin', 'casserole', 'pan', 'mop'))


def r_marty2(t, u):
    return r_marty(t, u, zoom=0.08, Z=2.3, s=20.0)


def r_end(t, u):
    """the ladies march on the cab; Dibs sips"""
    acts = taxi_acts(t, 850.0, 716.0, 6.2, 0.0)
    for i, (who, x) in enumerate((('mrs_w', 610.0), ('rose', 655.0), ('dot', 700.0), ('bev', 742.0))):
        acts.append(lady_act(who, x + 40 * u, GY + 4 + 4 * (i % 2), 7.4, t, expr='glare', flip=False, step=t * 8 + i))
    big = street(735.0, 500.0, 1.2, acts=acts, t=t, sy=330)
    return big


# ================================================================== shot table
SHOTS = [
    (0.00, 1.85, 'hook'), (1.85, 3.30, 'ope'), (3.30, 4.55, 'marty'), (4.55, 7.85, 'board'), (7.85, 10.00, 'd2'), (10.00, 11.00, 'snacks1'),
    (11.00, 12.15, 'snacks2'), (12.15, 14.70, 'thing'), (14.70, 16.40, 'chase'), (16.40, 17.30, 'lap1'), (17.30, 18.40, 'park'),
    (18.40, 18.75, 'lap2'), (18.75, 19.05, 'lap3'), (19.05, 20.95, 'point'), (20.95, 22.40, 'move'), (22.40, 23.25, 'curtains'),
    (23.25, 25.50, 'd4'), (25.50, 25.95, 'doors'), (25.95, 26.45, 'lineup'), (26.45, 27.95, 'ope3'), (27.95, 28.70, 'ope_cu'), (28.70, TURN_T, 'naperville'),
    (TURN_T, 31.95, 'burrito'), (31.95, 33.30, 'chief'), (33.30, 34.35, 'cry'), (34.35, 36.70, 'heated'), (36.70, 37.40, 'taxi'),
    (37.40, 39.20, 'cabbie'), (39.20, 39.95, 'chorus'), (39.95, 41.40, 'marty2'), (41.40, DUR + 1, 'end'),
]
FUNCS = {'hook': r_hook, 'ope': r_ope, 'marty': r_marty, 'board': r_board, 'd2': r_d2, 'snacks1': r_snacks1, 'snacks2': r_snacks2,
         'thing': r_thing, 'chase': r_chase, 'lap1': r_lap1, 'park': r_park, 'lap2': r_lap2, 'lap3': r_lap3, 'point': r_point, 'move': r_move,
         'curtains': r_curtains, 'd4': r_d4, 'doors': r_doors, 'lineup': r_lineup, 'ope3': r_ope3, 'ope_cu': r_ope_cu, 'naperville': r_naperville,
         'burrito': r_burrito, 'chief': r_chief, 'cry': r_cry, 'heated': r_heated, 'taxi': r_taxi, 'cabbie': r_cabbie, 'chorus': r_chorus,
         'marty2': r_marty2, 'end': r_end}


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    return FUNCS[name](t, u)


# ================================================================== overlays
def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 6, ['OPE.', 'BUSTED.'], hook_t=(0.15, 2.0),
              stickers=[
                  (st('25 MPH', (255, 236, 120), 64), 14.85, 16.35, 540, 330),
                  (st('SEASON 2', (110, 210, 255), 84), 40.40, DUR + 1, 540, 360),
              ],
              flashes=[], mosaics=[], cap_default=1400,
              cap_y={'hook': 520, 'board': 1790, 'thing': 1500, 'chase': 1500, 'snacks2': 1760, 'lap1': 1500, 'point': 1720, 'ope3': 1500, 'burrito': 1500,
                     'taxi': 1500, 'end': 1500, 'cry': 1560, 'curtains': 1780, 'chorus': 1780})


def render(t):
    big = render_scene(t)
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
