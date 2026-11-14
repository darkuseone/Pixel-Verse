"""S01E03 «ГДЕ МОЯ МАШИНА?!» (43.8 s, twist at 25.35 s / 58 %, type: «злодей — свой» — the neighbour swapped the flags).
Main question: will Жора find his own car under the snow?
HOOK: the seagull close up on a snow mound: «Дальний Восток. За ночь насыпало ещё метр. И теперь все машины во дворе — одинаковые
сугробы.» — the courtyard: rows of identical car-shaped snow mounds with flags. Жора: «Так. Спокойно. Я ж флажок ставил!…» Гоша in a
folding chair with a thermos and a jar of red caviar (a bundle of spare flags behind his back — the clue): «Доброе утро, Жорик! Да-да,
твой, твой. Копай, родной…» Two hours of digging: «Гош, а ты-то чего не копаешь?» — «А зачем? Ты ж копаешь.» — «Два часа! Но откопал же!
Ласточка моя!» — his key fob: nothing. TWIST: Гоша's fob — the car blinks for HIM: «Не понял.» — «Спасибо, Жорик! Это ж моя. Я флажки
ночью поменял.» — «А моя-то где?!» — «Да под моим флажком! Не переживай, с меня икра!» — the jar is empty. «Ну ничего. Завтра я ему
флажки поменяю.» — the gull: «Завтра — ещё метр. Зимуем.»
  python3 ep03.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
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

K.DAY = 97
EPI = Episode('ep03', VOICE, DUR, FPS, colors=dict(K.COL, gosha=(200, 255, 140)), slug=SLUG, endcard=dict(style='zamelo', lang='ru'),
              promo='ru')
TAB = (C.XTRA, C.EXPR)
FZ = M.Face([(0.0, 'proud'), (10.4, 'cocky'), (15.7, 'exhausted'), (21.2, 'cheerful'), (24.8, 'blank'), (25.4, 'stunned'),
             (30.8, 'outraged'), (35.6, 'shock'), (36.3, 'gloomy'), (38.0, 'cocky')], TAB, seed=3)
FC = M.Face([(0.0, 'dry')], TAB, seed=8)
FG = M.Face([(0.0, 'sly'), (18.9, 'smug'), (25.3, 'cheer'), (32.1, 'grin')], TAB, seed=21)
MOUND_A = (552.0, 584.0)           # Жора's flag (Гоша's car underneath)
MOUND_B = (850.0, 604.0)           # Гоша's flag (Жора's car underneath)
CHAIR = (262.0, 652.0)
CAR_K = 1.42
FLAGS = [('ТЁЩИНА', (320.0, 470.0), (120, 80, 200)), ('НЕ ТРОГАТЬ', (1128.0, 520.0), (40, 90, 190)), ('ПРОДАМ', (120.0, 440.0), (230, 140, 40)),
         ('ЛАДА — ЭТО Я', (700.0, 410.0), (60, 150, 90))]


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def face(F, who, t, base=(0.7, 0.0), **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), **kw), M.bob(t, m)


def S_of(v, z=1.0):
    return K.WS['carfield'] * 3 * v.Z * z


def flags(v, t, swap_shown=True, skip=()):
    S = S_of(v)
    out = []
    for lab, (x, y), col in FLAGS:
        if lab in skip: continue
        a = A(C.flag, x, y - 40, S * 1.4, t=t + x * 0.01, label=lab, col=col); a.near = 0.99; out.append(a)
    if 'ЖОРА' not in skip:
        a = A(C.flag, MOUND_A[0] - 30, MOUND_A[1] - 150, S * 1.5, t=t, label='ЖОРА', col=(220, 50, 60)); a.near = 0.99; out.append(a)
    if 'ГОША' not in skip:
        a = A(C.flag, MOUND_B[0] + 10, MOUND_B[1] - 160, S * 1.5, t=t + 0.4, label='ГОША', col=(70, 160, 80)); a.near = 0.99; out.append(a)
    return out


def gosha_chair(t, v, base=(0.8, 0.0), z=1.0, empty=False, **extra):
    S = S_of(v, z)
    kw, dy = face(FG, 'gosha', t, base, sit=True, prop_n=C.thermos, prop_f=lambda sp, h: C.caviar(sp, h, empty=empty), **extra)
    g = A(C.gosha, CHAIR[0], CHAIR[1] + dy * 0.3, S, t=t, **kw); g.near = 0.99
    # the bundle of spare flags behind his back (the clue)
    fl = [A(C.flag, CHAIR[0] - 38 + i * 6, CHAIR[1] - 4, S * 0.55, t=t + i, label=lab, col=col, lean=-4 + i * 2)
          for i, (lab, col) in enumerate((('ЖОРА', (220, 50, 60)), ('ГОША', (70, 160, 80)), ('?', (230, 140, 40))))]
    for a in fl: a.near = 0.99
    return fl + [g]


def car_act(t, v, x, y, snow=0.0, blink=False, z=1.0, speed=0.0, chains=True):
    a = A(C.corolla, x, y, S_of(v, z) * CAR_K, t=t, snow=snow, blink=blink, chains=chains, speed=speed); a.near = 0.99
    return a


# ================================================================== 0: «Дальний Восток.» — CU the seagull on a snow mound
def r_gull(t, u):
    Z = 2.6 * (1 + 0.025 * u)
    cx, cy = 560.0, 400.0
    v = K.V('carfield', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 560.0, 440.0 + dy * 0.3, S_of(v) * 2.0, t=t, flip=True, **kw); g.near = 0.99
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=[g], focus=0.6, dof_k=26, t=t, snow_n=60, kick=kick(t, [(0.12, 0.8)]))


# ================================================================== 1: the courtyard — identical mounds with flags
def r_field(t, u):
    L = CUTS[2] - CUTS[1]
    k = glide(u / L)
    Z = lerp(1.0, 1.15, k)
    cx, cy = lerp(300.0, 900.0, k), 420.0
    v = K.V('carfield', cx, cy, Z)
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=flags(v, t), t=t, focus=0.6, dof_k=6, snow_n=70,
                  glints=(0, 1300, 1080, 1900), par=(-10 + 20 * k, 0))


# ================================================================== 2: «Так. Спокойно. Я ж флажок ставил!…» — Жора walks to «ЖОРА»
def r_walk(t, u):
    Z = 1.5
    cx, cy = 520.0, 470.0
    v = K.V('carfield', cx, cy, Z)
    x = lerp(400.0, 480.0, glide(min(1.0, u / 2.5)))
    kw, dy = face(FZ, 'zhora', t, (0.8, -0.2), walk=t * 7.0 if u < 2.5 else None, hand_n=(20.0, 40.0),
                  prop_n=lambda sp, h: C.shovel(sp, h, ang=1.3, l=30.0), hand_f=(-12.0, 66.0) if u > 2.6 else None)
    z = A(C.zhora, x, 640.0 + dy, S_of(v), t=t, **kw); z.near = 0.99
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=flags(v, t) + [z], t=t, focus=0.8, dof_k=8, snow_n=55)


# ================================================================== 3: Гоша in his folding chair: «Доброе утро, Жорик!…»
def r_gosha(t, u):
    Z = 3.6 * (1 + 0.015 * u)
    cx, cy = 262.0, 612.0
    v = K.V('carfield', cx, cy, Z)
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=gosha_chair(t, v, (0.8, 0.1)), t=t, focus=0.9, dof_k=18, snow_n=45)


# ================================================================== 4: two hours of digging (time-lapse) — «Гош, а ты-то чего не копаешь?»
def r_dig(t, u):
    Z = 1.45
    cx, cy = 530.0, 480.0
    v = K.V('carfield', cx, cy, Z)
    L = CUTS[5] - CUTS[4]
    snow = 1.0 - 0.55 * (u / L)
    ph = (t * 2.6) % 1.0
    k = math.sin(ph * math.pi) ** 2
    kw, dy = face(FZ, 'zhora', t, (-0.8, 0.2), hand_n=(20.0 + 4 * k, 30.0 + 26 * k), sweat=1.0,
                  prop_n=lambda sp, h: C.shovel(sp, h, ang=-1.5 + 0.9 * k, l=30.0, snow=k))
    z = A(C.zhora, 430.0, 645.0 + dy, S_of(v), t=t, **kw); z.near = 0.99
    car = car_act(t, v, MOUND_A[0], MOUND_A[1], snow=snow)
    def f(big, _):
        ox, oy = v.opt(500.0, 560.0)
        K.puff(big, ox, oy - 60, t, t - (ph / 2.6), n=8, seed=int(t * 3), life=0.45, speed=520, px=12)
        O.overlay(big, ST_1H if u < L * 0.5 else ST_2H, 300, 380, 1.0)
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=flags(v, t, skip=('ЖОРА',)) + [z], fx_=f, t=t, focus=0.85,
                  dof_k=8, snow_n=55)


def r_gosha2(t, u):
    Z = 3.8
    cx, cy = 262.0, 612.0
    v = K.V('carfield', cx, cy, Z)
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=gosha_chair(t, v, (0.9, 0.0)), t=t, focus=0.9, dof_k=24, snow_n=40)


# ================================================================== 6: the car is out: «Два часа! Но откопал же! Ласточка моя!»
def r_car(t, u):
    Z = 1.45
    cx, cy = 535.0, 490.0
    v = K.V('carfield', cx, cy, Z)
    kw, dy = face(FZ, 'zhora', t, (0.6, -0.3), hand_n=(22.0, 46.0), hand_f=(-10.0, 46.0))
    z = A(C.zhora, 440.0, 645.0 + dy, S_of(v), t=t, **kw); z.near = 0.99
    car = car_act(t, v, MOUND_A[0], MOUND_A[1], snow=0.0)
    def f(big, _):
        if u < 1.2:
            sx, sy = v.opt(MOUND_A[0] + 20, MOUND_A[1] - 40)
            for i in range(4):
                big_ = None
            fx.glow(big, int(sx), int(sy), 220, (255, 250, 220), 0.25 * (1 - u / 1.2))
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=[car] + flags(v, t, skip=('ЖОРА',)) + [z], fx_=f, t=t, focus=0.85,
                  dof_k=8, snow_n=50, glints=(200, 800, 1000, 1300))


# ================================================================== 7: insert — his key fob: click… nothing
def key_fob(sp, t=0.0, lit=False):
    sp.sup(0.0, 8.0, 5.0, 8.0, tones_k((40, 40, 50)), n=3.0, gloss=1.0)
    for i, y in enumerate((11.0, 6.0)): sp.ell(0.0, y, 2.6, 2.0, tones_k((80, 80, 96)))
    sp.blob(0.0, 14.6, 0.8, (255, 60, 40) if lit else (90, 40, 40))
    C.thin(sp, (0.0, 16.0), (2.0, 22.0), (190, 196, 210), 0.6)
    sp.ell(2.4, 23.0, 2.0, 2.0, tones_k((190, 196, 210)))


def tones_k(c): return C.tones(c)


def r_key(t, u):
    Z = 1.5
    cx, cy = 580.0, 480.0
    def pre(big, _v): big[:] = K.blur(big, 12)
    def f(big, _):
        sp = ZX.draw(key_fob, 26.0, t=t, lit=u > 0.15)
        blit(big, sp, 560, 1400, 26.0, None, False)
        mt = ZX.draw(C.zhora_mitten if hasattr(C, 'zhora_mitten') else mitten, 18.0, t=t)
        blit(big, mt, 600, 1560 - int(20 * min(1.0, u / 0.15)), 18.0, None, False)
    return K.shot('carfield', K.light_morning, cx, cy, Z, pre=pre, fx_=f, t=t, dof_k=0, snow_n=40, kick=kick(t, [(CUTS[7] + 0.15, 0.5)]))


def mitten(sp, t=0.0):
    sp.ell(0.0, 7.0, 9.0, 8.0, C.tones(C.MITT), frost=False)
    sp.ell(-7.4, 11.0, 3.2, 4.4, C.tones(C.MITT), frost=False)
    for q in range(9):
        x0 = -8.0 + q * 2.0
        C.thin(sp, (x0, 1.6 + (q % 2) * 1.2), (x0 + 2.0, 1.6 + ((q + 1) % 2) * 1.2), C.WHITE, 0.45)
    sp.sup(0.0, -2.0, 8.6, 2.6, C.tones(C.ALASKA), n=3.0)


# ================================================================== 8: TWIST — Гоша's fob: the car blinks for him; Жора: «Не понял.»
def r_twist(t, u):
    Z = 1.3
    cx, cy = 385.0, 540.0
    v = K.V('carfield', cx, cy, Z)
    kw, dy = face(FZ, 'zhora', t, (-0.7, 0.0), hand_n=(18.0, 50.0), prop_n=lambda sp, h: key_fob_small(sp, h))
    z = A(C.zhora, 470.0, 640.0 + dy, S_of(v), t=t, **kw); z.near = 0.99
    car = car_act(t, v, MOUND_A[0], MOUND_A[1], snow=0.0, blink=True)
    g = gosha_chair(t, v, (0.9, 0.2), hand_n=(12.0, 58.0))
    def f(big, _):
        hx, hy = v.opt(MOUND_A[0] + 80, MOUND_A[1] - 40)
        if int(t * 6) % 2 == 0: fx.glow(big, int(hx), int(hy), 120, (255, 200, 80), 0.6)
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=[car] + g + [z], fx_=f, t=t, focus=0.85, dof_k=8, snow_n=45,
                  kick=kick(t, [(TWIST, 1.0)]))


def key_fob_small(sp, h):
    x, y = h
    sp.sup(x + 0.6, y + 2.0, 1.4, 2.2, C.tones((40, 40, 50)), n=3.0)


# ================================================================== 9: Гоша gets into the car: «Спасибо, Жорик! Это ж моя…»
def r_g_car(t, u):
    Z = 1.8
    cx, cy = 560.0, 500.0
    v = K.V('carfield', cx, cy, Z)
    kw, dy = face(FG, 'gosha', t, (-0.7, 0.0), hand_n=(12.0, 50.0), prop_n=C.thermos)
    g = A(C.gosha, 640.0, 636.0 + dy * 0.3, S_of(v), t=t, flip=True, **kw); g.near = 0.99
    car = car_act(t, v, MOUND_A[0], MOUND_A[1], snow=0.0)
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=[car, g], t=t, focus=0.9, dof_k=14, snow_n=45)


# ================================================================== 10: «А моя-то где?!» — CU Жора
def r_where(t, u):
    Z = 2.6
    cx, cy = 470.0, 520.0
    v = K.V('carfield', cx, cy, Z)
    kw, dy = face(FZ, 'zhora', t, (0.6, -0.2), hand_n=(24.0, 64.0), hand_f=(-14.0, 64.0))
    z = A(C.zhora, 455.0, 640.0 + dy, S_of(v), t=t, **kw); z.near = 0.99
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=[z], t=t, focus=0.95, dof_k=26, snow_n=45, kick=kick(t, [(30.9, 0.7)]))


# ================================================================== 11: Гоша drives away on chains: «Да под моим флажком!…» — the jar flies
def r_drive(t, u):
    Z = 1.3
    cx, cy = 640.0, 500.0
    v = K.V('carfield', cx, cy, Z)
    x = MOUND_A[0] + 520.0 * (u / (CUTS[12] - CUTS[11])) ** 1.4
    car = car_act(t, v, x, MOUND_A[1], speed=10.0)
    kw, dy = face(FZ, 'zhora', t, (0.9, -0.2), hand_n=(20.0, 40.0))
    z = A(C.zhora, 430.0, 640.0 + dy, S_of(v), t=t, **kw); z.near = 0.99
    def f(big, _):
        wx_, wy_ = v.opt(x + 10, MOUND_A[1] - 60)
        kg, _ = face(FG, 'gosha', t, (-0.9, 0.0))
        sp = ZX.draw(C.gosha, S_of(v) * 0.9, t=t, legs=False, flip=True, **kg)
        blit(big, sp, wx_, wy_ + 260, S_of(v) * 0.9, None, True)
        if u > 2.6:                                                         # the jar flies back to Жора
            k = (u - 2.6) / 0.75
            jx = lerp(wx_, 560, k); jy = lerp(wy_, 1000, k) - 300 * math.sin(math.pi * min(1, k))
            jar = ZX.draw(lambda s_, t=0: C.caviar(s_, (0, 0), empty=True, ladle=False), 14.0, t=t)
            blit(big, jar, jx, jy, 14.0, None, False)
        K.puff(big, wx_ - 260, wy_ + 160, t, t - (t * 6 % 0.17), n=8, seed=int(t * 6), life=0.3, speed=300, px=12)
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=flags(v, t, skip=('ЖОРА',)) + [z, car], fx_=f, t=t, focus=0.85,
                  dof_k=8, snow_n=55)


# ================================================================== 12: the jar — EMPTY
def r_jar(t, u):
    Z = 2.4
    cx, cy = 470.0, 520.0
    v = K.V('carfield', cx, cy, Z)
    kw, dy = face(FZ, 'zhora', t, (0.8, 0.9), hand_n=(18.0, 54.0), prop_n=lambda sp, h: C.caviar(sp, (h[0] - 1, h[1] + 1), empty=True, ladle=False))
    z = A(C.zhora, 455.0, 640.0 + dy, S_of(v), t=t, **kw); z.near = 0.99
    def f(big, _): O.draw_sticker(big, ST_EMPTY, t, CUTS[12] + 0.1, CUTS[13], 560, 560)
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=[z], fx_=f, t=t, focus=0.95, dof_k=26, snow_n=45)


# ================================================================== 13: «Ну ничего. Завтра я ему флажки поменяю.» — at Гоша's flag
def r_revenge(t, u):
    Z = 1.6
    cx, cy = 800.0, 500.0
    v = K.V('carfield', cx, cy, Z)
    kw, dy = face(FZ, 'zhora', t, (0.9, -0.1), hand_n=(18.0, 50.0), prop_n=lambda sp, h: C.shovel(sp, h, ang=1.3, l=30.0),
                  hand_f=(-12.0, 60.0))
    z = A(C.zhora, 720.0, 645.0 + dy, S_of(v), t=t, **kw); z.near = 0.99
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=flags(v, t, skip=('ЖОРА',)) + [z], t=t, focus=0.85, dof_k=8, snow_n=70)


# ================================================================== 14: BUTTON — the gull on Гоша's flag: «Завтра — ещё метр. Зимуем.»
def r_button(t, u):
    Z = 2.6 * (1 + 0.02 * u)
    cx, cy = 880.0, 440.0
    v = K.V('carfield', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 880.0, MOUND_B[1] - 160 + dy * 0.3, S_of(v) * 2.0, t=t, flip=True, **kw); g.near = 0.99
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=[g], t=t, focus=0.99, dof_k=26, snow_n=160)


ST_1H = K.st('1 ЧАС', fg=(255, 255, 255), size=52)
ST_2H = K.st('2 ЧАСА', fg=(255, 214, 80), size=52)
ST_EMPTY = K.st('ПУСТАЯ!', fg=(255, 110, 150), size=60)
R = [r_gull, r_field, r_walk, r_gosha, r_dig, r_gosha2, r_car, r_key, r_twist, r_g_car, r_where, r_drive, r_jar, r_revenge, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 3, ['ГДЕ МОЯ', 'МАШИНА?!'], hook_t=(0.10, 2.4), hook_y=230, hook_size=84,
              stickers=[(K.st('ФЛАЖКИ ПОМЕНЯЛ!', fg=(255, 110, 150), size=56), 27.9, 30.7, 540, 380)],
              flashes=[TWIST, CUTS[1]], mosaics=[CUTS[4]],
              cap_y={0: 1480, 1: 1380, 2: 1460, 3: 1560, 4: 1500, 5: 1560, 6: 1460, 7: 600, 8: 1460, 9: 1200, 10: 1480, 11: 1460,
                     12: 1480, 13: 1460, 14: 1400})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
