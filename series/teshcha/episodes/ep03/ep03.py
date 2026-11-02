"""E03 «Ещё тарелочку!» — the mother-in-law force-feeds Tolik («ты похудел»), the fifth plate was only a starter, the «diet» dish is
olivier without bread. Tolik secretly feeds Pusya under the table — TWIST (the saviour is the victim): Pusya has swollen into a ball,
and Raisa decides HE lost weight: «Ему тоже добавки!» Sveta comes home: «Толя же поправился!» — «Значит, ты его плохо кормила».
  python3 ep03.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
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

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG, promo='ru',
              endcard=dict(style='teshcha', lang='ru', promise='ЗАВТРА: ШАПКУ НАДЕНЬ!'))
SH.init(EPI, day=40)
KIT = SH.world('kitchen')
HALL = SH.world('hallway')
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0
TOP = 452.0                       # table top line in the kitchen bg
STOOL = (900.0, 690.0)            # Tolik's stool (floor point)
RAI = (720.0, 690.0, 12.6)        # Raisa standing by the stove, facing right
DIET = R.plate(66, 18, ['ДИЕТИЧЕСКОЕ'], bg=(255, 244, 170), colors=[(184, 30, 40)], border=(150, 130, 70), pad=1.0)

D.attach(KIT, [
    (R.plate(30, 38, ['ДЕНЬ', '40'], bg=(250, 248, 240), colors=[(184, 30, 40), (34, 28, 30)], border=(120, 110, 100), weights=[0.55, 1],
             stripe=((200, 40, 40), 0.3), pad=1.2), 70, 80),
    (R.plate(46, 16, ['НЕ ОТКРЫВАТЬ!'], bg=(255, 244, 170), colors=[(184, 30, 40)], border=(150, 130, 70), pad=1.0, tilt=-3), 186, 232),
    (R.plate(36, 14, ['СОЛЕНЬЯ'], bg=(250, 246, 230), colors=[(34, 28, 30)], border=(120, 110, 90), pad=0.9), 1000, 112),
    (R.plate(46, 16, ['МЕНЮ НА НЕДЕЛЮ'], bg=(250, 250, 240), colors=[(40, 60, 150)], border=(150, 140, 120), pad=1.0, tilt=2), 450, 296),
    (R.plate(40, 14, ['ЕШЬ, ПОКА ГОРЯЧЕЕ'], bg=(236, 220, 180), colors=[(120, 40, 30)], border=(100, 80, 60), pad=0.8), 960, 300),
])
D.attach(HALL, [
    (R.plate(30, 13, ['КВ. 33'], bg=(236, 206, 120), colors=[(34, 28, 30)], border=(120, 84, 30), pad=1.0), 1060, 150),
    (R.plate(44, 16, ['ТАПКИ — ТУТ!'], bg=(255, 244, 170), colors=[(184, 30, 40)], border=(150, 130, 70), pad=1.0, tilt=3), 700, 560),
])


def light_kitchen(v):
    wx, wy = v.opt(620.0, 120.0)
    return Light(amb=(1.03, 0.98, 0.9), keys=[(wx, wy, 1300, (255, 220, 160), 0.6)], rim=(1, -0.4, (255, 230, 180), 0.35), grad=(1.04, 0.9))


def light_hall(v):
    lx, ly = v.opt(640.0, 60.0)
    return Light(amb=(1.02, 0.96, 0.88), keys=[(lx, ly, 1200, (255, 210, 140), 0.55)], rim=(-1, -0.4, (255, 220, 170), 0.3), grad=(1.04, 0.9))


# ---------------------------------------------------------------- food (world px)
def plate(L, x, y, r, food=None, seed=0):
    F.ell(L, (x, y), r, r * 0.32, (244, 244, 236), 0, (255, 255, 255), (200, 204, 210))
    F.ell(L, (x, y - 1), r * 0.7, r * 0.22, (230, 230, 222))
    if food == 'cutlet':
        for k in range(3): F.ell(L, (x - r * 0.4 + k * r * 0.4, y - r * 0.18), r * 0.26, r * 0.16, (140, 80, 40), 0, (176, 110, 60), (100, 56, 30))
    elif food == 'blini':
        for k in range(6): F.ell(L, (x, y - 3 - k * 3.2), r * 0.62, r * 0.18, (236, 176, 80), 0, (250, 210, 120), (200, 140, 60))
    elif food == 'golubtsy':
        for k in range(3): F.ell(L, (x - r * 0.35 + k * r * 0.35, y - r * 0.2), r * 0.22, r * 0.17, (170, 200, 110), 0.3, (200, 226, 140), (120, 160, 80))
        F.ell(L, (x, y - r * 0.15), r * 0.5, r * 0.1, (200, 70, 50))


def bowl(L, x, y, r, col=(240, 226, 170), dome=0.5):
    """salad bowl / basin with a dome of olivier: peas and carrot dots"""
    F.ell(L, (x, y - r * 0.15), r, r * 0.35 + r * dome * 0.4, col, 0, (252, 242, 200), (210, 190, 130))
    rng = np.random.default_rng(int(x + y))
    for i in range(int(14 + r / 3)):
        a = rng.random() * 6.28; d = rng.random() * 0.8
        F.dot(L, (x + math.cos(a) * r * d, y - r * 0.2 - math.sin(a) * r * 0.3 * d - r * dome * 0.25), (110, 170, 60) if i % 2 else (230, 120, 50), 1.6)
    F.poly(L, [(x - r * 1.05, y - r * 0.1), (x + r * 1.05, y - r * 0.1), (x + r * 0.7, y + r * 0.35), (x - r * 0.7, y + r * 0.35)], (196, 210, 226))
    F.cap(L, (x - r * 1.05, y - r * 0.1), (x + r * 1.05, y - r * 0.1), 2.2, 2.2, (230, 236, 246))


def pot(L, x, y, r, t=0.0):
    F.poly(L, [(x - r, y), (x + r, y), (x + r * 0.95, y - r * 1.1), (x - r * 0.95, y - r * 1.1)], (200, 60, 50))
    F.ell(L, (x, y - r * 1.1), r * 0.95, r * 0.25, (150, 40, 34))
    F.cap(L, (x - r * 1.3, y - r * 0.9), (x - r * 0.95, y - r * 0.9), 2.5, 2.5, (60, 40, 30))
    F.cap(L, (x + r * 0.95, y - r * 0.9), (x + r * 1.3, y - r * 0.9), 2.5, 2.5, (60, 40, 30))


def food_table(CH, v, t, extra=0):
    """the mountain of plates on the kitchen table in front of Tolik"""
    L = Layer(v.wcam())
    for i in range(5):                                                       # stack of eaten plates
        F.ell(L, (980, TOP - 4 - i * 6), 34, 10, (244, 244, 236), 0, (255, 255, 255), (200, 204, 210))
    plate(L, 1060, TOP + 4, 40, 'cutlet')
    plate(L, 1150, TOP - 2, 36, 'blini')
    plate(L, 1100, TOP - 22, 34, 'golubtsy')
    bowl(L, 1205, TOP - 6, 30)
    pot(L, 1250, TOP - 30, 22, t)
    for k in range(extra): plate(L, 1010 + k * 40, TOP + 14 + (k % 2) * 6, 30, ('cutlet', 'blini', 'golubtsy')[k % 3])
    F.outline(L, T.OL); CH.add(L)


def kitchen(v, t, draw=None, steam=None, after=None):
    def aft(big, v_):
        if steam: B.steam(big, v_, t, steam[0], steam[1], -99, n=8, rise=160, size=46, a=0.5)
        if after: after(big, v_)
    return SH.generic(KIT, v, t, draw, light=light_kitchen(v), motes=(400, 80, 800, 360), after=aft)


SIT = dict(T.TPOSE['sit'], nleg=(1.45, -0.3), fleg=(1.35, -0.25))


def tolik_sit(CH, v, t, expr='whine', k=1.0, pose=None, **kw):
    un = 12.0 * k
    seat = STOOL[1] - 86
    L = Layer(v.wcam())                                                      # stool
    F.ell(L, (STOOL[0] - 6, seat + 4), 34, 9, (150, 96, 60), 0, (180, 120, 80), (110, 70, 44))
    for sx in (-24, 20): F.cap(L, (STOOL[0] + sx, seat + 8), (STOOL[0] + sx * 1.2, STOOL[1]), 3.5, 3.0, (110, 70, 44))
    F.outline(L, T.OL); CH.add(L)
    cam = v.cam(STOOL[0] - 10, seat + 13.6 * un, un)
    pp = dict(SIT) if pose is None else pose
    r = T.tolik(CH, cam, pp, t=t, mouth_=mouth('tolik', t), expr=expr, **kw)
    face(v, cam, r)
    return cam, r


def raisa_st(CH, v, t, expr='sweet', pos=RAI, pose=None, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un)
    r = T.raisa(CH, cam, pose or T.RPOSE['offer'], t=t, mouth_=mouth('raisa', t), expr=expr, **kw)
    face(v, cam, r, 3.6)
    return cam, r


def held_plate(food):
    return lambda L_, h: (F.ell(L_, (h[0] + 1.2, h[1] - 0.3), 2.6, 0.8, (244, 244, 236), 0, (255, 255, 255), (200, 204, 210)),
                          F.ell(L_, (h[0] + 1.2, h[1] - 0.8), 1.6, 0.6, (140, 80, 40) if food == 'cutlet' else (236, 176, 80)))


# ---------------------------------------------------------------- shots
def r_hook(t, u, extra=1):
    """«Толечка, ты похудел. Съешь ещё тарелочку!» — Tolik at the table behind a mountain of food, Raisa brings yet another plate"""
    v = view_at(KIT, 930, 420, 1.12 + 0.03 * sm(u / 3), 180, 330)

    def draw(CH, v_):
        raisa_st(CH, v_, t, 'sweet', prop_n=held_plate('cutlet'))
        tolik_sit(CH, v_, t, 'whine')
        food_table(CH, v_, t, extra)
    return kitchen(v, t, draw, steam=(1250, TOP - 60))


def r_tolik_full(t, u):
    """«Раиса Захаровна, я уже пятую доедаю!» — close on Tolik with cheeks full, the plate stack next to him"""
    un = 12.0 * 1.35
    seat = STOOL[1] - 86
    v = view_at(KIT, STOOL[0] + 10, seat + 13.6 * un - 27 * un + 40, 1.42, 180, 320)

    def draw(CH, v_):
        tolik_sit(CH, v_, t, 'whine', k=1.35)
        food_table(CH, v_, t, 2)
    return kitchen(v, t, draw)


def r_hot(t, u):
    """«Это была закуска. Сейчас будет горячее.» — Raisa with a steaming pot, proud"""
    x, y, un = RAI
    v = view_at(KIT, x + 40, y - 21 * un * 1.25 + 30, 1.4, 180, 300)

    def draw(CH, v_):
        cam, r = raisa_st(CH, v_, t, 'smug', pos=(x, y + 40, un * 1.25), pose=T.RPOSE['hold'])
        hx, hy = u2w(v_, cam, r['hand_n'])
        L = Layer(v_.wcam()); pot(L, hx + 10, hy + 30, 34); F.outline(L, T.OL); CH.add(L)
        SH_hx[0] = (hx + 10, hy - 20)
    big = kitchen(v, t, draw)
    B.steam(big, v, t, SH_hx[0][0], SH_hx[0][1], -99, n=10, rise=200, size=60, a=0.6)
    return big


SH_hx = [(0.0, 0.0)]


def r_diet(t, u):
    """«Я на диете! Мне нельзя!» — Tolik pleading, hands up"""
    un = 12.0 * 1.35
    seat = STOOL[1] - 86
    v = view_at(KIT, STOOL[0] + 10, seat + 13.6 * un - 27 * un + 40, 1.42, 180, 320)

    def draw(CH, v_):
        tolik_sit(CH, v_, t, 'shout', k=1.35, pose=dict(SIT, n=(5.2, 20.4), f=(-3.6, 20.6), bn=1, bf=-1))
        food_table(CH, v_, t, 2)
    return kitchen(v, t, draw)


def r_olivier(t, u):
    """«Хорошо. Вот тебе диетическое — оливье. Без хлеба.» — a basin-sized bowl of olivier lands on the table, sticker «ДИЕТИЧЕСКОЕ»"""
    v = view_at(KIT, 1060, 400, 1.3, 180, 330)
    land = sm(u / 0.5)

    def draw(CH, v_):
        raisa_st(CH, v_, t, 'sweet', pos=(880, 700, 13.0), pose=T.RPOSE['offer'])
        food_table(CH, v_, t, 2)
        L = Layer(v_.wcam()); bowl(L, 1060, TOP + 10 - 140 * (1 - land), 70, dome=0.9); F.outline(L, T.OL); CH.add(L)
    big = kitchen(v, t, draw)
    if land > 0.95: D.blit(big, v, DIET, 1060 - 33, TOP - 70)
    if 0.45 < u < 0.7: B.shake(big, t, 8, 40)
    return big


def under(v, t, draw=None):
    """under the table: the hanging oilcloth edge at the top, Tolik's legs, the floor"""
    def aft(big, v_):
        h = big.shape[0]
        band = int(h * 0.16)
        big[:band] = (big[:band] * 0.35 + np.array((236, 200, 120)) * 0.65).astype(np.uint8)        # oilcloth
        for i in range(0, big.shape[1], 54):
            big[band - 30:band, i:i + 30] = (220, 80, 60)
        big[band:] = (big[band:] * 0.62).astype(np.uint8)                                               # shadow under the table
    return SH.generic(KIT, v, t, draw, light=light_kitchen(v), after=aft, vign=0.4)


