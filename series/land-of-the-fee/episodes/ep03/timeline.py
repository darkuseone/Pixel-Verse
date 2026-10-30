"""S01E03 «$40 FOR A HUG?!» — timing for video (ep03.py) and audio (mix.py). Voice: tightened takes voice/ep03_t.
Sound design (earshot pass, /earshot): own foley (series/land-of-the-fee/sfx) + code-made bank sounds (sfx/es) + the kazoo march v2."""
DUR = 30.8
FPS = 30
SLUG = 'land-of-the-fee'
MASTER = 0.80
LUFS = -14.0

VOICE = [
    ('d1', 'ep03_t', 'd1', 0.00, 0.00, 2.21, 'duke', 'FORTY bucks?! For a HUG?!'),
    ('d2', 'ep03_t', 'd2', 5.30, 0.00, 2.59, 'duke', "I'm a BALD EAGLE. I'm on the DOLLAR!"),
    ('s1', 'ep03_t', 's1', 8.01, 0.00, 1.94, 'sal', "Dollar don't cover THIS."),
    ('f1', 'ep03_t', 'f1', 10.10, 0.00, 3.50, 'feebee', "Sounds like you said — PRE-EXISTING! Doctor's note, please!"),
    ('d3', 'ep03_t', 'd3', 13.72, 0.00, 1.35, 'duke', 'Doc! A NOTE!'),
    ('c1', 'ep03_t', 'c1', 15.19, 0.00, 2.14, 'chuck', 'I need your INSURANCE approval first.'),
    ('c2', 'ep03_t', 'c2', 17.55, 0.00, 1.51, 'chuck', 'Doctor says YES.'),
    ('c3', 'ep03_t', 'c3', 19.65, 0.00, 1.72, 'chuck', 'Insurance says NO.'),
    ('d4', 'ep03_t', 'd4', 21.55, 0.00, 1.98, 'duke', 'So who do I CALL?'),
    ('c4', 'ep03_t', 'c4', 23.65, 0.00, 0.62, 'chuck', 'Me.'),
    ('n1', 'ep03_t', 'n1', 24.90, 0.00, 2.08, 'nurse', 'Aww. Come here, sweetie.'),
    ('s2', 'ep03_t', 's2', 27.20, 0.00, 2.41, 'sal', "Don't hug her BACK. That's double."),
]

#       hook  flash hug   dollar phone  doc    twist  wide   call   me     faint  button
CUTS = [0.0, 2.30, 3.95, 5.25, 10.00, 13.65, 17.40, 18.20, 21.45, 23.55, 24.35, 27.05, DUR]
NAMES = ['hook', 'flash', 'hug', 'dollar', 'phone', 'doc', 'twist', 'wide', 'call', 'me', 'faint', 'button']
TWIST = 17.42
SMACK = 3.45

