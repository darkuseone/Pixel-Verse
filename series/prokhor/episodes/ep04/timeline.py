"""S01E04 «К ВРАЧУ ЧЕРЕЗ МЕСЯЦ?!» — timing for video (ep04.py) and audio (mix.py). Voice: tightened takes voice/ep04_t. Series-own sounds only."""
DUR = 30.0
FPS = 30
SLUG = 'prokhor'
MASTER = 0.74

VOICE = [
    ('p1', 'ep04_t', 'p1', 0.00, 0.00, 3.11, 'prokhor', 'Запись к зубному — через МЕСЯЦ?!'),
    ('p2', 'ep04_t', 'p2', 3.25, 0.00, 3.66, 'prokhor', 'Лайфхак: нитка и лось. Сам ВЫДЕРНУ!'),
    ('p3b', 'ep04_t', 'p3b', 7.10, 0.00, 3.45, 'prokhor', 'Городские, учитесь! Лось — ТЯНИ!'),
    ('m1', 'ep04_t', 'm1', 11.00, 0.00, 2.43, 'moose', 'Направление ЕСТЬ?'),
    ('m2', 'ep04_t', 'm2', 13.60, 0.00, 4.28, 'moose', 'Без направления не тяну. Талон — у КУКУШКИ.'),
    ('p5', 'ep04_t', 'p5', 18.15, 0.00, 2.98, 'prokhor', 'Кукушка, кукушка... Когда мой ПРИЁМ?'),
    ('p6', 'ep04_t', 'p6', 24.75, 0.00, 1.65, 'prokhor', 'МЕСЯЦ...'),
    ('b1', 'ep04_t', 'b1', 26.85, 0.00, 1.88, 'bear', 'Я за ВАМИ.'),
]

#       selfie wide   moose  tripod CUCKOO plead  calls  count  fall   queue
CUTS = [0.0, 7.00, 10.85, 13.60, 16.00, 18.00, 21.15, 22.90, 24.60, 26.70, DUR]
NAMES = ['selfie', 'wide', 'moose', 'tripod', 'cuckoo', 'plead', 'calls', 'count', 'fall', 'queue']
TWIST = CUTS[4]

X = 'series/prokhor/sfx/'
SFX = [
    (X + 'tooth_throb.mp3', 0.05, 0.85),
    (X + 'phone_notify.mp3', 0.15, 0.70),
    (X + 'tooth_throb.mp3', 3.20, 0.45),
    (X + 'snow_steps_valenki.mp3', 5.20, 0.45),
    (X + 'phone_rec_start.mp3', 7.01, 0.40),
    (X + 'thread_twang.mp3', 7.30, 0.90),
    (X + 'thread_twang.mp3', 9.70, 0.70),
    (X + 'moose_snort.mp3', 10.55, 0.90),
    (X + 'crow_caw.mp3', 13.20, 0.20),
    (X + 'twist_hit.mp3', 16.00, 0.70),
    (X + 'cuckoo_calls.mp3', 16.15, 0.55, 0.0, 0.9),
    (X + 'snow_crawl_in.mp3', 18.00, 0.45),
    (X + 'cuckoo_calls.mp3', 21.15, 0.95, 0.0, 3.4),
    (X + 'tooth_throb.mp3', 23.10, 0.55),
    (X + 'snowdrift_landing.mp3', 25.35, 0.90),
    (X + 'ticket_print.mp3', 26.70, 0.75),
    (X + 'snot_bubble_pop.mp3', 28.75, 0.50),
]

BEDS = [
    ('series/prokhor/sfx/taiga_wind_loop.mp3', 8.0, 0.0, DUR, 0.40, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 2.0, 15.95, 0.20, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 18.0, DUR, 0.17, True),
]

VFX = {'bear': 'aecho=0.6:0.4:35:0.12', 'moose': 'aecho=0.5:0.3:25:0.08'}
VGAIN = {'prokhor': 1.55, 'bear': 1.75, 'moose': 1.6}
