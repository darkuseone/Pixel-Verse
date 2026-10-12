"""«Прохор. Таёжные лайфхаки» E05 cast + gear, «Морозный лубок» manner (props/taigapix.py). Sprite px, feet at (0, 0), y up.
  ranger(sp, ...)     — егерь Людмила Петровна: a «fridge in uniform» (a tall box of forest-green bushlat with orange hi-vis stripes),
                        a peaked forester cap on a purple perm, blue eyeshadow, red lipstick, a mole, a gold tooth, a whistle
  snowmobile(sp, ...) — «ЛЕСХОЗ» snowmobile, side view
  drone(sp, ...)      — the «ЛЕСООХРАНА» quadcopter (spinning rotors, blinking lights, a camera)
  fine_book(sp, h)    — the receipt book held in a hand; fine_slip(sp, ...) — a torn-off fine receipt (standalone, e.g. on a forehead)"""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik
from props.taigapix import tones, thin, stroke, INK, WHITE
from props.taigacast import X

SKIN = (236, 172, 146)
COAT = (52, 98, 66)                 # forest-green bushlat
VIS = (255, 136, 36)                # hi-vis orange
SILVER = (214, 222, 230)
COLLAR = (150, 146, 140)            # grey fur collar
PERM = (150, 62, 104)               # «химия»: purple-burgundy curls
CAPC = (44, 84, 56)
GOLD = (230, 190, 70)
BOOT = (46, 42, 44)
LIPS = (196, 30, 56)
SHADOW_EYE = (90, 130, 220)         # blue eyeshadow


def fine_book(sp, h, open_=0.0):
    """the receipt book: a blue cover «КВИТАНЦИИ», a white page edge; open_ shows a page"""
    x, y = h
    m = sp.m_super(x + 3.0, y + 2.6, 4.6, 3.4, 4.0)[0]
    sp.paint(m, tones((50, 80, 170)), None, olc=INK)
    sp.fill(m & (DX.YC < y + 0.2), (246, 244, 236))
    sp.txt_box(['ШТРАФ'], (x - 1.2, y + 1.0, x + 7.2, y + 5.0), (255, 236, 120), pad=0.2)
    if open_ > 0:
        pg = sp.m_super(x + 3.0, y + 7.6, 4.2, 2.8 * open_, 4.0)[0]
        sp.paint(pg, tones((248, 246, 236)), None, olc=(120, 120, 130))


def fine_slip(sp, t=0.0, amount='3 000 ₽', title='ШТРАФ'):
    """a torn-off fine receipt (standalone, centred at the origin)"""
    w, hh = 12.0, 15.0
    m = sp.m_poly([(-w / 2, -hh / 2), (w / 2, -hh / 2 + 0.4), (w / 2 - 0.3, hh / 2), (-w / 2 + 0.2, hh / 2 - 0.3)])
    sp.paint(m, [(200, 198, 206), (246, 244, 234), (255, 255, 248)], np.clip((DX.XC + w / 2) / w, 0, 1) * 0.6 + 0.3, olc=(120, 120, 130))
    for q in range(6):                                                                          # torn top edge
        sp.fill(sp.m_ell(-w / 2 + 1.0 + q * 2.0, hh / 2, 0.7, 0.5)[0], (120, 120, 130))
    sp.fill(m & (DX.YC > hh / 2 - 4.0), (200, 40, 40))
    sp.txt_box([title], (-w / 2 + 0.6, hh / 2 - 3.8, w / 2 - 0.6, hh / 2 - 0.4), WHITE, pad=0.2)
    sp.txt_box(['КОСТЁР'], (-w / 2 + 0.6, -0.6, w / 2 - 0.6, hh / 2 - 4.4), (40, 40, 50), pad=0.3)
    sp.txt_box([amount], (-w / 2 + 0.6, -hh / 2 + 1.0, w / 2 - 0.6, -1.0), (210, 30, 36), pad=0.3)
    sp.outline(INK, 1)


