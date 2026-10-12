"""S01E05 «ШТРАФ ЗА КОСТЁР?!» — timing for video (ep05.py) and audio (mix.py). Voice: tightened takes voice/ep05_t. Series-own sounds only."""
DUR = 30.2
FPS = 30
SLUG = 'prokhor'
MASTER = 0.74

VOICE = [
    ('p1', 'ep05_t', 'p1', 0.05, 0.00, 1.56, 'prokhor', 'Штраф за КОСТЁР?!'),
    ('r1', 'ep05_t', 'r1', 1.95, 0.00, 2.96, 'ranger', 'И за дым. И за запах. ПОДПИСЫВАЙТЕ!'),
    ('p2', 'ep05_t', 'p2', 5.15, 0.00, 5.25, 'prokhor', 'Лайфхак: маскировка «ёлочка». Ни дрон, ни егерь — не УВИДЯТ!'),
    ('p3', 'ep05_t', 'p3', 10.85, 0.00, 2.98, 'prokhor', 'Ёлка. Гирлянда. НЕВИДИМКА.'),
    ('r2', 'ep05_t', 'r2', 18.10, 0.00, 2.26, 'ranger', 'Ёлочка! СПРЯЧЬ меня!'),
    ('r3', 'ep05_t', 'r3', 22.90, 0.00, 1.21, 'ranger', 'Он УШЁЛ?'),
    ('p4', 'ep05_t', 'p4', 24.30, 0.00, 3.47, 'prokhor', 'Укрытие. По тарифу. Плюс ПЕНИ.'),
    ('b1', 'ep05_t', 'b1', 28.20, 0.00, 1.28, 'bear', 'УЧИТСЯ.'),
]

#       slap  ranger lifehack wide  drone  BEAR   run    sniff  fine   button
CUTS = [0.0, 1.85, 5.00, 10.60, 14.60, 16.40, 18.00, 21.00, 24.20, 28.00, DUR]
NAMES = ['slap', 'ranger', 'hack', 'wide', 'drone', 'bear', 'run', 'sniff', 'fine', 'button']
TWIST = CUTS[5]

X = 'series/prokhor/sfx/'
SFX = [
    (X + 'paper_slap_ice.mp3', 0.00, 0.90),
    (X + 'snowmobile_arrive.mp3', 1.40, 0.55),
    (X + 'pen_signature.mp3', 3.80, 0.50),
    (X + 'phone_rec_start.mp3', 5.01, 0.40),
    (X + 'branches_rustle.mp3', 7.20, 0.90),
    (X + 'garland_on.mp3', 8.15, 0.90),
    (X + 'drone_buzz.mp3', 10.60, 0.75),
    (X + 'drone_buzz.mp3', 13.40, 0.80),
    (X + 'sign_knock.mp3', 15.85, 1.00),
    (X + 'twist_hit.mp3', 16.40, 0.70),
    (X + 'bear_wake_growl.mp3', 16.45, 1.00),
    (X + 'snow_run_panic.mp3', 18.00, 0.90),
    (X + 'snow_run_panic.mp3', 19.80, 0.70),
    (X + 'branches_rustle.mp3', 20.50, 1.00),
    (X + 'breath_frost.mp3', 21.20, 0.70),
    (X + 'snow_steps_valenki.mp3', 22.40, 0.50),
    (X + 'receipt_tear.mp3', 26.55, 0.90),
    (X + 'paper_slap_ice.mp3', 27.10, 0.90),
    (X + 'drone_crunch.mp3', 28.00, 1.00),
]

BEDS = [
    ('series/prokhor/sfx/taiga_wind_loop.mp3', 8.0, 0.0, DUR, 0.35, True),
    ('series/prokhor/sfx/campfire_loop.mp3', 8.0, 0.0, 10.6, 0.90, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 2.0, 16.35, 0.20, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 18.0, DUR, 0.17, True),
]

VFX = {'bear': 'aecho=0.6:0.4:35:0.12'}
VGAIN = {'prokhor': 1.55, 'bear': 1.75, 'ranger': 1.5}
