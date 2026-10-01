"""S01E01 «Dibs» — Special Agent Dibs covers a bomb with his lawn chair and calls dibs. The villains, the bomb squad and a tank respect the
chair; the bomb does not, but the blast goes AROUND the chair. Brad from Naperville asks if the spot is open.
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
from props import chi_cast as C
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
CHU = 0.62                              # chair/bomb size relative to a person (a real lawn chair is ~half a man tall)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def snow_fx(t, n=70):
    return lambda big, v: K.snow(big, v, t, n)


def sit_anchor(un):
    """character anchor for Dibs sitting on the chair at (CH_X, CH_Y): hips on the seat, feet just above the ground"""
    return CH_X - 2.0 * un, CH_Y + 2.3 * un


# ================================================================== reusable pieces
def chair_bomb(t, un, ay=CH_Y, ax=CH_X, fuse=1.0, spark=None):
    """un = the chair's own unit (world px per unit)"""
    def bomb_(CH, v):
        sp = PR.bomb(CH, v.cam(ax, ay, un), t, fuse)
        if spark is not None: spark['p'] = (ax + sp[0] * un, ay - sp[1] * un)
    def chair_(CH, v): PR.dibs_chair(CH, v.cam(ax, ay, un), t=t)
    return [bomb_, chair_]


def spark_glow(spark, t, r=300, a=0.8):
    def emit(big, v):
        if 'p' in spark:
            ox, oy = v.opt(*spark['p'])
            fx.glow(big, ox, oy, r * v.Z / 2.0, (255, 150, 50), a * (0.8 + 0.2 * math.sin(t * 40)))
    return emit


def cu_dibs(t, u, expr, Z=2.3, shades=True, pose=None, dx=0.0, dy=0.0, zoom=0.06, hand=None, prop=None, k=1.8, ax=500.0, ay=646.0, un=13.0,
            extra=(), sit=False, soot=0.0, sy=262, front=(), emit=None, light=K.light_street):
    if sit: ax, ay = sit_anchor(un)
    Zt = Z + zoom * u
    acts = [lambda CH, v: C.dibs(CH, v.cam(ax, ay, un), pose or C.POSE['stand'], t, mouth('dibs', t, k), expr, 0.0, shades, chair=False,
                                 hand_n=hand, prop_n=prop, soot=soot)]
    return K.shot(WORLD, light, ax + 1.5 * un + dx, ay - 21.0 * un + dy, Zt, acts=list(extra) + acts, front=front, fx_=snow_fx(t), sx=180, sy=sy, emit=emit)


def cu_char(fn, who, ax, ay, un, hy, Z, t, u, expr, pose=None, flip=False, dx=0.0, dy=0.0, zoom=0.05, k=1.7, sy=262, **kw):
    Zt = Z + zoom * u
    sgn = -1 if flip else 1
    acts = [lambda CH, v: fn(CH, v.cam(ax, ay, un, flip), pose or C.POSE['stand'], t, mouth(who, t, k), expr, 0.0, **kw)]
    return K.shot(WORLD, K.light_street, ax + sgn * 1.5 * un + dx, ay - hy * un + dy, Zt, acts=acts, fx_=snow_fx(t), sx=180, sy=sy)


def standing_group(t, dibs_expr='smug', dibs_pose='hips', shades=True, chair=True, bomb=True):
    """Dibs next to the chair, as the base of the wide shots"""
    acts = []
    if bomb: acts.append(lambda CH, v: PR.bomb(CH, v.cam(CH_X, CH_Y, 6.8 * CHU), t))
    if chair: acts.append(lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X, CH_Y, 6.8 * CHU), t=t))
    acts.append(lambda CH, v: C.dibs(CH, v.cam(DB_X, CH_Y - 4, 6.8), C.POSE[dibs_pose], t, 0.0, dibs_expr, 0.0, shades, chair=False))
    return acts


