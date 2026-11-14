"""S01E01 «ОСТАВЛЕН У ДВЕРИ?!» (pilot; 36.5 s, twist at 21.85 s / 60 %, type: «не та дверь» — the answer was two metres away).
Main question (opened at 0 s, closed at ~88 %): will Жора get his parcel?
HOOK: Жора in the open window of his 9th floor, the snow level with the sill, the phone: «ОЗНОБ. Заказ доставлен. Оставлен у двери» —
«Как это — оставлен у двери?! Моя дверь — под снегом!». The seagull: «Дальний Восток. Снега — по девятый этаж. Девятый теперь —
первый.» Жора: «Кыш, баклан! Мы, дальневосточники, — привычные. Откопаю!» — «Я — чайка. Баклан — это ты.» He dives into the drift and
digs down along the facade (the shaft: windows of floors 8…2 go up, баба Нина with seedlings: «Жорик, так курьер же по крышам ходит!» —
«Некогда, баба Нина!»), reaches the buried entrance door: «Двадцать семь метров! И где посылка?!» TWIST: the landing of the 9th floor,
the open roof hatch, the parcel on the doormat of THEIR flat; Ира on the phone: «Жора! Она у нашей двери! Курьер через крышу ходит!» —
«А чего он в окно не постучал?!» (a lump of snow falls on his head) — Витёк over the pit: «Братан, окно — это не адрес. Оцени
доставку!» — «Одна звезда.» — the seagull: «Себе поставь.»
Clue in the first half: баба Нина says it outright, Жора does not listen; the sign «ОЗНОБ ПВЗ → ПО КРЫШАМ» in the yard.
  python3 ep01.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import fx
import atmos as AT
import overlays as O
import stage as ST
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import zamcast as C
from props import zamkit as K
from props import zampix as ZX
from props import mimic as M
from props import rusigns as RS
from props.dibspix import blit
from props.zamkit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T_PLOP

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='zamelo', lang='ru'), promo='ru')
TAB = (C.XTRA, C.EXPR)
FZ = M.Face([(0.0, 'normal'), (4.8, 'outraged'), (7.9, 'cocky'), (9.9, 'proud'), (11.7, 'offended'), (14.4, 'proud'), (18.0, 'cocky'),
             (19.9, 'exhausted'), (21.2, 'outraged'), (22.7, 'shock'), (26.4, 'offended'), (28.8, 'gloomy'), (32.8, 'gloomy')], TAB, seed=3)
FC = M.Face([(0.0, 'chew'), (3.0, 'dry'), (11.4, 'dry'), (33.9, 'dry')], TAB, seed=8)
FI = M.Face([(0.0, 'yelling'), (24.0, 'angry')], TAB, seed=5)
FV = M.Face([(0.0, 'cheerful')], TAB, seed=11)
FN = M.Face([(0.0, 'kind')], TAB, seed=7)
NEAR_ROOM = 0.40                 # depth of the kitchen behind the open window (facade.depth: interior 0.34, wall under the sill 0.56)


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def face(F, who, t, base=(0.7, 0.0), **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), **kw), M.bob(t, m)


def feet_for_head(v, ox, oy, S, head=(3.6, 66.0)):
    """world feet point that puts a hero's head anchor at output (ox, oy) at output scale S (px per sprite px)"""
    return wpt(v, ox - head[0] * S, oy + head[1] * S)


def phone_n(sp, h): C.phone(sp, h)


def shovel_up(sp, h): C.shovel(sp, h, ang=1.3, l=30.0)


def shovel_dig(k):
    """k 0 = blade down in the snow, 1 = lifted with a load"""
    def f(sp, h): C.shovel(sp, h, ang=-1.5 + 0.9 * k, l=30.0, snow=max(0.0, k))
    return f


def dig_pose(t, rate=1.6):
    """the digging cycle: (hand_n, shovel prop, load k, phase) — push down, lift with a load, throw up and back"""
    ph = (t * rate) % 1.0
    k = math.sin(ph * math.pi) ** 2
    hand = (20.0 + 4.0 * k, 30.0 + 26.0 * k)
    return hand, shovel_dig(k), k, ph


