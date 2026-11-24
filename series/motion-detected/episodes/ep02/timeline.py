"""S01E02 «ONE BULB OUT?!» (MOTION DETECTED, US) — timing for video (ep02.py) and audio (mix.py).
Voice: voice/ep02_t (tempo 1.10). Sound: CC0 (library/cc0/sfx) + 2 own ElevenLabs SFX (sfx/crowd_yes, sfx/power_out) + FreePD music."""
DUR = 37.2
FPS = 30
SLUG = 'motion-detected'
LUFS = -14.0

_T = dict(g1=0.00, d1=3.70, g2=7.37, g3=10.57, d2=14.61, g4=17.16, d3=20.70, g5=25.20, t1=27.90, d4=32.00)
_D = dict(g1=3.66, d1=3.63, g2=3.16, g3=4.00, d2=2.51, g4=2.61, d3=4.44, g5=2.61, t1=2.80, d4=4.23)
_W = dict(g='glenn', d='doris', t='trent')
_TX = dict(g1="Six HUNDRED lights! ONE bulb is dead, and they ALL went out!", d1="Motion detected. Glenn. On a ladder. AGAIN.",
           g2="Barry across the street did his whole house with ONE button.", g3="But I have a SYSTEM. I check every bulb. One by ONE.",
           d2="It's midnight, Glenn. Linda ate your DINNER.", g4="Bulb six hundred. This is the ONE.",
           d3="Congratulations. Brightest house on the street. The ONLY house.", g5="I WON. Why is everybody walking toward ME?",
           t1="Evening, folks! Got a minute to talk about SOLAR?", d4="Motion detected. Entire street. Holding FLASHLIGHTS.")
VOICE = [(k, 'ep02_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

CLICK = 19.60                    # bulb 600 goes in — the house blazes
BZZT = 20.30                     # the whole street goes dark
MONT = 12.80                     # the bulb-by-bulb montage starts
YES = 30.75
#        hook  doris  barry  system dcu   g4     blaze  only   g5     trent  crowd
CUTS = [0.0, 3.70, 7.37, 10.57, 14.61, 17.16, 19.60, 20.70, 25.20, 27.90, 30.75, DUR]
NAMES = ['hook', 'doris', 'barry', 'system', 'dcu', 'g4', 'blaze', 'only', 'g5', 'trent', 'crowd']
TWIST = CUTS[6]                  # 19.60 / 37.2 = 53 %

L = 'library/cc0/sfx/'
S = 'series/motion-detected/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'bottle_clink.mp3', 0.05, 0.55),             # bulbs clink on the string
    (L + 'chair_creak.mp3', 0.40, 0.45),              # the stepladder creaks
    (L + 'sms_message.mp3', 3.62, 0.45),              # Doris chime
    (L + 'bottle_clink.mp3', 10.70, 0.40),
    (L + 'phone_key_click.mp3', 12.80, 0.70),         # tester beeps through the montage
    (L + 'phone_key_click.mp3', 13.30, 0.60),
    (L + 'phone_key_click.mp3', 13.80, 0.60),
    (L + 'clock_fast.mp3', 13.00, 0.55),
    (L + 'sms_message.mp3', 14.53, 0.45),
    (L + 'chair_creak.mp3', 17.20, 0.40),
    (L + 'light_switch_click.mp3', CLICK - 0.05, 1.00),
    (L + 'gong_strong.mp3', CLICK, 0.30),
    (S + 'power_out.mp3', BZZT - 0.15, 0.95),
    (L + 'small_dog_bark.mp3', 22.6, 0.30),
    (L + 'door_apartment_open.mp3', 23.4, 0.45),      # neighbors' doors open in the dark
    (L + 'steps_concrete.mp3', 25.4, 0.60),
    (L + 'snow_steps.mp3', 26.4, 0.55),
    (L + 'steps_concrete.mp3', 29.0, 0.50),
    (S + 'crowd_yes.mp3', YES, 1.00),
    (L + 'rimshot_joke.mp3', 31.9, 0.25),
    (L + 'snow_steps.mp3', 32.5, 0.55),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_busybody.mp3', 30.0, 0.0, 12.75, 0.80, True, VOICE_DIP),
    (CM + 'freepd_managing_mischief.mp3', 20.0, 12.75, CLICK - 0.05, 0.85, True, VOICE_DIP),
    (CM + 'freepd_fensters_explanation.mp3', 168.9, BZZT + 1.2, YES - 0.05, 0.70, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, YES + 0.9, DUR, 0.85, True, VOICE_DIP),
]
VGAIN = {'glenn': 2.0, 'doris': 2.1, 'trent': 1.9}
