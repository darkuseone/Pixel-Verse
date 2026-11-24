"""S01E05 «IN-LAWS IN 1 HOUR?!» (MOTION DETECTED, US) — timing for video (ep05.py) and audio (mix.py). Voice: voice/ep05_t."""
DUR = 36.3
FPS = 30
SLUG = 'motion-detected'
LUFS = -14.0

_T = dict(g1=0.00, d1=3.45, g2=7.58, d2=10.60, g3=14.68, d3=17.75, r1=22.50, g4=25.76, t1=27.90, d4=30.50)
_D = dict(g1=3.40, d1=4.08, g2=2.93, d2=4.00, g3=3.00, d3=4.65, r1=3.21, g4=1.44, t1=2.46, d4=4.75)
_W = dict(g='glenn', d='doris', r='ron', t='trent')
_TX = dict(g1="Linda's parents in ONE hour?! This house needs a WEEK!", d1="Motion detected. Laundry pile. Moving. Oh, that's GLENN.",
           g2="I have a SYSTEM. Everything goes in ONE closet.", d2="Closet capacity: four hundred PERCENT. Door holding. For NOW.",
           g3="Fifty-nine minutes. Spotless. I'm a GENIUS.", d3="Motion detected. Ron. He's been in your driveway for FORTY minutes.",
           r1="Glenn. Pat's still in the car. Can I hide in your CLOSET?", g4="Ron, NOT the clos-",
           t1="Hi, guys! Got a minute to talk about SOLAR?", d4="Motion detected. Two men. One salesman. Under a LAUNDRY pile.")
VOICE = [(k, 'ep05_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

MONT = 10.55
TWIST = 20.50                    # «…for FORTY minutes»: the in-law dreads it too — 20.5 / 36.3 = 56 %
AVAL = 26.90                     # the closet bursts
#        hook  laundry sys    mont   clean  monitor ron    aval   heads  pile
CUTS = [0.0, 3.45, 7.58, MONT, 14.65, 17.72, 22.45, 25.74, 27.85, 30.45, DUR]
NAMES = ['hook', 'laundry', 'sys', 'mont', 'clean', 'monitor', 'ron', 'aval', 'heads', 'pile']

L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'phone_vibrate.mp3', 0.00, 0.70),
    (L + 'cloth_rustle.mp3', 3.50, 0.70),
    (L + 'cloth_rustle.mp3', 5.40, 0.80),             # Glenn pops out of the laundry
    (L + 'sms_message.mp3', 3.38, 0.40),
    (L + 'door_apartment_open.mp3', 7.60, 0.50),
    (L + 'whoosh_1.mp3', 10.60, 0.50), (L + 'whoosh_3.mp3', 11.30, 0.45), (L + 'whoosh_1.mp3', 12.00, 0.45),
    (L + 'whoosh_3.mp3', 12.70, 0.45), (L + 'whoosh_1.mp3', 13.40, 0.45),
    (L + 'clock_fast.mp3', 10.70, 0.40),
    (L + 'door_slam_2.mp3', 14.50, 0.80),             # shut!
    (L + 'floor_squeak.mp3', 15.80, 0.45),            # the door creaks under pressure
    (L + 'sms_message.mp3', 17.66, 0.40),
    (L + 'gong_strong.mp3', TWIST, 0.30),
    (L + 'door_unlock_open.mp3', 22.30, 0.80),
    (L + 'floor_squeak.mp3', 25.80, 0.55),
    (L + 'door_apartment_open.mp3', AVAL - 0.15, 0.70),
    (L + 'anvil_clank.mp3', AVAL + 0.05, 0.35),
    (L + 'canvas_bag_drop.mp3', AVAL + 0.20, 0.90),
    (L + 'boing_cartoon.mp3', AVAL + 0.45, 0.40),
    (L + 'canvas_bag_drop.mp3', AVAL + 0.70, 0.70),
    (L + 'rimshot_joke.mp3', 30.40, 0.25),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_busybody.mp3', 110.0, 0.0, MONT - 0.05, 0.80, True, VOICE_DIP),
    (CM + 'freepd_managing_mischief.mp3', 60.0, MONT - 0.05, 17.70, 0.85, True, VOICE_DIP),
    (CM + 'freepd_lurking_sloth.mp3', 157.8, 17.70, TWIST - 0.05, 0.85, True, VOICE_DIP),
    (CM + 'freepd_fensters_explanation.mp3', 168.9, TWIST + 0.6, AVAL - 0.1, 0.70, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, AVAL + 0.9, DUR, 0.85, True, VOICE_DIP),
]
VGAIN = {'glenn': 2.0, 'doris': 2.1, 'trent': 1.9, 'ron': 2.0}
