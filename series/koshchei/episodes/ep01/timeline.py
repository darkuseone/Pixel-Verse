"""S01E01 «ПЕНСИЮ НЕ ДАЮТ?!» — timing for video (ep01.py) and audio (mix.py). Voice: tightened takes voice/ep01_t, common_t.
Series-own sounds only (series/koshchei/sfx)."""
DUR = 32.6
FPS = 30
SLUG = 'koshchei'
MASTER = 0.66

VOICE = [
    ('k1', 'ep01_t', 'k1', 0.00, 0.00, 3.68, 'koshchei', '999 лет — и не ПОЛОЖЕНО?!'),
    ('g1', 'ep01_t', 'g1', 3.78, 0.00, 3.47, 'galina', 'С тысячи лет. Год остался. ПОТЕРПИТЕ.'),
    ('k2', 'ep01_t', 'k2', 7.40, 0.00, 2.74, 'koshchei', 'Я — Кощей БЕССМЕРТНЫЙ!'),
    ('g2', 'ep01_t', 'g2', 10.22, 0.00, 1.38, 'galina', 'Вот и ДОЖДЁТЕСЬ.'),
    ('k4', 'ep01_t', 'k4', 11.80, 0.00, 2.93, 'koshchei', 'У-у-у-у! ТРЕПЕЩИТЕ!'),
    ('k5', 'ep01_t', 'k5', 16.75, 0.00, 1.88, 'koshchei', 'Мне — ТЫСЯЧА!'),
    ('g4', 'ep01_t', 'g4', 18.72, 0.00, 1.54, 'galina', 'Повысили. С ДВУХ.'),
    ('k3', 'ep01_t', 'k3', 20.45, 0.00, 2.53, 'koshchei', 'Стаж — тридцать ЦАРСТВ!'),
    ('g3', 'ep01_t', 'g3', 23.08, 0.00, 3.08, 'galina', 'Трудовой нет. Царства — НЕОФИЦИАЛЬНО.'),
    ('k6', 'ep01_t', 'k6', 26.35, 0.00, 2.09, 'koshchei', 'Я ж — БЕССМЕРТНЫЙ.'),
    ('g5', 'ep01_t', 'g5', 28.52, 0.00, 2.14, 'galina', 'Вот. Вам — не к СПЕХУ.'),
    ('z1', 'common_t', 'zhut', 30.80, 0.00, 1.10, 'kuzmich', 'ЖУТЬ.'),
]

#       hook  galina wide  scare  YEAR   stazh  folder deflate zhut  loop
CUTS = [0.0, 3.72, 7.32, 11.70, 16.40, 20.35, 23.03, 26.25, 30.70, 31.95, DUR]
NAMES = ['hook', 'galina', 'wide', 'scare', 'year', 'stazh', 'folder', 'deflate', 'zhut', 'loop']
TWIST = CUTS[4]

X = 'series/koshchei/sfx/'
SFX = [
    (X + 'stamp_thud.mp3', 0.00, 0.95),
    (X + 'biscuit_crunch.mp3', 4.10, 0.70),
    (X + 'biscuit_crunch.mp3', 6.60, 0.50),
    (X + 'whoosh_fast.mp3', 7.30, 0.50),
    (X + 'magic_crackle.mp3', 11.75, 0.80),
    (X + 'thunder_indoor.mp3', 12.40, 0.85),
    (X + 'sign_clack.mp3', 14.85, 1.00),
    (X + 'vhs_rewind.mp3', 16.30, 0.75),
    (X + 'candles_flare.mp3', 16.80, 0.70),
    (X + 'page_flip.mp3', 18.60, 0.70),
    (X + 'twist_choir_hit.mp3', 19.25, 0.85),
    (X + 'stamp_thud.mp3', 19.30, 0.90),
    (X + 'page_flip.mp3', 23.10, 0.55),
    (X + 'biscuit_crunch.mp3', 26.30, 0.55),
    (X + 'breaker_clunk.mp3', 30.70, 0.60),
    (X + 'stamp_thud.mp3', 31.95, 0.60),
    (X + 'whoosh_fast.mp3', 31.60, 0.45),
]

BEDS = [
    ('series/koshchei/sfx/office_amb_loop.mp3', 8.0, 0.0, DUR, 0.40, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 3.72, 16.30, 0.22, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 19.40, DUR, 0.20, True),
]

VGAIN = {'koshchei': 1.5, 'galina': 1.55, 'kuzmich': 1.8}
VFX = {'kuzmich': 'aecho=0.6:0.4:40:0.15'}
