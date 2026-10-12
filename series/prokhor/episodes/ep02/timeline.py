"""S01E02 «ПВЗ ЗА 40 КМ?!» — timing for video (ep02.py) and audio (mix.py). Voice: tightened takes voice/ep02_t. Series-own sounds only."""
DUR = 30.0
FPS = 30
SLUG = 'prokhor'
MASTER = 0.66

VOICE = [
    ('p1', 'ep02_t', 'p1', 0.00, 0.00, 2.69, 'prokhor', 'Сорок километров до пункта ВЫДАЧИ?!'),
    ('p2', 'ep02_t', 'p2', 2.80, 0.00, 4.47, 'prokhor', 'Лайфхак: открываю пункт выдачи у себя. Посылки сами ПРИДУТ!'),
    ('p3', 'ep02_t', 'p3', 7.40, 0.00, 2.78, 'prokhor', 'Всё. Теперь я — пункт ВЫДАЧИ.'),
    ('f1', 'ep02_t', 'f1', 10.35, 0.00, 3.46, 'fox', 'Лиса-Экспресс! Распишитесь: тут, тут и ТУТ.'),
    ('p4', 'ep02_t', 'p4', 13.90, 0.00, 3.91, 'prokhor', 'Пять минут — и носки дома! Городские, УЧИТЕСЬ!'),
    ('b1', 'ep02_t', 'b1', 18.05, 0.00, 2.74, 'bear', 'Мой заказ где? Неделю ЖДУ.'),
    ('f2', 'ep02_t', 'f2', 20.95, 0.00, 3.17, 'fox', 'Это всё — вам. Вы же пункт ВЫДАЧИ!'),
    ('p5', 'ep02_t', 'p5', 24.25, 0.00, 2.04, 'prokhor', 'Я ж только НОСКИ заказал!'),
    ('b2', 'ep02_t', 'b2', 26.75, 0.00, 1.48, 'bear', 'Одна ЗВЕЗДА.'),
]

#       selfie hammer proud  fox    box    QUEUE  dump   buried rate
CUTS = [0.0, 2.75, 7.35, 10.25, 13.85, 17.85, 20.90, 24.20, 26.40, DUR]
NAMES = ['selfie', 'hammer', 'proud', 'fox', 'box', 'queue', 'dump', 'buried', 'rate']
TWIST = CUTS[5]

X = 'series/prokhor/sfx/'
SFX = [
    (X + 'phone_notify.mp3', 0.10, 0.80),
    (X + 'breath_frost.mp3', 1.50, 0.40),
    (X + 'crow_caw.mp3', 2.20, 0.22),
    (X + 'hammer_nail_log.mp3', 2.95, 0.85),
    (X + 'hammer_nail_log.mp3', 5.40, 0.55, 0.6, 2.0),
    (X + 'phone_rec_start.mp3', 7.36, 0.45),
    (X + 'ski_sled_arrive.mp3', 10.25, 0.85),
    (X + 'pen_signature.mp3', 12.10, 0.75),
    (X + 'box_thump.mp3', 13.60, 0.70),
    (X + 'snow_steps_valenki.mp3', 14.20, 0.35),
    (X + 'whip_pan.mp3', 17.82, 0.90),
    (X + 'twist_hit.mp3', 17.88, 0.70),
    (X + 'animal_queue_murmur.mp3', 18.00, 0.75),
    (X + 'animal_queue_murmur.mp3', 20.20, 0.45),
    (X + 'ski_sled_arrive.mp3', 21.60, 0.40, 1.5, 2.5),
    (X + 'box_avalanche.mp3', 21.95, 1.00),
    (X + 'box_thump.mp3', 23.40, 0.70),
    (X + 'snowdrift_landing.mp3', 22.40, 0.45),
    (X + 'rating_tap.mp3', 26.42, 0.90),
    (X + 'phone_notify.mp3', 26.50, 0.55),
]

BEDS = [
    ('series/prokhor/sfx/taiga_wind_loop.mp3', 8.0, 0.0, DUR, 0.40, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 2.75, 17.80, 0.20, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 20.90, DUR, 0.18, True),
]

VFX = {'bear': 'aecho=0.6:0.4:35:0.12'}
VGAIN = {'prokhor': 1.55, 'bear': 1.75, 'fox': 1.6}
