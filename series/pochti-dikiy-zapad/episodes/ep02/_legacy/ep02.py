import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import numpy as np, math, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
import scene as S
import hd as HDP
from scene import Layer, cap, dot, outline, comp, hsh, sm, lerp, GROUND

FPS = 30
DUR = 46.3
PX_FONT = P.FONT_PX


# ---------------------------------------------------------------- camera with anchor + flip
class ACam:
    def __init__(s, ax, ay, sx, sy, sc, flip=False):
        s.ax, s.ay, s.sx, s.sy, s.sc, s.flip = ax, ay, sx, sy, sc, flip
    def p(s, x, y):
        X = (x - s.ax) * s.sc
        return (s.sx + (-X if s.flip else X), s.sy + (y - s.ay) * s.sc)
    def sub(s, wx, wy, scale=1.0, flip=False):
        """camera for an object drawn around anchor (1000,1000) placed at world (wx,wy)"""
        sx, sy = s.p(wx, wy)
        return ACam(1000.0, 1000.0, sx, sy, s.sc * scale, flip)

_ell0 = S.ell
def ell_flip(L, cxy, rx, ry, c, ang=0.0, **kw):
    if getattr(L.cam, 'flip', False): ang = -ang
    return _ell0(L, cxy, rx, ry, c, ang, **kw)
S.ell = ell_flip
ell = ell_flip

# ---------------------------------------------------------------- audio envelopes
ENV = {k: S.load_env(P.voice_wav('ep02', k)) for k in ('b1', 'b2', 'b3', 'b4', 'b5', 'm1', 'm2', 'm3', 's1', 's2', 's3')}
ENV['n4'] = None  # lip flap for reused ep01 line is synthetic
def env(k, tl):
    e = ENV.get(k)
    if e is None: return 0.0
    i = int(tl * 100)
    return float(e[i]) if 0 <= i < len(e) else 0.0

# (name, start_on_timeline, clip_in, clip_out)
CLIPS = [('b1', 0.0, 0.10, 2.45), ('b2', 2.6, 0.0, 6.32), ('m1a', 8.8, 0.0, 1.0), ('m1b', 9.8, 1.45, 2.16),
         ('b3', 11.1, 0.0, 1.70), ('m2', 14.3, 0.0, 0.96), ('s1', 18.3, 0.0, 3.36), ('b4', 21.6, 0.0, 1.45),
         ('s2', 23.4, 0.0, 2.0), ('s3', 27.7, 0.0, 3.84), ('n4', 31.7, 0.0, 0.72), ('b5', 37.1, 0.0, 4.56),
         ('m3', 42.4, 0.0, 0.80)]
SPK = {'b': 'billy', 'm': 'molniya', 's': 'sam', 'n': 'molniya'}
def talk(who, t):
    v = 0.0
    for nm, st, a, b in CLIPS:
        if SPK[nm[0]] != who: continue
        if st <= t < st + (b - a):
            key = nm[:2] if nm[:2] in ENV else nm
            v = max(v, env(key, a + t - st)) if key in ENV and ENV[key] is not None else max(v, 0.6 * (0.5 + 0.5 * math.sin(t * 40)))
    return v

# ---------------------------------------------------------------- layout (world units, 108x192 space)
HORSE_Y = GROUND - 19
CACT = (80.0, 144.0)            # barrel-cactus costume centre
POST_X = 47.0                   # wanted-poster post (Molniya "hides" behind it)
H_X0, H_X1 = 20.0, 30.5         # Molniya before / after hiding
DONKEY_STOP = 100.0

T_HIDE0, T_HIDE1 = 12.8, 14.0
T_OUT0, T_OUT1 = 33.0, 34.2     # Molniya steps back out
T_DONKEY_IN0, T_DONKEY_IN1 = 15.3, 17.8
T_DISMOUNT0, T_DISMOUNT1 = 17.9, 18.3
T_SAM_WALK0, T_SAM_WALK1 = 18.5, 20.8   # to cactus
T_SIT = 21.3
T_STAND = 25.8
T_WALK2_0, T_WALK2_1 = 26.0, 27.6       # to Molniya
T_SPILL = 29.9
T_WALK3_0, T_WALK3_1 = 32.5, 34.3       # back to donkey
T_MOUNT = 34.4
T_LEAVE0, T_LEAVE1 = 34.6, 37.2
T_BURST = 36.8
T_JUMPBACK0, T_JUMPBACK1 = 44.0, 44.9
CU_COSTUME = [(0.0, 2.4), (45.0, DUR + 1)]
CU_MOLNIYA = [(8.6, 11.0), (41.7, 43.9)]

SAM_X_SIT = CACT[0] + 0.5
SAM_X_GIVE = 67.0

# ---------------------------------------------------------------- pixel text
_font_cache = {}
def pfont(size):
    if size not in _font_cache: _font_cache[size] = ImageFont.truetype(PX_FONT, size)
    return _font_cache[size]

def px_text(F, text, cx, cy, size, col, shadow=None):
    f = pfont(size)
    bb = f.getbbox(text); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    img = Image.new('L', (tw + 4, th + 4), 0)
    d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((2 - bb[0], 2 - bb[1]), text, font=f, fill=255)
    m = np.array(img) > 127
    x0, y0 = int(round(cx - tw / 2)) - 2, int(round(cy - th / 2)) - 2
    Hh, Ww = F.shape[:2]
    ys, xs = np.nonzero(m)
    for off, c in (((1, 1), shadow), ((0, 0), col)):
        if c is None: continue
        yy, xx = ys + y0 + off[1], xs + x0 + off[0]
        ok = (yy >= 0) & (yy < Hh) & (xx >= 0) & (xx < Ww)
        F[yy[ok], xx[ok]] = c

# ---------------------------------------------------------------- props
def rect(L, x0, y0, x1, y1, c):
    ax, ay = L.cam.p(x0, y0); bx, by = L.cam.p(x1, y1)
    xa, xb = sorted((ax, bx)); ya, yb = sorted((ay, by))
    w = S.win(xa, xb, ya, yb)
    if w is None: return
    X = S.XX[w]; Y = S.YY[w]
    L.set(w, (X >= xa) & (X < xb) & (Y >= ya) & (Y < yb), c)
