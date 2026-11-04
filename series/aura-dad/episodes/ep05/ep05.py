"""S01E05 «$200 HAIR?!» — Lily sells Doug a $200 serum «that grows hair in ONE night». Doug: «tomorrow I'll look like a ROCK STAR».
MIRRA: «the label says ONE drop» — «One drop is for QUITTERS», he pours the whole bottle on the dome. Night: Biscuit the basset hound
licks the empty bottle by the bed (clue). Morning, in a beanie: «Ladies and gentlemen. The new DOUG.» — bald, four hairs left. TWIST
(56 %, «someone else took the prize»): Biscuit walks in with a flowing rock-star mane, guitar riff, wind. Kayden: «The dog has better
hair than you NOW.» Tammy: «He looks forty. In a GOOD way.» Doug: «I've still… GOT it?» — a hair falls. MIRRA: «Dog: plus one
thousand. Doug: minus four HUNDRED.»
  python3 ep05.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import stage as ST
from stage import view_at
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import decals as D
from props import auracast as A
from props import aurakit as K
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG,
              endcard=dict(style='auradad', lang='us', promise='TOMORROW: THE AURA BATTLE'))
talk = EPI.talk
W = K.build(names=['kitchen', 'bathroom', 'bedroom'])
K.decorate(W)
K.decorate_bed(W['bedroom'])
BATH, BED = W['bathroom'], W['bedroom']
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0

DB = (720.0, 670.0, 12.8)            # Doug at the vanity, facing left
LB = (520.0, 678.0, 13.0)            # Lily, facing right
LABEL = D.plate(40, 18, ['HAIR SERUM', 'USE 1 DROP'], bg=(255, 240, 200), colors=[(120, 70, 40), (226, 46, 70)], border=(120, 70, 40), pad=1.0)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def face(v, cam, r, ru=3.2):
    K.logface(v, cam, r['head'], ru)


def bathroom(v, t, draw=None, talk_=0.0, expr='calm', morning=False):
    CH, FX = K.begin()
    big = v.bg()
    L = Layer(v.wcam()); K.mirra_glass(L, t, talk_, expr); CH.add(L)
    if draw: draw(CH, v)
    L = Layer(K.fgcam(v, 0.45)); K.fg_plant(L, 1240, 800, 1.1, pot=(120, 200, 200)); F.outline(L, A.OL); CH.add(L)
    CH.comp(big, K.light_bath(v))
    K.glass_glow(big, v, t)
    if morning: fx.shafts(big, t, 0.6, 0.08, (255, 240, 200), 90, 260, 300)
    fx.motes(FX, v, t, 900, 120, 1240, 380, n=16, col=(255, 250, 230), seed=6)
    FX.comp(big)
    fx.vignette(big, 0.22)
    return big


def bedroom(v, t, draw=None):
    CH, FX = K.begin()
    big = v.bg()
    if draw: draw(CH, v)
    CH.comp(big, K.light_bed(v))
    fx.motes(FX, v, t, 880, 120, 1080, 340, n=14, col=(170, 190, 255), seed=13)
    FX.comp(big)
    fx.vignette(big, 0.36)
    return big


def doug_at(CH, v, t, pos, k=1.0, flip=True, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    kw.setdefault('expr', 'normal')
    if 'mouth_' not in kw: kw['mouth_'] = mouth('doug', t)
    r = A.doug(CH, cam, t=t, **kw)
    face(v, cam, r, 3.4)
    return cam, r


def char_at(fn, who, CH, v, t, pos, k=1.0, flip=False, ru=2.8, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    r = fn(CH, cam, t=t, mouth_=mouth(who, t), **kw)
    face(v, cam, r, ru)
    return cam, r


def dog_at(CH, v, t, pos, flip=False, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un, flip=flip)
    r = A.biscuit(CH, cam, t=t, **kw)
    face(v, cam, r, 1.8)
    return cam, r


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Daddy, this hair serum costs two hundred dollars. It grows hair in ONE night!» — Lily holds the bottle up; Doug bends to it,
    eyes huge, the dome gleams; MIRRA above in the mirror"""
    v = view_at(BATH, 640, 640, 1.08 + 0.04 * sm(u / 5.0), 180, 600)

    def draw(CH, v_):
        char_at(A.lily, 'lily', CH, v_, t, LB, expr='happy', pose=A.LPOSE['show'], prop_n=A.serum, patches=False)
        doug_at(CH, v_, t, DB, expr='shock', pose=A.DPOSE['fists'], mouth_=0.45 + 0.1 * math.sin(t * 6), lean=-0.6,
                shine=0.5 + 0.5 * math.sin(t * 5))
    return bathroom(v, t, draw, 0.0, 'smug')


