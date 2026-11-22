"""S01E02 v2 «ГОДОВАЯ ПРЕМИЯ» (standard «голливудский уровень», reference = E01 v2 variant A; 34.5 s, twist at 17.00 s / 49 %,
type: success worse than failure). Radio-play story: Людмила brings Эдик his yearly bonus — 40 000. «Аркадий, я богат!» — «Не спеши. У неё
калькулятор.» Minus tax (35), minus lateness (20) — «Я опоздал один раз!» — «Двенадцать раз. По пять минут.» TWIST: «Итого: вы должны
компании триста рублей.» — «Как… должен?!» — «Взнос на юбилей шефа. Добровольный.» — «Я не сдавал на юбилей!» — «Вот и сдали.» The boss
passes showing off a new gold watch: «Булкин! Спасибо за часы! Мы же одна семья!» Фикус: «Поздравляю. Ты премировал начальника.»
Rewatch clue: the sheet «СБОР НА ЮБИЛЕЙ В. П.» is on the honor board from the first frame; the tape at the twist says «ПРОЧЕЕ −20 300».
No loop at the end, no background blur, the ficus close-up = a real camera move onto the windowsill.
  python3 ep02.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import fx
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import kscast as C
from props import kskit as K
from props import decals as D
from props import rusigns as R
from props import mimic as M
from props.kskit import at, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T0

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='ks', lang='ru', promise='ЗАВТРА: КОРПОРАТИВ'),
              promo='ru')
TAB = (C.XTRA, C.EXPR)
FE = M.Face([(0.0, 'hopeful'), (3.29, 'beam'), (6.5, 'beam'), (9.0, 'proud'), (10.9, 'hopeful'), (12.9, 'bark'), (14.95, 'shock'),
             (17.0, 'shock'), (19.6, 'panic'), (22.0, 'shock'), (24.5, 'bark'), (26.44, 'crushed'), (27.6, 'crushed')], TAB, seed=3)
FF = M.Face([(0.0, 'deadpan'), (6.48, 'smirk'), (8.3, 'deadpan'), (31.58, 'deadpan'), (32.6, 'smirk')], TAB, seed=8)
FL = M.Face([(0.0, 'strict'), (9.0, 'deadpan'), (26.44, 'smirk')], TAB, seed=11)
FS = M.Face([(0.0, 'boss'), (27.55, 'sweet')], TAB, seed=5)
WS_SILL = 2.9
SILL = (1040.0, 372.0)

# the rewatch clue: the collection notice on the honor board, from the first frame
D.attach(K.world('office'), [(R.plate(66, 72, ['СБОР НА ЮБИЛЕЙ', 'В. П. ГРОМОВА', '20 300', 'С КАЖДОГО', 'ДОБРОВОЛЬНО-', 'ОБЯЗАТЕЛЬНО'],
                                      bg=(252, 250, 240), colors=[(190, 40, 40), (40, 70, 130), (190, 40, 40), (34, 30, 28), (34, 30, 28),
                                                                  (34, 30, 28)], border=None, pad=1.0, weights=[0.9, 0.7, 1.3, 0.7, 0.6, 0.6]),
                              337, 186)])


def mouth(who, t): return M.mouth(EPI.talk, who, t)


def kw_(F, who, t, base, **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def ekw(t, base=(0.7, 0.0), **kw): return kw_(FE, 'edik', t, base, **kw)
def fkw(t, base=(0.0, 0.0), **kw): return kw_(FF, 'fikus', t, base, **kw)
def lkw(t, base=(0.7, 0.0), **kw): return kw_(FL, 'lyuda', t, base, **kw)
def skw(t, base=(0.7, 0.0), **kw): return kw_(FS, 'shef', t, base, **kw)


def floor_actor(fn, wx, wy, Z, **kw): return K.A(fn, wx, wy, K.ws_at(wy) * 3 * Z, **kw)


def shot(name, cx, cy, Z, **kw):
    kw.setdefault('dof_k', 0.0)
    kw.setdefault('clock', '16:40')
    return K.shot(name, cx, cy, Z, **kw)


def tally(big, text, fg=(255, 232, 110), y=380, size=64):
    img = O.sticker(text, fg=fg, size=size)
    O.overlay(big, img, (OUT_W - img.shape[1]) // 2, y, 1.0)


# ================================================================== 0: HOOK — «Булкин, распишитесь. Годовая премия — сорок тысяч.»
def r_hook(t, u):
    Z = 1.2
    cx, cy = 480.0, 330.0
    ly = floor_actor(C.lyuda, 405.0, 575.0, Z, **lkw(t, (0.9, 0.0), hand_n=(12.0, 40.0), prop_n=lambda sp, h: C.envelope(sp, h)))
    ed = floor_actor(C.edik, 545.0, 585.0, Z, flip=True,
                     **ekw(t, (-0.9, 0.2), hand_n=(16.0, 40.0), prop_n=(lambda sp, h: C.envelope(sp, h)) if t > 1.6 else None))
    return shot('office', cx, cy, Z, acts=[ly, ed], par=(-6 + 8 * u, 0), t=t)


# ================================================================== close-ups
def r_ecu(t, u, base=(0.0, 0.0), y=860, **kw):
    Z = 1.3
    cx, cy = 520.0, 360.0
    v = K.V('office', cx, cy, Z)
    ed = at(C.edik, v, 540, y, 32.0, pin='head', near=0.99, **ekw(t, base, **kw))
    return shot('office', cx, cy, Z, acts=[ed], par=(-6 + 10 * u, 0), t=t)


def r_lcu(t, u, base=(0.0, -0.2), stick=None):
    Z = 1.3
    cx, cy = 440.0, 330.0
    v = K.V('office', cx, cy, Z)
    ly = at(C.lyuda, v, 540, 860, 34.0, pin='head', near=0.99, **lkw(t, base, hand_n=(9.0, 40.0), prop_n=lambda sp, h: C.calc(sp, h)))
    big = shot('office', cx, cy, Z, acts=[ly], par=(4 - 6 * u, 0), t=t)
    if stick: tally(big, *stick)
    return big


def r_fik(t, u, Z0=2.3):
    """the ficus close-up = the camera moves in on the windowsill (the pot stands ON the sill at its real size)"""
    Z = Z0 + 0.06 * u
    fk = K.A(C.fikus, SILL[0], SILL[1], WS_SILL * 3 * Z, **fkw(t))
    return shot('office', SILL[0] + 6.0, 290.0, Z, acts=[fk], par=(-2 + 3 * u, 0), t=t)


def r_e1(t, u): return r_ecu(t, u, (0.9, 0.1), hand_n=(18.0, 62.0 + 3 * math.sin(t * 8)), prop_n=lambda sp, h: C.envelope(sp, h))
def r_fik1(t, u): return r_fik(t, u)
def r_l3(t, u): return r_lcu(t, u, stick=('20 000', (255, 200, 110), 380, 72))
def r_e3(t, u): return r_ecu(t, u, (0.0, 0.0), sweat=1.0, hand_n=(12.0, 52.0), prop_n=lambda sp, h: C.envelope(sp, h))
def r_l4(t, u): return r_lcu(t, u, stick=('12 × 5 МИНУТ', (140, 236, 150), 380, 60))
def r_e5(t, u): return r_ecu(t, u, (0.0, 0.2), sweat=2.0, hand_n=(10.0, 44.0), hand_f=(-4.0, 44.0))
def r_e4(t, u): return r_ecu(t, u, (-0.3, 0.0), sweat=2.0, hand_n=(18.0, 64.0), hand_f=(-6.0, 50.0))
def r_l7(t, u): return r_lcu(t, u, (0.6, 0.0))
def r_f2(t, u): return r_fik(t, u, 2.2)


# ================================================================== 3 / 7: the calculator-printer and its tape
def calc_insert(t, rows, total, red=False, shake=0.0):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    yy = np.linspace(0, 1, OUT_H)[:, None, None]
    big[:] = (np.array((150, 118, 84)) * (1 - yy) + np.array((110, 84, 58)) * yy).astype(np.uint8)          # the desk
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    ox = int(6 * math.sin(t * 60) * shake)
    d.rounded_rectangle([140 + ox, 1040, 940 + ox, 1820], 36, fill=(206, 200, 184), outline=(60, 54, 46), width=10)   # the machine
    d.rectangle([200 + ox, 1090, 880 + ox, 1230], fill=(40, 60, 46), outline=(30, 30, 30), width=8)                # the display
    f = O.pfont(84)
    d.text((850 + ox - f.getlength(total), 1118), total, font=f, fill=(255, 80, 70) if red else (150, 240, 150))
    for r in range(4):
        for c in range(5):
            col = (236, 120, 60) if c == 4 else (236, 232, 220)
            d.rounded_rectangle([210 + c * 135 + ox, 1280 + r * 125, 320 + c * 135 + ox, 1380 + r * 125], 16, fill=col, outline=(80, 74, 64), width=4)
    h_ = 120 + 96 * len(rows)
    d.rectangle([250 + ox, 1060 - h_, 830 + ox, 1060], fill=(250, 248, 238))                                 # the paper tape
    for i, (a, b, c_) in enumerate(rows):
        y = 1060 - h_ + 50 + i * 96
        fa = O.pfont(30)
        d.text((272 + ox, y), a, font=fa, fill=c_); d.text((808 + ox - fa.getlength(b), y), b, font=fa, fill=c_)
    return np.array(im)


INK, RED, GRN = (40, 40, 44), (200, 40, 40), (40, 120, 60)


def r_calc(t, u):
    rows = [('ПРЕМИЯ', '40 000', INK), ('НАЛОГ', '-5 000', RED)]
    total = '35 000'
    if t > 9.9: rows.append(('=', '35 000', GRN))
    return calc_insert(t, rows, total)


def r_twist(t, u):
    rows = [('ПРЕМИЯ', '40 000', INK), ('НАЛОГ', '-5 000', RED), ('ОПОЗДАНИЯ', '-15 000', RED), ('ПРОЧЕЕ', '-20 300', RED),
            ('ИТОГО', '-300', RED)]
    big = calc_insert(t, rows, '-300', red=True, shake=max(0.0, 1 - u / 0.6))
    tally(big, 'ВЫ ДОЛЖНЫ 300 ₽'.replace('₽', 'Р'), (255, 110, 100), 300, 70)
    return big


# ================================================================== 9: the collection notice on the honor board (real camera move)
def r_board(t, u):
    Z = 2.2 + 0.25 * glide(u / 2.0)
    return shot('office', 370.0, 225.0, Z, acts=[], par=(0, 0), t=t)


# ================================================================== 12: the boss passes, showing off the new gold watch
def r_shef(t, u):
    Z = 1.15
    cx, cy = 400.0, 340.0
    v = K.V('office', cx, cy, Z)
    w = glide(min(1.0, u / 2.4))
    sh = floor_actor(C.shef, lerp(250.0, 330.0, w), 528.0, Z, **skw(t, (0.9, 0.2), walk=t * 6.0 if u < 2.4 else None,
                                                                    hand_n=(14.0, 76.0) if u > 1.0 else None))
    ly = floor_actor(C.lyuda, 420.0, 582.0, Z, **lkw(t, (-0.6, 0.0), hand_n=(9.0, 40.0), prop_n=lambda sp, h: C.calc(sp, h)))
    ed = floor_actor(C.edik, 545.0, 590.0, Z, flip=True, **ekw(t, (-0.9, 0.0)))
    def f(big, v_):
        if hasattr(sh, 'last') and u > 1.0:
            hx, hy = aout(sh, v, 'hand')
            M.sparkle(big, hx + 10, hy - 30, t, px=8, col=(255, 236, 140))
            M.sparkle(big, hx - 26, hy + 6, t + 0.3, px=6, col=(255, 236, 140))
    return shot('office', cx, cy, Z, acts=[sh, ly, ed], par=(-4 + 6 * u, 0), t=t, fx_=f)


R = [r_hook, r_e1, r_fik1, r_calc, r_l3, r_e3, r_l4, r_twist, r_e5, r_board, r_e4, r_l7, r_shef, r_f2]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['ГОДОВАЯ', 'ПРЕМИЯ!'], hook_t=(0.10, 2.6), hook_y=210, hook_size=80,
              stickers=[(K.st('40 000!', fg=(255, 232, 110), size=84), 3.4, 5.6, 540, 400)],
              flashes=[TWIST], mosaics=[9.01, 22.02],
              cap_y={0: 1560, 1: 1560, 2: 1580, 3: 1720, 4: 1560, 5: 1560, 6: 1560, 7: 1720, 8: 1560, 9: 1560, 10: 1560, 11: 1560,
                     12: 1560, 13: 1580})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
