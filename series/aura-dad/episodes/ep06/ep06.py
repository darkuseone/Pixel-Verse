"""S01E06 «AURA BATTLE?!» (season finale) — block party in the cul-de-sac: Doug vs Brett, a ring of kids voting with their phones.
«I've trained for this my whole life. Five DAYS.» Brett flexes: +300; Doug's shades: −50. Doug remembers E01, presses his tongue up
and goes silent — Brett gets nervous and babbles; the phones: DOUG +1000. «Dad, you WON!» TWIST (57 %, «the reward is the same
problem»): the prize — a lifetime subscription to AURA SCAN PRO, $9.99/week forever. Tammy: «So now we PAY every week to hear you're
minus four hundred.» Doug: «HA! I've still GOT it!» — Kayden, exactly as in E01: «Dad, my aura app just scanned you. Minus four
HUNDRED.» (season loop); a minivan rolls in: «GRANDPA IS HERE FOR XMAS» -> SEASON 2: GRANDPA MAXXING.
  python3 ep06.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
              endcard=dict(style='auradad', lang='us', promise='SEASON 2: GRANDPA MAXXING'))
talk = EPI.talk
W = K.build(names=['kitchen', 'bathroom', 'culdesac'])
K.decorate(W)
K.decorate_cul(W['culdesac'])
CUL = W['culdesac']
D.attach(CUL, [
    (D.plate(200, 30, ['SAGUARO SHADOWS', 'BLOCK PARTY!'], bg=(255, 182, 214), colors=[(44, 18, 70), (226, 46, 70)], border=(44, 18, 70),
             bw=1.5, pad=1.5), 540, 220),
    (D.plate(60, 30, ['AURA', 'BATTLE', 'TODAY 4PM'], bg=(255, 255, 255), colors=[(110, 60, 200), (110, 60, 200), (30, 22, 40)],
             border=(110, 60, 200), weights=[1, 1, 0.6], pad=1.2, tilt=-4), 300, 420),
    (D.plate(46, 20, ['FREE', 'HOT DOGS'], bg=(255, 214, 60), colors=[(30, 22, 40), (226, 46, 70)], border=(30, 22, 40), pad=1.0, tilt=3),
     480, 440),
])
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0

UN = 8.8
DX, BX, FY = 540.0, 760.0, 600.0
VAN = D.plate(88, 22, ['GRANDPA IS HERE', 'FOR XMAS!'], bg=(255, 255, 255), colors=[(200, 30, 40), (40, 140, 70)], border=(200, 30, 40),
              pad=1.0)
PRIZE = D.plate(84, 46, ['LIFETIME', 'AURA SCAN PRO', '$9.99/WK', 'FOREVER'], bg=(255, 250, 230),
                colors=[(110, 60, 200), (30, 22, 40), (226, 46, 70), (226, 46, 70)], border=(214, 170, 60), bw=2.0,
                weights=[0.8, 1, 0.8, 0.8], pad=2.0)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def face(v, cam, r, ru=3.2):
    K.logface(v, cam, r['head'], ru)


def balloons(FX, v, t):
    for i, (x, y, col) in enumerate([(530, 200, (255, 120, 170)), (560, 190, (120, 230, 240)), (730, 196, (150, 250, 190)),
                                     (760, 186, (214, 186, 255))]):
        L = Layer(v.wcam())
        yy = y + 4 * math.sin(t * 2 + i)
        F.cap(L, (x, yy + 14), (x + 2 * math.sin(t + i), yy + 44), 0.6, 0.6, (240, 240, 240))
        F.ell(L, (x, yy), 12, 15, col, 0, (255, 255, 255), None)
        F.outline(L, A.OL); FX.add(L)


def cul(v, t, draw=None, van=False):
    CH, FX = K.begin()
    big = v.bg()
    if draw: draw(CH, v)
    L = Layer(K.fgcam(v, 0.5)); K.fg_plant(L, 70, 800, 1.3, pot=(190, 90, 60)); F.outline(L, A.OL); CH.add(L)
    CH.comp(big, K.light_cul(v))
    balloons(FX, v, t)
    fx.motes(FX, v, t, 200, 150, 1200, 500, n=30, col=(255, 220, 240), seed=14)
    FX.comp(big)
    if van: D.blit(big, v, VAN, 905, 352)
    fx.vignette(big, 0.2)
    return big


def doug_at(CH, v, t, pos, k=1.0, flip=False, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    kw.setdefault('expr', 'normal')
    if 'mouth_' not in kw: kw['mouth_'] = mouth('doug', t)
    r = A.doug(CH, cam, t=t, **kw)
    face(v, cam, r, 3.4)
    return cam, r


def brett_at(CH, v, t, pos, k=1.0, flip=True, babble=False, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    m = (0.5 + 0.5 * math.sin(t * 23)) * 0.8 if babble else mouth('brett', t)
    r = A.brett(CH, cam, t=t, mouth_=m, **kw)
    face(v, cam, r, 2.6)
    return cam, r


def kid_at(fn, who, CH, v, t, pos, flip=False, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un, flip=flip)
    r = fn(CH, cam, t=t, mouth_=mouth(who, t) if who else 0.0, **kw)
    face(v, cam, r, 2.6)
    return cam, r


def ring(CH, v, t, front=True, expr='bored'):
    """the kids around the battle, phones up (back row by the mailboxes, front row closer and bigger)"""
    back = [(470.0, 584.0, 7.2, False, 'k', 0), (500.0, 592.0, 6.4, False, 'l', 1), (830.0, 586.0, 6.6, True, 'l', 2),
            (860.0, 594.0, 7.2, True, 'k', 1), (420.0, 704.0, 9.4, False, 'l', 0), (890.0, 706.0, 10.4, True, 'k', 0)]
    for i, (x, y, un, fl, kind, p) in enumerate(back):
        if kind == 'k':
            kid_at(A.kayden, None, CH, v, t + i, (x, y, un), fl, expr=expr, pose=A.KPOSE['phone'], prop_n=A.phone, pal=A.FRIEND_PALS[p % 2])
        else:
            kid_at(A.lily, None, CH, v, t + i, (x, y, un), fl, expr='smug', pose=A.LPOSE['show'], prop_n=A.phone, pal=A.KID_PALS[p])


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Dad, it's the block party. You and Brett are in an aura battle…» — Doug and Brett face to face, kids with phones around,
    Kayden the referee in front"""
    v = view_at(CUL, 650, 600, 0.9 + 0.04 * sm(u / 4.5), 180, 560)

    def draw(CH, v_):
        ring(CH, v_, t)
        brett_at(CH, v_, t, (BX, FY, UN), expr='smug', pose=A.BPOSE['stand'], lift=0.0)
        doug_at(CH, v_, t, (DX, FY, UN), expr='angry', pose=A.DPOSE['hips'], mouth_=0.0)
        kid_at(A.kayden, 'kayden', CH, v_, t, (560.0, 700.0, 10.4), expr='flat', pose=A.KPOSE['phone'], prop_n=A.phone)
    return cul(v, t, draw)


