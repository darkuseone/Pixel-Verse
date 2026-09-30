"""S01E01 «Самый быстрый» — HD-пересборка пилота на общем движке (xAI-задник + код-герои, свет, частицы), 9:16.
  python3 ep01.py test 1 5 20 | frame 12 | all [4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import math
import numpy as np
import stage as ST
from stage import View, view_at, Chars, Light, shadow, ell, OUT_W, OUT_H, UP
import scene as S
from scene import Layer, cap, dot, outline, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import chars as C
from props import pilot as PL
from timeline import DUR, FPS, VOICE

EPI = Episode('ep01', VOICE, DUR, FPS)
talk = EPI.talk
ROAD = ST.ai_world(P.series() / 'bg' / 'desert_road.png')

FEET = 588.0
U = 5.6
DU = U * 0.85
CACTUS_X = 1010.0
T_BRAKE, T_LAUNCH, T_LAND = 12.35, 12.55, 14.95
T_HAT = 2.3
CARROT_X = 800.0


def light():
    return Light(amb=(1.05, 0.97, 0.88), rim=(1, -1, (255, 236, 190), 0.45), grad=(1.06, 0.9))


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z)); return Chars(), Chars()


# ---------------------------------------------------------------- choreography (jump-cut crossings, camera follows)
RUNS = [(0.0, 2.4, 100, 300), (2.4, 5.4, 40, 320), (5.4, 7.6, 150, 300), (7.6, 9.8, 60, 330), (9.8, 11.6, 200, 300), (11.6, T_BRAKE, 480, 320)]


def mol_x(t):
    for a, b, x0, v in RUNS:
        if a <= t < b: return x0 + v * (t - a)
    xb = 480 + 320 * (T_BRAKE - 11.6)
    return xb + 24 * sm((t - T_BRAKE) / 0.3)


def mol_pose(t):
    if t < T_BRAKE:
        Pz, p = C.gallop(t)
        if 10.0 <= t < 11.6: Pz['jaw'] = min(talk('molniya', t) * 1.6, 1.0) * 0.8
        return Pz, p
    if t < T_BRAKE + 0.5:
        Pz = S.brake_pose(t); Pz.update(lid=0.1, ear=0.8); return Pz, 0.0
    chew = 17.4 <= t < 21.4 or t >= 32.4
    return C.molniya_pose(t, chew, talk('molniya', t)), 0.0


def sam_x(t):
    if 20.6 <= t < 26.2: return lerp(260, 690, sm((t - 20.6) / 2.7)) + (220 * (t - 23.5) if t > 23.5 else 0)
    return None


def sam_front_x(t):
    if 26.4 <= t < 30.6: return 1050 - 190 * (t - 26.4)
    return None


def billy_flight(t):
    Pz, _ = mol_pose(T_LAUNCH - 0.01)
    x0, y0 = C.rider_hip_world(mol_x(T_LAUNCH), FEET, U, Pz)
    x1, y1 = CACTUS_X, FEET - 14 * U
    k = min(1.0, max(0.0, (t - T_LAUNCH) / (T_LAND - T_LAUNCH)))
    return lerp(x0, x1, k), lerp(y0, y1, k) - 300 * math.sin(math.pi * k), -k * 6.28 * 1.25


def hat_pos(t):
    Pz, _ = mol_pose(T_LAUNCH - 0.01)
    x0, y0 = C.rider_hip_world(mol_x(T_LAUNCH), FEET, U, Pz)
    x0, y0 = x0 + 0.4 * U, y0 - 11.6 * U
    Pz2, _ = mol_pose(T_LAUNCH + 2.5)
    ax, ay = C.horse_anchor(mol_x(T_LAUNCH + 2.5), FEET, U)
    hp, _r = S.head_hat_anchor(1000.0, 1000.0, Pz2)
    x1, y1 = ax + (hp[0] - 1000) * U, ay + (hp[1] - 1000) * U
    k = min(1.0, max(0.0, (t - T_LAUNCH) / T_HAT))
    return lerp(x0, x1, k), lerp(y0, y1, k) - 200 * math.sin(math.pi * k), k * 9.0


def scene(CH, FX, big, v, t):
    fx.motes(FX, v, t, 0, 300, 1280, 700, n=36, seed=4)
    ev = []
    if t < T_BRAKE: ev += fx.gallop_dust(t, mol_x, FEET, max(0.0, t - 0.8), t, 8, 12)
    ev += [(T_BRAKE, mol_x(T_BRAKE) + 40, FEET, 26), (T_LAND, CACTUS_X, FEET, 22)]
    if sam_x(t) is not None: ev += fx.gallop_dust(t, sam_x, FEET - 12, max(20.6, t - 0.8), t, 5, 8)
    fx.dust_puffs(FX, v, t, ev)
    if t >= 11.0:
        PL.cactus_big(CH, v, CACTUS_X, FEET, 3.0 * math.exp(-(t - T_LAND) * 4) * math.sin((t - T_LAND) * 30) if t >= T_LAND else 0.0)
    x = sam_x(t)
    if x is not None:
        shadow(big, v, x, FEET - 12, 13 * DU, 1.6 * DU)
        C.donkey(CH, v.cam(x, FEET - 12 - 19 * DU, DU), t, moving=True, rider=C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t)))
    Pz, ph = mol_pose(t)
    mx = mol_x(t)
    shadow(big, v, mx, FEET, 16 * U, 1.8 * U)
    rider = None
    if t < T_LAUNCH:
        rider = PL.rider_hat(C.POSES['ride_whip'] if t < 10.0 else C.POSES['ride'], talk('billy', t), hat=True)
    ax, ay = C.horse_anchor(mx, FEET, U)
    C.molniya(CH, v.cam(ax, ay, U), t, Pz, rider=rider, p=ph, hat=t < T_LAUNCH or t >= T_LAUNCH + T_HAT,
              carrot=17.4 <= t < 21.0 or t >= 32.4)
    if 11.6 <= t < T_BRAKE + 0.3:
        L = Layer(v.wcam())
        cap(L, (CARROT_X, FEET - 6), (CARROT_X + 26, FEET - 12), 6.0, 2.0, (236, 128, 40), hi=(255, 176, 90))
        for a in (-0.5, 0.0, 0.5): cap(L, (CARROT_X, FEET - 6), (CARROT_X - 10 * math.cos(a), FEET - 6 - 10 * math.sin(a) - 4), 2.0, 1.1, (84, 160, 60))
        outline(L, (70, 40, 20)); CH.add(L)
        fx.embers(FX, v, CARROT_X + 12, FEET - 10, t, n=8, h=40, spread=30, col=((255, 250, 200), (255, 230, 150), (255, 255, 255)))
    if t >= T_LAUNCH:
        if t < T_LAND:
            bx, by, rot = billy_flight(t)
            C.billy(CH, v.cam(bx, by, U), S.pose_fly(t), rot, talk('billy', t), 'shout', hat=False)
        elif t < 26.3:
            hip = (CACTUS_X + 2, FEET - 14 * U)
            C.billy(CH, v.cam(hip[0], hip[1], U), C.POSES['shout'], -0.05, talk('billy', t), 'shout' if t < 17 else 'amazed', hat=False)
            if 15.6 <= t < 17.6:
                L = Layer(v.cam(hip[0], hip[1], U))
                for i in range(3):
                    a = t * 4 + i * 2.1
                    S.star(L, (1000.6 + 4.5 * math.cos(a), 1000 - 14.5 + 1.2 * math.sin(a)))
                CH.add(L)
        else:
            bx = 560.0
            shadow(big, v, bx, FEET, 5 * U, 1.2 * U)
            C.billy(CH, v.cam(bx, FEET - C.HIP_H * U, U), C.POSES['hips'] if t < 28.5 else C.POSES['point'], 0.05, talk('billy', t), 'normal', hat=False)
    if T_LAUNCH <= t < T_LAUNCH + T_HAT:
        hx, hy, hr = hat_pos(t)
        L = Layer(v.cam(hx, hy, U)); S.hat(L, (1000.0, 1000.0), hr); outline(L, (60, 40, 20)); CH.add(L)
    xf = sam_front_x(t)
    if xf is not None:
        duf = DU * 1.25
        shadow(big, v, xf, FEET + 50, 13 * duf, 1.6 * duf)
        C.donkey(CH, v.cam(xf, FEET + 50 - 19 * duf, duf, True), t, moving=True, rider=C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t)))


# ---------------------------------------------------------------- shots
SHOTS = [
    (0.0, 2.4, 'cu_billy'), (2.4, 5.4, 'wide1'), (5.4, 7.6, 'cu_billy2'), (7.6, 9.8, 'wide2'), (9.8, 11.6, 'cu_mol'),
    (11.6, T_LAUNCH, 'carrot'), (T_LAUNCH, T_LAND, 'flight'), (T_LAND, 17.4, 'cactus'), (17.4, 20.6, 'cu_mol_h1'),
    (20.6, 24.3, 'sam_pass'), (24.3, 26.2, 'cu_mol_sp'), (26.2, 30.4, 'two'), (30.4, 32.4, 'cu_mol_nea'), (32.4, DUR + 1, 'cu_mol_end'),
]
FLASH_AT = [T_LAUNCH, T_LAND, 26.2]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    def head(): return C.head_of_horse(mol_x(t), FEET, U, mol_pose(t)[0])
    def hip(): return C.rider_hip_world(mol_x(t), FEET, U, mol_pose(t)[0])
    if name in ('cu_billy', 'cu_billy2'):
        hx, hy = hip(); v = view_at(ROAD, hx + 4, hy - 56, 2.6 - 0.08 * u, 180, 400)
    elif name in ('wide1', 'wide2'):
        v = View(ROAD, mol_x(t) - 130, 60, 1.0)
    elif name in ('cu_mol', 'cu_mol_h1', 'cu_mol_sp', 'cu_mol_nea'):
        hx, hy = head(); v = view_at(ROAD, hx + 20, hy + 10, 3.0 + 0.05 * u, 180, 430)
    elif name == 'carrot':
        v = View(ROAD, mol_x(t) - 100, 60, 1.0)
    elif name == 'flight':
        k = sm(u / (T_LAND - T_LAUNCH)); v = view_at(ROAD, lerp(760, 960, k), 440, 0.95, 180, 400)
    elif name == 'cactus':
        v = view_at(ROAD, 880, 480, 1.15, 180, 400)
    elif name == 'sam_pass':
        sx = sam_x(t) or 700; v = view_at(ROAD, sx + 60, 500, 1.5, 180, 420)
    elif name == 'two':
        v = view_at(ROAD, 690, 500, 1.05, 180, 420)
    else:
        hx, hy = head(); v = view_at(ROAD, hx + 10, hy + 20, 2.7 - 0.04 * u, 180, 440)
    CH, FX = begin(v.Z)
    big = v.bg()
    scene(CH, FX, big, v, t)
    CH.comp(big, light()); FX.comp(big)
    fx.vignette(big, 0.3)
    if name in ('cu_billy', 'wide1', 'wide2', 'cu_billy2', 'cu_mol', 'carrot'): fx.speed_lines(big, t, 0.9)
    elif name == 'flight': fx.speed_lines(big, t, 0.6)
    return big


# ---------------------------------------------------------------- overlays
BADGE = O.make_badge('СЕЗОН 1 • СЕРИЯ 1/6')
HOOK = O.pixel_title(['САМЫЙ', 'БЫСТРЫЙ?'], 64)
TEASE = O.pixel_title(['СЕРИЯ 2 СКОРО'], 40)
STICKERS = [
    (O.sticker('3 ГОДА', fg=(255, 236, 120), size=64), 10.0, 11.5, 540, 560),
    (O.sticker('!', fg=(255, 120, 90), size=110), 11.65, 12.4, 540, 620),
    (O.sticker('ОЙ!', fg=(255, 236, 120), size=80), 15.1, 16.2, 540, 560),
    (O.sticker('+1', icon=C.carrot_icon(1, 7)), 17.7, 19.0, 540, 560),
]


def render(t):
    big = render_scene(t)
    for img, a, b, cx, cy in STICKERS: O.draw_sticker(big, img, t, a, b, cx, cy)
    O.overlay(big, BADGE, 36, 96, 1.0)
    if 0.2 <= t < 2.3:
        k = min(1.0, (t - 0.2) / 0.1) * (1 - sm((t - 2.1) / 0.2))
        O.overlay(big, HOOK, 0, 220, k)
    if t < 32.4: EPI.captions.draw(big, t, 780)
    if t >= 32.6: O.overlay(big, TEASE, 0, 1540, min(1.0, (t - 32.6) / 0.15))
    for fa in FLASH_AT:
        if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
    for m0 in (5.4, 9.8, 20.6, 26.2):
        if m0 <= t < m0 + 0.25: O.mosaic(big, int(lerp(40, 1, (t - m0) / 0.25)))
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
