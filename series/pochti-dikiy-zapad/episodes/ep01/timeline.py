"""S01E01 «Самый быстрый» (HD-пересборка на общем движке) — timing for video (ep01.py) and audio (mix.py)."""
DUR = 35.6
FPS = 30

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)   CAPS word = punch (speaker colour)
VOICE = [
    ('c1',  'ep01', 'c1', 0.00, 0.30, 5.70, 'billy',   'Н-но, родная! Я — САМЫЙ быстрый ковбой на всём Диком Западе!'),
    ('n1',  'ep01', 'n1', 5.60, 0.00, 4.30, 'billy',   'Сегодня я наконец поймаю Кривого СЭМА!'),
    ('n2',  'ep01', 'n2', 10.00, 0.10, 1.70, 'molniya', 'Он ловит его ТРЕТИЙ год.'),
    ('c2',  'ep01', 'c2', 12.50, 0.10, 2.16, 'billy',   'А-А-А-А-А!'),
    ('c3a', 'ep01', 'c3', 15.35, 0.13, 0.75, 'billy',   'Ой...'),
    ('c3b', 'ep01', 'c3', 16.25, 1.36, 2.00, 'billy',   'КАКТУС...'),
    ('h1a', 'ep01', 'h1', 17.50, 0.00, 1.45, 'molniya', 'Самый быстрый тут — Я.'),
    ('h1b', 'ep01', 'h1', 19.15, 3.05, 4.50, 'molniya', 'А ты просто сверху СИДЕЛ.'),
    ('n3',  'ep01', 'n3', 21.60, 0.10, 2.55, 'sam',     'Приятного аппетита, МЭМ.'),
    ('n4',  'ep01', 'n4', 24.30, 0.12, 0.75, 'molniya', 'СПАСИБО.'),
    ('n5',  'ep01', 'n5', 26.40, 0.15, 3.90, 'billy',   'Молния... Ты не видела Кривого СЭМА?'),
    ('n6',  'ep01', 'n6', 30.50, 0.20, 0.66, 'molniya', 'НЕ-А.'),
]

SFX = [
    ('library/sfx/horse_gallop.mp3', 0.00, 0.8), ('library/sfx/horse_gallop.mp3', 1.80, 0.8), ('library/sfx/horse_gallop.mp3', 3.60, 0.8),
    ('library/sfx/horse_gallop.mp3', 5.40, 0.8), ('library/sfx/horse_gallop.mp3', 7.20, 0.8), ('library/sfx/horse_gallop.mp3', 9.00, 0.8),
    ('library/sfx/horse_gallop.mp3', 10.80, 0.8),
    ('library/sfx/brake_skid.mp3', 12.30, 1.0),
    ('library/sfx/whoosh.mp3', 12.55, 0.7),
    ('series/pochti-dikiy-zapad/sfx/cactus_boing.mp3', 14.95, 1.0),
    ('library/sfx/carrot_crunch.mp3', 17.60, 0.6), ('library/sfx/carrot_crunch.mp3', 18.30, 0.6),
    ('library/sfx/donkey_walk.mp3', 20.60, 0.5),
    ('library/sfx/donkey_bray.mp3', 25.00, 0.7),
    ('library/sfx/donkey_walk.mp3', 26.40, 0.5),
    ('library/sfx/carrot_crunch.mp3', 32.60, 0.6),
]

# looped beds: (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 0.0, 12.6, 0.26, True),
    ('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 14.6, 35.6, 0.28, True),
    ('library/sfx/amb_desert_wind.mp3', 7.8, 0.0, 35.6, 0.7, False),
]