X = 'series/land-of-the-fee/sfx/'
E = X + 'es/'
SFX = [
    (X + 'monitor_beep.mp3', 0.00, 2.0),
    (E + 'hit_punch.wav', 0.04, 0.50),
    (E + 'hit_sub.wav', 0.04, 0.45),
    (X + 'feather_burst.mp3', 0.12, 6.0, None, None, -0.2),
    (E + 'whoosh_cape.wav', 2.30 + 0.037 - 0.6 + 0.4, 0.40),
    (X + 'wing_flap.mp3', 2.35, 0.8, None, None, -0.5),
    (X + 'glass_smack.mp3', SMACK, 2.4, None, None, 0.4),
    (E + 'impact_short.wav', SMACK, 0.45, None, None, 0.4),
    (E + 'hit_sub.wav', SMACK, 0.40),
    (X + 'feather_burst.mp3', SMACK + 0.02, 6.0, None, None, 0.4),
    (E + 'glitch_mid.wav', 3.92, 0.20),
    (X + 'hug_rustle.mp3', 4.05, 8.0, None, None, -0.2),
    (X + 'printer_receipt.mp3', 4.30, 1.2, None, None, 0.5),
    (X + 'ka_ching.mp3', 4.70, 0.55, None, None, 0.4),
    (E + 'pop_step.wav', 4.72, 0.22),
    (E + 'swell_short.wav', 5.00, 0.26),
    (X + 'feather_burst.mp3', 5.30, 4.0),
    (X + 'monitor_beep.mp3', 6.80, 1.5, None, None, -0.4),
    (X + 'pigeon_coo.mp3', 7.85, 0.30, None, None, 0.2),
    (E + 'swish_flick.wav', 9.89, 0.28),
    (E + 'chime_up4.wav', 10.02, 0.22),
    (E + 'pop_step.wav', 12.80, 0.28),
    (X + 'ka_ching.mp3', 12.82, 0.40),
    (E + 'swish_flick.wav', 13.54, 0.25),
    (E + 'hit_punch.wav', 13.74, 0.28, None, None, -0.3),
    (X + 'monitor_beep.mp3', 15.10, 1.5, None, None, 0.3),
    (E + 'riser_snatch.wav', 17.03, 0.32),
    (E + 'sub_drop_twist.wav', 17.42, 0.65),
    (X + 'twist_sting.mp3', 17.40, 0.60),
    (E + 'pop_soft.wav', 17.45, 0.22),
    (X + 'desk_phone_ring.mp3', 17.45, 0.30, None, None, 0.5),
    (E + 'whoosh_tight.wav', 18.04, 0.55),
    (E + 'pop_soft.wav', 18.20, 0.18),
    (X + 'chair_roll.mp3', 19.20, 3.0, None, None, 0.3),
    (E + 'swish_flick.wav', 21.34, 0.22),
    (X + 'monitor_beep.mp3', 21.50, 1.5, None, None, -0.3),
    (E + 'whoosh_tight.wav', 23.43, 0.28),
    (E + 'hit_sub.wav', 23.65, 0.35),
    (X + 'body_flop.mp3', 24.45, 3.0),
    (X + 'hug_rustle.mp3', 24.70, 8.0),
    (E + 'pop_soft.wav', 24.40, 0.20),
    (X + 'printer_receipt.mp3', 26.20, 1.2, None, None, 0.5),
    (X + 'ka_ching.mp3', 26.62, 0.60, None, None, 0.4),
    (E + 'hit_sub.wav', 26.62, 0.35),
    (E + 'pop_wide.wav', 26.64, 0.22),
    (X + 'pigeon_coo.mp3', 27.05, 0.28, None, None, 0.2),
    (E + 'pop_soft.wav', 28.80, 0.20),
    (E + 'pop_wide.wav', 29.80, 0.30),                # end card «SUBSCRIBE!»
    (E + 'glock_d6.wav', 29.82, 0.22),
]

M = 'series/land-of-the-fee/music/freedom_kazoo_v2_16s.mp3'
HAAS = 'adelay=0|18'
STOP = "volume='if(between(t,3.20,3.45)+between(t,17.02,17.42),0.30,1)':eval=frame"
BEDS = [
    (X + 'er_amb_loop.mp3', 8.0, 0.0, 2.30, 0.9, True, HAAS),
    (X + 'mall_amb_loop.mp3', 8.0, 2.30, 3.95, 0.8, True, HAAS),
    (X + 'er_amb_loop.mp3', 8.0, 3.95, 17.40, 0.9, True, HAAS),
    (X + 'office_amb_loop.mp3', 8.0, 17.40, 21.45, 0.9, True, HAAS),
    (X + 'er_amb_loop.mp3', 8.0, 21.45, 23.55, 0.9, True, HAAS),
    (X + 'office_amb_loop.mp3', 8.0, 23.55, 24.35, 0.9, True, HAAS),
    (X + 'er_amb_loop.mp3', 8.0, 24.35, DUR, 0.9, True, HAAS),
    (M, 16.0, 0.30, DUR, 0.65, 0.70, 'equalizer=f=2000:t=q:w=1.4:g=-5,bass=g=4:f=70,' + STOP + ',' + HAAS),
]

VOICE_LUFS = -14.5
VFX = {'feebee': 'highpass=f=150,lowpass=f=8000,aecho=1.0:0.85:14:0.10'}
VGAIN = {'duke': 1.0, 'sal': 1.0, 'feebee': 1.0, 'chuck': 1.0, 'nurse': 1.0}
MASTER_EQ = 'equalizer=f=50:t=q:w=1.0:g=6,equalizer=f=90:t=q:w=1.0:g=2,equalizer=f=2400:t=q:w=1.2:g=-1.5'
