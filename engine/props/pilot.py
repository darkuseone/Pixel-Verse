"""Props of the pilot two episodes (S01E01/E02) in the shared hybrid style: barrel-cactus suit, sign post with poster, vulture,
spilled carrots, hatted rider. All take a Chars canvas and a stage.View (any aspect)."""
import math
import scene as S
from scene import Layer, cap, dot, outline
from stage import ell, wrect, px_text
import stage as ST
from props import chars as C


def rider_hat(pose, mouth=0.0, hat=True, rot=0.05):
    """Billy in the saddle (for chars.molniya(rider=...)); hat=True keeps the hat on his head"""
    def f(L, T):
        hip = T(-1.0, -9.4)
        S.CC['mst'] = (96, 60, 36)
        S.cowboy(L, hip, rot, pose, hat_on=hat, mouth=mouth)
        HP = C.HPf(rot, hip)
        if not hat:
            ell(L, HP(0.4, 11.4), 2.9, 1.5, (104, 66, 40), rot, hi=(136, 90, 56))
        cap(L, HP(1.4, 8.55), HP(3.1, 8.45), 0.55, 0.45, (96, 60, 36))
    return f


def cactus_big(CH, v, x, feet, wob=0.0):
    L = Layer(v.cam(x, feet + 8, 7.0))
    S.cactus(L, 1000.0, 1000.0, wob)
    outline(L, (40, 72, 36)); CH.add(L)


def costume(CH, v, x, feet, u, wob=0.0, squash=1.0, hand=0.0, spines=1.0):
    """barrel-cactus suit; Billy's eyes look out of a dark hole. anchor (1000,1000) = body centre"""
    L = Layer(v.cam(x + wob, feet - 6 * u * squash, u))
    g, gh, gs = (70, 140, 66), (112, 180, 92), (44, 100, 50)
    ell(L, (1000.0, 1000.0), 7.2, 6.4 * squash, g, hi=gh, sh=gs)
    for k in (-4.5, -2.4, 0.0, 2.4, 4.5):
        cap(L, (1000.0 + k, 995.2 + 0.6), (1000.0 + k * 0.95, 1004.8 * squash + 1000 * (1 - squash) + 0.0), 0.22, 0.22, gs)
    for k in (-4.5, -2.4, 0.0, 2.4, 4.5):
        for yy in (-4.2, -1.6, 1.0, 3.6):
            dot(L, (1000.0 + k * 0.95, 1000.0 + yy * squash), (238, 234, 200), 0.24 * spines)
    ell(L, (1000.0, 993.9 + 6.4 * (1 - squash)), 1.7, 0.9, (240, 110, 160))
    ell(L, (1000.0 + 0.2, 999.4), 3.6, 2.3, (26, 18, 18))
    for ex in (-1.3, 1.5):
        ell(L, (1000.0 + ex, 999.1), 1.0, 1.25, (250, 250, 244)); dot(L, (1000.0 + ex + 0.2, 999.2), (20, 14, 12), 0.45)
    if hand > 0:
        hx = 1007.0 + 5.5 * hand
        cap(L, (1006.0, 1001.0), (hx, 1000.0 - 2.5 * hand), 1.5, 1.2, (170, 60, 50))
        dot(L, (hx + 0.8, 1000.0 - 2.7 * hand), (226, 176, 136), 1.2)
    outline(L, (30, 60, 30)); CH.add(L)


def costume_halves(CH, v, x, feet, u, k):
    """the suit bursts into two halves (k = seconds since the pop)"""
    for side in (-1, 1):
        L = Layer(v.cam(x + side * (3 + 34 * k), feet - 6 * u + (-90 * k + 220 * k * k), u))
        ell(L, (1000.0, 1000.0), 3.6, 6.4, (70, 140, 66), hi=(112, 180, 92), sh=(44, 100, 50), ang=side * k * 2.2)
        for yy in (-3, 0, 3): dot(L, (1000.0 + side * 1.0, 1000.0 + yy), (238, 234, 200), 0.24)
        outline(L, (30, 60, 30)); CH.add(L)


def signpost(CH, v, x, feet):
    L = Layer(v.wcam())
    wrect(L, x - 5, feet - 205, x + 5, feet, (112, 74, 42)); wrect(L, x - 5, feet - 205, x - 2, feet, (146, 100, 60))
    for i, (y0, wx0, wx1) in enumerate(((feet - 195, x - 74, x + 8), (feet - 172, x - 60, x + 8))):
        wrect(L, wx0, y0, wx1, y0 + 18, (150, 104, 60)); wrect(L, wx0, y0 + 16, wx1, y0 + 18, (96, 62, 36))
    wrect(L, x + 8, feet - 168, x + 78, feet - 96, (232, 218, 176)); wrect(L, x + 8, feet - 168, x + 78, feet - 165, (196, 172, 124))
    wrect(L, x + 34, feet - 146, x + 52, feet - 138, (46, 40, 48)); wrect(L, x + 36, feet - 138, x + 50, feet - 128, (226, 176, 136))
    wrect(L, x + 36, feet - 135, x + 50, feet - 132, (24, 20, 24)); wrect(L, x + 38, feet - 134, x + 40, feet - 133, (240, 240, 240))
    outline(L, (50, 30, 18)); CH.add(L)
    if v.Z >= 0.7:
        for txt, wx, wy, col in (('САЛУН', x - 33, feet - 186, (60, 34, 20)), ('ТЮРЬМА', x - 26, feet - 163, (60, 34, 20)),
                                 ('РОЗЫСК', x + 43, feet - 158, (140, 36, 26)), ('$500', x + 43, feet - 112, (90, 50, 30))):
            sx, sy = v.pt(wx, wy); px_text(CH, txt, sx, sy, 8 if ST.PX[0] == 1 else 8, col)


def vulture(CH, v, x, y, t):
    L = Layer(v.cam(x, y, 4.0))
    ell(L, (1000.0, 1000.0), 3.6, 2.6, (44, 36, 36), hi=(70, 60, 58))
    cap(L, (1002.0, 998.5), (1004.0, 995.5), 0.9, 0.9, (44, 36, 36))
    dot(L, (1004.5, 995.0), (200, 90, 80), 1.0); cap(L, (1005.2, 995.2), (1007.0, 996.0), 0.4, 0.15, (230, 190, 70))
    bob = 0.6 * math.sin(t * 3)
    cap(L, (998.0, 1000.0), (995.0, 1001.5 + bob), 1.3, 0.6, (34, 28, 28))
    outline(L, (20, 14, 14)); CH.add(L)


def carrots_ground(CH, v, x, feet, t, eaten):
    L = Layer(v.wcam())
    for i, dx in enumerate((-36, -18, 4, 22, 40, 12, -8)):
        if i < 7 - eaten:
            y = feet + 8 + (i % 3) * 5; x0 = x + dx
            cap(L, (x0, y), (x0 + 20, y - 4), 4.0, 1.4, (236, 128, 40), hi=(255, 176, 90))
            for a in (-0.5, 0.0, 0.5): cap(L, (x0, y), (x0 - 8 * math.cos(a), y - 8 * math.sin(a) - 3), 1.6, 0.9, (84, 160, 60))
    outline(L, (70, 40, 20)); CH.add(L)
