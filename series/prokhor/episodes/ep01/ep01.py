"""S01E01 «9 000 ЗА ТЕПЛО?!» (pilot, 12.10.2026, 34.2 s, twist at 17.5 s / 51 %).
Прохор in his frozen izba screams at a heating bill, burns it («пять секунд тепла — бесплатно»), and shows the city folk lifehack №1:
a free radiator — the sleeping bear. «Без счётчика!» — while an old meter sits by the den. In the den: «Тариф — ноль», the meter spins,
«Городские — учитесь!». Twist: the bubble pops, one eye opens behind the glasses: «Отопление. Девять тысяч.» The den is an office
(УК «Берлога»): «Ты ж спишь!» — «Я на удалёнке.» — «А если не заплачу?» — «Отключу.» — he flies out into a drift and freezes solid:
«Го-городские... НЕ учитесь.» Button: the bear from the hole slaps the bill on the ice — «Плюс пени.» Loops into the bill of the hook.
  python3 ep01.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
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
IZBA, TAIGA, DEN = K.world('izba'), K.world('taiga'), K.world('den')
WI = 6.0              # izba: world px per sprite px (close interior)
WT = 2.0              # taiga clearing
WD = 3.6              # den
BEAR_XY = (700.0, 690.0)
DESK_XY = (880.0, 700.0)
HOLE = (651.0, 468.0, 51.0, 54.0)          # den entrance ellipse on the taiga background (cx, cy, rx, ry)
METER_XY = (720.0, 492.0)


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def bill_prop(big=True):
    def f(sp, h): C.bill(sp, h, big=big)
    return f


def bill_only(sp, t=0.0):
    C.bill(sp, (0.0, 0.0), big=True)
    sp.outline(K.INK, 1)


# ================================================================== IZBA
def r_hook(t, u):
    """0.0: close-up — frost in the beard, breath steam, the bill «ОТОПЛЕНИЕ 9 000 ₽» right by his face: «Девять тыщ за ТЕПЛО?!»"""
    m = mouth('prokhor', t)
    def f(big, v, a):
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 30, hy + 10, t, 0.9 + 0.4 * m, dirx=1.0, scale=1.8, period=1.1)
    big, a = K.cu(C.prokhor, t, IZBA, 600.0, 330.0, 1.35, 27.0, head=(390, 1010), light=K.light_izba, blur=3, extra_fx=f,
                  expr='shout', mouth_=max(0.5, m), look=(0.8, 0.0), frost=1.0, hand_n=(15.0, 41.0), prop_n=bill_prop())
    if u < 0.3: K.CK.shake(big, t, 10, 33)
    return big


def r_stove(t, u):
    """the bill goes into the cold stove door: a flare (5 seconds of warmth)"""
    Z = 3.0
    burn = sm((t - 2.75) / 0.12) * (1 - sm((t - 3.30) / 0.15))
    hold = t < 2.95
    hx, hy = 300.0 + 30 * (1 - sm(u / 0.5)), 452.0
    a = A(C.prokhor, hx, hy, WI * 3 * Z * 0.80, flip=True, pin='hand', t=t, expr='smug', hand_n=(17.0, 30.0),
          prop_n=bill_prop() if hold else None, frost=0.6)
    def f(big, v):
        ox, oy = v.opt(285, 470)
        if burn > 0:
            K.fire(big, ox, oy + 40, t, w=260, h=420 * burn, k=burn)
            fx.glow(big, ox, oy, 700, (255, 170, 80), 0.35 * burn)
    return K.shot(IZBA, K.light_izba, 290.0, 440.0, Z, acts=[a], fx_=f, sy=330)


def r_warm(t, u):
    """medium: he warms his mittens at the dying flame, smug: «Вот. Пять секунд тепла — бесплатно.»"""
    Z = 1.25
    k = max(0.0, 1 - (t - 3.45) / 1.0)
    a = A(C.prokhor, 455.0, 700.0, WI * 3 * Z, flip=True, t=t, expr='smug' if t < 4.4 else 'proud', mouth_=mouth('prokhor', t),
          look=(0.6, 0.0), hand_n=(15.0, 30.0), hand_f=(13.0, 33.0), frost=0.8)
    def f(big, v):
        ox, oy = v.opt(285, 470)
        if k > 0: K.fire(big, ox, oy + 30, t, w=160 * k + 30, h=180 * k + 20, k=max(0.15, k))
        else:
            for i in range(3):                                                         # a thin wisp of smoke: it is over
                ph = (t * 0.8 + i / 3) % 1.0
                K.puff(big, ox + 20 * math.sin(t * 3 + i), oy - 260 * ph, 30 + 40 * ph, 0.35 * (1 - ph), (150, 150, 160))
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx - 20, hy, t, 0.6, dirx=-1.0, scale=1.0)
    return K.shot(IZBA, K.light_izba, 380.0 - 20 * u, 410.0, Z, acts=[a], fx_=f, sy=320)


def r_blog(t, u):
    """the blog: phone-camera frame (REC), he presents to the city folk: «Городские! Лайфхак номер ОДИН!»"""
    Z = 1.05 + 0.08 * K.J(u, 1.5, 1.0)
    point = t > 6.3
    a = A(C.prokhor, 600.0, 712.0, WI * 3 * Z, t=t, expr='shout' if speaking('prokhor', t) else 'proud', mouth_=mouth('prokhor', t),
          look=(0.2, 0.1), hand_n=(18.0, 58.0) if point else (17.0, 36.0), frost=0.6)
    def f(big, v):
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 30, hy, t, 0.7, scale=1.1)
        K.blog_frame(big, t)
    return K.shot(IZBA, K.light_izba, 600.0, 430.0, Z, acts=[a], fx_=f, sy=300)


# ================================================================== TAIGA
def r_trek(t, u):
    """wide: low sun, he trudges through deep snow with a pillow towards the steaming snow mound (the den)"""
    Z = 1.0
    x = 300.0 + 150.0 * sm(u / 2.0)
    a = A(C.prokhor, x, 640.0, WT * 3 * Z, t=t, expr='proud', mouth_=mouth('prokhor', t), walk=t * 9.0, look=(1.0, 0.0),
          hand_n=(16.0, 30.0), prop_n=lambda sp, h: C.pillow(sp, h))
    def f(big, v):
        ox, oy = v.opt(648, 190)
        for i in range(3):
            ph = (t * 0.5 + i / 3) % 1.0
            K.puff(big, ox + 30 * math.sin(t + i), oy - 300 * ph, 26 + 50 * ph, 0.4 * (1 - ph), (236, 240, 250))
    return K.shot(TAIGA, K.light_taiga, 380.0 + 40 * u, 430.0, Z, acts=[a], fx_=f, sy=330)


def r_entrance(t, u):
    """closer at the den: «...Без СЧЁТЧИКА!» — and right there, half under the snow, an old meter (the clue) + «НЕ БУДИТЬ!»"""
    Z = 1.9 + 0.05 * u
    a = A(C.prokhor, 596.0, 572.0, WT * 3 * Z, t=t, expr='proud' if not speaking('prokhor', t) else 'smug', mouth_=mouth('prokhor', t),
          look=(0.6, 0.1), hand_n=(17.0, 46.0) if t < 11.2 else (17.0, 30.0), hand_f=(-14.0, 28.0), prop_f=lambda sp, h: C.pillow(sp, h))
    def f(big, v):
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 20, hy, t, 0.5)
    return K.shot(TAIGA, K.light_taiga, 655.0, 470.0, Z, acts=[a], fx_=f, sy=330)


def bear_snug(t, Z, expr='asleep', bubble=None, **kw):
    return A(C.potapych, BEAR_XY[0], BEAR_XY[1], WD * 3 * Z, t=t, expr=expr, bubble=bubble, **kw)


def prokhor_lap(t, Z, **kw):
    return A(C.prokhor, 706.0, 770.0, WD * 3 * Z, t=t, legs=False, frost=0.0, **kw)


def r_snuggle(t, u):
    """in the den: he settles into the sleeping bear's lap with his pillow; snot bubble; «Спит до апреля. Тариф — НОЛЬ.»"""
    Z = 1.6 + 0.06 * u
    b = bear_snug(t, Z, hand_n=(-2.0, 30.0))
    p = prokhor_lap(t, Z, expr='bliss' if not speaking('prokhor', t) else 'smug', mouth_=mouth('prokhor', t, 1.2),
                    hand_n=(16.0, 30.0), hand_f=(-12.0, 30.0))
    return K.shot(DEN, K.light_den, 720.0, 520.0, Z, acts=[b, p], sy=320)


