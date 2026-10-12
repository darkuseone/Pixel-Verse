"""S01E05 «ШТРАФ ЗА КОСТЁР?!» (12.10.2026, v2 format; ~30.2 s, twist at 16.4 s / 54 %, type «охотник просит помощи»).
SELFIE by his campfire: a fine slaps onto his forehead — «Штраф за костёр?!» The forest ranger Людмила Петровна on her «ЛЕСХОЗ»
snowmobile with a drone: «И за дым. И за запах. Подписывайте!» SELFIE: «Лайфхак: маскировка «ёлочка». Ни дрон, ни егерь — не увидят!»
— he turns into a fir tree with a blinking garland. WIDE (tripod): the drone searches over the clearing, «Ёлка. Гирлянда. Невидимка.»
The drone bumps the «НЕ БУДИТЬ!» sign over the den. TWIST: the bear wakes up roaring and chases the ranger; she runs to the tree —
«Ёлочка! Спрячь меня!» — and hides in his branches. The bear sniffs the tree and walks off. «Он ушёл?» Прохор pulls out a receipt
book: «Укрытие. По тарифу. Плюс пени.» — and slaps the fine on HER forehead (loop to the hook). Button: the bear chews the drone —
«Учится.»
  python3 ep05.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props import taigaranger as RG
from props import taigakit as K
from props.taigakit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

COL = dict(K.COL, ranger=(150, 230, 120))
EPI = Episode('ep05', VOICE, DUR, FPS, colors=COL, slug=SLUG, endcard=dict(style='taiga', lang='ru'))
TAIGA = K.world('taiga2')
W = 2.4                      # taiga clearing: world px per sprite px
GROUND = 640.0
TREE_X = 520.0               # Прохор-«ёлочка»
FIRE = (610.0, 650.0)        # the campfire
SIGN = (940.0, 466.0)        # «НЕ БУДИТЬ!» over the den
DEN = (812.0, 560.0)         # the den mouth (floor)
SLED = (700.0, 652.0)        # the snowmobile


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def campfire(big, v, t, k=1.0):
    ox, oy = v.opt(*FIRE)
    s = v.Z * 3 / 3.0
    for i, (dx, ang) in enumerate(((-40, 0.25), (40, -0.25), (0, 0.0))):
        L = 90 * s; th = 18 * s
        x0, y0 = ox + dx * s - math.cos(ang) * L / 2, oy - 6 * s
        for q in range(int(L)):
            x = int(x0 + q * math.cos(ang)); y = int(y0 + q * math.sin(ang))
            if 0 <= x < OUT_W and 0 <= y - int(th) and y < OUT_H:
                big[y - int(th / 2):y + int(th / 2), x:x + 2] = (92, 58, 36) if q % 14 > 2 else (60, 38, 24)
    K.fire(big, int(ox), int(oy - 8 * s), t, w=int(70 * s), h=int(120 * s), k=k)


def tree(t, x, Z, s=1.0, **kw):
    kw.setdefault('expr', 'sly')
    kw.setdefault('garland', t)
    return A(C.prokhor, x, GROUND, W * s * 3 * Z, t=t, tree=True, **kw)


def ranger(t, x, Z, flip=False, y=GROUND, s=1.0, **kw):
    kw.setdefault('mouth_', mouth('ranger', t))
    return A(RG.ranger, x, y, W * s * 3 * Z, t=t, flip=flip, **kw)


def slip_on(big, v, act, t, t0, anchor='head', dx=1.0, dy=7.0, s=1.0, from_dx=12.0):
    """a fine slip flying in at t0 and sticking to an actor's forehead"""
    if t < t0: return
    p = sm((t - t0) / 0.14)
    hx, hy = aout(act, v, anchor)
    sc = act.scale(v)
    ox = hx + (-1 if act.flip else 1) * (dx + from_dx * (1 - p)) * sc
    oy = hy - dy * sc
    wx, wy = wpt(v, ox, oy)
    A(RG.fine_slip, wx, wy, sc * 0.85 * s, t=t, rot=-10 + 30 * (1 - p))(big, v, None)


# ================================================================== 0: SELFIE — the fine slaps onto his forehead
def r_slap(t, u):
    def f(big, v, a):
        slip_on(big, v, a, t, 0.0, dx=2.0, dy=9.0, s=0.8, from_dx=22.0)
        K.breath(big, 760, 1150, t, 0.8, scale=1.6, period=1.2)
    big, a = K.cu(C.prokhor, t, TAIGA, 640.0, 470.0, 1.25, 24.0, head=(480, 1240), light=K.light_taiga2, blur=2, extra_fx=f,
                  expr='shout', mouth_=max(0.5, mouth('prokhor', t)), look=(0.3, 0.2), hand_n=(20.0, 30.0))
    if u < 0.25: K.CK.shake(big, t, 14, 33)
    return K.shift(big, *K.handheld(t, 1.0))


