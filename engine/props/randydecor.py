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


# ---------------------------------------------------------------- Tumbleweed Intl airport (airport.png / airport_b.png)
def dress_airport(W):
    D.attach(W, [
        (D.plate(132, 50, ['SECURITY', 'CHECKPOINT'], bg=(40, 70, 150), colors=[WH, YEL], border=(200, 210, 230), round_=2.0), 205, 34),
        (D.plate(152, 50, ['WELCOME TO ARIZONA', "IT'S A DRY HEAT (LIE)"], bg=(200, 96, 40), colors=[WH, CREAM], border=(250, 220, 160),
                 weights=[1.0, 0.8], round_=2.0), 714, 34),
        (D.plate(90, 58, ['NOW', 'BOARDING:', 'NOBODY'], bg=(20, 30, 50), colors=[(120, 220, 255), (120, 220, 255), YEL], border=None, pad=1.0), 386, 150),
        (D.plate(150, 46, ['LIQUIDS 3.4 OZ', 'YES, GRAVY TOO'], bg=WH, colors=[RED, BLK], border=RED, bw=1.4, pad=1.4), 520, 300),
        (D.plate(118, 22, ['REMOVE SHOES, BELTS, DIGNITY'], bg=YEL, fg=BLK, border=BLK, pad=0.8), 640, 488),
        (D.plate(62, 30, ['ARMS UP', 'DIGNITY DOWN'], bg=(220, 240, 250), colors=[NAVY, RED], border=NAVY, pad=1.0), 1030, 330),
        (D.plate(70, 20, ['BIN RETURN >'], bg=NAVY, fg=WH, border=WH, pad=0.8), 110, 500),
        (D.plate(170, 22, ['TUMBLEWEED INTL AIRPORT'], bg=(250, 240, 214), fg=(160, 70, 30), border=(160, 70, 30), round_=1.0), 505, 236),
        (D.sticker('WAIT HERE (FOREVER)', bg=YEL, fg=BLK, w=74, h=12, tilt=0), 470, 640),
    ])
    D.anim(W, dust((0, 80, 1280, 420), n=30, seed=12, col=(255, 236, 190)))
    D.anim(W, lamp_blink(1050, 128, 10, 6, (255, 60, 60), 0.5))


def dress_airport_b(W):
    D.attach(W, [
        (D.plate(144, 46, ['GATE B', 'DELAYED: YES'], bg=(40, 70, 150), colors=[WH, YEL], border=(200, 210, 230), round_=2.0), 133, 84),
        (D.plate(144, 46, ['CONFISCATED', 'TODAY: 312 GRAVIES'], bg=(196, 40, 36), colors=[WH, YEL], border=(250, 220, 160),
                 weights=[1.0, 0.8], round_=2.0), 1003, 84),
        (D.plate(84, 60, ['LANE 2', 'GRAVY', 'CHECK'], bg=(20, 30, 50), colors=[(120, 220, 255), YEL, YEL], border=None, pad=1.0), 852, 312),
        (D.plate(120, 40, ['LIQUIDS 3.4 OZ', 'YES, GRAVY TOO'], bg=WH, colors=[RED, BLK], border=RED, bw=1.4, pad=1.2), 610, 340),
        (D.plate(86, 18, ['BIN RETURN >'], bg=NAVY, fg=WH, border=WH, pad=0.8), 300, 470),
    ])
    D.anim(W, dust((0, 80, 1280, 420), n=26, seed=13, col=(255, 236, 190)))


# ---------------------------------------------------------------- Randy's kitchen at night (kitchen.png / kitchen_b.png)
def dress_kitchen(W):
    D.attach(W, [
        (D.plate(72, 76, ['THANKS-', 'GIVING:', 'TOMORROW', '!!!', 'TOM: ROCK'], bg=WH, colors=[NAVY, NAVY, RED, RED, (40, 110, 200)],
                 border=(70, 120, 200), weights=[0.8, 0.8, 0.9, 0.9, 0.7], pad=1.0, tilt=-2), 244, 170),
        (D.plate(74, 70, ['NOV', '25', 'WED'], bg=WH, colors=[RED, BLK, BLK], border=(150, 150, 160), weights=[0.6, 1.4, 0.6], pad=1.2), 138, 163),
        (D.plate(130, 30, ['LIVE * LAUGH * LOAF'], bg=(196, 150, 96), fg=(250, 240, 220), border=(110, 70, 40), round_=1.0), 262, 66),
        (D.plate(114, 26, ["NANA'S TUPPERWARE", 'RETURN OR ELSE'], bg=(250, 246, 226), colors=[(120, 60, 140), RED], border=(120, 60, 140), pad=0.8), 92, 66),
        (D.plate(70, 22, ['SMOKE ALARM:', 'NOT TODAY'], bg=YEL, colors=[BLK, RED], border=BLK, pad=0.8, tilt=3), 1120, 40),
        (D.plate(76, 42, ['HOW TO THAW:', '1. PLAN', '2. TOO LATE'], bg=CREAM, colors=[NAVY, BLK, RED], border=(150, 120, 80), pad=1.0, tilt=4), 362, 238),
        (D.plate(140, 18, ['GO AWAY (JK) HAPPY TURKEY'], bg=(150, 90, 50), fg=(250, 230, 190), border=(90, 54, 30), pad=0.8), 1092, 598),
    ])
    D.anim(W, dust((640, 120, 1000, 420), n=18, seed=21, col=(255, 236, 180)))


