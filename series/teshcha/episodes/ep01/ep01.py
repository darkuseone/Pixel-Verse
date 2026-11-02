"""E01 «Я к вам на недельку!» (v2) — the mother-in-law arrives «for a week» with a mountain of plaid bags (more pour out of the lift), takes Tolik's
armchair («Я в этом доме мужик!» — «Мужик, тапки сними. Я помыла.»), Pusya drops the clue («три года жили»), TWIST: Sveta herself has
rented out mum's flat «на год». Tolik sleeps on the balcony; Pusya in his armchair: «Отправь тому…»; doorbell: «Это Люся. Тоже на
недельку!» -> loop into the opening scream.
  python3 ep01.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import stage as ST
from stage import view_at, shadow
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
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG, promo='ru',
              endcard=dict(style='teshcha', lang='ru', promise='ЗАВТРА: ТЁЩА И ТЕЛЕВИЗОР'))
talk = EPI.talk
W = K.build()
K.decorate(W, day=1)
LAND, ROOM, BALC = W['landing'], W['room'], W['balcony']
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0

DOOR = (962.0, 560.0, 12.5)          # Tolik in the doorway, facing left
RAI_L = (812.0, 646.0, 13.6)         # Raisa on the landing, facing right
OUT_L = (872.0, 652.0, 13.6)         # Tolik stepped out onto the landing, facing left (stairs)
SVETA = (176.0, 706.0, 14.6)         # Sveta coming up the stairs, facing right
CHAIR = (600.0, 650.0)
TAG = R.plate(54, 16, ['КВАРТИРАНТАМ'], bg=(250, 244, 220), colors=[(176, 30, 40)], border=(120, 100, 70), pad=1.2)
CHAIR_TAG = R.plate(72, 20, ['КРЕСЛО ТОЛИКА'], bg=(236, 210, 130), colors=[(60, 30, 20)], border=(90, 60, 30), pad=1.0)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def u2w(v, cam, pt):
    """unit point of a character cam -> world px"""
    x, y = cam.p(*pt)
    k = ST.PX[0]
    return v.X0 + x * k / v.Z, v.Y0 + (y * k - v.oy) / v.Z


def face(v, cam, r, r_units=3.0):
    K.logface(v, cam, r['head'], r_units)


# ---------------------------------------------------------------- landing props
PILE = [('carpet', 548, 664), ('bag', 612, 668, 96, 74, 0.0, 1), ('bag', 690, 676, 104, 80, 0.05, 2), ('tv', 742, 640),
        ('bag', 650, 606, 84, 64, -0.06, 3), ('ficus', 772, 690)]


def pile(L, extra=0):
    for it in PILE:
        if it[0] == 'bag': T.chelnok(L, it[1], it[2], it[3], it[4], it[5], it[6])
        elif it[0] == 'carpet': T.carpet_roll(L, it[1], it[2], 150, 16, -0.3)
        elif it[0] == 'tv': T.tv_rubin(L, it[1], it[2], 0.9)
        elif it[0] == 'ficus': T.ficus(L, it[1], it[2], 1.0)


def lift(L, k_open, bags_u):
    """lift doors slide open (k_open 0..1) and plaid bags slide out one after another (bags_u seconds since they started)"""
    x0, y0, x1, y1 = 242, 96, 410, 500
    mid = (x0 + x1) / 2
    gap = (x1 - x0) / 2 * k_open
    if gap > 4:
        ST.wrect(L, mid - gap, y0, mid + gap, y1, (34, 30, 36))
        ST.wrect(L, mid - gap, y1 - 30, mid + gap, y1, (60, 52, 50))
        ST.wrect(L, x0, y0, mid - gap, y1, (92, 94, 98)); ST.wrect(L, mid + gap, y0, x1, y1, (92, 94, 98))
        for xx in (x0 + 10, x1 - 14):
            ST.wrect(L, xx, y0 + 6, xx + 4, y1 - 6, (120, 124, 128))
        ST.wrect(L, mid - gap - 3, y0, mid - gap, y1, (60, 58, 56)); ST.wrect(L, mid + gap, y0, mid + gap + 3, y1, (60, 58, 56))
    if bags_u > 0:
        for i in range(6):
            u = sm((bags_u - i * 0.18) / 0.4)
            if u <= 0: continue
            tx, ty = 330 + (i % 3) * 70 + (i // 3) * 30, 560 + (i % 2) * 40 + (i // 3) * 30
            x = lerp(mid, tx, u); y = lerp(y1, ty, u) - 40 * math.sin(math.pi * u)
            T.chelnok(L, x, y, 80, 62, 0.4 * (1 - u) * (1 if i % 2 else -1), i + 7)


def landing(v, t, draw=None, lift_k=0.0, bags_u=0.0, extra_pile=True):
    CH, FX = K.begin()
    big = v.bg()
    if lift_k > 0 or bags_u > 0:
        L = Layer(v.wcam()); lift(L, lift_k, bags_u); CH.add(L)
    if extra_pile:
        L = Layer(v.wcam()); pile(L); CH.add(L)
    if draw: draw(CH, v)
    CH.comp(big, K.light_landing(v))
    fx.motes(FX, v, t, 520, 40, 780, 300, n=26, col=(255, 236, 190), seed=3)
    FX.comp(big)
    fx.vignette(big, 0.28)
    return big


def tolik_door(CH, v, t, pos=DOOR, k=1.0, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=True)
    kw.setdefault('expr', 'scream')
    r = T.tolik(CH, cam, t=t, mouth_=mouth('tolik', t), **kw)
    face(v, cam, r)
    return cam, r


def raisa_l(CH, v, t, pos=RAI_L, k=1.0, pusya=True, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k)
    kw.setdefault('expr', 'sweet')
    r = T.raisa(CH, cam, t=t, mouth_=mouth('raisa', t), **kw)
    face(v, cam, r, 3.6)
    if pusya:
        px, py = u2w(v, cam, F.H(3.4, 9.0))
        T.pusya(CH, v.cam(px, py, un * k * 0.62), t=t, expr='deadpan')
    return cam, r


# ---------------------------------------------------------------- shots
def r_tolik_cu(t, u, scream=True):
    """«Как на недельку?! Света сказала — на один денёчек!» — waist-up Tolik in the doorway, horrified; the curlers of the
    mother-in-law in the foreground at the bottom-left, a plaid bag at the bottom-right"""
    x, y, un = DOOR
    k = 1.25
    hx, hy = x - 1.3 * un * k, y + 40 - 27.2 * un * k
    v = view_at(LAND, hx + 40, hy, 1.42 + 0.03 * u, 190, 330)

    def draw(CH, v_):
        tolik_door(CH, v_, t, (x, y + 40, un), k, pose=T.TPOSE['shock'], expr='shout', shake=0.04)
        L = Layer(v_.wcam()); T.chelnok(L, 1066, 820, 150, 110, 0.06, 4); CH.add(L)
        raisa_l(CH, v_, t, (836, 760, 15.6), 1.0, pusya=False, expr='smug')
    return landing(v, t, draw, extra_pile=False)


def r_hook(t, u):
    """«Толечка, здравствуй! Я к вам приехала на недельку!» — two-shot at the door: the mother-in-law in curlers with Pusya and a
    mountain of plaid bags, Tolik in the doorway with his jaw on the floor (readable without sound)"""
    v = view_at(LAND, 856 - 10 * sm(u / 3.0), 300, 1.15 + 0.04 * sm(u / 3.0), 180, 330)

    def draw(CH, v_):
        raisa_l(CH, v_, t, pose=T.RPOSE['hold'])
        tolik_door(CH, v_, t, expr='shock', pose=T.TPOSE['shock'])
    return landing(v, t, draw)


def r_raisa_door(t, u):
    """«На недельку, Толечка. Сумки бери.» — two-shot, she hands him a bag; whip-pan to the lift: more bags pour out"""
    pan = sm((u - 1.05) / 0.35)
    cx = lerp(870, 352, pan); cy = lerp(420, 380, pan)
    v = view_at(LAND, cx, cy, 1.12, 180, 330)

    def draw(CH, v_):
        cam, r = raisa_l(CH, v_, t, pose=T.RPOSE['offer'], hand_n=None)
        hx, hy = u2w(v_, cam, r['hand_n'])
        L = Layer(v_.wcam()); T.chelnok(L, hx + 8, hy + 66, 74, 58, 0.04, 5); CH.add(L)
        tolik_door(CH, v_, t, expr='shock', pose=T.TPOSE['shock'])
    big = landing(v, t, draw, lift_k=sm((u - 1.3) / 0.3), bags_u=max(0.0, u - 1.55))
    if 0.95 < u < 1.45: fx.speed_lines(big, t, 0.8)
    return big


def room(v, t, draw=None, tv=0.0, prints=0, px0=800.0, py0=690.0, big_prints=1.0):
    CH, FX = K.begin()
    big = v.bg()
    if prints:
        L = Layer(v.wcam())
        for i in range(prints):
            g = big_prints
            px, py = px0 - 60 * g - i * 52 * g, py0 + (i % 2) * 14 * g
            F.ell(L, (px, py), 16 * g, 6 * g, (78, 52, 32)); F.ell(L, (px + 18 * g, py), 5 * g, 4 * g, (78, 52, 32))
            for k_ in range(3): F.ell(L, (px - 6 * g + k_ * 7 * g, py - 4 * g), 2.2 * g, 1.6 * g, (110, 76, 46))
        CH.add(L)
    if draw: draw(CH, v)
    CH.comp(big, K.light_room(v, tv))
    if tv > 0:
        fx.glow(big, *v.opt(*K.R_TV), 260, (120, 170, 255), 0.18 * tv * (0.8 + 0.2 * math.sin(t * 13)))
    fx.motes(FX, v, t, 760, 120, 1000, 420, n=18, col=(255, 226, 170), seed=5)
    FX.comp(big)
    fx.vignette(big, 0.26)
    return big


def chair(CH, v, s, part):
    L = Layer(v.wcam()); T.armchair(L, CHAIR[0], CHAIR[1], s, part)
    if part == 'back': K.decal_layer(L, v, CHAIR_TAG, CHAIR[0] - 18 * s - 36, CHAIR[1] - 236 * s + 14 * s)
    CH.add(L)


def raisa_sit(CH, v, t, s=0.65, unit=12.0, drop=0.0, **kw):
    seat = CHAIR[1] - 64 * s
    x, y = CHAIR[0] + 6, seat + 6.4 * unit - drop
    cam = v.cam(x, y, unit)
    kw.setdefault('expr', 'sweet')
    r = T.raisa(CH, cam, T.RPOSE['sit'], t=t, mouth_=mouth('raisa', t), **kw)
    face(v, cam, r, 3.6)
    return cam, r


def r_manly(t, u):
    """«Я в этом доме мужик!» — she plops into HIS armchair, Pusya on her lap; Tolik puffs his chest"""
    v = view_at(ROOM, 704, 430, 1.1 + 0.02 * u, 180, 330)
    drop = 60 * (1 - sm(u / 0.25))

    def draw(CH, v_):
        chair(CH, v_, 0.65, 'back')
        cam, r = raisa_sit(CH, v_, t, drop=drop, look=0.6)
        px, py = u2w(v_, cam, r['lap'])
        T.pusya(CH, v_.cam(px, py + 2, 7.4), t=t, expr='deadpan')
        chair(CH, v_, 0.65, 'front')
        x, y, un = 800.0, 664.0, 12.0
        c2 = v_.cam(x, y, un, flip=True)
        r2 = T.tolik(CH, c2, T.TPOSE['fists'], t=t, mouth_=mouth('tolik', t), expr='proud')
        face(v_, c2, r2)
    return room(v, t, draw, prints=4)


def r_prints(t, u):
    """«Я полы помыла.» — accent on the dirty footprints across the freshly washed floor, ending at Tolik's slippers"""
    v = view_at(ROOM, 780, 470, 1.44, 180, 330)

    def draw(CH, v_):
        c2 = v_.cam(862.0, 600.0, 11.0, flip=True)
        T.tolik(CH, c2, T.TPOSE['stand'], t=t, expr='sad', look=0.3)
    big = room(v, t, draw, prints=4, px0=858.0, py0=592.0, big_prints=1.25)
    for i in range(4):                                                             # shine sparkles on the washed floor
        sx, sy = v.opt(700 + i * 55, 640 + (i % 2) * 18)
        fx.glow(big, sx, sy, 46, (255, 255, 255), 0.55 * abs(math.sin(t * 8 + i)))
    return big


