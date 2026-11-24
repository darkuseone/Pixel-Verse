"""S01E02 «ONE BULB OUT?!» (MOTION DETECTED, US; 37.2 s, twist 19.6 s / 53 %, type: success is worse than failure).
STORY (radio play): night, Glenn on a stepladder at his porch with a dead string: «Six HUNDRED lights! ONE bulb is dead, and they ALL
went out!» — Doris: «Motion detected. Glenn. On a ladder. AGAIN.» — «Barry across the street did his whole house with ONE button.»
(Barry's house blazes, a snowman) — «But I have a SYSTEM. I check every bulb. One by ONE.» (montage: BULB 1/600 … 599/600, 6:40 PM →
11:58 PM) — «It's midnight, Glenn. Linda ate your DINNER.» — «Bulb six hundred. This is the ONE.» — CLICK: his house blazes like the sun
… BZZT: the whole street goes dark, only Glenn's house is lit — «Congratulations. Brightest house on the street. The ONLY house.» — «I
WON. Why is everybody walking toward ME?» — flashlights in the dark; Trent: «Evening, folks! Got a minute to talk about SOLAR?» — the
street: «YES!» — «Motion detected. Entire street. Holding FLASHLIGHTS.»
Season thread: «ATTEMPT 2 OF 3» tag on the door. No background blur, no loop-repeat (owner 22.11.2026).
  python3 ep02.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import mdcast as C
from props import mdkit as K
from props import mddecor as DEC
from props import mimic as M
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, CLICK, BZZT, MONT, YES

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='md', lang='us', promise='TOMORROW: $25 LIMIT'))
TAB = (C.XTRA, C.EXPR)
FG = M.Face([(0.0, 'furious'), (3.7, 'crushed'), (7.37, 'crushed'), (10.57, 'smug'), (12.8, 'stare'), (14.61, 'dead'), (17.16, 'stare'),
             (CLICK, 'shock'), (20.0, 'proud'), (BZZT + 0.2, 'shock'), (21.5, 'proud'), (25.2, 'proud'), (26.4, 'panic'), (27.9, 'dead'),
             (30.75, 'panic')], TAB, seed=3)
FD = M.Face([(0.0, 'deadpan'), (3.7, 'smirk'), (6.0, 'deadpan'), (14.61, 'sweet'), (20.7, 'smirk'), (32.0, 'deadpan')], TAB, seed=8)
FT = M.Face([(0.0, 'sales')], TAB, seed=5)

W = 'porch_night'
DORIS = (346.0, 324.0)
DS = 1.55
LAD = (664.0, 606.0)                     # stepladder feet on the lawn right of the porch railing
LAD_H = 24.0                             # its top platform (sprite px)
WS_L = K.ws_at(LAD[1])                   # Glenn and the ladder share one scale
GFEET = LAD[1] - LAD_H * WS_L            # Glenn stands on the platform
TRENT_K = 1.34


def mouth(who, t): return M.mouth(EPI.talk, who, t)


def kw_(F, who, t, base, **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def gkw(t, base=(-0.8, 0.0), **kw): return kw_(FG, 'glenn', t, base, **kw)
def dkw(t, base=(0.6, 0.0), **kw): return kw_(FD, 'doris', t, base, **kw)
def tkw(t, base=(0.8, 0.0), **kw): return kw_(FT, 'trent', t, base, **kw)


def lit_at(t):
    """Glenn's lights: off until CLICK, blaze (flicker) after"""
    if t < CLICK: return 0.0
    return 1.0 if t > CLICK + 0.25 else 0.5 + 0.5 * (int(t * 30) % 2)


def set_state(t):
    DEC.BLACKOUT[0] = 1.0 if t >= BZZT else 0.0
    K.LGLOW[0] = lit_at(t) * (1.4 if t < BZZT + 0.3 else 1.0)


def doris_act(t, Z, base=(0.6, 0.0)):
    return K.A(C.doris, DORIS[0], DORIS[1], DS * 3 * Z, rim=None, **dkw(t, base, dnd=False))


def ladder_act(Z):
    return K.A(lambda sp, **kw: C.stepladder(sp, h=LAD_H), LAD[0], LAD[1], WS_L * 3 * Z, rim=None)


def glenn_on_ladder(t, Z, base=(-0.8, 0.3), string=True, test=None, **kw):
    lit = lit_at(t)
    prop = (lambda sp, h: C.light_string(sp, h, lit=lit, t=t, test=test)) if string else kw.pop('prop_n', None)
    kw.setdefault('hand_n', (13.0, 74.0))
    return K.A(C.glenn, LAD[0] - 2.0, GFEET, WS_L * 3 * Z, flip=True, **gkw(t, base, prop_n=prop, **kw))