# ================================================================== shots
def r_hook(t, u):
    un, ay = 13.0, 646.0
    fall = max(0.0, 1.0 - t / 0.10)
    sp = {}
    cu_ = un * CHU
    acts = [lambda CH, v: C.dibs(CH, v.cam(540.0, ay, un), C.POSE['reach'], t, mouth('dibs', t, 1.9), 'shout', 0.0, False, chair=False),
            lambda CH, v: spark_bomb(CH, v, sp, 640.0, ay, cu_, t),
            lambda CH, v: PR.dibs_chair(CH, v.cam(640.0, ay - fall * 520, cu_), t=t)]
    big = K.shot(WORLD, K.light_street, 552.0, 369.0, 1.7, acts=acts, emit=spark_glow(sp, t), fx_=snow_fx(t), sx=118, sy=160)
    if 0.10 <= t < 0.16: O.flash(big, 0.45)
    if 0.10 < t < 0.5: B.shake(big, t, 12 * max(0.0, 1 - (t - 0.10) / 0.4), 33)
    return big


def spark_bomb(CH, v, sp, ax, ay, un, t, fuse=1.0):
    q = PR.bomb(CH, v.cam(ax, ay, un), t, fuse)
    sp['p'] = (ax + q[0] * un, ay - q[1] * un)


def r_insert(t, u):
    cu_ = 12.0
    sp = {}
    acts = [lambda CH, v: spark_bomb(CH, v, sp, CH_X + 20.0, 646.0, cu_, t), lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X + 20.0, 646.0, cu_), t=t)]
    big = K.shot(WORLD, K.light_street, CH_X + 20.0, 540.0, 1.5 + 0.10 * u, acts=acts, emit=spark_glow(sp, t, 360), fx_=snow_fx(t), sx=180, sy=330)
    K.deb_window(big, t, 'smile' if u < 1.5 else 'nervous', mouth('deb', t, 1.6), box=(690, 390, 1030, 730))
    return big


def r_deb(t, u, expr='smile'):
    return K.deb_frame(t, expr, mouth('deb', t, 1.6), Z=2.0, u=u)


def r_suv(t, u):
    k = min(1.0, u / 0.85)
    x = lerp(1180.0, 810.0, 1 - (1 - k) ** 2)
    acts = standing_group(t)
    acts += [lambda CH, v: PR.suv(CH, v.cam(x, 706.0, 4.2, True), t, rot=-x * 0.25, shake=0.4 if k < 1 else 0.0)]
    if u > 0.9:
        acts += [lambda CH, v: C.terry(CH, v.cam(735.0, 668.0, 6.8, True), C.POSE['stand'], t, 0.0, 'nervous'),
                 lambda CH, v: C.gary(CH, v.cam(695.0, 672.0, 6.8, True), C.POSE['stand'], t, 0.0, 'normal')]
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


def card_prop(t):
    return lambda L, h: PR.cue_card(L, h, -0.2)


def r_two(t, u):
    show_card = 0.45 < u < 1.05
    acts = [lambda CH, v: PR.bomb(CH, v.cam(CH_X - 10, 678.0, 6.8 * CHU * 1.3), t),
            lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X - 10, 678.0, 6.8 * CHU * 1.3), t=t),
            lambda CH, v: C.gary(CH, v.cam(790.0, 668.0, 8.4, True), C.POSE['stand'], t, 0.0, 'nervous', shades=True),
            lambda CH, v: C.terry(CH, v.cam(728.0, 664.0, 9.0, True), C.POSE['reach'], t, mouth('terry', t, 1.7), 'nervous',
                                  prop_f=card_prop(t) if show_card else None, hand_f=C.H(1.0, 17.0) if show_card else None, shades=True)]
    return K.shot(WORLD, K.light_street, 705.0, 540.0, 1.35 + 0.1 * u, acts=acts, fx_=snow_fx(t), sy=340)


def r_gary(t, u):
    return cu_char(C.gary, 'gary', 790.0, 662.0, 13.0, 19.6, 2.3, t, u, 'nervous', flip=True, k=1.6)


def r_sorry(t, u):
    k = sm(u / 1.2)
    acts = [lambda CH, v: PR.bomb(CH, v.cam(CH_X + 10, CH_Y, 8.0 * CHU), t), lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X + 10, CH_Y, 8.0 * CHU), t=t),
            lambda CH, v: C.gary(CH, v.cam(lerp(780.0, 850.0, k), 670.0, 8.0, True), C.POSE['hat'], t, 0.0, 'nervous',
                                 prop_n=PR.hat_in_hand, hand_n=C.H(3.8, 12.5)),
            lambda CH, v: C.terry(CH, v.cam(lerp(720.0, 790.0, k), 664.0, 8.4, True), C.POSE['hat'], t, mouth('terry', t, 1.8), 'nervous',
                                  prop_n=PR.hat_in_hand, hand_n=C.H(3.8, 12.5))]
    return K.shot(WORLD, K.light_street, 725.0, 520.0, 1.35, acts=acts, fx_=snow_fx(t), sy=340)


