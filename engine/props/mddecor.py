"""«MOTION DETECTED» set dressing (rule 10.10.2026: dense local atmosphere, readable US suburban jokes) for porch / hall.
Rewatch clue in the first frame: «NO SOLICITORS — THIS MEANS YOU, TRENT» by the door. Animated: falling leaves, porch-lamp moths,
neighbor's blinking string lights. dress(name, world) is called once by mdkit.world()."""
import math
import numpy as np
from props import decals as D
from props import rusigns as R

BLACKOUT = [0.0]                       # E02: 0..1 — the street loses power (neighbor lights off)
WH, BLK, RED, NAVY = (250, 248, 238), (34, 30, 28), (200, 40, 40), (30, 50, 120)
YEL, BRASS, ORG = (255, 226, 90), (214, 180, 90), (246, 128, 40)


def leaves(box, n=26, seed=5, speed=22.0):
    r = np.random.default_rng(seed)
    P = [(r.random(), r.random(), 0.6 + r.random(), r.random() * 6.28) for _ in range(n)]
    cols = [(230, 110, 40), (200, 70, 30), (240, 170, 50)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for i, (u, w, s, ph) in enumerate(P):
            y = y0 + ((w * (y1 - y0) + t * speed * s) % (y1 - y0))
            x = x0 + ((u * (x1 - x0) + t * 9 * s + math.sin(t * 1.4 + ph) * 12) % (x1 - x0))
            ox, oy = v.opt(x, y)
            q = max(2, int(1.2 * s * v.Z * 3))
            ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q:
                big[iy:iy + q, ix:ix + q] = cols[i % 3]
                if math.sin(t * 6 + ph) > 0: big[iy:iy + q // 2, ix:ix + q] = (250, 200, 90)
    return f


def moths(cx, cy, n=4, seed=2):
    r = np.random.default_rng(seed)
    P = [(r.random() * 6.28, 6 + r.random() * 14, 2 + r.random() * 3) for _ in range(n)]
    def f(big, v, t):
        for ph, rad, sp_ in P:
            x = cx + math.cos(t * sp_ + ph) * rad; y = cy + math.sin(t * sp_ * 1.3 + ph) * rad * 0.6
            ox, oy = v.opt(x, y); q = max(2, int(0.7 * v.Z * 3)); ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q: big[iy:iy + q, ix:ix + q] = (255, 240, 200)
    return f


def string_lights(pts, seed=1):
    cols = ((255, 60, 60), (60, 220, 90), (255, 214, 60), (70, 140, 255))
    def f(big, v, t):
        if BLACKOUT[0] > 0.5: return
        for i, (x, y) in enumerate(pts):
            on = (int(t * 3) + i) % 3 != 0
            if not on: continue
            ox, oy = v.opt(x, y); q = max(2, int(0.9 * v.Z * 3)); ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q: big[iy:iy + q, ix:ix + q] = cols[i % 4]
    return f


def dress_porch(W):
    D.attach(W, [
        (R.plate(30, 36, ['NO', 'SOLICITORS', 'THIS MEANS', 'YOU, TRENT'], bg=WH, colors=[RED, RED, BLK, BLK], border=RED,
                 weights=[1.2, 1.0, 0.7, 0.7], pad=0.9), 296, 432),                                              # rewatch clue
        (R.plate(110, 26, ['GO AWAY*', '*UNLESS PACKAGE'], bg=(150, 110, 60), colors=[(60, 36, 20), (60, 36, 20)], border=None,
                 weights=[1.3, 0.6], pad=0.8), 245, 518),                                                       # the doormat
        (R.plate(36, 14, ['1408'], bg=(30, 30, 34), fg=BRASS, border=BRASS, pad=0.5), 190, 74),
        (R.plate(24, 16, ['PROTECTED', 'BY KNOCKR'], bg=(30, 60, 110), colors=[WH, (120, 220, 255)], border=WH, pad=0.6), 296, 292),
        (R.plate(30, 12, ['HOLLIS'], bg=(30, 30, 34), fg=WH, border=None, pad=0.4), 1082, 412),                 # mailbox
        (R.plate(56, 30, ['SUNNYSIDE', 'SOLAR: ASK ME!'], bg=(250, 200, 40), colors=[(200, 60, 20), BLK], border=BLK, pad=0.8), 905, 382),
        (R.plate(44, 16, ['SLOW: KIDS', '& DADS'], bg=YEL, colors=[BLK, BLK], border=BLK, pad=0.5), 690, 455),
    ])
    D.anim(W, leaves((560, 40, 1280, 700), n=24, seed=4))
    D.anim(W, moths(390, 175, n=4))
    D.anim(W, string_lights([(650 + i * 16, 312 + 4 * math.sin(i * 0.9)) for i in range(20)] +
                            [(690 + i * 9, 270 - i * 6.6) for i in range(10)] + [(835 + i * 9, 205 + i * 7.6) for i in range(14)]))


def dress_hall(W):
    D.attach(W, [
        (R.plate(66, 40, ['GLENN\'S', 'DELIVERY', 'COMMAND', 'CENTER'], bg=WH, colors=[NAVY, RED, RED, RED], border=NAVY,
                 weights=[0.8, 1.0, 1.0, 1.0], pad=1.0, tilt=-2), 690, 255),
        (R.plate(64, 34, ['LIVE', 'LAUGH', 'SIGN FOR IT'], bg=(250, 246, 230), colors=[(120, 80, 50)] * 3, border=(120, 80, 50), pad=0.9), 850, 85),
        (R.plate(40, 18, ['HONEY-DO', 'LIST: 47'], bg=YEL, colors=[BLK, RED], border=None, pad=0.6, tilt=4), 960, 128),
        (R.plate(34, 16, ['KEYS', '(NOT YOURS)'], bg=WH, colors=[BLK, BLK], border=BLK, pad=0.5), 70, 470),
    ])


def dress_breakroom(W):
    D.attach(W, [
        (R.plate(150, 30, ['WHITE ELEPHANT', '$25 LIMIT (KYLE!!)'], bg=WH, colors=[RED, NAVY], border=None, pad=1.0), 165, 240),
        (R.plate(56, 26, ['STEALS:', 'MAX 3'], bg=YEL, colors=[BLK, RED], border=BLK, pad=0.6, tilt=-3), 300, 300),
        (R.plate(48, 22, ['LABEL YOUR', 'FOOD. KYLE.'], bg=(255, 250, 200), colors=[BLK, RED], border=None, pad=0.6, tilt=3), 700, 330),
        (R.plate(56, 30, ['HAPPY', 'HOLIDAYS!', '(MANDATORY)'], bg=(30, 110, 60), colors=[WH, WH, YEL], border=WH, pad=0.6), 1220, 210),
        (R.plate(40, 16, ['DECAF', '(SORRY)'], bg=WH, colors=[BLK, BLK], border=BLK, pad=0.4), 820, 278),
        (R.plate(62, 20, ['CUBICLE 7: TEMP'], bg=(200, 200, 205), fg=BLK, border=BLK, pad=0.5), 1020, 390),
    ])
    D.anim(W, string_lights([(470 + (i % 6) * 14, 210 + i * 12) for i in range(20)]))


def dress_postoffice(W):
    D.attach(W, [
        (R.plate(240, 60, ['PARCEL POST', 'WE DELIVER*'], bg=(30, 60, 110), colors=[WH, YEL], border=WH, pad=1.0), 630, 140),
        (R.plate(120, 16, ['*EVENTUALLY'], bg=WH, fg=RED, border=None, pad=0.5), 630, 196),
        (R.plate(44, 70, ['MISSING:', 'MY', 'PACKAGE', '(SINCE', 'OCT)'], bg=WH, colors=[RED, BLK, BLK, BLK, BLK], border=BLK, pad=0.8), 990, 260),
        (R.plate(120, 22, ['HOLIDAY RATES APPLY'], bg=(200, 40, 40), fg=WH, border=WH, pad=0.6), 420, 470),
        (R.plate(70, 22, ['LINE STARTS', 'HERE (OCT 1)'], bg=YEL, colors=[BLK, RED], border=BLK, pad=0.5), 1105, 470),
        (R.plate(40, 14, ['NEXT ->'], bg=(250, 246, 230), fg=BLK, border=BLK, pad=0.4), 820, 372),
    ])


def dress_momporch(W):
    D.attach(W, [
        (R.plate(44, 28, ['NO SOLICITORS', '(EXCEPT', 'NICE ONES)'], bg=WH, colors=[RED, BLK, BLK], border=RED, pad=0.6), 240, 420),
        (R.plate(90, 16, ['BLESS THIS MESS'], bg=(150, 110, 60), fg=(60, 36, 20), border=None, pad=0.5), 255, 524),
        (R.plate(52, 16, ['GNOME SWEET', 'GNOME'], bg=WH, colors=[(30, 110, 60), (30, 110, 60)], border=(30, 110, 60), pad=0.4), 620, 566),
        (R.plate(30, 18, ['PROTECTED', 'BY KNOCKR'], bg=(30, 60, 110), colors=[WH, (120, 220, 255)], border=WH, pad=0.5), 700, 400),
        (R.plate(40, 14, ['PIE 4 SALE'], bg=(255, 200, 220), fg=(150, 40, 80), border=None, pad=0.4, tilt=3), 500, 228),
    ])
    D.anim(W, flakes((0, 0, 1280, 700)))


def flakes(box, n=60, seed=7):
    r = np.random.default_rng(seed)
    P = [(r.random(), r.random(), 0.5 + r.random()) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, s in P:
            y = y0 + ((w * (y1 - y0) + t * 16 * s) % (y1 - y0)); x = x0 + u * (x1 - x0) + math.sin(t + u * 9) * 6
            ox, oy = v.opt(x, y); q = max(2, int(0.8 * s * v.Z * 3)); ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q: big[iy:iy + q, ix:ix + q] = (240, 244, 255)
    return f


def dress(name, W):
    if name.startswith('postoffice'): return dress_postoffice(W)
    if name.startswith('momporch'): return dress_momporch(W)
    if name.startswith('breakroom'): return dress_breakroom(W)
    if name == 'porch_night':
        D.attach(W, [
            (R.plate(40, 26, ['ATTEMPT', '2 OF 3'], bg=(255, 140, 40), colors=[(40, 20, 10), (40, 20, 10)], border=None, pad=0.6), 232, 330),
            (R.plate(70, 24, ["BARRY'S", 'WINTER WONDERLAND'], bg=(30, 110, 60), colors=[WH, YEL], border=WH, pad=0.7), 800, 412),
            (R.plate(34, 16, ['ONE CLICK', 'SETUP!'], bg=WH, colors=[RED, BLK], border=RED, pad=0.5), 960, 418),
        ])
    if name.startswith('porch'): return dress_porch(W)
    if name.startswith('hall'): return dress_hall(W)
