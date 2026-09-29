"""S01E04 «Category 5 (Permit)» — Dale throws a hurricane party; Brenda fines the hurricane (Kevin, no permit), the storm obeys and leaves,
and the fine goes to the homeowner whose lawn it landed on. Earl: she never fined me. Think about that.
  python3 ep04.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props import bytfx as B
from props.usshots import Shots, J, hit
from timeline import DUR, FPS, VOICE, SLUG

EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
YARD = ST.ai_world(P.series(SLUG) / 'bg' / 'yard.png')
STORM = ST.ai_world(P.series(SLUG) / 'bg' / 'yard_storm.png')
WU = 6.4
FLASHES = ((0.95, 1.08), (10.25, 10.40), (11.60, 11.75))
STORM_END = 17.95


def storm_post(big, t):
    UP.rain(big, t, 1.0, 0.35, 150)
    B.shake(big, t, 3, 29)
    for a, b in FLASHES:
        if a <= t < b: O.flash(big, 0.55 * (1 - (t - a) / (b - a)))


def calm_post(big, t):
    UP.rainbow(big, 0.28)


SS = Shots(talk, STORM, light=K.light_storm, post=storm_post)
CS = Shots(talk, YARD, post=calm_post)


def chair_behind(t):
    def f(CH, v):
        DX, DY, DU = SS.D
        UP.lawn_chair(CH, v.cam(DX, DY, DU), t)
    return f


def cooler_front(x_off=8.2, s=0.7):
    def f(CH, v):
        DX, DY, DU = SS.D
        UP.cooler(CH, v.cam(DX + x_off * DU, DY, DU * s))
    return f


def umbrella_front(hand_x=3.4, hand_h=13.0):
    def f(CH, v):
        BX, BY, BU = SS.B
        UP.umbrella(CH, v.cam(BX, BY, BU, flip=True), hand_x, hand_h)
    return f


def weeds_front(CS_=None):
    def f(CH, v):
        DX, DY, DU = SS.D
        UP.weeds(CH, v.cam(DX, DY, DU))
    return f


def notice_prop(txt, w=5.6, hh=7.0, ang=-0.2):
    return lambda L, h: UP.notice(L, h, ang, w, hh, txt)


def debris_front(t):
    """Kevin (plastic flamingo) and the ticket drift on the pond after the storm"""
    def f(CH, v):
        EX, EY, EU = CS.E
        UP.flamingo(CH, v.cam(EX + 9.5 * EU, EY + 0.2 * EU, EU * 0.42, flip=True), t, True, True, 0.0, 0.0)
    return f


# ================================================================== shots
def r_hook(t, u):
    return SS.cu_dale(t, u, 'cheer', 1.6, dx=18, dy=-6, shades=True, hand=U.H(6.6, 12.4), prop=UP.koozie_can, red=0.15, look=0.2,
                      behind=chair_behind(t), front=cooler_front(9.0, 0.8))


def r_b1(t, u):
    return SS.cu_brenda(t, u, 'sweet', 2.0, hand=U.H(3.4, 12.0), prop=lambda L, h: UP.clipboard(L, h, -0.15, w=4.4, hh=6.0), behind=umbrella_front())


def r_d2(t, u):
    return SS.cu_dale(t, u, 'cheer', 2.1, shades=True, hand=U.H(8.6, 25.0 - 1.2 * math.sin(u * 16)), behind=chair_behind(t), zoom=0.12, red=0.2)


def r_d0(t, u):
    return SS.cu_dale(t, u, 'smug', 1.7 + J(u, 1.8, 0.4), dx=22, shades=True, hand=U.H(6.6, 12.4), prop=UP.koozie_can, red=0.2,
                      behind=chair_behind(t), front=cooler_front(9.0, 0.8))


def r_storm(t, u):
    """the hurricane arrives: flamingos, a mailbox and Dale in his lawn chair fly past"""
    Z = 1.0
    v = view_at(STORM, 480, 470, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    for i in range(6):
        ph = (u * 0.85 + i * 0.19) % 1.0
        x = lerp(780.0, 120.0, ph); y = 300 + 40 * i + 50 * math.sin(ph * 9 + i)
        UP.flamingo(CH, v.cam(x, y, 3.6 + 0.3 * (i % 3), flip=int(t * 12 + i) % 2 == 0), t + i, True, i % 2 == 0, 0.0, 0.0)
    ph = (u * 0.7 + 0.1) % 1.0
    UP.mailbox_world(CH, v, lerp(760.0, 110.0, ph), 330 + 60 * math.sin(ph * 12), 0.0, t, s=0.9)
    CH.comp(big, K.light_storm(v))
    C2 = Chars()
    px = lerp(760.0, -20.0, min(1.0, u / 3.0)); py = 545 - 50 * abs(math.sin(u * 5))
    UP.lawn_chair(C2, v.cam(px, py, 5.0))
    U.dale(C2, v.cam(px, py - 4 * 5.0, 5.0), U.DPOSE['cheer'], t, 0.8, 'cheer', 0.0, True, legs=False, hand_n=U.H(7.4, 24.0 + 2 * math.sin(t * 20)),
           prop_n=UP.koozie_can)
    C2.comp(big, K.light_storm(v))
    storm_post(big, t)
    UP.rain(big, t + 0.5, 0.6, 0.6, 120)
    fx.vignette(big, 0.3)
    return big


def r_b3(t, u):
    return SS.cu_brenda(t, u, 'sweet', 2.1 + J(u, 2.1), pose=U.BPOSE['hands'], lean=0.2, behind=umbrella_front(3.8, 12.2))


def r_ticket(t, u):
    """Brenda hands the storm a ticket; the storm stops and leaves"""
    storm = u < 0.9
    world = STORM if storm else YARD
    Z = 1.1
    v = view_at(world, 540, 470, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    light = K.light_storm if storm else K.light_yard
    C2 = Chars()
    hand = U.H(6.0 + 2.0 * sm(u / 0.4), 22.0 - 2.0 * sm(u / 0.4)) if storm else U.H(3.4, 13.6)
    U.brenda(C2, v.cam(620.0, 600.0, WU, flip=True), U.BPOSE['point'] if storm else U.BPOSE['wave'], t, 0.0, 'sweet', 0.0, hand_n=hand)
    if storm: UP.umbrella(C2, v.cam(620.0, 600.0, WU, flip=True), 3.4, 12.0)
    C2.comp(big, light(v))
    if storm:                                                                                    # the ticket flies off into the wind
        L = Layer(v.cam(500.0 - 220 * max(0.0, u - 0.3), 330.0 - 60 * max(0.0, u - 0.3), 6.0))
        UP.notice(L, U.H(0, 0), 0.3 + 9 * u, 5.4, 7.0, '$500')
        C3 = Chars(); C3.add(L); C3.comp(big, light(v))
        storm_post(big, t)
    else:
        UP.rainbow(big, 0.34)
    fx.vignette(big, 0.24)
    return big


def r_d3(t, u):
    return CS.cu_dale(t, u, 'shock', 2.0, shades=None, sweat=1.0, look=0.3, front=weeds_front(), zoom=0.08)


def r_b4(t, u):
    return CS.cu_brenda(t, u, 'sweet', 2.2, pose=U.BPOSE['hands'], lean=0.3)


def r_d4(t, u):
    return CS.cu_dale(t, u, 'smug', 2.0 + J(u, 1.3), shades=None, sweat=0.7, front=weeds_front(), red=0.1)


def r_b5(t, u):
    return CS.cu_brenda(t, u, 'hollow' if u < 0.9 else 'evil', 2.4, pose=U.BPOSE['hands'], lean=0.4, zoom=0.14)


def r_d5(t, u):
    return CS.cu_dale(t, u, 'shock', 2.3, shades=None, sweat=1.0, front=weeds_front(), pose=U.DPOSE['shout'], zoom=0.2)


def r_b6(t, u):
    return CS.cu_brenda(t, u, 'bright' if u < 2.4 else 'sweet', 2.1 + J(u, 2.0), hand=U.H(7.4, 13.6), prop=notice_prop('$4750'))


def r_d6(t, u):
    return CS.cu_dale(t, u, 'sad', 2.0 + J(u, 1.1, 0.3), shades=None, sweat=1.0, front=weeds_front(), hand=U.H(6.2, 12.8), prop=notice_prop('$4750', 5.0, 6.4), zoom=0.12)


def r_earl(t, u):
    return CS.cu_earl(t, u, 0.5, 2.4 + J(u, 2.5, 0.4), front=debris_front(t))


def r_tail(t, u):
    slide = 1 - sm(u / 0.25)
    return CS.cu_dale(t, u, 'sad' if u < 0.5 else 'incredulous', 1.75, dx=34, shades=None, hand=U.H(5.6 + 6 * slide, 12.6 - 6 * slide),
                      prop=notice_prop('$4750', 5.2, 6.8, -0.2 - 1.2 * slide), red=0.3, sweat=0.6, front=weeds_front())


SHOTS = [
    (0.00, 2.40, 'hook'), (2.40, 4.12, 'b1'), (4.12, 5.97, 'd2'), (5.97, 9.60, 'd0'), (9.60, 12.70, 'storm'), (12.70, 17.06, 'b3'),
    (17.06, 18.96, 'ticket'), (18.96, 21.33, 'd3'), (21.33, 22.87, 'b4'), (22.87, 25.58, 'd4'), (25.58, 27.48, 'b5'), (27.48, 28.36, 'd5'),
    (28.36, 32.95, 'b6'), (32.95, 35.17, 'd6'), (35.17, 40.29, 'earl'), (40.29, DUR + 1, 'tail'),
]
FN = dict(hook=r_hook, b1=r_b1, d2=r_d2, d0=r_d0, storm=r_storm, b3=r_b3, ticket=r_ticket, d3=r_d3, b4=r_b4, d4=r_d4, b5=r_b5, d5=r_d5,
          b6=r_b6, d6=r_d6, earl=r_earl, tail=r_tail)


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 4, ['CATEGORY 5:', 'THE GOOD ONE?'], hook_t=(0.15, 2.3),
              stickers=[
                  (st('HURRICANE PARTY', (255, 236, 120), 60), 6.2, 7.8, 540, 380),
                  (st('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30), 9.5, 11.2, 540, 1480),
                  (st('WIND: 156 MPH', (255, 120, 110), 64), 9.85, 12.3, 540, 380),
                  (st('FINE: $500 (WIND)', (255, 236, 120), 46), 17.5, 18.9, 540, 1200),
                  (st('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30), 25.6, 27.2, 540, 1480),
                  (st('AURA -9999', (255, 100, 100), 60), 27.5, 28.6, 540, 340),
                  (st('$4,750', (255, 84, 96), 130), 29.4, 31.6, 540, 470),
                  (st('TOTAL FINES: $5,900', (255, 236, 120), 40), 40.7, 42.3, 540, 1450),
              ],
              flashes=[17.95], mosaics=[9.6, 35.17], cap_y={'storm': 1500, 'ticket': 1500},
              teaser='NEXT: SUGGESTED TIP')


def render(t):
    a, b, name = shot_at(t)
    big = FN[name](t, t - a)
    SHOW.apply(big, t, name)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
