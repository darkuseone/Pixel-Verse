"""Fake studio logos + main title of the feature cut, Molniya announces the «director's cut»."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *

DUR = 8.4
VOICE = [('x6', 'movie', 'x6', 3.60, 0.00, 3.40, 'molniya', 'РЕЖИССЁРСКАЯ версия. Режиссёр — Я.')]
SFX = [
    ('library/sfx/film_click.mp3', 0.00, 0.8), ('library/sfx/film_click.mp3', 1.55, 0.8),
    ('library/sfx/title_stinger.mp3', 2.70, 1.0),
]
BEDS = [('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 2.6, 8.4, 0.28, True)]
EPI = episode('mv_title', VOICE, DUR)
talk = EPI.talk
ROAD = bgworld('desert_road')
TITLE = O.pixel_title(['ПОЧТИ ДИКИЙ ЗАПАД'], 92, width=1920)
SUB = O.pixel_title(['РЕЖИССЁРСКАЯ ВЕРСИЯ'], 52, width=1920)
FEET, U = 590.0, 6.6


def render_scene(t):
    if t < 2.65:
        big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (14, 10, 8)
        ic = C.carrot_icon(1, 8)
        if 0.15 <= t < 1.45:
            k = min(1.0, (t - 0.15) / 0.15)
            WO.ptext(big, 'МОРКОВЬ ПРОДАКШН', 960, 500, 60, (255, 190, 90), 'c')
            O.overlay(big, ic, 960 - ic.shape[1] // 2, 330, k)
            WO.ptext(big, 'ПРЕДСТАВЛЯЕТ', 960, 620, 26, (200, 190, 170), 'c')
        elif 1.65 <= t < 2.6:
            WO.ptext(big, 'ПРИ ПОДДЕРЖКЕ КРИВОГО СЭМА', 960, 480, 44, (214, 170, 255), 'c')
            WO.ptext(big, '(ОН НАСТОЯЛ)', 960, 570, 30, (200, 190, 170), 'c')
        if int(t * 24) % 5 == 0: big[::3] = (big[::3] * 0.8).astype(np.uint8)
        return big
    u = t - 2.65
    v = ST.View(ROAD, 640 - 320 / 1.05, 430 - 180 / 1.05, 1.05 + 0.02 * u)

    def draw(CH, FX, big, vv):
        fx.motes(FX, vv, t, 0, 300, 1280, 700, n=30, seed=8)
        Pz = C.molniya_pose(t, False, talk('molniya', t))
        ax, ay = C.horse_anchor(690.0, FEET, U)
        shadow(big, vv, 690.0, FEET, 16 * U, 1.8 * U)
        C.molniya(CH, vv.cam(ax, ay, U), t, Pz, hat=True)
    big = shot(v, t, draw, Light(amb=(1.05, 0.97, 0.88), rim=(1, -1, (255, 236, 190), 0.45), grad=(1.06, 0.9)))
    big[:400] = (big[:400] * np.linspace(0.45, 1.0, 400)[:, None, None]).astype(np.uint8)
    return big


def render(t):
    big = render_scene(t)
    if t >= 2.7:
        k = min(1.0, (t - 2.7) / 0.15)
        O.overlay(big, TITLE, 0, 90, k)
        O.overlay(big, SUB, 0, 250, min(1.0, max(0.0, (t - 3.1) / 0.2)))
        if t >= 3.4: WO.ptext(big, 'СЕЗОН 1 · ПОЛНАЯ ВЕРСИЯ · БЕЗ ЦЕНЗУРЫ · С МОРКОВЬЮ', 960, 370, 22, (255, 255, 255), 'c')
        EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [2.7], 0.15, 0.8)
    return big
