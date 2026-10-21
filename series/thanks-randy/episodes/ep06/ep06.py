"""S01E06 «$199 TV?!» (season finale; 32.5 s, twist at 16.72 s / 51 %, type: someone else took the prize).
Black Friday 4:59 AM, Best Bye. HOOK: Randy's face pressed to the frosty glass door, a pyramid of «65" $199» boxes behind it —
«One ninety-nine for a TV?!» The line: grannies in camping chairs under «NO CAMPING», a tent with the chair «JOYCE · SINCE TUE» (clue,
knitting clicks from the tent); Brayden sells spots: «Spots in line. Forty bucks. It's a startup.» The clock 4:59: Randy cracks his
knuckles in the turkey mitt — «Twenty years of Black Fridays. Never lost!» — «You never got up.» 5:00 — the doors, a cartoon stampede
(grannies on walkers with speed lines, flying shoes). Slow-mo: Randy grabs the last real box off the «DISPLAY ONLY» pyramid — «MINE!»
Kyle at the register: «That one's on hold.» — «For WHO?!» TWIST: the box flap opens, tiny Nana inside, knitting: «Me, sweetie. Since
Tuesday.» — «No, it's fine. Carry me to the car.» Self-checkout — the same Scan-Dee: «Unexpected item in bagging area.» — on the bagging
shelf: Tom (the first insert of E01 — the season loop): «Miss me?» — «Total: one ninety-nine. Plus grandma.» — Randy, to himself:
«…Thanks, Randy.» Snow, «SEASON 2: RANDY HOSTS CHRISTMAS», THAW-O-METER «CHRISTMAS?» — Tom: «Still frozen.»
  python3 ep06.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
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

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='randy', lang='us'))
OUT, IN, IN_B = K.world('bbout'), K.world('bbin'), K.world('bbin_b')
WS_OUT = 2.35                  # world px per sprite px on the Best Bye sidewalk (door 225 px = 2.1 m)
WS_IN = 2.6                    # inside the store
SIDEWALK = 628.0
FLOOR_IN = 640.0
BAG = (24.0, 33.0)             # kiosk bagging-shelf anchor
TOMX = 19.0
BOX_TOP = 36.0                 # tv_box top (sprite px)
JOY_IN_BOX = 13.0              # Nana's seat sits this far under the box top


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def W(v, ox, oy):
    return wpt(v, ox, oy)


def light_out(v):
    keys = [(600, 420, 420, (255, 196, 120), 0.45), (40, 270, 200, (255, 210, 140), 0.30), (1210, 150, 260, (255, 220, 160), 0.25)]
    return Light(amb=(0.86, 0.90, 1.06), keys=[(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in keys], rim=(1, -0.3, (255, 190, 120), 0.30),
                 grad=(0.95, 1.02))


def light_in(v):
    keys = [(580, 40, 900, (230, 240, 255), 0.30), (1000, 380, 380, (150, 200, 255), 0.25)]
    return Light(amb=(1.0, 1.0, 1.04), keys=[(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in keys], rim=(-1, -0.3, (170, 210, 255), 0.30),
                 grad=(1.04, 0.95))


_FROST = {}


def frost(big, side='right', k=1.0):
    """frost on the glass the camera looks through: blocky white crystals growing in from an edge"""
    if side not in _FROST:
        r = np.random.default_rng(7)
        q = 24
        gh, gw = OUT_H // q + 1, OUT_W // q + 1
        yy, xx = np.mgrid[0:gh, 0:gw].astype(np.float32)
        d = (gw - 1 - xx) / gw if side == 'right' else xx / gw
        d = np.minimum(d, yy / gh * 1.6)
        a = np.clip(1.0 - d * 4.2 + r.random((gh, gw)) * 0.55 - 0.2, 0, 1) * 0.72
        _FROST[side] = np.kron(a, np.ones((q, q), np.float32))[:OUT_H, :OUT_W, None]
    a = _FROST[side] * k
    big[:] = (big * (1 - a) + np.array((232, 244, 255), np.float32) * a).astype(np.uint8)


def breath(big, x, y, t, k=1.0, scale=1.0):
    for i in range(3):
        ph = (t / 1.1 + i / 3) % 1.0
        K.puff(big, x + 90 * ph * scale, y - 40 * ph * scale, (20 + 50 * ph) * scale, 0.35 * k * (1 - ph), (236, 244, 255), q=max(6, int(8 * scale)))


def flying_shoe(sp, t=0.0):
    C.shoe_prop(sp, (0.0, 0.0))


def box_with_nana(acts, wx, wy, s, t, flap=1.0, joyce=None, scale_world=None):
    """the 65" box standing at world (wx, wy) with Nana sitting inside (only the perm + face + needles above the flap)"""
    sw = scale_world
    if joyce is not None:
        acts.append(A(C.joyce, wx, wy - (BOX_TOP - JOY_IN_BOX) * sw, s, sit=True, t=t, **joyce))
    acts.append(A(C.tv_box, wx, wy, s, t=t, flap=flap))
    return acts


