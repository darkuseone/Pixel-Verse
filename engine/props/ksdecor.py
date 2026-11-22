"""«Ключевой сотрудник» set dressing (rule 10.10.2026: dense local atmosphere) for the office worlds (office / office_night /
office_morning share one layout): door plate of the boss, «ООО ВЕКТОР-СНАБ-СБЫТ», the honor board with the empty «СОТРУДНИК ГОДА — ?»
frame (the season thread), «МЫ — ОДНА СЕМЬЯ!», «ПРИНТЕР НЕ РАБОТАЕТ (С 2019)», «КТО ВЗЯЛ МОЮ КРУЖКУ — ВЕРНИ!», «ВОДИЧКА-ОФИС»,
password sticker, kitten calendar; animated: the wall clock (time set per shot: CLOCK[0] = 'HH:MM'), snow behind the window, dust
in the lamp light. dress(name, world) is called once by kskit.world()."""
import math
import numpy as np
from props import decals as D
from props import rusigns as R

WH, BLK, RED, NAVY = (250, 248, 238), (34, 30, 28), (190, 40, 40), (30, 50, 120)
YEL, BRASS, CORK = (255, 226, 90), (214, 180, 90), (176, 130, 80)
CLOCK = ['17:59']                       # set by the episode before drawing a frame
FRAME_FILL = [None]                     # E06: a photo in the empty «СОТРУДНИК ГОДА» frame


