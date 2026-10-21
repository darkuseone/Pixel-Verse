"""S01E05 «$30 FOR FOOTBALL?!» — timing for video (ep05.py) and audio (mix.py). Voice: tightened takes voice/ep05_t.
Sound design: ONLY this series' own sounds (series/thanks-randy/sfx) + the sitcom theme loop."""
DUR = 32.25
FPS = 30
SLUG = 'thanks-randy'
MASTER = 0.80

VOICE = [
    ('r1', 'ep05_t', 'r1', 0.00, 0.00, 1.93, 'randy', 'THIRTY bucks?! For FOOTBALL?!'),
    ('j1', 'ep05_t', 'j1', 2.00, 0.00, 2.51, 'joyce', "Randy, it's PERFECT!"),
    ('r2', 'ep05_t', 'r2', 4.56, 0.00, 2.51, 'randy', 'Twenty years! Never burned a TURKEY!'),
    ('b1', 'ep05_t', 'b1', 7.12, 0.00, 2.14, 'brayden', 'It still has the PRICE TAG.'),
    ('s1', 'ep05_t', 's1', 9.34, 0.00, 3.24, 'scandee', 'Download the APP. Verify your EMAIL. Reset your PASSWORD.'),
    ('s2', 'ep05_t', 's2', 12.64, 0.00, 2.51, 'scandee', 'Security question. Name of your first PET?'),
    ('r3', 'ep05_t', 'r3', 15.22, 0.00, 1.28, 'randy', 'TOM?'),
    ('t1', 'ep05_t', 't1', 16.56, 0.00, 1.25, 'tom', 'We never MET.'),
    ('s3', 'ep05_t', 's3', 17.90, 0.00, 4.23, 'scandee', 'To speak to an agent, subscribe to SUPPORT PLUS. Twenty-nine NINETY-NINE.'),
    ('r4', 'ep05_t', 'r4', 22.25, 0.00, 2.04, 'randy', 'I just want to watch the GAME!'),
    ('j2', 'ep05_t', 'j2', 24.40, 0.00, 2.80, 'joyce', "No, it's FINE. I have CABLE."),
    ('b2', 'ep05_t', 'b2', 27.80, 0.00, 2.01, 'brayden', 'Spoiler. We LOST.'),
    ('f', 'ep05_t', 'f', 29.95, 0.00, 1.99, 'family', 'Thanks, RANDY.'),
]

#       hook  table tag   windows question tom    freezer twist  knees  cable  final  thanks
CUTS = [0.0, 2.00, 7.10, 9.30, 12.62, 15.20, 16.52, 17.86, 22.20, 24.35, 27.30, 29.90, DUR]
NAMES = ['hook', 'table', 'tag', 'windows', 'question', 'tom', 'freezer', 'twist', 'knees', 'cable', 'final', 'thanks']
TWIST = CUTS[7]

X = 'series/thanks-randy/sfx/'
SFX = [
    (X + 'remote_click.mp3', 0.00, 4.0),
    (X + 'tv_popup.mp3', 0.05, 3.0),
    (X + 'family_applause.mp3', 2.05, 0.6),
    (X + 'fork_drop.mp3', 7.30, 0.5),
    (X + 'tv_popup.mp3', 9.40, 2.6),
    (X + 'tv_popup.mp3', 10.20, 2.6),
    (X + 'tv_popup.mp3', 11.00, 2.6),
    (X + 'tv_popup.mp3', 11.80, 2.6),
    (X + 'chewing.mp3', 9.60, 4.0),
    (X + 'tv_popup.mp3', 12.70, 2.6),
    (X + 'ice_creak.mp3', 16.55, 0.7),
    (X + 'twist_sting.mp3', 17.86, 0.65),
    (X + 'kiosk_error.mp3', 17.90, 0.6),
    (X + 'knees_thud.mp3', 22.20, 3.0),
    (X + 'purse_rummage_soft.mp3', 24.45, 2.0),
    (X + 'tv_static_soft.mp3', 25.60, 0.35),
    (X + 'tiny_tv_crowd.mp3', 26.10, 0.35),
    (X + 'tiny_tv_crowd.mp3', 27.30, 0.45),
    (X + 'remote_click.mp3', 31.80, 4.0),
]

BEDS = [
    ('series/thanks-randy/sfx/dinner_amb_loop.mp3', 8.0, 0.0, DUR, 7.0, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 2.00, 17.80, 0.20, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 22.20, DUR, 0.20, True),
]

VFX = {'scandee': 'highpass=f=180,lowpass=f=7000,aecho=0.5:0.3:18:0.15'}
VGAIN = {'family': 1.6, 'randy': 1.5, 'tom': 1.65, 'joyce': 1.6, 'brayden': 1.55, 'scandee': 1.35}