def clock_card(big, t, y=210):
    """the store's LED door clock: 4:59 → 5:00"""
    on = t >= 10.38
    txt = '5:00' if on else '4:59'
    f = O.pfont(120)
    w = int(f.getlength('4:59')) + 90; h = 190
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=(16, 14, 20, 235), outline=(255, 186, 60, 255), width=6)
    blink = on and int(t * 8) % 2 == 0
    col = (255, 60, 60) if not blink else (255, 230, 120)
    d.text((45, 22), txt, font=f, fill=col)
    O.overlay(big, np.array(im), (OUT_W - w) // 2, y, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=((OUT_W - w) // 2, y, (OUT_W + w) // 2, y + h))


def bb_screen(t, w=900, h=640, step=0):
    """Best Bye self-checkout — the same Scan-Dee software (header still says SHOP'N'WEEP under the sticker)"""
    im = Image.new('RGB', (w, h), (20, 34, 58)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, 70], fill=(30, 70, 170))
    fh = O.pfont(30)
    d.text((24, 20), 'BEST BYE  SELF-CHECKOUT', font=fh, fill=(255, 214, 60))
    f = O.pfont(34); fb = O.pfont(56); fs = O.pfont(26)
    d.text((40, 110), 'TV 65" (LAST ONE)', font=f, fill=(255, 255, 255))
    d.text((w - 40 - f.getlength('$199.00'), 110), '$199.00', font=f, fill=(255, 255, 255))
    if step >= 1:
        d.text((40, 170), 'GRANDMA (ON HOLD)', font=f, fill=(255, 150, 150))
        d.text((w - 40 - f.getlength('INCL.'), 170), 'INCL.', font=f, fill=(255, 150, 150))
    d.line([(40, 236), (w - 40, 236)], fill=(90, 110, 150), width=4)
    d.text((40, 270), 'TOTAL', font=fb, fill=(255, 230, 80))
    d.text((w - 40 - fb.getlength('$199.00'), 270), '$199.00', font=fb, fill=(255, 230, 80))
    if step >= 1:
        fg = O.pfont(52)
        d.text((w - 40 - fg.getlength('+ GRANDMA'), 345), '+ GRANDMA', font=fg, fill=(255, 120, 120))
    d.text((40, 430), 'NO RETURNS ON GRANDMA', font=fs, fill=(170, 190, 220))
    d.rounded_rectangle([40, h - 150, w - 40, h - 40], 20, fill=(40, 160, 90))
    d.text(((w - f.getlength('PAY NOW')) / 2, h - 112), 'PAY NOW', font=f, fill=(255, 255, 255))
    out = np.zeros((h + 60, w + 60, 4), np.uint8)
    out[..., :3] = (44, 48, 58); out[..., 3] = 255
    out[:8] = (52, 26, 48, 255); out[-8:] = (52, 26, 48, 255); out[:, :8] = (52, 26, 48, 255); out[:, -8:] = (52, 26, 48, 255)
    out[30:30 + h, 30:30 + w, :3] = np.array(im)
    return out


def snow(big, t, n=90, seed=3):
    r = np.random.default_rng(seed)
    P_ = r.random((n, 3))
    for u, w, ph in P_:
        y = ((w + t * (0.08 + 0.06 * ph)) % 1.0) * OUT_H
        x = (u * OUT_W + math.sin(t * 1.2 + ph * 9) * 40) % OUT_W
        q = 8 + int(ph * 10)
        big[int(y):int(y) + q, int(x):int(x) + q] = (246, 250, 255)


