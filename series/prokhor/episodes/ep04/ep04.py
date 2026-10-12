"""S01E04 «К ВРАЧУ ЧЕРЕЗ МЕСЯЦ?!» (12.10.2026, v2 format; ~29.6 s, twist at 16.0 s / 54 %, type «бюрократическая рекурсия»).
SELFIE with a balloon cheek: the polyclinic app — «Запись к зубному — через месяц?!» — «Лайфхак: нитка и лось. Сам выдерну!» (the pan
shows the moose with a «САНИТАР» badge by the «ЛЕСНАЯ ПОЛИКЛИНИКА» sign). WIDE (tripod): the thread from his tooth to the moose's antler,
eyes shut — «Городские, учитесь! Лось — тяни!» The moose doesn't move: «Направление есть?» TRIPOD CAM: «Без направления не тяну.»
TWIST: push into the hollow of the big birch under «ЭЛЕКТРОННАЯ ОЧЕРЕДЬ» — the cuckoo pops out: «Талон — у кукушки.» He kneels:
«Кукушка, кукушка... Когда мой приём?» Cuckoo calls, a day counter runs 1..30, he counts on his mittens — and falls back into the snow:
«Месяц...» Button: the bear on the «ОЖИДАНИЕ» bench with a queue ticket: «Я за вами.»
  python3 ep04.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props.taigakit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

COL = dict(K.COL, moose=(200, 160, 255))
EPI = Episode('ep04', VOICE, DUR, FPS, colors=COL, slug=SLUG, endcard=dict(style='taiga', lang='ru'))
BIRCH = K.world('birch')
WB = 3.4                     # birch glade: world px per sprite px in the foreground
GROUND = 640.0
MOOSE_X = 430.0
HOLLOW = (1086.0, 446.0)     # the natural hollow of the big birch (the «registry»)
BENCH = (912.0, 520.0)       # seat of the «ОЖИДАНИЕ» bench
CALLS = (21.15, 24.55)       # the cuckoo's count: the day counter runs 1..30
THREAD = (236, 226, 200)


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def ticket(sp, h, num='№ 2'):
    """a queue ticket from the «electronic queue»"""
    x, y = h[0] + 2.0, h[1] + 2.4
    sp.sup(x, y, 4.2, 2.8, C.tones((246, 244, 236)), n=4.0, snow=False)
    sp.txt_box([num], (x - 3.6, y - 2.2, x + 3.6, y + 2.2), (30, 30, 40), pad=0.2)


def phone_prop(sp, h):
    C.phone(sp, h, rec=False)


def thread(big, p0, p1, t, twang=0.0, sag=40.0, w=6):
    """the thread from his tooth to the antler (output px): a sagging, vibrating line with a dark edge"""
    n = 60
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) + 1e-6
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    for i in range(n + 1):
        s = i / n
        x = lerp(x0, x1, s); y = lerp(y0, y1, s) + sag * 4 * s * (1 - s)
        vib = twang * 14 * math.sin(math.pi * s) * math.sin(t * 90.0)
        x += nx * vib; y += ny * vib
        xi, yi = int(x), int(y)
        if 0 <= xi - w < OUT_W - 2 * w and 0 <= yi - w < OUT_H - 2 * w:
            big[yi - w:yi + w, xi - w:xi + w] = (40, 34, 30)
    for i in range(n + 1):
        s = i / n
        x = lerp(x0, x1, s); y = lerp(y0, y1, s) + sag * 4 * s * (1 - s)
        vib = twang * 14 * math.sin(math.pi * s) * math.sin(t * 90.0)
        x += nx * vib; y += ny * vib
        xi, yi = int(x), int(y)
        if 0 <= xi - w < OUT_W - 2 * w and 0 <= yi - w < OUT_H - 2 * w:
            big[yi - w + 2:yi + w - 2, xi - w + 2:xi + w - 2] = THREAD


def antler(a, v):
    """output px of the tip of the near antler (head anchor + offset in sprite px)"""
    hx, hy = aout(a, v, 'head')
    sc = a.scale(v)
    return hx + (-1 if a.flip else 1) * 4.0 * sc, hy - 11.0 * sc


def twang(t):
    k = max(0.0, 1 - (t - 7.30) / 0.6) if t >= 7.30 else 0.0
    return k + (max(0.0, 1 - (t - 9.70) / 0.5) if t >= 9.70 else 0.0)


def moose_act(t, Z, x=MOOSE_X, flip=False, **kw):
    return A(F.critter, x, GROUND - 10.0, WB * 0.72 * 3 * Z, t=t, kind='moose', badge='САНИТАР', flip=flip,
             expr=kw.pop('expr', 'deadpan'), mouth_=mouth('moose', t, 1.4), look=kw.pop('look', (0.6, 0.0)), **kw)


def hollow_act(t, Z):
    return A(F.hollow, HOLLOW[0], HOLLOW[1] + 4, WB * 1.25 * 3 * Z, t=t)


_DAY = {}


def day_counter(big, t):
    if not (CALLS[0] <= t < CALLS[1] + 0.9): return
    p = min(1.0, (t - CALLS[0]) / (CALLS[1] - CALLS[0]))
    n = 1 + int(29 * p ** 1.4)
    if n not in _DAY: _DAY[n] = O.sticker(f'ДЕНЬ {n}', fg=(255, 236, 120) if n < 30 else (255, 90, 80), size=84)
    im = _DAY[n]
    O.overlay(big, im, (OUT_W - im.shape[1]) // 2, 300, 1.0)
    if ST.LOG[0] is not None: ST.log('sticker', bbox=((OUT_W - im.shape[1]) // 2, 300, (OUT_W + im.shape[1]) // 2, 300 + im.shape[0]))


# ================================================================== 0: SELFIE — the balloon cheek, the polyclinic app
def r_selfie(t, u):
    m = mouth('prokhor', t)
    hook = t < 3.1
    pan = sm((t - 3.6) / 2.6)
    v0 = view_at(BIRCH, 760.0 - 260.0 * pan, 400.0, 1.2, 180, 320)
    mz = moose_act(t, 1.2, x=MOOSE_X, expr='deadpan', look=(0.8, 0.0))
    def f(big, v, a):
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 30, hy + 10, t, 0.5 + 0.6 * m, scale=1.6, period=1.3)
    big, a = K.cu(C.prokhor, t, BIRCH, 760.0 - 260.0 * pan, 400.0, 1.2, 24.0 if hook else 21.0,
                  head=(520, 1240) if hook else (700, 1180), light=K.light_taiga2, blur=2, extra_fx=f, acts_before=[mz] if pan > 0 else (),
                  expr='shout' if hook else ('sly' if t < 5.0 else 'grin'), mouth_=max(0.4 if hook else 0.0, m), swollen=1.0,
                  look=(0.3, 0.2) if hook else (-0.7, 0.0), hand_n=(20.0, 30.0) if hook else (22.0, 34.0), flip=not hook)
    big = K.shift(big, *K.handheld(t, 1.2))
    if t < 0.3: K.CK.shake(big, t, 12, 33)
    if t > 3.1: K.blog_frame(big, t)
    K.phone_card(big, t, 0.15, 3.05, ['ЛЕСНАЯ ПОЛИКЛИНИКА', 'Стоматолог: ближайшая запись', 'через 30 дней'], icon='+',
                 icon_col=(200, 40, 50), y=700, colors=[(30, 30, 40), (90, 90, 100), (200, 30, 40)])
    return big


# ================================================================== 1: WIDE — the thread from the tooth to the antler
def r_wide(t, u):
    Z = 1.0
    pull = sm((t - 8.6) / 0.4) * (1 - sm((t - 10.2) / 0.4))
    a = A(C.prokhor, 680.0 + 14 * pull, GROUND, WB * 3 * Z, t=t, flip=True, expr='shout' if speaking('prokhor', t) else 'plead',
          mouth_=mouth('prokhor', t), swollen=1.0, blink=t > 8.4, look=(0.6, 0.0), lean=0.4 * pull, hand_n=(18.0, 52.0), hand_f=(-12.0, 50.0))
    mz = moose_act(t, Z, x=500.0, look=(0.2, -0.2))
    tp = A(C.tripod, 775.0, GROUND + 30.0, WB * 1.05 * 3 * Z, t=t, flip=True)
    def f(big, v):
        thread(big, aout(a, v, 'mouth'), antler(mz, v), t, twang(t), sag=60 * (1 - pull) + 6)
    return K.shot(BIRCH, K.light_taiga2, 620.0, 470.0, Z, acts=[mz, a, tp], fx_=f, sy=330)


# ================================================================== 2: the moose: «Направление есть?»
def r_moose(t, u):
    big, a = K.cu(F.critter, t, BIRCH, MOOSE_X - 40, 420.0, 1.3, 15.0, head=(560, 820), light=K.light_taiga2, blur=3,
                  kind='moose', badge='САНИТАР', expr='deadpan', mouth_=mouth('moose', t, 1.4), look=(0.7, -0.1), flip=False)
    if u < 0.5: K.breath(big, 860, 900, t, 1.0 - u * 2, scale=2.4, period=0.8)                  # the snort
    return big


# ================================================================== 3: TRIPOD CAM — «Без направления не тяну.»
def r_tripod(t, u):
    Z = 1.45
    a = A(C.prokhor, 625.0, GROUND, WB * 3 * Z, t=t, flip=True, expr='angry' if t < 15.2 else 'shock', mouth_=0.25, swollen=1.0,
          look=(0.8, 0.1), hand_n=(18.0, 46.0), hand_f=(-14.0, 30.0))
    mz = moose_act(t, Z, x=475.0, look=(0.6, 0.0))
    def f(big, v):
        thread(big, aout(a, v, 'mouth'), antler(mz, v), t, 0.0, sag=90)
    big = K.shot(BIRCH, K.light_taiga2, 555.0, 460.0, Z, acts=[mz, a], fx_=f, sy=330)
    K.blog_frame(big, t)
    return big


# ================================================================== 4: TWIST — the hollow under «ЭЛЕКТРОННАЯ ОЧЕРЕДЬ»: the cuckoo pops out
def r_cuckoo(t, u):
    Z = lerp(2.05, 2.3, sm(u / 1.6))
    pop = sm((u - 0.08) / 0.22)
    call = 0.9 if 0.15 < u < 0.4 or 0.55 < u < 0.8 else 0.1
    acts = [hollow_act(t, Z)]
    if pop > 0:
        acts.append(A(F.cuckoo, HOLLOW[0] - 2, HOLLOW[1] + 8 - 10 * pop, WB * 1.2 * (0.25 + 0.75 * pop) * 3 * Z, t=t, call=call,
                      look=(-0.6, 0.0), flip=True))
    big = K.shot(BIRCH, K.light_taiga2, HOLLOW[0] + 6, 400.0, Z, acts=acts, sy=320)
    if u < 0.25: K.CK.shake(big, t, 10, 40)
    return big


# ================================================================== 5: he kneels at the hollow: «Кукушка, кукушка... Когда мой приём?»
def r_plead(t, u):
    Z = 1.15
    a = A(C.prokhor, 985.0, GROUND - 6.0, WB * 3 * Z, t=t, expr='plead', mouth_=mouth('prokhor', t), swollen=1.0, look=(0.7, 0.5),
          hand_n=(16.0, 50.0), hand_f=(-8.0, 50.0), legs=False)
    bird = A(F.cuckoo, HOLLOW[0] - 2, HOLLOW[1] - 2, WB * 1.2 * 3 * Z, t=t, call=0.1, look=(-0.8, -0.4), flip=True)
    return K.shot(BIRCH, K.light_taiga2, 990.0, 440.0, Z, acts=[hollow_act(t, Z), bird, a], fx_=lambda b, v: None, sy=330)


# ================================================================== 6: the cuckoo counts (day counter 1..30)
def r_calls(t, u):
    call = 1.0 if (t * 2.6) % 1.0 < 0.45 else 0.1
    big, a = K.cu(F.cuckoo, t, BIRCH, HOLLOW[0] - 60, 570.0, 2.2, 34.0, head=(560, 900), light=K.light_taiga2, blur=3,
                  call=call, look=(-0.6, 0.0), flip=True)
    day_counter(big, t)
    return big


def r_count(t, u):
    k = 0.5 + 0.5 * math.sin(t * 9.0)
    big, a = K.cu(C.prokhor, t, BIRCH, 900.0, 420.0, 1.3, 22.0, head=(540, 980), light=K.light_taiga2, blur=3,
                  expr='plead' if u < 0.9 else 'frozen', mouth_=0.2 + 0.2 * k, swollen=1.0, look=(-0.4, 0.3), flip=True,
                  hand_n=(14.0 + 4 * k, 44.0), hand_f=(-12.0, 46.0 - 4 * k), sweat=0.6)
    day_counter(big, t)
    return big


# ================================================================== 8: he falls back into the snow: «Месяц...»
def r_fall(t, u):
    Z = 1.15
    fall = sm((t - 25.0) / 0.4)
    a = A(C.prokhor, 900.0, GROUND, WB * 3 * Z, t=t, flip=True, expr='frozen' if fall < 1 else 'asleep', mouth_=mouth('prokhor', t),
          swollen=1.0, look=(0.0, 0.6), hand_n=(18.0, 40.0), hand_f=(-12.0, 40.0), rot=-84 * fall, pivot=(0.0, 0.0))
    big = K.shot(BIRCH, K.light_taiga2, 800.0, 600.0, Z, acts=[a], sy=330)
    if t > 25.35:
        ox, oy = view_at(BIRCH, 800.0, 600.0, Z, 180, 330).opt(760.0, GROUND)
        K.snow_burst(big, ox, oy - 20, t, 25.35, n=60)
    return big


# ================================================================== 9: BUTTON — the bear on the «ОЖИДАНИЕ» bench with a ticket
def r_queue(t, u):
    Z = 1.15
    b = A(C.potapych, BENCH[0] - 10, BENCH[1] + 6, WB * 0.62 * 3 * Z, t=t, expr='boss' if speaking('bear', t) else 'asleep',
          mouth_=mouth('bear', t, 1.5), look=(-0.7, -0.3), hand_n=(26.0, 40.0), prop_n=ticket, flip=True,
          bubble=None if t < 28.75 else 0.0, snore=False)
    a = A(C.prokhor, 1010.0, GROUND + 36.0, WB * 1.1 * 3 * Z, t=t, flip=True, expr='asleep', swollen=1.0, rot=-84, pivot=(0.0, 0.0))
    return K.shot(BIRCH, K.light_taiga2, 890.0, 600.0, Z, acts=[b, a], sy=330)


R = [r_selfie, r_wide, r_moose, r_tripod, r_cuckoo, r_plead, r_calls, r_count, r_fall, r_queue]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 4, ['К ВРАЧУ', 'ЧЕРЕЗ МЕСЯЦ?!'], hook_t=(0.10, 3.0), hook_y=250,
              stickers=[(K.st('ЛАЙФХАК №4', fg=(255, 214, 80)), 3.3, 5.8, 540, 520),
                        (K.st('РЕГИСТРАТУРА', fg=(255, 90, 80), size=72), 16.1, 17.6, 540, 250),
                        (K.st('№ 2', fg=(255, 236, 120), size=96), 27.0, 28.4, 540, 420)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1720, 1: 1640, 2: 1640, 3: 1640, 4: 1640, 5: 1640, 6: 1640, 7: 1640, 8: 1120, 9: 1180})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
