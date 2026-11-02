"""E06 «Тёща уезжает!» (season finale, day 365) — the tenants moved out, the mother-in-law goes home. Tolik dances, takes back his
armchair and the remote: «Я в этом доме мужик!» — echo, silence. Three days later: dirty dishes, stuck dumplings; he phones her: «А может,
вернётесь? На недельку?» TWIST (the reward is the same problem): a jackhammer, a hole in the wall carpet, Raisa's face: «Толечка, а я
соседнюю квартиру купила! Сейчас дверь сделаем!» Pusya climbs through straight into the armchair: «Кресло опять моё.» Sveta: «Толя, это
же мама!» Tolik, crying: «Навсегда?!»  End card: «ПОДПИШИСЬ! СЕЗОН 2: ТЁЩА НА ДАЧЕ».
  python3 ep06.py test 1 5 20 | frames t… | all | shots <i>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import stage as ST
from stage import view_at, Light
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import decals as D
from props import rusigns as R
from props import teshcast as T
from props import teshkit as K
from props import teshshots as SH
from props.teshshots import mouth, u2w, face
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=dict(K.COL, tolik_echo=K.COL['tolik']), slug=TL.SLUG, promo='ru',
              endcard=dict(style='teshcha', lang='ru', promise='СЕЗОН 2: ТЁЩА НА ДАЧЕ'))
SH.init(EPI, day=365)
HALL = SH.world('hallway')
KIT = SH.world('kitchen')
ROOM = SH.ROOM
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0
RED = (184, 30, 40)
YEL = (255, 244, 170)
HOLE = (575.0, 285.0)
CS = 0.85                          # armchair scale
SEAT = SH.CHAIR[1] - 64 * CS


def _p(lines, w, h, bg=(250, 248, 240), fg=(34, 28, 30), border=(120, 110, 100), tilt=0, stripe=None, weights=None):
    kw = dict(bg=bg, colors=[fg] * len(lines), border=border, pad=1.0, tilt=tilt)
    if stripe: kw['stripe'] = stripe
    if weights: kw['weights'] = weights
    return R.plate(w, h, lines, **kw)


D.attach(HALL, [
    (_p(['ДЕНЬ', '365'], 30, 38, fg=RED, stripe=((200, 40, 40), 0.3), weights=[0.55, 1]), 640, 170),
    (_p(['КВАРТИРАНТЫ', 'СЪЕХАЛИ!'], 56, 26, bg=YEL, fg=RED, border=(150, 130, 70), tilt=-4), 1092, 300),
    (_p(['ТАПКИ ТОЛИКА'], 58, 12, bg=(236, 206, 120), border=(120, 84, 30)), 790, 508),
])
D.attach(KIT, [
    (_p(['ПОМЫТЬ', 'ПОСУДУ (ПОТОМ)'], 56, 24, bg=YEL, fg=RED, border=(150, 130, 70), tilt=3), 186, 232),
    (_p(['ДЕНЬ 368'], 40, 14, bg=(250, 248, 240), fg=RED), 70, 90),
])
TAG = _p(['РАЯ.', 'НЕ КАНТОВАТЬ!'], 40, 20, bg=(236, 206, 120), fg=(60, 30, 20), border=(120, 84, 30))
PELM = _p(['ПЕЛЬМЕНИ', '«ЛЕНИВЫЕ»'], 46, 22, bg=(240, 246, 255), fg=(40, 60, 150), border=(40, 60, 150))


def light_hall(v):
    lx, ly = v.opt(610.0, 80.0)
    return Light(amb=(1.02, 0.96, 0.88), keys=[(lx, ly, 1200, (255, 210, 140), 0.55)], rim=(-1, -0.4, (255, 220, 170), 0.3), grad=(1.04, 0.9))


def light_kitchen(v):
    wx, wy = v.opt(620.0, 120.0)
    return Light(amb=(1.03, 0.98, 0.9), keys=[(wx, wy, 1300, (255, 220, 160), 0.6)], rim=(1, -0.4, (255, 230, 180), 0.35), grad=(1.04, 0.9))


def hall(v, t, draw=None, after=None):
    return SH.generic(HALL, v, t, draw, light=light_hall(v), motes=(450, 60, 800, 300), after=after)


def tolik(CH, v, t, x, y, un, flip=False, pose='stand', expr='normal', m=None, **kw):
    cam = v.cam(x, y, un, flip=flip)
    pp = T.TPOSE[pose] if isinstance(pose, str) else pose
    r = T.tolik(CH, cam, pp, t=t, mouth_=mouth('tolik', t) if m is None else m, expr=expr, **kw)
    face(v, cam, r)
    return cam, r


def raisa(CH, v, t, x, y, un, pose='stand', expr='sweet', flip=False, **kw):
    cam = v.cam(x, y, un, flip=flip)
    pp = T.RPOSE[pose] if isinstance(pose, str) else pose
    r = T.raisa(CH, cam, pp, t=t, mouth_=mouth('raisa', t), expr=expr, **kw)
    face(v, cam, r, 3.6)
    return cam, r


SITC = dict(T.TPOSE['sit'], nleg=(1.45, -0.3), fleg=(1.35, -0.25))


def tolik_chair(CH, v, t, un=13.0, expr='smug', pose=None, **kw):
    SH.chair(CH, v, CS, 'back')
    cam = v.cam(SH.CHAIR[0] - 4, SEAT + 13.6 * un, un)
    r = T.tolik(CH, cam, pose or SITC, t=t, mouth_=kw.pop('m', mouth('tolik', t) + mouth('tolik_echo', t)), expr=expr, **kw)
    face(v, cam, r)
    SH.chair(CH, v, CS, 'front')
    return cam, r


def mess(L):
    """three days without her: socks, an empty dumplings pack, a crumpled shirt"""
    F.ell(L, (430, 668), 22, 7, (236, 236, 240), 0.3); F.cap(L, (420, 664), (452, 672), 4, 4, (200, 200, 206))     # sock
    F.ell(L, (780, 676), 20, 6, (60, 60, 70)); F.cap(L, (772, 672), (800, 680), 4, 4, (50, 50, 60))                # sock
    F.poly(L, [(860, 690), (930, 680), (940, 700), (870, 710)], (220, 230, 250))                                       # dumplings pack
    F.poly(L, [(330, 690), (380, 678), (400, 700), (350, 712)], (220, 220, 240))                                       # shirt
    F.outline(L, T.OL)


class Grab:
    """collects the layers a rig adds, so they can be clipped (Raisa seen only through the hole)"""
    def __init__(s): s.L = []
    def add(s, L): s.L.append(L)


def hole_pts(k, t):
    cx, cy = HOLE
    pts = []
    for i in range(18):
        a = i / 18 * 6.283
        jag = 1.0 + 0.18 * math.sin(i * 2.7 + 1.3) + 0.1 * math.sin(i * 5.1)
        pts.append((cx + math.cos(a) * 64 * k * jag, cy + math.sin(a) * 78 * k * jag))
    return pts


def wall_hole(CH, v, t, k, face_in=True, look=0.0):
    if k <= 0.02: return
    pts = hole_pts(k, t)
    L = Layer(v.wcam())
    F.poly(L, hole_pts(k * 1.12, t), (196, 110, 70))                                       # broken bricks around
    F.poly(L, pts, (34, 28, 26))
    F.outline(L, T.OL); CH.add(L)
    if face_in:
        M = Layer(v.wcam()); F.poly(M, pts, (0, 0, 0))
        G = Grab()
        un = 14.0
        cam = v.cam(HOLE[0] - 1.6 * un - 6, HOLE[1] + 20.1 * un, un)
        r = T.raisa(G, cam, T.RPOSE['stand'], t=t, mouth_=mouth('raisa', t), expr='sweet', look=look)
        for l in G.L:
            l.m &= M.m; CH.add(l)
        face(v, cam, r, 3.6)


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Толечка, год прошёл, квартиранты съехали. Я уезжаю домой.» — Raisa at the door with the bags and Pusya; Tolik can't believe it"""
    v = view_at(HALL, 850, 335, 1.2 - 0.04 * sm(u / 4.0), 180, 300)

    def draw(CH, v_):
        L = Layer(v_.wcam()); T.chelnok(L, 985, 700, 80, 62, 0.1, 21); T.chelnok(L, 1010, 650, 66, 50, -0.12, 22); CH.add(L)
        cam, r = raisa(CH, v_, t, 948, 700, 15.6, pose='hold', flip=True, expr='sweet', look=0.4)
        wx, wy = u2w(v_, cam, r['hand_n'])
        c = v_.cam(wx + 4, wy + 2.6 * 5.6, 5.6); rp = T.pusya(CH, c, t=t, expr='smug', shiver=1.2); face(v_, c, rp, 2.0)
        tolik(CH, v_, t, 742, 692, 15.0, pose='stand', expr='shock', m=0.4)
    big = hall(v, t, draw)
    D.blit(big, v, TAG, 975, 652)
    return big


