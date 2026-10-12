"""«Прохор. Таёжные лайфхаки» — the forest cast (E02–E06), drawn in the «Морозный лубок» manner (props/taigapix.py), v2 rules:
big heads, big readable eyes, clean shapes, a few fur strokes only.
  critter(sp, kind=..., ...) — upright cartoon animals of the taiga «system»: 'fox' (courier «Лиса-Экспресс»), 'hare', 'squirrel'
                                ('guard' = squirrel in a security vest), 'moose' (orderly with a «САНИТАР» badge)
  ranger(sp, ...)            — егерь Людмила Петровна (E05)
Props: parcel, hammer, sled, birdhouse_cam, snowmobile, drone, deckchair, palm_fir, samovar, suitcase, cuckoo.
Coordinates: sprite px, feet anchor at (0, 0), x right = facing side, y UP."""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR
from props.taigapix import tones, thin, stroke, INK, WHITE
from props.taigacast import X, bill, terminal, WOOD, STEEL, MITT, TAPE

KINDS = dict(
    fox=dict(fur=(226, 112, 40), belly=(246, 238, 224), dark=(64, 36, 30), iris=(110, 160, 40), body=(0.0, 23.0, 10.0, 13.0),
             head=(3.0, 45.0, 9.0, 8.4), snout=(12.4, 42.0, 6.4, 3.4), leg=10.0, arm=(8.0, 7.5), ears='fox', tail='fox', lash=True),
    hare=dict(fur=(234, 236, 244), belly=(250, 250, 252), dark=(150, 150, 170), iris=(70, 110, 170), body=(0.0, 20.0, 9.0, 11.0),
              head=(2.0, 37.5, 7.6, 7.2), snout=(8.4, 35.0, 3.6, 3.0), leg=8.0, arm=(6.5, 6.0), ears='hare', tail='puff', teeth=True),
    squirrel=dict(fur=(200, 106, 46), belly=(246, 222, 180), dark=(110, 56, 26), iris=(40, 30, 24), body=(0.0, 13.0, 6.4, 8.0),
                  head=(2.0, 26.0, 6.4, 5.8), snout=(7.4, 24.6, 3.2, 2.4), leg=5.0, arm=(4.6, 4.2), ears='squirrel', tail='squirrel',
                  teeth=True),
    moose=dict(fur=(112, 74, 48), belly=(170, 130, 96), dark=(60, 40, 28), iris=(60, 40, 30), body=(0.0, 40.0, 17.0, 19.0),
               head=(6.0, 70.0, 9.4, 10.6), snout=(16.0, 62.0, 10.0, 7.0), leg=22.0, arm=(13.0, 12.0), ears='moose', tail='none'),
)
KINDS['guard'] = dict(KINDS['squirrel'])


def _ears(sp, kind, hx, hy, K, wig):
    f, b = K['fur'], K['belly']
    if kind == 'fox':
        for dx, sh in ((-3.6, 0.85), (4.4, 1.0)):
            c = f if sh == 1.0 else dark(f, 0.85)
            m = sp.m_poly([(hx + dx - 3.2, hy + 5.0), (hx + dx + 3.0, hy + 5.6), (hx + dx + 0.6 + wig, hy + 15.0)])
            sp.paint(m, tones(c), np.clip((DX.YC - hy - 5) / 10, 0, 1) * 0.6 + 0.3)
            sp.fill(m & sp.m_poly([(hx + dx - 1.4, hy + 6.4), (hx + dx + 1.6, hy + 6.8), (hx + dx + 0.6 + wig, hy + 12.0)]), (40, 26, 26))
    elif kind == 'hare':
        for dx, ang, c in ((-2.4, 0.18, dark(f, 0.9)), (2.6, -0.12 + 0.05 * wig, f)):
            sp.ell(hx + dx - 1.2, hy + 14.0, 2.4, 9.0, tones(c), ang=ang)
            sp.ell(hx + dx - 1.2, hy + 14.6, 1.1, 6.8, tones((240, 170, 180)), ang=ang, ol=False, snow=False)
    elif kind in ('squirrel', 'guard'):
        for dx in (-2.6, 2.8):
            sp.ell(hx + dx, hy + 5.6, 1.8, 2.6, tones(f))
            stroke(sp, [(hx + dx, hy + 7.6), (hx + dx - 0.4, hy + 9.6 + wig * 0.3)], dark(f, 0.6), 0.35)
    elif kind == 'moose':
        for dx, ang in ((-6.0, 0.9), (5.4, -0.7)):
            sp.ell(hx + dx, hy + 4.0, 4.2, 1.8, tones(f), ang=ang)
        # palmate antlers: two broad flat paddles with tines
        for sgn in (-1, 1):
            base = (hx + sgn * 3.0, hy + 7.4)
            pad = sp.m_ell(hx + sgn * 13.0, hy + 14.0, 9.0, 4.4, -0.25 * sgn)[0]
            for q in range(4):
                pad |= sp.m_cap((hx + sgn * (7.0 + q * 4.0), hy + 15.0), (hx + sgn * (6.0 + q * 4.6), hy + 21.0 + (q % 2) * 2), 1.4, 0.8)[0]
            pad |= sp.m_cap(base, (hx + sgn * 8.0, hy + 12.0), 1.8, 1.6)[0]
            sp.paint(pad, tones((214, 196, 160)), np.clip((DX.YC - hy - 8) / 14, 0, 1) * 0.6 + 0.3)


