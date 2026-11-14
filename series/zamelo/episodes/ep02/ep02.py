"""S01E02 «СМЕНКУ ЗАБЫЛ!» (43.6 s, twist at 24.6 s / 56 %, type: «ошибка решила дело»).
Main question: will they let Тёма into school without his indoor shoes?
HOOK: the seagull close up — «Дальний Восток. В школу тут ездят прямо из окна. С девятого этажа. На ледянке.» — the slope from the
9th-floor windows down to the school, Тёма flies down on his sled. Ира out of the window: «Тёма, стой! Ты ж сменку забыл!…» Жора grabs
the string bag from the hook OUTSIDE the window (clue: two identical bags — the slippers inside, the frozen pelmeni outside, the
Siberian «freezer»), in his alaska, family shorts and valenki sits into a zinc basin: «Спокойно, мать… Щас догоню!» — the gull: «Сорок
два года. В трусах. На тазике.» Down the slope, he stops on the red of a traffic light sticking out of the snow. The school hall in the
snow tunnel: the watchwoman: «Без сменки не пущу.» — «Стоять! Вот она, сменка!» TWIST: «Пап. А почему она мороженая? Это ж пельмени.»
— «Пельмени — это не сменка, мужчина. Хотя. А домашние?» — «Жена лепила. Целый килограмм!» — the turnstile beeps green — «Пап, а что,
так можно было?!» — the gull: «Запоминай. Сменка не нужна. Нужен килограмм пельменей.»
  python3 ep02.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
import stage as ST
from scene import lerp
from cam25 import glide, kick
from episode import Episode
from props import zamcast as C
from props import zamkit as K
from props import zampix as ZX
from props import mimic as M
from props.dibspix import blit
from props.zamkit import A
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

K.DAY = 121
EPI = Episode('ep02', VOICE, DUR, FPS, colors=dict(K.COL, tyoma=(120, 220, 255), valya=(255, 200, 120)), slug=SLUG,
              endcard=dict(style='zamelo', lang='ru'), promo='ru')
TAB = (C.XTRA, C.EXPR)
FZ = M.Face([(0.0, 'normal'), (9.2, 'cocky'), (15.9, 'yelling'), (20.8, 'proud'), (23.8, 'shock'), (27.4, 'nervous'), (31.6, 'proud'),
             (36.0, 'cocky')], TAB, seed=3)
FC = M.Face([(0.0, 'dry')], TAB, seed=8)
FI = M.Face([(0.0, 'yelling')], TAB, seed=5)
FT = M.Face([(0.0, 'cheer'), (19.0, 'sad'), (23.8, 'stunned'), (27.4, 'nervous'), (35.2, 'cheer'), (36.1, 'shock')], TAB, seed=12)
FVA = M.Face([(0.0, 'deadpan'), (27.4, 'glare'), (29.7, 'sly'), (31.7, 'smug')], TAB, seed=14)
NEAR_ROOM = 0.40
T_SNIFF = 29.6


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def face(F, who, t, base=(0.7, 0.0), **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), **kw), M.bob(t, m)


def bag(kind):
    def f(sp, h): C.avoska(sp, (h[0] + 0.6, h[1] + 1.0), kind)
    return f


def bag_act(kind):
    def f(sp, t=0.0): C.avoska(sp, (0.0, 0.0), kind, t)
    return f


def slope_xy(k):
    """the sled track on the slope (world px of slope.png): k 0 = the open window at the top .. 1 = the school tunnel"""
    pts = [(480.0, 290.0), (450.0, 400.0), (380.0, 580.0), (320.0, 760.0), (300.0, 940.0), (330.0, 1090.0), (352.0, 1150.0)]
    k = min(1.0, max(0.0, k)) * (len(pts) - 1)
    i = min(len(pts) - 2, int(k)); f = k - i
    return lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)


# ================================================================== 0: «Дальний Восток.» — CU the seagull on the windowsill
def r_gull(t, u):
    Z = 2.5 * (1 + 0.025 * u)
    cx, cy = 770.0, 420.0
    v = K.V('facade', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 830.0, 477.0 + dy * 0.3, K.WS['facade'] * 3 * v.Z * 0.95, t=t, flip=True, **kw); g.near = 0.62
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[g], focus=0.62, dof_k=30, t=t, snow_n=50, kick=kick(t, [(0.12, 0.8)]))


# ================================================================== 1: the slope — from the 9th-floor window down to the school; Тёма flies
def r_slope(t, u):
    L = CUTS[2] - CUTS[1]
    k = glide(min(1.0, u / L))
    x, y = slope_xy(k * 0.98)
    Z = lerp(0.57, 0.85, k)
    cy_ = lerp(640.0, max(560.0, y), k)
    v = K.V('slope', 360.0, cy_, Z)
    S = K.WS['slope'] * 3 * v.Z * 2.6
    kw, _ = face(FT, 'tyoma', t, (0.8, 0.4), sit=1.0)
    ty = A(C.tyoma, x, y, S, t=t, rot=-12.0 * (1 - k), **kw); ty.near = 0.99
    sl = A(C.ledyanka, x - 2, y + 2, S, t=t, rim=None, rot=-12.0 * (1 - k)); sl.near = 0.99
    def f(big, _):
        ox, oy = v.opt(x, y)
        K.puff(big, ox - 40, oy, t, t - ((t * 4) % 0.25), n=6, seed=int(t * 4), life=0.3, speed=300, px=10)
    return K.shot('slope', K.light_morning, 360.0, cy_, Z, acts=[sl, ty], fx_=f, t=t, focus=0.9, dof_k=0, snow_n=50,
                  glints=(0, 600, 1080, 1900))


# ================================================================== 2: Ира out of the window: «Тёма, стой! Ты ж сменку забыл!…»
def r_ira(t, u):
    Z = 1.55
    cx, cy = 700.0, 395.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade')
    kw, dy = face(FI, 'ira', t, (0.9, -0.3), hand_n=(13.0, 60.0 + 3 * math.sin(t * 10)), point=True)
    ira = A(C.ira, 690.0, 615.0 + dy, S, t=t, **kw); ira.near = NEAR_ROOM
    inner = A(bag_act('smenka'), 612.0, 300.0, S, t=t, rim=None); inner.near = NEAR_ROOM - 0.02
    outer = A(bag_act('pelmeni'), 560.0, 330.0, S, t=t); outer.near = 0.60
    return K.shot('facade', K.light_window, cx, cy, Z, acts=[inner, ira, outer], focus=0.45, dof_k=14, t=t, snow_n=55,
                  par=(-4 + 8 * u / 4.3, 0))


# ================================================================== 3: Жора grabs the OUTER bag (pelmeni) — in the alaska, family shorts, valenki
def r_grab(t, u):
    Z = 1.18
    cx, cy = 690.0, 430.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade') * 0.95
    grabbed = u > 1.1
    hf = (-12.0, 70.0) if not grabbed else (-15.0, 30.0)
    kw, dy = face(FZ, 'zhora', t, (-0.6, 0.3) if not grabbed else (0.8, -0.2), undies=True, hand_f=hf,
                  prop_f=bag('pelmeni') if grabbed else None, hand_n=(22.0, 34.0))
    z = A(C.zhora, 640.0, 628.0 + dy, S, t=t, **kw); z.near = 0.72
    acts = [z]
    if not grabbed:
        o = A(bag_act('pelmeni'), 560.0, 330.0, S, t=t); o.near = 0.60; acts.insert(0, o)
    inner = A(bag_act('smenka'), 612.0, 300.0, S, t=t, rim=None); inner.near = NEAR_ROOM - 0.02
    tz = A(C.taz, 760.0, 640.0, S, t=t); tz.near = 0.74
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[inner] + acts + [tz], focus=0.7, dof_k=10, t=t, snow_n=55,
                  kick=kick(t, [(CUTS[3] + 1.1, 0.6)]))


# ================================================================== 4: «Сорок два года. В трусах. На тазике.» — Жора in the basin at the top
def r_taz(t, u):
    Z = 2.6
    x, y = 470.0, 300.0
    v = K.V('slope', x + 10, y - 40, Z)
    S = K.WS['slope'] * 3 * v.Z * 1.25
    kw, dy = face(FZ, 'zhora', t, (0.8, 0.3), undies=True, sit=1.0, hand_f=(-12.0, 30.0), prop_f=bag('pelmeni'), hand_n=(22.0, 40.0))
    tz = A(C.taz, x + 6, y + 4, S * 1.1, t=t); tz.near = 0.99
    z = A(C.zhora, x, y + sitoff(S, v) + dy * 0.3, S, t=t, **kw); z.near = 0.99
    kc, _ = face(FC, 'chayka', t, (-0.5, 0.0))
    g = A(C.chayka, x + 52, y + 12, S * K.GULL * 1.3, t=t, flip=True, **kc); g.near = 0.99
    return K.shot('slope', K.light_morning, x + 10, y - 40, Z, acts=[z, tz, g], t=t, focus=0.9, dof_k=0, snow_n=45)


# ================================================================== 5-6: the ride down; the traffic light: red — he brakes, green — go
def sitoff(S, v):
    """world px that sinks a seated Жора into the basin (9 hero sprite px)"""
    return 9.0 * S / (3 * v.Z)


def zhora_taz(t, x, y, S, rot=0.0, look=(0.9, 0.4), shout=True, v=None):
    kw, dy = face(FZ, 'zhora', t, look, undies=True, sit=1.0, hand_f=(-12.0, 52.0), prop_f=bag('pelmeni'), hand_n=(22.0, 60.0))
    tz = A(C.taz, x + 6, y + 4, S * 1.1, t=t, rot=rot); tz.near = 0.99
    z = A(C.zhora, x, y + sitoff(S, v), S, t=t, rot=rot, **kw); z.near = 0.99
    return [z, tz]


def r_ride_a(t, u):
    L = CUTS[6] - CUTS[5]
    k = lerp(0.03, 0.42, u / L)
    x, y = slope_xy(k)
    Z = 1.9
    v = K.V('slope', x, y - 40, Z)
    S = K.WS['slope'] * 3 * v.Z * 1.25
    acts = zhora_taz(t, x, y, S, rot=-14.0, v=v)
    def f(big, _):
        ox, oy = v.opt(x, y)
        K.puff(big, ox - 60, oy + 10, t, t - ((t * 5) % 0.2), n=8, seed=int(t * 5), life=0.3, speed=380, px=12)
        fx.speed_lines(big, t, 0.22)
    return K.shot('slope', K.light_morning, x, y - 40, Z, acts=acts, fx_=f, t=t, focus=0.9, dof_k=0, snow_n=60)


LIGHT = (564.0, 708.0)


def r_ride_b(t, u):
    L = CUTS[7] - CUTS[6]
    t_green = CUTS[6] + 0.75
    if t < t_green:
        k = glide(min(1.0, u / 0.45)); x, y = lerp(400.0, 486.0, k), lerp(640.0, 700.0, k)
    else:
        k = ((t - t_green) / (L - 0.75)) ** 1.6; x, y = lerp(486.0, 420.0, k), lerp(700.0, 900.0, k)
    Z = 1.4
    v = K.V('slope', 480.0, 720.0, Z)
    S = K.WS['slope'] * 3 * v.Z * 1.25
    acts = zhora_taz(t, x, y, S, rot=-10.0, look=(0.6, 0.9), v=v)
    green = t >= t_green
    def f(big, _):
        lx, ly = v.opt(*LIGHT)
        for i, (dy_, col, on) in enumerate(((-26, (255, 60, 50), not green), (-6, (255, 200, 40), False), (14, (60, 255, 120), green))):
            if on: fx.glow(big, int(lx), int(ly + dy_ * 3 * v.Z / 3), 60, col, 0.9)
        if not green and u < 0.6:
            ox, oy = v.opt(x, y)
            K.puff(big, ox + 40, oy, t, CUTS[6] + 0.05, n=18, seed=2, life=0.5, speed=420, px=12)
    st_ = ST_RED if not green else ST_GREEN
    def f2(big, _):
        f(big, _)
        O.draw_sticker(big, st_, t, CUTS[6] + (0.1 if not green else 0.75), CUTS[7], 760, 520)
    return K.shot('slope', K.light_morning, 480.0, 720.0, Z, acts=acts, fx_=f2, t=t, focus=0.9, dof_k=0, snow_n=55,
                  kick=kick(t, [(CUTS[6] + 0.08, 0.8)]))


# ================================================================== 7: the school hall: Тёма at the turnstile, тётя Валя: «Без сменки не пущу.»
def valya_act(t, v, x=1000.0, y=470.0, base=(-0.7, 0.0), knit=1.0, z=1.0, **extra):
    S = K.S_of(v, 'school') * z
    sniff = min(1.0, max(0.0, (t - T_SNIFF) / 0.3)) if t >= T_SNIFF else 0.0
    kw, dy = face(FVA, 'valya', t, base, knit=knit, sniff=sniff, **extra)
    a = A(C.valya, x, y + dy, S, t=t, flip=True, **kw); a.near = 0.99
    return a


def tyoma_act(t, v, x, y, base=(0.7, 0.0), z=1.0, flip=False, **extra):
    S = K.S_of(v, 'school') * z
    kw, dy = face(FT, 'tyoma', t, base, **extra)
    a = A(C.tyoma, x, y + dy, S, t=t, flip=flip, **kw); a.near = 0.99
    return a


def r_hall(t, u):
    Z = 0.95
    cx, cy = 830.0, 380.0
    v = K.V('school', cx, cy, Z)
    ty = tyoma_act(t, v, 680.0, 640.0, (0.8, 0.1), z=0.92)
    va = valya_act(t, v)
    return K.shot('school', K.light_morning, cx, cy, Z, acts=[ty, va], t=t, focus=0.8, dof_k=8, snow_n=0, par=(-4 + 6 * u / 1.85, 0))


# ================================================================== 8: Жора bursts out of the snow tunnel in the basin: «Стоять! Вот она, сменка!»
def r_burst(t, u):
    Z = 1.05
    cx, cy = 600.0, 400.0
    v = K.V('school', cx, cy, Z)
    S = K.S_of(v, 'school') * 0.92
    k = glide(min(1.0, u / 0.9))
    x = lerp(220.0, 520.0, k)
    up = u > 1.0
    kw, dy = face(FZ, 'zhora', t, (0.9, 0.0), undies=True, sit=1.0, hand_f=(-10.0, 72.0) if up else (-12.0, 40.0),
                  prop_f=bag('pelmeni'), hand_n=(22.0, 40.0))
    tz = A(C.taz, x + 6, 648.0, S * 1.1, t=t); tz.near = 0.99
    z = A(C.zhora, x, 644.0 + sitoff(S, v) + dy, S, t=t, **kw); z.near = 0.99
    ty = tyoma_act(t, v, 720.0, 640.0, (-0.8, 0.1), z=0.92, flip=True)
    def f(big, _):
        ox, oy = v.opt(x, 650.0)
        if u < 1.0: K.puff(big, ox - 80, oy, t, t - ((t * 5) % 0.2), n=10, seed=int(t * 5), life=0.35, speed=420, px=12)
    return K.shot('school', K.light_morning, cx, cy, Z, acts=[ty, z, tz], fx_=f, t=t, focus=0.85, dof_k=6, snow_n=0,
                  kick=kick(t, [(CUTS[8] + 0.9, 1.0)]))


# ================================================================== 9: TWIST — Тёма opens the bag: frozen pelmeni
def r_open(t, u):
    Z = 2.1
    cx, cy = 700.0, 470.0
    v = K.V('school', cx, cy, Z)
    open_ = t >= TWIST - 0.2
    ty = tyoma_act(t, v, 690.0, 690.0, (0.6, 0.8) if open_ else (0.6, 0.3), z=0.95, hand_n=(10.0, 34.0),
                   prop_n=bag('pelmeni'))
    def f(big, _):
        if open_:
            fx.glow(big, 760, 1290, 140, (220, 240, 255), 0.35)
            K.puff(big, 760, 1250, t, TWIST, n=14, seed=7, life=0.7, speed=260, px=8, col=(230, 244, 255))
        if TWIST - 0.15 <= t < TWIST + 1.5:                                 # insert: the bag close up — frozen pelmeni in frost
            big[:] = K.blur(big, 10)
            sp = ZX.draw(bag_act('pelmeni'), 30.0, t=t)
            blit(big, sp, 540, 1380, 30.0, None, False)
            fx.glow(big, 540, 1050, 260, (220, 240, 255), 0.25)
    return K.shot('school', K.light_morning, cx, cy, Z, acts=[ty], fx_=f, t=t, focus=0.95, dof_k=26, snow_n=0)


# ================================================================== 10: тётя Валя: «Пельмени — это не сменка, мужчина. Хотя. А домашние?»
def r_valya(t, u):
    Z = 2.15 * (1 + 0.02 * u)
    cx, cy = 990.0, 330.0
    v = K.V('school', cx, cy, Z)
    va = valya_act(t, v, 1000.0, 470.0, (-0.7, 0.2) if t < T_SNIFF else (-0.6, 0.5), knit=0.0 if t > T_SNIFF else 1.0)
    return K.shot('school', K.light_morning, cx, cy, Z, acts=[va], t=t, focus=0.95, dof_k=28, snow_n=0)


# ================================================================== 11: Жора proud: «Ну а какие ещё? Жена лепила. Целый килограмм!»
def r_proud(t, u):
    Z = 2.0
    cx, cy = 560.0, 420.0
    v = K.V('school', cx, cy, Z)
    S = K.S_of(v, 'school') * 0.92
    kw, dy = face(FZ, 'zhora', t, (0.9, 0.0), undies=True, sit=1.0, hand_n=(22.0, 64.0), prop_n=bag('pelmeni'))
    z = A(C.zhora, 520.0, 644.0 + sitoff(S, v) + dy, S, t=t, **kw); z.near = 0.99
    tz = A(C.taz, 526.0, 648.0, S * 1.1, t=t); tz.near = 0.99
    return K.shot('school', K.light_morning, cx, cy, Z, acts=[z, tz], t=t, focus=0.95, dof_k=26, snow_n=0)


# ================================================================== 12: the bag goes under the desk, the turnstile beeps green, Тёма walks in
def r_pass(t, u):
    Z = 0.95
    cx, cy = 830.0, 380.0
    v = K.V('school', cx, cy, Z)
    x = lerp(680.0, 860.0, glide(min(1.0, u / 0.85)))
    ty = tyoma_act(t, v, x, 640.0, (0.8, 0.0), z=0.92, hand_n=(8.0, 26.0))
    va = valya_act(t, v, knit=0.0, hand_n=(-6.0, 6.0))
    def f(big, _):
        lx, ly = v.opt(712.0, 432.0)
        fx.glow(big, int(lx), int(ly), 40, (60, 255, 120), 0.9)
    return K.shot('school', K.light_morning, cx, cy, Z, acts=[ty, va], fx_=f, t=t, focus=0.8, dof_k=8, snow_n=0)


# ================================================================== 13: Тёма: «Пап, а что, так можно было?!»
def r_wow(t, u):
    Z = 2.0
    cx, cy = 820.0, 470.0
    v = K.V('school', cx, cy, Z)
    ty = tyoma_act(t, v, 830.0, 690.0, (-0.9, 0.1), z=0.95, flip=True)
    return K.shot('school', K.light_morning, cx, cy, Z, acts=[ty], t=t, focus=0.95, dof_k=26, snow_n=0)


# ================================================================== 14: BUTTON — the gull on the turnstile: «Запоминай…»
def r_button(t, u):
    Z = 2.4 * (1 + 0.02 * u)
    cx, cy = 690.0, 380.0
    v = K.V('school', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 700.0, 392.0 + dy * 0.3, K.S_of(v, 'school') * K.GULL * 1.4, t=t, flip=True, **kw); g.near = 0.99
    def f(big, _): O.overlay(big, ST_KG, (1080 - ST_KG.shape[1]) // 2, 1500, min(1.0, (t - 40.0) / 0.2) if t > 40.0 else 0.0)
    return K.shot('school', K.light_morning, cx, cy, Z, acts=[g], fx_=f, t=t, focus=0.99, dof_k=30, snow_n=0)


ST_RED = K.st('КРАСНЫЙ!', fg=(255, 80, 70), size=56)
ST_GREEN = K.st('ЗЕЛЁНЫЙ!', fg=(90, 255, 130), size=56)
ST_KG = K.st('СМЕНКА = 1 КГ ПЕЛЬМЕНЕЙ', fg=(255, 214, 80), size=40)
R = [r_gull, r_slope, r_ira, r_grab, r_taz, r_ride_a, r_ride_b, r_hall, r_burst, r_open, r_valya, r_proud, r_pass, r_wow, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 2, ['СМЕНКУ', 'ЗАБЫЛ!'], hook_t=(0.10, 2.4), hook_y=230, hook_size=84,
              stickers=[(K.st('ПЕЛЬМЕНИ?!', fg=(255, 110, 150), size=64), TWIST + 0.05, TWIST + 2.4, 540, 360)],
              flashes=[TWIST, CUTS[1]], mosaics=[CUTS[7]],
              cap_y={0: 1480, 1: 1380, 2: 1480, 3: 1500, 4: 1460, 5: 1400, 6: 1400, 7: 1440, 8: 1440, 9: 1460, 10: 1480, 11: 1480,
                     12: 1440, 13: 1480, 14: 1380})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