def mitten(sp, t=0.0):
    """Жора's red knitted mitten (an insert holding the phone): mitt + thumb + white zigzag cuff"""
    sp.ell(0.0, 7.0, 9.0, 8.0, C.tones(C.MITT), frost=False)
    sp.ell(-7.4, 11.0, 3.2, 4.4, C.tones(C.MITT), frost=False)
    for q in range(9):
        x0 = -8.0 + q * 2.0
        C.thin(sp, (x0, 1.6 + (q % 2) * 1.2), (x0 + 2.0, 1.6 + ((q + 1) % 2) * 1.2), C.WHITE, 0.45)
    sp.sup(0.0, -2.0, 8.6, 2.6, C.tones(C.ALASKA), n=3.0)


def snow_lump(sp, t=0.0): C.snow_pile(sp, 16.0, 7.0)


def parcel_act(sp, t=0.0): C.parcel(sp, 0.0, 0.0, 18.0, 12.0)



# ================================================================== 0: «Дальний Восток.» — CU the seagull on Жора's windowsill
def r_gull(t, u):
    Z = 2.5 * (1 + 0.025 * u)
    cx, cy = 770.0, 420.0
    v = K.V('facade', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 830.0, 477.0 + dy * 0.3, K.WS['facade'] * 3 * v.Z * 0.95, t=t, flip=True, **kw); g.near = 0.62
    kz, _ = face(FZ, 'zhora', t, (0.6, -0.6), hand_n=(18.0, 56.0), prop_n=phone_n)
    z = A(C.zhora, 660.0, 560.0, K.S_of(v, 'facade') * 0.55, t=t, **kz); z.near = NEAR_ROOM
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[z, g], focus=0.62, dof_k=30, t=t, snow_n=50, kick=kick(t, [(0.12, 0.8)]))


# ================================================================== 1: the CUTAWAY — 9 floors under the snow, the door at the very bottom
def zhora_in_window(big, v, t, win, S, look=(0.6, -0.4), F=None, who='zhora', fn=None, kw=None, head=(3.4, 67.0)):
    """draw a hero inside a side-wall window of the cutaway (clipped to the window rect, world px)"""
    x0, y0, x1, y1 = win
    tmp = big.copy()
    S_ = S
    hx, hy = (x0 + x1) / 2, y0 + (y1 - y0) * 0.45
    with ZX.res(ZX.res_for(S_)), ZX.sky_light():
        sp = ZX.Spr(); (fn or C.zhora)(sp, t=t, **(kw or {})); sp.rim(); sp.outline(ZX.INK)
    ox, oy = v.opt(hx, hy)
    blit(tmp, sp, ox - head[0] * S_, oy + head[1] * S_, S_, None, False)
    ax, ay = v.opt(x0, y0); bx, by = v.opt(x1, y1)
    ax, ay, bx, by = int(max(0, ax)), int(max(0, ay)), int(min(big.shape[1], bx)), int(min(big.shape[0], by))
    if ax < bx and ay < by: big[ay:by, ax:bx] = tmp[ay:by, ax:bx]


WIN9 = (290.0, 168.0, 336.0, 224.0)
WIN8 = (290.0, 288.0, 336.0, 346.0)


def measure(big, v, t, k):
    """the dashed «27 М» line from Жора's window down to the buried door, drawn progressively (k 0..1)"""
    x = 392.0
    ya, yb = 205.0, 1150.0
    yk = ya + (yb - ya) * k
    for y in np.arange(ya, yk, 18.0):
        ox, oy = v.opt(x, y); oy2 = v.opt(x, min(yk, y + 10.0))[1]
        if -10 < oy < big.shape[0] + 10:
            big[int(max(0, oy)):int(max(0, min(big.shape[0], oy2))), int(ox) - 5:int(ox) + 5] = (255, 214, 60)
    ox, oy = v.opt(x, yk)
    if 0 < oy < big.shape[0] - 30:
        for i in range(18):
            big[int(oy) + i:int(oy) + i + 2, int(ox) - 18 + i:int(ox) + 18 - i] = (255, 214, 60)


