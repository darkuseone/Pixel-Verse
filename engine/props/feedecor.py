"""«Land of the Fee» set dressing (rule 10.10.2026: dense local atmosphere): American signs, bills, stickers and fine print laid over the
xAI worlds as hi-res decals (props/decals.py), plus animated ambience (dust in the sunbeam, a blinking router, store lights). Every
inscription is auto-fitted inside its plate. dress(name, world) is called once by feekit.world().
Parody brands of the series: XFEENITY (internet + phones), Fee-Bee AI, Liberty Plaza, Slice of Freedom, Liberty Lofts."""
import math
import numpy as np
from props import decals as D

RED, NAVY, BLK, WH = (200, 40, 48), (34, 48, 104), (28, 26, 30), (250, 248, 238)
YEL, GRN, MINT, PURP = (255, 214, 60), (34, 110, 70), (110, 240, 196), (126, 72, 190)
CREAM = (250, 242, 220)
MONEY = (40, 96, 64)


# ---------------------------------------------------------------- animated ambience
def dust_beam(box, n=26, seed=9, col=(255, 240, 200)):
    """dust motes glittering in the window sunbeam"""
    r = np.random.default_rng(seed)
    P_ = [(r.random(), r.random(), r.random() * 6.28) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, ph in P_:
            yy = y0 + ((w + t * 0.02) % 1.0) * (y1 - y0)
            xx = x0 + u * (x1 - x0) + math.sin(t * 0.5 + ph) * 8
            ox, oy = v.opt(xx, yy)
            q = max(3, int(0.6 * v.Z * 3)); ix, iy = int(ox), int(oy)
            if (math.sin(t * 2.0 + ph * 3) > 0.1) and 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q:
                big[iy:iy + q, ix:ix + q] = col
    return f


def blink(x, y, w, h, col, period=0.6, duty=0.5, phase=0.0):
    """a small light that blinks (router LED, OPEN sign)"""
    def f(big, v, t):
        if ((t + phase) % period) / period > duty: return
        ox0, oy0 = v.opt(x, y); ox1, oy1 = v.opt(x + w, y + h)
        X0, X1, Y0, Y1 = int(ox0), int(ox1) + 1, int(oy0), int(oy1) + 1
        X0, Y0 = max(0, X0), max(0, Y0); X1, Y1 = min(big.shape[1], X1), min(big.shape[0], Y1)
        if X0 < X1 and Y0 < Y1: big[Y0:Y1, X0:X1] = col
    return f


def clouds(y0, y1, n=3, seed=2, speed=6.0):
    """slow pixel clouds drifting over the sky band (mall)"""
    r = np.random.default_rng(seed)
    P_ = [(r.random() * 1280, y0 + r.random() * (y1 - y0), 30 + r.random() * 40) for _ in range(n)]
    def f(big, v, t):
        for (x, y, s) in P_:
            xx = (x + t * speed) % 1400 - 60
            for k, (dx, dy, rr) in enumerate(((0, 0, 1.0), (s * 0.5, -s * 0.15, 0.8), (-s * 0.5, -s * 0.05, 0.7))):
                ox, oy = v.opt(xx + dx, y + dy)
                R = s * 0.35 * rr * v.Z * 3
                q = max(6, int(2 * v.Z * 3))
                X0, X1, Y0, Y1 = int(max(0, ox - R)), int(min(big.shape[1], ox + R)), int(max(0, oy - R * 0.6)), int(min(big.shape[0], oy + R * 0.6))
                if X0 >= X1 or Y0 >= Y1: continue
                yy, xx_ = np.mgrid[Y0:Y1, X0:X1]
                m = (((xx_ // q) * q - ox) / R) ** 2 + (((yy // q) * q - oy) / (R * 0.6)) ** 2 <= 1
                reg = big[Y0:Y1, X0:X1]
                reg[m] = (reg[m] * 0.25 + np.array((250, 252, 255)) * 0.75).astype(np.uint8)
    return f


# ---------------------------------------------------------------- Duke's studio apartment (apartment.png)
def dress_apartment(W):
    D.attach(W, [
        (D.plate(56, 30, ['XFEENITY', 'PAST DUE'], bg=WH, colors=[PURP, RED], border=PURP, pad=1.0, tilt=-4), 22, 182),       # bills on the fridge
        (D.plate(52, 30, ['RENT', '$2,400'], bg=CREAM, colors=[NAVY, RED], border=NAVY, pad=1.0, tilt=3), 104, 176),
        (D.plate(58, 26, ['FINAL', 'NOTICE'], bg=(255, 220, 220), colors=[RED, RED], border=RED, pad=1.0, tilt=-2), 26, 300),
        (D.plate(56, 34, ['PAPER BILL', 'FEE $9.99', '(BY EMAIL)'], bg=WH, colors=[BLK, RED, BLK], border=(120, 120, 130),
                 weights=[0.8, 0.9, 0.6], pad=1.0, tilt=5), 104, 288),
        (D.plate(50, 22, ['LATE FEE', 'FOR LATE FEE'], bg=YEL, colors=[BLK, RED], border=BLK, pad=0.8, tilt=-6), 60, 420),
        (D.plate(72, 120, ['MAJESTIC', 'SINCE', '1782'], bg=(28, 44, 96), colors=[YEL, WH, YEL], border=(200, 160, 60),
                 weights=[0.9, 0.7, 1.2], bw=1.4, pad=2.0), 1094, 150),                                               # poster in the frame
        (D.plate(58, 70, ["WORLD'S", 'OKAYEST', 'EAGLE'], bg=CREAM, colors=[NAVY, RED, NAVY], border=(110, 70, 40), pad=1.4), 1198, 205),
        (D.plate(120, 24, ['HOME SWEET RENTED HOME'], bg=(196, 150, 96), fg=(250, 240, 220), border=(110, 70, 40), round_=1.0), 404, 92),
        (D.plate(34, 10, ['XFEENITY'], bg=(40, 40, 50), fg=PURP, border=None, pad=0.4), 520, 196),                        # on the router
        (D.sticker('NO PIGEONS', bg=RED, fg=WH, w=40, h=10, tilt=-5), 906, 116),                                          # on the window glass
        (D.plate(54, 16, ['WI-FI: DOWN', '(AGAIN)'], bg=WH, colors=[RED, BLK], border=RED, pad=0.6, tilt=2), 610, 236),
    ])
    D.anim(W, dust_beam((520, 120, 900, 520), n=28, seed=11))
    D.anim(W, blink(539, 214, 4, 3, (255, 50, 40), 0.5, 0.5))
    D.anim(W, blink(551, 214, 4, 3, (255, 50, 40), 0.5, 0.5, 0.25))


# ---------------------------------------------------------------- Liberty Plaza strip mall (mall.png)
def dress_mall(W):
    D.attach(W, [
        (D.plate(190, 42, ['XFEENITY'], bg=(40, 30, 70), fg=MINT, border=PURP, bw=1.4, pad=2.0), 669, 290),
        (D.plate(88, 26, ['NOW 100% AI!'], bg=MINT, fg=(20, 40, 50), border=WH, pad=1.0), 718, 376),
        (D.plate(112, 12, ['*HUMANS AVAILABLE (FEES APPLY)'], bg=WH, fg=BLK, border=None, pad=0.4), 706, 448),
        (D.plate(76, 40, ['LIBERTY', 'PLAZA'], bg=CREAM, colors=[NAVY, RED], border=NAVY, pad=1.2), 32, 160),              # pylon panels
        (D.plate(76, 38, ['NAILS', 'PIZZA', 'FEES'], bg=(176, 210, 236), colors=[NAVY, NAVY, RED], border=NAVY, pad=1.0), 32, 206),
        (D.plate(76, 40, ['PARKING', '$5 / 15 MIN'], bg=RED, colors=[WH, YEL], border=WH, pad=1.2), 32, 250),
        (D.plate(144, 40, ['NAIL IT', 'NAILS & SPA'], bg=(210, 240, 214), colors=[GRN, BLK], border=GRN, weights=[1.3, 0.6], pad=1.4), 168, 302),
        (D.plate(150, 40, ['SLICE OF', 'FREEDOM'], bg=(252, 230, 196), colors=[RED, NAVY], border=(150, 50, 40), pad=1.4), 416, 298),
        (D.plate(168, 40, ['COIN LAUNDRY', '$8 A LOAD (LOL)'], bg=(200, 240, 236), colors=[NAVY, RED], border=NAVY, weights=[1.0, 0.7], pad=1.4), 965, 300),
        (D.sticker('PARKING ENFORCED BY FEE-BEE', bg=YEL, fg=BLK, w=120, h=12), 820, 520),
    ])
    D.anim(W, clouds(20, 200, n=4, seed=3))
    D.anim(W, blink(740, 470, 40, 4, (140, 255, 210), 1.2, 0.7))


# ---------------------------------------------------------------- XFEENITY store interior (store.png)
def dress_store(W):
    D.attach(W, [
        (D.plate(196, 176, ['XFEENITY', 'NOW WITH', 'FEE-BEE AI', 'NO HUMANS!', '(YAY!)'], bg=(40, 30, 70), colors=[MINT, WH, MINT, YEL, WH],
                 border=None, weights=[1.3, 0.7, 1.0, 0.9, 0.6], pad=2.0), 44, 170),                                    # left wall screen
        (D.plate(244, 124, ['YOUR CALL IS', 'IMPORTANT TO US', "(IT ISN'T)"], bg=(30, 40, 70), colors=[WH, WH, YEL], border=None,
                 weights=[1.0, 1.0, 0.8], pad=2.0), 371, 220),
        (D.plate(170, 24, ['SERVICE DESK: CLOSED (FOREVER)'], bg=RED, fg=WH, border=WH, pad=1.0), 30, 460),
        (D.plate(66, 30, ['HUMANS', 'BY APPOINTMENT'], bg=WH, colors=[NAVY, RED], border=NAVY, pad=1.0), 1150, 214),
        (D.plate(40, 12, ['$1,299 + FEES'], bg=YEL, fg=BLK, border=BLK, pad=0.4), 300, 480),
        (D.plate(40, 12, ['$899 + FEES'], bg=YEL, fg=BLK, border=BLK, pad=0.4), 462, 560),
        (D.plate(44, 12, ['ROUTER RENTAL', ], bg=YEL, fg=BLK, border=BLK, pad=0.4), 520, 470),
        (D.sticker('UPGRADE TODAY!', bg=PURP, fg=WH, w=64, h=12, tilt=-4), 760, 230),
    ])
    D.anim(W, dust_beam((100, 60, 1200, 500), n=16, seed=5, col=(255, 255, 255)))


DRESS = dict(apartment=dress_apartment, mall=dress_mall, store=dress_store)


def dress(name, W):
    fn = DRESS.get(name)
    if fn: fn(W)
