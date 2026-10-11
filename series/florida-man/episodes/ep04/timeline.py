"""S01E04 «Wind or Flood» — timing for video (ep04.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep04_t).
The «Flood.» takes came out as repeats («Flood. Flood. Flood» — checked once with STT): one word is cut out of each."""
DUR = 31.8
FPS = 30
SLUG = 'florida-man'
MASTER = 0.64

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('f1', 'ep04_t', 'f1', 0.00, 0.00, 2.38, 'fm', 'EIGHT GRAND?! For a TRAILER?!'),
    ('t1', 'ep04_t', 't1', 2.44, 0.00, 2.61, 'tanner', "Actually, we're leaving Florida! No worries!"),
    ('f2', 'ep04_t', 'f2', 5.12, 0.00, 2.85, 'fm', "Fine. I'll insure MYSELF."),
    ('f3', 'ep04_t', 'f3', 8.03, 0.00, 2.01, 'fm', 'Mort. Hold my sub.'),
    ('m1', 'ep04_t', 'm1', 10.10, 0.00, 1.67, 'mort', "Sub's not COVERED."),
    ('m2', 'ep04_t', 'm2', 13.00, 0.00, 2.06, 'mort', "Is it legal? It's CHEAPER."),
    ('f4', 'ep04_t', 'f4', 17.00, 0.00, 1.93, 'fm', 'Was it WIND, or FLOOD?'),
    ('f5', 'ep04_t', 'f5', 19.00, 1.38, 2.00, 'fm', 'Flood.'),
    ('f6', 'ep04_t', 'f6', 19.70, 0.00, 0.99, 'fm', 'DENIED!'),
    ('d1', 'ep04_t', 'd1', 21.55, 1.30, 1.82, 'darlene', 'Flood.'),
    ('d2', 'ep04_t', 'd2', 22.75, 0.00, 0.94, 'darlene', 'Noted.'),
    ('m3', 'ep04_t', 'm3', 23.75, 0.00, 2.51, 'mort', "Congrats. You're the bad guy NOW."),
    ('d3', 'ep04_t', 'd3', 27.65, 0.00, 2.53, 'darlene', 'EIGHT GRAND?! For a TRAILER?!'),
    ('f7', 'ep04_t', 'f7', 30.25, 0.00, 1.18, 'fm', 'No worries!'),
]

# shot boundaries (ep04.py)
CUTS = [0.0, 2.42, 5.10, 8.0, 10.08, 11.8, 12.95, 15.06, 15.9, 16.95, 18.95, 19.65, 20.72, 21.5, 23.72, 26.28, 27.6, 30.2, DUR]
TWIST = 16.95                                   # 16.95 / 31.8 = 53 %
STAMPS = [13.45, 14.0, 14.55, 19.95, 20.85, 21.2, 22.15]

S = 'library/sfx/'
SFX = [
    (S + 'paper_crumple_slap.mp3', 0.00, 0.8),
    (S + 'record_scratch.mp3', 0.02, 0.0),
    (S + 'cash_register.mp3', 0.15, 0.35),
    (S + 'tank_reverse_beeps.mp3', 2.45, 0.25),
    (S + 'old_car_start_roar.mp3', 5.10, 0.35),
    (S + 'truck_horn_old.mp3', 6.2, 0.3),
    (S + 'gator_gulp.mp3', 9.80, 0.8),
    (S + 'chair_scoot.mp3', 11.85, 0.4),
    (S + 'sack_coins_thud.mp3', 14.30, 0.5),
    (S + 'thunder_crack.mp3', 15.10, 0.45),
    (S + 'rain_heavy.mp3', 15.40, 0.35, 0.0, 3.5),
    (S + 'bath_splash.mp3', 16.10, 0.5),
    (S + 'record_scratch.mp3', 16.96, 0.5),
    (S + 'water_drip_single.mp3', 18.98, 0.6),
    (S + 'crowd_sigh.mp3', 20.75, 0.3),
    (S + 'hole_punch.mp3', 22.50, 0.9),
    (S + 'paper_unroll.mp3', 26.30, 0.4),
    (S + 'pencil_scribble.mp3', 26.40, 0.6),
    (S + 'news_breaking_sting.mp3', 26.62, 0.55),
    (S + 'record_scratch.mp3', 27.62, 0.4),
    (S + 'app_notify_ping.mp3', 30.30, 0.3),
] + [(S + 'stamp.mp3', s, 0.9) for s in STAMPS]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_florida_yard_soft.mp3', 7.9, 0.0, DUR, 0.32, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 0.0, 16.95, 0.24, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 18.9, DUR, 0.24, True),
]

VFX = {}
VGAIN = {'fm': 1.9, 'tanner': 1.45, 'mort': 1.7, 'darlene': 1.65}
