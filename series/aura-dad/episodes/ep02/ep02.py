"""S01E02 «$340 SKINCARE?!» — Lily (11) shows her nine-step routine: $340. Doug marches into SEPHORIA to return it all and «teach her
the value of money». Clerk Skylar: «this card already bought a nine-hundred-dollar eye cream yesterday». TWIST (54 %, «the villain is
one of us»): pull back — Tammy is right behind him in the line with a full basket and gold eye patches: «Mommy ALSO has a nine-step
routine.» Skylar sprays a tester on Doug's hand — «Oh, that's NICE» — «That's ninety dollars.» Button: the whole family in sheet masks,
«I've still GOT it!» — MIRRA: «Skin: plus ten. Wallet: DEAD.»
  python3 ep02.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
              endcard=dict(style='auradad', lang='us', promise='TOMORROW: AURA FARMING'))
talk = EPI.talk
W = K.build(names=['kitchen', 'bathroom', 'sephoria'])
K.decorate(W)
K.decorate_store(W['sephoria'])
KIT, BATH, STORE = W['kitchen'], W['bathroom'], W['sephoria']
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0
COUNTER = K.occluder(STORE, K.S_COUNTER, 'counter')

SKY = (1080.0, 548.0, 9.8)           # Skylar behind the counter, facing left
DST = (840.0, 650.0, 11.0)           # Doug at the counter, facing right
TST = (640.0, 646.0, 11.0)           # Tammy behind him in the line, facing right
RECEIPT = D.plate(34, 12, ['$339.99'], bg=(252, 250, 244), colors=[(226, 46, 70)], border=None, pad=0.8)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def face(v, cam, r, ru=3.2):
    K.logface(v, cam, r['head'], ru)


def u2w(v, cam, pt):
    x, y = cam.p(*pt)
    k = ST.PX[0]
    return v.X0 + x * k / v.Z, v.Y0 + (y * k - v.oy) / v.Z


def walk(t, sp=8.0):
    s_ = math.sin(t * sp)
    return dict(n=(2.8 - 1.6 * s_, 12.4), f=(-2.6 + 1.6 * s_, 12.6), bn=1, bf=-1, nleg=(0.38 * s_, 0.2 * max(0, -s_)),
                fleg=(-0.38 * s_, 0.2 * max(0, s_)))


# ---------------------------------------------------------------- worlds
def kitchen(v, t, draw=None):
    CH, FX = K.begin()
    big = v.bg()
    if draw: draw(CH, v)
    L = Layer(K.fgcam(v, 0.4)); K.fg_plant(L, 1230, 790, 1.15); F.outline(L, A.OL); CH.add(L)       # foreground layer
    CH.comp(big, K.light_kitchen(v))
    fx.motes(FX, v, t, 480, 120, 840, 380, n=22, col=(255, 244, 210), seed=4)
    FX.comp(big)
    B.steam(big, v, t, K.K_MUG[0], K.K_MUG[1] - 14, n=4, rise=60, size=18, a=0.35)
    fx.vignette(big, 0.22)
    return big


def store(v, t, draw=None, counter=True, bags=True, mist=None):
    CH, FX = K.begin()
    big = v.bg()
    B.steam(big, v, t, 776, 230, n=5, rise=70, size=22, a=0.25)                                          # fountain spray behind the glass
    if draw: draw(CH, v)
    CH.comp(big, K.light_store(v))
    if counter: K.draw_occluder(big, v, COUNTER)                                                        # counter in front of Skylar
    CH2, _ = K.begin()
    if bags:
        L = Layer(K.fgcam(v, 0.45)); K.fg_bags(L, 70, 760, 1.25); F.outline(L, A.OL); CH2.add(L)
    if mist: mist(FX, v)
    CH2.comp(big, K.light_store(v))
    fx.motes(FX, v, t, 300, 60, 1100, 300, n=26, col=(255, 220, 240), seed=8)
    FX.comp(big)
    fx.vignette(big, 0.2)
    return big


def bathroom(v, t, draw=None, talk_=0.0, expr='calm'):
    CH, FX = K.begin()
    big = v.bg()
    L = Layer(v.wcam()); K.mirra_glass(L, t, talk_, expr); CH.add(L)
    if draw: draw(CH, v)
    CH.comp(big, K.light_bath(v))
    K.glass_glow(big, v, t)
    fx.motes(FX, v, t, 900, 120, 1240, 380, n=16, col=(255, 250, 230), seed=6)
    FX.comp(big)
    fx.vignette(big, 0.22)
    return big


def doug_at(CH, v, t, pos, k=1.0, flip=False, **kw):
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


def crowd(CH, v, t, xs=(130, 240, 470, 560), y=606.0, un=8.4):
    """the Sephora kids: recoloured Lilys with tumblers, browsing the shelves"""
    for i, x in enumerate(xs):
        cam = v.cam(x + 6 * math.sin(t * 0.8 + i), y + (i % 2) * 14, un, flip=bool(i % 2))
        A.lily(CH, cam, A.LPOSE['cup'] if i % 2 else A.LPOSE['show'], t=t + i, expr='happy' if i % 2 else 'smug',
               pal=A.KID_PALS[i % 3], prop_n=A.tumbler if i % 2 else A.jar, band=i % 3 == 0, patches=i % 2 == 0)


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Daddy, this is my nine-step skincare routine! It only costs three hundred and forty dollars.» — Lily in her bunny headband
    and gold patches holds up a receipt that unrolls to the floor; Doug behind her, screaming; clue: Tammy also wears gold patches and
    a SEPHORIA bag waits on the table"""
    v = view_at(KIT, 820, 650, 0.98 + 0.04 * sm(u / 5.0), 180, 580)
    box = {}

    def draw(CH, v_):
        L = Layer(v_.wcam()); K.fg_bags(L, 1080, 452, 0.45); F.outline(L, A.OL); CH.add(L)                  # bag on the table (clue)
        char_at(A.tammy, 'tammy', CH, v_, t, (990.0, 690.0, 11.2), flip=True, expr='tired', pose=A.TPOSE['mug'], prop_n=A.mug,
                patches=True)
        doug_at(CH, v_, t, (860.0, 660.0, 11.4), flip=True, expr='shock' if u < 1.0 else 'shout', pose=A.DPOSE['shout'],
                mouth_=0.6 + 0.15 * math.sin(t * 7))
        ln = 4.0 + 8.0 * sm((u - 0.3) / 0.9)
        cam, r = char_at(A.lily, 'lily', CH, v_, t, (745.0, 716.0, 16.5), expr='happy', pose=A.LPOSE['show'],
                         prop_n=lambda L, h: A.receipt(L, h, ln, t * 3), prop_f=A.jar, ru=3.0)
        box['h'] = u2w(v_, cam, r['hand_n'])
    big = kitchen(v, t, draw)
    hx, hy = box['h']
    D.blit(big, v, RECEIPT, hx - 14, hy + 4)
    return big


