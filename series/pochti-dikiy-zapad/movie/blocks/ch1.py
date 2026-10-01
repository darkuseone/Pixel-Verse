"""Chapter 1 «Самый быстрый»: new ranch rehearsal + S01E01 rebuilt in HD 16:9 (desert road, code heroes, hybrid look)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *

DUR = 48.6
DAY, INCOME = 1, (0, 1, 29.0)

VOICE = [
    ('a1',  'movie', 'a1', 0.00, 0.15, 5.33, 'billy',   'Сдавайся, Кривой Сэм! Нет. СДАВАЙСЯ, Кривой Сэм!'),
    ('a2',  'movie', 'a2', 6.00, 0.10, 4.05, 'molniya', 'Репетирует третий ГОД. Интонация не РАСТЁТ.'),
    ('c1',  'ep01',  'c1', 12.50, 0.30, 5.70, 'billy',  'Н-но, родная! Я — САМЫЙ быстрый ковбой на всём Диком Западе!'),
    ('n1',  'ep01',  'n1', 18.30, 0.00, 4.30, 'billy',  'Сегодня я наконец поймаю Кривого СЭМА!'),
    ('n2',  'ep01',  'n2', 22.80, 0.10, 1.70, 'molniya', 'Он ловит его ТРЕТИЙ год.'),
    ('c2',  'ep01',  'c2', 25.30, 0.10, 2.16, 'billy',  'А-А-А-А-А!'),
    ('c3a', 'ep01',  'c3', 28.20, 0.13, 0.75, 'billy',  'Ой...'),
    ('c3b', 'ep01',  'c3', 29.05, 1.36, 2.00, 'billy',  'КАКТУС...'),
    ('h1a', 'ep01',  'h1', 30.70, 0.00, 1.45, 'molniya', 'Самый быстрый тут — Я.'),
    ('h1b', 'ep01',  'h1', 32.35, 3.05, 4.50, 'molniya', 'А ты просто сверху СИДЕЛ.'),
    ('n3',  'ep01',  'n3', 34.60, 0.10, 2.55, 'sam',     'Приятного аппетита, МЭМ.'),
    ('n4',  'ep01',  'n4', 37.30, 0.12, 0.75, 'molniya', 'СПАСИБО.'),
    ('n5',  'ep01',  'n5', 39.60, 0.15, 3.90, 'billy',  'Молния... Ты не видела Кривого СЭМА?'),
    ('n6',  'ep01',  'n6', 43.65, 0.20, 0.66, 'molniya', 'НЕ-А.'),
    ('a3',  'movie', 'a3', 45.00, 0.10, 3.05, 'molniya', 'МОРКОВКА первая. Запомните ЦЕНУ.'),
]
SFX = [
    ('library/sfx/film_click.mp3', 0.00, 0.7),
    ('library/sfx/horse_snort.mp3', 6.20, 0.5),
    ('library/sfx/whoosh.mp3', 10.40, 0.7),
    ('library/sfx/horse_gallop.mp3', 12.60, 0.8), ('library/sfx/horse_gallop.mp3', 14.40, 0.8), ('library/sfx/horse_gallop.mp3', 16.20, 0.8),
    ('library/sfx/horse_gallop.mp3', 18.00, 0.8), ('library/sfx/horse_gallop.mp3', 19.80, 0.8), ('library/sfx/horse_gallop.mp3', 21.60, 0.8),
    ('library/sfx/horse_gallop.mp3', 23.40, 0.8),
    ('library/sfx/brake_skid.mp3', 25.05, 1.0),
    ('library/sfx/whoosh.mp3', 25.30, 0.7),
    ('series/pochti-dikiy-zapad/sfx/cactus_boing.mp3', 27.65, 1.0),
    ('library/sfx/carrot_crunch.mp3', 28.90, 0.6), ('library/sfx/carrot_crunch.mp3', 29.60, 0.6),
    ('library/sfx/counter_blip.mp3', 29.00, 0.6),
    ('library/sfx/donkey_walk.mp3', 34.40, 0.5),
    ('library/sfx/donkey_bray.mp3', 38.00, 0.7),
    ('library/sfx/donkey_walk.mp3', 39.60, 0.5),
    ('library/sfx/carrot_crunch.mp3', 45.30, 0.6),
]
BEDS = [
    ('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 0.0, 25.0, 0.26, True),
    ('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 27.4, 48.6, 0.28, True),
    ('library/sfx/amb_desert_wind.mp3', 7.8, 0.0, 48.6, 0.7, False),
]
EPI = episode('mv_ch1', VOICE, DUR)
talk = EPI.talk

RANCH, ROAD = bgworld('ranch_dawn'), bgworld('desert_road')
FEET_R, FEET = 610.0, 588.0            # ranch yard / desert road ground line (world px)
U = 5.6                                # rider / horse unit on the road
DU = U * 0.85
CACTUS_X = 1010.0
T_BRAKE, T_LAUNCH, T_LAND = 25.05, 25.3, 27.7
B0 = 12.5


def light(scene):
    if scene == 'ranch':
        return Light(amb=(1.12, 0.92, 0.78), rim=(1, -1, (255, 190, 120), 0.55), grad=(1.08, 0.85))
    return Light(amb=(1.05, 0.97, 0.88), rim=(1, -1, (255, 236, 190), 0.45), grad=(1.06, 0.9))


def wv(world, cx, cy, Z):
    return ST.View(world, cx - ST.W / 2 / Z, cy - ST.H / 2 / Z, Z)


# ---------------------------------------------------------------- actors
def rider_hat(pose, mouth=0.0, hat=True, rot=0.05):
    def f(L, T):
        hip = T(-1.0, -9.4)
        S.CC['mst'] = (96, 60, 36)
        S.cowboy(L, hip, rot, pose, hat_on=hat, mouth=mouth)
        HP = C.HPf(rot, hip)
        if not hat:
            ell(L, HP(0.4, 11.4), 2.9, 1.5, (104, 66, 40), rot, hi=(136, 90, 56))
        cap(L, HP(1.4, 8.55), HP(3.1, 8.45), 0.55, 0.45, (96, 60, 36))
    return f


def mol_x(t):
    """Molniya's x on the road (jump-cut crossings: each shot re-enters from the left)"""
    if t < B0: return 300.0
    for a, b, x0, v in ((12.5, 15.1, 80, 380), (15.1, 17.9, 20, 330), (17.9, 20.3, 90, 400), (20.3, 22.5, 20, 330),
                        (22.5, 24.4, 30, 330), (24.4, T_BRAKE, 330, 480)):
        if a <= t < b: return x0 + v * (t - a)
    x = 330 + 480 * (T_BRAKE - 24.4)
    return x + 24 * sm((t - T_BRAKE) / 0.3)


