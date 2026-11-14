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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='zamelo', lang='ru'), promo='ru')
TAB = (C.XTRA, C.EXPR)
FZ = M.Face([(0.0, 'outraged'), (3.0, 'normal'), (7.6, 'cocky'), (9.6, 'proud'), (11.4, 'offended'), (14.0, 'proud'), (17.3, 'cocky'),
             (19.1, 'exhausted'), (20.4, 'outraged'), (21.9, 'shock'), (25.6, 'offended'), (27.9, 'gloomy'), (32.0, 'gloomy')], TAB, seed=3)
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


def shovel_up(sp, h): C.shovel(sp, h, ang=1.25, l=26.0)


def shovel_dig(k):
    def f(sp, h): C.shovel(sp, h, ang=-1.4 + 0.5 * k, l=22.0, snow=max(0.0, k))
    return f


def snow_lump(sp, t=0.0): C.snow_pile(sp, 16.0, 7.0)


def parcel_act(sp, t=0.0): C.parcel(sp, 0.0, 0.0, 18.0, 12.0)


# ================================================================== 0: HOOK — CU Жора in the window, the push on the phone
def r_hook(t, u):
    Z = 1.32
    cx, cy = 712.0, 352.0 - 6.0 * u
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade')
    kw, dy = face(FZ, 'zhora', t, (0.5, -0.5), hand_n=(18.0, 58.0 + 1.5 * math.sin(t * 9)), prop_n=phone_n, frost=0.3)
    wx, wy = feet_for_head(v, 430, 1120 + dy * 8, S)
    z = A(C.zhora, wx, wy, S, t=t, **kw); z.near = NEAR_ROOM
    def f(big, _):
        ph = K.push_screen(t, w=440, h=720, t_push=0.05)
        O.overlay(big, ph, 620, 700 + int(6 * math.sin(t * 3)), 1.0)
        if ST.LOG[0] is not None: ST.log('card', bbox=(620, 700, 620 + ph.shape[1], 700 + ph.shape[0]))
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[z], focus=0.42, dof_k=18, fx_=f, t=t, kick=kick(t, [(0.3, 0.8)]),
                  snow_n=50, par=(-6 + 6 * u, 0))


# ================================================================== 1: «Дальний Восток.» — the buried town, the volcano
def r_vostok(t, u):
    Z = lerp(1.18, 1.02, glide(u / 1.35))
    cx, cy = lerp(780.0, 840.0, u / 1.35), 380.0
    def f(big, _):
        x = lerp(-200, 1200, u / 1.35); y = 520 + 40 * math.sin(u * 4)
        sp = ZX.draw(C.chayka, 6.0, t=t, fly=True, expr='dry')
        blit(big, sp, x, y, 6.0, None, False)
    return K.shot('yard', K.light_morning, cx, cy, Z, fx_=f, t=t, focus=0.55, dof_k=10, par=(-12 + 18 * u / 1.35, 0), snow_n=70,
                  glints=(0, 1300, 1080, 1900))


# ================================================================== 2: «Снега — по девятый этаж.» — tilt down the СНЕГОМЕР
def r_etazh(t, u):
    Z = 1.05
    cx, cy = 850.0, lerp(250.0, 400.0, glide(u / 1.7))
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade')
    kw, dy = face(FZ, 'zhora', t, (0.6, -0.6), hand_n=(18.0, 56.0), prop_n=phone_n)
    z = A(C.zhora, 690.0, 640.0 + dy, S, t=t, **kw); z.near = NEAR_ROOM
    def f(big, _):
        if u > 0.9:
            sx, sy = v.opt(946.0, 470.0)
            O.draw_sticker(big, ST_9, t, CUTS[2] + 0.9, CUTS[3], 540, 1000)
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[z], fx_=f, t=t, focus=0.55, dof_k=10, snow_n=60, par=(4, 0),
                  glints=(0, 1500, 1080, 1900))


# ================================================================== 3: «Девятый теперь — первый.» — CU the seagull on the sill
def r_pervyi(t, u):
    Z = 2.2 * (1 + 0.015 * u)
    cx, cy = 780.0, 430.0
    v = K.V('facade', cx, cy, Z)
    S = 3.4 * 3 * v.Z
    kw, dy = face(FC, 'chayka', t, (0.3, 0.0), chew=0.0)
    g = A(C.chayka, 800.0, 476.0 + dy * 0.3, S, t=t, **kw); g.near = 0.62
    kz, _ = face(FZ, 'zhora', t, (0.9, -0.3), hand_n=(18.0, 56.0), prop_n=phone_n)
    z = A(C.zhora, 640.0, 640.0, K.S_of(v, 'facade'), t=t, **kz); z.near = NEAR_ROOM
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[z, g], focus=0.62, dof_k=26, t=t, snow_n=45)


