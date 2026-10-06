"""S01E01 «Кто крайний?» (v2) — timing for video (ep01.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep01_t)."""
DUR = 34.8
FPS = 30
SLUG = 'mazutych'
MASTER = 0.68

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('m1', 'ep01_t', 'm1', 0.00, 0.00, 3.79, 'maz', 'Терпи, ласточка! Щас ЗАПРАВИМСЯ!'),
    ('w1', 'ep01_t', 'w1', 3.95, 0.00, 1.84, 'wheel', 'Ты тащить ТОННА, друга!'),
    ('z1', 'ep01_t', 'z1', 6.95, 0.00, 2.20, 'zoya', 'Бензина НЕТ.'),
    ('m2', 'ep01_t', 'm2', 9.30, 0.00, 1.83, 'maz', 'Я — НЕФТЯНИК!'),
    ('z2', 'ep01_t', 'z2', 11.30, 0.00, 1.82, 'zoya', 'А я — БАЛЕРИНА.'),
    ('z3', 'ep01_t', 'z3', 13.30, 0.00, 2.45, 'zoya', 'Вот ТАМ и заправляйтесь.'),
    ('bz', 'ep01_t', 'bz', 16.60, 0.00, 1.32, 'maz', 'БЕНЗОВОЗ...'),
    ('d1', 'ep01_t', 'd1', 19.50, 0.00, 1.86, 'tolik', 'Мужики, кто КРАЙНИЙ?'),
    ('d2', 'ep01_t', 'd2', 23.20, 0.00, 2.41, 'tolik', 'ПУСТОЙ. С весны не заправлялся.'),
    ('w2', 'ep01_t', 'w2', 25.75, 0.00, 2.73, 'wheel', 'Заряд НОЛЬ процент. Пока, друга.'),
    ('d3', 'ep01_t', 'd3', 29.60, 0.00, 2.03, 'tolik', 'А я его ВОЖУ.'),
    ('z2b', 'ep01_t', 'z2', 32.30, 0.00, 1.82, 'zoyam', 'А я — БАЛЕРИНА.'),
]

# shot boundaries (ep01.py)
CUTS = [0.0, 1.70, 4.60, 6.10, 6.90, 9.25, 11.25, 13.25, 15.85, 16.45, 18.00, 19.40, 21.50, 22.60, 25.65, 28.50, 32.20, DUR]

S = 'library/sfx/'
SFX = [
    (S + 'rope_strain_creak.mp3', 0.00, 0.55),
    (S + 'whoosh.mp3', 1.65, 0.5),
    (S + 'car_honks_chorus.mp3', 4.70, 0.5),
    (S + 'fist_slam_counter.mp3', 9.32, 0.7),
    (S + 'gum_pop.mp3', 13.05, 0.6),
    (S + 'truck_horn_old.mp3', 16.05, 0.45),
    (S + 'choir_hallelujah_short.mp3', 16.45, 0.55),
    (S + 'truck_horn_old.mp3', 18.05, 0.8),
    (S + 'car_honks_chorus.mp3', 18.25, 0.5),
    (S + 'crowd_cheer_short.mp3', 18.30, 0.45),
    (S + 'brake_skid.mp3', 19.05, 0.5),
    (S + 'record_scratch.mp3', 21.42, 0.75),
    (S + 'sad_trombone.mp3', 21.60, 0.55),
    (S + 'tank_knock_hollow.mp3', 22.75, 0.9),
    (S + 'battery_die_beeps.mp3', 25.70, 0.45, 0.0, 0.9),
    (S + 'battery_die_beeps.mp3', 28.15, 0.75),
    (S + 'rope_strain_creak.mp3', 28.55, 0.5),
    (S + 'rope_strain_creak.mp3', 31.20, 0.4),
    (S + 'pa_chime_feedback.mp3', 32.05, 0.35, 0.0, 0.4),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('library/sfx/amb_refinery.mp3', 7.8, 0.0, DUR, 0.5, False),
    ('library/sfx/monowheel_whine.mp3', 3.8, 0.0, 28.3, 0.28, True),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 0.0, 21.45, 0.26, True),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 28.5, DUR, 0.24, True),
]

MEGA = 'highpass=f=420,lowpass=f=3600,acompressor=threshold=0.25:ratio=4,volume=1.3'
VFX = {'zoyam': MEGA, 'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25'}
VGAIN = {'maz': 1.6, 'zoya': 1.55, 'zoyam': 1.55, 'wheel': 1.45, 'tolik': 1.5}
