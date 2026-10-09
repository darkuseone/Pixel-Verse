"""S01E05 «Python Money» — timing for video (ep05.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep05_t);
f6 (whimper) +9 dB and f7 (zen) compressed +11 dB in voice/ep05_t so they sit with the rest."""
DUR = 32.6
FPS = 30
SLUG = 'florida-man'
MASTER = 0.60

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('f1', 'ep05_t', 'f1', 0.00, 0.00, 2.74, 'fm', 'THIRTY-FOUR HUNDRED?! For a SHED?!'),
    ('t1', 'ep05_t', 't1', 2.78, 0.00, 2.46, 'tanner', "It's a TINY HOME! Very trendy!"),
    ('f2', 'ep05_t', 'f2', 5.30, 0.00, 2.19, 'fm', 'Mort. Hold my sub.'),
    ('m1', 'ep05_t', 'm1', 7.55, 0.00, 1.88, 'mort', 'My fee is a THIRD.'),
    ('f3', 'ep05_t', 'f3', 10.55, 0.00, 1.46, 'fm', 'Easy, buddy.'),
    ('f4', 'ep05_t', 'f4', 12.06, 0.00, 1.46, 'fm', 'Not the SUB.'),
    ('t2', 'ep05_t', 't2', 14.25, 0.00, 2.17, 'tanner', 'Twenty feet! A THOUSAND bucks!'),
    ('f5', 'ep05_t', 'f5', 16.48, 0.00, 1.31, 'fm', 'RENT money!'),
    ('t3', 'ep05_t', 't3', 17.85, 0.00, 2.30, 'tanner', "You make python money now? Rent's UP!"),
    ('f6', 'ep05_t', 'f6', 20.22, 1.25, 2.56, 'fm', "That's MORE than I made."),
    ('m2', 'ep05_t', 'm2', 21.62, 0.00, 1.44, 'mort', 'And my THIRD.'),
    ('t4', 'ep05_t', 't4', 23.12, 0.00, 2.04, 'tanner', "Rented it! He's got better CREDIT."),
    ('f7', 'ep05_t', 'f7', 25.22, 0.00, 1.78, 'fm', 'Officer. Take me HOME.'),
    ('d1', 'ep05_t', 'd1', 28.20, 0.00, 2.04, 'darlene', "One more. Then it's FREE."),
]

# shot boundaries (ep05.py)
CUTS = [0.0, 2.76, 5.28, 7.52, 9.45, 10.52, 12.04, 12.9, 13.55, 14.22, 16.45, 17.82, 20.2, 21.6, 23.1, 25.2, 27.05, 28.18, 30.3, DUR]
TWIST = 17.82                                   # 17.82 / 32.6 = 55 %

S = 'library/sfx/'
SFX = [
    (S + 'paper_crumple_slap.mp3', 0.00, 0.9),
    (S + 'record_scratch.mp3', 0.02, 0.0),
    (S + 'cash_register.mp3', 0.18, 0.35),
    (S + 'app_notify_ping.mp3', 2.82, 0.3),
    (S + 'paper_unroll.mp3', 5.30, 0.35),
    (S + 'gator_gulp.mp3', 7.10, 0.6),
    (S + 'coin_clink.mp3', 8.70, 0.5),
    (S + 'airboat_roar.mp3', 9.45, 0.55),
    (S + 'pond_bloop.mp3', 10.50, 0.6),
    (S + 'python_hiss.mp3', 10.70, 0.6),
    (S + 'gator_gulp.mp3', 12.75, 0.8),
    (S + 'debris_crash.mp3', 13.55, 0.5),
    (S + 'cartoon_boom_big.mp3', 13.60, 0.35),
    (S + 'python_hiss.mp3', 14.05, 0.45),
    (S + 'sack_coins_thud.mp3', 15.40, 0.5),
    (S + 'cash_register.mp3', 16.20, 0.45),
    (S + 'record_scratch.mp3', 17.83, 0.5),
    (S + 'cloth_flap.mp3', 17.85, 0.6),
    (S + 'paper_crumple_slap.mp3', 19.40, 0.9),
    (S + 'sad_trombone.mp3', 20.40, 0.2),
    (S + 'coin_clink.mp3', 21.70, 0.6),
    (S + 'python_hiss.mp3', 23.20, 0.35),
    (S + 'pencil_scribble.mp3', 24.00, 0.45),
    (S + 'handcuffs_click.mp3', 26.60, 0.8),
    (S + 'camera_flash.mp3', 27.05, 0.8),
    (S + 'news_breaking_sting.mp3', 27.07, 0.55),
    (S + 'hole_punch.mp3', 28.45, 0.9),
    (S + 'paper_crumple_slap.mp3', 30.45, 0.9),
    (S + 'python_hiss.mp3', 30.95, 0.9),
    (S + 'record_scratch.mp3', 31.0, 0.35),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_florida_yard_soft.mp3', 7.9, 0.0, 9.45, 0.3, True),
    (S + 'amb_night_crickets.mp3', 7.9, 9.45, 17.8, 0.25, True),
    (S + 'amb_florida_yard_soft.mp3', 7.9, 17.8, DUR, 0.3, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 0.0, 17.82, 0.24, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 19.7, DUR, 0.24, True),
]

VFX = {}
VGAIN = {'fm': 1.9, 'tanner': 1.45, 'mort': 1.7, 'darlene': 1.65}
