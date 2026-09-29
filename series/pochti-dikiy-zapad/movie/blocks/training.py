"""Chapter 6 intro: Billy's training montage («Я стану быстрее ветра!»)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *

DUR = 14.6
DAY, INCOME = 1090, 58
VOICE = [
    ('i1', 'movie', 'i1', 0.30, 0.00, 5.90, 'billy',   'Раз! Два! ...Кактус ТЯЖЁЛЫЙ.'),
    ('i2', 'movie', 'i2', 6.60, 0.05, 3.15, 'molniya', 'Тренировка — это БОЛЬНО и без морковки.'),
    ('i3', 'movie', 'i3', 11.20, 0.10, 2.30, 'billy',  'Я стану БЫСТРЕЕ ветра!'),
]
SFX = [('library/sfx/film_click.mp3', 0.00, 0.5), ('library/sfx/boots_stomp.mp3', 0.60, 0.7), ('library/sfx/boots_stomp.mp3', 1.70, 0.7),
       ('library/sfx/boots_stomp.mp3', 2.80, 0.7), ('series/pochti-dikiy-zapad/sfx/cactus_boing.mp3', 6.00, 0.9),
       ('library/sfx/horse_snort.mp3', 6.40, 0.5), ('library/sfx/whoosh.mp3', 11.60, 0.8), ('library/sfx/wind_gust.mp3', 13.20, 0.8)]
BEDS = [('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 0.0, 14.6, 0.28, True)]
EPI = episode('mv_train', VOICE, DUR)
talk = EPI.talk
TRAIN = bgworld('training_field')
FEET, U = 640.0, 8.0
BX = 520.0


def tumbleweed(CH, v, t):
    x = 100 + 380 * max(0.0, t - 12.0)
    L = Layer(v.cam(x, FEET - 22, 7.0))
    ell(L, (1000.0, 1000.0), 3.0, 3.0, (168, 128, 70))
    for i in range(6):
        a = t * 12 + i * 1.05
        cap(L, (1000 + 2.6 * math.cos(a), 1000 + 2.6 * math.sin(a)), (1000 - 2.6 * math.cos(a), 1000 - 2.6 * math.sin(a)), 0.25, 0.25, (110, 80, 44))
    outline(L, (60, 40, 20)); CH.add(L)


def draw(CH, FX, big, v, t):
    fx.motes(FX, v, t, 0, 300, 1280, 700, n=30, col=(255, 210, 150), seed=17)
    if t < 6.4:
        sag = 0.0 if t < 4.6 else 1.0 * min(1.0, (t - 4.6) / 1.2)
        shake = 1.2 * math.sin(t * 20) * (0.3 + sag)
        drop = 4.0 * sag
        pose = C.blend_pose(C.POSES['excited'], C.POSES['hips'], 0.0)
        shadow(big, v, BX, FEET, 5 * U, 1.2 * U)
        C.billy(CH, v.cam(BX + shake, FEET - C.HIP_H * U + drop, U), pose, 0.02 * math.sin(t * 9), talk('billy', t), 'shout', hat=True)
        cx = BX + 1.2 * math.sin(t * 20) * 0.5
        if t < 6.0:
            L = Layer(v.cam(cx, FEET - (C.HIP_H + 16.5) * U + drop, 6.0)); S.cactus(L, 1000.0, 1000.0, 1.5 * math.sin(t * 8)); outline(L, (40, 72, 36)); CH.add(L)
        else:
            k = t - 6.0
            L = Layer(v.cam(BX + 30, FEET - 8 * U + 250 * max(0.0, 0.5 - k) ** 1 * 0 + min(1.0, k * 4) * (8 * U - 10), 6.0))
            S.cactus(L, 1000.0, 1000.0, 0.0); outline(L, (40, 72, 36)); CH.add(L)
        if sag > 0 or (int(t * 6) % 3 == 0):
            L = Layer(v.cam(BX - 40, FEET - (C.HIP_H + 9) * U, U))
            for i in range(3):
                yy = ((t * 2.2 + i * 0.4) % 1.0) * 6
                ell(L, (1000.0 - 1.5 * i, 1000.0 + yy), 0.35, 0.55, (170, 220, 255))
            CH.add(L)
    elif t < 10.2:
        Pz = C.molniya_pose(t, False, talk('molniya', t))
        ax, ay = C.horse_anchor(900.0, FEET, 6.8)
        shadow(big, v, 900.0, FEET, 16 * 6.8, 1.8 * 6.8)
        C.molniya(CH, v.cam(ax, ay, 6.8), t, Pz, hat=True, carrot=False)
    else:
        x = 100 + 300 * max(0.0, t - 11.4)
        shadow(big, v, x, FEET, 5 * U, 1.2 * U)
        C.billy(CH, v.cam(x, FEET - C.HIP_H * U, U), C.walk_pose(t, 15, 0.9), 0.18, talk('billy', t), 'shout', hat=True)
        fx.dust_puffs(FX, v, t, fx.gallop_dust(t, lambda tt: 100 + 300 * max(0.0, tt - 11.4), FEET, max(11.4, t - 0.8), t, 8, 8) if t > 11.4 else [])
        if t >= 12.0: tumbleweed(CH, v, t)


def render_scene(t):
    if t < 1.6: v = wv(TRAIN, BX + 20, 470, 2.2)
    elif t < 4.2: v = wv(TRAIN, BX + 40, 500, 1.5)
    elif t < 6.4: v = wv(TRAIN, BX + 10, 480, 2.0 + 0.05 * (t - 4.2))
    elif t < 10.2:
        hx, hy = C.head_of_horse(900.0, FEET, 6.8, C.molniya_pose(t)); v = wv(TRAIN, hx + 30, hy + 20, 2.3)
    elif t < 11.6: v = wv(TRAIN, 460, 500, 1.2)
    else:
        x = 100 + 300 * max(0.0, t - 11.4); v = wv(TRAIN, x + 180, 500, 1.15)
    return shot(v, t, lambda CH, FX, big, vv: draw(CH, FX, big, vv, t),
                Light(amb=(1.08, 0.95, 0.82), rim=(-1, -1, (255, 200, 130), 0.5), grad=(1.06, 0.9)), speed=0.8 if t >= 11.6 else 0.0)


STICK = [(O.sticker('ДЕНЬ 1090', fg=(255, 236, 120), size=56), 0.2, 1.7, 960, 300),
         (O.sticker('×1', icon=C.carrot_icon(1, 7)), 7.0, 8.4, 1450, 300)]


def render(t):
    big = render_scene(t)
    WO.stickers(big, STICK, t)
    WO.hud(big, t, DAY, INCOME)
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [0.0, 6.4, 10.2], 0.12, 0.5)
    return big
