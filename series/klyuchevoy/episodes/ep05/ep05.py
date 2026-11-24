"""S01E05 «НЕ ТОТ ЧАТ» (twist type: the network sees everything). «Аркадий… я написал «шеф — дятел». В общий чат.» — «Сорок семь
человек. И дятел.» — «Удалю! Удалить у всех… Есть! Никто не видел!» — silence, the printer «НЕ РАБОТАЕТ (С 2019)» hums: «Принтер. Семь лет
не работал.» TWIST, Людмила: «Ой. Я переписку на печать отправила. Для отчёта.» — «Он же сломан!» — «Ради такого — ожил.» The boss with
the printout: «Булкин. Это кто тут «дятел»?» — «Это… про птицу. Я орнитолог.» — «Орнитолог, задержись на пять минут.» — «Это до пенсии.»
Rewatch clue: the plate «ПРИНТЕР НЕ РАБОТАЕТ (С 2019)» is visible next to the ficus from the first wide shot.
  python3 ep05.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import math
import numpy as np
import kscommon as KC
from kscommon import C, K, M, O, at, shot, floor_actor, tally, sm, lerp, OUT_W, OUT_H
from cam25 import glide, kick
from timeline import DUR, VOICE, CUTS, NAMES, TWIST, T0, PH1, DEL

EPI = KC.ep('ep05', VOICE, DUR, 'ЗАВТРА: СОТРУДНИК ГОДА')
FC = KC.Faces(EPI, {
    'edik': ([(0.0, 'panic'), (T0['e2'], 'panic'), (DEL + 0.4, 'beam'), (T0['f2'] - 0.9, 'hopeful'), (TWIST, 'shock'), (T0['e3'], 'panic'),
              (T0['s1'], 'shock'), (T0['e4'], 'sweet'), (T0['s2'], 'crushed')], 3),
    'fikus': ([(0.0, 'deadpan'), (T0['f3'], 'smirk'), (T0['f4'], 'deadpan')], 8),
    'lyuda': ([(0.0, 'deadpan')], 11),
    'shef': ([(0.0, 'strict'), (T0['s2'], 'smirk')], 5)})
MSGS = [('Людмила', 'Отчёт сдала', False), ('Вован', 'Кто обедать?', False), ('Эдик', 'Шеф — дятел', True)]


def ecu(t, u, **kw): return KC.cu(FC, 'edik', C.edik, t, u, **kw)


def r_hook(t, u): return ecu(t, u, base=(0.0, -0.4), sweat=2.0, hand_n=(18.0, 46.0), prop_n=lambda sp, h: C.phone(sp, h, 'ЧАТ'))


def r_phone(t, u):
    big = KC.phone_insert(t, MSGS)
    return big


def r_fik1(t, u): return KC.fik_cu(FC, t, u)
def r_e2(t, u): return ecu(t, u, base=(0.0, -0.4), sweat=2.0, hand_n=(18.0, 46.0 + 2 * math.sin(t * 20)), prop_n=lambda sp, h: C.phone(sp, h, 'ЧАТ'))


def r_deleted(t, u):
    gone = t > DEL + 0.3
    return KC.phone_insert(t, MSGS, deleted=gone, banner='Удалено у всех' if gone else 'Удалить у всех?')


def printer_sheets(big, v, t, t0, n=8):
    """sheets slide out of the printer and flutter to the floor"""
    px, py = v.opt(1105.0, 440.0)
    sc = v.Z * 3
    for i in range(n):
        k = (t - t0) * 1.4 - i * 0.35
        if k <= 0: continue
        x = px + 20 * sc * k + 8 * sc * math.sin(k * 4 + i)
        y = py + min(k, 3.0) * 30 * sc
        w, h = int(14 * sc), int(18 * sc)
        x0, y0 = int(x - w / 2), int(y - h / 2)
        if 0 <= x0 < OUT_W - w and 0 <= y0 < OUT_H - h:
            big[y0:y0 + h, x0:x0 + w] = (248, 248, 242)
            big[y0 + h // 4:y0 + h // 4 + max(2, h // 12), x0 + w // 6:x0 + w - w // 6] = (60, 60, 66)
            big[y0 + h // 2:y0 + h // 2 + max(2, h // 14), x0 + w // 6:x0 + w - w // 3] = (60, 60, 66)


def r_printer(t, u, t0=None):
    """the printer next to the ficus: the camera moves in on the window corner (both at real scale)"""
    Z = 1.55 + 0.08 * u
    cx, cy = 1075.0, 335.0
    v = K.V('office', cx, cy, Z)
    fk = K.A(C.fikus, KC.SILL[0], KC.SILL[1], KC.WS_SILL * 3 * Z, **FC.kw('fikus', t, (0.8, -0.4)))
    shake = (int(t * 30) % 2) * 2 - 1
    def f(big, v_): printer_sheets(big, v_, t, t0 if t0 is not None else T0['f2'] - 0.4)
    return shot('office', cx, cy, Z, acts=[fk], par=(shake * 0.6, 0), t=t, fx_=f)


def r_printer2(t, u): return r_printer(t, u, T0['f2'] - 0.4)
def r_lyuda(t, u): return KC.cu(FC, 'lyuda', C.lyuda, t, u, cx=440.0, cy=330.0, s=34.0, base=(0.6, 0.0), hand_n=(9.0, 40.0),
                                 prop_n=lambda sp, h: C.mug(sp, h, 'ЛЮДА'))
def r_e3(t, u): return ecu(t, u, base=(0.8, 0.0), sweat=2.0, hand_n=(18.0, 66.0), hand_f=(-6.0, 62.0))


def r_shef(t, u):
    return KC.cu(FC, 'shef', C.shef, t, u, cx=520.0, cy=340.0, y=900, s=34.0, base=(0.6, 0.2), hand_n=(8.0, 54.0),
                 prop_n=lambda sp, h: C.sheet(sp, h))


def r_e4(t, u): return ecu(t, u, base=(-0.6, 0.0), sweat=2.0, hand_n=(12.0, 50.0), hand_f=(-2.0, 48.0))
def r_shef2(t, u): return r_shef(t, u)
def r_f4(t, u): return KC.fik_cu(FC, t, u, Z0=2.2)


R = [r_hook, r_phone, r_fik1, r_e2, r_deleted, r_printer, r_lyuda, r_e3, r_printer2, r_shef, r_e4, r_shef2, r_f4]
assert len(R) == len(CUTS) - 1 == len(NAMES)
SHOW = K.Show(EPI, ['НЕ ТОТ', 'ЧАТ!'], hook_t=(0.10, 2.4), hook_y=210, hook_size=90,
              stickers=[(K.st('47 ЧЕЛОВЕК', fg=(255, 232, 110), size=70), T0['f1'] + 0.3, T0['e2'], 540, 400),
                        (K.st('ПЕЧАТАЕТ?!', fg=(255, 120, 110), size=80), T0['f2'] - 0.6, T0['l1'], 540, 420)],
              flashes=[TWIST], mosaics=[PH1],
              cap_y={0: 1560, 1: 1720, 2: 1580, 3: 1560, 4: 1720, 5: 1580, 6: 1560, 7: 1560, 8: 1580, 9: 1560, 10: 1560, 11: 1560, 12: 1580})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    return SHOW.apply(R[i](t, t - CUTS[i]), t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
