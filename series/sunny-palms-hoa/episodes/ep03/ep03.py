"""S01E03 «Suspicious Man (Walking)» — Brenda posts Dale taking out the trash as a "suspicious man" on NeighborNet; Dale's own Ring
shows Brenda moving his mailbox six inches at 3 a.m.; the footage is inadmissible (black doorbell); Earl has a cat on his head.
  python3 ep03.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import paths as P
import stage as ST
from stage import Chars, view_at
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import us_cast as U
from props import us_props as UP
from props import uskit as K
from props import folk as F
from props import bytfx as B
from props.usshots import Shots, J, hit
from timeline import DUR, FPS, VOICE, SLUG

EPI = Episode('ep03', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
YARD = ST.ai_world(P.series(SLUG) / 'bg' / 'yard.png')
S = Shots(talk, YARD)
WU = 6.4
MB = (345.0, 478.0)


def ph(screen):
    return lambda L, h: UP.phone(L, h, 0.0, screen=screen)


def cat_hook(t):
    """Mr. Whiskers (Valera's fat ginger cat, reused) sits on Earl's head, unbothered"""
    def f(CH, v):
        EX, EY, EU = S.E
        F.cat(CH, v.cam(EX - 2.6 * EU, EY - 3.7 * EU, EU * 0.42), t, 'loaf', 0.0, 0.55 if (t % 4.5) > 0.2 else 0.95, (0.0, 0.0), 'deadpan', tail=0.5)
    return f


# ================================================================== shots
def r_hook(t, u):
    return S.cu_dale(t, u, 'incredulous', 1.75, dx=34, hand=U.H(6.4, 14.6), prop=ph('feed'), red=0.3, look=0.2)


def r_b1(t, u):
    return S.cu_brenda(t, u, 'sweet', 2.0, hand=U.H(6.2, 13.0), prop=ph('ring'))


def r_d2(t, u):
    return S.cu_dale(t, u, 'shout', 2.1, red=0.7, sweat=0.5, hand=U.H(6.4, 12.4), prop=UP.trash_bag)


def r_b2(t, u):
    return S.cu_brenda(t, u, 'bright' if u < 2.4 else 'sweet', 2.1 + J(u, 2.0), hand=U.H(3.4, 10.6), prop=lambda L, h: UP.clipboard(L, h, -0.15, w=4.4, hh=6.0, title='CALENDAR'))


def r_feed(t, u):
    big = np.zeros((1920, 1080, 3), np.uint8)
    UP.neighbornet_feed(big, t, u)
    return big


def r_d3(t, u):
    return S.cu_dale(t, u, 'sly', 2.0 + J(u, 1.9), shades=True, hand=U.H(6.8, 14.4), prop=ph('truck'), red=0.25)


def r_ring(t, u):
    """Ring footage, 3:04 a.m.: Brenda in a robe and curlers digs, shifts the mailbox six inches, measures, waves at the camera"""
    Z = 1.2
    v = view_at(YARD, 400, 490, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    mbx = MB[0] - 26.0 * sm((u - 1.55) / 0.45)
    UP.mailbox_world(CH, v, mbx, MB[1], 0.0, t, s=0.75)
    if u > 1.0:                                                                                   # heap of dirt at the post
        L = Layer(v.wcam())
        UP.ell(L, (338 + 6 * u, 560), 16, 5, (96, 66, 46), 0, (130, 92, 62), (60, 40, 28))
        CH.add(L)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    bx = 395.0
    if u < 0.9:
        x = lerp(600.0, bx, u / 0.9)
        U.brenda(C2, v.cam(x, 592.0, WU, flip=True), U.bwalk(t, 9.0, 0.5, 'shoulder'), t, 0.0, 'sweet', 0.0, hand_n=U.H(2.2, 19.6), prop_n=lambda L, h: UP.shovel(L, h, -2.4),
                 outfit='robe', blink=False)
    elif u < 1.55:
        dig = 0.9 * math.sin((u - 0.9) * 12)
        U.brenda(C2, v.cam(bx, 592.0, WU, flip=True), U.BPOSE['shovel'], t, 0.0, 'evil', 0.0, hand_n=U.H(6.8, 12.0 + dig), prop_n=lambda L, h: UP.shovel(L, h, 1.0), outfit='robe')
    elif u < 2.4:
        U.brenda(C2, v.cam(bx, 592.0, WU, flip=True), U.BPOSE['point'], t, 0.0, 'evil', 0.0, hand_n=U.H(6.6 + 1.2 * math.sin(u * 10), 16.2), outfit='robe')
    elif u < 3.1:
        U.brenda(C2, v.cam(bx, 592.0, WU, flip=True), U.BPOSE['measure'], t, 0.0, 'sweet', 0.0, hand_n=U.H(6.8, 11.6), prop_n=UP.tape_hold, outfit='robe')
    else:
        U.brenda(C2, v.cam(bx, 592.0, WU, flip=True), dict(U.BPOSE['wave'], n=(5.4, 22.6 + 1.6 * math.sin(t * 14))), t, 0.0, 'sweet', 0.0, outfit='robe', blink=False)
    C2.comp(big, K.light_yard(v))
    if 2.4 <= u < 3.1:                                                                            # the tape: 6 inches, exaggerated
        L = Layer(v.wcam())
        k = sm((u - 2.4) / 0.25)
        x0 = 372.0; x1 = x0 - 74 * k
        UP.cap(L, (x0, 510), (x1, 510), 2.6, 2.6, (255, 214, 50)); UP.cap(L, (x0, 510), (x1, 510), 0.5, 0.5, (30, 30, 34))
        FX.add(L); FX.comp(big)
    if u < 0.15:                                                                                  # cut glitch
        r = np.random.default_rng(int(t * 60))
        for i in range(10):
            y0 = int(r.integers(0, 1900)); big[y0:y0 + 18] = np.roll(big[y0:y0 + 18], int(r.integers(-120, 120)), 1)
    UP.ring_look(big, t)
    return big


def r_d4(t, u):
    return S.cu_dale(t, u, 'shock', 2.0 + J(u, 1.6), shades=None, sweat=0.9, red=0.05, look=0.3, pose=U.DPOSE['stand'], zoom=0.1)


def r_b3(t, u):
    return S.cu_brenda(t, u, 'sweet', 2.1 + J(u, 1.5), hand=U.H(4.4, 11.4), prop=UP.tape_hold)


def r_d5(t, u):
    return S.cu_dale(t, u, 'cheer', 2.1, shades=(u > 0.1), hand=U.H(8.6, 26.0 - 1.4 * math.sin(u * 20)), zoom=0.15)


def r_b4(t, u):
    return S.cu_brenda(t, u, 'sweet' if u < 1.5 else 'evil', 2.1 + J(u, 1.9), pose=U.BPOSE['hands'], lean=0.3)


def r_d6(t, u):
    return S.cu_dale(t, u, 'shout', 2.2 + J(u, 1.3), shades=None, red=0.9, sweat=0.7, pose=U.DPOSE['shout'])


def r_b5(t, u):
    return S.cu_brenda(t, u, 'bright', 2.3, pose=U.BPOSE['hands'], lean=0.3)


def r_bless(t, u):
    return S.cu_brenda(t, u, 'sweet', 2.3, lean=0.4, pose=U.BPOSE['hands'])


def r_earl(t, u):
    return S.cu_earl(t, u, 0.5, 2.3 + 0.0, front=cat_hook(t), dy=8, dx=14)


def r_tail(t, u):
    slide = 1 - sm(u / 0.25)
    return S.cu_dale(t, u, 'sad' if u < 0.5 else 'incredulous', 1.75, dx=34, shades=None, hand=U.H(5.6 + 6 * slide, 12.6 - 6 * slide),
                     prop=lambda L, h: UP.notice(L, h, -0.2 - 1.2 * slide, w=5.2, hh=6.8, txt='$100'), red=0.4, sweat=0.4)


SHOTS = [
    (0.00, 3.00, 'hook'), (3.00, 5.66, 'b1'), (5.66, 7.80, 'd2'), (7.80, 11.95, 'b2'), (11.95, 15.30, 'feed'), (15.30, 19.15, 'd3'),
    (19.15, 23.00, 'ring'), (23.00, 26.31, 'd4'), (26.31, 29.31, 'b3'), (29.31, 30.69, 'd5'), (30.69, 34.50, 'b4'), (34.50, 37.13, 'd6'),
    (37.13, 38.69, 'b5'), (38.69, 40.40, 'bless'), (40.40, 42.10, 'earl'), (42.10, DUR + 1, 'tail'),
]
FN = dict(hook=r_hook, b1=r_b1, d2=r_d2, b2=r_b2, feed=r_feed, d3=r_d3, ring=r_ring, d4=r_d4, b3=r_b3, d5=r_d5, b4=r_b4, d6=r_d6, b5=r_b5,
          bless=r_bless, earl=r_earl, tail=r_tail)


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 3, ['SUSPICIOUS MAN', '(WALKING)'], hook_t=(0.15, 2.5),
              stickers=[
                  (st('TRASH = TUESDAY', (150, 255, 170), 58), 8.6, 9.9, 540, 380),
                  (st('TODAY = WEDNESDAY', (255, 100, 100), 52), 10.05, 11.9, 540, 380),
                  (st('47 CLIPS OF HIS TRUCK', (255, 236, 120), 40), 16.7, 19.0, 540, 380),
                  (st('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30), 17.6, 19.1, 540, 1480),
                  (st('6 INCHES', (255, 236, 90), 100), 21.85, 22.95, 540, 420),
                  (st('AURA +9999', (255, 236, 96), 60), 29.35, 30.6, 540, 340),
                  (st('AURA -9999', (255, 100, 100), 60), 32.2, 33.5, 540, 340),
                  (st('ECRU WHISPER', (250, 232, 190), 64), 37.15, 38.65, 540, 380),
                  (st('(TRANSLATION: YOU IDIOT)', (255, 190, 226), 28), 38.75, 40.35, 540, 1130),
                  (st('TOTAL FINES: $1,150', (255, 236, 120), 40), 42.6, 44.2, 540, 1450),
              ],
              flashes=[29.31], mosaics=[11.95, 19.15], cap_y={'feed': 1800, 'ring': 1700},
              teaser='NEXT: CATEGORY 5')


def render(t):
    a, b, name = shot_at(t)
    big = FN[name](t, t - a)
    SHOW.apply(big, t, name)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