def mol_pose(t):
    if t < B0: return C.molniya_pose(t, False, talk('molniya', t)), 0.0
    if t < T_BRAKE:
        Pz, p = C.gallop(t)
        if 22.8 <= t < 24.4: Pz['jaw'] = min(talk('molniya', t) * 1.6, 1.0) * 0.8
        return Pz, p
    if t < T_BRAKE + 0.5:
        Pz = S.brake_pose(t); Pz.update(lid=0.1, ear=0.8); return Pz, 0.0
    chew = 28.3 <= t < 34.0 or 45.0 <= t
    Pz = C.molniya_pose(t, chew, talk('molniya', t))
    return Pz, 0.0


def billy_flight(t, sx):
    Pz, _ = mol_pose(T_LAUNCH - 0.01)
    x0, y0 = C.rider_hip_world(sx, FEET, U, Pz)
    x1, y1 = CACTUS_X, FEET - 14 * U
    k = min(1.0, max(0.0, (t - T_LAUNCH) / (T_LAND - T_LAUNCH)))
    return lerp(x0, x1, k), lerp(y0, y1, k) - 300 * math.sin(math.pi * k), -k * 6.28 * 1.25


T_HAT = 2.3


def hat_pos(t, sx):
    """Billy's hat: leaves his head at the launch, lands on Molniya's head 2.3 s later"""
    Pz, _ = mol_pose(T_LAUNCH - 0.01)
    x0, y0 = C.rider_hip_world(sx, FEET, U, Pz)
    x0, y0 = x0 + 0.4 * U, y0 - 11.6 * U
    Pz2, _ = mol_pose(T_LAUNCH + 2.5)
    xs = mol_x(T_LAUNCH + 2.5)
    ax, ay = C.horse_anchor(xs, FEET, U)
    hp, _r = S.head_hat_anchor(1000.0, 1000.0, Pz2)
    x1, y1 = ax + (hp[0] - 1000) * U, ay + (hp[1] - 1000) * U
    k = min(1.0, max(0.0, (t - T_LAUNCH) / T_HAT))
    return lerp(x0, x1, k), lerp(y0, y1, k) - 200 * math.sin(math.pi * k), k * 9.0


