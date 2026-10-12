"""«Прохор. Таёжные лайфхаки» set dressing (rule 10.10.2026: dense local atmosphere): Russian signs, notices, labels and props laid over
the xAI worlds as hi-res decals (props/decals.py + props/rusigns.py for Cyrillic), plus animated ambience (snow sparkles, drifting flakes,
dust in the light beam). Every inscription is auto-fitted inside its plate. dress(name, world) is called once by taigakit.world().
Parody brands of the series: УК «Берлога», «Тайга-Банк», «Сберорех», «Лиса-Экспресс», «Пятнюшка-Тайга», «Дикая Ягода»."""
import math
import numpy as np
from props import decals as D
from props import rusigns as R
from props import taigapix as TX
from props import taigacast as C

RED, NAVY, BLK, WH = (190, 30, 34), (30, 44, 90), (30, 28, 30), (244, 240, 226)
BIRCH = (236, 232, 220)
PLY = (214, 180, 124)


def _spr(fn, s, **kw):
    img, (ax, ay) = D.sprite(fn, s, TX.draw, **kw)
    return img, ax, ay


def place_sprite(world, fn, wx, wy, s, **kw):
    """a code-drawn object standing on a surface: feet anchor at world (wx, wy); s = world px per sprite px"""
    img, ax, ay = _spr(fn, s * D.WS, **kw)
    D.PROPS.add(id(img))
    D.attach(world, [(img, wx - ax / D.WS, wy - ay / D.WS)])


def _post(w, h, col=(110, 76, 46)):
    """a plain wooden post (world px) for signposts"""
    img = np.zeros((int(h * D.WS), int(w * D.WS), 4), np.uint8)
    img[..., :3] = col; img[..., 3] = 255
    img[:, :D.WS, :3] = (70, 46, 28); img[:, -D.WS:, :3] = (70, 46, 28)
    return img


def birch(w, h, lines, colors=None, weights=None, seed=0, tilt=0.0):
    """a birch-bark plate: white with black bark dashes along the edges, hand-lettered"""
    img = R.plate(w, h, lines, bg=BIRCH, fg=BLK, border=(70, 64, 58), colors=colors, weights=weights, hand=True, seed=seed, pad=2.2)
    rng = np.random.default_rng(seed + 7)
    H_, W_ = img.shape[:2]
    for _ in range(int(w * 0.5)):
        y = int(rng.integers(0, H_)); x = int(rng.integers(0, W_)); ln = int(rng.integers(6, 22))
        if y < 10 or y > H_ - 10 or rng.random() < 0.6:
            img[y:y + 3, x:min(W_, x + ln), :3] = (46, 42, 40)
    if tilt: img = D.rotate(img, tilt)
    return img


