"""New Year props for «Валера и кот» (and any winter series): blinking garland, tinsel, tangerines, a fir sprig, a stool,
the junk that lives on every Soviet mezzanine (кирзачи, тушёнка, лыжи, гармонь, фляга, альбом «ДМБ»...), bath things
(towel, slippers, loofah), a glass, and fireworks.
Junk items are drawn in unit coords around (1000, 1000) of a Layer made with v.cam(x, y, s), rotated by `ang`.
Fireworks and the garland are emissive: draw them on the FX canvas (no hero light)."""
import math
import numpy as np
from scene import Layer
from props.folk import cap, ell, poly, dot, outline
import fx

_R = np.random.default_rng(31)
SEED = _R.random((400, 6))
BULBS = [(255, 70, 60), (90, 220, 110), (80, 150, 255), (255, 210, 70), (230, 110, 255)]


# ---------------------------------------------------------------- decorations (world coords)
def garland(FX, v, t, pts, n=24, sag=26, phase=0.0, glow_big=None):
    """string of blinking bulbs hanging between world points pts[0] -> pts[1] -> ...; returns bulb world positions"""
    L = Layer(v.wcam())
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        prev = None
        for i in range(n + 1):
            k = i / n
            x = x0 + (x1 - x0) * k; y = y0 + (y1 - y0) * k + sag * math.sin(math.pi * k)
            if prev: cap(L, prev, (x, y), 0.9, 0.9, (40, 52, 36))
            prev = (x, y)
            if 0 < i < n and i % 2 == 0: out.append((x, y + 4))
    for j, (x, y) in enumerate(out):
        on = (math.sin(t * 3.1 + j * 1.7 + phase) > -0.35)
        c = BULBS[j % len(BULBS)]
        c = c if on else tuple(int(q * 0.35) for q in c)
        ell(L, (x, y), 3.2, 4.2, c)
        dot(L, (x - 1, y - 1.5), tuple(min(255, q + 90) for q in c) if on else c, 1.0)
    FX.add(L)
    return out


def garland_glow(big, v, t, bulbs, phase=0.0, r=18, a=0.35):
    for j, (x, y) in enumerate(bulbs):
        if math.sin(t * 3.1 + j * 1.7 + phase) > -0.35:
            ox, oy = v.opt(x, y)
            fx.glow(big, ox, oy, r * v.Z * 3, BULBS[j % len(BULBS)], a)


def tinsel(FX, v, t, x0, x1, y, amp=8, col=(236, 206, 80), col2=(255, 244, 170), step=9):
    """sparkly zigzag tinsel strand along y from x0 to x1 (world)"""
    L = Layer(v.wcam())
    xs = np.arange(x0, x1, step)
    for i, x in enumerate(xs[:-1]):
        ya = y + amp * math.sin(i * 0.9) ; yb = y + amp * math.sin((i + 1) * 0.9)
        cap(L, (x, ya), (x + step, yb), 2.2, 2.2, col if (i + int(t * 6)) % 3 else col2)
        if (i * 7 + int(t * 9)) % 11 == 0: dot(L, (x, ya - 3), (255, 255, 230), 1.6)
    FX.add(L)


def tangerine(L, c, r=1.0):
    ell(L, c, 1.3 * r, 1.15 * r, (255, 140, 30), 0, (255, 186, 80), (210, 96, 20))
    dot(L, (c[0] + 0.2 * r, c[1] - 1.0 * r), (60, 110, 40), 0.3 * r)


def fir_sprig(L, base, h=6.0):
    """fir branch in a glass jar (unit coords)"""
    x, y = base
    ell(L, (x, y - 1.3), 1.4, 1.5, (170, 210, 220), 0, (220, 240, 250), (120, 160, 170))           # jar
    cap(L, (x, y - 2.4), (x + 0.3, y - h), 0.25, 0.18, (90, 60, 40))
    for i in range(6):
        k = i / 6
        yy = y - 2.8 - k * (h - 3.2); w = 2.4 * (1 - k * 0.7)
        for s in (-1, 1):
            cap(L, (x + 0.2, yy), (x + s * w, yy + 0.8), 0.45, 0.25, (40, 110, 60) if i % 2 else (56, 130, 70))
    dot(L, (x - 0.9, y - 4.0), (255, 60, 60), 0.45); dot(L, (x + 1.1, y - 5.2), (255, 220, 70), 0.4)


