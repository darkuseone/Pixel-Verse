"""S01E02 «$95 TO APPLY?!» — timing for video (ep02.py) and audio (mix.py). Voice: tightened takes voice/ep02_t.
Sound design (earshot pass, /earshot): own foley (series/land-of-the-fee/sfx) + code-made bank sounds (sfx/es) + the kazoo march v2."""
DUR = 30.0
FPS = 30
SLUG = 'land-of-the-fee'
MASTER = 0.80
LUFS = -14.0

VOICE = [
    ('d1', 'ep02_t', 'd1', 0.00, 0.00, 2.79, 'duke', 'NINETY-FIVE bucks?! Just to APPLY?!'),
    ('m1', 'ep02_t', 'm1', 2.90, 0.00, 1.78, 'madison', 'Plus the AMENITY fee!'),
    ('d2', 'ep02_t', 'd2', 4.80, 0.00, 2.59, 'duke', "I'm a BALD EAGLE. I'm on the DOLLAR!"),
    ('s1', 'ep02_t', 's1', 7.51, 0.00, 1.76, 'sal', "Dollar's broke too."),
    ('f1', 'ep02_t', 'f1', 9.40, 0.00, 2.02, 'feebee', 'Sounds like you said — PET fee!'),
    ('d3', 'ep02_t', 'd3', 11.54, 0.00, 1.13, 'duke', "I'm not a PET!"),
    ('m2', 'ep02_t', 'm2', 12.79, 0.00, 2.19, 'madison', 'You have FEATHERS, sir.'),
    ('d4', 'ep02_t', 'd4', 15.10, 0.00, 2.34, 'duke', "Who's the LANDLORD?! I'll talk to HIM!"),
    ('s2', 'ep02_t', 's2', 17.56, 0.00, 2.97, 'sal', 'S.P. Holdings. Sal Pigeon.'),
    ('d5', 'ep02_t', 'd5', 20.65, 0.00, 1.62, 'duke', "You don't even PAY rent!"),
    ('s3', 'ep02_t', 's3', 22.39, 0.00, 2.72, 'sal', "Pigeons don't pay rent. We COLLECT it."),
    ('f2', 'ep02_t', 'f2', 25.25, 0.00, 2.01, 'feebee', 'Sounds like you said — RENEW!'),
    ('s4', 'ep02_t', 's4', 27.45, 0.00, 1.06, 'sal', 'Welcome home.'),
]

#       hook  amen  dollar tablet pet    lord   twist  rent   renew  button
CUTS = [0.0, 2.85, 4.75, 9.35, 11.50, 15.05, 17.50, 20.60, 25.20, 27.35, DUR]
NAMES = ['hook', 'amen', 'dollar', 'tablet', 'pet', 'lord', 'twist', 'rent', 'renew', 'button']
TWIST = 17.56

X = 'series/land-of-the-fee/sfx/'
E = X + 'es/'
SFX = [
    (X + 'table_slam.mp3', 0.04, 3.0),
    (E + 'hit_punch.wav', 0.04, 0.50),
    (E + 'hit_sub.wav', 0.04, 0.45),
    (X + 'feather_burst.mp3', 0.12, 6.0, None, None, -0.3),
    (E + 'swish_flick.wav', 2.74, 0.32),
    (E + 'hit_sub.wav', 2.85, 0.30),
    (E + 'hit_sub.wav', 11.52, 0.35),
    (E + 'hit_sub.wav', 15.08, 0.35),
    (E + 'hit_sub.wav', 20.64, 0.35),
    (X + 'duck_squeak.mp3', 3.55, 0.45, None, None, 0.1),
    (E + 'pop_step.wav', 4.20, 0.20, None, None, 0.5),
    (E + 'swell_short.wav', 4.51, 0.28),
    (X + 'feather_burst.mp3', 4.78, 4.0, None, None, 0.3),
    (X + 'keys_jingle.mp3', 7.30, 1.4, None, None, -0.5),
    (X + 'pigeon_coo.mp3', 9.20, 0.30, None, None, -0.5),
    (E + 'swish_flick.wav', 9.24, 0.28, None, None, 0.2),
    (E + 'chime_up4.wav', 9.37, 0.22),
    (E + 'pop_step.wav', 11.05, 0.30),
    (X + 'ka_ching.mp3', 11.07, 0.45),
    (E + 'hit_punch.wav', 11.56, 0.28, None, None, -0.3),
    (X + 'latte_slurp.mp3', 15.00, 0.55, None, None, 0.4),
    (X + 'feather_burst.mp3', 15.12, 4.0),
    (E + 'riser_snatch.wav', 17.12, 0.32),
    (E + 'whoosh_thump.wav', 17.38, 0.40),
    (E + 'sub_drop_twist.wav', 17.52, 0.65),
    (X + 'twist_sting.mp3', 17.50, 0.60),
    (X + 'keys_jingle.mp3', 17.60, 1.6, None, None, 0.2),
    (E + 'pop_soft.wav', 17.56, 0.22),
    (X + 'wing_flap.mp3', 18.30, 0.8, None, None, -0.5),
    (E + 'hit_punch.wav', 20.66, 0.28, None, None, -0.4),
    (X + 'keys_jingle.mp3', 23.70, 1.2, None, None, 0.3),
    (X + 'briefcase_snap.mp3', 24.70, 2.2, None, None, 0.3),
    (E + 'swish_flick.wav', 25.09, 0.26),
    (E + 'celesta_bb.wav', 25.22, 0.22),
    (X + 'ka_ching.mp3', 26.95, 0.65),
    (E + 'hit_sub.wav', 26.95, 0.35),
    (E + 'pop_wide.wav', 26.97, 0.22),
    (E + 'pop_soft.wav', 22.60, 0.20),
    (X + 'pigeon_coo.mp3', 27.30, 0.30, None, None, 0.2),
    (E + 'pop_soft.wav', 28.00, 0.20),
    (E + 'pop_wide.wav', 29.00, 0.30),                # end card «SUBSCRIBE!»
    (E + 'glock_d6.wav', 29.02, 0.22),
]

M = 'series/land-of-the-fee/music/freedom_kazoo_v2_16s.mp3'
HAAS = 'adelay=0|18'
STOP = "volume='if(between(t,17.10,17.52),0.30,1)':eval=frame"
BEDS = [
    (X + 'office_amb_loop.mp3', 8.0, 0.0, 2.85, 0.9, True, HAAS),
    (X + 'mall_amb_loop.mp3', 8.0, 2.85, 9.35, 0.8, True, HAAS),
    (X + 'office_amb_loop.mp3', 8.0, 9.35, 17.50, 0.9, True, HAAS),
    (X + 'roof_wind_loop.mp3', 8.0, 17.50, DUR, 0.8, True, HAAS),
    (M, 16.0, 0.30, DUR, 0.65, 0.70, 'equalizer=f=2000:t=q:w=1.4:g=-5,bass=g=4:f=70,' + STOP + ',' + HAAS),
]

VOICE_LUFS = -14.5
VFX = {'feebee': 'highpass=f=150,lowpass=f=8000,aecho=1.0:0.85:14:0.10'}
VGAIN = {'duke': 1.0, 'sal': 1.0, 'feebee': 1.0, 'madison': 1.0}
MASTER_EQ = 'equalizer=f=50:t=q:w=1.0:g=6,equalizer=f=90:t=q:w=1.0:g=2,equalizer=f=2400:t=q:w=1.2:g=-1.5'