def dress_kitchen_b(W):
    D.attach(W, [
        (D.plate(132, 74, ['THANKSGIVING:', 'TOMORROW!!!', 'TOM: ROCK'], bg=WH, colors=[NAVY, RED, (40, 110, 200)], border=None,
                 weights=[0.8, 0.9, 0.8], pad=1.2), 112, 430),
        (D.plate(70, 68, ['NOV', '25', 'WED'], bg=WH, colors=[RED, BLK, BLK], border=(150, 150, 160), weights=[0.6, 1.4, 0.6], pad=1.2), 176, 188),
        (D.plate(140, 28, ['LIVE * LAUGH * LOAF'], bg=(196, 150, 96), fg=(250, 240, 220), border=(110, 70, 40), round_=1.0), 312, 140),
        (D.plate(78, 44, ['HOW TO THAW:', '1. PLAN', '2. TOO LATE'], bg=CREAM, colors=[NAVY, BLK, RED], border=(150, 120, 80), pad=1.0, tilt=-3), 760, 240),
        (D.plate(150, 18, ['GO AWAY (JK) HAPPY TURKEY'], bg=(150, 90, 50), fg=(250, 230, 190), border=(90, 54, 30), pad=0.8), 1036, 560),
    ])
    D.anim(W, dust((560, 100, 900, 380), n=16, seed=22, col=(255, 236, 180)))


# ---------------------------------------------------------------- Butterbutt Turkey Talk-Line call centre (callcenter.png)
def dress_callcenter(W):
    D.attach(W, [
        (D.plate(296, 120, ['DAYS WITHOUT A', 'FROZEN TURKEY:', '0'], bg=(20, 16, 18), colors=[(255, 90, 60), (255, 90, 60), (255, 220, 60)],
                 border=(60, 60, 66), weights=[0.8, 0.8, 1.6], pad=1.6), 515, 138),
        (D.plate(78, 98, ['STAY', 'CALM', '(WE', "CAN'T)"], bg=(240, 236, 220), colors=[NAVY, NAVY, RED, RED], border=(120, 80, 50), pad=1.2), 371, 155),
        (D.plate(98, 110, ['EMPLOYEE', 'OF THE', 'MONTH:', 'OVEN'], bg=(250, 230, 160), colors=[BLK, BLK, BLK, RED], border=(150, 110, 50),
                 weights=[0.8, 0.8, 0.8, 1.3], pad=1.2), 857, 145),
        (D.plate(62, 74, ['1-800', 'GOBBLE'], bg=(40, 70, 150), colors=[WH, YEL], border=(200, 210, 230), pad=1.0), 1000, 168),
        (D.plate(80, 110, ['BUTTER', 'BUTT', 'TALK-', 'LINE', 'SINCE 81'], bg=(226, 112, 36), colors=[WH, WH, YEL, YEL, CREAM],
                 border=(250, 220, 120), pad=1.0), 1168, 152),
    ])
    D.anim(W, lamp_blink(400, 58, 90, 30, (250, 255, 230), 0.17))


# ---------------------------------------------------------------- Randy's front yard, Thanksgiving morning (yard.png / yard_b.png)
def _turkey_balloon(W, x, y, s):
    from props import randypix as RX, randycast as C
    img, (ax, ay) = D.sprite(C.inflatable_turkey, s * D.WS, RX.draw, t=0.0)
    D.PROPS.add(id(img))
    D.attach(W, [(img, x - ax / D.WS, y - ay / D.WS)])