def _tail(sp, kind, K, t, wag):
    f, b = K['fur'], K['belly']
    if kind == 'fox':
        pts = [(-7.0, 14.0), (-14.0, 12.0 + 2 * wag), (-19.0, 17.0 + 3 * wag)]
        sp.union([sp.m_ell(-11.0, 13.0 + wag, 7.6, 5.0, 0.3), sp.m_ell(-17.0, 16.0 + 2 * wag, 5.4, 4.2, -0.2)], tones(f))
        sp.ell(-20.4, 18.4 + 2 * wag, 3.0, 2.8, tones(b))
    elif kind in ('squirrel', 'guard'):
        sp.union([sp.m_ell(-7.0, 10.0, 4.6, 7.0, 0.3), sp.m_ell(-9.6, 22.0 + wag, 5.6, 8.0, -0.2), sp.m_ell(-6.0, 31.0 + wag, 4.4, 3.4, 0.6)],
                 tones(dark(f, 0.95)))
        stroke(sp, [(-6.0, 6.0), (-10.0, 16.0), (-10.0, 26.0), (-6.4, 32.0)], dark(f, 0.66), 0.4)
    elif kind == 'hare':
        sp.ell(-8.0, 14.0, 3.0, 2.8, tones(b))


def critter(sp, kind='fox', t=0.0, expr='normal', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None,
            prop_f=None, walk=None, cap=None, backpack=False, vest=None, badge=None, wag=None, scale_head=1.0):
    """an upright cartoon taiga animal. cap='courier' (yellow «ЛИСА-ЭКСПРЕСС» cap) / 'guard' (black security cap);
    backpack=True (yellow courier cube); vest='ОХРАНА' (black security vest with the word); badge='САНИТАР' (a badge on the chest)"""
    K = KINDS[kind]
    E = X(expr)
    if blink is None: blink = (t % 3.3) < 0.12
    f, b, dk = K['fur'], K['belly'], K['dark']
    bx, by, brx, bry = K['body']
    hx, hy, hrx, hry = K['head']
    hrx *= scale_head; hry *= scale_head
    br = 0.3 * math.sin(t * 2.4)
    bob = abs(math.sin(walk)) * 0.8 if walk is not None else 0.0
    wg = (math.sin(t * 6.0) if wag is None else wag)
    L = K['leg']
    # tail, far arm
    _tail(sp, kind, K, t, wg)
    shF = (bx - brx * 0.55, by + bry * 0.55 + bob)
    a1, a2 = K['arm']
    hf = hand_f if hand_f is not None else (bx - brx * 0.9, by - bry * 0.1 + bob)
    kF, eF = ik(shF, hf, a1, a2, -1.0)
    sp.cap(shF, kF, a1 * 0.28, a1 * 0.24, tones(dark(f, 0.82))); sp.cap(kF, eF, a1 * 0.24, a1 * 0.2, tones(dark(f, 0.82)))
    sp.ell(*eF, a1 * 0.26, a1 * 0.24, tones(dark(dk, 1.2)))
    if prop_f: prop_f(sp, eF)
    # legs
    sw = math.sin(walk) * L * 0.25 if walk is not None else 0.0
    for k_, dx in enumerate((-brx * 0.45, brx * 0.45)):
        s_ = sw if k_ else -sw
        c = f if k_ else dark(f, 0.85)
        sp.cap((bx + dx, L), (bx + dx + s_, 2.0), L * 0.22 + 1.0, L * 0.18 + 0.8, tones(c))
        sp.ell(bx + dx + s_ + 1.4, 1.4, L * 0.18 + 2.0, 1.6, tones(dk))
    # backpack (behind the body)
    if backpack:
        sp.sup(bx - brx * 0.8, by + 4.0 + bob, 7.0, 8.0, tones((250, 200, 40)), n=3.4)
        sp.txt_box(['ЛИСА', 'ЭКСПРЕСС'], (bx - brx * 0.8 - 6.2, by - 2.0 + bob, bx - brx * 0.8 + 6.2, by + 10.0 + bob), (40, 30, 30), pad=0.3)
    # body + belly
    body = sp.ell(bx, by + bob, brx, bry, tones(f))
    sp.ell(bx + brx * 0.25, by - bry * 0.1 + bob, brx * 0.62, bry * 0.72, tones(b), flat=0.05)
    if vest:
        vm = sp.m_ell(bx, by + bob, brx * 1.02, bry * 0.9)[0] & (DX.YC < by + bry * 0.75 + bob)
        sp.paint(vm, tones((40, 44, 52)), np.clip((DX.YC - by + bry) / (2 * bry), 0, 1) * 0.5 + 0.3)
        sp.txt_box([vest], (bx - brx * 0.8, by + 1.6 + bob, bx + brx * 0.55, by + 6.0 + bob), (250, 220, 60), pad=0.2)
    if badge:
        sp.sup(bx + brx * 0.4, by + bry * 0.35 + bob, 6.0, 2.6, tones((240, 240, 236)), n=4.0)
        sp.txt_box([badge], (bx + brx * 0.4 - 5.6, by + bry * 0.35 - 2.2 + bob, bx + brx * 0.4 + 5.6, by + bry * 0.35 + 2.2 + bob), (180, 30, 34), pad=0.1)
    # head
    hy2 = hy + bob
    _ears(sp, kind, hx, hy2, K, wg * 0.6)
    head = sp.union([sp.m_ell(hx, hy2, hrx, hry), sp.m_ell(*K['snout'][:2], K['snout'][2], K['snout'][3])] if kind != 'moose' else
                    [sp.m_ell(hx, hy2, hrx, hry), sp.m_ell(K['snout'][0], K['snout'][1] + bob, K['snout'][2], K['snout'][3], -0.4)], tones(f))
    sx, sy, srx, sry = K['snout']; sy += bob
    if kind in ('fox',):
        sp.fill(sp.m_ell(hx + 3.0, hy2 - 3.0, 6.4, 3.4)[0] & head, b)                # white cheeks + muzzle
    if kind == 'moose':
        sp.ell(sx + 1.0, sy - 1.0, srx * 0.8, sry * 0.75, tones(dark(f, 1.15)), ang=-0.4)
        sp.ell(hx + 2.0, hy2 - 10.0, 2.6, 4.0, tones(dark(f, 0.9)))              # dewlap
    nx = sx + srx * 0.92; ny = sy + sry * 0.25
    sp.ell(nx, ny, 1.4 + 0.12 * srx, 1.1 + 0.08 * srx, tones((30, 24, 26)), gloss=1.0, snow=False)
    lx, ly = look
    ew, eh = (4.6, 5.0) if kind in ('fox', 'hare') else (3.8, 4.0) if kind != 'moose' else (3.8, 3.8)
    ex = hx + hrx * 0.28; ey = hy2 + hry * 0.25
    DX.eye(sp, ex + ew * 0.55, ey, ew, eh, E, K['iris'], (lx, ly), blink, lash=INK, skin=f, bold=1, flick=K.get('lash', False))
    DX.eye(sp, ex - ew * 0.75, ey, ew * 0.85, eh * 0.95, E, K['iris'], (lx, ly), blink, lash=INK, skin=f, bold=1, flick=K.get('lash', False))
    DX.brow(sp, ex + ew * 0.55, ey + eh * 0.85, ew * 1.1, E, +1, dark(f, 0.5), th=1)
    DX.brow(sp, ex - ew * 0.75, ey + eh * 0.85, ew, E, -1, dark(f, 0.5), th=1)
    mx, my = sx + srx * 0.3, sy - sry * 0.55
    mo = max(mouth_, E['mo'])
    if mo > 0.10:
        hw = 1.6 + 1.2 * mo + srx * 0.12; hh = 0.6 + 2.6 * mo
        mm = sp.m_ell(mx, my - hh * 0.4, hw, hh)[0]
        sp.fill(mm, (90, 24, 30)); sp.fill(mm & (DX.YC < my - hh * 0.85), (220, 110, 120)); sp.fill(mm & ~erode(mm), INK)
        if K.get('teeth'): sp.fill(sp.m_super(mx - 0.4, my + 0.1, 1.0, 1.0, 3.0)[0], WHITE, keep=True)
    else:
        c_ = E['mc']
        stroke(sp, [(mx - 2.0, my + 0.6 * c_), (mx, my - 0.2), (mx + 1.4, my + 0.6 * c_)], INK, 0.28)
        if K.get('teeth'): sp.fill(sp.m_super(mx - 0.2, my - 1.0, 0.9, 0.9, 3.0)[0], WHITE, keep=True)
    if kind == 'fox':
        for q in range(3): thin(sp, (sx + srx * 0.2, sy + 0.4 - q * 0.6), (sx + srx * 0.2 + 3.4, sy + 1.0 - q * 0.9), dark(f, 0.5), 0.12)
    # caps
    if cap == 'courier':
        sp.ell(hx - 0.4, hy2 + hry * 0.72, hrx * 0.95, hry * 0.45, tones((250, 200, 40)))
        sp.ell(hx + hrx * 0.95, hy2 + hry * 0.52, hrx * 0.62, hry * 0.14, tones((230, 170, 30)))
    elif cap == 'guard':
        sp.ell(hx - 0.2, hy2 + hry * 0.72, hrx * 0.95, hry * 0.42, tones((34, 38, 46)))
        sp.ell(hx + hrx * 0.9, hy2 + hry * 0.5, hrx * 0.6, hry * 0.13, tones((24, 26, 30)))
        sp.sup(hx + 0.6, hy2 + hry * 0.78, 1.6, 1.2, tones((240, 200, 60)), n=3.0)
    sp.anchors.update(head=(hx, hy2), mouth=(mx, my), nose=(nx, ny))
    sp.outline(INK, 1)
    # near arm
    before = sp.m.copy()
    shN = (bx + brx * 0.55, by + bry * 0.55 + bob)
    hn = hand_n if hand_n is not None else (bx + brx * 1.0, by - bry * 0.05 + bob)
    kN, eN = ik(shN, hn, a1, a2, -1.0)
    sp.cap(shN, kN, a1 * 0.3, a1 * 0.26, tones(f)); sp.cap(kN, eN, a1 * 0.26, a1 * 0.22, tones(f))
    sp.ell(*eN, a1 * 0.28, a1 * 0.26, tones(dk if kind != 'hare' else b))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ================================================================================ props
