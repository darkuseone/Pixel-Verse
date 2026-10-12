"""S01E01 v2 «9 000 ЗА ТЕПЛО?!» (pilot, remake 12.10.2026 after the owner's notes: a clear story in long takes, selfie camera + a tripod,
new rough voice, series-own sound design; 32.0 s, twist at 17.95 s / 56 %).
SELFIE: Прохор shakes the heating bill at his phone — «Девять тыщ за отопление?!» — «А я в тайгу переехал. Тут тепло — бесплатно!»
WIDE (his phone on a tripod in the snow records): he trudges to the den — «Лайфхак: зимой медведь — это батарея.»
TRIPOD CAM: «Тихо. Спит.» — he crawls into the hole. DEN (one take, push-in): he snuggles into the sleeping bear —
«Тридцать восемь градусов. Без счётчика.» — «Городские, учитесь.» TWIST: the snot bubble pops, one eye opens: «Отопление. Девять тысяч.»,
the card reader beeps. «Нету...» — «Отключаю.» — a paw shove: he flies out of the den, lands by his tripod and freezes into a block of ice.
TRIPOD CAM: «Го-городские... не учитесь.» — the paw slaps the bill on the ice: «Плюс пени.» Loops into the bill of the hook.
  python3 ep01.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props import taigakit as K
from props.taigakit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='taiga', lang='ru'))
PORCH, TAIGA, DEN = K.world('porch'), K.world('taiga2'), K.world('den2')
WT = 2.2                     # taiga clearing: world px per sprite px (he is ~150 world px, the cave mouth 183)
WD = 4.1                     # den
CAVE = (805.0, 500.0, 102.0, 92.0)      # cave mouth ellipse on taiga2 (cx, cy, rx, ry); its floor at y ~ 585
GROUND = 612.0
TRIPOD = (430.0, 690.0)       # the tripod in the foreground of the wide shots
BEAR = (720.0, 612.0)


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def bill_prop(big=True):
    def f(sp, h): C.bill(sp, h, big=big)
    return f


def handheld(t, amp=1.0):
    """selfie camera wobble (output px)"""
    return (math.sin(t * 2.3) * 10 + math.sin(t * 5.1) * 4) * amp, (math.sin(t * 1.7 + 1) * 8 + math.sin(t * 6.3) * 3) * amp


def shift(big, dx, dy):
    if not dx and not dy: return big
    return np.roll(np.roll(big, int(dy), 0), int(dx), 1)


def cave_swallow(big, v, x_front):
    """the part of the hero that is already inside the cave mouth goes dark: inside the mouth ellipse and right of x_front (world)"""
    xs, ys = v.grid()
    cx, cy, rx, ry = CAVE
    X = xs[None, :].astype(np.float32); Y = ys[:, None].astype(np.float32)
    inside = ((((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2) < 1.0) & (X > x_front)
    bg = v.bg()
    big[inside] = bg[inside]


# ================================================================== 0: SELFIE at the cabin
def r_selfie(t, u):
    """his phone at arm's length (front camera): the bill — «Девять тыщ за отопление?!», then the taiga behind him — «Тут тепло — бесплатно!»"""
    m = mouth('prokhor', t)
    hook = t < 2.3
    sz = 25.0 if hook else 21.0
    head = (340, 1000) if hook else (420, 1040)
    def f(big, v, a):
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 30, hy + 10, t, 0.6 + 0.6 * m, dirx=1.0, scale=1.6, period=1.3)
    kw = dict(expr='shout', hand_n=(17.0, 44.0), prop_n=bill_prop()) if hook else \
         dict(expr='grin' if t < 4.3 else 'proud', hand_n=(26.0, 40.0) if t > 4.3 else (18.0, 30.0))
    pan = 0.0 if hook else sm((t - 2.3) / 2.0)
    big, a = K.cu(C.prokhor, t, PORCH, 380.0 + 360.0 * pan, 330.0, 1.25, sz, head=head, light=K.light_porch, blur=2, extra_fx=f,
                  mouth_=max(0.4 if hook else 0.0, m), look=(0.5, 0.0), **kw)
    big = shift(big, *handheld(t, 1.2))
    if hook and t < 0.35: K.CK.shake(big, t, 12, 33)
    K.blog_frame(big, t)
    return big