def r_meter(t, u):
    """insert (visual gag): the old meter by the den wakes up — the disc spins, the rouble drum runs"""
    Z = 5.0
    k = sm(u / 0.7)
    rub = int(9000 * k)
    a = A(C.meter, METER_XY[0], METER_XY[1], 2.1 * 3 * Z, t=t, rub=rub, spin=u * 9.0)
    return K.shot(TAIGA, K.light_taiga, METER_XY[0], 466.0, Z, acts=[a], sy=320)


def r_bliss(t, u):
    """close-up: steaming, sweating, smug to the camera: «Городские — УЧИТЕСЬ!»"""
    m = mouth('prokhor', t)
    sz = 20.0 + 1.2 * u
    def f(big, v, a):
        K.sweat_glow(big, 0.8)
    hx_o, hy_o = 470, 980
    # the bear's belly behind him, at the same world ratio as in the wide shot (offset feet: bear -22, -10 world px)
    px_feet = (hx_o - 4.0 * sz, hy_o + 53.5 * sz)
    bx, by = px_feet[0] - 22.0 / WD * sz, px_feet[1] - 10.0 / WD * sz
    v0 = view_at(DEN, 720.0, 520.0, 1.6, 180, 320)
    bw = wpt(v0, bx, by)
    bear = A(C.potapych, bw[0], bw[1], sz, t=t, expr='asleep')
    big, a = K.cu(C.prokhor, t, DEN, 720.0, 520.0, 1.6, sz, head=(hx_o, hy_o), light=K.light_den, blur=4, extra_fx=f,
                  acts_before=[bear], expr='smug' if m > 0.05 else 'proud', mouth_=m, look=(0.2, 0.0), sweat=1.0, frost=0.0, legs=False,
                  hand_n=(19.0, 56.0))
    return big


