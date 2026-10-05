"""S01E05 «Don't Let Go» (v2 cast) — Dibs, handcuffed to a briefcase, is lifted by the Hawk (the wind off the lake) and flies over the river
and between the towers. He delivers first, slams into the Bean and lands at the Chief's feet. The wind snatches the trophy and drops it
into Brad's hands. «I called DIBS!» — «Not in writing.» The oversized cuffs just fall off.
  python3 ep05.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from episode import Episode
from props import dibspix as DX
from props import dibscast as DC
from props import dibskit as DK
from props import chi_props as PR
from props import chikit as K
from props import bytfx as B
from timeline import DUR, FPS, VOICE, SLUG, SPLAT_T, TURN_T

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
RIVER = K.world('skyline_river')
PLAZA = K.world('bean_plaza')
CU_S = 12.5
FLOOR = 668.0                                # plaza floor line (crowd feet)
POD = (785.0, 646.0)                         # podium (Chief stands on it)
BEAN = (640.0, 345.0, 262.0, 150.0)          # the Bean: centre, half-width, half-height (world px)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def A(fn, wx, wy, un=None, s=None, flip=False, pin=None, **P):
    return DX.Act(fn, wx, wy, s_=s, un=un, flip=flip, pin=pin, **P)


CASE = {'R': 'briefcase'}
UP = {'R': (32.0, 110.0)}


def flyer(x, y, t, un=None, s=None, rot=-80.0, expr='wind', mth=0.0, pin='mid', wind=1.0, flip=False, **kw):
    """Dibs pulled through the air by the briefcase (arm up = forward when rotated); (x, y) = world position of his middle"""
    return A(DC.dibs, x, y, un=un, s=s, pin=pin, flip=flip, pose='arms_up', hands=UP, props=CASE, t=t, expr=expr, mouth_=mth, wind=wind,
             rot=rot, pivot=(0.0, 60.0), **kw)


def gust(t, k=1.0):
    def f(big, v):
        K.wind_snow(big, t, k)
        fx.speed_lines(big, t, 0.5 * k)
    return f


def pigeons(big, t, t0, n=5):
    """pigeons blown backwards: facing left, drifting right, wings beating"""
    for i in range(n):
        sp = DX.Spr(); DC.pigeon(sp, flap=t * 22 + i)
        x = -200 + ((t - t0) * 900 + i * 260) % 1500
        y = 380 + 170 * i + 30 * math.sin(t * 6 + i)
        DX.blit(big, sp, x, y, 9.0, None, True)


def confetti(big, t, t0, n=90, seed=3):
    if t < t0: return
    r = np.random.default_rng(seed)
    cols = [(255, 214, 60), (226, 40, 60), (104, 186, 240), (250, 250, 250), (120, 230, 120)]
    for i in range(n):
        x0 = r.uniform(0, OUT_W); sp = r.uniform(180, 380); ph = r.uniform(0, 3)
        y = (t - t0) * sp - 200 + r.uniform(0, 900)
        if y < -20 or y > OUT_H: continue
        x = int(x0 + 40 * math.sin(t * 3 + ph)); s = int(r.choice((10, 14, 18)))
        w = s if int(t * 8 + i) % 2 else s // 2
        big[int(y):int(y) + s, max(0, x):max(0, min(OUT_W, x + w))] = cols[i % len(cols)]


def lights(big, t, t0, xs, y):
    """traffic lights along the bridge flick to green one after another"""
    for i, x in enumerate(xs):
        green = t > t0 + i * 0.35
        big[y - 150:y, x - 6:x + 6] = (40, 42, 52)
        big[y - 230:y - 140, x - 30:x + 30] = (24, 24, 30)
        for k, c in enumerate(((226, 40, 50), (240, 180, 40), (60, 230, 110))):
            on = (k == 2) if green else (k == 0)
            cc = c if on else tuple(v // 5 for v in c)
            big[y - 222 + k * 28:y - 200 + k * 28, x - 12:x + 12] = cc
        if green and t < t0 + i * 0.35 + 0.15: fx.glow(big, x, y - 166, 90, (60, 230, 110), 0.6)


def podium(big, v):
    """ceremony podium draped in the Chicago flag (white, two light-blue stripes, four red stars) with a gold seal on top"""
    x0, y0 = v.opt(POD[0] - 70, POD[1] - 38)
    x1, y1 = v.opt(POD[0] + 70, POD[1] + 22)
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    H_, W_ = big.shape[:2]
    def box(a, b, c, d, col):
        big[max(0, b):max(0, min(H_, d)), max(0, a):max(0, min(W_, c))] = col
    h = y1 - y0
    box(x0 - 6, y0 - 6, x1 + 6, y1, (24, 18, 40))                                    # outline
    box(x0, y0, x1, y1, (236, 238, 244))
    box(x0, y0, x1, y0 + max(2, h // 12), (250, 250, 252))
    for k in (0.28, 0.66):
        yy = y0 + int(h * k); box(x0, yy, x1, yy + max(3, h // 9), (110, 190, 240))
    cy = y0 + int(h * 0.47); r = max(3, h // 14)
    for i in range(4):                                                               # six-pointed stars, pixel style
        cx = x0 + int((x1 - x0) * (0.2 + 0.2 * i))
        box(cx - r, cy - r // 3, cx + r, cy + r // 3 + 1, (226, 40, 50)); box(cx - r // 3, cy - r, cx + r // 3 + 1, cy + r, (226, 40, 50))
    box(x0 - 10, y0 - 14, x1 + 10, y0, (150, 104, 24)); box(x0 - 10, y0 - 14, x1 + 10, y0 - 9, (244, 204, 80))   # gold top rail


CROWD = [(548, FLOOR + 22, 7.4, 0), (598, FLOOR + 36, 7.8, 2), (650, FLOOR + 26, 7.2, 4), (700, FLOOR + 44, 8.0, 5), (848, FLOOR + 30, 7.6, 3),
         (885, FLOOR + 46, 8.0, 6), (520, FLOOR + 50, 8.2, 7)]


def crowd(t, pose='stand', expr='normal', skip=(), look=0.4, cheer=False):
    out = []
    for i, (x, y, un, var) in enumerate(CROWD):
        if i in skip: continue
        p = DC.walk('arms_up', t, 7.0, 0.1, 0.6) if cheer else pose
        out.append(A(DC.townie, x, y, un=un, flip=x > 640, variant=var, pose=p, t=t + i, expr='cheer' if cheer else expr, look=look, shadow=0.25))
    return out


def plaza(t, cx, cy, Z, acts=(), front=(), emit=None, fx_=None, sy=330, pre=None, pod=True):
    def emit2(big, v):
        if emit: emit(big, v)
    def pre2(big, v):
        if pod: podium(big, v)
        if pre: pre(big, v)
    def fx2(big, v):
        K.snow(big, v, t, 50)
        if fx_: fx_(big, v)
    return K.shot(PLAZA, K.light_bean, cx, cy, Z, acts=acts, front=front, pre=pre2, emit=emit2, fx_=fx2, sx=180, sy=sy)


def chief_act(t, x=POD[0], y=POD[1] - 30, un=7.6, pose='hold', trophy=True, mth=0.0, expr='deadpan', **kw):
    return A(DC.chief, x, y, un=un, flip=True, pose=pose, t=t, mouth_=mth, expr=expr, props={'R': 'trophy'} if trophy else None,
             hands={'R': (24.0, 50.0)} if trophy and pose == 'hold' else None, shadow=0.0, **kw)


# ================================================================== shots
def cu_wind(t, u, expr='wind', mth=0.0, Z=2.2, rot=-12.0, pan=70.0, cy=170.0, s=14.0):
    """close-up of Dibs in the wind over the river: background races past, he stays in frame"""
    cx = 560.0 - pan * u
    a = A(DC.dibs, cx, cy, s=s, pin='head', pose='arms_up', hands=UP, props=CASE, t=t, expr=expr, mouth_=mth, wind=1.0,
          rot=rot, pivot=(3.0, 82.0))
    big = K.shot(RIVER, K.light_river, cx, cy + 40.0, Z, acts=[a], fx_=gust(t, 1.0), sx=180, sy=300)
    B.shake(big, t, 5, 41)
    return big


def r_hook(t, u):
    return cu_wind(t, u, mth=0.25 + 0.2 * math.sin(t * 17))


def r_kite(t, u):
    k = sm(u / 1.75)
    Z = lerp(2.0, 1.0, k)
    x = lerp(520.0, 600.0, k); y = lerp(170.0, 190.0, k)
    a = flyer(x, y, t, s=lerp(14.0, 5.0, k) * 0.8, rot=lerp(-25.0, -80.0, k))
    return K.shot(RIVER, K.light_river, lerp(560.0, 620.0, k), lerp(200.0, 330.0, k), Z, acts=[a], fx_=gust(t, 0.8), sx=180, sy=320)


def r_d1(t, u):
    return cu_wind(t, u, expr='shout', mth=mouth('dibs', t, 1.9), Z=2.3, rot=-20.0, pan=90.0, s=13.0)


def r_river(t, u):
    k = u / 3.45
    x = lerp(400.0, 800.0, k); y = 190.0 - 40.0 * math.sin(k * math.pi)
    a = flyer(x, y, t, un=6.4, rot=-80.0 + 8.0 * math.sin(t * 3))
    def emit(big, v):
        pass
    return K.shot(RIVER, K.light_river, lerp(540.0, 700.0, k), 330.0, 1.0, acts=[a], fx_=gust(t, 0.7), emit=emit, sx=180, sy=330)


def r_d2(t, u):
    return cu_wind(t, u, expr='shout', mth=mouth('dibs', t, 1.9), Z=2.4, rot=-8.0, pan=60.0, s=14.0)


def r_deb(t, u):
    return DK.deb_frame(t, 'smile', mouth('deb', t, 1.6), Z=2.0, u=u)


def r_d3(t, u):
    roar = t > 15.35
    big = cu_wind(t, u, expr='shout' if roar else 'stunned', mth=mouth('dibs', t, 2.0), Z=2.3 + (0.25 * sm((t - 15.35) / 0.3) if roar else 0.0),
                  rot=-10.0, pan=40.0, s=13.5)
    if roar: B.shake(big, t, 14, 37)
    return big


def r_towers(t, u):
    k = u / 1.85
    cx = lerp(560.0, 700.0, k)
    x = cx - 10.0; y = 235.0 + 10 * math.sin(t * 4)
    dib = flyer(x, y, t, un=6.0, rot=-78.0, expr='shout', mth=0.3, shades=True)
    def chair(CH, v):
        if not hasattr(dib, 'last'): return
        sp, sc = dib.last, dib.scale(v)
        hxl, hyl = sp.anchors['handL']; mx, my = sp.anchors['mid']
        wx = dib.wx + (hxl - mx) * sc / (3 * v.Z); wy = dib.wy - (hyl - my) * sc / (3 * v.Z)
        cu = 6.0 * 0.62 * 1.4
        PR.dibs_chair(CH, v.cam(wx, wy - 2, cu), t=t, sign=False)
        px, py = v.pt(wx, wy)
        K.rot_chars(CH, -0.5 + 0.12 * math.sin(t * 6), px, py)
    def emit(big, v): pigeons(big, t, 16.3)
    return K.shot(RIVER, K.light_river, cx, 170.0, 1.6, acts=[dib], front=[chair], emit=emit, fx_=gust(t, 1.2), sx=180, sy=330)


def van_with_brad(t, x, y, un=4.6, wave=True, mth=0.0):
    return [lambda CH, v: PR.minivan(CH, v.cam(x, y, un), t, rot=-x * 0.3, driver=False, blinker=True),
            A(DC.brad, x + 5.0 * un, y - 9.6 * un, un=un * 0.62, pin='head', pose='wave' if wave else 'wheel', t=t, mouth_=mth, expr='grin',
              legs=False, clip_h=58.0, look=-0.6)]


def r_brad(t, u):
    x = 760.0 + 30.0 * u
    acts = van_with_brad(t, x, 458.0, 5.2, True, mouth('brad', t, 1.7))
    acts += [flyer(880.0 + 40 * u, 250.0, t, un=4.0, rot=-80.0)]
    return K.shot(RIVER, K.light_river, 820.0, 400.0, 1.5, acts=acts, fx_=lambda big, v: K.snow(big, v, t, 50), sx=180, sy=330)


def r_race(t, u):
    x = 700.0 + 40.0 * u
    acts = van_with_brad(t, x, 458.0, 4.2, False)
    acts += [flyer(780.0 + 160 * u, 300.0, t, un=5.0, rot=-82.0, expr='shout', mth=0.4)]
    def emit(big, v): lights(big, t, 19.75, (300, 560, 820), int(v.opt(0, 452.0)[1]))
    return K.shot(RIVER, K.light_river, 820.0, 400.0, 1.15, acts=acts, emit=emit, fx_=gust(t, 0.9), sx=180, sy=330)


def r_splat(t, u):
    p = t - SPLAT_T
    acts = crowd(t, expr='shock' if p > 0 else 'normal', look=0.0)
    acts.append(chief_act(t))
    if p < 0:                                                                               # flying in
        k = sm((t - 21.0) / (SPLAT_T - 21.0))
        acts.append(flyer(lerp(470.0, 600.0, k), lerp(230.0, 250.0, k), t, un=6.4, rot=-80.0, expr='shout', mth=0.5))
    elif p < 0.40:                                                                          # slides down the Bean's skin
        k = sm(p / 0.40)
        ang = lerp(math.pi * 0.62, math.pi * 0.32, k)
        bx = BEAN[0] + BEAN[2] * 0.8 * math.cos(ang); by = BEAN[1] - BEAN[3] * 0.9 * math.sin(ang)
        acts.append(flyer(bx, by, t, un=6.4, rot=lerp(-80.0, 20.0, k), expr='stunned', wind=0.3))
    elif p < 0.65:                                                                          # drops off the edge onto the plaza
        k = (p - 0.40) / 0.25
        ang = math.pi * 0.32
        sx_, sy_ = BEAN[0] + BEAN[2] * 0.8 * math.cos(ang), BEAN[1] - BEAN[3] * 0.9 * math.sin(ang)
        acts.append(flyer(lerp(sx_, POD[0] - 88.0, k), lerp(sy_, FLOOR - 100.0, k * k), t, un=6.4, rot=lerp(20.0, 0.0, k), expr='stunned', wind=0.3))
    else:                                                                                   # lands at the Chief's feet, briefcase up
        acts.append(A(DC.dibs, POD[0] - 88.0, FLOOR - 4, un=6.4, pose='arms_up', hands=UP, props=CASE, t=t, expr='stunned', shades=False, shadow=0.3))
    big = plaza(t, 700.0, 440.0, 1.0, acts=acts)
    if 0 <= p < 0.1: O.flash(big, 0.7 * (1 - p / 0.1))
    if 0 <= p < 0.5: B.shake(big, t, 18 * (1 - p / 0.5), 37)
    return big


def r_chief1(t, u):
    Z = 2.3 + 0.05 * u
    a = A(DC.chief, POD[0], 470.0, s=CU_S * Z / 2.3, flip=True, pin='head', pose='hold', hands={'R': (26.0, 52.0)}, props={'R': 'trophy'}, t=t,
          mouth_=mouth('chief', t, 1.5), expr='deadpan', look=-0.4)
    def emit(big, v):
        confetti(big, t, 23.1)
        if int(t * 10) % 7 == 0: O.flash(big, 0.25)
    return plaza(t, POD[0], 470.0, Z, acts=[a], emit=emit, sy=262)


def r_teary(t, u):
    Z = 2.3 + 0.06 * u
    a = A(DC.dibs, 560.0, 470.0, s=CU_S * Z / 2.3, pin='head', pose='tears', t=t, mouth_=mouth('dibs', t, 1.6), expr='teary', badge22=True, look=0.5)
    return plaza(t, 560.0, 470.0, Z, acts=[a], emit=lambda big, v: confetti(big, t, 23.1, 60), sy=262)


def trophy_sprite(sp, t=0.0, **_):
    DC.p_trophy(sp, (0.0, 4.0), 0.0, t)
    sp.anchors['head'] = (0.0, 30.0)
    sp.outline()


def r_trophy(t, u):
    k = sm(u / 1.45)
    acts = crowd(t, expr='shock', look=0.0) + [chief_act(t, pose='arms_up' if u < 0.35 else 'shrug', trophy=u < 0.35, expr='shock' if u > 0.35 else 'deadpan')]
    if u >= 0.35:
        q = (u - 0.35) / 1.1
        acts.append(A(trophy_sprite, lerp(POD[0] - 20, 450.0, q), lerp(470.0, 400.0, q) - 70 * math.sin(math.pi * q), un=9.0, t=t, rot=-540.0 * q))
    def emit(big, v):
        confetti(big, t, 23.1, 120, seed=int(u * 3) + 5)
        fx.speed_lines(big, t, 0.3)
    big = plaza(t, lerp(760.0, 600.0, k), 440.0, 1.15, acts=acts, emit=emit)
    g = big.mean(axis=2, keepdims=True)
    big[:] = (big * 0.75 + g * 0.25).astype(np.uint8)                                                # slow-motion grade
    return big


def r_catch(t, u):
    k = sm(min(1.0, u / 0.35))
    acts = [lambda CH, v: PR.minivan(CH, v.cam(330.0, FLOOR + 6, 6.4), t, driver=False, blinker=False)]
    brad = A(DC.brad, 470.0, FLOOR + 10, un=8.4, flip=True, pose='arms_up', t=t, mouth_=mouth('brad', t, 1.7), expr='grin' if u > 0.4 else 'shock',
             props={'R': 'trophy'} if u > 0.35 else None, ting=1.0 if 0.4 < u < 0.8 else 0.0, shadow=0.3)
    acts.append(brad)
    if u <= 0.35: acts.append(A(trophy_sprite, lerp(620.0, 485.0, k), lerp(380.0, 455.0, k), un=8.4, t=t, rot=-200.0 * (1 - k)))
    return plaza(t, 450.0, 470.0, 1.6, acts=acts, emit=lambda big, v: confetti(big, t, 23.1, 70))


def r_d5(t, u):
    Z = 2.3 + 0.08 * u
    a = A(DC.dibs, 560.0, 470.0, s=CU_S * Z / 2.3, pin='head', pose='shout', t=t, mouth_=mouth('dibs', t, 1.9), expr='angry', badge22=True)
    big = plaza(t, 560.0, 470.0, Z, acts=[a], sy=262)
    B.shake(big, t, 6, 40)
    return big


def r_chief2(t, u):
    Z = 2.5 + 0.04 * u
    a = A(DC.chief, POD[0], 470.0, s=CU_S * 1.1, flip=True, pin='head', pose='stand', t=t, mouth_=mouth('chief', t, 1.5), expr='deadpan', look=-0.6)
    return plaza(t, POD[0], 470.0, Z, acts=[a], sy=262)


def r_crowd(t, u):
    acts = crowd(t, cheer=True, skip=(2, 3))
    acts += [A(DC.terry, 530.0, FLOOR + 40, un=8.6, pose=DC.walk('arms_up', t, 9.0, 0.1, 0.8), t=t, expr='cheer', mouth_=0.6, shadow=0.3),
             A(DC.gary, 596.0, FLOOR + 44, un=8.4, flip=True, pose=DC.walk('arms_up', t + 0.3, 9.0, 0.1, 0.8), t=t, expr='cheer', mouth_=0.7, shadow=0.3),
             A(DC.brad, 712.0, FLOOR + 22, un=8.0, flip=True, pose='arms_up', t=t, expr='grin', props={'R': 'trophy'}, ting=0.6, shadow=0.3)]
    return plaza(t, 625.0 + 20 * u, 480.0, 1.25, acts=acts, emit=lambda big, v: confetti(big, t, 33.9, 110, 9))


CUFF_HAND = (600.0, 560.0)                    # world point of Dibs's right hand in the cuffs insert
CUFF_HIT = 0.58                               # u when the dropped briefcase hits the floor (below frame)


def r_cuffs(t, u):
    """insert: the oversized STANDARD ISSUE cuff slides off Dibs's wrist, the briefcase drops out of frame — CLANG"""
    s = 17.0
    hx, hy = CUFF_HAND
    a = A(DC.dibs, hx, hy, s=s, pin='handR', pose='hold', hands={'R': (36.0, 72.0)}, t=t, expr='sad')
    def emit(big, v):
        sp = DX.Spr(); DC.p_briefcase(sp, (0.0, 30.0), 0.0, t, mode='hang')      # ring at sprite y=30 (case stays on the canvas)
        ox, oy = v.opt(hx, hy)
        sl = sm((u - 0.16) / 0.20)                                     # ring slides down over the mitten
        dy = 2.0 - 9.0 * sl                                            # ring centre relative to the hand, sprite px (y up)
        if u > 0.36: dy -= 0.5 * 3600.0 * (u - 0.36) ** 2               # free fall
        jig = 0.6 * math.sin(t * 40) if u < 0.16 else 0.0
        DX.blit(big, sp, ox + jig * s, oy + (30.0 - dy) * s, s, K.light_bean(v), False)
        if u > CUFF_HIT:                                               # snow puff from the floor below
            q = min(1.0, (u - CUFF_HIT) / 0.12)
            r = np.random.default_rng(int(t * 30))
            for _ in range(40):
                x = int(r.uniform(300, 900)); y = int(OUT_H - r.uniform(0, 260) * q)
                big[y - 10:y + 10, x - 10:x + 10] = (226, 232, 244)
    big = plaza(t, hx - 12.0, hy + 20.0, 3.2, acts=[a], emit=emit, sy=300)
    fx.vignette(big, 0.35)
    if u > CUFF_HIT: B.shake(big, t, 16 * max(0.0, 1 - (u - CUFF_HIT) / 0.12), 40)
    return big


