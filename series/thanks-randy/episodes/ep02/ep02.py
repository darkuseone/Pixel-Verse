"""S01E02 «GRAVY'S A LIQUID?!» (32.75 s, twist at 17.50 s / 53 %, type: success worse than failure).
Tuesday, Tumbleweed Intl, Arizona. HOOK: Officer Patty's blue glove holds Nana's gallon of gravy over the X-ray belt — Randy: «Gravy's a
LIQUID?!» — «Over three point four ounces. Liquid.» — «It's Nana's gravy!» — «Then it's a family liquid.» X-RAY: Tom in a bin (he flew
the turkey to Arizona to thaw): «Flew me to Arizona to thaw. Still frozen.» Randy unscrews the jug: «If it's inside me — it's not
luggage.» — chugs the whole gallon, belly inflates: «Zero liquid!» TWIST: the body scanner shows him FULL of gravy — «Unexpected liquid.
One hundred twenty-eight ounces.» — «Sir. You are a liquid now.» — sloshing: «Twenty years — never burned a turkey!» — «Not flying
today either.» He rides into baggage in a grey bin; Tom passes: «Still frozen. Still flying.» X-ray: «LIQUID.» (loops to the hook).
Clue: the sign «LIQUIDS 3.4 OZ — YES, GRAVY TOO» on the machine and the body scanner booth behind them from the first shots.
  python3 ep02.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props import randycast as C
from props import randykit as K
from props.randykit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='randy', lang='us'))
AIR, AIR_B = K.world('airport'), K.world('airport_b')
WS = 4.0                       # world px per sprite px in front of the X-ray machine
FLOOR = 650.0
RAN = (470.0, FLOOR)           # Randy at the start of the belt
PAT = (722.0, FLOOR)           # Officer Patty by the tunnel exit
BOOTH = (1052.0, 412.0)        # body scanner floor (inside the glass)
GLASS = (948.0, 140.0, 1162.0, 412.0)


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def W(v, ox, oy):
    return wpt(v, ox, oy)


def jug(tilt=0.0, level=1.0):
    return lambda sp, h: C.gravy_jug(sp, (h[0] - 1.0, h[1] - 2.0), tilt=tilt, level=level)


def light(alarm=0.0):
    return lambda v: K.light_airport(v, alarm)


def card(big, img, x, y):
    O.overlay(big, img, x, y, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x, y, x + img.shape[1], y + img.shape[0]))


def patty_act(v, x, y, s, t, **kw):
    kw.setdefault('expr', 'dead')
    return A(C.patty, *W(v, x, y), s, t=t, flip=True, mouth_=mouth('patty', t), bubble=kw.pop('bubble', 0.0), **kw)


# ================================================================== 0: HOOK — the gloved hand holds the gravy over the belt
def r_hook(t, u):
    Z = 1.35
    v = V(AIR, 560.0, 400.0, Z)
    s = 22.0
    pat = patty_act(v, 1260.0, 1100.0 + 60.0 * s, s, t, hand_n=(14.0, 52.0), prop_n=jug(), look=(-0.9, 0.0))
    big, a = K.cu(C.randy, t, AIR, 560.0, 400.0, Z, s, head=(360, 880), light=light(), blur=4, acts_after=[pat],
                  expr='shout', mouth_=max(0.5, mouth('randy', t)), tremble=1.0, look=(1.0, 0.1), stache='up', hand_n=(18.0, 60.0))
    if u < 0.3: K.CK.shake(big, t, 14, 33)
    return big


# ================================================================== 1: PATTY — «Over three point four ounces. Liquid.»
def r_patty(t, u):
    pop = sm((t - 4.20) / 0.15) * (1 - sm((t - 4.36) / 0.05))
    big, a = K.cu(C.patty, t, AIR, 640.0, 330.0, 1.35, 20.0 + 0.8 * u, head=(560, 980), light=light(), blur=3, flip=True,
                  expr='dead', mouth_=mouth('patty', t), look=(-0.6, 0.0), bubble=pop, hand_n=(14.0, 50.0), prop_n=jug(),
                  hand_f=(-12.0, 44.0 + 4 * abs(math.sin(t * 3))))
    return big


# ================================================================== 2: PLEAD — two-shot across the belt
def r_plead(t, u):
    k = sm(u / 4.0)
    Z = lerp(1.04, 1.12, k)
    cx = lerp(596.0, 600.0, k)
    v = V(AIR, cx, 470.0, Z)
    s = WS * Z * 3
    r = A(C.randy, *RAN, s, t=t, expr='plead' if speaking('randy', t) else 'sad', mouth_=mouth('randy', t), look=(1.0, 0.0),
          hand_n=(16.0, 58.0), hand_f=(12.0, 56.0))
    p = A(C.patty, *PAT, s, t=t, flip=True, expr='dead', mouth_=mouth('patty', t), look=(-1.0, 0.0), hand_n=(16.0, 50.0), prop_n=jug(),
          bubble=0.0)
    return K.shot(AIR, light(), cx, 470.0, Z, acts=[r, p])


# ================================================================== 3: X-RAY — Tom in a bin: «Flew me to Arizona to thaw. Still frozen.»
def r_xray(t, u):
    Z = 1.3
    v = V(AIR_B, 520.0, 420.0, Z)
    s = 24.0
    bx, by = 560.0, 1700.0
    acts = [A(C.tsa_bin, *W(v, bx, by), s, t=t, part='back'),
            A(C.tom, *W(v, bx - 30.0, by - 3.0 * s), s, t=t, expr='dead', mouth_=mouth('tom', t, 1.6), look=(-0.2, -0.2)),
            A(C.tsa_bin, *W(v, bx, by), s, t=t, part='front')]
    def pre(big, v_): big[:] = K.dof(big, 6)
    def f(big, v_):
        K.cold_vapor(big, bx - 20, by - 18 * s, t, 1.0, 1.3)
        K.thaw_meter(big, t, 10.6, 12.27, 'ROCK', x=930, y=1240)
    big = K.shot(AIR_B, light(), 520.0, 420.0, Z, acts=acts, pre=pre, fx_=f)
    scr = K.xray_ui(C.tom, t, 860, 560, s=12.0, label='SOLID FOOD', sub='UNLIMITED')
    card(big, scr, (OUT_W - scr.shape[1]) // 2, 250)
    return big


# ================================================================== 4: SCHEME — CU, unscrewing the cap
def r_scheme(t, u):
    big, a = K.cu(C.randy, t, AIR, 600.0, 400.0, 1.35, 23.0 + 1.0 * u, head=(470, 900), light=light(), blur=4,
                  expr='sly', mouth_=mouth('randy', t), look=(0.9, 0.2), hand_n=(16.0, 52.0), prop_n=jug(),
                  hand_f=(12.0, 66.0 + 2 * math.sin(t * 14)), stache='up')
    return big


# ================================================================== 5: CHUG — the whole gallon, belly inflates: «Zero liquid!»
def r_chug(t, u):
    Z = 1.12
    v = V(AIR, 572.0, 470.0, Z)
    s = WS * Z * 3
    drink = t < 15.5
    bel = sm((t - 14.95) / 0.6)
    lvl = 1.0 - bel
    if drink:
        r = A(C.randy, *RAN, s, t=t, expr='content', mouth_=0.0, belly=bel, gravy=bel, look=(0.8, 0.6),
              hand_n=(13.0, 70.0), prop_n=jug(tilt=150.0, level=lvl), hand_f=(10.0, 60.0))
    else:
        r = A(C.randy, *RAN, s, t=t, expr='cheer', mouth_=mouth('randy', t), belly=1.0, gravy=1.0, look=(0.8, 0.0),
              hand_n=(19.0, 74.0), prop_n=jug(tilt=-30.0, level=0.0), hand_f=(-14.0, 70.0), stache='up')
    p = A(C.patty, *PAT, s, t=t, flip=True, expr='dead', look=(-1.0, 0.0), bubble=0.5 + 0.5 * sm((t - 16.2) / 1.0), hand_n=(10.0, 30.0))
    def f(big, v_):
        if drink:
            hx, hy = aout(r, v_, 'mouth')
            for q in range(3):
                ph = (t * 6 + q / 3) % 1.0
                K.puff(big, hx + 10, hy + 30 + 120 * ph, 14, 0.8 * (1 - ph), (130, 76, 36), q=9)
    return K.shot(AIR, light(), 572.0, 470.0, Z, acts=[r, p], fx_=f)


# ================================================================== 6: TWIST — the body scanner: he is FULL of gravy
def r_scanner(t, u):
    Z = 1.2
    cx = 1000.0
    v = V(AIR, cx, 330.0, Z)
    s = 3.0 * Z * 3
    r = A(C.randy, *BOOTH, s, t=t, expr='shock', mouth_=0.3, belly=1.0, gravy=1.0, look=(-0.6, 0.0), hand_n=(10.0, 90.0), hand_f=(-8.0, 90.0))
    def f(big, v_):
        bg = v_.bg()                                                         # the glass in front of him: blend the booth back over
        x0, y0 = v_.opt(GLASS[0], GLASS[1]); x1, y1 = v_.opt(GLASS[2], GLASS[3])
        X0, X1, Y0, Y1 = int(max(0, x0)), int(min(OUT_W, x1)), int(max(0, y0)), int(min(OUT_H, y1))
        if X0 < X1 and Y0 < Y1:
            big[Y0:Y1, X0:X1] = (big[Y0:Y1, X0:X1] * 0.72 + bg[Y0:Y1, X0:X1] * 0.28).astype(np.uint8)
        if u < 0.3: K.CK.shake(big, t, 16, 40)
    big = K.shot(AIR, light(1.0), cx, 330.0, Z, acts=[r], fx_=f)
    K.alarm_tint(big, t, 0.5)
    scr = K.scanner_ui(t, level=0.62, w=560, h=640)
    card(big, scr, 40, 230)
    return big


# ================================================================== 7: LIQUID — «Sir. You are a liquid now.»
def r_liquid(t, u):
    pop = sm((t - 23.15) / 0.15) * (1 - sm((t - 23.32) / 0.05))
    big, a = K.cu(C.patty, t, AIR, 700.0, 340.0, 1.35, 23.0 + 1.0 * u, head=(560, 960), light=light(0.5), blur=4, flip=True,
                  expr='dead', mouth_=mouth('patty', t), look=(-0.4, 0.0), bubble=pop, hand_n=(15.0, 54.0), hand_f=(-14.0, 30.0))
    K.alarm_tint(big, t, 0.3)
    return big


# ================================================================== 8: SLOSH — «Twenty years — never burned a turkey!» — «Not flying today either.»
def r_slosh(t, u):
    k = sm(u / 5.0)
    Z = lerp(1.04, 1.12, k)
    cx = 600.0
    v = V(AIR, cx, 470.0, Z)
    s = WS * Z * 3
    step = math.sin(t * 6.0)
    r = A(C.randy, RAN[0] + 20.0 * k, FLOOR, s, t=t, expr='plead' if speaking('randy', t) else 'sad', mouth_=mouth('randy', t),
          belly=1.0 + 0.10 * step, gravy=1.0, look=(1.0, 0.0), walk=t * 6.0 if t < 26.3 else None, hand_n=(17.0, 60.0), hand_f=(13.0, 58.0))
    p = A(C.patty, *PAT, s, t=t, flip=True, expr='dead', mouth_=mouth('patty', t), look=(-1.0, 0.0), hand_n=(15.0, 46.0),
          hand_f=(-12.0, 46.0), bubble=0.0)
    return K.shot(AIR, light(), cx, 470.0, Z, acts=[r, p])


# ================================================================== 9: BINS — Randy rides into baggage in a grey bin, Tom passes
def r_bins(t, u):
    Z = 1.25
    v = V(AIR_B, 600.0, 420.0, Z)
    s = 9.0
    q = u / (CUTS[10] - CUTS[9])
    bx = lerp(300.0, 600.0, q)
    by = 1330.0
    acts = [A(C.tsa_bin, *W(v, bx, by), s, t=t, part='back'),
            A(C.randy, *W(v, bx - 6.0 * s, by - 4.0 * s), s, t=t, rot=-90.0, pivot=(0.0, 30.0), expr='sad', belly=1.0, gravy=1.0,
              look=(0.0, 0.8), mitt=True),
            A(C.tsa_bin, *W(v, bx, by), s, t=t, part='front')]
    tx = lerp(1000.0, 900.0, q)
    acts += [A(C.tsa_bin, *W(v, tx, by), s, t=t, part='back'),
             A(C.tom, *W(v, tx - 10.0, by - 3.0 * s), s, t=t, expr='dead', mouth_=mouth('tom', t, 1.6), look=(-0.8, -0.2)),
             A(C.tsa_bin, *W(v, tx, by), s, t=t, part='front')]
    def f(big, v_):
        K.cold_vapor(big, tx - 10, by - 18 * s, t, 0.8, 0.9)
    return K.shot(AIR_B, light(), 600.0, 420.0, Z, acts=acts, fx_=f)


# ================================================================== 10: LOOP — the X-ray: «LIQUID.»
def r_loop(t, u):
    Z = 1.3
    v = V(AIR_B, 640.0, 420.0, Z)
    def pre(big, v_): big[:] = K.dof(big, 8)
    big = K.shot(AIR_B, light(1.0), 640.0, 420.0, Z, pre=pre)
    K.alarm_tint(big, t, 0.5)
    scr = K.xray_ui(C.randy, t, 860, 620, s=8.0, label='LIQUID', sub='128 OZ OF GRAVY', ok=False, rot=-90.0,
                    spr=dict(belly=1.0, gravy=1.0, expr='sad'), at=(150, 420))
    card(big, scr, (OUT_W - scr.shape[1]) // 2, 720)
    return big


R = [r_hook, r_patty, r_plead, r_xray, r_scheme, r_chug, r_scanner, r_liquid, r_slosh, r_bins, r_loop]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 2, ["GRAVY'S A", 'LIQUID?!'], hook_t=(0.10, 1.40), hook_y=300, hook_size=74,
              day=(1.50, 4.40, 'TUESDAY', '2 DAYS TO TURKEY', 1650),
              stickers=[(K.st('LIQUID: 0 OZ', fg=(170, 255, 90), size=58), 16.20, 17.45, 540, 330),
                        (K.st('128 OZ!', fg=(255, 90, 80), size=84), 18.10, 20.45, 800, 1100),
                        (K.st('FRAGILE', fg=(255, 214, 80), size=60), 29.00, 31.70, 540, 640)],
              flashes=[TWIST, 31.74], mosaics=[],
              cap_y={0: 1560, 1: 1600, 2: 1600, 3: 1100, 4: 1560, 5: 1600, 6: 1560, 7: 1600, 8: 1600, 9: 1620, 10: 1560})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