def r_dance(t, u):
    """«Уезжаете?! Насовсем?! Ура!» — the door shuts; Tolik dances alone in the hallway, confetti"""
    v = view_at(HALL, 760, 335, 1.2, 180, 300)
    step = int(u / 0.32) % 3
    hop = abs(math.sin(u * math.pi / 0.32)) * 14 if u > 0.9 else 0.0

    def draw(CH, v_):
        pose = ('stand', 'fists', 'shock')[step] if u > 0.9 else 'shock'
        tolik(CH, v_, t, 760, 692 - hop, 15.0, flip=step == 1, pose=pose, expr='shock' if u < 0.9 else 'proud')
        if u > 0.9:
            L = Layer(v_.wcam())
            rng = np.random.default_rng(3)
            for i in range(60):
                x = 560 + rng.random() * 420; y0 = 160 + rng.random() * 120
                y = y0 + ((u - 0.9) * (120 + rng.random() * 80)) % 520
                F.dot(L, (x + 8 * math.sin(t * 5 + i), y), [(255, 80, 120), (255, 220, 60), (90, 200, 255), (120, 230, 120)][i % 4], 3.2)
            CH.add(L)
    return hall(v, t, draw)


def r_chair(t, u):
    """«Моё кресло. Мой пульт. Я в этом доме мужик!» — Tolik back in his armchair with the remote; the empty room echoes"""
    z = 1.3 - 0.12 * sm((u - 2.4) / 1.8)                                                   # pulls back: an empty, echoing room
    v = view_at(ROOM, 640, 470, z, 180, 330)

    def draw(CH, v_):
        tolik_chair(CH, v_, t, expr='smug' if u < 2.6 else 'proud', prop_n=lambda L, h: SH.remote(L, h, -1.2))
    return SH.room(v, t, draw, tv=1.0)


