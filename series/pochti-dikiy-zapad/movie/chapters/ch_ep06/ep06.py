"""S01E06 «Самый быстрый. Реванш» — season finale. xAI backgrounds (race_finish + reused canyon), heroes lit into them.
  python3 ep06.py test 1 5 20 | frame 12 | all [4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[5] / 'engine'))
import paths as P
import math
import numpy as np
import stage as ST
from widecam import View, view_at, halves
from stage import Chars, Light, shadow, ell, wrect, px_text, OUT_W, OUT_H, UP
import scene as S
from scene import Layer, cap, dot, outline, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import chars as C
from props import frontier as FR
from props import racetrack as R
from timeline import DUR, FPS, VOICE

EPI = Episode('ep06', VOICE, DUR, FPS)
talk = EPI.talk
FIN = R.build()['finish']
CANYON = FR.build()['canyon']

U = 6.0                 # heroes at the finish
DU = U * 0.85           # donkey
START_M, START_S = 560.0, 770.0
CARROT = (548.0, R.FEET + 4)
T_BRAKE, T_LAUNCH, T_LAND = 25.0, 25.2, 27.6
SACK_HANG = (645.0, 300.0)
T_SACK_HIT, T_SACK_LAND = 25.95, 36.55


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def light(scene):
    if scene == 'canyon':
        return Light(amb=(1.06, 0.95, 0.83), rim=(1, -1, (255, 232, 170), 0.5), grad=(1.08, 0.86))
    return Light(amb=(1.05, 0.97, 0.88), rim=(1, -1, (255, 236, 190), 0.45), grad=(1.06, 0.9))


def finish_fx(big, v, t, FX, sunset=0.0):
    FX.comp(big)
    fx.vignette(big, 0.3)
    if sunset > 0: fx.grade(big, (1 + 0.08 * sunset, 1 - 0.06 * sunset, 1 - 0.18 * sunset))


# ---------------------------------------------------------------- finish choreography
def mol_x(t):
    if t < 22.0: return START_M
    if t < T_BRAKE: return -120 + 197 * (t - 22.0)
    return -120 + 197 * (T_BRAKE - 22.0) + 24 * sm((t - T_BRAKE) / 0.3)

def mol_pose(t):
    if 22.0 <= t < T_BRAKE:
        return C.gallop(t)
    if T_BRAKE <= t < T_BRAKE + 0.5:
        Pz = S.brake_pose(t); Pz.update(lid=0.1, ear=0.8); return Pz, 0.0
    chew = t >= 33.0
    Pz = C.molniya_pose(t, chew, talk('molniya', t))
    if 32.9 <= t < 34.8: Pz['neck'] = lerp(Pz['neck'], 0.35, sm((t - 32.9) / 0.3) * (1 - sm((t - 34.5) / 0.3))); Pz['head'] = 1.3
    if t < 15.4: Pz['ear'] = 0.6
    return Pz, 0.0

def billy_flight(t):
    """(x, hip_y, rot) of Billy flying from the saddle to the cactus"""
    Pz, _ = mol_pose(T_LAUNCH - 0.01)
    x0, y0 = C.rider_hip_world(mol_x(T_LAUNCH), R.FEET, U, Pz)
    x1, y1 = R.CACTUS_X, R.FEET - 14 * U
    k = min(1.0, max(0.0, (t - T_LAUNCH) / (T_LAND - T_LAUNCH)))
    return lerp(x0, x1, k), lerp(y0, y1, k) - 300 * math.sin(math.pi * k), -k * 6.28 * 1.25

def hat_pos(t):
    """hat: on Molniya until launch, then flies onto Billy in the cactus"""
    Pz, _ = mol_pose(T_LAUNCH - 0.01)
    ax, ay = C.horse_anchor(mol_x(T_LAUNCH), R.FEET, U)
    hp, _ = S.head_hat_anchor(1000.0, 1000.0, Pz)
    x0, y0 = ax + (hp[0] - 1000) * U, ay + (hp[1] - 1000) * U
    x1, y1 = R.CACTUS_X + 0.8 * U, R.FEET - 14 * U - 11.9 * U
    k = min(1.0, max(0.0, (t - T_LAUNCH) / 2.7))
    return lerp(x0, x1, k), lerp(y0, y1, k) - 220 * math.sin(math.pi * k), k * 9.0

def sam_finish_x(t): return lerp(-100, 300, sm((t - 29.8) / 1.2))

def draw_cactus(CH, v, t):
    L = Layer(v.cam(R.CACTUS_X, R.FEET + 8, 7.0))
    wob = 3.0 * math.exp(-(t - T_LAND) * 4) * math.sin((t - T_LAND) * 30) if t >= T_LAND else 0.0
    S.cactus(L, 1000.0, 1000.0, wob)
    outline(L, (40, 72, 36)); CH.add(L)

def draw_prize_sack(CH, v, t):
    L = Layer(v.wcam())
    if t < T_SACK_HIT:
        cap(L, (SACK_HANG[0], 262), (SACK_HANG[0], SACK_HANG[1] - 14), 1.5, 1.5, (120, 90, 60))
        x, y = SACK_HANG
    elif t < T_SACK_HIT + 0.8:
        k = (t - T_SACK_HIT) / 0.8; x, y = SACK_HANG[0] + 180 * k, SACK_HANG[1] - 500 * k      # knocked into the sky
    elif t < T_SACK_LAND - 0.3:
        return
    elif t < T_SACK_LAND:
        k = (t - (T_SACK_LAND - 0.3)) / 0.3; x, y = R.CACTUS_X + 10, lerp(-200, R.FEET - 14 * U - 60, k * k)
    else:
        x, y = R.CACTUS_X + 44, R.FEET - 16
    ell(L, (x, y), 17, 15, (216, 188, 128), hi=(238, 214, 160), sh=(186, 158, 104))
    cap(L, (x, y - 15), (x, y - 21), 4, 6, (216, 188, 128)); cap(L, (x - 6, y - 14), (x + 6, y - 14), 1.6, 1.6, (140, 100, 60))
    outline(L, (70, 50, 30)); CH.add(L)
    if v.Z >= 1.5 and not (T_SACK_HIT + 0.8 <= t < T_SACK_LAND - 0.3):
        sx, sy = v.pt(x, y + 2)
        px_text(CH, '$', sx, sy, 16 if ST.PX[0] == 1 else 8, (90, 60, 30))

def ribbon(CH, v, t):
    L = Layer(v.wcam())
    y = 334
    if t < T_SACK_HIT:
        for i in range(10):
            a0, a1 = i / 10, (i + 1) / 10
            cap(L, (lerp(R.GATE[0], R.GATE[1], a0), y + 10 * math.sin(math.pi * a0)),
                (lerp(R.GATE[0], R.GATE[1], a1), y + 10 * math.sin(math.pi * a1)), 2.2, 2.2, (210, 40, 40))
    else:
        k = min(1.0, (t - T_SACK_HIT) / 0.5)
        for side, x0 in ((0, R.GATE[0]), (1, R.GATE[1])):
            d = 1 if side == 0 else -1
            cap(L, (x0, y), (x0 + d * 60 * (1 - k), y + 80 * k), 2.2, 2.2, (210, 40, 40))
    outline(L, (90, 20, 20)); CH.add(L)

CONF = np.random.default_rng(3).random((70, 4))
def confetti(FX, v, t, t0=T_SACK_HIT, cx=645, cy=330):
    if not (t0 <= t < t0 + 2.2): return
    u = t - t0; L = Layer(v.wcam())
    cols = [(255, 80, 80), (255, 220, 80), (80, 200, 255), (120, 230, 120), (255, 140, 220)]
    for i, (a, b, c, d) in enumerate(CONF):
        ang = a * 2 * math.pi; spd = 120 + 160 * b
        x = cx + math.cos(ang) * spd * u + 10 * math.sin(u * 8 + i); y = cy + math.sin(ang) * spd * u * 0.6 + 160 * u * u
        if u < 2.0: dot(L, (x, y), cols[i % 5], 1.6 + c)
    FX.add(L)

def coin_sparks(FX, v, t):
    if T_SACK_LAND <= t < T_SACK_LAND + 1.2:
        fx.embers(FX, v, R.CACTUS_X + 44, R.FEET - 20, t, n=18, h=90, spread=50,
                  col=((255, 236, 120), (255, 210, 80), (255, 250, 200)))

def finish_scene(CH, FX, big, v, t, parts=('mol', 'sam', 'billy', 'props')):
    fx.motes(FX, v, t, 0, 150, 1280, 640, n=40, seed=5)
    if 'props' in parts:
        ribbon(CH, v, t)
        if t >= 22.0:
            L = Layer(v.wcam())                                                             # carrot on the track (bait)
            if t < 33.0:
                cap(L, CARROT, (CARROT[0] + 22, CARROT[1] - 4), 5.5, 1.8, (236, 128, 40), hi=(255, 176, 90))
                for a in (-0.5, 0.0, 0.5): cap(L, CARROT, (CARROT[0] - 9 * math.cos(a), CARROT[1] - 9 * math.sin(a) - 3), 1.8, 1.0, (84, 160, 60))
            outline(L, (70, 40, 20)); CH.add(L)
            if t < 25.0:
                fx.embers(FX, v, CARROT[0] + 10, CARROT[1], t, n=8, h=40, spread=30, col=((255, 250, 200), (255, 230, 150), (255, 255, 255)))
        draw_prize_sack(CH, v, t)
        confetti(FX, v, t); coin_sparks(FX, v, t)
    # dust
    ev = []
    if 22.0 <= t < 25.6: ev += fx.gallop_dust(t, mol_x, R.FEET, max(22.0, t - 0.8), min(t, T_BRAKE), 8, 12)
    ev += [(T_BRAKE, mol_x(T_BRAKE) + 40, R.FEET, 26), (T_LAND, R.CACTUS_X, R.FEET, 22)]
    if 29.8 <= t < 31.5: ev += fx.gallop_dust(t, sam_finish_x, R.FEET - 14, max(29.8, t - 0.8), min(t, 31.0), 5, 8)
    fx.dust_puffs(FX, v, t, ev)
    # Sam
    if 'sam' in parts:
        if t < 15.4: sx, feet, mv = START_S, R.FEET - 16, False
        elif t >= 29.8: sx, feet, mv = sam_finish_x(t), R.FEET - 14, t < 31.0
        else: sx = None
        if sx is not None:
            shadow(big, v, sx, feet, 13 * DU, 1.6 * DU)
            C.donkey(CH, v.cam(sx, feet - 19 * DU, DU), t, moving=mv,
                     rider=C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t)))
    # Molniya (+ Billy riding before the launch)
    if 'mol' in parts and (t < 15.4 or t >= 22.0):
        Pz, ph = mol_pose(t)
        mx = mol_x(t)
        shadow(big, v, mx, R.FEET, 16 * U, 1.8 * U)
        rider = None
        if t < T_LAUNCH:
            pose = C.POSES['lean'] if 8.6 <= t < 12.3 else C.POSES['ride']
            rider = C.rider_billy(pose, talk('billy', t))
        ax, ay = C.horse_anchor(mx, R.FEET, U)
        C.molniya(CH, v.cam(ax, ay, U), t, Pz, rider=rider, p=ph, hat=t < T_LAUNCH, carrot=t >= 33.0)
    # Billy flying / in the cactus, hat
    if 'billy' in parts and t >= T_LAUNCH:
        if t < T_LAND:
            bx, by, rot = billy_flight(t)
            C.billy(CH, v.cam(bx, by, U), S.pose_fly(t), rot, talk('billy', t), 'shout')
        else:
            draw_cactus(CH, v, t)
            hip = (R.CACTUS_X + 2, R.FEET - 14 * U)
            hat_on = t >= T_LAUNCH + 2.7
            C.billy(CH, v.cam(hip[0], hip[1], U), C.POSES['shout'], -0.05, talk('billy', t),
                    'shout' if t < 30 else 'amazed', hat=hat_on)
            if t >= 36.6:                                                                    # dizzy stars
                L = Layer(v.cam(hip[0], hip[1], U))
                for i in range(3):
                    a = t * 4 + i * 2.1
                    S.star(L, (1000.6 + 4.5 * math.cos(a), 1000 - 14.5 + 1.2 * math.sin(a)))
                CH.add(L)
        if t < T_LAUNCH + 2.7:
            hx, hy, hr = hat_pos(t)
            L = Layer(v.cam(hx, hy, U)); S.hat(L, (1000.0, 1000.0), hr); outline(L, (60, 40, 20)); CH.add(L)
    if 'billy' in parts and t < T_LAUNCH and t >= 22.0:
        pass
    if 'billy' in parts and t >= T_LAND - 0.01 and 'props' not in parts:
        pass


def canyon_x(t, who):
    return 300 + 120 * (t - 15.4) if who == 'sam' else 40 + 190 * (t - 15.4)

def canyon_scene(CH, FX, big, v, t, only=None):
    feet = FR.CANYON_FEET
    fx.dust_puffs(FX, v, t, fx.gallop_dust(t, lambda tt: canyon_x(tt, 'mol'), feet, max(15.4, t - 0.8), t, 8, 10) +
                  fx.gallop_dust(t, lambda tt: canyon_x(tt, 'sam'), feet, max(15.4, t - 0.8), t, 5, 7))
    fx.motes(FX, v, t, 400, 120, 1100, 560, n=50, seed=3)
    if only in (None, 'sam'):
        x = canyon_x(t, 'sam'); du = 5.0 * 0.85
        shadow(big, v, x, feet, 13 * du, 1.6 * du)
        C.donkey(CH, v.cam(x, feet - 19 * du, du), t, moving=True, speed=2.4,
                 rider=C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t)))
    if only in (None, 'mol'):
        x = canyon_x(t, 'mol'); Pz, ph = C.gallop(t)
        shadow(big, v, x, feet, 16 * 5.0, 1.8 * 5.0)
        pose = C.POSES['heroic'] if 17.6 <= t < 19.2 else C.POSES['ride']
        ax, ay = C.horse_anchor(x, feet, 5.0)
        C.molniya(CH, v.cam(ax, ay, 5.0), t, Pz, rider=C.rider_billy(pose, talk('billy', t)), p=ph)


# ---------------------------------------------------------------- shots
SHOTS = [
    (0.00, 2.60, 'face_split'), (2.60, 4.90, 'cu_sam_start'), (4.90, 6.50, 'cu_mol_side'), (6.50, 8.60, 'wide_start'),
    (8.60, 10.50, 'cu_billy_whisper'), (10.50, 12.40, 'two_whisper'), (12.40, 14.20, 'cu_mol_cam'), (14.20, 15.40, 'countdown'),
    (15.40, 17.60, 'split_race'), (17.60, 19.60, 'wide_canyon'), (19.60, 22.00, 'cu_sam_race'), (22.00, 23.80, 'finish_wide'),
    (23.80, 25.20, 'cu_mol_carrot'), (25.20, 27.60, 'flight'), (27.60, 30.00, 'cu_billy_cactus'), (30.00, 32.60, 'sam_arrives'),
    (32.60, 35.30, 'two_sam_mol'), (35.30, 37.40, 'sack_fall'), (37.40, 39.30, 'cu_billy_hat'), (39.30, 41.20, 'wide_cactus'),
    (41.20, 45.00, 'cu_mol_final'), (45.00, DUR + 1, 'endcard'),
]
FLASH_AT = [0.0, 15.4, 22.0, 36.55]

def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]

def billy_head_start(t):
    Pz, _ = mol_pose(t)
    hx, hy = C.rider_hip_world(START_M, R.FEET, U, Pz)
    return hx + 0.6 * U, hy - 9.7 * U

def sam_head(x, feet, du=DU):
    return x - 0.2 * du, feet - 19 * du - 9.0 * du - 9.7 * U

def render_finish(name, t, u):
    if name == 'face_split':
        hx, hy = billy_head_start(t)
        vt = view_at(FIN, hx, hy + 10, 3.0, 180, 190, hlog=320)
        sx, sy = sam_head(START_S, R.FEET - 16)
        vb = view_at(FIN, sx, sy + 10, 3.0, 180, 190, hlog=320)
        out = []
        for v in (vt, vb):
            CH, FX = begin(v.Z); b = v.bg(); finish_scene(CH, FX, b, v, t); CH.comp(b, light('finish')); finish_fx(b, v, t, FX)
            out.append(b)
        return halves(out)
    if name == 'cu_sam_start':
        sx, sy = sam_head(START_S, R.FEET - 16); v = view_at(FIN, sx, sy, 3.0 + 0.08 * u, 180, 430)
    elif name in ('cu_mol_side', 'cu_mol_cam', 'cu_mol_final', 'cu_mol_carrot'):
        hx, hy = C.head_of_horse(mol_x(t), R.FEET, U, mol_pose(t)[0])
        Z = 3.0 + 0.1 * u if name != 'cu_mol_final' else 3.0 + 0.18 * u
        v = view_at(FIN, hx + 16, hy + 12, Z, 180, 430)
    elif name in ('wide_start', 'countdown'):
        v = View(FIN, 470 + 8 * u, 150, 1.0 + 0.03 * u)
    elif name == 'cu_billy_whisper':
        hx, hy = billy_head_start(t); v = view_at(FIN, hx + 10, hy, 2.8 + 0.08 * u, 180, 430)
    elif name == 'two_whisper':
        hx, hy = billy_head_start(t); v = view_at(FIN, hx + 60, hy + 40, 1.8, 180, 420)
    elif name == 'finish_wide':
        v = View(FIN, max(0.0, min(330.0, mol_x(t) - 90)), 150, 1.0)
    elif name == 'flight':
        bx, by, _ = billy_flight(t)
        v = view_at(FIN, lerp(560, 900, sm(u / 2.4)), 420, 1.05, 180, 380)
    elif name == 'cu_billy_cactus' or name == 'cu_billy_hat':
        v = view_at(FIN, R.CACTUS_X + 8, R.FEET - 14 * U - 9.7 * U, 2.8 + 0.1 * u, 180, 430)
    elif name == 'sam_arrives':
        v = view_at(FIN, 380, 470, 1.35, 180, 420)
    elif name == 'two_sam_mol':
        v = view_at(FIN, 452, 500, 1.1, 180, 420)
    elif name == 'sack_fall':
        v = view_at(FIN, R.CACTUS_X - 10, 470, 1.6, 180, 380)
    elif name == 'wide_cactus':
        v = view_at(FIN, 980, 470, 1.25 + 0.03 * u, 180, 420)
    else:  # endcard
        v = View(FIN, 720 + 10 * u, 150, 0.9)
    CH, FX = begin(v.Z)
    big = v.bg()
    finish_scene(CH, FX, big, v, t)
    CH.comp(big, light('finish'))
    finish_fx(big, v, t, FX, sunset=min(1.0, max(0.0, (t - 37.0) / 6)))
    if name == 'flight':
        fx.speed_lines(big, t, 0.6)
    if name == 'cu_mol_carrot' and t >= 24.3:
        sx, sy = v.opt(*C.head_of_horse(mol_x(t), R.FEET, U, mol_pose(t)[0]))
        O.overlay(big, O.pixel_title(['!'], 64), 0, max(0, int(sy) - 420), 1.0)
    return big

def render_canyon(name, t, u):
    if name == 'split_race':
        out = []
        for who in ('sam', 'mol'):
            v = view_at(CANYON, canyon_x(t, who) + 20, FR.CANYON_FEET - 65, 1.7, 180, 200, hlog=320)
            CH, FX = begin(v.Z); b = v.bg(); canyon_scene(CH, FX, b, v, t, who)
            CH.comp(b, light('canyon')); FX.comp(b); fx.vignette(b, 0.3); fx.speed_lines(b, t, 0.6)
            out.append(b)
        return halves(out)
    if name == 'wide_canyon':
        cx = (canyon_x(t, 'mol') + canyon_x(t, 'sam')) / 2; v = view_at(CANYON, cx + 30, 560, 1.05, 180, 400)
    else:  # cu_sam_race
        x = canyon_x(t, 'sam'); du = 5.0 * 0.85
        v = view_at(CANYON, x - 4, FR.CANYON_FEET - 19 * du - 9 * du - 9.7 * 5.0, 2.8, 180, 430)
    CH, FX = begin(v.Z)
    big = v.bg(); canyon_scene(CH, FX, big, v, t)
    CH.comp(big, light('canyon')); FX.comp(big)
    fx.shafts(big, t, angle=2.3, a=0.05, col=(255, 226, 160)); fx.vignette(big, 0.3); fx.speed_lines(big, t, 0.8)
    return big

def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name in ('split_race', 'wide_canyon', 'cu_sam_race'): return render_canyon(name, t, u)
    return render_finish(name, t, u)


# ---------------------------------------------------------------- overlays
BADGE = O.make_badge('СЕЗОН 1 • СЕРИЯ 6/6')
HOOK = O.pixel_title(['ФИНАЛЬНАЯ', 'ГОНКА'], 64)
COUNT = {n: O.pixel_title([n], 160) for n in ('3', '2', '1')}
END1 = O.pixel_title(['КОНЕЦ', '1 СЕЗОНА'], 64)
END2 = O.pixel_title(['СЕЗОН 2 СКОРО'], 40)
import wideov as WO
DAY, INCOME = 1096, 158                                 # HUD of the feature cut
STICKERS = [
    (O.sticker('$500', size=88), 6.7, 8.5, 960, 330),
    (O.sticker('1 МЕСТО', fg=(255, 236, 120), size=64), 26.3, 27.6, 960, 330),
    (O.sticker('$500', size=88), 36.7, 37.4, 1450, 330),
]

def render(t):
    big = render_scene(t)
    WO.stickers(big, STICKERS, t)
    WO.hud(big, t, DAY, 58 if t < 36.6 else INCOME)
    if 14.2 <= t < 15.4:
        n = '321'[min(2, int((t - 14.2) / 0.4))]
        O.overlay(big, COUNT[n], 0, 330, 1.0)
    if t < 45.0: EPI.captions.draw(big, t, WO.CAP_Y)
    for fa in FLASH_AT:
        if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
    if 22.0 <= t < 22.3: O.mosaic(big, int(lerp(44, 1, (t - 22.0) / 0.3)))
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