def parcel(sp, h=None, t=0.0, w=9.0, hh=7.0, label='ДИКАЯ ЯГОДА', tape=True, standalone=False):
    """a cardboard marketplace box (in a hand at h, or standalone at the feet anchor)"""
    x, y = h if h is not None else (0.0, hh / 2 + 0.2)
    m = sp.m_super(x, y, w / 2, hh / 2, 5.0)[0]
    sp.paint(m, tones((196, 150, 96)), np.clip((DX.YC - y + hh / 2) / hh, 0, 1) * 0.6 + 0.25, olc=(100, 70, 40))
    if tape: sp.fill(m & (np.abs(DX.XC - x) < 0.6), (220, 196, 140))
    sp.txt_box([label], (x - w / 2 + 0.6, y - hh / 2 + 0.6, x + w / 2 - 0.6, y - 0.2), (150, 40, 120), pad=0.15)
    if standalone: sp.outline(INK, 1)


def parcel_stack(sp, t=0.0, n=6, seed=1, label='ДИКАЯ ЯГОДА'):
    rng = np.random.default_rng(seed)
    y = 0.0
    for i in range(n):
        w = 8.0 + rng.random() * 6.0; hh = 5.0 + rng.random() * 3.0
        x = (rng.random() - 0.5) * 3.0
        parcel(sp, (x, y + hh / 2), w=w, hh=hh, label=label)
        y += hh - 0.3
    sp.outline(INK, 1)


