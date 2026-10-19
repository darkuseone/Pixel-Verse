"""S01E06 «СЛАДОСТЬ ИЛИ ГАДОСТЬ?!» (19.10.2026; finale, 31.6 s, twist at 16.3 s / 52 %).
HOOK: 31 October, the doorbell: three trick-or-treating students (zombie, vampire, skeleton) at door 13 — «Сладость или гадость?!» —
«Дед, костюм — топ! Где брал?» — «Это — лицо.» He has nothing in the sideboard but the crystal duck — he brings the egg with the needle:
«Отдаю самое дорогое — смерть свою!» — «Дед, нам бы — шоколадку.» He takes off his crown and unwraps it: chocolate foil, empty. Яга from
below: «Хэллоуин — не наш праздник!» TWIST (the reward is the same problem): the phone pings — «СОЦФОНД: ПЕНСИЯ НАЧИСЛЕНА» — «Дождался!»
— 13 ₽ 66 к. He pours the coins into a student's palm: «Дед. Это — гадость.» — «Это — пенсия.» Leaving, the students pass Яга on the
bench: «Бабуль, классный костюм Бабы Яги!» — «Я — в халате.» Кузьмич unwraps a candy in his box: «Жуть.» SEASON LOOP: the Соцфонд window,
Кощей pressed to the glass (= first frame of E01): «Тринадцать рублей?!» — «СЕЗОН 2: ДЕД МОРОЗ ПО ЗАПИСИ».
  python3 ep06.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='kosh', lang='ru'))
STAIRS = K.world('stairs')
FLAT = K.world('flat')
YARD = K.world('yard')
OFF = K.world('office')
CAL = K.calendar(0)
WS = 5.4
FL_S = 606.0
COSTUMES = [('zombie', 420.0), ('vampire', 510.0), ('skeleton', 600.0)]


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def students(t, Z, s=WS, xs=None, front=0, **kw):
    acts = []
    for i, (cos, x) in enumerate(COSTUMES):
        x = xs[i] if xs else x
        m = mouth('student', t) if i == front else 0.0
        acts.append(A(C.student, x, FL_S, s * 1.05 * 3 * Z, flip=True, t=t + i, costume=cos, expr='grin' if m < 0.05 else 'cheer', mouth_=m,
                      look=(0.8, 0.0), **kw))
    return acts[::-1]


def kosh_door(t, Z, x=280.0, **kw):
    return A(C.koshchei, x, FL_S, WS * 3 * Z, t=t, mouth_=mouth('koshchei', t), look=(0.8, 0.0), **kw)


# ================================================================== 0: HOOK — «Сладость или гадость?!»
def r_hook(t, u):
    Z = 1.0
    k = kosh_door(t, Z, expr='shock', hand_n=(12.0, 32.0))
    st = students(t, Z, front=1)
    def f(big, v):
        for i, a in enumerate(st):
            hx, hy = aout(a, v, 'head')
            fx.glow(big, hx, hy + 200, 160, (255, 180, 80), 0.15)
    big = K.shot(STAIRS, K.light_stairs, 420.0, 350.0, Z, acts=[k] + st, fx_=f, sy=330)
    if u < 0.3: K.CK.shake(big, t, 6, 40)
    return big


# ================================================================== 1: COSTUME — «Дед, костюм — топ!»
def r_costume(t, u):
    m = mouth('student', t)
    big, a = K.cu(C.student, t, STAIRS, 600.0, 330.0, 1.3, 19.0, head=(640, 880), light=K.light_stairs, blur=2, flip=True,
                  costume='zombie', expr='cheer' if m > 0.05 else 'grin', mouth_=m, look=(0.8, 0.1), hand_n=(10.0, 44.0))
    return big


# ================================================================== 2: FACE — «Это — лицо.»
def r_face(t, u):
    big, a = K.cu(C.koshchei, t, STAIRS, 260.0, 330.0, 1.3, 22.0, head=(480, 900), light=K.light_stairs, blur=2,
                  expr='glare' if not speaking('koshchei', t) else 'angry', mouth_=mouth('koshchei', t), look=(0.6, 0.0),
                  hand_n=(9.0, 30.0))
    return big


# ================================================================== 3: DEATH — the egg with the needle, solemnly
def r_death(t, u):
    Z = 1.3
    k = A(C.koshchei, 520.0, 690.0, 5.0 * 3 * Z, t=t, expr='proud' if not speaking('koshchei', t) else 'shout', mouth_=mouth('koshchei', t),
          look=(0.6, 0.3), hand_n=(20.0, 50.0), prop_n=lambda sp, h: C.needle_egg(sp, h), fire=0.6)
    def f(big, v):
        D.blit(big, v, CAL, 1146.0, 250.0)
        ea = aout(k, v, 'egg')
        fx.glow(big, ea[0], ea[1], 160, (255, 236, 150), 0.45)
    return K.shot(FLAT, K.light_flat, 460.0, 400.0, Z, acts=[k], fx_=f, sy=330)


# ================================================================== 4: CHOCO — «Дед, нам бы — шоколадку.»
def r_choco(t, u):
    Z = 1.0
    k = kosh_door(t, Z, expr='stunned', hand_n=(20.0, 46.0), prop_n=lambda sp, h: C.needle_egg(sp, h))
    st = students(t, Z, front=0)
    return K.shot(STAIRS, K.light_stairs, 420.0, 400.0, Z, acts=[k] + st, sy=330)


# ================================================================== 5: CROWN — he unwraps his foil crown: empty
def r_crown(t, u):
    def f(big, v, a):
        hx, hy = aout(a, v, 'hand_n')
        flat = sm(u / 0.4)
        w = int(lerp(120, 300, flat)); h = int(lerp(110, 40, flat))
        big[int(hy - h):int(hy), int(hx - w // 2):int(hx + w // 2)] = (236, 190, 70)
        for i in range(0, w, 20): big[int(hy - h):int(hy), int(hx - w // 2 + i):int(hx - w // 2 + i + 6)] = (255, 236, 150)
    big, a = K.cu(C.koshchei, t, STAIRS, 260.0, 330.0, 1.3, 20.0, head=(480, 860), light=K.light_stairs, blur=2, extra_fx=f, crown=False,
                  expr='sad', look=(0.6, -0.9), hand_n=(18.0, 54.0))
    return big


# ================================================================== 6: YAGA from below
def r_yaga(t, u):
    big, a = K.cu(C.yaga, t, YARD, 280.0, 400.0, 1.5, 17.0, head=(560, 1000), light=K.light_yard, blur=2,
                  expr='angry' if speaking('yaga', t) else 'gossip', mouth_=mouth('yaga', t), look=(0.6, 0.9), hand_n=(12.0, 40.0))
    return big


# ================================================================== 7: TWIST — «СОЦФОНД: ПЕНСИЯ НАЧИСЛЕНА» — «Дождался!» — 13 ₽ 66 к.
def r_sms(t, u):
    m = mouth('koshchei', t)
    def f(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.green_fire(big, hx - 260, hy - 100, t, r=60, k=0.6, seed=7); K.green_fire(big, hx + 280, hy - 90, t, r=60, k=0.6, seed=8)
    big, a = K.cu(C.koshchei, t, STAIRS, 260.0, 330.0, 1.3, 20.0, head=(480, 1060), light=K.light_stairs, blur=2, extra_fx=f,
                  expr='cheer', mouth_=max(0.3, m), look=(0.3, 0.6), hand_n=(18.0, 52.0), prop_n=lambda sp, h: C.phone_btn(sp, h, env=True, glow=1.0),
                  hand_f=(-14.0, 60.0))
    K.phone_card(big, t, 16.35, 18.9, ['СОЦФОНД', 'ПЕНСИЯ НАЧИСЛЕНА:', '13 ₽ 66 к.'], icon='СФ', icon_col=(34, 70, 130), y=520,
                 colors=[(30, 30, 40), (40, 40, 50), (190, 30, 34)])
    return big


# ================================================================== 8: COINS — «Это — гадость.» — «Это — пенсия.»
def r_coins(t, u):
    Z = 1.55
    give = sm(u / 0.4)
    k = kosh_door(t, Z, expr='proud' if not speaking('koshchei', t) else 'smile', hand_n=(lerp(12.0, 26.0, give), 40.0),
                  prop_n=C.coins if u < 0.6 else None)
    st = students(t, Z, front=0, xs=[400.0, 480.0, 560.0])
    def f(big, v):
        if 0.4 < u < 1.0:
            ha = aout(k, v, 'hand_n')
            for i in range(5):
                ph = (u - 0.4) / 0.6
                big[int(ha[1] + ph * 120 + i * 6):int(ha[1] + ph * 120 + i * 6) + 14, int(ha[0] + i * 16):int(ha[0] + i * 16) + 14] = (230, 190, 90)
    return K.shot(STAIRS, K.light_stairs, 360.0, 380.0, Z, acts=[k] + st, fx_=f, sy=330)


# ================================================================== 9: BENCH — «Бабуль, классный костюм Бабы Яги!» — «Я — в халате.»
def r_bench(t, u):
    Z = 1.25
    walk = sm(u / 4.0)
    st = []
    for i, (cos, x) in enumerate(COSTUMES):
        m = mouth('student', t) if i == 1 else 0.0
        st.append(A(C.student, lerp(495.0, 545.0, walk) + i * 72, 600.0, 4.2 * 1.05 * 3 * Z, flip=True, t=t + i, costume=cos,
                    expr='cheer' if m > 0.05 else 'grin', mouth_=m, look=(0.8, 0.0)))
    yg = A(C.yaga, 425.0, 600.0, 4.2 * 1.1 * 3 * Z, t=t, expr='glare' if not speaking('yaga', t) else 'angry', mouth_=mouth('yaga', t),
           look=(0.8, 0.0))
    return K.shot(YARD, K.light_yard, 512.0, 400.0, Z, acts=[yg] + st[::-1], sy=330)


# ================================================================== 10: Кузьмич unwraps a candy: «Жуть.»
def r_zhut(t, u):
    def pre(big, v):
        x0, y0 = v.opt(430.0, 150.0); x1, y1 = v.opt(512.0, 262.0)
        big[int(y0):int(y1), int(x0):int(x1)] = (24, 22, 22)
    def f(big, v, a):
        hx, hy = aout(a, v, 'head')
        big[int(hy + 120):int(hy + 170), int(hx + 120):int(hx + 200)] = (220, 40, 60)
    big, a = K.cu(C.domovoy, t, STAIRS, 470.0, 190.0, 4.4, 30.0, head=(560, 1010), light=K.light_stairs, pre_fx=pre, extra_fx=f,
                  expr='zhut', mouth_=mouth('kuzmich', t, 2.0), look=(0.0, -0.1), glow=(int(t * 3) % 2) * 1.0)
    return big


# ================================================================== 11: SEASON LOOP — the Соцфонд window again (= E01 first frame)
def r_season(t, u):
    m = mouth('koshchei', t)
    def f(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.green_fire(big, hx - 70, hy - 20, t, r=40, k=0.5, seed=1)
        K.green_fire(big, hx + 110, hy - 10, t, r=40, k=0.5, seed=2)
    big, a = K.cu(C.koshchei, t, OFF, 652.0, 330.0, 1.35, 23.0, head=(500, 900), light=K.light_office, blur=3, extra_fx=f,
                  expr='scream', mouth_=max(0.45, m), look=(0.5, 0.1), fire=0.8, hand_n=(9.0, 30.0), hand_f=(-7.0, 30.0),
                  prop_n=lambda sp, h: C.pension_slip(sp, (h[0] + 2.0, h[1] + 2.0)))
    k_ = sm((u - 0.35) / 0.2) * (1 - sm((u - 1.35) / 0.15))
    K.ticker_text(big, 'СЕЗОН 2:', 1180, 64, k=k_)
    K.ticker_text(big, 'ДЕД МОРОЗ', 1290, 64, k=k_)
    K.ticker_text(big, 'ПО ЗАПИСИ', 1400, 64, k=k_)
    return big


R_ = [r_hook, r_costume, r_face, r_death, r_choco, r_crown, r_yaga, r_sms, r_coins, r_bench, r_zhut, r_season]
assert len(R_) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 6, ['СЛАДОСТЬ', 'ИЛИ ГАДОСТЬ?!'], hook_t=(0.10, 2.10), hook_y=230, hook_size=70,
              stickers=[(K.st('ЭТО ЛИЦО', fg=(120, 255, 150)), 5.6, 6.7, 540, 560),
                        (K.st('13 РУБ?!', fg=(255, 90, 80), size=90), 17.2, 18.8, 540, 1240),
                        (K.st('ГАДОСТЬ', fg=(255, 160, 220)), 20.2, 21.3, 540, 560)],
              flashes=[TWIST, CUTS[-2]], mosaics=[],
              cap_y={0: 1640, 1: 1600, 2: 1640, 3: 1640, 4: 1640, 5: 1640, 6: 1640, 7: 1700, 8: 1640, 9: 1640, 10: 1520, 11: 1640})


def render(t):
    i = max(0, min(len(R_) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R_[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