def sam_x(t):
    if 34.0 <= t < 37.6: return -100 + 300 * (t - 34.0)
    return None


def sam_front_x(t):
    if 39.6 <= t < 43.6: return -150 + 380 * (t - 39.6)
    return None


def draw_cactus(CH, v, t, wob=0.0):
    L = Layer(v.cam(CACTUS_X, FEET + 8, 7.0))
    S.cactus(L, 1000.0, 1000.0, wob)
    outline(L, (40, 72, 36)); CH.add(L)


def road_scene(CH, FX, big, v, t, parts=('mol', 'billy', 'sam', 'cactus')):
    fx.motes(FX, v, t, 0, 300, 1280, 700, n=36, seed=4)
    ev = []
    if B0 <= t < T_BRAKE: ev += fx.gallop_dust(t, mol_x, FEET, max(B0, t - 0.8), t, 8, 12)
    ev += [(T_BRAKE, mol_x(T_BRAKE) + 40, FEET, 26), (T_LAND, CACTUS_X, FEET, 22)]
    if sam_x(t) is not None: ev += fx.gallop_dust(t, sam_x, FEET - 12, max(34.0, t - 0.8), t, 5, 8)
    fx.dust_puffs(FX, v, t, ev)
    if 'cactus' in parts and t >= 24.0: draw_cactus(CH, v, t, 3.0 * math.exp(-(t - T_LAND) * 4) * math.sin((t - T_LAND) * 30) if t >= T_LAND else 0.0)
    if 'sam' in parts:
        x = sam_x(t)
        if x is not None:
            shadow(big, v, x, FEET - 12, 13 * DU, 1.6 * DU)
            C.donkey(CH, v.cam(x, FEET - 12 - 19 * DU, DU), t, moving=True,
                     rider=C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t)))
        xf = sam_front_x(t)
        if xf is not None:
            duf = DU * 1.25
            shadow(big, v, xf, FEET + 50, 13 * duf, 1.6 * duf)
            C.donkey(CH, v.cam(xf, FEET + 50 - 19 * duf, duf), t, moving=True,
                     rider=C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t)))
    if 'mol' in parts:
        Pz, ph = mol_pose(t)
        mx = mol_x(t)
        shadow(big, v, mx, FEET, 16 * U, 1.8 * U)
        rider = None
        if t < T_LAUNCH:
            pose = C.POSES['ride_whip'] if 12.5 <= t < 17.9 else C.POSES['ride']
            rider = rider_hat(pose, talk('billy', t), hat=True)
        ax, ay = C.horse_anchor(mx, FEET, U)
        C.molniya(CH, v.cam(ax, ay, U), t, Pz, rider=rider, p=ph, hat=t < T_LAUNCH or t >= T_LAUNCH + T_HAT, carrot=28.6 <= t < 33.5 or t >= 45.0)
    if 'billy' in parts and T_LAUNCH <= t < 39.7 or ('billy' in parts and t >= 43.0):
        pass
    if 'billy' in parts and t >= T_LAUNCH:
        sx = mol_x(T_LAUNCH)
        if t < T_LAND:
            bx, by, rot = billy_flight(t, sx)
            C.billy(CH, v.cam(bx, by, U), S.pose_fly(t), rot, talk('billy', t), 'shout', hat=False)
        elif t < 39.4:
            draw_cactus(CH, v, t) if False else None
            hip = (CACTUS_X + 2, FEET - 14 * U)
            C.billy(CH, v.cam(hip[0], hip[1], U), C.POSES['shout'], -0.05, talk('billy', t), 'shout' if t < 30 else 'amazed', hat=False)
            if 29.6 <= t < 31.8:
                L = Layer(v.cam(hip[0], hip[1], U))
                for i in range(3):
                    a = t * 4 + i * 2.1
                    S.star(L, (1000.6 + 4.5 * math.cos(a), 1000 - 14.5 + 1.2 * math.sin(a)))
                CH.add(L)
        else:                                                       # Billy climbed out, stands next to the cactus, asks about Sam
            bx = 560.0
            shadow(big, v, bx, FEET, 5 * U, 1.2 * U)
            C.billy(CH, v.cam(bx, FEET - C.HIP_H * U, U), C.POSES['hips'] if t < 41.5 else C.POSES['point'], 0.05, talk('billy', t),
                    'normal', hat=False)
    if T_LAUNCH <= t < T_LAUNCH + T_HAT:
        hx, hy, hr = hat_pos(t, mol_x(T_LAUNCH))
        L = Layer(v.cam(hx, hy, U)); S.hat(L, (1000.0, 1000.0), hr); outline(L, (60, 40, 20)); CH.add(L)
    if T_LAUNCH + 2.7 <= t and 'mol' in parts:
        pass
    if 24.4 <= t < T_BRAKE + 0.6 or (T_BRAKE <= t < T_LAND):
        cx = 760.0 if t < T_BRAKE else 760.0
        L = Layer(v.wcam())
        if t < T_BRAKE + 0.2:
            cap(L, (cx, FEET - 6), (cx + 26, FEET - 12), 6.0, 2.0, (236, 128, 40), hi=(255, 176, 90))
            for a in (-0.5, 0.0, 0.5): cap(L, (cx, FEET - 6), (cx - 10 * math.cos(a), FEET - 6 - 10 * math.sin(a) - 4), 2.0, 1.1, (84, 160, 60))
            outline(L, (70, 40, 20)); CH.add(L)
            fx.embers(FX, v, cx + 12, FEET - 10, t, n=8, h=40, spread=30, col=((255, 250, 200), (255, 230, 150), (255, 255, 255)))


