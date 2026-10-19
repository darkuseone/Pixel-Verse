"""S01E04 «БАТАРЕИ ЛЕДЯНЫЕ?!» — timing for video (ep04.py) and audio (mix.py). Voice: voice/ep04_t, common_t. Series-own sounds only.
k3 is used only up to its first sentence («Я — Кощей Бессмертный!», 0–2.45 s)."""
DUR = 30.2
FPS = 30
SLUG = 'koshchei'
MASTER = 0.66

VOICE = [
    ('k1', 'ep04_t', 'k1', 0.00, 0.00, 3.81, 'koshchei', 'Октябрь — а батареи ЛЕДЯНЫЕ!'),
    ('g1', 'ep04_t', 'g1', 3.90, 0.00, 3.50, 'galina', 'Отопительный сезон открыт. Батарею — ПОТРОГАЙТЕ.'),
    ('g2', 'ep04_t', 'g2', 7.95, 0.00, 2.27, 'galina', 'Значит, до вас — не ДОШЛО.'),
    ('k3', 'ep04_t', 'k3', 10.30, 0.00, 2.45, 'koshchei', 'Я — Кощей БЕССМЕРТНЫЙ!'),
    ('g3', 'ep04_t', 'g3', 12.85, 0.00, 2.35, 'galina', 'Бессмертный — не значит ТЁПЛЫЙ.'),
    ('k4', 'ep04_t', 'k4', 15.45, 0.00, 2.30, 'koshchei', 'Тепло — УТЕКАЕТ.'),
    ('y1', 'ep04_t', 'y1', 18.20, 0.00, 2.46, 'yaga', 'Ножки МЁРЗНУТ.'),
    ('k5', 'ep04_t', 'k5', 20.80, 0.00, 1.85, 'koshchei', 'Это ж ОБЩЕЕ тепло!'),
    ('y2', 'ep04_t', 'y2', 22.75, 0.00, 3.13, 'yaga', 'Было общее. Теперь — НАСИЖЕННОЕ.'),
    ('z1', 'common_t', 'zhut', 27.75, 0.00, 1.10, 'kuzmich', 'ЖУТЬ.'),
]

#       hook  galina stuck  proud  carpet HUT    common egg    zhut   loop
CUTS = [0.0, 3.85, 7.45, 10.25, 14.95, 17.85, 20.65, 25.95, 27.65, 28.90, DUR]
NAMES = ['hook', 'galina', 'stuck', 'proud', 'carpet', 'hut', 'common', 'egg', 'zhut', 'loop']
TWIST = CUTS[5]

X = 'series/koshchei/sfx/'
SFX = [
    (X + 'ice_ting.mp3', 0.00, 0.95),
    (X + 'teeth_chatter.mp3', 0.40, 0.65),
    (X + 'phone_ring_old.mp3', 3.85, 0.35, 0.0, 0.9),
    (X + 'ice_ting.mp3', 7.50, 0.90),
    (X + 'teeth_chatter.mp3', 10.40, 0.50),
    (X + 'phone_click.mp3', 15.10, 0.60),
    (X + 'carpet_swish.mp3', 14.95, 0.80),
    (X + 'pipe_steam_soft.mp3', 15.30, 0.80),
    (X + 'hen_cluck.mp3', 17.85, 0.85),
    (X + 'twist_choir_hit.mp3', 17.88, 0.70),
    (X + 'basin_splash.mp3', 18.40, 0.60),
    (X + 'pipe_steam_soft.mp3', 20.70, 0.60),
    (X + 'wood_legs_creak.mp3', 26.00, 0.80),
    (X + 'hen_cluck.mp3', 26.20, 0.90),
    (X + 'egg_crack_shell.mp3', 26.90, 0.55),
    (X + 'wood_legs_creak.mp3', 27.30, 0.60),
    (X + 'ice_ting.mp3', 28.95, 0.90),
]

BEDS = [
    ('series/koshchei/sfx/stairwell_amb_loop.mp3', 8.0, 0.0, 14.95, 0.30, True),
    ('series/koshchei/sfx/eerie_wind_howl.mp3', 2.5, 14.95, 27.65, 0.30, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 3.85, 17.80, 0.18, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 18.40, DUR, 0.18, True),
]

PHONE = 'highpass=f=320,lowpass=f=3400,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {'kuzmich': 'aecho=0.6:0.4:40:0.15'}
VGAIN = {'koshchei': 1.5, 'galina': 1.55, 'yaga': 1.5, 'kuzmich': 1.8}
