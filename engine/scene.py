import numpy as np, math, wave, sys, subprocess
import paths as P
from PIL import Image, ImageDraw, ImageFont

W, H = 108, 192          # logical pixel canvas (9:16)
S = 10                   # upscale -> 1080x1920
FPS = 30
DUR = 16.0
GROUND = 150
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32) + 0.5

# ---------------------------------------------------------------- timeline
V = 40.0                 # gallop scroll speed px/s
T_BRAKE, T_STOP = 6.1, 6.8
T_LAUNCH, T_LAND = 6.35, 7.45
T_HAT = 8.1
T_EAT0, T_EAT1 = 8.4, 10.3
T_CLOSE = 10.4
HORSE_SX = 34            # horse screen x while tracking


def cam_x(t):
    if t < T_BRAKE:
        return V * t
    d = T_STOP - T_BRAKE
    u = min(t - T_BRAKE, d)
    return V * T_BRAKE + V * u - V * u * u / (2 * d)


CAMX_STOP = cam_x(T_STOP)
HORSE_WX = CAMX_STOP + HORSE_SX
CARROT_WX = HORSE_WX + 21
CACTUS_WX = CAMX_STOP + 88


def clamp01(x): return 0.0 if x < 0 else 1.0 if x > 1 else x
def sm(x): x = clamp01(x); return x * x * (3 - 2 * x)
def lerp(a, b, t): return a + (b - a) * t


# ---------------------------------------------------------------- audio envelopes (lip flap)
def load_env(path):
    w = wave.open(path)
    n = w.getnframes(); sr = w.getframerate()
    a = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
    hop = int(sr / 100)
    rms = np.array([np.sqrt(np.mean(a[i:i + hop * 3] ** 2) + 1e-9) for i in range(0, len(a), hop)])
    return rms / (rms.max() + 1e-9)


ENV = {k: load_env(P.voice_wav('ep01', k)) for k in ('c1', 'h1')}
def amp(k, tl):
    e = ENV[k]; i = int(tl * 100)
    return float(e[i]) if 0 <= i < len(e) else 0.0

# horse speech placed in two chunks
HA_T, HA_IN, HA_OUT = 10.9, 0.0, 1.48
HB_T, HB_IN, HB_OUT = 13.05, 3.05, 4.75
def horse_amp(t):
    if HA_T <= t < HA_T + HA_OUT - HA_IN: return amp('h1', HA_IN + t - HA_T)
    if HB_T <= t < HB_T + HB_OUT - HB_IN: return amp('h1', HB_IN + t - HB_T)
    return 0.0

# ---------------------------------------------------------------- drawing core
class Cam:
    def __init__(s, x0, y0, sc=1.0): s.x0, s.y0, s.sc = x0, y0, sc
    def p(s, x, y): return ((x - s.x0) * s.sc, (y - s.y0) * s.sc)


class Layer:
    def __init__(s, cam):
        s.cam = cam
        s.col = np.zeros((H, W, 3), np.uint8)
        s.m = np.zeros((H, W), bool)
    def set(s, w, m, c):
        sub = s.col[w]; sub[m] = c
        mm = s.m[w]; mm |= m


def win(x0, x1, y0, y1):
    xa = max(int(math.floor(x0)), 0); xb = min(int(math.ceil(x1)) + 1, W)
    ya = max(int(math.floor(y0)), 0); yb = min(int(math.ceil(y1)) + 1, H)
    if xa >= xb or ya >= yb: return None
    return (slice(ya, yb), slice(xa, xb))


def cap(L, a, b, r0, r1, c, hi=None, sh=None, hit=0.45, sht=-0.5):
    cm = L.cam
    ax, ay = cm.p(*a); bx, by = cm.p(*b); r0 *= cm.sc; r1 *= cm.sc
    R = max(r0, r1) + 1
    w = win(min(ax, bx) - R, max(ax, bx) + R, min(ay, by) - R, max(ay, by) + R)
    if w is None: return
    X = XX[w]; Y = YY[w]
    dx, dy = bx - ax, by - ay; l2 = dx * dx + dy * dy + 1e-6
    t = np.clip(((X - ax) * dx + (Y - ay) * dy) / l2, 0, 1)
    ex = X - (ax + t * dx); ey = Y - (ay + t * dy)
    r = r0 + (r1 - r0) * t
    m = ex * ex + ey * ey <= r * r
    L.set(w, m, c)
    if hi is not None or sh is not None:
        s_ = -ey / np.maximum(r, 0.6)
        if hi is not None: L.set(w, m & (s_ > hit), hi)
        if sh is not None: L.set(w, m & (s_ < sht), sh)


def ell(L, cxy, rx, ry, c, ang=0.0, hi=None, sh=None, hit=0.5, sht=-0.45):
    cm = L.cam
    cx, cy = cm.p(*cxy); rx *= cm.sc; ry *= cm.sc
    R = max(rx, ry) + 1
    w = win(cx - R, cx + R, cy - R, cy + R)
    if w is None: return
    X = XX[w] - cx; Y = YY[w] - cy
    ca, sa = math.cos(ang), math.sin(ang)
    u = X * ca + Y * sa; v = -X * sa + Y * ca
    m = (u / rx) ** 2 + (v / ry) ** 2 <= 1
    L.set(w, m, c)
    if hi is not None: L.set(w, m & (-Y / ry > hit), hi)
    if sh is not None: L.set(w, m & (-Y / ry < sht), sh)


