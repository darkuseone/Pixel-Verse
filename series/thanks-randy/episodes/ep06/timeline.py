"""S01E06 «$199 TV?!» (season finale) — timing for video (ep06.py) and audio (mix.py). Voice: tightened takes voice/ep06_t.
Sound design: ONLY this series' own sounds (series/thanks-randy/sfx) + the sitcom theme loop."""
DUR = 32.5
FPS = 30
SLUG = 'thanks-randy'
MASTER = 0.80

VOICE = [
    ('r1', 'ep06_t', 'r1', 0.00, 0.00, 2.19, 'randy', 'One ninety-nine for a TV?!'),
    ('b1', 'ep06_t', 'b1', 2.28, 0.00, 3.68, 'brayden', "Spots in line. Forty BUCKS. It's a STARTUP."),
    ('r2', 'ep06_t', 'r2', 6.06, 0.00, 2.98, 'randy', 'Twenty years of Black Fridays. Never LOST!'),
    ('b2', 'ep06_t', 'b2', 9.12, 0.00, 1.54, 'brayden', 'You never GOT UP.'),
    ('r3', 'ep06_t', 'r3', 13.05, 0.00, 0.81, 'randy', 'MINE!'),
    ('k1', 'ep06_t', 'k1', 14.15, 0.00, 1.54, 'kyle', "That one's on HOLD."),
    ('r4', 'ep06_t', 'r4', 15.78, 0.00, 0.84, 'randy', 'For WHO?!'),
    ('j1', 'ep06_t', 'j1', 16.82, 0.00, 2.66, 'joyce', 'Me, sweetie. Since TUESDAY.'),
    ('j2', 'ep06_t', 'j2', 19.60, 0.00, 3.11, 'joyce', "No, it's FINE. Carry me to the CAR."),
    ('s1', 'ep06_t', 's1', 22.90, 0.00, 2.09, 'scandee', 'Unexpected item in bagging AREA.'),
    ('t1', 'ep06_t', 't1', 25.12, 0.00, 0.94, 'tom', 'Miss ME?'),
    ('s2', 'ep06_t', 's2', 26.18, 0.00, 2.59, 'scandee', 'Total: one ninety-nine. Plus GRANDMA.'),
    ('r5', 'ep06_t', 'r5', 28.90, 0.00, 1.41, 'randy', 'Thanks, RANDY.'),
    ('t2', 'ep06_t', 't2', 30.48, 0.00, 1.75, 'tom', 'Still FROZEN.'),
]

#       hook  line  clock  stampede mine  hold   twist  car    bag    total  s2
CUTS = [0.0, 2.25, 6.02, 10.70, 13.00, 14.05, 16.72, 19.55, 22.82, 26.12, 30.40, DUR]
NAMES = ['hook', 'line', 'clock', 'stampede', 'mine', 'hold', 'twist', 'car', 'bag', 'total', 's2']
TWIST = CUTS[6]

X = 'series/thanks-randy/sfx/'
SFX = [
    (X + 'sneaker_squeak.mp3', 0.00, 0.5),
    (X + 'tent_zip.mp3', 3.20, 0.6),
    (X + 'knit_clicks.mp3', 4.20, 1.4, 0.0, 1.2),
    (X + 'knuckles_crack.mp3', 6.10, 3.0),
    (X + 'doors_slide.mp3', 10.65, 0.9),
    (X + 'stampede.mp3', 10.75, 0.9),
    (X + 'slowmo_whoosh.mp3', 13.00, 0.7),
    (X + 'scan_beep.mp3', 14.10, 0.6),
    (X + 'box_flap.mp3', 16.70, 1.0),
    (X + 'twist_sting.mp3', 16.72, 0.65),
    (X + 'knit_clicks.mp3', 17.10, 1.6, 0.0, 1.4),
    (X + 'box_carry.mp3', 19.70, 0.9),
    (X + 'kiosk_error.mp3', 22.85, 0.7),
    (X + 'turkey_clonk.mp3', 25.05, 0.6),
    (X + 'ice_creak.mp3', 25.20, 0.6),
    (X + 'scan_beep.mp3', 26.15, 0.7),
    (X + 'receipt_print.mp3', 28.00, 0.6),
    (X + 'sleigh_bells.mp3', 30.40, 0.8),
]

BEDS = [
    ('series/thanks-randy/sfx/dawn_cold_loop.mp3', 8.0, 0.0, 10.70, 2.0, True),
    ('series/thanks-randy/sfx/store_chaos_loop.mp3', 6.0, 10.70, 30.40, 0.30, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 2.25, 16.65, 0.20, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 19.55, DUR, 0.22, True),
]

VFX = {'scandee': 'highpass=f=180,lowpass=f=7000,aecho=0.5:0.3:18:0.15'}
VGAIN = {'randy': 1.5, 'tom': 1.65, 'joyce': 1.6, 'brayden': 1.55, 'kyle': 1.6, 'scandee': 1.35}
