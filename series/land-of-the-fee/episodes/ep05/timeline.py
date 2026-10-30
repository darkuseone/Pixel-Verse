"""S01E05 «$600 NOSEBLEEDS?!» — timing for video (ep05.py) and audio (mix.py). Voice: tightened takes voice/ep05_t.
Sound design (earshot pass, /earshot): own foley (series/land-of-the-fee/sfx) + code-made bank sounds (sfx/es) + the kazoo march v2."""
DUR = 34.4
FPS = 30
SLUG = 'land-of-the-fee'
MASTER = 0.80
LUFS = -14.0

VOICE = [
    ('d1', 'ep05_t', 'd1', 0.00, 0.00, 2.38, 'duke', 'SIX HUNDRED?! For NOSEBLEEDS?!'),
    ('f1', 'ep05_t', 'f1', 2.46, 0.00, 3.20, 'feebee', "You're in the QUEUE! You are number — four MILLION!"),
    ('d2', 'ep05_t', 'd2', 5.74, 0.00, 2.52, 'duke', "I'm a BALD EAGLE. I'm on the DOLLAR!"),
    ('s1', 'ep05_t', 's1', 8.34, 0.00, 3.48, 'sal', "So you're face value. Nobody PAYS face value."),
    ('d3', 'ep05_t', 'd3', 11.90, 0.00, 1.44, 'duke', "What's a FEE fee?!"),
    ('f2', 'ep05_t', 'f2', 13.42, 0.00, 1.55, 'feebee', "It's the fee for the FEES!"),
    ('d4', 'ep05_t', 'd4', 15.05, 0.00, 2.39, 'duke', "Forget it. I'll get in like an EAGLE."),
    ('r1', 'ep05_t', 'r1', 17.55, 0.00, 2.40, 'rex', 'Six hundred. For my OWN show.'),
    ('r2', 'ep05_t', 'r2', 20.07, 0.00, 2.88, 'rex', "I've been screaming FOR you for forty years."),
    ('r3', 'ep05_t', 'r3', 23.05, 0.00, 2.16, 'rex', "Get me in, kid. I'll scream for you."),
    ('f3', 'ep05_t', 'f3', 29.00, 0.00, 3.18, 'feebee', 'Two birds detected! TWO tickets! Plus FEES!'),
    ('s2', 'ep05_t', 's2', 32.40, 0.00, 1.29, 'sal', 'Majestic.'),
]

#       hook  queue dollar cart   wall   twist  rex    stage  jumbo  button
CUTS = [0.0, 2.42, 5.70, 11.86, 15.00, 17.50, 20.00, 25.30, 28.85, 32.25, DUR]
NAMES = ['hook', 'queue', 'dollar', 'cart', 'wall', 'twist', 'rex', 'stage', 'jumbo', 'button']
TWIST = 17.55
REX_SCREAM = 25.55
CHIRP = (27.30, 28.45)

X = 'series/land-of-the-fee/sfx/'
E = X + 'es/'
SFX = [
    (X + 'laptop_typing.mp3', 0.00, 1.4),
    (E + 'hit_punch.wav', 0.04, 0.50),
    (E + 'hit_sub.wav', 0.04, 0.45),
    (X + 'feather_burst.mp3', 0.12, 6.0),
    (E + 'swish_flick.wav', 2.31, 0.28),
    (E + 'chime_up4.wav', 2.44, 0.22),
    (E + 'swell_short.wav', 5.45, 0.26),
    (X + 'feather_burst.mp3', 5.76, 4.0),
    (X + 'fry_munch.mp3', 8.10, 5.0, None, None, 0.5),
    (E + 'swish_flick.wav', 11.75, 0.26),
    (E + 'pop_step.wav', 12.00, 0.24), (E + 'pop_step.wav', 12.55, 0.24), (E + 'pop_step.wav', 13.10, 0.24), (E + 'pop_step.wav', 13.65, 0.28),
    (X + 'ka_ching.mp3', 14.20, 0.50),
    (E + 'hit_sub.wav', 14.20, 0.35),
    (E + 'whoosh_cape.wav', 15.00 + 0.037 - 0.6 + 0.6, 0.45),
    (X + 'wing_flap.mp3', 15.10, 0.9, None, None, -0.4),
    (X + 'wing_flap.mp3', 16.30, 0.7, None, None, 0.3),
    (E + 'riser_snatch.wav', 17.16, 0.32),
    (E + 'sub_drop_twist.wav', 17.55, 0.65),
    (X + 'twist_sting.mp3', 17.52, 0.55),
    (E + 'pop_soft.wav', 17.58, 0.22),
    (E + 'whoosh_tight.wav', 25.15, 0.40),
    (X + 'guitar_chord.mp3', 25.30, 0.8),
    (X + 'hawk_scream.mp3', REX_SCREAM, 0.85),
    (X + 'crowd_roar.mp3', 26.30, 0.55),
    (X + 'mic_feedback.mp3', 27.10, 0.20, None, None, 0.3),
    (X + 'eagle_chirp.mp3', CHIRP[0], 1.2),
    (X + 'crowd_roar_big.mp3', 28.20, 0.55),
    (E + 'pop_soft.wav', 25.90, 0.20),
    (E + 'chime_up4.wav', 28.95, 0.22),
    (E + 'swish_flick.wav', 28.75, 0.26),
    (E + 'pop_step.wav', 29.20, 0.24),
    (X + 'ka_ching.mp3', 31.80, 0.60),
    (E + 'hit_sub.wav', 31.80, 0.35),
    (E + 'pop_wide.wav', 31.82, 0.22),
    (X + 'pigeon_coo.mp3', 32.20, 0.28, None, None, 0.2),
    (E + 'pop_soft.wav', 32.40, 0.20),
    (E + 'pop_wide.wav', 33.40, 0.30),                # end card «SUBSCRIBE!»
    (E + 'glock_d6.wav', 33.42, 0.22),
]

M = 'series/land-of-the-fee/music/freedom_kazoo_v2_16s.mp3'
HAAS = 'adelay=0|18'
STOP = "volume='if(between(t,17.15,17.55)+between(t,25.10,28.80),0.25,1)':eval=frame"     # the band plays live on stage: march steps back
BEDS = [
    (X + 'apt_amb_loop.mp3', 8.0, 0.0, 15.00, 0.9, True, HAAS),
    (X + 'stadium_amb_loop.mp3', 8.0, 15.00, 25.30, 0.8, True, HAAS),
    (X + 'arena_amb_loop.mp3', 8.0, 25.30, DUR, 0.35, True, HAAS),
    (M, 16.0, 0.30, DUR, 0.65, 0.70, 'equalizer=f=2000:t=q:w=1.4:g=-5,bass=g=4:f=70,' + STOP + ',' + HAAS),
]

VOICE_LUFS = -14.5
VFX = {'feebee': 'highpass=f=150,lowpass=f=8000,aecho=1.0:0.85:14:0.10'}
VGAIN = {'duke': 1.0, 'sal': 1.0, 'feebee': 1.0, 'rex': 1.0}
MASTER_EQ = 'equalizer=f=50:t=q:w=1.0:g=6,equalizer=f=90:t=q:w=1.0:g=2,equalizer=f=2400:t=q:w=1.2:g=-1.5'