# ---------------------------------------------------------------- animated ambience
def sparkles(box, n=40, seed=3):
    """snow glints twinkling on the ground"""
    r = np.random.default_rng(seed)
    pts = [(box[0] + r.random() * (box[2] - box[0]), box[1] + r.random() * (box[3] - box[1]), r.random() * 6.28, 1.5 + r.random() * 2.5) for _ in range(n)]
    def f(big, v, t):
        for x, y, ph, sp in pts:
            k = max(0.0, math.sin(t * sp + ph))
            if k < 0.75: continue
            ox, oy = v.opt(x, y)
            q = max(3, int(2.2 * v.Z * 3))
            ix, iy = int(ox), int(oy)
            if q < ix < big.shape[1] - q and q < iy < big.shape[0] - q:
                big[iy - q // 2:iy + q // 2 + 1, ix - q * 2:ix + q * 2] = (255, 255, 255)
                big[iy - q * 2:iy + q * 2, ix - q // 2:ix + q // 2 + 1] = (255, 255, 255)
    return f


def flakes(box, n=50, seed=5, speed=12.0, col=(240, 246, 255)):
    """slow drifting snowflakes (world box), chunky square pixels"""
    r = np.random.default_rng(seed)
    P = [(r.random(), r.random(), 0.5 + r.random(), r.random() * 6.28) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, s, ph in P:
            y = y0 + ((w * (y1 - y0) + t * speed * s) % (y1 - y0))
            x = x0 + u * (x1 - x0) + math.sin(t * 0.9 + ph) * 6
            ox, oy = v.opt(x, y)
            q = max(3, int(1.0 * s * v.Z * 3))
            ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q:
                big[iy:iy + q, ix:ix + q] = col
    return f


def beam_dust(box, n=26, seed=9):
    """dust motes glittering in the cold light beam (den)"""
    r = np.random.default_rng(seed)
    P = [(r.random(), r.random(), r.random() * 6.28) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, ph in P:
            yy = y0 + ((w + t * 0.03) % 1.0) * (y1 - y0)
            xx = x0 + u * (x1 - x0) + math.sin(t * 0.7 + ph) * 8 + (yy - y0) * 0.12
            ox, oy = v.opt(xx, yy)
            q = max(3, int(0.7 * v.Z * 3)); ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q:
                big[iy:iy + q, ix:ix + q] = (200, 220, 255)
    return f


# ---------------------------------------------------------------- locations
def dress_izba(W):
    D.attach(W, [
        (R.plate(52, 64, ['ОКТЯБРЬ', '12', 'ДО ВЕСНЫ', '180 ДН.'], bg=(246, 244, 236), colors=[RED, BLK, NAVY, NAVY],
                 border=None, weights=[0.8, 2.2, 0.7, 0.7], pad=1.6), 538, 241),                                   # tear-off calendar
        (R.plate(82, 74, ['ГРАМОТА', 'ЛУЧШИЙ', 'ЛАЙФХАКЕР', 'ТАЙГИ'], bg=(250, 236, 200), colors=[RED, BLK, BLK, BLK],
                 border=(196, 150, 60), weights=[1.3, 0.8, 0.8, 0.8], bw=2.0), 607, 133),                            # certificate in the frame
        (birch(92, 40, ['ГАЗ ПРОВЕДУТ', 'В 1987 Г.'], colors=[NAVY, RED], seed=2, tilt=-3), 380, 268),          # notice on the logs
        (R.plate(30, 54, ['-42°'], bg=(236, 240, 246), fg=(30, 60, 160), border=(90, 90, 100), weights=[1.0], pad=1.4), 960, 140),   # thermometer
        (R.plate(30, 14, ['ОГУРЦЫ'], bg=(250, 246, 220), fg=BLK, border=None, pad=0.8), 367, 207),                  # jar labels
        (R.plate(30, 14, ['ГРИБЫ ?'], bg=(250, 246, 220), fg=RED, border=None, pad=0.8), 418, 207),
        (R.plate(34, 14, ['2019'], bg=(250, 246, 220), fg=BLK, border=None, pad=0.8), 446, 123),
        (R.plate(76, 16, ['ТАЙГА-ЛАЙФХАК'], bg=(30, 110, 200), fg=WH, border=WH, round_=2.0, pad=1.0, tilt=4), 383, 342),   # sticker on the radio
        (R.plate(58, 20, ['НЕ ТОПИТЬ', '(ДОРОГО)'], bg=WH, colors=[RED, BLK], border=RED, pad=1.0, tilt=-2), 228, 344),   # on the stove
    ])
    D.anim(W, flakes((0, 0, 1280, 720), n=36, seed=4, speed=6.0, col=(226, 236, 255)))          # frost dust falling inside
    D.anim(W, sparkles((0, 560, 1280, 720), n=30, seed=6))


def dress_taiga(W):
    D.attach(W, [
        (birch(60, 30, ['ПРОХОР', 'ПОЧТА РАЗ В ГОД'], colors=[BLK, RED], weights=[1.2, 0.8], seed=3), 984, 384),      # mailbox plate
        (R.plate(44, 22, ['НЕ', 'БУДИТЬ!'], bg=PLY, fg=RED, border=(110, 80, 50), weights=[0.8, 1.0], tilt=-5, hand=True, seed=5), 612, 370),
        (birch(48, 22, ['ЛОВИТ', 'ТУТ ↑'.replace('↑', '^')], colors=[NAVY, RED], seed=8), 1046, 400),             # on the pine trunk
        (R.plate(70, 18, ['ГОРОД 400 КМ →'.replace('→', '>')], bg=(240, 236, 220), fg=BLK, border=(60, 50, 40), tilt=2), 140, 450),
        (R.plate(64, 18, ['ПВЗ 40 КМ →'.replace('→', '>')], bg=(250, 210, 60), fg=BLK, border=(60, 50, 40), tilt=-3), 146, 470),
        (birch(70, 20, ['ТАЙГА-ЛАЙФХАК'], colors=[(30, 110, 200)], seed=9), 196, 336),                            # over the cabin door
    ])
    place_sprite(W, C.meter, 720, 492, 2.1, rub=0, spin=0.0)
    D.anim(W, sparkles((0, 500, 1280, 720), n=60, seed=7))
    D.anim(W, flakes((0, 0, 1280, 720), n=60, seed=8, speed=14.0))


def dress_den(W):
    D.attach(W, [
        (R.plate(120, 46, ['УК «БЕРЛОГА»', 'УПРАВЛЯЮЩИЙ М. П. ТОПТЫГИН'], bg=(170, 30, 34), colors=[(250, 220, 120), WH],
                 border=(250, 220, 120), weights=[1.4, 0.6], bw=1.6), 790, 150),                                     # pennant board
        (R.plate(96, 34, ['ПРИЁМ ГРАЖДАН:', 'С АПРЕЛЯ ПО АПРЕЛЬ'], bg=WH, colors=[BLK, RED], border=BLK, weights=[1, 0.9]), 610, 196),
        (R.plate(74, 26, ['НЕ КУРИТЬ.', 'НЕ БУДИТЬ.'], bg=(240, 236, 220), colors=[BLK, RED], border=BLK, tilt=3), 450, 330),
    ])
    D.anim(W, beam_dust((740, 40, 880, 460), n=30))


DRESS = dict(izba=dress_izba, taiga=dress_taiga, den=dress_den)


def dress(name, W):
    if name in DRESS: DRESS[name](W)


# ---------------------------------------------------------------- v2 worlds (12.10.2026)
def dress_porch(W):
    D.attach(W, [
        (R.plate(30, 54, ['-42°'], bg=(236, 240, 246), fg=(30, 60, 160), border=(90, 90, 100), pad=1.4), 300, 140),     # thermometer
        (birch(96, 40, ['ГАЗ ПРОВЕДУТ', 'В 1987 Г.'], colors=[NAVY, RED], seed=2, tilt=-3), 18, 345),
        (R.plate(80, 18, ['ТАЙГА-ЛАЙФХАК'], bg=(30, 110, 200), fg=WH, border=WH, round_=2.0, pad=1.0, tilt=4), 150, 120),
    ])
    D.anim(W, flakes((0, 0, 1280, 720), n=70, seed=11, speed=16.0))
    D.anim(W, sparkles((450, 480, 1280, 720), n=40, seed=12))


def dress_taiga2(W):
    D.attach(W, [
        (R.plate(56, 28, ['НЕ', 'БУДИТЬ!'], bg=PLY, fg=RED, border=(110, 80, 50), weights=[0.8, 1.0], tilt=-5, hand=True, seed=5), 912, 452),
        (birch(60, 26, ['ЛОВИТ', 'ТУТ ^'], colors=[NAVY, RED], seed=8), 1092, 420),
        (_post(7, 150), 368, 466),
        (R.plate(84, 20, ['ГОРОД 400 КМ >'], bg=(240, 236, 220), fg=BLK, border=(60, 50, 40), tilt=2), 330, 470),
        (R.plate(76, 20, ['ПВЗ 40 КМ >'], bg=(250, 210, 60), fg=BLK, border=(60, 50, 40), tilt=-3), 336, 494),
        (birch(84, 22, ['ТАЙГА-ЛАЙФХАК'], colors=[(30, 110, 200)], seed=9), 96, 300),
    ])
    place_sprite(W, C.meter, 700, 590, 2.4, rub=0, spin=0.0)
    D.anim(W, sparkles((0, 520, 1280, 720), n=70, seed=7))
    D.anim(W, flakes((0, 0, 1280, 720), n=70, seed=8, speed=14.0))


def dress_den2(W):
    D.anim(W, beam_dust((640, 60, 800, 470), n=36))


DRESS.update(porch=dress_porch, taiga2=dress_taiga2, den2=dress_den2)
