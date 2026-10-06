"""S01E02 «Талон на талон» — timing for video (ep02.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep02_t)."""
DUR = 31.6
FPS = 30
SLUG = 'mazutych'
MASTER = 0.68

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('m1', 'ep02_t', 'm1', 0.00, 0.00, 3.10, 'maz', 'Премия! Талон на ДЕСЯТЬ литров!'),
    ('b1', 'ep02_t', 'b1', 3.30, 0.00, 3.14, 'boss', 'Заслужил! Только не ПЕЙ сразу.'),
    ('m2', 'ep02_t', 'm2', 6.75, 0.00, 2.15, 'maz', 'Посторонись! У меня ТАЛОН!'),
    ('z1', 'ep02_t', 'z1', 9.95, 0.00, 1.82, 'zoya', 'Талоны ПРИНИМАЕМ.'),
    ('z2', 'ep02_t', 'z2', 11.95, 0.00, 0.89, 'zoya', 'По ЧЁТНЫМ.'),
    ('m3', 'ep02_t', 'm3', 13.00, 0.00, 0.98, 'maz', 'А СЕГОДНЯ?'),
    ('z3', 'ep02_t', 'z3', 14.10, 0.00, 1.26, 'zoya', 'НЕЧЁТНОЕ.'),
    ('m4', 'ep02_t', 'm4', 17.30, 0.00, 1.09, 'maz', 'ЧЁТНОЕ!'),
    ('z4', 'ep02_t', 'z4', 19.15, 0.00, 2.50, 'zoya', 'Вот. Талон НА ТАЛОН.'),
    ('m5', 'ep02_t', 'm5', 21.85, 0.00, 1.43, 'maz', 'А бензин КОГДА?'),
    ('z5', 'ep02_t', 'z5', 23.40, 0.00, 0.92, 'zoya', 'В ЧЕТВЕРГ.'),
    ('m6', 'ep02_t', 'm6', 24.55, 0.00, 1.16, 'maz', 'КАКОЙ?'),
    ('z6', 'ep02_t', 'z6', 25.95, 0.00, 0.89, 'zoya', 'ЧЁТНЫЙ.'),
    ('w1', 'ep02_t', 'w1', 27.60, 0.00, 1.73, 'wheel', 'Такого НЕТ, друга.'),
]

CUTS = [0.0, 3.20, 6.60, 9.00, 9.85, 12.90, 14.05, 15.60, 17.20, 18.45, 19.10, 21.75, 23.35, 24.45, 25.85, 27.40, 29.60, DUR]

S = 'library/sfx/'
SFX = [
    (S + 'choir_hallelujah_short.mp3', 0.00, 0.5),
    (S + 'paper_unroll.mp3', 0.05, 0.6),
    (S + 'fist_slam_counter.mp3', 3.55, 0.5),
    (S + 'whoosh.mp3', 6.55, 0.5),
    (S + 'car_honks_chorus.mp3', 7.40, 0.45),
    (S + 'fist_slam_counter.mp3', 9.10, 0.8),
    (S + 'gum_pop.mp3', 15.45, 0.7),
    (S + 'clock_fast_ticks.mp3', 15.65, 0.5),
    (S + 'snore.mp3', 15.90, 0.6),
    (S + 'clock_midnight_chime.mp3', 17.15, 0.55),
    (S + 'stamp.mp3', 18.52, 0.9),
    (S + 'paper_crumple_slap.mp3', 19.10, 0.5),
    (S + 'record_scratch.mp3', 21.70, 0.55),
    (S + 'gate_rolling.mp3', 26.40, 0.7),
    (S + 'bucket_clang.mp3', 26.95, 0.6),
    (S + 'sad_trombone.mp3', 29.70, 0.45),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('library/sfx/amb_refinery.mp3', 7.8, 0.0, 15.6, 0.45, False),
    ('library/sfx/amb_night_crickets.mp3', 6.8, 15.6, DUR, 0.35, False),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 0.0, 15.6, 0.26, True),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 18.4, DUR, 0.22, True),
]

VFX = {'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25'}
VGAIN = {'maz': 1.6, 'zoya': 1.55, 'wheel': 1.45, 'boss': 1.5}
