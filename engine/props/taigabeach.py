"""«Прохор. Таёжные лайфхаки» E06 props: the DIY «sea» on the frozen lake, «Морозный лубок» manner. Sprite px, feet at (0, 0), y up.
  samovar(sp, ...)    — a copper samovar (the «heater» that melted the ice hole)
  ice_hole(sp, ...)   — the steaming ice hole («море»), flat ellipse
  ski_chair(sp, ...)  — a deckchair of two skis and a stump, with a towel embroidered «М. П.» already on it (the clue)
  palm_fir(sp, ...)   — a small fir «пальма» in beads with pine-cone «coconuts» and a tag «ПАЛЬМА»
  suitcase(sp, h)     — a small suitcase held in a paw (with a «ЮГ» sticker)
  hotel_sign(sp, ...) — the stake sign «ОТЕЛЬ «БЕРЛОГА» · ALL INCLUSIVE»
  beach_sign(sp, ...) — Прохор's stake sign «ПЛЯЖ «У ПРОХОРА»»"""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode
from props.taigapix import tones, thin, stroke, INK, WHITE

COPPER = (204, 120, 60)
WOOD = (170, 112, 60)


def samovar(sp, t=0.0, steam=1.0):
    sp.ell(0.0, 1.2, 5.0, 1.4, tones(dark(COPPER, 0.8)))                                           # foot
    sp.cap((0.0, 2.0), (0.0, 4.0), 2.2, 2.6, tones(dark(COPPER, 0.9)))
    body = sp.ell(0.0, 10.0, 7.0, 6.6, tones(COPPER), gloss=1.2)
    for q in range(3): sp.fill(body & (np.abs(DX.YC - (6.0 + q * 3.6)) < 0.3), dark(COPPER, 0.7))
    sp.cap((5.6, 8.0), (9.6, 7.0), 0.7, 0.6, tones(dark(COPPER, 0.8)))                              # tap
    sp.ell(-7.4, 12.0, 1.4, 2.2, tones((40, 34, 30)))                                              # handles
    sp.ell(7.4, 12.0, 1.4, 2.2, tones((40, 34, 30)))
    sp.cap((0.0, 16.0), (0.0, 22.0), 1.6, 1.4, tones(dark(COPPER, 0.85)))                           # chimney
    sp.ell(0.0, 23.0, 2.2, 1.0, tones(dark(COPPER, 0.7)))
    sp.outline(INK, 1)
    sp.anchors.update(top=(0.0, 23.0), tap=(9.6, 7.0))


def ice_hole(sp, t=0.0, w=16.0):
    sp.ell(0.0, 0.0, w + 1.6, w * 0.3 + 0.8, tones((226, 238, 252)), snow=False, ol=False)           # ice rim
    m = sp.m_ell(0.0, 0.0, w, w * 0.3)[0]
    sp.fill(m, (30, 70, 120))
    for q in range(3):                                                                               # ripples
        ph = (t * 0.8 + q / 3) % 1.0
        r = m & ~sp.m_ell(0.0, 0.0, w * (0.3 + 0.6 * ph), w * 0.3 * (0.3 + 0.6 * ph))[0] & sp.m_ell(0.0, 0.0, w * (0.34 + 0.6 * ph), w * 0.3 * (0.34 + 0.6 * ph))[0]
        sp.fill(r, (90, 150, 210))
    sp.fill(m & ~erode(m), INK)


def ski_chair(sp, t=0.0, towel=True):
    """two skis leaned into a reclined deckchair on a stump; the towel «М. П.» on the back"""
    sp.sup(-6.0, 3.0, 4.0, 3.0, tones(WOOD), n=2.4)                                                  # stump
    for k_, dx in enumerate((-1.0, 1.0)):
        c = (200, 40, 40) if k_ else dark((200, 40, 40), 0.8)
        sp.cap((-22.0 + dx, 2.0), (2.0 + dx, 8.0), 1.0, 1.0, tones(c))                              # seat ski
        sp.cap((2.0 + dx, 8.0), (10.0 + dx, 24.0), 1.0, 1.0, tones(c))                              # back ski
        sp.cap((10.0 + dx, 24.0), (9.0 + dx, 27.0), 1.0, 0.8, tones(c))                             # ski tip
    if towel:
        tw = sp.m_poly([(3.0, 9.0), (7.4, 9.0), (12.6, 22.0), (8.0, 22.0)])
        sp.paint(tw, tones((250, 240, 230)), None, olc=INK)
        for q in range(4): sp.fill(tw & (np.abs(DX.YC - (11.0 + q * 3.0)) < 0.4), (60, 120, 210))
        sp.txt_box(['М.П.'], (4.6, 14.0, 11.6, 18.4), (200, 30, 40), pad=0.1)
    sp.outline(INK, 1)
    sp.anchors.update(seat=(-8.0, 6.0), back=(7.0, 18.0))


