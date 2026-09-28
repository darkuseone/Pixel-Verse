"""S01E04 «Прокат» — single source of timing for video (ep04.py) and audio (mix.py)."""
DUR = 44.5
FPS = 30

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)   CAPS word = punch (speaker colour)
VOICE = [
    ('b1',  'ep04', 'b1', 0.05, 0.00, 3.71, 'billy',   'Ты УВОЛЕНА! Найду себе лошадь ЧЕСТНУЮ!'),
    ('m1a', 'ep04', 'm1', 3.95, 0.00, 1.31, 'molniya', 'Выходное пособие.'),
    ('m1b', 'ep04', 'm1', 5.75, 4.47, 5.13, 'molniya', 'МОРКОВЬЮ.'),
    ('s1a', 'ep04', 's1', 8.75, 0.00, 5.00, 'sam',     'Добро пожаловать в прокат! Тарифы: эконом, комфорт...'),
    ('s1b', 'ep04', 's1', 14.20, 5.75, 7.24, 'sam',    'и ПРЕМИУМ.'),
    ('b2',  'ep04', 'b2', 16.00, 0.00, 3.32, 'billy',  'Мы с вами... раньше не ВСТРЕЧАЛИСЬ?'),
    ('s2',  'ep04', 's2', 19.60, 0.00, 3.63, 'sam',    'Никогда. Я Сэм... СЭМЮЭЛЬ.'),
    ('b3',  'ep04', 'b3', 27.40, 0.00, 4.21, 'billy',  'Вот это конь! Сразу видно — ЧЕСТНЫЙ!'),
    ('s3',  'ep04', 's3', 31.90, 0.00, 5.25, 'sam',    'Первый день бесплатно. Дальше автопродление. Отмена — ПИСЬМОМ.'),
    ('c1a', 'ep01', 'c1', 38.00, 0.28, 1.64, 'billy',  'Н-но, РОДНАЯ!'),
    ('n5a', 'ep01', 'n5', 40.50, 0.20, 1.02, 'billy',  'МОЛНИЯ...'),
    ('m2',  'ep04', 'm2', 41.80, 0.00, 1.11, 'molniya', 'Спасибо за ПОДПИСКУ.'),
]

SFX = [
    ('library/sfx/whoosh.mp3', 6.40, 0.5),
    ('library/sfx/shop_bell.mp3', 8.30, 0.9),
    ('library/sfx/whoosh.mp3', 11.15, 0.4),
    ('library/sfx/donkey_bray.mp3', 23.40, 0.8),
    ('library/sfx/whoosh.mp3', 24.85, 0.5),
    ('library/sfx/curtain_reveal.mp3', 26.35, 1.0),
    ('library/sfx/stamp.mp3', 37.20, 1.0),
    ('library/sfx/whoosh.mp3', 39.70, 0.6),
    ('series/pochti-dikiy-zapad/sfx/cactus_boing.mp3', 40.15, 0.6),
    ('library/sfx/carrot_crunch.mp3', 42.95, 0.6),
]

MUSIC = 'series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3'
MUSIC_LOOP = 14.6
MUSIC_MUTE = []