def r_vow(t, u):
    """«Son, I've trained for this my whole life. Five DAYS.» — Doug close, heroic, shades slide down, dome twinkle"""
    k = 1.7
    hy = FY - 25.4 * UN * k
    v = view_at(CUL, DX + 1.0 * UN * k, hy, 1.4, 180, 330)

    def draw(CH, v_):
        doug_at(CH, v_, t, (DX, FY, UN), k, expr='smug', pose=A.DPOSE['point'], shine=sm((u - 1.4) / 0.3) * (1 - sm((u - 2.2) / 0.3)))
    return cul(v, t, draw)


def r_flex(t, u):
    """«Let's GO! Round one!» — Brett double-biceps flex, kids gasp"""
    k = 1.25
    v = view_at(CUL, BX - 20, FY - 120, 1.3, 180, 330)

    def draw(CH, v_):
        brett_at(CH, v_, t, (BX, FY, UN), k, expr='smug', pose=A.BPOSE['flex'] if u > 0.3 else A.BPOSE['stand'])
    big = cul(v, t, draw)
    if 0.3 < u < 0.7: B.shake(big, t, 8, 30)
    return big


def r_score(t, u):
    """«Brett, plus three HUNDRED! Doug, minus FIFTY!» — Jaxon referees with his phone; the phone scores pop up"""
    v = view_at(CUL, 620, 600, 1.15, 180, 560)

    def draw(CH, v_):
        brett_at(CH, v_, t, (BX, FY, UN), expr='smug', pose=A.BPOSE['flex'])
        doug_at(CH, v_, t, (DX, FY, UN), expr='sad' if u > 2.2 else 'smug', pose=A.DPOSE['point'], mouth_=0.0)
        kid_at(A.kayden, 'jaxon', CH, v_, t, (420.0, 690.0, 10.6), expr='smirk', pose=A.KPOSE['phone'], prop_n=A.phone, pal=A.FRIEND_PALS[0])
    return cul(v, t, draw)


def r_mew(t, u):
    """Doug remembers E01: tongue up, cheeks puffed, silent; Brett starts babbling nervously; every phone flips to DOUG +1000"""
    v = view_at(CUL, 650, 600, 0.95, 180, 560)
    puff = sm(u / 0.3)

    def draw(CH, v_):
        ring(CH, v_, t, expr='shock' if u > 1.0 else 'bored')
        brett_at(CH, v_, t, (BX, FY, UN), expr='scared', pose=A.BPOSE['stand'], babble=u > 0.4)
        doug_at(CH, v_, t, (DX, FY, UN), expr='mew' if puff > 0.4 else 'smug', pose=A.DPOSE['fists'], mouth_=0.0)
    return cul(v, t, draw)