def clock(cx=137.0, cy=107.0, r=31.0):
    """the wall clock over the boss's door: white face, 12 ticks, hands from CLOCK[0]"""
    def f(big, v, t):
        hh, mm = (int(x) for x in CLOCK[0].split(':'))
        ox, oy = v.opt(cx, cy); R_ = r * v.Z * 3
        if ox + R_ < 0 or ox - R_ > big.shape[1] or oy + R_ < 0 or oy - R_ > big.shape[0]: return
        x0, x1 = int(max(0, ox - R_)), int(min(big.shape[1], ox + R_ + 1))
        y0, y1 = int(max(0, oy - R_)), int(min(big.shape[0], oy + R_ + 1))
        yy, xx = np.mgrid[y0:y1, x0:x1]
        d = np.hypot(xx - ox, yy - oy)
        reg = big[y0:y1, x0:x1]
        reg[d < R_] = (238, 234, 220)
        reg[(d >= R_ * 0.90) & (d < R_)] = (40, 36, 34)
        q = max(2, int(v.Z * 3 * 1.3))
        for k in range(12):
            a = k / 12 * 2 * math.pi
            tx, ty = ox + math.sin(a) * R_ * 0.78, oy - math.cos(a) * R_ * 0.78
            s_ = q * (2 if k % 3 == 0 else 1)
            big[int(ty) - s_ // 2:int(ty) + s_ // 2 + 1, int(tx) - s_ // 2:int(tx) + s_ // 2 + 1] = (40, 36, 34)
        for ang, ln, w, c in (((hh % 12 + mm / 60) / 12, 0.50, 2.2, (30, 26, 24)), (mm / 60, 0.78, 1.5, (30, 26, 24)),
                              (((t * 1.0) % 60) / 60, 0.80, 0.6, (200, 40, 40))):
            a = ang * 2 * math.pi
            n = int(R_ * ln)
            for i in range(n):
                x = int(ox + math.sin(a) * i); y = int(oy - math.cos(a) * i); ww = max(1, int(w * v.Z * 1.5))
                if 0 <= y - ww and y + ww < big.shape[0] and 0 <= x - ww and x + ww < big.shape[1]:
                    big[y - ww:y + ww + 1, x - ww:x + ww + 1] = c
        big[int(oy) - q:int(oy) + q + 1, int(ox) - q:int(ox) + q + 1] = (200, 40, 40)
    return f


def flakes(box, n=60, seed=5, speed=14.0, col=(236, 242, 255)):
    r = np.random.default_rng(seed)
    P = [(r.random(), r.random(), 0.5 + r.random(), r.random() * 6.28) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, s, ph in P:
            y = y0 + ((w * (y1 - y0) + t * speed * s) % (y1 - y0))
            x = x0 + u * (x1 - x0) + math.sin(t * 0.9 + ph) * 5
            ox, oy = v.opt(x, y)
            q = max(2, int(0.8 * s * v.Z * 3))
            ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q:
                big[iy:iy + q, ix:ix + q] = col
    return f


def dust(box, n=28, seed=9, col=(255, 236, 190)):
    r = np.random.default_rng(seed)
    P = [(r.random(), r.random(), r.random() * 6.28) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, ph in P:
            yy = y0 + ((w + t * 0.02) % 1.0) * (y1 - y0)
            xx = x0 + u * (x1 - x0) + math.sin(t * 0.6 + ph) * 6
            ox, oy = v.opt(xx, yy)
            q = max(2, int(0.5 * v.Z * 3)); ix, iy = int(ox), int(oy)
            if 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q and math.sin(t * 2 + ph) > -0.2:
                big[iy:iy + q, ix:ix + q] = col
    return f


def frame_fill():
    def f(big, v, t):
        if FRAME_FILL[0] is not None: FRAME_FILL[0](big, v, t)
    return f


def dress(name, W):
    if not name.startswith('office'): return
    night = name == 'office_night'
    D.attach(W, [
        (R.plate(250, 20, ['ООО «ВЕКТОР-СНАБ-СБЫТ»'], bg=(40, 70, 130), fg=WH, border=BRASS, bw=1.2), 306, 104),
        (R.plate(54, 16, ['В. П. ГРОМОВ', 'ГЕН. ДИРЕКТОР'], bg=BRASS, colors=[BLK, BLK], border=(120, 90, 40), weights=[1, 0.7], pad=1.0), 104, 251),
        (R.plate(66, 28, ['ПЛАНЁРКА 8:00', 'БЕЗ ОПОЗДАНИЙ!'], bg=WH, colors=[NAVY, RED], border=NAVY, pad=1.2), 96, 300),
        (R.plate(120, 16, ['ДОСКА ПОЧЁТА'], bg=(170, 30, 40), fg=(250, 220, 120), border=(250, 220, 120)), 372, 132),
        (R.plate(56, 92, ['СОТРУДНИК', 'ГОДА', '?'], bg=(244, 236, 214), colors=[RED, RED, BLK], border=(150, 110, 60),
                 weights=[0.6, 0.6, 2.6], bw=2.0, pad=1.6), 589, 190),
        (R.plate(70, 64, ['МЫ —', 'ОДНА', 'СЕМЬЯ!'], bg=(250, 214, 80), colors=[RED, RED, RED], border=RED, pad=1.4, tilt=-2), 1195, 110),
        (R.plate(42, 22, ['ВЫКЛЮЧАЙТЕ', 'СВЕТ!'], bg=WH, colors=[BLK, RED], border=BLK, pad=0.8), 236, 280),
        (R.plate(64, 26, ['ПРИНТЕР НЕ', 'РАБОТАЕТ (С 2019)'], bg=WH, colors=[RED, BLK], border=RED, pad=1.0, tilt=2), 1040, 500),
        (R.plate(48, 24, ['КТО ВЗЯЛ', 'КРУЖКУ — ВЕРНИ!'], bg=(255, 250, 200), colors=[BLK, RED], border=None, pad=0.8, tilt=-3), 632, 380),
        (R.plate(22, 12, ['ПАРОЛЬ', '12345'], bg=YEL, colors=[BLK, BLK], border=None, pad=0.6, tilt=4), 532, 386),
        (R.plate(58, 14, ['ВОДИЧКА-ОФИС'], bg=(40, 110, 200), fg=WH, border=WH, pad=0.8), 1190, 462),
        (R.plate(40, 50, ['КОТИКИ', '2026', 'НОЯБРЬ'], bg=(252, 246, 236), colors=[(220, 100, 40), BLK, RED], border=(120, 120, 120),
                 weights=[0.9, 1.4, 0.8], pad=1.2), 724, 180),
    ])
    D.anim(W, clock())
    D.anim(W, frame_fill())
    D.anim(W, flakes((862, 90, 1172, 352), n=50, seed=4, speed=12.0, col=(250, 250, 255) if not night else (220, 230, 255)))
    if name != 'office_morning':
        D.anim(W, dust((560, 360, 700, 470), n=18, seed=3))