def r_cut(t, u):
    L = CUTS[2] - CUTS[1]
    k = glide(min(1.0, u / (L - 0.35)))
    Z = lerp(1.05, 1.18, k)
    cx, cy = 360.0, lerp(330.0, 960.0, k)
    v = K.V('cutaway', cx, cy, Z)
    S = K.WS['cutaway'] * 3 * v.Z
    def pre(big, _v):
        kz, _ = face(FZ, 'zhora', t, (0.9, 0.4), hand_n=(18.0, 58.0), prop_n=phone_n)
        zhora_in_window(big, v, t, WIN9, S, kw=kz)
        measure(big, v, t, min(1.0, k * 1.05))
    def f(big, _):
        dx, dy = v.opt(309.0, 1060.0)
        if k > 0.85: O.draw_sticker(big, ST_DOOR, t, CUTS[1] + (L - 0.6), CUTS[2], int(dx) + 120, int(dy) - 110)
        lx, ly = v.opt(392.0, lerp(205.0, 1150.0, k))
        if 0.25 < k < 0.95: O.overlay(big, ST_27, int(lx) + 30, int(ly) - ST_27.shape[0] // 2 - 120, 1.0)
    return K.shot('cutaway', K.light_cut, cx, cy, Z, pre=pre, fx_=f, t=t, focus=0.5, dof_k=0, snow_n=40, bloom=(240, 14, 0.25))


# ================================================================== 2: insert — the phone in the red mitten: «Оставлен у двери»
def r_phone(t, u):
    Z = 1.6
    cx, cy = 715.0, 330.0
    def pre(big, _v): big[:] = K.blur(big, 12)
    def f(big, _):
        ph = K.push_screen(t, w=520, h=860, t_push=CUTS[2] + 0.05)
        x0, y0 = 280, 520 + int(10 * math.sin(t * 4))
        O.overlay(big, ph, x0, y0, 1.0)
        sp = ZX.draw(mitten, 22.0, t=t)
        blit(big, sp, x0 + ph.shape[1] // 2 + 40, y0 + ph.shape[0] + 60, 22.0, None, False)
        if ST.LOG[0] is not None: ST.log('card', bbox=(x0, y0, x0 + ph.shape[1], y0 + ph.shape[0]))
    return K.shot('facade', K.light_window, cx, cy, Z, pre=pre, fx_=f, t=t, dof_k=0, snow_n=50, kick=kick(t, [(CUTS[2] + 0.35, 0.9)]))


# ================================================================== 3: CU Жора in the window: «Моя дверь — под снегом!»
def r_zcu(t, u):
    Z = 2.05 * (1 + 0.02 * u)
    cx, cy = 700.0, 380.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade')
    kw, dy = face(FZ, 'zhora', t, (0.4, -0.3), hand_n=(19.0, 52.0 + 2 * math.sin(t * 9)), prop_n=phone_n, frost=0.3)
    wx, wy = feet_for_head(v, 470, 1060 + dy * 10, S, head=(3.4, 67.0))
    z = A(C.zhora, wx, wy, S, t=t, **kw); z.near = NEAR_ROOM
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[z], focus=0.42, dof_k=22, t=t, snow_n=45, kick=kick(t, [(6.55, 0.7)]))


# ================================================================== 4: «Кыш, баклан! … Откопаю!» — MS, Жора shoos the gull, the shovel
def r_kysh(t, u):
    Z = 1.6
    cx, cy = 742.0 + 6 * u, 410.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade')
    shoo = 8.0 < t < 9.2
    up = t > 10.2
    hand = (24.0 + 3.0 * math.sin(t * 16), 62.0) if shoo else ((20.0, 66.0) if up else (18.0, 50.0))
    kw, dy = face(FZ, 'zhora', t, (0.9, -0.3), hand_n=hand, prop_n=shovel_up if up else None)
    z = A(C.zhora, 680.0, 640.0 + dy, S, t=t, **kw); z.near = NEAR_ROOM
    hop = abs(math.sin((t - 8.1) * 9)) * 4 if shoo else 0.0
    kc, _ = face(FC, 'chayka', t, (-0.6, 0.0), wing=1.0 if shoo else 0.0)
    g = A(C.chayka, 838.0, 477.0 - hop, S * K.GULL, t=t, flip=True, **kc); g.near = 0.62
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[z, g], focus=0.45, dof_k=14, t=t, snow_n=55,
                  kick=kick(t, [(10.5, 0.7)]), par=(-4 + 8 * u / 3.8, 0))


