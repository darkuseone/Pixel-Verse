"""S01E03 «РЕМОНТ В 7 УТРА?!» — timing for video (ep03.py) and audio (mix.py). Voice: voice/ep03_t, common_t. Series-own sounds only.
Горыныч: one designed voice, three heads = three pitches (gorynych2 bass / gorynych3 squeak via VFX)."""
DUR = 30.0
FPS = 30
SLUG = 'koshchei'
MASTER = 0.66

VOICE = [
    ('k1', 'ep03_t', 'k1', 0.00, 0.00, 2.74, 'koshchei', 'В семь утра?! Я только ЛЁГ!'),
    ('r1', 'ep03_t', 'r1', 2.95, 0.00, 3.29, 'gorynych2', 'Тишина — с двадцати трёх. А сейчас — ДЕНЬ.'),
    ('k3', 'ep03_t', 'k3', 6.35, 0.00, 2.59, 'koshchei', 'Я — Кощей БЕССМЕРТНЫЙ!'),
    ('r2', 'ep03_t', 'r2', 9.05, 0.00, 2.69, 'gorynych3', 'А я — трёхголовый. И ЧТО?'),
    ('k4', 'ep03_t', 'k4', 11.95, 0.00, 4.34, 'koshchei', 'У-у-у-у! Спокойной ночи, СОСЕДУШКА.'),
    ('g1', 'ep03_t', 'g1', 16.65, 0.00, 2.59, 'galina', 'Шум после двадцати трёх. ШТРАФ.'),
    ('k5', 'ep03_t', 'k5', 19.35, 0.00, 1.99, 'koshchei', 'Вы ж — в СОЦФОНДЕ!'),
    ('g2', 'ep03_t', 'g2', 21.42, 0.00, 1.33, 'galina', 'По СОВМЕСТИТЕЛЬСТВУ.'),
    ('k6', 'ep03_t', 'k6', 22.95, 0.00, 2.14, 'koshchei', 'А он — СВЕРЛИТ!'),
    ('g3', 'ep03_t', 'g3', 25.17, 0.00, 1.91, 'galina', 'Он — днём. По ЗАКОНУ.'),
    ('z1', 'common_t', 'zhut', 27.30, 0.00, 1.10, 'kuzmich', 'ЖУТЬ.'),
]

#       hook  door   haughty heads revenge duvets DOORBELL fake  law    zhut   loop
CUTS = [0.0, 2.90, 6.30, 9.00, 11.85, 14.30, 16.45, 19.30, 22.85, 27.20, 28.40, DUR]
NAMES = ['hook', 'door', 'haughty', 'heads', 'revenge', 'duvets', 'doorbell', 'fake', 'law', 'zhut', 'loop']
TWIST = CUTS[6]

X = 'series/koshchei/sfx/'
SFX = [
    (X + 'hammer_drill.mp3', 0.00, 0.95),
    (X + 'coffin_lid_bang.mp3', 0.30, 0.70),
    (X + 'plaster_fall.mp3', 0.60, 0.60),
    (X + 'slipper_stairs_run.mp3', 1.90, 0.55),
    (X + 'hammer_drill.mp3', 3.00, 0.45),
    (X + 'hammer_drill.mp3', 9.20, 0.40),
    (X + 'magic_crackle.mp3', 11.90, 0.80),
    (X + 'chains_rattle.mp3', 12.10, 0.75),
    (X + 'eerie_wind_howl.mp3', 12.20, 0.55),
    (X + 'bulb_pop.mp3', 13.30, 0.85),
    (X + 'whoosh_fast.mp3', 14.30, 0.50),
    (X + 'doorbell_old.mp3', 16.40, 0.90),
    (X + 'twist_choir_hit.mp3', 16.45, 0.75),
    (X + 'door_open_creak.mp3', 16.80, 0.55),
    (X + 'page_flip.mp3', 18.40, 0.55),
    (X + 'hammer_drill.mp3', 23.10, 0.45),
    (X + 'plaster_fall.mp3', 26.00, 0.75),
    (X + 'breaker_clunk.mp3', 27.20, 0.50),
    (X + 'hammer_drill.mp3', 29.25, 0.90),
]

BEDS = [
    ('series/koshchei/sfx/stairwell_amb_loop.mp3', 8.0, 0.0, DUR, 0.38, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 2.90, 11.80, 0.20, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 17.40, DUR, 0.18, True),
]

VFX = {'gorynych2': 'asetrate=44100*0.84,aresample=44100,atempo=1.15', 'gorynych3': 'asetrate=44100*1.22,aresample=44100,atempo=0.82',
       'kuzmich': 'aecho=0.6:0.4:40:0.15'}
VGAIN = {'koshchei': 1.5, 'gorynych2': 1.6, 'gorynych3': 1.5, 'galina': 1.55, 'kuzmich': 1.8}