# ---------------------------------------------------------------- ranch (rehearsal)
BX, MX = 520.0, 250.0
UR = 8.0


def billy_ranch(t):
    """(x, pose, expr, flip) of Billy in the yard"""
    if t < 10.2:
        pose = C.POSES['heroic'] if 0.3 <= t < 1.6 else C.POSES['angry'] if 3.1 <= t < 4.9 else C.POSES['hips']
        if 4.6 <= t < 5.9: pose = C.POSES['shout']
        return BX, pose, 'shout' if (0.3 <= t < 1.6 or 4.6 <= t < 5.9) else 'sly', False
    x = lerp(BX, MX + 30, sm((t - 10.2) / 0.5))
    return x, C.walk_pose(t, 12, 0.6), 'shout', True


def ranch_draw(CH, FX, big, v, t):
    fx.motes(FX, v, t, 0, 200, 1280, 650, n=34, col=(255, 210, 150), seed=2)
    ax, ay = C.horse_anchor(MX, FEET_R, UR * 0.72)
    shadow(big, v, MX, FEET_R, 16 * UR * 0.72, 1.8 * UR * 0.72)
    Pz = C.molniya_pose(t, chew=6.0 <= t < 10.0, jaw_talk=talk('molniya', t))
    C.molniya(CH, v.cam(ax, ay, UR * 0.72), t, Pz, hat=True, carrot=False)
    x, pose, expr, flip = billy_ranch(t)
    if t < 10.6:
        shadow(big, v, x, FEET_R + 14, 5 * UR, 1.2 * UR)
        C.billy(CH, v.cam(x, FEET_R + 14 - C.HIP_H * UR, UR, flip), pose, 0.05, talk('billy', t), expr, hat=True)
    elif t < 11.6:
        shadow(big, v, x, FEET_R + 14, 5 * UR, 1.2 * UR)
        C.billy(CH, v.cam(x, FEET_R + 14 - C.HIP_H * UR, UR, flip), pose, 0.05, 0.0, expr, hat=True)
    fx.dust_puffs(FX, v, t, [(10.4 + 0.15 * i, x_, FEET_R + 10, 12) for i, x_ in enumerate((330, 370, 410))] if t > 10.4 else [])