# ================================================================== 5: «Я — чайка. Баклан — это ты.» — CU the gull to camera
def r_baklan(t, u):
    Z = 2.9 * (1 + 0.02 * u)
    cx, cy = 820.0, 445.0
    v = K.V('facade', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 852.0, 478.0 + dy * 0.3, K.WS['facade'] * 3 * v.Z * K.GULL, t=t, flip=True, **kw); g.near = 0.62
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[g], focus=0.62, dof_k=34, t=t, snow_n=40)


# ================================================================== 6: he climbs out and digs at the foot of the wall: snow flies
def r_dig(t, u):
    Z = 1.35
    cx, cy = 715.0, 470.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade')
    hand, prop, k, ph = dig_pose(t, 2.4)
    sink = 40.0 * u / (CUTS[7] - CUTS[6])
    kw, dy = face(FZ, 'zhora', t, (0.7, -0.6), hand_n=hand, prop_n=prop)
    z = A(C.zhora, 700.0, 660.0 + sink, S, t=t, **kw); z.near = 0.55
    def f(big, _):
        px_, py_ = v.opt(760.0, 600.0)
        for j in range(3):
            K.puff(big, px_, py_, t, CUTS[6] + j * 0.22, n=14, seed=j + 4, life=0.55, speed=650, px=14)
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[z], pre=hole_dig(u / (CUTS[7] - CUTS[6])), fx_=f, t=t, focus=0.6,
                  dof_k=10, snow_n=60, kick=kick(t, [(CUTS[6] + 0.1, 0.6)]))


def hole_dig(k):
    def f(big, v):
        x, y = 706.0, 556.0
        ox, oy = v.opt(x, y); Rx, Ry = (46 + 30 * k) * 3 * v.Z, (12 + 6 * k) * 3 * v.Z
        yy, xx = np.mgrid[0:big.shape[0], 0:big.shape[1]]
        m = ((xx - ox) / Rx) ** 2 + ((yy - oy) / Ry) ** 2 <= 1
        big[m] = (36, 48, 96)
    return f


# ================================================================== 7: the shaft in the cutaway — slowly past the 8th floor (баба Нина)
def dig_in_shaft(t, feet, Z, cx, cy_off=70.0, rate=1.8, nina=False, fast=False):
    cy = feet - cy_off
    v = K.V('cutaway', cx, cy, Z)
    S = K.WS['cutaway'] * 3 * v.Z
    hand, prop, k, ph = dig_pose(t, rate)
    kw, dy = face(FZ, 'zhora', t, (-0.8, 0.3) if nina else (0.6, -0.6), hand_n=hand, prop_n=prop, sweat=1.0)
    z = A(C.zhora, 388.0, feet + dy, S, t=t, **kw); z.near = 0.99
    def pre(big, _v):
        K.shaft_cut(big, v, feet + 4.0, t)
        if nina:
            kn, _ = face(FN, 'nina', t, (0.9, -0.2))
            zhora_in_window(big, v, t, WIN8, S * 1.25, fn=C.nina, kw=dict(kn, can=False), head=(1.6, 54.0))
    def f(big, _):
        sx, sy = v.opt(400.0, feet - 30.0)
        if k > 0.8 and not fast: K.puff(big, sx + 60, sy - 40, t, t - (ph % 0.3), n=8, seed=int(t * 3), life=0.5, speed=500, px=12)
        if fast: fx.speed_lines(big, t, 0.25)
        n = int(max(1, min(9, 9 - (feet - 262) / 117.0)))
        hrs = 1 if feet < 600 else (2 if feet < 900 else 3)
        O.overlay(big, floor_st(n, hrs), 40, 1500, 1.0)
    return K.shot('cutaway', K.light_cut, cx, cy, Z, acts=[z], pre=pre, fx_=f, t=t, focus=0.9, dof_k=0, snow_n=0, bloom=(240, 14, 0.25))


_FS = {}


def floor_st(n, h):
    key = (n, h)
    if key not in _FS:
        _FS[key] = K.st(f'ЭТАЖ {n} • {h} {"ЧАС" if h == 1 else "ЧАСА"}', fg=(255, 214, 80) if n <= 2 else (255, 255, 255), size=44)
    return _FS[key]


def r_shaft_a(t, u):
    L = CUTS[8] - CUTS[7]
    feet = lerp(300.0, 392.0, glide(u / L))
    return dig_in_shaft(t, feet, 1.75, 362.0, nina=True)