# ---------------------------------------------------------------- Glenn's lights on the porch: beam, column, railing
BULBS = ([(x, 100.0 - (x - 430.0) * 0.21) for x in range(440, 690, 14)] + [(592.0, y) for y in range(118, 345, 18)] +
         [(x, 352.0) for x in range(446, 590, 16)])


def porch_lights(t):
    lit = lit_at(t)
    def pre(big, v_):
        if t >= BZZT: blackout(big, v_)
        r = max(2, int(2.0 * v_.Z * 3))
        for i, (x, y) in enumerate(BULBS):
            ox, oy = v_.opt(x, y)
            if not (-60 < ox < OUT_W + 60 and -60 < oy < OUT_H + 60): continue
            c = np.array(C.BULBS[i % 4], np.float32)
            if lit > 0:
                R_ = int(r * (9 if t < BZZT + 0.4 else 7))
                x0, x1, y0, y1 = int(max(0, ox - R_)), int(min(OUT_W, ox + R_)), int(max(0, oy - R_)), int(min(OUT_H, oy + R_))
                if x0 < x1 and y0 < y1:
                    yy, xx = np.mgrid[y0:y1, x0:x1]
                    g = np.clip(1 - np.hypot(xx - ox, yy - oy) / R_, 0, 1)[..., None] ** 2 * 0.85 * lit
                    big[y0:y1, x0:x1] = np.clip(big[y0:y1, x0:x1] + g * (c * 0.6 + 100), 0, 255).astype(np.uint8)
                col = np.clip(c * 0.7 + 90, 0, 255)
            else:
                col = c * 0.30 + 20
            ix, iy = int(ox), int(oy)
            if 0 <= ix - r and ix + r < OUT_W and 0 <= iy - r and iy + r < OUT_H:
                rr_ = r if lit <= 0 else int(r * 1.5)
                big[iy - rr_:iy + rr_, ix - rr_ // 2:ix + rr_ // 2 + 1] = col.astype(np.uint8)
    return pre


def blackout(big, v_):
    """the street and the neighbors lose power: everything right of Glenn's porch (world x > 620, y < 470) goes night-dark"""
    x0, _ = v_.opt(620.0, 0.0)
    _, y1 = v_.opt(0.0, 470.0)
    xa, yb = int(max(0, x0)), int(min(OUT_H, y1))
    if xa < OUT_W and yb > 0:
        reg = big[:yb, xa:].astype(np.float32)
        g = reg.mean(axis=2, keepdims=True)
        big[:yb, xa:] = np.clip(g * 0.22 * np.array((0.7, 0.8, 1.35)) + 6, 0, 255).astype(np.uint8)


def shot(cx, cy, Z, t, acts, pre=None, **kw):
    set_state(t)
    kw.setdefault('dof_k', 0.0)
    pl = porch_lights(t)
    def pre2(big, v_):
        pl(big, v_)
        if pre: pre(big, v_)
    return K.shot(W, cx, cy, Z, acts=acts, pre=pre2, t=t, **kw)


def plate(big, text, y, fg=(255, 255, 255), size=44, x=None):
    img = O.sticker(text, fg=fg, size=size)
    O.overlay(big, img, (OUT_W - img.shape[1]) // 2 if x is None else x, y, 1.0)


def torches(t, k, pts, target=(600.0, 200.0)):
    """flashlight beams of the neighbors, additive cones aimed at Glenn's lit porch"""
    def f(big, v_):
        tx, ty = v_.opt(*target)
        for (wx, wy, ph) in pts:
            ox, oy = v_.opt(wx, wy)
            ang = math.atan2(ty - oy, tx - ox) + 0.12 * math.sin(t * 2.2 + ph)
            L_ = 520 * v_.Z
            yy, xx = np.mgrid[0:OUT_H:2, 0:OUT_W:2]
            dx, dy = xx - ox, yy - oy
            d = np.hypot(dx, dy) + 1e-3
            a = np.arctan2(dy, dx)
            da = np.abs((a - ang + math.pi) % (2 * math.pi) - math.pi)
            m = np.clip(1 - da / 0.22, 0, 1) * np.clip(1 - d / L_, 0, 1) * k
            m = np.repeat(np.repeat(m, 2, 0), 2, 1)[:OUT_H, :OUT_W][..., None]
            big[:] = np.clip(big + m * np.array((120, 115, 90)), 0, 255).astype(np.uint8)
            if 0 <= ox < OUT_W and 0 <= oy < OUT_H:
                Y, X = np.ogrid[0:OUT_H, 0:OUT_W]
                big[(X - ox) ** 2 + (Y - oy) ** 2 < (10 * v_.Z) ** 2] = (255, 250, 220)
    return f


# ================================================================== 0: HOOK — Glenn on the stepladder with the dead string
def r_hook(t, u):
    Z = 1.75 + 0.10 * glide(u / 3.6)
    cx, cy = LAD[0] - 20.0, 200.0
    shake = 4 * math.sin(t * 30) * math.exp(-t * 1.5)
    g = glenn_on_ladder(t, Z, hand_n=(14.0, 86.0 + 3 * math.sin(t * 12)), lean=-2.0)
    return shot(cx, cy, Z, t, [ladder_act(Z), g], par=(-4 + 6 * u, 0), kick=(shake, 0))


# ================================================================== 1/4: DORIS close-up at night
def r_doris(t, u, Z0=2.8, clock=None):
    Z = Z0 + 0.15 * glide(u / 3.0)
    cx, cy = DORIS[0] + 30.0, DORIS[1] - 30.0
    big = shot(cx, cy, Z, t, [doris_act(t, Z)], par=(-2 + 3 * u, 0))
    if clock:
        plate(big, clock, 1360, fg=(255, 214, 120), size=64)
        plate(big, 'BULB 599/600', 1450, fg=(120, 220, 255), size=48)
    return big


def r_d1(t, u): return r_doris(t, u, 2.7)
def r_dcu(t, u): return r_doris(t, u, 3.0, clock='11:58 PM')


# ================================================================== 2: BARRY's house across the street (one button)
def r_barry(t, u):
    Z = 1.25 + 0.08 * glide(u / 3.2)
    cx, cy = lerp(700.0, 770.0, glide(u / 3.2)), 300.0
    g = glenn_on_ladder(t, Z, base=(0.9, 0.0))
    g.flip = False
    return shot(cx, cy, Z, t, [ladder_act(Z), g], par=(-6 + 8 * u, 0))


# ================================================================== 3: «I have a SYSTEM» + the bulb-by-bulb montage
def r_system(t, u):
    Z = 1.6
    cx, cy = LAD[0] - 30.0, 230.0
    mont = t >= MONT
    k = 0.0 if not mont else min(1.0, (t - MONT) / (CUTS[5] - MONT))
    n = 1 + int(598 * k)
    g = glenn_on_ladder(t, Z, base=(-0.5, 0.6), test=n % 9, sweat=k * 2.0,
                        hand_f=(4.0, 80.0), prop_f=lambda sp, h: C.tester(sp, h, beep=int(t * 8) % 2 == 0))
    big = shot(cx, cy, Z, t, [ladder_act(Z), g], par=(-3 + 4 * u, 0))
    if mont:
        mins = int(lerp(18 * 60 + 40, 23 * 60 + 58, k))
        hh = mins // 60 % 12 or 12
        plate(big, f'{hh}:{mins % 60:02d} PM', 1360, fg=(255, 214, 120), size=64)
        plate(big, f'BULB {n}/600', 1450, fg=(120, 220, 255), size=48)
    return big


# ================================================================== 5: «Bulb six hundred. This is the ONE.»
def r_g4(t, u):
    Z = 2.6 + 0.2 * glide(u / 2.4)
    cx, cy = LAD[0] - 16.0, 150.0
    g = glenn_on_ladder(t, Z, base=(-0.6, 0.6), hand_n=(10.0, 92.0), sweat=1.0)
    return shot(cx, cy, Z, t, [ladder_act(Z), g], par=(2 - 3 * u, 0))


# ================================================================== 6/7: CLICK — the blaze, then BZZT — the street goes dark
def r_blaze(t, u, hold=False):
    Z = 0.95
    cx, cy = 600.0, 340.0
    g = glenn_on_ladder(t, Z, base=(0.9, 0.0) if t > BZZT + 0.6 else (-0.6, 0.6), hand_n=(13.0, 80.0))
    if t > BZZT + 0.6: g.flip = False
    big = shot(cx, cy, Z, t, [ladder_act(Z), g], kick=kick(t, [(CLICK, 0.8), (BZZT, 1.0)]))
    if CLICK <= t < CLICK + 0.35:
        big[:] = np.clip(big * 0.5 + 200, 0, 255).astype(np.uint8)
    return big


def r_only(t, u):
    Z = 0.95 + 0.25 * glide(u / 4.5)
    cx, cy = lerp(600.0, 640.0, glide(u / 4.5)), 330.0
    g = glenn_on_ladder(t, Z, base=(0.9, -0.1), hand_n=(13.0, 80.0))
    g.flip = False
    pts = [(1060.0, 460.0, 0.0), (930.0, 470.0, 1.3)] if t > 22.8 else []
    big = shot(cx, cy, Z, t, [ladder_act(Z), g], fx_=torches(t, sm((t - 22.8) / 0.6), pts) if pts else None)
    return big


# ================================================================== 8: «I WON. Why is everybody walking toward ME?»
def r_g5(t, u):
    Z = 1.7
    cx, cy = LAD[0] + 10.0, 230.0
    g = glenn_on_ladder(t, Z, base=(0.9, 0.1), hand_n=(13.0, 80.0), sweat=1.0 if t > 26.4 else 0.0)
    g.flip = False
    pts = [(lerp(900.0, 800.0, u / 2.7), 470.0, 0.0), (lerp(1000.0, 880.0, u / 2.7), 480.0, 1.7)]
    return shot(cx, cy, Z, t, [ladder_act(Z), g], fx_=torches(t, 1.0, pts))


# ================================================================== 9: TRENT in the dark, torch under his chin
def r_trent(t, u):
    Z = 2.0
    cx, cy = 760.0, 282.0
    tr = K.A(C.trent, 760.0, 530.0, K.ws_at(530.0) * TRENT_K * 3 * Z, flip=True, rim=None,
             **tkw(t, (-0.9, 0.0), hand_n=(10.0, 40.0), prop_n=lambda sp, h: C.clipboard(sp, h)))
    def f(big, v_):
        yy, xx = np.mgrid[0:OUT_H, 0:OUT_W]
        fx_, fy_ = 560, 1150
        m = np.clip(1 - np.hypot(xx - fx_, (yy - fy_) * 0.7) / 760, 0, 1)[..., None] ** 1.3
        big[:] = np.clip(big * (0.35 + 1.1 * m) + m * np.array((40, 36, 20)), 0, 255).astype(np.uint8)
    return shot(cx, cy, Z, t, [tr], fx_=f, motes=False)


# ================================================================== 10: the crowd with flashlights at the porch (button)
def r_crowd(t, u):
    Z = 0.85
    cx, cy = 800.0, 370.0
    g = glenn_on_ladder(t, Z, base=(0.9, 0.2), hand_n=(13.0, 80.0), sweat=2.0)
    g.flip = False
    acts = [ladder_act(Z), g]
    walk = min(1.0, u / 3.0)
    pts = []
    for i, (x0, x1, y, kind) in enumerate(((1060, 880, 500, 0), (1150, 960, 520, 1), (1230, 1040, 545, 2), (980, 800, 535, 0))):
        x = lerp(x0, x1, walk)
        ws = K.ws_at(y) * 0.95
        acts.append(K.A(lambda sp, k=kind, w_=t * 7 + i, **kw: C.silhouette(sp, kind=k, walk=w_ if walk < 1 else 0.0), x, y, ws * 3 * Z, flip=True, rim=None))
        pts.append((x - 15.0 * ws, y - 44.0 * ws, i))
    return shot(cx, cy, Z, t, acts, fx_=torches(t, 1.0, pts))


ST_BLAZE = K.st('600/600!', fg=(255, 230, 90), size=72)
ST_ONLY = K.st('POWER: ONLY GLENN', fg=(255, 120, 90), size=50)
ST_YES = K.st('"YES."', fg=(180, 255, 120), size=72)
R = [r_hook, r_d1, r_barry, r_system, r_dcu, r_g4, r_blaze, r_only, r_g5, r_trent, r_crowd]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['ONE BULB OUT?!'], hook_t=(0.10, 2.7), hook_y=1180, hook_size=66,
              stickers=[(ST_BLAZE, CLICK + 0.05, BZZT, 540, 560), (ST_ONLY, 21.4, 25.1, 540, 420), (ST_YES, YES, YES + 1.3, 540, 520)],
              flashes=[TWIST, BZZT], mosaics=[12.8],
              cap_y={0: 1560, 1: 1580, 2: 1580, 3: 1250, 4: 1250, 5: 1580, 6: 1580, 7: 1580, 8: 1580, 9: 1600, 10: 1560})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
