"""S01E04 «The Plug» — timing for video (ep04.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep04_t);
«Relax, pal.» is reused from the pilot (voice/ep01_t/k1)."""
DUR = 33.4
FPS = 30
SLUG = 'grim-ride'
MASTER = 0.74

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('g1', 'ep04_t', 'g1', 0.00, 0.00, 1.80, 'grim', "I'm looking for the PLUG."),
    ('k1', 'ep04_t', 'k1', 1.88, 0.00, 1.20, 'kayden', "Who's ASKING?"),
    ('g2', 'ep04_t', 'g2', 3.15, 0.00, 2.30, 'grim', 'I am DEATH.'),
    ('k1b', 'ep01_t', 'k1', 5.52, 0.00, 1.59, 'kayden', 'Relax, PAL.'),
    ('k2', 'ep04_t', 'k2', 7.20, 0.00, 2.17, 'kayden', "Nice costume. Where'd you COP it?"),
    ('g3', 'ep04_t', 'g3', 9.45, 0.00, 2.12, 'grim', "It's NOT a costume!"),
    ('k3', 'ep04_t', 'k3', 11.65, 0.00, 0.71, 'kayden', 'BET.'),
    ('g4', 'ep04_t', 'g4', 12.45, 0.00, 3.97, 'grim', "I need FORTY miles an hour. Harold's too FAST."),
    ('k4', 'ep04_t', 'k4', 16.50, 0.00, 1.65, 'kayden', "Harold's a CUSTOMER."),
    ('e1', 'ep04_t', 'e1', 18.55, 0.00, 2.09, 'edgar', 'Forty bucks. CASH.'),
    ('g5', 'ep04_t', 'g5', 20.72, 0.00, 0.89, 'grim', 'EDGAR?!'),
    ('e2', 'ep04_t', 'e2', 21.68, 0.00, 1.65, 'edgar', "A bird's gotta EAT."),
    ('g6', 'ep04_t', 'g6', 23.40, 0.00, 2.19, 'grim', 'You sold one to HAROLD?!'),
    ('e3', 'ep04_t', 'e3', 25.66, 0.00, 1.15, 'edgar', 'He TIPS.'),
    ('k5', 'ep04_t', 'k5', 26.90, 0.00, 1.28, 'kayden', 'Family DISCOUNT?'),
    ('e4', 'ep04_t', 'e4', 28.25, 0.00, 1.54, 'edgar', "He's not FAMILY."),
    ('e5', 'ep04_t', 'e5', 31.45, 0.00, 1.36, 'edgar', 'No REFUNDS.'),
]

CUTS = [0.0, 1.85, 3.10, 5.48, 7.15, 9.42, 11.62, 12.42, 14.40, 16.45, 18.25, 20.70, 21.65, 23.38, 25.62, 26.85, 28.22, 29.82, 30.50, 31.42,
        32.85, DUR]
TWIST = 18.25                                   # 18.25 / 33.4 = 55 %

S = 'library/sfx/'
G = 'series/grim-ride/sfx/'
SFX = [
    (G + 'etrike_rev.mp3', 0.00, 0.45),
    (S + 'heartbeat_slow.mp3', 0.10, 0.4),
    (S + 'neon_buzz_tense.mp3', 1.85, 0.3),
    (S + 'sad_trombone.mp3', 4.80, 0.25),
    (S + 'record_scratch.mp3', 9.42, 0.3),
    (S + 'battery_die_beeps.mp3', 14.45, 0.4),
    (S + 'pigeons_flap_burst.mp3', 18.10, 0.6),
    (G + 'raven_caw.mp3', 18.25, 0.6),
    (S + 'record_scratch.mp3', 18.22, 0.6),
    (S + 'plastic_bag_rustle.mp3', 18.80, 0.6),
    (S + 'cash_register.mp3', 20.00, 0.45),
    (S + 'crowd_gasp.mp3', 20.72, 0.3),
    (S + 'coin_clink.mp3', 26.00, 0.6),
    (S + 'seatbelt_click.mp3', 29.85, 0.8),
    (S + 'electric_zap_sparks.mp3', 30.00, 0.5),
    (G + 'etrike_rev.mp3', 30.45, 0.8),
    (S + 'whoosh.mp3', 30.55, 0.6),
    (G + 'raven_caw.mp3', 32.85, 0.3),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_night_crickets.mp3', 6.9, 0.0, DUR, 0.40, False),
    (S + 'monowheel_whine.mp3', 3.8, 0.0, 18.2, 0.16, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 0.0, 18.2, 0.24, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 18.6, DUR, 0.26, True),
]

VFX = {}
VGAIN = {'grim': 1.55, 'edgar': 1.6, 'kayden': 1.55}