def r_shaft_b(t, u):
    L = CUTS[9] - CUTS[8]
    k = u / L
    feet = lerp(392.0, 1186.0, k * k * (3 - 2 * k))
    return dig_in_shaft(t, feet, 1.5, 365.0, rate=3.0, fast=True)


# ================================================================== 8: the bottom — the buried entrance door, nothing on the step
def r_bottom(t, u):
    Z = lerp(1.12, 1.24, glide(u / 2.7))
    cx, cy = 640.0, 420.0
    v = K.V('door', cx, cy, Z)
    S = K.S_of(v, 'door')
    look = (-0.9, -0.2) if u < 1.0 else ((0.9, -0.2) if u < 1.6 else (0.4, 0.4))
    kw, dy = face(FZ, 'zhora', t, look, frost=1.0, snowcap=0.8, hand_n=(22.0, 34.0), prop_n=shovel_dig(0.0))
    z = A(C.zhora, 520.0, 612.0 + dy, S, t=t, **kw)
    def f(big, _):
        hx, hy = v.opt(545.0, 380.0)
        for i in range(3):                                                 # breath steam
            ph = (t * 0.9 + i / 3) % 1.0
            r = int(14 + ph * 40)
            fx.glow(big, int(hx + 120 + ph * 90), int(hy - 40 - ph * 80), r, (240, 246, 255), 0.25 * (1 - ph))
    return K.shot('door', K.light_pit, cx, cy, Z, acts=[z], fx_=f, t=t, dof_k=12, snow_n=40, par=(-6 + 6 * u / 2.7, 0))


# ================================================================== 9: TWIST — the landing: the parcel at THEIR door, Ира on the phone
def r_twist(t, u):
    Z = lerp(1.12, 1.2, glide(u / 3.8))
    cx, cy = 700.0, 430.0
    v = K.V('landing', cx, cy, Z)
    S = K.S_of(v, 'landing')
    kw, dy = face(FI, 'ira', t, (-0.6, -0.2), hand_n=(-1.0, 57.0), prop_n=lambda sp, h: C.phone(sp, (h[0] - 1.0, h[1] - 3.0)),
                  hand_f=(-14.0, 40.0))
    ira = A(C.ira, 810.0, 626.0 + dy, S, t=t, flip=True, **kw)
    box = A(parcel_act, 650.0, 590.0, S, t=t, rim=None)
    return K.shot('landing', K.light_landing, cx, cy, Z, acts=[box, ira], t=t, dof_k=10, snow_n=18, rays=dict(src=(1040, 30), a=0.28),
                  kick=kick(t, [(TWIST, 1.0)]))


# ================================================================== 10: «А чего он в окно не постучал?!» — up from the pit; PLOP
def r_up(t, u):
    Z = 1.75
    cx, cy = 600.0, 400.0
    v = K.V('door', cx, cy, Z)
    S = K.S_of(v, 'door')
    plop = t >= T_PLOP + 0.18
    kw, dy = face(FZ, 'zhora', t, (0.6, 0.95) if not plop else (0.6, -0.2), frost=1.0, snowcap=0.8 if not plop else 1.6,
                  hand_n=(20.0, 70.0) if not plop else (18.0, 40.0), prop_n=phone_n)
    z = A(C.zhora, 560.0, 640.0 + dy, S, t=t, **kw)
    acts = [z]
    if T_PLOP - 0.3 < t < T_PLOP + 0.18:                                   # the lump falls
        y = lerp(160.0, 300.0, (t - (T_PLOP - 0.3)) / 0.48)
        acts.append(A(snow_lump, 575.0, y, S, t=t, rim=None))
    def f(big, _):
        if plop:
            hx, hy = aout(z, v, 'hat') if hasattr(z, 'last') else (500, 600)
            K.puff(big, hx, hy, t, T_PLOP + 0.18, n=20, seed=5, life=0.5, speed=500, px=14)
    return K.shot('door', K.light_pit, cx, cy, Z, acts=acts, fx_=f, t=t, dof_k=22, snow_n=50,
                  kick=kick(t, [(T_PLOP + 0.18, 1.2)]))


# ================================================================== 11: Витёк over the pit: «Братан, окно — это не адрес. Оцени доставку!»
HOLE = (700.0, 612.0, 90.0, 22.0)