WOOD, WOOD_H, WOOD_D = (140, 92, 54), (172, 120, 74), (96, 60, 34)
PAPER, PAPER_D = (238, 220, 172), (200, 176, 124)

def draw_town(F, cam):
    L = Layer(cam)
    col, win = (176, 124, 96), (140, 92, 72)
    for x0, w, h in ((66, 7, 7), (73.5, 9, 10), (83, 6, 6), (89.5, 8, 8)):
        rect(L, x0, 141 - h, x0 + w, 141, col)
        rect(L, x0 + 1, 141 - h - 1.5, x0 + w - 1, 141 - h, col)   # false front
    cap(L, (97.5, 141), (97.5, 132), 0.4, 0.4, col); cap(L, (100.5, 141), (100.5, 132), 0.4, 0.4, col)
    ell(L, (99, 130.5), 2.8, 2.2, col)                       # water tower
    cap(L, (78, 131), (78, 128), 0.25, 0.25, col)             # flag pole
    comp(F, L)
    for x in (68, 70, 75, 77.5, 80, 85, 91, 93.5):
        sx, sy = cam.p(x, 137); F[int(sy):int(sy) + 2, int(sx):int(sx) + 1] = win
    sx, sy = cam.p(78, 128.3); F[int(sy):int(sy) + 2, int(sx):int(sx) + 3] = (190, 60, 50)

def draw_skull(L, x, y):
    w = (240, 234, 220)
    ell(L, (x, y), 3.0, 1.9, w, hi=(252, 250, 244))
    cap(L, (x - 2.2, y - 0.8), (x - 5.0, y - 3.0), 0.6, 0.3, w)
    cap(L, (x + 2.2, y - 0.8), (x + 5.0, y - 3.0), 0.6, 0.3, w)
    cap(L, (x, y + 1.0), (x, y + 2.6), 1.1, 0.8, w)
    dot(L, (x - 1.1, y - 0.2), (60, 44, 40), 0.45); dot(L, (x + 1.1, y - 0.2), (60, 44, 40), 0.45)

def draw_signpost(F, cam, big=False):
    L = Layer(cam)
    cap(L, (12, 152), (12, 101), 1.1, 1.0, WOOD, sh=WOOD_D)
    # plank 1 -> right (САЛУН), plank 2 <- left (ТЮРЬМА)
    for (xa, xb, y, tip) in ((3.5, 24.5, 106, 1), (0.5, 22.5, 116, -1)):
        cap(L, (xa, y), (xb, y), 3.3, 3.3, WOOD, hi=WOOD_H, sh=WOOD_D)
        tx = xb + 2.6 if tip > 0 else xa - 2.6
        ell(L, (tx - tip * 0.6, y), 2.4, 3.0, WOOD)
    outline(L, (60, 36, 20)); comp(F, L)
    s = 8 if cam.sc < 3 else (16 if cam.sc < 6 else 32)
    x, y = cam.p(14.0, 106); px_text(F, 'САЛУН', x, y + 1, s, (250, 236, 196), (70, 40, 20))
    x, y = cam.p(11.5, 116); px_text(F, 'ТЮРЬМА', x, y + 1, s, (250, 236, 196), (70, 40, 20))
    # vulture perch top
    return (12, 101)

def draw_poster(F, cam, post_front=False, board=True):
    if board:
        L = Layer(cam)
        cap(L, (POST_X, 150), (POST_X, 78), 1.1, 1.0, WOOD, sh=WOOD_D)
        comp(F, L)
        L = Layer(cam)
        x0, x1, y0, y1 = POST_X - 13.5, POST_X + 13.5, 78.5, 108.5
        rect(L, x0, y0, x1, y1, PAPER)
        rect(L, x0, y1 - 1.0, x1, y1, PAPER_D)
        rect(L, x1 - 0.8, y0, x1, y1, PAPER_D)
        for (a, b) in ((x0 + 1, y1 - 1.2), (x1 - 1.4, y0 + 1)):
            ell(L, (a, b), 1.6, 1.3, PAPER_D)                                            # worn corners
        # Sam portrait
        fx, fy = POST_X, 94.5
        ell(L, (fx, fy + 0.8), 3.8, 4.2, (226, 176, 136), sh=(196, 146, 108))
        cap(L, (fx - 6.0, fy - 3.3), (fx + 6.0, fy - 3.3), 0.9, 0.9, (46, 40, 48))
        ell(L, (fx, fy - 5.2), 3.4, 2.2, (46, 40, 48))
        cap(L, (fx - 3.6, fy - 0.2), (fx + 3.6, fy - 0.2), 1.0, 1.0, (24, 20, 24))
        dot(L, (fx - 1.6, fy - 0.2), (250, 250, 250), 0.35); dot(L, (fx + 1.6, fy - 0.2), (250, 250, 250), 0.35)
        cap(L, (fx - 3.2, fy + 2.8), (fx + 3.2, fy + 2.8), 0.8, 0.5, (34, 26, 24))
        for a, b in ((x0 + 1.2, y0 + 1.2), (x1 - 1.2, y0 + 1.2)):
            dot(L, (a, b), (120, 110, 100), 0.45)
        outline(L, (92, 70, 44)); comp(F, L)
        s = 8 if cam.sc < 3 else (16 if cam.sc < 6 else 32)
        x, y = cam.p(POST_X, 83.3); px_text(F, 'РОЗЫСК', x, y, s, (120, 36, 28))
        x, y = cam.p(POST_X, 104.3); px_text(F, '$500', x, y, s, (60, 44, 30))
    if post_front:  # the thin post in front of the horse
        L = Layer(cam)
        cap(L, (POST_X, 151), (POST_X, 109), 1.1, 1.0, WOOD, sh=WOOD_D)
        outline(L, (60, 36, 20)); comp(F, L)