def dot(L, xy, c, r=0.5):
    cm = L.cam
    x, y = cm.p(*xy)
    rr = max(r * cm.sc, 0.5)
    w = win(x - rr - 1, x + rr + 1, y - rr - 1, y + rr + 1)
    if w is None: return
    X = XX[w] - x; Y = YY[w] - y
    m = (np.abs(X) <= rr) & (np.abs(Y) <= rr)
    if not m.any():
        xi, yi = int(x), int(y)
        if 0 <= xi < W and 0 <= yi < H: L.col[yi, xi] = c; L.m[yi, xi] = True
        return
    L.set(w, m, c)


def outline(L, c):
    m = L.m
    d = np.zeros_like(m)
    d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
    o = d & ~m
    L.col[o] = c; L.m |= o


def comp(F, L): F[L.m] = L.col[L.m]


def hsh(n):
    n = (np.asarray(n, np.int64) * 374761393 + 668265263) & 0xffffffff
    n = ((n ^ (n >> 13)) * 1274126177) & 0xffffffff
    return n ^ (n >> 16)

# ---------------------------------------------------------------- background
SKY = [(62, 98, 164), (84, 128, 188), (118, 160, 204), (164, 192, 212), (220, 204, 172), (242, 194, 140)]
SKY_E = [0, 30, 56, 78, 98, 114]
MESAS = [(-60, 14, 26), (-5, 9, 18), (40, 16, 30), (95, 8, 20), (140, 18, 24), (190, 10, 32), (240, 14, 22), (290, 12, 28)]


def sky_rows():
    col = np.zeros((H, 3), np.uint8); dith = np.zeros(H, bool)
    for y in range(H):
        k = 0
        for i, e in enumerate(SKY_E):
            if y >= e: k = i
        col[y] = SKY[k]
        if k + 1 < len(SKY_E) and SKY_E[k + 1] - y <= 2: dith[y] = True
    return col, dith
SKY_COL, SKY_DITH = sky_rows()


