"""S01E04 «RANDY, NO!» (34.45 s, twist at 17.70 s / 51 %, type: the saviour is a victim too).
Thursday 9:58 AM, the driveway. HOOK: Randy in welding goggles lowers frozen Tom on a hook into the Fry-Hard 3000; the family at the
window: «RANDY, NO!» — FIREBALL. Tom drops from the sky into a crater: «Still frozen.» Randy, soot, no eyebrows: «Twenty years. Never
burned a turkey.» — Nana with an extinguisher from her purse: «You burned the GARAGE.» — on the phone with the garage ablaze: «Garage is
on FIRE! Send EVERYBODY!» — Brayden streams: «Bro. We're trending.» — by the fire-department flyer (clue: ANNUAL TURKEY FRY · THU 10 AM AT
THE STATION): «Okay. The pros are here.» TWIST: the engine skids in with its own ladder on fire, Captain Dunn holds a charred turkey:
«Ours went off at the station.» — «Twenty years. Never burned a turkey.» — «…Same.» (they hug, both smoking) — Nana: «So. When are
you getting married?» — «To the job, ma'am.» — Dunn eyes Tom: «That bird still frozen? Got any oil?» — the family: «RANDY, NO!» (loop).
  python3 ep04.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
import stage as ST
from stage import view_at, OUT_W, OUT_H, Light
from scene import sm, lerp
from episode import Episode
from props import randycast as C
from props import randykit as K
from props import taigakit as TK
from props.randykit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='randy', lang='us'))
YARD, YARD_B = K.world('yard'), K.world('yard_b')
WS = 3.0                       # world px per sprite px on the driveway
FLOOR = 650.0
FRY = (450.0, 655.0)
RAN = (330.0, FLOOR)
WINDOW = (600.0, 303.0, 673.0, 393.0)
GARAGE = (82.0, 292.0, 455.0, 482.0)
CRATER = (760.0, 612.0)
FLYER = (459.0, 300.0)


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def W(v, ox, oy):
    return wpt(v, ox, oy)


def light_yard(v, siren=0.0, fire=0.0, t=0.0):
    keys = [(640, 0, 1100, (220, 226, 240), 0.22)]
    if fire > 0: keys.append((260, 400, 700, (255, 140, 60), 0.45 * fire))
    if siren > 0:
        c = (255, 50, 50) if int(t * 6) % 2 == 0 else (60, 120, 255)
        keys.append((900, 600, 900, c, 0.40 * siren))
    return Light(amb=(0.96, 0.97, 1.02), keys=[(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in keys], rim=(1, -0.3, (230, 236, 250), 0.25),
                 grad=(1.0, 0.92))


def burning_garage(big, v, t, k=1.0):
    """flames filling the open garage + black smoke over the roof (world box GARAGE)"""
    if k <= 0: return
    x0, y0, x1, y1 = GARAGE
    for i in range(6):
        wx = x0 + (i + 0.5) * (x1 - x0) / 6
        ox, oy = v.opt(wx, y1 - 6)
        TK.fire(big, ox, oy, t + i * 0.37, w=110 * v.Z, h=(260 + 60 * math.sin(t * 3 + i)) * v.Z * k, k=k, seed=i)
    for i in range(5):
        ph = (t * 0.25 + i / 5) % 1.0
        ox, oy = v.opt(x0 + 80 + i * 70, y0 - 20 - 260 * ph)
        K.puff(big, ox, oy, (60 + 120 * ph) * v.Z, 0.55 * (1 - ph) * k, (50, 46, 50), q=12)


def inside_window(big, v, acts, lt, rect=WINDOW, tint=0.22):
    """people standing behind the front window: drawn on a copy, pasted back only inside the window glass, glass tint on top"""
    tmp = big.copy()
    for a in acts: a(tmp, v, lt)
    ox0, oy0 = v.opt(rect[0], rect[1]); ox1, oy1 = v.opt(rect[2], rect[3])
    X0, X1, Y0, Y1 = int(max(0, ox0)), int(min(OUT_W, ox1)), int(max(0, oy0)), int(min(OUT_H, oy1))
    if X0 < X1 and Y0 < Y1:
        big[Y0:Y1, X0:X1] = (tmp[Y0:Y1, X0:X1] * (1 - tint) + np.array((210, 220, 236)) * tint).astype(np.uint8)


def family_window(v, t, scream=1.0):
    s = 1.7 * v.Z * 3
    m = max(0.6 * scream, mouth('family', t))
    return [A(C.joyce, 622.0, 420.0, s, t=t, expr='panic', mouth_=m, look=(-0.8, 0.0), purse=None, flip=True),
            A(C.brayden, 656.0, 486.0, s, t=t, expr='panic', mouth_=m, look=(-0.8, 0.0), stick=False, flip=True)]


def fireball(big, x, y, t, t0, scale=1.0):
    u = t - t0
    if u < 0 or u > 2.0: return
    r = (100 + 520 * min(1.0, u / 0.35)) * scale
    a = 1.0 if u < 0.6 else max(0.0, 1 - (u - 0.6) / 1.4)
    for i, (dx, dy, c) in enumerate(((0, 0, (255, 240, 160)), (-0.4, -0.3, (255, 170, 60)), (0.4, -0.35, (255, 120, 40)),
                                      (0.0, -0.7, (220, 70, 40)), (-0.2, -1.0, (90, 80, 80)), (0.3, -1.1, (70, 66, 70)))):
        rr = r * (0.55 if i < 4 else 0.45)
        K.puff(big, x + dx * r, y + dy * r - u * 300 * scale, rr, a * (0.95 if i < 4 else 0.7), c, q=14)


# ================================================================== 0: HOOK — lowering frozen Tom into the fryer, the family at the window
def r_hook(t, u):
    Z = 0.98
    cx = 468.0
    v = V(YARD, cx, 470.0, Z)
    s = WS * Z * 3
    lower = sm(u / 1.4)
    r = A(C.randy, *RAN, s, t=t, expr='proud', mouth_=0.0, goggles=True, look=(1.0, 0.4), hand_n=(18.0, 52.0 - 6 * lower),
          prop_n=lambda sp, h: C.hook_pole(sp, h, 20.0), hand_f=(14.0, 50.0 - 6 * lower))
    fr = A(C.fryer, *FRY, s, t=t)
    def f(big, v_):
        hx, hy = aout(r, v_, 'hand')
        ex, ey = hx + 20.0 * 0.8 * s, hy + (20.0 * 0.25 + 2.4) * s
        tom = A(C.tom, *W(v_, ex - 2 * s, ey + 16.0 * s), s, t=t, expr='dead', look=(-0.4, 0.4))
        tom(big, v_, light_yard(v_))
        inside_window(big, v_, family_window(v_, t), light_yard(v_))
    return K.shot(YARD, light_yard, cx, 470.0, Z, acts=[fr, r], fx_=f)


# ================================================================== 1: BOOM — the fireball
def r_boom(t, u):
    Z = 1.05
    cx = 450.0
    v = V(YARD, cx, 460.0, Z)
    s = WS * Z * 3
    fr = A(C.fryer, *FRY, s, t=t, flames=1.0)
    r = A(C.randy, RAN[0] - 120.0 * sm(u / 0.4), FLOOR, s, t=t, expr='shock', mouth_=0.8, goggles=True, soot=0.3 * sm(u / 0.5),
          look=(1.0, 0.0), hand_n=(18.0, 70.0), hand_f=(-14.0, 70.0), rot=24.0 * sm(u / 0.4), pivot=(0.0, 0.0))
    def pre(big, v_): burning_garage(big, v_, t, sm(u / 1.0))
    def f(big, v_):
        ox, oy = v_.opt(*FRY)
        fireball(big, ox, oy - 160, t, CUTS[1] + 0.02, 1.0)
        if u < 0.6: K.CK.shake(big, t, 30, 40)
        K.thaw_meter(big, t, 2.2, 3.5, 'FIRE!', x=880, y=1240, level=1.0)
    return K.shot(YARD, lambda v_: light_yard(v_, fire=1.0), cx, 460.0, Z, acts=[fr, r], pre=pre, fx_=f)


# ================================================================== 2: CRATER — Tom drops from the sky: «Still frozen.»
def r_crater(t, u):
    Z = 1.45
    v = V(YARD, CRATER[0], 470.0, Z)
    s = WS * Z * 3 * 1.4
    fall = sm(u / 0.12) if u < 0.12 else 1.0
    tom = A(C.tom, CRATER[0], lerp(200.0, CRATER[1], fall), s, t=t, expr='dead', mouth_=mouth('tom', t, 1.6), look=(-0.1, -0.2))
    def pre(big, v_):
        ox, oy = v_.opt(*CRATER)
        K.puff(big, ox, oy + 10, 240, 0.85, (60, 52, 44), q=12)
        K.puff(big, ox, oy - 4, 200, 0.85, (40, 34, 30), q=12)
    def f(big, v_):
        ox, oy = v_.opt(*CRATER)
        K.cold_vapor(big, ox, oy - 200, t, 1.0, 1.3)
        if 0.10 < u < 0.4: K.CK.shake(big, t, 20, 40)
        TK.snow_burst(big, ox, oy - 40, t, CUTS[2] + 0.10, n=36, col=(120, 90, 60))
        K.thaw_meter(big, t, 3.9, 5.4, 'ROCK', x=900, y=600, level=0.08)
    return K.shot(YARD, light_yard, CRATER[0], 470.0, Z, acts=[tom], pre=pre, fx_=f)


# ================================================================== 3: SOOT — CU, no eyebrows: «Twenty years. Never burned a turkey.»
def r_soot(t, u):
    big, a = K.cu(C.randy, t, YARD, 300.0, 400.0, 1.3, 23.0 + 0.8 * u, head=(560, 960), light=lambda v_: light_yard(v_, fire=1.0), blur=4,
                  expr='proud' if speaking('randy', t) else 'stunned', mouth_=mouth('randy', t), soot=0.32, brows=False, goggles=True,
                  look=(0.4, 0.0), stache='droop', hand_n=(17.0, 40.0), mitt=True)
    hx, hy = 560, 960
    for q in range(3):
        ph = (t * 0.8 + q / 3) % 1.0
        K.puff(big, hx + 140 + 30 * q, hy + 60 - 300 * ph, 40 + 60 * ph, 0.5 * (1 - ph), (70, 66, 70), q=12)
    return big


def r_garage(t, u):
    """Nana with an extinguisher from her purse: «You burned the GARAGE.»"""
    Z = 1.25
    cx = 330.0
    v = V(YARD, cx, 470.0, Z)
    s = WS * Z * 3
    r = A(C.randy, 280.0, FLOOR, s, t=t, expr='stunned', mouth_=0.0, soot=0.32, brows=False, goggles=True, look=(0.8, 0.2), stache='droop')
    j = A(C.joyce, 410.0, FLOOR + 10.0, s, t=t, flip=True, expr='fine', mouth_=mouth('joyce', t), look=(-0.8, 0.2), purse='side',
          hand_n=(9.0, 22.0), prop_n=lambda sp, h: C.extinguisher(sp, h))
    def pre(big, v_): burning_garage(big, v_, t, 1.0)
    def f(big, v_):
        if t > 8.45:
            hx, hy = aout(j, v_, 'hand')
            for q in range(5):
                ph = (t * 3 + q / 5) % 1.0
                K.puff(big, hx - 60 - 260 * ph, hy - 40 - 60 * ph, 30 + 50 * ph, 0.6 * (1 - ph), (240, 240, 244), q=10)
    return K.shot(YARD, lambda v_: light_yard(v_, fire=1.0), cx, 470.0, Z, acts=[r, j], pre=pre, fx_=f)


# ================================================================== 4: CALL — the garage ablaze: «Send EVERYBODY!» — «We're trending.»
def r_call(t, u):
    Z = 1.0 + 0.08 * sm(u / 5.0)
    cx = 380.0
    v = V(YARD, cx, 470.0, Z)
    s = WS * Z * 3
    r = A(C.randy, 330.0, FLOOR, s, t=t, expr='panic' if speaking('randy', t) else 'losing', mouth_=mouth('randy', t), soot=0.32, brows=False,
          goggles=True, look=(0.6, 0.0), hand_n=(15.0, 64.0), prop_n=lambda sp, h: C.cell(sp, h), hand_f=(-14.0, 64.0), tremble=0.6)
    b = A(C.brayden, 520.0, FLOOR + 20.0, s, t=t, flip=True, expr='hype' if speaking('brayden', t) else 'lazy', mouth_=mouth('brayden', t),
          look=(-0.8, 0.0))
    def pre(big, v_): burning_garage(big, v_, t, 1.0)
    def f(big, v_):
        if t > 13.1: K.live_frame(big, t, viewers=int(1200 + (t - 13.1) * 41000), k=1.0)
    return K.shot(YARD, lambda v_: light_yard(v_, fire=1.0), cx, 470.0, Z, acts=[r, b], pre=pre, fx_=f)


# ================================================================== 5: PROS — by the fire-dept flyer: «Okay. The pros are here.»
def r_pros(t, u):
    Z = 1.35
    cx = 470.0
    v = V(YARD, cx, 440.0, Z)
    s = WS * Z * 3
    sir = sm((t - 15.6) / 2.0)
    r = A(C.randy, 430.0, FLOOR, s, t=t, expr='content' if speaking('randy', t) else 'smile', mouth_=mouth('randy', t), soot=0.32, brows=False,
          goggles=True, look=(1.0, -0.2), hand_n=(16.0, 40.0), stache='up')
    def pre(big, v_): burning_garage(big, v_, t, 0.8)
    return K.shot(YARD, lambda v_: light_yard(v_, siren=sir, fire=0.6, t=t), cx, 440.0, Z, acts=[r], pre=pre)


# ================================================================== 6: TRUCK — TWIST: the engine's own ladder is on fire
def r_truck(t, u):
    Z = 1.1
    cx = 780.0
    v = V(YARD_B, cx, 470.0, Z)
    s = 3.4 * Z * 3
    k = sm(u / 0.35)
    tx = lerp(300.0, 860.0, k)
    truck = A(C.fire_truck, tx, 712.0, s, t=t)
    d = A(C.dunn, tx - 10.0, 716.0, s * 0.95, t=t, flip=True, expr='dead', mouth_=mouth('dunn', t), look=(-0.6, 0.0), soot=0.8,
          hand_n=(16.0, 50.0)) if u > 0.45 else None
    acts = [truck] + ([d] if d else [])
    def f(big, v_):
        for i in range(5):
            wx = tx + (-60.0 - i * 9.0) * 3.4
            ox, oy = v_.opt(wx, 712.0 - 50.0 * 3.4)
            TK.fire(big, ox, oy, t + i * 0.3, w=90 * v_.Z, h=200 * v_.Z, k=1.0, seed=i)
            K.puff(big, ox, oy - 260 - 100 * ((t + i * 0.2) % 1.0), 70, 0.4, (60, 56, 60), q=12)
        if d:
            hx, hy = aout(d, v_, 'hand')
            bt = A(C.tom, *W(v_, hx - 20, hy + 150), s * 0.9, t=t, face=False, char=0.85, frost=0.0, flip=True)
            bt(big, v_, None)
            K.puff(big, hx + 60, hy - 120 - 120 * ((t * 1.3) % 1.0), 50, 0.5, (70, 66, 70), q=10)
        if u < 0.5: K.CK.shake(big, t, 18, 40)
    return K.shot(YARD_B, lambda v_: light_yard(v_, siren=1.0, t=t), cx, 470.0, Z, acts=acts, fx_=f)


# ================================================================== 7: SAME — «Twenty years. Never burned a turkey.» — «…Same.» (hug)
def r_same(t, u):
    Z = 1.32
    cx = 520.0
    v = V(YARD, cx, 450.0, Z)
    s = WS * Z * 3
    hug = sm((t - 22.95) / 0.4)
    r = A(C.randy, 420.0 + 40.0 * hug, FLOOR, s, t=t, expr='cry' if t > 22.2 else 'stunned', mouth_=mouth('randy', t), soot=0.32, brows=False,
          goggles=True, look=(1.0, 0.0), hand_n=(18.0 + 6 * hug, 52.0 + 6 * hug), hand_f=(16.0, 50.0))
    d = A(C.dunn, 620.0 - 40.0 * hug, FLOOR, s * 0.95, t=t, flip=True, expr='dead' if not speaking('dunn', t) else 'sad', mouth_=mouth('dunn', t),
          look=(-0.9, 0.0), soot=0.8, hand_n=(17.0 + 5 * hug, 56.0 + 6 * hug), hand_f=(-12.0, 40.0))
    def pre(big, v_): burning_garage(big, v_, t, 0.6)
    def f(big, v_):
        for a in (r, d):
            hx, hy = aout(a, v_, 'head')
            ph = (t * 0.8) % 1.0
            K.puff(big, hx, hy - 160 - 200 * ph, 40 + 40 * ph, 0.45 * (1 - ph), (70, 66, 70), q=10)
    return K.shot(YARD, lambda v_: light_yard(v_, siren=0.5, fire=0.5, t=t), cx, 450.0, Z, acts=[d, r], pre=pre, fx_=f)


# ================================================================== 8: MARRIED — Nana tugs the captain's sleeve
def r_married(t, u):
    Z = 1.42
    cx = 560.0
    v = V(YARD, cx, 440.0, Z)
    s = WS * Z * 3
    j = A(C.joyce, 500.0, FLOOR + 6.0, s, t=t, expr='nosy', mouth_=mouth('joyce', t), look=(0.6, 0.8), purse='side', hand_n=(9.0, 34.0))
    d = A(C.dunn, 610.0, FLOOR, s * 0.95, t=t, flip=True, expr='dead' if t < 26.5 else 'sad', mouth_=mouth('dunn', t), look=(-0.6, -0.6),
          soot=0.8, hand_f=(-14.0, 34.0))
    return K.shot(YARD, lambda v_: light_yard(v_, siren=0.4, t=t), cx, 440.0, Z, acts=[j, d])


# ================================================================== 9: OIL — Dunn eyes Tom in the crater: «Got any oil?»
def r_oil(t, u):
    Z = 1.3
    cx = 700.0
    v = V(YARD, cx, 450.0, Z)
    s = WS * Z * 3
    d = A(C.dunn, 640.0, FLOOR - 20.0, s * 0.95, t=t, expr='dead' if t < 30.2 else 'grin', mouth_=mouth('dunn', t), look=(0.6, 0.8),
          soot=0.8, hand_n=(14.0, 60.0 if t > 30.2 else 40.0))
    tom = A(C.tom, CRATER[0] + 20.0, CRATER[1], s * 1.1, t=t, expr='dead', look=(-0.8, -0.4))
    r = A(C.randy, 500.0, FLOOR, s, t=t, expr='smug' if t > 29.0 else 'normal', mouth_=0.0, soot=0.32, brows=False, goggles=True,
          look=(1.0, 0.0), stache='up' if t > 29 else None)
    def pre(big, v_):
        ox, oy = v_.opt(*CRATER)
        K.puff(big, ox + 60, oy + 10, 200, 0.85, (60, 52, 44), q=12)
    def f(big, v_):
        ox, oy = v_.opt(CRATER[0] + 20.0, CRATER[1])
        K.cold_vapor(big, ox, oy - 140, t, 0.8, 1.0)
    return K.shot(YARD, lambda v_: light_yard(v_, siren=0.3, t=t), cx, 450.0, Z, acts=[r, d, tom], pre=pre, fx_=f)


# ================================================================== 10: LOOP — the family at the window: «RANDY, NO!»
def r_loop(t, u):
    Z = 1.3
    v = V(YARD, 636.0, 360.0, Z)
    def pre(big, v_): big[:] = K.dof(big, 6)
    m = max(0.6, mouth('family', t))
    acts = [A(C.joyce, *W(v, 380.0, 1520.0), 24.0, t=t, flip=True, expr='panic', mouth_=m, look=(-0.4, 0.0), purse=None),
            A(C.brayden, *W(v, 720.0, 2120.0), 20.0, t=t, flip=True, expr='panic', mouth_=m, look=(-0.6, 0.0), stick=False)]
    def f(big, v_):
        big[:] = (big * 0.86 + np.array((210, 220, 236)) * 0.14).astype(np.uint8)       # window glass
        big[:, 520:548] = (236, 230, 214); big[860:888, :] = (236, 230, 214)            # window mullions
        big[:, :26] = (236, 230, 214); big[:, -26:] = (236, 230, 214)
    return K.shot(YARD, light_yard, 636.0, 360.0, Z, acts=acts, pre=pre, fx_=f)


R = [r_hook, r_boom, r_crater, r_soot, r_garage, r_call, r_pros, r_truck, r_same, r_married, r_oil, r_loop]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 4, ['RANDY,', 'NO!'], hook_t=(0.10, 1.48), hook_y=300, hook_size=96,
              day=(3.60, 6.80, 'THURSDAY 9:58 AM', 'TURKEY DAY', 1650),
              stickers=[(K.st('FRY-HARD 3000', fg=(255, 214, 80), size=56), 0.20, 1.45, 760, 1240),
                        (K.st('SAME', fg=(255, 90, 60), size=96), 17.90, 19.40, 540, 560),
                        (K.st('TRENDING #1', fg=(170, 255, 90), size=58), 13.40, 15.55, 540, 560)],
              flashes=[1.50, TWIST], mosaics=[],
              cap_y={0: 1600, 1: 1600, 2: 560, 3: 1600, 4: 1600, 5: 1620, 6: 1600, 7: 1600, 8: 1600, 9: 1600, 10: 1650, 11: 1680})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
