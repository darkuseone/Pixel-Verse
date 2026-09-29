"""S01E06 «С лёгким паром» — season finale. 31 December: hot water is finally back at 23:55, Valera digs his bath kit out
of the mezzanine (and gets buried by twenty years of army junk), but the cat is already lying in the hot tub. At midnight
the water goes icy again — the very first frame of E01 — and the ZhEK posts «С 01.01 ПЛАНОВОЕ ОТКЛЮЧЕНИЕ».
  python3 ep06.py test 1 5 20 | frame 12 | all [4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import View, view_at, Chars, Light, shadow
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from props import newyear as NY
from timeline import DUR, FPS, VOICE, SLUG, T_OPEN, T_DOOR, T_MIDNIGHT, T_ICE

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
W = PK.build()
KIT = np.array(PK.kitchen(31))
BATH, TUB, TUBXY = W['bath'], W['tub'], W['tub_xy']
HALL = PK.q(Image.open(PK.BG / 'hallway.png').convert('RGB'))
YARD = W['yard']

STOVE_V = (960.0, 660.0, 16.5)                           # Valera in the kitchen, facing left
LIFT_V = (780.0, 670.0, 16.5)
STOOL_V = (650.0, 600.0, 15.0)                           # Valera on a stool under the mezzanine
PILE_V = (650.0, 875.0, 15.0)                            # buried: only the head sticks out of the junk
DALI_V = (900.0, 715.0, 17.0)
FLOOR_V = (850.0, 700.0, 17.0)                           # bathroom floor, facing left (towards the tub)
RIM_V = (525.0, 596.0, 14.0)                             # sitting on the tub rim, facing left
SHOWER_V = (468.0, 470.0)                                # standing in the tub under the shower (E01 framing)
CAT_TUB = (330.0, 432.0, 13.0)                           # cat's chin at the waterline in the tub
CAT_WASH = (1150.0, 424.0, 7.5)                          # cat on the washing machine
FAUCET = (636.0, 404.0)
ANTRESOL = (505, 96, 800, 186)
KIT_GARLAND = [(10, 34), (420, 22), (840, 26), (1275, 40)]
AVA = NY.Avalanche(T_OPEN + 0.05, (560, 110, 760, 186), 716, 660, mound_h=120, mound_w=140, scale=14.0, seed=6)


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def notice_world(stamp):
    img = Image.fromarray(PK.q(Image.open(PK.BG / 'stairwell.png').convert('RGB')))
    img = PK.notice(img, [('ОБЪЯВЛЕНИЕ', 8, (40, 36, 40)), ('С 01.01', 16, (170, 30, 30)), ('ПЛАНОВОЕ', 8, (40, 36, 40)),
                          ('ОТКЛЮЧЕНИЕ', 8, (40, 36, 40)), ('ГОРЯЧЕЙ ВОДЫ', 8, (170, 30, 30)), ('ЖЭК №3', 8, (60, 60, 120))])
    if stamp:                                                                             # round red stamp, slightly rotated
        st = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
        d.ellipse((4, 4, 59, 59), outline=(190, 30, 36, 255), width=3); d.ellipse((11, 11, 52, 52), outline=(190, 30, 36, 255), width=1)
        st = PK.text(st, 'ЖЭК', 32, 27, 8, (190, 30, 36, 255)); st = PK.text(st, '№3', 32, 39, 8, (190, 30, 36, 255))
        st = st.rotate(-18, resample=Image.NEAREST)
        x0, y0, x1, y1 = PK.NOTICE
        img.paste(st, (x1 - 60, y1 - 64), st)
    return np.array(img)


STAIR_N, STAIR_S = notice_world(False), notice_world(True)


# ---------------------------------------------------------------- kitchen (festive)
def kitchen_decor(v, t):
    DEC = Chars()
    NY.tinsel(DEC, v, t, PK.RAD[0] + 6, PK.RAD[2] - 6, PK.RAD[1] + 4)
    L = Layer(v.cam(1150, 492, 12.0))                                                     # table: tangerines + a fir sprig
    for i, (dx, dy) in enumerate(((-4.0, 0.0), (-1.6, 0.3), (-2.8, -1.6), (0.8, 0.1))): NY.tangerine(L, (1000 + dx, 1000 + dy))
    NY.fir_sprig(L, (1000 + 5.0, 1000 + 1.2), 6.5)
    F.outline(L); DEC.add(L)
    return DEC


def kitchen_frame(v, t, draw_chars=None, cat=True, cat_kw=None, clock=None):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    kitchen_decor(v, t).comp(big, K.light_kit(v))
    if cat:
        x, y = PK.CAT_K
        kw = dict(mouth=mouth('cat', t, 2.0), lid=0.55, tail=0.6); kw.update(cat_kw or {})
        F.cat(CH, v.cam(x, y, PK.CAT_K_UNIT), t=t, pose='loaf', **kw)
        L = Layer(v.cam(x, y, PK.CAT_K_UNIT))                                             # tinsel collar
        for i in range(7):
            a0, a1 = math.pi * (0.1 + i / 7 * 0.8), math.pi * (0.1 + (i + 1) / 7 * 0.8)
            F.cap(L, (1004.4 - 2.6 * math.cos(a0), 1000 - 4.2 + 0.9 * math.sin(a0)),
                  (1004.4 - 2.6 * math.cos(a1), 1000 - 4.2 + 0.9 * math.sin(a1)), 0.45, 0.45,
                  (236, 206, 80) if (i + int(t * 6)) % 3 else (255, 244, 170))
        CH.add(L)
    CH.comp(big, K.light_kit(v))
    if draw_chars:
        CH2 = Chars(); draw_chars(CH2, v); CH2.comp(big, K.light_kit(v))
    bulbs = NY.garland(FX, v, t, KIT_GARLAND, n=26, sag=24)
    if clock is not None:
        cx, cy, r = PK.CLOCK
        L = Layer(v.wcam()); a_m, a_h = clock
        F.cap(L, (cx, cy), (cx + math.sin(a_m) * r * 0.8, cy - math.cos(a_m) * r * 0.8), 1.6, 1.2, (30, 24, 20))
        F.cap(L, (cx, cy), (cx + math.sin(a_h) * r * 0.5, cy - math.cos(a_h) * r * 0.5), 2.2, 1.8, (30, 24, 20))
        FX.add(L)
    B.snow_in(FX, v, t, PK.WINDOW_OPEN, n=30, drift=(-90, 220))
    FX.comp(big)
    NY.garland_glow(big, v, t, bulbs)
    fx.vignette(big, 0.3)
    return big


def v_kitchen(CH, v, t, pose, expr, hold=True, look=0.0):
    x, y, un = STOVE_V
    F.valera(CH, v.cam(x, y, un, flip=True), pose, t, mouth('valera', t), expr, 'home', look=look,
             prop_n=(lambda L, h: B.basin(L, (h[0] + 0.4, h[1] - 1.2), scale=0.9, tilt=-0.2)) if hold else None)


def r_hook(t, u):
    x, y, un = STOVE_V
    fx_, fy_ = K.face_w(x, y, un, flip=True, h=20.3)
    v = view_at(KIT, fx_ - 34, fy_ + 26, 1.9 + 0.08 * u, 180, 300)
    return kitchen_frame(v, t, lambda CH, v_: v_kitchen(CH, v_, t, F.VPOSE['hold'], 'proud' if talk('valera', t) < 0.3 else 'shout'),
                         cat=False)


def r_calendar(t, u):
    x0, y0, x1, y1 = PK.CALENDAR
    v = view_at(KIT, (x0 + x1) / 2, y0 + 80, 2.6 + 0.25 * sm(u / 1.4), 180, 300)
    return kitchen_frame(v, t, cat=False)


def r_trad(t, u):
    x, y, un = LIFT_V
    v = view_at(KIT, x + 10, 400, 1.2 + 0.05 * u, 180, 330)
    lift = sm(u / 0.4)
    bh = lerp(14.0, 27.5, lift)
    def draw(CH, v_):
        F.valera(CH, v_.cam(x, y, un), F.VPOSE['overhead'], t, mouth('valera', t), 'shout', 'home', hand_n=(1000 + 5.6, 1000 - bh),
                 hand_f=(1000 - 3.6, 1000 - bh))
        L = Layer(v_.cam(x, y, un)); B.basin(L, (1000 + 1.0, 1000 - bh - 0.9), scale=1.15); F.outline(L); CH.add(L)
    return kitchen_frame(v, t, draw, cat=True, cat_kw=dict(lid=0.85, mouth=0.0))


def r_cat_tinsel(t, u, Z=3.0, sy=300, **kw):
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx, hy + 5, Z + 0.06 * u, 180, sy)
    return kitchen_frame(v, t, cat=True, cat_kw=kw)


def r_clock(t, u, t0, t1, m0, m1, Z=3.0):
    cx, cy, r = PK.CLOCK
    v = view_at(KIT, cx - 10, cy + 20, Z + 0.1 * u, 180, 300)
    k = sm(min(1.0, (t - t0) / (t1 - t0)))
    mins = lerp(m0, m1, k)
    a_m = mins / 60 * 2 * math.pi; a_h = (11 + mins / 60) / 12 * 2 * math.pi
    return kitchen_frame(v, t, cat=False, clock=(a_m, a_h))


# ---------------------------------------------------------------- bathroom
def light_bath(v, warm=1.0):
    bx, by = v.opt(*PK.BULB)
    return Light(amb=(0.98, 1.0, 1.05), keys=[(bx, by, 900, (255, 214, 150), 0.7 * warm)], rim=(1, -0.3, (196, 222, 255), 0.35),
                 grad=(1.06, 0.9))


def foam(FX, v, t, x0=150, x1=560, y=424):
    L = Layer(v.wcam())
    for i in range(int((x1 - x0) / 16)):
        a, b, c, d, e, f_ = NY.SEED[100 + i]
        x = x0 + i * 16 + 6 * a
        r = 9 + 7 * b
        yy = y - 3 - 5 * c + 1.5 * math.sin(t * 1.3 + i)
        F.ell(L, (x, yy), r, r * 0.8, (246, 248, 252), 0, (255, 255, 255), (206, 214, 230))
    F.outline(L, (150, 160, 180)); FX.add(L)


def cat_tub(CH, v, t, lid=0.55, expr='deadpan'):
    x, y, un = CAT_TUB
    F.cat(CH, v.cam(x, y, un), t, 'bath', mouth('cat', t, 2.0), lid, (0.0, 0.0), expr, towel=True)


def steamy(big, v, t, a=0.45, n=10, x0=120, x1=720, y=430, seed=0):
    for i in range(n):
        B.steam(big, v, t, x0 + (x1 - x0) * i / max(1, n - 1), y, -99, n=3, rise=260, size=50, a=a, seed=seed + i * 5)


def bath_frame(v, t, cat=True, cat_kw=None, valera=None, valera_front=True, duck=True, steam_a=0.35, fw=None, spray=False,
               light=None):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    if fw is not None:                                                                   # fireworks flashing in the window
        wx, wy = v.opt(1135, 130)
        c = NY.BULBS[int(fw) % 5]; k = 0.5 + 0.5 * math.sin(fw * 6.0)
        fx.glow(big, wx, wy, 380 * v.Z, c, 0.35 * k)
    if cat: cat_tub(CH, v, t, **(cat_kw or {}))
    if valera and not valera_front: valera(CH, v)
    CH.comp(big, light or light_bath(v))
    K.occlude(big, v, TUB, TUBXY)
    if cat or duck: foam(FX, v, t)
    if duck:
        L = Layer(v.wcam()); B.duck(L, 505, 410, 4.2, t); F.outline(L); FX.add(L)
    if spray: B.spray(FX, v, t, PK.SHOWER, spread=60, drop=260, n=90)
    FX.comp(big)
    if valera and valera_front:
        CH2 = Chars(); valera(CH2, v); CH2.comp(big, light or light_bath(v))
    if steam_a > 0: steamy(big, v, t, steam_a)
    fx.vignette(big, 0.3)
    return big


def r_tap(t, u):
    v = view_at(BATH, FAUCET[0] - 20, FAUCET[1] - 10, 3.0 + 0.1 * u, 180, 300)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    k = t - 7.45
    L = Layer(v.wcam())
    if k < 0.55:                                                                          # coughing: spits of air and droplets
        for i in range(6):
            a, b, c, d, e, f_ = NY.SEED[i]
            if (k * 9 + a * 3) % 1 < 0.5:
                F.dot(L, (FAUCET[0] - 6 - 30 * b * ((k * 7 + a) % 1), FAUCET[1] + 6 + 40 * c * ((k * 7 + a) % 1)), (170, 210, 250), 1.8)
    FX.add(L)
    B.jet(FX, v, t, 8.0, (FAUCET[0] - 6, FAUCET[1] + 4), (FAUCET[0] - 30, FAUCET[1] + 70), arc=6, col=(200, 230, 255),
          col2=(236, 248, 255), width=4.0, grow=0.12)
    FX.comp(big)
    B.steam(big, v, t, FAUCET[0] - 30, FAUCET[1] + 40, 8.05, n=7, rise=120, size=24, a=0.6)
    if k < 0.55: B.shake(big, t, 4, 50)
    fx.vignette(big, 0.3)
    return big


def v_floor(CH, v, t, expr='shout', pose=None):
    x, y, un = FLOOR_V
    F.valera(CH, v.cam(x, y, un, flip=True), pose or F.VPOSE['hips'], t, mouth('valera', t), expr, 'towel', hat='ushanka', wet=0.3)


def r_reveal(t, u):
    x, y, un = CAT_TUB
    k = sm((u - 0.35) / 1.2)
    v = view_at(BATH, lerp(420, x, k), lerp(330, y - 40, k), lerp(1.05, 2.5, k), 180, 300)
    big = bath_frame(v, t, cat_kw=dict(lid=0.8 if talk('cat', t) < 0.05 else 0.6), steam_a=0.35)
    if u < 1.0:                                                                           # the door bursts open: steam wall
        a = 0.85 * (1 - sm(u / 1.0))
        big[:] = np.clip(big * (1 - a) + np.array((236, 240, 246)) * a, 0, 255).astype(np.uint8)
    return big


def r_outrage(t, u):
    x, y, un = FLOOR_V
    fx_, fy_ = K.face_w(x, y, un, flip=True, h=20.6)
    v = view_at(BATH, fx_ + 10, fy_ + 16, 2.1 + 0.08 * u, 180, 300)
    return bath_frame(v, t, cat=False, duck=False, valera=lambda CH, v_: v_floor(CH, v_, t, 'shout'), steam_a=0.25)


def r_cat_bath(t, u):
    x, y, un = CAT_TUB
    v = view_at(BATH, x + 6, y - 44, 2.7 + 0.06 * u, 180, 300)
    return bath_frame(v, t, cat_kw=dict(lid=0.75, expr='smug'), steam_a=0.3)


def v_rim(CH, v, t):
    x, y, un = RIM_V
    raise_ = sm((t - 25.8) / 0.4)
    F.valera(CH, v.cam(x, y, un, flip=True), dict(F.VPOSE['sit'], bn=-1), t, mouth('valera', t), 'sad' if raise_ < 0.5 else 'blissful',
             'towel', hat='ushanka', hand_n=F.H(lerp(4.4, 7.0, raise_), lerp(11.5, 14.6, raise_)), prop_n=NY.glass, wet=0.3)


def r_toast(t, u):
    v = view_at(BATH, 428, 330, 1.22 + 0.04 * u, 180, 330)
    return bath_frame(v, t, cat_kw=dict(lid=0.8), valera=lambda CH, v_: v_rim(CH, v_, t), steam_a=0.25, fw=t)


def r_ice(t, u):
    hx, hy = SHOWER_V[0] + 0.9 * PK.B_UNIT, SHOWER_V[1] - 21.2 * PK.B_UNIT
    fx_, fy_ = K.face_w(SHOWER_V[0], SHOWER_V[1], PK.B_UNIT, h=20.6)
    v = view_at(BATH, fx_, fy_, 2.25, 180, 290)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    cold = t >= T_ICE
    F.valera(CH, v.cam(*SHOWER_V, PK.B_UNIT), F.VPOSE['shiver'] if cold else F.VPOSE['stand'], t,
             max(0.5, mouth('valera', t)) if cold else 0.0, 'shout' if cold else 'blissful', 'towel', hat='ushanka',
             cold=0.8 if cold else 0.0, wet=1, breath=not cold)
    CH.comp(big, K.light_cold(v) if cold else light_bath(v))
    if t >= T_ICE - 0.05: B.spray(FX, v, t, PK.SHOWER, spread=60, drop=260, n=90)
    FX.comp(big)
    fx.vignette(big, 0.3)
    if cold: B.shake(big, t, 8, 37)
    return big


def r_cat_washer(t, u):
    x, y, un = CAT_WASH
    v = view_at(BATH, x, y - 11.4 * un + 6, 3.0 + 0.06 * u, 180, 300)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    F.cat(CH, v.cam(x, y, un), t, 'sit', mouth('cat', t, 2.0), 0.55, (0.0, 0.0), tail=0.4)
    L = Layer(v.cam(x, y, un))                                                            # towel turban
    F.ell(L, F.H(0.0, 15.2), 3.3, 1.6, (240, 244, 250), 0, (255, 255, 255), (200, 210, 226))
    F.ell(L, F.H(0.8, 16.5), 1.8, 1.2, (240, 244, 250), 0.4, (255, 255, 255), (200, 210, 226))
    F.outline(L); CH.add(L)
    CH.comp(big, light_bath(v))
    fx.vignette(big, 0.3)
    return big


# ---------------------------------------------------------------- hallway
def hall_frame(v, t, draw=None, antresol_open=0.0, pile=False, pile_exclude=(), steam=True, dust=None):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    if antresol_open > 0:                                                                # doors swing open, dark cavity
        x0, y0, x1, y1 = ANTRESOL
        L = Layer(v.wcam())
        F.poly(L, [(x0 + 6, y0 + 4), (x1 - 6, y0 + 4), (x1 - 6, y1 - 2), (x0 + 6, y1 - 2)], (26, 20, 16))
        k = antresol_open
        mx = (x0 + x1) / 2
        F.poly(L, [(x0, y0), (x0 - 60 * k, y0 - 10 * k), (x0 - 60 * k, y1 + 10 * k), (x0, y1)], (88, 52, 30))
        F.poly(L, [(x1, y0), (x1 + 60 * k, y0 - 10 * k), (x1 + 60 * k, y1 + 10 * k), (x1, y1)], (88, 52, 30))
        F.outline(L); FX.add(L); FX.comp(big); FX = Chars()
    lx, ly = v.opt(650, 60)
    light = Light(amb=(1.0, 0.95, 0.88), keys=[(lx, ly, 1500, (255, 206, 140), 0.7)], rim=(1, -0.3, (255, 236, 200), 0.3))
    if draw: draw(CH, v)
    CH.comp(big, light)
    if pile:
        P = Chars()
        AVA.draw(P, v, 99.0, exclude=pile_exclude)
        P.comp(big, light)
    if steam: B.steam(big, v, t, 1030, 330, -99, n=5, rise=200, size=40, a=0.35)
    if dust is not None and dust > 0:
        for i in range(6):
            B.steam(big, v, t, 560 + 40 * i, 640, -99, n=2, rise=120, size=70, a=0.55 * dust, seed=i * 3)
    fx.vignette(big, 0.3)
    return big


def r_dali(t, u):
    x, y, un = DALI_V
    fx_, fy_ = K.face_w(x, y, un, h=20.6)
    v = view_at(HALL, fx_ + 30, fy_ + 26, 1.9 + 0.1 * u, 180, 300)
    return hall_frame(v, t, lambda CH, v_: F.valera(CH, v_.cam(x, y, un), F.VPOSE['fist'], t, mouth('valera', t),
                                                   'shout' if t < 9.4 else 'blissful', 'home', hand_n=F.H(8.2, 25.0)))


def v_stool(CH, v, t, reach=1.0, expr='shout'):
    x, y, un = STOOL_V
    L = Layer(v.cam(x, y, un)); NY.stool(L, (1000.0, 1000.0), w=3.0, h=(716 - y) / un); F.outline(L); CH.add(L)
    tn = F.H(6.6, 15.0) if expr != 'shock' else F.H(5.0, 24.5)                             # commanding hand / cover up
    tf = F.H(lerp(-3.0, -1.2, reach), lerp(11.0, 28.6, reach))                             # far hand reaches the cupboard
    F.valera(CH, v.cam(x, y, un), F.VPOSE['overhead'], t, mouth('valera', t), expr, 'home', hand_n=tn, hand_f=tf, look=0.0)


def r_hall_ms(t, u):
    v = view_at(HALL, 650, 330, 1.0 + 0.04 * u, 180, 330)
    return hall_frame(v, t, lambda CH, v_: v_stool(CH, v_, t, sm((t - 9.8) / 0.5)))


def r_avalanche(t, u):
    v = view_at(HALL, 650, 360, 1.0, 180, 330)
    open_k = sm((t - T_OPEN) / 0.15)
    fall = sm((t - T_OPEN - 0.3) / 0.45)                                                  # knocked off the stool into the pile
    hat = AVA.landed('ushanka', t)
    def draw(CH, v_):
        if fall <= 0: v_stool(CH, v_, t, 1.0, 'shock')
        else:
            x, y, un = STOOL_V
            F.valera(CH, v_.cam(x, lerp(y, PILE_V[1], fall), un), F.VPOSE['overhead'], t, mouth('valera', t), 'shock', 'home',
                     hat='ushanka' if hat else None, hand_n=F.H(5.0, 24.5), hand_f=F.H(-2.0, 27.0))
        AVA.draw(CH, v_, t, exclude=('ushanka',) if hat else ())
    big = hall_frame(v, t, draw, antresol_open=open_k, dust=sm((t - T_OPEN - 0.55) / 0.3) * (1 - sm((t - T_OPEN - 1.1) / 0.3)))
    if t > T_OPEN + 0.1: B.shake(big, t, 9 if t < T_OPEN + 1.0 else 3, 45)
    return big


def v_pile(CH, v, t, fist=False):
    x, y, un = PILE_V
    pose = F.VPOSE['fist'] if fist else F.VPOSE['stand']
    F.valera(CH, v.cam(x, y, un), pose, t, mouth('valera', t), 'proud', 'home', hat='ushanka',
             prop_n=(lambda L, h: NY.loofah(L, h)) if fist else None)


def r_pile_cu(t, u):
    x, y, un = PILE_V
    fx_, fy_ = K.face_w(x, y, un, h=20.6)
    v = view_at(HALL, fx_ + 6, fy_ + 30, 2.2 + 0.06 * u, 180, 300)
    return hall_frame(v, t, lambda CH, v_: v_pile(CH, v_, t), antresol_open=1.0, pile=True, pile_exclude=('ushanka', 'loofah'),
                      steam=False)


def r_pile_ms(t, u):
    v = view_at(HALL, 660, 420, 1.35 + 0.05 * u, 180, 330)
    return hall_frame(v, t, lambda CH, v_: v_pile(CH, v_, t, fist=True), antresol_open=1.0, pile=True,
                      pile_exclude=('ushanka', 'loofah'))


def r_run(t, u):
    x = lerp(660, 1010, u / 1.05)
    v = view_at(HALL, x + 20, 400, 1.05, 180, 330)
    return hall_frame(v, t, lambda CH, v_: F.valera(CH, v_.cam(x, 716, 15.0), F.vwalk(t, 22, 0.6), t, 0.0, 'shout', 'home',
                                                   hat='ushanka', lean=1.2, prop_n=lambda L, h: NY.loofah(L, h)),
                      antresol_open=1.0, pile=True, pile_exclude=('ushanka', 'loofah'))


# ---------------------------------------------------------------- yard at midnight
BURSTS = [(30.35, 330, 350, 200, 0), (30.6, 520, 505, 150, 2), (30.85, 420, 450, 265, 3), (31.1, 590, 565, 235, 4),
          (31.35, 300, 320, 140, 1), (31.6, 480, 470, 190, 0), (31.85, 380, 400, 120, 2), (32.1, 560, 540, 170, 3)]


def r_yard(t, u):
    v = View(YARD, 250 + 10 * u, 60, 1.0)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    x0, y0, x1, y1 = PK.Y_WINDOW                                                         # Valera's window flickers cold blue
    L = Layer(v.wcam())
    k = 0.5 + 0.5 * math.sin(t * 30)
    F.poly(L, [(x0 + 4, y0 + 4), (x1 - 4, y0 + 4), (x1 - 4, y1 - 4), (x0 + 4, y1 - 4)],
           (int(lerp(150, 210, k)), int(lerp(200, 236, k)), 255))
    FX.add(L)
    lit = NY.fireworks(FX, v, t, BURSTS, 1.3)
    B.falling_snow(FX, v, t, 240, 40, 700, 800, n=70, speed=40)
    FX.comp(big)
    for (bx, by, c, f_) in lit:
        ox, oy = v.opt(bx, by); fx.glow(big, ox, oy, 520, c, 0.5 * f_)
    wx, wy = v.opt((x0 + x1) / 2, (y0 + y1) / 2); fx.glow(big, wx, wy, 220, (170, 220, 255), 0.4)
    fx.vignette(big, 0.3)
    return big


def r_notice(t, u):
    stamp = t >= 34.4
    x0, y0, x1, y1 = PK.NOTICE
    Z = 2.3 + 0.12 * u
    v = view_at(STAIR_S if stamp else STAIR_N, (x0 + x1) / 2, (y0 + y1) / 2 + 10, Z, 180, 300)
    big = v.bg()
    k = 0.85 + 0.15 * math.sin(t * 40) * (1 if (t * 7) % 1 < 0.3 else 0)                # lamp flicker
    fx.grade(big, (k, k, k * 1.03))
    fx.vignette(big, 0.4)
    if stamp and t < 34.6: B.shake(big, t, 10, 50)
    return big


# ---------------------------------------------------------------- shots
SHOTS = [
    (0.00, 1.75, 'hook'), (1.75, 3.25, 'calendar'), (3.25, 4.55, 'trad'), (4.55, 6.40, 'cat_tinsel'), (6.40, 7.45, 'clock'),
    (7.45, 8.40, 'tap'), (8.40, 9.80, 'dali'), (9.80, T_OPEN, 'hall_ms'), (T_OPEN, 13.50, 'avalanche'), (13.50, 15.00, 'pile_cu'),
    (15.00, 16.50, 'pile_ms'), (16.50, T_DOOR, 'run'), (T_DOOR, 20.25, 'reveal'), (20.25, 22.30, 'outrage'),
    (22.30, T_MIDNIGHT, 'cat_bath'), (T_MIDNIGHT, 25.60, 'midnight'), (25.60, 28.10, 'toast'), (28.10, 30.80, 'ice'),
    (30.80, 32.50, 'yard'), (32.50, 33.75, 'cat_washer'), (33.75, DUR + 1, 'notice'),
]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name == 'hook': return r_hook(t, u)
    if name == 'calendar': return r_calendar(t, u)
    if name == 'trad': return r_trad(t, u)
    if name == 'cat_tinsel': return r_cat_tinsel(t, u)
    if name == 'clock': return r_clock(t, u, 6.4, 7.35, 50, 55)
    if name == 'tap': return r_tap(t, u)
    if name == 'dali': return r_dali(t, u)
    if name == 'hall_ms': return r_hall_ms(t, u)
    if name == 'avalanche': return r_avalanche(t, u)
    if name == 'pile_cu': return r_pile_cu(t, u)
    if name == 'pile_ms': return r_pile_ms(t, u)
    if name == 'run': return r_run(t, u)
    if name == 'reveal': return r_reveal(t, u)
    if name == 'outrage': return r_outrage(t, u)
    if name == 'cat_bath': return r_cat_bath(t, u)
    if name == 'midnight':
        big = r_clock(t, u, T_MIDNIGHT, T_MIDNIGHT + 0.25, 59, 60, 3.2)
        c = NY.BULBS[int(t * 3) % 5]; k = max(0.0, math.sin(t * 9))
        fx.glow(big, 540, 200, 900, c, 0.18 * k)
        return big
    if name == 'toast': return r_toast(t, u)
    if name == 'ice': return r_ice(t, u)
    if name == 'yard': return r_yard(t, u)
    if name == 'cat_washer': return r_cat_washer(t, u)
    return r_notice(t, u)


SHOW = K.Show(EPI, 6, ['С ЛЁГКИМ', 'ПАРОМ?!'], hook_t=(0.12, 2.2),
              stickers=[(K.lcd_sticker('23:55', (255, 120, 90)), 6.5, 7.45, 540, 1560),
                        (K.lcd_sticker('00:00', (255, 120, 90)), T_MIDNIGHT + 0.2, 25.6, 540, 1560),
                        (O.sticker('А-А-А!', fg=(170, 220, 255), size=64), 30.95, 32.4, 420, 520)],
              flashes=[T_DOOR, T_ICE], mosaics=[9.80, 30.80, 33.75],
              cap_y={'calendar': 1400, 'hall_ms': 1420, 'avalanche': 1420, 'yard': 1420, 'toast': 1400, 'notice': 1420},
              teaser='СЕЗОН 2?')


def render(t):
    big = render_scene(t)
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