# ================================================================== 1: WIDE — the tripod records, he walks to the den
def r_walk(t, u):
    Z = 1.5
    k = sm(u / 3.9)
    x = lerp(330.0, 640.0, k)
    point = t > 8.9
    a = A(C.prokhor, x, GROUND, WT * 3 * Z, t=t, expr='grin' if speaking('prokhor', t) else 'proud', mouth_=mouth('prokhor', t),
          walk=None if point and k > 0.98 else t * 7.0, look=(1.0, 0.0), hand_n=(22.0, 46.0) if point else None)
    cxw = lerp(300.0, 610.0, k)
    tp = A(C.tripod, cxw - 92.0, 700.0, WT * 1.25 * 3 * Z, t=t)
    def f(big, v):
        ox, oy = v.opt(845, 220)
        for i in range(3):                                                        # the den breathes steam
            ph = (t * 0.5 + i / 3) % 1.0
            K.puff(big, ox + 30 * math.sin(t + i), oy - 260 * ph, 26 + 50 * ph, 0.45 * (1 - ph), (236, 240, 250))
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 24, hy, t, 0.5)
    return K.shot(TAIGA, K.light_taiga2, cxw, 470.0, Z, acts=[a, tp], fx_=f, sy=330)


# ================================================================== 2: TRIPOD CAM at the cave — «Тихо. Спит.» and he crawls in
def r_crawl(t, u):
    Z = 1.5
    crawl = sm((t - 11.55) / 1.4)
    if t < 11.55:
        a = A(C.prokhor, 700.0, GROUND, WT * 3 * Z, t=t, expr='sly', mouth_=mouth('prokhor', t, 1.2), look=(-0.4, 0.2),
              hand_n=(15.0, 49.0), flip=True)
        front = 9999
    else:
        x = lerp(690.0, 820.0, crawl)
        a = A(C.prokhor, x, GROUND - 6.0, WT * 3 * Z, t=t, expr='sly', rot=-72.0, pivot=(0.0, 20.0), walk=t * 14.0,
              hand_n=(20.0, 26.0 + 3 * math.sin(t * 14)), hand_f=(17.0, 22.0 - 3 * math.sin(t * 14)))
        front = lerp(790.0, 712.0, crawl)
    def f(big, v):
        if front < 9999: cave_swallow(big, v, front)
        K.blog_frame(big, t)
    return K.shot(TAIGA, K.light_taiga2, 760.0, 480.0, Z, acts=[a], fx_=f, sy=330)


# ================================================================== 3: DEN — one take: he snuggles into the sleeping bear
def bear_act(t, Z, **kw):
    return A(C.potapych, BEAR[0], BEAR[1], WD * 3 * Z, t=t, **kw)


def r_den(t, u):
    k = sm(u / 4.9)
    Z = lerp(1.0, 1.55, k)
    cx, cy = lerp(560.0, 715.0, k), lerp(450.0, 470.0, k)
    sit = t >= 13.75
    b = bear_act(t, Z, expr='asleep', hand_n=(-6.0, 24.0) if sit else None)
    if not sit:                                                                     # crawling in from the entrance, flat on his belly
        x = lerp(160.0, 600.0, sm(u / 0.75))
        p = A(C.prokhor, x, 650.0, WD * 3 * Z, t=t, expr='grin', rot=-80.0, pivot=(0.0, 20.0), walk=t * 14.0)
    else:
        p = A(C.prokhor, 742.0, 712.0, WD * 3 * Z, t=t, legs=False, expr='bliss' if not speaking('prokhor', t) else
              ('smug' if t > 16.0 else 'bliss'), mouth_=mouth('prokhor', t, 1.3), hand_n=(17.0, 24.0), hand_f=(-14.0, 26.0),
              look=(0.0, 0.0), sweat=sm((t - 14.5) / 1.0))
    def f(big, v):
        if sit:
            hx, hy = aout(p, v, 'head')
            for i in range(3):                                                          # he steams in the warmth
                ph = (t * 0.6 + i / 3) % 1.0
                K.puff(big, hx - 60 + 60 * i, hy - 220 - 260 * ph, 30 + 40 * ph, 0.30 * (1 - ph), (255, 240, 220))
        K.sweat_glow(big, 0.5 * sm((t - 14.0) / 2.0))
    return K.shot(DEN, K.light_den2, cx, cy, Z, acts=[b, p], fx_=f, sy=330)


# ================================================================== 4: TWIST — the bubble pops, one eye opens
def r_eye(t, u):
    awake = t >= 18.0
    bub = 0.0 if awake else min(1.0, 0.75 + 0.25 * u / 0.05)
    big, a = K.cu(C.potapych, t, DEN, 715.0, 420.0, 1.5, 23.0 - 1.5 * sm(u / 1.3), head=(470, 980), light=K.light_den2, blur=5,
                  expr='boss' if awake else 'asleep', eyes='one' if awake else None, bubble=bub, snore=not awake,
                  mouth_=mouth('bear', t, 1.4))
    if u < 0.3: K.CK.shake(big, t, 14, 40)
    return big


