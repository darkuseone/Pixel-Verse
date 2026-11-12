"""S01E01 «FREE PARKING?» — timing for video (ep01.py) and audio (mix.py). Voice: tightened takes voice/ep01_t (tempo 1.08–1.10).
Sound: this series' own sounds (series/still-1986/sfx) + CC0 library (scratch, whoosh, rimshot) + the synthwave loop (phone EQ)."""
DUR = 45.0
FPS = 30
SLUG = 'still-1986'
LUFS = -14.0

VOICE = [
    ('v1', 'ep01_t', 'v1', 0.00, 0.00, 3.90, 'vince', "Ocean Drive. Sunset. And I'm parking for FREE, baby."),
    ('f1', 'ep01_t', 'f1', 3.98, 0.00, 3.17, 'fran', 'Honey. Nobody parks free on Ocean DRIVE.'),
    ('v2', 'ep01_t', 'v2', 7.24, 0.00, 2.98, 'vince', "Watch me. It's eighty-six. Parking's a QUARTER."),
    ('f2', 'ep01_t', 'f2', 10.55, 0.00, 3.79, 'fran', "Honey, it's twenty twenty-six. There's an APP."),
    ('v3', 'ep01_t', 'v3', 14.42, 0.00, 2.91, 'vince', 'Fourteen an HOUR?! Plus a CONVENIENCE fee?!'),
    ('v5', 'ep01_t', 'v5', 17.42, 0.00, 4.16, 'vince', "New plan. If I never STOP, it's not PARKING."),
    ('f3', 'ep01_t', 'f3', 21.70, 0.00, 3.79, 'fran', 'Lap forty-seven. Send this to your friend who does THIS.'),
    ('v7', 'ep01_t', 'v7', 25.70, 0.00, 1.24, 'vince', 'FREE PARKING!'),
    ('r1', 'ep01_t', 'r1', 28.80, 0.00, 2.18, 'rey', 'Tow and storage. Three-fifty, AMIGO.'),
    ('v8', 'ep01_t', 'v8', 31.05, 0.00, 1.45, 'vince', 'It SAID free!'),
    ('r2', 'ep01_t', 'r2', 32.57, 0.00, 2.00, 'rey', "Parking's free. The RIDE'S three-fifty."),
    ('v10', 'ep01_t', 'v10', 34.66, 0.00, 1.97, 'vince', "FINE! I'll pay in QUARTERS!"),
    ('r3', 'ep01_t', 'r3', 36.72, 0.00, 1.94, 'rey', "Tow's pay-by-APP, amigo."),
    ('v9', 'ep01_t', 'v9', 38.80, 0.00, 2.86, 'vince', 'Still the coolest guy on Ocean DRIVE.'),
    ('f4', 'ep01_t', 'f4', 41.77, 0.00, 2.88, 'fran', 'Coolest guy on a TOW truck, honey.'),
]

#       hook  fran_on meter bonk  fran_cu app    plan   laps_a laps_b twist  lift   rey    said   star   coins  tow_app drive  button
CUTS = [0.0, 3.98, 7.24, 10.05, 10.75, 14.42, 17.42, 19.35, 22.40, 25.58, 27.90, 28.80, 31.05, 32.57, 34.66, 36.72, 38.80, 41.77, DUR]
NAMES = ['hook', 'fran_on', 'meter', 'bonk', 'fran_cu', 'app', 'plan', 'laps_a', 'laps_b', 'twist', 'lift', 'rey', 'said', 'star',
         'coins', 'tow_app', 'drive', 'button']
TWIST = CUTS[9]                  # 25.58 / 45.0 = 57 %

X = 'series/still-1986/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'sax_fantasy.mp3', 0.00, 0.55),
    (X + 'car_cruise.mp3', 0.10, 0.45),
    (X + 'neon_on.mp3', 4.05, 0.9),
    (X + 'car_cruise.mp3', 4.40, 0.35),
    (L + 'car_arrive_stop.mp3', 6.70, 0.45),
    (X + 'coin_bonk.mp3', 9.05, 0.95),
    (X + 'coin_bonk.mp3', 10.18, 0.9),
    (L + 'boing_cartoon.mp3', 10.25, 0.35),
    (X + 'neon_on.mp3', 10.75, 0.5),
    (X + 'app_ding.mp3', 14.45, 0.7),
    (L + 'vinyl_scratch.mp3', 14.90, 0.55),
    (L + 'whoosh_1.mp3', 19.30, 0.5),
    (X + 'car_cruise.mp3', 19.40, 0.5),
    (X + 'car_cruise.mp3', 20.90, 0.45),
    (L + 'whoosh_3.mp3', 22.35, 0.45),
    (X + 'car_cruise.mp3', 22.50, 0.45),
    (X + 'car_cruise.mp3', 24.00, 0.4),
    (X + 'sax_fantasy.mp3', 25.62, 0.65),
    (L + 'whoosh_1.mp3', 25.55, 0.4),
    (X + 'car_cruise.mp3', 26.40, 0.45),
    (X + 'tow_winch.mp3', 27.30, 0.85),
    (L + 'anvil_clank.mp3', 27.95, 0.40),
    (L + 'vinyl_scratch.mp3', 27.09, 0.45),
    (L + 'cloth_rustle.mp3', 29.00, 0.4),
    (X + 'neon_on.mp3', 32.60, 0.35),
    (L + 'whoosh_3.mp3', 32.57, 0.35),
    (L + 'keys_on_table.mp3', 34.80, 0.45),
    (X + 'app_ding.mp3', 36.80, 0.65),
    (X + 'tow_winch.mp3', 38.70, 0.5),
    (X + 'car_cruise.mp3', 39.10, 0.5),
    (X + 'neon_on.mp3', 41.80, 0.6),
    (L + 'rimshot_joke.mp3', 43.85, 0.45),
    (X + 'app_ding.mp3', 44.00, 0.5),
]

BEDS = [
    (X + 'miami_eve_loop.mp3', 8.0, 0.0, DUR, 0.55, True),
    (X + 'neon_buzz_loop.mp3', 4.0, 4.0, 14.4, 0.25, True),
    ('series/still-1986/music/synth_theme_phone.mp3', 15.0, 0.0, 27.85, 0.30, True, 'equalizer=f=1500:t=q:w=1.4:g=-6'),
    ('series/still-1986/music/synth_theme_phone.mp3', 15.0, 28.75, DUR, 0.28, True, 'equalizer=f=1500:t=q:w=1.4:g=-6'),
]

VFX = {'fran': 'highpass=f=120,aecho=0.6:0.25:22:0.12'}
VGAIN = {'vince': 1.5, 'fran': 1.6, 'rey': 1.6}
