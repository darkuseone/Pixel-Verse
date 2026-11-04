"""S01E04 «HE MOGGED ME?!» — at the mailboxes the neighbour Brett (a fridge with a tiny head and a brick jaw) towers over Doug. Kayden:
«Brett just mogged you — he looks better than you just by standing next to you.» Doug: «In MY cul-de-sac? Not TODAY.» A box arrives:
«HEIGHT INSOLES +4 IN»; Doug wobbles back on them: «Nice weather up HERE.» — Brett: «You look TALLER.» TWIST (51 %, «the hunter asks
for help»): Brett steps back, twists his ankle and falls — «+6 IN» insoles fly out of his sneakers (the empty «+6 IN» box sat on his
porch since the first shot); sitting on the grass he is tiny: «Doug, buddy. Help me up. Please don't tell ANYONE.» Doug offers a
hand and falls off his own insoles. Tammy from the porch: «So you're BOTH five foot six. Great. Come eat.» Doug on the ground: «I've
still GOT it!» — the doorbell MIRRA: «Height: recalculating. Still five foot SIX.»
  python3 ep04.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
              endcard=dict(style='auradad', lang='us', promise='TOMORROW: THE $200 HAIR SERUM'))
talk = EPI.talk
W = K.build(names=['kitchen', 'bathroom', 'culdesac'])
K.decorate(W)
K.decorate_cul(W['culdesac'])
CUL = W['culdesac']
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0

UN = 8.6
DX, BX, FY = 560.0, 735.0, 590.0      # Doug left of the mailboxes, Brett right of them, feet line
KX = 420.0
BOX = D.plate(36, 22, ['HEIGHT', 'INSOLES +4'], bg=(200, 160, 110), colors=[(30, 22, 40), (226, 46, 70)], border=(120, 90, 60),
              pad=1.0)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def face(v, cam, r, ru=3.2):
    K.logface(v, cam, r['head'], ru)


def cul(v, t, draw=None, after=None):
    CH, FX = K.begin()
    big = v.bg()
    if draw: draw(CH, v)
    L = Layer(K.fgcam(v, 0.5)); K.fg_plant(L, 70, 800, 1.3, pot=(190, 90, 60)); F.outline(L, A.OL); CH.add(L)
    CH.comp(big, K.light_cul(v))
    fx.motes(FX, v, t, 200, 200, 1200, 500, n=16, col=(255, 250, 230), seed=12)
    if after: after(FX, v)
    FX.comp(big)
    fx.vignette(big, 0.2)
    return big


def lifts(CH, v, x, y, un, lift, flip=False):
    """thick foam insoles visible under Doug's sneakers"""
    if lift <= 0: return
    L = Layer(v.wcam())
    for dx in (-0.6, 0.9):
        xx = x + (dx if not flip else -dx) * un + (0.9 * un if not flip else -0.9 * un)
        ST.wrect(L, xx - 1.9 * un, y - lift * un, xx + 1.9 * un, y, (255, 226, 180))
        ST.wrect(L, xx - 1.9 * un, y - lift * un * 0.55, xx + 1.9 * un, y - lift * un * 0.45, (255, 170, 130))
    F.outline(L, A.OL); CH.add(L)


def doug_at(CH, v, t, pos, k=1.0, flip=False, lift=0.0, sit=False, **kw):
    x, y, un = pos
    un = un * k
    yy = y - lift * un + (10.0 * un if sit else 0.0)
    cam = v.cam(x, yy, un, flip=flip)
    kw.setdefault('expr', 'normal')
    if 'mouth_' not in kw: kw['mouth_'] = mouth('doug', t)
    pose = A.DPOSE['sit'] if sit else kw.pop('pose', None)
    kw.pop('pose', None)
    r = A.doug(CH, cam, t=t, pose=pose, **kw)
    face(v, cam, r, 3.4)
    lifts(CH, v, x, y, un, lift, flip)
    return cam, r


def brett_at(CH, v, t, pos, k=1.0, flip=True, sit=False, **kw):
    x, y, un = pos
    un = un * k
    yy = y + (6.0 * un if sit else 0.0)
    cam = v.cam(x, yy, un, flip=flip)
    if sit: kw['pose'] = A.BPOSE['sit']; kw['lift'] = 0.0
    r = A.brett(CH, cam, t=t, mouth_=mouth('brett', t), **kw)
    face(v, cam, r, 2.6)
    return cam, r