# ================================================================== 4: «Кыш, баклан! … Откопаю!» — MS, Жора shoos the gull, the shovel
def r_kysh(t, u):
    Z = 1.42
    cx, cy = 742.0 + 6 * u, 402.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade')
    shoo = 7.7 < t < 8.9
    up = t > 9.9
    hand = (24.0 + 3.0 * math.sin(t * 16), 62.0) if shoo else ((20.0, 66.0) if up else (18.0, 50.0))
    kw, dy = face(FZ, 'zhora', t, (0.9, -0.3), hand_n=hand, prop_n=shovel_up if up else None)
    z = A(C.zhora, 670.0, 640.0 + dy, S, t=t, **kw); z.near = NEAR_ROOM
    hop = abs(math.sin((t - 7.8) * 9)) * 6 if shoo else 0.0
    kc, _ = face(FC, 'chayka', t, (-0.6, 0.0), wing=1.0 if shoo else 0.0)
    g = A(C.chayka, 846.0, 476.0 - hop, 3.4 * 3 * v.Z, t=t, flip=True, **kc); g.near = 0.62
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[z, g], focus=0.45, dof_k=14, t=t, snow_n=55,
                  kick=kick(t, [(10.2, 0.7)]), par=(-4 + 8 * u / 3.8, 0))


# ================================================================== 5: «Я — чайка. Баклан — это ты.» — CU the gull to camera
def r_baklan(t, u):
    Z = 2.5 * (1 + 0.02 * u)
    cx, cy = 820.0, 440.0
    v = K.V('facade', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 862.0, 478.0 + dy * 0.3, 3.4 * 3 * v.Z, t=t, flip=True, **kw); g.near = 0.62
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[g], focus=0.62, dof_k=34, t=t, snow_n=40)


# ================================================================== 6: the dive — over the sill, head first into the drift
def r_dive(t, u):
    Z = 1.05
    cx, cy = 715.0, 410.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade')
    k = min(1.0, u / 0.75)
    if k < 1.0:
        x = lerp(680.0, 720.0, k); y = lerp(560.0, 700.0, k) - 260 * math.sin(math.pi * k)
        rot = -170.0 * glide(k)
        kw, _ = face(FZ, 'zhora', t, (0.6, -0.8), hand_n=(26.0, 76.0), prop_n=shovel_up)
        z = A(C.zhora, x, y, S, t=t, rot=rot, pivot=(0.0, 40.0), **kw)
        z.near = NEAR_ROOM if k < 0.25 else 0.70
        acts = [z]
    else:                                                                  # only the valenki stick out of the drift, kicking
        kw, _ = face(FZ, 'zhora', t, (0.6, -0.8))
        z = A(C.zhora, 720.0, 560.0 + 6 * math.sin(t * 20), S, t=t, rot=180.0, pivot=(0.0, 0.0), **kw)
        z.near = 0.62
        acts = [z]
    def f(big, _):
        px, py = v.opt(720.0, 600.0)
        K.puff(big, px, py, t, CUTS[6] + 0.75 * 1.0, n=24, seed=3, life=0.7, speed=700, px=16)
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=acts, fx_=f, t=t, focus=0.6, dof_k=10, snow_n=60,
                  kick=kick(t, [(CUTS[6] + 0.75, 1.1)]))


# ================================================================== 7: the SHAFT — down along the facade, floors 8 … 2
def scene_nina(sub, t):
    sub[:] = (110, 90, 130)
    sub[-60:] = (90, 70, 60)
    sp = ZX.draw(C.nina, 7.0, t=t, expr=FN.speak(t, mouth('nina', t)), mouth_=mouth('nina', t), blink=FN.blink(t), look=(-0.6, -0.4))
    blit(sub, sp, 300, sub.shape[0] + 160, 7.0, None, True)
    lamp = (190, 90, 255)
    sub[:24] = lamp
    sp2 = ZX.draw(C.seedlings, 6.0, t=t)
    blit(sub, sp2, 120, sub.shape[0] - 6, 6.0, None, False)