def r_dream(t, u):
    """«One night? Then tomorrow I'll look like a ROCK STAR.» — Doug close, dreamy, twinkle"""
    x, y, un = DB
    k = 1.25
    hy = y - 25.4 * un * k
    v = view_at(BATH, x - 1.2 * un * k, hy, 1.42, 180, 330)

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, expr='happy', pose=A.DPOSE['cheer'], shine=0.6 + 0.4 * math.sin(t * 6))
    return bathroom(v, t, draw, 0.0, 'calm')


def r_label(t, u):
    """«Doug, the label says ONE drop.» — MIRRA close on the glass, the label decal under her"""
    v = view_at(BATH, 640, 240, 1.38 + 0.04 * sm(u / 2.5), 180, 300)
    big = bathroom(v, t, None, mouth('mirra', t, 2.0), 'calm')
    D.blit(big, v, LABEL, 612, 330)
    return big


def r_pour(t, u):
    """«One drop is for QUITTERS.» — he pours the whole bottle on the dome: glug, gleam, drips"""
    x, y, un = DB
    k = 1.15
    v = view_at(BATH, x - 0.6 * un * k, y - 22 * un * k, 1.3, 180, 330)
    hand = F.H(1.6, 32.4)

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, expr='smug', pose=A.DPOSE['stand'], hand_n=hand,
                prop_n=lambda L, h: A.serum(L, (h[0], h[1] + 2.4), empty=u > 1.6), wet=sm((u - 0.6) / 0.6))
    big = bathroom(v, t, draw, 0.0, 'sad')
    if 0.4 < u < 2.0:
        for i in range(5):
            dx, dy = v.opt(x - 0.5 * un * k + (i - 2) * 9, y - 31 * un * k + ((t * 300 + i * 40) % 90))
            fx.glow(big, dx, dy, 16, (140, 90, 50), 0.8)
    return big


def r_night(t, u):
    """night: Doug snores under the duvet in a shower cap; Biscuit pads to the empty bottle on the carpet and licks it (clue)"""
    v = view_at(BED, 760, 520, 1.18, 180, 480)
    x = lerp(980, 820, sm(u / 0.8))

    def draw(CH, v_):
        L = Layer(v_.wcam()); A.serum(L, (760.0, 606.0), empty=True); F.outline(L, A.OL); CH.add(L)
        dog_at(CH, v_, t, (x, 640.0, 10.0), flip=True, walk=1.0 if u < 0.8 else 0.0, lick=sm((u - 0.85) / 0.2))
    big = bedroom(v, t, draw)
    return big


def r_reveal(t, u):
    """«Ladies and gentlemen. The new DOUG.» — morning, Doug in a beanie at the mirror; he yanks it off: still bald, four hairs"""
    x, y, un = DB
    k = 1.15
    v = view_at(BATH, x - 0.4 * un * k, y - 20 * un * k, 1.25, 180, 330)
    off = u > 2.5

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, expr='proud' if not off else 'shock', pose=A.DPOSE['cheer'] if not off else A.DPOSE['shout'],
                hat=None if off else 'beanie', hairs=4, mouth_=mouth('doug', t) if not off else 0.5)
    return bathroom(v, t, draw, 0.0, 'smug', morning=True)


def r_twist(t, u):
    """TWIST: Biscuit walks in with a glorious flowing mane — slow motion, wind, guitar riff; flash"""
    x = lerp(380, 520, sm(u / 1.6))
    v = view_at(BATH, 560, 690, 1.3, 180, 400)

    def draw(CH, v_):
        dog_at(CH, v_, t, (x, 690.0, 15.0), walk=0.6, mane=1.0, wind=1.2)
    big = bathroom(v, t, draw, 0.0, 'happy', morning=True)
    fx.glow(big, *v.opt(x + 40, 610), 420, (255, 230, 150), 0.25)
    return big