def r_win(t, u):
    """«Dad, you WON! Best aura on the BLOCK!» — Kayden shocked with the phone «+1000», Doug triumphant with puffed cheeks"""
    v = view_at(CUL, 600, 620, 1.2, 180, 580)

    def draw(CH, v_):
        doug_at(CH, v_, t, (DX + 30, FY, UN), expr='mew', pose=A.DPOSE['cheer'], mouth_=0.0, bob=0.15)
        kid_at(A.kayden, 'kayden', CH, v_, t, (440.0, 690.0, 10.6), expr='shock', pose=A.KPOSE['shock'], prop_n=A.phone)
    big = cul(v, t, draw)
    if u < 1.2:
        ui = O._scale(K.phone_ui(1000, t, 'score'), 0.5)
        O.overlay(big, ui, 60, 980, 1.0)
        ST.log('sticker', bbox=(60, 980, 60 + ui.shape[1], 980 + ui.shape[0]))
    return big


def r_prize(t, u):
    """TWIST «Congrats, Doug. Your prize: a lifetime subscription to Aura Scan PRO.» — Brett hands over a giant certificate:
    «$9.99/WK FOREVER»; Doug's smile freezes"""
    v = view_at(CUL, 650, 560, 1.22, 180, 520)
    box = {}

    def draw(CH, v_):
        cam, r = brett_at(CH, v_, t, (BX, FY, UN), expr='friendly', pose=A.BPOSE['stand'], hand_n=F.H(6.6, 13.0))
        doug_at(CH, v_, t, (DX, FY, UN), expr='proud' if u < 3.0 else 'shock', pose=A.DPOSE['reach'], mouth_=mouth('doug', t))
        box['h'] = cam.p(*r['hand_n'])
    big = cul(v, t, draw)
    if u > 2.4:
        k = sm((u - 2.4) / 0.25)
        hx, hy = box['h']
        D.blit(big, v, PRIZE, v.X0 + hx * ST.PX[0] / v.Z - 84 * k, v.Y0 + hy * ST.PX[0] / v.Z - 52)
    return big


def r_tammy(t, u):
    """«So now we PAY every week to hear you're minus four hundred.» — Tammy with her mug, the card terminal beeps on her phone"""
    v = view_at(CUL, 320, 560, 1.32, 180, 520)

    def draw(CH, v_):
        cam = v_.cam(320.0, 610.0, 10.0, flip=False)
        r = A.tammy(CH, cam, A.TPOSE['mug'], t=t, mouth_=mouth('tammy', t), expr='tired', prop_n=A.mug, prop_f=A.phone)
        face(v_, cam, r, 2.6)
    return cul(v, t, draw)


def r_proud(t, u):
    """«HA! I've still GOT it!» — Doug close with the certificate, fists up, twinkle"""
    k = 1.55
    hy = FY - 25.4 * UN * k
    v = view_at(CUL, DX + 0.8 * UN * k, hy + 30, 1.38, 180, 330)

    def draw(CH, v_):
        doug_at(CH, v_, t, (DX, FY, UN), k, expr='proud', pose=A.DPOSE['cheer'], shine=sm((u - 0.8) / 0.3))
    return cul(v, t, draw)


def r_loop(t, u):
    """«Dad, my aura app just scanned you. Minus four HUNDRED.» — exactly the E01 hook: Kayden's phone «-400» at Doug; behind them a
    minivan rolls in: «GRANDPA IS HERE FOR XMAS!» (season hook)"""
    v = view_at(CUL, 850, 600, 0.9, 180, 560)

    def draw(CH, v_):
        doug_at(CH, v_, t, (790.0, FY, UN), expr='shock', pose=A.DPOSE['stand'], mouth_=0.55 + 0.1 * math.sin(t * 9))
        kid_at(A.kayden, 'kayden', CH, v_, t, (905.0, 690.0, 10.6), flip=True, expr='bored', pose=A.KPOSE['phone'], prop_n=A.phone)
    big = cul(v, t, draw, van=u > 0.6)
    ui = O._scale(K.phone_ui(-400 if u > 0.8 else 0, t, 'score' if u > 0.8 else 'scan'), 0.5)
    O.overlay(big, ui, 30, 1040, 1.0)
    ST.log('sticker', bbox=(30, 1040, 30 + ui.shape[1], 1040 + ui.shape[0]))
    return big


SHOT = dict(hook=r_hook, vow=r_vow, flex=r_flex, score=r_score, mew=r_mew, win=r_win, prize=r_prize, tammy=r_tammy, proud=r_proud,
            loop=r_loop)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 6, ['AURA BATTLE?!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('BRETT +300', fg=(255, 160, 80), size=70), F0['score'] + 0.5, F0['mew'], 540, 520),
                        (O.sticker('DOUG -50', fg=(255, 90, 110), size=70), F0['score'] + 2.1, F0['mew'], 540, 640),
                        (O.sticker('DOUG +1000', fg=(150, 250, 190), size=84), F0['mew'] + 1.0, F0['win'] + 1.0, 540, 560),
                        (O.sticker('$9.99/WK?!', fg=(255, 90, 110), size=90), TL.TWIST + 3.0, F0['tammy'] + 1.5, 540, 560),
                        (O.sticker('-400', fg=(255, 90, 110), size=96), F0['loop'] + 2.4, TL.DUR - 1.0, 540, 600)],
              flashes=[TL.TWIST + 2.4], mosaics=[F0['vow'], F0['tammy']],
              cap_y={'hook': 1460, 'win': 1420, 'loop': 960, 'tammy': 1440}, cap_default=1420)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