def drone(sp, t=0.0, lights=True, tilt=0.0, broken=0.0, at=(0.0, 0.0)):
    """«ЛЕСООХРАНА» quadcopter: a grey body, 4 arms, blurred spinning rotors, camera ball, red/green blinking lights"""
    G = (150, 156, 166)
    ax, ay = at
    for sx in (-1, 1):
        sp.cap((ax, ay + 3.0), (ax + sx * 9.0, ay + 4.6 + sx * tilt), 0.7, 0.6, tones(dark(G, 0.8)))
        sp.cap((ax + sx * 9.0, ay + 4.6 + sx * tilt), (ax + sx * 9.0, ay + 6.0 + sx * tilt), 0.6, 0.6, tones(dark(G, 0.7)))
        ph = (t * 40.0 + sx) % 1.0
        if broken < 0.5:
            sp.ell(ax + sx * 9.0, ay + 6.4 + sx * tilt, 5.4 * (0.6 + 0.4 * abs(math.cos(ph * 6.28))), 0.7, tones((200, 206, 216)), ol=False, snow=False)
    body = sp.sup(ax, ay + 3.0, 5.0, 2.4, tones(G), n=3.2)
    sp.txt_box(['ЛЕСООХРАНА'], (ax - 4.4, ay + 2.0, ax + 4.4, ay + 4.4), (30, 90, 50), pad=0.1)
    sp.ell(ax + 1.0, ay + 0.4, 1.5, 1.4, tones((40, 40, 50)), gloss=1.0, snow=False)                     # camera ball
    if lights:
        on = int(t * 4) % 2 == 0
        sp.fill(sp.m_ell(ax - 4.6, ay + 3.0, 0.6, 0.6)[0], (255, 40, 40) if on else (120, 30, 30))
        sp.fill(sp.m_ell(ax + 4.6, ay + 3.0, 0.6, 0.6)[0], (40, 230, 80) if not on else (30, 110, 40))
    if at == (0.0, 0.0): sp.outline(INK, 1)
    sp.anchors.update(cam=(ax + 1.0, ay + 0.4), body=(ax, ay + 3.0))


def snowmobile(sp, t=0.0, idle=1.0, light=True):
    """«ЛЕСХОЗ» snowmobile, side view facing right: front ski, rear track, orange-red hood, windshield, black seat"""
    jig = 0.25 * math.sin(t * 40.0) * idle
    RED = (214, 64, 40)
    sp.cap((-22.0, 3.0), (2.0, 3.0), 3.0, 3.0, tones((40, 40, 46)))                             # track
    for q in range(7): sp.ell(-20.0 + q * 3.6, 3.0, 1.0, 1.0, tones((90, 90, 100)), snow=False)
    sp.cap((10.0, 1.0), (26.0, 1.0), 0.9, 0.9, tones((60, 60, 66)))                           # ski
    sp.cap((25.0, 1.2), (28.0, 3.6), 0.9, 0.9, tones((60, 60, 66)))
    sp.cap((16.0, 1.6), (14.0, 7.0), 0.8, 0.8, tones((70, 70, 76)))                           # ski strut
    hm = sp.m_poly([(-14.0, 6.0 + jig), (20.0, 6.0 + jig), (24.0, 9.0 + jig), (12.0, 15.0 + jig), (-14.0, 12.0 + jig)])
    hood = sp.paint(hm, tones(RED), np.clip((DX.YC - 6.0) / 9.0, 0, 1) * 0.6 + 0.3, gloss=0.6)
    sp.fill(hood & (np.abs(DX.YC - (9.0 + jig)) < 0.6), WHITE)
    sp.txt_box(['ЛЕСХОЗ'], (-4.0, 6.8 + jig, 12.0, 11.6 + jig), WHITE, pad=0.2)
    sp.sup(-12.0, 13.6 + jig, 9.0, 2.0, tones((30, 30, 34)), n=3.0)                          # seat
    ws = sp.m_poly([(10.0, 14.6 + jig), (14.0, 14.6 + jig), (11.0, 21.0 + jig), (7.6, 20.6 + jig)])
    sp.fill(ws, mix((150, 200, 240), (255, 255, 255), 0.3))
    sp.fill(ws & ~erode(ws), INK)
    sp.cap((6.0, 15.0 + jig), (9.0, 18.0 + jig), 0.6, 0.6, tones((50, 50, 56)))              # handlebar
    if light: sp.fill(sp.m_ell(22.4, 9.4 + jig, 1.2, 0.9)[0], (255, 244, 170))
    sp.outline(INK, 1)
    sp.anchors.update(seat=(-12.0, 15.0 + jig), bar=(9.0, 18.0 + jig))


