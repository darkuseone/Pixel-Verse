"""S01E03 «Из-под полы» — timing for video (ep03.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep03_t)."""
DUR = 31.3
FPS = 30
SLUG = 'mazutych'
MASTER = 0.82

VOICE = [
    ('v1', 'ep03_t', 'v1', 0.00, 0.00, 1.27, 'vadik', 'Бензин НУЖЕН?'),
    ('v2', 'ep03_t', 'v2', 3.55, 0.00, 2.76, 'vadik', 'Девяносто пятый. СВЕЖАК.'),
    ('m1', 'ep03_t', 'm1', 6.55, 0.00, 0.80, 'maz', 'ПОЧЁМ?'),
    ('v3', 'ep03_t', 'v3', 7.55, 0.00, 0.86, 'vadik', 'ПЯТЬСОТ.'),
    ('m2', 'ep03_t', 'm2', 8.65, 0.00, 1.05, 'maz', 'За ЛИТР?!'),
    ('v4', 'ep03_t', 'v4', 9.95, 0.00, 1.34, 'vadik', 'За ПОСМОТРЕТЬ.'),
    ('m3', 'ep03_t', 'm3', 11.90, 0.00, 3.21, 'maz', 'Это НЕ девяносто пятый.'),
    ('v5', 'ep03_t', 'v5', 15.30, 0.00, 0.92, 'vadik', 'А КАКОЙ?'),
    ('m4', 'ep03_t', 'm4', 16.50, 0.00, 2.33, 'maz', 'МОЙ. Партия четырнадцать.'),
    ('v6', 'ep03_t', 'v6', 19.05, 0.00, 2.37, 'vadik', 'Так я ж у твоего НАЧАЛЬНИКА беру.'),
    ('b1', 'ep03_t', 'b1', 21.80, 0.00, 2.89, 'boss', 'Мазутыч? Тебе — со СКИДКОЙ!'),
    ('b2', 'ep03_t', 'b2', 24.95, 0.00, 2.06, 'boss', 'Литр — по цене ДВУХ.'),
    ('v7', 'ep03_t', 'v7', 27.25, 0.00, 0.92, 'vadik', 'СКИДКА.'),
    ('w1', 'ep03_t', 'w1', 28.60, 0.00, 1.58, 'wheel', 'Это НЕ скидка, друга.'),
]

CUTS = [0.0, 2.40, 3.20, 6.45, 7.45, 8.55, 9.85, 11.70, 15.20, 16.40, 19.00, 21.60, 24.85, 27.15, 28.45, DUR]

S = 'library/sfx/'
SFX = [
    (S + 'glass_slide.mp3', 0.15, 0.6),
    (S + 'whoosh.mp3', 2.45, 0.35), (S + 'whoosh.mp3', 2.85, 0.35),
    (S + 'curtain_reveal.mp3', 3.25, 0.5),
    (S + 'choir_hallelujah_short.mp3', 3.30, 0.5),
    (S + 'record_scratch.mp3', 8.60, 0.45),
    (S + 'coin_clink.mp3', 11.70, 0.7),
    (S + 'sack_coins_thud.mp3', 21.70, 0.6),
    (S + 'many_doors_open.mp3', 21.62, 0.5, 0.0, 0.8),
    (S + 'cash_register.mp3', 25.10, 0.55),
    (S + 'sad_trombone.mp3', 29.90, 0.4),
]

BEDS = [
    ('library/sfx/amb_night_crickets.mp3', 6.8, 0.0, DUR, 0.35, False),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 0.0, DUR, 0.22, True),
]

VFX = {'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25'}
VGAIN = {'maz': 1.6, 'vadik': 1.7, 'wheel': 1.45, 'boss': 1.5}
