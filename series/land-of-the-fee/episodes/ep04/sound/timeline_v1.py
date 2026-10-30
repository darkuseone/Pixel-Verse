"""S01E04 «$400 A MONTH?!» — timing for video (ep04.py) and audio (mix.py). Voice: tightened takes voice/ep04_t.
Sound design (earshot pass, /earshot): own foley (series/land-of-the-fee/sfx) + code-made bank sounds (sfx/es) + the kazoo march v2."""
DUR = 33.0
FPS = 30
SLUG = 'land-of-the-fee'
MASTER = 0.80
LUFS = -14.0

VOICE = [
    ('d1', 'ep04_t', 'd1', 0.00, 0.00, 3.29, 'duke', "FOUR HUNDRED a month?! It's a 2009 HATCHBACK!"),
    ('f1', 'ep04_t', 'f1', 3.40, 0.00, 2.50, 'feebee', 'Sounds like you said — ADD a DRIVER!'),
    ('d2', 'ep04_t', 'd2', 6.02, 0.00, 2.55, 'duke', "I'm a BALD EAGLE. I'm on the DOLLAR!"),
    ('s2', 'ep04_t', 's2', 8.68, 0.00, 2.10, 'sal', "Dollar can't afford gas either."),
    ('d3', 'ep04_t', 'd3', 10.90, 0.00, 3.02, 'duke', "Eagles don't NEED cars! Sal, hit the SCREAM!"),
    ('d4', 'ep04_t', 'd4', 15.05, 0.00, 2.45, 'duke', 'No insurance! No GAS!'),
    ('o1', 'ep04_t', 'o1', 17.55, 0.00, 2.47, 'officer', 'Unregistered DRONE! Land NOW!'),
    ('o2', 'ep04_t', 'o2', 20.20, 0.00, 3.37, 'officer', 'No flight plan. No license. No AIRCRAFT insurance.'),
    ('o3', 'ep04_t', 'o3', 23.70, 0.00, 1.67, 'officer', "That's nine hundred a MONTH."),
    ('d5', 'ep04_t', 'd5', 25.48, 0.00, 1.15, 'duke', "I'm a BIRD!"),
    ('o4', 'ep04_t', 'o4', 26.75, 0.00, 1.90, 'officer', "Birds got a PILOT'S license?"),
    ('s3', 'ep04_t', 's3', 28.85, 0.00, 2.22, 'sal', 'Need a ride? Twenty BUCKS.'),
]

#       hook  dash  dollar sell   takeoff soar   twist  ticket bird   button
CUTS = [0.0, 3.35, 5.95, 10.85, 13.95, 15.00, 17.50, 20.10, 25.40, 28.75, DUR]
NAMES = ['hook', 'dash', 'dollar', 'sell', 'takeoff', 'soar', 'twist', 'ticket', 'bird', 'button']
TWIST = 17.55
SCREAM = 13.95

X = 'series/land-of-the-fee/sfx/'
E = X + 'es/'
SFX = [
    (X + 'engine_sputter.mp3', 0.00, 0.35),
    (E + 'hit_punch.wav', 0.04, 0.50),
    (E + 'hit_sub.wav', 0.04, 0.45),
    (X + 'feather_burst.mp3', 0.12, 6.0),
    (E + 'swish_flick.wav', 3.24, 0.28),
    (E + 'chime_up4.wav', 3.38, 0.22),
    (E + 'pop_step.wav', 5.30, 0.28),
    (X + 'ka_ching.mp3', 5.32, 0.45),
    (E + 'swell_short.wav', 5.72, 0.26),
    (X + 'feather_burst.mp3', 6.05, 4.0),
    (X + 'drone_buzz_loop.mp3', 7.60, 0.10, 0.0, 1.6, 0.6),          # the clue: a Sky Patrol drone passes far behind
    (X + 'pigeon_coo.mp3', 8.50, 0.28, None, None, 0.4),
    (X + 'car_door_creak.mp3', 10.90, 1.2, None, None, -0.3),
    (E + 'knock_wood.wav', 11.40, 0.25),
    (X + 'speaker_click.mp3', 13.70, 8.0, None, None, 0.4),
    (X + 'hawk_scream.mp3', SCREAM, 1.0),
    (X + 'wing_flap.mp3', SCREAM + 0.05, 1.0),
    (E + 'whoosh_cape.wav', SCREAM - 0.2, 0.45),
    (X + 'feather_burst.mp3', SCREAM + 0.1, 5.0),
    (X + 'wing_flap.mp3', 15.10, 0.7, None, None, -0.3),
    (X + 'whoosh_fly.mp3', 15.70, 0.6),
    (X + 'police_siren.mp3', 17.20, 0.75, None, None, 0.4),
    (E + 'sub_drop_twist.wav', 17.50, 0.65),
    (X + 'twist_sting.mp3', 17.48, 0.55),
    (E + 'pop_soft.wav', 17.55, 0.22),
    (X + 'drone_buzz_loop.mp3', 17.50, 0.55, 0.0, 2.6, 0.3),
    (E + 'whoosh_tight.wav', 19.95, 0.30),
    (E + 'hit_punch.wav', 20.10, 0.40),                # Duke lands on the gravel
    (X + 'ticket_tear.mp3', 23.40, 0.8, None, None, 0.3),
    (E + 'pop_soft.wav', 20.30, 0.20),
    (E + 'pop_step.wav', 23.80, 0.25),
    (X + 'ka_ching.mp3', 23.82, 0.50),
    (E + 'hit_sub.wav', 23.82, 0.35),
    (E + 'hit_punch.wav', 25.50, 0.28, None, None, -0.3),
    (X + 'engine_sputter.mp3', 28.60, 0.35, None, None, 0.6),
    (X + 'car_honk.mp3', 31.12, 0.55, None, None, 0.2),
    (E + 'pop_soft.wav', 31.00, 0.20),
    (E + 'pop_wide.wav', 32.00, 0.30),                # end card «SUBSCRIBE!»
    (E + 'glock_d6.wav', 32.02, 0.22),
]

M = 'series/land-of-the-fee/music/freedom_kazoo_v2_16s.mp3'
HAAS = 'adelay=0|18'
STOP = "volume='if(between(t,17.12,17.52),0.30,1)':eval=frame"
BEDS = [
    (X + 'street_amb_loop.mp3', 8.0, 0.0, 15.00, 1.6, True, HAAS),
    (X + 'highway_amb_loop.mp3', 8.0, 15.00, 20.10, 0.5, True, HAAS),
    (X + 'highway_amb_loop.mp3', 8.0, 20.10, DUR, 0.6, True, HAAS),
    (M, 16.0, 0.30, DUR, 0.65, 0.70, 'equalizer=f=2000:t=q:w=1.4:g=-5,bass=g=4:f=70,' + STOP + ',' + HAAS),
]

VOICE_LUFS = -14.5
VFX = {'feebee': 'highpass=f=150,lowpass=f=8000,aecho=1.0:0.85:14:0.10'}
VGAIN = {'duke': 1.0, 'sal': 1.0, 'feebee': 1.0, 'officer': 1.0}
MASTER_EQ = 'equalizer=f=50:t=q:w=1.0:g=6,equalizer=f=90:t=q:w=1.0:g=2,equalizer=f=2400:t=q:w=1.2:g=-1.5'