def r_days(t, u):
    """«3 ДНЯ СПУСТЯ»: the kitchen — a tower of dirty plates, a lump of stuck dumplings with a fork in it, flies"""
    v = view_at(KIT, 1060, 400, 1.3, 180, 330)

    def draw(CH, v_):
        L = Layer(v_.wcam())
        top = 452.0
        for i in range(9):                                                                   # dirty plate tower
            F.ell(L, (990 + (i % 2) * 4, top - 4 - i * 7), 36, 10, (226, 226, 214), 0, (244, 244, 236), (180, 176, 160))
            F.dot(L, (980 + (i * 13) % 30, top - 6 - i * 7), (150, 110, 60), 2.5)
        F.ell(L, (1120, top + 6), 44, 13, (244, 244, 236), 0, (255, 255, 255), (200, 204, 210))
        for k in range(7):                                                                   # stuck dumplings lump
            F.ell(L, (1100 + (k % 4) * 12, top - 6 - (k // 4) * 10), 13, 9, (236, 232, 214), 0, (250, 248, 236), (200, 194, 170))
        F.cap(L, (1124, top - 18), (1140, top - 64), 2.2, 2.2, (190, 194, 204))
        F.outline(L, T.OL); CH.add(L)
    big = SH.generic(KIT, v, t, draw, light=light_kitchen(v), vign=0.32)
    D.blit(big, v, PELM, 1170, 410)
    for i in range(4):                                                                       # flies
        fx_, fy_ = v.opt(1110 + 40 * math.sin(t * 7 + i * 2), 380 + 20 * math.cos(t * 9 + i))
        if 0 <= fy_ < big.shape[0] - 6 and 0 <= fx_ < big.shape[1] - 6:
            big[int(fy_):int(fy_) + 6, int(fx_):int(fx_) + 6] = (20, 20, 20)
    return big


def r_call(t, u):
    """«Раиса Захаровна… А может, вернётесь? На недельку?» — unshaven Tolik in the armchair, phone at his ear, socks on the floor"""
    v = view_at(ROOM, 620, 470, 1.32, 180, 330)

    def draw(CH, v_):
        L = Layer(v_.wcam()); mess(L); CH.add(L)
        tolik_chair(CH, v_, t, expr='sad', pose=dict(SITC, n=(4.6, 21.6)), prop_n=lambda L, h: T.phone(L, h, -1.9))
    return SH.room(v, t, draw)


def r_twist(t, u):
    """TWIST: a jackhammer behind the wall carpet — the room shakes, dust, a hole bursts open"""
    v = view_at(ROOM, 620, 380, 1.2, 180, 330)
    k = sm((u - 0.25) / 0.35)

    def draw(CH, v_):
        tolik_chair(CH, v_, t, expr='shock', pose=dict(SITC, n=(4.6, 21.6)), m=0.6, prop_n=lambda L, h: T.phone(L, h, -1.9))
        wall_hole(CH, v_, t, k, face_in=False)
    big = SH.room(v, t, draw)
    B.shake(big, t, 10 + 6 * k, 38)
    if k > 0.05:
        cx, cy = v.opt(*HOLE)
        for i in range(5): B.puff(big, cx + 60 * math.sin(i * 2.1 + t * 3), cy + 50 * math.cos(i * 1.7), 60 + 30 * k, 0.4 * k)
    return big


def r_hole(t, u):
    """«Толечка, а я соседнюю квартиру купила! Сейчас дверь сделаем!» — Raisa's beaming face in the hole in the carpet"""
    v = view_at(ROOM, HOLE[0] + 20, HOLE[1] + 40, 1.42, 180, 300)

    def draw(CH, v_):
        wall_hole(CH, v_, t, 1.0, face_in=True, look=0.6)
    big = SH.room(v, t, draw)
    cx, cy = v.opt(*HOLE)
    B.puff(big, cx - 80, cy + 120, 70, 0.25 * (1 - sm(u / 2)))
    if u > 2.5: B.shake(big, t, 4, 40)
    return big


def r_pusya(t, u):
    """«Кресло опять моё.» — Pusya came through the hole straight into the armchair, dusty, deadpan to camera"""
    un = 21.0
    x, y = 660.0, 640.0
    v = view_at(ROOM, x, y - 5.2 * un, 1.38 + 0.05 * sm(u / 2.0), 180, 300)

    def draw(CH, v_):
        L = Layer(v_.wcam()); T.armchair(L, SH.CHAIR[0] - 40, SH.CHAIR[1] + 30, 1.1, 'back'); CH.add(L)
        cam = v_.cam(x, y, un)
        r = T.pusya(CH, cam, t=t, mouth_=mouth('pusya', t, 2.0), expr='smug', shiver=0.8)
        face(v_, cam, r, 2.0)
        L = Layer(cam)
        for k in range(6): F.dot(L, (-2.0 + k * 0.8, 5.5 + (k % 3) * 0.9), (170, 150, 130), 0.25)       # plaster dust on him
        CH.add(L)
    return SH.room(v, t, draw)


def r_sveta(t, u):
    """«Толя, это же мама!» — Sveta in the room doorway, shrugging, smiling"""
    v = view_at(ROOM, 250, 430, 1.25, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(200, 660, 14.0)
        r = T.sveta(CH, cam, T.SPOSE['shrug'], t=t, mouth_=mouth('sveta', t), expr='smile')
        face(v_, cam, r)
    return SH.room(v, t, draw)


def r_cry(t, u):
    """«Навсегда?!» — close on Tolik, tears streaming, half happy, half horrified; the hole behind him"""
    x, y, un = 760.0, 640.0, 15.0 * 1.3
    v = view_at(ROOM, x - 20, y + 50 - 27 * un + 60, 1.42, 180, 300)

    def draw(CH, v_):
        cam, r = tolik(CH, v_, t, x, y + 50, un, flip=True, pose='cheeks', expr='whine')
        hx, hy = r['head']
        L = Layer(cam)
        for s_ in (-0.2, 1.2):
            for k in range(3):
                ty = hy + 0.2 + ((u * 1.6 + k * 0.33) % 1.0) * 3.0
                F.ell(L, (hx + s_ + 0.2, ty), 0.3, 0.42, (150, 210, 255), 0, (230, 246, 255), (90, 160, 230))
        CH.add(L)
    return SH.room(v, t, draw)


def r_loop(t, u):
    big = r_hook(t, u + 0.4)
    fx.speed_lines(big, t, 0.8)
    return big


SHOT = dict(hook=r_hook, dance=r_dance, chair=r_chair, days=r_days, call=r_call, twist=r_twist, hole=r_hole, pusya=r_pusya,
            sveta=r_sveta, cry=r_cry, loop=r_loop)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 6, ['ТЁЩА', 'УЕЗЖАЕТ?!'], hook_t=(0.06, 2.8), hook_y=200,
              stickers=[(O.sticker('УРА!!!', fg=(255, 222, 80), size=110), F0['dance'] + 1.0, F0['chair'], 540, 520),
                        (O.sticker('ЭХО...', fg=(200, 210, 230), size=80), F0['chair'] + 2.8, F0['days'], 540, 520),
                        (O.sticker('3 ДНЯ СПУСТЯ', fg=(255, 236, 120), size=76), F0['days'] + 0.05, F0['call'], 540, 560),
                        (O.sticker('ЗА СТЕНКОЙ!', fg=(255, 120, 150), size=92), F0['hole'] + 0.6, F0['pusya'], 540, 1500)],
              flashes=[TL.TWIST + 0.5], mosaics=[F0['days'], F0['sveta']],
              cap_y={'hook': 1290, 'pusya': 1450, 'hole': 1300, 'days': 1500}, cap_default=1380)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
