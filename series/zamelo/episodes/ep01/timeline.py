"""S01E01 «ОСТАВЛЕН У ДВЕРИ?!» — timing for video (ep01.py) and audio (mix.py). Voice: tightened takes voice/ep01_t (tempo 1.06–1.08).
Sound: own sounds of the series (series/zamelo/sfx) + CC0 library (whoosh, sms, boing, rimshot, scratch, snow steps) + a cheerful CC0 bed."""
DUR = 37.7
FPS = 30
SLUG = 'zamelo'
LUFS = -14.0

VOICE = [
    ('c0', 'ep01_t', 'c0', 0.00, 0.00, 4.83, 'chayka', 'Дальний Восток. Снег — по девятый этаж. А Жоре посылку оставили «у ДВЕРИ».'),
    ('z1', 'ep01_t', 'z1', 4.88, 0.00, 3.03, 'zhora', 'Как это — «оставлен у двери»?! Моя дверь — под СНЕГОМ!'),
    ('z2', 'ep01_t', 'z2', 7.96, 0.00, 3.76, 'zhora', 'Кыш, баклан! Мы, дальневосточники, — привычные. ОТКОПАЮ!'),
    ('c2', 'ep01_t', 'c2', 11.76, 0.00, 2.67, 'chayka', 'Я — чайка. Баклан — это ТЫ.'),
    ('n1', 'ep01_t', 'n1', 15.05, 0.00, 3.54, 'nina', 'Жорик, так курьер же по КРЫШАМ ходит!'),
    ('z4', 'ep01_t', 'z4', 18.15, 0.00, 1.78, 'zhora', 'Некогда, баба Нина!'),
    ('z5', 'ep01_t', 'z5', 19.98, 0.00, 2.62, 'zhora', 'Двадцать семь МЕТРОВ! И где посылка?!'),
    ('i2', 'ep01_t', 'i2', 22.83, 0.00, 3.55, 'ira', 'Жора! Она у НАШЕЙ двери! Курьер через КРЫШУ ходит!'),
    ('z6', 'ep01_t', 'z6', 26.53, 0.00, 2.06, 'zhora', 'А чего он в ОКНО не постучал?!'),
    ('v1', 'ep01_t', 'v1', 29.78, 0.00, 3.00, 'vitek', 'Братан, окно — это не АДРЕС. Оцени доставку!'),
    ('z7', 'ep01_t', 'z7', 32.93, 0.00, 1.63, 'zhora', 'Одна ЗВЕЗДА.'),
    ('c3', 'ep01_t', 'c3', 35.33, 0.00, 1.25, 'chayka', 'Себе ПОСТАВЬ.'),
]

#       gull   cut    phone  zcu    kysh   baklan dig    shaft_a shaft_b bottom twist  up     vitek  star   button
CUTS = [0.0, 1.55, 4.88, 5.90, 7.96, 11.76, 14.45, 15.05, 18.05, 19.95, 22.68, 26.48, 29.73, 32.83, 35.25, DUR]
NAMES = ['gull', 'cut', 'phone', 'zcu', 'kysh', 'baklan', 'dig', 'shaft_a', 'shaft_b', 'bottom', 'twist', 'up', 'vitek', 'star', 'button']
TWIST = CUTS[10]                 # 22.68 / 37.7 = 60 %
T_PLOP = 28.78

X = 'series/zamelo/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'seagull_cry.mp3', 0.00, 0.55),
    (L + 'whoosh_3.mp3', 1.50, 0.45),
    (L + 'whoosh_1.mp3', 3.10, 0.30),
    (L + 'sms_message.mp3', 4.85, 0.7),
    (L + 'vinyl_scratch.mp3', 5.20, 0.35),
    (L + 'cloth_rustle.mp3', 8.00, 0.45),
    (X + 'seagull_cry.mp3', 8.40, 0.35),
    (L + 'boing_cartoon.mp3', 13.50, 0.30),
    (X + 'shovel_snow.mp3', 14.45, 0.80),
    (X + 'shovel_snow.mp3', 15.60, 0.70),
    (X + 'shovel_snow.mp3', 17.00, 0.65),
    (L + 'whoosh_1.mp3', 18.05, 0.45),
    (X + 'shovel_snow.mp3', 18.30, 0.70),
    (X + 'snow_dive.mp3', 19.70, 0.70),
    (L + 'teeth_chatter.mp3', 20.10, 0.45),
    (L + 'whoosh_1.mp3', 22.62, 0.55),
    (L + 'gong_strong.mp3', 22.69, 0.35),
    (L + 'door_apartment_open.mp3', 22.88, 0.45),
    (L + 'vinyl_scratch.mp3', 26.45, 0.30),
    (X + 'snow_plop.mp3', 28.78, 1.4),
    (L + 'boing_cartoon.mp3', 28.88, 0.30),
    (L + 'snow_steps.mp3', 29.78, 0.50),
    (L + 'sms_message.mp3', 32.03, 0.55),
    (L + 'phone_key_click.mp3', 34.13, 0.6),
    (X + 'seagull_cry.mp3', 35.10, 0.35),
    (L + 'rimshot_joke.mp3', 36.60, 0.45),
]

BEDS = [
    (X + 'frost_wind_loop.mp3', 8.0, 0.0, 15.05, 0.50, True),
    (X + 'frost_wind_loop.mp3', 8.0, 26.48, DUR, 0.45, True),
    ('library/cc0/music/komiku_mandolin.mp3', 30.0, 0.0, DUR, 0.85, True, 'equalizer=f=1800:t=q:w=1.3:g=-9'),
]

VFX = {}
VGAIN = {'zhora': 2.0, 'chayka': 2.2, 'ira': 2.0, 'vitek': 2.0, 'nina': 2.1}