# ================================================================== 5: the bear sits up with the card reader, Прохор frozen in his lap
def r_terminal(t, u):
    Z = 1.35
    lift = sm((t - 19.4) / 0.5)
    b = bear_act(t, Z, expr='boss', mouth_=mouth('bear', t, 1.4), hand_n=(26.0 + 4 * lift, 18.0 + 30.0 * lift),
                 prop_n=lambda sp, h: C.terminal(sp, h, glow=lift))
    p = A(C.prokhor, 742.0, 712.0, WD * 3 * Z, t=t, legs=False, expr='shock', mouth_=0.3, hand_n=(18.0, 44.0), hand_f=(-14.0, 42.0),
          look=(0.8, 0.4))
    return K.shot(DEN, K.light_den2, 735.0, 440.0, Z, acts=[b, p], sy=330)


def r_plead(t, u):
    big, a = K.cu(C.prokhor, t, DEN, 700.0, 440.0, 1.5, 21.0 + 0.8 * u, head=(560, 960), light=K.light_den2, blur=4,
                  expr='plead', mouth_=mouth('prokhor', t), look=(-0.6, 0.4), legs=False, hand_n=(15.0, 40.0), hand_f=(-6.0, 40.0))
    return big


def r_shove(t, u):
    """«Отключаю.» — and the paw shoves: the frame whips"""
    hit_ = sm((t - 23.35) / 0.25)
    big, a = K.cu(C.potapych, t, DEN, 715.0, 420.0, 1.5, 19.0, head=(470 - 120 * hit_, 860), light=K.light_den2, blur=3,
                  expr='angry' if t < 23.3 else 'boss', mouth_=mouth('bear', t, 1.5), hand_n=(30.0 - 34.0 * hit_, 40.0), rot=-12 * hit_,
                  pivot=(0.0, 40.0))
    if hit_ > 0:
        fx.speed_lines(big, t, hit_)
        K.CK.shake(big, t, 22 * hit_, 30)
    return big


# ================================================================== 8: WIDE — he flies out, lands by the tripod and freezes
def r_fly(t, u):
    Z = 1.25
    k = min(1.0, u / 0.75)
    x = lerp(790.0, 610.0, k); y = lerp(560.0, GROUND + 8.0, k) - 170.0 * math.sin(math.pi * k)
    ice = sm((t - 24.85) / 0.8)
    a = A(C.prokhor, x, y, WT * 3 * Z, t=t, expr='shock' if ice < 0.5 else 'frozen', mouth_=0.8 if k < 1 else 0.2,
          rot=0 if k >= 1 else -360 * k, pivot=(0.0, 30.0), post=(lambda sp: C.ice_over(sp, ice)) if ice > 0 else None)
    tp = A(C.tripod, 552.0, 700.0, WT * 1.25 * 3 * Z, t=t)
    def f(big, v):
        ox, oy = v.opt(610.0, GROUND)
        K.snow_burst(big, ox, oy - 30, t, 24.65, n=60)
        if 0 < ice < 1: fx.glow(big, ox, oy - 200, 520, (210, 236, 255), 0.45 * (1 - ice))
    big = K.shot(TAIGA, K.light_taiga2, 660.0, 470.0, Z, acts=[a, tp], fx_=f, sy=330)
    if 0.70 < u < 1.0: K.CK.shake(big, t, 16, 36)
    return big


# ================================================================== 9: TRIPOD CAM — the ice block; the paw slaps the bill: «Плюс пени.»
def r_ice(t, u):
    slap = sm((t - 29.85) / 0.25)
    def f(big, v, a):
        if slap > 0:
            pw = A(C.bear_paw, wpt(v, 1200 - 520 * slap, 1250)[0], wpt(v, 0, 1250)[1], 19.0, t=t, reach=1.0)
            pw(big, v, None)
        K.blog_frame(big, t)
    big, a = K.cu(C.prokhor, t, TAIGA, 540.0, 500.0, 1.5, 17.5 + 0.6 * u, head=(520, 900), light=K.light_taiga2, blur=3, extra_fx=f,
                  expr='chatter', chatter=1.0 if speaking('prokhor', t) or t < 29.8 else 0.0, mouth_=mouth('prokhor', t, 1.2),
                  look=(0.0, 0.1), post=lambda sp: C.ice_over(sp, 1.0))
    if 29.85 <= t < 30.05: K.CK.shake(big, t, 10, 40)
    return big


R = [r_selfie, r_walk, r_crawl, r_den, r_eye, r_terminal, r_plead, r_shove, r_fly, r_ice]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 1, ['9 000 ЗА', 'ТЕПЛО?!'], hook_t=(0.10, 2.25), hook_y=420,
              stickers=[(K.st('ЛАЙФХАК №1', fg=(255, 214, 80)), 8.6, 10.2, 540, 560),
                        (K.st('ТАРИФ: 0 ₽', fg=(150, 255, 160)), 14.4, 15.9, 560, 520),
                        (K.st('9 000 ₽', fg=(255, 90, 80), size=84), 19.7, 21.25, 540, 330)],
              flashes=[TWIST, 23.45], mosaics=[],
              cap_y={0: 1560, 1: 1000, 2: 1560, 3: 1620, 4: 1450, 5: 1660, 9: 1580})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
