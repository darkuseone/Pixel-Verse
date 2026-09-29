"""S01E04 «Сто сорок третий» — timing for video (ep04.py) and audio (mix.py)."""
DUR = 35.6
FPS = 30
SLUG = 'valera-i-kot'
MASTER = 0.78
PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {'robot': PHONE, 'nina': PHONE}

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('v1', 'ep04', 'v1', 0.00, 0.00, 1.65, 'valera', 'Алло! Это ЖЭК?!'),
    ('r1', 'ep04', 'r1', 1.75, 0.00, 4.62, 'robot', 'Ваш звонок очень важен для нас. Вы — сто сорок ТРЕТИЙ.'),
    ('c1', 'ep04', 'c1', 8.60, 2.24, 3.82, 'cat', 'Я уже ПОДПЕВАЮ.'),
    ('n1', 'ep04', 'n1', 10.45, 0.00, 2.36, 'nina', 'ЖЭК. Слушаю.'),
    ('v2', 'ep04', 'v2', 12.95, 0.00, 1.86, 'valera', 'Где горячая ВОДА?!'),
    ('n2', 'ep04', 'n2', 14.95, 0.00, 2.56, 'nina', 'В ТРУБАХ, мужчина.'),
    ('v3', 'ep04', 'v3', 17.65, 0.00, 2.05, 'valera', 'Когда в КРАНЕ будет?!'),
    ('n3', 'ep04', 'n3', 19.80, 0.00, 1.50, 'nina', 'До ПЯТНАДЦАТОГО.'),
    ('v4', 'ep04', 'v4', 21.40, 0.00, 2.37, 'valera', 'Сегодня ШЕСТНАДЦАТОЕ!'),
    ('n4', 'ep04', 'n4', 23.90, 0.00, 2.18, 'nina', 'Значит, до СЛЕДУЮЩЕГО.'),
    ('v5', 'ep04', 'v5', 27.15, 0.00, 2.57, 'valera', 'Это что... ПЛЕСК?!'),
    ('n5', 'ep04', 'n5', 29.85, 0.00, 2.48, 'nina_clear', 'Это вода. СЛУЖЕБНАЯ.'),
    ('r2', 'ep04', 'r2', 32.90, 0.00, 2.13, 'robot', 'Вы — сто сорок ЧЕТВЁРТЫЙ.'),
]

SFX = [
    ('library/sfx/phone_pickup.mp3', 0.00, 0.9),
    ('library/sfx/whoosh.mp3', 4.15, 0.35),
    ('library/sfx/clock_fast_ticks.mp3', 6.40, 0.6),
    ('library/sfx/clock_fast_ticks.mp3', 7.50, 0.5),
    ('library/sfx/phone_pickup.mp3', 10.25, 0.8),
    ('library/sfx/fist_slam_counter.mp3', 21.45, 0.9),
    ('library/sfx/whoosh.mp3', 23.95, 0.5),
    ('library/sfx/bath_splash.mp3', 26.15, 1.0),
    ('library/sfx/rubber_duck.mp3', 26.90, 0.9),
    ('library/sfx/bath_splash.mp3', 30.10, 0.6),
    ('library/sfx/phone_slam.mp3', 32.50, 1.0),
]

BEDS = [
    ('series/valera-i-kot/music/theme_panelka_15s.mp3', 14.6, 0.0, 6.35, 0.22, True),
    ('library/sfx/hold_music_elise.mp3', 14.3, 6.25, 10.45, 0.55, True),
    ('series/valera-i-kot/music/theme_panelka_15s.mp3', 14.6, 10.35, 23.95, 0.22, True),
    ('series/valera-i-kot/music/operation_sneaky_15s.mp3', 14.6, 23.9, 35.6, 0.22, True),
    ('library/sfx/amb_flat_winter.mp3', 7.8, 0.0, 10.4, 0.4, False),
    ('library/sfx/amb_office_night.mp3', 7.8, 10.3, 35.6, 0.45, False),
]
