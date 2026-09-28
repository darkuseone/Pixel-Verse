"""S01E04 «Прокат» — single source of timing for video (ep04.py) and audio (mix.py)."""
DUR = 44.5
FPS = 30

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)   CAPS word = punch (speaker colour)
VOICE = [
    ('b1',  'ep04', 'b1', 0.05, 0.00, 3.63, 'billy',   'Ты УВОЛЕНА! Найду себе лошадь... ЧЕСТНУЮ!'),
    ('m1a', 'ep04', 'm1', 3.90, 0.00, 1.96, 'molniya', 'Выходное пособие...'),
    ('m1b', 'ep04', 'm1', 6.05, 2.59, 3.55, 'molniya', 'МОРКОВЬЮ.'),
    ('s1a', 'ep04', 's1', 8.75, 0.00, 4.19, 'sam',     'Добро пожаловать в прокат! Тарифы: эконом, комфорт...'),
    ('s1b', 'ep04', 's1', 13.45, 4.70, 5.80, 'sam',    'и ПРЕМИУМ.'),
    ('b2',  'ep04', 'b2', 16.00, 0.00, 3.18, 'billy',  'Мы с вами... раньше не ВСТРЕЧАЛИСЬ?'),
    ('s2',  'ep04', 's2', 19.60, 0.00, 3.44, 'sam',    'Никогда! Я Сэм... СЭМЮЭЛЬ.'),
    ('b3',  'ep04', 'b3', 27.40, 0.00, 3.89, 'billy',  'Вот это конь! Сразу видно — ЧЕСТНЫЙ!'),
    ('s3',  'ep04', 's3', 31.90, 0.00, 3.77, 'sam',    'Первый день бесплатно, дальше автопродление, отмена — только ПИСЬМОМ.'),
    ('c1a', 'ep01', 'c1', 38.00, 0.28, 1.64, 'billy',  'Н-но, РОДНАЯ!'),
    ('n5a', 'ep01', 'n5', 40.50, 0.20, 1.02, 'billy',  'МОЛНИЯ...'),
    ('m2',  'ep04', 'm2', 41.80, 0.00, 1.50, 'molniya', 'Спасибо за ПОДПИСКУ.'),
]

SFX = [
    ('library/sfx/horse_snort.mp3', 5.95, 0.6),
    ('library/sfx/boots_stomp.mp3', 7.05, 0.9),
    ('library/sfx/shop_bell.mp3', 8.30, 0.9),
    ('library/sfx/whoosh.mp3', 11.10, 0.4),
    ('library/sfx/cash_register.mp3', 13.50, 0.7),
    ('library/sfx/donkey_bray.mp3', 23.40, 0.8),
    ('library/sfx/rocking_creak.mp3', 24.85, 0.9),
    ('library/sfx/curtain_reveal.mp3', 26.35, 1.0),
    ('library/sfx/cash_register.mp3', 26.75, 0.6),
    ('library/sfx/paper_unroll.mp3', 32.00, 0.8),
    ('library/sfx/stamp.mp3', 37.20, 1.0),
    ('library/sfx/wind_gust.mp3', 39.60, 0.55),
    ('series/pochti-dikiy-zapad/sfx/cactus_boing.mp3', 40.15, 0.6),
    ('library/sfx/horse_snort.mp3', 41.35, 0.5),
    ('library/sfx/carrot_crunch.mp3', 43.35, 0.6),
]

# looped beds: (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 0.0, 8.6, 0.25, True),
    ('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 8.3, 37.4, 0.30, True),
    ('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 37.2, 44.5, 0.25, True),
    ('library/sfx/amb_desert_wind.mp3', 7.8, 0.0, 8.6, 0.9, False),
    ('library/sfx/amb_stable.mp3', 7.8, 8.3, 37.4, 0.8, False),
    ('library/sfx/amb_desert_wind.mp3', 7.8, 37.2, 44.5, 0.9, False),
]
