"""E06 «ДЕНЬ МАТЕРИ — ПОДАРОК САМИ!» (season finale) — 29 November, Mother's Day: Batya and Tyoma make a gift in the garage «сами»;
measured «на глаз», the stool comes out with three legs («Как штатив!»). TWIST (the reward taken by another): Batya's own mother,
babushka Valentina, walks in — «Витенька! Это мне?! Сынок, сам сделал!» — and takes the stool. Ira has already laid the table herself
(the handbell from E01 on it). Button (callback to the pilot): babushka, standing on the three-legged stool, feels his forehead —
«Витенька, ты похудел! И лоб горячий!» — «Мама… Тридцать семь и два…»
  python3 ep06.py test … | frames … | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from stage import view_at, Light
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as BF
from props import decals as D
from props import batyacast as B
from props import batyakit as K
from props import batyashots as S
from props.batyashots import mouth, u2w, face, P, KIT, UN
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=dict(K.COL, babushka=(255, 170, 200)), slug=TL.SLUG, promo='ru',
              endcard=dict(style='batya', lang='ru', promise='СЕЗОН 2: ДЕКАБРЬ — ЁЛКА САМИ!'))
S.init(EPI)
GAR = S.extra_world('garage')
F0 = TL.T0
OL = B.OL
INK, RED, CREAM = (34, 28, 30), (184, 30, 40), (255, 252, 236)
GF = 660.0                                   # standing floor line in the garage foreground
WOOD, WOOD_HI, WOOD_SH = (200, 150, 90), (230, 184, 124), (150, 104, 56)

D.attach(GAR, [
    (P(80, 104, ['НОЯБРЬ', '29 —', 'ДЕНЬ', 'МАТЕРИ!'], CREAM, [INK, RED, RED, RED], (150, 140, 120), pad=0.7,
       weights=[0.7, 1, 1, 1]), 628, 124),
    (P(84, 108, ['ГАРАЖ', 'САНЫЧА', 'НЕ ТРОГАТЬ!'], (255, 244, 170), [INK, INK, RED], (150, 130, 70), pad=0.7,
       weights=[1, 1, 0.8]), 758, 124),
    (P(50, 18, ['ГВОЗДИ «НА ГЛАЗ»'], CREAM, [INK], None, pad=0.4), 270, 328),
    (P(44, 18, ['ЛЕЩ 2005 →'], CREAM, [RED], None, pad=0.4, tilt=-4, hand=True), 30, 520),
])
D.attach(KIT, [
    (P(110, 30, ['С ДНЁМ МАТЕРИ!'], (255, 236, 240), [RED], (200, 120, 140), pad=0.5, tilt=-2), 860, 300),
])


# ---------------------------------------------------------------- props
def plane(L, h):
    """рубанок: wooden body with a front knob"""
    F.poly(L, [(h[0] - 2.2, h[1] + 0.2), (h[0] + 2.6, h[1] + 0.2), (h[0] + 2.4, h[1] - 0.9), (h[0] - 2.0, h[1] - 0.9)], WOOD)
    F.ell(L, (h[0] + 1.6, h[1] - 1.2), 0.5, 0.5, (150, 60, 40))
    F.cap(L, (h[0] - 2.0, h[1] + 0.25), (h[0] + 2.4, h[1] + 0.25), 0.12, 0.12, (170, 172, 180))


def plank(L, h):
    F.cap(L, (h[0] - 6.0, h[1] - 0.8), (h[0] + 2.0, h[1] - 0.2), 0.7, 0.7, WOOD, WOOD_HI, WOOD_SH)


def stool(L, x, y, s=1.0, wob=0.0, legs=3):
    """the gift: a crooked stool with three legs (world px, (x, y) = the floor under its centre)"""
    a = wob
    def T(dx, dy): return (x + dx * math.cos(a) - dy * math.sin(a), y + dx * math.sin(a) + dy * math.cos(a))
    for k, (dx, ln) in enumerate(((-30, 1.0), (4, 0.92), (30, 1.06))[:legs]):
        F.cap(L, T(dx * s, -84 * s), T((dx * 1.25 + (6 if k == 1 else 0)) * s, -84 * s + 84 * s * ln), 5 * s, 4 * s, WOOD, WOOD_HI, WOOD_SH)
    F.cap(L, T(16 * s, -84 * s), T(17 * s, -60 * s), 4 * s, 4 * s, WOOD_SH)                                  # the missing 4th leg: a stub
    F.poly(L, [T(13 * s, -60 * s), T(21 * s, -60 * s), T(18 * s, -52 * s), T(16 * s, -57 * s)], WOOD_SH)
    F.ell(L, T(0, -88 * s), 44 * s, 12 * s, WOOD, 0, WOOD_HI, WOOD_SH)
    F.ell(L, T(0, -91 * s), 40 * s, 9 * s, WOOD_HI)
    for k in range(3): F.dot(L, T((-20 + k * 18) * s, -92 * s), (110, 110, 118), 2.2 * s)          # crooked nails


def shavings(big, v, t, x, y, t0, n=14):
    """wood shavings flying off the plane (output px)"""
    for k in range(n):
        ph = ((t - t0) * 1.6 + k / n) % 1.0
        a = -1.2 + 2.4 * ((k * 37) % n) / n
        wx = x + math.cos(a) * 140 * ph; wy = y - 120 * ph + 160 * ph * ph
        ox, oy = v.opt(wx, wy); r = int(6 * v.Z)
        if 0 <= oy - r and oy + r < big.shape[0] and 0 <= ox - r and ox + r < big.shape[1]:
            big[int(oy - r):int(oy + r), int(ox - r * 1.6):int(ox + r * 1.6)] = (236, 196, 130)


def table_spread(CH, v):
    """Ira's table: olivier, a «Napoleon» cake, glasses and the handbell from E01"""
    L = Layer(v.wcam())
    F.ell(L, (930, 424), 40, 13, (240, 240, 236), 0, (255, 255, 255), (200, 200, 196))
    F.ell(L, (930, 416), 30, 10, (236, 216, 150)); [F.dot(L, (912 + k * 9, 414 + (k % 2) * 3), (90, 160, 70), 2.4) for k in range(5)]
    F.poly(L, [(990, 428), (1060, 428), (1056, 396), (994, 396)], (236, 210, 160))
    for k in range(4): F.cap(L, (994, 402 + k * 7), (1056, 402 + k * 7), 1.6, 1.6, (200, 160, 100))
    F.ell(L, (1025, 396), 31, 6, (250, 240, 220))
    for gx in (1090, 1120): F.cap(L, (gx, 426), (gx, 400), 5, 6, (220, 236, 246))
    B.bell(L, (1170, 412), 0.0, 0.0)
    F.outline(L, OL); CH.add(L)


