"""S01E02 «СМЕНКУ ЗАБЫЛ!» — timing for video (ep02.py) and audio (mix.py). Voice: voice/ep02_t (c1 and v1 trimmed at a pause)."""
DUR = 43.6
FPS = 30
SLUG = 'zamelo'
LUFS = -14.0

VOICE = [
    ('c0', 'ep02_t', 'c0', 0.00, 0.00, 4.88, 'chayka', 'Дальний Восток. В школу тут ездят прямо из ОКНА. С девятого этажа. На ледянке.'),
    ('i1', 'ep02_t', 'i1', 4.95, 0.00, 4.23, 'ira', 'Тёма, стой! Ты ж СМЕНКУ забыл! Без сменки тебя даже на порог не пустят!'),
    ('z1', 'ep02_t', 'z1', 9.25, 0.00, 3.76, 'zhora', 'Спокойно, мать. Мы, дальневосточники, — привычные. Щас ДОГОНЮ!'),
    ('c1', 'ep02_t', 'c1', 13.08, 0.00, 2.85, 'chayka', 'Сорок два года. В ТРУСАХ. На тазике.'),
    ('z2', 'ep02_t', 'z2', 16.00, 0.00, 2.38, 'zhora', 'Тёма-а-а! Сменку ВЕЗУ!'),
    ('v1', 'ep02_t', 'v1', 19.05, 0.00, 1.72, 'valya', 'Без сменки НЕ ПУЩУ.'),
    ('z3', 'ep02_t', 'z3', 20.85, 0.00, 2.87, 'zhora', 'Стоять! Вот она, СМЕНКА! Держи, сын!'),
    ('t1', 'ep02_t', 't1', 23.80, 0.00, 3.53, 'tyoma', 'Пап. А почему она мороженая? Это ж ПЕЛЬМЕНИ.'),
    ('v2', 'ep02_t', 'v2', 27.40, 0.00, 4.23, 'valya', 'Пельмени — это не сменка, мужчина. Хотя. А ДОМАШНИЕ?'),
    ('z4', 'ep02_t', 'z4', 31.70, 0.00, 3.47, 'zhora', 'Ну а какие ещё? Жена лепила. Целый КИЛОГРАММ!'),
    ('t2', 'ep02_t', 't2', 36.10, 0.00, 2.64, 'tyoma', 'Пап, а что, так МОЖНО было?!'),
    ('c2', 'ep02_t', 'c2', 38.85, 0.00, 3.74, 'chayka', 'Запоминай. Сменка не нужна. Нужен КИЛОГРАММ пельменей.'),
]

#       gull  slope  ira    grab   taz    ride_a ride_b hall   burst  open   valya  proud  pass   wow    button
CUTS = [0.0, 1.60, 4.95, 9.25, 13.05, 15.93, 17.60, 19.00, 20.85, 23.80, 27.40, 31.70, 35.20, 36.10, 38.85, DUR]
NAMES = ['gull', 'slope', 'ira', 'grab', 'taz', 'ride_a', 'ride_b', 'hall', 'burst', 'open', 'valya', 'proud', 'pass', 'wow', 'button']
TWIST = 24.60                    # the bag opens: frozen pelmeni. 24.6 / 43.6 = 56 %

X = 'series/zamelo/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'seagull_cry.mp3', 0.00, 0.55),
    (L + 'whoosh_3.mp3', 1.55, 0.45),
    (X + 'snow_dive.mp3', 2.60, 0.40),
    (L + 'sliding_door_open.mp3', 4.95, 0.35),
    (L + 'zipper.mp3', 10.20, 0.35),
    (L + 'canvas_bag_drop.mp3', 11.30, 0.45),
    (L + 'boing_cartoon.mp3', 15.70, 0.30),
    (L + 'whoosh_1.mp3', 15.95, 0.55),
    (X + 'snow_dive.mp3', 16.20, 0.45),
    (L + 'car_arrive_stop.mp3', 17.75, 0.40),
    (L + 'whoosh_1.mp3', 18.55, 0.45),
    (X + 'snow_dive.mp3', 20.80, 0.80),
    (L + 'vinyl_scratch.mp3', 24.55, 0.40),
    (L + 'gong_strong.mp3', 24.60, 0.35),
    (L + 'freezer_close.mp3', 24.70, 0.40),
    (L + 'chair_creak.mp3', 27.40, 0.35),
    (L + 'phone_key_click.mp3', 35.25, 0.7),
    (L + 'elevator_ride.mp3', 35.40, 0.20, 0.0, 0.6),
    (L + 'slipper_steps.mp3', 35.55, 0.45),
    (X + 'seagull_cry.mp3', 38.60, 0.35),
    (L + 'rimshot_joke.mp3', 42.40, 0.45),
]

BEDS = [
    (X + 'frost_wind_loop.mp3', 8.0, 0.0, 19.0, 0.45, True),
    ('library/cc0/music/komiku_weekly_fair.mp3', 30.0, 0.0, DUR, 0.85, True, 'equalizer=f=1800:t=q:w=1.3:g=-9'),
]

VFX = {}
VGAIN = {'zhora': 2.0, 'chayka': 2.2, 'ira': 2.0, 'tyoma': 2.0, 'valya': 2.1}