def r_doug_cu(t, u):
    """«Three hundred and FORTY?! You're ELEVEN! Your skin is brand NEW!» — close-up, receipt in his fist, shake"""
    x, y, un = 840.0, 650.0, 11.0
    k = 1.3
    hy = y - 25.4 * un * k
    v = view_at(KIT, x - 1.0 * un * k, hy, 1.4, 180, 330)

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, flip=True, expr='shout', pose=A.DPOSE['shout'], shake=0.03 if u < 1.0 else 0.0,
                prop_n=lambda L, h: A.receipt(L, h, 6.0, t * 4))
    big = kitchen(v, t, draw)
    if u < 0.35: B.shake(big, t, 10, 33)
    return big


def r_march(t, u):
    """«I'm returning ALL of this. And I'm teaching her the value of MONEY.» — Doug marches into SEPHORIA past a crowd of tweens
    with tumblers; the camera travels with him (crossing)"""
    x = lerp(330, 640, sm(u / 3.6))
    v = view_at(STORE, x + 30, 640, 1.0, 180, 580)

    def draw(CH, v_):
        crowd(CH, v_, t)
        doug_at(CH, v_, t, (x, 650.0, 11.0), expr='angry', pose=walk(t), prop_n=lambda L, h: A.receipt(L, h, 3.0, t * 5))
        hx, hy = x + 3.4 * 11.0, 650 - 12.4 * 11.0
        L = Layer(v_.wcam()); K.fg_bags(L, hx + 10, hy + 60, 0.55); F.outline(L, A.OL); CH.add(L)
    return store(v, t, draw, counter=True, bags=False)