def stool(L, c, w=4.2, h=6.0):
    """kitchen табуретка: top centre c (unit coords), legs down"""
    x, y = c
    for s in (-1, 1):
        cap(L, (x + s * (w - 0.8), y + 0.4), (x + s * (w - 0.4), y + h), 0.45, 0.4, (150, 104, 60), None, (110, 74, 40))
    cap(L, (x - w * 0.55, y + h * 0.65), (x + w * 0.55, y + h * 0.65), 0.25, 0.25, (130, 90, 50))
    cap(L, (x - w, y), (x + w, y), 0.7, 0.7, (184, 132, 80), (214, 164, 108), (140, 96, 56))


def glass(L, h, fill=(255, 226, 120)):
    """faceted glass (гранёный стакан) with lemonade held at hand point h (unit coords)"""
    x, y = h[0] + 0.3, h[1] - 0.2
    poly(L, [(x - 0.9, y - 2.6), (x + 0.9, y - 2.6), (x + 0.75, y + 0.4), (x - 0.75, y + 0.4)], (206, 226, 232))
    poly(L, [(x - 0.8, y - 1.9), (x + 0.8, y - 1.9), (x + 0.7, y + 0.3), (x - 0.7, y + 0.3)], fill)
    for k in (-0.45, 0.0, 0.45): cap(L, (x + k, y - 2.5), (x + k * 0.9, y + 0.3), 0.06, 0.06, (240, 250, 255))
    for i in range(3): dot(L, (x - 0.3 + 0.3 * i, y - 1.2 + 0.4 * i), (255, 250, 220), 0.12)


def loofah(L, h, s=1.0):
    """мочалка (washcloth) in hand h"""
    x, y = h[0] + 0.4, h[1] - 0.4
    ell(L, (x, y), 1.5 * s, 1.0 * s, (226, 206, 120), 0.3, (246, 232, 160), (180, 156, 80))
    for i in range(6): dot(L, (x - 0.9 * s + 0.35 * i * s, y - 0.3 * s + 0.2 * (i % 2) * s), (190, 166, 90), 0.15 * s)


# ---------------------------------------------------------------- mezzanine junk (unit coords around (1000,1000), rotated)
def _rot(ang, cx=1000.0, cy=1000.0):
    ca, sa = math.cos(ang), math.sin(ang)
    return lambda x, y: (cx + x * ca - y * sa, cy + x * sa + y * ca)


