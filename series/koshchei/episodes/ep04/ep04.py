"""S01E04 «БАТАРЕИ ЛЕДЯНЫЕ?!» (19.10.2026; 30.2 s, twist at 17.85 s / 59 %).
HOOK: Кощей hugs an ice-cold radiator, an icicle on his nose, frost on the foil crown, teeth chattering: «Октябрь — а батареи ледяные!»
Галина Аркадьевна in the УК by her orange heater, plaid, steaming tea, phone at her ear: «Отопительный сезон открыт. Батарею — потрогайте.»
His finger sticks to the ice («дзынь») — «Значит, до вас — не дошло.» — «Я — Кощей Бессмертный!» — «Бессмертный — не значит тёплый.»
He wraps himself in the wall carpet (a shawarma) and follows the steaming heating pipe across the yard: «Тепло — утекает.» TWIST (the reward
went to someone else): pull back — Яга's hut on chicken legs SITS on the pipe like a brooding hen, the chimney smoking, Яга in the window:
«Ножки мёрзнут.» — «Это ж общее тепло!» — «Было общее. Теперь — насиженное.» The hut clucks and lays a hot egg; Кощей reaches for it —
the hut sits back down. Кузьмич: «Жуть.» LOOP: he hugs the ice-cold radiator again (= first frame).
  python3 ep04.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props import taigakit as TK
from props import decals as D
from props.koshkit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='kosh', lang='ru'))
FLAT = K.world('flat')
DESK = K.world('desk')
YARD = K.world('yard')
STAIRS = K.world('stairs')
CAL = K.calendar(3)
WP = 5.0                         # flat
FLOOR = 690.0
WY = 4.2                         # yard
FL_Y = 600.0
HUT = (745.0, 352.0, 4.4)        # hut on the pipe: feet anchor + world px per sprite px


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def flat_fx(t, tv=False):
    def f(big, v):
        D.blit(big, v, CAL, 1146.0, 250.0)
        if tv:                                                               # the weather on the TV: «+12»
            x0, y0 = v.opt(848.0, 388.0); x1, y1 = v.opt(924.0, 450.0)
            big[int(y0):int(y1), int(x0):int(x1)] = (40, 60, 120)
    return f


def icicle(big, v, a, k=1.0):
    """an icicle hanging from his nose (output px from the head anchor)"""
    hx, hy = aout(a, v, 'head')
    sc = a.scale(v)
    nx, ny = hx + 11.5 * sc, hy + 5.4 * sc
    L = int(9 * sc * k)
    for i in range(L):
        w = max(1, int(0.9 * sc * (1 - i / max(1, L))))
        big[int(ny + i), int(nx - w):int(nx + w)] = (210, 236, 255)


def frosty(big, k=1.0):
    TK.frost_edges(big, k * 0.55, seed=2)


# ================================================================== 0: HOOK — hugging the ice-cold radiator
def r_hook(t, u, loop=False):
    m = mouth('koshchei', t)
    Z = 1.75
    k = A(C.koshchei, 448.0, FLOOR, WP * 3 * Z, t=t, expr='frozen' if (m < 0.05 or loop) else 'shout', mouth_=m, look=(0.6, -0.4),
          shiver=1.0, hand_n=(25.0, 31.0), hand_f=(20.0, 26.0), lean=0.6)
    def f(big, v):
        icicle(big, v, k)
        hx, hy = aout(k, v, 'head')
        K.steam(big, hx + 200, hy + 60, t, 0.7, 0.8)
        frosty(big, 0.8)
    return K.shot(FLAT, K.light_flat, 520.0, 450.0, Z, acts=[k], fx_=f, sy=330)


# ================================================================== 1: Галина in the УК — heater, plaid, tea, phone
def galina_phone(sp, h):
    C.phone_btn(sp, h, glow=1.0)


def r_galina(t, u):
    gm = mouth('galina', t)
    def pre(big, v):
        fx.glow(big, 860, 1500, 700, (255, 140, 60), 0.55)                 # the orange heater glow
    def f(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.steam(big, hx - 260, hy + 380, t, 0.6, 0.7)
        for i in range(5): big[1640:1660, 700 + i * 70:740 + i * 70] = (255, 120 + i * 20, 40)    # heater coil
    big, a = K.cu(C.galina, t, DESK, 600.0, 330.0, 1.05, 22.0, head=(680, 880), light=K.light_office, blur=2, pre_fx=pre, extra_fx=f,
                  flip=True, expr='content' if gm < 0.05 else 'normal', mouth_=gm, look=(0.4, -0.3),
                  hand_f=(-4.0, 40.0), prop_f=galina_phone, post=lambda sp: sp.clip_below(14.0))
    return big


# ================================================================== 2: STUCK — his finger freezes to the radiator
def r_stuck(t, u):
    pull = sm((u - 0.6) / 0.3) * math.sin(t * 30) * 0.4
    def f(big, v, a):
        frosty(big, 1.0)
        icicle(big, v, a)
    Z = 2.0
    k = A(C.koshchei, 448.0, FLOOR, WP * 3 * Z, t=t, expr='shock' if u < 1.0 else 'sad', mouth_=0.5 if u < 0.6 else 0.0, look=(0.9, -0.9),
          shiver=1.0, hand_n=(25.0 + pull, 31.0), hand_f=(-8.0, 30.0), lean=0.6)
    def g(big, v):
        f(big, v, k)
    return K.shot(FLAT, K.light_flat, 540.0, 470.0, Z, acts=[k], fx_=g, sy=330)


# ================================================================== 3: PROUD (shivering) — «Я — Кощей Бессмертный!»
def r_proud(t, u):
    Z = 1.15
    k = A(C.koshchei, 600.0, FLOOR, WP * 3 * Z, t=t, expr='shout' if speaking('koshchei', t) else ('frozen' if t < 12.85 else 'sad'),
          mouth_=mouth('koshchei', t), look=(0.4, 0.2), shiver=1.0, hand_n=(22.0, 54.0) if speaking('koshchei', t) else (12.0, 34.0),
          hand_f=(-7.0, 63.0), prop_f=lambda sp, h: C.phone_btn(sp, h))
    def f(big, v):
        flat_fx(t, tv=True)(big, v)
        x0, y0 = v.opt(848.0, 388.0)
        from props import rusigns as R
        D.blit(big, v, R.plate(76, 60, ['НА УЛИЦЕ', '+12'], bg=(40, 60, 120), fg=(255, 255, 255), border=None, weights=[0.5, 1.0]), 848.0, 390.0)
        icicle(big, v, k)
        frosty(big, 0.6)
    return K.shot(FLAT, K.light_flat, 640.0, 400.0, Z, acts=[k], fx_=f, sy=330)


# ================================================================== 4: CARPET — wrapped in the wall carpet, along the steaming pipe
def carpet_wrap(big, v, a):
    """the red wall carpet wrapped around him like shawarma (output px around the torso)"""
    hx, hy = aout(a, v, 'head')
    sc = a.scale(v)
    x0, x1 = int(hx - 9 * sc), int(hx + 8 * sc)
    y0, y1 = int(hy + 12 * sc), int(hy + 44 * sc)
    reg = big[max(0, y0):min(OUT_H, y1), max(0, x0):min(OUT_W, x1)]
    reg[:] = (150, 40, 34)
    hh, ww = reg.shape[:2]
    q = max(6, int(sc))
    for yy in range(0, hh, q * 4):
        for xx in range(0, ww, q * 4):
            reg[yy:yy + q * 2, xx + q:xx + q * 2] = (220, 160, 60)
    reg[:q, :] = (230, 190, 90); reg[-q:, :] = (230, 190, 90)


def r_carpet(t, u):
    Z = 1.35
    walk = sm(u / 2.8)
    k = A(C.koshchei, lerp(340.0, 560.0, walk), FL_Y, WY * 3 * Z, t=t, expr='suspicious' if False else ('normal' if not speaking('koshchei', t) else 'sly'),
          mouth_=mouth('koshchei', t), look=(0.9, 0.3), shiver=0.6, walk=t * 7, hand_n=(12.0, 40.0), hand_f=(-6.0, 40.0))
    def f(big, v):
        carpet_wrap(big, v, k)
        for i, x in enumerate((420.0, 600.0, 700.0)):
            ox, oy = v.opt(x, 330.0)
            K.steam(big, ox, oy, t + i * 0.5, 0.7, 0.9)
    return K.shot(YARD, K.light_yard, lerp(420.0, 560.0, walk), 430.0, Z, acts=[k], fx_=f, sy=330)


# ================================================================== 5: TWIST — the hut sits on the pipe like a brooding hen
def hut_acts(t, Z, cluck=0.0, sit=1.0, egg=0.0, yaga_m=0.0):
    x, y, s = HUT
    hut = A(C.izba, x, y, s * 3 * Z, t=t, sit=sit, cluck=cluck, egg=egg, sign=False)
    yg = A(C.yaga, x + 0.5 * s, y + (4.6 - 22.0 * (1 - sit)) * s, s * 0.62 * 3 * Z, t=t, expr='content' if yaga_m < 0.05 else 'sly',
           mouth_=yaga_m, look=(0.8, -0.2), prop_f=None, post=lambda sp: sp.clip_below(30.0))
    return [hut, yg]


def hut_fx(t, acts):
    def f(big, v):
        hut = acts[0]
        cx, cy = aout(hut, v, 'chimney')
        K.steam(big, cx, cy, t, 0.9, 1.1)
        for i, x in enumerate((560.0, 1000.0)):
            ox, oy = v.opt(x, 330.0)
            K.steam(big, ox, oy, t + i * 0.7, 0.8, 0.8)
        D.blit(big, v, SIGN_PRIV, HUT[0] - 66.0, HUT[1] - 58.0)
    return f


from props import rusigns as _R
SIGN_PRIV = _R.plate(50, 26, ['ЧАСТНАЯ', 'ТЕРРИТОРИЯ'], bg=(244, 240, 226), fg=(190, 30, 34), border=(190, 30, 34), bw=1.0)


def r_hut(t, u):
    pull = sm(u / 0.9)
    Z = lerp(1.6, 1.05, pull)
    acts = hut_acts(t, Z, yaga_m=mouth('yaga', t), cluck=0.3)
    k = A(C.koshchei, 600.0, FL_Y, WY * 3 * Z, t=t, expr='shock', mouth_=0.3, look=(0.9, 0.2), shiver=0.6, hand_n=(12.0, 40.0), hand_f=(-6.0, 40.0))
    def f(big, v):
        hut_fx(t, acts)(big, v)
        carpet_wrap(big, v, k)
    return K.shot(YARD, K.light_yard, lerp(760.0, 680.0, pull), lerp(330.0, 400.0, pull), Z, acts=acts + [k], fx_=f, sy=330)


# ================================================================== 6: COMMON — «Это ж общее тепло!» — «Теперь — насиженное.»
def r_common(t, u):
    Z = 1.15
    acts = hut_acts(t, Z, yaga_m=mouth('yaga', t))
    k = A(C.koshchei, 575.0, FL_Y, WY * 3 * Z, t=t, expr='shout' if speaking('koshchei', t) else 'sad', mouth_=mouth('koshchei', t),
          look=(0.9, 0.3), shiver=0.6, hand_n=(22.0, 56.0) if speaking('koshchei', t) else (12.0, 40.0), hand_f=(-6.0, 40.0))
    def f(big, v):
        hut_fx(t, acts)(big, v)
        carpet_wrap(big, v, k)
    return K.shot(YARD, K.light_yard, 660.0, 380.0, Z, acts=acts + [k], fx_=f, sy=330)


# ================================================================== 7: EGG — the hut clucks, lays a hot egg, sits back down
def r_egg(t, u):
    Z = 1.15
    up = sm(u / 0.3) * (1 - sm((u - 1.3) / 0.3))
    egg = sm((u - 0.6) / 0.6) if u < 1.4 else 0.0
    acts = hut_acts(t, Z, cluck=1.0 if u < 1.0 else 0.0, sit=1.0 - 0.35 * up, egg=egg)
    k = A(C.koshchei, 575.0 + 30 * egg, FL_Y, WY * 3 * Z, t=t, expr='grin' if egg > 0.3 and u < 1.35 else 'sad', look=(0.9, 0.6),
          shiver=0.6, hand_n=(24.0, 36.0) if egg > 0.3 else (12.0, 40.0), hand_f=(-6.0, 40.0))
    def f(big, v):
        hut_fx(t, acts)(big, v)
        carpet_wrap(big, v, k)
    return K.shot(YARD, K.light_yard, 660.0, 380.0, Z, acts=acts + [k], fx_=f, sy=330)


# ================================================================== 8: Кузьмич warms his hands on the meter: «Жуть.»
def r_zhut(t, u):
    def pre(big, v):
        x0, y0 = v.opt(430.0, 150.0); x1, y1 = v.opt(512.0, 262.0)
        big[int(y0):int(y1), int(x0):int(x1)] = (24, 22, 22)
    big, a = K.cu(C.domovoy, t, STAIRS, 470.0, 190.0, 4.4, 30.0, head=(560, 1010), light=K.light_stairs, pre_fx=pre,
                  expr='zhut', mouth_=mouth('kuzmich', t, 2.0), look=(0.0, -0.1), glow=(int(t * 3) % 2) * 1.0)
    frosty(big, 0.5)
    return big


def r_loop(t, u):
    return r_hook(t, u, loop=True)


R_ = [r_hook, r_galina, r_stuck, r_proud, r_carpet, r_hut, r_common, r_egg, r_zhut, r_loop]
assert len(R_) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 4, ['БАТАРЕИ', 'ЛЕДЯНЫЕ?!'], hook_t=(0.10, 2.70), hook_y=230,
              stickers=[(K.st('СЕЗОН ОТКРЫТ', fg=(255, 220, 110)), 5.0, 7.3, 540, 520),
                        (K.st('ДЗЫНЬ!', fg=(200, 236, 255), size=84), 7.5, 8.4, 540, 1180),
                        (K.st('НАСЕДКА', fg=(255, 90, 80), size=84), 18.0, 19.6, 540, 520)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1640, 1: 1560, 2: 1640, 3: 1640, 4: 1640, 5: 1640, 6: 1640, 7: 1640, 8: 1520, 9: 1640})


def render(t):
    i = max(0, min(len(R_) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R_[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
