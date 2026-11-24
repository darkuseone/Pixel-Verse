"""S01E06 «СОТРУДНИК ГОДА» (finale; twist type: the reward taken by another). 31 December, tinsel. «Аркадий, сегодня меня назовут
сотрудником года. Я и речь написал.» — «Семнадцать лет пишешь. Одну и ту же.» The boss at the honor board: «Сотрудник года! Семнадцать лет
без больничных!» (Эдик rises) «Ни одной жалобы! Ни разу не просил премию!» (Эдик walks up) — a drum-roll pause — TWIST: «Наш… фикус
Аркадий!» — «Он же растение!» — «Вот! Ничего не просит! Мы же одна семья!» The ficus, carried to the office with a window: «Ключ от туалета —
оставь себе.» Эдик alone in front of the honor board where the empty «СОТРУДНИК ГОДА — ?» frame (hanging since E01) now holds the ficus:
«С Новым годом… меня.»
  python3 ep06.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import math
import numpy as np
import kscommon as KC
from kscommon import C, K, M, O, at, shot, floor_actor, tally, sm, lerp, OUT_W, OUT_H
from props import decals as D
from props import rusigns as R_
from props import ksdecor as DEC
from props import kspix as KX
from props.dibspix import blit
from cam25 import glide, kick
from timeline import DUR, VOICE, CUTS, NAMES, TWIST, T0

EPI = KC.ep('ep06', VOICE, DUR, 'СЕЗОН 2 — СКОРО')
FC = KC.Faces(EPI, {
    'edik': ([(0.0, 'proud'), (T0['s1'], 'hopeful'), (T0['s2'], 'beam'), (TWIST, 'shock'), (T0['e2'], 'panic'), (T0['s4'], 'crushed'),
              (T0['e3'], 'crushed')], 3),
    'fikus': ([(0.0, 'deadpan'), (TWIST, 'shock'), (TWIST + 1.0, 'smirk'), (T0['f2'], 'smirk')], 8),
    'shef': ([(0.0, 'boss'), (T0['s3'], 'sweet'), (T0['s4'], 'beam')], 5)})
D.attach(K.world('office'), [(R_.plate(110, 22, ['С НОВЫМ 2027!'], bg=(170, 30, 40), fg=(250, 220, 120), border=(250, 220, 120)), 720, 140)])
_PH = {}


def frame_photo(big, v, t):
    """after the twist the empty «СОТРУДНИК ГОДА — ?» frame holds the ficus (the season thread pays off)"""
    if t < T0['e2']: return
    x0, y0 = v.opt(589.0, 190.0); x1, y1 = v.opt(645.0, 282.0)
    xa, xb, ya, yb = int(max(0, x0)), int(min(OUT_W, x1)), int(max(0, y0)), int(min(OUT_H, y1))
    if xa >= xb or ya >= yb: return
    big[ya:yb, xa:xb] = (236, 228, 206)
    s = (y1 - y0) / 70.0
    sp = KX.draw(C.fikus, s, expr='smirk', medal=True)
    blit(big, sp, (x0 + x1) / 2, y1 - 4 * s, s, None)


DEC.FRAME_FILL[0] = frame_photo


def tinsel(big, t):
    """festive tinsel garlands along the top of the frame"""
    for row, (y0, amp, col) in enumerate(((240, 40, (240, 200, 60)), (300, 30, (220, 50, 60)))):
        for x in range(0, OUT_W, 6):
            y = int(y0 + amp * math.sin(x / 180.0 * math.pi + row) ** 2)
            tw = 1.0 + 0.4 * math.sin(t * 6 + x * 0.05)
            big[y:y + 10, x:x + 6] = np.clip(np.array(col) * tw, 0, 255)


def fest(big, t):
    tinsel(big, t)
    return big


def r_hook(t, u):
    return fest(KC.cu(FC, 'edik', C.edik, t, u, base=(0.2, 0.0), hand_n=(16.0, 52.0), prop_n=lambda sp, h: C.sheet(sp, h, ('РЕЧЬ',))), t)


def r_fik1(t, u): return fest(KC.fik_cu(FC, t, u, garland=True), t)


def r_award(t, u, walk=False):
    Z = 1.15
    cx, cy = 470.0, 330.0
    sh = floor_actor(C.shef, 450.0, 535.0, Z, **FC.kw('shef', t, (0.9, 0.0), hand_n=(26.0, 70.0)))
    ex = lerp(640.0, 560.0, glide((t - T0['s2']) / 2.5)) if walk else 640.0
    ed = floor_actor(C.edik, ex, 600.0, Z, flip=True, walk=t * 6.0 if walk else None,
                     **FC.kw('edik', t, (-0.9, 0.2), hand_n=(16.0, 52.0), prop_n=lambda sp, h: C.sheet(sp, h, ('РЕЧЬ',))))
    return fest(shot('office', cx, cy, Z, acts=[sh, ed], par=(-4 + 6 * u, 0), t=t), t)


def r_walk(t, u): return r_award(t, u, walk=True)


def r_drum(t, u):
    big = KC.cu(FC, 'shef', C.shef, t, u, cx=470.0, cy=320.0, y=900, s=34.0, base=(0.0, 0.0), hand_n=(26.0, 70.0))
    fest(big, t)
    if t < TWIST: tally(big, 'И СОТРУДНИК ГОДА…', (255, 232, 110), 420, 54)
    else: tally(big, 'ФИКУС?!', (130, 236, 140), 420, 96)
    return big


def r_e2(t, u):
    return fest(KC.cu(FC, 'edik', C.edik, t, u, base=(0.0, 0.0), sweat=2.0, hand_n=(18.0, 66.0), hand_f=(-6.0, 62.0),
                      prop_n=lambda sp, h: C.sheet(sp, h, ('РЕЧЬ',))), t)


def r_hug(t, u):
    """the boss proudly holds the ficus with its medal"""
    Z = 1.3
    cx, cy = 470.0, 330.0
    v = K.V('office', cx, cy, Z)
    sh = at(C.shef, v, 420, 1950, 20.0, **FC.kw('shef', t, (0.8, 0.0), hand_n=(26.0, 52.0)))
    fk = at(C.fikus, v, 760, 1500, 13.0, near=0.99, **FC.kw('fikus', t, (-0.8, 0.0), medal=True))
    return fest(shot('office', cx, cy, Z, acts=[sh, fk], par=(-4 + 6 * u, 0), t=t), t)


def r_carry(t, u):
    """the ficus carried away to the office with a window — it says goodbye over the boss's shoulder"""
    Z = 1.15
    cx, cy = 300.0, 330.0
    w = glide(u / 2.2)
    sx = lerp(420.0, 190.0, w)
    sh = floor_actor(C.shef, sx, 520.0, Z, flip=True, walk=t * 6.0, **FC.kw('shef', t, (-0.9, 0.0), hand_n=(22.0, 50.0), hand_f=(10.0, 50.0)))
    fk = K.A(C.fikus, sx - 18.0, 520.0 - 46.0 * K.ws_at(520.0), K.ws_at(520.0) * 3 * Z * 0.75,
             **FC.kw('fikus', t, (0.9, 0.0), medal=True))
    fk.near = 0.99
    return fest(shot('office', cx, cy, Z, acts=[sh, fk], par=(-4 + 6 * u, 0), t=t), t)


def r_alone(t, u):
    """Эдик alone in front of the honor board: the frame now holds the ficus"""
    Z = 1.5
    cx, cy = 560.0, 260.0
    v = K.V('office', cx, cy, Z)
    ed = at(C.edik, v, 330, 1250, 26.0, pin='head', near=0.99,
            **FC.kw('edik', t, (0.8, -0.4), hand_n=(14.0, 46.0), prop_n=lambda sp, h: C.sheet(sp, h, ('РЕЧЬ',))))
    big = shot('office', cx, cy, Z, acts=[ed], par=(4 - 6 * u, 0), t=t, clock='23:59')
    return fest(KC.darken(big, 0.8), t)


R = [r_hook, r_fik1, r_award, r_walk, r_drum, r_e2, r_hug, r_carry, r_alone]
assert len(R) == len(CUTS) - 1 == len(NAMES)
SHOW = K.Show(EPI, ['СОТРУДНИК', 'ГОДА?!'], hook_t=(0.10, 2.6), hook_y=200, hook_size=82, stickers=[],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1560, 1: 1580, 2: 1560, 3: 1560, 4: 1560, 5: 1560, 6: 1500, 7: 1560, 8: 1600})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    return SHOW.apply(R[i](t, t - CUTS[i]), t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
