"""S01E05 «Операция «Кипяток»» — timing for video (ep05.py) and audio (mix.py)."""
DUR = 36.6
FPS = 30
SLUG = 'valera-i-kot'
MASTER = 0.8

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('v1', 'ep05', 'v1', 0.00, 0.18, 3.23, 'valera', 'Операция «Кипяток». НАЧИНАЕМ.'),
    ('c1', 'ep05', 'c1', 4.20, 0.00, 4.58, 'cat', 'Подвал. Прапорщик. Что может пойти НЕ ТАК?'),
    ('v2', 'ep05', 'v2', 9.00, 0.00, 3.25, 'valera', 'Не трогать? Прапорщику — МОЖНО.'),
    ('v3', 'ep05', 'v3', 12.40, 0.00, 2.30, 'valera', 'И-и-и... РАЗ!'),
    ('v4', 'ep05', 'v4', 15.90, 0.00, 2.38, 'valera', 'Пошла, РОДИМАЯ!'),
    ('v5', 'ep05', 'v5', 19.45, 0.40, 1.34, 'valera', 'А где?..'),
    ('c2', 'ep05', 'c2', 20.60, 0.00, 1.22, 'cat', 'Во ДВОРЕ.'),
    ('z1', 'ep05', 'z1', 23.60, 0.00, 2.72, 'zina', 'Люба, мы на КУРОРТЕ!'),
    ('l1', 'ep05', 'l1', 26.45, 0.00, 2.42, 'lyuba', 'Всё ВКЛЮЧЕНО.'),
    ('v6', 'ep05', 'v6', 29.05, 0.00, 2.02, 'valera', 'Бабоньки! А МНЕ?!'),
    ('z2', 'ep05', 'z2', 31.25, 0.20, 1.08, 'zina', 'Мест НЕТ.'),
    ('c3', 'ep05', 'c3', 32.50, 0.00, 3.52, 'cat', 'Двадцать лет в армии. Отопил ДВОР.'),
]

SFX = [
    ('library/sfx/flashlight_click.mp3', 0.00, 1.0),
    ('library/sfx/water_drip_single.mp3', 3.40, 0.5),
    ('library/sfx/water_drip_single.mp3', 7.10, 0.4),
    ('library/sfx/valve_creak.mp3', 12.55, 1.0),
    ('library/sfx/pipes_rumble.mp3', 14.30, 1.0),
    ('library/sfx/steam_hiss.mp3', 14.90, 0.7),
    ('library/sfx/stairs_run.mp3', 18.30, 0.9),
    ('library/sfx/tap_squeak.mp3', 19.10, 0.7),
    ('library/sfx/water_drip_single.mp3', 19.95, 1.0),
    ('library/sfx/whoosh.mp3', 21.95, 0.5),
    ('library/sfx/geyser_steam.mp3', 22.00, 0.9),
    ('library/sfx/bath_splash.mp3', 23.05, 0.6),
    ('library/sfx/rubber_duck.mp3', 28.95, 0.9),
    ('library/sfx/flashlight_click.mp3', 34.40, 0.9),
]

BEDS = [
    ('series/valera-i-kot/music/operation_sneaky_15s.mp3', 14.6, 0.0, 18.3, 0.24, True),
    ('series/valera-i-kot/music/theme_panelka_15s.mp3', 14.6, 21.9, 34.4, 0.22, True),
    ('series/valera-i-kot/music/operation_sneaky_15s.mp3', 14.6, 34.4, 36.6, 0.24, True),
    ('library/sfx/amb_basement.mp3', 7.8, 0.0, 18.4, 0.5, False),
    ('library/sfx/amb_flat_winter.mp3', 7.8, 18.3, 22.0, 0.4, False),
    ('library/sfx/amb_hot_spring.mp3', 7.8, 21.9, 34.5, 0.5, False),
    ('library/sfx/amb_winter_yard.mp3', 7.8, 21.9, 34.5, 0.25, False),
    ('library/sfx/amb_basement.mp3', 7.8, 34.4, 36.6, 0.5, False),
]
