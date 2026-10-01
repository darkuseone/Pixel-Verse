"""Ad break: «Страхование от Кривого Сэма» (Sam sells insurance against himself)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *

DUR = 14.8
VOICE = [
    ('r1', 'movie', 'r1', 0.90, 0.00, 3.97, 'sam', 'Кривой Сэм. Страхование от Кривого СЭМА.'),
    ('r2', 'movie', 'r2', 5.20, 0.00, 5.10, 'sam', 'Ограбил Сэм? Звоните СЭМУ. Он перезвонит. ПОЗЖЕ.'),
    ('r3', 'movie', 'r3', 10.70, 0.00, 3.10, 'sam', 'Условия — МЕЛКИМ шрифтом. На вашем кошельке.'),
]
SFX = [
    ('library/sfx/ad_jingle_zapad.mp3', 0.00, 0.9),
    ('library/sfx/film_click.mp3', 5.00, 0.6),
    ('library/sfx/counter_blip.mp3', 3.30, 0.6),
    ('library/sfx/paper_unroll.mp3', 10.60, 0.7),
]
BEDS = [('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 0.0, 14.8, 0.22, True)]
EPI = episode('mv_ad', VOICE, DUR)
talk = EPI.talk
STUDIO = bgworld('ad_studio')
TAG = O.pixel_title(['РЕКЛАМНАЯ ПАУЗА'], 60, width=1920)
FEET, U = 640.0, 8.0


def light():
    return Light(amb=(1.1, 0.98, 0.86), rim=(0, -1, (255, 230, 160), 0.5), grad=(1.15, 0.85))


def board_text(CH, v, t):
    """text on the easel (world board x 895..1075, y 215..430)"""
    lines = [('КРИВОЙ СЭМ', 8, (140, 36, 26), 240), ('СТРАХОВАНИЕ', 8, (60, 40, 30), 270), ('ОТ КРИВОГО', 8, (60, 40, 30), 290),
             ('СЭМА', 8, (60, 40, 30), 310), ('8-800-СЭМ-СЭМ', 8, (30, 90, 40), 345)]
    for txt, size, col, wy in lines:
        sx, sy = v.pt(985, wy); px_text(CH, txt, sx, sy, size, col)
    if t >= 10.7:                                                     # the fine print
        for i in range(8):
            wrect_l = Layer(v.wcam()); wrect(wrect_l, 905, 368 + i * 7, 1065 - (i % 3) * 12, 369 + i * 7, (90, 80, 70)); CH.add(wrect_l)


def draw(CH, FX, big, v, t):
    fx.motes(FX, v, t, 200, 100, 1100, 600, n=40, col=(255, 236, 170), seed=1)
    if t < 5.0: x, flip, pose = 560.0, False, C.POSES['present']
    elif t < 10.5: x, flip, pose = lerp(560, 430, sm((t - 5.0) / 0.6)), True, C.POSES['point']
    else: x, flip, pose = 760.0, False, C.POSES['point']
    shadow(big, v, x, FEET, 5 * U, 1.2 * U)
    C.sam(CH, v.cam(x, FEET - C.HIP_H * U, U, flip), pose, 0.03, talk('sam', t))
    if 5.2 <= t < 10.0:                                               # the phone rings on the desk
        pass
    board_text(CH, v, t)


def render_scene(t):
    if t < 5.0: v = wv(STUDIO, 640, 470, 1.0)
    elif t < 10.4: v = wv(STUDIO, 400, 450, 1.55 - 0.03 * (t - 5.0))
    else: v = wv(STUDIO, 930 - 15 * (t - 10.4), 430, 1.6 + 0.3 * min(1.0, (t - 10.4) / 3.0))
    return shot(v, t, lambda CH, FX, big, vv: draw(CH, FX, big, vv, t), light(), vig=0.25)


def render(t):
    big = render_scene(t)
    crt(big)
    if t < 2.0: O.overlay(big, TAG, 0, 80, min(1.0, t / 0.1) * (1 - sm((t - 1.8) / 0.2)))
    WO.ptext(big, '● РЕКЛАМА', 1880, 60, 28, (255, 90, 80), 'r')
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [0.0, 5.0, 10.6], 0.12, 0.6)
    return big
