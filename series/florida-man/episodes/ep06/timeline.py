"""S01E06 «Jail & Resort» (season finale) — timing for video (ep06.py) and audio (mix.py). Voice clips are the tightened takes
(voice/ep06_t; d2 and f3 sped up x1.1 there). The season loop reuses the E01 hook take («NINE GRAND?! For the A/C?!», voice/ep01_t/f1)."""
DUR = 34.1
FPS = 30
SLUG = 'florida-man'
MASTER = 0.70

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('f1', 'ep06_t', 'f1', 0.00, 0.00, 1.85, 'fm', "Jail's CHEAPER than RENT!"),
    ('d1', 'ep06_t', 'd1', 1.90, 0.00, 1.62, 'darlene', "You're breaking IN?!"),
    ('f2', 'ep06_t', 'f2', 3.57, 0.00, 1.10, 'fm', "Checkin' in."),
    ('d2', 'ep06_t', 'd2', 4.72, 0.00, 3.79, 'darlene', 'Ten. Free night. Whoopee.'),
    ('f3', 'ep06_t', 'f3', 8.56, 0.00, 3.92, 'fm', 'Free A/C. Free food. NO premium.'),
    ('m1', 'ep06_t', 'm1', 12.53, 0.00, 1.72, 'mort', "I'm FULL."),
    ('t1', 'ep06_t', 't1', 14.30, 0.00, 3.12, 'tanner', 'Welcome to Sunshine County JAIL! Under new management!'),
    ('t2', 'ep06_t', 't2', 17.47, 0.00, 2.82, 'tanner', "Night's free! Plus a forty-nine dollar RESORT fee!"),
    ('f4', 'ep06_t', 'f4', 20.34, 0.00, 1.10, 'fm', "It's a JAIL."),
    ('t3', 'ep06_t', 't3', 21.49, 0.00, 1.31, 'tanner', 'Jail-and-RESORT!'),
    ('t4', 'ep06_t', 't4', 22.85, 0.00, 2.60, 'tanner', "Towel's ten. Mint's five. Pillow's a SUBSCRIPTION."),
    ('t5', 'ep06_t', 't5', 25.52, 0.00, 2.09, 'tanner', "Oh! A/C's extra. Nine GRAND."),
    ('f1x', 'ep01_t', 'f1', 27.68, 0.00, 2.61, 'fm', 'NINE GRAND?! For the A/C?!'),
    ('m2', 'ep06_t', 'm2', 30.36, 0.00, 2.28, 'mort', 'My client pleads. FLORIDA.'),
]

# shot boundaries (ep06.py)
CUTS = [0.0, 1.88, 3.55, 4.70, 6.40, 8.53, 10.55, 12.50, 14.27, 15.80, 17.45, 20.32, 21.47, 22.83, 25.48, 26.5, 27.65, 30.33, 32.66, DUR]
TWIST = 17.45                                   # 17.45 / 34.1 = 51 %

S = 'library/sfx/'
SFX = [
    (S + 'fence_rattle.mp3', 0.00, 0.8),
    (S + 'siren_whoop.mp3', 0.05, 0.45),
    (S + 'record_scratch.mp3', 0.02, 0.0),
    (S + 'pa_chime_feedback.mp3', 1.86, 0.35, 1.2, 2.0),
    (S + 'flipflop_stomp.mp3', 4.20, 0.6),
    (S + 'fist_slam_counter.mp3', 4.95, 0.6),
    (S + 'shop_bell.mp3', 5.70, 0.4),
    (S + 'hole_punch.mp3', 6.55, 0.9),
    (S + 'brass_fanfare_short.mp3', 6.60, 0.35),
    (S + 'coin_clink.mp3', 6.62, 0.6),
    (S + 'crowd_cheer_short.mp3', 6.70, 0.18),
    (S + 'choir_hallelujah_short.mp3', 8.58, 0.25),
    (S + 'book_thud.mp3', 10.75, 0.7),
    (S + 'bean_splat_slide.mp3', 13.65, 0.6),
    (S + 'paper_crumple_slap.mp3', 13.95, 0.5),
    (S + 'cell_door_clang.mp3', 14.28, 0.5),
    (S + 'record_scratch.mp3', 17.46, 0.5),
    (S + 'cash_register.mp3', 18.65, 0.5),
    (S + 'vhs_rewind.mp3', 18.70, 0.25),
    (S + 'ui_tap_chirp.mp3', 21.50, 0.4),
    (S + 'counter_blip.mp3', 23.05, 0.4),
    (S + 'counter_blip.mp3', 23.75, 0.4),
    (S + 'counter_blip.mp3', 24.45, 0.4),
    (S + 'ac_compressor_die.mp3', 25.30, 0.75),
    (S + 'record_scratch.mp3', 27.66, 0.0),
    (S + 'cash_register.mp3', 27.80, 0.35),
    (S + 'gavel_bang.mp3', 32.15, 0.7),
    (S + 'seagull.mp3', 32.70, 0.45),
    (S + 'brass_fanfare_short.mp3', 32.75, 0.3),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_night_crickets.mp3', 7.9, 0.0, 4.70, 0.35, True),
    (S + 'amb_office_night.mp3', 7.9, 4.70, 32.66, 0.45, True),
    (S + 'amb_night_crickets.mp3', 7.9, 32.66, DUR, 0.35, False),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 0.0, 17.45, 0.24, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 19.0, 27.6, 0.24, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 30.3, DUR, 0.3, True),
]

VFX = {}
VGAIN = {'fm': 1.9, 'tanner': 1.45, 'mort': 1.7, 'darlene': 1.65}
