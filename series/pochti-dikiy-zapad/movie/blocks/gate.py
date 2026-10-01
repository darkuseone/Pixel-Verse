"""Chapter 3 intro: Billy and Molniya ride into «Пыльный Кактус» (population 12, more cacti)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *

DUR = 6.6
DAY, INCOME = 340, 8
VOICE = [('e1', 'movie', 'e1', 0.50, 0.00, 5.30, 'molniya', 'ПЫЛЬНЫЙ Кактус. Население — двенадцать. Кактусов — БОЛЬШЕ.')]
SFX = [('library/sfx/film_click.mp3', 0.00, 0.6), ('library/sfx/horse_gallop.mp3', 0.20, 0.5), ('library/sfx/horse_gallop.mp3', 2.30, 0.5),
       ('library/sfx/horse_gallop.mp3', 4.40, 0.5), ('library/sfx/counter_blip.mp3', 2.30, 0.5), ('library/sfx/counter_blip.mp3', 4.10, 0.5)]
BEDS = [('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 0.0, 6.6, 0.26, True),
        ('library/sfx/amb_desert_wind.mp3', 7.8, 0.0, 6.6, 0.6, False)]
EPI = episode('mv_gate', VOICE, DUR)
talk = EPI.talk
GATE = bgworld_t('town_gate', [('ПЫЛЬНЫЙ КАКТУС', 648, 118, 28, (244, 224, 176), (40, 24, 14)),
                               ('НАСЕЛЕНИЕ: 12', 648, 160, 14, (230, 196, 130), (40, 24, 14))], 'v1')
FEET, U = 650.0, 6.0


def rx(t): return -150.0 + 150.0 * t


def draw(CH, FX, big, v, t):
    fx.motes(FX, v, t, 0, 300, 1280, 700, n=30, seed=9)
    fx.dust_puffs(FX, v, t, fx.gallop_dust(t, rx, FEET, max(0, t - 0.8), t, 6, 10))
    Pz, ph = C.gallop(t, 1.5)
    x = rx(t)
    shadow(big, v, x, FEET, 16 * U, 1.8 * U)
    ax, ay = C.horse_anchor(x, FEET, U)
    C.molniya(CH, v.cam(ax, ay, U), t, Pz, rider=C.rider_billy(C.POSES['ride'], 0.0), p=ph, hat=True)


def render_scene(t):
    if t < 2.6: v = wv(GATE, 640, 250, 0.85)
    elif t < 5.0: v = wv(GATE, rx(t) + 150, 480, 1.4)
    else: v = wv(GATE, 650, 175, 1.3 - 0.04 * (t - 5.0))
    return shot(v, t, lambda CH, FX, big, vv: draw(CH, FX, big, vv, t),
                Light(amb=(1.05, 0.97, 0.9), rim=(1, -1, (255, 236, 190), 0.4), grad=(1.06, 0.92)), speed=0.5 if t < 5 else 0.0)


STICK = [(O.sticker('НАСЕЛЕНИЕ 12', fg=(255, 236, 120), size=48), 2.3, 3.9, 960, 300),
         (O.sticker('КАКТУСОВ 400+', fg=(120, 230, 130), size=48), 4.1, 6.4, 960, 300)]


def render(t):
    big = render_scene(t)
    WO.stickers(big, STICK, t)
    WO.hud(big, t, DAY, INCOME)
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [0.0], 0.12, 0.6)
    return big
