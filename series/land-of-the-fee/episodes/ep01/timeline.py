"""S01E01 «REPRESENTATIVE!» — timing for video (ep01.py) and audio (mix.py). Voice: tightened takes voice/ep01_t.
Sound design: ONLY this series' own sounds (series/land-of-the-fee/sfx, owner rule 12.10.2026) + the code-synth kazoo march."""
DUR = 31.0
FPS = 30
SLUG = 'land-of-the-fee'
MASTER = 0.80
LUFS = -14.0                     # owner's test rule 25.10.2026: -14 LUFS / -1 dBTP

VOICE = [
    ('d1', 'ep01_t', 'd1', 0.00, 0.00, 1.33, 'duke', 'REPRESENTATIVE!!'),
    ('f1', 'ep01_t', 'f1', 1.45, 0.00, 2.41, 'feebee', 'Sounds like you said — UPGRADE! Done!'),
    ('d2', 'ep01_t', 'd2', 3.98, 0.00, 2.55, 'duke', "I'm a BALD EAGLE. I'm on the DOLLAR!"),
    ('s1', 'ep01_t', 's1', 6.65, 0.00, 1.66, 'sal', 'Not on YOURS.'),
    ('d3', 'ep01_t', 'd3', 8.70, 0.00, 2.37, 'duke', "Fine. I'm talking to a HUMAN."),
    ('d4', 'ep01_t', 'd4', 11.20, 0.00, 1.30, 'duke', 'HUMAN! NOW!'),
    ('f2', 'ep01_t', 'f2', 12.62, 0.00, 2.00, 'feebee', 'Sounds like you said — HUMMUS!'),
    ('o1', 'ep01_t', 'o1', 14.80, 0.00, 2.78, 'doris', "Hi, hon! I'm a REAL human!"),
    ('o2', 'ep01_t', 'o2', 17.70, 0.00, 2.34, 'doris', "That's nineteen ninety-nine a MINUTE."),
    ('d5', 'ep01_t', 'd5', 20.16, 0.00, 0.87, 'duke', 'For WHAT?!'),
    ('o3', 'ep01_t', 'o3', 21.15, 0.00, 2.18, 'doris', "Eye contact's EXTRA, hon."),
    ('d6', 'ep01_t', 'd6', 23.45, 0.00, 1.95, 'duke', "Forget it! I'll take the ROBOT!"),
    ('f3', 'ep01_t', 'f3', 25.52, 0.00, 1.98, 'feebee', 'Sounds like you said — HUMAN!'),
    ('s2', 'ep01_t', 's2', 29.40, 0.00, 1.32, 'sal', 'Majestic.'),
]

#       hook  phone proud sal   fly   kiosk  door   twist  what   run    kiosk2 button
CUTS = [0.0, 1.40, 3.92, 6.60, 8.62, 11.15, 14.70, 17.65, 20.10, 23.40, 25.45, 27.55, DUR]
NAMES = ['hook', 'phone', 'proud', 'sal', 'fly', 'kiosk', 'door', 'twist', 'what', 'run', 'kiosk2', 'button']
TWIST = 17.70
CHIRP = (28.05, 29.25)           # Duke's real (wimpy) bald-eagle call

X = 'series/land-of-the-fee/sfx/'
SFX = [
    (X + 'phone_grip.mp3', 0.00, 1.2),
    (X + 'table_slam.mp3', 0.04, 3.0),
    (X + 'feather_burst.mp3', 0.10, 6.0),
    (X + 'assistant_wake.mp3', 1.40, 0.45),
    (X + 'ka_ching.mp3', 3.25, 0.55),
    (X + 'feather_burst.mp3', 3.95, 5.0),
    (X + 'pigeon_coo.mp3', 6.45, 0.35),
    (X + 'fry_munch.mp3', 6.55, 6.0),
    (X + 'fry_munch.mp3', 8.05, 5.0),
    (X + 'wallet_moth.mp3', 8.15, 9.0),
    (X + 'wing_flap.mp3', 8.62, 0.9),
    (X + 'whoosh_fly.mp3', 9.20, 0.7),
    (X + 'wing_flap.mp3', 10.10, 0.7),
    (X + 'glass_doors.mp3', 11.10, 1.2),
    (X + 'talons_tile.mp3', 11.18, 1.6),
    (X + 'assistant_wake.mp3', 12.55, 0.35),
    (X + 'hummus_plop.mp3', 14.30, 1.3),
    (X + 'door_burst.mp3', 14.70, 1.0),
    (X + 'holy_choir.mp3', 14.74, 0.65),
    (X + 'twist_sting.mp3', 17.66, 0.75),
    (X + 'ka_ching.mp3', 17.72, 0.75),
    (X + 'meter_tick.mp3', 18.00, 1.6),
    (X + 'meter_tick.mp3', 22.70, 1.6),
    (X + 'ka_ching.mp3', 22.95, 0.70),
    (X + 'talons_tile.mp3', 23.42, 1.8),
    (X + 'whoosh_fly.mp3', 23.60, 0.5),
    (X + 'talons_tile.mp3', 24.30, 1.6),
    (X + 'assistant_wake.mp3', 25.45, 0.35),
    (X + 'ka_ching.mp3', 27.40, 0.80),
    (X + 'meter_tick.mp3', 27.50, 1.4),
    (X + 'big_inhale.mp3', 27.58, 0.9),
    (X + 'eagle_chirp.mp3', CHIRP[0], 1.15),
    (X + 'pigeon_coo.mp3', 29.30, 0.25),
    (X + 'ka_ching.mp3', 30.00, 0.35),                 # end card «SUBSCRIBE!» pops (coin clink)
]

M = 'series/land-of-the-fee/music/freedom_kazoo_16s.mp3'
BEDS = [
    (X + 'apt_amb_loop.mp3', 8.0, 0.0, 8.62, 0.8, True),
    (X + 'mall_amb_loop.mp3', 8.0, 8.62, 11.15, 0.9, True),
    (X + 'store_amb_loop.mp3', 8.0, 11.15, DUR, 0.8, True),
    (M, 16.0, 1.40, 14.70, 0.24, True),
    (M, 16.0, 20.10, 27.55, 0.20, True),
]

VFX = {'feebee': 'highpass=f=160,lowpass=f=7600,aecho=0.5:0.3:14:0.12'}
VGAIN = {'duke': 1.45, 'sal': 1.6, 'feebee': 1.35, 'doris': 1.5}