def r_raisa_chair(t, u):
    if u > 1.3: return r_prints(t, u)
    """«Мужик, тапки сними. Я помыла.» — close on her sweet gold-tooth smile, then tilt down to his slippers and the dirty prints"""
    tilt = sm((u - 1.3) / 0.6)
    s, un = 0.82, 15.0
    seat = CHAIR[1] - 64 * s
    fy = seat + 6.4 * un - 18.6 * un * 1.2
    v = view_at(ROOM, lerp(640, 850, tilt), lerp(fy + 30, 520, tilt), 1.44, 180, lerp(300, 330, tilt))

    def draw(CH, v_):
        L = Layer(v_.wcam()); T.armchair(L, CHAIR[0], CHAIR[1], s, 'back'); CH.add(L)
        raisa_sit(CH, v_, t, s=s, unit=un, look=0.4)
        L = Layer(v_.wcam()); T.armchair(L, CHAIR[0], CHAIR[1], s, 'front'); CH.add(L)
        c2 = v_.cam(905.0, 692.0, 11.0, flip=True)
        r2 = T.tolik(CH, c2, T.TPOSE['stand'], t=t, expr='sad', look=0.3)
        if tilt > 0.5: face(v_, c2, r2)
    big = room(v, t, draw, prints=5, px0=905.0)
    if tilt > 0.6:
        for i in range(3):                                                         # shine sparkles on the washed floor
            sx, sy = v.opt(760 + i * 60, 712 + (i % 2) * 10)
            fx.glow(big, sx, sy, 40, (255, 255, 255), 0.5 * abs(math.sin(t * 9 + i)))
    return big


