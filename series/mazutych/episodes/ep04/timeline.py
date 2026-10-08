"""S01E04 v2 «Без прав» (08.10.2026, по статистике TikTok) — timing for video (ep04.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep04_t)."""
DUR = 29.4
FPS = 30
SLUG = 'mazutych'
MASTER = 0.75

VOICE = [
    ('c1', 'ep04_t', 'c1', 0.00, 0.00, 2.28, 'cop', 'Стоять! ПРЕВЫШАЕМ, гражданин!'),
    ('m1', 'ep04_t', 'm1', 2.40, 0.00, 1.61, 'maz', 'Двадцать пять В ЧАС.'),
    ('c3', 'ep04_t', 'c3', 4.15, 0.00, 2.71, 'cop', 'Права категории «МОНО» есть?'),
    ('m2', 'ep04_t', 'm2', 6.95, 0.00, 1.37, 'maz', 'Такой НЕТ.'),
    ('c4', 'ep04_t', 'c4', 8.45, 0.00, 2.25, 'cop', 'Значит, БЕЗ ПРАВ.'),
    ('w1', 'ep04_t', 'w1', 10.85, 0.00, 2.74, 'wheel', 'У меня есть права, друга. КИТАЙСКИЙ.'),
    ('c5', 'ep04_t', 'c5', 13.70, 0.00, 1.92, 'cop', 'Документики на ТРАНСПОРТ!'),
    ('m3', 'ep04_t', 'm3', 15.70, 0.00, 1.70, 'maz', 'Вот. От ШЕСТЁРКИ.'),
    ('c6', 'ep04_t', 'c6', 17.50, 0.00, 2.52, 'cop', 'Ладно... ДОТАЩИШЬ — отпущу.'),
    ('c7', 'ep04_t', 'c7', 20.15, 0.00, 1.86, 'cop', 'Третий день БЕЗ БЕНЗИНА.'),
    ('d1', 'ep04_t', 'd1', 23.60, 0.00, 3.32, 'tolik', 'Мужики, а КТО КОГО остановил?!'),
    ('c8', 'ep04_t', 'c8', 27.05, 0.00, 2.04, 'cop', 'УИ-У! УИ-У!'),
]

#        hook  sign  cat   none  fine  licen docs  wheel WHISPR bushes tow    tolik  siren
CUTS = [0.0, 2.30, 4.10, 6.90, 8.40, 10.80, 13.65, 15.65, 17.45, 20.10, 22.10, 23.60, 27.00, DUR]
TWIST = 17.45

S = 'library/sfx/'
SFX = [
    (S + 'police_whistle.mp3', 0.00, 0.6),
    (S + 'paper_crumple_slap.mp3', 0.30, 0.4),
    (S + 'brake_skid.mp3', 2.30, 0.5),
    (S + 'whoosh.mp3', 4.05, 0.4),
    (S + 'pencil_scribble.mp3', 8.70, 0.6),
    (S + 'app_notify_ping.mp3', 10.80, 0.5),
    (S + 'paper_crumple_slap.mp3', 15.75, 0.4),
    (S + 'record_scratch.mp3', 17.45, 0.5),
    (S + 'curtain_reveal.mp3', 20.10, 0.4),
    (S + 'rope_strain_creak.mp3', 22.10, 0.5),
    (S + 'truck_horn_old.mp3', 23.55, 0.6),
    (S + 'police_whistle.mp3', 29.05, 0.3),
]

BEDS = [
    ('library/sfx/amb_refinery.mp3', 7.8, 0.0, DUR, 0.45, False),
    ('library/sfx/monowheel_whine.mp3', 3.8, 22.1, 27.0, 0.25, True),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 0.0, DUR, 0.22, True),
]

VFX = {'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25'}
VGAIN = {'maz': 1.6, 'cop': 1.5, 'wheel': 1.45, 'tolik': 1.5}
