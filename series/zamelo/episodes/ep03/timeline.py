"""S01E03 «ГДЕ МОЯ МАШИНА?!» — timing for video (ep03.py) and audio (mix.py). Voice: voice/ep03_t (c1 not used)."""
DUR = 43.8
FPS = 30
SLUG = 'zamelo'
LUFS = -14.0

VOICE = [
    ('c0', 'ep03_t', 'c0', 0.00, 0.00, 5.88, 'chayka', 'Дальний Восток. За ночь насыпало ещё МЕТР. И теперь все машины во дворе — одинаковые СУГРОБЫ.'),
    ('z1', 'ep03_t', 'z1', 5.95, 0.00, 4.45, 'zhora', 'Так. Спокойно. Я ж ФЛАЖОК ставил! Вон он, мой. С надписью «Жора».'),
    ('g1', 'ep03_t', 'g1', 10.50, 0.00, 5.21, 'gosha', 'Доброе утро, Жорик! Да-да, твой, твой. Копай, РОДНОЙ, не стесняйся.'),
    ('z2', 'ep03_t', 'z2', 16.10, 0.00, 2.79, 'zhora', 'Гош, а ты-то чего не КОПАЕШЬ? Тебе ж тоже ехать.'),
    ('g2', 'ep03_t', 'g2', 18.95, 0.00, 2.21, 'gosha', 'А зачем? Ты ж КОПАЕШЬ.'),
    ('z3', 'ep03_t', 'z3', 21.25, 0.00, 3.48, 'zhora', 'Два ЧАСА! Но откопал же! Ласточка моя!'),
    ('z4', 'ep03_t', 'z4', 25.50, 0.00, 1.48, 'zhora', 'Не ПОНЯЛ.'),
    ('g3', 'ep03_t', 'g3', 27.05, 0.00, 3.78, 'gosha', 'Спасибо, Жорик! Это ж МОЯ. Я флажки ночью ПОМЕНЯЛ.'),
    ('z5', 'ep03_t', 'z5', 30.90, 0.00, 1.25, 'zhora', 'А моя-то ГДЕ?!'),
    ('g4', 'ep03_t', 'g4', 32.20, 0.00, 3.34, 'gosha', 'Да под МОИМ флажком! Не переживай, с меня ИКРА!'),
    ('z6', 'ep03_t', 'z6', 36.40, 0.00, 3.55, 'zhora', 'Ну ничего. Завтра я ему флажки ПОМЕНЯЮ.'),
    ('c2', 'ep03_t', 'c2', 40.05, 0.00, 2.76, 'chayka', 'Завтра — ещё МЕТР. Зимуем.'),
]

#       gull  field  walk   gosha  dig    gosha2 car    key    twist  g_car  where  drive  jar    revenge button
CUTS = [0.0, 1.60, 5.95, 10.50, 15.71, 18.95, 21.20, 24.75, 25.35, 27.05, 30.85, 32.15, 35.55, 36.35, 40.00, DUR]
NAMES = ['gull', 'field', 'walk', 'gosha', 'dig', 'gosha2', 'car', 'key', 'twist', 'g_car', 'where', 'drive', 'jar', 'revenge', 'button']
TWIST = CUTS[8]                  # Гоша's key fob — the dug-out car blinks for HIM. 25.35 / 43.8 = 58 %

X = 'series/zamelo/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'seagull_cry.mp3', 0.00, 0.55),
    (L + 'whoosh_3.mp3', 1.55, 0.45),
    (L + 'snow_steps.mp3', 6.00, 0.55),
    (L + 'bottle_clink.mp3', 10.60, 0.45),
    (X + 'shovel_snow.mp3', 15.75, 0.75),
    (X + 'shovel_snow.mp3', 17.10, 0.70),
    (X + 'shovel_snow.mp3', 19.80, 0.55),
    (L + 'vinyl_scratch.mp3', 21.20, 0.30),
    (L + 'phone_key_click.mp3', 24.85, 0.8),
    (L + 'whoosh_1.mp3', 25.30, 0.45),
    (L + 'doorbell_2.mp3', 25.36, 0.55),
    (L + 'car_arrive_stop.mp3', 27.10, 0.35),
    (L + 'gong_strong.mp3', 30.85, 0.25),
    (L + 'bus_horn.mp3', 33.80, 0.30),
    (L + 'whoosh_1.mp3', 35.00, 0.45),
    (L + 'boing_cartoon.mp3', 35.75, 0.40),
    (X + 'seagull_cry.mp3', 39.80, 0.35),
    (L + 'rimshot_joke.mp3', 42.85, 0.45),
]

BEDS = [
    (X + 'frost_wind_loop.mp3', 8.0, 0.0, DUR, 0.40, True),
    ('library/cc0/music/komiku_fetch_contest.mp3', 30.0, 0.0, DUR, 0.85, True, 'equalizer=f=1800:t=q:w=1.3:g=-9'),
]

VFX = {}
VGAIN = {'zhora': 2.0, 'chayka': 2.2, 'gosha': 2.1}
