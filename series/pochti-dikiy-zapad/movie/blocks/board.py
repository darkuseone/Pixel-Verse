"""«Разбор полётов»: Billy's investigation board (red strings), Molniya comments to camera."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *

DUR = 17.4
DAY, INCOME = 340, 22
VOICE = [
    ('d1', 'movie', 'd1', 1.00, 0.00, 4.91, 'billy',   'Он всегда рядом. Всегда исчезает. Слабых мест НЕТ.'),
    ('d2', 'movie', 'd2', 6.30, 0.00, 2.35, 'molniya', 'ЕСТЬ. Он платит вовремя.'),
    ('d3', 'movie', 'd3', 9.30, 0.10, 2.40, 'billy',   'Молния, ты видишь здесь СВЯЗЬ?'),
    ('d4', 'movie', 'd4', 12.60, 0.10, 2.85, 'molniya', 'Ничего не вижу. Уже НЕДЕЛЮ.'),
]
SFX = [
    ('library/sfx/pencil_scribble.mp3', 1.30, 0.6), ('library/sfx/pushpin_pop.mp3', 2.40, 0.8), ('library/sfx/pushpin_pop.mp3', 3.20, 0.8),
    ('library/sfx/pushpin_pop.mp3', 4.00, 0.8), ('library/sfx/pencil_scribble.mp3', 5.00, 0.5),
    ('library/sfx/horse_snort.mp3', 6.10, 0.5), ('library/sfx/pushpin_pop.mp3', 10.00, 0.8), ('library/sfx/pushpin_pop.mp3', 10.80, 0.8),
    ('library/sfx/carrot_crunch.mp3', 13.60, 0.5),
]
BEDS = [('series/pochti-dikiy-zapad/music/board_tension_15s.mp3', 15.0, 0.0, 17.4, 0.30, True)]
EPI = episode('mv_board', VOICE, DUR)
talk = EPI.talk
BARN = bgworld('barn_board')
FEET = 575.0
# polaroids on the cork board: (cx, cy, kind, label, appear_time)
PHOTOS = [(470, 260, 'cactus', 'КАКТУС', 1.2), (560, 380, 'cactus', 'КАКТУС', 1.8), (690, 250, 'cactus', 'КАКТУС?!', 2.4),
          (800, 370, 'cactus', 'КАКТУС', 3.0), (860, 250, 'cactus', 'ОПЯТЬ', 3.6), (655, 335, 'sam', 'СЭМ?', 4.4),
          (500, 400, 'mol', 'ЛОШАДЬ', 4.8)]
STRINGS = [(0, 2), (2, 4), (4, 3), (3, 1), (1, 0), (2, 5), (5, 3), (5, 1), (0, 5), (4, 5)]


def polaroid(L, x, y, kind):
    wrect(L, x - 30, y - 34, x + 30, y + 38, (236, 230, 214)); wrect(L, x - 26, y - 30, x + 26, y + 16, (184, 170, 120))
    if kind == 'cactus':
        wrect(L, x - 26, y + 6, x + 26, y + 16, (156, 128, 84)); cap(L, (x, y + 8), (x, y - 20), 3.2, 3.0, (70, 140, 66))
        cap(L, (x, y - 4), (x - 10, y - 4), 1.8, 1.8, (70, 140, 66)); cap(L, (x - 10, y - 4), (x - 10, y - 14), 1.8, 1.8, (70, 140, 66))
        cap(L, (x, y - 8), (x + 10, y - 8), 1.8, 1.8, (70, 140, 66)); cap(L, (x + 10, y - 8), (x + 10, y - 16), 1.8, 1.8, (70, 140, 66))
    elif kind == 'sam':
        wrect(L, x - 26, y - 30, x + 26, y + 16, (120, 100, 80)); wrect(L, x - 12, y - 18, x + 12, y - 12, (46, 40, 48))
        wrect(L, x - 9, y - 12, x + 9, y + 2, (226, 176, 136)); wrect(L, x - 9, y - 9, x + 9, y - 5, (24, 20, 24))
        wrect(L, x - 5, y - 8, x - 3, y - 6, (240, 240, 240)); wrect(L, x + 3, y - 8, x + 5, y - 6, (240, 240, 240))
        for i in range(4): wrect(L, x - 26 + i * 14, y + 4 - (i % 2) * 3, x - 20 + i * 14, y + 16, (60, 50, 44))   # blur streaks
    else:
        ell(L, (x, y - 2), 12, 10, (150, 96, 52)); wrect(L, x - 8, y - 22, x + 10, y - 18, (204, 172, 120)); wrect(L, x - 5, y - 28, x + 7, y - 22, (214, 182, 130))
        cap(L, (x + 4, y + 2), (x + 20, y + 6), 3.0, 1.0, (236, 128, 40))
    cap(L, (x, y - 34), (x, y - 34), 2.4, 2.4, (200, 40, 40))


def board_world(CH, v, t, upto):
    L = Layer(v.wcam())
    for (x, y, k, lab, ta) in PHOTOS:
        if t >= ta: polaroid(L, x, y, k)
    outline(L, (30, 20, 12)); CH.add(L)
    L2 = Layer(v.wcam())
    n = 0
    for (a, b) in STRINGS:
        ta = max(PHOTOS[a][4], PHOTOS[b][4]) + 0.4 + 0.25 * n; n += 1
        if t < ta: continue
        k = min(1.0, (t - ta) / 0.25)
        xa, ya = PHOTOS[a][0], PHOTOS[a][1] - 34; xb, yb = PHOTOS[b][0], PHOTOS[b][1] - 34
        cap(L2, (xa, ya), (lerp(xa, xb, k), lerp(ya, yb, k)), 1.2, 1.2, (210, 40, 40))
    CH.add(L2)
    if t >= 8.0:                                                       # the string Billy never draws: Molniya - carrots
        pass
    if v.Z >= 1.4:
        for (x, y, k, lab, ta) in PHOTOS:
            if t >= ta:
                sx, sy = v.pt(x, y + 30); px_text(CH, lab, sx, sy, 8, (60, 40, 30))


def draw(CH, FX, big, v, t):
    fx.glow(big, *v.opt(520, 210), 420, (255, 170, 80), 0.32 + 0.03 * math.sin(t * 9))
    fx.motes(FX, v, t, 300, 150, 1000, 600, n=34, col=(255, 200, 130), seed=5)
    board_world(CH, v, t, 0)
    # Billy at the board (left), Molniya chewing at the right
    bx = 420.0; U_ = 7.6
    pose = C.POSES['point'] if 1.0 <= t < 6.0 or t >= 9.3 else C.POSES['hips']
    shadow(big, v, bx, FEET, 5 * U_, 1.2 * U_)
    C.billy(CH, v.cam(bx, FEET - C.HIP_H * U_, U_), pose, 0.05 + 0.18 * (1 if pose is C.POSES['point'] else 0), talk('billy', t),
            'sly' if t < 6 else 'normal', hat=False)
    mx, um = 990.0, 6.4
    Pz = C.molniya_pose(t, chew=t >= 13.3, jaw_talk=talk('molniya', t))
    ax, ay = C.horse_anchor(mx, FEET, um)
    shadow(big, v, mx, FEET, 16 * um, 1.8 * um)
    C.molniya(CH, v.cam(ax, ay, um, True), t, Pz, hat=True, carrot=t >= 13.3)


def light(v, t):
    ox, oy = v.opt(520, 230)
    return Light(amb=(0.86, 0.76, 0.68), keys=[(ox, oy, 900, (255, 190, 110), 0.9)], rim=(1, -1, (255, 200, 120), 0.4),
                 grad=(1.0, 0.85), flick=1.0 + 0.06 * math.sin(t * 8.3))


def render_scene(t):
    if t < 5.6: v = wv(BARN, 650, 395, 0.95 + 0.01 * t)
    elif t < 9.0:
        hx, hy = C.head_of_horse(990.0, FEET, 6.4, C.molniya_pose(t), True)
        v = wv(BARN, hx - 30, hy + 20, 2.4)
    elif t < 12.4: v = wv(BARN, 560, 400, 1.3)
    else:
        hx, hy = C.head_of_horse(990.0, FEET, 6.4, C.molniya_pose(t), True)
        v = wv(BARN, hx - 30, hy + 20, 2.3)
    return shot(v, t, lambda CH, FX, big, vv: draw(CH, FX, big, vv, t), light(v, t), vig=0.4)


def render(t):
    big = render_scene(t)
    WO.hud(big, t, DAY, INCOME)
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [0.0], 0.12, 0.6)
    if 0.0 <= t < 1.6:
        O.overlay(big, O.pixel_title(['РАЗБОР ПОЛЁТОВ'], 60, width=1920), 0, 110, min(1.0, t / 0.1) * (1 - sm((t - 1.4) / 0.2)))
    return big
