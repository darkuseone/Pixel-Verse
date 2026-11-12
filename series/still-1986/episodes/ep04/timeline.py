"""S01E04 «DROP DAY» — timing (ep04.py) and audio (mix.py)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
CM.EP = 'ep04'
FPS = 30
SLUG = 'still-1986'
LUFS = -14.0

VOICE, _e = CM.seq([
    ('v1', 'vince', 'Boss... I got the eighty-six FLU.'),
    ('g1', 'gary', "Rest up, Vince. Doctor's ORDERS."),
    ('f1', 'fran', 'Honey. Half this line has the FLU.'),
    ('v2', 'vince', 'Nice disguise, buddy. Hiding from your BOSS?'),
    ('g2', 'gary', 'Like a NINJA.'),
    ('v3', 'vince', "Watch this. I'll call mine and tell him I'm BETTER."),
    ('g3', 'gary', "Gary speaking... I've got the FLU.", 0.9),
    ('v4', 'vince', 'GARY?!', 0.1),
    ('g4', 'gary', 'VINCE?!'),
    ('f2', 'fran', "Send this to your boss. He's in line TOO.", 1.0),
    ('g5', 'gary', 'Nobody saw NOTHING.', 1.7),
    ('v5', 'vince', "Deal. And I'm taking FRIDAY."),
    ('f3', 'fran', 'Honey. The whole office is taking FRIDAY.'),
])
DUR = round(_e + 0.5, 2)
T = {r[0]: r[3] for r in VOICE}
E = {r[0]: round(r[3] + r[5], 2) for r in VOICE}
RING = E['v3'] + 0.15
GATE = E['f2'] + 0.25
CUTS = [0.0, T['g1'] - 0.05, T['f1'] - 0.05, T['v2'] - 0.05, T['v3'] - 0.05, RING - 0.05, T['v4'] - 0.1, T['g4'] - 0.05,
        E['g4'] + 0.1, GATE, T['v5'] - 0.05, T['f3'] - 0.05, DUR]
CUTS = [round(c, 2) for c in CUTS]
NAMES = ['hook', 'line', 'fran', 'whisper', 'call', 'ring', 'twist', 'gary', 'office', 'gate', 'deal', 'button']
TWIST = CUTS[6]

X = 'series/still-1986/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (L + 'phone_key_click.mp3', 0.05, 0.4),
    (X + 'neon_on.mp3', T['f1'] - 1.1, 0.45),
    (L + 'phone_key_click.mp3', T['v3'] + 1.6, 0.5),
    (L + 'phone_dial_tone.mp3', E['v3'] - 0.3, 0.3),
    (X + 'ringtone.mp3', RING, 0.55),
    (L + 'vinyl_scratch.mp3', TWIST - 0.85, 0.55),
    (L + 'boing_cartoon.mp3', TWIST + 0.1, 0.35),
    (L + 'whoosh_1.mp3', CUTS[8] - 0.05, 0.4),
    (X + 'gate_crowd.mp3', GATE, 0.8),
    (X + 'sax_fantasy.mp3', T['v5'], 0.45),
    (L + 'rimshot_joke.mp3', DUR - 1.55, 0.45),
    (X + 'app_ding.mp3', DUR - 1.0, 0.45),
]
BEDS = CM.beds(DUR, X + 'mall_amb_loop.mp3', t_cut=TWIST)
VGAIN, VFX = CM.VGAIN, CM.VFX
