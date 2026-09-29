"""S01E01 «Закалка» — timing for video (ep01.py) and audio (mix.py)."""
DUR = 34.8
FPS = 30
SLUG = 'valera-i-kot'

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('v1', 'ep01', 'v1', 0.00, 0.00, 2.40, 'valera', 'А-а-а! ЛЕДЯНАЯ!'),
    ('v2', 'ep01', 'v2', 3.70, 0.00, 4.22, 'valera', 'Ничего! Я ДВАДЦАТЬ лет в армии!'),
    ('c1', 'ep01', 'c1', 8.05, 0.20, 1.45, 'cat', 'На СКЛАДЕ.'),
    ('v3', 'ep01', 'v3', 10.60, 0.00, 2.65, 'valera', 'Дембель! Операция «ТАЗИК»!'),
    ('c2', 'ep01', 'c2', 14.00, 0.00, 1.90, 'cat', 'К ВЕСНЕ помоется.'),
    ('v4', 'ep01', 'v4', 17.20, 0.00, 3.45, 'valera', 'Стоп... В батарее — ГОРЯЧАЯ!'),
    ('v5', 'ep01', 'v5', 22.20, 0.00, 1.75, 'valera', 'ГОРЯЧЕНЬКАЯ!'),
    ('v6', 'ep01', 'v6', 25.30, 0.00, 2.60, 'valera', 'Как в санатории...'),
    ('c3', 'ep01', 'c3', 28.30, 0.00, 1.15, 'cat', 'КОПЧЁНЫЙ.'),
    ('c4', 'ep01', 'c4', 30.40, 0.00, 3.15, 'cat', 'Ещё ЧЕТЫРНАДЦАТЬ дней.'),
]

SFX = [
    ('library/sfx/shower_cold_spray.mp3', 0.00, 0.9),
    ('library/sfx/whoosh.mp3', 2.35, 0.5),
    ('library/sfx/paper_unroll.mp3', 2.45, 0.6),
    ('library/sfx/shower_cold_spray.mp3', 2.40, 0.35, 0.0, 1.2),
    ('library/sfx/whoosh.mp3', 9.35, 0.4),
    ('library/sfx/basin_clank.mp3', 10.55, 0.8),
    ('library/sfx/clock_fast_ticks.mp3', 15.90, 0.7),
    ('library/sfx/kettle_whistle.mp3', 16.30, 0.55, 0.0, 1.0),
    ('library/sfx/radiator_valve_gush.mp3', 20.55, 1.0),
    ('library/sfx/steam_hiss.mp3', 21.60, 0.6),
    ('library/sfx/basin_clank.mp3', 22.10, 0.6),
    ('library/sfx/water_pour_head.mp3', 24.00, 1.0),
    ('library/sfx/steam_hiss.mp3', 24.40, 0.8),
    ('library/sfx/steam_hiss.mp3', 26.20, 0.4),
    ('library/sfx/whoosh.mp3', 30.30, 0.35),
    ('library/sfx/tap_squeak.mp3', 34.05, 0.9),
]

# looped beds: (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/valera-i-kot/music/theme_panelka_15s.mp3', 14.6, 0.0, 17.3, 0.26, True),
    ('series/valera-i-kot/music/operation_sneaky_15s.mp3', 14.6, 17.1, 25.4, 0.26, True),
    ('series/valera-i-kot/music/theme_panelka_15s.mp3', 14.6, 25.2, 34.8, 0.24, True),
    ('library/sfx/amb_flat_winter.mp3', 7.8, 2.4, 34.8, 0.5, False),
]
MASTER = 0.8