# ================================================================== 1: the ranger on the snowmobile + her drone
def r_ranger(t, u):
    Z = 1.75
    sm_ = A(RG.snowmobile, SLED[0], SLED[1], W * 3 * Z, t=t)
    r = ranger(t, SLED[0] - 10.0 * W, Z, y=SLED[1] - 6.0 * W, legs=False, expr='angry' if speaking('ranger', t) else 'glare',
               look=(0.7, 0.0), hand_n=(17.0, 46.0 + 2 * math.sin(t * 6)), prop_n=RG.fine_book)
    dr = A(RG.drone, SLED[0] + 46.0, SLED[1] - 150.0 + 6 * math.sin(t * 3.0), W * 1.1 * 3 * Z, t=t)
    return K.shot(TAIGA, K.light_taiga2, SLED[0] + 10.0, 540.0, Z, acts=[r, sm_, dr], sy=330)


# ================================================================== 2: SELFIE — «маскировка «ёлочка»»
def r_hack(t, u):
    on = t > 7.2
    m = mouth('prokhor', t)
    def f(big, v, a):
        if 7.05 < t < 7.6:                                                                     # needles flying as he turns into a tree
            r = np.random.default_rng(int(t * 30))
            for i in range(40):
                px, py = int(540 + (r.random() - 0.5) * 900), int(1100 + (r.random() - 0.5) * 900)
                if 0 <= px < OUT_W - 14 and 0 <= py < OUT_H - 14: big[py:py + 14, px:px + 14] = (60, 120, 70)
    big, a = K.cu(C.prokhor, t, TAIGA, 830.0, 470.0, 1.25, 19.0 if on else 21.0, head=(520, 1120), light=K.light_taiga2, blur=2,
                  extra_fx=f, expr='sly' if t < 9.0 else 'grin', mouth_=m, look=(0.2, 0.1), hand_n=(22.0, 34.0) if not on else None,
                  tree=on, garland=t if t > 8.15 else None)
    big = K.shift(big, *K.handheld(t, 1.0))
    K.blog_frame(big, t)
    return big


# ================================================================== 3: WIDE (tripod) — the drone searches; «Ёлка. Гирлянда. Невидимка.»
def r_wide(t, u):
    Z = 1.3
    k = u / 4.0
    dx = lerp(450.0, 720.0, k); dy = 430.0 + 30 * math.sin(t * 2.0)
    dr = A(RG.drone, dx, dy, W * 1.2 * 3 * Z, t=t, tilt=0.8)
    a = tree(t, TREE_X, Z, expr='smug' if speaking('prokhor', t) else 'nervous', mouth_=mouth('prokhor', t, 1.2),
             look=(lerp(-0.8, 0.8, k), 0.6))
    tp = A(C.tripod, 640.0, GROUND + 22.0, W * 1.05 * 3 * Z, t=t, flip=True)
    def f(big, v): campfire(big, v, t, 0.5)
    return K.shot(TAIGA, K.light_taiga2, 552.0, 470.0, Z, acts=[tp, a, dr], fx_=f, sy=330)


# ================================================================== 4: the drone bumps the «НЕ БУДИТЬ!» sign
def r_drone(t, u):
    Z = 2.2
    hit_t = 15.85
    k = min(1.0, u / (hit_t - CUTS[4]))
    dx = lerp(800.0, SIGN[0] - 4.0, k); dy = lerp(420.0, SIGN[1] - 2.0, k)
    if t > hit_t: dx -= 20 * sm((t - hit_t) / 0.3); dy -= 10 * sm((t - hit_t) / 0.3)
    dr = A(RG.drone, dx, dy, W * 1.2 * 3 * Z, t=t, tilt=1.5 if t > hit_t else 0.4)
    big = K.shot(TAIGA, K.light_taiga2, 916.0, 470.0, Z, acts=[dr], sy=330)
    if t > hit_t:
        K.CK.shake(big, t, 12 * (1 - min(1.0, (t - hit_t) / 0.5)), 40)
        ox, oy = view_at(TAIGA, 916.0, 470.0, Z, 180, 330).opt(SIGN[0], SIGN[1] - 30)
        K.snow_burst(big, ox, oy, t, hit_t, n=50)
    return big


# ================================================================== 5: TWIST — the bear wakes up roaring
def r_bear(t, u):
    def f(big, v, a):
        mx, my = aout(a, v, 'mouth')
        K.breath(big, mx + 80, my, t, 1.4, scale=3.0, period=0.6)
    big, a = K.cu(C.potapych, t, TAIGA, DEN[0], 480.0, 1.6, 15.0 + 2.0 * sm(u / 0.4), head=(500, 900), light=K.light_taiga2, blur=3,
                  extra_fx=f, expr='angry', mouth_=1.0 if u < 1.2 else 0.5, look=(0.6, -0.1), bubble=0.0, snore=False,
                  hand_n=(36.0, 56.0))
    if u < 0.9: K.CK.shake(big, t, 18 * (1 - u), 30)
    return big


