"""S01E05 «Почти поймал» — single source of timing for video (ep05.py) and audio (mix.py)."""
DUR = 45.0
FPS = 30

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)   CAPS word = punch (speaker colour)
VOICE = [
    ('m1a', 'ep05', 'm1', 0.10, 0.00, 1.88, 'molniya', 'Сэм просрочил ПЛАТЁЖ.'),
    ('m1b', 'ep05', 'm1', 3.10, 2.61, 3.87, 'molniya', 'Подъём, КОВБОЙ.'),
    ('b1',  'ep05', 'b1', 5.00, 0.00, 1.99, 'billy',   'Ты... мне ПОМОГАЕШЬ?!'),
    ('m2',  'ep05', 'm2', 7.50, 0.00, 1.11, 'molniya', 'Не ПРИВЫКАЙ.'),
    ('b2',  'ep05', 'b2', 12.00, 0.00, 2.90, 'billy',  'Йи-ха! Попался, Кривой СЭМ!'),
    ('s1',  'ep05', 's1', 16.20, 0.00, 2.51, 'sam',    'Мэм! Мы же ДОГОВОРИЛИСЬ!'),
    ('m3',  'ep05', 'm3', 18.90, 0.00, 2.52, 'molniya', 'Оплата была... ВЧЕРА.'),
    ('b3',  'ep05', 'b3', 21.80, 0.00, 2.46, 'billy',  'Три года! НАКОНЕЦ-ТО!'),
    ('b4',  'ep05', 'b4', 25.00, 0.00, 4.31, 'billy',  'Сначала — фото. Для плаката «ЛУЧШИЙ КОВБОЙ».'),
    ('s2',  'ep05', 's2', 33.60, 0.00, 1.74, 'sam',    'Прекрасное фото, СЭР!'),
    ('n5b', 'ep01', 'n5', 35.90, 1.59, 3.87, 'billy',  'Ты не видела Кривого СЭМА?'),
    ('n6',  'ep01', 'n6', 38.70, 0.24, 0.66, 'molniya', 'НЕ-А.'),
]

SFX = [
    ('library/sfx/bucket_clang.mp3', 0.00, 0.9),
    ('library/sfx/snore.mp3', 2.50, 0.7),
    ('library/sfx/whoosh.mp3', 4.40, 0.5),
    ('library/sfx/whoosh.mp3', 9.45, 0.6),
    ('library/sfx/horse_gallop.mp3', 9.60, 0.8),
    ('library/sfx/donkey_walk.mp3', 9.70, 0.6),
    ('library/sfx/horse_gallop.mp3', 11.50, 0.8),
    ('library/sfx/lasso_swing.mp3', 12.30, 0.6),
    ('library/sfx/horse_gallop.mp3', 13.40, 0.8),
    ('library/sfx/lasso_swing.mp3', 13.70, 0.6),
    ('library/sfx/rope_yank.mp3', 14.95, 1.0),
    ('library/sfx/donkey_bray.mp3', 15.50, 0.7),
    ('library/sfx/whoosh.mp3', 21.45, 0.5),
    ('library/sfx/cash_register.mp3', 22.00, 0.6),
    ('library/sfx/camera_flash.mp3', 29.80, 0.9),
    ('library/sfx/carrot_crunch.mp3', 30.50, 0.6),
    ('library/sfx/camera_flash.mp3', 31.00, 0.9),
    ('library/sfx/rope_yank.mp3', 31.60, 0.6),
    ('library/sfx/camera_flash.mp3', 32.20, 0.9),
    ('library/sfx/donkey_walk.mp3', 33.30, 0.5),
    ('library/sfx/horse_snort.mp3', 38.30, 0.5),
    ('library/sfx/carrot_crunch.mp3', 39.20, 0.7),
    ('library/sfx/camera_flash.mp3', 40.00, 0.8),
]

# looped beds: (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 0.0, 9.7, 0.28, True),
    ('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 9.5, 29.4, 0.26, True),
    ('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 29.2, 45.0, 0.30, True),
    ('library/sfx/amb_campfire_night.mp3', 7.8, 0.0, 9.7, 0.9, False),
    ('library/sfx/amb_desert_wind.mp3', 7.8, 9.5, 21.7, 0.7, False),
    ('library/sfx/amb_desert_wind.mp3', 7.8, 21.5, 45.0, 0.8, False),
]
