"""S01E03 «STILL FROZEN?!» (33.1 s, twist at 17.72 s / 54 %, type: the hunter asks for help — the expert needs the loser).
Wednesday 3:07 AM, Randy's kitchen. HOOK: he blasts a hair dryer at Tom in the sink — «It's STILL FROZEN?!» — Tom: «Twenty-two pounds,
pal. I'm a glacier.» — «Okay. Calling the experts.» Hold screen of the Butterbutt Turkey Talk-Line: «Wait time: four hours. Our
experts are ALSO thawing.» (clue) — «4 HOURS LATER» he sleeps on the turkey. SPLIT: «Butterbutt Talk-Line, this is Carol!» — «It's still
frozen! Twenty-two pounds!» — «Oh. Honey.» TWIST: the call centre — every expert is blasting a hair dryer at her own frozen turkey:
«Mine's frozen too. Can I come to yours?» The back door: Carol and the operators with their turkeys — «We brought dip!» — the kitchen
fills with dryers, Brayden films: «Bro. This is a startup.» — Nana in curlers: «So. Which one of you is getting married?» — Tom among
ten frozen turkeys: «Great. Now it's a support group.» — Randy clicks the dryer on (the sound of the first frame).
  python3 ep03.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props.randykit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep03', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='randy', lang='us'))
KIT, KIT_B, CC = K.world('kitchen'), K.world('kitchen_b'), K.world('callcenter')
WS = 4.6                       # world px per sprite px at the counter
FLOOR = 660.0
SINK = (600.0, 398.0)          # Tom lies in the sink (counter top line)
RAN = (430.0, FLOOR)
DOOR_X = 1160.0
CC_FLOOR = 690.0


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def W(v, ox, oy):
    return wpt(v, ox, oy)


def light_kit(v, k=1.0):
    keys = [(600, 330, 520, (255, 210, 130), 0.45), (700, 200, 600, (120, 160, 255), 0.25), (900, 120, 500, (255, 220, 150), 0.30)]
    return Light(amb=(0.86, 0.86, 0.98), keys=[(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in keys], rim=(1, -0.3, (150, 180, 255), 0.30),
                 grad=(0.98, 0.88))


def light_cc(v):
    keys = [(640, 60, 900, (230, 240, 255), 0.30)]
    return Light(amb=(0.98, 1.0, 1.02), keys=[(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in keys], rim=(-1, -0.3, (200, 220, 255), 0.25),
                 grad=(1.02, 0.94))


def counter_front(big, v, y_world=SINK[1], x0=480.0, x1=720.0):
    """the counter front occludes the lower half of what lies in the sink: paste the background back below the counter line"""
    bg = v.bg()
    ox0, oy = v.opt(x0, y_world); ox1, _ = v.opt(x1, y_world)
    X0, X1, Y0 = int(max(0, ox0)), int(min(OUT_W, ox1)), int(max(0, oy))
    if X0 < X1 and Y0 < OUT_H: big[Y0:, X0:X1] = bg[Y0:, X0:X1]


def dryer_wind(big, x, y, t, dirx=1.0, k=1.0, n=10):
    """hot-air streaks + ice chips flying from the nozzle (output px)"""
    rng = np.random.default_rng(int(t * 24))
    for i in range(n):
        ph = (t * 3.0 + i / n) % 1.0
        px = x + dirx * ph * 360; py = y + (rng.random() - 0.5) * 80 * ph
        big[int(max(0, py)):int(max(0, py)) + 6, int(min(px, px + dirx * 40)):int(max(px, px + dirx * 40))] = (255, 236, 200)
    for i in range(int(6 * k)):
        ph = (t * 2.2 + i / 6) % 1.0
        px = x + dirx * (300 + 200 * ph); py = y - 120 * ph + 300 * ph * ph
        q = 10
        if 0 <= px < OUT_W - q and 0 <= py < OUT_H - q: big[int(py):int(py) + q, int(px):int(px) + q] = (230, 246, 255)


# ================================================================== 0: HOOK — the hair dryer at Tom in the sink
def r_hook(t, u):
    Z = 1.35
    v = V(KIT, 560.0, 330.0, Z)
    s = 22.0
    tom = A(C.tom, *W(v, 930.0, 1450.0), 26.0, t=t, expr='dead', look=(-0.6, 0.2))
    big, a = K.cu(C.randy, t, KIT, 560.0, 330.0, Z, s, head=(330, 900), light=light_kit, blur=4, acts_after=[tom],
                  expr='shout', mouth_=max(0.5, mouth('randy', t)), tremble=1.0, sweat=1.0, look=(1.0, 0.2), mitt=False,
                  hand_n=(20.0, 50.0), prop_n=lambda sp, h: C.hair_dryer(sp, h, t=t))
    nx, ny = aout(a, v, 'hand')
    dryer_wind(big, nx + 200, ny - 40, t)
    K.cold_vapor(big, 960, 1200, t, 1.0, 1.2)
    if u < 0.3: K.CK.shake(big, t, 12, 33)
    return big


# ================================================================== 1: TOM in the sink — «Twenty-two pounds, pal. I'm a glacier.»
def r_tom(t, u):
    Z = 1.4
    v = V(KIT, 600.0, 330.0, Z)
    s = 30.0 + 1.0 * u
    tx, ty = 560.0, 1300.0
    tom = A(C.tom, *W(v, tx, ty), s, t=t, expr='dead', mouth_=mouth('tom', t, 1.6), look=(-0.1, -0.1))
    def pre(big, v_): big[:] = K.dof(big, 5)
    def f(big, v_):
        dryer_wind(big, -60, ty - 13 * s, t, 1.0, 0.8, n=8)
        K.cold_vapor(big, tx + 40, ty - 17 * s, t, 1.0, 1.4)
        K.thaw_meter(big, t, 3.10, 4.80, 'GLACIER', x=930, y=600)
    return K.shot(KIT, light_kit, 600.0, 330.0, Z, acts=[tom], pre=pre, fx_=f)


# ================================================================== 2: DIAL — «Okay. Calling the experts.»
def r_dial(t, u):
    Z = lerp(1.15, 1.25, sm(u / 1.9))
    cx = 520.0
    v = V(KIT, cx, 420.0, Z)
    s = WS * Z * 3
    r = A(C.randy, *RAN, s, t=t, expr='glare' if not speaking('randy', t) else 'angry', mouth_=mouth('randy', t), look=(0.6, 0.3),
          mitt=False, hand_n=(15.0, 56.0), prop_n=lambda sp, h: C.cell(sp, h), hand_f=(10.0, 42.0), sweat=0.5)
    tom = A(C.tom, SINK[0] - 10.0, SINK[1] + 40.0, s * 0.92, t=t, expr='dead')
    def f(big, v_):
        counter_front(big, v_)
        r(big, v_, light_kit(v_))
    return K.shot(KIT, light_kit, cx, 420.0, Z, acts=[tom], fx_=f)


# ================================================================== 3: HOLD — the Talk-Line hold screen
def r_hold(t, u):
    Z = 1.2
    def pre(big, v_): big[:] = K.dof(big, 9)
    big = K.shot(KIT_B, light_kit, 600.0, 360.0, Z, pre=pre)
    secs = int(4 * 3600 - (t - 6.7) * 37)
    timer = f'{secs // 3600}:{(secs // 60) % 60:02d}:{secs % 60:02d}'
    ph = K.phone_ui(t, status='ON HOLD', timer=timer)
    x0 = (OUT_W - ph.shape[1]) // 2
    O.overlay(big, ph, x0, 300, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, 300, x0 + ph.shape[1], 300 + ph.shape[0]))
    return big


# ================================================================== 4: LATER — asleep on the turkey
def r_later(t, u):
    Z = 1.25
    cx = 560.0
    v = V(KIT, cx, 420.0, Z)
    s = WS * Z * 3
    tom = A(C.tom, SINK[0] - 10.0, SINK[1] + 40.0, s * 0.92, t=t, expr='dead', look=(-0.8, 0.4))
    r = A(C.randy, RAN[0] + 60.0, FLOOR, s, t=t, expr='content', mouth_=0.2, look=(0.0, 0.0), mitt=False, lean=2.2,
          hand_n=(18.0, 66.0), prop_n=lambda sp, h: C.cell(sp, h, glow=False), hand_f=(16.0, 50.0))
    def f(big, v_):
        counter_front(big, v_)
        r(big, v_, light_kit(v_))
        hx, hy = aout(r, v_, 'mouth')
        for q in range(3):
            ph = (t * 1.2 + q / 3) % 1.0
            O.overlay(big, K.st('Z', fg=(200, 220, 255), size=40 + int(30 * ph)), int(hx + 60 + 80 * ph), int(hy - 120 - 200 * ph), 1 - ph)
    return K.shot(KIT, light_kit, cx, 420.0, Z, acts=[tom], fx_=f)


# ================================================================== 5: SPLIT — Randy (kitchen) | Carol (call centre)
def _randy_cu(t, expr, look=(1.0, 0.0), **kw):
    big, a = K.cu(C.randy, t, KIT, 600.0, 360.0, 1.3, 20.0, head=(540, 980), light=light_kit, blur=5, expr=expr,
                  mouth_=mouth('randy', t), look=look, mitt=False, hand_n=(15.0, 56.0), prop_n=lambda sp, h: C.cell(sp, h), **kw)
    return big


def _carol_cu(t, expr, panic=0.0, sz=22.0, head=(540, 980), look=(-0.8, 0.0)):
    big, a = K.cu(C.carol, t, CC, 1000.0, 560.0, 1.3, sz, head=head, light=light_cc, blur=7, flip=True, expr=expr, mouth_=mouth('carol', t),
                  look=look, panic=panic, hand_n=(12.0, 40.0), hand_f=(-8.0, 22.0))
    return big


def r_split(t, u):
    awake = t >= 13.35
    left = _randy_cu(t, 'losing' if awake else 'content', sweat=1.0 if awake else 0.0, look=(1.0, 0.0) if awake else (0.0, 0.0))
    if not awake:
        hx = 540
        for q in range(2):
            ph = (t * 1.2 + q / 2) % 1.0
            O.overlay(left, K.st('Z', fg=(200, 220, 255), size=40 + int(30 * ph)), int(hx + 120 + 60 * ph), int(700 - 200 * ph), 1 - ph)
    right = _carol_cu(t, 'hype' if t < 13.4 else 'nervous', panic=0.0)
    big = K.split(left, right)
    if ST.LOG[0] is not None: ST.log('card', bbox=(OUT_W // 2 - 6, 0, OUT_W // 2 + 6, OUT_H))
    return big


# ================================================================== 6: HONEY — Carol CU: «Oh. Honey.»
def r_honey(t, u):
    return _carol_cu(t, 'sad', panic=0.3 * sm(u / 1.5), sz=24.0 + 1.2 * u, head=(560, 960), look=(-0.4, 0.2))


# ================================================================== 7: TWIST — the call centre: every expert blasts her own frozen turkey
def r_twist(t, u):
    Z = 1.05
    cx, cy = 640.0, 430.0
    v = V(CC, cx, cy, Z)
    sw = 3.0
    s = sw * Z * 3
    acts = []
    xs = [470.0, 600.0, 730.0]
    for i, x in enumerate(xs):
        op = C.OPERATORS[i]
        acts.append(A(C.carol, x, CC_FLOOR - 40.0, s, t=t, expr='panic', panic=1.0, hand_n=(15.0, 24.0), mouth_=0.6 * abs(math.sin(t * 8 + i)),
                      prop_n=lambda sp, h: C.hair_dryer(sp, h), **op))
        acts.append(A(C.tom, x + 44.0, CC_FLOOR - 36.0, s, t=t, face=False))
    car = A(C.carol, 620.0, CC_FLOOR + 30.0, s * 1.5, t=t, flip=True, expr='panic', panic=1.0, mouth_=mouth('carol', t),
            look=(-0.6, 0.0), hand_n=(10.0, 40.0), hand_f=(-6.0, 36.0))
    acts.append(car)
    def f(big, v_):
        for i, x in enumerate(xs):
            ox, oy = v_.opt(x + 17.0 * sw, CC_FLOOR - 40.0 - 25.0 * sw)
            dryer_wind(big, ox, oy, t + i * 0.3, 1.0, 0.6, n=6)
            K.puff(big, ox + 120, oy - 200 - 80 * ((t + i) % 1.0), 40, 0.25, (200, 200, 210))
        if u < 0.3: K.CK.shake(big, t, 14, 40)
    return K.shot(CC, light_cc, cx, cy, Z, acts=acts, fx_=f)


# ================================================================== 8: DOOR — Carol and the operators at the back door: «We brought dip!»
def r_door(t, u):
    Z = 1.2
    cx = 1020.0
    v = V(KIT, cx, 420.0, Z)
    s = WS * Z * 3
    enter = sm(u / 0.8)
    acts = []
    for i, dx in enumerate((-150.0, -60.0, 60.0, 150.0)):
        x = DOOR_X + dx * enter
        acts.append(A(C.carol, x, FLOOR - 30.0 + 10.0 * (i % 2), s * 0.92, t=t, flip=True, expr='hype', hand_n=(13.0, 26.0),
                      **C.OPERATORS[i]))
        acts.append(A(C.tom, x - 40.0, FLOOR - 30.0 - 22.0 * WS * 0.92 + 10.0 * (i % 2), s * 0.62, t=t, face=False))
    acts.append(A(C.carol, DOOR_X - 230.0 * enter, FLOOR + 10.0, s, t=t, flip=True, expr='smile' if not speaking('carol2', t) else 'cheer',
                  mouth_=mouth('carol2', t), look=(-0.8, 0.0), hand_n=(13.0, 30.0), prop_n=lambda sp, h: C.dip_bowl(sp, h),
                  hand_f=(-6.0, 30.0)))
    r = A(C.randy, 760.0, FLOOR + 20.0, s, t=t, expr='shock', mouth_=0.4, look=(1.0, 0.0), mitt=False, sweat=0.6,
          hand_n=(14.0, 48.0), prop_n=lambda sp, h: C.cell(sp, h))
    acts.append(r)
    return K.shot(KIT, light_kit, cx, 420.0, Z, acts=acts)


# ================================================================== 9: GROUP — the kitchen full of dryers: «Bro. This is a startup.»
TURKEYS = [380.0, 470.0, 560.0, 650.0, 740.0, 830.0]


def r_group(t, u):
    Z = 1.0 + 0.08 * sm(u / 2.8)
    cx = 600.0
    v = V(KIT, cx, 400.0, Z)
    s = WS * Z * 3 * 0.82
    acts = [A(C.tom, x, 404.0, s * 0.62, t=t, face=(i == 2), expr='dead', look=(-0.4, 0.2)) for i, x in enumerate(TURKEYS)]
    for i, x in enumerate((500.0, 760.0, 980.0)):
        acts.append(A(C.carol, x, FLOOR + 30.0, s, t=t, expr='hype', hand_n=(15.0, 30.0), prop_n=lambda sp, h: C.hair_dryer(sp, h), **C.OPERATORS[i + 1]))
    acts.append(A(C.randy, 640.0, FLOOR + 40.0, s * 1.05, t=t, expr='stunned', mouth_=0.1, mitt=False, look=(0.0, 0.0),
                  hand_n=(18.0, 52.0), prop_n=lambda sp, h: C.hair_dryer(sp, h), hand_f=(-16.0, 52.0),
                  prop_f=lambda sp, h: C.hair_dryer(sp, h)))
    b = A(C.brayden, 450.0, FLOOR + 50.0, s * 1.05, t=t, expr='hype' if speaking('brayden', t) else 'lazy', mouth_=mouth('brayden', t),
          look=(0.9, 0.0))
    acts.append(b)
    def f(big, v_):
        for x in (500.0, 760.0, 980.0):
            ox, oy = v_.opt(x + 14.0 * s / (3 * v_.Z), FLOOR + 30.0 - 30.0 * s / (3 * v_.Z))
            dryer_wind(big, ox, oy, t, 1.0, 0.4, n=5)
        for x in TURKEYS:
            ox, oy = v_.opt(x, 404.0 - 60.0)
            K.cold_vapor(big, ox, oy, t + x, 0.6, 0.6, w=60)
    return K.shot(KIT, light_kit, cx, 400.0, Z, acts=acts, fx_=f)


# ================================================================== 10: JOYCE — curlers at the door: «Which one of you is getting married?»
def r_joyce(t, u):
    big, a = K.cu(C.joyce, t, KIT_B, 1050.0, 360.0, 1.35, 26.0 + 1.0 * u, head=(560, 960), light=light_kit, blur=4, flip=True,
                  robe=True, expr='nosy', mouth_=mouth('joyce', t), squint=0.4, look=(-0.8, 0.0), purse=None, hand_n=(7.0, 24.0))
    return big


# ================================================================== 11: SUPPORT — Tom among the frozen turkeys: «Now it's a support group.»
def r_support(t, u):
    Z = 1.45
    v = V(KIT, 560.0, 330.0, Z)
    s = 20.0
    acts = []
    for i, ox in enumerate((90.0, 330.0, 790.0, 1010.0)):
        acts.append(A(C.tom, *W(v, ox, 1280.0 + 30.0 * (i % 2)), s, t=t, face=False))
    tom = A(C.tom, *W(v, 560.0, 1330.0), s * 1.2, t=t, expr='dead', mouth_=mouth('tom', t, 1.6), look=(0.0, -0.3))
    acts.append(tom)
    def pre(big, v_): big[:] = K.dof(big, 5)
    def f(big, v_):
        for ox in (90.0, 330.0, 560.0, 790.0, 1010.0):
            K.cold_vapor(big, ox + 20, 1080, t + ox, 0.7, 0.8, w=80)
    return K.shot(KIT, light_kit, 560.0, 330.0, Z, acts=acts, pre=pre, fx_=f)


R = [r_hook, r_tom, r_dial, r_hold, r_later, r_split, r_honey, r_twist, r_door, r_group, r_joyce, r_support]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 3, ['STILL', 'FROZEN?!'], hook_t=(0.10, 1.60), hook_y=300, hook_size=86,
              day=(1.70, 4.70, 'WEDNESDAY 3:07 AM', 'TURKEY DAY: TOMORROW', 1640),
              stickers=[(K.st('4 HOURS LATER', fg=(255, 214, 80), size=64), 10.40, 11.00, 540, 560),
                        (K.st('EXPERTS: ALSO FROZEN', fg=(150, 220, 255), size=52), 17.85, 20.45, 540, 1000),
                        (K.st('STARTUP!', fg=(170, 255, 90), size=70), 23.40, 25.55, 300, 560)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1580, 1: 560, 2: 1600, 3: 1560, 4: 1600, 5: 1580, 6: 1600, 7: 1180, 8: 1620, 9: 1600, 10: 1600, 11: 560})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
