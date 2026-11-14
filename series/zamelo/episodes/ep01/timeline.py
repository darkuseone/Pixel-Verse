"""S01E01 «ОСТАВЛЕН У ДВЕРИ?!» — timing for video (ep01.py) and audio (mix.py). Voice: tightened takes voice/ep01_t (tempo 1.06–1.08).
Sound: own sounds of the series (series/zamelo/sfx) + CC0 library (whoosh, sms, boing, rimshot, scratch, snow steps) + a cheerful CC0 bed."""
DUR = 36.5
FPS = 30
SLUG = 'zamelo'
LUFS = -14.0

VOICE = [
    ('z1', 'ep01_t', 'z1', 0.00, 0.00, 3.03, 'zhora', 'Как это — «оставлен у двери»?! Моя дверь — под снегом!'),
    ('c1', 'ep01_t', 'c1', 3.05, 0.00, 4.56, 'chayka', 'Дальний Восток. Снега — по девятый этаж. Девятый теперь — первый.'),
    ('z2', 'ep01_t', 'z2', 7.66, 0.00, 3.76, 'zhora', 'Кыш, баклан! Мы, дальневосточники, — привычные. ОТКОПАЮ!'),
    ('c2', 'ep01_t', 'c2', 11.45, 0.00, 2.67, 'chayka', 'Я — чайка. Баклан — это ТЫ.'),
    ('n1', 'ep01_t', 'n1', 14.30, 0.00, 3.54, 'nina', 'Жорик, так курьер же по КРЫШАМ ходит!'),
    ('z4', 'ep01_t', 'z4', 17.40, 0.00, 1.78, 'zhora', 'Некогда, баба Нина!'),
    ('z5', 'ep01_t', 'z5', 19.18, 0.00, 2.62, 'zhora', 'Двадцать семь МЕТРОВ! И где посылка?!'),
    ('i2', 'ep01_t', 'i2', 22.00, 0.00, 3.55, 'ira', 'Жора! Она у НАШЕЙ двери! Курьер через КРЫШУ ходит!'),
    ('z6', 'ep01_t', 'z6', 25.70, 0.00, 2.06, 'zhora', 'А чего он в ОКНО не постучал?!'),
    ('v1', 'ep01_t', 'v1', 28.95, 0.00, 3.00, 'vitek', 'Братан, окно — это не АДРЕС. Оцени доставку!'),
    ('z7', 'ep01_t', 'z7', 32.10, 0.00, 1.63, 'zhora', 'Одна ЗВЕЗДА.'),
    ('c3', 'ep01_t', 'c3', 34.10, 0.00, 1.25, 'chayka', 'Себе ПОСТАВЬ.'),
]

#       hook  vostok etazh  pervyi kysh   baklan  dive   shaft  bottom twist  up     vitek  star   button
CUTS = [0.0, 3.05, 4.40, 6.10, 7.66, 11.45, 14.12, 15.20, 19.18, 21.85, 25.65, 28.90, 32.00, 33.95, DUR]
NAMES = ['hook', 'vostok', 'etazh', 'pervyi', 'kysh', 'baklan', 'dive', 'shaft', 'bottom', 'twist', 'up', 'vitek', 'star', 'button']
TWIST = CUTS[9]                  # 21.85 / 36.5 = 60 %

X = 'series/zamelo/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (L + 'sms_message.mp3', 0.00, 0.7),
    (L + 'vinyl_scratch.mp3', 0.25, 0.35),
    (L + 'whoosh_3.mp3', 3.02, 0.45),
    (X + 'seagull_cry.mp3', 3.30, 0.55),
    (L + 'whoosh_1.mp3', 4.38, 0.35),
    (X + 'seagull_cry.mp3', 6.15, 0.30),
    (L + 'cloth_rustle.mp3', 7.70, 0.45),
    (L + 'boing_cartoon.mp3', 13.20, 0.30),
    (L + 'zipper.mp3', 14.15, 0.35),
    (X + 'snow_dive.mp3', 14.65, 0.95),
    (X + 'shovel_snow.mp3', 15.30, 0.75),
    (X + 'shovel_snow.mp3', 16.80, 0.70),
    (X + 'shovel_snow.mp3', 18.20, 0.70),
    (L + 'teeth_chatter.mp3', 19.30, 0.45),
    (L + 'whoosh_1.mp3', 21.80, 0.55),
    (L + 'gong_strong.mp3', 21.86, 0.35),
    (L + 'door_apartment_open.mp3', 22.05, 0.45),
    (L + 'vinyl_scratch.mp3', 25.62, 0.30),
    (X + 'snow_plop.mp3', 27.95, 1.4),
    (L + 'boing_cartoon.mp3', 28.05, 0.30),
    (L + 'snow_steps.mp3', 28.95, 0.50),
    (L + 'sms_message.mp3', 31.20, 0.55),
    (L + 'phone_key_click.mp3', 33.30, 0.6),
    (X + 'seagull_cry.mp3', 34.00, 0.35),
    (L + 'rimshot_joke.mp3', 35.35, 0.45),
]

BEDS = [
    (X + 'frost_wind_loop.mp3', 8.0, 0.0, 15.2, 0.50, True),
    (X + 'frost_wind_loop.mp3', 8.0, 25.65, DUR, 0.45, True),
    ('library/cc0/music/komiku_mandolin.mp3', 30.0, 0.0, DUR, 0.85, True, 'equalizer=f=1800:t=q:w=1.3:g=-9'),
]

VFX = {}
VGAIN = {'zhora': 2.0, 'chayka': 2.2, 'ira': 2.0, 'vitek': 2.0, 'nina': 2.1}