def draw_costume(F, cam, t, squash=0.0, eyes='normal', sway=0.0, hand=0.0, pieces=None):
    """barrel-cactus costume with Billy inside. pieces: None (closed) or offset 0..1 of the two halves flying apart"""
    g, gh, gs = (86, 150, 72), (126, 190, 98), (56, 112, 52)
    cx, cy = CACT
    rx, ry = 7.6 * (1 + 0.12 * squash), 8.4 * (1 - 0.18 * squash)
    cy = 152.4 - ry
    L = Layer(cam)
    # boots peeking out
    if pieces is None or pieces < 0.05:
        for bx in (-2.6, 2.4):
            cap(L, (cx + bx, 151.4), (cx + bx + 1.8, 151.6), 1.1, 1.0, (80, 50, 34))
    if pieces is None:
        ell(L, (cx + sway, cy), rx, ry, g, hi=gh, sh=gs)
        for k in (-4.6, -2.0, 0.6, 3.2, 5.6):  # ribs
            cap(L, (cx + sway + k * 0.95, cy - ry * 0.82), (cx + sway + k, cy + ry * 0.82), 0.35, 0.35, gs)
        ell(L, (cx + sway, cy - ry + 0.6), 2.2, 1.3, (236, 110, 150), hi=(255, 160, 190))  # flower
        dot(L, (cx + sway, cy - ry + 0.3), (255, 220, 120), 0.5)
        # hand popping out: "ХВАТЬ!"
        if hand > 0:
            hx0, hy0 = cx + sway + rx - 1, cy + 0.5
            hx1, hy1 = hx0 + 7 * hand, hy0 - 3.5 * hand
            cap(L, (hx0, hy0), (hx1, hy1), 1.0, 0.9, (198, 66, 50))
            ell(L, (hx1 + 0.6, hy1 - 0.2), 1.3, 1.1, (236, 186, 144))
        # face window
        fx, fy = cx + sway, cy + 0.3
        ell(L, (fx, fy), 4.3, 2.6, (40, 30, 28))
        big = 1.35 if eyes == 'bulge' else 1.0
        if eyes == 'closed':
            cap(L, (fx - 2.4, fy - 0.3), (fx - 0.8, fy - 0.3), 0.3, 0.3, (236, 186, 144))
            cap(L, (fx + 0.8, fy - 0.3), (fx + 2.4, fy - 0.3), 0.3, 0.3, (236, 186, 144))
        else:
            look = {'left': -0.45, 'right': 0.45}.get(eyes, 0.0)
            if eyes == 'dart': look = 0.45 * math.sin(t * 7)
            for ex in (-1.6, 1.6):
                ell(L, (fx + ex, fy - 0.4), 1.15 * big, 1.25 * big, (250, 250, 246))
                dot(L, (fx + ex + look, fy - 0.3), (30, 20, 16), 0.45 * big)
        cap(L, (fx - 1.8, fy + 1.5), (fx + 1.8, fy + 1.5), 0.55, 0.45, (96, 60, 36))  # mustache
        outline(L, (40, 72, 36)); comp(F, L)
        L = Layer(cam)
        for i in range(14):  # spines
            a = i * 2 * math.pi / 14 + 0.3
            dot(L, (cx + sway + (rx + 0.4) * math.cos(a), cy + (ry + 0.3) * math.sin(a)), (244, 240, 212), 0.35)
        comp(F, L)
    else:
        k = pieces
        for side in (-1, 1):
            ox = side * 14 * k; oy = -10 * k + 16 * k * k; rot = side * 3.0 * k
            ll = Layer(cam)
            c = (cx + ox + side * rx * 0.45, cy + oy)
            ell(ll, c, rx * 0.5, ry, g, rot, hi=gh, sh=gs)
            cap(ll, (c[0], c[1] - ry * 0.7), (c[0], c[1] + ry * 0.7), 0.35, 0.35, gs)
            outline(ll, (40, 72, 36)); comp(F, ll)
        comp(F, L)


def draw_vulture(L, x, y, flap, perched=False, facing=1):
    body, head = (52, 42, 46), (206, 128, 118)
    if perched:
        ell(L, (x, y - 3.0), 2.6, 3.4, body, hi=(78, 66, 70))
        cap(L, (x - facing * 1.8, y - 1.0), (x - facing * 3.4, y + 0.8), 0.9, 0.5, body)
        cap(L, (x - 1.4, y - 5.8), (x + 1.4, y - 5.8), 0.8, 0.8, (214, 206, 196))  # ruff
        cap(L, (x + facing * 0.4, y - 6.4), (x + facing * 1.0, y - 8.2), 0.5, 0.5, head)
        ell(L, (x + facing * 1.2, y - 8.6), 1.0, 0.9, head)
        cap(L, (x + facing * 1.9, y - 8.6), (x + facing * 2.9, y - 8.0), 0.4, 0.25, (230, 210, 150))
        dot(L, (x + facing * 1.4, y - 8.9), (20, 14, 14), 0.3)
        return
    w = math.sin(flap)
    ell(L, (x, y), 1.8, 0.9, body)
    for side in (-1, 1):
        cap(L, (x + side * 0.8, y), (x + side * 4.2, y - 1.6 * w), 0.8, 0.5, body)
        cap(L, (x + side * 4.2, y - 1.6 * w), (x + side * 6.4, y - 0.4 * w), 0.5, 0.25, body)
    ell(L, (x + facing * 1.9, y - 0.3), 0.6, 0.55, head)


def draw_sack(L, x, y, open_k=0.0):
    ell(L, (x, y), 3.2, 2.8, (216, 188, 128), hi=(238, 214, 160), sh=(186, 158, 104))
    if open_k < 0.5:
        cap(L, (x, y - 2.8), (x, y - 4.2), 0.9, 1.2, (216, 188, 128))
        cap(L, (x - 1.1, y - 3.0), (x + 1.1, y - 3.0), 0.35, 0.35, (140, 100, 60))


def draw_carrot(L, x, y, ang, s=1.0):
    ca, sa = math.cos(ang), math.sin(ang)
    x1, y1 = x + 4.6 * s * ca, y + 4.6 * s * sa
    cap(L, (x, y), (x1, y1), 1.3 * s, 0.4 * s, (236, 128, 40), hi=(255, 176, 90))
    for a in (-0.5, 0.0, 0.5):
        cap(L, (x, y), (x - 2.0 * s * math.cos(ang + a), y - 2.0 * s * math.sin(ang + a)), 0.45 * s, 0.25 * s, (84, 160, 60))