def hole(big, v):
    x, y, rx, ry = HOLE
    ox, oy = v.opt(x, y); Rx, Ry = rx * 3 * v.Z, ry * 3 * v.Z
    yy, xx = np.mgrid[0:big.shape[0], 0:big.shape[1]]
    m = ((xx - ox) / Rx) ** 2 + ((yy - oy) / Ry) ** 2 <= 1
    rim_ = ((xx - ox) / (Rx + 14)) ** 2 + ((yy - oy) / (Ry + 10)) ** 2 <= 1
    big[rim_ & ~m] = (214, 226, 250)
    depth_ = np.clip((yy - (oy - Ry)) / (2 * Ry), 0, 1)
    col = np.array((30, 40, 80), np.float32)[None, None] * (0.7 + 0.3 * depth_[..., None])
    big[m] = col[m].astype(np.uint8)


def r_vitek(t, u):
    Z = 1.55
    cx, cy = 760.0, 470.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade') * 0.95
    kw, dy = face(FV, 'vitek', t, (0.7, -0.6), phone_up=True, hand_n=(14.0, 38.0), lean=0.55)
    vk = A(C.vitek, 812.0, 640.0 + dy, S, t=t, flip=True, **kw)
    vk.near = 0.70
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[vk], pre=hole, t=t, focus=0.70, dof_k=16, snow_n=55,
                  glints=(0, 1400, 1080, 1900))


# ================================================================== 12: «Одна звезда.» — Жора at the bottom, the rating screen
def r_star(t, u):
    Z = 1.75
    cx, cy = 600.0, 400.0
    v = K.V('door', cx, cy, Z)
    S = K.S_of(v, 'door')
    kw, dy = face(FZ, 'zhora', t, (0.9, -0.2), frost=1.0, snowcap=1.5, hand_n=(18.0, 52.0), prop_n=phone_n)
    z = A(C.zhora, 560.0, 640.0 + dy, S, t=t, **kw)
    def f(big, _):
        sc = K.rating_screen(t, stars=1, t_star=CUTS[13] + 0.6, w=480, h=640)
        O.overlay(big, sc, 560, 1000 + int(5 * math.sin(t * 3)), 1.0)
        if ST.LOG[0] is not None: ST.log('card', bbox=(560, 1000, 560 + sc.shape[1], 1000 + sc.shape[0]))
    return K.shot('door', K.light_pit, cx, cy, Z, acts=[z], fx_=f, t=t, dof_k=22, snow_n=40)


# ================================================================== 13: BUTTON — the gull at the edge of the pit: «Себе поставь.»
def r_button(t, u):
    Z = 2.6 * (1 + 0.02 * u)
    cx, cy = 790.0, 575.0
    v = K.V('facade', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 806.0, 624.0 + dy * 0.3, K.WS['facade'] * 3 * v.Z * K.GULL, t=t, flip=True, **kw); g.near = 0.72
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[g], pre=hole, focus=0.72, dof_k=30, t=t, snow_n=40)


ST_DOOR = K.st('ДВЕРЬ ПОДЪЕЗДА ↓', fg=(255, 255, 255), size=40)
ST_27 = K.st('27 М', fg=(255, 214, 80), size=52)
R = [r_gull, r_cut, r_phone, r_zcu, r_kysh, r_baklan, r_dig, r_shaft_a, r_shaft_b, r_bottom, r_twist, r_up, r_vitek, r_star, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 1, ['ОСТАВИЛИ', 'У ДВЕРИ?!'], hook_t=(0.10, 2.5), hook_y=230, hook_size=78,
              stickers=[(K.st('У ДВЕРИ… КВАРТИРЫ!', fg=(255, 110, 150), size=52), 22.85, 25.4, 540, 360),
                        (K.st('ПЛЮХ', fg=(255, 255, 255), size=64), T_PLOP + 0.2, T_PLOP + 0.9, 760, 520)],
              flashes=[TWIST, CUTS[1]], mosaics=[CUTS[7]],
              cap_y={0: 1480, 1: 1380, 2: 1660, 3: 1520, 4: 1480, 5: 1420, 6: 1300, 7: 1240, 8: 1240, 9: 1380, 10: 1150, 11: 1420,
                     12: 1380, 13: 820, 14: 1440})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
