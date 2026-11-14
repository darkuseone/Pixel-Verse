"""S01E06 «РАСТАЯЛО!» — timing for video (ep06.py) and audio (mix.py). Voice: voice/ep06_t."""
DUR = 42.0
FPS = 30
SLUG = 'zamelo'
LUFS = -14.0

VOICE = [
    ('c0', 'ep06_t', 'c0', 0.00, 0.00, 5.04, 'chayka', 'Дальний Восток. Весна. Снег, который копили полгода, растаял за одну ночь.'),
    ('z1', 'ep06_t', 'z1', 5.09, 0.00, 4.13, 'zhora', 'Ира! Растаяло! Всё, теперь на работу — как человек, через дверь!'),
    ('i1', 'ep06_t', 'i1', 9.27, 0.00, 2.95, 'ira', 'Жора, лифт не работает. Девятый этаж.'),
    ('z2', 'ep06_t', 'z2', 12.27, 0.00, 4.00, 'zhora', 'Да хоть двадцатый! Я полгода в окно лазил — уж по лестнице-то сбегаю!'),
    ('z3', 'ep06_t', 'z3', 16.32, 0.00, 4.83, 'zhora', 'Девятый, пятый, первый! Ну, здравствуй, свобода!'),
    ('z4', 'ep06_t', 'z4', 21.95, 0.00, 2.14, 'zhora', 'Это что такое?'),
    ('v1', 'ep06_t', 'v1', 24.14, 0.00, 3.71, 'vitek', 'Такси «Лодка», тариф «Эконом»! Город маленький!'),
    ('z5', 'ep06_t', 'z5', 27.90, 0.00, 1.46, 'zhora', 'Ну и сколько до работы?'),
    ('v2', 'ep06_t', 'v2', 29.41, 0.00, 2.32, 'vitek', 'Три тысячи. Но гребёшь — сам.'),
    ('i2', 'ep06_t', 'i2', 31.78, 0.00, 4.36, 'ira', 'Жора! УК пишет: лужу уберут зимой. Замёрзнет — сама.'),
    ('z6', 'ep06_t', 'z6', 36.19, 0.00, 3.87, 'zhora', 'Ничего! Мы, дальневосточники, — непотопляемые!'),
    ('c1', 'ep06_t', 'c1', 40.15, 0.00, 0.97, 'chayka', 'Плаваем.'),
]

#       gull  melt  joy   ira   run    f9     f5     f1     door   twist  boat   much   row    ira2   defy   gull2
CUTS = [0.0, 2.30, 5.07, 9.25, 12.25, 16.30, 17.75, 18.65, 19.35, 21.35, 24.10, 27.88, 29.39, 31.76, 36.17, 40.10, DUR]
NAMES = ['gull', 'melt', 'joy', 'ira', 'run', 'f9', 'f5', 'f1', 'door', 'twist', 'boat', 'much', 'row', 'ira2', 'defy', 'gull2']
TWIST = 21.35                    # he steps out of the door — the whole yard is a lake. 21.35 / 42.0 = 51 %

X = 'series/zamelo/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'seagull_cry.mp3', 0.00, 0.55),
    (L + 'whoosh_3.mp3', 2.25, 0.40),
    (X + 'snow_plop.mp3', 3.20, 0.35),
    (X + 'snow_plop.mp3', 4.10, 0.30),
    (L + 'door_apartment_open.mp3', 12.30, 0.6),
    (L + 'steps_concrete.mp3', 12.90, 0.7),
    (L + 'whoosh_1.mp3', 16.28, 0.4),
    (L + 'steps_concrete.mp3', 16.35, 0.8),
    (L + 'whoosh_1.mp3', 17.15, 0.4),
    (L + 'whoosh_1.mp3', 17.98, 0.4),
    (L + 'door_apartment_open.mp3', 18.90, 0.6),
    (X + 'splash_big.mp3', 21.35, 1.0),
    (L + 'gong_strong.mp3', 21.35, 0.25),
    (X + 'rowing.mp3', 24.10, 3.0),
    (X + 'rowing.mp3', 28.10, 2.4),
    (L + 'sms_message.mp3', 31.80, 0.55),
    (L + 'teeth_chatter.mp3', 36.40, 0.45),
    (X + 'seagull_cry.mp3', 40.05, 0.30),
    (L + 'rimshot_joke.mp3', 41.25, 0.45),
]

BEDS = [
    (X + 'melt_drip_loop.mp3', 8.0, 0.0, 12.25, 0.9, True),
    (X + 'melt_drip_loop.mp3', 8.0, 18.85, DUR, 1.0, True),
    ('library/cc0/music/komiku_weekly_fair.mp3', 30.0, 0.0, DUR, 0.85, True, 'equalizer=f=1800:t=q:w=1.3:g=-9'),
]

VFX = {}
VGAIN = {'zhora': 2.0, 'chayka': 2.2, 'vitek': 2.0, 'ira': 2.0}