def walk_pose(p):
    legs = []
    for kind, off in (('h', 0.0), ('f', 0.25), ('h', 0.5), ('f', 0.75)):
        ph = 2 * math.pi * (p + off)
        if kind == 'f':
            a1 = 0.02 + 0.28 * math.sin(ph); a2 = a1 - 0.7 * max(0.0, math.cos(ph)) ** 2
        else:
            a1 = -0.33 + 0.26 * math.sin(ph); a2 = a1 + 0.5 + 0.5 * max(0.0, math.cos(ph)) ** 2
        legs.append((a1, a2))
    return dict(legs=legs, bob=-0.5 * abs(math.sin(2 * math.pi * p)), pitch=0.0, neck=-0.92, head=0.8,
                jaw=0.0, wind=0.0, ear=0.3, lid=0.55)

DONKEY = dict(body=(150, 144, 140), hi=(182, 176, 170), sh=(114, 108, 106), far=(118, 112, 110), farsh=(92, 88, 86),
              mane=(70, 64, 64), maneh=(100, 94, 92), muz=(214, 208, 198), white=(236, 232, 224),
              blanket=(176, 128, 60), blanket_h=(206, 160, 84))
BANDIT = dict(hat=(46, 40, 48), hat_h=(76, 68, 80), band=(190, 50, 50), shirt=(96, 70, 128), shirt_h=(124, 96, 158),
              shirt_sh=(70, 50, 96), vest=(40, 34, 36), jeans=(90, 80, 70), jeans_sh=(66, 58, 50), bandana=(196, 52, 52),
              mst=(34, 26, 24), skin=(226, 176, 136))

def with_pal(d, pal, fn):
    old = {k: d[k] for k in pal}; d.update(pal)
    try: return fn()
    finally: d.update(old)

def long_ears(L, hs, hd_, up, ear, t, moving):
    for side, off in ((0, -0.7), (1, 0.5)):
        base = (hs[0] + up[0] * 2.3 - hd_[0] * (0.2 - off), hs[1] + up[1] * 2.3 - hd_[1] * (0.2 - off))
        e = ear + side * 0.25 + (0.15 * math.sin(t * 6) if moving else 0.05 * math.sin(t * 1.3))
        tip = (base[0] + 6.2 * (up[0] * math.cos(e) - hd_[0] * math.sin(e)), base[1] + 6.2 * (up[1] * math.cos(e) - hd_[1] * math.sin(e)))
        cap(L, base, tip, 1.4, 0.7, S.HC['body'] if side else S.HC['far'])
        if side: cap(L, base, tip, 0.5, 0.3, (90, 84, 82))

def draw_donkey(F, cam, x, t, moving, flip):
    c = cam.sub(x, GROUND, 0.78, flip)
    L = Layer(c)
    p = (t * 1.6) % 1.0
    P = walk_pose(p) if moving else S.stand_pose(t)
    P.update(neck=-0.55, head=0.95, ear=0.75, lid=0.3)
    T, hs, hd_, up = with_pal(S.HC, DONKEY, lambda: S.draw_horse(L, 1000.0, 1000.0 - 19, P, t, p, saddle=True))
    with_pal(S.HC, DONKEY, lambda: long_ears(L, hs, hd_, up, P['ear'], t, moving))
    outline(L, (38, 30, 30)); comp(F, L)
    return c, T

def sam_pose(kind, t):
    if kind == 'walk':
        s = math.sin(t * 9)
        return dict(nleg=(0.45 * s, 0.2 * max(0, -s)), fleg=(-0.45 * s, 0.2 * max(0, s)), narm=(-0.4 * s, -0.2), farm=(0.4 * s, -0.2))
    if kind == 'stand':
        return dict(nleg=(0.08, 0.0), fleg=(-0.08, 0.0), narm=(0.15, 0.1), farm=(-0.1, 0.0))
    if kind == 'sit':
        return dict(nleg=(1.45, 0.25), fleg=(1.35, 0.3), narm=(0.9, 1.9), farm=(0.6, 1.2))
    if kind == 'give':
        return dict(nleg=(0.08, 0.0), fleg=(-0.08, 0.0), narm=(1.4, 1.6), farm=(-0.1, 0.0))
    if kind == 'ride':
        return dict(nleg=(1.3, 0.15), fleg=(1.25, 0.2), narm=(0.9, 1.6), farm=(0.8, 1.5))
    return sam_pose('stand', t)

def draw_sam(F, cam, hip_w, flip, kind, t, tip=0.0, carry=False):
    c = cam.sub(hip_w[0], hip_w[1], 0.9, flip)
    L = Layer(c)
    hip = (1000.0, 1000.0)
    pose = sam_pose(kind, t)
    if tip > 0: pose['narm'] = (lerp(pose['narm'][0], 2.9, tip), lerp(pose['narm'][1], 3.6, tip))
    mouth = talk('sam', t)
    hatpos = with_pal(S.CC, BANDIT, lambda: S.cowboy(L, hip, 0.03, pose, hat_on=tip < 0.05, mouth=mouth))
    if tip >= 0.05:
        with_pal(S.CC, BANDIT, lambda: S.hat(L, (hatpos[0] + 0.8 * tip, hatpos[1] - 2.2 * tip), -0.3 * tip))
    cap(L, (hip[0] - 1.2, hip[1] - 10.3), (hip[0] + 2.6, hip[1] - 10.3), 0.75, 0.75, (24, 20, 24))
    dot(L, (hip[0] + 1.8, hip[1] - 10.3), (240, 240, 240), 0.3)
    cap(L, (hip[0] + 1.3, hip[1] - 8.4), (hip[0] + 3.4, hip[1] - 7.2), 0.6, 0.4, (34, 26, 24))
    if carry:
        draw_sack(L, hip[0] - 3.2, hip[1] + 4.4 - 9.5)
        cap(L, (hip[0] - 1.6, hip[1] - 6.5), (hip[0] - 3.0, hip[1] - 8.2), 0.5, 0.5, (140, 100, 60))
    outline(L, (20, 14, 14)); comp(F, L)

