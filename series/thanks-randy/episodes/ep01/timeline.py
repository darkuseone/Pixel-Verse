"""S01E01 «$89 TURKEY?!» — timing for video (ep01.py) and audio (mix.py). Voice: tightened takes voice/ep01_t.
Sound design: ONLY this series' own sounds (series/thanks-randy/sfx, owner rule 12.10.2026) + the sitcom theme loop."""
DUR = 30.8
FPS = 30
SLUG = 'thanks-randy'
MASTER = 0.80

VOICE = [
    ('r1', 'ep01_t', 'r1', 0.00, 0.00, 2.29, 'randy', 'EIGHTY-NINE bucks?! For a BIRD?!'),
    ('t1', 'ep01_t', 't1', 2.42, 0.00, 1.33, 'tom', "I'm worth IT."),
    ('r2', 'ep01_t', 'r2', 3.86, 0.00, 3.99, 'randy', "This year I'm HOSTING. Twenty years — never burned a TURKEY!"),
    ('b1', 'ep01_t', 'b1', 7.95, 0.00, 1.54, 'brayden', 'You never COOKED one.'),
    ('s1', 'ep01_t', 's1', 9.62, 0.00, 2.16, 'scandee', 'Unexpected item in bagging AREA.'),
    ('s2', 'ep01_t', 's2', 12.45, 0.00, 1.28, 'scandee', 'Unexpected ITEM.'),
    ('r4', 'ep01_t', 'r4', 15.15, 0.00, 1.59, 'randy', "There's NOTHING there!"),
    ('j1', 'ep01_t', 'j1', 16.98, 0.00, 1.85, 'joyce', "I'm RESTING, sweetie."),
    ('s3', 'ep01_t', 's3', 18.98, 0.00, 2.74, 'scandee', 'Grandma detected. Four ninety-nine per POUND.'),
    ('j2', 'ep01_t', 'j2', 21.88, 0.00, 3.63, 'joyce', "No, it's FINE. I'll just die HERE."),
    ('j3', 'ep01_t', 'j3', 25.65, 0.00, 2.61, 'joyce', 'So. When are you getting MARRIED?'),
    ('s4', 'ep01_t', 's4', 28.40, 0.00, 2.19, 'scandee', 'Total. Eighty-nine NINETY-NINE.'),
]

#       hook  tom   host  scan  lift   nothing twist  weigh  fine   married glitch
CUTS = [0.0, 2.42, 3.86, 9.55, 12.30, 15.10, 16.80, 18.95, 21.80, 25.58, 28.32, DUR]
NAMES = ['hook', 'tom', 'host', 'scan', 'lift', 'nothing', 'twist', 'weigh', 'fine', 'married', 'glitch']
TWIST = CUTS[6]

X = 'series/thanks-randy/sfx/'
SFX = [
    (X + 'scan_beep.mp3', 0.00, 0.85),
    (X + 'sneaker_squeak.mp3', 0.30, 0.55),
    (X + 'ice_creak.mp3', 2.42, 0.85),
    (X + 'knit_clicks.mp3', 2.70, 1.6, 0.0, 1.0),
    (X + 'phone_rec.mp3', 3.90, 3.0),
    (X + 'sneaker_squeak.mp3', 6.20, 0.35),
    (X + 'kiosk_error.mp3', 9.55, 0.80),
    (X + 'knit_clicks.mp3', 11.70, 1.8, 0.0, 0.8),
    (X + 'body_lift_strain.mp3', 12.35, 1.6),
    (X + 'cloth_rustle.mp3', 12.40, 0.55),
    (X + 'turkey_slide.mp3', 12.50, 0.45),
    (X + 'turkey_clonk.mp3', 13.00, 1.0),
    (X + 'ice_creak.mp3', 13.10, 0.6),
    (X + 'cloth_rustle.mp3', 13.62, 0.55),
    (X + 'wallet_slap.mp3', 13.85, 3.0),
    (X + 'kiosk_error.mp3', 13.95, 0.40),
    (X + 'cap_whoosh.mp3', 14.15, 2.0),
    (X + 'kiosk_error.mp3', 14.40, 0.40),
    (X + 'sneaker_squeak.mp3', 14.50, 0.6),
    (X + 'shoe_bounce.mp3', 14.70, 3.0),
    (X + 'kiosk_error.mp3', 14.85, 0.45),
    (X + 'knit_clicks.mp3', 15.30, 2.2, 0.0, 1.3),
    (X + 'bag_rip.mp3', 16.74, 1.0),
    (X + 'twist_sting.mp3', 16.80, 0.75),
    (X + 'knit_clicks.mp3', 17.20, 2.0, 0.0, 1.6),
    (X + 'scan_beep.mp3', 18.95, 0.7),
    (X + 'scan_beep.mp3', 19.20, 0.6),
    (X + 'kiosk_error.mp3', 21.40, 0.45),
    (X + 'cloth_rustle.mp3', 24.70, 0.5),
    (X + 'knit_clicks.mp3', 25.60, 1.6, 0.0, 1.2),
    (X + 'kiosk_glitch.mp3', 28.30, 0.85),
    (X + 'receipt_print.mp3', 29.30, 0.75),
    (X + 'scan_beep.mp3', 29.80, 0.65),
]

BEDS = [
    ('series/thanks-randy/sfx/store_amb_loop.mp3', 8.0, 0.0, DUR, 0.70, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 3.86, 16.70, 0.24, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 18.95, DUR, 0.20, True),
]

VFX = {'scandee': 'highpass=f=180,lowpass=f=7000,aecho=0.5:0.3:18:0.15'}
VGAIN = {'randy': 1.5, 'tom': 1.65, 'joyce': 1.6, 'brayden': 1.55, 'scandee': 1.35}