def background(camx, t):
    F = np.empty((H, W, 3), np.uint8)
    F[:] = SKY_COL[:, None, :]
    # dither band transitions
    for y in range(H):
        if SKY_DITH[y]:
            k = [i for i, e in enumerate(SKY_E) if y >= e][-1]
            if k + 1 < len(SKY):
                F[y, (np.arange(W) + y) % 2 == 0] = SKY[k + 1]
    # sun + glow
    L = Layer(Cam(0, 0))
    d2 = (XX - 92) ** 2 + (YY - 70) ** 2
    glow = (d2 < 14 ** 2) & (d2 >= 11 ** 2) & (((XX + YY).astype(int) % 2) == 0)
    F[glow] = (250, 226, 170)
    F[d2 < 10.5 ** 2] = (255, 226, 150)
    F[d2 < 9 ** 2] = (255, 240, 196)
    # clouds
    for bx, by, sz, par in ((20, 22, 1.0, 0.03), (95, 60, 0.8, 0.05), (160, 34, 1.2, 0.02)):
        x = (bx - camx * par - t * 1.2) % (W + 60) - 30
        L = Layer(Cam(0, 0))
        ell(L, (x, by), 9 * sz, 2.6 * sz, (246, 244, 236))
        ell(L, (x - 4 * sz, by - 1.8 * sz), 4.5 * sz, 2.6 * sz, (246, 244, 236))
        ell(L, (x + 3 * sz, by - 2.4 * sz), 5 * sz, 3 * sz, (250, 250, 244))
        sub = L.m & (YY > by + 1.2 * sz)
        L.col[sub] = (212, 214, 224)
        comp(F, L)
    # far mesas
    cols = np.arange(W) + 0.5
    wx = cols + camx * 0.08
    h = np.zeros(W)
    for c, hw, ht in MESAS:
        for rep in (-340, 0, 340, 680):
            h = np.maximum(h, np.clip(ht - np.maximum(0, np.abs(wx - c - rep) - hw) * 1.8, 0, None))
    base = 132
    for x in range(W):
        top = int(base - h[x])
        if h[x] <= 0: continue
        F[top:base, x] = (204, 126, 94)
        F[top, x] = (232, 160, 120)
        if top + 1 < base: F[top + 1, x] = (222, 146, 108)
        for yy in range(top + 4, base, 5):
            F[yy, x] = (182, 108, 82)
    # mid hills
    wx2 = cols + camx * 0.25
    hh = 5 + 2.5 * np.sin(wx2 * 0.07) + 2 * np.sin(wx2 * 0.023 + 1.3)
    for x in range(W):
        top = int(139 - hh[x])
        F[top:141, x] = (190, 144, 98)
        F[top, x] = (210, 166, 116)
    # mid-ground props (parallax 0.55)
    L = Layer(Cam(0, 0))
    off = camx * 0.55
    for k in range(int(off // 26) - 1, int((off + W) // 26) + 2):
        hv = int(hsh(k))
        x = k * 26 + (hv % 17) - off
        if hv % 3 == 0:
            ht = 5 + hv % 4
            cap(L, (x, 140), (x, 140 - ht), 1.1, 1.1, (96, 132, 76))
            cap(L, (x - 2.2, 137 - ht * 0.3), (x - 2.2, 134 - ht * 0.5), 0.7, 0.7, (96, 132, 76))
        elif hv % 3 == 1:
            ell(L, (x, 140), 2.2, 1.3, (150, 120, 96), hi=(176, 148, 120))
    outline(L, (120, 96, 70))
    comp(F, L)
    # ground bands
    F[141:, :] = (216, 176, 122)
    F[143:161, :] = (230, 198, 148)
    F[143, :] = (204, 164, 112)
    F[161:170, :] = (210, 168, 112)
    F[170:, :] = (182, 150, 96)
    # ruts & pebbles scroll at parallax 1
    wxi = (np.arange(W) + int(camx)).astype(np.int64)
    hv = hsh(wxi)
    for y, sal in ((148, 7), (156, 11)):
        m = (hv // sal) % 5 < 3
        F[y, m] = (214, 180, 132)
    peb = hv % 19 == 0
    py = 145 + (hv // 19) % 14
    for x in np.where(peb)[0]:
        F[py[x], x] = (186, 150, 108)
        if x + 1 < W: F[py[x], x + 1] = (244, 220, 176)
    # grass tufts on near sand
    peb2 = hv % 7 == 0
    for x in np.where(peb2)[0]:
        y0 = 162 + (hv[x] // 7) % 6
        F[y0:y0 + 2, x] = (150, 150, 80)
    # foreground scrub (parallax 1.3)
    wxf = (np.arange(W) + int(camx * 1.3)).astype(np.int64)
    hf = hsh(wxf + 9999)
    for x in range(W):
        hgt = 3 + int(hf[x] % 6) if hf[x] % 3 == 0 else int(hf[x] % 2)
        F[192 - 14 - hgt:192 - 14, x] = (120, 124, 60) if hf[x] % 2 else (146, 146, 72)
        F[192 - 14:, x] = (110, 104, 58)
    lighter = (hf % 11 == 0)
    F[181, lighter] = (170, 164, 90)
    return F

# ---------------------------------------------------------------- horse
HC = dict(body=(152, 88, 48), hi=(186, 118, 66), sh=(114, 64, 36), far=(118, 68, 40), farsh=(92, 52, 30),
          mane=(52, 34, 28), maneh=(86, 58, 44), hoof=(46, 36, 32), white=(238, 232, 216), ol=(38, 24, 18),
          muz=(104, 62, 42), mouth=(80, 30, 30), eye=(24, 16, 14), blanket=(170, 52, 42), blanket_h=(206, 78, 58),
          saddle=(94, 58, 36), saddle_h=(130, 84, 52))


def gallop_pose(p, t):
    legs = []
    for kind, off in (('h', 0.0), ('f', 0.42), ('h', 0.1), ('f', 0.52)):
        ph = 2 * math.pi * (p + off)
        if kind == 'f':
            a1 = 0.12 + 0.62 * math.sin(ph)
            a2 = a1 - 1.7 * max(0.0, math.cos(ph)) ** 1.5
        else:
            a1 = -0.35 + 0.58 * math.sin(ph)
            a2 = a1 + 0.5 + 1.2 * max(0.0, math.cos(ph)) ** 1.5
        legs.append((a1, a2))
    return dict(legs=legs, bob=-1.4 * math.sin(2 * math.pi * p + 0.6), pitch=0.05 * math.sin(2 * math.pi * p),
                neck=-0.92 + 0.1 * math.sin(2 * math.pi * p + 1.2), head=0.72, jaw=0.0, wind=1.0, ear=0.7, lid=0.0)


def stand_pose(t):
    return dict(legs=[(-0.3, 0.2), (0.02, 0.0), (-0.36, 0.14), (-0.04, -0.04)], bob=0.0, pitch=0.0,
                neck=-0.95, head=0.78, jaw=0.0, wind=0.0, ear=0.3, lid=0.0)


def brake_pose(t):
    return dict(legs=[(0.45, 0.9), (0.75, 0.8), (0.35, 0.8), (0.85, 0.9)], bob=2.5, pitch=-0.22,
                neck=-1.25, head=0.35, jaw=0.25, wind=0.6, ear=-0.2, lid=0.0)


def blend(a, b, k):
    o = {}
    for key in a:
        if key == 'legs':
            o[key] = [(lerp(x[0], y[0], k), lerp(x[1], y[1], k)) for x, y in zip(a[key], b[key])]
        else:
            o[key] = lerp(a[key], b[key], k)
    return o


def horse_frames(x, y, P):
    """returns transform + key frames (head start/dir) in world coords"""
    pc, ps = math.cos(P['pitch']), math.sin(P['pitch'])
    by = y + P['bob']
    def T(lx, ly): return (x + lx * pc - ly * ps, by + lx * ps + ly * pc)
    an = P['neck']
    nb = (8.0, -3.0)
    ne = (nb[0] + 11 * math.cos(an), nb[1] + 11 * math.sin(an))
    ah = P['head']
    hd = (math.cos(ah + P['pitch']), math.sin(ah + P['pitch']))
    hs = T(*ne)
    return T, nb, ne, hs, hd


def head_hat_anchor(x, y, P):
    T, nb, ne, hs, hd = horse_frames(x, y, P)
    up = (hd[1], -hd[0])
    pos = (hs[0] + up[0] * 2.6 + hd[0] * 1.2, hs[1] + up[1] * 2.6 + hd[1] * 1.2)
    rot = math.atan2(up[0], -up[1])
    return pos, rot


def draw_leg(L, T, att, a1, a2, l1, l2, r1a, r1b, r2, col, shc, sock):
    K = (att[0] + l1 * math.sin(a1), att[1] + l1 * math.cos(a1))
    Fp = (K[0] + l2 * math.sin(a2), K[1] + l2 * math.cos(a2))
    Hf = (Fp[0] + 1.7 * math.sin(a2), Fp[1] + 1.7 * math.cos(a2))
    cap(L, T(*att), T(*K), r1a, r1b, col, sh=shc)
    cap(L, T(*K), T(*Fp), r2, r2 * 0.9, col)
    if sock:
        mid = (lerp(K[0], Fp[0], 0.55), lerp(K[1], Fp[1], 0.55))
        cap(L, T(*mid), T(*Fp), r2 * 0.95, r2 * 0.95, HC['white'])
    cap(L, T(*Fp), T(*Hf), 1.35, 1.25, HC['hoof'])


def draw_horse(L, x, y, P, t, p_gallop, saddle=True):
    T, nb, ne, hs, hd = horse_frames(x, y, P)
    legs = P['legs']
    # far legs
    draw_leg(L, T, (-10, 2), *legs[0], 8, 7.5, 3.6, 1.8, 1.25, HC['far'], HC['farsh'], False)
    draw_leg(L, T, (10, 3), *legs[1], 7, 7.5, 2.6, 1.5, 1.2, HC['far'], HC['farsh'], False)
    # tail
    w = P['wind']
    base = (-14.5, -3.5)
    pts = [base]
    ang0 = lerp(1.35, 0.3, w)
    for i in range(1, 6):
        a = ang0 + 0.28 * w * math.sin(2 * math.pi * 2 * p_gallop - i * 0.9) + (1 - w) * 0.06 * math.sin(t * 2.2 - i * 0.7) + i * 0.08 * (1 - w)
        px, py = pts[-1]
        pts.append((px - 3.2 * math.cos(a), py + 3.2 * math.sin(a)))
    for i in range(5):
        r0 = 2.4 - i * 0.35
        cap(L, T(*pts[i]), T(*pts[i + 1]), r0, r0 - 0.35, HC['mane'])
    for i in range(1, 4):
        cap(L, T(*pts[i]), T(*pts[i + 1]), 0.6, 0.4, HC['maneh'])
    # body
    ell(L, T(-9, -0.5), 7.4, 7.2, HC['body'], P['pitch'], hi=HC['hi'], sh=HC['sh'])
    ell(L, T(9, 0.5), 6.4, 6.6, HC['body'], P['pitch'], hi=HC['hi'], sh=HC['sh'])
    ell(L, T(0, 0.3), 13.5, 6.4, HC['body'], P['pitch'], hi=HC['hi'], sh=HC['sh'])
    # dapple shading patch on hindquarter
    ell(L, T(-10, 1.5), 3.2, 2.2, HC['sh'], P['pitch'])
    # neck
    cap(L, T(*nb), T(*ne), 5.2, 3.3, HC['body'], hi=HC['hi'], sh=HC['sh'])
    # head
    he = (hs[0] + hd[0] * 8.5, hs[1] + hd[1] * 8.5)
    dn = (-hd[1], hd[0]); up = (hd[1], -hd[0])
    if dn[1] < 0: dn, up = up, dn
    cap(L, hs, he, 3.4, 2.3, HC['body'], hi=HC['hi'], sh=HC['sh'])
    mz0 = (hs[0] + hd[0] * 6.2, hs[1] + hd[1] * 6.2)
    cap(L, mz0, he, 2.35, 2.2, HC['muz'])
    jaw = P['jaw']
    if jaw > 0.05:
        j0 = (hs[0] + hd[0] * 4 + dn[0] * 1.2, hs[1] + hd[1] * 4 + dn[1] * 1.2)
        j1 = (he[0] + dn[0] * (0.9 + jaw * 2.6) - hd[0] * jaw, he[1] + dn[1] * (0.9 + jaw * 2.6) - hd[1] * jaw)
        cap(L, (hs[0] + hd[0] * 5 + dn[0] * 0.8, hs[1] + hd[1] * 5 + dn[1] * 0.8),
            (he[0] + dn[0] * (0.6 + jaw * 1.2), he[1] + dn[1] * (0.6 + jaw * 1.2)), 1.2, 1.1, HC['mouth'])
        cap(L, j0, j1, 1.5, 1.3, HC['muz'])
    # blaze
    b0 = (hs[0] + hd[0] * 0.8 + up[0] * 1.3, hs[1] + hd[1] * 0.8 + up[1] * 1.3)
    b1 = (he[0] + up[0] * 0.6 - hd[0] * 0.6, he[1] + up[1] * 0.6 - hd[1] * 0.6)
    cap(L, b0, b1, 0.55, 0.75, HC['white'])
    # nostril
    dot(L, (he[0] - hd[0] * 0.6 + up[0] * 0.2, he[1] - hd[1] * 0.6 + up[1] * 0.2), HC['eye'], 0.35)
    # eye
    ec = (hs[0] + hd[0] * 2.0 + up[0] * 1.0, hs[1] + hd[1] * 2.0 + up[1] * 1.0)
    ell(L, ec, 0.8, 0.8, HC['eye'])
    if L.cam.sc > 1.5:
        dot(L, (ec[0] + 0.25, ec[1] - 0.25), (250, 250, 250), 0.2)
        lid = P['lid']
        if lid > 0:
            cap(L, (ec[0] - 1.0, ec[1] - 1.05 + lid * 0.9), (ec[0] + 1.0, ec[1] - 1.05 + lid * 0.9), 0.55, 0.55, HC['sh'])
            cap(L, (ec[0] - 1.0, ec[1] - 0.55 + lid * 0.9), (ec[0] + 1.0, ec[1] - 0.55 + lid * 0.9), 0.18, 0.18, HC['ol'])
    # mane strands
    ndir = (math.cos(P['neck']), math.sin(P['neck']))
    nbk = (math.sin(P['neck']), -math.cos(P['neck']))
    for k in range(6):
        s0 = (nb[0] + ndir[0] * (k * 2.1 + 0.2) + nbk[0] * (4.4 - k * 0.3), nb[1] + ndir[1] * (k * 2.1 + 0.2) + nbk[1] * (4.4 - k * 0.3))
        flow = (lerp(0.3, -4.2, w) , lerp(3.2, 0.2, w) + 0.8 * w * math.sin(2 * math.pi * 2 * p_gallop - k))
        s1 = (s0[0] + flow[0], s0[1] + flow[1])
        cap(L, T(*s0), T(*s1), 1.9, 0.7, HC['mane'])
        if k % 2 == 0: cap(L, T(*s0), T(*s1), 0.5, 0.3, HC['maneh'])
    # forelock
    fl0 = (hs[0] + up[0] * 2.2, hs[1] + up[1] * 2.2)
    cap(L, fl0, (fl0[0] + hd[0] * 2.2 + dn[0] * 0.8, fl0[1] + hd[1] * 2.2 + dn[1] * 0.8), 1.1, 0.5, HC['mane'])
    # saddle + blanket
    if saddle:
        ell(L, T(-1, -5.2), 5.4, 2.3, HC['blanket'], P['pitch'], hi=HC['blanket_h'])
        ell(L, T(-1, -6.6), 4.4, 1.9, HC['saddle'], P['pitch'], hi=HC['saddle_h'])
        cap(L, T(3.2, -8.6), T(3.2, -7), 0.8, 0.8, HC['saddle'])
        cap(L, T(0, -5), T(0.6, 1.5), 0.35, 0.35, HC['saddle'])
    # near legs
    draw_leg(L, T, (-10, 2), *legs[2], 8, 7.5, 3.8, 1.9, 1.3, HC['body'], HC['sh'], True)
    draw_leg(L, T, (10, 3), *legs[3], 7, 7.5, 2.8, 1.6, 1.25, HC['body'], HC['sh'], False)
    return T, hs, hd, up


def draw_ears(L, hs, hd, up, ear):
    for side, off in ((0, -0.6), (1, 0.4)):
        base = (hs[0] + up[0] * 2.4 - hd[0] * (0.2 - off), hs[1] + up[1] * 2.4 - hd[1] * (0.2 - off))
        e = ear + side * 0.15
        tip = (base[0] + 3.3 * (up[0] * math.cos(e) - hd[0] * math.sin(e)), base[1] + 3.3 * (up[1] * math.cos(e) - hd[1] * math.sin(e)))
        cap(L, base, tip, 1.25, 0.35, HC['body'] if side else HC['far'])
        if side: cap(L, base, ((base[0] + tip[0]) / 2, (base[1] + tip[1]) / 2), 0.5, 0.3, HC['sh'])

# ---------------------------------------------------------------- cowboy
CC = dict(skin=(236, 186, 144), skin_sh=(200, 146, 108), shirt=(198, 66, 50), shirt_h=(228, 100, 74), shirt_sh=(150, 46, 38),
          vest=(98, 64, 42), jeans=(66, 92, 152), jeans_sh=(48, 66, 114), boot=(80, 50, 34), hat=(196, 154, 96), hat_h=(226, 190, 128),
          band=(92, 56, 34), bandana=(44, 122, 186), ol=(30, 20, 16), mst=(96, 60, 36), far=(0, 0, 0))


def hat(L, c, rot):
    u = (math.sin(rot), -math.cos(rot)); f = (math.cos(rot), math.sin(rot))
    def P_(a, b): return (c[0] + f[0] * a + u[0] * b, c[1] + f[1] * a + u[1] * b)
    cap(L, P_(-4.6, 0), P_(4.9, 0), 0.8, 0.8, CC['hat'], hi=CC['hat_h'])
    ell(L, P_(0.2, 1.9), 2.9, 2.1, CC['hat'], rot, hi=CC['hat_h'])
    cap(L, P_(-2.5, 0.9), P_(2.8, 0.9), 0.5, 0.5, CC['band'])


def cowboy(L, hip, rot, pose, hat_on=True, mouth=0.0):
    u = (math.sin(rot), -math.cos(rot)); f = (math.cos(rot), math.sin(rot))
    def P_(a, b): return (hip[0] + f[0] * a + u[0] * b, hip[1] + f[1] * a + u[1] * b)
    def D(th): return (-u[0] * math.cos(th) + f[0] * math.sin(th), -u[1] * math.cos(th) + f[1] * math.sin(th))
    def limb(o, th1, th2, l1, l2, r1, r2, col, sh, endc, endlen, endr):
        d1 = D(th1); k = (o[0] + d1[0] * l1, o[1] + d1[1] * l1)
        d2 = D(th2); e = (k[0] + d2[0] * l2, k[1] + d2[1] * l2)
        cap(L, o, k, r1, r1 * 0.9, col, sh=sh)
        cap(L, k, e, r2, r2 * 0.9, col, sh=sh)
        if endc is not None:
            fe = D(th2 + 1.4) if endlen > 1.2 else d2
            cap(L, e, (e[0] + fe[0] * endlen, e[1] + fe[1] * endlen), endr, endr, endc)
    sh_ = P_(0.4, 6.0); hp = P_(0, 0.3)
    # far limbs
    limb(sh_, *pose['farm'], 3.4, 3.2, 1.0, 0.9, CC['shirt_sh'], None, CC['skin_sh'], 0.8, 0.9)
    limb(hp, *pose['fleg'], 4.4, 4.4, 1.5, 1.2, CC['jeans_sh'], None, CC['boot'], 1.8, 1.0)
    # torso
    cap(L, P_(0, 0), P_(0.3, 6.4), 2.3, 2.5, CC['shirt'], hi=CC['shirt_h'], sh=CC['shirt_sh'])
    cap(L, P_(-1.1, 0.8), P_(-0.9, 5.8), 1.2, 1.3, CC['vest'])
    cap(L, P_(-0.4, 0.2), P_(0.6, 0.2), 1.1, 1.1, CC['band'])
    ell(L, P_(0.5, 7.3), 1.6, 1.1, CC['bandana'], rot)
    # head
    hc = P_(0.6, 9.7)
    ell(L, hc, 2.6, 2.6, CC['skin'], rot, sh=CC['skin_sh'])
    cap(L, P_(2.6, 9.6), P_(3.3, 9.3), 0.7, 0.6, CC['skin'])
    dot(L, P_(1.7, 10.3), CC['ol'], 0.4)
    cap(L, P_(1.4, 8.5), P_(3.1, 8.4), 0.55, 0.45, CC['mst'])
    if mouth > 0.25:
        dot(L, P_(2.1, 7.7), (90, 20, 20), 0.45 + 0.3 * mouth)
    cap(L, P_(-1.6, 10.8), P_(-1.9, 8.6), 0.9, 0.7, CC['mst'])  # hair back
    if hat_on:
        hat(L, P_(0.5, 11.9), rot)
    # near limbs
    limb(hp, *pose['nleg'], 4.4, 4.4, 1.6, 1.3, CC['jeans'], CC['jeans_sh'], CC['boot'], 1.8, 1.05)
    limb(sh_, *pose['narm'], 3.4, 3.2, 1.05, 0.95, CC['shirt'], CC['shirt_sh'], CC['skin'], 0.8, 0.95)
    return P_(0.5, 11.9)


def pose_ride(t):
    pump = math.sin(t * 7)
    return dict(nleg=(1.35, 0.15), fleg=(1.3, 0.2), narm=(0.9, 1.7), farm=(2.7 + 0.2 * pump, 3.0 + 0.15 * pump))


def pose_fly(t):
    return dict(nleg=(0.8 + 0.6 * math.sin(t * 22), 0.3), fleg=(-0.5 + 0.6 * math.sin(t * 22 + 2), -0.2),
                narm=(2.5 + 0.7 * math.sin(t * 25), 2.9 + 0.8 * math.sin(t * 25 + 1)), farm=(2.2 + 0.7 * math.sin(t * 25 + 2), 2.6 + 0.6 * math.sin(t * 25 + 3)))


def pose_sit(t, shock):
    return dict(nleg=(1.55, 0.35 + 0.15 * math.sin(t * 3)), fleg=(1.3, 0.2),
                narm=(lerp(0.35, 2.5, shock), lerp(0.2, 2.9, shock)), farm=(lerp(-0.3, 2.3, shock), lerp(-0.2, 2.6, shock)))

# ---------------------------------------------------------------- props
def cactus(L, cx, base, wob):
    g, gh, gs = (86, 150, 72), (124, 188, 96), (58, 112, 52)
    def X(yup): return cx + wob * (yup / 24.0) ** 1.5
    cap(L, (cx, base), (X(24), base - 24), 3.4, 3.1, g, hi=None)
    cap(L, (cx - 1.4, base - 1), (X(23) - 1.4, base - 23), 0.7, 0.7, gh)
    cap(L, (cx + 1.6, base - 1), (X(23) + 1.6, base - 23), 0.6, 0.6, gs)
    cap(L, (X(11) - 2, base - 11), (X(11) - 6.5, base - 11), 1.8, 1.8, g)
    cap(L, (X(11) - 6.5, base - 11), (X(18) - 6.5, base - 18), 1.8, 1.7, g)
    cap(L, (X(12) - 7.2, base - 12), (X(18) - 7.2, base - 18), 0.5, 0.5, gh)
    cap(L, (X(8) + 2, base - 8), (X(8) + 6, base - 8), 1.7, 1.7, g)
    cap(L, (X(8) + 6, base - 8), (X(15) + 6, base - 15), 1.7, 1.6, g)
    cap(L, (X(9) + 6.8, base - 9), (X(15) + 6.8, base - 15), 0.5, 0.5, gs)
    for (dx, dy) in ((-3.8, 5), (3.6, 10), (-3.6, 16), (3.7, 20), (-8.6, 14), (8.1, 12), (-0.5, 25.5), (2.6, 24.7)):
        dot(L, (X(dy) + dx, base - dy), (244, 240, 210), 0.4)
    ell(L, (X(25) + 0.5, base - 25.8), 1.4, 0.9, (236, 110, 150))


def carrot(L, x, y, frac):
    if frac <= 0.02: return
    ln = 7 * frac
    cap(L, (x, y), (x + ln, y - 0.4), 1.8, 0.6, (236, 128, 40), hi=(255, 176, 90))
    for a in (-0.5, 0.0, 0.5):
        cap(L, (x - 0.6, y - 0.3), (x - 3.2 * math.cos(a), y - 1.2 - 2.4 * math.sin(a + 0.8)), 0.6, 0.3, (84, 160, 60))


def tumbleweed(L, c, ang):
    for i in range(14):
        a = ang + i * 2 * math.pi / 14
        a2 = a + 2.2
        cap(L, (c[0] + 3.4 * math.cos(a), c[1] + 3.4 * math.sin(a)), (c[0] + 3.4 * math.cos(a2), c[1] + 3.4 * math.sin(a2)), 0.35, 0.35, (160, 118, 66))


def star(L, c, col=(255, 230, 90)):
    dot(L, c, col, 0.45)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        dot(L, (c[0] + dx, c[1] + dy), col, 0.3)


def bubble(F, x, y, k):
    x, y = int(x), int(y)
    if k <= 0: return
    w, h = 5, 8
    x0, y0 = x - w // 2, y - h
    if x0 < 1 or y0 < 1: return
    F[y0 - 1:y0 + h + 1, x0:x0 + w] = (40, 24, 18)
    F[y0:y0 + h, x0 - 1:x0 + w + 1] = (40, 24, 18)
    F[y0:y0 + h, x0:x0 + w] = (250, 248, 240)
    F[y0 + 1:y0 + 5, x0 + 2] = (214, 40, 40)
    F[y0 + 6, x0 + 2] = (214, 40, 40)
    F[y0 + h, x0 + 1] = (40, 24, 18); F[y0 + h + 1, x0 + 1] = (40, 24, 18)

# ---------------------------------------------------------------- particles
rng = np.random.default_rng(7)
PART = []
t_ = 0.0
while t_ < T_BRAKE:
    PART.append(dict(b=t_, x=-9 + rng.uniform(-3, 3), y=GROUND - 1, vx=-V + rng.uniform(4, 10), vy=rng.uniform(-8, -3), life=0.45, r0=0.8, r1=2.6, rel=True))
    t_ += 0.11
t_ = T_BRAKE
while t_ < T_STOP:
    PART.append(dict(b=t_, x=13 + rng.uniform(-2, 3), y=GROUND - 1, vx=rng.uniform(8, 34), vy=rng.uniform(-20, -6), life=0.8, r0=1.2, r1=4.0, rel=True))
    t_ += 0.025
for i in range(12):
    a = rng.uniform(0, math.pi)
    PART.append(dict(b=T_LAND, x=CACTUS_WX - CAMX_STOP, y=GROUND - 22, vx=26 * math.cos(a) * rng.uniform(.4, 1), vy=-26 * math.sin(a) * rng.uniform(.4, 1), life=0.5, r0=1.4, r1=2.8, rel=False))


def draw_particles(F, t, cam_sx):
    L = Layer(Cam(0, 0))
    for p in PART:
        a = t - p['b']
        if a < 0 or a > p['life']: continue
        k = a / p['life']
        x0 = HORSE_SX + p['x'] if p['rel'] else p['x']
        x = x0 + p['vx'] * a + cam_sx
        y = p['y'] + p['vy'] * a + 12 * a * a
        r = lerp(p['r0'], p['r1'], k)
        ell(L, (x, y), r, r * 0.8, (238, 218, 180), hi=(250, 238, 212))
        if k > 0.55:
            thin = ((XX.astype(int) + YY.astype(int)) % 2 == 0)
            if k > 0.8: thin = thin | ((XX.astype(int) % 2) == 0)
            L.m &= ~thin | ~L.m
    comp(F, L)

# ---------------------------------------------------------------- captions
FONT = ImageFont.truetype(P.FONT_BOLD, 64)
CAPS = [
    (0.25, 5.95, 'Н-но, родная! Я\u00a0— самый быстрый ковбой на всём Диком Западе!', (255, 222, 96)),
    (6.3, 7.5, 'А-А-А-А-А!', (255, 222, 96)),
    (7.9, 9.95, 'Ой-й... кактус...', (255, 222, 96)),
    (10.9, 12.5, 'Самый быстрый тут\u00a0—\u00a0я.', (255, 255, 255)),
    (13.05, 16.0, 'А ты просто сверху сидел.', (255, 255, 255)),
]


def make_caption(text, color):
    img = Image.new('RGBA', (1080, 420), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    words = text.split(); lines = []; cur = ''
    for w in words:
        tst = (cur + ' ' + w).strip()
        if d.textlength(tst, font=FONT) > 1000 and cur:
            lines.append(cur); cur = w
        else:
            cur = tst
    lines.append(cur)
    y = 20
    for ln in lines:
        tw = d.textlength(ln, font=FONT)
        d.text(((1080 - tw) / 2, y), ln, font=FONT, fill=color + (255,), stroke_width=8, stroke_fill=(20, 12, 10, 255))
        y += 86
    return np.array(img)
CAP_IMG = [make_caption(c[2], c[3]) for c in CAPS]
CAP_Y = 250

# ---------------------------------------------------------------- frame
def horse_pose_at(t):
    p = (t * 2.3) % 1.0
    if t < T_BRAKE:
        P = gallop_pose(p, t)
        if t > 5.8: P['ear'] = lerp(0.7, -0.3, sm((t - 5.8) / 0.15))
    elif t < T_STOP:
        P = blend(gallop_pose(p, t), brake_pose(t), sm((t - T_BRAKE) / 0.2))
    elif t < 7.25:
        P = blend(brake_pose(t), stand_pose(t), sm((t - T_STOP) / 0.45))
    else:
        P = stand_pose(t)
        if T_EAT0 <= t < T_CLOSE:
            k_dn = sm((t - T_EAT0) / 0.35) * (1 - sm((t - 10.0) / 0.35))
            P['neck'] = lerp(-0.95, 0.62, k_dn)
            P['head'] = lerp(0.78, 1.45, k_dn)
            if 8.75 < t < 10.1:
                P['jaw'] = 0.5 * (1 + math.sin(2 * math.pi * 4.5 * t)) * 0.6
        if t >= T_CLOSE:
            P['lid'] = 0.55
            P['ear'] = 0.15
            ha = horse_amp(t)
            chew = 0.0
            if t > 12.4 and t < 13.0: chew = 0.25 * (1 + math.sin(2 * math.pi * 3 * t))
            P['jaw'] = max(min(ha * 1.6, 1.0) * 0.8, chew)
            # slow blink
            if 14.9 < t < 15.05: P['lid'] = 1.0
    return P, p


def render(t):
    close = t >= T_CLOSE
    camx = cam_x(t)
    if t >= T_LAND and t < T_LAND + 0.3:
        shake = (int(hsh(int(t * 60)) % 5) - 2, int(hsh(int(t * 60) + 7) % 3) - 1)
    else:
        shake = (0, 0)
    bg = background(camx, t)
    if close:
        ox, oy = 20, 62
        bg = np.repeat(np.repeat(bg[oy:oy + 96, ox:ox + 54], 2, 0), 2, 1)
        cam = Cam(CAMX_STOP + ox, oy, 2.0)
    else:
        cam = Cam(camx - shake[0], -shake[1], 1.0)
    F = bg
    hx = camx + HORSE_SX
    hy = GROUND - 19
    P, p = horse_pose_at(t)

    # props behind horse
    L = Layer(cam)
    wob = 0.0
    if t >= T_LAND: wob = 3.0 * math.exp(-(t - T_LAND) * 3) * math.sin((t - T_LAND) * 18)
    cactus(L, CACTUS_WX, GROUND + 2, wob)
    outline(L, (40, 72, 36)); comp(F, L)

    L = Layer(cam)
    frac = 1.0
    if t > 8.75: frac = 1 - sm((t - 8.75) / 1.25)
    carrot(L, CARROT_WX, GROUND - 0.5, frac)
    outline(L, (70, 40, 20)); comp(F, L)

    # tumbleweed
    if 0.6 < t < 4.2 and not close:
        L = Layer(Cam(0, 0))
        tx = 122 - (t - 0.6) * 48
        ty = GROUND - 3.5 - abs(math.sin((t - 0.6) * 5)) * 7
        tumbleweed(L, (tx, ty), -(t * 9))
        comp(F, L)

    # horse
    L = Layer(cam)
    T, hs, hd, up = draw_horse(L, hx, hy, P, t, p, saddle=True)
    hat_on_horse = t >= T_HAT
    if hat_on_horse:
        pos, rot = head_hat_anchor(hx, hy, P)
        hat(L, pos, rot)
    draw_ears(L, hs, hd, up, P['ear'])
    outline(L, HC['ol']); comp(F, L)

    # cowboy
    L = Layer(cam)
    mouth = amp('c1', t - 0.2) if t < 6.0 else (1.0 if 6.3 < t < 7.5 else 0.0)
    hatL = None
    if t < T_LAUNCH:
        hip = T(-1, -8.4)
        lean = 0.12 + 0.05 * math.sin(2 * math.pi * p + 1)
        if t > T_BRAKE: lean = lerp(lean, 0.6, sm((t - T_BRAKE) / 0.25))
        rot = P['pitch'] + lean
        cowboy(L, hip, rot, pose_ride(t), True, mouth)
    else:
        # launch point
        P0, _ = horse_pose_at(T_LAUNCH - 1e-3)
        T0 = horse_frames(cam_x(T_LAUNCH) + HORSE_SX, hy, P0)[0]
        L0 = T0(-1, -8.4)
        target = (CACTUS_WX + 0.3, GROUND + 2 - 25.2)
        if t < T_LAND:
            s = (t - T_LAUNCH) / (T_LAND - T_LAUNCH)
            hip = (lerp(L0[0], target[0], s), lerp(L0[1], target[1], s) - 44 * 4 * s * (1 - s))
            rot = lerp(0.6, 2 * math.pi, s)
            cowboy(L, hip, rot, pose_fly(t), False, mouth)
        else:
            a = t - T_LAND
            bounce = -3.5 * math.exp(-a * 5) * abs(math.sin(a * 14))
            hip = (target[0] + wob * 0.9, target[1] + bounce)
            shock = 1 - sm((a - 0.6) / 0.8)
            cowboy(L, hip, 0.0, pose_sit(t, shock), False, 0.0)
            # spines stuck
            for dx, dy in ((-1.2, 0.2), (1.0, -0.4), (0.2, 0.6)):
                dot(L, (hip[0] + dx, hip[1] + dy + 1.5), (250, 246, 220), 0.3)
        # flying hat
        if t < T_HAT:
            Pl, _ = horse_pose_at(T_HAT)
            tgt, trot = head_hat_anchor(HORSE_WX, hy, Pl)
            h0 = (L0[0] + 1, L0[1] - 12)
            s = (t - T_LAUNCH) / (T_HAT - T_LAUNCH)
            hp_ = (lerp(h0[0], tgt[0], s), lerp(h0[1], tgt[1], s) - 58 * 4 * s * (1 - s))
            hatL = (hp_, lerp(0.0, trot + 4 * math.pi, s))
    outline(L, CC['ol']); comp(F, L)
    if hatL:
        L = Layer(cam); hat(L, *hatL); outline(L, CC['ol']); comp(F, L)

    # stars around dazed cowboy
    if T_LAND + 0.1 < t < 9.9 and not close:
        L = Layer(cam)
        cx_, cy_ = CACTUS_WX + 0.9, GROUND + 2 - 25.2 - 13
        for i in range(3):
            a = t * 5 + i * 2 * math.pi / 3
            star(L, (cx_ + 5 * math.cos(a), cy_ + 1.6 * math.sin(a)))
        comp(F, L)

    if not close:
        draw_particles(F, t, 0)
        if 5.8 <= t < 6.35:
            k = sm((t - 5.8) / 0.08)
            hx_s, hy_s = cam.p(*hs)
            bubble(F, hx_s + 3, hy_s - 5, k)

    # upscale + captions
    big = np.repeat(np.repeat(F, S, 0), S, 1)
    for (a, b, _, _), img in zip(CAPS, CAP_IMG):
        if a <= t < b:
            k = min(1.0, (t - a) / 0.08)
            y0 = CAP_Y
            region = big[y0:y0 + img.shape[0]]
            al = img[..., 3:4].astype(np.float32) / 255 * k
            region[:] = (region * (1 - al) + img[..., :3] * al).astype(np.uint8)
    # tiny vignette-free letterbox line at bottom for polish
    return big


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        for tt in map(float, sys.argv[2:]):
            Image.fromarray(render(tt)).resize((360, 640), Image.NEAREST).save(P.build('scene', f'test_{tt:05.2f}.png'))
        sys.exit()
    n = int(DUR * FPS)
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', str(FPS),
                             '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p',
                             P.build('scene', 'video_noaudio.mp4')], stdin=subprocess.PIPE)
    for i in range(n):
        proc.stdin.write(render(i / FPS).tobytes())
        if i % 60 == 0: print(i, flush=True)
    proc.stdin.close(); proc.wait()
    print('done')