def r_proud(t, u):
    Z = 1.35 + 0.05 * u
    w = sm((u - 2.15) / 0.45)                                                            # the Hawk is back (into the loop)
    acts = [A(DC.dibs, 585.0, FLOOR, un=8.4, pose='stand', t=t, expr='stunned' if w > 0.3 else 'sad', look=0.2 if w < 0.3 else 0.8,
              wind=w, shadow=0.3)]
    def pre(big, v):
        sp = DX.Spr(); DC.p_briefcase(sp, (0.0, 0.0), 0.0, t, mode='floor')
        ox, oy = v.opt(632.0 + 6 * w * math.sin(t * 30), FLOOR + 2)
        DX.blit(big, sp, ox, oy, 8.4 * Z * 0.75, K.light_bean(v), False)
    big = plaza(t, 595.0, 470.0, Z, acts=acts, pre=pre, fx_=gust(t, w) if w > 0.02 else None, pod=False)
    DK.deb_window(big, t, 'smile' if t < 37.4 else 'deadpan', mouth('deb', t, 1.6), box=(650, 230, 1010, 590))
    return big


def r_loop(t, u):
    if u > 1.25: return cu_wind(t, 0.0)
    k = sm(u / 1.25)
    a = flyer(585.0 + 20 * k, FLOOR - 126.0 - 120 * k, t, un=8.4, rot=lerp(0.0, -70.0, k), expr='shock', wind=k)
    return plaza(t, 595.0, 470.0 - 60 * k, 1.35 + 0.4 * k, acts=[a], fx_=gust(t, k), pod=False)