def r_squad(t, u):
    k = sm(min(1.0, u / 0.6))
    tx = lerp(1250.0, 850.0, 1 - (1 - k) ** 2)
    ofl = u < 1.35
    helmet = u < 1.3
    ox = 800.0 - 130.0 * sm(min(1.0, max(0.0, (u - 0.45) / 0.65))) + 130.0 * sm(min(1.0, max(0.0, (u - 1.5) / 0.5)))
    rx = 800.0 - 130.0 * sm(min(1.0, max(0.0, (u - 0.5) / 0.7))) + 140.0 * sm(min(1.0, max(0.0, (u - 1.5) / 0.55)))
    acts = standing_group(t)
    acts += [lambda CH, v: PR.squad_truck(CH, v.cam(tx, 706.0, 4.2, True), t, rot=-tx * 0.25)]
    if u > 0.45:
        acts += [lambda CH, v: PR.puffer_person(CH, v.cam(ox, 668.0, 7.4, ofl), (24, 60, 140), (240, 240, 246), t, phase=1.0, hat_on=helmet, look=-1 if ofl else 1)]
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


def sit_scene(t, un, terry_pose, gary_pose, tprop, gprop, expr='smug', hand=None, prop=PR.coffee_cup, soot=0.0, extra=(), mth=0.0, tx=(780.0, 835.0)):
    ax, ay = sit_anchor(un)
    cu_ = un * CHU
    acts = [lambda CH, v: PR.bomb(CH, v.cam(CH_X, CH_Y, cu_), t), lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X, CH_Y, cu_), t=t),
            lambda CH, v: C.dibs(CH, v.cam(ax, ay, un), C.POSE['sit'], t, mth, expr, 0.0, True, chair=False, hand_n=hand or C.H(5.4, 14.4), prop_n=prop, soot=soot),
            lambda CH, v: C.terry(CH, v.cam(tx[0], 668.0, un, True), terry_pose, t, 0.0, 'panic' if terry_pose is C.POSE['ears'] else 'nervous', prop_n=tprop),
            lambda CH, v: C.gary(CH, v.cam(tx[1], 672.0, un * 0.95, True), gary_pose, t, 0.0, 'panic' if gary_pose is C.POSE['ears'] else 'nervous', prop_n=gprop)]
    return acts + list(extra)


def r_sit(t, u):
    acts = sit_scene(t, 8.5, C.POSE['ears'] if u > 1.2 else C.POSE['hat'], C.POSE['ears'] if u > 1.3 else C.POSE['hat'],
                     None if u > 1.2 else PR.hat_in_hand, None if u > 1.3 else PR.hat_in_hand, tx=(780.0, 835.0))
    big = K.shot(WORLD, K.light_street, 700.0, 520.0, 1.55, acts=acts, fx_=snow_fx(t), sy=340)
    K.deb_window(big, t, 'panic', mouth('deb', t, 1.7), box=(650, 190, 1010, 550))
    return big


def r_dsit(t, u):
    s = sm((u - 1.3) / 0.4)
    hand = C.H(lerp(5.4, 3.4, s), lerp(12.6, 17.8, s))
    un = 13.0
    ax, ay = sit_anchor(un)
    cu_ = un * CHU
    acts = [lambda CH, v: PR.bomb(CH, v.cam(CH_X, CH_Y, cu_), t), lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X, CH_Y, cu_), t=t),
            lambda CH, v: C.dibs(CH, v.cam(ax, ay, un), C.POSE['sit'], t, mouth('dibs', t, 1.8), 'smug', 0.0, True, chair=False, hand_n=hand, prop_n=PR.coffee_cup)]
    return K.shot(WORLD, K.light_street, ax + 1.5 * un, ay - 21.0 * un - 10, 2.1 + 0.06 * u, acts=acts, fx_=snow_fx(t), sx=180, sy=300)