# ================================================================== the TWIST
def r_eye(t, u):
    """17.5: the bubble pops, ONE eye opens behind the glasses — «Отопление. Девять ТЫСЯЧ.»"""
    awake = t >= 17.62
    bub = None if awake else min(1.0, 0.7 + 0.3 * (u / 0.12))
    if awake: bub = 0.0
    sz = 24.0 - 1.5 * sm(u / 1.6)
    big, a = K.cu(C.potapych, t, DEN, 720.0, 470.0, 1.6, sz, head=(470, 980), light=K.light_den, blur=5,
                  expr='asleep' if not awake else 'boss', eyes='one' if awake else None, bubble=bub, snore=not awake,
                  mouth_=mouth('bear', t, 1.4))
    if u < 0.25: K.CK.shake(big, t, 14, 40)
    return big


def r_bearcu(t, u):
    """the bear, both eyes now, deadpan; the «ТАЙГА-БАНК» card reader rises from under the pillow: «...Девять ТЫСЯЧ.»"""
    lift = sm((t - 19.5) / 0.5)
    hand = (24.0 + 4.0 * lift, 14.0 + 30.0 * lift)
    big, a = K.cu(C.potapych, t, DEN, 720.0, 470.0, 1.5, 17.0, head=(430, 820), light=K.light_den, blur=3,
                  expr='boss', mouth_=mouth('bear', t, 1.4), hand_n=hand, prop_n=lambda sp, h: C.terminal(sp, h, glow=lift))
    return big


def lamp_k(t):
    return sm((t - 20.66) / 0.06)