def item(L, kind, ang=0.0):
    P = _rot(ang)
    if kind == 'boot':                                                                        # кирзач
        cap(L, P(0, -3.6), P(0, 0.2), 1.25, 1.2, (44, 40, 38), (86, 80, 74), (26, 24, 24))
        ell(L, P(1.3, 0.7), 2.2, 1.0, (44, 40, 38), ang, (86, 80, 74), (26, 24, 24))
        cap(L, P(-0.9, 1.5), P(3.3, 1.5), 0.3, 0.3, (22, 20, 20))
    elif kind == 'can':                                                                       # тушёнка
        poly(L, [P(-1.2, -1.6), P(1.2, -1.6), P(1.2, 1.6), P(-1.2, 1.6)], (170, 176, 184))
        poly(L, [P(-1.2, -0.7), P(1.2, -0.7), P(1.2, 0.8), P(-1.2, 0.8)], (180, 52, 44))
        cap(L, P(-0.7, 0.05), P(0.7, 0.05), 0.18, 0.18, (240, 220, 160))
        ell(L, P(0, -1.6), 1.2, 0.35, (206, 212, 220), ang)
    elif kind == 'skis':
        for dy in (-0.45, 0.45):
            cap(L, P(-7.0, dy), P(6.6, dy), 0.32, 0.32, (160, 106, 60), (200, 146, 96), (116, 74, 40))
            cap(L, P(6.6, dy), P(7.6, dy - 0.9), 0.32, 0.25, (160, 106, 60))
        cap(L, P(-0.8, -0.8), P(-0.8, 0.8), 0.3, 0.3, (60, 60, 70))
    elif kind == 'accordion':                                                                 # гармонь
        for s in (-1, 1):
            poly(L, [P(s * 1.2, -1.8), P(s * 2.6, -1.8), P(s * 2.6, 1.8), P(s * 1.2, 1.8)], (170, 40, 40))
            for j in range(3): dot(L, P(s * 1.9, -1.0 + j * 0.9), (240, 200, 90), 0.25)
        for j in range(5):
            x = -1.0 + j * 0.5
            poly(L, [P(x, -1.6), P(x + 0.25, -1.6), P(x + 0.25, 1.6), P(x, 1.6)], (30, 30, 34) if j % 2 else (200, 60, 60))
    elif kind == 'ushanka':
        ell(L, P(0, 0), 2.6, 1.7, (112, 104, 98), ang, (150, 142, 134), (80, 74, 70))
        for s in (-1, 1): ell(L, P(s * 2.3, 1.1), 0.8, 1.3, (100, 92, 86), ang)
        dot(L, P(0, -0.8), (200, 170, 60), 0.35)
    elif kind == 'canteen':                                                                   # фляга
        ell(L, P(0, 0.3), 1.6, 2.0, (86, 104, 64), ang, (120, 140, 90), (60, 74, 44))
        cap(L, P(0, -1.9), P(0, -2.6), 0.4, 0.4, (60, 60, 60))
    elif kind == 'album':                                                                     # дембельский альбом
        poly(L, [P(-2.1, -1.5), P(2.1, -1.5), P(2.1, 1.5), P(-2.1, 1.5)], (40, 52, 118))
        poly(L, [P(-1.8, -1.2), P(1.8, -1.2), P(1.8, 1.2), P(-1.8, 1.2)], (52, 66, 140))
        dot(L, P(-0.9, 0), (230, 190, 80), 0.45); dot(L, P(0, 0), (230, 190, 80), 0.45); dot(L, P(0.9, 0), (230, 190, 80), 0.45)
    elif kind == 'slippers':                                                                  # тапки
        for dx in (-1.0, 1.1):
            ell(L, P(dx, 0), 0.9, 1.9, (150, 60, 60), ang, (190, 90, 90), (110, 40, 40))
            ell(L, P(dx, -0.7), 0.95, 0.8, (230, 220, 210), ang)
    elif kind == 'towel':
        poly(L, [P(-2.6, -1.0), P(2.6, -1.0), P(2.4, 1.1), P(-2.4, 1.1)], (240, 244, 250))
        for x in (-1.6, 0.0, 1.6):
            poly(L, [P(x - 0.25, -1.0), P(x + 0.25, -1.0), P(x + 0.25, 1.1), P(x - 0.25, 1.1)], (90, 130, 220))
    elif kind == 'loofah':
        loofah(L, P(-0.4, 0.4))
    elif kind == 'basin':
        ell(L, P(0, 0), 3.4, 1.2, (150, 158, 166), ang, (196, 204, 212), (112, 118, 126))
        ell(L, P(0, 0.9), 3.0, 1.3, (136, 144, 152), ang, (176, 184, 192), (104, 110, 118))


JUNK = ['skis', 'boot', 'can', 'accordion', 'boot', 'can', 'album', 'canteen', 'basin', 'can', 'ushanka',
        'towel', 'slippers', 'loofah']


