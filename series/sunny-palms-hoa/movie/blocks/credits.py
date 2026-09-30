"""The end: frozen finale frame, Earl's last word, credits over the bloopers."""
from shots import *
from blocks.ch6 import tail as finale_tail

LINES = [
    ('CAST', 34, (0, 214, 232)), ('', 20, None),
    ('DALE', 26, (255, 214, 74)), ('AS HIMSELF (ALLEGEDLY)', 18, (255, 255, 255)), ('', 14, None),
    ('BRENDA', 26, (255, 120, 190)), ('AS BRENDA (APPROVED)', 18, (255, 255, 255)), ('', 14, None),
    ('EARL', 26, (140, 235, 110)), ('GRANDFATHERED IN', 18, (255, 255, 255)), ('', 14, None),
    ('KEVIN', 26, (255, 150, 200)), ('PLASTIC', 18, (255, 255, 255)), ('', 14, None),
    ('HURRICANE KEVIN', 26, (196, 222, 255)), ('HIMSELF (IN COLLECTIONS)', 18, (255, 255, 255)), ('', 30, None),
    ('THE FINE PRINT', 34, (0, 214, 232)), ('', 20, None),
    ('NO ALLIGATORS WERE FINED', 20, (255, 255, 255)), ('', 14, None),
    ('NO FLAMINGOS WERE HARMED', 20, (255, 255, 255)), ('KEVIN WAS ALREADY PLASTIC', 20, (255, 255, 255)), ('', 14, None),
    ('FILMED WITHOUT A PERMIT', 20, (255, 255, 255)), ('FINE: $250', 26, (255, 84, 96)), ('', 14, None),
    ('APPROVED BY THE BOARD', 20, (255, 255, 255)), ('(BRENDA)', 20, (255, 255, 255)), ('', 40, None),
    ('SEASON 2', 40, (255, 236, 120)), ('HURRICANE SEASON', 26, (255, 236, 120)),
]


def _build():
    h = sum(sz * 2 + 8 for _, sz, _ in LINES) + 200
    img = Image.new('RGBA', (620, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    y = 20
    for txt, sz, col in LINES:
        if txt:
            f = O.pfont(sz); bb = f.getbbox(txt)
            for dx in (-2, 0, 2):
                for dy in (-2, 0, 2):
                    if dx or dy: d.text((310 - (bb[2] - bb[0]) // 2 - bb[0] + dx, y - bb[1] + dy), txt, font=f, fill=(20, 6, 40, 255))
            d.text((310 - (bb[2] - bb[0]) // 2 - bb[0], y - bb[1]), txt, font=f, fill=col + (255,))
        y += sz * 2 + 8
    return np.array(img)


_CR = {}


def credits_panel(big, tc):
    if 'i' not in _CR: _CR['i'] = _build()
    reg = big[:, 1290:]
    reg[:] = (reg * 0.28 + np.array([24, 8, 44]) * 0.72).astype(np.uint8)
    img = _CR['i']
    speed = (img.shape[0] + 380 - 200) / max(1.0, BLOCK.DUR - T0['c'])
    y0 = int(H_ - tc * speed)
    O.overlay(big, img, 1300, y0, 1.0)


def clapper(big, take, u, x=120, y=150, open_=True):
    box = np.zeros((190, 340, 4), np.uint8); box[..., :3] = (20, 20, 24); box[..., 3] = 255
    for i in range(6): box[10:50, 10 + i * 56:10 + i * 56 + 28, :3] = (250, 250, 250)
    box[54:180, 10:330, :3] = (40, 40, 48)
    O.overlay(big, box, x, y, 1.0)
    ptext(big, 'SUNNY PALMS  S1', x + 170, y + 95, 18, (255, 255, 255), (20, 20, 24))
    ptext(big, f'TAKE {take}', x + 170, y + 145, 26, (255, 236, 120), (20, 20, 24))


def f_frozen(ctx, t, u, dur, z=0.0):
    big = finale_tail(None, 2.0, 0.0 + 0.3 * u, 4.0)
    pip(big, earl_cu(ctx, t, u, dur, 'clubhouse', lid=0.5, Z=2.3, zoom=0.03), 'br', 700, 1.0)
    return big


def f_credits(ctx, t, u, dur):
    big = finale_tail(None, 2.0, 1.4, 4.0)
    credits_panel(big, t - T0['c'])
    pip(big, earl_cu(ctx, t, u, dur, 'clubhouse', lid=0.5, Z=2.3, zoom=0.03), 'bl', 560, 1.0)
    return big


T0 = {'c': 0.0}


def bl(fnc, take, clap=True):
    def fn(ctx, t, u, dur):
        big = fnc(ctx, t, u, dur)
        credits_panel(big, t - T0['c'])
        if clap: clapper(big, take, u)
        return big
    return fn


BLOCK = Block('credits', [
    dict(v=('movie_t', 'f1', 'earl', "And that is how a man with six thousand dollars in fines became PRESIDENT."), fn=f_frozen, lead=0.2, pad=0.2, cap=None, mosaic=[0.0],
         st=[('THE END', (255, 236, 120), 100, 700, 420, 2.4, 5.0)]),
    dict(v=('movie_t', 'f2', 'earl', "I have lived here since nineteen eighty-seven. It has always been like THIS."), fn=f_credits, lead=0.1, pad=0.3, cap=None),
    dict(v=('movie_t', 'bl1', 'dale', "Two hundred fifty?! For a MAIL, mail, mailbag?"), fn=bl(cu('dale', 'yard', 1.3, 0.04, expr='shout', red=0.7, sweat=0.5, hand_n=U.H(5.6, 12.6), prop_n=lambda L, h: UP.notice(L, h, -0.2, w=5.2, hh=6.8)), 13), sfx=[('library/sfx/clapper_clack.mp3', 0.0, 0.8)],
         st=[('[BLOOPERS]', (255, 255, 255), 30, 700, 1010, 0.1, 3.4)], cap=940),
    dict(v=('movie_t', 'bl2', 'earl', "Take fourteen."), fn=bl(lambda c, t, u, d: earl_cu(c, t, u, d, 'yard', lid=0.7, Z=2.3), 14), sfx=[('library/sfx/clapper_clack.mp3', 0.0, 0.8)], cap=940, pad=0.2),
    dict(v=('movie_t', 'bl3', 'brenda', "Bless your, [laughs] I can't. I'm sorry."), fn=bl(cu('brenda', 'yard', 1.35, 0.05, expr='cheer', lean=0.4, pose=U.BPOSE['hands'], shake=0.0), 15), sfx=[('library/sfx/clapper_clack.mp3', 0.0, 0.8)],
         st=[('[BRENDA BREAKS]', (255, 190, 226), 34, 700, 1010, 0.4, 4.4)], cap=940),
    dict(v=('movie_t', 'bl4', 'earl', "The alligator hit every mark. Just saying."), fn=bl(lambda c, t, u, d: earl_cu(c, t, u, d, 'yard', lid=0.5, Z=2.3, grin=0.3), 16), sfx=[('library/sfx/clapper_clack.mp3', 0.0, 0.8)], cap=940, pad=0.3),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.3, True), ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, None, 0.25, False)], hud=False, chapter='The End, Credits and Bloopers')
T0['c'] = BLOCK.beats[1]['t0']
