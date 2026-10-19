"""S01E05 «СВЕТ ОТКЛЮЧАТ?!» (19.10.2026; 30.4 s, twist at 16.6 s / 55 %) — the season's peak.
HOOK: Галина Аркадьевна on a stool at the stairwell electrical box with huge bolt cutters; Кощей in a double foil crown holding a carved
zucchini lantern (pumpkins are 1499 ₽): «Свет отрезать — в Хэллоуин?!» — she unrolls a printout to the floor: «Долг за свет — 47 рублей.
С 1902-го.» — «Я — Кощей Бессмертный!» — «А долг — вечный.» SNIP — black. PARTY in the dark: zucchini lanterns, Горыныч with three
torches in three mouths, Яга's coal eyes, Кощей's green eyes: «Ну вот. Теперь — атмосфера.» Галина alone on the black stairs, her phone
torch dying (1 %), drips, the garbage chute moans. TWIST (the hunter asks for help): two green eyes open right in front of her — she grabs
his vest: «Кощей Кощеевич. Проводите до выхода.» He leads her down, his eyes as a torch: «Свет — по графику.» At the entrance she hands
him the cutters and runs; Яга: «Кощей! Ты — страшный!» — «Правда?» — «С лица — да.» Кузьмич pulls the breaker up himself — light, the
party cheers: «Жуть.» LOOP: the light blinks out — snip (= first frame).
  python3 ep05.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props import rusigns as R
from props.koshkit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='kosh', lang='ru'))
STAIRS = K.world('stairs')
FLAT = K.world('flat')
YARD = K.world('yard')
WS = 5.4
FL_S = 606.0
STOOL_H = 70.0                  # world px: Галина stands on a stool to reach the box
CAL = K.calendar(2)
PUMPKIN = R.plate(64, 30, ['ТЫКВА 1499 ₽', 'ОБОЙДЁМСЯ'], bg=(250, 200, 60), fg=(30, 28, 30), border=(190, 30, 34), bw=1.0,
                  colors=[(190, 30, 34), (30, 28, 30)])


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def stool(big, v, x):
    x0, y0 = v.opt(x - 34.0, FL_S - STOOL_H); x1, y1 = v.opt(x + 34.0, FL_S - STOOL_H + 10.0)
    big[int(y0):int(y1), int(x0):int(x1)] = (150, 100, 60)
    for lx in (x - 28.0, x + 22.0):
        a0, b0 = v.opt(lx, FL_S - STOOL_H + 10.0); a1, b1 = v.opt(lx + 6.0, FL_S)
        big[int(b0):int(b1), int(a0):int(a1)] = (120, 80, 50)


def zucchini_hand(sp, h):
    C.zucchini(sp, (h[0] + 1.0, h[1] - 2.0), lit=1.0)


def galina_stool(t, Z, cut=0.4, **kw):
    gm = mouth('galina', t)
    return A(C.galina, 540.0, FL_S - STOOL_H, WS * 1.0 * 3 * Z, flip=True, t=t, expr='deadpan' if gm < 0.05 else 'normal', mouth_=gm,
             look=(0.6, 0.6), hand_n=(12.0, 50.0), prop_n=lambda sp, h: C.cutters(sp, h, cut), **kw)


def kosh_party(t, Z, x=270.0, **kw):
    return A(C.koshchei, x, FL_S, WS * 3 * Z, t=t, mouth_=mouth('koshchei', t), look=(0.8, 0.2), hand_n=(18.0, 34.0),
             prop_n=zucchini_hand, **kw)


# ================================================================== 0: HOOK — the cutters at the box
def r_hook(t, u, loop=False):
    Z = 1.2
    snap = K.hit(t, 0.0, 0.25) if not loop else K.hit(t, 29.85, 0.25)
    g = galina_stool(t, Z, cut=0.1 + 0.6 * snap)
    k = kosh_party(t, Z, x=330.0, expr='scream' if not loop else 'shock')
    def pre(big, v): stool(big, v, 540.0)
    def f(big, v):
        ha = aout(k, v, 'hand_n'); K.candles(big, [(ha[0] + 20, ha[1] - 30)], t, 0.8)
        if loop and t > 29.4: K.darken(big, sm((t - 29.4) / 0.3) * 0.8)
    big = K.shot(STAIRS, K.light_stairs, 440.0, 330.0, Z, acts=[k, g], pre=pre, fx_=f, sy=330)
    if snap > 0.5: K.CK.shake(big, t, 8, 40)
    return big


# ================================================================== 1: DEBT — the printout to the floor
def r_debt(t, u):
    gm = mouth('galina', t)
    unroll = sm(u / 1.2)
    def f(big, v, a):
        hx, hy = aout(a, v, 'hand_f')
        y1 = hy + unroll * 1200
        big[int(hy):int(min(OUT_H, y1)), int(hx - 70):int(hx + 70)] = (244, 240, 226)
        for yy in range(int(hy) + 20, int(min(OUT_H, y1)), 36):
            big[yy:yy + 8, int(hx - 56):int(hx + 40 - (yy % 50))] = (120, 120, 130)
    big, a = K.cu(C.galina, t, STAIRS, 500.0, 330.0, 1.3, 20.0, head=(600, 820), light=K.light_stairs, blur=2, extra_fx=f, flip=True,
                  expr='deadpan' if gm < 0.05 else 'normal', mouth_=gm, look=(0.2, -0.8), hand_f=(-2.0, 22.0),
                  hand_n=(6.0, 36.0), prop_n=lambda sp, h: C.cutters(sp, h, 0.2))
    return big


# ================================================================== 2: ETERNAL — «Я — Кощей Бессмертный!» — «А долг — вечный.» — snip
def r_eternal(t, u):
    Z = 1.1
    snip = t > 11.1
    g = galina_stool(t, Z, cut=0.7 if t < 11.0 else 0.0)
    k = kosh_party(t, Z, x=320.0, expr='shout' if speaking('koshchei', t) else ('proud' if t < 9.6 else 'shock'),
                   fire=0.5 if speaking('koshchei', t) else 0.0)
    def pre(big, v): stool(big, v, 540.0)
    def f(big, v):
        ha = aout(k, v, 'hand_n'); K.candles(big, [(ha[0] + 20, ha[1] - 30)], t, 0.8)
        if snip: K.darken(big, sm((t - 11.1) / 0.12))
    return K.shot(STAIRS, K.light_stairs, 440.0, 380.0, Z, acts=[k, g], pre=pre, fx_=f, sy=330)


# ================================================================== 3: PARTY in the dark
def r_party(t, u):
    Z = 0.78
    gr = A(C.gorynych, 830.0, 690.0, 5.0 * 1.1 * 3 * Z, flip=True, t=t, mouths=(0.5, 0.5, 0.5), exprs=('grin', 'grin', 'grin'),
           looks=[(0.6, 0.2)] * 3)
    yg = A(C.yaga, 640.0, 690.0, 5.0 * 1.1 * 3 * Z, t=t, expr='sly', mouth_=mouth('yaga', t), look=(0.6, 0.0), prop_f=None)
    k = A(C.koshchei, 470.0, 690.0, 5.0 * 3 * Z, t=t, expr='grin', look=(0.6, 0.0), hand_n=(18.0, 34.0), prop_n=zucchini_hand)
    def f(big, v):
        K.darken(big, 0.55)
        D.blit(big, v, PUMPKIN, 120.0, 520.0)
        for x in (180.0, 300.0, 1000.0):
            ox, oy = v.opt(x, 670.0); K.candles(big, [(ox, oy)], t, 1.0)
            fx.glow(big, ox, oy, 120, (255, 190, 80), 0.35)
        for name in ('head1', 'head2', 'head3'):                              # torches in the dragon's three mouths
            hx, hy = aout(gr, v, name)
            fx.glow(big, hx - 120, hy + 30, 200, (255, 250, 210), 0.6)
        hx, hy = aout(k, v, 'head'); K.eyes_glow(big, [(hx + 20, hy - 30), (hx + 90, hy - 26)], r=18)
        yx, yy = aout(yg, v, 'head'); K.eyes_glow(big, [(yx + 20, yy - 16), (yx + 64, yy - 14)], r=14, col=(255, 120, 60))
        ha = aout(k, v, 'hand_n'); K.candles(big, [(ha[0] + 20, ha[1] - 30)], t, 1.0)
    big = K.shot(FLAT, K.light_dark, 640.0, 420.0, Z, acts=[k, yg, gr], fx_=f, sy=330)
    return big


# ================================================================== 4: ALONE — Галина on the black stairs, phone torch dying
def r_alone(t, u):
    Z = 1.6
    g = A(C.galina, 560.0, FL_S, WS * 1.2 * 3 * Z, flip=True, t=t, expr='nervous', mouth_=0.1, look=(-0.8, 0.3), scared=sm(u / 1.5),
          hand_n=(10.0, 30.0), prop_n=lambda sp, h: C.phone_btn(sp, h, glow=1.0))
    def f(big, v):
        K.darken(big, 0.6)
        ha = aout(g, v, 'hand_n')
        flick = 1.0 if (int(t * 9) % 4) else 0.3
        fx.glow(big, ha[0] - 40, ha[1] - 60, 260 * (1 - 0.6 * u / 2.1), (230, 240, 255), 0.55 * flick)
        K.phone_card(big, t, 14.6, 16.5, ['ЗАРЯД 1 %'], icon='!', icon_col=(190, 30, 34), y=380)
        rng = np.random.default_rng(int(t * 8))
        for i in range(3):                                                    # drips
            ph = (t * 1.3 + i * 0.33) % 1.0
            big[int(200 + ph * 1400):int(200 + ph * 1400) + 18, 200 + i * 300:212 + i * 300] = (120, 140, 160)
    return K.shot(STAIRS, K.light_dark, 560.0, 380.0, Z, acts=[g], fx_=f, sy=330)


# ================================================================== 5: TWIST — green eyes open in front of her; «Проводите до выхода»
def r_twist(t, u):
    Z = 1.75
    g = A(C.galina, 600.0, FL_S, WS * 1.2 * 3 * Z, flip=True, t=t, expr='panic' if u < 0.8 else 'plead' if False else 'nervous',
          mouth_=mouth('galina', t), look=(-0.9, 0.4), scared=1.0, hand_n=(14.0, 32.0), hand_f=(10.0, 30.0))
    k = A(C.koshchei, 470.0, FL_S, WS * 3 * Z, t=t, expr='sinister', look=(0.9, -0.4), hand_n=(12.0, 30.0))
    def f(big, v):
        K.darken(big, 0.68)
        hx, hy = aout(k, v, 'head')
        op = sm((u - 0.05) / 0.2)
        K.eyes_glow(big, [(hx + 20, hy - 30), (hx + 90, hy - 26)], k=op, r=22)
        fx.glow(big, hx + 50, hy, 360, (120, 255, 150), 0.25 * op)
    return K.shot(STAIRS, K.light_dark, 540.0, 360.0, Z, acts=[k, g], fx_=f, sy=330)


# ================================================================== 6: GUIDE — down the stairs, his eyes as a torch
def r_guide(t, u):
    Z = 1.3
    step = u * 2.0
    k = A(C.koshchei, 900.0 - 140 * sm(u / 2.6), FL_S - 10 * math.sin(step * 3), WS * 3 * Z, t=t, flip=True,
          expr='smug' if not speaking('koshchei', t) else 'proud', mouth_=mouth('koshchei', t), look=(0.9, -0.1), walk=t * 6,
          hand_n=(12.0, 30.0), hand_f=(-4.0, 34.0))
    g = A(C.galina, 1000.0 - 140 * sm(u / 2.6), FL_S - 10 * math.sin(step * 3 + 1), WS * 1.2 * 3 * Z, flip=True, t=t, expr='nervous',
          look=(-0.9, 0.0), scared=0.8, hand_n=(14.0, 30.0))
    def f(big, v):
        K.darken(big, 0.62)
        hx, hy = aout(k, v, 'head')
        K.eyes_glow(big, [(hx - 20, hy - 30), (hx - 90, hy - 26)], r=20)
        for i in range(10):                                                   # the green beam out of his eyes
            q = i / 10
            fx.glow(big, hx - 120 - 600 * q, hy + 40 + 260 * q, 90 + 120 * q, (120, 255, 150), 0.22 * (1 - q))
    return K.shot(STAIRS, K.light_dark, 820.0, 360.0, Z, acts=[g, k], fx_=f, sy=330)


# ================================================================== 7: YARD — she hands him the cutters and runs; Яга: «Ты — страшный!»
def r_yard(t, u):
    Z = 1.4
    run = sm((u - 0.6) / 1.2)
    k = A(C.koshchei, 300.0, 600.0, 4.2 * 3 * Z, t=t, expr='proud' if t < 25.7 else ('smile' if t < 26.7 else 'sad'),
          mouth_=mouth('koshchei', t), look=(0.8, 0.0), hand_n=(18.0, 44.0), prop_n=lambda sp, h: C.cutters(sp, h, 0.3))
    g = A(C.galina, lerp(380.0, 900.0, run), 600.0, 4.2 * 1.2 * 3 * Z, t=t, expr='panic', look=(0.8, 0.0), scared=0.6,
          hand_n=(14.0, 30.0))
    yg = A(C.yaga, 470.0, 600.0, 4.2 * 1.1 * 3 * Z, flip=True, t=t, expr='sly' if not speaking('yaga', t) else 'grin', mouth_=mouth('yaga', t),
           look=(0.8, 0.1))
    acts = [k, yg] + ([g] if run < 1 else [])
    return K.shot(YARD, K.light_yard, 380.0, 400.0, Z, acts=acts, sy=330)


# ================================================================== 8: Кузьмич pulls the breaker up himself: light! «Жуть.»
def r_zhut(t, u):
    on = sm((u - 0.15) / 0.1)
    def pre(big, v):
        x0, y0 = v.opt(430.0, 150.0); x1, y1 = v.opt(512.0, 262.0)
        big[int(y0):int(y1), int(x0):int(x1)] = (24, 22, 22)
        bx, by = v.opt(498.0, lerp(230.0, 170.0, on))
        big[int(by) - 40:int(by) + 40, int(bx) - 30:int(bx) + 30] = (200, 40, 40)                     # the breaker lever
    big, a = K.cu(C.domovoy, t, STAIRS, 470.0, 190.0, 4.4, 30.0, head=(520, 1010), light=K.light_stairs, pre_fx=pre,
                  expr='zhut', mouth_=mouth('kuzmich', t, 2.0), look=(0.6, -0.1), glow=1.0)
    if on < 1: K.darken(big, 0.8 * (1 - on))
    return big


def r_loop(t, u):
    return r_hook(t, u, loop=True)


R_ = [r_hook, r_debt, r_eternal, r_party, r_alone, r_twist, r_guide, r_yard, r_zhut, r_loop]
assert len(R_) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 5, ['СВЕТ', 'ОТКЛЮЧАТ?!'], hook_t=(0.10, 2.50), hook_y=230,
              stickers=[(K.st('+ ПЕНИ ЗА 124 ГОДА', fg=(255, 90, 80), size=52), 4.6, 6.8, 540, 560),
                        (K.st('ПО ГРАФИКУ', fg=(120, 255, 150)), 21.2, 22.4, 540, 520)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1640, 1: 1640, 2: 1640, 3: 1640, 4: 1640, 5: 1640, 6: 1640, 7: 1640, 8: 1520, 9: 1640})


def render(t):
    i = max(0, min(len(R_) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R_[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
