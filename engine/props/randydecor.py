"""«Thanks, Randy» set dressing (rule 10.10.2026: dense local atmosphere): American signs, price cards, banners, stickers and props laid
over the xAI worlds as hi-res decals (props/decals.py, Latin 3x5 font), plus animated ambience (freezer mist, dust in the lamp light,
drifting autumn leaves). Every inscription is auto-fitted inside its plate. dress(name, world) is called once by randykit.world().
Parody brands of the series: Shop'n'Weep (supermarket), Butterbutt (frozen turkeys, Turkey Talk-Line 1-800-GOBBLE), Fry-Hard 3000,
StreamFlix Ultra+ Max, Best Bye, Tumbleweed Intl, Maple Falls FD."""
import math
import numpy as np
from props import decals as D

RED, NAVY, BLK, WH = (196, 34, 40), (30, 44, 96), (28, 26, 30), (250, 248, 238)
YEL, ORG, GRN = (255, 214, 60), (236, 120, 40), (46, 120, 70)
CREAM = (250, 240, 214)


# ---------------------------------------------------------------- animated ambience
def mist(box, n=10, seed=3, col=(220, 240, 255)):
    """cold freezer mist curling up (chunky translucent puffs)"""
    r = np.random.default_rng(seed)
    P_ = [(r.random(), r.random(), 0.6 + r.random() * 0.6) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, ph, sp in P_:
            k = (t * 0.18 * sp + ph) % 1.0
            x = x0 + u * (x1 - x0) + math.sin(t * 0.8 + ph * 6) * 10
            y = y1 - k * (y1 - y0)
            ox, oy = v.opt(x, y)
            rr = (10 + 26 * k) * v.Z * 3
            a = 0.22 * math.sin(math.pi * k)
            q = max(6, int(3 * v.Z * 3))
            X0, X1 = int(max(0, ox - rr)), int(min(big.shape[1], ox + rr)); Y0, Y1 = int(max(0, oy - rr)), int(min(big.shape[0], oy + rr))
            if X0 >= X1 or Y0 >= Y1: continue
            yy, xx = np.mgrid[Y0:Y1, X0:X1]
            m = (((xx // q) * q + q / 2 - ox) ** 2 + ((yy // q) * q + q / 2 - oy) ** 2) <= rr * rr
            reg = big[Y0:Y1, X0:X1]
            reg[m] = (reg[m] * (1 - a) + np.array(col) * a).astype(np.uint8)
    return f


def dust(box, n=24, seed=9, col=(255, 244, 210)):
    """dust motes glittering under the store lamps"""
    r = np.random.default_rng(seed)
    P_ = [(r.random(), r.random(), r.random() * 6.28) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, ph in P_:
            yy = y0 + ((w + t * 0.025) % 1.0) * (y1 - y0)
            xx = x0 + u * (x1 - x0) + math.sin(t * 0.6 + ph) * 8
            ox, oy = v.opt(xx, yy)
            q = max(3, int(0.6 * v.Z * 3)); ix, iy = int(ox), int(oy)
            if (math.sin(t * 2.0 + ph * 3) > 0.2) and 0 <= ix < big.shape[1] - q and 0 <= iy < big.shape[0] - q:
                big[iy:iy + q, ix:ix + q] = col
    return f


def leaves(box, n=8, seed=5):
    """paper autumn leaves of the garland fluttering down from the ceiling (slow, chunky)"""
    r = np.random.default_rng(seed)
    cols = [(214, 80, 30), (236, 150, 40), (190, 50, 30), (226, 180, 60)]
    P_ = [(r.random(), r.random(), 0.5 + r.random(), r.random() * 6.28, cols[i % 4]) for i in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, s, ph, c in P_:
            y = y0 + ((w * (y1 - y0) + t * 14 * s) % (y1 - y0))
            x = x0 + u * (x1 - x0) + math.sin(t * 1.3 + ph) * 18
            ox, oy = v.opt(x, y)
            q = max(4, int(2.2 * v.Z * 3)); ix, iy = int(ox), int(oy)
            fl = abs(math.sin(t * 3 + ph))
            if 0 <= ix < big.shape[1] - 2 * q and 0 <= iy < big.shape[0] - q:
                big[iy:iy + max(2, int(q * fl)), ix:ix + 2 * q] = c
    return f


def lamp_blink(x, y, w, h, col=(255, 60, 60), period=0.5):
    """a blinking lamp / LED in the background (world box)"""
    def f(big, v, t):
        if int(t / period) % 2: return
        ox0, oy0 = v.opt(x, y); ox1, oy1 = v.opt(x + w, y + h)
        X0, X1 = int(max(0, ox0)), int(min(big.shape[1], ox1)); Y0, Y1 = int(max(0, oy0)), int(min(big.shape[0], oy1))
        if X0 < X1 and Y0 < Y1: big[Y0:Y1, X0:X1] = col
    return f


# ---------------------------------------------------------------- Shop'n'Weep (store.png / store_b.png, 1280x720)
def dress_store(W):
    D.attach(W, [
        (D.plate(96, 110, ["SHOP'N", 'WEEP', 'PRICES THAT', 'MOVE YOU', '(TO TEARS)'], bg=(196, 40, 36), colors=[WH, WH, YEL, YEL, CREAM],
                 border=(240, 200, 90), weights=[1.4, 1.4, 0.6, 0.6, 0.6], bw=1.2, pad=1.2), 142, 32),               # red banner
        (D.plate(92, 110, ['TURKEYS', '$3.99/LB*', '*LB =', 'LITTLE', 'BIT'], bg=(52, 118, 64), colors=[WH, YEL, CREAM, CREAM, CREAM],
                 border=(240, 200, 90), weights=[1.0, 1.1, 0.6, 0.6, 0.6], bw=1.2, pad=1.2), 862, 34),               # green banner
        (D.plate(92, 116, ['HAPPY', 'THANKS', 'GIVING', 'NO REFUNDS', 'ON GRATITUDE'], bg=(226, 112, 36), colors=[WH, WH, WH, NAVY, NAVY],
                 border=(250, 220, 120), weights=[0.9, 0.9, 0.9, 0.55, 0.55], bw=1.2, pad=1.2), 1092, 40),           # orange banner
        (D.plate(210, 22, ['SELF-CHECKOUT: YOU WORK HERE NOW'], bg=NAVY, fg=WH, border=(200, 210, 230), round_=2.0), 545, 212),  # over the far kiosks
        (D.plate(60, 16, ['ATTENDANT ON', 'BREAK SINCE 2019'], bg=YEL, fg=BLK, border=BLK, pad=0.8), 610, 352),
        (D.plate(196, 22, ['BUTTERBUTT - AMERICAS MOST FROZEN TURKEY'], bg=(240, 236, 226), colors=[NAVY], border=NAVY, round_=1.5), 150, 548),
        (D.plate(64, 30, ['LIMIT 1', 'CRANBERRY CAN', 'PER FAMILY'], bg=WH, colors=[RED, BLK, BLK], border=RED, pad=1.0, tilt=-3), 6, 300),
        (D.plate(74, 36, ['GOURDS', '(DO NOT', 'EAT)'], bg=CREAM, colors=[ORG, BLK, BLK], border=(120, 80, 40), weights=[1.2, 0.8, 0.8],
                 pad=1.2, tilt=4), 880, 470),                                                                         # price card on the pallet
        (D.plate(62, 22, ['PUMPKINS', '$19.99 EA'], bg=YEL, colors=[BLK, RED], border=BLK, pad=0.8, tilt=-2), 1090, 486),
        (D.plate(84, 18, ['TISSUES > AISLE 7', '(NEXT TO EGGS)'], bg=(40, 110, 200), colors=[WH, YEL], border=WH, pad=0.8), 380, 168),
        (D.sticker('SALE', bg=RED, fg=WH, w=24, h=10, shape='round', tilt=-8), 60, 418),
        (D.sticker('$89.99', bg=YEL, fg=RED, w=26, h=9, tilt=6), 330, 452),
    ])
    D.anim(W, mist((10, 260, 490, 420), n=12, seed=4))
    D.anim(W, dust((300, 120, 1000, 420), n=26, seed=8))
    D.anim(W, leaves((0, 80, 1280, 500), n=9, seed=6))
    D.anim(W, lamp_blink(519, 236, 7, 9, (255, 220, 60), 0.6))


def dress_store_b(W):
    D.attach(W, [
        (D.plate(110, 84, ["SHOP'N", 'WEEP', 'SINCE 1987'], bg=(52, 118, 64), colors=[WH, WH, YEL], border=(240, 200, 90),
                 weights=[1.3, 1.3, 0.6], bw=1.2, pad=1.2), 186, 70),
        (D.plate(104, 84, ['BAGS 10C', 'BAG FOR', 'BAGS 25C'], bg=(196, 52, 36), colors=[WH, YEL, WH], border=(240, 200, 90),
                 weights=[1.0, 0.7, 1.0], bw=1.2, pad=1.2), 826, 68),
        (D.plate(104, 86, ['ALL', 'TURKEYS', 'FROZEN', '(SORRY)'], bg=(232, 176, 44), colors=[NAVY, NAVY, NAVY, RED], border=(250, 220, 120),
                 weights=[0.8, 1.0, 1.0, 0.7], bw=1.2, pad=1.2), 1082, 70),
        (D.plate(240, 22, ['BUTTERBUTT - THAW TIME: 5 DAYS (LOL)'], bg=(240, 236, 226), colors=[NAVY], border=NAVY, round_=1.5), 180, 552),
        (D.plate(70, 34, ['GOURDS', '(DO NOT', 'EAT)'], bg=CREAM, colors=[ORG, BLK, BLK], border=(120, 80, 40), weights=[1.2, 0.8, 0.8],
                 pad=1.2, tilt=-4), 880, 470),
        (D.plate(56, 16, ['LANE CLOSED', '(FOREVER)'], bg=RED, colors=[WH, YEL], border=WH, pad=0.8), 752, 320),
    ])
    D.anim(W, mist((20, 180, 540, 430), n=14, seed=7))
    D.anim(W, dust((300, 120, 1000, 420), n=22, seed=3))
    D.anim(W, leaves((0, 80, 1280, 500), n=8, seed=2))
    D.anim(W, lamp_blink(788, 219, 7, 9, (255, 60, 60), 0.45))


DRESS = dict(store=dress_store, store_b=dress_store_b)


def dress(name, W):
    if name in DRESS: DRESS[name](W)
