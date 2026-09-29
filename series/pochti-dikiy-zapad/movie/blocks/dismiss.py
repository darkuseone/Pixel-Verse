"""Chapter 4 intro: Billy's «Приказ №1» — the horse is dismissed; Molniya: «Я на аутсорсе»."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *
from props import rental as R

DUR = 8.8
DAY, INCOME = 620, 22
VOICE = [
    ('f1', 'movie', 'f1', 0.30, 0.05, 4.85, 'billy',   'Приказ номер ОДИН. Лошадь УВОЛИТЬ. Подпись: Билли.'),
    ('f2', 'movie', 'f2', 5.40, 0.15, 3.25, 'molniya', 'Я не в штате. Я на АУТСОРСЕ.'),
]
SFX = [('library/sfx/film_click.mp3', 0.00, 0.6), ('library/sfx/paper_unroll.mp3', 0.20, 0.8), ('library/sfx/stamp.mp3', 4.90, 0.9),
       ('library/sfx/horse_snort.mp3', 5.20, 0.5)]
BEDS = [('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 0.0, 8.8, 0.24, True),
        ('library/sfx/amb_desert_wind.mp3', 7.8, 0.0, 8.8, 0.7, False)]
EPI = episode('mv_dismiss', VOICE, DUR)
talk = EPI.talk
EXT = bgworld('rental_ext')
FEET, U = float(R.EXT_FEET), 6.6
BX, MX = 560.0, 330.0


def paper(CH, v, t):
    hx, hy = BX, FEET - (C.HIP_H + 9.7) * U
    L = Layer(v.wcam())
    x0, y0, x1, y1 = hx - 100, hy + 20, hx - 12, hy + 120
    wrect(L, x0, y0, x1, y1, (236, 224, 188)); wrect(L, x0, y0, x1, y0 + 3, (200, 180, 140)); wrect(L, x0, y1 - 3, x1, y1, (200, 180, 140))
    outline(L, (60, 40, 24)); CH.add(L)
    if v.Z >= 1.6:
        for txt, dy, col in (('ПРИКАЗ №1', 16, (150, 36, 26)), ('ЛОШАДЬ', 40, (60, 40, 30)), ('УВОЛИТЬ', 56, (60, 40, 30)), ('БИЛЛИ', 88, (40, 50, 120))):
            sx, sy = v.pt((x0 + x1) / 2, y0 + dy); px_text(CH, txt, sx, sy, 8, col)
    if t >= 4.9:
        L2 = Layer(v.wcam()); cx, cy = x0 + 50, y0 + 72
        wrect(L2, cx - 30, cy - 9, cx + 30, cy + 9, (190, 40, 40)); CH.add(L2)
        sx, sy = v.pt(cx, cy); px_text(CH, 'УВОЛЕНА', sx, sy, 8, (250, 240, 220))


def draw(CH, FX, big, v, t):
    fx.motes(FX, v, t, 0, 300, 1280, 700, n=26, col=(255, 226, 170), seed=12)
    shadow(big, v, BX, FEET + 6, 5 * U, 1.2 * U)
    pose = C.POSES['angry'] if 1.0 <= t < 4.8 else C.POSES['hips']
    C.billy(CH, v.cam(BX, FEET + 6 - C.HIP_H * U, U, True), pose, 0.05, talk('billy', t), 'angry' if t < 5.2 else 'sly', hat=False)
    paper(CH, v, t)
    Pz = C.molniya_pose(t, chew=t >= 5.5, jaw_talk=talk('molniya', t))
    ax, ay = C.horse_anchor(MX, FEET, U)
    shadow(big, v, MX, FEET, 16 * U, 1.8 * U)
    C.molniya(CH, v.cam(ax, ay, U), t, Pz, hat=True, carrot=t >= 5.5)


def render_scene(t):
    if t < 1.6: v = wv(EXT, 450, 470, 1.15)
    elif t < 5.2: v = wv(EXT, BX - 40, FEET - (C.HIP_H + 6) * U, 2.5 + 0.03 * (t - 1.6))
    else:
        hx, hy = C.head_of_horse(MX, FEET, U, C.molniya_pose(t)); v = wv(EXT, hx + 30, hy + 10, 2.5)
    return shot(v, t, lambda CH, FX, big, vv: draw(CH, FX, big, vv, t),
                Light(amb=(1.05, 0.96, 0.86), rim=(1, -1, (255, 230, 180), 0.45), grad=(1.06, 0.9)))


def render(t):
    big = render_scene(t)
    WO.hud(big, t, DAY, INCOME)
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [0.0, 5.2], 0.12, 0.6)
    return big
