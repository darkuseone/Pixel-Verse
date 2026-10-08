"""S01E01 «Class 3» — timing for video (ep01.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep01_t)."""
DUR = 36.8
FPS = 30
SLUG = 'grim-ride'
MASTER = 0.70

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('g1', 'ep01_t', 'g1', 0.00, 0.00, 3.60, 'grim', 'Behold! DEATH, on a Class THREE!'),
    ('e1', 'ep01_t', 'e1', 3.66, 0.00, 1.91, 'edgar', 'Four easy PAYMENTS.'),
    ('t1', 'ep01_t', 't1', 6.30, 0.00, 2.95, 'todd', "Bro! Sick costume! Where's your FOG machine?"),
    ('g3', 'ep01_t', 'g3', 9.32, 0.00, 2.01, 'grim', 'I am DEATH!'),
    ('t2', 'ep01_t', 't2', 11.40, 0.00, 2.04, 'todd', 'Not even TWELVE feet, buddy.'),
    ('e2', 'ep01_t', 'e2', 13.50, 0.00, 1.20, 'edgar', 'Short KING.'),
    ('g4', 'ep01_t', 'g4', 14.80, 0.00, 3.13, 'grim', 'Harold. Your time is UP.'),
    ('h1', 'ep01_t', 'h1', 18.00, 0.00, 2.14, 'harold', 'Over my dead BODY.'),
    ('g5', 'ep01_t', 'g5', 20.20, 0.00, 1.57, 'grim', "That's the PLAN."),
    ('h2', 'ep01_t', 'h2', 22.05, 0.00, 3.34, 'harold', 'Catch me, BONES.'),
    ('g6', 'ep01_t', 'g6', 25.45, 0.00, 3.13, 'grim', "Slow DOWN! You're NINETY-SEVEN!"),
    ('k1', 'ep01_t', 'k1', 28.65, 0.00, 1.59, 'kayden', 'Relax, PAL.'),
    ('e3', 'ep01_t', 'e3', 30.32, 0.00, 2.19, 'edgar', 'Dead battery. IRONIC.'),
    ('g7', 'ep01_t', 'g7', 32.60, 0.00, 1.49, 'grim', 'He RATED me?'),
    ('h3', 'ep01_t', 'h3', 34.20, 0.00, 1.78, 'harold', 'Happy Halloween, KID!'),
]

# shot boundaries (ep01.py)
CUTS = [0.0, 1.75, 3.6, 5.57, 6.3, 8.1, 9.28, 11.36, 13.46, 14.75, 17.95, 20.16, 21.8, 23.7, 25.4, 28.6, 30.28, 32.55, 34.12, 36.0, DUR]
TWIST = 21.80                                   # 21.80 / 36.8 = 59 %

S = 'library/sfx/'
G = 'series/grim-ride/sfx/'
SFX = [
    (S + 'thunder_crack.mp3', 0.00, 0.55),
    (S + 'whoosh.mp3', 1.69, 0.45),
    (S + 'battery_die_beeps.mp3', 3.65, 0.30, 0.0, 0.5),
    (S + 'app_notify_ping.mp3', 5.62, 0.6),
    (S + 'brake_skid.mp3', 8.05, 0.45),
    (S + 'thunder_crack.mp3', 9.34, 0.6),
    (S + 'sad_trombone.mp3', 11.96, 0.35),
    (S + 'cloak_shimmer.mp3', 14.77, 0.4),
    (S + 'rocking_creak.mp3', 18.01, 0.55),
    (S + 'cloth_flap.mp3', 21.75, 0.7),
    (S + 'record_scratch.mp3', 21.77, 0.6),
    (G + 'etrike_rev.mp3', 22.04, 0.75),
    (S + 'crowd_gasp.mp3', 21.92, 0.25),
    (G + 'etrike_zoom.mp3', 23.70, 0.7),
    (G + 'raven_caw.mp3', 25.40, 0.35),
    (G + 'etrike_zoom.mp3', 28.60, 0.55),
    (S + 'battery_die_beeps.mp3', 30.28, 0.6),
    (S + 'piano_stop.mp3', 30.67, 0.35),
    (S + 'app_notify_ping.mp3', 32.55, 0.55),
    (S + 'sad_trombone.mp3', 33.64, 0.3),
    (G + 'etrike_zoom.mp3', 34.12, 0.6),
    (G + 'raisin_bonk.mp3', 35.17, 4.0),
    (S + 'thunder_crack.mp3', 36.05, 0.45),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_night_crickets.mp3', 6.9, 0.0, DUR, 0.45, False),
    (S + 'monowheel_whine.mp3', 3.8, 0.0, 14.7, 0.22, True),
    (S + 'monowheel_whine.mp3', 3.8, 23.7, 30.3, 0.22, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 0.0, 21.75, 0.26, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 23.7, DUR, 0.26, True),
]

VFX = {}
VGAIN = {'grim': 1.55, 'edgar': 1.6, 'todd': 1.5, 'harold': 1.6, 'kayden': 1.55}