# ---------------------------------------------------------------- horse (Molniya)
def molniya_x(t):
    if t < T_HIDE0: return H_X0
    if t < T_HIDE1: return lerp(H_X0, H_X1, sm((t - T_HIDE0) / (T_HIDE1 - T_HIDE0)))
    if t < T_OUT0: return H_X1
    if t < T_OUT1: return lerp(H_X1, H_X0, sm((t - T_OUT0) / (T_OUT1 - T_OUT0)))
    return H_X0

def molniya_pose(t):
    moving = (T_HIDE0 < t < T_HIDE1) or (T_OUT0 < t < T_OUT1)
    p = (t * 1.3) % 1.0
    P = walk_pose(p) if moving else S.stand_pose(t)
    P.update(lid=0.55, ear=0.3 + 0.08 * math.sin(t * 1.1))
    if not moving: P.update(neck=-0.95, head=0.78)
    ha = talk('molniya', t)
    chew = 0.0
    if T_SPILL + 0.4 < t < 31.5 or 34.5 < t < 44.0: chew = 0.2 * (1 + math.sin(2 * math.pi * 2.3 * t))
    if T_SPILL + 0.3 < t < 31.5:  # bends to the carrots
        k = sm((t - T_SPILL - 0.3) / 0.5) * (1 - sm((t - 31.0) / 0.5))
        P['neck'] = lerp(P['neck'], 0.4, k); P['head'] = lerp(P['head'], 1.35, k)
    P['jaw'] = max(chew, min(ha * 1.6, 1.0) * 0.8)
    # glance at Sam while he talks to her
    if T_WALK2_1 < t < 31.6 and P['neck'] < 0: P['head'] = 0.9
    return P, p, moving

def draw_molniya(F, cam, t, carrot_in_mouth=False):
    x = molniya_x(t)
    P, p, moving = molniya_pose(t)
    L = Layer(cam)
    T, hs, hd_, up = S.draw_horse(L, x, HORSE_Y, P, t, p, saddle=True)
    pos, rot = S.head_hat_anchor(x, HORSE_Y, P); S.hat(L, pos, rot)
    if carrot_in_mouth:
        he = (hs[0] + hd_[0] * 8.5, hs[1] + hd_[1] * 8.5); dn = (-hd_[1], hd_[0])
        draw_carrot(L, he[0] + dn[0] * 1.5 - hd_[0] * 0.6, he[1] + dn[1] * 1.5 - hd_[1] * 0.6, 0.15, 1.1)
    S.draw_ears(L, hs, hd_, up, P['ear'])
    outline(L, S.HC['ol']); comp(F, L)
    return hs, hd_, up

# ---------------------------------------------------------------- particles (deterministic)
rng = np.random.default_rng(22)
PARTS = []
def puff_burst(t0, x, y, n, spd, life, r0, r1, col=(238, 218, 180)):
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        v = spd * rng.uniform(0.4, 1.0)
        PARTS.append(dict(b=t0, x=x, y=y, vx=v * math.cos(a), vy=v * math.sin(a) - spd * 0.3, life=life * rng.uniform(0.7, 1.1), r0=r0, r1=r1, col=col))
puff_burst(T_DISMOUNT1, DONKEY_STOP - 8, GROUND - 0.5, 6, 10, 0.5, 0.8, 2.2)
puff_burst(T_SIT, CACT[0], GROUND - 1, 8, 12, 0.6, 0.8, 2.4)
puff_burst(T_SPILL, SAM_X_GIVE - 8, GROUND - 1, 8, 12, 0.6, 0.8, 2.4)
puff_burst(T_BURST, CACT[0], CACT[1], 14, 26, 0.7, 1.2, 3.4)
puff_burst(T_BURST, CACT[0], CACT[1], 10, 30, 0.8, 0.4, 0.4, col=(126, 190, 98))  # green bits
puff_burst(T_JUMPBACK1, CACT[0], GROUND + 1, 6, 12, 0.35, 0.8, 2.0)
for k in range(12):  # sparkles over carrots
    PARTS.append(dict(b=T_SPILL + 0.3 + k * 0.08, x=SAM_X_GIVE - 9 + rng.uniform(-5, 5), y=GROUND - 3 + rng.uniform(-3, 1),
                      vx=0, vy=-6, life=0.5, r0=0.0, r1=0.0, col=(255, 240, 150), star=True))

def draw_parts(F, cam, t):
    L = Layer(cam)
    thin1 = ((S.XX.astype(int) + S.YY.astype(int)) % 2 == 0)
    for p in PARTS:
        a = t - p['b']
        if a < 0 or a > p['life']: continue
        k = a / p['life']
        x = p['x'] + p['vx'] * a; y = p['y'] + p['vy'] * a + 10 * a * a
        if p.get('star'):
            S.star(L, (x, y), p['col']); continue
        r = lerp(p['r0'], p['r1'], k)
        if r < 0.6: dot(L, (x, y), p['col'], 0.4)
        else: ell(L, (x, y), r, r * 0.8, p['col'], hi=(250, 238, 212) if p['col'][0] > 200 else None)
    if L.m.any():
        fade = thin1 & L.m
        L.m &= ~fade | (np.random.default_rng(int(t * 30)).random(L.m.shape) > 0.5)
    comp(F, L)

def draw_motes(F, cam, t):
    for i in range(22):
        x = (i * 37.3 + t * (3 + i % 4)) % 116 - 4
        y = 96 + (i * 13.7) % 54 + 1.5 * math.sin(t * 1.3 + i)
        sx, sy = cam.p(x, y)
        if 0 <= sx < S.W - 1 and 0 <= sy < S.H - 1:
            F[int(sy), int(sx)] = (252, 244, 214) if i % 3 else (236, 220, 180)

