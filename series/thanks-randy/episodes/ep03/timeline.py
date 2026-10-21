"""S01E03 «STILL FROZEN?!» — timing for video (ep03.py) and audio (mix.py). Voice: tightened takes voice/ep03_t.
Sound design: ONLY this series' own sounds (series/thanks-randy/sfx) + the sitcom theme loop (hold music = the theme through a phone EQ)."""
DUR = 33.1
FPS = 30
SLUG = 'thanks-randy'
MASTER = 0.80

VOICE = [
    ('r1', 'ep03_t', 'r1', 0.00, 0.00, 1.52, 'randy', "It's STILL FROZEN?!"),
    ('t1', 'ep03_t', 't1', 1.65, 0.00, 3.08, 'tom', "Twenty-two pounds, pal. I'm a GLACIER."),
    ('r2', 'ep03_t', 'r2', 4.85, 0.00, 1.75, 'randy', 'Okay. Calling the EXPERTS.'),
    ('s1', 'ep03_t', 's1', 6.75, 0.00, 3.58, 'scandee', 'Wait time: FOUR hours. Our experts are ALSO thawing.'),
    ('c1', 'ep03_t', 'c1', 11.00, 0.00, 2.30, 'carol', 'Butterbutt Talk-Line, this is CAROL!'),
    ('r3', 'ep03_t', 'r3', 13.40, 0.00, 2.46, 'randy', "It's still FROZEN! Twenty-two POUNDS!"),
    ('c2', 'ep03_t', 'c2', 15.98, 0.00, 1.67, 'carol', 'Oh. HONEY.'),
    ('c3', 'ep03_t', 'c3', 17.80, 0.00, 2.64, 'carol', "Mine's frozen too. Can I come to YOURS?"),
    ('c4', 'ep03_t', 'c4', 21.45, 0.00, 1.12, 'carol2', 'We brought DIP!'),
    ('b1', 'ep03_t', 'b1', 22.80, 0.00, 2.74, 'brayden', 'Bro. THIS is a startup.'),
    ('j1', 'ep03_t', 'j1', 25.70, 0.00, 3.42, 'joyce', 'So. Which one of you is getting MARRIED?'),
    ('t2', 'ep03_t', 't2', 29.30, 0.00, 3.58, 'tom', "Great. Now it's a support GROUP."),
]

#       hook  tom   dial  hold  later  split  honey  twist  door   group  joyce  support
CUTS = [0.0, 1.62, 4.80, 6.70, 10.40, 11.00, 15.90, 17.72, 20.52, 22.70, 25.62, 29.22, DUR]
NAMES = ['hook', 'tom', 'dial', 'hold', 'later', 'split', 'honey', 'twist', 'door', 'group', 'joyce', 'support']
TWIST = CUTS[7]

X = 'series/thanks-randy/sfx/'
SFX = [
    (X + 'ice_creak.mp3', 0.10, 0.9),
    (X + 'ice_creak.mp3', 2.20, 0.6),
    (X + 'phone_dial.mp3', 5.10, 0.7),
    (X + 'phone_pickup.mp3', 6.65, 0.9),
    (X + 'man_snore.mp3', 10.40, 0.8),
    (X + 'phone_pickup.mp3', 10.98, 0.9),
    (X + 'sneaker_squeak.mp3', 13.40, 0.5),
    (X + 'twist_sting.mp3', 17.70, 0.7),
    (X + 'doorbell.mp3', 20.55, 0.7),
    (X + 'door_open.mp3', 20.95, 0.8),
    (X + 'crowd_shuffle.mp3', 21.10, 2.4),
    (X + 'bowl_set.mp3', 22.60, 0.8),
    (X + 'phone_rec.mp3', 22.75, 3.0),
    (X + 'slippers.mp3', 25.55, 2.5),
    (X + 'ice_creak.mp3', 29.25, 0.7),
    (X + 'phone_pickup.mp3', 32.85, 0.6),
]

BEDS = [
    ('series/thanks-randy/sfx/kitchen_night_loop.mp3', 8.0, 0.0, DUR, 6.0, True),
    ('series/thanks-randy/sfx/hair_dryer_loop.mp3', 4.0, 0.0, 4.80, 0.22, True),
    ('series/thanks-randy/music/randy_theme_phone.mp3', 15.0, 6.75, 10.40, 0.30, True),
    ('series/thanks-randy/sfx/callcenter_amb_loop.mp3', 8.0, 11.00, 17.72, 0.25, True),
    ('series/thanks-randy/sfx/many_dryers.mp3', 3.0, 17.72, 20.52, 0.26, True),
    ('series/thanks-randy/sfx/many_dryers.mp3', 3.0, 22.70, 25.62, 0.18, True),
    ('series/thanks-randy/sfx/hair_dryer_loop.mp3', 4.0, 32.85, DUR, 0.25, False),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 1.65, 6.70, 0.20, True),
    ('series/thanks-randy/music/randy_theme_15s.mp3', 15.0, 20.52, 32.80, 0.20, True),
]

VFX = {'scandee': 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.3',
       'carol': 'highpass=f=260,lowpass=f=4200'}
VGAIN = {'randy': 1.5, 'tom': 1.65, 'carol': 1.6, 'carol2': 1.6, 'brayden': 1.55, 'joyce': 1.6, 'scandee': 1.35}
