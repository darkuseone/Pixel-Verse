"""S01E04 «ТАКСИ — 3000?!» — timing for video (ep04.py) and audio (mix.py). Voice: voice/ep04_t (v5 not used)."""
DUR = 43.9
FPS = 30
SLUG = 'zamelo'
LUFS = -14.0

VOICE = [
    ('c0', 'ep04_t', 'c0', 0.00, 0.00, 5.86, 'chayka', 'Дальний Восток. Автобус тут ходит — в АПРЕЛЕ. Поэтому все ездят на такси. А такси — на СОБАКАХ.'),
    ('z1', 'ep04_t', 'z1', 5.92, 0.00, 3.50, 'zhora', 'Сколько?! Три ТЫСЯЧИ до работы?! Тут же три километра!'),
    ('z2', 'ep04_t', 'z2', 9.48, 0.00, 2.91, 'zhora', 'Ну и ладно. Пешком — это на МАТЕРИКЕ. Заказываю!'),
    ('v1', 'ep04_t', 'v1', 12.50, 0.00, 2.85, 'vitek', 'Такси «Ямщик», тариф «ЭКОНОМ»! Садись, братан!'),
    ('z3', 'ep04_t', 'z3', 15.42, 0.00, 2.08, 'zhora', 'Витёк?! Ты ж вчера КУРЬЕРОМ был!'),
    ('v2', 'ep04_t', 'v2', 17.56, 0.00, 1.71, 'vitek', 'Ну. Город-то МАЛЕНЬКИЙ.'),
    ('z4', 'ep04_t', 'z4', 19.35, 0.00, 3.75, 'zhora', 'Вот это СЕРВИС! За три тыщи — с ветерком!'),
    ('v3', 'ep04_t', 'v3', 23.75, 0.00, 3.69, 'vitek', 'Всё, братан, приехали. У собак ОБЕД. А на «Экономе» дальше тянет ПАССАЖИР.'),
    ('z5', 'ep04_t', 'z5', 27.50, 0.00, 2.64, 'zhora', 'В смысле?! Я ж три тысячи ЗАПЛАТИЛ!'),
    ('v4', 'ep04_t', 'v4', 30.20, 0.00, 3.43, 'vitek', 'Так три тысячи — это СОБАКАМ. А ты — бесплатно.'),
    ('z6', 'ep04_t', 'z6', 33.70, 0.00, 2.27, 'zhora', 'Баклан, ну хоть ты ПОМОГИ!'),
    ('c1', 'ep04_t', 'c1', 36.03, 0.00, 2.81, 'chayka', 'Я — чайка. А ты теперь — ЕЗДОВОЙ.'),
    ('v6', 'ep04_t', 'v6', 39.00, 0.00, 2.81, 'vitek', 'Оценочку, братан. Собаки СМОТРЯТ.'),
    ('z7', 'ep04_t', 'z7', 42.00, 0.00, 0.85, 'zhora', 'Пять ЗВЁЗД.'),
]

#       gull  reveal phone  order  arrive small  ride   twist  what   sitin  pull   port
CUTS = [0.0, 1.60, 5.90, 9.45, 12.45, 17.53, 19.30, 23.60, 27.47, 30.17, 33.65, 38.90, DUR]
NAMES = ['gull', 'reveal', 'phone', 'order', 'arrive', 'small', 'ride', 'twist', 'what', 'sitin', 'pull', 'port']
TWIST = CUTS[7]                  # the dogs lie down: lunch. 23.6 / 43.9 = 54 %

X = 'series/zamelo/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'seagull_cry.mp3', 0.00, 0.55),
    (L + 'whoosh_3.mp3', 1.55, 0.45),
    (L + 'small_dog_bark.mp3', 2.40, 0.40),
    (L + 'sms_message.mp3', 5.92, 0.6),
    (L + 'vinyl_scratch.mp3', 6.30, 0.35),
    (L + 'phone_key_click.mp3', 12.00, 0.7),
    (L + 'small_dog_bark.mp3', 12.40, 0.55),
    (L + 'snow_steps.mp3', 12.50, 0.5),
    (L + 'whoosh_1.mp3', 19.30, 0.5),
    (L + 'small_dog_bark.mp3', 20.40, 0.40),
    (L + 'gong_strong.mp3', 23.60, 0.30),
    (L + 'boing_cartoon.mp3', 23.70, 0.35),
    (L + 'small_dog_bark.mp3', 30.60, 0.35),
    (L + 'snow_steps.mp3', 33.70, 0.7),
    (X + 'seagull_cry.mp3', 35.90, 0.35),
    (L + 'snow_steps.mp3', 36.50, 0.6),
    (L + 'sms_message.mp3', 39.40, 0.5),
    (L + 'rimshot_joke.mp3', 42.85, 0.45),
]

BEDS = [
    (X + 'frost_wind_loop.mp3', 8.0, 0.0, DUR, 0.40, True),
    ('library/cc0/music/town_cheerful.mp3', 30.0, 0.0, DUR, 0.85, True, 'equalizer=f=1800:t=q:w=1.3:g=-9'),
]

VFX = {}
VGAIN = {'zhora': 2.0, 'chayka': 2.2, 'vitek': 2.0}