def r_counter(t, u):
    """«Sure. But this card already bought a nine-hundred-dollar eye cream YESTERDAY.» — two-shot at the checkout, Skylar bored
    behind the counter (the counter is a foreground layer), Doug's card in the terminal"""
    v = view_at(STORE, 975, 640, 1.0, 180, 580)

    def draw(CH, v_):
        char_at(A.skylar, 'skylar', CH, v_, t, SKY, flip=True, expr='bored', pose=A.SPOSE['lean'], gum=0.0)
        doug_at(CH, v_, t, DST, expr='normal', pose=A.DPOSE['stand'], look=0.3)
    return store(v, t, draw)


def r_twist(t, u):
    """TWIST «Nine HUNDRED?! WHO?!» — close on Doug's scream, then the camera pulls back: Tammy right behind him in the line with a
    basket full of jars and gold eye patches"""
    x, y, un = DST
    k0 = sm((u - 0.9) / 0.5)
    hy = y - 25.4 * un
    cx = lerp(x + 1.0 * un, 860, k0); cy = lerp(hy, 640, k0)
    Z = lerp(1.42, 1.0, k0)
    v = view_at(STORE, cx, cy, Z, 180, lerp(300, 580, k0))

    def draw(CH, v_):
        char_at(A.tammy, 'tammy', CH, v_, t, TST, expr='smirk' if k0 > 0.5 else 'tired', pose=A.TPOSE['stand'],
                prop_n=A.basket, patches=True)
        char_at(A.skylar, 'skylar', CH, v_, t, SKY, flip=True, expr='bored', pose=A.SPOSE['lean'], gum=sm((u - 1.2) / 0.6))
        doug_at(CH, v_, t, DST, expr='shout' if u < 1.6 else 'shock', pose=A.DPOSE['shout'], shake=0.03 * (1 - k0))
    big = store(v, t, draw)
    if 0.9 < u < 1.4: fx.speed_lines(big, t, 0.8)
    return big


def r_tammy(t, u):
    """«Doug. Mommy ALSO has a nine-step routine.» — Tammy medium, calm, lifts the heavy basket; Doug turned to her, jaw on the floor"""
    v = view_at(STORE, 720, 640, 1.2 + 0.03 * sm(u / 3.0), 180, 600)

    def draw(CH, v_):
        char_at(A.tammy, 'tammy', CH, v_, t, TST, expr='smirk', pose=A.TPOSE['stand'], prop_n=A.basket, patches=True, ru=2.8)
        doug_at(CH, v_, t, (830.0, 652.0, 11.0), flip=True, expr='shock', pose=A.DPOSE['stand'], mouth_=0.5)
    return store(v, t, draw, counter=False)


def r_spray(t, u):
    """«Oh. Oh, that's NICE. What is this?» — Skylar sprays a tester on his hand, sparkles, Doug melts"""
    v = view_at(STORE, 985, 600, 1.15, 180, 540)
    hand = F.H(6.2, 17.2)

    def draw(CH, v_):
        char_at(A.skylar, 'skylar', CH, v_, t, SKY, flip=True, expr='smirk', pose=A.SPOSE['spray'], prop_n=A.bottle)
        doug_at(CH, v_, t, DST, expr='happy', pose=A.DPOSE['stand'], hand_n=hand, look=0.0)

    def mist(FX, v_):
        if u < 1.2:
            B.spray(FX, v_, t, (1010, 420), spread=40, drop=40, n=18, col=(240, 220, 255), col2=(220, 240, 255), speed=2.0)
    big = store(v, t, draw, mist=mist)
    hx, hy = v.opt(DST[0] + 6.2 * DST[2], DST[1] - 17.2 * DST[2])
    fx.glow(big, hx, hy, 120, (255, 230, 250), 0.35 * (0.6 + 0.4 * math.sin(t * 9)))
    return big


