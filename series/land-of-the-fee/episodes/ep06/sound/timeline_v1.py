"""S01E06 «$89 TO SIT?!» (season finale) — timing for video (ep06.py) and audio (mix.py). Voice: tightened takes voice/ep06_t; the last
line is E01's very first scream (voice/ep01_t/d1) — the season loops back into the pilot.
Sound design (earshot pass, /earshot): own foley (series/land-of-the-fee/sfx) + code-made bank sounds (sfx/es) + the kazoo march v2."""
DUR = 31.0
FPS = 30
SLUG = 'land-of-the-fee'
MASTER = 0.80
LUFS = -14.0

VOICE = [
    ('d1', 'ep06_t', 'd1', 0.00, 0.00, 2.15, 'duke', 'EIGHTY-NINE bucks?! To SIT?!'),
    ('f1', 'ep06_t', 'f1', 2.25, 0.00, 2.95, 'feebee', 'Sounds like you said — CARRY-ON! Wings count!'),
    ('d2', 'ep06_t', 'd2', 5.30, 0.00, 2.58, 'duke', "I'm a BALD EAGLE. I'm on the DOLLAR!"),
    ('s1', 'ep06_t', 's1', 7.98, 0.00, 2.62, 'sal', 'Then fold in HALF. Like the dollar.'),
    ('d3', 'ep06_t', 'd3', 10.75, 0.00, 3.39, 'duke', "I'm an EAGLE. I'll fly MYSELF! Sal, the SCREAM!"),
    ('d4', 'ep06_t', 'd4', 14.90, 0.00, 2.25, 'duke', 'No fees. No bots.'),
    ('f2', 'ep06_t', 'f2', 17.30, 0.00, 2.55, 'feebee', 'Welcome to paradise, Duke! RESORT fee!'),
    ('s2', 'ep06_t', 's2', 22.10, 0.00, 2.35, 'sal', 'Got here free. Checked BAG.'),
    ('f3', 'ep06_t', 'f3', 24.60, 0.00, 1.97, 'feebee', 'Sounds like you said — UPGRADE!'),
    ('d5', 'ep01_t', 'd1', 26.80, 0.00, 1.33, 'duke', 'REPRESENTATIVE!!'),
]

#       hook  kiosk dollar fold   takeoff sea    twist  prices sal    upgrade button
CUTS = [0.0, 2.20, 5.25, 9.40, 10.75, 14.15, 17.25, 19.90, 22.05, 24.55, 26.70, DUR]
NAMES = ['hook', 'kiosk', 'dollar', 'fold', 'takeoff', 'sea', 'twist', 'prices', 'sal', 'upgrade', 'button']
TWIST = 17.30
SCREAM = 14.18
FOLD = 9.55
PRICES = (20.15, 20.75, 21.35)

X = 'series/land-of-the-fee/sfx/'
E = X + 'es/'
SFX = [
    (X + 'airport_ding.mp3', 0.00, 0.4),
    (E + 'hit_punch.wav', 0.04, 0.50),
    (E + 'hit_sub.wav', 0.04, 0.45),
    (X + 'feather_burst.mp3', 0.12, 6.0),
    (E + 'swish_flick.wav', 2.09, 0.28),
    (E + 'chime_up4.wav', 2.22, 0.22),
    (E + 'pop_step.wav', 4.60, 0.28),
    (X + 'ka_ching.mp3', 4.62, 0.45),
    (E + 'swell_short.wav', 5.00, 0.26),
    (X + 'feather_burst.mp3', 5.32, 4.0),
    (X + 'pigeon_coo.mp3', 7.80, 0.30, None, None, -0.3),
    (E + 'whoosh_tight.wav', 9.28, 0.30),
    (X + 'bag_sizer_squeeze.mp3', FOLD, 3.0, None, None, -0.3),
    (X + 'feather_burst.mp3', FOLD + 0.1, 6.0, None, None, -0.3),
    (E + 'pop_step.wav', FOLD + 0.4, 0.25),
    (X + 'ka_ching.mp3', FOLD + 0.42, 0.45),
    (X + 'feather_burst.mp3', 10.80, 5.0),
    (X + 'speaker_click.mp3', 13.90, 8.0, None, None, 0.4),
    (X + 'hawk_scream.mp3', SCREAM, 1.0),
    (X + 'wing_flap.mp3', SCREAM + 0.05, 1.0),
    (E + 'whoosh_cape.wav', SCREAM - 0.3, 0.45),
    (X + 'wing_flap.mp3', 15.40, 0.6),
    (E + 'knock_wood.wav', 16.30, 0.25),
    (E + 'celesta_bb.wav', 17.20, 0.25, None, None, 0.4),
    (E + 'riser_snatch.wav', 16.91, 0.30),
    (E + 'sub_drop_twist.wav', 17.30, 0.65),
    (X + 'twist_sting.mp3', 17.28, 0.55),
    (E + 'pop_soft.wav', 17.33, 0.22),
    (E + 'pop_step.wav', PRICES[0], 0.28), (X + 'ka_ching.mp3', PRICES[0] + 0.02, 0.40),
    (E + 'pop_step.wav', PRICES[1], 0.28), (X + 'ka_ching.mp3', PRICES[1] + 0.02, 0.42),
    (E + 'pop_wide.wav', PRICES[2], 0.30), (X + 'ka_ching.mp3', PRICES[2] + 0.02, 0.50), (E + 'hit_sub.wav', PRICES[2], 0.35),
    (X + 'cocktail_slurp.mp3', 21.90, 0.6, None, None, -0.3),
    (E + 'pop_soft.wav', 22.20, 0.20),
    (E + 'celesta_bb.wav', 24.52, 0.22, None, None, 0.3),
    (E + 'pop_step.wav', 25.60, 0.25), (X + 'ka_ching.mp3', 25.62, 0.45),
    (X + 'big_inhale.mp3', 26.30, 0.8),
    (E + 'hit_punch.wav', 26.80, 0.45),
    (E + 'hit_sub.wav', 26.80, 0.45),
    (X + 'feather_burst.mp3', 26.85, 6.0),
    (E + 'swell_short.wav', 27.80, 0.30),
    (E + 'pop_wide.wav', 28.30, 0.30),
    (E + 'pop_soft.wav', 29.00, 0.20),
    (E + 'pop_wide.wav', 30.00, 0.30),                # end card «SUBSCRIBE!»
    (E + 'glock_d6.wav', 30.02, 0.22),
]

M = 'series/land-of-the-fee/music/freedom_kazoo_v2_16s.mp3'
HAAS = 'adelay=0|18'
STOP = "volume='if(between(t,16.90,17.30)+between(t,26.40,26.80),0.30,1)':eval=frame"
BEDS = [
    (X + 'terminal_amb_loop.mp3', 8.0, 0.0, 14.15, 0.9, True, HAAS),
    (X + 'waves_loop.mp3', 8.0, 14.15, DUR, 0.45, True, HAAS),
    (M, 16.0, 0.30, DUR, 0.65, 0.70, 'equalizer=f=2000:t=q:w=1.4:g=-5,bass=g=4:f=70,' + STOP + ',' + HAAS),
]

VOICE_LUFS = -14.5
VFX = {'feebee': 'highpass=f=150,lowpass=f=8000,aecho=1.0:0.85:14:0.10'}
VGAIN = {'duke': 1.0, 'sal': 1.0, 'feebee': 1.0}
MASTER_EQ = 'equalizer=f=50:t=q:w=1.0:g=6,equalizer=f=90:t=q:w=1.0:g=2,equalizer=f=2400:t=q:w=1.2:g=-1.5'
