"""S01E03 «Информатор» — single source of timing for video (ep03.py) and audio (mix.py)."""
DUR = 45.0
FPS = 30

# voice pieces: (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption_text)
# caption text: words in CAPS are the punch words (coloured); tags are stripped already.
VOICE = [
    ('b1',  'ep03', 'b1', 0.05, 0.00, 3.40, 'billy',   'Всем стоять! Мне нужен ИНФОРМАТОР!'),
    ('s1',  'ep03', 's1', 4.30, 0.00, 3.97, 'sam',     'Итак, мэм. Как обычно: морковь за неделю?'),
    ('m1a', 'ep03', 'm1', 8.35, 0.00, 0.90, 'molniya', 'Инфляция.'),
    ('m1b', 'ep03', 'm1', 9.70, 4.02, 4.44, 'molniya', 'ДВЕ.'),
    ('s2',  'ep03', 's2', 11.45, 0.00, 2.85, 'sam',    'Грабёж средь бела ДНЯ.'),
    ('n5a', 'ep01', 'n5', 17.10, 0.20, 1.02, 'billy',  'Молния...'),
    ('n5b', 'ep01', 'n5', 17.95, 1.59, 3.87, 'billy',  'Ты не видела Кривого СЭМА?'),
    ('n6',  'ep01', 'n6', 21.25, 0.24, 0.66, 'molniya', 'НЕ-А.'),
    ('b2',  'ep03', 'b2', 22.40, 0.00, 4.21, 'billy',  'А вы, мистер... случайно не ИНФОРМАТОР?'),
    ('s3a', 'ep03', 's3', 27.65, 0.00, 3.40, 'sam',    'Информатор. Сэм уехал на ЮГ.'),
    ('s3b', 'ep03', 's3', 31.55, 4.80, 6.35, 'sam',    'Пять ДОЛЛАРОВ.'),
    ('b3',  'ep03', 'b3', 34.05, 0.00, 2.35, 'billy',  'За мной, Молния! На ЮГ!'),
    ('n4',  'ep01', 'n4', 39.20, 0.00, 0.72, 'molniya', 'СПАСИБО.'),
    ('m2a', 'ep03', 'm2', 40.30, 0.00, 0.72, 'molniya', 'Третий год.'),
    ('m2b', 'ep03', 'm2', 41.60, 4.47, 5.49, 'molniya', 'Лучший КЛИЕНТ.'),
]

# sfx: (path relative to repo, t_start, gain)
SFX = [
    ('library/sfx/saloon_doors_bang.mp3', 0.00, 1.0),
    ('library/sfx/piano_stop.mp3', 2.05, 0.8),
    ('library/sfx/whoosh.mp3', 4.05, 0.5),
    ('library/sfx/whoosh.mp3', 9.95, 0.4),
    ('library/sfx/saloon_doors_bang.mp3', 14.50, 0.6),      # hand slam on the counter (bang part)
    ('library/sfx/whoosh.mp3', 16.35, 0.8),                 # whip pan
    ('library/sfx/coin_clink.mp3', 33.35, 1.0),
    ('library/sfx/saloon_doors_bang.mp3', 36.35, 1.0),
    ('library/sfx/coin_clink.mp3', 38.80, 0.6),
    ('library/sfx/carrot_crunch.mp3', 43.20, 0.7),
]

# music: theme looped; muted for the freeze gag (piano stops) 2.9..4.2
MUSIC = 'series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3'
MUSIC_LOOP = 14.6           # usable length of the theme (tail is silence)
MUSIC_MUTE = [(2.9, 4.2)]
