"""S01E03 «Разведка» — timing for video (ep03.py) and audio (mix.py)."""
DUR = 34.4
FPS = 30
SLUG = 'valera-i-kot'
MASTER = 0.9

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('v1', 'ep03', 'v1', 0.00, 0.18, 2.84, 'valera', 'Бабки на посту. Идём СКРЫТНО.'),
    ('z1a', 'ep03', 'z1', 4.20, 0.00, 0.70, 'zina', 'Люба.'),
    ('z1b', 'ep03', 'z1', 5.05, 1.17, 2.32, 'zina', 'СУГРОБ ползёт.'),
    ('l1', 'ep03', 'l1', 6.45, 0.00, 1.60, 'lyuba', 'С ПУЗОМ.'),
    ('v2', 'ep03', 'v2', 8.25, 0.00, 3.30, 'valera', 'Я сугроб. Я СУГРОБ.'),
    ('z2', 'ep03', 'z2', 11.75, 0.00, 1.96, 'zina', 'Сугроб, ты КУДА?'),
    ('v3', 'ep03', 'v3', 13.90, 0.27, 1.32, 'valera', 'За ХЛЕБОМ!'),
    ('l2', 'ep03', 'l2', 15.25, 0.00, 3.38, 'lyuba', 'Хлеб в БУТЫЛКАХ не продают.'),
    ('v4', 'ep03', 'v4', 19.15, 0.00, 2.72, 'valera', 'Бабоньки... ДОГОВОРИМСЯ?'),
    ('z3', 'ep03', 'z3', 22.05, 0.28, 1.97, 'zina', 'Мы тебя НЕ ВИДЕЛИ.'),
    ('z4', 'ep03', 'z4', 24.60, 0.00, 3.14, 'zina', 'Алло, Тамара? Валера идёт. Готовь ПАКЕТ.'),
    ('c1', 'ep03', 'c1', 28.70, 0.00, 4.90, 'cat', 'Двадцать лет в армии. Спалился за ДВАДЦАТЬ секунд.'),
]

SFX = [
    ('library/sfx/whoosh.mp3', 0.00, 0.3),
    ('library/sfx/snow_crawl.mp3', 3.70, 0.9),
    ('library/sfx/knitting.mp3', 6.40, 0.6),
    ('library/sfx/snow_crawl.mp3', 12.20, 0.5),
    ('library/sfx/cloth_flap.mp3', 13.80, 1.0),
    ('library/sfx/whoosh.mp3', 13.85, 0.4),
    ('library/sfx/knitting.mp3', 15.30, 0.5),
    ('library/sfx/snow_steps.mp3', 21.95, 0.8),
    ('library/sfx/whistle_tune.mp3', 22.40, 0.5),
    ('library/sfx/flip_phone.mp3', 24.10, 0.9),
    ('library/sfx/brake_skid.mp3', 27.70, 0.35),
    ('library/sfx/whoosh.mp3', 28.60, 0.35),
]

BEDS = [
    ('series/valera-i-kot/music/operation_sneaky_15s.mp3', 14.6, 0.0, 22.0, 0.25, True),
    ('series/valera-i-kot/music/theme_panelka_15s.mp3', 14.6, 21.9, 34.4, 0.24, True),
    ('library/sfx/amb_winter_yard.mp3', 7.8, 0.0, 28.6, 0.6, False),
    ('library/sfx/amb_flat_winter.mp3', 7.8, 28.6, 34.4, 0.45, False),
]