# ================================================================== 0: HOOK — face to the frosty glass: «One ninety-nine for a TV?!»
def r_hook(t, u):
    Z = 1.3
    def ex(big, v, a):
        try:
            mx, my = aout(a, v, 'mouth')
            breath(big, mx + 40, my, t, 1.0, 1.6)
        except Exception: pass
        frost(big, 'right', 0.85)
    big, a = K.cu(C.randy, t, OUT, 560.0, 500.0, Z, 22.0, head=(360, 960), light=light_out, blur=3, extra_fx=ex,
                  expr='shout', mouth_=max(0.5, mouth('randy', t)), tremble=1.0, look=(1.0, -0.1), stache='up', hand_n=(22.0, 72.0))
    if u < 0.35: K.CK.shake(big, t, 12, 33)
    return big


# ================================================================== 1: LINE — grannies under NO CAMPING, JOYCE · SINCE TUE, Brayden sells spots
def r_line(t, u):
    k = sm(u / 3.6)
    Z = 1.5
    cx = lerp(250.0, 345.0, k)
    v = V(OUT, cx, 500.0, Z)
    s = WS_OUT * Z * 3
    sw = WS_OUT
    acts = []
    for i, (x, kw) in enumerate([(150.0, dict(expr='nosy', look=(0.8, 0.0))), (235.0, dict(expr='sleepy', look=(0.0, -0.4)))]):
        g = C.GRANNIES[i]
        acts.append(A(C.folding_chair, x, SIDEWALK, s * 1.5, t=t, name='GERT' if i == 0 else 'BEV', sub='SINCE MON' if i == 0 else 'SINCE SUN'))
        acts.append(A(C.joyce, x, SIDEWALK - 12.0 * 1.5 * sw, s, sit=True, t=t, purse=None, perm=g['perm'], card=g['card'], **kw))
    acts.append(A(C.folding_chair, 380.0, SIDEWALK, s * 1.9, t=t, name='JOYCE', sub='SINCE TUE', tent=True))
    acts.append(A(C.yarn_ball, 412.0, SIDEWALK - 2.0, s, t=t))
    b = A(C.brayden, 305.0, SIDEWALK + 6.0, s, t=t, flip=True, expr='lazy' if not speaking('brayden', t) else 'dead', mouth_=mouth('brayden', t),
          look=(-0.3, 0.2), stick=False, hand_n=(10.0, 44.0))
    acts.append(b)
    def f(big, v_):
        ox, oy = v_.opt(380.0, SIDEWALK - 40.0)
        if 4.1 < t < 5.6: O.overlay(big, K.st('click-clack', fg=(200, 170, 255), size=40), int(ox - 330), int(oy - 360), 1.0)
        for x in (150.0, 235.0):
            hx, hy = v_.opt(x + 6.0, SIDEWALK - 52.0 * sw)
            breath(big, hx, hy, t + x, 0.6, 0.8)
    def pre(big, v_): big[:] = K.dof(big, 3)
    return K.shot(OUT, light_out, cx, 500.0, Z, acts=acts, pre=pre, fx_=f)


