"""S01E03 «BOAT DAY» — timing (ep03.py) and audio (mix.py)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
CM.EP = 'ep03'
FPS = 30
SLUG = 'still-1986'
LUFS = -14.0

VOICE, _e = CM.seq([
    ('v1', 'vince', "Speedboat. Sunset. Chase scene. Let's GO, baby."),
    ('f1', 'fran', 'Honey. Read the BOARD.'),
    ('v2', 'vince', 'Nine HUNDRED?! For a BOAT?!', 0.5),
    ('f2', 'fran', "Honey, that's RENT."),
    ('v3', 'vince', "Fine. I'll take the eighty-six SPECIAL."),
    ('v4', 'vince', 'Chase scene... in PROGRESS.', 0.7),
    ('v5', 'vince', 'CHASE SCENE!', 0.9),
    ('f3', 'fran', 'Send this to your friend who always rents the CHEAP one.'),
    ('d1', 'diaz', "Sir. We're out of gas. Can you... TOW us?", 0.5),
    ('v6', 'vince', 'Eighty-six, baby. Hop ON.'),
    ('d2', 'diaz', 'Towing without a license. Two-FIFTY.', 2.6),
    ('v7', 'vince', 'I SAVED you!'),
    ('f4', 'fran', "Honey. You're the tow truck NOW."),
])
DUR = round(_e + 0.5, 2)
T = {r[0]: r[3] for r in VOICE}
E = {r[0]: round(r[3] + r[5], 2) for r in VOICE}
PASS = E['v4'] + 0.2                        # the patrol boat roars past
CUTS = [0.0, T['f1'] - 0.05, E['f1'] + 0.05, T['f2'] - 0.05, T['v3'] - 0.05, T['v4'] - 0.6, PASS, T['f3'] - 0.05, T['d1'] - 0.35,
        T['v6'] - 0.05, E['v6'] + 0.05, T['d2'] - 0.05, T['f4'] - 0.05, DUR]
CUTS = [round(c, 2) for c in CUTS]
NAMES = ['hook', 'fran', 'board', 'rent', 'special', 'pedal', 'pass', 'chase', 'twist', 'hopon', 'towing', 'ticket', 'button']
TWIST = CUTS[8]

X = 'series/still-1986/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'sax_fantasy.mp3', 0.0, 0.5),
    (L + 'steps_concrete.mp3', 0.5, 0.35),
    (X + 'neon_on.mp3', T['f1'] - 1.2, 0.5),
    (L + 'vinyl_scratch.mp3', T['v2'] - 0.7, 0.5),
    (L + 'boing_cartoon.mp3', E['v3'] - 0.1, 0.35),
    (X + 'pedal_loop.mp3', T['v4'] - 0.6, 0.6),
    (X + 'pedal_loop.mp3', T['v4'] + 2.3, 0.5),
    (X + 'boat_pass.mp3', PASS - 1.2, 0.8),
    (X + 'splash.mp3', PASS + 0.15, 0.85),
    (X + 'pedal_loop.mp3', T['v5'] + 0.5, 0.6),
    (X + 'pedal_loop.mp3', T['v5'] + 3.2, 0.5),
    (X + 'engine_die.mp3', T['d1'] - 1.0, 0.7),
    (L + 'whoosh_1.mp3', TWIST - 0.1, 0.45),
    (X + 'sax_fantasy.mp3', CUTS[10] + 0.1, 0.7),
    (X + 'pedal_loop.mp3', CUTS[10], 0.5),
    (L + 'phone_key_click.mp3', T['d2'] + 0.5, 0.4),
    (L + 'rimshot_joke.mp3', DUR - 1.55, 0.45),
    (X + 'app_ding.mp3', DUR - 1.0, 0.45),
]
BEDS = CM.beds(DUR, X + 'marina_amb_loop.mp3', t_cut=TWIST)
VGAIN, VFX = CM.VGAIN, CM.VFX
