"""S01E01 «Class 3» — timing for video (ep01.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep01_t)."""
DUR = 34.5
FPS = 30
SLUG = 'grim-ride'
MASTER = 0.70

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('g1', 'ep01_t', 'g1', 0.00, 0.00, 3.08, 'grim', 'Behold! DEATH, on a Class THREE!'),
    ('e1', 'ep01_t', 'e1', 3.10, 0.00, 1.70, 'edgar', 'Four easy PAYMENTS.'),
    ('t1', 'ep01_t', 't1', 5.70, 0.00, 3.29, 'todd', "Bro! Sick costume! Where's your FOG machine?"),
    ('g3', 'ep01_t', 'g3', 9.05, 0.00, 1.54, 'grim', 'I am DEATH!'),
    ('t2', 'ep01_t', 't2', 10.68, 0.00, 1.93, 'todd', 'Not even TWELVE feet, buddy.'),
    ('e2', 'ep01_t', 'e2', 12.70, 0.00, 1.12, 'edgar', 'Short KING.'),
    ('g4', 'ep01_t', 'g4', 13.92, 0.00, 2.82, 'grim', 'Harold. Your time is UP.'),
    ('h1', 'ep01_t', 'h1', 16.80, 0.00, 1.91, 'harold', 'Over my dead BODY.'),
    ('g5', 'ep01_t', 'g5', 18.75, 0.00, 1.75, 'grim', "That's the PLAN."),
    ('h2', 'ep01_t', 'h2', 20.75, 0.00, 2.72, 'harold', 'Catch me, BONES.'),
    ('g6', 'ep01_t', 'g6', 23.55, 0.00, 2.43, 'grim', "Slow DOWN! You're NINETY-SEVEN!"),
    ('k1', 'ep01_t', 'k1', 26.05, 0.00, 1.57, 'kayden', 'Relax, PAL.'),
    ('e3', 'ep01_t', 'e3', 27.75, 0.00, 2.25, 'edgar', 'Dead battery. IRONIC.'),
    ('g7', 'ep01_t', 'g7', 30.10, 0.00, 1.33, 'grim', 'He RATED me?'),
    ('h3', 'ep01_t', 'h3', 31.75, 0.00, 1.78, 'harold', 'Happy Halloween, KID!'),
]

# shot boundaries (ep01.py)
CUTS = [0.0, 1.55, 3.05, 4.85, 5.60, 7.45, 9.00, 10.62, 12.66, 13.88, 16.75, 18.72, 20.35, 21.95, 23.50, 25.95, 27.70, 30.05, 31.70,
        33.70, DUR]
TWIST = 20.35                                   # 20.35 / 34.5 = 59 %

S = 'library/sfx/'
G = 'series/grim-ride/sfx/'
SFX = [
    (S + 'thunder_crack.mp3', 0.00, 0.55),
    (S + 'whoosh.mp3', 1.50, 0.45),
    (S + 'battery_die_beeps.mp3', 3.10, 0.30, 0.0, 0.5),
    (S + 'app_notify_ping.mp3', 4.90, 0.6),
    (S + 'brake_skid.mp3', 7.40, 0.45),
    (S + 'thunder_crack.mp3', 9.05, 0.6),
    (S + 'sad_trombone.mp3', 11.20, 0.35),
    (S + 'cloak_shimmer.mp3', 13.90, 0.4),
    (S + 'rocking_creak.mp3', 16.80, 0.55),
    (S + 'cloth_flap.mp3', 20.30, 0.7),
    (S + 'record_scratch.mp3', 20.32, 0.6),
    (G + 'etrike_rev.mp3', 20.55, 0.75),
    (S + 'crowd_gasp.mp3', 20.45, 0.25),
    (G + 'etrike_zoom.mp3', 21.95, 0.7),
    (G + 'raven_caw.mp3', 23.50, 0.35),
    (G + 'etrike_zoom.mp3', 25.95, 0.55),
    (S + 'battery_die_beeps.mp3', 27.70, 0.6),
    (S + 'piano_stop.mp3', 28.10, 0.35),
    (S + 'app_notify_ping.mp3', 30.05, 0.55),
    (S + 'sad_trombone.mp3', 31.20, 0.3),
    (G + 'etrike_zoom.mp3', 31.70, 0.6),
    (G + 'raisin_bonk.mp3', 32.75, 4.0),
    (S + 'thunder_crack.mp3', 33.75, 0.45),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_night_crickets.mp3', 6.9, 0.0, DUR, 0.45, False),
    (S + 'monowheel_whine.mp3', 3.8, 0.0, 13.9, 0.22, True),
    (S + 'monowheel_whine.mp3', 3.8, 21.9, 27.9, 0.22, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 0.0, 20.3, 0.26, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 21.9, DUR, 0.26, True),
]

VFX = {}
VGAIN = {'grim': 1.55, 'edgar': 1.6, 'todd': 1.5, 'harold': 1.6, 'kayden': 1.55}
