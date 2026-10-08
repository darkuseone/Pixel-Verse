"""S01E05 v2 «Биотопливо» (08.10.2026: boss cuts the queue instead of Толик's callback) — timing for video (ep05.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep05_t)."""
DUR = 30.6
FPS = 30
SLUG = 'mazutych'
MASTER = 0.72

VOICE = [
    ('m1', 'ep05_t', 'm1', 0.25, 0.00, 2.53, 'maz', 'Почти ПОЛУЧИЛОСЬ.'),
    ('m2', 'ep05_t', 'm2', 3.95, 0.00, 3.24, 'maz', 'Лузга. Давление. НАУКА.'),
    ('d1', 'ep05_t', 'd1', 7.40, 0.00, 1.87, 'tolik', 'Одну тебе, одну МНЕ.'),
    ('d2', 'ep05_t', 'd2', 9.90, 0.00, 0.91, 'tolik', 'КАПАЕТ!'),
    ('m3', 'ep05_t', 'm3', 11.05, 0.00, 1.12, 'maz', 'НАЛИВАЙ!'),
    ('d3', 'ep05_t', 'd3', 13.90, 0.00, 2.20, 'tolik', 'Завелась, РОДИМАЯ!'),
    ('z1', 'ep05_t', 'z1', 16.60, 0.00, 3.11, 'zoyam', 'Бензина нет! Ждём СЕМЕЧКИ!'),
    ('b1', 'ep05_t', 'b1', 20.00, 0.00, 2.22, 'boss', 'Начальству — БЕЗ ОЧЕРЕДИ!'),
    ('m4', 'ep05_t', 'm4', 22.35, 0.00, 1.44, 'maz', 'Это МОЙ гараж!'),
    ('w1', 'ep05_t', 'w1', 24.00, 0.00, 2.02, 'wheel', 'Давление МНОГО, друга.'),
    ('m1b', 'ep05_t', 'm1', 26.70, 0.00, 2.53, 'maz', 'Почти ПОЛУЧИЛОСЬ.'),
]

CUTS = [0.0, 2.90, 3.80, 7.30, 9.40, 11.00, 12.30, 13.70, 16.30, 19.90, 22.25, 23.90, 26.10, DUR]

S = 'library/sfx/'
SFX = [
    (S + 'cartoon_boom_big.mp3', 0.00, 0.8),
    (S + 'debris_crash.mp3', 0.10, 0.4),
    (S + 'vhs_rewind.mp3', 2.90, 0.6),
    (S + 'sack_coins_thud.mp3', 7.45, 0.3),
    (S + 'water_drip_single.mp3', 9.75, 0.9),
    (S + 'choir_hallelujah_short.mp3', 9.70, 0.55),
    (S + 'old_car_start_roar.mp3', 12.35, 0.85),
    (S + 'crowd_cheer_short.mp3', 14.00, 0.35),
    (S + 'many_doors_open.mp3', 16.30, 0.5, 0.0, 0.8),
    (S + 'car_honks_chorus.mp3', 16.50, 0.5),
    (S + 'car_honks_chorus.mp3', 20.10, 0.45),
    (S + 'crowd_gasp.mp3', 20.30, 0.4),
    (S + 'pressure_whistle_rattle.mp3', 23.70, 2.6),
    (S + 'pressure_whistle_rattle.mp3', 25.10, 3.0, 0.0, 1.0),
    (S + 'cartoon_boom_big.mp3', 26.10, 0.9),
    (S + 'debris_crash.mp3', 26.20, 0.4),
]

BEDS = [
    ('library/sfx/amb_night_crickets.mp3', 6.8, 0.0, DUR, 0.3, False),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 2.9, 26.1, 0.24, True),
]

MEGA = 'highpass=f=420,lowpass=f=3600,acompressor=threshold=0.25:ratio=4,volume=1.3'
VFX = {'zoyam': MEGA, 'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25'}
VGAIN = {'maz': 1.6, 'zoyam': 1.55, 'wheel': 1.45, 'tolik': 1.5}
