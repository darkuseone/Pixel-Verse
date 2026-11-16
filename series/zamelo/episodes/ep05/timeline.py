"""S01E05 «1400 ЗА СНЕГ?!» — timing for video (ep05.py) and audio (mix.py). Voice: voice/ep05_t (g1 not used: twist ≤ 60 %)."""
DUR = 43.5
FPS = 30
SLUG = 'zamelo'
LUFS = -14.0

VOICE = [
    ('c0', 'ep05_t', 'c0', 0.00, 0.00, 4.94, 'chayka', 'Дальний Восток. Снег тут убирает управляющая компания. А платит за это — Жора.'),
    ('z1', 'ep05_t', 'z1', 4.98, 0.00, 3.34, 'zhora', 'Тысяча четыреста за уборку снега?! Да я ж сам всё чищу!'),
    ('d1', 'ep05_t', 'd1', 8.36, 0.00, 4.55, 'disp', 'Мужчина, ну это вам не материк. У нас снег убирается весной. Сам.'),
    ('z2', 'ep05_t', 'z2', 12.95, 0.00, 3.84, 'zhora', 'Сам?! Я тут старший по окну! Требую грейдер! Сегодня же!'),
    ('d2', 'ep05_t', 'd2', 16.83, 0.00, 3.53, 'disp', 'Ладно, ладно. Заявку приняли. Ждите.'),
    ('z3', 'ep05_t', 'z3', 20.40, 0.00, 3.74, 'zhora', 'Вот! Мы, дальневосточники, своего добиваемся!'),
    ('v1', 'ep05_t', 'v1', 25.60, 0.00, 2.56, 'vitek', 'Грейдер вызывали? Город маленький!'),
    ('v2', 'ep05_t', 'v2', 28.20, 0.00, 2.93, 'vitek', 'Дорогу почистил! А снег — к вам. Распишитесь!'),
    ('z4', 'ep05_t', 'z4', 31.17, 0.00, 2.95, 'zhora', 'Ещё шестьсот?! За то, что меня закопали?!'),
    ('i1', 'ep05_t', 'i1', 34.16, 0.00, 3.92, 'ira', 'Поздравляю, старший по окну. Окна-то у нас больше нет.'),
    ('z5', 'ep05_t', 'z5', 38.12, 0.00, 2.53, 'zhora', 'Мы, дальневосточники, — привычные.'),
    ('c1', 'ep05_t', 'c1', 40.69, 0.00, 2.17, 'chayka', 'Привыкай. Ты теперь — подвал.'),
]

#       gull  uk    pays  rcpt  disp  shout disp2 proud grader slam  cab   road  dark  candle used  beak
CUTS = [0.0, 1.60, 3.40, 4.96, 8.34, 12.93, 16.81, 20.38, 23.70, 24.50, 25.58, 28.18, 31.15, 34.14, 38.10, 40.67, DUR]
NAMES = ['gull', 'uk', 'pays', 'rcpt', 'disp', 'shout', 'disp2', 'proud', 'grader', 'slam', 'cab', 'road', 'dark', 'candle', 'used', 'beak']
TWIST = 24.85                    # the snow wave from the grader buries the window. 24.85 / 43.5 = 57 %

X = 'series/zamelo/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'seagull_cry.mp3', 0.00, 0.55),
    (L + 'whoosh_3.mp3', 1.55, 0.40),
    (L + 'sms_message.mp3', 4.98, 0.6),
    (L + 'vinyl_scratch.mp3', 5.25, 0.30),
    (L + 'phone_dial_tone.mp3', 8.05, 0.30),
    (L + 'phone_key_click.mp3', 16.55, 0.6),
    (L + 'sms_message.mp3', 20.10, 0.55),
    (X + 'grader_engine.mp3', 22.40, 0.45),
    (X + 'grader_engine.mp3', 23.70, 0.85),
    (L + 'whoosh_1.mp3', 24.45, 0.5),
    (X + 'snow_avalanche.mp3', 24.85, 1.0),
    (L + 'gong_strong.mp3', 24.85, 0.28),
    (X + 'snow_plop.mp3', 25.30, 0.6),
    (X + 'grader_engine.mp3', 28.18, 0.40),
    (X + 'snow_dive.mp3', 29.20, 0.5),
    (L + 'sms_message.mp3', 31.20, 0.55),
    (L + 'cloth_rustle.mp3', 34.30, 0.4),
    (L + 'keys_on_table.mp3', 37.60, 0.25),
    (X + 'snow_plop.mp3', 40.62, 0.7),
    (X + 'seagull_cry.mp3', 40.75, 0.25),
    (L + 'rimshot_joke.mp3', 42.86, 0.45),
]

BEDS = [
    (X + 'frost_wind_loop.mp3', 8.0, 0.0, 24.9, 0.40, True),
    (X + 'frost_wind_loop.mp3', 8.0, 25.58, 31.15, 0.35, True),
    ('library/cc0/music/komiku_shoe_shop.mp3', 30.0, 0.0, DUR, 0.85, True, 'equalizer=f=1800:t=q:w=1.3:g=-9'),
]

VFX = {}
VGAIN = {'zhora': 2.0, 'chayka': 2.2, 'vitek': 2.0, 'ira': 2.0, 'disp': 2.0}
