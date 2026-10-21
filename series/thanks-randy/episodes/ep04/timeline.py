"""S01E04 «RANDY, NO!» — timing for video (ep04.py) and audio (mix.py). Voice: tightened takes voice/ep04_t.
Sound design: ONLY this series' own sounds (series/thanks-randy/sfx) + the sitcom theme loop."""
DUR = 34.45
FPS = 30
SLUG = 'thanks-randy'
MASTER = 0.64

VOICE = [
    ('f', 'ep04_t', 'f', 0.00, 0.00, 1.62, 'family', 'RANDY, NO!'),
    ('t1', 'ep04_t', 't1', 3.55, 0.00, 1.75, 'tom', 'Still FROZEN.'),
    ('r1', 'ep04_t', 'r1', 5.45, 0.00, 2.85, 'randy', 'Twenty years. Never burned a TURKEY.'),
    ('j1', 'ep04_t', 'j1', 8.42, 0.00, 1.99, 'joyce', 'You burned the GARAGE.'),
    ('r2', 'ep04_t', 'r2', 10.55, 0.00, 2.53, 'randy', 'Garage is on FIRE! Send EVERYBODY!'),
    ('b1', 'ep04_t', 'b1', 13.20, 0.00, 2.38, 'brayden', "Bro. We're TRENDING."),
    ('r3', 'ep04_t', 'r3', 15.70, 0.00, 1.91, 'randy', 'Okay. The PROS are here.'),
    ('d1', 'ep04_t', 'd1', 17.85, 0.00, 1.54, 'dunn', 'Ours went off at the STATION.'),
    ('d2', 'ep04_t', 'd2', 19.55, 0.00, 2.59, 'dunn', 'Twenty years. Never burned a turkey.'),
    ('r4', 'ep04_t', 'r4', 22.25, 0.00, 0.86, 'randy', 'SAME.'),
    ('j2', 'ep04_t', 'j2', 23.95, 0.00, 2.51, 'joyce', 'So. When are you getting MARRIED?'),
    ('d3', 'ep04_t', 'd3', 26.58, 0.00, 1.52, 'dunn', "To the job, MA'AM."),
    ('d4', 'ep04_t', 'd4', 28.25, 0.00, 1.99, 'dunn', 'That bird still FROZEN?'),
    ('d5', 'ep04_t', 'd5', 30.35, 0.00, 2.17, 'dunn', 'Got any OIL?'),
    ('f2', 'ep04_t', 'f', 32.65, 0.00, 1.62, 'family', 'RANDY, NO!'),
]

#       hook  boom  crater soot  garage call   pros   truck  same   married oil    loop
CUTS = [0.0, 1.50, 3.50, 5.40, 8.35, 10.50, 15.62, 17.70, 19.45, 24.00, 28.20, 32.60, DUR]
NAMES = ['hook', 'boom', 'crater', 'soot', 'garage', 'call', 'pros', 'truck', 'same', 'married', 'oil', 'loop']
TWIST = CUTS[7]

X = 'series/thanks-randy/sfx/'
SFX = [
    (X + 'oil_bubble_loop.mp3', 0.00, 0.6, 0.0, 1.5),
    (X + 'hook_clank.mp3', 0.20, 4.0),
    (X + 'oil_splash.mp3', 1.10, 0.9),
    (X + 'fireball.mp3', 1.45, 1.0),
    (X + 'turkey_clonk.mp3', 3.55, 1.0),
    (X + 'ice_creak.mp3', 3.70, 0.7),
    (X + 'extinguisher.mp3', 8.40, 0.5),
    (X + 'phone_dial.mp3', 10.40, 0.6),
    (X + 'phone_rec.mp3', 13.15, 3.0),
    (X + 'siren_approach.mp3', 14.80, 0.7),
    (X + 'truck_brakes.mp3', 17.62, 0.55),
    (X + 'twist_sting.mp3', 17.70, 0.65),
    (X + 'back_pats.mp3', 23.10, 2.5),
    (X + 'cloth_rustle.mp3', 23.90, 0.5),
    (X + 'ice_creak.mp3', 28.30, 0.6),
    (X + 'oil_bubble_loop.mp3', 32.50, 0.6, 0.0, 1.9),
]

BEDS = [
    ('series/thanks-randy/sfx/yard_wind_loop.mp3', 8.0, 0.0, DUR, 0.65, True),
    ('series/thanks-randy/sfx/fire_crackle_loop.mp3', 6.0, 1.50, 32.60, 1.6, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 3.55, 17.60, 0.20, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 19.45, 32.55, 0.20, True),
]

VFX = {'randy': 'acompressor=threshold=0.5:ratio=2'}
VGAIN = {'family': 1.5, 'randy': 1.5, 'tom': 1.65, 'joyce': 1.6, 'brayden': 1.45, 'dunn': 1.6}