def r_count(t, u):
    acts = sit_scene(t, 8.2, C.POSE['ears'], C.POSE['ears'], None, None, hand=C.H(3.4, 17.6), tx=(775.0, 830.0))
    return K.shot(WORLD, K.light_street, 695.0, 520.0, 1.35 + 0.1 * u, acts=acts, fx_=snow_fx(t), sy=340)


def r_window(t, u, who, prop, flip=False):
    return K.window_cut(t, u, who, open_t=0.04, prop=prop, flip=flip)


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
    ax, ay = sit_anchor(un)
    cu_ = un * CHU
    soot = sm(p / 0.35)
    acts = [lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X, CH_Y, cu_), t=t),
            lambda CH, v: C.dibs(CH, v.cam(ax, ay, un), C.POSE['sit'], t, 0.0, 'shock' if p < 0.2 else 'stunned', 0.0, True, chair=False,
                                 hand_n=C.H(5.4, 14.4), prop_n=PR.coffee_cup, soot=soot)]
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


def r_crater(t, u, Z=1.5):
    un = 8.5
    ax, ay = sit_anchor(un)
    cu_ = un * CHU
    smoke = max(0.0, 1.0 - u / 2.2)
    acts = [lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X, CH_Y, cu_), t=t),
            lambda CH, v: C.dibs(CH, v.cam(ax, ay, un), C.POSE['sit'], t, mouth('dibs', t, 1.8), 'deadpan', 0.0, True, chair=False,
                                 hand_n=C.H(5.4, 14.4), prop_n=PR.coffee_cup, soot=0.88)]
    def fx_(big, v):
        snow_fx(t, 40)(big, v)
        hx, hy = v.opt(ax + 1.0 * un, ay - 26 * un)
        for i in range(6):
            ph = (t * 0.9 + i / 6) % 1.0
            B.puff(big, hx + 24 * math.sin(i + t * 2) + 20 * ph, hy - 40 - 280 * ph, (40 + 90 * ph) * v.Z, 0.6 * (1 - ph), (70, 66, 70))
    return K.shot(WORLD, K.light_street, 680.0, 540.0, Z + 0.05 * u, acts=acts, pre=crater_pre(smoke), fx_=fx_, sy=350)


def r_van(t, u):
    k = sm(min(1.0, u / 1.0))
    x = lerp(1160.0, 880.0, k)
    un = 8.0
    ax, ay = sit_anchor(un)
    cu_ = un * CHU
    acts = [lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X, CH_Y, cu_), t=t),
            lambda CH, v: C.dibs(CH, v.cam(ax, ay, un), C.POSE['sit'], t, 0.0, 'deadpan', 0.0, True, chair=False, hand_n=C.H(5.4, 14.4), prop_n=PR.coffee_cup, soot=0.88),
            lambda CH, v: PR.minivan(CH, v.cam(x, 700.0, 5.0, True), t, rot=-x * 0.2, driver=False, blinker=True),
            lambda CH, v: C.brad(CH, v.cam(x - 5.2 * 5.0 * 0.0 - 1.0 * 5.0 * 0.0 + 4.3 * 5.0 * 0.0 + (5.0 * 5.2) * 0.0 - 26.0, 700.0, 3.1, True),
                                 dict(C.POSE['hold'], n=(5.2, 14.4), f=(4.4, 14.6)), t, mouth('brad', t, 1.7), 'grin', 0.0, legs=False, clip_h=16.0)]
    return K.shot(WORLD, K.light_street, 740.0, 540.0, 1.15, acts=acts, pre=crater_pre(0.0), fx_=snow_fx(t, 40), sy=350)


def r_brad(t, u):
    Zt = 2.3 + 0.05 * u
    un = 13.0
    acts = [lambda CH, v: C.brad(CH, v.cam(800.0, 700.0, un, True), C.POSE['hold'], t, mouth('brad', t, 1.7), 'ope' if u > 0.3 else 'grin', legs=False, look=-0.8)]
    def emit(big, v):
        big[0:140, :] = (60, 66, 76)                                                            # van roof edge
        big[1560:1920, 0:150] = (60, 66, 76)                                                    # door pillar
    return K.shot(WORLD, K.light_street, 800.0 - 1.5 * un, 700.0 - 21.0 * un, Zt, acts=acts, fx_=snow_fx(t, 40), sx=180, sy=262, emit=emit)


