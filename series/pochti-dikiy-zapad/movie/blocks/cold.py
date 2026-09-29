"""Cold open: slow-mo flight into the cactus (from the finale), freeze, Molniya narrates, VHS rewind to day 1."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *
import importlib

_p = str(HERE / 'chapters' / 'ch_ep06')
sys.path.insert(0, _p); sys.modules.pop('timeline', None)
E6 = importlib.import_module('ep06')
sys.modules.pop('timeline', None); sys.path.remove(_p)

DUR = 19.2
T_FREEZE, T_REW = 3.4, 16.3
E_FRZ = 26.85
VOICE = [
    ('c2', 'ep01',  'c2', 0.00, 0.10, 2.16, 'billy',   'А-А-А-А-А!'),
    ('x2', 'movie', 'x2', 3.75, 0.00, 2.60, 'molniya', 'Это Билли. Он летит в КАКТУС.'),
    ('x3', 'movie', 'x3', 6.80, 0.00, 3.30, 'molniya', 'Как он туда попал? Придётся отмотать три ГОДА.'),
    ('x4', 'movie', 'x4', 10.55, 0.00, 2.65, 'billy',   'Молния, сними с ПАУЗЫ!'),
    ('x5', 'movie', 'x5', 13.50, 0.00, 2.50, 'molniya', 'Не сейчас. Ты ПОВИСИШЬ.'),
]
SFX = [
    ('library/sfx/slowmo_whoosh.mp3', 0.00, 0.9),
    ('library/sfx/record_scratch.mp3', 3.35, 1.0),
    ('library/sfx/vhs_rewind.mp3', 16.30, 1.0),
]
BEDS = [
    ('series/pochti-dikiy-zapad/music/finale_fanfare_15s.mp3', 14.9, 0.0, 3.4, 0.30, True),
]
EPI = episode('mv_cold', VOICE, DUR)
HOOK = O.pixel_title(['ЗАЧЕМ ОН ЛЕТИТ', 'В КАКТУС?'], 64, width=1920)
_frz = {}


def e6_time(t):
    if t < T_FREEZE: return 25.3 + 0.47 * t
    if t < T_REW: return E_FRZ
    u = (t - T_REW) / (DUR - T_REW)
    return max(0.0, E_FRZ * (1 - u ** 1.6))


def render_scene(t):
    te = e6_time(t)
    if T_FREEZE <= te <= 27.7 and T_FREEZE <= t < T_REW:
        if 'f' not in _frz: _frz['f'] = E6.render_scene(E_FRZ)
        big = _frz['f'].copy()
    else:
        big = E6.render_scene(te)
    if t < T_FREEZE:
        fx.speed_lines(big, t, 0.5)
    elif t < T_REW:
        k = min(1.0, (t - T_FREEZE) / 0.25)
        big = sepia(big, 0.7 * k)
        big = zoom_crop(big, 1.0 + 0.028 * (t - T_FREEZE), 0.92, 0.0)
        fx.vignette(big, 0.35)
    return big


def render(t):
    big = render_scene(t)
    rew = t >= T_REW
    if rew:
        u = (t - T_REW) / (DUR - T_REW)
        fx.vhs(big, t, 1.0)
        day = max(1, int(1096 * (1 - u ** 1.6))); inc = int(158 * (1 - u ** 1.6))
        if int(t * 5) % 2 == 0: WO.ptext(big, '◀◀ ПЕРЕМОТКА', 1880, 70, 32, (255, 255, 255), 'r')
    else:
        day, inc = 1096, 158
    WO.hud(big, t, day, inc)
    if T_FREEZE <= t < T_REW:
        WO.ptext(big, '❚❚ ПАУЗА', 1880, 70, 32, (255, 255, 255), 'r')
    if 0.2 <= t < 2.4:
        O.overlay(big, HOOK, 0, 300, min(1.0, (t - 0.2) / 0.1) * (1 - sm((t - 2.2) / 0.2)))
    if not rew: EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [0.0], 0.12, 0.6)
    return big