def kay_at(CH, v, t, pos, k=1.0, flip=False, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    kw.setdefault('expr', 'bored')
    r = A.kayden(CH, cam, t=t, mouth_=mouth('kayden', t), **kw)
    face(v, cam, r, 2.8)
    return cam, r


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Dad, Brett just mogged you…» — at the mailboxes huge Brett (on hidden +6 insoles) flexes; Doug looks UP at his jaw; Kayden
    explains; clue: the empty «+6 IN LIFTS» box on Brett's porch"""
    v = view_at(CUL, 600, 590, 1.0 + 0.04 * sm(u / 5.0), 180, 580)

    def draw(CH, v_):
        kay_at(CH, v_, t, (KX + 20, FY + 6, UN), pose=A.KPOSE['stand'], expr='flat', look=0.3)
        brett_at(CH, v_, t, (BX, FY, UN), expr='smug', pose=A.BPOSE['flex'], lift=6.0)
        doug_at(CH, v_, t, (DX, FY, UN), expr='shock', pose=A.DPOSE['stand'], look=0.0, mouth_=0.4)
    return cul(v, t, draw)


def r_offended(t, u):
    """«Mogged? In MY cul-de-sac? Not TODAY.» — Doug close, offended, cheeks red"""
    k = 1.7
    hy = FY - 25.4 * UN * k
    v = view_at(CUL, DX + 1.0 * UN * k, hy, 1.4, 180, 330)

    def draw(CH, v_):
        doug_at(CH, v_, t, (DX, FY, UN), k, expr='angry', pose=A.DPOSE['hips'])
    return cul(v, t, draw)


def r_box(t, u):
    """a delivery box «HEIGHT INSOLES +4» lands at the door; Doug rips it open, holds the insoles up — twinkle"""
    v = view_at(CUL, 250, 300, 1.25, 180, 300)

    def draw(CH, v_):
        doug_at(CH, v_, t, (260.0, 420.0, 9.6), expr='smug' if u > 0.6 else 'normal', pose=A.DPOSE['cheer'] if u > 0.6 else A.DPOSE['stand'],
                mouth_=0.0, shine=sm((u - 1.1) / 0.3))
        if u > 0.6:
            for dx in (-30, 30):
                L = Layer(v_.wcam()); A.insole(L, 260 + dx * 1.2, 420 - 300 + 8 * math.sin(t * 6), 1.3); F.outline(L, A.OL); CH.add(L)
    big = cul(v, t, draw)
    D.blit(big, v, BOX, 300 - 18 * (1 - sm(u / 0.2)) * 0, 380 - 140 * (1 - sm(u / 0.25)))
    return big


def r_wobble(t, u):
    """«Good morning, Brett. Nice weather up HERE.» — Doug wobbles back on the tall insoles; now as tall as Brett"""
    x = lerp(DX - 120, DX, sm(u / 1.6))
    v = view_at(CUL, 640, 580, 1.15, 180, 560)

    def draw(CH, v_):
        brett_at(CH, v_, t, (BX, FY, UN), expr='friendly', pose=A.BPOSE['stand'], lift=6.0)
        doug_at(CH, v_, t, (x, FY, UN), expr='smug', pose=A.DPOSE['hips'], lift=5.0, lean=0.5 * math.sin(t * 7), look=0.2)
    return cul(v, t, draw)


def r_brett(t, u):
    """«Morning, Doug. You look TALLER.» — Brett, suspicious, eyes down at Doug's shoes"""
    k = 1.55
    hy = FY - (6.0 + 7.4 + 17.6) * UN * k
    v = view_at(CUL, BX - 0.8 * UN * k, hy + 30, 1.38, 180, 330)

    def draw(CH, v_):
        doug_at(CH, v_, t, (DX + 40, FY, UN), k, expr='smug', pose=A.DPOSE['hips'], lift=5.0, mouth_=0.0)
        brett_at(CH, v_, t, (BX, FY, UN), k, expr='smug', pose=A.BPOSE['stand'], lift=6.0, look=0.4)
    return cul(v, t, draw)


def r_twist(t, u):
    """TWIST: Brett steps back, twists the ankle, crashes down — «+6 IN» insoles fly out of his sneakers; sitting on the sidewalk he
    is tiny (flash, sticker)"""
    v = view_at(CUL, 650, 580, 1.15, 180, 560)
    fall = sm((u - 0.2) / 0.3)

    def draw(CH, v_):
        doug_at(CH, v_, t, (DX, FY, UN), expr='shock', pose=A.DPOSE['stand'], lift=5.0, mouth_=0.5)
        if fall < 0.98:
            brett_at(CH, v_, t, (BX + 20 * fall, FY + 30 * fall, UN), expr='shock', pose=A.BPOSE['fall'] if fall > 0.05 else A.BPOSE['stand'],
                     lift=6.0 * (1 - fall), lean=-1.5 * fall)
        else:
            brett_at(CH, v_, t, (BX + 20, FY, UN), sit=True, expr='scared')
        if u > 0.45:
            for i, dx in enumerate((-60, 70)):
                k = sm((u - 0.45) / 0.8)
                ix = BX + dx * k * 2; iy = FY - 60 - 260 * math.sin(math.pi * min(1.0, k)) + 40 * k
                L = Layer(v_.wcam()); A.insole(L, ix, iy, 1.2); F.outline(L, A.OL); CH.add(L)
    big = cul(v, t, draw)
    if 0.45 < u < 0.8: B.shake(big, t, 12, 33)
    return big


def r_tiny(t, u):
    """«Doug, buddy. Help me up. Please don't tell ANYONE.» — Brett sitting on the sidewalk, small, whispering; Doug above on lifts"""
    v = view_at(CUL, 690, 560, 1.3, 180, 540)

    def draw(CH, v_):
        doug_at(CH, v_, t, (DX + 30, FY, UN), expr='smug', pose=A.DPOSE['hips'], lift=5.0, mouth_=0.0, look=0.3)
        brett_at(CH, v_, t, (BX + 20, FY, UN), sit=True, expr='whisper')
        L = Layer(v_.wcam())
        for dx in (-70, 110): A.insole(L, BX + dx, FY + 4, 1.2)
        F.outline(L, A.OL); CH.add(L)
    return cul(v, t, draw)


def r_help(t, u):
    """Doug proudly offers a hand — and topples off his own insoles; both sit on the sidewalk, the same height"""
    v = view_at(CUL, 660, 570, 1.2, 180, 550)
    fall = sm((u - 0.55) / 0.3)

    def draw(CH, v_):
        brett_at(CH, v_, t, (BX + 20, FY, UN), sit=True, expr='scared')
        if fall < 0.98:
            doug_at(CH, v_, t, (DX + 30, FY + 40 * fall, UN), expr='proud' if fall < 0.1 else 'shock', pose=A.DPOSE['reach'],
                    lift=5.0 * (1 - fall), lean=1.6 * fall)
        else:
            doug_at(CH, v_, t, (DX + 30, FY, UN), sit=True, expr='shock', mouth_=0.4)
    big = cul(v, t, draw)
    if 0.8 < u < 1.0: B.shake(big, t, 10, 33)
    return big


def r_tammy(t, u):
    """«So you're BOTH five foot six. Great. Come eat.» — Tammy at the front door with her mug, unimpressed"""
    x, y = K.C_DOOR_P
    v = view_at(CUL, x + 30, y - 120, 1.42, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(x, y + 18, 10.6, flip=False)
        r = A.tammy(CH, cam, A.TPOSE['mug'], t=t, mouth_=mouth('tammy', t), expr='tired', prop_n=A.mug)
        face(v_, cam, r, 2.6)
    return cul(v, t, draw)


def r_ground(t, u):
    """«I've still GOT it!» — Doug and Brett sitting side by side on the sidewalk; Doug proud, dome twinkles"""
    v = view_at(CUL, 650, 560, 1.38, 180, 520)

    def draw(CH, v_):
        brett_at(CH, v_, t, (BX + 20, FY, UN), sit=True, expr='scared')
        doug_at(CH, v_, t, (DX + 30, FY, UN), sit=True, expr='proud', shine=sm((u - 0.8) / 0.3))
    return cul(v, t, draw)


def r_button(t, u):
    """«Height: recalculating. Still five foot SIX.» — the smart doorbell shows MIRRA; plate «HEIGHT 5'6»"""
    x0, y0, x1, y1 = K.C_BELL
    v = view_at(CUL, (x0 + x1) / 2, (y0 + y1) / 2, 1.45, 180, 280)

    def draw(CH, v_):
        L = Layer(v_.wcam()); K.mirra_panel(L, K.C_BELL, t, mouth('mirra', t, 2.0), 'smug'); CH.add(L)
    return cul(v, t, draw)


SHOT = dict(hook=r_hook, offended=r_offended, box=r_box, wobble=r_wobble, brett=r_brett, twist=r_twist, tiny=r_tiny, help=r_help,
            tammy=r_tammy, ground=r_ground, button=r_button)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 4, ['HE MOGGED ME?!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('+4 IN', fg=(255, 220, 120), size=96), F0['box'] + 0.7, F0['wobble'], 760, 1180),
                        (O.sticker('+6 IN?!', fg=(255, 90, 110), size=100), TL.TWIST + 0.6, F0['tiny'] + 1.0, 540, 560),
                        (O.sticker("5'6\"", fg=(150, 250, 190), size=100), F0['button'] + 1.0, TL.DUR - 1.0, 540, 1180)],
              flashes=[TL.TWIST + 0.5], mosaics=[F0['box'], F0['tammy']],
              cap_y={'hook': 1420, 'offended': 1420, 'wobble': 1420, 'brett': 1420, 'tiny': 1420, 'tammy': 1440, 'ground': 1420,
                     'button': 1440}, cap_default=1420)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