def r_price(t, u):
    """«That's ninety DOLLARS.» — Skylar close, flat, a pink gum bubble pops"""
    x, y, un = SKY
    k = 1.4
    hy = y - 24.4 * un * k
    v = view_at(STORE, x - 1.0 * un * k, hy, 1.42, 180, 320)

    def draw(CH, v_):
        char_at(A.skylar, 'skylar', CH, v_, t, (x, y, un), k, flip=True, expr='flat', pose=A.SPOSE['lean'],
                gum=sm((u - 1.05) / 0.4) * (1 - sm((u - 1.45) / 0.05)))
    return store(v, t, draw, counter=True, bags=False)


def r_masks(t, u):
    """«I've still GOT it!» — that night: Doug, Lily and Tammy in white sheet masks and bunny headbands at the bathroom mirror"""
    v = view_at(BATH, 650, 400, 0.94 + 0.04 * sm(u / 1.5), 180, 400)

    def draw(CH, v_):
        char_at(A.lily, 'lily', CH, v_, t, (545.0, 676.0, 13.0), expr='proud', pose=A.LPOSE['cup'], prop_n=A.tumbler, mask=True,
                patches=False)
        char_at(A.tammy, 'tammy', CH, v_, t, (768.0, 672.0, 12.6), flip=True, expr='bliss', pose=A.TPOSE['hug'], prop_n=A.mug, mask=True,
                band=True)
        doug_at(CH, v_, t, (640.0, 670.0, 12.8), expr='proud', pose=A.DPOSE['cheer'], mask=True, band=True,
                shine=sm((u - 0.6) / 0.3))
    return bathroom(v, t, draw, 0.0, 'smug')


def r_button(t, u):
    """«Recalculating. Skin: plus ten. Wallet: DEAD.» — push-in on MIRRA, the family in masks below"""
    v = view_at(BATH, 640, 300, 1.1 + 0.1 * sm(u / 3.0), 180, 300)

    def draw(CH, v_):
        char_at(A.lily, 'lily', CH, v_, t, (545.0, 676.0, 13.0), expr='smug', pose=A.LPOSE['cup'], prop_n=A.tumbler, mask=True,
                patches=False)
        char_at(A.tammy, 'tammy', CH, v_, t, (768.0, 672.0, 12.6), flip=True, expr='tired', pose=A.TPOSE['hug'], prop_n=A.mug, mask=True,
                band=True)
        doug_at(CH, v_, t, (640.0, 670.0, 12.8), expr='sad' if u > 2.2 else 'proud', pose=A.DPOSE['stand'], mask=True, band=True,
                mouth_=0.0)
    return bathroom(v, t, draw, mouth('mirra', t, 2.0), 'smug')


SHOT = dict(hook=r_hook, doug_cu=r_doug_cu, march=r_march, counter=r_counter, twist=r_twist, tammy=r_tammy, spray=r_spray,
            price=r_price, masks=r_masks, button=r_button)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 2, ['$340 SKINCARE?!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('$900?!', fg=(255, 90, 110), size=90), F0['counter'] + 2.2, TL.TWIST + 0.9, 760, 560),
                        (O.sticker('MOM?!', fg=(255, 182, 214), size=100), TL.TWIST + 1.0, F0['tammy'], 540, 500),
                        (O.sticker('$90', fg=(255, 90, 110), size=96), F0['price'] + 0.6, F0['masks'], 760, 560),
                        (O.sticker('SKIN +10', fg=(150, 250, 190), size=70), F0['button'] + 1.2, TL.DUR - 1.0, 540, 760),
                        (O.sticker('WALLET: DEAD', fg=(255, 90, 110), size=64), F0['button'] + 2.2, TL.DUR - 1.0, 540, 880)],
              flashes=[TL.TWIST + 0.92], mosaics=[F0['march'], F0['masks']],
              cap_y={'hook': 1060, 'doug_cu': 1400, 'march': 1420, 'counter': 1420, 'twist': 1420, 'tammy': 1420, 'spray': 1420,
                     'price': 1420, 'masks': 1430, 'button': 1440}, cap_default=1400)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