def r_under(t, u, ball=0.0):
    """«Пуся, выручай. Ешь, пока она не видит.» — under the table: Tolik's hand slips Pusya a cutlet"""
    v = view_at(KIT, 1040, 560, 1.42, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(1040, 712, 13.0)
        r = T.pusya(CH, cam, t=t, mouth_=0.6 if (u % 0.5) < 0.25 and ball < 0.5 else 0.0, expr='smug' if ball < 0.5 else 'shock',
                    ball=ball, shiver=0.3)
        face(v_, cam, r, 2.0)
        if ball < 0.5:
            L = Layer(v_.wcam())
            hx, hy = 960 + 20 * math.sin(t * 3), 600
            F.cap(L, (840, 560), (hx, hy), 9, 8, (34, 176, 168))                                   # tracksuit sleeve
            F.ell(L, (hx + 8, hy), 12, 10, (242, 196, 162))
            F.ell(L, (hx + 24, hy + 2), 14, 8, (140, 80, 40), 0, (176, 110, 60), (100, 56, 30))     # cutlet
            F.outline(L, T.OL); CH.add(L)
    return under(v, t, draw)


def r_peek(t, u):
    big = r_under(t, u, ball=1.0)
    fx.speed_lines(big, t, 1.2)
    return big


def r_twist(t, u):
    """TWIST: «Ой, Пусечка похудел! Ему тоже добавки!» — Pusya is a perfectly round ball; Raisa peeks under the table, delighted"""
    v = view_at(KIT, 1040, 560, 1.42, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(1040, 712, 13.0)
        r = T.pusya(CH, cam, t=t, expr='shock', ball=1.0, shiver=0.2)
        face(v_, cam, r, 2.0)
        c2 = v_.cam(1150, 760, 15.0, flip=True)                                                    # Raisa bending in from the right
        r2 = T.raisa(CH, c2, dict(T.RPOSE['offer'], n=(7.0, 12.0)), t=t, mouth_=mouth('raisa', t), expr='shout', prop_n=held_plate('blini'))
        face(v_, c2, r2, 3.6)
    big = under(v, t, draw)
    if u < 0.3: B.shake(big, t, 10, 40)
    return big


def r_ball(t, u):
    """«Я больше не могу. Это всё Толик.» — close on Pusya the ball, sweater bursting, panting deadpan to camera"""
    v = view_at(KIT, 1040, 640, 1.42, 180, 300)

    def draw(CH, v_):
        cam = v_.cam(1040, 712, 19.0)
        r = T.pusya(CH, cam, t=t, mouth_=mouth('pusya', t, 2.0), expr='deadpan', ball=1.0, shiver=0.2)
        face(v_, cam, r, 2.0)
    return under(v, t, draw)


def r_sveta(t, u):
    """«Мама, Толя же поправился!» — Sveta home from work in the hallway, bag in hand, staring at round Tolik"""
    v = view_at(HALL, 760, 430, 1.25, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(820, 690, 13.5, flip=True)
        r = T.sveta(CH, cam, T.SPOSE['shrug'], t=t, mouth_=mouth('sveta', t), expr='shock')
        face(v_, cam, r)
    return SH.generic(HALL, v, t, draw, light=light_hall(v), motes=(500, 60, 900, 300))


def r_button(t, u):
    """«Значит, ты его плохо кормила, Светочка.» — close on Raisa, sweet poison, handing over another plate"""
    x, y, un = RAI
    v = view_at(KIT, x + 40, y - 21 * un * 1.25 + 30, 1.4, 180, 300)

    def draw(CH, v_):
        raisa_st(CH, v_, t, 'sweet', pos=(x, y + 40, un * 1.25), prop_n=held_plate('blini'))
    return kitchen(v, t, draw)


def r_loop(t, u):
    big = r_hook(t, u + 1.0, extra=3)
    fx.speed_lines(big, t, 0.8)
    return big


SHOT = dict(hook=r_hook, tolik_full=r_tolik_full, hot=r_hot, diet=r_diet, olivier=r_olivier, under=r_under, peek=r_peek,
            twist=r_twist, ball=r_ball, sveta=r_sveta, button=r_button, loop=r_loop)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 3, ['ЕЩЁ', 'ТАРЕЛОЧКУ?!'], hook_t=(0.06, 2.8), hook_y=200,
              stickers=[(O.sticker('5-Я ТАРЕЛКА', fg=(255, 222, 80), size=62), F0['tolik_full'] + 0.3, F0['hot'], 540, 560),
                        (O.sticker('ШАР?!', fg=(255, 120, 150), size=110), TL.TWIST + 0.3, F0['ball'], 540, 560),
                        (O.sticker('+5 КГ', fg=(255, 186, 214), size=70), F0['sveta'] + 0.4, F0['button'], 540, 560)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['under'], F0['sveta']],
              cap_y={'hook': 1500, 'ball': 1450, 'twist': 1450, 'under': 1450, 'peek': 1450}, cap_default=1380)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
