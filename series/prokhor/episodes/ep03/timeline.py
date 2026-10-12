"""S01E03 «МАЛИНА ПО 900?!» — timing for video (ep03.py) and audio (mix.py). Voice: tightened takes voice/ep03_t. Series-own sounds only."""
DUR = 29.8
FPS = 30
SLUG = 'prokhor'
MASTER = 0.76

VOICE = [
    ('p1', 'ep03_t', 'p1', 0.00, 0.00, 1.87, 'prokhor', 'Девятьсот за МАЛИНУ?!'),
    ('p2', 'ep03_t', 'p2', 2.00, 0.00, 4.39, 'prokhor', 'Лайфхак: тайга — бесплатный магазин. Иду за ПОКУПКАМИ!'),
    ('p3', 'ep03_t', 'p3', 6.75, 0.00, 2.51, 'prokhor', 'Маскхалат. Чтоб медведь не ВИДЕЛ.'),
    ('p4', 'ep03_t', 'p4', 9.45, 0.00, 6.05, 'prokhor', 'Малина. Гриб. Шишка. Всё — даром! Городские, УЧИТЕСЬ!'),
    ('s1', 'ep03_t', 's1', 16.85, 0.00, 2.94, 'squirrel', 'Мужчина! Пакетик откройте. Малина — по ВЕСУ.'),
    ('p5', 'ep03_t', 'p5', 19.95, 0.00, 1.29, 'prokhor', 'Я ж в ТАЙГЕ!'),
    ('s2', 'ep03_t', 's2', 21.40, 0.00, 1.58, 'squirrel', 'Тайга — по КАРТЕ.'),
    ('b1', 'ep03_t', 'b1', 23.60, 0.00, 3.88, 'bear', 'Карта «Берлога-Плюс» есть? Нет? ДЕВЯТЬСОТ.'),
]

#       selfie camo   eat    CAM    guard  protest seed  till
CUTS = [0.0, 6.45, 9.35, 15.55, 16.60, 19.85, 21.30, 23.20, DUR]
NAMES = ['selfie', 'camo', 'eat', 'cam', 'guard', 'protest', 'seed', 'till']
TWIST = CUTS[3]

X = 'series/prokhor/sfx/'
SFX = [
    (X + 'phone_notify.mp3', 0.10, 0.80),
    (X + 'breath_frost.mp3', 1.40, 0.40),
    (X + 'snow_steps_valenki.mp3', 3.80, 0.55),
    (X + 'crow_caw.mp3', 5.40, 0.22),
    (X + 'phone_rec_start.mp3', 6.46, 0.40),
    (X + 'branches_rustle.mp3', 6.50, 0.90),
    (X + 'snow_crawl_in.mp3', 8.10, 0.45),
    (X + 'branches_rustle.mp3', 9.40, 0.45),
    (X + 'berry_munch.mp3', 10.10, 0.75),
    (X + 'berry_munch.mp3', 12.60, 0.65),
    (X + 'cam_servo_beep.mp3', 15.55, 0.95),
    (X + 'twist_hit.mp3', 15.60, 0.70),
    (X + 'small_jump_land.mp3', 16.98, 0.95),
    (X + 'tablet_tap.mp3', 18.20, 0.80),
    (X + 'seed_spit.mp3', 22.85, 0.90),
    (X + 'barcode_beep.mp3', 23.35, 0.80),
    (X + 'barcode_beep.mp3', 27.60, 1.00),
    (X + 'cash_drawer.mp3', 28.00, 0.80),
]

BEDS = [
    ('series/prokhor/sfx/taiga_wind_loop.mp3', 8.0, 0.0, DUR, 0.40, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 2.0, 15.50, 0.20, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 19.85, DUR, 0.18, True),
]

VFX = {'bear': 'aecho=0.6:0.4:35:0.12'}
VGAIN = {'prokhor': 1.55, 'bear': 1.75, 'squirrel': 1.5}
