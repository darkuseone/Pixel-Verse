"""S01E02 v2 «Талон на талон» (08.10.2026, по статистике TikTok) — timing for video (ep02.py) and audio (mix.py).
Voice clips are the tightened takes (voice/ep02_t)."""
DUR = 28.6
FPS = 30
SLUG = 'mazutych'
MASTER = 0.70

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('m0', 'ep02_t', 'm0', 0.00, 0.00, 1.69, 'maz', 'Премия — ТАЛОНОМ?!'),
    ('b1', 'ep02_t', 'b1', 1.85, 0.00, 3.14, 'boss', 'Заслужил! Только не ПЕЙ сразу.'),
    ('m2', 'ep02_t', 'm2', 5.05, 0.00, 2.15, 'maz', 'Посторонись! У меня ТАЛОН!'),
    ('w0', 'ep02_t', 'w0', 7.40, 0.00, 1.56, 'wheel', 'У всех ТАЛОН, друга.'),
    ('z1', 'ep02_t', 'z1', 9.10, 0.00, 1.82, 'zoya', 'Талоны ПРИНИМАЕМ.'),
    ('z2', 'ep02_t', 'z2', 10.97, 0.00, 0.89, 'zoya', 'По ЧЁТНЫМ.'),
    ('m3', 'ep02_t', 'm3', 12.00, 0.00, 0.98, 'maz', 'А СЕГОДНЯ?'),
    ('z3', 'ep02_t', 'z3', 13.05, 0.00, 1.26, 'zoya', 'НЕЧЁТНОЕ.'),
    ('m4', 'ep02_t', 'm4', 15.65, 0.00, 1.09, 'maz', 'ЧЁТНОЕ!'),
    ('z4', 'ep02_t', 'z4', 17.45, 0.00, 2.50, 'zoya', 'Вот. Талон НА ТАЛОН.'),
    ('m5', 'ep02_t', 'm5', 20.10, 0.00, 1.43, 'maz', 'А бензин КОГДА?'),
    ('z5', 'ep02_t', 'z5', 21.65, 0.00, 0.92, 'zoya', 'В ЧЕТВЕРГ.'),
    ('m6', 'ep02_t', 'm6', 22.70, 0.00, 1.16, 'maz', 'КАКОЙ?'),
    ('z6', 'ep02_t', 'z6', 24.00, 0.00, 0.89, 'zoya', 'ЧЁТНЫЙ.'),
    ('w1', 'ep02_t', 'w1', 25.30, 0.00, 1.73, 'wheel', 'Такого НЕТ, друга.'),
]

#        hook  boss  cross coupons zoya1  hope   zoya3  lapse  wake   STAMP  talon2 when   thurs  which  shutter wheel  loop
CUTS = [0.0, 1.80, 5.00, 7.25, 9.05, 11.95, 13.00, 14.45, 15.60, 16.80, 17.40, 20.00, 21.60, 22.65, 23.90, 25.20, 27.15, DUR]
TWIST = 16.80
NIGHT0, MIDNIGHT = 14.45, 15.60
STAMP_T = 16.85
SHUT_T = 24.20

S = 'library/sfx/'
SFX = [
    (S + 'record_scratch.mp3', 0.00, 0.5),
    (S + 'paper_unroll.mp3', 0.05, 0.6),
    (S + 'fist_slam_counter.mp3', 2.10, 0.5),
    (S + 'whoosh.mp3', 5.00, 0.5),
    (S + 'paper_crumple_slap.mp3', 7.45, 0.35),
    (S + 'paper_crumple_slap.mp3', 7.75, 0.35),
    (S + 'paper_crumple_slap.mp3', 8.05, 0.35),
    (S + 'car_honks_chorus.mp3', 7.60, 0.4),
    (S + 'fist_slam_counter.mp3', 9.10, 0.7),
    (S + 'gum_pop.mp3', 14.35, 0.7),
    (S + 'clock_fast_ticks.mp3', 14.45, 0.5),
    (S + 'snore.mp3', 14.55, 0.6),
    (S + 'clock_midnight_chime.mp3', 15.50, 0.55),
    (S + 'stamp.mp3', 16.85, 0.9),
    (S + 'paper_crumple_slap.mp3', 17.40, 0.5),
    (S + 'record_scratch.mp3', 20.00, 0.45),
    (S + 'gate_rolling.mp3', 24.15, 0.7),
    (S + 'bucket_clang.mp3', 24.70, 0.6),
    (S + 'sad_trombone.mp3', 26.30, 0.35),
    (S + 'choir_hallelujah_short.mp3', 27.15, 0.45),
    (S + 'paper_unroll.mp3', 27.30, 0.5),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('library/sfx/amb_refinery.mp3', 7.8, 0.0, 14.45, 0.40, False),
    ('library/sfx/amb_night_crickets.mp3', 6.8, 14.45, 27.15, 0.35, False),
    ('library/sfx/amb_refinery.mp3', 7.8, 27.15, DUR, 0.40, False),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 0.0, 14.45, 0.26, True),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 16.8, DUR, 0.22, True),
]

VFX = {'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25'}
VGAIN = {'maz': 1.6, 'zoya': 1.55, 'wheel': 1.45, 'boss': 1.5}