def palm_fir(sp, t=0.0):
    FIR = (46, 112, 68)
    sp.cap((0.0, 0.0), (1.0, 30.0), 1.4, 1.0, tones(WOOD))                                          # bare trunk (a palm!)
    for q in range(6):
        sp.fill(sp.m_cap((-1.4, 4.0 + q * 4.6), (1.6, 5.2 + q * 4.6), 0.3, 0.3)[0], dark(WOOD, 0.6))
    for k_ in range(7):                                                                              # fir branches as palm fronds
        a = -0.3 + k_ * 0.6 + 0.08 * math.sin(t * 1.6 + k_)
        ex, ey = 1.0 + math.cos(a + 0.2) * 13.0, 30.0 + math.sin(a + 0.2) * 5.0 - 3.0
        sp.cap((1.0, 31.0), (ex, ey), 2.6, 1.2, tones(FIR))
        for q in range(5):
            px_ = 1.0 + (ex - 1.0) * (0.25 + q * 0.17); py_ = 31.0 + (ey - 31.0) * (0.25 + q * 0.17)
            thin(sp, (px_, py_), (px_ + 0.8, py_ - 2.2), dark(FIR, 0.6), 0.25)
    for (x, y) in ((-0.6, 28.4), (2.4, 28.0), (0.8, 27.0)):                                         # pine-cone «coconuts»
        sp.ell(x, y, 1.4, 1.8, tones((120, 76, 40)))
    for q in range(8):                                                                               # beads
        a = q * 0.8
        sp.ell(1.0 + math.cos(a) * 7.0, 31.0 + math.sin(a) * 2.2 - 1.0, 0.8, 0.8, tones(((255, 80, 80), (255, 220, 60), (80, 180, 255))[q % 3]), ol=False, snow=False, gloss=1.0)
    sp.outline(INK, 1)
    sp.sup(1.0, 12.0, 4.8, 2.0, tones((246, 240, 226)), n=4.0)
    sp.txt_box(['ПАЛЬМА'], (-3.4, 10.4, 5.4, 13.6), (30, 30, 40), pad=0.1)


def suitcase(sp, h, col=(220, 80, 60), label='ЮГ'):
    x, y = h
    sp.cap((x - 1.2, y), (x + 1.2, y), 0.4, 0.4, tones((40, 40, 46)))                               # handle
    m = sp.m_super(x, y - 4.2, 4.6, 3.4, 4.0)[0]
    sp.paint(m, tones(col), None, olc=INK)
    sp.fill(m & (np.abs(DX.XC - x) < 0.3), dark(col, 0.6))
    sp.sup(x + 2.0, y - 4.6, 1.8, 1.2, tones((250, 236, 120)), n=3.0)
    sp.txt_box([label], (x + 0.4, y - 5.6, x + 3.6, y - 3.6), (40, 40, 50), pad=0.05)


def _stake_sign(sp, lines, bg, fg, w=26.0, h=11.0, top=34.0, colors=None):
    sp.cap((0.0, 0.0), (0.0, top - h), 0.9, 0.9, tones(WOOD))
    m = sp.m_super(0.0, top - h / 2, w / 2, h / 2, 6.0)[0]
    sp.paint(m, tones(bg), None, olc=INK)
    sp.txt_box(lines, (-w / 2 + 1.0, top - h + 0.8, w / 2 - 1.0, top - 0.8), fg, pad=0.3)
    sp.outline(INK, 1)


def hotel_sign(sp, t=0.0):
    _stake_sign(sp, ['ОТЕЛЬ «БЕРЛОГА»', 'ALL INCLUSIVE'], (60, 40, 120), (255, 220, 90), w=30.0, h=12.0, top=36.0)
    for q in range(6):                                                                               # blinking bulbs on the frame
        on = int(t * 4 + q) % 2 == 0
        sp.ell(-14.0 + q * 5.6, 36.6, 0.7, 0.7, tones((255, 236, 120) if on else (120, 100, 60)), ol=False, snow=False, gloss=1.0)


def beach_sign(sp, t=0.0):
    _stake_sign(sp, ['ПЛЯЖ', '«У ПРОХОРА»'], (250, 210, 60), (30, 30, 40), w=24.0, h=11.0, top=32.0)
