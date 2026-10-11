"""S01E02 «Grand Theft Sub» — timing for video (ep02.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep02_t).
Darlene's «Mornin', Travis.» is split around the name: the store PA «DING-DONG» covers it (running gag: his name is never heard)."""
DUR = 31.2
FPS = 30
SLUG = 'florida-man'
MASTER = 0.64

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('f1', 'ep02_t', 'f1', 0.00, 0.00, 2.59, 'fm', 'FIFTEEN BUCKS?! For a SUB?!'),
    ('t1', 'ep02_t', 't1', 2.66, 0.00, 2.46, 'tanner', 'Fourteen ninety-NINE. Totally different!'),
    ('f2', 'ep02_t', 'f2', 5.16, 0.00, 3.08, 'fm', 'Mort. Hold my—'),
    ('m1', 'ep02_t', 'm1', 8.30, 0.00, 2.85, 'mort', 'No sub. This is an EMERGENCY.'),
    ('f3', 'ep02_t', 'f3', 11.20, 0.00, 3.32, 'fm', "Nine-one-one? I'd like to report a ROBBERY."),
    ('d1a', 'ep02_t', 'd1', 14.58, 0.00, 0.48, 'darlene', "Mornin'—"),
    ('d1b', 'ep02_t', 'd1', 15.58, 1.38, 2.95, 'darlene', "Prices aren't a CRIME."),
    ('d2', 'ep02_t', 'd2', 17.56, 0.00, 1.33, 'darlene', "Hands where I can SEE 'em!"),
    ('t2', 'ep02_t', 't2', 18.95, 0.00, 1.52, 'tanner', "That's Pubbix PROPERTY!"),
    ('d3', 'ep02_t', 'd3', 20.52, 0.00, 1.46, 'darlene', "So's my PAYCHECK."),
    ('m2', 'ep02_t', 'm2', 22.03, 0.00, 2.90, 'mort', "I'm representing the price now. Pays BETTER."),
    ('t3', 'ep02_t', 't3', 26.66, 0.00, 2.09, 'tanner', 'New price! Covers legal FEES!'),
    ('f4', 'ep02_t', 'f4', 28.86, 0.00, 1.96, 'fm', 'Nine-one-one? Me again.'),
]

# shot boundaries (ep02.py)
CUTS = [0.0, 2.62, 5.12, 6.95, 8.26, 11.15, 12.75, 15.55, 16.75, 17.2, 17.55, 18.93, 20.5, 22.0, 24.98, 26.62, 28.8, DUR]
TWIST = 17.55                                   # 17.55 / 31.2 = 56 %

S = 'library/sfx/'
SFX = [
    (S + 'glass_slide.mp3', 0.00, 0.8),
    (S + 'record_scratch.mp3', 0.02, 0.0),
    (S + 'cash_register.mp3', 0.12, 0.4),
    (S + 'register_keys.mp3', 2.68, 0.35),
    (S + 'whoosh.mp3', 5.10, 0.25, 0.0, 0.8),
    (S + 'counter_blip.mp3', 5.40, 0.4),
    (S + 'sad_trombone.mp3', 7.05, 0.22),
    (S + 'counter_blip.mp3', 8.30, 0.45),
    (S + 'flip_phone.mp3', 11.10, 0.6),
    (S + 'slowmo_whoosh.mp3', 14.52, 0.3),
    (S + 'pa_chime_feedback.mp3', 15.02, 0.75, 0.0, 1.3),
    (S + 'neon_buzz_tense.mp3', 16.75, 0.25, 0.0, 0.5),
    (S + 'pushpin_pop.mp3', 17.40, 0.7),
    (S + 'siren_whoop.mp3', 17.52, 0.55),
    (S + 'record_scratch.mp3', 17.55, 0.5),
    (S + 'handcuffs_click.mp3', 17.95, 1.0),
    (S + 'crowd_gasp.mp3', 18.95, 0.3),
    (S + 'fist_slam_counter.mp3', 20.52, 0.6),
    (S + 'coin_clink.mp3', 23.30, 0.5),
    (S + 'cash_register.mp3', 24.45, 0.35),
    (S + 'camera_flash.mp3', 24.98, 0.8),
    (S + 'news_breaking_sting.mp3', 25.00, 0.55),
    (S + 'camera_flash.mp3', 25.80, 0.7),
    (S + 'hole_punch.mp3', 26.15, 0.9),
    (S + 'pushpin_pop.mp3', 27.10, 0.7),
    (S + 'cash_register.mp3', 28.20, 0.4),
    (S + 'flip_phone.mp3', 28.78, 0.6),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_grocery_store.mp3', 7.9, 0.0, DUR, 0.7, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 0.0, 17.50, 0.24, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 18.9, DUR, 0.24, True),
]

VFX = {}
VGAIN = {'fm': 1.9, 'tanner': 1.45, 'mort': 1.7, 'darlene': 1.65}