def r_pusya1_unused(t, u):
    """«Мы у сестры так на недельку… три года жили.» — Pusya on the armrest, trembling, deadpan to camera, slow push-in"""
    un = 21.0
    x, y = 660.0, 640.0
    v = view_at(ROOM, x, y - 5.2 * un, 1.36 + 0.06 * sm(u / 4.0), 180, 300)

    def draw(CH, v_):
        L = Layer(v_.wcam()); T.armchair(L, CHAIR[0] - 40, CHAIR[1] + 30, 1.1, 'back'); CH.add(L)
        cam = v_.cam(x, y, un)
        r = T.pusya(CH, cam, t=t, mouth_=mouth('pusya', t, 2.0), expr='deadpan', shiver=1.2)
        face(v_, cam, r, 2.0)
    return room(v, t, draw)


def r_run(t, u):
    v = view_at(ROOM, lerp(700, 300, u / 0.2), 420, 1.1, 180, 330)
    big = room(v, t)
    fx.speed_lines(big, t, 1.4)
    return big


def r_phone(t, u, k_out=0.0):
    """«Света! Твоя мама — на недельку?!» — Tolik out on the landing with the phone, the bag mountain behind him"""
    x, y, un = OUT_L
    k = 1.3
    hx, hy = x - 1.3 * un * k, y + 30 - 27.2 * un * k
    v = view_at(LAND, hx + 30, hy + 40, 1.38, 190, 300)

    def draw(CH, v_):
        tolik_door(CH, v_, t, (x, y + 30, un), k, pose=T.TPOSE['phone'], expr='shout', prop_n=lambda L, h: T.phone(L, h, -1.75))
    return landing(v, t, draw)