def hammer(sp, h, ang=0.6):
    x, y = h
    a = (x + math.cos(ang) * 1.0, y + math.sin(ang) * 1.0); b = (x + math.cos(ang) * 8.0, y + math.sin(ang) * 8.0)
    sp.cap(a, b, 0.6, 0.6, tones(WOOD))
    px, py = -math.sin(ang), math.cos(ang)
    sp.cap((b[0] - px * 2.2, b[1] - py * 2.2), (b[0] + px * 1.6, b[1] + py * 1.6), 1.1, 1.1, tones(STEEL))


def sled(sp, t=0.0, load=3):
    """a wooden courier sled with parcels"""
    for q in range(2): sp.cap((-14.0, 1.0 + q * 0.2), (14.0, 1.0), 0.6, 0.6, tones(STEEL))
    sp.cap((14.0, 1.0), (17.0, 5.0), 0.6, 0.6, tones(STEEL))
    sp.sup(0.0, 4.0, 14.0, 2.2, tones(WOOD), n=4.0)
    y = 6.0
    for i in range(load):
        parcel(sp, (-6.0 + i * 6.0, y + 3.0), w=6.4, hh=6.0)
    sp.outline(INK, 1)


def tablet(sp, h, t=0.0, rec=True):
    """a security tablet in a paw: the replay of him eating berries (a tiny red figure) + REC"""
    x, y = h
    m = sp.m_super(x + 3.0, y + 3.0, 5.2, 3.8, 4.0)[0]
    sp.paint(m, tones((40, 40, 46)), None, olc=INK)
    sc = sp.m_super(x + 3.0, y + 3.0, 4.4, 3.0, 4.0)[0]
    sp.fill(sc, (60, 110, 80))
    sp.fill(sp.m_ell(x + 3.0, y + 2.6, 1.0, 1.6)[0], (200, 90, 40))                     # the tiny thief
    sp.fill(sp.m_ell(x + 3.0, y + 4.4, 1.1, 0.8)[0], (110, 80, 60))
    for q in range(4): sp.fill(sp.m_ell(x + 5.0 + (q % 2), y + 1.4 + q * 0.6, 0.35, 0.35)[0], (220, 40, 50))
    if rec and int(t * 2) % 2 == 0: sp.fill(sp.m_ell(x - 0.6, y + 5.2, 0.5, 0.5)[0], (255, 40, 40))


