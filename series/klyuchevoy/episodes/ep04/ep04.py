"""S01E04 «ОТПУСК» (twist type: success worse than failure). Людмила brings the 2027 vacation chart: «Ваш — в феврале.» — «Я семнадцать
лет прошу июль!» — «Июль — шеф. Август — шеф. Июнь — жена шефа.» — «Она у нас даже не работает!» — «Не работает. Но отдыхает.» — «Летом —
собака шефа. Свободно только двадцать девятое февраля.» — «Беру!» (stamp «УТВЕРЖДЕНО»). TWIST, the ficus: «Поздравляю. В двадцать седьмом
году двадцать девятого февраля нет.» (the calendar: the «29» cell dissolves) — «Перепишите!» — «Утверждено. Не положено.» — «Зато не сгорит.»
Rewatch clue: the «29» cell on the chart is circled in red from the first insert.
  python3 ep04.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import math
import numpy as np
from PIL import Image, ImageDraw
import kscommon as KC
from kscommon import C, K, M, O, at, shot, floor_actor, tally, sm, lerp, OUT_W, OUT_H
from cam25 import glide, kick
from timeline import DUR, VOICE, CUTS, NAMES, TWIST, T0, CAL

EPI = KC.ep('ep04', VOICE, DUR, 'ЗАВТРА: НЕ ТОТ ЧАТ')
FC = KC.Faces(EPI, {
    'edik': ([(0.0, 'hopeful'), (T0['e1'], 'bark'), (T0['e2'], 'shock'), (T0['l4'], 'pleading'), (T0['e4'], 'beam'), (TWIST, 'shock'),
              (T0['e5'], 'panic'), (T0['f2'], 'crushed')], 3),
    'fikus': ([(0.0, 'deadpan'), (TWIST + 0.6, 'smirk'), (T0['f2'], 'deadpan')], 8),
    'lyuda': ([(0.0, 'strict'), (T0['l3'], 'smirk'), (T0['l4'], 'deadpan'), (T0['l5'], 'strict')], 11)})
RED, INK, GRY = (190, 40, 40), (40, 40, 44), (150, 150, 150)


def r_hook(t, u):
    Z = 1.2
    cx, cy = 480.0, 330.0
    ly = floor_actor(C.lyuda, 405.0, 575.0, Z, **FC.kw('lyuda', t, (0.9, 0.0), hand_n=(12.0, 40.0), prop_n=lambda sp, h: C.clipboard(sp, h)))
    ed = floor_actor(C.edik, 545.0, 585.0, Z, flip=True, **FC.kw('edik', t, (-0.9, 0.2), hand_n=(16.0, 40.0)))
    return shot('office', cx, cy, Z, acts=[ly, ed], par=(-6 + 8 * u, 0), t=t)


def ecu(t, u, **kw): return KC.cu(FC, 'edik', C.edik, t, u, **kw)
def lcu(t, u, **kw): return KC.cu(FC, 'lyuda', C.lyuda, t, u, cx=440.0, cy=330.0, s=34.0, hand_n=(9.0, 40.0),
                                   prop_n=lambda sp, h: C.clipboard(sp, h), **kw)


def r_e1(t, u): return ecu(t, u, base=(0.0, 0.0), hand_n=(18.0, 62.0), hand_f=(-4.0, 50.0))
def r_e2(t, u): return ecu(t, u, base=(0.2, 0.0), sweat=1.0, hand_n=(14.0, 56.0))
def r_l3(t, u): return lcu(t, u, base=(0.6, 0.0))
def r_e4(t, u):
    big = ecu(t, u, base=(0.0, -0.3), hand_n=(16.0, 44.0), prop_n=lambda sp, h: C.clipboard(sp, h))
    if t > T0['e4'] + 0.55: tally(big, 'УТВЕРЖДЕНО', (230, 60, 60), 420, 84)
    return big
def r_e5(t, u): return ecu(t, u, base=(0.0, 0.2), sweat=2.0, hand_n=(18.0, 66.0), hand_f=(-6.0, 62.0))
def r_l5(t, u): return lcu(t, u, base=(0.0, -0.2))
def r_fik(t, u): return KC.fik_cu(FC, t, u)
def r_f2(t, u): return KC.fik_cu(FC, t, u, Z0=2.2)


# ================================================================== the vacation chart insert (rows appear with the words)
def chart(t, rows, free=False):
    big = KC.desk_bg()
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([90, 250, 990, 1650], fill=(250, 248, 238), outline=(60, 50, 40), width=8)
    d.rectangle([90, 250, 990, 380], fill=(40, 70, 130))
    f = O.pfont(44); txt = 'ГРАФИК ОТПУСКОВ 2027'
    d.text(((1080 - f.getlength(txt)) / 2, 292), txt, font=f, fill=(255, 255, 255))
    for i, (m, who, col) in enumerate(rows):
        y = 420 + i * 150
        d.rectangle([120, y, 960, y + 120], outline=(200, 196, 180), width=3)
        d.text((150, y + 38), m, font=O.pfont(40), fill=INK)
        d.text((520, y + 38), who, font=O.pfont(40), fill=col)
    if free:                                                                            # the circled «29» — the rewatch clue
        y = 420 + len(rows) * 150
        d.rectangle([120, y, 960, y + 120], outline=(200, 196, 180), width=3)
        d.text((150, y + 38), 'ФЕВРАЛЬ', font=O.pfont(40), fill=INK)
        d.ellipse([500, y + 10, 700, y + 110], outline=RED, width=8)
        d.text((560, y + 36), '29', font=O.pfont(44), fill=RED)
        d.text((730, y + 46), 'СВОБОДНО', font=O.pfont(26), fill=(40, 140, 60))
    return np.array(im)


def r_chart1(t, u):
    rows = [('ИЮЛЬ', 'ШЕФ', RED)]
    if t > T0['l2'] + 1.0: rows.append(('АВГУСТ', 'ШЕФ', RED))
    if t > T0['l2'] + 2.0: rows.append(('ИЮНЬ', 'ЖЕНА ШЕФА', RED))
    return chart(t, rows)


def r_chart2(t, u):
    rows = [('ИЮЛЬ', 'ШЕФ', RED), ('АВГУСТ', 'ШЕФ', RED), ('ИЮНЬ', 'ЖЕНА ШЕФА', RED), ('ЛЕТО', 'СОБАКА ШЕФА', (150, 90, 40))]
    return chart(t, rows, free=t > T0['l4'] + 1.6)


# ================================================================== the twist insert: February 2027 has 28 days
def r_cal(t, u):
    k = sm((u - 0.3) / 1.2)
    big = KC.calendar_insert(t, 'ФЕВРАЛЬ 2027', days=28, first=0, mark=True, vanish=k)
    tally(big, '29-го НЕТ', (255, 110, 100), 1500 if k > 0.5 else 1700, 80) if k > 0.4 else None
    return big


R = [r_hook, r_e1, r_chart1, r_e2, r_l3, r_chart2, r_e4, r_fik, r_cal, r_e5, r_l5, r_f2]
assert len(R) == len(CUTS) - 1 == len(NAMES)
SHOW = K.Show(EPI, ['ОТПУСК', 'В ФЕВРАЛЕ?!'], hook_t=(0.10, 2.6), hook_y=210, hook_size=80, stickers=[],
              flashes=[TWIST, CAL], mosaics=[CUTS[2], CUTS[5]],
              cap_y={0: 1560, 1: 1560, 2: 1720, 3: 1560, 4: 1560, 5: 1720, 6: 1560, 7: 1580, 8: 1720, 9: 1560, 10: 1560, 11: 1580})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    return SHOW.apply(R[i](t, t - CUTS[i]), t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
