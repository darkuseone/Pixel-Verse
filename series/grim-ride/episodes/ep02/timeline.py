"""S01E02 «Verify You're Human» — timing for video (ep02.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep02_t)."""
DUR = 32.4
FPS = 30
SLUG = 'grim-ride'
MASTER = 0.76

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('g1', 'ep02_t', 'g1', 0.00, 0.00, 3.03, 'grim', 'Select all squares with a PULSE?'),
    ('e1', 'ep02_t', 'e1', 3.12, 0.00, 0.78, 'edgar', 'OOPS.'),
    ('d1', 'ep02_t', 'd1', 3.98, 0.00, 2.80, 'dashley', "Oopsie! Let's try again. Are you a HUMAN?"),
    ('g2', 'ep02_t', 'g2', 6.86, 0.00, 2.04, 'grim', 'I am DEATH!'),
    ('d2', 'ep02_t', 'd2', 8.96, 0.00, 1.96, 'dashley', "Sorry, I didn't CATCH that!"),
    ('g3', 'ep02_t', 'g3', 11.00, 0.00, 3.19, 'grim', 'Speed. Unlock. NOW.'),
    ('d3', 'ep02_t', 'd3', 14.26, 0.00, 3.03, 'dashley', 'For your safety, your bike is now Class ONE!'),
    ('d4', 'ep02_t', 'd4', 17.36, 0.00, 1.75, 'dashley', 'Transferring you to a SPECIALIST!'),
    ('g5', 'ep02_t', 'g5', 19.55, 0.00, 0.84, 'grim', 'Hello?'),
    ('g5b', 'ep02_t', 'g5', 19.95, 0.00, 0.84, 'grimph', '...hello?'),
    ('e2', 'ep02_t', 'e2', 20.55, 0.00, 0.97, 'edgar', 'PROMOTED.'),
    ('d5', 'ep02_t', 'd5', 21.60, 0.00, 1.91, 'dashley', 'The specialist is UNAVAILABLE!'),
    ('g6', 'ep02_t', 'g6', 23.58, 0.00, 1.75, 'grim', "I'M AVAILABLE!"),
    ('h1', 'ep02_t', 'h1', 25.45, 0.00, 1.20, 'harold', 'Evening, BONES!'),
    ('d6', 'ep02_t', 'd6', 26.75, 0.00, 2.85, 'dashley', 'Your estimated wait time is ETERNITY!'),
    ('g7', 'ep02_t', 'g7', 29.70, 0.00, 1.38, 'grim', "That's MY line."),
]

CUTS = [0.0, 2.55, 3.10, 3.95, 6.82, 8.92, 10.95, 14.22, 17.32, 19.15, 20.50, 21.55, 23.55, 25.40, 26.70, 29.65, 31.10, DUR]
TWIST = 19.15                                   # 19.15 / 32.4 = 59 %

S = 'library/sfx/'
G = 'series/grim-ride/sfx/'
SFX = [
    (S + 'app_notify_ping.mp3', 0.00, 0.6),
    (S + 'ui_tap_chirp.mp3', 2.68, 0.5), (G + 'flatline_beep.mp3', 2.72, 0.22),
    (S + 'ui_tap_chirp.mp3', 2.83, 0.5), (G + 'flatline_beep.mp3', 2.87, 0.22),
    (S + 'ui_tap_chirp.mp3', 2.98, 0.5), (G + 'flatline_beep.mp3', 3.02, 0.22),
    (S + 'scanner_beep.mp3', 3.20, 0.4),
    (S + 'app_notify_ping.mp3', 4.00, 0.5),
    (S + 'thunder_crack.mp3', 6.86, 0.6),
    (S + 'app_notify_ping.mp3', 9.00, 0.5),
    (S + 'battery_die_beeps.mp3', 14.30, 0.45),
    (S + 'sad_trombone.mp3', 16.20, 0.3),
    (G + 'phone_ring_pocket.mp3', 19.15, 0.35),
    (S + 'record_scratch.mp3', 19.12, 0.6),
    (S + 'phone_pickup.mp3', 19.48, 0.6),
    (G + 'raven_caw.mp3', 20.50, 0.25),
    (S + 'phone_slam.mp3', 25.20, 0.5),
    (G + 'etrike_zoom.mp3', 25.40, 0.7),
    (S + 'sad_trombone.mp3', 29.40, 0.3),
    (S + 'app_notify_ping.mp3', 31.10, 0.5),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_night_crickets.mp3', 6.9, 0.0, DUR, 0.45, False),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 0.0, 17.3, 0.24, True),
    (S + 'hold_music_elise.mp3', 14.2, 17.4, DUR, 0.30, True),
]

PH = 'highpass=f=300,lowpass=f=3400,acompressor=threshold=0.2:ratio=4,volume=1.2'
VFX = {'dashley': 'highpass=f=180,lowpass=f=6500,aecho=0.6:0.4:18:0.15', 'grimph': PH}
VGAIN = {'grim': 1.55, 'grimph': 1.3, 'edgar': 1.6, 'harold': 1.6, 'dashley': 1.45}