def r_reveal(t, u):
    """pull back: the cozy den is an OFFICE — the lamp clicks on over a stump-desk (folders «ДОЛЖНИКИ», abacus, mug), the board
    «УК «БЕРЛОГА»»; Прохор in the lap: «Ты ж СПИШЬ!»"""
    Z = 1.35 - 0.25 * sm(u / 0.6)
    lk = lamp_k(t)
    b = bear_snug(t, Z, expr='boss', hand_n=(30.0, 40.0), prop_n=lambda sp, h: C.terminal(sp, h))
    p = prokhor_lap(t, Z, expr='shock', mouth_=mouth('prokhor', t), hand_n=(18.0, 48.0), hand_f=(-14.0, 44.0), look=(0.8, 0.2))
    d = A(C.stump_desk, DESK_XY[0], DESK_XY[1], WD * 3 * Z * 1.15, t=t, lamp=lk)
    def f(big, v):
        if lk > 0:
            ox, oy = aout(d, v, 'lamp')
            fx.glow(big, ox, oy + 60, 520, (255, 220, 140), 0.40 * lk)
    big = K.shot(DEN, lambda v: K.light_den(v, lk), 760.0, 520.0, Z, acts=[b, p, d], fx_=f, sy=330)
    if u < 0.2: K.CK.shake(big, t, 8, 30)
    return big


def r_remote(t, u):
    """the bear in the lamp light, deadpan: «Я на УДАЛЁНКЕ.»"""
    def f(big, v, a):
        fx.glow(big, 980, 1400, 700, (255, 220, 140), 0.25)
    big, a = K.cu(C.potapych, t, DEN, 760.0, 470.0, 1.5, 18.0 + 0.6 * u, head=(440, 820), light=lambda v: K.light_den(v, 1.0), blur=3,
                  extra_fx=f, expr='boss', mouth_=mouth('bear', t, 1.4), hand_n=(30.0, 36.0), prop_n=lambda sp, h: C.terminal(sp, h))
    return big


def r_plead(t, u):
    """Прохор close-up, small and nervous: «А если не ЗАПЛАЧУ?»"""
    big, a = K.cu(C.prokhor, t, DEN, 700.0, 470.0, 1.6, 21.0 + 0.8 * u, head=(560, 960), light=lambda v: K.light_den(v, 1.0), blur=4,
                  expr='plead', mouth_=mouth('prokhor', t), look=(-0.6, 0.3), frost=0.0, legs=False, hand_n=(14.0, 44.0), hand_f=(-6.0, 44.0))
    return big


def r_yawn(t, u):
    """the bear yawns (fangs) — «ОТКЛЮЧУ.» — and rolls over: a shove"""
    yawn = t < 26.15
    roll = sm((t - 26.9) / 0.4)
    big, a = K.cu(C.potapych, t, DEN, 720.0, 470.0, 1.5, 19.0, head=(440 - 260 * roll, 820 + 120 * roll), light=lambda v: K.light_den(v, 1.0),
                  blur=3, expr='yawn' if yawn else 'boss', mouth_=1.0 if yawn else mouth('bear', t, 1.4), rot=-25 * roll, pivot=(0.0, 40.0))
    if roll > 0:
        fx.speed_lines(big, t, roll)
        K.CK.shake(big, t, 18 * roll, 30)
    return big


# ================================================================== out into the snow
def r_fly(t, u):
    """he shoots out of the den hole in an arc and plunges into a drift — snow splash — and freezes solid (ice block)"""
    Z = 1.35
    k = min(1.0, u / 0.65)
    x = lerp(650.0, 520.0, k); y = lerp(490.0, 640.0, k) - 120.0 * math.sin(math.pi * k)
    frozen = u > 0.9
    a = A(C.prokhor, x, y, WT * 3 * Z, t=t, expr='shock' if not frozen else 'frozen', rot=0 if k >= 1 else -400 * k, pivot=(0.0, 30.0),
          post=(lambda sp: C.ice_over(sp, 1.0)) if frozen else None, frost=1.0)
    def f(big, v):
        ox, oy = v.opt(520.0, 640.0)
        K.snow_burst(big, ox, oy - 40, t, 28.05, n=50)
        if u > 0.9 and u < 1.05: fx.glow(big, ox, oy - 120, 400, (220, 240, 255), 0.6)
    big = K.shot(TAIGA, K.light_taiga, 600.0, 470.0, Z, acts=[a], fx_=f, sy=330)
    if 0.6 < u < 0.9: K.CK.shake(big, t, 16, 36)
    return big


def r_ice(t, u):
    """close-up in the ice block, chattering: «Го-городские... НЕ учитесь.»"""
    def f(big, v, a):
        pass
    big, a = K.cu(C.prokhor, t, TAIGA, 560.0, 520.0, 1.6, 17.0 + 0.8 * u, head=(540, 960), light=K.light_taiga, blur=4, extra_fx=f,
                  expr='chatter', chatter=1.0, mouth_=mouth('prokhor', t, 1.2), look=(0.0, 0.1), frost=1.0, post=lambda sp: C.ice_over(sp, 1.0))
    return big


