"""S01E03 v2 «Из-под полы» (08.10.2026, по статистике TikTok) — timing for video (ep03.py) and audio (mix.py).
Voice clips are the tightened takes (voice/ep03_t)."""
DUR = 27.3
FPS = 30
SLUG = 'mazutych'
MASTER = 0.82

VOICE = [
    ('m0', 'ep03_t', 'm0', 0.00, 0.00, 1.78, 'maz', 'Пятьсот?! За ЛИТР?!'),
    ('v4', 'ep03_t', 'v4', 1.90, 0.00, 1.34, 'vadik', 'За ПОСМОТРЕТЬ.'),
    ('v2', 'ep03_t', 'v2', 3.35, 0.00, 2.76, 'vadik', 'Девяносто пятый. СВЕЖАК.'),
    ('m3', 'ep03_t', 'm3', 6.30, 0.00, 3.21, 'maz', 'Это НЕ девяносто пятый.'),
    ('v5', 'ep03_t', 'v5', 9.65, 0.00, 0.92, 'vadik', 'А КАКОЙ?'),
    ('m4', 'ep03_t', 'm4', 10.70, 0.00, 2.33, 'maz', 'МОЙ. Партия четырнадцать.'),
    ('v6', 'ep03_t', 'v6', 13.15, 0.00, 2.37, 'vadik', 'Так я ж у твоего НАЧАЛЬНИКА беру.'),
    ('b1', 'ep03_t', 'b1', 15.90, 0.00, 2.89, 'boss', 'Мазутыч? Тебе — со СКИДКОЙ!'),
    ('b2', 'ep03_t', 'b2', 19.00, 0.00, 2.06, 'boss', 'Литр — по цене ДВУХ.'),
    ('v7', 'ep03_t', 'v7', 21.20, 0.00, 0.92, 'vadik', 'СКИДКА.'),
    ('w1', 'ep03_t', 'w1', 22.25, 0.00, 1.58, 'wheel', 'Это НЕ скидка, друга.'),
    ('b3', 'ep03_t', 'b3', 24.00, 0.00, 1.65, 'boss', 'Или — по ТАЛОНУ!'),
]

#        hook  v500  trunk sniff which mine  bossln REVEAL bosscu money  nod    button talon  wallet
CUTS = [0.0, 1.85, 3.30, 6.20, 9.60, 10.60, 13.10, 15.60, 17.30, 18.90, 21.10, 22.20, 23.90, 25.70, DUR]
TWIST = 15.60

S = 'library/sfx/'
SFX = [
    (S + 'record_scratch.mp3', 0.00, 0.5),
    (S + 'glass_slide.mp3', 1.90, 0.5),
    (S + 'curtain_reveal.mp3', 3.30, 0.5),
    (S + 'choir_hallelujah_short.mp3', 3.35, 0.5),
    (S + 'coin_clink.mp3', 6.25, 0.7),
    (S + 'many_doors_open.mp3', 15.62, 0.5, 0.0, 0.8),
    (S + 'sack_coins_thud.mp3', 15.70, 0.6),
    (S + 'cash_register.mp3', 19.10, 0.55),
    (S + 'paper_unroll.mp3', 24.05, 0.6),
    (S + 'cloth_flap.mp3', 25.75, 0.5),
    (S + 'sad_trombone.mp3', 25.95, 0.4),
]

BEDS = [
    ('library/sfx/amb_night_crickets.mp3', 6.8, 0.0, DUR, 0.35, False),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 0.0, DUR, 0.22, True),
]

VFX = {'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25'}
VGAIN = {'maz': 1.6, 'vadik': 1.7, 'wheel': 1.45, 'boss': 1.5}
