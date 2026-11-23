"""S01E01 «I WAS HOME!» (MOTION DETECTED, US) — timing for video (ep01.py) and audio (mix.py).
Voice: voice/ep01_t (tempo 1.10). Sound: ONLY real CC0 recordings (library/cc0/sfx) + FreePD (CC0) live-instrument music."""
DUR = 36.8
FPS = 30
SLUG = 'motion-detected'
LUFS = -14.0

_T = dict(g1=0.00, d1=3.05, g2=6.39, g3=9.05, d2=12.44, g4=15.93, d3=18.10, g5=22.25, t1=24.75, d5=27.40, g7=30.32, d6=32.00)
_D = dict(g1=3.00, d1=3.29, g2=2.61, g3=3.34, d2=1.99, g4=2.14, d3=4.10, g5=1.88, t1=2.48, d5=2.85, g7=1.38, d6=3.79)
_W = dict(g='glenn', d='doris', t='trent')
_TX = dict(g1="I was HOME! All DAY! And they leave me THIS?!", d1="You were home, Glenn. Nine hours. In the ROBE.",
           g2="I took a vacation day to sign for Linda's GIFT!", g3="I had a SYSTEM. Chair. Coffee. Eyes on that DOOR.",
           d2="Correct. Let's watch two-fourteen.", g4="He was RIGHT there. Why didn't it RING?",
           d3="Do Not Disturb, Glenn. You set it Monday. For SOLICITORS.", g5="Unmute it! Unmute it NOW!",
           t1="Hi there! Got a minute to talk about SOLAR?", d5="Muted. Oh, and the depot closes at FIVE.",
           g7="It's four fifty-EIGHT!", d6="Motion detected. Glenn. Running. In the ROBE.")
VOICE = [(k, 'ep01_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

#        hook  doris  phone  flash  dcu   foot   g4     twist  g5     trent  dcu2   watch  run
CUTS = [0.0, 3.05, 6.39, 9.05, 12.44, 14.43, 15.93, 18.10, 22.25, 24.15, 27.40, 30.32, 31.75, DUR]
NAMES = ['hook', 'doris', 'phone', 'flash', 'dcu', 'foot', 'g4', 'twist', 'g5', 'trent', 'dcu2', 'watch', 'run']
TWIST = CUTS[7]                  # 18.10 / 36.8 = 49 % (the reveal itself starts on the footage at 14.43)
DING = 24.20

L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'paper_handle.mp3', 0.00, 0.80),            # the tag rattles in his hand
    (L + 'sms_message.mp3', 2.95, 0.45),              # Doris chime before she talks
    (L + 'phone_key_click.mp3', 6.40, 0.70),
    (L + 'whoosh_1.mp3', 8.95, 0.35),
    (L + 'chair_creak.mp3', 9.20, 0.80),
    (L + 'bottle_clink.mp3', 10.6, 0.35),             # coffee mug
    (L + 'sms_message.mp3', 12.38, 0.45),
    (L + 'vinyl_scratch.mp3', 14.38, 0.45),           # rewind into the footage
    (L + 'steps_concrete.mp3', 14.50, 0.70),
    (L + 'light_switch_click.mp3', 14.95, 0.80),      # the button: click... and silence
    (L + 'paper_handle.mp3', 15.20, 0.80),            # tag slapped on the door
    (L + 'whoosh_3.mp3', 15.45, 0.60),                # courier gone
    (L + 'gong_strong.mp3', 18.10, 0.35),             # TWIST hit
    (L + 'doorbell_3.mp3', DING, 0.95),               # finally it rings — for Trent
    (L + 'steps_wood_floor.mp3', 23.95, 0.50),
    (L + 'sms_message.mp3', 27.32, 0.45),
    (L + 'rimshot_joke.mp3', 30.20, 0.30),
    (L + 'slipper_steps.mp3', 31.75, 0.95),           # the sprint
    (L + 'whoosh_1.mp3', 31.80, 0.45),
    (L + 'small_dog_bark.mp3', 33.4, 0.35),           # a neighbor's dog joins the chase
    (L + 'slipper_steps.mp3', 33.0, 0.70),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_busybody.mp3', 10.0, 0.0, 14.40, 0.80, True, VOICE_DIP),
    (CM + 'freepd_lurking_sloth.mp3', 157.8, 14.40, TWIST - 0.05, 0.85, True, VOICE_DIP),
    (CM + 'freepd_fensters_explanation.mp3', 168.9, TWIST + 0.6, 30.30, 0.70, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, 31.70, DUR, 0.85, True, VOICE_DIP),
]
VGAIN = {'glenn': 2.0, 'doris': 2.1, 'trent': 1.9}