def r_reveal(t, u):
    """TWIST: pull back and pan left from Tolik to the stairs: Sveta is coming up with the keys «КВАРТИРАНТАМ» — «Я мамину квартиру
    сдала. На год.»"""
    x, y, un = OUT_L
    k = sm((u - 0.1) / 0.55)
    hx, hy = x - 1.3 * un * 1.3, y + 30 - 27.2 * un * 1.3
    cx, cy = lerp(hx + 30, 300, k), lerp(hy + 40, 430, k)
    Z = lerp(1.38, 0.98, k)
    v = view_at(LAND, cx, cy, Z, lerp(190, 180, k), lerp(300, 330, k))

    def draw(CH, v_):
        tolik_door(CH, v_, t, (x, y + 30, un), 1.3, pose=T.TPOSE['phone'], expr='shock', prop_n=lambda L, h: T.phone(L, h, -1.75))
        sx, sy, su = SVETA
        cam = v_.cam(sx, sy, su)
        r = T.sveta(CH, cam, T.SPOSE['keys'], t=t, mouth_=mouth('sveta', t), expr='guilty', prop_n=lambda L, h: T.keys(L, h, t))
        face(v_, cam, r)
        TAGW[0] = u2w(v_, cam, (r['hand_n'][0] + 0.9, r['hand_n'][1] + 2.6))
    big = landing(v, t, draw)
    tx, ty = TAGW[0]
    D.blit(big, v, TAG, tx - 6, ty)
    if 0.1 < u < 0.65: fx.speed_lines(big, t, 0.9)
    return big