# ================================================================== 6: the ranger runs to the tree, the bear behind her
def r_run(t, u):
    Z = 0.95
    hide = 20.45
    k = min(1.0, u / (hide - CUTS[6]))
    rx = lerp(800.0, TREE_X - 6.0, k)
    a = tree(t, TREE_X, Z, expr='shock', mouth_=0.3, look=(0.9, 0.0))
    acts = [a]
    if t < hide:
        acts.append(ranger(t, rx, Z, flip=True, expr='panic', look=(-0.8, 0.1), walk=t * 14.0, lean=-0.4,
                           hand_n=(20.0, 60.0), hand_f=(-14.0, 60.0)))
    bx = lerp(870.0, 715.0, sm(u / 2.6))
    acts.append(A(C.potapych, bx, GROUND + 4.0, W * 0.8 * 3 * Z, t=t, flip=True, expr='angry', mouth_=0.6 + 0.3 * math.sin(t * 8),
                  look=(0.8, 0.0), bubble=0.0, snore=False, hand_n=(38.0, 50.0)))
    shake = 1.0 - min(1.0, (t - hide) / 0.6) if t > hide else 0.0
    big = K.shot(TAIGA, K.light_taiga2, 640.0, 470.0, Z, acts=acts, sy=330)
    v = view_at(TAIGA, 640.0, 470.0, Z, 180, 330)
    ox, oy = v.opt(bx - 40, GROUND)
    K.snow_burst(big, ox, oy, t, 18.2 + (int((t - 18.2) / 0.5) * 0.5), n=24, seed=int(t * 2))
    if shake: K.CK.shake(big, t, 10 * shake, 40)
    return big


# ================================================================== 7: the bear sniffs the tree; «Он ушёл?»
def r_sniff(t, u):
    Z = 1.5
    leave = sm((t - 22.3) / 0.9)
    bx = lerp(TREE_X + 70.0, TREE_X + 260.0, leave)
    b = A(C.potapych, bx, GROUND + 4.0, W * 0.8 * 3 * Z, t=t, flip=leave < 0.3, expr='deadpan', look=(-0.9, 0.1), bubble=0.0, snore=False,
          hand_n=(30.0, 40.0), slump=0.3 * math.sin(t * 7.0) * (1 - leave))
    peek = sm((t - 22.7) / 0.3)
    r = ranger(t, TREE_X - 30.0 - 14.0 * peek, Z, expr='panic' if t < 22.8 else 'nervous', look=(-0.6, 0.3), mouth_=mouth('ranger', t),
               hand_n=(14.0, 50.0))
    a = tree(t, TREE_X, Z, expr='panic' if leave < 0.5 else 'nervous', mouth_=0.15, look=(0.9, -0.1), sweat=1.0)
    return K.shot(TAIGA, K.light_taiga2, TREE_X + 20.0, 470.0, Z, acts=[r, a, b], sy=330)


# ================================================================== 8: «Укрытие. По тарифу. Плюс пени.» — the fine on HER forehead
def r_fine(t, u):
    Z = 1.6
    tear = t > 26.55
    r = ranger(t, TREE_X + 120.0, Z, flip=True, expr='shock' if t > 27.1 else 'stunned', look=(0.7, 0.0), mouth_=0.2, hand_n=(16.0, 30.0))
    a = tree(t, TREE_X, Z, expr='sly' if not speaking('prokhor', t) else 'smug', mouth_=mouth('prokhor', t), look=(0.8, 0.0),
             hand_n=(22.0, 34.0) if not tear else (26.0, 46.0), prop_n=lambda sp, h: RG.fine_book(sp, h, open_=1.0 if not tear else 0.4))
    def f(big, v):
        slip_on(big, v, r, t, 27.1, dx=1.0, dy=7.0, s=0.7, from_dx=20.0)
    return K.shot(TAIGA, K.light_taiga2, TREE_X + 48.0, 470.0, Z, acts=[r, a], fx_=f, sy=330)


# ================================================================== 9: BUTTON — the bear chews the drone: «Учится.»
def r_button(t, u):
    chew = 0.5 + 0.5 * math.sin(t * 9.0)
    big, a = K.cu(C.potapych, t, TAIGA, 760.0, 470.0, 1.4, 15.0, head=(440, 860), light=K.light_taiga2, blur=3,
                  expr='boss', mouth_=max(mouth('bear', t, 1.5), 0.15 + 0.25 * chew), look=(0.3, -0.4), bubble=0.0, snore=False,
                  hand_n=(30.0, 50.0), prop_n=lambda sp, h: RG.drone(sp, t, lights=False, tilt=2.0, broken=1.0, at=(h[0] + 2.0, h[1] + 2.0)))
    return big


R = [r_slap, r_ranger, r_hack, r_wide, r_drone, r_bear, r_run, r_sniff, r_fine, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 5, ['ШТРАФ ЗА', 'КОСТЁР?!'], hook_t=(0.10, 1.85), hook_y=250,
              stickers=[(K.st('ЛАЙФХАК №5', fg=(255, 214, 80)), 5.2, 7.2, 540, 520),
                        (K.st('РАЗБУДИЛИ!', fg=(255, 90, 80), size=80), 16.5, 17.9, 540, 300),
                        (K.st('ПЛЮС ПЕНИ', fg=(255, 236, 120), size=80), 27.2, 28.0, 540, 360)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1720, 1: 1640, 2: 1720, 3: 1640, 4: 1640, 5: 1640, 6: 1640, 7: 1640, 8: 1640, 9: 1640})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
