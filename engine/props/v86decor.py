"""«STILL 1986» set dressing (rule 10.10.2026: dense local atmosphere): Miami Beach signs, a cafe menu board, parking and tow
plates, motel and lot signs laid over the xAI worlds as hi-res decals (props/decals.py, every text fitted inside its plate),
plus animated ambience (seagulls over the sunset, moths at the lamps). dress(name, world) is called once by v86kit.world().
Parody brands of the series: ParkMeMaybe (parking app), Rey's Towing 24 HR, The Palms / The Mint (hotels)."""
import math
import numpy as np
from props import decals as D

PINK, CYAN, CREAM, INK = (255, 70, 180), (60, 230, 255), (250, 244, 226), (28, 18, 64)
YEL, RED, WH, BLK = (255, 214, 60), (214, 40, 60), (248, 246, 240), (24, 20, 30)


def pole_sign(w, h, lines, pole_h, bg, fg, border, colors=None):
    """a street sign on a grey pole: plate on top, pole down to the sidewalk (one RGBA decal)"""
    pl = D.plate(w, h, lines, bg=bg, fg=fg, border=border, colors=colors)
    ws = D.WS
    H_ = pl.shape[0] + int(pole_h * ws)
    img = np.zeros((H_, pl.shape[1], 4), np.uint8)
    img[:pl.shape[0]] = pl
    c0 = pl.shape[1] // 2 - ws
    img[pl.shape[0]:, c0:c0 + 2 * ws, :3] = (120, 126, 146); img[pl.shape[0]:, c0:c0 + 2 * ws, 3] = 255
    img[pl.shape[0]:, c0:c0 + ws // 2, :3] = (170, 176, 196)
    return img


def gulls(n=3, seed=2, box=(0, 40, 1280, 200)):
    r = np.random.default_rng(seed)
    P_ = [(r.random(), r.random(), 0.6 + r.random() * 0.5) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, sp in P_:
            x = x0 + ((u + t * 0.02 * sp) % 1.0) * (x1 - x0); y = y0 + w * (y1 - y0) + math.sin(t * 1.5 + u * 9) * 6
            ox, oy = v.opt(x, y); q = max(3, int(round(v.Z * 3 * 0.9)))
            flap = 1 if (int(t * 6 + u * 10) % 2) else -1
            for k in range(-3, 4):
                yy = int(oy + abs(k) * q * 0.6 * flap * (-1)); xx = int(ox + k * q)
                if 0 <= xx < big.shape[1] - q and 0 <= yy < big.shape[0] - q: big[yy:yy + q, xx:xx + q] = (40, 26, 60)
    return f


def moths(cx, cy, n=6, seed=4):
    r = np.random.default_rng(seed)
    P_ = [(r.random() * 6.28, 6 + r.random() * 14, 1 + r.random() * 2) for _ in range(n)]
    def f(big, v, t):
        for ph, rad, sp in P_:
            x = cx + math.cos(t * sp * 3 + ph) * rad; y = cy + math.sin(t * sp * 4.3 + ph) * rad * 0.7
            ox, oy = v.opt(x, y); q = max(3, int(round(v.Z * 2)))
            if 0 <= ox < big.shape[1] - q and 0 <= oy < big.shape[0] - q: big[int(oy):int(oy) + q, int(ox):int(ox) + q] = (255, 240, 200)
    return f


def dress(name, W):
    if name in ('ocean', 'ocean_night'):
        D.attach(W, [
            (D.plate(140, 40, ['NO VACANCY'], bg=(60, 20, 70), fg=PINK, border=PINK, round_=6), 1005, 350),
            (D.plate(36, 220, ['T', 'H', 'E', ' ', 'P', 'A', 'L', 'M', 'S'], bg=(70, 24, 60), fg=(255, 220, 240), border=PINK, round_=10, lead=0.6), 600, 190),
            (D.plate(120, 20, ['THE MINT HOTEL'], bg=(230, 252, 240), fg=(30, 120, 100), border=(30, 120, 100)), 30, 424),
            (pole_sign(66, 42, ['PAY BY APP', 'ZONE 86'], 40, bg=WH, fg=INK, border=(40, 90, 200), colors=[INK, (40, 90, 200)]), 812, 470),
            (pole_sign(56, 46, ['TOW-AWAY', 'ZONE'], 38, bg=WH, fg=RED, border=RED), 352, 466),
            (D.plate(44, 50, ['MOJITO', '$19', 'HAPPY HR:', 'NEVER'], bg=(30, 40, 36), fg=WH, border=(140, 100, 60),
                     colors=[YEL, WH, CYAN, PINK]), 930, 478),
            (D.plate(70, 18, ["SPRING BREAK '86"], bg=YEL, fg=(200, 40, 120), border=(200, 40, 120)), 230, 300),
        ])
        if name == 'ocean': D.anim(W, gulls())
        else:
            D.anim(W, moths(832, 470)); D.anim(W, moths(1052, 470, seed=7))
    elif name == 'side':
        D.attach(W, [
            (D.plate(118, 60, ["REY'S TOWING", 'VIOLATORS', 'TOWED 24/7'], bg=(250, 240, 220), fg=RED, border=INK,
                     colors=[RED, INK, INK]), 455, 297),
            (D.plate(80, 22, ['PRIVATE LOT'], bg=YEL, fg=INK, border=INK), 660, 428),
            (D.plate(58, 18, ['VACANCY'], bg=(40, 20, 50), fg=CYAN, border=CYAN), 1040, 300),
            (D.plate(38, 16, ['ICE $5'], bg=WH, fg=(30, 120, 200), border=(30, 120, 200)), 1158, 432),
            (pole_sign(60, 40, ['NO PARKING', 'ANYTIME'], 36, bg=WH, fg=RED, border=RED), 300, 450),
        ])
        D.anim(W, moths(836, 300)); D.anim(W, moths(74, 300, seed=9))
    elif name == 'club':
        D.attach(W, [
            (D.plate(440, 120, ['NEON PALACE', "86 NIGHT TONIGHT"], bg=(60, 20, 70), fg=PINK, border=CYAN, colors=[PINK, CYAN], round_=12), 300, 55),
            (D.plate(90, 22, ['TICKETS'], bg=(30, 20, 40), fg=YEL, border=YEL), 790, 262),
            (D.plate(84, 40, ['CASH', 'NOT KING'], bg=WH, fg=RED, border=RED), 812, 400),
            (D.plate(64, 34, ['DRESS CODE:', 'PASTEL'], bg=(250, 240, 250), fg=(150, 40, 120), border=(150, 40, 120)), 200, 300),
            (D.plate(70, 30, ['NO REFUNDS', 'NO REGRETS'], bg=YEL, fg=INK, border=INK), 560, 330),
        ])
    elif name == 'disco':
        D.attach(W, [
            (D.plate(150, 40, ['SILENT DISCO'], bg=(30, 16, 50), fg=CYAN, border=PINK), 565, 205),
            (D.plate(110, 60, ['HEADPHONES', '$15', '+ FEES'], bg=WH, fg=INK, border=PINK, colors=[INK, RED, (120, 120, 140)]), 1120, 300),
            (D.plate(80, 26, ['BAR: $22'], bg=(30, 16, 50), fg=YEL, border=YEL), 120, 300),
        ])
    elif name == 'marina':
        D.attach(W, [
            (D.plate(84, 70, ['SPEEDBOAT', '$900/DAY', '+FUEL', '+CAPTAIN'], bg=(30, 40, 36), fg=WH, border=(140, 100, 60),
                     colors=[YEL, WH, CYAN, PINK]), 128, 462),
            (D.plate(120, 26, ["CAPT. RICO'S RENTALS"], bg=(250, 240, 220), fg=(30, 90, 150), border=(30, 90, 150)), 40, 308),
            (D.plate(70, 22, ['NO WAKE'], bg=WH, fg=RED, border=RED), 1100, 470),
            (D.plate(60, 30, ['PEDAL', '$25/HR'], bg=PINK, fg=WH, border=WH), 270, 470),
        ])
        D.anim(W, gulls(seed=5, box=(300, 60, 1280, 220)))
    elif name == 'bay':
        D.anim(W, gulls(n=4, seed=8, box=(0, 80, 1280, 300)))
    elif name == 'mall':
        D.attach(W, [
            (D.plate(380, 90, ['BYTE BUY', 'MIDNIGHT LAUNCH'], bg=(40, 16, 60), fg=PINK, border=CYAN, colors=[PINK, CYAN], round_=10), 300, 160),
            (D.plate(70, 50, ['THE DROP', '00:00'], bg=(20, 20, 30), fg=CYAN, border=CYAN), 255, 360),
            (D.plate(70, 50, ['LIMIT 1', 'PER FAN'], bg=YEL, fg=INK, border=INK), 760, 360),
            (D.plate(60, 26, ['LINE STARTS', 'HERE'], bg=WH, fg=RED, border=RED), 160, 470),
        ])
    elif name == 'tvstudio':
        D.attach(W, [
            (D.plate(220, 70, ['APPLAUSE', '$1 / CLAP'], bg=(40, 16, 60), fg=PINK, border=CYAN, colors=[PINK, YEL], round_=10), 770, 62),
            (D.plate(330, 44, ['VINCE VELOUR LIVE'], bg=(250, 240, 230), fg=(200, 40, 120), border=CYAN), 95, 515),
            (D.plate(120, 30, ['ON AIR'], bg=(200, 20, 40), fg=WH, border=WH), 30, 30),
        ])
    elif name == 'studio':
        D.attach(W, [
            (D.plate(110, 36, ["IT'S 1986"], bg=(30, 16, 50), fg=PINK, border=CYAN), 405, 140),
            (D.plate(64, 22, ['RENT DUE'], bg=WH, fg=RED, border=RED), 840, 330),
        ])