TAGW = [(0.0, 0.0)]


def r_nagod(t, u):
    """«На год?!» — punch-in on Tolik's scream, shake + VHS glitch"""
    x, y, un = OUT_L
    k = 1.45
    hx, hy = x - 1.3 * un * k, y + 60 - 27.2 * un * k
    v = view_at(LAND, hx + 30, hy, 1.4 + 0.05 * sm(u / 0.3), 190, 320)

    def draw(CH, v_):
        tolik_door(CH, v_, t, (x, y + 60, un), k, pose=T.TPOSE['shock'], expr='scream', shake=0.08)
    big = landing(v, t, draw)
    B.shake(big, t, 12, 37)
    if u < 0.5: fx.vhs(big, t, 0.8 * (1 - u / 0.5))
    return big


def balcony(v, t, draw=None, snow=70):
    CH, FX = K.begin()
    big = v.bg()
    if draw: draw(CH, v)
    CH.comp(big, K.light_balcony(v))
    B.falling_snow(FX, v, t, 280, 100, 960, 470, n=snow, speed=60)
    B.snow_in(FX, v, t, (300, 150, 900, 300), n=30, drift=(-120, 260))
    FX.comp(big)
    fx.vignette(big, 0.34)
    return big


SITB = dict(T.TPOSE['sit'], nleg=(1.45, -0.55), fleg=(1.35, -0.5))


def tolik_bed(CH, v, t, k=1.0, expr='cold', m=None, shake=0.07):
    L = Layer(v.wcam()); T.campbed(L, K.B_BED[0], K.B_BED[1], 240, 1.6); CH.add(L)
    un = 11.0 * k
    seat = K.B_BED[1] - 58
    cam = v.cam(K.B_BED[0] + 10, seat + 13.6 * un, un, flip=True)
    r = T.tolik(CH, cam, SITB, t=t, mouth_=mouth('tolik', t) if m is None else m, expr=expr, hat='knit', blanket=True, cold=0.35,
                shake=shake, hand_n=F.H(3.4, 16.4), hand_f=F.H(2.8, 16.8))
    face(v, cam, r)
    return cam, r


def r_balcony(t, u):
    """«Мужик спит на балконе. Закаляйся.» — Tolik on the camp bed in the snow, blanket and knitted hat; Raisa in the warm doorway"""
    v = view_at(BALC, 262, 430, 0.97, 180, 330)

    def draw(CH, v_):
        tolik_bed(CH, v_, t)
        cam = v_.cam(150.0, 636.0, 12.4)
        r = T.raisa(CH, cam, T.RPOSE['hips'], t=t, mouth_=mouth('raisa', t), expr='sweet')
        face(v_, cam, r, 3.6)
    big = balcony(v, t, draw)
    for hx in (0,):
        B.puff(big, *v.opt(K.B_BED[0] - 40, K.B_BED[1] - 300), 40 + 20 * math.sin(t * 3), 0.25)
    return big