def r_kayden(t, u):
    """«Dad. The dog has better hair than you NOW.» — Kayden in the doorway, flat; the maned dog in front, Doug bald behind"""
    v = view_at(BATH, 600, 640, 0.95, 180, 560)

    def draw(CH, v_):
        doug_at(CH, v_, t, (760.0, 668.0, 12.8), expr='sad', pose=A.DPOSE['stand'], hairs=4, mouth_=0.0)
        char_at(A.kayden, 'kayden', CH, v_, t, (450.0, 668.0, 12.8), expr='flat', pose=A.KPOSE['look'], prop_n=A.phone)
        dog_at(CH, v_, t, (530.0, 700.0, 12.0), mane=1.0, wind=0.6)
    return bathroom(v, t, draw, 0.0, 'happy', morning=True)


def r_tammy(t, u):
    """«Doug, look at him. He looks forty. In a GOOD way.» — Tammy pets the maned dog, delighted"""
    v = view_at(BATH, 600, 640, 1.08, 180, 560)

    def draw(CH, v_):
        dog_at(CH, v_, t, (520.0, 700.0, 12.0), mane=1.0, wind=0.5)
        char_at(A.tammy, 'tammy', CH, v_, t, (660.0, 670.0, 12.6), flip=True, expr='bliss', pose=A.TPOSE['stand'],
                hand_n=F.H(4.6, 8.4), prop_f=A.mug)
    return bathroom(v, t, draw, 0.0, 'happy', morning=True)


def r_hair(t, u):
    """«I've still… GOT it?» — Doug close, unsure; one more hair drifts down from the dome"""
    x, y, un = 760.0, 668.0, 12.8
    k = 1.25
    hy = y - 25.4 * un * k
    v = view_at(BATH, x - 1.2 * un * k, hy, 1.42, 180, 330)

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, expr='sad', pose=A.DPOSE['stand'], hairs=4 if u < 0.9 else 3)
        if u > 0.9:
            kk = (u - 0.9) / 1.2
            hx = x - 0.5 * un * k + 30 * math.sin(kk * 9); hy2 = y - 29.5 * un * k + 260 * kk
            L = Layer(v_.wcam()); F.cap(L, (hx, hy2), (hx + 14, hy2 - 6), 1.2, 1.0, (150, 112, 80)); CH.add(L)
    return bathroom(v, t, draw, 0.0, 'smug', morning=True)


def r_button(t, u):
    """«Recalculating. Dog: plus one thousand. Doug: minus four HUNDRED.» — MIRRA in the mirror; below, the maned dog and bald Doug"""
    v = view_at(BATH, 640, 360, 1.0 + 0.08 * sm(u / 3.5), 180, 300)

    def draw(CH, v_):
        dog_at(CH, v_, t, (520.0, 694.0, 12.0), mane=1.0, wind=0.4)
        doug_at(CH, v_, t, (760.0, 668.0, 12.8), expr='sad', pose=A.DPOSE['stand'], hairs=3, mouth_=0.0)
    return bathroom(v, t, draw, mouth('mirra', t, 2.0), 'smug', morning=True)


SHOT = dict(hook=r_hook, dream=r_dream, label=r_label, pour=r_pour, night=r_night, reveal=r_reveal, twist=r_twist, kayden=r_kayden,
            tammy=r_tammy, hair=r_hair, button=r_button)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 5, ['$200 HAIR?!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('ROCK STAR?', fg=(255, 220, 120), size=80), F0['dream'] + 1.2, F0['label'], 540, 560),
                        (O.sticker('1 DROP', fg=(255, 90, 110), size=90), F0['label'] + 1.0, F0['pour'], 540, 1100),
                        (O.sticker('ZZZ...', fg=(170, 190, 255), size=80), F0['night'] + 0.1, F0['reveal'], 400, 560),
                        (O.sticker('4 LEFT', fg=(255, 90, 110), size=90), F0['reveal'] + 2.7, TL.TWIST, 760, 560),
                        (O.sticker('DOG: +1000', fg=(150, 250, 190), size=72), F0['button'] + 1.7, TL.DUR - 1.0, 540, 780),
                        (O.sticker('DOUG: -400', fg=(255, 90, 110), size=72), F0['button'] + 3.0, TL.DUR - 1.0, 540, 900)],
              flashes=[TL.TWIST + 0.1], mosaics=[F0['night'], F0['reveal']],
              cap_y={'hook': 1420, 'label': 1440, 'night': 1420, 'kayden': 1420, 'tammy': 1420, 'button': 1440}, cap_default=1420)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
