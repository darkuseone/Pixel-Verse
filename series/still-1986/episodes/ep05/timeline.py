"""S01E05 «ROOF: $9.99/MO» — timing (ep05.py) and audio (mix.py)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
CM.EP = 'ep05'
FPS = 30
SLUG = 'still-1986'
LUFS = -14.0

VOICE, _e = CM.seq([
    ('v1', 'vince', "Close the ROOF! The game's getting WET!"),
    ('r1', 'roofe', 'Roof control requires Premium. Nine ninety-nine a MONTH.', 0.15),
    ('v2', 'vince', "It's MY roof! I bought this car in nineteen... twenty-NINETEEN!"),
    ('f1', 'fran', "Honey. You're renting your ROOF."),
    ('v3', 'vince', 'FINE! SUBSCRIBE!', 1.3),
    ('r2', 'roofe', 'Plus a three-fifty CONVENIENCE fee.'),
    ('v4', 'vince', 'Convenient for WHO?!', 0.0, 'ep01'),
    ('v5', 'vince', '...Okay. Now open the ROOF.', 1.7),
    ('r3', 'roofe', 'Opening requires ULTRA. Nineteen ninety-NINE.'),
    ('f2', 'fran', 'Send this to anyone who subscribed to their own CAR.', 0.8),
    ('v6', 'vince', "A convertible that doesn't CONVERT."),
    ('f3', 'fran', "Honey. That's a hatchback NOW."),
])
DUR = round(_e + 0.5, 2)
T = {r[0]: r[3] for r in VOICE}
E = {r[0]: round(r[3] + r[5], 2) for r in VOICE}
CLOSE = E['v4_ep01'] + 0.05                     # the roof unfolds
SUN = T['v5'] - 0.6                        # rain stops, the sun comes out
CUTS = [0.0, T['r1'] - 0.05, T['v2'] - 0.05, T['f1'] - 0.05, T['v3'] - 1.3, T['r2'] - 0.05, CLOSE, SUN, T['r3'] - 0.05,
        T['f2'] - 0.05, T['v6'] - 0.05, T['f3'] - 0.05, DUR]
CUTS = [round(c, 2) for c in CUTS]
NAMES = ['hook', 'screen', 'mine', 'fran', 'flood', 'fee', 'close', 'sun', 'ultra', 'sweat', 'convert', 'button']
TWIST = CUTS[7]

X = 'series/still-1986/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'car_chime.mp3', T['r1'] - 0.2, 0.7),
    (L + 'vinyl_scratch.mp3', T['v2'] - 0.7, 0.4),
    (X + 'neon_on.mp3', T['f1'] - 1.1, 0.4),
    (X + 'splash.mp3', T['v3'] - 0.5, 0.5),
    (X + 'car_chime.mp3', T['r2'] - 0.15, 0.7),
    (X + 'app_ding.mp3', T['r2'] + 1.0, 0.5),
    (X + 'roof_motor.mp3', CLOSE, 0.8),
    (L + 'whoosh_1.mp3', SUN - 0.1, 0.45),
    (X + 'sax_fantasy.mp3', SUN + 0.1, 0.45),
    (X + 'car_chime.mp3', T['r3'] - 0.15, 0.7),
    (L + 'vinyl_scratch.mp3', T['r3'] + 1.2, 0.4),
    (L + 'rimshot_joke.mp3', DUR - 1.55, 0.45),
    (X + 'app_ding.mp3', DUR - 1.0, 0.45),
]
BEDS = [(X + 'rain_loop.mp3', 8.0, 0.0, SUN + 0.2, 0.55, True), (X + 'miami_eve_loop.mp3', 8.0, SUN, DUR, 0.4, True),
        (CM.MUSIC, 15.0, SUN, DUR, 0.14, True, CM.MUSIC_DIP)]
VGAIN, VFX = CM.VGAIN, CM.VFX