def dress_yard(W):
    D.attach(W, [
        (D.plate(78, 92, ['MAPLE FALLS', 'FIRE DEPT', 'ANNUAL', 'TURKEY FRY', 'THU 10 AM', 'AT THE', 'STATION'], bg=WH,
                 colors=[RED, RED, BLK, RED, NAVY, BLK, BLK], border=RED, weights=[0.7, 0.7, 0.6, 0.8, 0.7, 0.6, 0.6], pad=1.0, tilt=-2), 459, 300),
        (D.plate(70, 22, ['IN CASE', 'OF RANDY'], bg=RED, colors=[WH, YEL], border=WH, pad=0.8), 150, 322),
        (D.plate(150, 30, ['OUR FRYER EXPLODED AND', 'ALL WE GOT WAS THIS SIGN'], bg=CREAM, colors=[BLK, RED], border=(90, 70, 40), pad=0.8), 1112, 432),
        (D.plate(96, 30, ['FAMILY PARKING:', 'LAWN IS FINE'], bg=(40, 110, 60), colors=[WH, YEL], border=WH, pad=0.8, tilt=3), 880, 478),
        (D.plate(26, 14, ['RANDY'], bg=WH, fg=BLK, border=None, pad=0.6), 543, 420),
    ])
    _turkey_balloon(W, 1000.0, 600.0, 3.0)
    D.anim(W, leaves((0, 120, 1280, 640), n=14, seed=31))


def dress_yard_b(W):
    D.attach(W, [
        (D.plate(70, 22, ['IN CASE', 'OF RANDY'], bg=RED, colors=[WH, YEL], border=WH, pad=0.8), 120, 360),
        (D.plate(110, 30, ['OUR FRYER EXPLODED AND', 'ALL WE GOT WAS THIS SIGN'], bg=CREAM, colors=[BLK, RED], border=(90, 70, 40), pad=0.8), 1120, 470),
        (D.plate(34, 16, ['RANDY'], bg=WH, fg=BLK, border=None, pad=0.6), 734, 470),
    ])
    _turkey_balloon(W, 1000.0, 660.0, 3.4)
    D.anim(W, leaves((0, 120, 1280, 700), n=14, seed=32))


# ---------------------------------------------------------------- living room + dinner table (living.png / living_b.png)
def dress_living(W):
    D.attach(W, [
        (D.plate(240, 104, ['GATHER', '(NOT TOO CLOSE)'], bg=(170, 120, 74), colors=[(250, 240, 220), (250, 220, 170)], border=(110, 70, 40),
                 weights=[1.6, 0.7], pad=2.0), 90, 38),
        (D.plate(96, 56, ['2:00 EAT', '2:05 NAP', '2:10 ARGUE'], bg=CREAM, colors=[NAVY, NAVY, RED], border=(150, 120, 80), pad=1.2, tilt=2), 540, 150),
        (D.plate(64, 22, ["DAD'S.", "DON'T."], bg=WH, colors=[BLK, RED], border=RED, pad=0.8, tilt=-4), 960, 296),
        (D.plate(96, 24, ["KIDS' TABLE"], bg=YEL, fg=RED, border=RED, pad=0.8, tilt=3), 1110, 452),
    ])
    D.anim(W, dust((700, 120, 1240, 420), n=18, seed=41, col=(255, 236, 180)))


def dress_living_b(W):
    D.attach(W, [
        (D.plate(160, 74, ['GATHER', '(NOT TOO CLOSE)'], bg=(170, 120, 74), colors=[(250, 240, 220), (250, 220, 170)], border=(110, 70, 40),
                 weights=[1.6, 0.7], pad=1.6), 477, 124),
        (D.plate(70, 22, ["DAD'S.", "DON'T."], bg=WH, colors=[BLK, RED], border=RED, pad=0.8, tilt=-4), 1030, 360),
        (D.plate(100, 24, ["KIDS' TABLE"], bg=YEL, fg=RED, border=RED, pad=0.8, tilt=3), 1090, 492),
    ])
    D.anim(W, dust((600, 120, 1240, 420), n=16, seed=42, col=(255, 236, 180)))


# ---------------------------------------------------------------- Best Bye, Black Friday dawn (bbout.png) + inside (bbin.png)
def dress_bbout(W):
    D.attach(W, [
        (D.plate(452, 92, ['BEST BYE'], bg=(30, 70, 170), fg=(252, 214, 40), border=(252, 214, 40), bw=2.0, pad=2.4), 386, 158),
        (D.plate(78, 120, ['BLACK', 'FRIDAY', 'DOOR-', 'BUSTERS', '(DOORS NOT', 'INCLUDED)'], bg=(30, 20, 30), colors=[YEL, YEL, WH, WH, CREAM, CREAM],
                 border=YEL, pad=1.0), 174, 304),
        (D.plate(78, 120, ['WAS $199', 'NOW', '$199', '(BUT IN', 'RED)'], bg=(30, 70, 170), colors=[WH, WH, (255, 90, 80), CREAM, CREAM],
                 border=YEL, pad=1.0), 944, 304),
        (D.plate(56, 36, ['OPEN 5 AM', 'SANITY', 'CLOSED'], bg=WH, colors=[NAVY, RED, RED], border=NAVY, pad=0.8), 434, 330),
        (D.plate(56, 36, ['LIMIT 1 PER', 'CUSTOMER', '0 PER RANDY'], bg=YEL, colors=[BLK, BLK, RED], border=BLK, pad=0.8), 712, 330),
        (D.plate(70, 22, ['NO CAMPING'], bg=RED, fg=WH, border=WH, pad=0.8), 16, 270),
        (D.plate(46, 16, ['65" $199'], bg=YEL, fg=RED, border=BLK, pad=0.6), 575, 372),
    ])
    D.anim(W, mist((0, 380, 1280, 560), n=10, seed=51, col=(220, 230, 255)))