def ranch_shot(t):
    u = t
    if t < 2.2:
        bxh = BX + 0.6 * UR
        v = wv(RANCH, bxh, FEET_R + 14 - (C.HIP_H + 9) * UR, 2.4 + 0.05 * u)
    elif t < 4.4:
        v = wv(RANCH, 470 + 6 * (t - 2.2), 470, 1.25)
    elif t < 6.0:
        v = wv(RANCH, BX + 10, FEET_R + 14 - (C.HIP_H + 9) * UR, 2.6 + 0.05 * (t - 4.4))
    elif t < 10.2:
        hx, hy = C.head_of_horse(MX, FEET_R, UR * 0.72, C.molniya_pose(t))
        v = wv(RANCH, hx + 30, hy + 10, 2.5 + 0.03 * (t - 6.0))
    else:
        v = wv(RANCH, lerp(330, 700, sm((t - 10.2) / 2.3)), 480, 1.2)
    return shot(v, t, lambda CH, FX, big, vv: ranch_draw(CH, FX, big, vv, t), light('ranch'))


# ---------------------------------------------------------------- road shots
def road_shot(t):
    fol = lambda x: 250 + 0.72 * x
    if t < 15.1: v = wv(ROAD, fol(mol_x(t)), 450, 0.95)                    # wide crossing
    elif t < 17.9:
        hx, hy = C.rider_hip_world(mol_x(t), FEET, U, mol_pose(t)[0]); v = wv(ROAD, hx + 90, hy - 40, 2.5)
    elif t < 20.3: v = wv(ROAD, fol(mol_x(t)), 450, 1.0)
    elif t < 22.5:
        hx, hy = C.rider_hip_world(mol_x(t), FEET, U, mol_pose(t)[0]); v = wv(ROAD, hx + 90, hy - 40, 2.5)
    elif t < 24.4:
        hx, hy = C.head_of_horse(mol_x(t), FEET, U, mol_pose(t)[0]); v = wv(ROAD, hx + 30, hy + 15, 2.7)
    elif t < 25.3: v = wv(ROAD, fol(mol_x(t)) + 60, 450, 0.95)
    elif t < 27.75:
        k = sm((t - 25.3) / 2.4); v = wv(ROAD, lerp(700, 900, k), 440, 0.95)
    elif t < 30.6:
        v = wv(ROAD, 840, 470, 1.15)
    elif t < 34.0:
        hx, hy = C.head_of_horse(mol_x(t), FEET, U, mol_pose(t)[0]); v = wv(ROAD, hx + 20, hy + 20, 2.6)
    elif t < 37.4: v = wv(ROAD, 660, 450, 1.0)
    elif t < 39.6:
        hx, hy = C.head_of_horse(mol_x(t), FEET, U, mol_pose(t)[0]); v = wv(ROAD, hx + 20, hy + 20, 2.8)
    elif t < 43.4: v = wv(ROAD, 660, 470, 1.05)
    elif t < 45.0:
        hx, hy = C.head_of_horse(mol_x(t), FEET, U, mol_pose(t)[0]); v = wv(ROAD, hx + 20, hy + 20, 2.8)
    else:
        hx, hy = C.head_of_horse(mol_x(t), FEET, U, mol_pose(t)[0]); v = wv(ROAD, hx + 10, hy + 15, 2.5 - 0.02 * (t - 45.0))
    sp = 1.0 if B0 <= t < 24.4 else 0.6 if T_LAUNCH <= t < T_LAND else 0.0
    return shot(v, t, lambda CH, FX, big, vv: road_scene(CH, FX, big, vv, t), light('road'), speed=sp)


# ---------------------------------------------------------------- overlays
STICKERS = [
    (O.sticker('!', fg=(255, 120, 90), size=110), 24.45, 25.2, 960, 300),
    (O.sticker('+1', icon=C.carrot_icon(1, 7)), 29.05, 30.4, 1450, 300),
]


def render_scene(t):
    if t < B0: return ranch_shot(t)
    return road_shot(t)


def render(t):
    big = render_scene(t)
    WO.stickers(big, STICKERS, t)
    WO.hud(big, t, DAY, INCOME[1] if t >= INCOME[2] else INCOME[0])
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [B0, 25.3, 27.7], 0.15, 0.6)
    if 12.5 <= t < 12.75: O.mosaic(big, int(lerp(44, 1, (t - 12.5) / 0.25)))
    return big