# ---------------------------------------------------------------- worlds
def light_gar(v):
    bx, by = v.opt(530.0, 100.0); dx, dy = v.opt(1150.0, 300.0)
    return Light(amb=(0.98, 0.94, 0.9), keys=[(bx, by, 1300, (255, 200, 120), 0.65), (dx, dy, 900, (200, 220, 255), 0.4)],
                 rim=(1, -0.4, (190, 210, 255), 0.45), grad=(1.03, 0.88))


def garage(v, t, draw=None, after=None):
    return S.world(GAR, v, t, draw, light_gar(v), snow=(1080, 40, 1280, 500), motes=(380, 80, 760, 360), after=after)


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Двадцать девятое — День матери! Подарок делаем сами!» — Batya with a plane over a plank, shavings fly, calendar «29»"""
    z = 1.2 + 0.08 * sm(min(1.0, u / 4.0))
    v = view_at(GAR, 620, 330, z, 180, 330)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(600, GF + 40, 17.0)
        sw = 1.2 * math.sin(t * 9)
        r = B.batya(CH, cam, dict(B.BPOSE['stand'], bn=-1), t=t, mouth_=mouth('batya', t), expr='proud', hand_n=F.H(5.0 + sw, 13.0),
                    prop_n=plane)
        face(v_, cam, r, 3.2); st['h'] = u2w(v_, cam, F.H(5.0 + sw, 13.0))
    return garage(v, t, draw, after=lambda b, v_: shavings(b, v_, t, st['h'][0], st['h'][1], 0.0))


def r_selfie(t, u):
    """«Батя решил: магазин — для слабых. Мы в гараже.» — Tyoma's stream, Batya planing behind"""
    v = view_at(GAR, 560, 330, 1.0, 180, 320)

    def draw(CH, v_):
        cam = v_.cam(440, GF - 40, 14.0)
        B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=0.0, expr='proud', hand_n=F.H(5.0 + 1.2 * math.sin(t * 9), 14.5), prop_n=plane,
                hand_f=F.H(3.0, 14.0), prop_f=plank)
        cam = v_.cam(668, 1040, 26.0, flip=True)
        r = B.tema(CH, cam, B.TPOSE['selfie'], t=t, mouth_=mouth('tema', t), expr='deadpan', prop_n=None, hand_n=F.H(9.5, 17.0), look=0.6)
        face(v_, cam, r, 2.6)
    return garage(v, t, draw, after=lambda b, v_: K.phone_ui(b, t, '120 400'))


