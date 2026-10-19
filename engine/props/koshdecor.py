"""«Кощей из панельки» set dressing (rule 10.10.2026: dense local atmosphere): Russian signs, notices, stickers and props laid over the
xAI worlds as hi-res decals (props/decals.py + props/rusigns.py), plus animated ambience (dust in the bulb light, moths, drifting leaves).
Every inscription is auto-fitted inside its plate. dress(name, world) is called once by koshkit.world().
Parody brands: «Соцфонд Тридесятого района», УК «Тридевятое царство», «ТЕМНОСБЫТ», банк «Сберёг», «Дикая Ягода», «Пятнюшка»."""
import math
import numpy as np
from props import decals as D
from props import rusigns as R

RED, BLK, WH = (190, 30, 34), (30, 28, 30), (244, 240, 226)
PAPER = (238, 232, 214)
GOV = (34, 70, 130)


def note(w, h, lines, seed=0, tilt=0.0, weights=None, col=BLK, bg=PAPER, hand=True):
    """a sheet of paper notice taped on a wall (two tape strips), hand-lettered"""
    img = R.plate(w, h, lines, bg=bg, fg=col, border=(150, 140, 120), bw=0.5, pad=1.6, weights=weights, hand=hand, seed=seed)
    H_, W_ = img.shape[:2]
    for x in (int(W_ * 0.15), int(W_ * 0.75)):
        img[:int(D.WS * 2.2), x:x + int(D.WS * 5)] = (230, 226, 190, 200)
    if tilt: img = D.rotate(img, tilt)
    return img


def scrawl(w, h, lines, col, seed=0, tilt=0.0, weights=None):
    """graffiti / pen scrawl straight on the wall (transparent plate)"""
    img = R.plate(w, h, lines, fg=col, border=None, transparent=True, hand=True, seed=seed, pad=0.5, weights=weights)
    return D.rotate(img, tilt) if tilt else img


def bats(x0, x1, y, n=9, seed=2):
    """a Halloween garland of black paper bats on a string (world px), as decals"""
    out = []
    rng = np.random.default_rng(seed)
    string = np.zeros((int(3 * D.WS), int((x1 - x0) * D.WS), 4), np.uint8); string[D.WS:2 * D.WS] = (60, 50, 40, 255)
    out.append((string, x0, y))
    for i in range(n):
        x = x0 + (i + 0.5) * (x1 - x0) / n
        w, h = 30, 14
        img = np.zeros((h * D.WS, w * D.WS, 4), np.uint8)
        yy, xx = np.mgrid[0:h * D.WS, 0:w * D.WS] / D.WS
        body = ((xx - w / 2) ** 2 / 4 + (yy - 5) ** 2 / 9) < 1
        wing = (np.abs(xx - w / 2) < w / 2) & (yy > 2 + np.abs(np.sin((xx - w / 2) * 0.9)) * 3) & (yy < 7 + 0.15 * np.abs(xx - w / 2))
        m = body | wing
        img[m] = (20, 16, 18, 255)
        e = m & ~(np.roll(m, D.WS, 0) & np.roll(m, -D.WS, 0) & np.roll(m, D.WS, 1) & np.roll(m, -D.WS, 1))
        img[e] = (230, 150, 40, 255)
        img[(np.abs(xx - w / 2 - 1.3) < 0.7) & (np.abs(yy - 4) < 0.7)] = (240, 200, 60, 255)
        img[(np.abs(xx - w / 2 + 1.3) < 0.7) & (np.abs(yy - 4) < 0.7)] = (240, 200, 60, 255)
        out.append((D.rotate(img, float(rng.normal(0, 8))), x - w / 2, y + 2))
    return out


