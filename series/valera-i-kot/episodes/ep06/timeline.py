"""S01E06 «С лёгким паром» — timing for video (ep06.py) and audio (mix.py)."""
DUR = 36.4
FPS = 30
SLUG = 'valera-i-kot'
MASTER = 0.74
T_OPEN = 12.10          # the mezzanine cupboard bursts open
T_DOOR = 17.60          # bathroom door: steam + the cat in the tub
T_MIDNIGHT = 24.10      # clock strikes twelve
T_ICE = 28.40           # the shower turns icy (callback to the very first frame of E01)

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('v1', 'ep06', 'v1', 0.00, 0.08, 4.46, 'valera', 'Тридцать первое! Горячая вода. ТРАДИЦИЯ!'),
    ('c1', 'ep06', 'c1', 4.55, 0.10, 1.78, 'cat', 'Третий год ПОДРЯД.'),
    ('v2', 'ep06', 'v2', 8.40, 0.00, 1.28, 'valera', 'ДАЛИ!'),
    ('v3', 'ep06', 'v3', 9.80, 0.00, 2.40, 'valera', 'Полотенце! Тапки! МОЧАЛКУ!'),
    ('v4', 'ep06', 'v4', 13.50, 0.00, 2.98, 'valera', 'Двадцать лет — всё по МЕСТАМ!'),
    ('c2', 'ep06', 'c2', 17.70, 0.09, 2.50, 'cat', 'С лёгким ПАРОМ.'),
    ('v5', 'ep06', 'v5', 20.25, 0.00, 1.99, 'valera', 'Это МОЯ традиция!'),
    ('c3', 'ep06', 'c3', 22.35, 0.08, 1.79, 'cat', 'Теперь — НАША.'),
    ('v6', 'ep06', 'v6', 25.60, 0.20, 2.65, 'valera', 'С Новым годом, ДЕМБЕЛЬ.'),
    ('v7', 'ep01', 'v1', T_ICE, 0.00, 2.40, 'valera', 'А-а-а! ЛЕДЯНАЯ!'),
    ('c4', 'ep06', 'c4', 32.50, 0.11, 1.25, 'cat', 'ТРАДИЦИЯ.'),
]

SFX = [
    ('library/sfx/basin_clank.mp3', 0.00, 0.9),
    ('library/sfx/paper_unroll.mp3', 1.75, 0.5),
    ('library/sfx/whoosh.mp3', 6.35, 0.4),
    ('library/sfx/clock_fast_ticks.mp3', 6.40, 0.7),
    ('library/sfx/faucet_sputter_gush.mp3', 7.45, 1.0),
    ('library/sfx/steam_hiss.mp3', 8.30, 0.6),
    ('library/sfx/junk_avalanche.mp3', T_OPEN, 1.0),
    ('library/sfx/basin_clank.mp3', T_OPEN + 1.05, 0.6),
    ('library/sfx/stairs_run.mp3', 16.55, 0.6),
    ('library/sfx/whoosh.mp3', T_DOOR - 0.05, 0.5),
    ('library/sfx/steam_hiss.mp3', T_DOOR, 0.8),
    ('library/sfx/bath_splash.mp3', T_DOOR + 0.35, 0.4),
    ('library/sfx/rubber_duck.mp3', 19.55, 0.8),
    ('library/sfx/clock_midnight_chime.mp3', T_MIDNIGHT, 0.9),
    ('library/sfx/fireworks_distant.mp3', T_MIDNIGHT + 0.6, 0.3),
    ('library/sfx/tap_squeak.mp3', 28.15, 0.8),
    ('library/sfx/shower_cold_spray.mp3', T_ICE - 0.05, 0.9),
    ('library/sfx/fireworks_distant.mp3', 30.80, 0.9),
    ('series/valera-i-kot/voice/ep01/v1.mp3', 30.95, 0.28, 1.1, 2.4),
    ('library/sfx/whoosh.mp3', 33.75, 0.4),
    ('library/sfx/stamp.mp3', 34.40, 1.0),
]

# looped beds: (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/valera-i-kot/music/new_year_15s.mp3', 14.6, 0.0, 28.3, 0.24, True),
    ('series/valera-i-kot/music/new_year_15s.mp3', 14.6, 30.8, 36.4, 0.24, True),
    ('library/sfx/amb_flat_winter.mp3', 7.8, 0.0, 17.6, 0.45, False),
    ('library/sfx/amb_hot_spring.mp3', 7.8, 17.6, 30.8, 0.3, False),
    ('library/sfx/amb_winter_yard.mp3', 7.8, 30.8, 32.5, 0.4, False),
    ('library/sfx/amb_flat_winter.mp3', 7.8, 32.5, 36.4, 0.4, False),
]
