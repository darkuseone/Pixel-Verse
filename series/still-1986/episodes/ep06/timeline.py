"""S01E06 «UPDATE: 6 HRS» (season finale) — timing (ep06.py) and audio (mix.py)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
CM.EP = 'ep06'
FPS = 30
SLUG = 'still-1986'
LUFS = -14.0

VOICE, _e = CM.seq([
    ('v1', 'vince', "Thursday's done. Tonight... I finally PLAY."),
    ('v2', 'vince', 'SIX HOURS?!', 1.0),
    ('f1', 'fran', "Honey. That's longer than the EIGHTIES."),
    ('v3', 'vince', "Rey, buddy. What's your Wi-Fi PASSWORD?", 0.8),
    ('r1', 'rey', "It's free, amigo."),
    ('v4', 'vince', 'Free... with a STAR?'),
    ('r2', 'rey', "Star's twenty BUCKS."),
    ('f2', 'fran', "Honey. I'm on level NINE.", 2.6),
    ('v5', 'vince', "That's MY game!"),
    ('f3', 'fran', "It's MY electricity."),
    ('f4', 'fran', "Send this to whoever's still DOWNLOADING.", 0.2),
    ('v6', 'vince', "...It's twenty twenty-six, baby.", 2.4),
])
DUR = round(_e + 1.6, 2)
T = {r[0]: r[3] for r in VOICE}
E = {r[0]: round(r[3] + r[5], 2) for r in VOICE}
TVON = E['v1'] + 0.1
LAPSE = E['r2'] + 0.1
CUTS = [0.0, TVON, T['v2'] - 0.05, T['f1'] - 0.05, T['v3'] - 0.3, T['r1'] - 0.05, T['v4'] - 0.05, T['r2'] - 0.05, LAPSE,
        T['f2'] - 0.25, T['v5'] - 0.05, T['f3'] - 0.05, T['f4'] - 0.05, E['f4'] + 0.05, T['v6'] - 0.05, E['v6'] + 0.25, DUR]
CUTS = [round(c, 2) for c in CUTS]
NAMES = ['hook', 'tv', 'six', 'fran', 'knock', 'rey', 'star', 'rey2', 'lapse', 'twist', 'mine', 'elec', 'share', 'play', 'cool', 'season2']
TWIST = CUTS[9]

X = 'series/still-1986/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'sax_fantasy.mp3', 0.0, 0.45),
    (X + 'crt_on.mp3', TVON - 0.05, 0.9),
    (L + 'vinyl_scratch.mp3', T['v2'] - 0.75, 0.5),
    (X + 'neon_on.mp3', T['f1'] - 1.1, 0.4),
    (L + 'door_knock.mp3', T['v3'] - 0.3, 0.6),
    (L + 'whoosh_3.mp3', LAPSE, 0.4),
    (L + 'whoosh_1.mp3', LAPSE + 0.8, 0.35),
    (X + 'pad_clicks.mp3', TWIST, 0.8),
    (L + 'vinyl_scratch.mp3', TWIST + 0.0, 0.35),
    (X + 'pad_clicks.mp3', T['f3'], 0.6),
    (X + 'pad_clicks.mp3', CUTS[13], 0.6),
    (X + 'car_cruise.mp3', CUTS[13] + 0.1, 0.35),
    (X + 'sax_fantasy.mp3', T['v6'] - 0.2, 0.6),
    (L + 'rimshot_joke.mp3', DUR - 1.55, 0.45),
    (X + 'app_ding.mp3', DUR - 1.0, 0.45),
]
BEDS = [(CM.MUSIC, 15.0, 0.0, DUR, 0.13, True, CM.MUSIC_DIP)]
VGAIN = dict(CM.VGAIN, rey=2.6)
VFX = dict(CM.VFX, rey='lowpass=f=1800,highpass=f=150')