# ---------------------------------------------------------------- animated ambience
def dust(box, n=30, seed=3, col=(255, 236, 180)):
    """dust motes floating in the bulb light"""
    r = np.random.default_rng(seed)
    P = [(r.random(), r.random(), r.random() * 6.28, 0.3 + r.random()) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, ph, s in P:
            x = x0 + u * (x1 - x0) + math.sin(t * 0.6 * s + ph) * 14
            y = y0 + ((w * (y1 - y0) - t * 6 * s) % (y1 - y0))
            ox, oy = v.opt(x, y)
            q = max(3, int(0.8 * v.Z * 3))
            ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q:
                big[iy:iy + q, ix:ix + q] = (big[iy:iy + q, ix:ix + q] * 0.4 + np.array(col) * 0.6).astype(np.uint8)
    return f


def moth(cx, cy, r=26, seed=1):
    """a moth circling a bulb (world px centre)"""
    def f(big, v, t):
        a = t * 5.0 + seed
        x, y = cx + math.cos(a) * r, cy + math.sin(a * 1.3) * r * 0.6
        ox, oy = v.opt(x, y)
        q = max(4, int(1.4 * v.Z * 3))
        fl = q if int(t * 24) % 2 else q // 2
        ix, iy = int(ox), int(oy)
        if q < ix < big.shape[1] - 2 * q and q < iy < big.shape[0] - q:
            big[iy:iy + q, ix - fl:ix + fl] = (200, 190, 170)
    return f


def leaves(box, n=14, seed=5):
    """yellow birch leaves drifting down (yard)"""
    r = np.random.default_rng(seed)
    P = [(r.random(), r.random(), 0.5 + r.random(), r.random() * 6.28) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, s, ph in P:
            y = y0 + ((w * (y1 - y0) + t * 22 * s) % (y1 - y0))
            x = x0 + ((u * (x1 - x0) + t * 14 * s) % (x1 - x0)) + math.sin(t * 2 + ph) * 10
            ox, oy = v.opt(x, y)
            q = max(4, int(1.6 * v.Z * 3))
            ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q:
                big[iy:iy + q, ix:ix + q + q // 2] = (230, 170, 40) if int(ph * 10) % 2 else (200, 120, 30)
    return f


def flicker_tube(box, seed=0):
    """a dying fluorescent tube: the box (world px) goes dark for a few frames now and then"""
    def f(big, v, t):
        if (math.sin(t * 7.3 + seed) + math.sin(t * 13.1)) < 1.55: return
        x0, y0 = v.opt(box[0], box[1]); x1, y1 = v.opt(box[2], box[3])
        x0, x1, y0, y1 = int(max(0, x0)), int(min(big.shape[1], x1)), int(max(0, y0)), int(min(big.shape[0], y1))
        if x0 < x1 and y0 < y1: big[y0:y1, x0:x1] = (big[y0:y1, x0:x1] * 0.35).astype(np.uint8)
    return f


# ---------------------------------------------------------------- locations
def dress(name, W):
    items = []
    if name == 'office':
        items += [(R.plate(230, 50, ['ОЧЕРЕДЬ', 'ВАШ НОМЕР: 999'], bg=(16, 14, 14), fg=(255, 60, 40), border=(60, 56, 50), weights=[0.6, 1.0], pad=1.4), 530, 84),
                  (R.plate(120, 20, ['ОКНО 1'], bg=GOV, fg=WH, border=(200, 200, 210), bw=0.6), 360, 186),
                  (R.plate(120, 20, ['ОКНО 3'], bg=GOV, fg=WH, border=(200, 200, 210), bw=0.6), 592, 186),
                  (R.plate(120, 20, ['ОКНО 7'], bg=GOV, fg=WH, border=(200, 200, 210), bw=0.6), 828, 186),
                  (note(110, 54, ['ОКНО 7', 'НЕ РАБОТАЕТ'], seed=3, tilt=-4.0, col=RED), 836, 232),
                  (R.plate(170, 70, ['СОЦФОНД', 'ТРИДЕСЯТОГО', 'РАЙОНА'], bg=GOV, fg=WH, border=(220, 190, 80), bw=1.0, weights=[1.0, 0.6, 0.6]), 110, 70),
                  (note(84, 70, ['ПЕНСИЯ —', 'ЭТО', 'ПРОСТО!'], seed=5, weights=[0.8, 0.6, 1.0], col=GOV), 1152, 196),
                  (note(84, 40, ['ПЕРЕРЫВ', '13:00–14:00'], seed=6, tilt=3.0), 1160, 282),
                  (R.plate(200, 26, ['МЕСТА ДЛЯ ЛЬГОТНИКОВ'], bg=PAPER, fg=BLK, border=(120, 110, 90), bw=0.5), 40, 330),
                  (note(54, 26, ['ВОДЫ НЕТ'], seed=7, col=RED, tilt=5.0), 1036, 300),
                  ]
        items += bats(250, 1030, 150, n=10)
        D.anim(W, dust((300, 120, 1000, 600)))
        D.anim(W, flicker_tube((1060, 20, 1180, 40)))
    elif name == 'desk':
        items += [(R.plate(120, 70, ['ГРАМОТА', 'ЗА 40 ЛЕТ', 'ОТКАЗОВ'], bg=(240, 232, 206), fg=RED, border=(170, 130, 50), bw=1.2, weights=[1.0, 0.6, 0.6]), 538, 84),
                  (R.plate(150, 30, ['ПОЛОЖЕНИЕ № 1000'], bg=(140, 40, 40), fg=WH, border=(60, 20, 20), bw=0.6), 160, 300),
                  (R.plate(130, 40, ['ОТКАЗАНО'], bg=(20, 40, 30), fg=(120, 255, 150), border=None, pad=1.0), 440, 270),
                  (note(70, 30, ['НЕ ВЛЕЗАЙ'], seed=2, col=RED, hand=False), 728, 190)]
        D.anim(W, dust((100, 60, 700, 420), n=20))
        D.anim(W, moth(150, 110))
    elif name == 'flat':
        items += [(R.plate(84, 60, ['ЛУЧШЕМУ', 'ЗЛОДЕЮ', '1342 г.'], bg=(240, 230, 200), fg=RED, border=(170, 130, 50), bw=1.2, weights=[0.8, 0.8, 0.6]), 410, 120),
                  (R.plate(120, 24, ['ХРУСТАЛЬ НЕ ТРОГАТЬ'], bg=PAPER, fg=RED, border=(120, 110, 90), bw=0.5), 110, 270)]
        D.anim(W, dust((420, 60, 900, 520), n=20))
        D.anim(W, moth(640, 110, r=34, seed=2))
    elif name == 'stairs':
        items += [(R.plate(70, 20, ['НЕ ВЛЕЗАЙ'], bg=(250, 210, 40), fg=BLK, border=BLK, bw=0.6), 436, 168),
                  (scrawl(40, 16, ['уже'], (40, 40, 160), seed=1, tilt=-8.0), 478, 192),
                  (scrawl(200, 34, ['КОЩЕЙ ЖИВ!'], (40, 40, 40), seed=2, tilt=-3.0), 680, 40),
                  (scrawl(260, 40, ['ГОРЫНЫЧ —', '3 ГОЛОВЫ, 0 МОЗГОВ'], (150, 30, 30), seed=3, tilt=2.0), 60, 30),
                  (note(200, 44, ['ТИШИНА С 23:00 ДО 7:00', 'УК «ТРИДЕВЯТОЕ ЦАРСТВО»'], seed=5, weights=[1.0, 0.6], hand=False), 380, 266),
                  (R.plate(50, 30, ['13'], bg=(230, 200, 90), fg=BLK, border=BLK, bw=0.6), 186, 214),
                  (note(70, 36, ['НЕ ЗВОНИТЬ', 'ДНЁМ СПЛЮ'], seed=6, tilt=4.0, col=RED), 176, 300),
                  (R.plate(50, 30, ['14'], bg=(230, 200, 90), fg=BLK, border=BLK, bw=0.6), 810, 230),
                  (note(70, 44, ['МУСОРО-', 'ПРОВОД', 'С 1987'], seed=7, col=RED, weights=[0.8, 0.8, 1.0]), 628, 300)]
        D.anim(W, dust((420, 60, 900, 560), n=24))
        D.anim(W, moth(612, 200, r=30, seed=4))
    elif name == 'yard':
        items += [(R.plate(120, 120, ['ХЭЛЛОУИН —', 'НЕ НАШ', 'ПРАЗДНИК!', 'НАШ —', 'СУББОТНИК'], bg=PAPER, fg=BLK, border=RED, bw=1.4,
                           colors=[BLK, BLK, RED, BLK, RED], weights=[0.8, 0.8, 1.0, 0.8, 1.0], hand=True, seed=9), 214, 214),
                  (note(60, 40, ['ПОВЕРКА', 'СЧЁТЧИКОВ'], seed=2, tilt=-4.0), 100, 250),
                  (note(50, 40, ['КУПЛЮ', 'ВОЛОСЫ'], seed=3, tilt=5.0), 136, 300),
                  (note(54, 40, ['ОТДАМ', 'КОТЯТ'], seed=4, tilt=-6.0), 1146, 190),
                  (note(54, 40, ['ПРОДАМ', 'ГАРАЖ'], seed=5, tilt=4.0), 1150, 250),
                  (R.plate(140, 24, ['НЕ СИДЕТЬ! ГОРЯЧО'], bg=(250, 210, 40), fg=BLK, border=BLK, bw=0.6), 700, 352),
                  (R.plate(130, 30, ['НЕ ПАРКОВАТЬСЯ', 'ШТРАФ'], bg=WH, fg=RED, border=RED, bw=1.0), 230, 150)]
        D.anim(W, leaves((300, 0, 1280, 640)))
    elif name == 'facade':
        items += [(R.plate(180, 26, ['КОЛЛ-ЦЕНТР 24/7'], bg=(30, 40, 90), fg=(120, 255, 150), border=(200, 200, 210), bw=0.6), 540, 340)]
    if items: D.attach(W, items)