class Avalanche:
    """junk falling out of a cupboard opening box=(x0,y0,x1,y1) onto a floor with a mound around mound_x.
    item i leaves at t0 + i*gap, falls with gravity, spins, and freezes on the pile."""
    def __init__(s, t0, box, floor, mound_x, mound_h=110, mound_w=150, scale=15.0, gap=0.07, kinds=JUNK, seed=0):
        s.items = []
        rng = np.random.default_rng(seed)
        g = 1500.0
        for i, kind in enumerate(kinds):
            ts = t0 + i * gap
            x0 = box[0] + (box[2] - box[0]) * rng.uniform(0.2, 0.8); y0 = box[3] - 10
            vx = rng.uniform(-160, 160); vy = rng.uniform(-260, -40)
            w = rng.uniform(-9, 9)
            xr_guess = x0 + vx * 0.6
            hmound = mound_h * math.exp(-((xr_guess - mound_x) / mound_w) ** 2)
            yr = floor - hmound * (0.35 + 0.65 * i / len(kinds)) - rng.uniform(0, 14)
            # time to fall from y0 to yr: y0 + vy*tau + g/2 tau^2 = yr
            a, b, c = 0.5 * g, vy, y0 - yr
            tau = (-b + math.sqrt(max(0.0, b * b - 4 * a * c))) / (2 * a)
            s.items.append(dict(kind=kind, ts=ts, x0=x0, y0=y0, vx=vx, vy=vy, w=w, g=g, tau=tau,
                                a_end=rng.uniform(-0.5, 0.5) + (math.pi / 2 if kind == 'skis' and rng.random() < 0.3 else 0),
                                sc=scale * (1.25 if kind in ('skis',) else 1.0)))
        s.t_land = max(it['ts'] + it['tau'] for it in s.items)

    def state(s, it, t):
        u = t - it['ts']
        if u < 0: return None
        if u >= it['tau']:
            u = it['tau']; ang = it['a_end']
        else:
            ang = it['a_end'] - it['w'] * (it['tau'] - u)
        return (it['x0'] + it['vx'] * u, it['y0'] + it['vy'] * u + 0.5 * it['g'] * u * u, ang)

    def landed(s, kind, t):
        for it in s.items:
            if it['kind'] == kind: return t >= it['ts'] + it['tau']
        return False

    def draw(s, CH, v, t, only=None, exclude=()):
        for it in s.items:
            if only and it['kind'] not in only: continue
            if it['kind'] in exclude: continue
            st = s.state(it, t)
            if st is None: continue
            x, y, ang = st
            L = Layer(v.cam(x, y, it['sc']))
            item(L, it['kind'], ang)
            outline(L); CH.add(L)


# ---------------------------------------------------------------- fireworks
def fireworks(FX, v, t, bursts, size=1.0):
    """bursts: [(t_launch, x_ground, x_burst, y_burst, colour_index)] in world coords; rocket trail, then a ring of sparks
    falling and fading; returns [(x, y, colour, k)] of bursts currently lit (for glows / light on the scene)"""
    L = Layer(v.wcam())
    lit = []
    for j, (tl, xg, xb, yb, ci) in enumerate(bursts):
        u = t - tl
        if u < 0 or u > 2.6: continue
        c = BULBS[ci % len(BULBS)]
        if u < 0.55:                                                                           # rocket
            k = u / 0.55
            x = xg + (xb - xg) * k; y = (v.Y0 + 700 / v.Z) + (yb - (v.Y0 + 700 / v.Z)) * (1 - (1 - k) ** 2)
            dot(L, (x, y), (255, 240, 200), 1.6 * size)
            for q in range(4): dot(L, (x - (xb - xg) * 0.02 * q, y + 7 * q * size), (255, 190, 120), (1.2 - 0.25 * q) * size)
            continue
        w = u - 0.55
        fade = max(0.0, 1 - w / 2.0)
        n = 30

        def pos(i, ww):
            a = i / n * 2 * math.pi + SEED[j, 0]
            sp = (110 + 50 * SEED[(i + j) % 400, 1]) * size
            return (xb + math.cos(a) * sp * (1 - math.exp(-3 * ww)),
                    yb + math.sin(a) * sp * (1 - math.exp(-3 * ww)) + 55 * ww * ww * size)
        for i in range(n):
            if fade < 0.05 or (i + int(t * 20)) % 6 == 0: continue
            cc = tuple(int(255 - (255 - q) * min(1.0, w * 2.5)) for q in c)
            p1 = pos(i, w); p0 = pos(i, max(0.0, w - 0.09))                              # streak = short trail
            cap(L, p0, p1, (1.2 * fade + 0.5) * size, (2.2 * fade + 0.8) * size, cc)
        if w < 0.12:                                                                   # the bang
            ell(L, (xb, yb), 18 * size * (1 - w / 0.12) + 4, 18 * size * (1 - w / 0.12) + 4, (255, 250, 230))
        lit.append((xb, yb, c, fade))
    FX.add(L)
    return lit
