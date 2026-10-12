"""S01E03 «МАЛИНА ПО 900?!» (12.10.2026, v2 format; ~29.8 s, twist at 15.55 s / 52 %, type «сеть видит всё»).
SELFIE at the forest edge: the shop app shows «МАЛИНА 900 ₽/кг» — «Девятьсот за малину?!» — «Лайфхак: тайга — бесплатный магазин.
Иду за покупками!» WIDE (tripod): he throws on a cape of fir branches — «Маскхалат. Чтоб медведь не видел.» TRIPOD CAM: in the
raspberry bushes, stuffing his mouth — «Малина. Гриб. Шишка. Всё — даром! Городские, учитесь!» TWIST: the birdhouse on the birch is a
security camera — it turns to him, the red light blinks. A squirrel guard in a vest drops from the tree with a tablet (the replay):
«Мужчина! Пакетик откройте. Малина — по весу.» — «Я ж в тайге!» — «Тайга — по карте.» Button: the bear at a stump «КАССА» with a
barcode scanner: «Карта «Берлога-Плюс» есть? Нет? Девятьсот.» — and scans the berry in Прохор's mouth: beep.
  python3 ep03.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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

COL = dict(K.COL, squirrel=(255, 200, 90))
EPI = Episode('ep03', VOICE, DUR, FPS, colors=COL, slug=SLUG, endcard=dict(style='taiga', lang='ru'))
GLADE = K.world('glade')
WG = 4.3                     # glade: world px per sprite px (raspberry bushes up to his chest)
GROUND = 660.0
BIRDHOUSE = (189.0, 309.0)   # the hole of the birdhouse on the birch
STUMP = (983.0, 478.0, 1199.0, 640.0)


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def berries(sp, h):
    for q in range(5):
        sp.ell(h[0] + 1.6 + (q % 3) * 1.2, h[1] + 1.6 + (q // 3) * 1.2, 0.9, 0.9, C.tones((210, 30, 50)), gloss=0.8, snow=False)


def eat_hand(t, base=(18.0, 26.0)):
    """the near mitten shuttles between the bush and his mouth"""
    k = 0.5 + 0.5 * math.sin(t * 7.0)
    return (lerp(base[0], 12.0, k), lerp(base[1], 40.0, k))


def cam_act(t, Z, turn=0.0):
    return A(F.birdhouse_cam, BIRDHOUSE[0], BIRDHOUSE[1], WG * 0.9 * 3 * Z, t=t, turn=turn)


def occlude_stump(big, v):
    xs, ys = v.grid()
    x0, y0, x1, y1 = STUMP
    m = ((ys[:, None] >= y0) & (ys[:, None] < y1)) & ((xs[None, :] >= x0) & (xs[None, :] < x1))
    big[m] = v.bg()[m]


# ================================================================== 0: SELFIE — the price
def r_selfie(t, u):
    m = mouth('prokhor', t)
    hook = t < 2.0
    pan = sm((t - 2.4) / 3.5)
    def f(big, v, a):
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 30, hy + 10, t, 0.6 + 0.6 * m, scale=1.6, period=1.3)
    big, a = K.cu(C.prokhor, t, GLADE, 640.0 - 280.0 * pan, 380.0, 1.25, 24.0 if hook else 21.0, head=(480, 1260) if hook else (430, 1150),
                  light=K.light_taiga2, blur=2, extra_fx=f, expr='shout' if hook else ('grin' if t < 4.6 else 'sly'),
                  mouth_=max(0.4 if hook else 0.0, m), look=(0.3, 0.2) if hook else (-0.6, 0.0), hand_n=(22.0, 34.0) if not hook else (20.0, 30.0))
    big = K.shift(big, *K.handheld(t, 1.2))
    if t < 0.3: K.CK.shake(big, t, 12, 33)
    if t > 2.0: K.blog_frame(big, t)
    K.phone_card(big, t, 0.15, 2.05, ['ПЯТНЮШКА', 'Малина свежая, 1 кг', 'Цена: 900 ₽'], icon='П', icon_col=(40, 150, 70), y=690,
                 colors=[(30, 30, 40), (90, 90, 100), (200, 30, 40)])
    return big


# ================================================================== 1: WIDE — the fir-branch camo cape
def r_camo(t, u):
    Z = 1.05
    on = t > 6.75
    x = lerp(470.0, 420.0, sm((u - 1.6) / 1.2))
    a = A(C.prokhor, x, GROUND, WG * 3 * Z, t=t, expr='sly', mouth_=mouth('prokhor', t, 1.2), look=(-0.4, 0.2), camo=on,
          hand_n=(15.0, 49.0) if speaking('prokhor', t) and t > 7.6 else (20.0, 30.0), hand_f=(-14.0, 28.0), lean=0.3 if on else 0.0)
    tp = A(C.tripod, 690.0, 712.0, WG * 1.05 * 3 * Z, t=t)
    def f(big, v):
        if 6.5 < t < 7.0:                                                                 # needles flying as he throws it on
            r = np.random.default_rng(int(t * 30))
            ox, oy = aout(a, v, 'chest') if 'chest' in a.last.anchors else v.opt(x, GROUND - 120)
            for i in range(20):
                px, py = int(ox + (r.random() - 0.5) * 360), int(oy + (r.random() - 0.5) * 360)
                if 0 <= px < OUT_W - 10 and 0 <= py < OUT_H - 10: big[py:py + 10, px:px + 10] = (60, 120, 70)
    return K.shot(GLADE, K.light_taiga2, 470.0, 470.0, Z, acts=[a, tp], fx_=f, sy=330)


# ================================================================== 2: TRIPOD CAM — eating the free taiga (the birdhouse watches)
def r_eat(t, u):
    Z = 1.15
    a = A(C.prokhor, 380.0, GROUND + 10.0, WG * 3 * Z, t=t, expr='grin' if speaking('prokhor', t) else 'bliss', mouth_=mouth('prokhor', t),
          look=(0.6, 0.0), camo=True, hand_n=eat_hand(t), prop_n=berries, hand_f=(-12.0, 26.0))
    big = K.shot(GLADE, K.light_taiga2, 310.0, 470.0, Z, acts=[cam_act(t, Z), a], sy=330)
    K.blog_frame(big, t)
    return big


# ================================================================== 3: TWIST — the birdhouse is a camera
def r_cam(t, u):
    Z = 4.2
    turn = sm(u / 0.5)
    big = K.shot(GLADE, K.light_taiga2, BIRDHOUSE[0] + 8.0, BIRDHOUSE[1] + 4.0, Z, acts=[cam_act(t, Z, turn=turn)], sy=320)
    if u < 0.25: K.CK.shake(big, t, 10, 40)
    return big


# ================================================================== 4: the squirrel guard drops with the tablet
def r_guard(t, u):
    Z = 1.15
    k = min(1.0, u / 0.45)
    gy = lerp(360.0, GROUND + 8.0, k * k)
    g = A(F.critter, 250.0, gy, WG * 1.0 * 3 * Z, t=t, kind='guard', cap='guard', vest='ОХРАНА', expr='angry' if k >= 1 else 'shock',
          mouth_=mouth('squirrel', t), hand_n=(9.0, 18.0), prop_n=lambda sp, h: F.tablet(sp, h, t))
    a = A(C.prokhor, 400.0, GROUND + 10.0, WG * 3 * Z, t=t, flip=True, expr='shock', mouth_=0.25, look=(0.6, 0.0), camo=True,
          hand_n=(14.0, 38.0), prop_n=berries)
    big = K.shot(GLADE, K.light_taiga2, 330.0, 470.0, Z, acts=[cam_act(t, Z, 1.0), g, a], sy=330)
    if 0.42 < u < 0.6: K.CK.shake(big, t, 10, 36)
    return big


def r_protest(t, u):
    big, a = K.cu(C.prokhor, t, GLADE, 420.0, 420.0, 1.3, 22.0, head=(560, 960), light=K.light_taiga2, blur=3,
                  expr='shout', mouth_=mouth('prokhor', t), look=(-0.6, 0.0), camo=True, hand_n=(18.0, 52.0), hand_f=(-10.0, 48.0))
    return big


def r_seed(t, u):
    big, a = K.cu(F.critter, t, GLADE, 300.0, 420.0, 1.3, 30.0, head=(470, 930), light=K.light_taiga2, blur=3,
                  kind='guard', cap='guard', vest='ОХРАНА', expr='deadpan', mouth_=mouth('squirrel', t), look=(0.6, 0.0),
                  hand_n=(9.0, 18.0), prop_n=lambda sp, h: F.tablet(sp, h, t))
    if t > 22.9:                                                                         # a husk flies off
        ox, oy = aout(a, None, 'mouth') if False else (700, 900)
        p = min(1.0, (t - 22.9) / 0.4)
        big[int(oy - 200 * p + 400 * p * p):int(oy - 200 * p + 400 * p * p) + 16, int(ox + 300 * p):int(ox + 300 * p) + 24] = (40, 30, 26)
    return big


# ================================================================== 7: BUTTON — the bear's till on the stump; the scanner beeps his mouth
def r_till(t, u):
    Z = 1.15
    scan = t > 27.55
    b = A(C.potapych, 1100.0, 650.0, WG * 3 * Z, t=t, expr='boss', mouth_=mouth('bear', t, 1.5), look=(-0.6, -0.1),
          hand_n=(30.0, 44.0) if not scan else (34.0, 52.0), prop_n=lambda sp, h: F.scanner(sp, h, t, beam=1.0 if scan else 0.0), flip=True)
    till = A(F.stump_till, 1050.0, 482.0, WG * 1.2 * 3 * Z, t=t)
    a = A(C.prokhor, 840.0, GROUND + 6.0, WG * 3 * Z, t=t, expr='nervous' if not scan else 'shock', mouth_=0.15 if not scan else 0.5,
          look=(0.8, 0.0), camo=True, hand_n=(15.0, 26.0), prop_n=berries)
    def f(big, v):
        occlude_stump(big, v)
        till(big, v, K.light_taiga2(v))
    return K.shot(GLADE, K.light_taiga2, 960.0, 470.0, Z, acts=[b], fx_=lambda big, v: (f(big, v), a(big, v, K.light_taiga2(v))), sy=330)


R = [r_selfie, r_camo, r_eat, r_cam, r_guard, r_protest, r_seed, r_till]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 3, ['МАЛИНА', 'ПО 900?!'], hook_t=(0.10, 2.0), hook_y=250,
              stickers=[(K.st('ЛАЙФХАК №3', fg=(255, 214, 80)), 3.0, 5.4, 540, 520),
                        (K.st('ВАС СНИМАЮТ', fg=(255, 90, 80), size=72), 15.65, 16.9, 540, 420),
                        (K.st('ПИК!', fg=(255, 236, 120), size=96), 27.6, 28.8, 540, 420)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1720, 1: 1640, 2: 1640, 3: 1500, 4: 1640, 5: 1620, 6: 1600, 7: 1640})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
