"""S01E02 «ПВЗ ЗА 40 КМ?!» (12.10.2026, v2 format: a clear story in long takes, selfie + tripod; ~30 s, twist at 17.85 s / 59 %).
SELFIE: the app pings «заказ ждёт в пункте выдачи — 40 км»: «Сорок километров до пункта выдачи?!» WIDE (tripod in the snow): he hammers
a sign «ПУНКТ ВЫДАЧИ «ДИКАЯ ЯГОДА»» onto his cabin — «Лайфхак: открываю пункт выдачи у себя. Посылки сами придут!» TRIPOD CAM:
«Всё. Теперь я — пункт выдачи.» The fox courier skis in: «Лиса-Экспресс! Распишитесь: тут, тут и тут.» SELFIE with the box:
«Пять минут — и носки дома! Городские, учитесь!» TWIST (success is worse than failure): a whip pan — the whole taiga queues at HIS
pick-up point, the bear in front: «Мой заказ где? Неделю жду.» The fox tips her sled: «Это всё — вам. Вы же пункт выдачи!» — an avalanche
of parcels. Buried: «Я ж только носки заказал!» Button: the bear rates him on his phone — «Одна звезда.»
  python3 ep02.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import taigacast as C
from props import taigafauna as F
from props import taigakit as K
from props import rusigns as R
from props import decals as D
from props.taigakit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

COL = dict(K.COL, fox=(255, 170, 60))
EPI = Episode('ep02', VOICE, DUR, FPS, colors=COL, slug=SLUG, endcard=dict(style='taiga', lang='ru'))
PORCH = K.world('porch')
WP = 5.3                         # porch: world px per sprite px (he is ~360 world px, the window sill above his head)
GROUND = 700.0
PX = 170.0                       # Прохор by the wall
SIGN = R.plate(184, 56, ['ПУНКТ ВЫДАЧИ', '«ДИКАЯ ЯГОДА»'], bg=(150, 40, 150), colors=[(255, 255, 255), (255, 220, 120)],
               border=(255, 220, 120), weights=[1.0, 0.85], bw=1.6, pad=2.0)
SIGN_XY = (228.0, 338.0)
QUEUE = [('bear', 640.0, 712.0, 1.00), ('hare', 800.0, 690.0, 0.92), ('squirrel', 900.0, 672.0, 0.86), ('moose', 1010.0, 650.0, 0.78),
         ('hare', 1120.0, 630.0, 0.70), ('squirrel', 1190.0, 615.0, 0.64), ('fox', 1250.0, 600.0, 0.58)]


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def sign_fx(t, t_on=3.05):
    """the sign nailed on the wall: hangs crooked after the first nail, straight after the second"""
    def f(big, v):
        if t < t_on: return
        img = SIGN if t >= 4.7 else D.rotate(SIGN, 7.0)
        D.blit(big, v, img, *SIGN_XY)
    return f


def box_prop(sp, h):
    F.parcel(sp, (h[0] + 3.0, h[1] + 2.0), w=11.0, hh=8.0)


# ================================================================== 0: SELFIE — the app ping
def r_selfie(t, u):
    m = mouth('prokhor', t)
    def f(big, v, a):
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 30, hy + 10, t, 0.6 + 0.6 * m, scale=1.6, period=1.3)
    big, a = K.cu(C.prokhor, t, PORCH, 420.0, 360.0, 1.25, 24.0, head=(480, 1260), light=K.light_porch, blur=2, extra_fx=f,
                  expr='shout', mouth_=max(0.4, m), look=(0.2, 0.3), hand_n=(20.0, 30.0))
    big = K.shift(big, *K.handheld(t, 1.2))
    if t < 0.3: K.CK.shake(big, t, 12, 33)
    if t > 2.0: K.blog_frame(big, t)
    K.phone_card(big, t, 0.15, 2.75, ['ДИКАЯ ЯГОДА', 'Заказ ждёт в пункте выдачи', 'Расстояние: 40 км'], y=690,
                 colors=[(30, 30, 40), (90, 90, 100), (200, 30, 40)])
    return big


# ================================================================== 1: WIDE — he nails his own pick-up point sign
def r_hammer(t, u):
    Z = 0.95
    beat = [3.0, 4.6, 6.2]
    hk = max([max(0.0, 1 - abs(t - b) / 0.18) for b in beat])
    hand = (19.0, 58.0 + 5.0 * (1 - hk))
    a = A(C.prokhor, PX, GROUND, WP * 3 * Z, t=t, expr='grin' if speaking('prokhor', t) else 'proud', mouth_=mouth('prokhor', t),
          look=(0.4, 0.4), hand_n=hand, prop_n=lambda sp, h: F.hammer(sp, h, ang=0.9 - 0.9 * hk), hand_f=(-12.0, 30.0))
    tp = A(C.tripod, 470.0, 716.0, WP * 0.9 * 3 * Z, t=t)
    def f(big, v):
        sign_fx(t)(big, v)
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 24, hy, t, 0.4)
    big = K.shot(PORCH, K.light_porch, 300.0 + 20 * u, 460.0, Z, acts=[a, tp], fx_=f, sy=330)
    if hk > 0.7: K.CK.shake(big, t, 6, 40)
    return big


# ================================================================== 2: TRIPOD CAM — proud under the sign
def r_proud(t, u):
    Z = 1.35 + 0.04 * u
    a = A(C.prokhor, 250.0, GROUND, WP * 3 * Z, t=t, expr='proud' if not speaking('prokhor', t) else 'grin', mouth_=mouth('prokhor', t),
          look=(0.0, 0.0), hand_n=(21.0, 50.0), hand_f=(-14.0, 26.0))
    big = K.shot(PORCH, K.light_porch, 300.0, 430.0, Z, acts=[a], fx_=sign_fx(t), sy=330)
    K.blog_frame(big, t)
    return big


# ================================================================== 3: WIDE — the fox courier skis in
def r_fox(t, u):
    Z = 0.95
    k = sm(u / 1.1)
    fxw = lerp(720.0, 450.0, k)
    sign_now = speaking('fox', t) and t > 11.6
    fox = A(F.critter, fxw, GROUND + 4.0, WP * 3 * Z, flip=True, t=t, kind='fox', cap='courier', backpack=True,
            expr='sly' if not speaking('fox', t) else 'grin', mouth_=mouth('fox', t), walk=t * 9.0 if k < 1 else None,
            hand_n=(14.0, 22.0), prop_n=lambda sp, h: C.bill(sp, h))
    sl = A(F.sled, fxw + 160.0, GROUND + 6.0, WP * 3 * Z, flip=True, t=t, load=3)
    pen = sm((t - 12.0) / 0.3) * (1 - sm((t - 13.4) / 0.3))
    a = A(C.prokhor, PX + 40, GROUND, WP * 3 * Z, t=t, expr='grin', look=(0.8, -0.2),
          hand_n=(21.0 + 2 * math.sin(t * 20) * pen, 30.0 + pen * 2), hand_f=(-12.0, 28.0))
    def f(big, v):
        sign_fx(t)(big, v)
        if k < 1:
            ox, oy = v.opt(fxw + 60, GROUND)
            for i in range(4):
                ph = (t * 3 + i / 4) % 1.0
                K.puff(big, ox + 200 * ph, oy - 20 - 30 * ph, 20 + 40 * ph, 0.5 * (1 - ph))
    return K.shot(PORCH, K.light_porch, 360.0, 460.0, Z, acts=[sl, fox, a], fx_=f, sy=330)


# ================================================================== 4: SELFIE with the box
def r_box(t, u):
    m = mouth('prokhor', t)
    big, a = K.cu(C.prokhor, t, PORCH, 420.0, 360.0, 1.25, 22.0, head=(470, 1060), light=K.light_porch, blur=2,
                  expr='grin' if t < 15.9 else 'smug', mouth_=m, look=(0.2, 0.2), hand_n=(14.0, 30.0), prop_n=box_prop)
    big = K.shift(big, *K.handheld(t, 1.0))
    K.blog_frame(big, t)
    return big


# ================================================================== 5: TWIST — whip pan: the whole taiga queues at HIS pick-up point
def queue_acts(t, Z, hold=True):
    acts = []
    for i, (kind, x, y, sc) in enumerate(QUEUE):
        tt = t + i * 0.7
        if kind == 'bear':
            acts.append(A(C.potapych, x, y, WP * 0.62 * sc * 3 * Z, t=tt, expr='boss', mouth_=mouth('bear', t, 1.5),
                          hand_n=(28.0, 40.0), prop_n=lambda sp, h: C.bill(sp, h, amount='№ 0001')))
        else:
            acts.append(A(F.critter, x, y, WP * sc * 3 * Z, flip=True, t=tt, kind=kind, expr='angry' if i % 2 else 'deadpan',
                          badge='САНИТАР' if kind == 'moose' else None, hand_n=None,
                          prop_n=(lambda sp, h: F.parcel(sp, (h[0] + 2, h[1] + 1), w=6.0, hh=4.4, label='ВОЗВРАТ')) if kind != 'moose' else None))
    return acts[::-1]


def r_queue(t, u):
    Z = 1.0
    whip = sm(u / 0.45)
    cx = lerp(300.0, 700.0, whip) + 40.0 * sm((u - 0.45) / 2.6)
    a = A(C.prokhor, PX + 40, GROUND, WP * 3 * Z, t=t, expr='shock', look=(1.0, 0.0), hand_n=(14.0, 30.0), prop_n=box_prop)
    big = K.shot(PORCH, K.light_porch, cx, 440.0, Z, acts=queue_acts(t, Z) + [a], fx_=sign_fx(t), sy=330)
    if whip < 1: fx.speed_lines(big, t, 1 - whip)
    return big


# ================================================================== 6: the fox tips her sled — an avalanche of parcels
def r_dump(t, u):
    Z = 0.95
    fox = A(F.critter, 470.0, GROUND + 4.0, WP * 3 * Z, flip=True, t=t, kind='fox', cap='courier', backpack=True,
            expr='sly' if not speaking('fox', t) else 'grin', mouth_=mouth('fox', t), hand_n=(10.0, 44.0))
    sl = A(F.sled, 630.0, GROUND + 6.0, WP * 3 * Z, flip=True, t=t, load=3, rot=-22 * sm((t - 21.9) / 0.3), pivot=(0.0, 0.0))
    fall0 = 22.0
    bury = sm((t - fall0) / 1.6)
    a = A(C.prokhor, PX + 40, GROUND, WP * 3 * Z, t=t, expr='shock' if t < fall0 + 0.3 else 'panic', mouth_=0.6 if t > fall0 else 0.2,
          look=(0.4, 0.8), hand_n=(18.0, 56.0) if t > fall0 else (14.0, 30.0), prop_n=None if t > fall0 else box_prop)
    acts = [sl, fox, a]
    rng = np.random.default_rng(3)
    for i in range(16):                                                     # falling boxes, landing into a pile on him
        t_i = fall0 + i * 0.09
        if t < t_i: continue
        p = min(1.0, (t - t_i) / 0.45)
        x0 = PX + 40 + (rng.random() - 0.5) * 120
        top = GROUND - 30 - (i % 8) * 34 - (i // 8) * 10
        y = lerp(80.0, top, p * p)
        acts.append(A(F.parcel, x0, y, WP * 0.9 * 3 * Z, t=t, w=8.0 + rng.random() * 4, hh=6.0 + rng.random() * 2, standalone=True,
                      rot=(rng.random() - 0.5) * 40 * (1 - p)))
    big = K.shot(PORCH, K.light_porch, 380.0, 460.0, Z, acts=acts, fx_=sign_fx(t), sy=330)
    if fall0 < t < fall0 + 1.4: K.CK.shake(big, t, 10 * (1 - bury), 34)
    return big


# ================================================================== 7: buried — only his head and a mitten out of the pile
def r_buried(t, u):
    def f(big, v, a):
        rng = np.random.default_rng(11)
        hx, hy = aout(a, v, 'head')
        for i in range(9):                                                    # the pile in front of him (his scale)
            bx = hx - 380 + (i % 4) * 260 + rng.integers(-30, 30)
            by = hy + 330 + (i // 4) * 210 + rng.integers(-20, 20)
            w = 300 + rng.integers(0, 80); h = 200 + rng.integers(0, 40)
            pw = wpt(v, bx, by); A(F.parcel, pw[0], pw[1], 24.0, t=t, w=w / 24.0, hh=h / 24.0, standalone=True)(big, v, None)
    big, a = K.cu(C.prokhor, t, PORCH, 420.0, 400.0, 1.25, 21.0, head=(520, 900), light=K.light_porch, blur=3, extra_fx=f,
                  expr='panic', mouth_=mouth('prokhor', t), look=(0.0, 0.4), hand_n=(18.0, 62.0 + 2 * math.sin(t * 9)))
    return big


# ================================================================== 8: BUTTON — the bear rates him: one star
def r_rate(t, u):
    tap = t > 26.4
    big, a = K.cu(C.potapych, t, PORCH, 760.0, 420.0, 1.3, 15.0, head=(430, 860), light=K.light_porch, blur=3,
                  expr='boss', mouth_=mouth('bear', t, 1.5), look=(0.3, -0.4), hand_n=(24.0, 46.0), prop_n=lambda sp, h: C.phone(sp, h, rec=False))
    K.phone_card(big, t, 26.45, DUR, ['ОТЗЫВ О ПУНКТЕ ВЫДАЧИ', 'М. П. Топтыгин'], icon='ДЯ', y=1490, stars=1)
    return big


R = [r_selfie, r_hammer, r_proud, r_fox, r_box, r_queue, r_dump, r_buried, r_rate]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 2, ['ПВЗ ЗА', '40 КМ?!'], hook_t=(0.10, 2.70), hook_y=250,
              stickers=[(K.st('ЛАЙФХАК №2', fg=(255, 214, 80)), 3.2, 5.6, 540, 520),
                        (K.st('ОЧЕРЕДЬ', fg=(255, 90, 80), size=80), 18.2, 20.8, 540, 420)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1720, 1: 1640, 2: 1600, 3: 1640, 4: 1600, 5: 1500, 6: 1640, 7: 1640, 8: 1200})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
