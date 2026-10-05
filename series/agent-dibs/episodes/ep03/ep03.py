"""S01E03 «Pothole» (v2 cast) — a car chase at 12 mph under the L. The villains drive into «Big Steve» and sink; Dibs calls 311
(«Please state your pothole.»), spends four months on hold and gets «Request closed: duplicate». One cone arrives. «It's marked.»
  python3 ep03.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import paths as P
import stage as ST
from stage import Chars, view_at, OUT_W, OUT_H
from scene import sm, lerp, Layer
import overlays as O
import fx
from episode import Episode
from props import dibspix as DX
from props import dibscast as DC
from props import chi_props as PR
from props import chikit as K
from props import chiui as UI
from props import bytfx as B
from props import folk
from props.folk import H, cap, ell, dot, poly, outline, OL
from props.us_props import rect, ltext, clipboard
from timeline import DUR, FPS, VOICE, SLUG, HOLD_T0, HOLD_T1

EPI = Episode('ep03', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
WORLD = K.world('avenue_under_L')
LANE_Y = 566.0                              # wheel line of the cars
BIG = (640.0, 580.0, 82.0, 15.0)            # «Big Steve»: centre x, y, half-width, half-height (world px)
SUV_X0 = 660.0


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


# ================================================================== potholes
def draw_hole(big, v, cx, cy, rx, ry, t=0.0, water=1.0):
    """pothole in the road (world px): broken asphalt rim, black hole, ice-water shimmer"""
    ox, oy = v.opt(cx, cy); s = v.Z * 3.0
    a, b = rx * s, ry * s
    y0, y1 = int(max(0, oy - b * 1.5)), int(min(OUT_H, oy + b * 1.5)); x0, x1 = int(max(0, ox - a * 1.3)), int(min(OUT_W, ox + a * 1.3))
    if y0 >= y1 or x0 >= x1: return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    nx, ny = (xx - ox) / a, (yy - oy) / b
    d = np.sqrt(nx * nx + ny * ny)
    ang = np.arctan2(ny, nx)
    jag = 1.0 + 0.07 * np.sin(ang * 9 + cx) + 0.05 * np.sin(ang * 17 + 1.0)
    inner = d < jag
    ring = (d < jag * 1.22) & ~inner
    reg = big[y0:y1, x0:x1]
    reg[ring] = (reg[ring].astype(np.float32) * 0.45 + np.array((84, 74, 80), np.float32) * 0.55).astype(np.uint8)
    top = ring & (ny < -0.4)
    reg[top & (((xx // 9 + yy // 9) % 3) == 0)] = (214, 226, 242)                                      # snow on the broken lip
    reg[inner] = (14, 16, 28)
    if water > 0:
        wat = inner & (ny > -0.15) & (d < jag * 0.9)
        reg[wat] = (30, 54, 92)
        sp = wat & ((((xx // 14) * 7 + (yy // 14) * 13 + int(t * 6)) % 9) == 0)
        reg[sp] = (150, 200, 240)
    reg[inner & (ny < -0.55)] = (6, 8, 16)


def holes_pre(holes, t=0.0):
    def pre(big, v):
        for cx, cy, rx, ry in holes: draw_hole(big, v, cx, cy, rx, ry, t)
    return pre


SMALL_HOLES = [(470.0, 590.0, 24.0, 6.0), (560.0, 574.0, 18.0, 5.0), (790.0, 596.0, 30.0, 7.0), (905.0, 580.0, 20.0, 5.0)]


# ================================================================== vehicles on the road
def A(fn, wx, wy, un=None, s=None, flip=False, pin=None, **P):
    return DX.Act(fn, wx, wy, s_=s, un=un, flip=flip, pin=pin, **P)


def sedan(t, x, y=LANE_Y, un=4.6, rot=0.0, shake=0.4, tilt=0.0, driver=True, expr='shout'):
    """Dibs's Bureau sedan; returns a list of actors (the car + Dibs through the window)"""
    acts = [lambda CH, v: PR.sedan(CH, v.cam(x, y, un), t, rot=rot, shake=shake, drivers=(), text='BUREAU')]
    if driver: acts.append(DC.driver(DC.dibs, x, y, un, 3.0, pose='wheel', t=t, expr=expr, shades=True))
    return acts


def suv(t, x, y=LANE_Y, un=4.6, rot=0.0, shake=0.3, antenna=0.0, signal=True, crew=True, expr='nervous'):
    """the villains' SUV; returns a list of actors (the car + Terry and Gary through the windows)"""
    acts = [lambda CH, v: PR.suv(CH, v.cam(x, y, un), t, rot=rot, shake=shake, drivers=(), signal=signal, antenna=antenna)]
    if crew:
        acts += [DC.driver(DC.terry, x, y, un, -6.0, h=10.6, pose='wheel', t=t, expr=expr, shades=True),
                 DC.driver(DC.gary, x, y, un, 2.0, h=10.6, size=3.4, pose='hold', t=t, expr=expr, shades=True)]
    return acts


