"""Glass preserving jars for «Валера и кот» S02E03 «Сорок банок»: 3-litre jars of pickles, tomatoes, jam and compote with tin lids and
blank paper labels, a pile (pyramid) of jars and a falling «avalanche». World-space drawing on scene.Layer(v.wcam()); sizes in world px."""
import math
from scene import Layer
from props.folk import ell, cap, dot, poly, outline

GLASS_HI = (236, 246, 240)
LID, LID_HI, LID_SH = (196, 198, 204), (236, 238, 242), (130, 132, 140)
LABEL = (240, 232, 210)
KIND = dict(cuke=((96, 132, 60), (140, 176, 90), (60, 90, 36), (70, 110, 40)),          # brine, highlight, shadow, contents
            tomato=((200, 70, 50), (240, 120, 90), (150, 40, 30), (220, 60, 40)),
            jam=((120, 26, 34), (170, 60, 70), (80, 14, 20), (100, 20, 28)),
            compote=((150, 30, 50), (200, 70, 90), (110, 20, 36), (90, 10, 30)))
ORDER = ('cuke', 'tomato', 'cuke', 'jam', 'compote', 'cuke', 'tomato')


def jar(L, x, y, h=70.0, kind='cuke', label=True, ang=0.0):
    """one jar standing on (x, y) = bottom centre; h = height in world px"""
    b, hi, sh, c = KIND[kind]
    w = h * 0.36
    ca, sa = math.cos(ang), math.sin(ang)
    def P(dx, dy): return (x + dx * ca - dy * sa, y + dx * sa + dy * ca)
    ell(L, P(0, -h * 0.45), w, h * 0.45, b, ang, hi, sh)
    if kind in ('cuke', 'tomato'):
        for k in range(5):
            px, py = (k % 2 - 0.5) * w * 0.8, -h * (0.18 + 0.15 * k)
            if kind == 'cuke': cap(L, P(px - w * 0.15, py), P(px + w * 0.2, py - h * 0.08), w * 0.18, w * 0.16, c)
            else: ell(L, P(px, py), w * 0.32, w * 0.3, c)
    cap(L, P(-w * 0.55, -h * 0.94), P(w * 0.55, -h * 0.94), h * 0.07, h * 0.07, LID, LID_HI, LID_SH)        # tin lid
    ell(L, P(-w * 0.62, -h * 0.68), w * 0.1, h * 0.16, GLASS_HI, ang)                                    # glass glint
    if label: poly(L, [P(-w * 0.7, -h * 0.42), P(w * 0.7, -h * 0.42), P(w * 0.7, -h * 0.18), P(-w * 0.7, -h * 0.18)], LABEL)


def pile(CH, v, cx, base, n_rows=6, h=70.0, seed=0, top=None):
    """pyramid of jars: rows from the floor `base` up; returns (x, y) of the top jar's lid"""
    L = Layer(v.wcam())
    w = h * 0.78
    y = base
    tx = ty = None
    for r in range(n_rows):
        n = n_rows - r
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * w + ((r * 7 + i * 3 + seed) % 5 - 2) * 2
            jar(L, x, y, h, 'cuke' if r == n_rows - 1 else ORDER[(r * 3 + i + seed) % len(ORDER)], ang=0.0 if r == n_rows - 1 else ((r + i + seed) % 3 - 1) * 0.04)
            tx, ty = x, y - h
        y -= h * 0.98
    outline(L); CH.add(L)
    return tx, ty


def avalanche(CH, v, t, x0, y0, x1, floor, k, n=24, h=70.0, seed=3):
    """jars tumbling out of a pantry: k = 0..1 progress; they fly from (x0..x1, y0) to the floor"""
    L = Layer(v.wcam())
    for i in range(n):
        a = ((i * 37 + seed * 11) % 100) / 100.0
        b = ((i * 61 + seed * 7) % 100) / 100.0
        kk = max(0.0, min(1.0, k * 1.6 - b * 0.6))
        x = x0 + a * (x1 - x0) + kk * (60 + 140 * b)
        y = y0 + (floor - y0) * min(1.0, kk * kk * 1.3) - 40 * math.sin(math.pi * kk) * b
        jar(L, x, min(y, floor - (i % 4) * h * 0.5), h, ORDER[i % len(ORDER)], ang=kk * (2.4 * b - 1.2))
    outline(L); CH.add(L)
