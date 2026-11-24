"""S01E03 «$25 LIMIT?!» (MOTION DETECTED, US) — timing for video (ep03.py) and audio (mix.py).
Voice: voice/ep03_t (m2 is not used: the steals are a visual montage). Sound: CC0 + FreePD."""
DUR = 36.1
FPS = 30
SLUG = 'motion-detected'
LUFS = -14.0

_T = dict(g1=0.00, m1=3.24, g2=7.64, d1=11.14, g3=17.15, e1=19.75, d2=22.75, m3=25.60, t1=28.35, e2=31.70)
_D = dict(g1=3.19, m1=4.35, g2=3.45, d1=4.38, g3=1.94, e1=2.87, d2=2.73, m3=2.61, t1=2.49, e2=3.40)
_W = dict(g='glenn', d='doris', e='doris', m='marcy', t='trent')
_TX = dict(g1="Twenty-five dollar LIMIT! And Kyle brought a SCRATCH-OFF?!",
           m1="White Elephant rules, Glenn! Any gift can be STOLEN. Three times, max!",
           g2="I have a SYSTEM. Let them fight. I steal LAST.", d1="Motion detected. Glenn. Staring at the GOLD box. Like a hawk.",
           g3="Sorry, Marcy. It's MINE!", e1="Motion detected. Glenn. Opening ME.", d2="Oh no. There's TWO of us now.",
           m3="Who brings a DOORBELL to a gift exchange?", t1="That's me! Got a minute to talk about SOLAR?",
           e2="Motion detected. Glenn. Regifting ME.")
VOICE = [(k, 'ep03_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

MONT = 15.55
RIP = 19.15
#        hook  marcy  whisper phone  mont   grab   twist  dcu    m3     trent  slide
CUTS = [0.0, 3.24, 7.64, 11.14, 15.55, 17.15, RIP, 22.70, 25.55, 28.30, 30.88, DUR]
NAMES = ['hook', 'marcy', 'whisper', 'phone', 'mont', 'grab', 'twist', 'dcu', 'm3', 'trent', 'slide']
TWIST = RIP                      # 19.15 / 36.1 = 53 %

L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'paper_handle.mp3', 0.05, 0.75),             # the scratch-off flaps
    (L + 'party_horn.mp3', 3.20, 0.40),
    (L + 'cloth_rustle.mp3', 7.70, 0.45),
    (L + 'sms_message.mp3', 11.06, 0.45),             # Doris chime (from the phone)
    (L + 'whoosh_1.mp3', 15.55, 0.50),                # steal 1
    (L + 'paper_crumple.mp3', 15.70, 0.45),
    (L + 'whoosh_3.mp3', 16.30, 0.50),                # steal 2
    (L + 'party_horn.mp3', 16.40, 0.30),
    (L + 'whoosh_1.mp3', 17.10, 0.45),
    (L + 'paper_crumple.mp3', RIP - 0.05, 0.95),      # the rip
    (L + 'gong_strong.mp3', RIP + 0.15, 0.30),
    (L + 'sms_message.mp3', 19.60, 0.55),             # the second doorbell boots up
    (L + 'sms_message.mp3', 22.62, 0.40),
    (L + 'vinyl_scratch.mp3', 25.50, 0.30),
    (L + 'chair_creak.mp3', 28.25, 0.40),             # Trent pops over the partition
    (L + 'cloth_rustle.mp3', 30.95, 0.55),            # Glenn slides the box back
    (L + 'paper_handle.mp3', 31.30, 0.50),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_busybody.mp3', 55.0, 0.0, MONT - 0.05, 0.80, True, VOICE_DIP),
    (CM + 'freepd_managing_mischief.mp3', 40.0, MONT - 0.05, RIP - 0.05, 0.85, True, VOICE_DIP),
    (CM + 'freepd_fensters_explanation.mp3', 168.9, RIP + 0.6, 30.85, 0.70, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, 30.85, DUR, 0.85, True, VOICE_DIP),
]
VGAIN = {'glenn': 2.0, 'doris': 2.1, 'trent': 1.9, 'marcy': 1.9}