# ================================================================== 2: CLOCK — 4:59, knuckles in the turkey mitt: «Never LOST!» — «You never GOT UP.»
def r_clock(t, u):
    k = sm(u / 4.6)
    Z = lerp(1.30, 1.42, k)
    cx = 585.0
    v = V(OUT, cx, 500.0, Z)
    s = WS_OUT * Z * 3
    crack = abs(math.sin(t * 7)) if t < 7.2 else 0.0
    r = A(C.randy, 545.0, SIDEWALK, s, t=t, expr='proud' if speaking('randy', t) else ('glare' if t > 9.0 else 'smug'),
          mouth_=mouth('randy', t), look=(0.8, 0.0) if t < 9.0 else (0.9, 0.0), stache='up' if t < 9.0 else 'droop',
          hand_n=(16.0 + 2 * crack, 58.0), hand_f=(12.0 - 2 * crack, 56.0), mitt=True)
    b = A(C.brayden, 668.0, SIDEWALK + 4.0, s, t=t, flip=True, expr='dead' if speaking('brayden', t) else 'lazy', mouth_=mouth('brayden', t),
          look=(-0.9, 0.0), stick=True)
    def f(big, v_):
        clock_card(big, t, 230)
        rx, ry = v_.opt(545.0 + 10.0 * WS_OUT, SIDEWALK - 66.0 * WS_OUT)
        breath(big, rx, ry, t, 0.6, 1.0)
        if t >= 10.38: fx.flash_burst(big, OUT_W // 2, 320, 0.5 * (1 - (t - 10.38) / 0.32))
    return K.shot(OUT, light_out, cx, 500.0, Z, acts=[r, b], fx_=f)


# ================================================================== 3: STAMPEDE — 5:00, doors, grannies on walkers, flying shoes, Randy tumbles in
def r_stampede(t, u):
    Z = 1.2
    cx = 600.0 + 40.0 * u
    v = V(IN, cx, 470.0, Z)
    s = WS_IN * Z * 3
    acts = []
    for i in range(5):
        g = C.GRANNIES[i % len(C.GRANNIES)]
        x = 430.0 + (u * 300.0 + i * 70.0) % 360.0
        y = FLOOR_IN + 18.0 + (i % 2) * 34.0
        acts.append(A(C.joyce, x, y, s, t=t + i, expr='angry' if i % 2 else 'shout', look=(1.0, 0.0), purse=None, perm=g['perm'], card=g['card'],
                      hand_n=(8.0, 20.0), prop_n=lambda sp, h: C.walker(sp, h)))
    for i in range(3):
        ph = (u * 0.9 + i * 0.33) % 1.0
        acts.append(A(flying_shoe, 420.0 + 380.0 * ph, 600.0 - 220.0 * math.sin(math.pi * ph) + i * 30.0, s * 2.6, t=t, rot=ph * 900.0 + i * 70))
    rx = lerp(420.0, 760.0, sm(u / 2.2))
    acts.append(A(C.randy, rx, FLOOR_IN + 10.0, s, t=t, expr='panic', mouth_=0.6, look=(1.0, 0.0), legs=True, rot=-u * 540.0, pivot=(0.0, 40.0),
                  mitt=True))
    def f(big, v_):
        fx.speed_lines(big, t, 1.4, 700, 1800)
        for i in range(5):
            ph = (t * 1.3 + i * 0.2) % 1.0
            ox, oy = v_.opt(300.0 + i * 120.0, FLOOR_IN + 30.0)
            K.puff(big, ox - 160 * ph, oy - 40 * ph, 60 + 80 * ph, 0.35 * (1 - ph), (226, 220, 210), q=12)
        K.CK.shake(big, t, 10, 30)
    return K.shot(IN, light_in, cx, 470.0, Z, acts=acts, fx_=f)


# ================================================================== 4: MINE — slow-mo leap to the top of the DISPLAY ONLY pyramid
def r_mine(t, u):
    Z = 1.15
    cx, cy = 600.0, 300.0
    v = V(IN_B, cx, cy, Z)
    s = WS_IN * Z * 3
    sw = WS_IN
    lift = 16.0 * math.sin(math.pi * min(1.0, u / 1.05))
    ry = 370.0 - lift
    r = A(C.randy, 640.0, ry, s, t=t, expr='cheer', mouth_=max(0.3, mouth('randy', t)), look=(0.0, 0.3), legs=True, mitt=True,
          hand_n=(12.0, 92.0), hand_f=(-8.0, 92.0), stache='up')
    bx = A(C.tv_box, 642.0, ry - 84.0 * sw, s * 0.85, t=t, flap=0.0)
    def pre(big, v_): big[:] = K.dof(big, 4)
    def f(big, v_):
        fx.speed_lines(big, t * 0.3, 0.6, 0, 1920)
    return K.shot(IN_B, light_in, cx, cy, Z, acts=[r, bx], pre=pre, fx_=f)


# ================================================================== 5: HOLD — Kyle with the scanner gun: «That one's on HOLD.» — «For WHO?!»
def r_hold(t, u):
    Z = 1.32
    cx, cy = 935.0, 440.0
    v = V(IN, cx, cy, Z)
    s = WS_IN * Z * 3
    ky = A(C.kyle, 1012.0, FLOOR_IN - 40.0, s, t=t, flip=True, expr='dead', mouth_=mouth('kyle', t), look=(-0.9, -0.2), hand_n=(8.0, 40.0))
    bx = A(C.tv_box, 935.0, FLOOR_IN - 30.0, s, t=t, flap=0.0)
    r = A(C.randy, 862.0, FLOOR_IN - 20.0, s, t=t, expr='shout' if t > 15.7 else 'proud', mouth_=mouth('randy', t), look=(1.0, 0.0),
          stache='up' if t < 15.7 else None, tremble=1.0 if t > 15.7 else 0.0, hand_n=(14.0, 46.0), mitt=True)
    def f(big, v_):
        if t > 14.25:
            ox, oy = v_.opt(935.0, FLOOR_IN - 30.0 - 30.0 * WS_IN)
            k = min(1.0, (t - 14.25) / 0.12)
            O.overlay(big, K.st('ON HOLD', fg=(255, 70, 70), size=int(70 * (0.6 + 0.4 * k))), int(ox - 150), int(oy - 50), 1.0)
        if 14.05 < t < 14.4:
            hx, hy = v_.opt(1010.0 - 14.0 * WS_IN, FLOOR_IN - 50.0 - 40.0 * WS_IN)
            fx.glow(big, int(hx), int(hy), 120, (255, 60, 60), 0.5)
    return K.shot(IN, light_in, cx, cy, Z, acts=[ky, bx, r], fx_=f)


# ================================================================== 6: TWIST — the flap opens: Nana inside, knitting: «Me, sweetie. Since TUESDAY.»
def r_twist(t, u):
    Z = 1.55
    cx, cy = 900.0, 420.0
    v = V(IN, cx, cy, Z)
    s = 26.0
    sw = s / (3 * Z)
    wx, wy = W(v, 560.0, 1980.0)
    flap = sm(u / 0.3)
    acts = []
    if u > 0.12:
        rise = sm((u - 0.12) / 0.35)
        jy = wy - (BOX_TOP - JOY_IN_BOX - 14.0 * (1 - rise)) * sw
        acts.append(A(C.joyce, wx, jy, s, sit=True, t=t, expr='sweet' if not speaking('joyce', t) else 'fine', mouth_=mouth('joyce', t),
                      knit=t, look=(-0.2, -0.1), purse=None))
    acts.append(A(C.tv_box, wx, wy, s, t=t, flap=flap))
    def pre(big, v_): big[:] = K.dof(big, 7)
    def f(big, v_):
        if u < 0.4: fx.flash_burst(big, 560, 900, 0.6 * (1 - u / 0.4))
    return K.shot(IN, light_in, cx, cy, Z, acts=acts, pre=pre, fx_=f)


# ================================================================== 7: CAR — «No, it's FINE. Carry me to the CAR.» Randy hauls box + Nana
def r_car(t, u):
    k = sm(u / 3.27)
    rx = lerp(480.0, 700.0, k)
    Z = 1.45
    cx = rx + 10.0
    v = V(IN_B, cx, 440.0, Z)
    s = WS_IN * Z * 3
    sw = WS_IN
    walk = t * 9.0
    r = A(C.randy, rx, FLOOR_IN, s, t=t, expr='strain', mouth_=0.0, look=(1.0, 0.0), walk=walk, lean=0.3, sweat=1.0, mitt=True,
          hand_n=(12.0, 88.0), hand_f=(-6.0, 88.0), stache='droop', tremble=0.4)
    acts = [r]
    bob = abs(math.sin(walk)) * 1.0 * sw
    box_with_nana(acts, rx + 3.0 * sw, FLOOR_IN - 80.0 * sw - bob, s * 0.85, t,
                  joyce=dict(expr='fine', mouth_=mouth('joyce', t), knit=t, look=(-0.4, 0.0), purse=None), scale_world=sw * 0.85)
    def pre(big, v_): big[:] = K.dof(big, 4)
    return K.shot(IN_B, light_in, cx, 440.0, Z, acts=acts, pre=pre)


# ================================================================== 8: BAG — Scan-Dee: «Unexpected item…» — Tom on the bagging shelf: «Miss ME?»
def r_bag(t, u):
    Z = 1.25
    s = 24.0
    v0 = V(IN_B, 960.0, 430.0, Z)
    pan = sm((t - 24.35) / 0.6)
    cx = 960.0 + 148.0 * pan                                  # pan from the alarm screen to the bagging shelf
    kwx, kwy = W(v0, 698.0, 2022.0)                            # kiosk feet (world): its screen sits at (540, 760) before the pan
    drop = sm((t - 24.75) / 0.3)
    twx, twy = W(v0, 698.0 + TOMX * s, 2022.0 - BAG[1] * s - 900.0 * (1 - drop))
    acts = [A(C.kiosk, kwx, kwy, s, t=t, screen='alarm', lamp='red', alarm=1.0, part='back')]
    if t > 24.7:
        acts.append(A(C.tom, twx, twy, s, t=t, expr='dead', mouth_=mouth('tom', t, 1.6), look=(-0.1, -0.1)))
    def pre(big, v_): big[:] = K.dof(big, 6)
    def f(big, v_):
        K.alarm_tint(big, t, 0.25)
        if t > 25.0:
            tx, ty = v_.opt(twx, twy)
            K.cold_vapor(big, tx + 40, ty - 17 * s, t, 1.0, 1.4)
            K.thaw_meter(big, t, 25.1, 26.1, 'ROCK', x=900, y=520)
        if 25.0 < t < 25.25: K.CK.shake(big, t, 14, 40)
    return K.shot(IN_B, light_in, cx, 430.0, Z, acts=acts, pre=pre, fx_=f)


# ================================================================== 9: TOTAL — the screen: «$199 + GRANDMA» → Randy, to himself: «…Thanks, Randy.»
def r_total(t, u):
    if t < 28.85:
        def pre(big, v_): big[:] = K.dof(big, 9)
        big = K.shot(IN_B, light_in, 980.0, 430.0, 1.0, pre=pre)
        card = bb_screen(t, step=1 if t > 27.2 else 0)
        O.overlay(big, card, (OUT_W - card.shape[1]) // 2, 520, 1.0)
        if ST.LOG[0] is not None: ST.log('card', bbox=((OUT_W - card.shape[1]) // 2, 520, (OUT_W + card.shape[1]) // 2, 520 + card.shape[0]))
        return big
    big, a = K.cu(C.randy, t, IN_B, 960.0, 420.0, 1.4, 22.0 + 1.5 * (u - 2.7), head=(520, 900), light=light_in, blur=6, flip=True,
                  expr='sad', mouth_=mouth('randy', t, 1.4), look=(-0.3, -0.5), stache='droop', mitt=True)
    return big


# ================================================================== 10: S2 — snow, «SEASON 2: RANDY HOSTS CHRISTMAS», Tom: «Still FROZEN.»
def r_s2(t, u):
    Z = 1.3
    v = V(OUT, 640.0, 470.0, Z)
    def pre(big, v_): big[:] = K.dof(big, 5)
    tom = A(C.tom, *W(v, 540.0, 1640.0), 26.0, t=t, expr='dead', mouth_=mouth('tom', t, 1.6), look=(0.0, 0.0), frost=1.0)
    def f(big, v_):
        snow(big, t, 110)
        K.cold_vapor(big, 560, 1120, t, 1.0, 1.4)
        K.thaw_meter(big, t, 30.55, DUR, 'CHRISTMAS?', x=900, y=1050)
    big = K.shot(OUT, light_out, 640.0, 470.0, Z, acts=[tom], pre=pre, fx_=f)
    K.day_card(big, t, 30.45, DUR, 'SEASON 2:', 'RANDY HOSTS CHRISTMAS', y=560)
    return big


R = [r_hook, r_line, r_clock, r_stampede, r_mine, r_hold, r_twist, r_car, r_bag, r_total, r_s2]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 6, ['$199 TV?!'], hook_t=(0.10, 2.10), hook_y=330, hook_size=86,
              day=(2.35, 5.40, 'BLACK FRIDAY 4:59 AM', 'BEST BYE', 1650),
              stickers=[(K.st('SPOT IN LINE: $40', fg=(170, 255, 90), size=54), 3.30, 5.95, 540, 520),
                        (K.st('BLACK FRIDAYS ATTENDED: 0', fg=(255, 120, 120), size=46), 9.30, 10.65, 540, 1240),
                        (K.st('LAST ONE!', fg=(255, 214, 80), size=80), 13.10, 14.0, 540, 1300),
                        (K.st('SINCE TUESDAY', fg=(200, 150, 255), size=70), 16.95, 19.45, 540, 330)],
              flashes=[TWIST, 10.70], mosaics=[],
              cap_y={0: 1600, 1: 1640, 2: 1650, 3: 1600, 4: 1640, 5: 1640, 6: 1160, 7: 1650, 8: 1660, 9: 1660, 10: 1660})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
