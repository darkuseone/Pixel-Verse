"""S01E02 «Засада» (HD-пересборка на общем движке) — timing for video (ep02.py) and audio (mix.py).
Молния вместо старой реплики «Можно. А зачем?» (стоп-лист) говорит новую: movie/b2."""
DUR = 36.6
FPS = 30

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)   CAPS word = punch (speaker colour)
VOICE = [
    ('e1', 'ep02',  'b1', 0.00, 0.10, 2.45, 'billy',   'Тс-с. Я — КАКТУС.'),
    ('e2', 'ep02',  'b2', 2.50, 0.20, 6.00, 'billy',   'План гениальный: Сэм подъедет — а я его... ХВАТЬ!'),
    ('m1', 'movie', 'b2', 8.50, 0.10, 3.50, 'molniya', 'Кактус с человеческим ЛИЦОМ. Смело.'),
    ('e3', 'ep02',  'b3', 12.00, 0.10, 1.70, 'billy',  'Молния! ПРЯЧЬСЯ!'),
    ('m2', 'ep02',  'm2', 13.70, 0.10, 1.00, 'molniya', 'Спряталась.'),
    ('s1', 'ep02',  's1', 16.00, 0.05, 3.30, 'sam',    'Какой славный кактус... Присяду.'),
    ('b4', 'ep02',  'b4', 19.60, 0.25, 1.85, 'billy',  'Ммм-мф-ф-ф!'),
    ('s2', 'ep02',  's2', 21.40, 0.20, 1.80, 'sam',    'Хм. Тёплый.'),
    ('s3', 'ep02',  's3', 23.50, 0.10, 3.90, 'sam',    'Как договаривались, мэм. Морковь за неделю.'),
    ('n4', 'ep01',  'n4', 27.50, 0.12, 0.75, 'molniya', 'СПАСИБО.'),
    ('b5', 'ep02',  'b5', 30.20, 0.08, 4.60, 'billy',  'Засада сработала! Он меня даже не ЗАМЕТИЛ!'),
    ('m3', 'ep02',  'm3', 34.90, 0.05, 0.75, 'molniya', 'ВОЗДУХАН.'),
]

SFX = [
    ('library/sfx/wind_gust.mp3', 0.20, 0.5),
    ('library/sfx/horse_snort.mp3', 8.40, 0.5),
    ('library/sfx/boots_stomp.mp3', 12.20, 0.4),
    ('library/sfx/vulture.mp3', 14.90, 0.6),
    ('library/sfx/donkey_walk.mp3', 14.40, 0.5),
    ('library/sfx/donkey_bray.mp3', 17.80, 0.6),
    ('library/sfx/boots_stomp.mp3', 23.30, 0.5),
    ('series/pochti-dikiy-zapad/sfx/carrot_spill.mp3', 25.70, 0.9),
    ('library/sfx/donkey_walk.mp3', 29.70, 0.5),
    ('series/pochti-dikiy-zapad/sfx/costume_pop.mp3', 30.30, 1.0),
    ('library/sfx/carrot_crunch.mp3', 35.00, 0.6),
]

# looped beds: (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 0.0, 36.6, 0.28, True),
    ('library/sfx/amb_desert_wind.mp3', 7.8, 0.0, 36.6, 0.7, False),
]
