"""S01E05 «Suggested Tip» — a FREE hot dog at the HOA barbecue costs $47.63 on the payment tablet (convenience fee, bun surcharge, tip prompts,
a guilt-tripping "no tip" flow); the tablet finally turns to the camera and asks YOU for a tip. Earl: Don't.
  python3 ep05.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
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

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
CLUB = ST.ai_world(P.series(SLUG) / 'bg' / 'clubhouse.png')
S = Shots(talk, CLUB, dale=(330.0, 600.0, 16.0), brenda=(760.0, 600.0, 16.0), earl=(1040.0, 585.0, 11.0))


def plate(L, h):
    UP.ell(L, h, 3.4, 1.0, (250, 250, 246), 0, (255, 255, 255), (196, 200, 208))
    UP.ell(L, h, 2.3, 0.6, (232, 236, 240))


def dog_tongs(L, h):
    UP.tongs(L, h, -0.2)
    UP.hot_dog(L, (h[0] + 2.9, h[1] + 0.6))


def naked_sausage(L, h):
    UP.hot_dog(L, h, bun=False, mustard=False)


def long_receipt(L, h):
    cx, cy = h[0] + 0.4, h[1] + 4.6
    UP.rect(L, cx, cy, 3.6, 12.0, 0.03, (252, 252, 250))
    for k in range(7): UP.cap(L, (cx - 1.2, cy - 5.0 + 1.5 * k), (cx + 1.2 - 0.3 * (k % 3), cy - 5.0 + 1.5 * k), 0.11, 0.11, (150, 156, 170))
    UP.ltext(L, '$47.63', (cx, cy + 4.4), 0.9, (220, 40, 50))


def ui(state):
    def f(t, u):
        big = np.zeros((1920, 1080, 3), np.uint8)
        UP.tablet_ui(big, t, state, u, talk('tablet', t))
        return big
    return f


# ================================================================== shots
def r_hook(t, u):
    return S.cu_dale(t, u, 'shout', 1.9, red=0.6, sweat=0.4, hand=U.H(6.6, 13.4), prop=plate, look=0.2)


def r_b1(t, u):
    return S.cu_brenda(t, u, 'sweet', 2.0, hand=U.H(4.8, 14.6), prop=dog_tongs)


def r_d2(t, u):
    return S.cu_dale(t, u, 'sly', 2.0 + J(u, 1.6), shades=True, hand=U.H(6.6, 13.4), prop=plate, red=0.2)


def r_d3(t, u):
    return S.cu_dale(t, u, 'shout', 2.2, red=0.9, sweat=0.7, pose=U.DPOSE['shout'])


def r_b2(t, u):
    return S.cu_brenda(t, u, 'sweet' if u < 1.7 else 'evil', 2.1 + J(u, 1.4), pose=U.BPOSE['hands'], lean=0.3)


def r_d4(t, u):
    return S.cu_dale(t, u, 'shock', 2.1 + J(u, 1.0, 0.3), sweat=0.9, look=1.0 * math.sin(t * 9), red=0.5)


def r_d5(t, u):
    return S.cu_dale(t, u, 'sad', 2.2, shades=None, sweat=0.6, zoom=0.1, red=0.2)


def r_d6(t, u):
    return S.cu_dale(t, u, 'shout', 2.3, red=1.0, sweat=0.8, pose=U.DPOSE['shout'], zoom=0.2)


def r_b3(t, u):
    return S.cu_brenda(t, u, 'bright', 2.1 + J(u, 1.2), hand=U.H(5.4, 14.0), prop=naked_sausage)


def r_video(t, u):
    big = ui('video')(t, u)
    if u > 3.0:                                                                                 # the tiny "no tip" gets circled
        k = sm((u - 3.0) / 0.5)
        im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        r = int(30 + 70 * k)
        d.ellipse([540 - r - 30, 1590 - r // 2 - 10, 540 + r + 30, 1590 + r // 2 + 10], outline=(230, 40, 60, 255), width=8)
        O.overlay(big, np.array(im), 0, 0, 1.0)
    return big


def r_earl(t, u):
    return S.cu_earl(t, u, 0.5, 2.4)


def r_tail(t, u):
    slide = 1 - sm(u / 0.25)
    return S.cu_dale(t, u, 'sad', 1.75, dx=34, shades=None, hand=U.H(5.6 + 6 * slide, 12.6 - 6 * slide), prop=long_receipt, red=0.4, sweat=0.5)


SHOTS = [
    (0.00, 1.82, 'hook'), (1.82, 5.89, 'tip'), (5.89, 8.26, 'b1'), (8.26, 11.39, 'd2'), (11.39, 15.15, 'receipt'), (15.15, 16.92, 'd3'),
    (16.92, 19.66, 'b2'), (19.66, 21.75, 'd4'), (21.75, 25.72, 'guilt'), (25.72, 27.10, 'd5'), (27.10, 29.60, 'review'), (29.60, 30.74, 'd6'),
    (30.74, 33.11, 'b3'), (33.11, 37.44, 'video'), (37.44, 39.00, 'earl'), (39.00, DUR + 1, 'tail'),
]
FN = dict(hook=r_hook, tip=ui('tip'), b1=r_b1, d2=r_d2, receipt=ui('receipt'), d3=r_d3, b2=r_b2, d4=r_d4, guilt=ui('guilt'), d5=r_d5,
          review=ui('review'), d6=r_d6, b3=r_b3, video=r_video, earl=r_earl, tail=r_tail)


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


UI_Y = 1750
SHOW = K.Show(EPI, 5, ['FREE HOT DOG', '$47.63?!'], hook_t=(0.15, 1.75),
              stickers=[
                  (st('20% x $0 = $0', (255, 236, 120), 56), 9.0, 11.2, 540, 380),
                  (st('CASH: +15%', (255, 100, 110), 76), 17.6, 19.5, 540, 380),
                  (st('[TABLET WHIMPERS]', (255, 255, 255), 30), 21.9, 24.0, 540, 1840),
                  (st('AURA -9999', (255, 100, 100), 60), 25.75, 26.95, 540, 340),
                  (st('BUN: +$1.50', (255, 236, 120), 76), 31.0, 32.9, 540, 470),
                  (st('[TABLET TURNS TO YOU]', (255, 255, 255), 30), 33.2, 35.2, 540, 1840),
                  (st('[NO TIP BUTTON: 4 PIXELS]', (255, 255, 255), 30), 35.5, 37.4, 540, 1840),
                  (st('TOTAL FINES: $5,947.63', (255, 236, 120), 36), 39.3, 41.0, 540, 1450),
              ],
              flashes=[29.60], mosaics=[11.39, 33.11], cap_y={'tip': UI_Y, 'receipt': UI_Y, 'guilt': UI_Y, 'review': UI_Y, 'video': UI_Y},
              teaser='NEXT: VOTE EARL')


def render(t):
    a, b, name = shot_at(t)
    big = FN[name](t, t - a)
    SHOW.apply(big, t, name)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