def r_measure(t, u):
    """«Рулетка не нужна. У меня глаз — алмаз!» — close: Batya squints one eye along a plank, the tape measure stays on his belt"""
    v = view_at(GAR, 600, 300, 1.35, 180, 300)

    def draw(CH, v_):
        cam = v_.cam(600, GF + 60, 18.0)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=mouth('batya', t), expr='smug', hand_n=F.H(7.0, 20.5), prop_n=plank,
                    hand_f=F.H(4.0, 20.0))
        face(v_, cam, r, 3.2)
    return garage(v, t, draw)


def r_stool(t, u):
    """«Табуретка. Три ноги. Это контент.» — the three-legged stool wobbles on the shavings, viewers 1 000 000"""
    v = view_at(GAR, 600, 420, 1.3, 180, 330)

    def draw(CH, v_):
        L = Layer(v_.wcam())
        stool(L, 600, 600, 1.6, 0.12 + 0.1 * math.sin(t * 6))
        F.outline(L, OL); CH.add(L)
    return garage(v, t, draw, after=lambda b, v_: K.phone_ui(b, t, '1 000 000'))


def r_tripod(t, u):
    """«Три ноги — устойчивее! Как штатив!» — Batya presents the stool, it wobbles"""
    v = view_at(GAR, 600, 340, 1.05, 180, 330)

    def draw(CH, v_):
        L = Layer(v_.wcam())
        stool(L, 690, GF - 10, 1.3, 0.12 + 0.08 * math.sin(t * 6))
        F.outline(L, OL); CH.add(L)
        cam = v_.cam(500, GF + 20, 15.5)
        r = B.batya(CH, cam, B.BPOSE['point'], t=t, mouth_=mouth('batya', t), expr='proud')
        face(v_, cam, r, 3.2)
    return garage(v, t, draw)


def r_twist(t, u):
    """«Витенька! Это мне?! Сынок, сам сделал!» — babushka Valentina in the garage door, then she hugs the stool"""
    z = 1.0 + 0.1 * sm(min(1.0, u / 3.0))
    v = view_at(GAR, 820, 340, z, 180, 330)
    k = sm(min(1.0, u / 1.6))

    def draw(CH, v_):
        L = Layer(v_.wcam())
        if u < 1.6: stool(L, 700, GF - 10, 1.3, 0.0)
        F.outline(L, OL); CH.add(L)
        cam = v_.cam(lerp(1000, 820, k), GF, 14.0, flip=True)
        held = (lambda A, h: stool(A, h[0] - 1.0, h[1] + 4.5, 0.055)) if u >= 1.6 else None
        r = B.babushka(CH, cam, B.IPOSE['tray'] if u >= 1.6 else dict(B.IPOSE['stand'], n=(4.5, 18.0), f=(-4.0, 18.0)), t=t,
                       mouth_=mouth('babushka', t), expr='happy', prop_n=held)
        face(v_, cam, r, 2.8)
    return garage(v, t, draw)


def r_mama(t, u):
    """«Мама… Вообще-то это для Иры…» — Batya, lost; babushka hugs the stool in the background"""
    v = view_at(GAR, 660, 320, 1.3, 180, 300)

    def draw(CH, v_):
        cam = v_.cam(820, GF - 20, 14.0, flip=True)
        r2 = B.babushka(CH, cam, B.IPOSE['tray'], t=t, mouth_=0.0, expr='sweet',
                        prop_n=lambda A, h: stool(A, h[0] - 1.0, h[1] + 4.5, 0.055))
        cam = v_.cam(560, GF + 50, 17.5)
        r = B.batya(CH, cam, B.BPOSE['stand'], t=t, mouth_=mouth('batya', t), expr='sad')
        face(v_, cam, r, 3.2)
    return garage(v, t, draw)