def r_ice2(t, u):
    """medium: the ice block in the drift by the den; «...НЕ учитесь.»; the striped nightcap creeps out of the hole behind"""
    Z = 2.0
    a = A(C.prokhor, 560.0, 610.0, WT * 3 * Z, t=t, expr='chatter', chatter=1.0, mouth_=mouth('prokhor', t, 1.2), frost=1.0,
          post=lambda sp: C.ice_over(sp, 1.0))
    peek = sm((t - 31.6) / 0.8)
    acts = [bear_hole(t, Z, peek)] if peek > 0 else []
    return K.shot(TAIGA, K.light_taiga, 610.0, 480.0, Z, acts=acts + [a], fx_=lambda big, v: hole_occlude(big, v, acts), sy=320)


def bear_hole(t, Z, k, **kw):
    """the bear rising inside the den hole (k 0..1): everything outside the hole and below its top edge is hidden by the snow"""
    y = 522.0 + 70.0 * (1 - k)
    return A(C.potapych, HOLE[0] - 4.0, y, 1.12 * 3 * Z, t=t, **kw)


def hole_occlude(big, v, acts):
    """restore the snow mound over the parts of the bear outside the hole ellipse (below the hole top) — he sits IN the hole"""
    if not acts: return
    xs, ys = v.grid()
    cx, cy, rx, ry = HOLE
    X = xs[None, :].astype(np.float32); Y = ys[:, None].astype(np.float32)
    outside = (((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2 > 1.0) & (Y > cy - ry * 0.55)
    bg = v.bg()
    big[outside] = bg[outside]


def r_button(t, u):
    """button: the bear peeks out of the hole in his nightcap; a paw slaps the bill on the ice block — to the camera: «Плюс ПЕНИ.»"""
    Z = 2.4
    slap = t >= 32.95
    p = A(C.prokhor, 590.0, 640.0, WT * 3 * Z, t=t, expr='frozen', frost=1.0, post=lambda sp: C.ice_over(sp, 1.0))
    b = bear_hole(t, Z, 1.0, expr='boss', mouth_=mouth('bear', t, 1.4), look=(0.0, -0.1), hand_n=(22.0, 46.0))
    acts = [b]
    bl = [A(bill_only, 578.0, 590.0, WT * 0.9 * 3 * Z, t=t)] if slap else []
    def f(big, v):
        hole_occlude(big, v, acts)
        if slap and t < 33.1: fx.glow(big, *v.opt(560, 540), 300, (255, 255, 255), 0.5)
    big = K.shot(TAIGA, K.light_taiga, 625.0, 470.0, Z, acts=acts, fx_=f, sy=320)
    # foreground: the ice block + the bill on top of everything (drawn after the occlusion)
    v = view_at(TAIGA, 625.0, 470.0, Z, 180, 320)
    lt = K.light_taiga(v)
    for x in [p] + bl: x(big, v, lt)
    fx.vignette(big, 0.2)
    return big


R = [r_hook, r_stove, r_warm, r_blog, r_trek, r_entrance, r_snuggle, r_meter, r_bliss, r_eye, r_bearcu, r_reveal, r_remote, r_plead,
     r_yawn, r_fly, r_ice, r_ice2, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 1, ['9 000 ЗА', 'ТЕПЛО?!'], hook_t=(0.10, 2.0), hook_y=300,
              stickers=[(K.st('ЛАЙФХАК №1', fg=(255, 214, 80)), 6.10, 7.95, 540, 620),
                        (K.st('ТАРИФ: 0 ₽', fg=(150, 255, 160)), 13.10, 14.60, 560, 520),
                        (K.st('СЧЁТ?!', fg=(255, 90, 80), size=80), 17.60, 19.15, 540, 560)],
              flashes=[2.80, TWIST, 27.40], mosaics=[CUTS[11]],
              cap_y={0: 1560, 4: 1000, 6: 1620, 9: 1450, 13: 1640, 16: 1500, 18: 1720})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
