"""S01E02 «GRAVY'S A LIQUID?!» — timing for video (ep02.py) and audio (mix.py). Voice: tightened takes voice/ep02_t.
Sound design: ONLY this series' own sounds (series/thanks-randy/sfx) + the sitcom theme loop."""
DUR = 32.75
FPS = 30
SLUG = 'thanks-randy'
MASTER = 0.80

VOICE = [
    ('r1', 'ep02_t', 'r1', 0.00, 0.00, 1.33, 'randy', "Gravy's a LIQUID?!"),
    ('p1', 'ep02_t', 'p1', 1.45, 0.00, 3.16, 'patty', 'Over three point four ounces. LIQUID.'),
    ('r2', 'ep02_t', 'r2', 4.72, 0.00, 1.54, 'randy', "It's Nana's GRAVY!"),
    ('p2', 'ep02_t', 'p2', 6.36, 0.00, 2.25, 'patty', "Then it's a family LIQUID."),
    ('t1', 'ep02_t', 't1', 8.74, 0.00, 3.47, 'tom', 'Flew me to Arizona to THAW. Still frozen.'),
    ('r3', 'ep02_t', 'r3', 12.32, 0.00, 2.80, 'randy', "If it's INSIDE me — it's not LUGGAGE."),
    ('r4', 'ep02_t', 'r4', 15.30, 0.00, 2.12, 'randy', 'Zero LIQUID!'),
    ('s1', 'ep02_t', 's1', 17.58, 0.00, 2.87, 'scandee', 'Unexpected LIQUID. One hundred twenty-eight ounces.'),
    ('p3', 'ep02_t', 'p3', 20.58, 0.00, 3.00, 'patty', 'Sir. YOU are a liquid now.'),
    ('r5', 'ep02_t', 'r5', 23.70, 0.00, 2.56, 'randy', 'Twenty years — never burned a TURKEY!'),
    ('p4', 'ep02_t', 'p4', 26.36, 0.00, 2.35, 'patty', 'Not flying today EITHER.'),
    ('t2', 'ep02_t', 't2', 28.84, 0.00, 2.85, 'tom', 'Still frozen. Still FLYING.'),
    ('s2', 'ep02_t', 's2', 31.80, 0.00, 0.71, 'scandee', 'LIQUID.'),
]

#       hook  patty  plead  xray   scheme chug   scanner liquid slosh  bins   loop
CUTS = [0.0, 1.42, 4.66, 8.68, 12.27, 14.95, 17.50, 20.52, 23.64, 28.78, 31.74, DUR]
NAMES = ['hook', 'patty', 'plead', 'xray', 'scheme', 'chug', 'scanner', 'liquid', 'slosh', 'bins', 'loop']
TWIST = CUTS[6]

X = 'series/thanks-randy/sfx/'
SFX = [
    (X + 'jug_slosh.mp3', 0.00, 4.0),
    (X + 'glove_snap.mp3', 0.05, 6.0),
    (X + 'gum_chew.mp3', 1.50, 1.2),
    (X + 'gum_pop.mp3', 4.35, 0.9),
    (X + 'sneaker_squeak.mp3', 4.75, 0.45),
    (X + 'jug_slosh.mp3', 6.30, 3.5),
    (X + 'gum_chew.mp3', 7.00, 0.9),
    (X + 'bin_clatter.mp3', 8.70, 0.9),
    (X + 'ice_creak.mp3', 9.10, 0.75),
    (X + 'scan_beep.mp3', 11.90, 0.45),
    (X + 'cap_unscrew.mp3', 12.90, 1.4),
    (X + 'jug_slosh.mp3', 14.20, 4.0),
    (X + 'chug_glug.mp3', 14.95, 1.0),
    (X + 'belly_slosh.mp3', 15.70, 3.0),
    (X + 'twist_sting.mp3', 17.48, 0.7),
    (X + 'scanner_alarm.mp3', 17.52, 0.45),
    (X + 'scanner_alarm.mp3', 19.00, 0.30),
    (X + 'gum_pop.mp3', 23.20, 0.9),
    (X + 'belly_slosh.mp3', 24.00, 3.0),
    (X + 'belly_slosh.mp3', 25.10, 3.0),
    (X + 'belly_slosh.mp3', 26.20, 2.5),
    (X + 'gum_chew.mp3', 26.40, 0.8),
    (X + 'body_squish.mp3', 28.80, 0.8),
    (X + 'bin_clatter.mp3', 29.10, 0.7),
    (X + 'ice_creak.mp3', 30.40, 0.6),
    (X + 'scanner_alarm.mp3', 31.76, 0.35),
]

BEDS = [
    ('series/thanks-randy/sfx/airport_amb_loop.mp3', 8.0, 0.0, DUR, 0.32, True),
    ('series/thanks-randy/sfx/xray_belt_loop.mp3', 6.0, 8.68, 12.27, 0.22, True),
    ('series/thanks-randy/sfx/xray_belt_loop.mp3', 6.0, 28.78, DUR, 0.25, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 1.45, 17.40, 0.22, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 20.52, DUR, 0.20, True),
]

VFX = {'scandee': 'highpass=f=180,lowpass=f=7000,aecho=0.5:0.3:18:0.15'}
VGAIN = {'randy': 1.5, 'tom': 1.65, 'patty': 1.6, 'scandee': 1.35}