def ranger(sp, t=0.0, expr='angry', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
           walk=None, legs=True, whistle=True, lean=0.0):
    """ЕГЕРЬ ЛЮДМИЛА ПЕТРОВНА — a «fridge in uniform»: a tall box of forest-green bushlat (hi-vis orange stripes, «ЕГЕРЬ» patch, grey
    fur collar), a small head under a peaked forester cap with a gold cockade sitting on a big purple perm; blue eyeshadow, red
    lipstick, a mole, a gold tooth; a whistle on a string; felt boots. walk = phase."""
    E = X(expr)
    if blink is None: blink = (t % 3.9) < 0.12
    bob = abs(math.sin(walk)) * 1.4 if walk is not None else 0.0
    swing = math.sin(walk) * 6.0 if walk is not None else 0.0
    def Q(x, y): return (x + lean * (y / 60.0) * 6.0, y + (bob if y > 9 else bob * 0.3))
    # far arm
    shF = Q(-10.0, 46.0)
    hf = hand_f if hand_f is not None else Q(-15.0 - swing * 0.6, 28.0)
    kF, eF = ik(shF, hf, 10.0, 9.0, -1.0)
    sp.cap(shF, kF, 3.6, 3.2, tones(dark(COAT, 0.78))); sp.cap(kF, eF, 3.2, 2.8, tones(dark(COAT, 0.78)))
    sp.ell(*eF, 2.4, 2.4, tones(dark(SKIN, 0.85)))
    if prop_f: prop_f(sp, eF)
    # legs: felt boots
    if legs:
        sw = math.sin(walk) * 3.0 if walk is not None else 0.0
        for k_, dx in enumerate((-5.0, 5.0)):
            s_ = sw if k_ else -sw
            c = BOOT if k_ else dark(BOOT, 0.8)
            sp.cap((dx, 12.0), (dx + s_ * 0.7, 3.0 + max(0.0, s_) * 0.4), 3.6, 3.4, tones(c))
            sp.ell(dx + s_ * 0.7 + 1.6, 2.2 + max(0.0, s_) * 0.4, 4.6, 2.4, tones(c))
    # the fridge: a tall boxy coat
    body = sp.union([sp.m_super(*Q(0.0, 30.0), 13.6, 21.0, 4.2)], tones(COAT))
    for yy in (19.0, 25.0):                                                                     # hi-vis stripes
        st = body & (np.abs(DX.YC - Q(0, yy)[1]) < 1.4)
        sp.fill(st, VIS); sp.fill(body & (np.abs(DX.YC - Q(0, yy)[1]) < 0.35), SILVER)
    sp.fill(body & (np.abs(DX.XC - Q(1.0, 30.0)[0]) < 0.3) & (DX.YC < Q(0, 48.0)[1]), dark(COAT, 0.6))   # placket
    for q in range(4): sp.fill(sp.m_ell(*Q(2.2, 14.0 + q * 8.0), 0.6, 0.6)[0], GOLD)
    px_, py_ = Q(6.4, 37.0)
    sp.sup(px_, py_, 5.2, 2.6, tones((246, 220, 90)), n=4.0)                                     # «ЕГЕРЬ» patch
    sp.txt_box(['ЕГЕРЬ'], (px_ - 4.8, py_ - 2.2, px_ + 4.8, py_ + 2.2), (40, 60, 40), pad=0.15)
    sp.cap(Q(-13.0, 12.0), Q(14.0, 12.0), 1.1, 1.1, tones((60, 40, 30)))                         # belt
    sp.union([sp.m_ell(*Q(1.0, 50.0), 11.0, 4.2)], tones(COLLAR))                                # fur collar
    # head on the collar
    hx, hy = Q(3.0, 59.0)
    # perm: curls around the head (behind the face)
    for (dx, dy, r) in ((-8.6, 4.0, 3.6), (-9.4, -0.6, 3.4), (-7.6, -4.6, 3.0), (7.8, 4.6, 3.0), (-4.0, 7.6, 3.4), (2.6, 8.4, 3.4),
                        (8.4, 1.0, 2.6)):
        sp.ell(hx + dx, hy + dy, r, r * 0.92, tones(PERM))
    face = sp.union([sp.m_ell(hx, hy, 8.4, 9.2), sp.m_ell(hx + 2.4, hy - 3.6, 7.0, 6.0)], tones(SKIN))
    lx, ly = look
    DX.eye(sp, hx + 3.6, hy + 1.8, 4.6, 5.0, E, (90, 70, 40), (lx, ly), blink, lash=INK, skin=SKIN, bold=1, lidc=SHADOW_EYE)
    DX.eye(sp, hx - 2.6, hy + 1.8, 4.0, 4.6, E, (90, 70, 40), (lx, ly), blink, lash=INK, skin=SKIN, bold=1, lidc=SHADOW_EYE)
    DX.brow(sp, hx + 3.8, hy + 6.2, 5.2, E, +1, (70, 40, 50), th=2, arch=1.2)
    DX.brow(sp, hx - 2.6, hy + 6.0, 4.4, E, -1, (70, 40, 50), th=2, arch=1.2)
    DX.blush(sp, hx - 1.6, hy - 2.4, 2.2, 1.4, (236, 110, 120))
    mx, my = hx + 3.6, hy - 5.0
    DX.mouth(sp, mx, my, 5.6, E, mouth_, LIPS, inside=(80, 20, 30), skin=SKIN, maxh=7)
    if max(mouth_, E['mo']) > 0.3:
        sp.fill(sp.m_super(mx + 1.2, my + 0.2, 0.7, 0.6, 3.0)[0], GOLD, keep=True)               # the gold tooth
    sp.ell(hx + 6.8, hy + 0.2, 1.8, 1.6, tones(mix(SKIN, (220, 110, 100), 0.4)), gloss=0.8)      # nose
    sp.dot(hx - 3.4, hy - 4.4, (80, 50, 40))                                                     # mole
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 0.6, hy + 1.8))
    # peaked forester cap
    crown = sp.union([sp.m_ell(hx + 0.4, hy + 11.4, 10.6, 3.4)], tones(CAPC))
    sp.union([sp.m_ell(hx + 0.6, hy + 8.6, 9.0, 1.8)], tones(dark(CAPC, 0.7)))                   # band
    sp.union([sp.m_ell(hx + 8.0, hy + 7.4, 5.2, 1.3, -0.15)], tones((24, 24, 28)), gloss=1.0)     # visor
    sp.ell(hx + 3.0, hy + 9.4, 1.5, 1.5, tones(GOLD), gloss=1.0, snow=False)                     # cockade
    for a in (-0.6, 0.6): thin(sp, (hx + 3.0, hy + 9.4), (hx + 3.0 + 2.4 * math.cos(a + 3.14), hy + 9.4 + 1.2 * math.sin(a)), GOLD, 0.3)
    sp.outline(INK, 1)
    # whistle on a string over the collar
    if whistle:
        stroke(sp, [(hx - 4.0, hy - 7.0), (hx - 1.0, hy - 12.0), (hx + 3.0, hy - 15.0)], (230, 230, 230), 0.16)
        sp.sup(hx + 3.6, hy - 15.8, 1.6, 0.9, tones(SILVER), n=3.0, gloss=1.0)
    # near arm
    before = sp.m.copy()
    shN = Q(12.0, 46.0)
    hn = hand_n if hand_n is not None else Q(16.0 + swing * 0.6, 28.0)
    kN, eN = ik(shN, hn, 10.0, 9.0, -1.0)
    sp.cap(shN, kN, 3.7, 3.3, tones(COAT)); sp.cap(kN, eN, 3.3, 3.0, tones(COAT))
    sp.ell(*eN, 2.6, 2.6, tones(SKIN))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o