def signs(t):
    return [lambda CH, v: PR.sign_board(CH, v.cam(405.0, 545.0, 3.5), [('POTHOLE', 1.8), ('(EST. 2019)', 1.0)], w=19.0),
            lambda CH, v: PR.sign_board(CH, v.cam(915.0, 548.0, 3.5), [('POTHOLE', 1.8), ('FEST', 1.8)], w=17.0, col=(120, 220, 255)),
            lambda CH, v: PR.sign_board(CH, v.cam(236.0, 548.0, 3.5), [('ROAD WORK', 1.4), ('AHEAD', 1.4), ('(2031)', 1.4)], w=17.0, col=(255, 140, 30))]


def sparks(t, seed=0):
    """welding-spark glints under the L (emissive)"""
    def f(big, v):
        rng = np.random.default_rng(seed + int(t * 12))
        for _ in range(26):
            x = int(rng.integers(0, OUT_W)); y = int(rng.integers(40, 560)); s = int(rng.choice((6, 9)))
            big[y:y + s, x:x + s] = (255, int(rng.integers(160, 230)), 70)
    return f


def puff_trail(t, x0, y0, n=5, rate=1.0):
    def f(big, v):
        for i in range(n):
            ph = (t * rate + i / n) % 1.0
            ox, oy = v.opt(x0 - 26 * ph * 3 - i * 3, y0 - 10 - 26 * ph)
            B.puff(big, ox, oy, (10 + 40 * ph) * v.Z * 3, 0.5 * (1 - ph), (214, 220, 230))
    return f


def road_shot(t, cx, acts, back=(), pre=None, fx_=None, emit=None, Z=1.0, cy=400.0, sy=320, ghost=()):
    return K.shot(WORLD, K.light_avenue, cx, cy, Z, acts=acts, back=back, pre=pre, fx_=fx_, emit=emit, sx=180, sy=sy, ghost=ghost, t=t)


# ================================================================== S1: interior hook
RATTLE = lambda t, a=1.0: (a * math.sin(t * 61), a * math.sin(t * 47 + 1))


def interior_parts(ax, ay, un, t):
    """steering wheel (behind the driver's hands) and dashboard with the 12 MPH gauge (in front), as callables a(CH, v)"""
    def wheel(CH, v):
        L = Layer(v.cam(ax, ay, un))
        pts = [H(8.4 + 1.9 * math.cos(k / 24 * 2 * math.pi), 12.6 + 5.6 * math.sin(k / 24 * 2 * math.pi)) for k in range(25)]
        for p0, p1 in zip(pts[:-1], pts[1:]): cap(L, p0, p1, 0.7, 0.7, (88, 92, 110), (170, 176, 198), (40, 42, 54))
        cap(L, H(8.4, 12.6), H(8.0, 7.0), 0.55, 0.55, (88, 92, 110)); cap(L, H(8.4, 12.6), H(8.9, 18.0), 0.55, 0.55, (88, 92, 110))
        ell(L, H(8.4, 12.6), 1.1, 1.3, (60, 62, 76), 0, (110, 114, 134), (24, 26, 32))
        outline(L, OL); CH.add(L)
    def dash(CH, v):
        L = Layer(v.cam(ax, ay, un))
        poly(L, [H(2.0, 5.2), H(30.0, 7.0), H(30.0, 15.4), H(11.0, 13.4), H(5.0, 11.4)], (62, 68, 90))
        poly(L, [H(2.0, 5.2), H(30.0, 7.0), H(30.0, 8.4), H(2.0, 6.4)], (14, 16, 24))
        cx_, cy_ = 15.4, 11.4
        ell(L, H(cx_, cy_), 4.4, 4.4, (22, 24, 32), 0, (60, 64, 80), (10, 10, 14))
        ell(L, H(cx_, cy_), 3.7, 3.7, (236, 234, 220), 0, (255, 254, 244), (190, 188, 176))
        for k in range(10):
            a = math.radians(225 - k * 27)
            cap(L, H(cx_ + 3.2 * math.cos(a), cy_ + 3.2 * math.sin(a)), H(cx_ + 3.65 * math.cos(a), cy_ + 3.65 * math.sin(a)), 0.1, 0.1, (40, 40, 50))
        a = math.radians(225 - 27 * 0.8) + 0.05 * math.sin(t * 70)
        cap(L, H(cx_, cy_), H(cx_ + 3.2 * math.cos(a), cy_ + 3.2 * math.sin(a)), 0.22, 0.12, (214, 30, 40))
        dot(L, H(cx_, cy_), (30, 30, 36), 0.55)
        ltext(L, '12', H(cx_ + 0.2, cy_ - 1.6), 0.95, (30, 30, 40))
        ltext(L, 'MPH', H(cx_, cy_ - 2.8), 0.65, (90, 90, 100))
        if int(t * 4) % 2 == 0: ell(L, H(21.0, 11.8), 0.9, 0.7, (255, 170, 30))
        if int(t * 3) % 2: ell(L, H(21.0, 10.2), 0.9, 0.7, (214, 40, 40))
        outline(L, OL); CH.add(L)
    return wheel, dash


DRIVE_POSE = dict(n=(8.2, 16.4), f=(7.0, 9.0), bn=1, bf=1, nleg=(1.3, 0.0), fleg=(1.2, 0.0))


