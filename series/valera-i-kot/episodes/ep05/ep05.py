"""S01E05 «Операция «Кипяток»» — Valera sneaks into the basement with a flashlight and opens the forbidden valve.
Hot water rushes... into the frozen sandbox in the yard, where the grannies now have a resort. «Отопил двор.»
  python3 ep05.py test 1 5 20 | frame 12 | all [4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import stage as ST
from stage import View, view_at, Chars, Light, OUT_W, OUT_H
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from timeline import DUR, FPS, VOICE, SLUG

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
W = PK.build()
KIT, BATH, STAIR = W['kitchen'], W['bath'], W['stair']
TUB, TUBXY = W['tub'], W['tub_xy']
BASE = PK.basement()
SPRING = PK.q(Image.open(PK.BG / 'yard_spring.png').convert('RGB'))
POOL = PK.q(Image.open(PK.BG / 'pool.png').convert('RGB'))

VX, VY, VU = 860.0, 715.0, 18.0                         # Valera at the valve (basement), facing right
WX, WY, WR = PK.BS_VALVE
CATB = (690.0, 712.0, 8.5)                              # cat in the basement
SHOWER_V = (468.0, 470.0)                               # Valera in the tub (feet hidden)
BEG = (1060.0, 900.0, 22.0)                             # Valera in a towel by the pool, facing left
T_TURN = 13.95                                          # the wheel gives way («РАЗ!»)
DARK = (0.5, 0.55, 0.68)
SP_X = (620, 1060)


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


# ---------------------------------------------------------------- basement lighting helpers
def beam(big, v, p0, ang, length, half=0.3, a=0.5, col=(255, 236, 180)):
    """flashlight cone from world p0 at angle ang (world length), stepped and pixelated (6 px cells)"""
    ox, oy = v.opt(*p0)
    Lo = length * v.Z * ST.UP
    ys, xs = np.mgrid[3:OUT_H:6, 3:OUT_W:6].astype(np.float32)
    dx, dy = xs - ox, ys - oy
    d = np.hypot(dx, dy)
    th = (np.arctan2(dy, dx) - ang + math.pi) % (2 * math.pi) - math.pi
    f = np.clip(1 - np.abs(th) / half, 0, 1) ** 0.6 * np.clip(1 - d / Lo, 0, 1) * np.clip(d / 40, 0, 1)
    f = np.floor(f * 5) / 5 * a
    f = f.repeat(6, 0).repeat(6, 1)[:OUT_H, :OUT_W][..., None]
    c = np.array(col, np.float32)
    big[:] = np.clip(big * (1 + f * 0.9) + f * c * 0.3, 0, 255).astype(np.uint8)


def light_base(v, keys=(), amb=(0.62, 0.68, 0.84)):
    bx, by = v.opt(*PK.BS_BULB)
    return Light(amb=amb, keys=[(bx, by, 900, (255, 196, 120), 0.45)] + list(keys), rim=(1, -0.3, (170, 200, 255), 0.3), grad=(1.0, 0.85))


def hand_world(X, Y, U, hn, flip=False):
    return (X + (hn[0] - 1000) * U * (-1 if flip else 1), Y + (hn[1] - 1000) * U)


def wheel_ang(t):
    if t < 12.4: return 0.0
    if t < T_TURN: return 0.04 * math.sin(t * 40) * sm((t - 12.4) / 0.5)
    return 0.9 * (t - T_TURN) + 1.2 * sm((t - T_TURN) / 0.4)


def wheel(CH, v, t):
    L = Layer(v.wcam())
    F.ell(L, (WX, WY), WR + 4, WR + 4, (46, 40, 38))                                      # backing plate hides the painted wheel
    a0 = wheel_ang(t)
    n = 28
    for i in range(n):
        a, b = a0 + i / n * 2 * math.pi, a0 + (i + 1) / n * 2 * math.pi
        F.cap(L, (WX + math.cos(a) * WR * 0.86, WY + math.sin(a) * WR * 0.86), (WX + math.cos(b) * WR * 0.86, WY + math.sin(b) * WR * 0.86),
              7.0, 7.0, (150, 52, 38), (196, 86, 60), (98, 32, 26))
    for k in range(5):
        a = a0 + k * 2 * math.pi / 5
        F.cap(L, (WX, WY), (WX + math.cos(a) * WR * 0.8, WY + math.sin(a) * WR * 0.8), 4.2, 3.2, (140, 48, 36), (186, 80, 58), (92, 30, 24))
    F.ell(L, (WX, WY), 13, 13, (120, 110, 100), 0, (170, 160, 146), (70, 64, 60))
    F.ell(L, (WX, WY), 5, 5, (60, 56, 54))
    F.outline(L); CH.add(L)


def gauges(FX, v, t):
    L = Layer(v.wcam())
    spin = max(0.0, t - 14.3)
    for i, (gx, gy, r) in enumerate(PK.BS_GAUGES):
        a = -2.2 + (0.4 if spin <= 0 else min(4.4, spin * 7) + 0.25 * math.sin(t * 40 + i))
        F.cap(L, (gx, gy), (gx + math.cos(a - math.pi / 2) * r * 0.8, gy + math.sin(a - math.pi / 2) * r * 0.8), 1.8, 1.0, (200, 40, 30))
        F.ell(L, (gx, gy), 2.4, 2.4, (40, 36, 34))
    FX.add(L)


def v_base(CH, v, t, x=VX, pose=None, expr='whisper', flash='fwd', **kw):
    """Valera in the basement (telnyashka + ushanka); flash: 'chin' | 'fwd' | 'down' | None -> returns lens world pos, beam angle"""
    hn, pn, info = None, None, None
    if flash == 'chin':
        hn = F.H(3.6, 14.2); pn = lambda L, h: B.flashlight(L, h, -1.75)
    elif flash == 'fwd':
        hn = F.H(6.2, 15.2); pn = lambda L, h: B.flashlight(L, h, 0.12)
    kw.setdefault('hand_n', hn)
    r = F.valera(CH, v.cam(x, VY, VU), pose or F.VPOSE['stand'], t, mouth('valera', t), expr, 'home', hat='ushanka',
                 prop_n=pn if flash in ('chin', 'fwd') else kw.pop('prop_n', None), **kw)
    hw = hand_world(x, VY, VU, r['hand_n'])
    if flash == 'chin': return (hw[0] - 0.4 * VU, hw[1] - 2.5 * VU), -1.9
    if flash == 'fwd': return (hw[0] + 2.6 * VU, hw[1] + 0.3 * VU), 0.12
    return None


def base_frame(v, t, valera=None, cat=None, steam=False, shake=0.0, keys=(), beam_a=0.5, wheel_on=True, grade=DARK):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    fx.grade(big, grade)
    if wheel_on: wheel(CH, v, t)
    if cat: cat(CH, v)
    CH.comp(big, light_base(v, keys))
    lens = None
    if valera:
        CH2 = Chars(); lens = valera(CH2, v)
        ks = list(keys)
        if lens is not None:
            lx, ly = v.opt(*lens[0]); ks.append((lx, ly, 520, (255, 232, 170), 0.9))
        CH2.comp(big, light_base(v, ks))
    gauges(FX, v, t)
    FX.comp(big)
    if lens is not None:
        if lens[1] > -1.0: beam(big, v, lens[0], lens[1], 520, a=beam_a)
        lx, ly = v.opt(*lens[0]); fx.glow(big, lx, ly, 40 * v.Z, (255, 240, 200), 0.8)
    bx, by = v.opt(*PK.BS_BULB); fx.glow(big, bx, by, 120 * v.Z, (255, 200, 120), 0.35 * (0.85 + 0.15 * math.sin(t * 23)))
    if steam:
        for i, (jx, jy) in enumerate(PK.BS_JOINTS + [(WX - 80, WY + 40)]):
            B.steam(big, v, t, jx, jy, 14.4, n=4, rise=120, size=30, a=0.5, seed=i * 7)
    fx.vignette(big, 0.5)
    if shake: B.shake(big, t, shake, 41)
    return big


def v_face(x=VX):
    return K.face_w(x, VY, VU, h=20.6)


# ---------------------------------------------------------------- basement shots
def r_hook(t, u, expr='whisper', Z=2.35):
    fx_, fy_ = v_face()
    v = view_at(BASE, fx_ - 6, fy_ + 14, Z + 0.07 * u, 180, 300)
    return base_frame(v, t, valera=lambda CH, v_: v_base(CH, v_, t, expr=expr, flash='chin'), grade=(0.42, 0.46, 0.6))


def r_corridor(t, u):
    x = lerp(470, 600, u / 2.2)
    v = view_at(BASE, 560 + 0.5 * (x - 470), 420, 1.0, 180, 330)
    return base_frame(v, t, valera=lambda CH, v_: v_base(CH, v_, t, x, F.vwalk(t, 6.5, 0.3), 'sly', 'fwd'), beam_a=0.55)


def cat_b(CH, v, t, x=CATB[0], pose='sit'):
    F.cat(CH, v.cam(x, CATB[1], CATB[2]), t, pose, mouth('cat', t, 2.0), 0.55, (0.0, 0.0) if pose == 'sit' else (0.3, 0.0), tail=0.6)


def r_cat_dark(t, u):
    x, y = CATB[0], CATB[1] - 11.4 * CATB[2]
    v = view_at(BASE, x, y + 10, 3.0 + 0.06 * u, 180, 300)
    lx, ly = v.opt(x - 60, y + 40)
    return base_frame(v, t, cat=lambda CH, v_: cat_b(CH, v_, t), keys=[(lx, ly, 700, (255, 230, 170), 0.8)])


def walk_x(t):
    return lerp(560, VX, sm((t - 6.4) / 2.4))


def r_walk(t, u):
    x = walk_x(t)
    v = view_at(BASE, x + 80, 420, 0.95, 180, 330)
    moving = t < 8.7
    pose = F.vwalk(t, 7.5, 0.32) if moving else F.VPOSE['stand']
    return base_frame(v, t, valera=lambda CH, v_: v_base(CH, v_, t, x, pose, 'sly', 'fwd'),
                      cat=lambda CH, v_: cat_b(CH, v_, t, x - 150, 'walk' if moving else 'sit'))


def r_sign(t, u):
    x0, y0, x1, y1 = PK.BS_TAG
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    v = view_at(BASE, cx, cy - 10, 2.3 + 0.1 * u, 180, 300)
    big = base_frame(v, t, grade=(0.4, 0.44, 0.56))
    sx, sy = v.opt(cx + 20 * math.sin(t * 2.5), cy + 6 * math.cos(t * 3))                   # flashlight spot sweeping the sign
    fx.glow(big, sx, sy, 380, (255, 238, 190), 0.3)
    return big


def r_v_proud(t, u):
    fx_, fy_ = v_face()
    v = view_at(BASE, fx_ - 6, fy_ + 14, 2.2 + 0.06 * u, 180, 300)
    lx, ly = v.opt(VX + 5 * VU, VY - 14 * VU)
    return base_frame(v, t, valera=lambda CH, v_: v_base(CH, v_, t, pose=F.VPOSE['proud'], expr='smug', flash=None),
                      keys=[(lx, ly, 800, (255, 232, 170), 0.7)])


def v_strain(CH, v, t):
    k = sm((t - 12.4) / 0.4)
    push = 0.4 * math.sin(t * 18) * (1 if t < T_TURN else 0)
    a = wheel_ang(t)
    a = min(a, 0.5)                                                                        # grip points ride the rim, then let go
    tn = (WX + math.cos(a + 2.25) * WR * 0.86, WY + math.sin(a + 2.25) * WR * 0.86)
    tf = (WX + math.cos(a + 2.75) * WR * 0.86, WY + math.sin(a + 2.75) * WR * 0.86)
    un = F.H((tn[0] - VX) / VU, (VY - tn[1]) / VU)
    uf = F.H((tf[0] - VX) / VU, (VY - tf[1]) / VU)
    expr = 'shout' if T_TURN - 0.3 < t < T_TURN + 0.5 else ('blissful' if t > T_TURN + 0.5 else 'angry')
    tint = (1.0 + 0.18 * k, 0.88, 0.86) if t < T_TURN + 0.3 else None
    F.valera(CH, v.cam(VX + push, VY, VU), dict(F.VPOSE['strain'], bn=-1, bf=-1), t, mouth('valera', t), expr, 'home',
             hat='ushanka', hand_n=un, hand_f=uf, lean=0.3, tint=tint)
    return None


def r_strain(t, u):
    v = view_at(BASE, 960, 420, 1.45 + 0.08 * u, 180, 320)
    lx, ly = v.opt(VX + 2 * VU, VY - 8 * VU)
    big = base_frame(v, t, valera=lambda CH, v_: v_strain(CH, v_, t), keys=[(lx, ly, 600, (255, 226, 160), 0.6)],
                     steam=t > 14.4, shake=6 if t > T_TURN else (2 if t > 12.6 else 0))
    return big


def r_pipes(t, u):
    v = view_at(BASE, 330, 330, 1.05 + 0.05 * u, 180, 320)
    big = base_frame(v, t, steam=True, shake=10, grade=(0.62, 0.66, 0.8))
    return big


def r_ecstatic(t, u):
    fx_, fy_ = v_face()
    v = view_at(BASE, fx_ + 30, fy_ + 18, 2.0 + 0.08 * u, 180, 300)
    lx, ly = v.opt(VX + 3 * VU, VY - 10 * VU)
    big = base_frame(v, t, valera=lambda CH, v_: v_base(CH, v_, t, pose=F.VPOSE['fist'], expr='blissful' if t > 17.6 else 'shout',
                                                         flash=None, hand_n=F.H(8.2, 25.0)), keys=[(lx, ly, 800, (255, 226, 160), 0.6)], steam=True, shake=3)
    return big


# ---------------------------------------------------------------- flat
def r_run(t, u):
    x = lerp(120, 1000, u / 1.1)
    v = view_at(STAIR, 560, 430, 1.0, 180, 330)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    F.valera(CH, v.cam(x, 700, 15.0), F.vwalk(t, 22, 0.6), t, 0.0, 'shout', 'home', hat='ushanka', lean=1.2)
    lx, ly = v.opt(840, 60)
    CH.comp(big, Light(amb=(0.92, 0.94, 1.0), keys=[(lx, ly, 1300, (255, 206, 140), 0.7)], rim=(-1, -0.3, (190, 214, 255), 0.3)))
    fx.speed_lines(big, t, 0.7)
    fx.vignette(big, 0.3)
    return big


def r_tap(t, u):
    x, y = SHOWER_V
    fx_, fy_ = K.face_w(x, y, PK.B_UNIT, h=20.6)
    v = view_at(BATH, fx_ + 4, fy_ - 20, 2.2 + 0.05 * u, 180, 330)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    F.valera(CH, v.cam(x, y, PK.B_UNIT), F.VPOSE['shrug'] if t > 19.5 else F.VPOSE['stand'], t, mouth('valera', t),
             'sad' if t > 20.1 else 'squint', 'towel', hat=None)
    CH.comp(big, K.light_bath(v))
    L = Layer(v.wcam())                                                                   # one lonely drop
    sx, sy = PK.SHOWER
    k = (t - 19.6) / 0.35
    if k < 0: F.ell(L, (sx, sy + 6 + 3 * max(0, (t - 19.2) / 0.4)), 2.2, 2.8, (170, 210, 250))
    elif k < 1: F.ell(L, (sx + 1, sy + 8 + (fy_ - 30 - sy) * k * k), 2.2, 3.4, (170, 210, 250))
    elif k < 1.4:
        for i in range(5): F.dot(L, (fx_ - 6 + 3 * i, fy_ - 34 - 10 * math.sin((k - 1) * 7) + i % 2 * 3), (170, 210, 250), 1.4)
    FX.add(L)
    FX.comp(big)
    fx.vignette(big, 0.3)
    return big


def r_cat_kit(t, u, Z=3.0, look=(0.6, -0.4), sy=300):
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx, hy + 5, Z + 0.06 * u, 180, sy)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    F.cat(CH, v.cam(x, y, PK.CAT_K_UNIT), t, 'loaf', mouth('cat', t, 2.0), 0.55, look, tail=0.8)
    CH.comp(big, K.light_kit(v))
    B.snow_in(FX, v, t, PK.WINDOW_OPEN, n=36, drift=(-90, 220))
    FX.comp(big)
    B.haze(big, v, t, (PK.RAD[0], PK.RAD[1] - 70, PK.RAD[2], PK.RAD[1] + 10), amp=6, a=0.4)
    fx.vignette(big, 0.3)
    return big


# ---------------------------------------------------------------- yard resort
def light_pool(v):
    wx, wy = v.opt(700, 560)
    sx, sy = v.opt(1240, 240)
    return Light(amb=(0.78, 0.88, 1.08), keys=[(wx, wy, 1400, (130, 255, 214), 0.65), (sx, sy, 1300, (255, 206, 140), 0.4)],
                 rim=(0, 1, (150, 255, 220), 0.35), grad=(0.95, 1.05))


def cocktail(L, h):
    x, y = h[0] + 0.2, h[1] - 0.6
    F.cap(L, (x, y + 0.2), (x, y - 1.4), 0.12, 0.12, (220, 236, 240))
    F.poly(L, [(x - 1.2, y - 3.2), (x + 1.2, y - 3.2), (x, y - 1.4)], (236, 244, 248))
    F.poly(L, [(x - 0.95, y - 3.0), (x + 0.95, y - 3.0), (x, y - 1.7)], (255, 150, 60))
    F.cap(L, (x + 0.5, y - 3.1), (x + 1.3, y - 4.4), 0.08, 0.08, (120, 90, 60))           # umbrella
    F.poly(L, [(x + 0.4, y - 4.3), (x + 2.2, y - 4.5), (x + 1.3, y - 5.2)], (255, 110, 170))


def duck(L, x, y, s, t):
    b = 0.6 * math.sin(t * 2.3) * s / 3
    F.ell(L, (x, y + b), 3.0 * s, 1.8 * s, (255, 214, 60), 0, (255, 240, 140), (220, 170, 40))
    F.ell(L, (x + 2.0 * s, y - 2.0 * s + b), 1.4 * s, 1.3 * s, (255, 214, 60), 0, (255, 240, 140), (220, 170, 40))
    F.ell(L, (x + 3.4 * s, y - 1.8 * s + b), 0.8 * s, 0.4 * s, (255, 130, 40))
    F.dot(L, (x + 2.4 * s, y - 2.3 * s + b), (20, 20, 24), 0.25 * s)


def grannies_pool(CH, v, t, zk=None, lk=None):
    zk = dict(dict(expr='smug', look=0.6), **(zk or {}))
    lk = dict(dict(expr='smug', hand_n=F.H(3.4, 10.4), prop_n=cocktail), **(lk or {}))
    F.babushka(CH, v.cam(*PK.PL_ZINA), t, 'zina', 'sit', mouth('zina', t), **zk)
    F.babushka(CH, v.cam(*PK.PL_LYUBA, flip=True), t, 'lyuba', 'sit', mouth('lyuba', t), **lk)
    PK.clip_below(CH, v, PK.PL_WATER, *PK.PL_X)


def pool_frame(v, t, zk=None, lk=None, valera=None, snow=True):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    grannies_pool(CH, v, t, zk, lk)
    CH.comp(big, light_pool(v))
    if valera:
        CH2 = Chars(); valera(CH2, v)
        wx, wy = v.opt(700, 560)
        CH2.comp(big, Light(amb=(0.95, 0.97, 1.04), keys=[(wx, wy, 1500, (130, 255, 214), 0.35)], rim=(-1, 0.3, (150, 255, 220), 0.4)))
    L = Layer(v.wcam()); duck(L, 690, PK.PL_WATER + 12, 5.0, t); F.outline(L); FX.add(L)
    if snow: B.falling_snow(FX, v, t, v.X0 - 20, v.Y0 - 20, v.X0 + 380 / v.Z + 20, v.Y0 + 660 / v.Z, n=60, speed=40)
    FX.comp(big)
    for i, x in enumerate((300, 520, 700, 900, 1060)):
        B.steam(big, v, t, x, PK.PL_WATER + 10, -99, n=3, rise=220, size=50, a=0.3, seed=i * 11)
    fx.vignette(big, 0.3)
    return big


def gz_face(): return PK.PL_ZINA[0] + 1.6 * PK.PL_ZINA[2], PK.PL_ZINA[1] - 11.8 * PK.PL_ZINA[2]


def gl_face(): return PK.PL_LYUBA[0] - 1.4 * PK.PL_LYUBA[2], PK.PL_LYUBA[1] - 11.8 * PK.PL_LYUBA[2]


def r_reveal(t, u):
    k = sm(u / 1.6)
    v = view_at(SPRING, lerp(840, 835, k), lerp(420, 560, k), lerp(0.9, 1.9, k), 180, lerp(330, 360, k))
    CH, FX = K.begin(v.Z)
    big = v.bg()
    F.babushka(CH, v.cam(*PK.SP_ZINA), t, 'zina', 'sit', 0.0, 'smug', 0.6)
    F.babushka(CH, v.cam(*PK.SP_LYUBA, flip=True), t, 'lyuba', 'sit', 0.0, 'smug', hand_n=F.H(3.4, 10.4), prop_n=cocktail)
    PK.clip_below(CH, v, PK.SP_WATER, *SP_X)
    CH.comp(big, light_pool(v))
    B.falling_snow(FX, v, t, v.X0 - 20, v.Y0 - 20, v.X0 + 380 / v.Z + 20, v.Y0 + 660 / v.Z, n=70, speed=40)
    FX.comp(big)
    B.steam(big, v, t, 840, 600, 21.95, n=10, rise=380, size=60, a=0.55)                 # geyser
    for i, x in enumerate((680, 760, 940, 1010)):
        B.steam(big, v, t, x, 605, -99, n=3, rise=160, size=30, a=0.3, seed=i * 5)
    fx.vignette(big, 0.3)
    return big


def r_pool_cu(t, u, who, Z=2.4, **kw):
    x, y = gz_face() if who == 'zina' else gl_face()
    v = view_at(POOL, x, y + 40, Z + 0.04 * u, 180, 300)
    return pool_frame(v, t, **kw)


def v_beg(CH, v, t):
    x, y, un = BEG
    F.valera(CH, v.cam(x, y, un, flip=True), F.VPOSE['shrug'], t, mouth('valera', t), 'shout' if talk('valera', t) > 0.3 else 'sad',
             'towel', hat='ushanka', cold=0.15, breath=False)


def r_beg(t, u):
    x, y, un = BEG
    fx_, fy_ = K.face_w(x, y, un, flip=True, h=20.6)
    v = view_at(POOL, fx_ - 20, fy_ + 50, 1.3 + 0.05 * u, 180, 280)
    big = pool_frame(v, t, valera=lambda CH, v_: v_beg(CH, v_, t))
    B.shake(big, t, 3, 50)
    return big


def r_loop(t, u):
    return r_hook(t, u, 'angry' if u > 0.3 else 'squint', 2.2)


# ---------------------------------------------------------------- shots
SHOTS = [
    (0.00, 1.95, 'hook'), (1.95, 4.20, 'corridor'), (4.20, 6.40, 'cat_dark'), (6.40, 9.00, 'walk'), (9.00, 10.75, 'sign'),
    (10.75, 12.40, 'v_proud'), (12.40, 14.60, 'strain'), (14.60, 15.90, 'pipes'), (15.90, 18.30, 'ecstatic'),
    (18.30, 19.40, 'run'), (19.40, 20.60, 'tap'), (20.60, 21.95, 'cat_window'), (21.95, 23.60, 'reveal'),
    (23.60, 26.35, 'zina'), (26.35, 29.00, 'lyuba'), (29.00, 31.20, 'beg'), (31.20, 32.50, 'zina2'),
    (32.50, 34.40, 'cat_end'), (34.40, DUR + 1, 'loop'),
]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name == 'hook': return r_hook(t, u)
    if name == 'corridor': return r_corridor(t, u)
    if name == 'cat_dark': return r_cat_dark(t, u)
    if name == 'walk': return r_walk(t, u)
    if name == 'sign': return r_sign(t, u)
    if name == 'v_proud': return r_v_proud(t, u)
    if name == 'strain': return r_strain(t, u)
    if name == 'pipes': return r_pipes(t, u)
    if name == 'ecstatic': return r_ecstatic(t, u)
    if name == 'run': return r_run(t, u)
    if name == 'tap': return r_tap(t, u)
    if name == 'cat_window': return r_cat_kit(t, u)
    if name == 'reveal': return r_reveal(t, u)
    if name == 'zina': return r_pool_cu(t, u, 'zina', 1.35)
    if name == 'lyuba': return r_pool_cu(t, u, 'lyuba', 1.45)
    if name == 'beg': return r_beg(t, u)
    if name == 'zina2': return r_pool_cu(t, u, 'zina', 1.7, zk=dict(look=1.0, expr='normal'))
    if name == 'cat_end': return r_cat_kit(t, u, 2.8, (0.0, 0.0))
    return r_loop(t, u)


SHOW = K.Show(EPI, 5, ['ОПЕРАЦИЯ', '«КИПЯТОК»'], hook_t=(0.12, 2.3),
              stickers=[(O.sticker('+95°', fg=(255, 150, 90), size=72), 14.7, 15.9, 540, 420),
                        (O.sticker('КУРОРТ «ПЕСОЧНИЦА»', fg=(140, 255, 220), size=44), 22.2, 23.6, 540, 360),
                        (O.sticker('-20°', fg=(160, 210, 255), size=72), 29.1, 31.1, 540, 1560)],
              flashes=[T_TURN, 21.95], mosaics=[18.30, 34.40], cap_y={'reveal': 1420, 'run': 1400, 'walk': 1400, 'corridor': 1400},
              teaser='ДАЛЬШЕ: НОВЫЙ ГОД')


def render(t):
    big = render_scene(t)
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
