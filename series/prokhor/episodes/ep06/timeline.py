"""S01E06 «МОРЕ ЗА 200 ТЫСЯЧ?!» — timing for video (ep06.py) and audio (mix.py). Voice: tightened takes voice/ep06_t. Series-own sounds only.
The last shot is the season loop: the first frames of E01 (Прохор screams at the heating bill in his icy cabin) with E01's own line."""
DUR = 31.4
FPS = 30
SLUG = 'prokhor'
MASTER = 0.74

VOICE = [
    ('p1', 'ep06_t', 'p1', 0.05, 0.00, 2.07, 'prokhor', 'Двести тыщ за МОРЕ?!'),
    ('p2', 'ep06_t', 'p2', 2.25, 0.00, 3.59, 'prokhor', 'Лайфхак последний: море — своими РУКАМИ!'),
    ('p3', 'ep06_t', 'p3', 6.05, 0.00, 4.97, 'prokhor', 'Самовар — прорубь. Ёлка — пальма. Лыжи — ШЕЗЛОНГ!'),
    ('p4', 'ep06_t', 'p4', 11.50, 0.00, 2.95, 'prokhor', 'Всё включено. Ноль РУБЛЕЙ.'),
    ('p5', 'ep06_t', 'p5', 19.50, 0.00, 1.53, 'prokhor', 'Это МОЁ море!'),
    ('b1', 'ep06_t', 'b1', 21.40, 0.00, 3.08, 'bear', 'Было ваше. Теперь — КУРОРТ.'),
    ('b2', 'ep06_t', 'b2', 24.80, 0.00, 2.75, 'bear', 'Девять тысяч. За ТЕПЛО.'),
]
LOOP_T = 27.80                 # E01's first frames from here (its line is mixed as a sound: the captions are baked into those frames)

#       selfie build  lounge BEAR   mine   resort bill   loop
CUTS = [0.0, 5.90, 11.20, 16.20, 19.40, 21.30, 24.60, LOOP_T, DUR]
NAMES = ['selfie', 'build', 'lounge', 'resort', 'mine', 'bear', 'bill', 'loop']
TWIST = CUTS[3]

X = 'series/prokhor/sfx/'
SFX = [
    (X + 'phone_notify.mp3', 0.10, 0.80),
    (X + 'breath_frost.mp3', 2.10, 0.35),
    (X + 'snow_steps_valenki.mp3', 4.20, 0.50),
    (X + 'phone_rec_start.mp3', 5.91, 0.40),
    (X + 'samovar_bubble.mp3', 6.20, 1.00),
    (X + 'ski_chair_clack.mp3', 9.70, 1.00),
    (X + 'phone_sea_waves.mp3', 11.20, 0.60),
    (X + 'cozy_creak.mp3', 14.80, 0.50),
    (X + 'snow_steps_valenki.mp3', 15.20, 0.70),
    (X + 'twist_hit.mp3', 16.20, 0.70),
    (X + 'sign_stake_thud.mp3', 16.35, 1.00),
    (X + 'suitcases_snow.mp3', 16.50, 0.90),
    (X + 'snowdrift_landing.mp3', 16.30, 0.60),
    (X + 'big_splash_ice.mp3', 23.60, 0.80),
    (X + 'bill_rustle.mp3', 25.00, 0.80),
    ('series/prokhor/voice/ep01b_t/p1.mp3', LOOP_T + 0.05, 1.55),
    (X + 'freeze_crackle.mp3', LOOP_T + 0.10, 0.50),
]

BEDS = [
    ('series/prokhor/sfx/taiga_wind_loop.mp3', 8.0, 0.0, DUR, 0.35, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 2.0, 16.15, 0.20, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 19.4, LOOP_T, 0.17, True),
]

VFX = {'bear': 'aecho=0.6:0.4:35:0.12'}
VGAIN = {'prokhor': 1.55, 'bear': 1.75}
