"""S01E01 «ПЕНСИЮ НЕ ДАЮТ?!» (19.10.2026; ~32.6 s, twist at 16.4 s / 50 %).
HOOK: Кощей pressed to the glass of window 3 in the Соцфонд, eyes green, the foil crown shaking: «999 лет — и не положено?!»
Галина Аркадьевна behind the glass, chewing a biscuit: «С тысячи лет. Год остался. Потерпите.» WIDE (pull-back, paper bats over the
windows): «Я — Кощей Бессмертный!» — «Вот и дождётесь.» SCARE: green fire, thunder, the tubes die — she sets a plate «ПУГАТЬ — ОКНО 7»
next to «ОКНО 7 НЕ РАБОТАЕТ». TWIST (bureaucratic recursion, the goal moves): VHS rewind, «ЧЕРЕЗ ГОД», a cake with a thousand candles —
«Мне — тысяча!» — «Повысили. С двух.» Then «Стаж — тридцать царств!» — «Царства — неофициально.», «Я ж — бессмертный.» —
«Вот. Вам — не к спеху.» Кузьмич in the electrical box behind her: «Жуть.» LOOP: he presses to the glass again (= first frame).
  python3 ep01.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import fx
import overlays as O
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import koshcast as C
from props import koshkit as K
from props import decals as D
from props import rusigns as R
from props.koshkit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='kosh', lang='ru'))
OFF = K.world('office')
DESK = K.world('desk')
WIN = (652.0, 290.0)            # window 3 glass centre (office world px)
FLOOR = 540.0                   # where Кощей stands (feet), office
WP = 3.9                        # office: world px per sprite px for Кощей at the window
CAL = K.calendar(6)
SIGN7 = R.plate(84, 34, ['ПУГАТЬ —', 'ОКНО 7'], bg=(244, 240, 226), fg=(30, 28, 30), border=(34, 70, 130), bw=1.2, colors=[(30, 28, 30), (190, 30, 34)])


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def k_expr(t, base='normal'):
    return 'shout' if speaking('koshchei', t) else base


def desk_dress(big, v):
    D.blit(big, v, CAL, 276.0, 46.0)                                    # the tear-off calendar on the clerk's wall


def glass(big, x0, y0, x1, y1, k=1.0):
    """the counter glass between them: a cool tint + two diagonal glare streaks (output px box)"""
    x0, y0, x1, y1 = max(0, int(x0)), max(0, int(y0)), min(OUT_W, int(x1)), min(OUT_H, int(y1))
    reg = big[y0:y1, x0:x1]
    reg[:] = (reg * (1 - 0.10 * k) + np.array((170, 210, 220)) * 0.10 * k).astype(np.uint8)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    for c in (0.22, 0.30):
        m = np.abs((xx - x0) + (yy - y0) * 0.6 - (x1 - x0) * c * 3) < 26
        reg[m] = np.clip(reg[m] * 0.75 + 255 * 0.25 * k, 0, 255).astype(np.uint8)


def galina_window(t, Z, scale_k=1.0, **kw):
    """Галина behind window 3 (office world): only the bust above the counter"""
    gm = mouth('galina', t)
    return A(C.galina, 700.0, 470.0, 3.0 * 3 * Z * scale_k, flip=True, t=t, expr='deadpan' if gm < 0.05 else 'normal', mouth_=gm,
             biscuit=True, chew=gm < 0.05, look=(0.6, -0.1), post=lambda sp: sp.clip_below(27.0), **kw)


# ================================================================== 0: HOOK — pressed to the glass
def r_hook(t, u, loop=False):
    m = mouth('koshchei', t) if not loop else 0.0
    sh = 6 * math.sin(t * 40) * (1.0 if t < 3.7 else 0.0)
    def f(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.green_fire(big, hx - 70, hy - 20, t, r=40, k=0.5, seed=1)
        K.green_fire(big, hx + 110, hy - 10, t, r=40, k=0.5, seed=2)
        glass(big, 0, 0, OUT_W, OUT_H, 0.8)
    big, a = K.cu(C.koshchei, t, OFF, 652.0, 330.0, 1.35, 23.0, head=(500 + sh, 900), light=K.light_office, blur=3, extra_fx=f,
                  expr='scream' if not loop else 'shout', mouth_=max(0.45, m) if not loop else 0.3, look=(0.5, 0.1), fire=0.8,
                  hand_n=(9.0, 30.0), hand_f=(-7.0, 30.0))
    big = K.shift(big, *K.handheld(t, 0.6))
    if t < 0.35: K.CK.shake(big, t, 14, 33)
    return big


# ================================================================== 1: Галина behind the glass, chewing
def r_galina(t, u):
    gm = mouth('galina', t)
    big, a = K.cu(C.galina, t, DESK, 600.0, 330.0, 1.05, 24.0, head=(700, 900), light=K.light_office, blur=2, pre_fx=desk_dress, flip=True,
                  expr='deadpan' if gm < 0.05 else 'normal', mouth_=gm, biscuit=True, chew=gm < 0.05, look=(0.5, -0.3),
                  hand_n=(10.0, 16.0), prop_n=C.stamp, post=lambda sp: sp.clip_below(14.0))
    glass(big, 0, 0, OUT_W, OUT_H, 0.6)
    return big


# ================================================================== 2: WIDE — pull back: Кощей in a vest and slippers at window 3
def r_wide(t, u):
    Z = lerp(1.25, 0.98, sm(u / 1.4))
    km = mouth('koshchei', t)
    k = A(C.koshchei, 600.0, FLOOR, WP * 3 * Z, t=t, expr=k_expr(t, 'proud' if t < 10.2 else 'sad'), mouth_=km, look=(0.6, 0.1),
          hand_n=(21.0, 50.0) if speaking('koshchei', t) else (10.0, 30.0), prop_f=C.string_bag, fire=0.6 if speaking('koshchei', t) else 0.0)
    g = galina_window(t, Z)
    return K.shot(OFF, K.light_office, 620.0, 360.0, Z, acts=[g, k], sy=330)


# ================================================================== 3: SCARE — green fire, thunder; «ПУГАТЬ — ОКНО 7»
def r_scare(t, u):
    Z = 1.35
    fire = sm((t - 11.8) / 0.4) * (1 - sm((t - 15.0) / 0.4))
    k = A(C.koshchei, 600.0, FLOOR, WP * 3 * Z, t=t, expr='sinister' if not speaking('koshchei', t) else 'scream', mouth_=mouth('koshchei', t),
          look=(0.6, 0.2), hand_n=(22.0, 52.0 + 4 * fire), hand_f=(-18.0, 50.0 + 4 * fire), fire=fire)
    g = galina_window(t, Z)
    thunder = K.hit(t, 12.4, 0.5)
    def f(big, v):
        if t >= 14.85:
            pop = min(1.0, (t - 14.85) / 0.12)
            D.blit(big, v, SIGN7, 610.0, 352.0 - 34.0 * pop * (1 - pop) * 0.5)
        if fire > 0:
            ha = aout(k, v, 'hand_n'); hf = aout(k, v, 'hand_f')
            K.green_fire(big, ha[0], ha[1], t, r=90, k=fire, seed=3); K.green_fire(big, hf[0], hf[1], t, r=90, k=fire, seed=4)
        if thunder > 0: O.flash(big, 0.6 * thunder)
        if 12.4 < t < 13.4 and int(t * 18) % 2: big[:] = (big * 0.55).astype(np.uint8)
    big = K.shot(OFF, K.light_office, 640.0, 340.0, Z, acts=[g, k], fx_=f, sy=330)
    if thunder > 0: K.CK.shake(big, t, 12 * thunder, 30)
    return big


# ================================================================== 4: TWIST — VHS «ЧЕРЕЗ ГОД»: a cake with a thousand candles
def r_year(t, u):
    Z = 1.2
    km = mouth('koshchei', t)
    k = A(C.koshchei, 600.0, FLOOR, WP * 3 * Z, t=t, expr=k_expr(t, 'proud') if t < 18.7 else ('shock' if t < 19.6 else 'sad'),
          mouth_=km, look=(0.6, 0.1), hand_n=(14.0, 44.0), hand_f=(-4.0, 44.0), prop_n=lambda sp, h: C.cake(sp, (h[0] - 6.0, h[1] - 3.0), n=70, t=t))
    g = galina_window(t, Z)
    def f(big, v):
        if t > 18.9:
            hx, hy = aout(k, v, 'head')
            for i in range(3): K.steam(big, hx - 100 + 60 * i, hy + 120, t + i, 0.6, 0.6)
    big = K.shot(OFF, K.light_office, 630.0, 330.0, Z, acts=[g, k], fx_=f, sy=330)
    if u < 0.5: K.vhs(big, t, 1 - u / 0.5)
    K.ticker_text(big, 'ЧЕРЕЗ ГОД', 520, 70, k=(sm(u / 0.15) * (1 - sm((u - 1.4) / 0.2))))
    return big


# ================================================================== 5: STAZH — he slaps a birch-bark «трудовая» on the counter
def scroll(sp, h):
    x, y = h
    m = sp.m_poly([(x - 2.0, y - 1.0), (x + 12.0, y - 0.4), (x + 12.4, y + 7.0), (x - 1.6, y + 6.6)])
    sp.paint(m, [(200, 186, 150), (236, 226, 196), (250, 244, 226)], None, olc=(90, 70, 50))
    sp.txt_box(['ТРУДОВАЯ', '30 ЦАРСТВ'], (x - 1.4, y - 0.2, x + 11.8, y + 6.2), (120, 40, 30), pad=0.2)
    for q in range(5): K.KX.thin(sp, (x - 1.0, y + 0.2 + q * 1.4), (x - 1.6, y + 0.6 + q * 1.4), (40, 30, 20), 0.2)


def r_stazh(t, u):
    Z = 1.6
    slap = sm((u - 0.3) / 0.12)
    k = A(C.koshchei, 590.0, FLOOR, WP * 3 * Z, t=t, expr=k_expr(t, 'proud'), mouth_=mouth('koshchei', t), look=(0.7, -0.2),
          hand_n=(18.0, lerp(54.0, 46.0, slap)), prop_n=scroll, hand_f=(-8.0, 30.0))
    g = galina_window(t, Z)
    big = K.shot(OFF, K.light_office, 640.0, 362.0, Z, acts=[g, k], sy=330)
    if 0.3 < u < 0.5: K.CK.shake(big, t, 8, 30)
    return big


# ================================================================== 6: FOLDER — Галина: «Царства — неофициально.»
def r_folder(t, u):
    gm = mouth('galina', t)
    big, a = K.cu(C.galina, t, DESK, 600.0, 330.0, 1.05, 22.0, head=(700, 880), light=K.light_office, blur=2, pre_fx=desk_dress, flip=True,
                  expr='deadpan' if gm < 0.05 else 'smug', mouth_=gm, look=(0.4, -0.6), hand_n=(10.0, 20.0 + 2 * math.sin(t * 6)),
                  post=lambda sp: sp.clip_below(14.0))
    glass(big, 0, 0, OUT_W, OUT_H, 0.5)
    return big


# ================================================================== 7: DEFLATE — wax on his crown, the cake smoking
def r_deflate(t, u):
    km = mouth('koshchei', t)
    def f(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.steam(big, hx + 160, hy + 520, t, 0.5, 0.8)
        for i in range(4):                                                   # wax drips on the crown
            x = hx - 180 + i * 70; y = hy - 330 + (i % 2) * 30
            big[int(y):int(y + 40 + 10 * i), int(x):int(x + 16)] = (250, 240, 200)
    big, a = K.cu(C.koshchei, t, OFF, 640.0, 330.0, 1.35, 21.0, head=(520, 960), light=K.light_office, blur=3, extra_fx=f,
                  expr='sad' if km > 0.05 or t < 28.4 else 'stunned', mouth_=km, look=(0.4, -0.2), hand_n=(12.0, 40.0),
                  prop_n=lambda sp, h: C.cake(sp, (h[0] - 6.0, h[1] - 3.0), n=70, lit=0.0))
    glass(big, 0, 0, OUT_W, OUT_H, 0.5)
    return big


# ================================================================== 8: Кузьмич in the electrical box behind her: «Жуть.»
def r_zhut(t, u):
    def pre(big, v):
        x0, y0 = v.opt(728.0, 112.0); x1, y1 = v.opt(800.0, 236.0)
        big[int(y0):int(y1), int(x0):int(x1)] = (24, 22, 22)
    def f(big, v, a):
        x0, y0 = v.opt(728.0, 112.0); x1, y1 = v.opt(800.0, 236.0)
        big[int(y0):int(y0) + 14, int(x0):int(x1)] = (120, 124, 130); big[int(y1) - 14:int(y1), int(x0):int(x1)] = (120, 124, 130)
    big, a = K.cu(C.domovoy, t, DESK, 764.0, 190.0, 3.4, 30.0, head=(560, 1010), light=K.light_office, pre_fx=pre, extra_fx=f,
                  expr='zhut', mouth_=mouth('kuzmich', t, 2.0), look=(0.0, -0.1), glow=(int(t * 3) % 2) * 1.0)
    return big


# ================================================================== 9: LOOP — he presses to the glass again (= first frame)
def r_loop(t, u):
    return r_hook(t, u, loop=True)


R_ = [r_hook, r_galina, r_wide, r_scare, r_year, r_stazh, r_folder, r_deflate, r_zhut, r_loop]
assert len(R_) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 1, ['ПЕНСИЮ', 'НЕ ДАЮТ?!'], hook_t=(0.10, 2.70), hook_y=260,
              stickers=[(K.st('ОКНО 7', fg=(255, 220, 110)), 14.9, 16.3, 540, 560),
                        (K.st('С 2000?!', fg=(255, 90, 80), size=84), 19.25, 20.30, 540, 520),
                        (K.st('НЕОФИЦИАЛЬНО', fg=(120, 255, 150)), 25.1, 26.2, 540, 560)],
              flashes=[TWIST, 19.25], mosaics=[],
              cap_y={0: 1640, 1: 1560, 2: 1600, 3: 1640, 4: 1640, 5: 1640, 6: 1580, 7: 1640, 8: 1520, 9: 1640})


def render(t):
    i = max(0, min(len(R_) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R_[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
