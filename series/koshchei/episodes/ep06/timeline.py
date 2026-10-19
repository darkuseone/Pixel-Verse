"""S01E06 «СЛАДОСТЬ ИЛИ ГАДОСТЬ?!» (finale) — timing for video (ep06.py) and audio (mix.py). Voice: voice/ep06_t, common_t.
Series-own sounds only."""
DUR = 31.6
FPS = 30
SLUG = 'koshchei'
MASTER = 0.66

VOICE = [
    ('s1', 'ep06_t', 's1', 0.00, 0.00, 2.06, 'student', 'Сладость или ГАДОСТЬ?!'),
    ('s2', 'ep06_t', 's2', 2.15, 0.00, 2.93, 'student', 'Дед, костюм — ТОП! Где брал?'),
    ('k1', 'ep06_t', 'k1', 5.15, 0.00, 1.59, 'koshchei', 'Это — ЛИЦО.'),
    ('k2', 'ep06_t', 'k2', 6.85, 0.00, 3.42, 'koshchei', 'Отдаю самое дорогое — СМЕРТЬ свою!'),
    ('s3', 'ep06_t', 's3', 10.35, 0.00, 2.85, 'student', 'Дед, нам бы — ШОКОЛАДКУ.'),
    ('y1', 'ep06_t', 'y1', 13.95, 0.00, 2.17, 'yaga', 'Хэллоуин — не НАШ праздник!'),
    ('k3', 'ep06_t', 'k3', 16.50, 0.00, 1.70, 'koshchei', 'ДОЖДАЛСЯ!'),
    ('s5', 'ep06_t', 's5', 18.95, 0.00, 2.30, 'student', 'Дед. Это — ГАДОСТЬ.'),
    ('k5', 'ep06_t', 'k5', 21.35, 0.00, 1.72, 'koshchei', 'Это — ПЕНСИЯ.'),
    ('s4', 'ep06_t', 's4', 23.20, 0.00, 3.03, 'student', 'Бабуль, классный костюм Бабы ЯГИ!'),
    ('y2', 'ep06_t', 'y2', 26.30, 0.00, 1.62, 'yaga', 'Я — в ХАЛАТЕ.'),
    ('z1', 'common_t', 'zhut', 28.05, 0.00, 1.10, 'kuzmich', 'ЖУТЬ.'),
    ('k6', 'ep06_t', 'k6', 29.30, 0.00, 1.93, 'koshchei', 'ТРИНАДЦАТЬ РУБЛЕЙ?!'),
]

#       hook  costume face   death  choco  crown  yaga   SMS    coins  bench  zhut   season
CUTS = [0.0, 2.10, 5.10, 6.75, 10.30, 13.20, 13.90, 16.30, 18.90, 23.10, 28.00, 29.20, DUR]
NAMES = ['hook', 'costume', 'face', 'death', 'choco', 'crown', 'yaga', 'sms', 'coins', 'bench', 'zhut', 'season']
TWIST = CUTS[7]

X = 'series/koshchei/sfx/'
SFX = [
    (X + 'doorbell_old.mp3', 0.00, 0.85),
    (X + 'youth_laugh.mp3', 0.20, 0.45),
    (X + 'door_open_creak.mp3', 0.30, 0.45),
    (X + 'youth_laugh.mp3', 4.20, 0.40),
    (X + 'cabinet_crystal.mp3', 6.80, 0.60),
    (X + 'magic_crackle.mp3', 8.20, 0.55),
    (X + 'wrapper_rustle.mp3', 13.25, 0.80),
    (X + 'sms_beep.mp3', 16.25, 0.95),
    (X + 'twist_choir_hit.mp3', 16.30, 0.80),
    (X + 'coins_jingle.mp3', 18.30, 0.85),
    (X + 'wrapper_rustle.mp3', 28.10, 0.70),
    (X + 'stamp_thud.mp3', 29.20, 0.85),
    (X + 'twist_choir_hit.mp3', 30.30, 0.55),
]

BEDS = [
    ('series/koshchei/sfx/stairwell_amb_loop.mp3', 8.0, 0.0, 29.20, 0.32, True),
    ('series/koshchei/sfx/office_amb_loop.mp3', 8.0, 29.20, DUR, 0.40, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 2.10, 16.20, 0.20, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 16.80, DUR, 0.22, True),
]

VFX = {'kuzmich': 'aecho=0.6:0.4:40:0.15'}
VGAIN = {'koshchei': 1.5, 'student': 1.5, 'yaga': 1.5, 'kuzmich': 1.8}