def r_dreact(t, u):
    un = 13.0
    ax, ay = sit_anchor(un)
    cu_ = un * CHU
    acts = [lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X, CH_Y, cu_), t=t),
            lambda CH, v: C.dibs(CH, v.cam(ax, ay, un), C.POSE['sit'], t, 0.0, 'deadpan', 0.0, True, chair=False, hand_n=C.H(5.4, 14.4), prop_n=PR.coffee_cup, soot=0.88)]
    return K.shot(WORLD, K.light_street, ax + 1.5 * un, ay - 21.0 * un - 10, 2.2 + 0.15 * u, acts=acts, pre=crater_pre(0.0), fx_=snow_fx(t, 40), sx=180, sy=300)


def r_marty(t, u):
    Zt = 2.0 + 0.05 * u
    un = 10.0
    ax, ay = 800.0, 598.0
    acts = [lambda CH, v: C.marty(CH, v.cam(ax, ay, un), t, mouth('marty', t, 1.7), 'deadpan', (0.7, 0.0), fry=False)]
    def fx_(big, v):
        B.steam(big, v, t, 790.0, 586.0, n=7, rise=170, size=60, a=0.55)
        snow_fx(t, 40)(big, v)
    return K.shot(WORLD, K.light_street, ax + 3.0 * un, ay - 9.0 * un, Zt, acts=acts, fx_=fx_, sy=330)


def r_tail(t, u):
    Z = lerp(1.9, 1.15, sm(u / 1.7))
    un = 8.5
    ax, ay = sit_anchor(un)
    cu_ = un * CHU
    acts = [lambda CH, v: PR.dibs_chair(CH, v.cam(CH_X, CH_Y, cu_), t=t),
            lambda CH, v: C.dibs(CH, v.cam(ax, ay, un), C.POSE['sit'], t, 0.0, 'smug', 0.0, True, chair=False, hand_n=C.H(3.4, 17.8), prop_n=PR.coffee_cup, soot=0.88)]
    return K.shot(WORLD, K.light_street, 680.0, 540.0, Z, acts=acts, pre=crater_pre(0.0), fx_=snow_fx(t, 60), sy=350)


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
    if name == 'd2': return cu_dibs(t, u, 'smug', Z=2.3, shades=u > 0.35, zoom=0.07)
    if name == 'deb2': return r_deb(t, u, 'nervous' if u < 0.9 else 'smile')
    if name == 'suv': return r_suv(t, u)
    if name == 'two': return r_two(t, u)
    if name == 'd3': return cu_dibs(t, u, 'deadpan', Z=2.25, zoom=0.08)
    if name == 'gary': return r_gary(t, u)
    if name == 'sorry': return r_sorry(t, u)
    if name == 'squad': return r_squad(t, u)
    if name == 'tank': return r_tank(t, u)
    if name == 'sit': return r_sit(t, u)
    if name == 'dsit': return r_dsit(t, u)
    if name in ('count1', 'count2'): return r_count(t, u)
    if name == 'win_pop': return r_window(t, u, 'rose', 'popcorn', True)
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
                  (st('BOMB: RESPECT 0', (255, 110, 110), 52), 29.50, 30.70, 540, 700),
                  (st('MARTY: INFORMANT (RAT)', (150, 255, 80), 34), 34.40, 35.60, 540, 1090),
                  (st('NAPERVILLE: SUBURB.', (255, 255, 255), 34), 35.70, 37.20, 540, 1020),
                  (st('28 MILES. DIFFERENT PLANET.', (255, 236, 120), 34), 35.90, 37.40, 540, 1090),
              ],
              flashes=[], mosaics=[], cap_default=1400,
              cap_y={'insert': 1450, 'sit': 1450, 'crater': 1500, 'tail': 1500, 'boom': 1500, 'squad': 1450, 'tank': 1450, 'suv': 1450})


def render(t):
    big = render_scene(t)
    if 25.30 <= t < 25.9: K.digits(big, '3', 540, 760, 420, pulse=1.0 + 0.12 * math.sin((t - 25.3) * 14))
    if 25.95 <= t < 26.5: K.digits(big, '2', 540, 760, 420, pulse=1.0 + 0.12 * math.sin((t - 25.95) * 14))
    if 26.55 <= t < BOOM_T: K.digits(big, '1', 540, 760, 420, pulse=1.0 + 0.12 * math.sin((t - 26.55) * 14))
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