def r_hook(t, u):
    un = 13.0
    head = (500.0, 470.0)
    ax, ay = head[0] - 0.9 * un, head[1] + 21.3 * un
    ahead = suv(t, 700.0 + 6 * u, 507.0, 1.7, signal=True)
    wheel, dash = interior_parts(ax, ay, un, t)
    dibs = A(DC.dibs, ax, ay, un=un, pose='wheel', t=t, mouth_=mouth('dibs', t, 1.9), expr='shout', shades=True, flap=t * 9)
    def pre(big, v):
        big[0:120, :] = (24, 26, 36); big[120:138, :] = (70, 76, 92)                # roof edge of the windshield frame
    big = K.shot(WORLD, K.light_avenue, 515.0, 522.0, 1.35, acts=[dibs], back=ahead + [wheel], front=[dash], pre=pre, sx=180, sy=330,
                 fx_=sparks(t, 3))
    rx, ry = RATTLE(t, 7.0)
    return np.roll(np.roll(big, int(ry), 0), int(rx), 1)


# ================================================================== S2: chase wide
def r_chase(t, u):
    x_s = SUV_X0 + 12.0 * u
    x_d = 470.0 + 11.0 * u
    acts = signs(t) + suv(t, x_s) + sedan(t, x_d, shake=0.5)
    def fx_(big, v):
        K.snow(big, v, t, 70)
        sparks(t, 1)(big, v)
        puff_trail(t, x_d - 22, LANE_Y)(big, v)
    return road_shot(t, 560.0, acts, pre=holes_pre(SMALL_HOLES + [BIG], t), fx_=fx_)


# ================================================================== S3: slalom
def r_slalom(t, u, a, b, name):
    k = (t - a) / (b - a)
    x = lerp(430.0, 640.0, k) if name != 'big' else lerp(500.0, 560.0, k)
    y = LANE_Y + 8.0 * math.sin(k * math.pi * 2.0)
    acts = signs(t) + suv(t, 735.0 + 18.0 * (t - 6.15)) + sedan(t, x, y, rot=0.0, shake=0.5)
    def fx_(big, v):
        K.snow(big, v, t, 60); sparks(t, 5)(big, v); puff_trail(t, x - 22, y)(big, v)
    if name == 'sl1': return road_shot(t, x + 80.0, acts, pre=holes_pre(SMALL_HOLES + [BIG], t), fx_=fx_, Z=1.25, sy=330)
    if name == 'sl2': return road_shot(t, x + 10.0, acts, pre=holes_pre(SMALL_HOLES + [BIG], t), fx_=fx_, Z=1.9, sy=400, cy=520.0)
    return road_shot(t, 620.0, acts, pre=holes_pre(SMALL_HOLES + [BIG], t), fx_=fx_, Z=1.0, sy=330)


