"""S01E03 «КОРПОРАТИВ» (twist type: the hunter asks for help). Morning: the boss cancels the party («Денег нет. Отметим по домам!»),
his phone keeps buzzing «ТЁЩА» (rewatch clue). Эдик: «Аркадий, это вызов. Сделаем тайный корпоратив.» — «Только не гирлянду на меня.»
Evening, the dark office, the ficus in a blinking garland: «Я же просил.» Людмила with a basin of olivier: «Тысяча с носа.» Toast «За
корпоратив без начальства!» — a knock. TWIST: the boss behind the door: «Булкин… пусти. Ко мне тёща на недельку приехала.» — «Вход —
тысяча, Виктор Палыч.» — «А… в рассрочку?» — «Не положено.» The boss dances with the basin; the ficus: «Скинулся — значит, родственник.»
  python3 ep03.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import math
import numpy as np
import kscommon as KC
from kscommon import C, K, M, at, aout, shot, floor_actor, tally, sm, lerp
from cam25 import glide, kick
from timeline import DUR, VOICE, CUTS, NAMES, TWIST, T0

EPI = KC.ep('ep03', VOICE, DUR, 'ЗАВТРА: ОТПУСК')
FC = KC.Faces(EPI, {
    'edik': ([(0.0, 'hopeful'), (T0['e1'], 'scheme'), (T0['l1'], 'beam'), (T0['e2'], 'beam'), (TWIST - 0.8, 'shock'), (T0['e3'], 'smirk'),
              (T0['f3'], 'beam')], 3),
    'fikus': ([(0.0, 'deadpan'), (T0['f2'], 'crushed'), (T0['f3'], 'smirk')], 8),
    'shef': ([(0.0, 'bark'), (1.5, 'boss'), (TWIST, 'pleading'), (T0['f3'], 'beam')], 5),
    'lyuda': ([(0.0, 'strict'), (T0['l2'], 'deadpan')], 11)})


def garland_glow(big, t, n=26, seed=3, k=1.0):
    """coloured light pools of the garland in the dark office"""
    rng = np.random.default_rng(seed)
    cols = np.array([(255, 60, 60), (60, 220, 90), (255, 214, 60), (70, 140, 255)], np.float32)
    H, W = big.shape[:2]
    out = big.astype(np.float32)
    for i in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.75)
        on = (int(t * 4) + i) % 3 != 0
        if not on: continue
        r = rng.uniform(60, 130)
        x0, x1, y0, y1 = int(max(0, x - r)), int(min(W, x + r)), int(max(0, y - r)), int(min(H, y + r))
        yy, xx = np.mgrid[y0:y1, x0:x1]
        m = np.clip(1 - np.hypot(xx - x, yy - y) / r, 0, 1)[..., None] ** 2 * 0.35 * k
        out[y0:y1, x0:x1] += m * cols[i % 4]
    big[:] = np.clip(out, 0, 255).astype(np.uint8)


def party(big, t, k=1.0):
    KC.darken(big, 0.78)
    garland_glow(big, t, k=k)


# ================================================================== 0: HOOK — the boss cancels the party, the phone buzzes «ТЁЩА»
def r_hook(t, u):
    return KC.cu(FC, 'shef', C.shef, t, u, name='office_morning', cx=200.0, cy=320.0, y=1010, s=34.0, base=(0.6, 0.1),
                 hand_n=(20.0, 52.0), prop_n=lambda sp, h: C.phone(sp, h, 'ТЁЩА'))


# ================================================================== 1: «Аркадий, это вызов…» — two-shot at the window
def r_aside(t, u):
    Z = 1.3
    cx, cy = 960.0, 330.0
    v = K.V('office_morning', cx, cy, Z)
    fk = K.A(C.fikus, KC.SILL[0], KC.SILL[1], KC.WS_SILL * 3 * Z, **FC.kw('fikus', t, (-0.8, 0.0)))
    ed = at(C.edik, v, 330, 1020, 22.0, pin='head', near=0.99, **FC.kw('edik', t, (0.9, 0.1), hand_n=(18.0, 56.0), hand_f=(10.0, 54.0)))
    return shot('office_morning', cx, cy, Z, acts=[fk, ed], par=(-6 + 8 * u, 0), t=t)


def r_fik1(t, u): return KC.fik_cu(FC, t, u, 'office_morning')


# ================================================================== 3: evening — the ficus in a blinking garland: «Я же просил.»
def r_garland(t, u):
    big = KC.fik_cu(FC, t, u, 'office_night', garland=True)
    party(big, t, 0.8)
    return big


# ================================================================== 4: Людмила with the olivier basin
def r_lyuda(t, u):
    big = KC.cu(FC, 'lyuda', C.lyuda, t, u, name='office_night', cx=440.0, cy=330.0, y=860, s=34.0, base=(0.0, -0.1),
                hand_n=(10.0, 38.0), prop_n=lambda sp, h: C.bowl(sp, h, 'ЛЮДА'))
    party(big, t)
    tally(big, '1000 С НОСА', (255, 232, 110), 380, 64)
    return big


# ================================================================== 5: the toast — wide, the dark office in garland light
def r_toast(t, u):
    Z = 1.15
    cx, cy = 820.0, 360.0
    v = K.V('office_night', cx, cy, Z)
    fk = K.A(C.fikus, KC.SILL[0], KC.SILL[1], KC.WS_SILL * 3 * Z, **FC.kw('fikus', t, (-0.6, 0.0), garland=True))
    ly = floor_actor(C.lyuda, 760.0, 575.0, Z, **FC.kw('lyuda', t, (0.6, 0.0), hand_n=(10.0, 38.0), prop_n=lambda sp, h: C.bowl(sp, h, 'ЛЮДА')))
    ed = floor_actor(C.edik, 900.0, 585.0, Z, flip=True,
                     **FC.kw('edik', t, (-0.6, 0.2), hand_n=(16.0, 74.0), prop_n=lambda sp, h: C.mug(sp, h, '')))
    big = shot('office_night', cx, cy, Z, acts=[fk, ly, ed], par=(-6 + 8 * u, 0), t=t, clock='21:00')
    party(big, t)
    return big


# ================================================================== 6: a knock — the door, then the boss's voice behind it (TWIST)
def r_door(t, u):
    Z = 1.6 + 0.2 * glide(u / 2.0)
    big = shot('office_night', 135.0, 340.0, Z, acts=[], t=t, clock='21:05', kick=kick(t, [(TWIST - 0.85, 0.5), (TWIST - 0.55, 0.5)]))
    party(big, t, 0.6)
    if t < TWIST: tally(big, 'ТУК-ТУК', (255, 232, 110), 420, 80)
    else: tally(big, 'ШЕФ?!', (255, 120, 110), 420, 90)
    return big


# ================================================================== 7: «Вход — тысяча, Виктор Палыч.» — Эдик at the half-open door
def r_smug(t, u):
    big = KC.cu(FC, 'edik', C.edik, t, u, name='office_night', cx=260.0, cy=330.0, y=860, s=32.0, base=(-0.8, 0.0), flip=True,
                hand_n=(16.0, 52.0), prop_n=lambda sp, h: C.mug(sp, h, ''))
    party(big, t, 0.7)
    return big


# ================================================================== 8: «А… в рассрочку?» — the boss in the doorway with a tiny bowl
def r_plead(t, u):
    big = KC.cu(FC, 'shef', C.shef, t, u, name='office_night', cx=150.0, cy=320.0, y=880, s=34.0, base=(0.8, -0.2),
                hand_n=(22.0, 48.0), prop_n=lambda sp, h: C.bowl(sp, h, '', big=False))
    party(big, t, 0.6)
    return big


def r_nelz(t, u):
    big = KC.cu(FC, 'lyuda', C.lyuda, t, u, name='office_night', cx=440.0, cy=330.0, y=860, s=34.0, base=(-0.6, 0.0),
                hand_n=(10.0, 38.0), prop_n=lambda sp, h: C.bowl(sp, h, 'ЛЮДА'))
    party(big, t)
    return big


# ================================================================== 10: the boss dances with the basin; the ficus button
def r_dance(t, u):
    Z = 0.95
    cx, cy = 900.0, 360.0
    v = K.V('office_night', cx, cy, Z)
    fk = K.A(C.fikus, KC.SILL[0], KC.SILL[1], KC.WS_SILL * 3 * Z, **FC.kw('fikus', t, (-0.6, 0.0), garland=True))
    sway = math.sin(t * 6.0)
    sh = floor_actor(C.shef, 850.0 + 10 * sway, 590.0, Z, hat_dm=True,
                     **FC.kw('shef', t, (0.6, 0.0), hand_n=(18.0, 70.0 + 6 * sway), hand_f=(-16.0, 70.0 - 6 * sway),
                             prop_n=lambda sp, h: C.bowl(sp, h, 'ЛЮДА')))
    ed = floor_actor(C.edik, 740.0, 585.0, Z, **FC.kw('edik', t, (0.8, 0.0), hand_n=(16.0, 60.0 + 6 * sway)))
    big = shot('office_night', cx, cy, Z, acts=[fk, ed, sh], par=(-4 + 6 * u, 0), t=t, clock='21:10')
    party(big, t)
    return big


R = [r_hook, r_aside, r_fik1, r_garland, r_lyuda, r_toast, r_door, r_smug, r_plead, r_nelz, r_dance]
assert len(R) == len(CUTS) - 1 == len(NAMES)
SHOW = K.Show(EPI, ['КОРПОРАТИВА', 'НЕ БУДЕТ!'], hook_t=(0.10, 2.6), hook_y=210, hook_size=74, stickers=[],
              flashes=[TWIST], mosaics=[CUTS[3]],
              cap_y={0: 1560, 1: 1560, 2: 1580, 3: 1580, 4: 1560, 5: 1560, 6: 1560, 7: 1560, 8: 1560, 9: 1560, 10: 1560})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    return SHOW.apply(R[i](t, t - CUTS[i]), t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