# ---------------------------------------------------------------- scene state helpers
SPILL_CARROTS = [(-4.5, -0.2, 0.2), (-7.8, 0.6, 2.7), (-10.5, -0.4, 0.9), (-6.2, 1.8, -0.4), (-12.6, 1.2, 3.4), (-9.2, 2.4, 1.6)]
def sam_state(t):
    """returns (hip_world, flip, kind, carry, on_donkey)"""
    hip_h = GROUND - 9.4 * 0.9
    if t < T_DISMOUNT0: return None
    if t < T_DISMOUNT1:
        k = (t - T_DISMOUNT0) / (T_DISMOUNT1 - T_DISMOUNT0)
        return ((lerp(DONKEY_STOP - 1, DONKEY_STOP - 7, k), lerp(GROUND - 14, hip_h, k) - 3 * math.sin(math.pi * k)), True, 'stand', True)
    if t < T_SAM_WALK0: return ((DONKEY_STOP - 7, hip_h), True, 'stand', True)
    if t < T_SAM_WALK1:
        k = (t - T_SAM_WALK0) / (T_SAM_WALK1 - T_SAM_WALK0)
        return ((lerp(DONKEY_STOP - 7, SAM_X_SIT + 5, k), hip_h - 0.4 * abs(math.sin(t * 9))), True, 'walk', True)
    if t < T_SIT: 
        k = sm((t - T_SAM_WALK1) / (T_SIT - T_SAM_WALK1))
        return ((lerp(SAM_X_SIT + 5, SAM_X_SIT, k), lerp(hip_h, CACT[1] - 9.2, k)), True, 'stand' if k < 0.5 else 'sit', True)
    if t < T_STAND: return ((SAM_X_SIT, CACT[1] - 8.4 * 0.95 + 0.6 * math.exp(-(t - T_SIT) * 4)), True, 'sit', True)
    if t < T_WALK2_0: return ((SAM_X_SIT + 1, hip_h), True, 'stand', True)
    if t < T_WALK2_1:
        k = (t - T_WALK2_0) / (T_WALK2_1 - T_WALK2_0)
        return ((lerp(SAM_X_SIT + 1, SAM_X_GIVE, k), hip_h - 0.4 * abs(math.sin(t * 9))), True, 'walk', True)
    if t < T_SPILL: return ((SAM_X_GIVE, hip_h), True, 'give' if t > T_SPILL - 0.8 else 'stand', True)
    if t < T_WALK3_0: return ((SAM_X_GIVE, hip_h), True, 'stand', False)
    if t < T_WALK3_1:
        k = (t - T_WALK3_0) / (T_WALK3_1 - T_WALK3_0)
        return ((lerp(SAM_X_GIVE, DONKEY_STOP - 7, k), hip_h - 0.4 * abs(math.sin(t * 9))), False, 'walk', False)
    if t < T_MOUNT: return ((DONKEY_STOP - 7, hip_h), False, 'stand', False)
    return 'donkey'

def donkey_state(t):
    if t < T_DONKEY_IN0: return None
    if t < T_DONKEY_IN1: return (lerp(128, DONKEY_STOP, (t - T_DONKEY_IN0) / (T_DONKEY_IN1 - T_DONKEY_IN0)), True, True)
    if t < T_LEAVE0: return (DONKEY_STOP, False if t >= T_MOUNT else True, False)
    if t < T_LEAVE1: return (lerp(DONKEY_STOP, 138, (t - T_LEAVE0) / (T_LEAVE1 - T_LEAVE0)), False, True)
    return None

def costume_state(t):
    """(visible_closed, pieces, squash, eyes, sway, hand)"""
    squash = 0.0
    if T_SIT <= t < T_STAND + 0.2: squash = min(1.0, (t - T_SIT) / 0.15) * (1 - sm((t - T_STAND) / 0.2))
    if t < 2.4: eyes = 'dart' if t > 0.7 else 'normal'
    elif T_SIT < t < 23.2: eyes = 'bulge'
    elif T_DONKEY_IN0 < t < T_SIT: eyes = 'right'
    elif T_WALK2_0 < t < T_WALK3_1: eyes = 'left'
    elif t > 45.0: eyes = 'closed' if 45.6 < t < 45.75 else 'dart'
    else: eyes = 'normal'
    sway = 0.5 * math.sin(t * 2.2) if 2.6 < t < 8.5 else 0.0
    hand = 0.0
    if 7.6 < t < 8.6: hand = sm((t - 7.6) / 0.12) * (1 - sm((t - 8.3) / 0.3))
    if T_BURST <= t < T_JUMPBACK0: return (False, min(1.0, (t - T_BURST) / 0.45), 0, eyes, 0, 0)
    if T_JUMPBACK0 <= t < T_JUMPBACK1:
        k = (t - T_JUMPBACK0) / (T_JUMPBACK1 - T_JUMPBACK0)
        if k < 0.7: return (False, 1.0 - k / 0.7, 0, eyes, 0, 0)
    return (True, None, squash, eyes, sway, hand)

def billy_out(t):
    """Billy standing outside the costume (after burst) -> hip world or None"""
    if T_BURST + 0.05 <= t < T_JUMPBACK0 + 0.63:
        if t < T_BURST + 0.5:
            k = (t - T_BURST) / 0.45
            return (CACT[0], GROUND - 9.4 - 6 * math.sin(math.pi * min(k, 1)))
        if t >= T_JUMPBACK0:
            k = (t - T_JUMPBACK0) / 0.63
            return (CACT[0], GROUND - 9.4 - 9 * math.sin(math.pi * k) + 4 * k)
        return (CACT[0], GROUND - 9.4)
    return None

# ---------------------------------------------------------------- overlays
FONT = ImageFont.truetype(P.FONT_BOLD, 64)
FONT_B = ImageFont.truetype(P.FONT_BOLD, 34)
YEL, WHT, PUR = (255, 222, 96), (255, 255, 255), (214, 170, 255)
CAPS = [
    (0.2, 2.45, 'Тс-с. Я\u00a0— КАКТУС.', YEL),
    (2.6, 8.8, 'План гениальный: Сэм подъедет\u00a0— а\u00a0я\u00a0его... ХВАТЬ!', YEL),
    (8.8, 11.0, 'Можно. А\u00a0зачем?', WHT),
    (11.1, 12.9, 'Молния! ПРЯЧЬСЯ!', YEL),
    (14.3, 15.6, 'Спряталась.', WHT),
    (18.3, 21.7, 'Какой славный кактус... Присяду.', PUR),
    (21.8, 23.1, 'Ммм-мф-ф-ф!', YEL),
    (23.5, 25.5, 'Хм. Тёплый.', PUR),
    (27.7, 31.6, 'Как договаривались, мэм. Морковь за\u00a0неделю.', PUR),
    (31.7, 32.6, 'Спасибо.', WHT),
    (37.1, 41.7, 'Засада сработала! Он меня даже не\u00a0ЗАМЕТИЛ!', YEL),
    (42.4, 43.9, 'Воздухан.', WHT),
]