def r_pusya2(t, u):
    """«Отправь тому, у кого тёща «на недельку».» — Pusya in Tolik's armchair under his plaid blanket, TV flicker"""
    s = 1.0
    x, y = CHAIR[0] - 4, CHAIR[1] - 64 * s + 4
    un = 19.0
    v = view_at(ROOM, x + 10, y - 5.0 * un, 1.4 + 0.05 * sm(u / 4.0), 180, 300)

    def draw(CH, v_):
        chair(CH, v_, s, 'back')
        cam = v_.cam(x, y, un)
        r = T.pusya(CH, cam, t=t, mouth_=mouth('pusya', t, 2.0), expr='smug', shiver=0.2)
        Bl = Layer(cam)
        F.poly(Bl, [F.H(-3.4, 3.4), F.H(3.4, 3.4), F.H(3.9, -0.2), F.H(-3.9, -0.2)], T.TC['blanket'])
        F.cap(Bl, F.H(-3.4, 3.4), F.H(3.4, 3.4), 0.5, 0.5, T.TC['blanket_hi'])
        m1 = F.band_mask(Bl, F.H(0, 2.0), 0.5, width=3.0); m2 = F.band_mask(Bl, F.H(0, 2.0), 0.5, width=3.0, ang=1.57)
        F.recolor(Bl, m1 & m2, [(T.TC['blanket'], T.TC['plaid']), (T.TC['blanket_hi'], T.TC['plaid'])])
        F.outline(Bl, T.OL); CH.add(Bl)
        face(v_, cam, r, 2.0)
        L = Layer(v_.wcam()); T.armchair(L, CHAIR[0], CHAIR[1], s, 'front'); CH.add(L)
    return room(v, t, draw, tv=1.0)


def r_bell(t, u):
    """dzzzin! — Tolik on the balcony snaps his eyes open"""
    return r_loop(t, u, scream=0.0, expr='shock')


def r_lyusya(t, u):
    """«Толечка, открой! Это Люся. Тоже на недельку!» — Raisa calls from the room doorway, hand at her mouth, delighted"""
    v = view_at(ROOM, 170, 470, 1.3, 170, 330)

    def draw(CH, v_):
        cam = v_.cam(150.0, 690.0, 15.0)
        r = T.raisa(CH, cam, T.RPOSE['call'], t=t, mouth_=mouth('raisa', t), expr='sweet', look=0.6, hand_n=F.H(6.0, 19.8))
        face(v_, cam, r, 3.6)
    return room(v, t, draw)


def r_loop(t, u, scream=None, expr=None):
    """close on Tolik on the camp bed: the face freezes, the mouth opens into the opening scream (loop)"""
    k = 1.55
    un = 11.0 * k
    seat = K.B_BED[1] - 58
    fx_, fy_ = K.B_BED[0] + 10 - 2.0 * un, seat + 13.6 * un - 27.0 * un
    v = view_at(BALC, fx_, fy_, 1.42, 180, 300)
    m = max(mouth('tolik', t), sm(u / 0.3)) if scream is None else scream

    def draw(CH, v_):
        L = Layer(v_.wcam()); T.campbed(L, K.B_BED[0], K.B_BED[1], 240, 1.6); CH.add(L)
        cam = v_.cam(K.B_BED[0] + 10, seat + 13.6 * un, un, flip=True)
        r = T.tolik(CH, cam, SITB, t=t, mouth_=m, expr=expr or ('scream' if m > 0.4 else 'shock'), hat='knit', blanket=True, cold=0.35,
                    shake=0.05 + 0.1 * m, hand_n=F.H(3.4, 16.4), hand_f=F.H(2.8, 16.8))
        face(v_, cam, r)
    big = balcony(v, t, draw, snow=50)
    if m > 0.5: B.shake(big, t, 8, 40)
    return big


SHOT = dict(hook=r_hook, tolik_cu=r_tolik_cu, teeth=lambda t, u: r_balcony(t, u), raisa_door=r_raisa_door, manly=r_manly, raisa_chair=r_raisa_chair, run=r_run,
            phone=r_phone, reveal=r_reveal, nagod=r_nagod, balcony=r_balcony, pusya2=r_pusya2, bell=r_bell, lyusya=r_lyusya,
            loop=r_loop)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 1, ['Я К ВАМ', 'НА НЕДЕЛЬКУ!'], hook_t=(0.06, 2.8), hook_y=200,
              stickers=[(O.sticker('СЛЕДЫ!', fg=(255, 222, 80), size=70), F0['raisa_chair'] + 1.45, F0['run'], 330, 1020),
                        (O.sticker('НА ГОД?!', fg=(255, 120, 150), size=84), TL.TWIST + 1.9, F0['nagod'], 700, 640),
                        (O.sticker('ДЕНЬ 1', fg=(255, 186, 214), size=54), F0['teeth'] + 0.1, F0['pusya2'], 820, 520)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['manly'], F0['phone'], F0['teeth']],
              cap_y={'hook': 1505, 'tolik_cu': 1420, 'pusya2': 1420, 'reveal': 1380, 'raisa_chair': 1120}, cap_default=1340)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
