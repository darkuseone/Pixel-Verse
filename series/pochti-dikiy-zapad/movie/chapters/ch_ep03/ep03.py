"""S01E03 «Информатор». Saloon world (engine/props/saloon.py) + code-drawn heroes, fast cutting.
  python3 ep03.py test 1 5 20      -> build/ep03/sheet.png
  python3 ep03.py seg A B          -> build/ep03/seg_AAAA.mp4 (frames A..B-1)
  python3 ep03.py all              -> build/ep03/noaudio.mp4 (4 parallel segments)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[5] / 'engine'))
import paths as P
import math, subprocess, os
import numpy as np
from PIL import Image
import stage as ST                                  # sets the (wide) logical canvas
import widecam as WC
import scene as S
from scene import Layer, cap, dot, ell as _ell0, outline, sm, lerp, clamp01
import overlays as O
from props import saloon as SAL
from timeline import DUR, FPS, VOICE

EP = 'ep03'
W, H, UP = ST.W, ST.H, ST.UP
OUT_W, OUT_H = W * UP, H * UP
S.W, S.H = W, H
S.YY, S.XX = [a.astype(np.float32) + 0.5 for a in np.mgrid[0:H, 0:W]]
WORLD, BT, OUTSIDE = SAL.build()
WW, WH = WORLD.shape[1], WORLD.shape[0]


# ---------------------------------------------------------------- camera
class ACam:
    def __init__(s, ax, ay, sx, sy, sc, flip=False): s.ax, s.ay, s.sx, s.sy, s.sc, s.flip = ax, ay, sx, sy, sc, flip
    def p(s, x, y):
        X = (x - s.ax) * s.sc
        return (s.sx + (-X if s.flip else X), s.sy + (y - s.ay) * s.sc)

def ell(L, cxy, rx, ry, c, ang=0.0, **kw):
    if getattr(L.cam, 'flip', False): ang = -ang
    return _ell0(L, cxy, rx, ry, c, ang, **kw)
S.ell = ell


class View:
    """world px -> logical screen px (16:9). Authored for a 360x640 window: View(X0,Y0,Z) = vertical world top-left, converted to wide
    around the same world centre; View.raw = already-wide top-left."""
    def __init__(s, X0, Y0, Z, oy=0, raw=False):
        if not raw:
            cx, cy = X0 + 180 / Z, Y0 + 320 / Z
            Z = max(Z * WC.kz(Z), max(W / WW, H / WH))
            X0, Y0 = cx - W / 2 / Z, cy - H / 2 / Z
        s.Z = Z
        s.X0 = min(max(X0, 0.0), WW - W / Z); s.Y0 = min(max(Y0, 0.0), WH - H / Z); s.oy = oy
    @classmethod
    def raw(cls, X0, Y0, Z): return cls(X0, Y0, Z, raw=True)
    def cam(s, wx, wy, unit, flip=False):
        return ACam(1000.0, 1000.0, (wx - s.X0) * s.Z, (wy - s.Y0) * s.Z + s.oy, unit * s.Z, flip)
    def pt(s, wx, wy): return ((wx - s.X0) * s.Z, (wy - s.Y0) * s.Z + s.oy)

def view_at(wx, wy, Z, sx=180, sy=400, half=None):
    """subject (wx,wy) centred horizontally (or in the left/right half of the wide frame: half=0/1)"""
    Zw = max(Z * WC.kz(Z), max(W / WW, H / WH))
    cx = W / 2 if half is None else W * (0.25 + 0.5 * half)
    return View.raw(wx - cx / Zw, wy - WC.SUBJ_Y / Zw, Zw)


def bg(v):
    xs = (v.X0 + (np.arange(OUT_W) + 0.5) / (UP * v.Z)).astype(np.int32).clip(0, WW - 1)
    ys = (v.Y0 + (np.arange(OUT_H) + 0.5 - v.oy * UP) / (UP * v.Z)).astype(np.int32).clip(0, WH - 1)
    return WORLD[ys[:, None], xs[None, :]], xs, ys


def blit_world(big, xs, ys, spr, x_left, y_top):
    sx = xs - x_left; sy = ys - y_top
    okx = (sx >= 0) & (sx < spr.shape[1]); oky = (sy >= 0) & (sy < spr.shape[0])
    if not okx.any() or not oky.any(): return
    cx = np.nonzero(okx)[0]; cy = np.nonzero(oky)[0]
    sub = spr[sy[cy][:, None], sx[cx][None, :]]
    m = sub[..., 3] > 0
    reg = big[cy[0]:cy[-1] + 1, cx[0]:cx[-1] + 1]
    reg[m] = sub[..., :3][m]


# ---------------------------------------------------------------- audio envelopes (lip flap + caption timing)
ENV = {}
for vid, ep, key, t0, a, b, who, txt in VOICE:
    if (ep, key) not in ENV: ENV[(ep, key)] = S.load_env(P.voice_wav(ep, key))

def talk(who, t):
    v = 0.0
    for vid, ep, key, t0, a, b, spk, txt in VOICE:
        if spk == who and t0 <= t < t0 + (b - a):
            e = ENV[(ep, key)]; i = int((a + t - t0) * 100)
            if 0 <= i < len(e): v = max(v, float(e[i]))
    return v

COL = dict(billy=(255, 222, 96), molniya=(255, 255, 255), sam=(214, 170, 255))
_items = []
for vid, ep, key, t0, a, b, who, txt in VOICE:
    wt = O.word_times(ENV[(ep, key)], t0, a, b, txt.split())
    ch = O.chunk_words(wt)
    for i, c in enumerate(ch):
        s0 = c[0][1]; e0 = ch[i + 1][0][1] if i + 1 < len(ch) else max(c[-1][2] + 0.35, t0 + (b - a))
        _items.append((s0, e0, [w[0] for w in c], COL[who]))
CAPTIONS = O.Captions(_items)
CAP_Y = 780


# ---------------------------------------------------------------- characters
CC_BANDIT = dict(hat=(46, 40, 48), hat_h=(76, 68, 80), band=(190, 50, 50), shirt=(96, 70, 128), shirt_h=(124, 96, 158),
                 shirt_sh=(70, 50, 96), vest=(40, 34, 36), jeans=(90, 80, 70), jeans_sh=(66, 58, 50), bandana=(196, 52, 52),
                 mst=(34, 26, 24), skin=(226, 176, 136))

def with_pal(d, pal, fn):
    old = {k: d[k] for k in pal}; d.update(pal)
    try: return fn()
    finally: d.update(old)

def HPf(rot):
    u = (math.sin(rot), -math.cos(rot)); f = (math.cos(rot), math.sin(rot))
    return lambda a, b: (1000.0 + f[0] * a + u[0] * b, 1000.0 + f[1] * a + u[1] * b)

POSES = dict(
    stand=dict(nleg=(0.08, 0.0), fleg=(-0.08, 0.0), narm=(0.15, 0.1), farm=(-0.1, 0.0)),
    shout=dict(nleg=(0.3, 0.0), fleg=(-0.3, 0.0), narm=(2.1, 2.6), farm=(-1.9, -2.4)),
    hips=dict(nleg=(0.25, 0.0), fleg=(-0.25, 0.0), narm=(0.9, -0.6), farm=(-0.6, 0.6)),
    lean=dict(nleg=(0.1, 0.0), fleg=(-0.2, 0.0), narm=(1.0, 1.5), farm=(0.4, 0.4)),
    point=dict(nleg=(0.1, 0.0), fleg=(-0.2, 0.0), narm=(1.55, 1.55), farm=(-0.1, 0.0)),
    heroic=dict(nleg=(0.35, 0.0), fleg=(-0.35, 0.0), narm=(2.7, 2.9), farm=(0.2, -0.3)),
    excited=dict(nleg=(0.1, 0.0), fleg=(-0.1, 0.0), narm=(1.9, 2.6), farm=(1.8, 2.5)),
    sit=dict(nleg=(1.45, 0.25), fleg=(1.35, 0.3), narm=(0.9, 1.9), farm=(0.6, 1.2)),
    sit_menu=dict(nleg=(1.45, 0.25), fleg=(1.35, 0.3), narm=(1.3, 2.4), farm=(1.1, 2.3)),
    sit_give=dict(nleg=(1.45, 0.25), fleg=(1.35, 0.3), narm=(1.45, 1.6), farm=(0.6, 1.2)),
)

def walk_pose(t, speed=9.0, amp=0.45):
    s = math.sin(t * speed)
    return dict(nleg=(amp * s, 0.2 * max(0, -s)), fleg=(-amp * s, 0.2 * max(0, s)), narm=(-amp * 0.9 * s, -0.2), farm=(amp * 0.9 * s, -0.2))

def run_pose(t):
    s = math.sin(t * 16)
    return dict(nleg=(0.9 * s, 0.9 * max(0, -s) + 0.2), fleg=(-0.9 * s, 0.9 * max(0, s) + 0.2),
                narm=(-1.1 * s + 0.3, 1.2), farm=(1.1 * s + 0.3, 1.2))

def blend_pose(a, b, k):
    return {kk: (lerp(a[kk][0], b[kk][0], k), lerp(a[kk][1], b[kk][1], k)) for kk in a}


def draw_billy(CH, cam, pose, rot=0.05, mouth=0.0, expr='normal'):
    L = Layer(cam)
    S.CC['mst'] = (96, 60, 36)
    S.cowboy(L, (1000.0, 1000.0), rot, pose, hat_on=False, mouth=mouth)
    HP = HPf(rot)
    ell(L, HP(0.4, 11.4), 2.9, 1.5, (104, 66, 40), rot, hi=(136, 90, 56))                  # hair (hat is on Molniya)
    for dx in (-1.5, -0.3, 0.9):
        cap(L, HP(dx, 11.9), HP(dx + 0.9, 12.9), 0.55, 0.2, (104, 66, 40))                   # tufts
    big = cam.sc > 9
    if big:                                                                                     # expressive eye
        ew = 0.78 if expr in ('excited', 'shout') else 0.6
        ell(L, HP(1.75, 10.35), ew * 0.85, ew, (250, 250, 244), rot)
        dot(L, HP(1.95, 10.3), (30, 20, 16), 0.32 if expr != 'excited' else 0.26)
        dot(L, HP(2.05, 10.5), (255, 255, 255), 0.1)
        by = {'excited': 11.55, 'shout': 11.5, 'sly': 11.0, 'normal': 11.2}.get(expr, 11.2)
        tilt = -0.35 if expr == 'sly' else 0.15
        cap(L, HP(1.1, by - tilt * 0.3), HP(2.5, by + tilt * 0.3), 0.2, 0.18, (96, 60, 36))
        ell(L, HP(1.2, 9.05), 0.55, 0.4, (236, 150, 130), rot)                                # cheek
    if mouth > 0.25 or expr == 'shout':
        m = max(mouth, 0.5 if expr == 'shout' else 0)
        ell(L, HP(2.2, 7.9), 0.45 + 0.35 * m, 0.25 + 0.55 * m, (90, 24, 24), rot)
    cap(L, HP(1.4, 8.55), HP(3.1, 8.45), 0.55, 0.45, (96, 60, 36))                           # mustache on top
    outline(L, (26, 16, 12)); CH.add(L)


def draw_sam(CH, cam, kind='sit', rot=0.03, mouth=0.0, menu=None, look_cam=False):
    L = Layer(cam)
    pose = POSES['sit_menu'] if menu in ('up', 'peek') else POSES[kind] if kind in POSES else kind
    with_pal(S.CC, CC_BANDIT, lambda: S.cowboy(L, (1000.0, 1000.0), rot, pose, hat_on=True, mouth=mouth))
    HP = HPf(rot)
    cap(L, HP(-1.2, 10.3), HP(2.7, 10.3), 0.78, 0.78, (24, 20, 24))                           # bandit mask
    ex = 1.9 if not look_cam else 1.6
    dot(L, HP(ex, 10.3), (240, 240, 240), 0.32)
    if cam.sc > 9: dot(L, HP(ex + (0.12 if not look_cam else -0.05), 10.3), (20, 14, 14), 0.14)
    cap(L, HP(1.3, 8.45), HP(3.4, 7.25), 0.6, 0.4, (34, 26, 24))                             # crooked mustache
    if mouth > 0.25: ell(L, HP(2.1, 7.7), 0.35 + 0.3 * mouth, 0.2 + 0.45 * mouth, (90, 24, 24), rot)
    if menu in ('up', 'peek'):
        dy = 0.0 if menu == 'up' else -1.6
        c0 = HP(3.3, 9.9 + dy)
        cap(L, HP(3.3, 12.2 + dy), HP(3.3, 7.4 + dy), 2.0, 2.0, (70, 42, 26))                    # menu card (wood frame)
        cap(L, HP(3.3, 12.0 + dy), HP(3.3, 7.6 + dy), 1.7, 1.7, (236, 222, 180))
        cap(L, HP(2.3, 11.6 + dy), HP(4.3, 11.6 + dy), 0.3, 0.3, (130, 34, 26))
        for k in range(3): cap(L, HP(2.3, 10.5 + dy - k * 0.9), HP(4.3, 10.5 + dy - k * 0.9), 0.14, 0.14, (120, 100, 80))
        dot(L, HP(4.4, 10.4 + dy), CC_BANDIT['skin'], 0.5)                                   # fingers
    outline(L, (20, 14, 14)); CH.add(L)
    return HP


def molniya_pose(t, chew=False, jaw_talk=0.0):
    Pz = S.stand_pose(t)
    Pz.update(lid=0.55, ear=0.3 + 0.08 * math.sin(t * 1.1), neck=-0.95, head=0.78)
    c = 0.2 * (1 + math.sin(2 * math.pi * 2.3 * t)) if chew else 0.0
    Pz['jaw'] = max(c, min(jaw_talk * 1.6, 1.0) * 0.8)
    return Pz


def draw_molniya(CH, cam, t, carrot=False, chew=False):
    L = Layer(cam)
    Pz = molniya_pose(t, chew, talk('molniya', t))
    T, hs, hd_, up = S.draw_horse(L, 1000.0, 1000.0, Pz, t, 0.0, saddle=True)
    pos, rot = S.head_hat_anchor(1000.0, 1000.0, Pz); S.hat(L, pos, rot)
    if carrot:
        he = (hs[0] + hd_[0] * 8.5, hs[1] + hd_[1] * 8.5); dn = (-hd_[1], hd_[0])
        c0 = (he[0] + dn[0] * 1.4 - hd_[0] * 0.6, he[1] + dn[1] * 1.4 - hd_[1] * 0.6)
        cap(L, c0, (c0[0] + 4.2, c0[1] + 0.9), 1.1, 0.4, (236, 128, 40), hi=(255, 176, 90))
        for a in (-0.5, 0.0, 0.5): cap(L, c0, (c0[0] - 1.8, c0[1] - 1.1 - a), 0.4, 0.22, (84, 160, 60))
    S.draw_ears(L, hs, hd_, up, Pz['ear'])
    if cam.sc > 9:                                                                               # big deadpan eye
        ec = (hs[0] + hd_[0] * 2.0 + up[0] * 1.0, hs[1] + hd_[1] * 2.0 + up[1] * 1.0)
        ell(L, ec, 0.95, 0.95, (30, 18, 14)); ell(L, (ec[0] - 0.15, ec[1] + 0.2), 0.55, 0.55, (70, 44, 30))
        dot(L, (ec[0] - 0.35, ec[1] + 0.3), (255, 255, 255), 0.15)
        ell(L, (ec[0], ec[1] - 0.35), 1.15, 0.75, S.HC['body'])
        cap(L, (ec[0] - 1.05, ec[1] - 0.1), (ec[0] + 1.05, ec[1] - 0.1), 0.12, 0.12, (40, 22, 14))
    outline(L, S.HC['ol']); CH.add(L)
    return hs, hd_


class Chars:
    """logical-resolution character canvas"""
    def __init__(s):
        s.col = np.zeros((H, W, 3), np.uint8); s.m = np.zeros((H, W), bool)
    def add(s, L):
        s.col[L.m] = L.col[L.m]; s.m |= L.m
    def clip_rows(s, y0, y1):
        s.m[:y0] = False; s.m[y1:] = False
    def comp(s, big):
        m = np.repeat(np.repeat(s.m, UP, 0), UP, 1)
        c = np.repeat(np.repeat(s.col, UP, 0), UP, 1)
        big[m] = c[m]


def wrect(L, x0, y0, x1, y1, c):
    ax, ay = L.cam.p(x0, y0); bx, by = L.cam.p(x1, y1)
    xa, xb = sorted((ax, bx)); ya, yb = sorted((ay, by))
    w = S.win(xa, xb, ya, yb)
    if w is None: return
    X = S.XX[w]; Y = S.YY[w]
    L.set(w, (X >= xa) & (X < xb) & (Y >= ya) & (Y < yb), c)


# ---------------------------------------------------------------- world layout
DOOR = (28, 112, 372, 452)          # doorway x0,x1 and batwing panel y0,y1
TABLE = (640, 548, 58, 12)          # centre x, top y, rx, ry
SAM_HIP = (586, 560)
MOL = (745, 612)                    # Molniya (body x, feet y)
BILLY_TABLE = (494, 612)
U_SAM, U_BILLY, U_MOL = 8.0, 8.0, 5.2

def mol_cam(v): return v.cam(MOL[0], MOL[1] - 19 * U_MOL, U_MOL, flip=True)

def mol_head_world(t):
    Pz = molniya_pose(t)
    hs = S.horse_frames(1000.0, 1000.0, Pz)[3]
    return MOL[0] - (hs[0] - 1000.0) * U_MOL, MOL[1] - 19 * U_MOL + (hs[1] - 1000.0) * U_MOL

def draw_doors(CH, v, ang):
    L = Layer(v.cam(0, 0, 1.0)); L.cam.ax = 0; L.cam.ay = 0
    x0, x1, y0, y1 = DOOR; half = (x1 - x0) / 2
    for side in (0, 1):
        w = half * max(0.12, math.cos(ang))
        if side == 0: a, b = x0, x0 + w
        else: a, b = x1 - w, x1
        wrect(L, a, y0, b, y1, (150, 100, 58))
        wrect(L, a, y0, b, y0 + 4, (190, 134, 80)); wrect(L, a, y1 - 4, b, y1, (96, 60, 34))
        n = 5
        for i in range(1, n):
            xx = lerp(a, b, i / n); wrect(L, xx, y0 + 6, xx + max(1.0, w / 30), y1 - 6, (104, 66, 38))
        yy = y0 + 18 + (6 if side else 0)
        cy = (y0 + y1) / 2
        wrect(L, a + (b - a) * 0.2, cy - 2, a + (b - a) * 0.8, cy + 2, (104, 66, 38))
    outline(L, (40, 24, 14)); CH.add(L)

def door_angle(t):
    if t < 0.25: return lerp(0.0, 1.35, sm(t / 0.25))
    if t < 2.5: return 1.35 * math.exp(-(t - 0.25) * 1.6) * math.cos((t - 0.25) * 7) if t > 0.6 else 1.35
    if 36.2 <= t < 45.0:
        u = t - 36.35
        if u < 0: return 0.0
        return 1.3 * math.exp(-u * 0.55) * abs(math.cos(u * 3.2))
    return 0.0

def draw_table(CH, v, t, coin=None, sack=True, carrots=2, paper=True):
    cx, ty, rx, ry = TABLE
    L = Layer(v.cam(0, 0, 1.0)); L.cam.ax = 0; L.cam.ay = 0
    for lx in (cx - rx * 0.7, cx + rx * 0.7):
        wrect(L, lx - 3, ty, lx + 3, 606, (84, 52, 30))
    wrect(L, cx - rx, ty, cx + rx, ty + 12, (120, 76, 42))
    wrect(L, cx - rx, ty + 10, cx + rx, ty + 12, (70, 44, 26))
    ell(L, (cx, ty), rx, ry, (156, 104, 60), hi=(186, 132, 80), hit=0.3)
    outline(L, (40, 24, 14)); CH.add(L)
    L = Layer(v.cam(0, 0, 1.0)); L.cam.ax = 0; L.cam.ay = 0
    if paper:
        ell(L, (cx - 12, ty - 1), 14, 5, (240, 228, 196)); cap(L, (cx - 22, ty - 2), (cx - 4, ty - 3), 0.8, 0.8, (120, 100, 80))
        cap(L, (cx - 20, ty + 1), (cx - 8, ty), 0.6, 0.6, (120, 100, 80))
    if sack:
        ell(L, (cx + 28, ty - 10), 13, 12, (216, 188, 128), hi=(238, 214, 160), sh=(186, 158, 104))
        cap(L, (cx + 28, ty - 22), (cx + 28, ty - 27), 3.5, 5, (216, 188, 128)); cap(L, (cx + 23, ty - 21), (cx + 33, ty - 21), 1.4, 1.4, (140, 100, 60))
    for k in range(carrots):
        x = cx + 8 + k * 7; y = ty + 2 - k
        cap(L, (x, y), (x + 14, y - 3), 3.2, 1.0, (236, 128, 40), hi=(255, 176, 90))
        for a in (-0.5, 0.0, 0.5): cap(L, (x, y), (x - 5 * math.cos(a), y - 5 * math.sin(a) - 2), 1.1, 0.6, (84, 160, 60))
    if coin is not None:
        x, y, spin = coin
        ell(L, (x, y), 4.5 * max(0.25, abs(math.cos(spin))), 2.4, (240, 196, 70), hi=(255, 236, 150))
    outline(L, (40, 24, 14)); CH.add(L)
    if sack:
        sx, sy = v.pt(cx + 28, ty - 9)
        if v.Z >= 2: px_small(CH, '$', sx, sy, 8 if v.Z < 3 else 16, (90, 60, 30))

def px_small(CH, txt, cx, cy, size, col):
    f = O.pfont(size); bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    img = Image.new('L', (tw + 4, th + 4), 0); from PIL import ImageDraw
    d = ImageDraw.Draw(img); d.fontmode = '1'; d.text((2 - bb[0], 2 - bb[1]), txt, font=f, fill=255)
    m = np.array(img) > 127; ys, xs = np.nonzero(m)
    yy = ys + int(cy - th / 2) - 2; xx = xs + int(cx - tw / 2) - 2
    ok = (yy >= 0) & (yy < H) & (xx >= 0) & (xx < W)
    CH.col[yy[ok], xx[ok]] = col; CH.m[yy[ok], xx[ok]] = True


# ---------------------------------------------------------------- states
def sam_state(t):
    if t < 16.9: return dict(flip=False, kind='sit', menu=None)
    if t < 24.5: return dict(flip=True, kind='sit', menu='up')
    if t < 26.8: return dict(flip=True, kind='sit', menu='peek')
    if 31.35 <= t < 33.5: return dict(flip=True, kind='sit_give', menu=None)
    if t < 38.0: return dict(flip=True, kind='sit', menu=None, look=26.8 <= t < 27.7)
    return dict(flip=False, kind='sit_give' if t < 39.0 else 'sit', menu=None)

def billy_corner(t):
    """(x, pose, rot, flip, expr) at the table"""
    x = BILLY_TABLE[0]
    if t < 17.4:
        k = sm((t - 16.9) / 0.5); return (lerp(420, x, k), walk_pose(t), 0.05, False, 'normal')
    if t < 22.3: return (x, POSES['stand'], 0.05, False, 'normal')
    if t < 27.0: return (x + 6 * sm((t - 22.3) / 0.4), POSES['lean'], 0.28 * sm((t - 22.3) / 0.4), False, 'sly')
    if t < 32.8: return (x + 6, POSES['excited'] if t >= 29.7 else POSES['lean'], 0.2 if t < 29.7 else 0.05, False, 'excited' if t >= 29.7 else 'sly')
    if t < 34.0: return (x + 10, POSES['point'], 0.12, False, 'excited')
    if t < 35.6: return (x, POSES['heroic'], 0.02, False, 'shout')
    k = (t - 35.6) / 0.8
    return (x - 190 * k, run_pose(t), -0.15, True, 'shout')


# ---------------------------------------------------------------- scenes
def corner_scene(CH, v, t, billy=True, table_kw=None):
    draw_molniya(CH, mol_cam(v), t, carrot=t >= 39.4, chew=t >= 39.4)
    st = sam_state(t)
    draw_sam(CH, v.cam(SAM_HIP[0], SAM_HIP[1], U_SAM, flip=st['flip']), st['kind'], mouth=talk('sam', t),
             menu=st['menu'], look_cam=st.get('look', False))
    draw_table(CH, v, t, **(table_kw or {}))
    if billy and 16.9 <= t < 36.4:
        x, pose, rot, flip, expr = billy_corner(t)
        draw_billy(CH, v.cam(x, BILLY_TABLE[1] - 8.9 * U_BILLY, U_BILLY, flip), pose, rot, talk('billy', t), expr)

def coin_state(t):
    cx, ty = TABLE[0], TABLE[1]
    if t < 33.3: return None
    if t < 33.6:
        k = (t - 33.3) / 0.3; return (cx - 30, ty - 40 * (1 - k * k) - 2, t * 20)
    if t < 38.2: return (cx - 30, ty - 2, (t - 33.6) * 14 * math.exp(-(t - 33.6) * 2.5) + math.pi / 2 * (t > 34.5))
    if t < 38.9:
        k = sm((t - 38.2) / 0.7); return (lerp(cx - 30, cx + 44, k), ty - 2, 0.0)
    return (cx + 44, ty - 2, 0.0) if t < 39.4 else None

SHOTS = [  # (t0, t1, name)
    (0.00, 2.50, 'doors'), (2.50, 4.10, 'freeze'), (4.10, 6.10, 'corner_wide'), (6.10, 8.30, 'cu_sam'),
    (8.30, 10.00, 'cu_mol'), (10.00, 11.40, 'menu'), (11.40, 14.30, 'cu_sam'), (14.30, 15.50, 'bar'),
    (15.50, 16.90, 'point'), (16.90, 19.00, 'two'), (19.00, 21.10, 'cu_billy'), (21.10, 22.30, 'cu_mol'),
    (22.30, 24.50, 'two_close'), (24.50, 26.70, 'cu_sam'), (26.70, 27.60, 'cu_sam_cam'), (27.60, 29.70, 'cu_sam'),
    (29.70, 31.40, 'cu_billy'), (31.40, 33.30, 'cu_sam'), (33.30, 34.00, 'coin'), (34.00, 36.35, 'two'),
    (36.35, 38.00, 'exit'), (38.00, 40.10, 'split'), (40.10, 43.00, 'cu_mol_cam'), (43.00, DUR + 1, 'doors_end'),
]
FLASH_AT = [0.0, 2.5, 16.9, 33.3, 36.35]

def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a; CH = Chars(); extra = []
    if name in ('doors', 'doors_end'):
        if name == 'doors':
            Z = lerp(2.3, 2.5, sm(u / 2.5)); sh = 5 * math.exp(-u * 8) * math.sin(u * 70)
            v = View(0 + sh / Z, 222, Z)
        else:
            v = View(0, 180, 1.45 + 0.03 * u)
        big, xs, ys = bg(v)
        draw_doors(CH, v, door_angle(t))
        if name == 'doors':
            bx = lerp(58, 74, sm(u / 0.3))
            pose = blend_pose(POSES['stand'], POSES['shout'], sm(u / 0.25))
            draw_billy(CH, v.cam(bx, 522 - 8.9 * 9, 9.0), pose, -0.08 + 0.1 * sm(u / 0.3), talk('billy', t), 'shout')
    elif name == 'freeze':
        v = View(96 + 6 * u, 40 + 6 * u, 1.0 + 0.05 * u)
        big, xs, ys = bg(v)
        blit_world(big, xs, ys, BT['polish0'], SAL.BT_X - 60, 0)
        pose = blend_pose(POSES['shout'], POSES['hips'], sm((u - 0.8) / 0.3))
        draw_billy(CH, v.cam(200, 632 - 8.9 * 11, 11.0), pose, 0.05, talk('billy', t), 'shout' if u < 1.0 else 'normal')
        if u > 0.2:
            for (wx, wy) in ((208, 398), (SAL.BT_X, 312)):
                sx, sy = v.pt(wx, wy - 6 * abs(math.sin(min(u - 0.2, 0.4) * 8)))
                px_small(CH, '!', sx, sy, 16, (255, 230, 90))
    elif name == 'corner_wide':
        v = View(500 + 8 * u, 128, 1.25)
        big, xs, ys = bg(v); corner_scene(CH, v, t)
    elif name in ('cu_sam', 'cu_sam_cam'):
        st = sam_state(t)
        Z = 3.1 + 0.08 * u
        v = view_at(SAM_HIP[0] + (1.5 if not st['flip'] else -1.5) * U_SAM, SAM_HIP[1] - 9.7 * U_SAM, Z, 170, 420)
        big, xs, ys = bg(v); corner_scene(CH, v, t)
    elif name in ('cu_mol', 'cu_mol_cam'):
        hx, hy = mol_head_world(t)
        Z = 3.0 + (0.1 * u if name == 'cu_mol' else 0.25 * sm(u / 2.5))
        v = view_at(hx - 4 * U_MOL, hy + 2 * U_MOL, Z, 180, 430)
        big, xs, ys = bg(v); corner_scene(CH, v, t, billy=False)
    elif name == 'menu':
        v = view_at(SAL.BAR_X + 42, 238 + 30 * sm(u / 1.0), 4.0 - 0.3 * sm(u / 1.2), 180, 380)
        big, xs, ys = bg(v)
    elif name == 'bar':
        sh = 4 * math.exp(-(t - 14.5) * 10) * math.sin((t - 14.5) * 60) if t > 14.5 else 0
        v = view_at(SAL.BT_X - 30 + sh, 430, 1.9, 180, 330)
        big, xs, ys = bg(v)
        blit_world(big, xs, ys, BT['polish%d' % (int(t * 4) % 2)], SAL.BT_X - 60, 0)
        k = sm((t - 14.35) / 0.15)
        pose = blend_pose(POSES['shout'], POSES['point'], k)
        draw_billy(CH, v.cam(SAL.BT_X - 70, 640 - 8.9 * 11, 11.0), pose, 0.05 + 0.2 * k, 0.0, 'normal')
    elif name == 'point':
        k = sm((t - 16.35) / 0.5)
        v0 = view_at(SAL.BT_X + 10, 345, 2.7, 150, 340); v1 = View(470, 166, 1.35)
        v = View.raw(lerp(v0.X0, v1.X0, k), lerp(v0.Y0, v1.Y0, k), lerp(v0.Z, v1.Z, k))
        big, xs, ys = bg(v)
        blit_world(big, xs, ys, BT['point0' if t >= 15.75 else 'polish0'], SAL.BT_X - 60, 0)
        if k > 0.5: corner_scene(CH, v, t, billy=False)
        if 0.05 < k < 0.95:                                                   # whip-pan smear
            sm_ = int(40 * math.sin(math.pi * k))
            big[:] = ((big.astype(np.uint16) + np.roll(big, sm_, 1) + np.roll(big, -sm_, 1)) // 3).astype(np.uint8)
    elif name in ('two', 'two_close'):
        if name == 'two': v = View(470 - 6 * u, 166, 1.35 + 0.02 * u)
        else: v = view_at(548, 470, 2.0 + 0.1 * u, 180, 420)
        big, xs, ys = bg(v); corner_scene(CH, v, t)
    elif name == 'cu_billy':
        x, pose, rot, flip, expr = billy_corner(t)
        v = view_at(x + 12, BILLY_TABLE[1] - 8.9 * U_BILLY - 9.7 * U_BILLY, 3.0 + 0.1 * u, 150, 420)
        big, xs, ys = bg(v); corner_scene(CH, v, t)
    elif name == 'coin':
        v = view_at(TABLE[0] - 24, TABLE[1] - 6, 3.6, 180, 330)
        big, xs, ys = bg(v); corner_scene(CH, v, t, table_kw=dict(coin=coin_state(t)))
    elif name == 'exit':
        v = View(0, 170, 1.4)
        big, xs, ys = bg(v)
        draw_doors(CH, v, door_angle(t))
        if u < 1.2:                                                           # tiny Billy running off outside
            bx = 60 + 12 * u
            draw_billy(CH, v.cam(bx, 432 - 8.9 * 2.2, 2.2, True), run_pose(t), -0.15, 0.0, 'normal')
    elif name == 'split':
        Zs = 1.15                                                        # table scene in the RIGHT half
        v = View.raw(TABLE[0] + 6 - 480 / Zs, TABLE[1] - 40 - 190 / Zs, Zs)
        big, xs, ys = bg(v)
        corner_scene(CH, v, t, billy=False, table_kw=dict(coin=coin_state(t)))
        CH.m[:, :322] = False
        # left half: desert chase (outside strip, 320 px tall logical -> 1080)
        scroll = int(t * 260) % (OUTSIDE.shape[1] * UP)
        oxs = ((np.arange(960) + scroll) // UP) % OUTSIDE.shape[1]
        oys = np.minimum((np.arange(OUT_H) * OUTSIDE.shape[0] / OUT_H).astype(int), OUTSIDE.shape[0] - 1)
        big[:, :960] = OUTSIDE[oys[:, None], oxs[None, :]]
        cam = ACam(1000.0, 1000.0, 160, 215 - 8.9 * 6.6, 6.6)
        draw_billy(CH, cam, run_pose(t), -0.2, 0.6 + 0.4 * math.sin(t * 11), 'shout')
        CH.m[:, 318:324] = False
        extra.append(('split', None))
    else:
        v = View(0, 0, 1.0); big, xs, ys = bg(v)
    CH.comp(big)
    if name == 'split': big[:, 954:966] = (30, 18, 12)
    if name == 'menu':
        pass
    return big


# ---------------------------------------------------------------- overlays
BADGE = O.make_badge('СЕЗОН 1 • СЕРИЯ 3/6')
HOOK = O.pixel_title(['ИЩЕТ', 'ИНФОРМАТОРА'], 64)
TEASE = O.pixel_title(['СЕРИЯ 4 СКОРО'], 40)

def carrot_icon(n=2, s=6):
    c = np.zeros((16 * s, (12 * n + 4) * s, 4), np.uint8)
    for k in range(n):
        x0 = k * 12 * s
        for i in range(10):
            w = max(1, 5 - i // 2)
            c[(4 + i) * s:(5 + i) * s, x0 + (6 - w // 2) * s:x0 + (6 + w - w // 2) * s] = (236, 128, 40, 255)
        c[0:4 * s, x0 + 5 * s:x0 + 7 * s] = (84, 160, 60, 255); c[s:3 * s, x0 + 3 * s:x0 + 9 * s] = (84, 160, 60, 255)
    return c

import wideov as WO
DAY, INCOME = 340, (8, 22, 10.0)                         # HUD of the feature cut: (before, after, bump time)
STICKERS = [
    (O.sticker('×2', icon=carrot_icon(1, 7)), 9.72, 10.0, 1450, 300),
    (O.sticker('50¢', fg=(255, 190, 90), size=80), 10.35, 11.40, 960, 300),
    (O.sticker('$5', fg=(255, 236, 120), size=88), 33.4, 34.9, 960, 280),
    (O.sticker('3 ГОДА', fg=(255, 236, 120), size=64), 40.35, 42.9, 960, 280),
]


def render(t):
    big = render_scene(t)
    WO.stickers(big, STICKERS, t)
    WO.hud(big, t, DAY, INCOME[1] if t >= INCOME[2] else INCOME[0])
    CAPTIONS.draw(big, t, WO.CAP_Y)
    for fa in FLASH_AT:
        if fa <= t < fa + 0.15: O.flash(big, 0.75 * (1 - (t - fa) / 0.15))
    if 4.10 <= t < 4.40: O.mosaic(big, int(lerp(48, 1, (t - 4.10) / 0.30)))
    if 43.0 <= t < 43.25: O.mosaic(big, int(lerp(36, 1, (t - 43.0) / 0.25)))
    return big


def cover_frame():
    p = P.episode(EP) / 'cover.png'
    return np.array(Image.open(p).convert('RGB').resize((OUT_W, OUT_H))) if p.exists() else None


def encode(a0, a1, out):
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OUT_W}x{OUT_H}', '-r', str(FPS),
                             '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    cov = cover_frame()
    for i in range(a0, a1):
        fr = cov if (i < 6 and cov is not None) else render(i / FPS)
        proc.stdin.write(fr.tobytes())
    proc.stdin.close(); proc.wait()


if __name__ == '__main__':
    n = int(round(DUR * FPS))
    if sys.argv[1] == 'test':
        ts = list(map(float, sys.argv[2:]))
        c = Image.new('RGB', (270 * len(ts), 480))
        for k, tt in enumerate(ts):
            c.paste(Image.fromarray(render(tt)).resize((270, 480), Image.LANCZOS), (k * 270, 0))
        c.save(P.build(EP, 'sheet.png')); print(P.build(EP, 'sheet.png'))
    elif sys.argv[1] == 'frame':
        Image.fromarray(render(float(sys.argv[2]))).save(P.build(EP, 'frame.png'))
    elif sys.argv[1] == 'seg':
        a0, a1 = int(sys.argv[2]), min(int(sys.argv[3]), n)
        encode(a0, a1, P.build(EP, f'seg_{a0:04d}.mp4')); print('done', a0, a1)
    elif sys.argv[1] == 'all':
        k = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        cuts = [round(n * i / k) for i in range(k + 1)]
        procs = [subprocess.Popen([sys.executable, __file__, 'seg', str(cuts[i]), str(cuts[i + 1])]) for i in range(k)]
        for p_ in procs: p_.wait()
        lst = P.build(EP, 'segs.txt')
        with open(lst, 'w') as f:
            for i in range(k): f.write(f"file '{P.build(EP, f'seg_{cuts[i]:04d}.mp4')}'\n")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', P.build(EP, 'noaudio.mp4')], check=True)
        print('ok', P.build(EP, 'noaudio.mp4'))
