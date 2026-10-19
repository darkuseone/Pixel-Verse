"""S01E02 «ЗВОНЯТ ИЗ БАНКА?!» (19.10.2026; ~30.4 s, twist at 16.6 s / 55 %).
HOOK: the push-button phone rings, Кощей at his ear, a call card «СЛУЖБА БЕЗОПАСНОСТИ» — «Служба безопасности банка «Сберёг». Ваша смерть —
в опасности!» He glances at the sideboard (the crystal duck): «Откуда вы знаете, где она?!» — then proud: «Я — Кощей Бессмертный! Меня не
обманешь!» — «Тогда продиктуйте код из СМС.» — «Семь. Три.» (Кузьмич twirls a finger at his temple behind the sideboard) — «Иглу положите
на балкон.» — he carries the egg-and-needle out. TWIST (the villain is one of us): pull back on the facade — one balcony above sits Змей
Горыныч, three heads, three phones, a laptop «КОЛЛ-ЦЕНТР», a fishing line coming down for the needle: «О, сосед! Здорово!» — «Горыныч?!» —
«Это не мы. Это — алгоритм.» Яга from the bench below: «Мне тоже звонили — внуком!» — head 3: «Бабуль, это тоже я.» Кузьмич: «Жуть.»
LOOP: the phone rings again (= first frame).
  python3 ep02.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import koshcast as C
from props import koshkit as K
from props import decals as D
from props.koshkit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

COL = dict(K.COL, gorynych_live=K.COL['gorynych'], gorynych3=K.COL['gorynych'])
EPI = Episode('ep02', VOICE, DUR, FPS, colors=COL, slug=SLUG, endcard=dict(style='kosh', lang='ru'))
FLAT = K.world('flat')
FAC = K.world('facade')
YARD = K.world('yard')
STAIRS = K.world('stairs')
CAL = K.calendar(5)
WPF = 5.0                      # flat: world px per sprite px
FLOOR = 690.0


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def flat_fx(t, duck=True):
    def f(big, v):
        D.blit(big, v, CAL, 1146.0, 250.0)
        if duck: A(lambda sp, **k: C.duck(sp, (0.0, 0.0)), 232.0, 396.0, WPF * 0.9 * 3 * v.Z, t=t)(big, v, None)
    return f


def call_card(big, t, t0, t1):
    K.phone_card(big, t, t0, t1, ['ВХОДЯЩИЙ ВЫЗОВ', 'СЛУЖБА БЕЗОПАСНОСТИ', '«СБЕРЁГ»'], icon='$', icon_col=(40, 140, 70), y=620,
                 colors=[(30, 30, 40), (190, 30, 34), (40, 120, 60)])


def phone_at_ear(sp, h):
    C.phone_btn(sp, h, glow=1.0)


# ================================================================== 0: HOOK — the phone rings
def r_hook(t, u, loop=False):
    ring = 0.5 + 0.5 * math.sin(t * 30)
    big, a = K.cu(C.koshchei, t, FLAT, 600.0, 330.0, 1.3, 22.0, head=(520, 930), light=K.light_flat, blur=3, pre_fx=flat_fx(t),
                  expr='shock' if not loop else 'stunned', mouth_=0.2, look=(-0.3, 0.2), hand_f=(-7.0, 63.0), prop_f=phone_at_ear,
                  hand_n=(9.0, 30.0))
    big = K.shift(big, *K.handheld(t, 0.6))
    if not loop: call_card(big, t, 0.15, 4.05)
    else: call_card(big, t, CUTS[-2] + 0.1, DUR)
    if (t < 0.6 or loop) and ring > 0.6: K.CK.shake(big, t, 6, 40)
    return big


# ================================================================== 1: WHERE — he glances at the sideboard
def r_where(t, u):
    Z = 1.45
    k = A(C.koshchei, 445.0, FLOOR, WPF * 3 * Z, t=t, expr='nervous', mouth_=mouth('koshchei', t), look=(-1.0, -0.1),
          hand_f=(-7.0, 63.0), prop_f=phone_at_ear, hand_n=(6.0, 30.0), flip=True)
    return K.shot(FLAT, K.light_flat, 400.0, 400.0, Z, acts=[k], fx_=flat_fx(t), sy=330)


# ================================================================== 2: PROUD — «Меня не обманешь!»
def r_proud(t, u):
    Z = lerp(1.05, 1.15, u / 4.2)
    k = A(C.koshchei, 600.0, FLOOR, WPF * 3 * Z, t=t, expr='proud' if not speaking('koshchei', t) else 'shout', mouth_=mouth('koshchei', t),
          look=(0.4, 0.2), hand_f=(-7.0, 63.0), prop_f=phone_at_ear, hand_n=(22.0, 52.0), fire=0.5 if speaking('koshchei', t) else 0.0)
    return K.shot(FLAT, K.light_flat, 560.0, 380.0, Z, acts=[k], fx_=flat_fx(t), sy=330)


# ================================================================== 3: CODE — «Семь. Три.» + Кузьмич twirls a finger at his temple
def r_code(t, u):
    Z = 1.2
    k = A(C.koshchei, 620.0, FLOOR, WPF * 3 * Z, t=t, expr='normal' if not speaking('koshchei', t) else 'shout', mouth_=mouth('koshchei', t),
          look=(0.3, 0.4), hand_f=(-7.0, 63.0), prop_f=phone_at_ear, hand_n=(10.0, 30.0))
    peek = sm((u - 1.4) / 0.4)
    dom = A(C.domovoy, 400.0 + 20 * peek, 596.0, WPF * 1.0 * 3 * Z, t=t, expr='deadpan', look=(1.0, 0.0))
    def f(big, v):
        flat_fx(t)(big, v)
        if peek > 0.5:                                                         # the finger twirling at his temple
            hx, hy = v.opt(400.0 + 20 * peek + 20, 596.0 - 80)
            a_ = t * 14
            big[int(hy + math.sin(a_) * 12) - 9:int(hy + math.sin(a_) * 12) + 9, int(hx + math.cos(a_) * 14) - 9:int(hx + math.cos(a_) * 14) + 9] = (176, 170, 160)
    return K.shot(FLAT, K.light_flat, 520.0, 400.0, Z, acts=[dom, k], fx_=f, sy=330)


# ================================================================== 4: NEEDLE — out of the duck, out of the egg, onto the balcony
def r_needle(t, u):
    Z = 1.6
    k = A(C.koshchei, 500.0, FLOOR, WPF * 3 * Z, t=t, expr='normal', mouth_=0.0, look=(0.8, 0.2), hand_f=(-7.0, 63.0), prop_f=phone_at_ear,
          hand_n=(20.0, 44.0), prop_n=lambda sp, h: C.needle_egg(sp, h, cracked=u > 0.8))
    return K.shot(FLAT, K.light_flat, 520.0, 420.0, Z, acts=[k], fx_=flat_fx(t, duck=False), sy=330)


# ================================================================== 5: TWIST — the facade: Горыныч one balcony up
def gor_balcony(t, Z, heads_m=None, s=2.4):
    heads_m = heads_m or (mouth('gorynych_live', t), mouth('gorynych_live', t) * 0.6, mouth('gorynych3', t))
    return A(C.gorynych, 600.0, 396.0, s * 3 * Z, t=t, phones=True, laptop=True, mouths=heads_m, wave=1.0 if t < 19.0 else 0.0,
             exprs=('grin', 'smug', 'grin'), looks=[(0.3, -0.8)] * 3, post=lambda sp: sp.clip_below(30.0))


def r_facade(t, u):
    pull = sm(u / 1.0)
    Z = lerp(2.6, 1.7, pull)
    cy = lerp(470.0, 405.0, pull)
    g = gor_balcony(t, Z)
    k = A(C.koshchei, 650.0, 556.0, 2.1 * 3 * Z, t=t, expr='shock' if t < 18.8 else 'scream', mouth_=mouth('koshchei', t), look=(0.2, 0.9),
          hand_n=(20.0, 50.0), prop_n=lambda sp, h: C.needle_egg(sp, h), hand_f=(-7.0, 63.0), prop_f=phone_at_ear,
          post=lambda sp: sp.clip_below(44.0))
    def f(big, v):
        ga = aout(g, v, 'head1'); ka = aout(k, v, 'egg')
        n = 40
        for i in range(n):                                                    # the fishing line from above to the needle
            q = i / n
            x = lerp(ga[0] - 40, ka[0] + 20, q) + math.sin(q * 3.1) * 20; y = lerp(ga[1], ka[1] - 40 + 60 * (1 - sm((t - 17.2) / 0.6)), q)
            big[int(y):int(y) + 4, int(x):int(x) + 4] = (220, 220, 230)
    big = K.shot(FAC, K.light_facade, 640.0, cy, Z, acts=[g, k], fx_=f, sy=330)
    if u < 0.4: fx.speed_lines(big, t, 1 - u / 0.4)
    return big


# ================================================================== 6: ALGO — the three heads close up
def r_algo(t, u):
    m = mouth('gorynych_live', t)
    big, a = K.cu(C.gorynych, t, FAC, 640.0, 330.0, 1.4, 21.0, head=(600, 1000), light=K.light_facade, blur=3, phones=True, laptop=True,
                  mouths=(m, m * 0.4, m * 0.2), exprs=('smug', 'deadpan', 'grin'), looks=[(0.3, -0.5)] * 3, post=lambda sp: sp.clip_below(18.0))
    return big


# ================================================================== 7: YAGA on the bench below
def r_yaga(t, u):
    big, a = K.cu(C.yaga, t, YARD, 330.0, 420.0, 1.5, 17.0, head=(520, 980), light=K.light_yard, blur=2, flip=False,
                  expr='angry' if speaking('yaga', t) else 'gossip', mouth_=mouth('yaga', t), look=(0.6, 0.9), hand_n=(12.0, 36.0))
    return big


# ================================================================== 8: HEAD 3 — «Бабуль, это тоже я.»
def r_head3(t, u):
    m = mouth('gorynych3', t)
    big, a = K.cu(C.gorynych, t, FAC, 700.0, 330.0, 1.4, 24.0, head=(300, 1150), light=K.light_facade, blur=3, phones=True,
                  mouths=(0.0, 0.0, m), exprs=('deadpan', 'deadpan', 'nervous'), looks=[(0.5, -0.9)] * 3, post=lambda sp: sp.clip_below(18.0))
    return big


# ================================================================== 9: Кузьмич in his box on the landing: «Жуть.»
def r_zhut(t, u):
    def pre(big, v):
        x0, y0 = v.opt(430.0, 150.0); x1, y1 = v.opt(512.0, 262.0)
        big[int(y0):int(y1), int(x0):int(x1)] = (24, 22, 22)
    big, a = K.cu(C.domovoy, t, STAIRS, 470.0, 190.0, 4.4, 30.0, head=(560, 1010), light=K.light_stairs, pre_fx=pre,
                  expr='zhut', mouth_=mouth('kuzmich', t, 2.0), look=(0.0, -0.1), glow=(int(t * 3) % 2) * 1.0)
    return big


def r_loop(t, u):
    return r_hook(t, u, loop=True)


R_ = [r_hook, r_where, r_proud, r_code, r_needle, r_facade, r_algo, r_yaga, r_head3, r_zhut, r_loop]
assert len(R_) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 2, ['ЗВОНЯТ', 'ИЗ БАНКА?!'], hook_t=(0.10, 2.70), hook_y=230,
              stickers=[(K.st('КОД ИЗ СМС', fg=(255, 220, 110)), 11.2, 12.8, 540, 560),
                        (K.st('СОСЕД?!', fg=(255, 90, 80), size=84), 16.7, 18.2, 540, 520),
                        (K.st('АЛГОРИТМ', fg=(170, 236, 110)), 21.6, 22.6, 540, 520),
                        (K.st('ЭТО ТОЖЕ Я', fg=(255, 220, 110)), 27.0, 28.2, 540, 520)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1640, 1: 1640, 2: 1640, 3: 1640, 4: 1640, 5: 1640, 6: 1560, 7: 1640, 8: 1600, 9: 1520, 10: 1640})


def render(t):
    i = max(0, min(len(R_) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R_[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