# ================================================================== shot table
SHOTS = [
    (0.00, 1.80, 'hook'), (1.80, 3.55, 'kite'), (3.55, 5.65, 'd1'), (5.65, 9.10, 'river'), (9.10, 10.75, 'd2'), (10.75, 14.30, 'deb'),
    (14.30, 16.30, 'd3'), (16.30, 18.15, 'towers'), (18.15, 19.70, 'brad'), (19.70, 21.00, 'race'), (21.00, 23.00, 'splat'),
    (23.00, 25.65, 'chief1'), (25.65, TURN_T, 'teary'), (TURN_T, 29.50, 'trophy'), (29.50, 31.00, 'catch'), (31.00, 32.70, 'd5'),
    (32.70, 34.00, 'chief2'), (34.00, 34.95, 'crowd'), (34.95, 35.65, 'cuffs'), (35.65, 38.25, 'proud'), (38.25, DUR + 1, 'loop'),
]
FUNCS = {'hook': r_hook, 'kite': r_kite, 'd1': r_d1, 'river': r_river, 'd2': r_d2, 'deb': r_deb, 'd3': r_d3, 'towers': r_towers, 'brad': r_brad,
         'race': r_race, 'splat': r_splat, 'chief1': r_chief1, 'teary': r_teary, 'trophy': r_trophy, 'catch': r_catch, 'd5': r_d5,
         'chief2': r_chief2, 'crowd': r_crowd, 'cuffs': r_cuffs, 'proud': r_proud, 'loop': r_loop}


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    return FUNCS[name](t, u)


# ================================================================== overlays
def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 5, ["DON'T", 'LET GO'], hook_t=(0.15, 2.2),
              stickers=[
                  (st('STANDARD ISSUE', (200, 210, 230), 50), 6.10, 8.10, 540, 380),
                  (st('THE HAWK: 80 MPH', (110, 210, 255), 56), 15.35, 17.40, 540, 236),
                  (st('22 YRS PROBATIONARY', (255, 120, 120), 44), 26.00, 27.95, 540, 330),
                  (st('AGENT OF THE YEAR: BRAD?!', (60, 225, 170), 40), 34.05, 34.95, 540, 330),
              ],
              flashes=[], mosaics=[], cap_default=1400,
              cap_y={'kite': 1500, 'river': 1500, 'towers': 1500, 'brad': 1500, 'race': 1450, 'splat': 1450, 'trophy': 1450, 'catch': 1450,
                     'crowd': 1500, 'cuffs': 1500, 'proud': 1500})


def render(t):
    big = render_scene(t)
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
