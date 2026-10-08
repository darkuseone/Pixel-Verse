"""S01E03 «Full Size» — timing for video (ep03.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep03_t);
«Catch me, BONES.» is reused from the pilot (voice/ep01_t/h2)."""
DUR = 31.1
FPS = 30
SLUG = 'grim-ride'
MASTER = 0.74

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('g1', 'ep03_t', 'g1', 0.00, 0.00, 3.68, 'grim', 'Full-size bars. He HAS to open the door.'),
    ('t1', 'ep03_t', 't1', 3.75, 0.00, 2.64, 'todd', 'One each, buddy. Seventeen bucks a BAG!'),
    ('e1', 'ep03_t', 'e1', 6.45, 0.00, 1.07, 'edgar', 'INFLATION.'),
    ('m1', 'ep03_t', 'm1', 7.60, 0.00, 2.35, 'mom', "Aren't you a little OLD for this?"),
    ('g2', 'ep03_t', 'g2', 10.02, 0.00, 3.34, 'grim', "I am DEATH! I'm four THOUSAND!"),
    ('m2', 'ep03_t', 'm2', 13.42, 0.00, 1.52, 'mom', "Then that's a NO."),
    ('e2', 'ep03_t', 'e2', 15.00, 0.00, 0.89, 'edgar', 'CARDED.'),
    ('k1', 'ep03_t', 'k1', 15.95, 0.00, 1.54, 'kayden', 'Relax, PAL.'),
    ('h1', 'ep03_t', 'h1', 18.65, 0.00, 1.75, 'harold', "That's full size NOW."),
    ('h2', 'ep01_t', 'h2', 21.45, 0.00, 3.34, 'harold', 'Catch me, BONES.'),
    ('k2', 'ep03_t', 'k2', 24.90, 0.00, 2.85, 'kayden', 'Bro. Did YOU kill full-size?'),
    ('g3', 'ep03_t', 'g3', 27.85, 0.00, 1.72, 'grim', "I didn't do THIS one."),
]

CUTS = [0.0, 1.85, 3.72, 6.42, 7.55, 9.98, 13.38, 14.96, 15.92, 17.50, 18.40, 20.40, 21.40, 24.86, 27.80, 29.60, DUR]
TWIST = 18.40                                   # 18.40 / 31.1 = 59 %

S = 'library/sfx/'
G = 'series/grim-ride/sfx/'
SFX = [
    (S + 'doorbell_chime.mp3', 0.00, 0.5),
    (S + 'plastic_bag_rustle.mp3', 4.90, 0.5),
    (S + 'coin_clink.mp3', 5.40, 0.5),
    (S + 'cash_register.mp3', 6.00, 0.35),
    (S + 'record_scratch.mp3', 7.55, 0.35),
    (S + 'thunder_crack.mp3', 10.02, 0.6),
    (S + 'stamp.mp3', 13.95, 0.6),
    (G + 'raven_caw.mp3', 14.96, 0.25),
    (G + 'etrike_zoom.mp3', 15.92, 0.55),
    (S + 'curtain_reveal.mp3', 17.50, 0.5),
    (S + 'choir_hallelujah_short.mp3', 17.55, 0.55),
    (S + 'record_scratch.mp3', 18.38, 0.6),
    (S + 'piano_stop.mp3', 18.42, 0.4),
    (S + 'crowd_sigh.mp3', 20.40, 0.6),
    (S + 'book_thud.mp3', 21.10, 0.5),
    (G + 'etrike_rev.mp3', 21.40, 0.7),
    (G + 'etrike_zoom.mp3', 22.40, 0.7),
    (G + 'etrike_zoom.mp3', 24.86, 0.4),
    (S + 'sad_trombone.mp3', 28.00, 0.3),
    (S + 'doorbell_chime.mp3', 29.60, 0.45),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_night_crickets.mp3', 6.9, 0.0, DUR, 0.45, False),
    (S + 'amb_bbq_chatter.mp3', 6.9, 0.0, 17.5, 0.20, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 0.0, 18.35, 0.26, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 21.4, DUR, 0.26, True),
]

VFX = {}
VGAIN = {'grim': 1.55, 'edgar': 1.6, 'todd': 1.5, 'harold': 1.6, 'kayden': 1.55, 'mom': 1.5}
