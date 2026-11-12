"""S01E02 «$40 + FEES» — timing (ep02.py) and audio (mix.py). Voices: voice/ep02_t (+ «Convenient for WHO?!» reused from ep01_t)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
CM.EP = 'ep02'
FPS = 30
SLUG = 'still-1986'
LUFS = -14.0

VOICE, _e = CM.seq([
    ('v1', 'vince', "Forty bucks for Eighty-Six Night? I'll pay CASH, baby."),
    ('t1', 'tiffany', 'Cash is a FEE.'),
    ('v2', 'vince', "It's eighty-six! Cash is KING!"),
    ('f1', 'fran', 'Honey. The king has a fee too.'),
    ('t2', 'tiffany', 'Service fee. Facility fee. CONVENIENCE fee.'),
    ('v4', 'vince', 'Convenient for WHO?!', 0.0, 'ep01'),
    ('t3', 'tiffany', 'And the fee fee.'),
    ('v3', 'vince', "What's a FEE fee?!"),
    ('t4', 'tiffany', 'The fee for the FEES.'),
    ('v5', 'vince', 'I want to DISPUTE these fees!'),
    ('t5', 'tiffany', 'Sure. Disputes are online. Five-dollar dispute FEE.', 0.1),
    ('f2', 'fran', 'Send this to whoever bought concert tickets this year.', 0.1),
    ('v6', 'vince', '...Total?'),
    ('t6', 'tiffany', 'With tax? Eighty-six EVEN.'),
    ('v7', 'vince', "Finally. Something that's still EIGHTY-SIX.", 0.15),
    ('f3', 'fran', 'Honey. Silence is fifteen EXTRA.', 0.5),
])
DUR = round(_e + 0.45, 2)
T = {r[0]: r[3] for r in VOICE}
E = {r[0]: round(r[3] + r[5], 2) for r in VOICE}

#   hook   tiff    two      fees     who        tiff2    whatfee   tiff3    hero     twist    fran     total     screen          moved    disco
CUTS = [0.0, T['t1'] - 0.05, T['v2'] - 0.05, T['t2'] - 0.05, T['v4_ep01'] - 0.05, T['t3'] - 0.05, T['v3'] - 0.05, T['t4'] - 0.05,
        T['v5'] - 0.05, T['t5'] - 0.05, T['f2'] - 0.05, T['v6'] - 0.05, T['t6'] - 0.05, T['v7'] - 0.05, T['f3'] - 0.4, DUR]
CUTS = [round(c, 2) for c in CUTS]
NAMES = ['hook', 'tiff', 'two', 'fees', 'who', 'tiff2', 'whatfee', 'tiff3', 'hero', 'twist', 'fran', 'total', 'screen', 'moved', 'disco']
TWIST = CUTS[9]

X = 'series/still-1986/sfx/'
L = 'library/cc0/sfx/'
SFX = [
    (X + 'sax_fantasy.mp3', 0.0, 0.45),
    (L + 'cloth_rustle.mp3', 0.6, 0.4),
    (X + 'gum_pop.mp3', E['t1'] - 0.1, 0.9),
    (X + 'neon_on.mp3', T['f1'] - 1.2, 0.5),
    (X + 'register.mp3', T['t2'] + 0.15, 0.45),
    (X + 'app_ding.mp3', T['t2'] + 1.1, 0.5),
    (X + 'app_ding.mp3', T['t2'] + 2.2, 0.5),
    (L + 'vinyl_scratch.mp3', T['v4_ep01'] - 0.8, 0.5),
    (X + 'app_ding.mp3', T['t3'] + 0.5, 0.5),
    (L + 'boing_cartoon.mp3', E['v3'] - 0.2, 0.3),
    (X + 'sax_fantasy.mp3', T['v5'] + 0.1, 0.5),
    (L + 'whoosh_1.mp3', TWIST - 0.1, 0.45),
    (X + 'register.mp3', T['t5'] + 2.2, 0.6),
    (X + 'neon_on.mp3', T['f2'] - 1.1, 0.45),
    (X + 'register.mp3', T['t6'] + 1.0, 0.6),
    (X + 'sax_fantasy.mp3', T['v7'] + 0.2, 0.6),
    (L + 'whoosh_3.mp3', T['f3'] - 0.45, 0.4),
    (L + 'rimshot_joke.mp3', DUR - 1.55, 0.45),
    (X + 'app_ding.mp3', DUR - 1.0, 0.45),
]
BEDS = CM.beds(DUR, X + 'club_amb_loop.mp3', t_cut=TWIST) + [(X + 'disco_shuffle_loop.mp3', 6.0, T['f3'] - 0.4, DUR, 0.5, True)]
VGAIN, VFX = CM.VGAIN, CM.VFX