# ================================================================== S4: the drop
def r_drop(t, u):
    d = max(0.0, u - 0.18) / 0.5                                        # sink progress
    sink = 70.0 * sm(min(1.0, d))
    x_s = BIG[0] + 4.0
    stash = {}
    def pre(big, v):
        holes_pre(SMALL_HOLES + [BIG], t)(big, v)
        stash['bg'] = big.copy()
    acts = signs(t)[:2] + suv(t, x_s, LANE_Y + sink, shake=0.8 * max(0.0, 1 - d), antenna=9.0, expr='panic' if d > 0.2 else 'nervous') + \
        sedan(t, 380.0 + 6.0 * max(0.0, 1 - u * 2), shake=0.0, expr='stunned')
    def emit(big, v):
        # the front lip of the hole hides everything that sank below the road line
        ox, oy = v.opt(BIG[0], BIG[1] + BIG[3] * 0.1)
        x0, x1 = int(v.opt(BIG[0] - BIG[2] * 1.25, 0)[0]), int(v.opt(BIG[0] + BIG[2] * 1.25, 0)[0])
        y0 = int(oy)
        yy, xx = np.mgrid[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
        nx = (xx - ox) / (BIG[2] * v.Z * 3.0 * 1.0); ny = (yy - oy) / (BIG[3] * v.Z * 3.0)
        m = (nx * nx + (ny * 0.0) ** 2) < 1.0
        reg = big[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
        reg[m] = stash['bg'][y0:OUT_H, max(0, x0):min(OUT_W, x1)][m]
        # splash + water ring
        if 0.15 < u < 0.9:
            for i in range(10):
                ph = (u - 0.15) * 1.8 + i * 0.07
                sx_, sy_ = v.opt(BIG[0] - 70 + i * 16, BIG[1] - 30 * math.sin(ph * 3.14) - 6)
                big[int(sy_):int(sy_) + 14, int(sx_):int(sx_) + 14] = (214, 236, 255)
    def fx_(big, v): K.snow(big, v, t, 60); puff_trail(t, 358.0, LANE_Y)(big, v)
    big = road_shot(t, 560.0, acts, pre=pre, fx_=fx_, emit=emit, Z=1.1, sy=330)
    if 0.15 < u < 0.7: B.shake(big, t, 14 * (1 - (u - 0.15) / 0.55), 37)
    return big


# ================================================================== S5: the antenna sinks («Ope?»)
def r_antenna(t, u):
    k = sm(u / 1.0)
    cx, cy = 640.0, 560.0
    def pre(big, v):
        draw_hole(big, v, cx, cy + 10, 82.0, 15.0, t)
    def emit(big, v):
        ox, oy = v.opt(cx - 20, cy + 6 + 26 * k)
        tip = int(oy)
        big[tip - 330:tip, int(ox) - 6:int(ox) + 6] = (80, 84, 98)
        big[tip - 336:tip - 306, int(ox) - 18:int(ox) + 18] = (226, 60, 60)
        for i in range(6):                                                                     # bubbles
            ph = (t * 1.3 + i * 0.17) % 1.0
            bx, by = ox + 40 * math.sin(i * 2.1 + t * 3), oy - 10 - 150 * ph
            r = int(8 + 14 * (1 - ph)); big[int(by):int(by) + r, int(bx):int(bx) + r] = (190, 224, 250)
        ring = int(40 + 220 * ((t * 1.2) % 1.0))
        yy, xx = np.ogrid[:OUT_H, :OUT_W]
        d = np.sqrt(((xx - ox) / 1.0) ** 2 + ((yy - oy) / 0.28) ** 2)
        big[(d > ring - 5) & (d < ring + 5)] = (200, 232, 255)
    return road_shot(t, cx, [], pre=pre, emit=emit, Z=2.0, cy=cy, sy=330)


# ================================================================== S6: Dibs peers over the edge
CU_S = 12.5
HEAD = (590.0, 470.0)


def cu_shot(t, u, act, Z=2.3, zoom=0.05, head=HEAD, sx=180, front=()):
    return K.shot(WORLD, K.light_avenue, head[0], head[1], Z + zoom * u, acts=[act], front=front,
                  pre=lambda big, v: draw_hole(big, v, 640.0, 585.0, 82.0, 15.0, t), fx_=lambda big, v: K.snow(big, v, t, 40), sx=sx, sy=262)


def r_peek(t, u):
    Z = 2.3 + 0.05 * u
    return cu_shot(t, u, A(DC.dibs, HEAD[0], HEAD[1], s=CU_S * Z / 2.3, pin='head', pose='stand', t=t, expr='deadpan', look=-0.6, shades=True))


# ================================================================== S7: dialling 311 on a flip phone
def flip_phone_big(big, cx, cy, s, digits, t):
    """large flip phone drawn on the output frame"""
    w, h = int(520 * s), int(860 * s)
    img = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([30, 30, w + 30, h + 30], 60, fill=(62, 66, 82, 255), outline=(20, 22, 30, 255), width=10)
    d.rounded_rectangle([60, 60, w, int(h * 0.44)], 30, fill=(18, 24, 20, 255), outline=(10, 10, 14, 255), width=6)
    d.rectangle([80, 80, w - 20, int(h * 0.44) - 20], fill=(150, 205, 140, 255))
    f = O.pfont(int(120 * s)); d.fontmode = '1'
    d.text(((w + 40) // 2, int(h * 0.22)), digits, font=f, fill=(24, 44, 26, 255), anchor='mm')
    fs = O.pfont(int(24 * s))
    d.text(((w + 40) // 2, int(h * 0.40)), 'CALLING...' if len(digits) >= 3 else 'DIAL', font=fs, fill=(24, 44, 26, 255), anchor='mm')
    for r in range(4):
        for c in range(3):
            bx = 90 + c * int((w - 130) / 3); by = int(h * 0.50) + r * int(h * 0.11)
            d.rounded_rectangle([bx, by, bx + int((w - 160) / 3), by + int(h * 0.085)], 16, fill=(170, 176, 190, 255), outline=(40, 44, 56, 255), width=5)
            lab = '123456789*0#'[r * 3 + c]
            d.text((bx + int((w - 160) / 6), by + int(h * 0.0425)), lab, font=O.pfont(int(40 * s)), fill=(30, 34, 46, 255), anchor='mm')
    O.overlay(big, np.array(img), int(cx - img.size[0] / 2), int(cy - img.size[1] / 2))


def r_dial(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    yy = np.arange(OUT_H)[:, None]
    big[:] = (16, 20, 44); big[(yy[:, 0] % 14) < 2] = (24, 30, 60)
    n = int((u - 0.05) / 0.2)
    digits = '311'[:max(0, min(3, n))]
    jig = 6 * math.sin(t * 40) if u < 0.3 else 0
    flip_phone_big(big, 540 + jig, 960, 1.5, digits, t)
    if u < 0.12: O.flash(big, 0.5 * (1 - u / 0.12))
    return big


# ================================================================== S8: the 311 operator (cubicle)
def cubicle(big, t):
    yy = np.arange(OUT_H)[:, None]
    big[:] = (176, 170, 150)                                                                   # beige partition fabric
    big[(yy[:, 0] % 16) < 2] = (160, 154, 134)
    big[:300] = (210, 208, 196)
    big[300:316] = (120, 112, 96)
    # cat poster «HANG IN THERE (ON HOLD)»
    big[470:1000, 90:620] = (24, 24, 30); big[484:986, 104:606] = (118, 170, 214)
    big[484:620, 104:606] = (170, 204, 236)
    big[640:686, 180:560] = (96, 150, 70)                                                      # branch
    big[686:730, 410:470] = (240, 150, 60)                                                      # hanging kitten body
    big[730:810, 424:456] = (240, 150, 60)
    big[700:730, 480:560] = (250, 250, 246)
    img = Image.fromarray(big); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((355, 900), 'HANG IN THERE', font=O.pfont(34), fill=(255, 255, 255), anchor='mm')
    d.text((355, 944), '(ON HOLD)', font=O.pfont(26), fill=(255, 236, 140), anchor='mm')
    # console with blinking lines
    d.rectangle([700, 1330, 1060, 1500], fill=(52, 56, 70), outline=(20, 22, 30), width=6)
    for i in range(12):
        c = (255, 80, 70) if (int(t * 3) + i) % 3 else (255, 190, 60)
        d.rectangle([720 + (i % 6) * 52, 1350 + (i // 6) * 60, 756 + (i % 6) * 52, 1384 + (i // 6) * 60], fill=c)
    big[:] = np.array(img)
    # desk
    big[1560:] = (110, 80, 52); big[1560:1580] = (150, 114, 78)


def operator_frame(t, expr='deadpan', mth=0.0, Z=2.0, u=0.0, dx=0.0, zoom=0.05, shake=0.0, hold=False):
    """Bea, the 311 operator, in her beige cubicle (frame drawn in output px; the desk hides everything below her waist)"""
    Zt = Z + zoom * u
    s = 13.0 * Zt / 2.0
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    cubicle(big, t)
    under = big.copy()
    sp = DX.Spr()
    DC.bea(sp, 'hold', t, mth, expr, gum=max(0.0, math.sin(t * 1.3)) ** 6 if mth < 0.05 else 0.0)
    hx, hy = sp.anchors['head']
    DX.blit(big, sp, 560 + dx * 3 - hx * s, 760 + hy * s, s, ST.Light(amb=(1.04, 1.02, 0.96), rim=(1, -0.3, (255, 240, 200), 0.3)))
    big[1560:] = under[1560:]
    fx.vignette(big, 0.26)
    if shake: B.shake(big, t, shake, 35)
    return big


# ================================================================== S9: Dibs on the phone
def dibs_phone(t, u, expr, k=1.7, Z=2.3, zoom=0.06, prop=True, pose='phone'):
    Zt = Z + zoom * u
    return cu_shot(t, u, A(DC.dibs, HEAD[0], HEAD[1], s=CU_S * Zt / 2.3, pin='head', pose=pose if prop else 'stand', t=t, mouth_=mouth('dibs', t, k),
                           expr=expr, shades=True, props={'R': 'flip'} if prop else None), Z=Z, zoom=zoom)


# ================================================================== S10: time-lapse «ON HOLD: 4 MONTHS»
MONTHS = ['JANUARY', 'APRIL', 'JULY', 'OCTOBER', 'JANUARY']


def r_lapse(t, u):
    span = HOLD_T1 - HOLD_T0
    k = min(0.999, u / span)
    ph = k * 4.0                                                         # 0..4 through the seasons
    season = int(ph)
    cyc = (ph * 3.0) % 1.0                                                # three day-cycles per season would be too fast: one dusk per season
    # sky tint cycles: night -> warm day -> night
    dayk = 0.5 - 0.5 * math.cos(ph * math.pi * 2.0)
    BEARD = min(1.0, k * 1.15)
    x_s = BIG[0]
    chair_x = 515.0
    ueq = 3.8 / 0.62
    acts = [
        lambda CH, v: PR.dibs_chair(CH, v.cam(chair_x, LANE_Y + 26, 3.8), t=t),
        A(DC.dibs, chair_x + 1.5 * ueq, LANE_Y + 26 + 0.2 * ueq, un=ueq, pose='sit', t=t, expr='sleepy' if int(t * 2) % 2 else 'deadpan', shades=True,
          beard=BEARD, hands={'R': (17.0, 40.0)}),
        lambda CH, v: PR.dibs_chair(CH, v.cam(chair_x, LANE_Y + 26, 3.8), t=t, only_sign=True),
    ]
    stash = {}
    def pre(big, v):
        holes_pre(SMALL_HOLES + [BIG], t)(big, v)
        stash['bg'] = big.copy()
    cars = [lambda CH, v: PR.suv(CH, v.cam(x_s, LANE_Y + 70.0, 4.6), t, signal=True, antenna=9.0)]
    heads = [A(DC.terry, x_s - 20.0, LANE_Y + 86.0, un=4.4, pose='hold', t=t, expr='smug', props={'R': 'cards'}, hat=True, clip_h=66.0),
             A(DC.gary, x_s + 22.0, LANE_Y + 88.0, un=4.4, flip=True, pose='hold', t=t, expr='smug', props={'R': 'cards'}, clip_h=40.0)]
    def emit(big, v):
        ox, oy = v.opt(BIG[0], BIG[1] + BIG[3] * 0.1)
        x0, x1 = int(v.opt(BIG[0] - BIG[2] * 1.25, 0)[0]), int(v.opt(BIG[0] + BIG[2] * 1.25, 0)[0])
        y0 = int(oy)
        yy, xx = np.mgrid[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
        nx = (xx - ox) / (BIG[2] * v.Z * 3.0)
        m = (nx * nx) < 1.0
        reg = big[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
        reg[m] = stash['bg'][y0:OUT_H, max(0, x0):min(OUT_W, x1)][m]
    def fx_(big, v):
        # season layers
        rng = np.random.default_rng(int(t * 24))
        if season in (0, 4): K.snow(big, v, t, 90)
        if season == 1:                                                    # spring: rain + tulips
            for i in range(60):
                x = int(rng.integers(0, OUT_W)); y = int(rng.integers(0, OUT_H)); big[y:y + 26, x:x + 4] = (170, 200, 240)
            for i, x in enumerate((70, 160, 770, 880, 980)):
                ox, oy = v.opt(x + 200, LANE_Y + 30)
                big[int(oy) - 40:int(oy), int(ox):int(ox) + 8] = (60, 160, 70)
                big[int(oy) - 64:int(oy) - 36, int(ox) - 12:int(ox) + 20] = (240, 70, 120) if i % 2 else (255, 214, 60)
        if season == 2:                                                    # summer: heat haze + sun glare
            fx.glow(big, 880, 280, 520, (255, 236, 150), 0.55)
            B.haze(big, v, t, (0, 760, 360, 1100), amp=6) if hasattr(B, 'haze') else None
        if season == 3:                                                    # autumn: leaves
            for i in range(46):
                ph_ = (t * 0.5 + i * 0.137) % 1.0
                x = int((i * 211 + math.sin(t * 2 + i) * 60) % OUT_W); y = int(ph_ * OUT_H)
                big[y:y + 18, x:x + 18] = [(224, 120, 30), (186, 70, 24), (240, 180, 40)][i % 3]
    big = road_shot(t, 580.0, acts, back=cars, pre=pre, fx_=fx_, emit=emit, Z=1.25, sy=360)
    # heads of the card players are drawn over the lip (they stand in the hole)
    v = view_at(WORLD, 580.0, 400.0, 1.25, 180, 360)
    lt = K.light_avenue(v)
    for a in heads: a(big, v, lt)
    # day / night tint
    tint = np.array((1.0, 1.0, 1.0)) * (0.62 + 0.55 * dayk) + np.array((0.04, 0.0, -0.10)) * dayk
    big[:] = np.clip(big.astype(np.float32) * tint, 0, 255).astype(np.uint8)
    # sun / moon sprite on an arc
    ang = ph * math.pi * 2.0
    mx = int(540 + 420 * math.sin(ang)); my = int(380 - 260 * math.cos(ang) * (1 if True else 0))
    if math.cos(ang) < 0.0:
        pass
    sun = dayk > 0.5
    r = 60
    yy, xx = np.ogrid[:OUT_H, :OUT_W]
    dd = np.sqrt((xx - mx) ** 2 + (yy - my) ** 2)
    big[dd < r] = (255, 232, 130) if sun else (236, 240, 255)
    # month tag + hold music equaliser
    img = Image.fromarray(big); d = ImageDraw.Draw(img); d.fontmode = '1'
    mo = MONTHS[min(4, int(ph + 0.5))]
    d.text((540, 250), mo, font=O.pfont(70), fill=(255, 255, 255), anchor='mm', stroke_width=7, stroke_fill=(20, 14, 40))
    big[:] = np.array(img)
    if u < 0.12: O.flash(big, 0.5 * (1 - u / 0.12))
    return big


# ================================================================== S11: the crew arrives, ONE cone
def r_crew(t, u, part):
    a = 35.85
    if part == 0:                                                            # truck rolls in
        k = sm(min(1.0, (t - a) / 0.55))
        tx = lerp(1020.0, 790.0, k)
        acts = [lambda CH, v: PR.city_truck(CH, v.cam(tx, LANE_Y + 14, 4.6, True), t)] + suv(t, BIG[0], LANE_Y + 70.0, 4.6, antenna=9.0, signal=True, crew=False)
        stash = {}
        def pre(big, v):
            holes_pre(SMALL_HOLES + [BIG], t)(big, v); stash['bg'] = big.copy()
        def emit(big, v):
            ox, oy = v.opt(BIG[0], BIG[1] + BIG[3] * 0.1)
            x0, x1 = int(v.opt(BIG[0] - BIG[2] * 1.25, 0)[0]), int(v.opt(BIG[0] + BIG[2] * 1.25, 0)[0])
            y0 = int(oy)
            yy, xx = np.mgrid[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
            m = (((xx - ox) / (BIG[2] * v.Z * 3.0)) ** 2) < 1.0
            reg = big[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
            reg[m] = stash['bg'][y0:OUT_H, max(0, x0):min(OUT_W, x1)][m]
        return road_shot(t, 760.0, acts, pre=pre, emit=emit, fx_=lambda big, v: K.snow(big, v, t, 60), Z=1.1, sy=330)
    # worker walks up, ONE cone on the roof of the SUV, orange X
    k = sm(min(1.0, (t - 36.4) / 0.4))
    wx = lerp(780.0, 690.0, min(1.0, (t - 36.2) / 0.5))
    stash = {}
    def pre(big, v):
        holes_pre(SMALL_HOLES + [BIG], t)(big, v)
        if t > 36.7:                                                          # sprayed orange X next to the hole
            for s_ in (-1, 1):
                for i in range(30):
                    x = 735.0 + i * 1.3 * s_ * 0 + (i - 15) * 1.0; y = 610.0 + (i - 15) * 0.5 * s_
                    ox, oy = v.opt(x, y); big[int(oy):int(oy) + 8, int(ox):int(ox) + 8] = (255, 130, 20)
        stash['bg'] = big.copy()
    acts = suv(t, BIG[0], LANE_Y + 70.0, 4.6, antenna=9.0, signal=False, crew=False) + [
            lambda CH, v: PR.cone(CH, v.cam(BIG[0] - 4.0, LANE_Y + 4.0 - 40 * (1 - k), 4.6)) if t > 36.35 else None,
            A(DC.worker, wx, LANE_Y + 14, un=4.8, flip=True, pose=DC.walk('stand', t, 5.0, 0.45, 0.4) if t < 36.7 else 'stand', t=t, expr='deadpan', shadow=0.3)]
    acts = [a for a in acts if a is not None]
    def emit(big, v):
        ox, oy = v.opt(BIG[0], BIG[1] + BIG[3] * 0.1)
        x0, x1 = int(v.opt(BIG[0] - BIG[2] * 1.25, 0)[0]), int(v.opt(BIG[0] + BIG[2] * 1.25, 0)[0])
        y0 = int(oy)
        yy, xx = np.mgrid[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
        m = (((xx - ox) / (BIG[2] * v.Z * 3.0)) ** 2) < 1.0
        reg = big[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
        reg[m] = stash['bg'][y0:OUT_H, max(0, x0):min(OUT_W, x1)][m]
    return road_shot(t, 700.0, acts, pre=pre, emit=emit, fx_=lambda big, v: K.snow(big, v, t, 60), Z=1.3, sy=340)


def r_worker(t, u):
    Z = 2.3 + 0.04 * u
    return cu_shot(t, u, A(DC.worker, HEAD[0], HEAD[1], s=CU_S * Z / 2.3, flip=True, pin='head', pose='hold', t=t, mouth_=mouth('chief', t, 1.5),
                           expr='deadpan', look=-0.7, props={'R': 'clipboard'}), zoom=0.04, sx=225)


def r_final(t, u):
    stash = {}
    def pre(big, v):
        holes_pre(SMALL_HOLES + [BIG], t)(big, v); stash['bg'] = big.copy()
    acts = suv(t, BIG[0], LANE_Y + 70.0, 4.6, antenna=9.0, signal=False, shake=0.0, crew=False) + [
            lambda CH, v: PR.cone(CH, v.cam(BIG[0] + 6.0, LANE_Y + 4.0, 5.2))]
    def emit(big, v):
        ox, oy = v.opt(BIG[0], BIG[1] + BIG[3] * 0.1)
        x0, x1 = int(v.opt(BIG[0] - BIG[2] * 1.25, 0)[0]), int(v.opt(BIG[0] + BIG[2] * 1.25, 0)[0])
        y0 = int(oy)
        yy, xx = np.mgrid[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
        m = (((xx - ox) / (BIG[2] * v.Z * 3.0)) ** 2) < 1.0
        reg = big[y0:OUT_H, max(0, x0):min(OUT_W, x1)]
        reg[m] = stash['bg'][y0:OUT_H, max(0, x0):min(OUT_W, x1)][m]
        # two hands holding «HELP (NO RUSH)» over the lip, left of the cone
        sx, sy = v.opt(BIG[0] - 34, BIG[1] + 2)
        sw, sh = 230, 150
        big[int(sy) - sh - 30:int(sy) - 30, int(sx) - sw // 2:int(sx) + sw // 2] = (250, 250, 246)
        big[int(sy) - sh - 30:int(sy) - sh - 18, int(sx) - sw // 2:int(sx) + sw // 2] = (214, 40, 50)
        im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.text((sx, sy - 112), 'HELP', font=O.pfont(48), fill=(30, 30, 40), anchor='mm')
        d.text((sx, sy - 62), '(NO RUSH)', font=O.pfont(26), fill=(30, 30, 40), anchor='mm')
        big[:] = np.array(im)
        for hx in (-sw // 2 + 10, sw // 2 - 10):
            big[int(sy) - 70:int(sy) - 6, int(sx) + hx - 30:int(sx) + hx + 30] = (240, 204, 176)
    return road_shot(t, 650.0, acts, pre=pre, emit=emit, fx_=lambda big, v: K.snow(big, v, t, 60), Z=1.6 - 0.15 * u, sy=360, cy=520.0)


# ================================================================== shot table
SHOTS = [
    (0.00, 2.50, 'hook'), (2.50, 4.20, 'seatbelt'), (4.20, 6.15, 'chase'), (6.15, 7.05, 'sl1'), (7.05, 7.55, 'sl2'), (7.55, 9.20, 'sl3'),
    (9.20, 10.25, 'drop'), (10.25, 11.30, 'antenna'), (11.30, 12.40, 'peek'), (12.40, 13.40, 'dial'), (13.40, 16.30, 'op1'),
    (16.30, 18.25, 'd3'), (18.25, 21.00, 'op2'), (21.00, 22.95, 'd4'), (22.95, HOLD_T0, 'op3'), (HOLD_T0, HOLD_T1, 'lapse'),
    (HOLD_T1, 31.45, 'op4'), (31.45, 33.00, 'd5'), (33.00, 35.85, 'op5'), (35.85, 36.40, 'crew1'), (36.40, 37.40, 'crew2'),
    (37.40, 38.55, 'd6'), (38.55, 40.45, 'worker'), (40.45, DUR + 1, 'final'),
]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def r_seatbelt(t, u):
    # Dibs in the car: the belt clicks on at the end of the line
    belt = sm(max(0.0, (t - 4.16) / 0.12))
    def belt_(sp):
        if belt <= 0.0: return
        a, b = (-15.0, 58.0), (-15.0 + 32.0 * belt, 58.0 - 34.0 * belt)
        sp.cap(a, b, 2.2, 2.2, [(22, 24, 30), (46, 48, 60), (70, 74, 90), (110, 114, 130)])
        if belt > 0.9: sp.rect(b[0] - 2, b[1] - 2, b[0] + 3, b[1] + 3, (214, 200, 90))
        sp.outline()
    Z = 2.3 + 0.05 * u
    a = A(DC.dibs, HEAD[0], HEAD[1], s=CU_S * Z / 2.3, pin='head', pose='stand', t=t, expr='shock' if belt < 0.5 else 'smug', shades=True, post=belt_)
    return K.shot(WORLD, K.light_avenue, HEAD[0], HEAD[1], Z, acts=[a], fx_=lambda big, v: K.snow(big, v, t, 40), sx=180, sy=262)


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name == 'hook': return r_hook(t, u)
    if name == 'seatbelt': return r_seatbelt(t, u)
    if name == 'chase': return r_chase(t, u)
    if name == 'sl1': return r_slalom(t, u, a, b, 'sl1')
    if name == 'sl2': return r_slalom(t, u, a, b, 'sl2')
    if name == 'sl3': return r_slalom(t, u, a, b, 'big')
    if name == 'drop': return r_drop(t, u)
    if name == 'antenna': return r_antenna(t, u)
    if name == 'peek': return r_peek(t, u)
    if name == 'dial': return r_dial(t, u)
    if name == 'op1': return operator_frame(t, 'deadpan', mouth('operator', t, 1.5), Z=2.0, u=u)
    if name == 'd3': return dibs_phone(t, u, 'deadpan', k=1.4)
    if name == 'op2': return operator_frame(t, 'blank', mouth('operator', t, 1.5), Z=2.4, u=u, dx=-6.0)
    if name == 'd4': return dibs_phone(t, u, 'shout', k=1.8, zoom=0.12)
    if name == 'op3': return operator_frame(t, 'deadpan', mouth('operator', t, 1.5), Z=2.1, u=u)
    if name == 'lapse': return r_lapse(t, u)
    if name == 'op4': return operator_frame(t, 'smile', mouth('operator', t, 1.5), Z=2.2, u=u)
    if name == 'd5': return dibs_phone(t, u, 'angry', k=1.9, zoom=0.1)
    if name == 'op5': return operator_frame(t, 'blank', mouth('operator', t, 1.5), Z=2.3, u=u, dx=6.0)
    if name == 'crew1': return r_crew(t, u, 0)
    if name == 'crew2': return r_crew(t, u, 1)
    if name == 'd6': return dibs_phone(t, u, 'stunned', k=1.5, prop=False)
    if name == 'worker': return r_worker(t, u)
    return r_final(t, u)


# ================================================================== overlays
def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 3, ['CAR CHASE', '(12 MPH)'], hook_t=(0.15, 2.4),
              stickers=[
                  (st('FRANK', (255, 255, 255), 66), 6.30, 7.05, 540, 600),
                  (st('LINDA', (255, 255, 255), 66), 7.05, 7.58, 540, 600),
                  (st('BIG STEVE', (255, 214, 70), 74), 7.58, 9.15, 540, 600),
                  (st('ON HOLD: 4 MONTHS', (255, 120, 120), 52), HOLD_T0 + 0.25, HOLD_T1, 540, 400),
                  (st('REQUEST #4,512,331: CLOSED', (150, 255, 160), 36), 40.50, 41.30, 540, 560),
              ],
              flashes=[], mosaics=[], cap_default=1400,
              cap_y={'chase': 1450, 'sl1': 1450, 'sl2': 1450, 'sl3': 1450, 'drop': 1450, 'crew1': 1450, 'crew2': 1450, 'final': 1600, 'lapse': 1700})


def render(t):
    big = render_scene(t)
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
