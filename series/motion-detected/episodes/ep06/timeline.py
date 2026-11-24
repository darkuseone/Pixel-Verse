"""S01E06 «FINAL ATTEMPT!» (MOTION DETECTED, US; season finale) — timing for video (ep06.py) and audio (mix.py). Voice: voice/ep06_t."""
DUR = 33.6
FPS = 30
SLUG = 'motion-detected'
LUFS = -14.0

_T = dict(g1=0.00, d1=3.45, t1=7.75, t2=10.62, g2=13.65, u1=16.55, d2=21.00, g3=25.40, d3=27.75)
_D = dict(g1=3.40, d1=3.81, t1=2.80, t2=2.95, g2=2.51, u1=4.34, d2=4.31, g3=2.19, d3=3.87)
_W = dict(g='glenn', d='doris', t='trent', u='ultra')
_TX = dict(g1="Final attempt. Six A.M. Nobody gets past ME.", d1="Motion detected. Glenn. Slept on the porch. In the ROBE.",
           t1="Morning, Glenn! New job. Got a minute to SIGN?", t2="Sign here. And here. And HERE. And one for the SOLAR.",
           g2="I SIGNED! Linda! Your gift is HERE!", u1="ULTRA online. Previous doorbell: obsolete. Deleting DORIS.",
           d2="Oh. That's fine. Motion detected. Glenn. Replacing ME.", g3="Nah. Trent? Return to SENDER.",
           d3="Motion detected. Glenn. Being a good GUY. In the ROBE.")
VOICE = [(k, 'ep06_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

VAN = 7.30
OPEN = 16.20
TWIST = 16.55                    # the gift is Doris's replacement — 16.55 / 33.6 = 49 %
S2 = 31.70
#        hook  doris  trent  sign   gift   twist  dsad   tag    bye
CUTS = [0.0, 3.45, VAN, 10.60, 13.60, TWIST, 21.00, 25.35, 27.70, DUR]
NAMES = ['hook', 'doris', 'trent', 'sign', 'gift', 'twist', 'dsad', 'tag', 'bye']

L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'yawn_man.mp3', 0.00, 0.35),
    (L + 'zipper.mp3', 0.30, 0.60),                   # the sleeping bag
    (L + 'sms_message.mp3', 3.38, 0.40),
    (L + 'car_arrive_stop.mp3', VAN - 0.3, 0.80),
    (L + 'steps_concrete.mp3', VAN + 0.3, 0.70),
    (L + 'pencil_sign.mp3', 10.70, 0.80), (L + 'pencil_sign.mp3', 11.60, 0.80), (L + 'pencil_sign.mp3', 12.50, 0.80),
    (L + 'party_horn.mp3', 13.70, 0.45),
    (L + 'paper_crumple.mp3', OPEN - 0.1, 0.80),
    (L + 'gong_strong.mp3', TWIST, 0.30),
    (L + 'sms_message.mp3', 20.92, 0.30),
    (L + 'paper_handle.mp3', 25.90, 0.80),            # the tag on ULTRA
    (L + 'steps_concrete.mp3', 27.90, 0.55),
    (L + 'sms_message.mp3', 27.66, 0.50),
    (L + 'party_horn.mp3', S2, 0.40),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_baltic_levity.mp3', 70.0, 0.0, VAN - 0.05, 0.80, True, VOICE_DIP),
    (CM + 'freepd_busybody.mp3', 140.0, VAN - 0.05, TWIST - 0.05, 0.80, True, VOICE_DIP),
    (CM + 'freepd_fensters_explanation.mp3', 168.9, TWIST + 0.6, 25.30, 0.70, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, 25.30, DUR, 0.85, True, VOICE_DIP),
]
VGAIN = {'glenn': 2.0, 'doris': 2.1, 'trent': 1.9, 'ultra': 2.0}
