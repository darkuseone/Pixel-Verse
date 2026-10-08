"""S01E01 «Кто крайний?» (v3, 09.10.2026: крик-хук «ГДЕ БЕНЗИН?!», поворот 17,4 с, 30,2 с) — timing for video (ep01.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep01_t)."""
DUR = 30.2
FPS = 30
SLUG = 'mazutych'
MASTER = 0.68

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('m0', 'ep01_t', 'm0', 0.00, 0.00, 1.60, 'maz', 'Где БЕНЗИН?!'),
    ('w1', 'ep01_t', 'w1', 1.70, 0.00, 1.84, 'wheel', 'Ты тащить ТОННА, друга!'),
    ('z1', 'ep01_t', 'z1', 5.45, 0.00, 2.20, 'zoya', 'Бензина НЕТ.'),
    ('m2', 'ep01_t', 'm2', 7.75, 0.00, 1.83, 'maz', 'Я — НЕФТЯНИК!'),
    ('z2', 'ep01_t', 'z2', 9.70, 0.00, 1.82, 'zoya', 'А я — БАЛЕРИНА.'),
    ('z3', 'ep01_t', 'z3', 11.65, 0.00, 2.45, 'zoya', 'Вот ТАМ и заправляйтесь.'),
    ('bz', 'ep01_t', 'bz', 14.75, 0.00, 1.32, 'maz', 'БЕНЗОВОЗ...'),
    ('d1', 'ep01_t', 'd1', 17.45, 0.00, 1.86, 'tolik', 'Мужики, кто КРАЙНИЙ?'),
    ('d2', 'ep01_t', 'd2', 20.45, 0.00, 2.41, 'tolik', 'ПУСТОЙ. С весны не заправлялся.'),
    ('w2', 'ep01_t', 'w2', 23.00, 0.00, 2.73, 'wheel', 'Заряд НОЛЬ процент. Пока, друга.'),
    ('d3', 'ep01_t', 'd3', 25.90, 0.00, 2.03, 'tolik', 'А я его ВОЖУ.'),
    ('z2b', 'ep01_t', 'z2', 28.05, 0.00, 1.82, 'zoyam', 'А я — БАЛЕРИНА.'),
]

# shot boundaries (ep01.py)
#        hook  reveal queue sign  nogas badge ballet point flare awe    arrive TWIST  react  knock  battery haul  callback
CUTS = [0.0, 1.65, 3.55, 4.70, 5.35, 7.70, 9.65, 11.60, 14.10, 14.70, 16.10, 17.40, 19.35, 20.40, 22.95, 25.85, 28.00, DUR]

S = 'library/sfx/'
SFX = [
    (S + 'rope_strain_creak.mp3', 0.00, 0.55),
    (S + 'whoosh.mp3', 1.62, 0.5),
    (S + 'car_honks_chorus.mp3', 3.60, 0.5),
    (S + 'fist_slam_counter.mp3', 7.80, 0.7),
    (S + 'gum_pop.mp3', 11.55, 0.6),
    (S + 'truck_horn_old.mp3', 14.15, 0.45),
    (S + 'choir_hallelujah_short.mp3', 14.72, 0.55),
    (S + 'truck_horn_old.mp3', 16.15, 0.8),
    (S + 'car_honks_chorus.mp3', 16.30, 0.5),
    (S + 'crowd_cheer_short.mp3', 16.35, 0.45),
    (S + 'brake_skid.mp3', 17.00, 0.5),
    (S + 'record_scratch.mp3', 19.33, 0.75),
    (S + 'sad_trombone.mp3', 19.50, 0.55),
    (S + 'tank_knock_hollow.mp3', 20.55, 0.9),
    (S + 'battery_die_beeps.mp3', 23.00, 0.45, 0.0, 0.9),
    (S + 'battery_die_beeps.mp3', 25.55, 0.75),
    (S + 'rope_strain_creak.mp3', 25.90, 0.5),
    (S + 'rope_strain_creak.mp3', 27.30, 0.4),
    (S + 'pa_chime_feedback.mp3', 27.90, 0.35, 0.0, 0.4),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('library/sfx/amb_refinery.mp3', 7.8, 0.0, DUR, 0.5, False),
    ('library/sfx/monowheel_whine.mp3', 3.8, 0.0, 25.7, 0.28, True),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 0.0, 19.33, 0.26, True),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 25.85, DUR, 0.24, True),
]

MEGA = 'highpass=f=420,lowpass=f=3600,acompressor=threshold=0.25:ratio=4,volume=1.3'
VFX = {'zoyam': MEGA, 'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25'}
VGAIN = {'maz': 1.6, 'zoya': 1.55, 'zoyam': 1.55, 'wheel': 1.45, 'tolik': 1.5}