def make_text(text, color, font=FONT, width=1000):
    img = Image.new('RGBA', (1080, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    words = text.split(); rows = []; cur = ''
    for w in words:
        tst = (cur + ' ' + w).strip()
        if d.textlength(tst, font=font) > width and cur: rows.append(cur); cur = w
        else: cur = tst
    rows.append(cur); y = 20
    for r in rows:
        tw = d.textlength(r, font=font)
        d.text(((1080 - tw) / 2, y), r, font=font, fill=color + (255,), stroke_width=8, stroke_fill=(20, 12, 10, 255))
        y += int(font.size * 1.3)
    return np.array(img)
CAP_IMG = [make_text(c[2], c[3]) for c in CAPS]

def pixel_title(lines, size=64):
    """series-style pixel title (same look as covers) rendered at full res, RGBA"""
    f = pfont(size)
    out = Image.new('RGBA', (1080, len(lines) * (size + 40) + 40), (0, 0, 0, 0))
    arr = np.array(out)
    y = 20
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (1080, th + 40), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((1080 - tw) // 2 - bb[0], 16 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        dil = m.copy()
        for dx in range(-8, 9, 2):
            for dy in range(-8, 9, 2):
                dil |= np.roll(np.roll(m, dy, 0), dx, 1)
        shd = np.roll(np.roll(dil, 10, 0), 6, 1)
        reg = arr[y:y + m.shape[0]]
        reg[shd] = (20, 10, 6, 255); reg[dil] = (42, 22, 12, 255)
        rows = np.where(m.any(1))[0]; r0, r1 = rows[0], rows[-1]
        for yy in range(m.shape[0]):
            k = (yy - r0) / max(1, r1 - r0)
            col = (255, 236, 120) if k < 0.34 else (255, 200, 70) if k < 0.67 else (255, 150, 50)
            reg[yy][m[yy]] = col + (255,)
        top = m & ~np.roll(m, 8, 0)
        reg[top] = (255, 250, 214, 255)
        y += th + 44
    return arr
HOOK = pixel_title(['ИДЕАЛЬНАЯ', 'МАСКИРОВКА'], 64)
TEASE = pixel_title(['СЕРИЯ 3 СКОРО'], 40)

def make_badge(text):
    img = Image.new('RGBA', (560, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    tw = d.textlength(text, font=FONT_B)
    d.rounded_rectangle((0, 0, tw + 36, 58), 14, fill=(20, 12, 10, 120))
    d.text((18, 9), text, font=FONT_B, fill=(255, 244, 214, 200))
    return np.array(img)
BADGE = make_badge('СЕЗОН 1 • СЕРИЯ 2/6')

def overlay(big, img, x0, y0, k=1.0):
    h, w = img.shape[:2]
    region = big[y0:y0 + h, x0:x0 + w]
    al = img[:region.shape[0], :region.shape[1], 3:4].astype(np.float32) / 255 * k
    region[:] = (region * (1 - al) + img[:region.shape[0], :region.shape[1], :3] * al).astype(np.uint8)

# ---------------------------------------------------------------- frame
CAMX = 300.0
def in_ranges(t, rr): return any(a <= t < b for a, b in rr)

def render(t):
    bg = S.background(CAMX, t)
    cu_c = in_ranges(t, CU_COSTUME); cu_m = in_ranges(t, CU_MOLNIYA)
    if cu_c:
        x0, y0 = 66.5, 110.5
        F = np.repeat(np.repeat(bg[int(y0 * 2):int(y0 * 2) + 96, int(x0 * 2):int(x0 * 2) + 54], 4, 0), 4, 1).copy()
        cam = ACam(x0, y0, 0, 0, 8.0)
    elif cu_m:
        P, p, _ = molniya_pose(t)
        hs0 = S.horse_frames(molniya_x(t), HORSE_Y, P)[3]
        x0 = round((hs0[0] - 12) * 2) / 2; y0 = round((hs0[1] - 27) * 2) / 2
        F = np.repeat(np.repeat(bg[int(y0 * 2):int(y0 * 2) + 96, int(x0 * 2):int(x0 * 2) + 54], 4, 0), 4, 1).copy()
        cam = ACam(x0, y0, 0, 0, 8.0)
    else:
        F = bg
        cam = ACam(0, 0, 0, 0, 2.0)
    wide = not (cu_c or cu_m)

    if wide: draw_town(F, cam)
    # vultures (sky)
    L = Layer(cam)
    vA_perch = 20.0 <= t < T_BURST
    for i, (cx, cy, r, sp, ph) in enumerate(((78, 66, 16, 0.55, 0.0), (66, 54, 11, -0.7, 2.0))):
        if i == 0 and t >= 19.0:
            if t < 20.0:
                k = sm(t - 19.0); a = ph + sp * 19.0
                sx0, sy0 = cx + r * math.cos(a), cy + 0.35 * r * math.sin(a)
                draw_vulture(L, lerp(sx0, 12, k), lerp(sy0, 101, k) - 3 * math.sin(math.pi * k), t * 9)
                continue
            if vA_perch:
                draw_vulture(L, 12, 101, 0, perched=True, facing=1 if (t % 6) < 3 else -1); continue
            k = t - T_BURST
            draw_vulture(L, 12 + 30 * k, 101 - 34 * k, t * 14); continue
        a = ph + sp * t
        draw_vulture(L, cx + r * math.cos(a), cy + 0.35 * r * math.sin(a), t * 6 + i, facing=1 if sp * math.cos(a) < 0 else -1)
    outline(L, (30, 24, 26)); comp(F, L)

    # signpost + skull (left) and poster board
    draw_signpost(F, cam)
    draw_poster(F, cam, board=True)
    L = Layer(cam); draw_skull(L, 7.5, 157.5)
    for (x, y, r) in ((30, 160, 1.6), (58, 163, 1.2), (102, 158, 1.8)):
        ell(L, (x, y), r * 1.4, r, (170, 138, 104), hi=(196, 166, 128))
    outline(L, (110, 84, 60)); comp(F, L)

    # donkey (behind cactus/Sam)
    dst = donkey_state(t)
    if dst:
        dx, dflip, dmoving = dst
        dcam, dT = draw_donkey(F, cam, dx, t, dmoving, dflip)
        if t >= T_MOUNT or t < T_DISMOUNT0:  # Sam riding
            L = Layer(dcam)
            hip = dT(-1, -8.4)
            pose = sam_pose('ride', t)
            bob = 0.4 * math.sin(t * 10) if dmoving else 0
            with_pal(S.CC, BANDIT, lambda: S.cowboy(L, (hip[0], hip[1] + bob), 0.05, pose, True, 0))
            cap(L, (hip[0] - 1.2, hip[1] + bob - 10.3), (hip[0] + 2.6, hip[1] + bob - 10.3), 0.75, 0.75, (24, 20, 24))
            cap(L, (hip[0] + 1.3, hip[1] + bob - 8.4), (hip[0] + 3.4, hip[1] + bob - 7.2), 0.6, 0.4, (34, 26, 24))
            if t < T_DISMOUNT0: draw_sack(L, hip[0] - 7.5, hip[1] - 1.5)
            outline(L, (20, 14, 14)); comp(F, L)

    # sack + spilled carrots
    if T_SPILL <= t:
        L = Layer(cam)
        sx = SAM_X_GIVE - 8
        k = min(1.0, (t - T_SPILL) / 0.5)
        draw_sack(L, sx, GROUND - 2.2, open_k=1.0)
        eaten = 0
        if t > 42.0: eaten = 1
        for i, (ox, oy, ang) in enumerate(SPILL_CARROTS[eaten:]):
            kk = sm(k * 1.3 - i * 0.05)
            draw_carrot(L, sx + ox * kk, GROUND - 1.5 + oy * kk - 3 * math.sin(math.pi * kk), ang * kk, 0.95)
        outline(L, (70, 40, 20)); comp(F, L)

    # Molniya
    hs, hd_, up = draw_molniya(F, cam, t, carrot_in_mouth=(t > 41.7 and t < 44.0))
    draw_poster(F, cam, post_front=True, board=False)

    # costume / Billy
    vis, pieces, squash, eyes, sway, hand = costume_state(t)
    b_hip = billy_out(t)
    if b_hip is not None:
        L = Layer(cam)
        arms = (2.8 + 0.2 * math.sin(t * 8), 3.1) if t < T_JUMPBACK0 else (2.4, 2.9)
        pose = dict(nleg=(0.12, 0.0), fleg=(-0.12, 0.05), narm=arms, farm=(2.6, 3.0))
        mouth = talk('billy', t)
        S.cowboy(L, b_hip, 0.0, pose, False, mouth)
        cap(L, (b_hip[0] - 1.6, b_hip[1] - 12.6), (b_hip[0] + 0.8, b_hip[1] - 13.4), 0.9, 0.6, CC_HAIR)
        outline(L, S.CC['ol']); comp(F, L)
    if vis:
        draw_costume(F, cam, t, squash, eyes, sway, hand, None)
    elif pieces is not None:
        draw_costume(F, cam, t, 0, eyes, 0, 0, pieces)

    # Sam on foot
    st = sam_state(t)
    if st and st != 'donkey':
        hip, flip, kind, carry = st
        tip = 0.0
        if T_WALK2_1 < t < T_WALK2_1 + 1.2: tip = sm((t - T_WALK2_1) / 0.25) * (1 - sm((t - T_WALK2_1 - 0.9) / 0.3))
        draw_sam(F, cam, hip, flip, kind, t, tip, carry)

    draw_parts(F, cam, t)
    if wide: draw_motes(F, cam, t)
    # tumbleweed
    if 15.0 < t < 18.8 and wide:
        L = Layer(cam)
        k = (t - 15.0) / 3.8
        S.tumbleweed(L, (lerp(-8, 118, k), GROUND + 4 - abs(math.sin(t * 5)) * 6), t * 8)
        comp(F, L)

    # upscale + overlays
    big = np.repeat(np.repeat(F, 5, 0), 5, 1)
    overlay(big, BADGE, 36, 96)
    for (a, b, _, _), img in zip(CAPS, CAP_IMG):
        if a <= t < b: overlay(big, img, 0, 250, min(1.0, (t - a) / 0.08))
    if 0.2 <= t < 2.3:
        k = min(1.0, (t - 0.2) / 0.1) * (1 - sm((t - 2.1) / 0.2))
        overlay(big, HOOK, 0, 700, k)
    if t >= 45.4:
        overlay(big, TEASE, 0, 1560, min(1.0, (t - 45.4) / 0.15))
    return big

CC_HAIR = (96, 60, 36)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        ts = list(map(float, sys.argv[2:]))
        c = Image.new('RGB', (270 * len(ts), 480))
        for k, tt in enumerate(ts):
            c.paste(Image.fromarray(render(tt)).resize((270, 480), Image.NEAREST), (k * 270, 0))
        c.save(P.build('ep02', 'sheet.png')); sys.exit()
    n = int(DUR * FPS)
    a0, a1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 and sys.argv[1] == 'seg' else (0, n)
    out = P.build('ep02', f'seg_{a0:04d}.mp4')
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', str(FPS),
                             '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    COVER = np.array(Image.open(str(P.episode('ep02') / 'cover.png')).convert('RGB'))
    for i in range(a0, min(a1, n)):
        if i < 6:
            proc.stdin.write(COVER.tobytes()); continue
        proc.stdin.write(render(i / FPS).tobytes())
    proc.stdin.close(); proc.wait(); print('done')
