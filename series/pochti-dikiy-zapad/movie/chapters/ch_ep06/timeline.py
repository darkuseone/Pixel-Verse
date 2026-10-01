"""S01E06 «Самый быстрый. Реванш» (финал сезона) — timing for video (ep06.py) and audio (mix.py)."""
DUR = 47.0
FPS = 30

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('b1',  'ep06', 'b1', 0.05, 0.00, 3.10, 'billy',   'Три года... я ждал этого ДНЯ.'),
    ('s1',  'ep06', 's1', 3.40, 0.00, 3.04, 'sam',     'Удачи, сэр. Она вам ПОНАДОБИТСЯ.'),
    ('b2',  'ep06', 'b2', 8.60, 0.00, 3.66, 'billy',   'Молния, выиграем — куплю тебе мешок МОРКОВКИ!'),
    ('m1',  'ep06', 'm1', 12.50, 0.00, 1.60, 'molniya', 'Ставки ПРИНЯТЫ.'),
    ('yh',  'ep05', 'b2', 17.80, 0.00, 1.07, 'billy',  'ЙИ-ХА!'),
    ('s3',  'ep06', 's3', 19.80, 0.00, 2.17, 'sam',    'Морковка уже на ФИНИШЕ.'),
    ('c2',  'ep01', 'c2', 25.30, 0.13, 2.16, 'billy',  'А-А-А-А!'),
    ('c3a', 'ep01', 'c3', 28.20, 0.13, 0.71, 'billy',  'Ой...'),
    ('c3b', 'ep01', 'c3', 29.10, 1.42, 1.99, 'billy',  'КАКТУС...'),
    ('s2',  'ep06', 's2', 30.30, 0.00, 2.07, 'sam',    'Он что... ВЫИГРАЛ?!'),
    ('n3',  'ep01', 'n3', 32.80, 0.15, 2.59, 'sam',    'Приятного аппетита, МЭМ.'),
    ('n4',  'ep01', 'n4', 35.50, 0.17, 0.76, 'molniya', 'СПАСИБО.'),
    ('b3',  'ep06', 'b3', 37.60, 0.00, 3.46, 'billy',  'Я же говорил... САМЫЙ быстрый.'),
    ('m2',  'ep06', 'm2', 41.40, 0.00, 3.47, 'molniya', 'Сезон два. Тариф — ТРИ.'),
]

SFX = [
    ('library/sfx/whoosh.mp3', 0.00, 0.6),
    ('library/sfx/horse_snort.mp3', 6.60, 0.5),
    ('library/sfx/cash_register.mp3', 6.80, 0.5),
    ('library/sfx/shop_bell.mp3', 14.20, 0.5),
    ('library/sfx/shop_bell.mp3', 14.60, 0.5),
    ('library/sfx/shop_bell.mp3', 15.00, 0.5),
    ('library/sfx/starter_pistol.mp3', 15.40, 0.9),
    ('library/sfx/horse_gallop.mp3', 15.50, 0.8),
    ('library/sfx/donkey_walk.mp3', 15.60, 0.6),
    ('library/sfx/horse_gallop.mp3', 17.50, 0.8),
    ('library/sfx/donkey_walk.mp3', 19.70, 0.5),
    ('library/sfx/horse_gallop.mp3', 22.00, 0.8),
    ('library/sfx/brake_skid.mp3', 24.95, 1.0),
    ('library/sfx/whoosh.mp3', 25.25, 0.7),
    ('library/sfx/ribbon_snap.mp3', 26.20, 0.9),
    ('series/pochti-dikiy-zapad/sfx/cactus_boing.mp3', 27.65, 1.0),
    ('library/sfx/donkey_walk.mp3', 29.80, 0.5),
    ('library/sfx/carrot_crunch.mp3', 33.30, 0.6),
    ('library/sfx/rope_yank.mp3', 35.90, 0.5),
    ('library/sfx/sack_coins_thud.mp3', 36.55, 1.0),
    ('library/sfx/cash_register.mp3', 36.90, 0.5),
    ('library/sfx/carrot_crunch.mp3', 44.95, 0.6),
]

# looped beds: (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/pochti-dikiy-zapad/music/theme_western_chiptune_16s.mp3', 14.6, 0.0, 15.5, 0.26, True),
    ('series/pochti-dikiy-zapad/music/finale_fanfare_15s.mp3', 14.9, 15.4, 30.2, 0.28, True),
    ('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 30.0, 37.6, 0.28, True),
    ('series/pochti-dikiy-zapad/music/finale_fanfare_15s.mp3', 14.9, 37.4, 47.0, 0.28, True),
    ('library/sfx/amb_desert_wind.mp3', 7.8, 0.0, 47.0, 0.7, False),
]
