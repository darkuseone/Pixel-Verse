"""S01E06 «Vote Earl» (season finale) — HOA election: Dale runs on "fewer fines"; Earl (resident since 1987) casts the deciding vote
("He's the main character"); Dale becomes president, puts on the visor and fines Brenda for her mailbox with her own E01 lines.
  python3 ep06.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
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

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
CLUB = ST.ai_world(P.series(SLUG) / 'bg' / 'clubhouse.png')
S = Shots(talk, CLUB, dale=(330.0, 600.0, 16.0), brenda=(760.0, 600.0, 16.0), earl=(1040.0, 585.0, 11.0))
WU = 6.4


def pod_d():
    def f(CH, v):
        DX, DY, DU = S.D
        UP.podium_front(CH, v.cam(DX, DY, DU))
    return f


def pod_b():
    def f(CH, v):
        BX, BY, BU = S.B
        UP.podium_front(CH, v.cam(BX, BY, BU, flip=True))
    return f


def ballot_front(t):
    def f(CH, v):
        EX, EY, EU = S.E
        UP.ballot_in_mouth(CH, v.cam(EX, EY, EU), 0.0, 'DALE')
    return f


def fines_board(L, h):
    UP.clipboard(L, h, -0.12, w=4.6, hh=6.2, title='FINES')


def notice250(L, h):
    UP.notice(L, h, -0.2, 5.4, 6.8, '$250')


# ================================================================== shots
def r_hook(t, u):
    return S.cu_dale(t, u, 'shout', 1.8, dx=10, red=0.35, front=pod_d())


def r_b1(t, u):
    return S.cu_brenda(t, u, 'sweet', 2.0 + J(u, 2.2), front=pod_b())


def r_d2(t, u):
    return S.cu_dale(t, u, 'smug', 2.0, shades=True, front=pod_d(), zoom=0.1)


def r_b2(t, u):
    return S.cu_brenda(t, u, 'hollow' if u < 1.3 else 'evil', 2.1, front=pod_b(), zoom=0.1)


def r_d3(t, u):
    return S.cu_dale(t, u, 'cheer' if u > 3.0 else 'smug', 1.9 + J(u, 1.9), front=pod_d(), red=0.3)


def confetti(big, t, k=1.0, n=70):
    rng = np.random.default_rng(3)
    cols = ((255, 90, 150), (90, 210, 240), (255, 220, 70), (120, 220, 120), (255, 255, 255))
    for i in range(int(n * k)):
        x = int(rng.uniform(0, 1080)); ph = (t * 0.7 + rng.uniform(0, 1)) % 1.0
        y = int(ph * 2100 - 120); w = int(rng.integers(10, 24))
        x = int(x + 40 * math.sin(t * 5 + i))
        if 0 <= y < 1900 and 0 <= x < 1050: big[y:y + w, x:x + w * 2 // 3] = cols[i % 5]


def r_cheer(t, u):
    """the crowd goes wild after «I will fine nobody. Except Brenda.»"""
    Z = 1.0
    v = view_at(CLUB, 540, 420, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    C1 = Chars()
    U.dale(C1, v.cam(390.0, 590.0, WU), U.DPOSE['cheer'], t, 0.7, 'cheer', 0.0, False, hand_n=U.H(8.6, 26.0 - 1.4 * math.sin(u * 20)), legs=False)
    UP.podium_front(C1, v.cam(390.0, 590.0, WU))
    U.brenda(C1, v.cam(690.0, 590.0, WU, flip=True), U.BPOSE['stand'], t, 0.0, 'hollow', 0.0, legs=False)
    UP.podium_front(C1, v.cam(690.0, 590.0, WU, flip=True))
    C1.comp(big, K.light_yard(v))
    C2 = Chars()
    UP.crowd_back(C2, v, 14, 690.0, 40.0, 1240.0, 7.0, t, 1.0)
    C2.comp(big, K.light_yard(v))
    confetti(big, t)
    B.shake(big, t, 5 * max(0.0, 1 - u / 0.8), 31)
    fx.vignette(big, 0.22)
    return big


def r_vote(t, u):
    """two ballots drop into the box: Brenda 1, Dale 1"""
    Z = 1.5
    v = view_at(CLUB, 330, 490, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    for k, t0 in enumerate((0.0, 0.85)):
        p = (u - t0) / 0.45
        if 0 <= p < 1.0: UP.ballot_paper(CH, v, 330.0, lerp(420.0, 528.0, p * p), 1.3, 0.3 * math.sin(p * 6))
    UP.ballot_box(CH, v, 330.0, 620.0, 1.15)
    CH.comp(big, K.light_yard(v))
    UP.tally_overlay(big, v, 1 if u > 0.4 else 0, 1 if u > 1.25 else 0, 330.0, 372.0)
    fx.vignette(big, 0.25)
    return big


def r_e1(t, u):
    return S.cu_earl(t, u, 0.5, 2.5, front=ballot_front(t))


def r_b3(t, u):
    return S.cu_brenda(t, u, 'shock', 2.2, front=pod_b(), sweat=1.0, zoom=0.14)


def r_e2(t, u):
    return S.cu_earl(t, u, 0.5, 2.4 + J(u, 1.6, 0.4))


def r_b4(t, u):
    return S.cu_brenda(t, u, 'hollow', 2.1 + J(u, 1.5), front=pod_b(), sweat=0.6, lean=0.3)


def r_yes(t, u):
    return S.cu_dale(t, u, 'cheer', 2.1, shades=True, hand=U.H(8.6, 26.0 - 1.4 * math.sin(u * 20)), front=pod_d(), zoom=0.15)


def r_visor(t, u):
    """the president's visor lands on Dale's head: the smile changes"""
    on = u > 0.3
    big = S.cu_dale(t, u, 'smug' if on else 'cheer', 2.0, shades=False, visor=on, front=pod_d(), zoom=0.12, red=0.1)
    if 0.3 <= u < 0.45: O.flash(big, 0.5 * (1 - (u - 0.3) / 0.15))
    if 0.3 <= u < 0.6: B.shake(big, t, 8 * (1 - (u - 0.3) / 0.3), 33)
    return big


def r_d4(t, u):
    return S.cu_dale(t, u, 'smug', 2.0 + J(u, 1.6, 0.3), visor=True, hand=U.H(5.6, 12.6), prop=fines_board, red=0.05)


def r_b5(t, u):
    return S.cu_brenda(t, u, 'shock', 2.2, hand=U.H(5.6, 13.2), prop=notice250, sweat=0.8, zoom=0.12)


def r_d5(t, u):
    return S.cu_dale(t, u, 'smug', 2.1, visor=True, hand=U.H(5.6, 12.6), prop=fines_board, zoom=0.1)


def r_b6(t, u):
    return S.cu_brenda(t, u, 'evil', 2.3, hand=U.H(5.6, 13.2), prop=notice250, sweat=0.6, zoom=0.14)


def r_d6(t, u):
    return S.cu_dale(t, u, 'smug', 2.3, visor=True, shades=None, zoom=0.14, lean=0.3)


def r_e3(t, u):
    return S.cu_earl(t, u, 0.5, 2.4 + J(u, 1.5, 0.4))


def r_tail(t, u):
    """wide: President Dale with the clipboard, Brenda with the pink notice, Earl watching"""
    Z = 1.0
    v = view_at(CLUB, 640, 430, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    C1 = Chars()
    U.dale(C1, v.cam(560.0, 592.0, WU), U.DPOSE['hold'], t, 0.0, 'smug', 0.0, False, visor=True, hand_n=U.H(6.4, 12.4), prop_n=fines_board)
    U.brenda(C1, v.cam(760.0, 592.0, WU, flip=True), U.BPOSE['stand'], t, 0.0, 'hollow', 0.0, hand_n=U.H(3.4, 12.4), prop_n=notice250, sweat=0.8)
    U.earl(C1, v.cam(1040.0, 585.0, 4.6), t, 0.0, 0.5, (-0.6, 0.0), None, 0.0, 1.0, True)
    C1.comp(big, K.light_yard(v))
    fx.vignette(big, 0.22)
    return big


SHOTS = [
    (0.00, 3.10, 'hook'), (3.10, 7.46, 'b1'), (7.46, 10.62, 'd2'), (10.62, 13.46, 'b2'), (13.46, 17.40, 'd3'), (17.40, 19.00, 'cheer'),
    (19.00, 21.10, 'vote'), (21.10, 23.94, 'e1'), (23.94, 25.92, 'b3'), (25.92, 28.40, 'e2'), (28.40, 31.48, 'b4'), (31.48, 32.42, 'yes'),
    (32.42, 33.85, 'visor'), (33.85, 37.08, 'd4'), (37.08, 38.51, 'b5'), (38.51, 41.33, 'd5'), (41.33, 43.05, 'b6'), (43.05, 44.53, 'd6'),
    (44.53, 47.48, 'e3'), (47.48, DUR + 1, 'tail'),
]
FN = dict(hook=r_hook, b1=r_b1, d2=r_d2, b2=r_b2, d3=r_d3, cheer=r_cheer, vote=r_vote, e1=r_e1, b3=r_b3, e2=r_e2, b4=r_b4, yes=r_yes,
          visor=r_visor, d4=r_d4, b5=r_b5, d5=r_d5, b6=r_b6, d6=r_d6, e3=r_e3, tail=r_tail)


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 6, ['VOTE DALE', 'NO FINES!'], hook_t=(0.15, 2.5),
              stickers=[
                  (st('[CROWD GOES WILD]', (255, 255, 255), 30), 17.5, 19.0, 540, 1480),
                  (st('RESIDENT SINCE 1987', (255, 226, 110), 46), 26.0, 28.3, 540, 380),
                  (st('DALE 2 - BRENDA 1', (255, 236, 120), 52), 29.0, 31.4, 540, 380),
                  (st('AURA +9999', (255, 236, 96), 60), 31.52, 32.4, 540, 340),
                  (st('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30), 32.2, 33.9, 540, 1480),
                  (st('PRESIDENT DALE', (255, 226, 110), 66), 33.9, 36.0, 540, 340),
                  (st('AURA -9999', (255, 100, 100), 60), 36.1, 37.0, 540, 340),
                  (st('FINE: $250', (255, 84, 96), 90), 37.3, 38.5, 540, 340),
                  (st('(TRANSLATION: YOU IDIOT)', (255, 190, 226), 28), 43.1, 44.5, 540, 1130),
                  (st('[SAXOPHONE GETS LOUDEST]', (255, 255, 255), 30), 44.1, 46.6, 540, 1480),
                  (st('TOTAL FINES: $250 (BRENDA)', (255, 236, 120), 34), 47.6, 49.4, 540, 1450),
              ],
              flashes=[31.48], mosaics=[17.4, 33.85], cap_y={'cheer': 1600, 'vote': 1600},
              teaser='SEASON 2: COMING SOON')


def render(t):
    a, b, name = shot_at(t)
    big = FN[name](t, t - a)
    SHOW.apply(big, t, name)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
