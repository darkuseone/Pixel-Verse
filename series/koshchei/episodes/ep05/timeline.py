"""S01E05 «СВЕТ ОТКЛЮЧАТ?!» — timing for video (ep05.py) and audio (mix.py). Voice: voice/ep05_t, common_t. Series-own sounds only."""
DUR = 30.4
FPS = 30
SLUG = 'koshchei'
MASTER = 0.66

VOICE = [
    ('k1', 'ep05_t', 'k1', 0.00, 0.00, 2.48, 'koshchei', 'Свет отрезать — в ХЭЛЛОУИН?!'),
    ('g1', 'ep05_t', 'g1', 2.58, 0.00, 4.21, 'galina', 'Долг за свет — 47 рублей. С 1902-ГО.'),
    ('k2', 'ep05_t', 'k2', 6.90, 0.00, 2.66, 'koshchei', 'Я — Кощей БЕССМЕРТНЫЙ!'),
    ('g2', 'ep05_t', 'g2', 9.65, 0.00, 1.59, 'galina', 'А долг — ВЕЧНЫЙ.'),
    ('y1', 'ep05_t', 'y1', 11.60, 0.00, 2.95, 'yaga', 'Ну вот. Теперь — АТМОСФЕРА.'),
    ('g3', 'ep05_t', 'g3', 16.75, 0.00, 2.87, 'galina', 'Кощей Кощеевич. Проводите до ВЫХОДА.'),
    ('k3', 'ep05_t', 'k3', 19.85, 0.00, 2.48, 'koshchei', 'Свет — по ГРАФИКУ.'),
    ('y2', 'ep05_t', 'y2', 22.55, 0.00, 3.13, 'yaga', 'Кощей! Ты — СТРАШНЫЙ!'),
    ('k4', 'ep05_t', 'k4', 25.80, 0.00, 0.84, 'koshchei', 'ПРАВДА?'),
    ('y3', 'ep05_t', 'y3', 26.75, 0.00, 1.52, 'yaga', 'С лица — ДА.'),
    ('z1', 'common_t', 'zhut2', 28.35, 0.00, 1.10, 'kuzmich', 'ЖУТЬ.'),
]

#       hook  debt   eternal party  alone  TWIST  guide  yard   zhut   loop
CUTS = [0.0, 2.55, 6.85, 11.30, 14.50, 16.60, 19.75, 22.45, 28.25, 29.45, DUR]
NAMES = ['hook', 'debt', 'eternal', 'party', 'alone', 'twist', 'guide', 'yard', 'zhut', 'loop']
TWIST = CUTS[5]

X = 'series/koshchei/sfx/'
SFX = [
    (X + 'wire_cutters.mp3', 0.00, 0.90),
    (X + 'party_ghost_music_low.mp3', 0.10, 0.55),
    (X + 'page_flip.mp3', 2.70, 0.60),
    (X + 'wire_cutters.mp3', 11.10, 1.00),
    (X + 'power_down.mp3', 11.20, 0.85),
    (X + 'tape_slowdown.mp3', 11.35, 0.70),
    (X + 'drips_echo.mp3', 14.50, 0.75),
    (X + 'chute_moan.mp3', 15.10, 0.70),
    (X + 'magic_crackle.mp3', 16.55, 0.70),
    (X + 'twist_choir_hit.mp3', 16.60, 0.80),
    (X + 'slipper_stairs_run.mp3', 19.90, 0.40),
    (X + 'door_open_creak.mp3', 22.45, 0.55),
    (X + 'breaker_clunk.mp3', 28.30, 0.95),
    (X + 'party_ghost_music_low.mp3', 28.45, 0.55),
    (X + 'power_down.mp3', 29.40, 0.60),
    (X + 'wire_cutters.mp3', 29.85, 0.80),
]

BEDS = [
    ('series/koshchei/sfx/stairwell_amb_loop.mp3', 8.0, 0.0, DUR, 0.35, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 2.55, 11.20, 0.20, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 19.75, DUR, 0.20, True),
]

VFX = {'kuzmich': 'aecho=0.6:0.4:40:0.15'}
VGAIN = {'koshchei': 1.5, 'galina': 1.55, 'yaga': 1.5, 'kuzmich': 1.8}