def scanner(sp, h, t=0.0, beam=0.0):
    x, y = h
    sp.cap((x, y), (x + 1.0, y - 3.0), 0.9, 0.8, tones((40, 40, 46)))
    sp.sup(x + 2.4, y + 0.6, 2.6, 1.4, tones((40, 40, 46)), n=3.0)
    if beam > 0: thin(sp, (x + 4.8, y + 0.6), (x + 14.0, y - 1.0), (255, 40, 40), 0.25)


def stump_till(sp, t=0.0):
    """the bear's cash desk on the stump: a cardboard sign «КАССА» and a tiny register"""
    sp.sup(4.0, 3.0, 6.0, 3.6, tones((70, 70, 80)), n=3.0)
    sp.sup(4.0, 7.0, 4.0, 1.6, tones((60, 60, 66)), n=3.0)
    sp.fill(sp.m_super(4.0, 7.0, 3.2, 1.0, 4.0)[0], (110, 220, 140))
    pl = sp.m_poly([(-12.0, 0.0), (-1.0, 0.4), (-1.6, 9.6), (-11.6, 9.0)])
    sp.paint(pl, tones((214, 178, 120)), None, olc=(110, 80, 50))
    sp.txt_box(['КАССА'], (-11.4, 1.6, -1.8, 8.2), (170, 30, 30), pad=0.4)
    sp.outline(INK, 1)


def birdhouse_cam(sp, t=0.0, turn=0.0, light=True):
    """the security camera hidden in the birdhouse hole: a lens on a stalk that turns (turn -1..1) + a blinking red light"""
    sp.cap((0.0, 0.0), (2.4 * turn, 0.6), 0.9, 0.9, tones((60, 60, 66)))
    sp.sup(2.6 * turn, 1.4, 3.0, 2.0, tones((50, 50, 56)), n=3.0)
    sp.ell(2.6 * turn + 2.4 * (1 if turn >= 0 else -1), 1.4, 1.2, 1.2, tones((40, 70, 120)), gloss=1.0, snow=False)
    if light and int(t * 3) % 2 == 0: sp.fill(sp.m_ell(2.6 * turn - 1.6, 3.0, 0.6, 0.6)[0], (255, 40, 40))
    sp.outline(INK, 1)