def r_table(t, u):
    """«Витя. Стол я накрыла сама. Садитесь.» — kitchen: the table is laid, the handbell from E01, Ira smiles"""
    v = view_at(KIT, 900, 330, 1.05, 180, 320)

    def draw(CH, v_):
        table_spread(CH, v_)
        cam = v_.cam(800, 670, UN, flip=False)
        r = B.ira(CH, cam, B.IPOSE['hips'], t=t, mouth_=mouth('ira', t), expr='happy')
        face(v_, cam, r, 2.6)
    return S.kitchen(v, t, draw)


def r_forehead(t, u):
    """«Витенька, ты похудел! И лоб горячий!» — babushka stands ON the three-legged stool to feel her son's forehead"""
    v = view_at(KIT, 860, 320, 1.1, 180, 320)

    def draw(CH, v_):
        table_spread(CH, v_)
        L = Layer(v_.wcam())
        stool(L, 800, 676, 1.2, 0.06 * math.sin(t * 7))
        F.outline(L, OL); CH.add(L)
        cam = v_.cam(920, 690, UN, flip=True)
        r = B.batya(CH, cam, B.BPOSE['stand'], t=t, mouth_=0.0, expr='sad')
        face(v_, cam, r, 3.2)
        fx_, fy_ = u2w(v_, cam, F.H(1.2, 26.4))
        bu = 13.5; bx, by = 800, 676 - 104
        cam2 = v_.cam(bx, by, bu)
        r2 = B.babushka(CH, cam2, B.IPOSE['stand'], t=t, mouth_=mouth('babushka', t), expr='worried', legs=True,
                        hand_n=F.H((fx_ - bx) / bu, (by - fy_) / bu))
        face(v_, cam2, r2, 2.8)
    return S.kitchen(v, t, draw)


def r_button(t, u):
    """«Мама… Тридцать семь и два…» — close: Batya, childlike and weak, babushka's palm on his forehead (callback to the pilot)"""
    v = view_at(KIT, 900, 260, 1.5, 180, 300)

    def draw(CH, v_):
        cam = v_.cam(920, 690, UN, flip=True)
        r = B.batya(CH, cam, B.BPOSE['stand'], t=t, mouth_=mouth('batya', t), expr='dying', sick=0.6)
        face(v_, cam, r, 3.2)
        fx_, fy_ = u2w(v_, cam, F.H(1.2, 26.4))
        bu = 13.5; bx, by = 800, 676 - 104
        cam2 = v_.cam(bx, by, bu)
        B.babushka(CH, cam2, B.IPOSE['stand'], t=t, mouth_=0.0, expr='worried', hand_n=F.H((fx_ - bx) / bu, (by - fy_) / bu))
    return S.kitchen(v, t, draw)


def r_loop(t, u):
    return r_hook(t, 0.0)


SHOT = dict(hook=r_hook, selfie=r_selfie, measure=r_measure, stool=r_stool, tripod=r_tripod, twist=r_twist, mama=r_mama,
            table=r_table, forehead=r_forehead, button=r_button, loop=r_loop)
CUTS, NAMES = TL.CUTS, TL.NAMES


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


QUESTION = K.question('СКОЛЬКО ЛЕТ ПОДАРКУ?', 'ПИШИ ЦИФРУ')


def extra(big, t, shot):
    if TL.DUR - 2.4 <= t < TL.DUR - 1.0:
        O.overlay(big, QUESTION, (big.shape[1] - QUESTION.shape[1]) // 2, 230, min(1.0, (t - (TL.DUR - 2.4)) / 0.12))


SHOW = K.Show(EPI, 1, 6, ['ДЕНЬ МАТЕРИ —', 'ПОДАРОК САМИ!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('ЭТО МНЕ?!', fg=(255, 170, 200), size=100), TL.TWIST + 0.3, F0['mama'], 540, 470),
                        (O.sticker('НА ГЛАЗ', fg=(255, 236, 120), size=80), F0['measure'] + 0.4, F0['stool'], 540, 440),
                        (O.sticker('37,2', fg=(255, 120, 120), size=120), F0['button'] + 1.2, TL.DUR - 2.4, 540, 470)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['twist'], F0['table']], extra=extra,
              cap_y={'selfie': 1460, 'stool': 1460}, cap_default=1400)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