def scene_sign(lines, bg=(70, 80, 110)):
    img = RS.plate(110, 40, lines, bg=(246, 242, 226), fg=(30, 30, 40), border=(200, 40, 40))
    def f(sub, t):
        sub[:] = bg
        h, w = sub.shape[:2]
        im = img
        if im.shape[1] > w - 40:
            fk = (w - 40) / im.shape[1]
            im = np.array(Image.fromarray(im).resize((int(im.shape[1] * fk), int(im.shape[0] * fk)), Image.NEAREST))
        O.overlay(sub, im, (w - im.shape[1]) // 2, (h - im.shape[0]) // 2, 1.0)
    return f


def scene_cat(sub, t):
    sub[:] = (200, 160, 110)
    h, w = sub.shape[:2]
    q = 10
    cat = ['..X...X..', '..XX.XX..', '.XXXXXXX.', '.XOXXXOX.', '.XXXXXXX.', '..XXXXX..', '.XXXXXXX.', 'XXXXXXXXX', 'XXXXXXXXX']
    for r, row in enumerate(cat):
        for c, ch in enumerate(row):
            col = (60, 60, 70) if ch == 'X' else ((250, 220, 60) if ch == 'O' else None)
            if col: sub[h - 30 - (len(cat) - r) * q:h - 30 - (len(cat) - r - 1) * q, w // 2 - 45 + c * q:w // 2 - 35 + c * q] = col


SCENES = {8: scene_nina, 7: scene_cat, 6: scene_sign(['НЕ КОПАТЬ!', 'ТУТ СПЯТ']), 5: scene_sign(['ПРОДАМ', 'ГАРАЖ. ГДЕ-ТО']),
          4: scene_sign(['ЖОРА,', 'ВЕРНИ ЛОПАТУ']), 3: scene_cat, 2: scene_sign(['ТУТ БЫЛ', 'СНЕГ 1987'])}


def r_shaft(t, u):
    L = CUTS[8] - CUTS[7]
    k = u / L
    floors = 0.30 + 0.25 * min(1.0, k / 0.38) + max(0.0, k - 0.38) / 0.62 * 5.9 * (0.6 + 0.4 * max(0.0, k - 0.38) / 0.62)
    big = K.shaft(t, floors, SCENES)
    dig = (t * 2.4) % 1.0
    S = 9.5
    kw, dy = face(FZ, 'zhora', t, (-0.3 if t < 17.4 else 0.6, 0.2 if t < 17.4 else -0.8),
                  hand_n=(22.0, 46.0 + 14.0 * math.sin(dig * 6.28)), prop_n=shovel_dig(max(0.0, math.sin(dig * 6.28))), sweat=1.0)
    with ZX.res(ZX.res_for(S)), ZX.sky_light():
        sp = ZX.Spr(); C.zhora(sp, t=t, **kw); sp.rim(); sp.outline(ZX.INK)
    yy = np.arange(big.shape[0])[:, None]; xx = np.arange(big.shape[1])[None, :]
    floor_ = yy > 1630 + 22 * np.sin(xx / 70.0)
    big[floor_] = (226, 236, 252); big[floor_ & (yy > 1700)] = (200, 214, 244)
    blit(big, sp, 560, 1650 + dy * 6, S, None, False)
    K.puff(big, 760, 1500, t, CUTS[7] + int((t - CUTS[7]) * 2.4) / 2.4, n=10, seed=int(t * 2.4), life=0.4, speed=500, px=12)
    K.snowfall(big, t, n=40, seed=4, speed=1.6)
    AT.juice(big, 1.2, 1.06)
    fx.vignette(big, 0.25)
    return big


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
T_PLOP = 27.95


def r_up(t, u):
    Z = 1.75
    cx, cy = 600.0, 400.0
    v = K.V('door', cx, cy, Z)
    S = K.S_of(v, 'door')
    plop = t >= T_PLOP + 0.18
    kw, dy = face(FZ, 'zhora', t, (0.6, 0.95) if not plop else (0.6, -0.2), frost=1.0, snowcap=0.8 if not plop else 2.2,
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
        sc = K.rating_screen(t, stars=1, t_star=32.6, w=480, h=640)
        O.overlay(big, sc, 560, 1000 + int(5 * math.sin(t * 3)), 1.0)
        if ST.LOG[0] is not None: ST.log('card', bbox=(560, 1000, 560 + sc.shape[1], 1000 + sc.shape[0]))
    return K.shot('door', K.light_pit, cx, cy, Z, acts=[z], fx_=f, t=t, dof_k=22, snow_n=40)


# ================================================================== 13: BUTTON — the gull at the edge of the pit: «Себе поставь.»
def r_button(t, u):
    Z = 2.35 * (1 + 0.02 * u)
    cx, cy = 790.0, 560.0
    v = K.V('facade', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 812.0, 624.0 + dy * 0.3, 3.4 * 3 * v.Z, t=t, flip=True, **kw); g.near = 0.72
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[g], pre=hole, focus=0.72, dof_k=30, t=t, snow_n=40)


ST_9 = K.st('9 ЭТАЖ = 1 ЭТАЖ', fg=(255, 214, 80), size=46)
R = [r_hook, r_vostok, r_etazh, r_pervyi, r_kysh, r_baklan, r_dive, r_shaft, r_bottom, r_twist, r_up, r_vitek, r_star, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 1, ['ОСТАВЛЕН', 'У ДВЕРИ?!'], hook_t=(0.10, 2.9), hook_y=230, hook_size=78,
              stickers=[(K.st('ЭТАЖ 8 • 1 ЧАС', fg=(255, 255, 255), size=46), 15.3, 16.9, 540, 240),
                        (K.st('ЭТАЖ 5 • 2 ЧАСА', fg=(255, 255, 255), size=46), 17.0, 18.0, 540, 240),
                        (K.st('ЭТАЖ 1 • 3 ЧАСА', fg=(255, 214, 80), size=46), 18.1, 19.2, 540, 240),
                        (K.st('У ДВЕРИ… КВАРТИРЫ!', fg=(255, 110, 150), size=52), 22.0, 24.6, 540, 360),
                        (K.st('ПЛЮХ', fg=(255, 255, 255), size=64), 28.15, 28.85, 760, 520)],
              flashes=[TWIST, 14.87], mosaics=[15.20],
              cap_y={0: 1480, 1: 1200, 2: 1250, 3: 1320, 4: 1480, 5: 1420, 6: 1260, 7: 860, 8: 1380, 9: 1150, 10: 1420, 11: 1380,
                     12: 820, 13: 1440})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
