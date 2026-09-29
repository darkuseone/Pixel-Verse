"""S01E02 «Цена по карте» — timing for video (ep02.py) and audio (mix.py)."""
DUR = 37.35
FPS = 30
SLUG = 'valera-i-kot'
MASTER = 0.8

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('v1', 'ep02', 'v1', 0.00, 0.00, 1.05, 'valera', 'СКОЛЬКО?!'),
    ('t1', 'ep02', 't1', 1.15, 0.25, 2.62, 'tamara', 'Двести восемьдесят ДЕВЯТЬ.'),
    ('v2', 'ep02', 'v2', 3.60, 0.00, 3.22, 'valera', 'На ценнике — сто девяносто ДЕВЯТЬ!'),
    ('t2a', 'ep02', 't2', 7.00, 0.00, 1.85, 'tamara', 'Крупно — по КАРТЕ.'),
    ('t2b', 'ep02', 't2', 9.05, 2.32, 2.97, 'tamara', 'Мелко —'),
    ('t2c', 'ep02', 't2', 9.75, 3.20, 4.08, 'tamara', 'по ПРАВДЕ.'),
    ('v3', 'ep02', 'v3', 10.70, 0.00, 2.70, 'valera', 'Я двадцать лет в АРМИИ!'),
    ('t3', 'ep02', 't3', 13.55, 0.00, 2.20, 'tamara', 'А я тридцать — на КАССЕ.'),
    ('v4', 'ep02', 'v4', 16.20, 0.25, 2.82, 'valera', 'По закону — цена с ПОЛКИ!'),
    ('t4a', 'ep02', 't4', 18.90, 0.00, 1.78, 'tamara', 'Ладно...'),
    ('t4b', 'ep02', 't4', 20.85, 2.32, 3.98, 'tamara', 'Сто девяносто девять.'),
    ('v5', 'ep02', 'v5', 22.65, 0.00, 2.14, 'valera', 'Так-то! И ПАКЕТ.'),
    ('t5', 'ep02', 't5', 24.95, 0.00, 1.85, 'tamara', 'Пакет — ДЕВЯНОСТО.'),
    ('c1', 'ep02', 'c1', 28.15, 0.20, 4.95, 'cat', 'Двести восемьдесят девять... ЧУВСТВУЕТСЯ.'),
    ('v6', 'ep02', 'v6', 33.10, 0.20, 1.87, 'valera', 'Пакет — СВОЙ!'),
    ('t6', 'ep02', 't6', 34.90, 0.22, 2.12, 'tamara', 'Двести ДЕВЯНОСТО девять.'),
]
# t2 is split in three: «Крупно — по карте.» / «Мелко —» / «по правде.» (long pauses inside the take are cut)

SFX = [
    ('library/sfx/scanner_beep.mp3', 0.00, 0.8),
    ('library/sfx/whoosh.mp3', 1.05, 0.35),
    ('library/sfx/gum_pop.mp3', 3.40, 0.9),
    ('library/sfx/whoosh.mp3', 5.25, 0.45),
    ('library/sfx/fist_slam_counter.mp3', 16.25, 1.0),
    ('library/sfx/register_keys.mp3', 20.55, 0.8),
    ('library/sfx/cash_register.mp3', 22.45, 0.7),
    ('library/sfx/plastic_bag_rustle.mp3', 24.80, 0.9),
    ('library/sfx/receipt_printer.mp3', 26.90, 0.9),
    ('library/sfx/cat_chewing.mp3', 28.15, 0.7),
    ('library/sfx/cat_chewing.mp3', 30.65, 0.6),
    ('library/sfx/plastic_bag_rustle.mp3', 33.05, 0.7),
    ('library/sfx/scanner_beep.mp3', 34.75, 0.8),
    ('library/sfx/scanner_beep.mp3', 37.20, 0.8),
]

BEDS = [
    ('series/valera-i-kot/music/theme_panelka_15s.mp3', 14.6, 0.0, 28.05, 0.24, True),
    ('series/valera-i-kot/music/theme_panelka_15s.mp3', 14.6, 28.05, 33.05, 0.22, True),
    ('series/valera-i-kot/music/theme_panelka_15s.mp3', 14.6, 32.95, 37.35, 0.24, True),
    ('library/sfx/amb_grocery_store.mp3', 7.8, 0.0, 28.15, 0.5, False),
    ('library/sfx/amb_flat_winter.mp3', 7.8, 28.15, 33.05, 0.45, False),
    ('library/sfx/amb_grocery_store.mp3', 7.8, 32.95, 37.35, 0.5, False),
]
