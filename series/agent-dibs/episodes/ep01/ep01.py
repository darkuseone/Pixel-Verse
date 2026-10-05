"""S01E01 «Dibs» (v2 cast) — Special Agent Dibs covers a bomb with his lawn chair and calls dibs. The villains, the bomb squad and a tank
respect the chair; the bomb does not, but the blast goes AROUND the chair. Brad from Naperville asks if the spot is open.
Heroes: pixel-sprite cast of this series (props/dibscast.py, engine props/dibspix.py); props (chair, bomb, vehicles) from chi_props.
  python3 ep01.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import paths as P
import stage as ST
from stage import Chars, view_at
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
from timeline import DUR, FPS, VOICE, SLUG

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
WORLD = K.world('dibs_row')
GY = 650.0                              # street line for the main group
CH_X, CH_Y = 640.0, 654.0               # the chair (and the bomb under it)
DB_X = 560.0                            # Dibs standing
BOOM_T = 27.30
SOOT = 0.55                             # how black Dibs gets after the blast (eyes and teeth stay white)
CHU = 0.62                              # chair/bomb size relative to a person (a real lawn chair is ~half a man tall)
SIGN_Y = 7.4                            # the cardboard sign hangs from the seat, so the bomb under the chair stays visible
BOMB_R = 4.0


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def snow_fx(t, n=70):
    return lambda big, v: K.snow(big, v, t, n)


def sit_anchor(un):
    """feet anchor for Dibs sitting on the chair at (CH_X, CH_Y): his hips (sprite y 22) land on the seat (8.4 chair units); shifted a bit
    forward so the towel and the back post of the chair peek out behind him and the bomb shows under the seat"""
    return CH_X + 1.5 * un, CH_Y + 0.2 * un


def ueq(s, Z):
    """sprite scale -> equivalent world unit (1 unit = 4 sprite px), so props drawn in units match the sprite heroes"""
    return s / (Z * 0.75)


def A(fn, wx, wy, un=None, s=None, flip=False, pin=None, **P):
    return DX.Act(fn, wx, wy, s_=s, un=un, flip=flip, pin=pin, **P)


# ================================================================== reusable pieces
def spark_bomb(CH, v, sp, ax, ay, un, t, fuse=1.0):
    q = PR.bomb(CH, v.cam(ax, ay, un), t, fuse, r=BOMB_R)
    sp['p'] = (ax + q[0] * un, ay - q[1] * un)


def spark_glow(spark, t, r=300, a=0.8):
    def emit(big, v):
        if 'p' in spark:
            ox, oy = v.opt(*spark['p'])
            fx.glow(big, ox, oy, r * v.Z / 2.0, (255, 150, 50), a * (0.8 + 0.2 * math.sin(t * 40)))
    return emit


def chair_acts(t, un, x=CH_X, y=CH_Y, bomb=True):
    cu_ = un * CHU
    acts = [lambda CH, v: PR.bomb(CH, v.cam(x, y, cu_), t, r=BOMB_R)] if bomb else []
    return acts + [lambda CH, v: PR.dibs_chair(CH, v.cam(x, y, cu_), t=t, sign_y=SIGN_Y)]


def chair_sign(t, un, x=CH_X, y=CH_Y):
    """the cardboard sign again, in front of Dibs sitting on the chair"""
    return lambda CH, v: PR.dibs_chair(CH, v.cam(x, y, un * CHU), t=t, only_sign=True, sign_y=SIGN_Y)


CU_BG = 1.45     # background zoom behind close-ups: the hero is near the camera (2x sprite), the street stays far and crisp


def cu(fn, who, t, u, hx, hy, Z=2.0, s=12.5, zoom=0.06, sx=180, sy=300, flip=False, k=1.8, extra=(), front=(), pre=None, emit=None,
       light=K.light_street, fxn=70, cdx=0.0, cdy=0.0, bgZ=CU_BG, **P):
    """close-up: the hero's head pinned at world (hx, hy), drawn at 2x sprite resolution; the background is zoomed less (bgZ) than the
    hero (a near subject against a far street), so it does not turn into pixel mush; slow push on both"""
    q = 1.0 + zoom * u / Z
    Zt = bgZ * q
    P.setdefault('mouth_', mouth(who, t, k))
    a = A(fn, hx, hy, s=s * q, flip=flip, pin='head', t=t, hires=True, **P)
    cx, cy = hx + cdx * Z / bgZ, hy + (30.0 + cdy) * Z / bgZ             # the head keeps its old place on screen
    return K.shot(WORLD, light, cx, cy, Zt, acts=list(extra) + [a], front=front, fx_=snow_fx(t, fxn), sx=sx, sy=sy, pre=pre, emit=emit)


def cu_dibs(t, u, expr, shades=True, pose='stand', soot=0.0, Z=2.1, s=12.5, zoom=0.07, hands=None, props=None, **kw):
    return cu(DC.dibs, 'dibs', t, u, 520.0, 420.0, Z=Z, s=s, zoom=zoom, expr=expr, shades=shades, pose=pose, soot=soot, hands=hands, props=props, **kw)


def standing_group(t, dibs_expr='smug', dibs_pose='hips', shades=True, chair=True, bomb=True, un=6.8):
    """Dibs next to the chair, as the base of the wide shots"""
    acts = chair_acts(t, un, bomb=bomb) if chair else []
    acts.append(A(DC.dibs, DB_X, CH_Y - 4, un=un, pose=dibs_pose, t=t, expr=dibs_expr, shades=shades, shadow=0.35))
    return acts


# ================================================================== shots
def r_hook(t, u):
    Z = 1.7
    s = 10.5
    un = ueq(s, Z)
    fall = max(0.0, 1.0 - t / 0.10)
    sp = {}
    cu_ = un * CHU * 1.15
    acts = [A(DC.dibs, 515.0, 660.0, s=s, pose='point', t=t, mouth_=mouth('dibs', t, 1.9), expr='shout', shadow=0.3, hires=True),
            lambda CH, v: spark_bomb(CH, v, sp, 612.0, 664.0, cu_, t),
            lambda CH, v: PR.dibs_chair(CH, v.cam(612.0, 664.0 - fall * 520, cu_), t=t, sign_y=SIGN_Y)]
    big = K.shot(WORLD, K.light_street, 562.0, 560.0, Z, acts=acts, emit=spark_glow(sp, t), fx_=snow_fx(t), sx=180, sy=330)
    if 0.10 <= t < 0.16: O.flash(big, 0.45)
    if 0.10 < t < 0.5: B.shake(big, t, 12 * max(0.0, 1 - (t - 0.10) / 0.4), 33)
    return big


def r_insert(t, u):
    cu_ = 12.0
    sp = {}
    acts = [lambda CH, v: spark_bomb(CH, v, sp, CH_X + 20.0, 646.0, cu_, t),
            lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X + 20.0, 646.0, cu_), t=t, sign_y=SIGN_Y)]
    big = K.shot(WORLD, K.light_street, CH_X + 20.0, 540.0, 1.5 + 0.10 * u, acts=acts, emit=spark_glow(sp, t, 360), fx_=snow_fx(t), sx=180, sy=330)
    DK.deb_window(big, t, 'smile' if u < 1.5 else 'nervous', mouth('deb', t, 1.6), box=(690, 390, 1030, 730))
    return big


def r_deb(t, u, expr='smile'):
    return DK.deb_frame(t, expr, mouth('deb', t, 1.6), Z=2.0, u=u)


def r_suv(t, u):
    k = min(1.0, u / 0.85)
    x = lerp(1180.0, 810.0, 1 - (1 - k) ** 2)
    acts = standing_group(t)
    acts += [lambda CH, v: PR.suv(CH, v.cam(x, 706.0, 4.2, True), t, rot=-x * 0.25, shake=0.4 if k < 1 else 0.0)]
    if u > 0.9:
        acts += [A(DC.gary, 700.0, 674.0, un=6.8, flip=True, t=t, expr='normal', shadow=0.3),
                 A(DC.terry, 742.0, 668.0, un=6.8, flip=True, t=t, expr='nervous', shadow=0.3)]
    def fx_(big, v):
        snow_fx(t)(big, v)
        if u < 1.1:
            for i in range(7):
                ph = u - i * 0.07
                if ph < 0: continue
                ox, oy = v.opt(x + 75 + 22 * i, 690 - 8 * ph * 14)
                B.puff(big, ox, oy, (30 + 60 * ph) * 3 * v.Z, 0.7 * max(0.0, 1 - ph / 1.0), (232, 238, 248))
    big = K.shot(WORLD, K.light_street, 690.0, 480.0, 1.0, acts=acts, fx_=fx_, sy=330)
    if u < 0.5: B.shake(big, t, 8 * (1 - u / 0.5), 33)
    return big


def r_two(t, u):
    show_card = 0.45 < u < 1.05
    Z = 1.35 + 0.1 * u
    un = 8.6
    acts = chair_acts(t, 6.8 * 1.3, x=CH_X - 30, y=678.0) + [
        A(DC.gary, 800.0, 674.0, un=un * 0.98, flip=True, t=t, expr='nervous', shades=True, shadow=0.3),
        A(DC.terry, 735.0, 668.0, un=un, flip=True, pose='reach' if show_card else 'stand', t=t, mouth_=mouth('terry', t, 1.7), expr='nervous',
          shades=True, props={'R': 'card'} if show_card else None, hands={'R': (17.0, 70.0)} if show_card else None, shadow=0.3)]
    return K.shot(WORLD, K.light_street, 705.0, 540.0, Z, acts=acts, fx_=snow_fx(t), sy=340)


def r_gary(t, u):
    return cu(DC.gary, 'gary', t, u, 800.0, 430.0, Z=2.1, s=13.0, flip=True, k=1.6, expr='nervous', shades=False)


def r_sorry(t, u):
    k = sm(u / 1.2)
    acts = chair_acts(t, 8.0, x=CH_X + 10) + [
        A(DC.gary, lerp(790.0, 860.0, k), 674.0, un=8.0, flip=True, pose='hat', t=t, expr='nervous', hat=False, props={'R': 'beanie'}, shadow=0.3),
        A(DC.terry, lerp(725.0, 795.0, k), 668.0, un=8.0, flip=True, pose='hat', t=t, mouth_=mouth('terry', t, 1.8), expr='nervous', hat=False,
          props={'R': 'beanie'}, shadow=0.3)]
    return K.shot(WORLD, K.light_street, 725.0, 520.0, 1.35, acts=acts, fx_=snow_fx(t), sy=340)


def r_squad(t, u):
    k = sm(min(1.0, u / 0.6))
    tx = lerp(1250.0, 850.0, 1 - (1 - k) ** 2)
    ofl = u < 1.35
    ox = 800.0 - 130.0 * sm(min(1.0, max(0.0, (u - 0.45) / 0.65))) + 130.0 * sm(min(1.0, max(0.0, (u - 1.5) / 0.5)))
    rx = 800.0 - 130.0 * sm(min(1.0, max(0.0, (u - 0.5) / 0.7))) + 140.0 * sm(min(1.0, max(0.0, (u - 1.5) / 0.55)))
    walk = 2.0 * math.sin(u * 14) if (0.45 < u < 1.1 or u > 1.5) else 0.0
    acts = standing_group(t)
    acts += [lambda CH, v: PR.squad_truck(CH, v.cam(tx, 706.0, 4.2, True), t, rot=-tx * 0.25)]
    if u > 0.45:
        acts += [A(DC.tech, ox, 670.0 - abs(walk) * 0.6, un=7.0, flip=ofl, t=t, expr='nervous' if u < 1.2 else 'stunned',
                   pose='hat' if 1.1 < u < 1.5 else 'stand', look=-0.6, shadow=0.3)]
    if u > 0.55:
        acts += [lambda CH, v: PR.robot(CH, v.cam(rx, 672.0, 6.0, ofl), t, sad=sm(min(1.0, max(0.0, (u - 1.15) / 0.3))))]
    def fx_(big, v):
        snow_fx(t)(big, v)
        if u < 0.7:
            for i in range(5):
                ph = u - i * 0.06
                if ph < 0: continue
                ox_, oy_ = v.opt(tx + 70 + 20 * i, 690 - 100 * ph)
                B.puff(big, ox_, oy_, (28 + 50 * ph) * 3 * v.Z, 0.6 * max(0.0, 1 - ph / 0.8), (232, 238, 248))
    return K.shot(WORLD, K.light_street, 700.0, 470.0, 1.0, acts=acts, fx_=fx_, sy=330)


def r_tank(t, u):
    k = sm(min(1.0, u / 0.85))
    x = lerp(-200.0, 400.0, 1 - (1 - k) ** 2) if u < 1.4 else lerp(400.0, -200.0, sm(min(1.0, (u - 1.4) / 0.8)))
    sal = 1.0 if 0.85 < u < 1.3 else 0.0
    dr = sm(min(1.0, max(0.0, (u - 0.85) / 0.25)))
    acts = standing_group(t)
    acts += [lambda CH, v: PR.tank(CH, v.cam(x, 696.0, 5.6), t, droop=dr * (1 if u < 1.5 else 0), salute=sal)]
    big = K.shot(WORLD, K.light_street, 580.0, 480.0, 1.0, acts=acts, fx_=snow_fx(t), sy=330)
    if u < 0.9 or u > 1.4: B.shake(big, t, 3, 29)
    return big


def sit_dibs(t, un=None, s=None, expr='smug', mth=0.0, soot=0.0, sip=False, look=0.0):
    """Dibs on the chair with his coffee (sprite); un or s"""
    ax, ay = sit_anchor(un if un else 8.0)
    hands = {'R': (17.0, 44.0)} if not sip else {'R': (13.0, 70.0)}
    return A(DC.dibs, ax, ay, un=un, s=s, pose='sit', t=t, mouth_=mth, expr=expr, shades=True, hands=hands, props={'R': 'coffee'}, soot=soot, look=look)


def sit_scene(t, un, tpose, gpose, expr='smug', soot=0.0, mth=0.0, tx=(780.0, 835.0), sip=False):
    acts = chair_acts(t, un) + [sit_dibs(t, un=un, expr=expr, mth=mth, soot=soot, sip=sip), chair_sign(t, un)]
    for fn, x, y, p in ((DC.terry, tx[0], 668.0, tpose), (DC.gary, tx[1], 674.0, gpose)):
        hat = p != 'hat'
        acts.append(A(fn, x, y, un=un * (0.97 if fn is DC.gary else 1.0), flip=True, pose=p, t=t, expr='panic' if p == 'ears' else 'nervous',
                      hat=hat, props=None if hat else {'R': 'beanie'}, shadow=0.3))
    return acts


def r_sit(t, u):
    acts = sit_scene(t, 8.5, 'ears' if u > 1.2 else 'hat', 'ears' if u > 1.3 else 'hat', tx=(780.0, 835.0))
    big = K.shot(WORLD, K.light_street, 700.0, 520.0, 1.55, acts=acts, fx_=snow_fx(t), sy=340)
    DK.deb_window(big, t, 'panic', mouth('deb', t, 1.7), box=(650, 190, 1010, 550))
    return big


def r_dsit(t, u):
    s_ = sm((u - 1.3) / 0.4)
    Z = CU_BG + 0.04 * u
    un = 7.0 * 2.1 / CU_BG                                                   # Dibs + chair near the camera, the street far behind
    ax, ay = sit_anchor(un)
    hands = {'R': (lerp(17.0, 13.0, s_), lerp(44.0, 70.0, s_))}
    acts = chair_acts(t, un) + [A(DC.dibs, ax, ay, un=un, pose='sit', t=t, mouth_=mouth('dibs', t, 1.8), expr='smug', shades=True, hands=hands,
                                  props={'R': 'coffee'}, hires=True), chair_sign(t, un)]
    hx, hy = ax + 3 * un / 4, ay - 82 * un / 4
    return K.shot(WORLD, K.light_street, hx + 8 * un / 4, hy + 40 * un / 4, Z, acts=acts, fx_=snow_fx(t), sx=180, sy=300)


def r_count(t, u):
    acts = sit_scene(t, 8.2, 'ears', 'ears', tx=(775.0, 830.0), sip=True)
    return K.shot(WORLD, K.light_street, 695.0, 520.0, 1.35 + 0.1 * u, acts=acts, fx_=snow_fx(t), sy=340)


def r_window(t, u, who, prop, flip=False, shift=(0, 0)):
    return DK.window_cut(t, u, who, open_t=0.04, prop=prop, flip=flip, shift=shift)


def blast_pre(p):
    """fireball + debris under the chair (output px); p = seconds since the bomb went off"""
    def pre(big, v):
        cx, cy = v.opt(CH_X, 610.0)
        R = 1700.0 * sm(p / 0.5)
        fade = 1.0 - sm((p - 0.45) / 0.45)
        yy, xx = np.ogrid[:1920, :1080]
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        for frac, col in ((1.0, (150, 36, 24)), (0.84, (240, 100, 30)), (0.64, (255, 206, 64)), (0.40, (255, 248, 226))):
            m = d < R * frac * (0.55 + 0.45 * fade) if frac > 0.5 else d < R * frac * fade
            big[m] = (big[m] * (1 - 0.92 * fade) + np.array(col) * 0.92 * fade).astype(np.uint8)
        rng = np.random.default_rng(3)
        for i in range(46):
            a = rng.uniform(0, 2 * math.pi); sp = rng.uniform(500, 2100); sz = int(rng.integers(14, 40))
            px_ = int(cx + math.cos(a) * sp * p * 1.3); py_ = int(cy + math.sin(a) * sp * p * 1.0 + 520 * p * p)
            if 0 <= px_ < 1080 - sz and 0 <= py_ < 1920 - sz:
                big[py_:py_ + sz, px_:px_ + sz] = [(60, 54, 58), (250, 244, 232), (120, 84, 60), (200, 60, 40)][i % 4]
    return pre


def r_boom(t, u):
    p = t - BOOM_T
    un = 8.3
    soot = SOOT * sm(p / 0.35)
    acts = chair_acts(t, un, bomb=False) + [sit_dibs(t, un=un, expr='shock' if p < 0.2 else 'stunned', soot=soot), chair_sign(t, un)]
    flung = []
    if p > 0.04:
        q = p - 0.04
        flung = [lambda CH, v: PR.suv(CH, v.cam(830.0 + 900 * q, 706.0 - 1500 * q + 800 * q * q, max(1.0, 4.2 * (1 - 0.7 * q)), True), t),
                 lambda CH, v: PR.tank(CH, v.cam(400.0 - 800 * q, 696.0 - 1300 * q + 700 * q * q, max(1.0, 5.6 * (1 - 0.7 * q))), t, hatch=False)]
    def fx_(big, v):
        if p > 0.35:
            sm_ = sm((p - 0.35) / 0.4) * (1 - sm((p - 1.1) / 0.4))
            for i in range(14):
                ox, oy = v.opt(CH_X + (i - 7) * 46, 560 - ((i * 37) % 120) - 140 * p)
                B.puff(big, ox, oy, (150 + 40 * (i % 3)) * v.Z, 0.85 * sm_, (58, 54, 58))
        if 0.05 < p < 0.4: fx.vhs(big, t, 0.5)
    big = K.shot(WORLD, K.light_street, 680.0, 540.0, 1.15, acts=flung + acts, pre=blast_pre(max(0.0, p)), fx_=fx_, sy=340)
    if p < 0.12: O.flash(big, 1.0 - p / 0.12)
    if 0.02 < p < 0.9: B.shake(big, t, 26 * (1 - p / 0.9), 37)
    if 0.08 < p < 0.5: O.mosaic(big, int(1 + 56 * math.sin(math.pi * (p - 0.08) / 0.42)))
    return big


def crater_pre(smoke):
    def pre(big, v):
        cx, cy = v.opt(CH_X, 630.0)
        rx, ry = 380.0 * v.Z * 3, 100.0 * v.Z * 3
        yy, xx = np.ogrid[:1920, :1080]
        d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
        for lim, k in ((1.0, 0.55), (0.66, 0.78), (0.33, 0.9)):
            m = d < lim
            big[m] = (big[m] * (1 - k) + np.array((26, 22, 24)) * k).astype(np.uint8)
        rng = np.random.default_rng(8)
        for i in range(30):
            a = rng.uniform(0, 2 * math.pi); r = rng.uniform(0.3, 1.25)
            px_ = int(cx + math.cos(a) * rx * r); py_ = int(cy + math.sin(a) * ry * r); sz = int(rng.integers(10, 24))
            if 0 <= px_ < 1080 - sz and 0 <= py_ < 1920 - sz: big[py_:py_ + sz, px_:px_ + sz] = [(70, 64, 66), (110, 90, 80), (40, 36, 40)][i % 3]
        big[:] = (big * (1 - 0.30 * smoke) + np.array((60, 54, 56)) * 0.30 * smoke).astype(np.uint8)
    return pre


def smoke_fx(t, ax, ay, un, n=40):
    def fx_(big, v):
        snow_fx(t, n)(big, v)
        hx, hy = v.opt(ax + 1.0 * un, ay - 26 * un)
        for i in range(6):
            ph = (t * 0.9 + i / 6) % 1.0
            B.puff(big, hx + 24 * math.sin(i + t * 2) + 20 * ph, hy - 40 - 280 * ph, (40 + 90 * ph) * v.Z, 0.6 * (1 - ph), (70, 66, 70))
    return fx_


def r_crater(t, u, Z=1.5):
    un = 8.5
    ax, ay = sit_anchor(un)
    smoke = max(0.0, 1.0 - u / 2.2)
    acts = chair_acts(t, un, bomb=False) + [sit_dibs(t, un=un, expr='deadpan', mth=mouth('dibs', t, 1.8), soot=SOOT), chair_sign(t, un)]
    return K.shot(WORLD, K.light_street, 680.0, 540.0, Z + 0.05 * u, acts=acts, pre=crater_pre(smoke), fx_=smoke_fx(t, ax, ay, un), sy=350)


def r_van(t, u):
    k = sm(min(1.0, u / 0.75))
    x = lerp(985.0, 805.0, k)
    un = 8.0
    acts = chair_acts(t, un, bomb=False) + [sit_dibs(t, un=un, expr='deadpan', soot=SOOT), chair_sign(t, un),
            lambda CH, v: PR.minivan(CH, v.cam(x, 700.0, 5.0, True), t, rot=-x * 0.2, driver=False, blinker=True)]
    front = [A(DC.brad, x - 26.0, 706.0, un=3.6, flip=True, pose='wave' if u > 0.75 else 'stand', t=t, mouth_=mouth('brad', t, 1.7),
               expr='grin', legs=False, clip_h=50.0)]
    def fx_(big, v):
        snow_fx(t, 40)(big, v)
        if u < 0.9:
            for i in range(5):
                ph = u - i * 0.07
                if ph < 0: continue
                ox_, oy_ = v.opt(x + 80 + 16 * i, 706 - 40 * ph)
                B.puff(big, ox_, oy_, (22 + 40 * ph) * 3 * v.Z, 0.55 * max(0.0, 1 - ph / 0.9), (232, 238, 248))
    return K.shot(WORLD, K.light_street, 725.0, 540.0, 1.15, acts=acts, front=front, pre=crater_pre(0.0), fx_=fx_, sy=300)


def r_brad(t, u):
    pose = 'point' if u > 0.35 else 'wave'
    def emit(big, v):
        big[0:150, :] = (46, 52, 64); big[150:166, :] = (92, 102, 118)                          # van window frame (roof edge)
        big[1330:1920, :] = (196, 202, 214); big[1330:1350, :] = (46, 52, 64)                   # silver sliding door under the window
        big[1350:1362, :] = (232, 236, 244); big[1560:1572, :] = (150, 156, 170)
        big[1420:1470, 820:960] = (60, 64, 76); big[1428:1462, 828:952] = (120, 126, 140)         # door handle
        big[150:1330, 0:130] = (46, 52, 64); big[150:1330, 130:146] = (92, 102, 118)            # door pillar
    return cu(DC.brad, 'brad', t, u, 790.0, 430.0, Z=2.1, s=12.5, flip=True, k=1.7, pose=pose, expr='grin',
              legs=False, look=0.8, ting=max(0.0, 1.0 - abs(u - 0.25) / 0.2), emit=emit, fxn=40)


def r_dreact(t, u):
    return cu_dibs(t, u, 'deadpan', shades=True, soot=SOOT, Z=2.2, zoom=0.15, pre=crater_pre(0.0), fxn=40)


def r_marty(t, u):
    def pre(big, v):
        B.steam(big, v, t, 790.0, 586.0, n=7, rise=170, size=60, a=0.55)
    q = 1.0 + 0.025 * u
    Zt = CU_BG * q
    a = A(DC.marty, 800.0, 598.0, s=18.0 * q, t=t, mouth_=mouth('marty', t, 1.7), expr='deadpan', look=0.6, hires=True)
    return K.shot(WORLD, K.light_street, 800.0 + 12.0 * 2.0 / CU_BG, 598.0 - 88.0 * 2.0 / CU_BG, Zt, acts=[a], pre=pre, fx_=snow_fx(t, 40), sy=330)


def r_tail(t, u):
    Z = lerp(1.6, 1.15, sm(u / 1.7))
    un = 8.5
    acts = chair_acts(t, un, bomb=False) + [sit_dibs(t, un=un, expr='smug', soot=SOOT, sip=True), chair_sign(t, un)]
    return K.shot(WORLD, K.light_street, 680.0, 540.0, Z, acts=acts, pre=crater_pre(0.0), fx_=snow_fx(t, 60), sy=420)


# ================================================================== shot table
SHOTS = [
    (0.00, 1.30, 'hook'), (1.30, 4.40, 'insert'), (4.40, 6.80, 'd2'), (6.80, 8.60, 'deb2'), (8.60, 10.10, 'suv'), (10.10, 11.80, 'two'),
    (11.80, 13.40, 'd3'), (13.40, 14.95, 'gary'), (14.95, 16.90, 'sorry'), (16.90, 19.00, 'squad'), (19.00, 21.20, 'tank'),
    (21.20, 23.30, 'sit'), (23.30, 25.30, 'dsit'), (25.30, 25.95, 'count1'), (25.95, 26.45, 'win_pop'), (26.45, BOOM_T, 'count2'),
    (BOOM_T, 28.80, 'boom'), (28.80, 30.60, 'crater'), (30.60, 31.60, 'van'), (31.60, 31.97, 'w1'), (31.97, 32.34, 'w2'), (32.34, 32.70, 'w3'),
    (32.70, 33.95, 'brad'), (33.95, 34.40, 'dreact'), (34.40, 36.10, 'marty'), (36.10, DUR + 1, 'tail'),
]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name == 'hook': return r_hook(t, u)
    if name == 'insert': return r_insert(t, u)
    if name == 'd2': return cu_dibs(t, u, 'smug', shades=u > 0.35)
    if name == 'deb2': return r_deb(t, u, 'nervous' if u < 0.9 else 'smile')
    if name == 'suv': return r_suv(t, u)
    if name == 'two': return r_two(t, u)
    if name == 'd3': return cu_dibs(t, u, 'deadpan', zoom=0.08)
    if name == 'gary': return r_gary(t, u)
    if name == 'sorry': return r_sorry(t, u)
    if name == 'squad': return r_squad(t, u)
    if name == 'tank': return r_tank(t, u)
    if name == 'sit': return r_sit(t, u)
    if name == 'dsit': return r_dsit(t, u)
    if name in ('count1', 'count2'): return r_count(t, u)
    if name == 'win_pop': return r_window(t, u, 'rose', 'popcorn', True, shift=(0, 110))
    if name == 'boom': return r_boom(t, u)
    if name == 'crater': return r_crater(t, u)
    if name == 'van': return r_van(t, u)
    if name == 'w1': return r_window(t, u, 'mrs_w', 'binoculars')
    if name == 'w2': return r_window(t, u, 'rose', 'popcorn', True)
    if name == 'w3': return r_window(t, u, 'dot', 'binoculars')
    if name == 'brad': return r_brad(t, u)
    if name == 'dreact': return r_dreact(t, u)
    if name == 'marty': return r_marty(t, u)
    return r_tail(t, u)


# ================================================================== overlays
def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 1, ['DIBS ON', 'THE BOMB'], hook_t=(0.15, 2.4),
              stickers=[
                  (st('RESPECT +1', (130, 255, 160), 72), 16.35, 17.40, 540, 560),
                  (st('RESPECT +1', (130, 255, 160), 72), 18.00, 19.05, 540, 560),
                  (st('RESPECT +1', (130, 255, 160), 72), 20.20, 21.25, 540, 560),
                  (st('BOOM', (255, 214, 70), 190), 27.42, 28.30, 540, 760),
                  (st('BOMB: RESPECT 0', (255, 110, 110), 52), 29.50, 30.70, 540, 330),
                  (st('MARTY: INFORMANT (RAT)', (150, 255, 80), 34), 34.40, 35.60, 540, 430),
                  (st('NAPERVILLE: SUBURB.', (255, 255, 255), 34), 35.70, 37.20, 540, 420),
                  (st('28 MILES. DIFFERENT PLANET.', (255, 236, 120), 34), 35.90, 37.40, 540, 490),
              ],
              flashes=[], mosaics=[], cap_default=1400,
              cap_y={'hook': 1720, 'brad': 1460, 'van': 1180, 'insert': 1700, 'sit': 1450, 'crater': 1500, 'tail': 1500, 'boom': 1500, 'squad': 1450, 'tank': 1450, 'suv': 1450})


def render(t):
    big = render_scene(t)
    if 25.30 <= t < 25.9: K.digits(big, '3', 540, 440, 380, pulse=1.0 + 0.12 * math.sin((t - 25.3) * 14))
    if 25.95 <= t < 26.5: K.digits(big, '2', 540, 250, 300, pulse=1.0 + 0.12 * math.sin((t - 25.95) * 14))
    if 26.55 <= t < BOOM_T: K.digits(big, '1', 540, 440, 380, pulse=1.0 + 0.12 * math.sin((t - 26.55) * 14))
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