def dress_bbin(W):
    BLU = (30, 70, 170)
    D.attach(W, [
        (D.plate(160, 92, ['BLACK', 'FRIDAY', 'DOOR-', 'BUSTERS'], bg=YEL, colors=[BLK, BLK, RED, RED], border=BLK, bw=1.2, pad=1.4), 66, 32),
        (D.plate(136, 86, ['NO', 'TRAMPLING', '(BEFORE', '5:00)'], bg=BLU, colors=[WH, WH, YEL, YEL], border=YEL, bw=1.2, pad=1.4), 333, 50),
        (D.plate(144, 66, ['SELF', 'CHECKOUT >'], bg=YEL, colors=[BLK, BLK], border=BLK, bw=1.2, pad=1.4), 815, 54),
        (D.plate(162, 84, ['WE LOVE', 'CUSTOMERS', '(FROM A', 'DISTANCE)'], bg=BLU, colors=[WH, WH, YEL, YEL], border=YEL, bw=1.2, pad=1.4), 1060, 30),
        (D.plate(118, 40, ['DISPLAY ONLY', '(EMPTY BOXES)'], bg=WH, colors=[RED, BLK], border=RED, pad=1.0), 572, 438),
        (D.plate(62, 24, ['65" $199', '1 LEFT'], bg=YEL, colors=[RED, BLK], border=BLK, pad=0.8), 452, 300),
        (D.plate(64, 22, ['SELF CHECKOUT', '(SELF BLAME)'], bg=NAVY, colors=[WH, YEL], border=WH, pad=0.8), 1104, 470),
        (D.plate(196, 18, ['OPEN BOX DEALS (BOX ONLY)'], bg=RED, fg=WH, border=WH, pad=0.8), 70, 404),
        (D.sticker('LOST SHOES >', bg=WH, fg=RED, w=58, h=12, tilt=-4), 150, 600),
    ])
    D.anim(W, dust((0, 120, 1280, 600), n=30, seed=61))


def dress_bbin_b(W):
    BLU = (30, 70, 170)
    D.attach(W, [
        (D.plate(180, 100, ['BLACK', 'FRIDAY', '5:00 AM'], bg=YEL, colors=[BLK, BLK, RED], border=BLK, bw=1.2, pad=1.4), 102, 32),
        (D.plate(72, 40, ['65"', '$199'], bg=YEL, colors=[BLK, RED], border=BLK, pad=0.8), 462, 146),
        (D.plate(178, 100, ['SELF', 'CHECKOUT', '(YOU WORK', 'HERE NOW)'], bg=BLU, colors=[WH, WH, YEL, YEL], border=YEL, bw=1.2, pad=1.4), 777, 42),
        (D.plate(66, 46, ['EXIT', '(NO)'], bg=BLU, colors=[WH, YEL], border=YEL, pad=0.8), 1077, 100),
        (D.plate(120, 40, ['DISPLAY ONLY', '(EMPTY BOXES)'], bg=WH, colors=[RED, BLK], border=RED, pad=1.0), 570, 430),
        (D.plate(70, 22, ['LANE 1', "ASK KYLE (HE WON'T)"], bg=NAVY, colors=[WH, YEL], border=WH, pad=0.8), 880, 470),
        (D.sticker('SALE', bg=RED, fg=WH, w=24, h=10, shape='round', tilt=-8), 30, 230),
    ])
    D.anim(W, dust((0, 120, 1280, 600), n=26, seed=62))


DRESS = dict(store=dress_store, store_b=dress_store_b, airport=dress_airport, airport_b=dress_airport_b, kitchen=dress_kitchen,
             kitchen_b=dress_kitchen_b, callcenter=dress_callcenter, yard=dress_yard, yard_b=dress_yard_b,
             living=dress_living, living_b=dress_living_b, bbout=dress_bbout,
             bbin=dress_bbin, bbin_b=dress_bbin_b)


def dress(name, W):
    if name in DRESS: DRESS[name](W)
