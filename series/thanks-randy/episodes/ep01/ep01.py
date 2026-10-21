"""S01E01 «$89 TURKEY?!» (pilot; 30.8 s, twist at 16.80 s / 55 %, type: the villain is family).
HOOK: Randy screams at the Shop'n'Weep self-checkout — «EIGHTY-NINE bucks?! For a BIRD?!» TOM (the frozen turkey on the bagging shelf,
to camera): «I'm worth it.» Randy brags to cousin Brayden's livestream: «This year I'm hosting. Twenty years — never burned a turkey!» —
«You never cooked one.» The kiosk: «Unexpected item in bagging area.» He drags Tom off (CLONK), throws away his wallet, cap, a shoe —
«Unexpected item.» — «There's NOTHING there!» TWIST: he rips the hanging bag off the rack — tiny Nana Joyce sits behind it, knitting:
«I'm resting, sweetie.» — «Grandma detected. Four ninety-nine per pound.» — «No, it's fine. I'll just die here.» — she squints at the
screen: «So. When are you getting married?» — the kiosk glitches: «Total. Eighty-nine ninety-nine.» (loops into the hook scream).
Clue in the first half: her tiny orthopedic shoes dangle under the shelf, lavender curls peek over the bag, knitting clicks.
  python3 ep01.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
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

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='randy', lang='us'))
STORE, STORE_B = K.world('store'), K.world('store_b')
WS = 3.2                       # world px per sprite px on the store floor (Randy ~256 world px tall)
FLOOR = 708.0
KIO = (760.0, 706.0)           # kiosk feet
RAN = (640.0, 708.0)           # Randy at the screen
BRA = (512.0, 690.0)           # Brayden filming
BAG = (24.0, 33.0)             # kiosk sprite anchors
SEAT = 28.5                    # Joyce sits at x=28.5 of the shelf (legs dangle over its right edge)
TOMX = 19.0                    # Tom lies at the front of the shelf


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def W(v, ox, oy):
    return wpt(v, ox, oy)


def kiosk_group(v, ox, oy, s, t, screen='idle', lamp='green', alarm=0.0, bag=True, joyce=None, tom=True, tom_kw=None):
    """kiosk at output (ox, oy) (feet), s output px per sprite px; returns actors in depth order:
    kiosk back, Joyce (hidden on the shelf), the hanging bag, Tom on the front of the shelf"""
    wx, wy = W(v, ox, oy)
    acts = [A(C.kiosk, wx, wy, s, t=t, screen=screen, lamp=lamp, alarm=alarm, part='back')]
    if joyce is not None:
        jx, jy = W(v, ox + SEAT * s, oy - BAG[1] * s)
        acts.append(A(C.joyce, jx, jy, s, sit=True, t=t, **joyce))
    if bag:
        acts.append(A(C.kiosk, wx, wy, s, t=t, part='front'))
    if tom:
        tx, ty = W(v, ox + TOMX * s, oy - BAG[1] * s)
        acts.append(A(C.tom, tx, ty, s, t=t, **(tom_kw or {})))
    return acts


def joyce_hidden(t):
    return dict(expr='sweet', knit=t, look=(0.6, 0.0), purse='side')


def scene(world_, cx, cy, Z):
    """a regular shot where the sprites live in world scale: returns (view, sprite scale, kiosk feet in output px)"""
    v = V(world_, cx, cy, Z)
    s = WS * Z * 3
    ox, oy = v.opt(*KIO)
    return v, s, (ox, oy)


def screen_glow(big, x, y, col=(255, 60, 60), k=1.0, r=420):
    fx.glow(big, x, y, r, col, 0.35 * k)


# ================================================================== 0: HOOK — CU Randy screaming at the price
def r_hook(t, u):
    Z = 1.3
    v = V(STORE, 700.0, 470.0, Z)
    s = 23.0
    ko = (960.0 + 6.6 * s, 1060.0 + 52.6 * s)              # kiosk screen anchor at (960, 1060): the price glows by his face
    kio = kiosk_group(v, ko[0], ko[1], s, t, screen='price', bag=False, tom=False)[:1]
    big, a = K.cu(C.randy, t, STORE, 700.0, 470.0, Z, s, head=(420, 900), light=K.light_store, blur=4,
                  acts_after=kio, expr='shout', mouth_=max(0.5, mouth('randy', t)), tremble=1.0, look=(1.0, -0.1),
                  hand_n=(19.0, 64.0 + 2 * math.sin(t * 9)), stache='up')
    if u < 0.35: K.CK.shake(big, t, 14, 33)
    screen_glow(big, 1020, 1180, (255, 220, 120), 0.6)
    return big


# ================================================================== 1: TOM on the bagging shelf — «I'm worth it.»
def r_tom(t, u):
    Z = 1.25
    v = V(STORE_B, 620.0, 500.0, Z)
    s = 30.0 + 1.2 * u
    tx, ty = 560.0, 1290.0                                   # Tom's feet (output)
    kx, ky = tx - TOMX * s, ty + BAG[1] * s
    acts = kiosk_group(v, kx, ky, s, t, joyce=None, tom_kw=dict(expr='dead', mouth_=mouth('tom', t, 1.6), look=(-0.1, -0.1)))
    yx, yy = W(v, kx + 33.0 * s, ky - BAG[1] * s)                # clue: a lavender yarn ball peeking from behind the bag
    acts.insert(1, A(C.yarn_ball, yx, yy, s, t=t))
    def pre(big, v_): big[:] = K.dof(big, 6)
    def f(big, v_):
        K.cold_vapor(big, tx + 40, ty - 17 * s, t, 1.0, 1.4)
        K.thaw_meter(big, t, 2.55, 3.86, 'ROCK', x=900, y=640)
    return K.shot(STORE_B, K.light_store_b, 620.0, 500.0, Z, acts=acts, pre=pre, fx_=f)


# ================================================================== 2: HOST — two-shot at the kiosk, Brayden's livestream
def r_host(t, u):
    k = sm(u / 5.6)
    Z = lerp(1.28, 1.46, k)
    pan = sm((t - 7.55) / 0.6)
    cx = lerp(742.0, 700.0, k) - 96.0 * pan
    v, s, (ox, oy) = scene(STORE, cx, 560.0, Z)
    talk = speaking('randy', t)
    r = A(C.randy, *RAN, s, t=t, expr='proud' if talk else ('glare' if t > 8.0 else 'smug'), mouth_=mouth('randy', t),
          look=(0.8, 0.0) if t < 7.9 else (-0.9, 0.0), stache='up' if 4.6 < t < 7.9 else None, flip=t > 7.9,
          hand_n=(17.0, 66.0) if 5.2 < t < 7.8 else None)
    b = A(C.brayden, *BRA, s, t=t, expr='lazy' if not speaking('brayden', t) else 'dead', mouth_=mouth('brayden', t), look=(0.9, 0.0))
    acts = [b] + kiosk_group(v, ox, oy, s, t, screen='price', joyce=joyce_hidden(t)) + [r]
    def f(big, v_):
        hx, hy = aout(b, v_, 'phone') if hasattr(b, 'last') else (0, 0)
        tx, ty = v_.opt(KIO[0] + TOMX * WS, KIO[1] - (BAG[1] + 16) * WS)
        K.cold_vapor(big, tx, ty, t, 0.7, 0.9)
    return K.shot(STORE, K.light_store, cx, 560.0, Z, acts=acts, fx_=f)


# ================================================================== 3: SCAN — «Unexpected item in bagging area.»
def r_scan(t, u):
    Z = 1.3
    v = V(STORE, 760.0, 470.0, Z)
    big, a = K.cu(C.randy, t, STORE, 760.0, 470.0, Z, 21.0 + 0.6 * u, head=(300, 1500), light=lambda v_: K.light_store(v_, 1.0), blur=5,
                  expr='stunned' if t < 10.8 else 'angry', mouth_=0.0, look=(0.7, 0.9), hand_n=(18.0, 58.0))
    K.alarm_tint(big, t, 0.8)
    scr = K.screen_ui('alarm', t, 900, 640)
    sc = 0.92 + 0.04 * sm(u / 2.5)
    from PIL import Image
    img = np.array(Image.fromarray(scr).resize((int(scr.shape[1] * sc), int(scr.shape[0] * sc)), Image.NEAREST))
    x0 = (OUT_W - img.shape[1]) // 2 + 30
    O.overlay(big, img, x0, 330, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, 330, x0 + img.shape[1], 330 + img.shape[0]))
    return big


# ================================================================== 4: LIFT — Tom off the shelf (CLONK), then wallet, cap, a shoe fly
def r_lift(t, u):
    Z = 1.18
    v, s, (ox, oy) = scene(STORE, 742.0, 520.0, Z)
    lifting = t < 12.95
    k = sm((t - 12.35) / 0.55)
    tom_on_shelf = t < 12.35
    sw = s / (3 * Z)                                           # = WS
    if lifting:
        hand = (lerp(18.0, 24.0, k), lerp(46.0, 58.0, k))
        r = A(C.randy, RAN[0] + 30.0, RAN[1], s, t=t, expr='strain', mouth_=0.4, look=(1.0, 0.2), hand_n=hand, hand_f=(hand[0] - 4.0, hand[1] - 2.0),
              lean=0.4)
    else:
        throw = (t - 13.6) % 0.45 if t > 13.6 else 0.0
        r = A(C.randy, RAN[0] + 30.0, RAN[1], s, t=t, expr='angry' if t < 13.6 else 'losing', mouth_=0.3 if t > 13.6 else 0.0, look=(1.0, 0.1),
              hand_n=(16.0 + 6 * math.sin(throw * 14), 60.0 if t > 13.6 else 40.0), mitt=t < 14.12, shoe_off=t > 14.5, tremble=0.6 if t > 13.6 else 0.0)
    acts = kiosk_group(v, ox, oy, s, t, screen='alarm', lamp='red', alarm=1.0, joyce=joyce_hidden(t), tom=tom_on_shelf)
    acts.append(r)
    if not tom_on_shelf:
        rx, ry = RAN[0] + 30.0, RAN[1]
        if lifting:                                            # Tom in his arms
            hx = rx + (lerp(18.0, 24.0, k) + 2.0) * sw; hy = ry - (lerp(46.0, 58.0, k) - 8.0) * sw
            acts.append(A(C.tom, hx, hy, s, t=t, expr='dead', rot=-12.0 * k))
        else:                                                  # dropped on the floor at his feet
            fall = sm((t - 12.95) / 0.12)
            acts.insert(len(acts) - 1, A(C.tom, rx - 20.0 * sw, lerp(ry - 40.0 * sw, FLOOR, fall), s, t=t, expr='dead', flip=True))
    items = [('wallet', 13.75, C.wallet, (-1, 0.0)), ('mitt', 14.12, C.turkey_mitt, (1, 0.0)), ('shoe', 14.55, C.shoe_prop, (-1, 0.0))]
    for name, t0, fn, (dirx, _) in items:
        if t >= t0:
            q = min(1.0, (t - t0) / 0.5)
            x0, y0 = RAN[0] + 30.0 + 16.0 * WS, RAN[1] - 60.0 * WS
            x = x0 + dirx * 160.0 * q + (40.0 if dirx > 0 else -260.0) * q
            y = y0 + (FLOOR - 4 - y0) * q * q - 120.0 * math.sin(math.pi * q)
            acts.append(A(lambda sp, h=(0.0, 0.0), fn=fn, **kw: fn(sp, h), x, y, s, rot=720 * q * dirx))
    def f(big, v_):
        if 12.95 <= t < 13.15: K.CK.shake(big, t, 18, 40)
        K.alarm_tint(big, t, 0.6)
    return K.shot(STORE, lambda v_: K.light_store(v_, 1.0), 742.0, 520.0, Z, acts=acts, fx_=f)


# ================================================================== 5: NOTHING — CU Randy losing it
def r_nothing(t, u):
    big, a = K.cu(C.randy, t, STORE, 760.0, 470.0, 1.35, 24.0 + 1.2 * u, head=(520, 960), light=lambda v_: K.light_store(v_, 1.0), blur=5,
                  expr='losing', mouth_=max(0.4, mouth('randy', t)), tremble=1.0, sweat=1.0, look=(-0.3, 0.4), shoe_off=True, mitt=False,
                  hand_n=(20.0 + 3 * math.sin(t * 20), 70.0), hand_f=(-14.0, 68.0))
    K.alarm_tint(big, t, 0.7)
    return big


# ================================================================== 6: TWIST — he rips the bag away: Nana knitting
def r_twist(t, u):
    Z = 1.5
    cx = 858.0 - 16.0 * sm(u / 2.0)
    v, s, (ox, oy) = scene(STORE, cx, 500.0, Z)
    ripped = t >= TWIST + 0.02
    acts = kiosk_group(v, ox, oy, s, t, screen='alarm', lamp='red', alarm=1.0, bag=not ripped, tom=False,
                       joyce=dict(expr='sweet' if not speaking('joyce', t) else 'smile', mouth_=mouth('joyce', t), knit=t if t > 17.6 else None,
                                  look=(0.7, 0.1), purse='side'))
    bx = KIO[0] + (SEAT + 26.0) * WS
    r = A(C.randy, bx, FLOOR, s, t=t, flip=True, expr='shock', mouth_=0.7, look=(0.9, -0.2), shoe_off=True, mitt=False,
          hand_n=(17.0 + 3 * sm(u / 0.2), 64.0), prop_n=(lambda sp, h: C.bag_prop(sp, (h[0], h[1] + 3.0), held=True)) if ripped else None)
    acts.append(r)
    def f(big, v_):
        if u < 0.25: K.CK.shake(big, t, 16, 40)
        K.alarm_tint(big, t, 0.4)
    return K.shot(STORE, lambda v_: K.light_store(v_, 1.0), cx, 500.0, Z, acts=acts, fx_=f)


# ================================================================== 7: WEIGH — «Grandma detected. Four ninety-nine per pound.»
def r_weigh(t, u):
    Z = 1.4
    v = V(STORE, 860.0, 520.0, Z)
    s = 24.0
    jx, jy = 600.0, 1450.0 + 21.9 * 24.0          # Joyce's head ends up at y ~1450, under the screen
    kx, ky = jx - SEAT * s, jy + BAG[1] * s
    acts = kiosk_group(v, kx, ky, s, t, screen='alarm', lamp='red', alarm=1.0, bag=False, tom=False,
                       joyce=dict(expr='sweet', knit=t, look=(0.4, 0.4), purse='side'))
    def pre(big, v_): big[:] = K.dof(big, 6)
    big = K.shot(STORE, lambda v_: K.light_store(v_, 1.0), 860.0, 520.0, Z, acts=acts, pre=pre)
    K.alarm_tint(big, t, 0.5)
    scr = K.screen_ui('grandma', t, 820, 600)
    x0 = (OUT_W - scr.shape[1]) // 2
    O.overlay(big, scr, x0, 250, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, 250, x0 + scr.shape[1], 250 + scr.shape[0]))
    return big


# ================================================================== 8: FINE — «No, it's fine. I'll just die here.»
def r_fine(t, u):
    Z = 1.42
    v, s, (ox, oy) = scene(STORE, 840.0 + 10.0 * sm(u / 3.6), 505.0, Z)
    die = sm((t - 24.55) / 0.45)
    acts = kiosk_group(v, ox, oy, s, t, screen='alarm', lamp='red', alarm=1.0, bag=False, tom=False,
                       joyce=dict(expr='fine' if die < 0.5 else 'sweet', mouth_=mouth('joyce', t), knit=t if die < 0.5 else None,
                                  look=(0.8, 0.0), purse='side'))
    jo = acts[1]
    jo.rot, jo.pivot = 34.0 * die, (-6.0, 0.0)
    bx = KIO[0] + (SEAT + 26.0) * WS
    r = A(C.randy, bx, FLOOR, s, t=t, flip=True, expr='plead', mouth_=0.0, look=(0.9, 0.1), shoe_off=True, mitt=False,
          hand_n=(12.0, 56.0), hand_f=(9.0, 54.0), prop_f=lambda sp, h: C.bag_prop(sp, (h[0], h[1] + 3.0), held=True))
    acts.append(r)
    return K.shot(STORE, lambda v_: K.light_store(v_, 0.6), 840.0 + 10.0 * sm(u / 3.6), 505.0, Z, acts=acts)


# ================================================================== 9: MARRIED — CU Nana squints at the kiosk screen
def r_married(t, u):
    Z = 1.35
    v = V(STORE_B, 640.0, 480.0, Z)
    s = 32.0 + 1.4 * u
    hx, hy = 680.0, 1000.0
    def pre(big, v_): big[:] = K.dof(big, 7)
    # Joyce sitting, facing LEFT to the screen (flip)
    a = A(C.joyce, *W(v, hx, hy), s, pin='head', t=t, flip=True, sit=True, expr='nosy', mouth_=mouth('joyce', t), squint=sm((t - 25.7) / 0.6),
          look=(0.9, -0.1), purse=None, knit=None, hand_n=(9.6, 7.0), hand_f=(6.0, 6.0))
    kx, ky = 150.0 + 6.6 * s, 1020.0 + 52.6 * s            # kiosk feet so that its screen sits at the left edge (150, 1020)
    kio = A(C.kiosk, *W(v, kx, ky), s, t=t, screen='alarm', lamp='red', alarm=1.0, part='back')
    big = K.shot(STORE_B, lambda v_: K.light_store_b(v_, 0.8), 640.0, 480.0, Z, acts=[kio, a], pre=pre)
    K.alarm_tint(big, t, 0.35)
    return big


# ================================================================== 10: GLITCH — the kiosk breaks: «Total. Eighty-nine ninety-nine.»
def r_glitch(t, u):
    Z = 1.3
    big, a = K.cu(C.randy, t, STORE, 760.0, 470.0, Z, 20.0, head=(820, 1510), light=K.light_store, blur=5,
                  expr='stunned', mouth_=0.15, look=(-0.9, 0.6), shoe_off=True, flip=True, mitt=False)
    mode = 'glitch' if t < 29.4 else 'price'
    scr = K.screen_ui(mode, t, 900, 640)
    x0 = (OUT_W - scr.shape[1]) // 2 - 20
    O.overlay(big, scr, x0, 520, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, 520, x0 + scr.shape[1], 520 + scr.shape[0]))
    if t < 29.4: K.glitch(big, t, 0.6 + 0.4 * math.sin(t * 9) ** 2)
    return big


R = [r_hook, r_tom, r_host, r_scan, r_lift, r_nothing, r_twist, r_weigh, r_fine, r_married, r_glitch]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 1, ['$89 TURKEY?!'], hook_t=(0.10, 2.30), hook_y=330, hook_size=78,
              day=(2.50, 5.20, 'MONDAY', '3 DAYS TO TURKEY', 1650),
              stickers=[(K.st('TURKEYS COOKED: 0', fg=(170, 255, 90), size=52), 8.05, 9.50, 560, 560),
                        (K.st('UNEXPECTED GRANDMA!', fg=(255, 214, 80), size=54), 17.00, 18.90, 540, 330)],
              flashes=[TWIST, 12.98, 28.32], mosaics=[28.32],
              cap_y={0: 1580, 1: 560, 2: 1240, 3: 1150, 4: 1560, 5: 1580, 6: 1280, 7: 1060, 8: 1600, 9: 1600, 10: 1320})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
