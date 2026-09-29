"""Chapter 5 insert: slow-motion canyon jump («Я всегда лечу. Это ты падаешь.»)"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *

DUR = 6.8
DAY, INCOME = 900, 30
VOICE = [
    ('h1', 'movie', 'h1', 0.90, 0.03, 1.95, 'billy',   'Молния, ты ЛЕТИШЬ?!'),
    ('h2', 'movie', 'h2', 3.30, 0.12, 3.40, 'molniya', 'Я всегда лечу. Это ты ПАДАЕШЬ.'),
]
SFX = [('library/sfx/film_click.mp3', 0.00, 0.5), ('library/sfx/horse_gallop.mp3', 0.10, 0.8), ('library/sfx/slowmo_whoosh.mp3', 0.60, 1.0),
       ('library/sfx/horse_gallop.mp3', 5.40, 0.8)]
BEDS = [('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 0.0, 6.8, 0.22, True),
        ('library/sfx/amb_desert_wind.mp3', 7.8, 0.0, 6.8, 0.6, False)]
EPI = episode('mv_jump', VOICE, DUR)
talk = EPI.talk
CANYON = bgworld('canyon')
FEET, U = 684.0, 5.6
T0, T1 = 0.7, 5.4


def pos(t):
    """(x, lift) of Molniya"""
    if t < T0: return 120.0 + 300 * t, 0.0
    if t < T1:
        k = (t - T0) / (T1 - T0)
        return 330.0 + 620 * k, 230 * math.sin(math.pi * k)
    return 950.0 + 260 * (t - T1), 0.0


def draw(CH, FX, big, v, t):
    x, lift = pos(t)
    fx.motes(FX, v, t, 200, 150, 1200, 620, n=40, seed=16)
    fx.dust_puffs(FX, v, t, [(T0, 330, FEET, 24), (T1, 950, FEET, 26)] + fx.gallop_dust(t, lambda tt: pos(tt)[0], FEET, max(0, t - 0.8), min(t, T0), 8, 10)
                  + fx.gallop_dust(t, lambda tt: pos(tt)[0], FEET, max(T1, t - 0.8), t, 8, 10) if t >= T1 else
                  [(T0, 330, FEET, 24)] + fx.gallop_dust(t, lambda tt: pos(tt)[0], FEET, max(0, t - 0.8), min(t, T0), 8, 10))
    ts = t if (t < T0 or t >= T1) else T0 + (t - T0) * 0.4
    Pz, ph = C.gallop(ts)
    if lift > 0: Pz = dict(Pz, pitch=-0.12)
    shadow(big, v, x, FEET, 16 * U * (1 - 0.25 * lift / 230), 1.8 * U, a=0.45 * (1 - 0.6 * lift / 230))
    ax, ay = C.horse_anchor(x, FEET - lift, U)
    C.molniya(CH, v.cam(ax, ay, U), t, Pz, rider=C.rider_billy(C.POSES['ride_whip'] if 0.7 <= t < 2.6 else C.POSES['ride'], talk('billy', t)), p=ph, hat=True)


def render_scene(t):
    x, lift = pos(t)
    v = wv(CANYON, x + 80, FEET - 130 - 0.95 * lift, 1.25)
    return shot(v, t, lambda CH, FX, big, vv: draw(CH, FX, big, vv, t),
                Light(amb=(1.06, 0.95, 0.83), rim=(1, -1, (255, 232, 170), 0.5), grad=(1.08, 0.86)),
                speed=0.4 if (t < T0 or t >= T1) else 0.0)


def render(t):
    big = render_scene(t)
    if T0 <= t < T1: fx.shafts(big, t, angle=2.3, a=0.05, col=(255, 226, 160))
    WO.hud(big, t, DAY, INCOME)
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [0.0, T0], 0.12, 0.5)
    return big
