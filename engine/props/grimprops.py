"""«Grim Ride» movie props in the «Lantern Stipple» manner (props/grimpix): Harold's grandfather clock (the twist), a kid's sign on a
stick, the DoomDash pizza box. Sprite px, feet at (0, 0), y up."""
import math
import numpy as np
from props.grimpix import tones, stroke, INK
from props.grimcast import txt, vgrad
from props import dibspix as DX

WOOD = (112, 50, 30)
BRASS = (230, 176, 60)


def grandfather_clock(sp, t=0.0, hh=1.0, mm=59.0, swing=1.0, label=True):
    """HAROLD'S CLOCK: a tall mahogany case, a brass pendulum in a glass window, a white dial (hour hh 0..12, minute mm 0..60)"""
    sp.rect(-9.0, 0.0, 9.0, 6.0, tones(WOOD)[1])                                           # plinth
    case = sp.m_poly([(-7.0, 6.0), (7.0, 6.0), (7.0, 46.0), (-7.0, 46.0)])
    sp.paint(case, tones(WOOD, glow=(255, 160, 80)), vgrad(46, 6, 0.2))
    win = sp.m_poly([(-4.0, 12.0), (4.0, 12.0), (4.0, 38.0), (-4.0, 38.0)])
    sp.fill(win, (40, 24, 40))
    ang = 0.35 * math.sin(t * math.pi) * swing                                              # pendulum: 1 s per swing
    px, py = 0.0, 37.0
    bx, by = px + 20.0 * math.sin(ang), py - 20.0 * math.cos(ang)
    stroke(sp, [(px, py), (bx, by + 2.5)], (200, 150, 50))
    sp.ell(bx, by, 2.6, 2.6, tones(BRASS, glow=(255, 240, 170)))
    sp.rect(-11.0, 46.0, 11.0, 49.0, tones(WOOD)[0])                                       # hood
    hood = sp.m_poly([(-9.0, 49.0), (9.0, 49.0), (9.0, 66.0), (-9.0, 66.0)])
    sp.paint(hood, tones(WOOD, glow=(255, 160, 80)), vgrad(66, 49, 0.2))
    crown = sp.m_poly([(-10.0, 66.0), (10.0, 66.0), (6.0, 71.0), (0.0, 73.0), (-6.0, 71.0)])
    sp.paint(crown, tones(WOOD), vgrad(73, 66, 0.2))
    cx, cy, r = 0.0, 57.5, 7.0
    sp.ell(cx, cy, r + 0.8, r + 0.8, tones(BRASS))
    sp.ell(cx, cy, r, r, [(236, 230, 210)] * 4, ol=False)
    for k in range(12):                                                                     # hour ticks
        a = k / 12 * 2 * math.pi
        sp.dot(cx + math.sin(a) * (r - 1.2), cy + math.cos(a) * (r - 1.2), (40, 30, 40), keep=True)
    am = mm / 60 * 2 * math.pi
    ah = ((hh % 12) + mm / 60) / 12 * 2 * math.pi
    sp.line((cx, cy), (cx + math.sin(am) * (r - 1.4), cy + math.cos(am) * (r - 1.4)), (30, 20, 30), 1, keep=True)
    sp.line((cx, cy), (cx + math.sin(ah) * (r - 3.0), cy + math.cos(ah) * (r - 3.0)), (160, 30, 30), 1, keep=True)
    sp.dot(cx, cy, BRASS, keep=True)
    if label:
        sp.rect(-4.0, 40.5, 4.0, 43.5, BRASS)                                               # a brass name plate (read in close-ups)
        sp.rect(-3.0, 41.5, 3.0, 42.5, (150, 100, 30))
    sp.outline(INK, 1)
    sp.anchors['dial'] = (cx, cy)
    sp.anchors['head'] = (cx, cy)


def sign_stick(sp, text='GO BONES', bg=(250, 240, 210), fg=(160, 30, 40), w=None):
    """a cardboard sign on a stick held up by a kid (feet = the bottom of the stick)"""
    w = w or (len(text) * 4.2 + 4.0)
    stroke(sp, [(0.0, 0.0), (0.0, 16.0)], (120, 90, 60), 1)
    sp.rect(-w / 2, 14.0, w / 2, 22.0, bg)
    txt(sp, text, -w / 2 + 2.0, 20.6, fg)
    sp.outline(INK, 1)
    sp.anchors['head'] = (0.0, 18.0)


def pizza_box(sp, open_=0.0):
    """a DoomDash pizza box (flat, held level)"""
    sp.rect(-19.0, 0.0, 19.0, 7.0, (236, 214, 170))
    sp.rect(-19.0, 6.0, 19.0, 7.0, (200, 170, 120))
    sp.rect(-17.0, 0.8, 17.0, 5.6, (150, 60, 220))
    txt(sp, 'DOOMDASH', -15.6, 5.0, (255, 255, 255))
    sp.outline(INK, 1)
    sp.anchors['head'] = (0.0, 2.0)
