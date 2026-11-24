"""S01E04 «$38 TO SHIP A MUG?!» (MOTION DETECTED, US) — timing for video (ep04.py) and audio (mix.py).
Voice: voice/ep04_t. Sound: CC0 + FreePD."""
DUR = 32.2
FPS = 30
SLUG = 'motion-detected'
LUFS = -14.0

_T = dict(g1=0.00, c1=2.93, g2=6.84, d1=8.96, g3=13.90, m1=17.70, d2=21.50, t1=26.20)
_D = dict(g1=2.87, c1=3.85, g2=2.06, d1=4.85, g3=3.30, m1=3.69, d2=2.16, t1=3.15)
_W = dict(g='glenn', c='clerk', d='doris', m='mom', t='trent')
_TX = dict(g1="Thirty-eight dollars to ship an EIGHT dollar mug?!", c1="Ground shipping. Arrives after Christmas. NEXT.",
           g2="I have a SYSTEM. I'll drive it MYSELF.", d1="Motion detected. Glenn. Driving six hours. To save thirty BUCKS.",
           g3="Two in the morning. Mom's house. Mission COMPLETE.",
           m1="Hi, sweetie! Mommy's on Do Not Disturb. Leave it by the GNOME!", d2="Huh. Wonder where she learned THAT.",
           t1="Glenn! Your mom said YES to solar. Want some PIE?")
VOICE = [(k, 'ep04_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

PRESS = 17.30                    # Glenn presses mom's doorbell: a click, the moon, no ring
TAGB = 23.75                     # he writes his own tag
DOOR = 25.80                     # the door opens — Trent with pie
#        hook   clerk  sys    map    mom    press  window dcu    tag    door
CUTS = [0.0, 2.93, 6.84, 8.96, 13.90, PRESS, 19.20, 21.50, TAGB, DOOR, DUR]
NAMES = ['hook', 'clerk', 'sys', 'map', 'mom', 'press', 'window', 'dcu', 'tag', 'door']
TWIST = PRESS                    # 17.3 / 32.2 = 54 %

L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'bottle_clink.mp3', 0.05, 0.50),             # the mug on the counter
    (L + 'calc_printer.mp3', 3.00, 0.55),             # the label printer
    (L + 'pencil_sign.mp3', 5.80, 0.50),
    (L + 'bus_horn.mp3', 8.90, 0.25),                 # the road
    (L + 'car_arrive_stop.mp3', 9.20, 0.40),
    (L + 'clock_fast.mp3', 10.0, 0.45),
    (L + 'sms_message.mp3', 8.88, 0.45),
    (L + 'car_arrive_stop.mp3', 13.40, 0.55),         # arrives at mom's
    (L + 'snow_steps.mp3', 14.0, 0.70),
    (L + 'light_switch_click.mp3', PRESS, 1.00),      # the button: click... and nothing
    (L + 'gong_strong.mp3', PRESS + 0.25, 0.30),
    (L + 'doorbell_2.mp3', 17.55, 0.25),              # the doorbell's own recorded chime
    (L + 'sms_message.mp3', 21.42, 0.40),
    (L + 'pencil_sign.mp3', TAGB + 0.1, 0.90),        # he writes his own tag
    (L + 'paper_handle.mp3', TAGB + 1.3, 0.80),
    (L + 'door_unlock_open.mp3', DOOR - 0.15, 0.95),
    (L + 'rimshot_joke.mp3', 29.40, 0.25),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_busybody.mp3', 80.0, 0.0, 8.90, 0.80, True, VOICE_DIP),
    (CM + 'freepd_baltic_levity.mp3', 30.0, 8.90, 13.85, 0.85, True, VOICE_DIP),
    (CM + 'freepd_lurking_sloth.mp3', 157.8, 13.85, PRESS - 0.05, 0.85, True, VOICE_DIP),
    (CM + 'freepd_fensters_explanation.mp3', 168.9, PRESS + 0.5, DOOR - 0.1, 0.70, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, DOOR, DUR, 0.85, True, VOICE_DIP),
]
VGAIN = {'glenn': 2.0, 'doris': 2.1, 'trent': 1.9, 'clerk': 2.0, 'mom': 2.0}
