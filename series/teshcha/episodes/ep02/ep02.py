"""E02 «Сделай потише!» — 7 a.m., the mother-in-law watches her soap at volume 100. Tolik hides the remote in the freezer — she has
a spare one in her robe pocket. He puts wireless headphones on her: silence… TWIST (success worse than failure): she can't hear
herself and shouts at the soap for the whole block — «МАРИНА, НЕ ВЕРЬ ЕМУ! ОН ЖЕ ЖЕНАТ!», neighbours bang on the radiators. Button:
«Что, Толечка? Сделать погромче?» -> the volume bar climbs back to 100 (loop).
  python3 ep02.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props.teshshots import mouth, u2w, face, room, chair, raisa_sit, CHAIR, ROOM
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG, promo='ru',
              endcard=dict(style='teshcha', lang='ru', promise='ЗАВТРА: ТЁЩА И ГОЛОДНЫЙ ЗЯТЬ'))
SH.init(EPI, day=12)
KIT = SH.world('kitchen')
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0
TVX, TVY, TVS = 800.0, 690.0, 1.35          # the big TV in front of the armchair (floor point, scale)
FRIDGE_FREEZER = (112, 188, 352, 300)       # freezer door box on the kitchen fridge (bg px)

D.attach(KIT, [
    (R.plate(30, 38, ['ДЕНЬ', '12'], bg=(250, 248, 240), colors=[(184, 30, 40), (34, 28, 30)], border=(120, 110, 100), weights=[0.55, 1],
             stripe=((200, 40, 40), 0.3), pad=1.2), 70, 80),
    (R.plate(46, 16, ['НЕ ОТКРЫВАТЬ!'], bg=(255, 244, 170), colors=[(184, 30, 40)], border=(150, 130, 70), pad=1.0, tilt=-3), 186, 232),
    (R.plate(36, 14, ['СОЛЕНЬЯ'], bg=(250, 246, 230), colors=[(34, 28, 30)], border=(120, 110, 90), pad=0.9), 1000, 112),
    (R.plate(40, 14, ['РАДИО «МАЯК»'], bg=(236, 220, 180), colors=[(60, 40, 30)], border=(100, 80, 60), pad=0.9), 980, 300),
    (R.plate(42, 16, ['ГАЗ — ЗЛО'], bg=(250, 250, 240), colors=[(184, 30, 40)], border=(150, 140, 120), pad=1.0, tilt=2), 450, 300),
])


def light_kitchen(v):
    wx, wy = v.opt(620.0, 120.0)
    return Light(amb=(1.03, 0.98, 0.9), keys=[(wx, wy, 1300, (255, 220, 160), 0.6)], rim=(1, -0.4, (255, 230, 180), 0.35), grad=(1.04, 0.9))


def tv(CH, v, t, osd=100, x=TVX, y=TVY, s=TVS):
    L = Layer(v.wcam()); box = SH.tv_big(L, x, y, s, t, osd=osd); CH.add(L)
    return box


def waves(big, v, t, x, y, k=1.0, col=(255, 240, 160)):
    """loud sound rings flying out of the TV speaker"""
    for i in range(3):
        ph = (t * 1.6 + i / 3) % 1.0
        cx, cy = v.opt(x, y)
        r = (30 + 150 * ph) * v.Z * 3 * 0.5 * k
        a = 0.55 * (1 - ph) * k
        if a <= 0.02: continue
        yy, xx = np.ogrid[:big.shape[0], :big.shape[1]]
        ring = np.abs(np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) - r) < 7
        big[ring] = (big[ring] * (1 - a) + np.array(col) * a).astype(np.uint8)


def raisa_hp(CH, v, cam, r, on=True):
    """big red headphones over the curlers (drawn in Raisa's unit space; her head is scaled 1.2 around the neck)"""
    if not on: return
    hx, hy = r['head']
    L = Layer(cam)
    F.cap(L, (hx - 4.4, hy - 0.4), (hx - 2.6, hy - 5.6), 0.55, 0.55, (40, 40, 48))
    F.cap(L, (hx - 2.6, hy - 5.6), (hx + 0.6, hy - 6.0), 0.55, 0.55, (40, 40, 48))
    F.ell(L, (hx - 4.3, hy + 0.1), 1.25, 1.6, (220, 40, 60), 0, (250, 100, 110), (150, 20, 40))
    F.ell(L, (hx - 4.1, hy + 0.1), 0.55, 0.8, (120, 16, 30))
    F.outline(L, T.OL); CH.add(L)


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Раиса Захаровна! Семь утра, а телевизор на всю громкость!» — Tolik on the balcony camp bed, pillow over his head, yelling at the
    door; the TV roar comes through it (sound rings)"""
    big = SH.tolik_cu_balcony(t, u, expr='shout', pillow=True, shake=0.04, k=1.5)
    for i in range(3):
        ph = (t * 1.8 + i / 3) % 1.0
        x0 = int(-60 + 260 * ph); a = 0.6 * (1 - ph)
        if a > 0.05:
            yy, xx = np.ogrid[:big.shape[0], :big.shape[1]]
            ring = np.abs(np.sqrt((xx + 120) ** 2 + (yy - 980) ** 2) - (180 + 420 * ph)) < 9
            big[ring] = (big[ring] * (1 - a) + np.array((255, 240, 160)) * a).astype(np.uint8)
    return big


def r_tv_raisa(t, u):
    """«Что? Толечка, говори громче, у меня сериал!» — Raisa in HIS armchair, Pusya with ears flat on her lap, the TV roaring at 100"""
    v = view_at(ROOM, 712, 440, 1.12 + 0.03 * u, 180, 330)

    def draw(CH, v_):
        chair(CH, v_, 0.65, 'back')
        cam, r = raisa_sit(CH, v_, t, look=0.8, expr='sweet')
        px, py = u2w(v_, cam, r['lap'])
        T.pusya(CH, v_.cam(px, py + 2, 7.4), t=t, expr='deadpan', ears_down=True, shiver=1.4)
        chair(CH, v_, 0.65, 'front')
        tv(CH, v_, t, 100)
    big = room(v, t, draw, tv=1.0)
    waves(big, v, t, TVX + 30, TVY - 110)
    B.shake(big, t, 3, 33)
    return big


def r_freezer(t, u):
    """«Всё. Пульт — в морозилку.» — the kitchen: Tolik sneaks the remote into the freezer of the old fridge"""
    v = view_at(KIT, 330, 420, 1.2, 180, 330)
    k_open = sm(u / 0.3) * (1 - sm((u - 1.35) / 0.25))

    def draw(CH, v_):
        L = Layer(v_.wcam())
        if k_open > 0.05:                                                        # freezer door swung open, frosty inside
            x0, y0, x1, y1 = FRIDGE_FREEZER
            ST.wrect(L, x0, y0, x1, y1, (200, 226, 246))
            ST.wrect(L, x0 + 12, y0 + 12, x1 - 12, y1 - 12, (226, 240, 252))
            for i in range(6): F.ell(L, (x0 + 30 + i * 36, y0 + 40 + (i % 2) * 30), 10, 6, (255, 255, 255))
            ST.wrect(L, x1, y0, x1 + 90 * k_open, y1, (236, 232, 222))
        CH.add(L)
        c2 = v_.cam(450.0, 650.0, 12.5, flip=True)
        holding = u < 1.3
        r2 = T.tolik(CH, c2, dict(T.TPOSE['stand'], n=(5.6, 21.0)), t=t, mouth_=mouth('tolik', t), expr='smug', look=0.4,
                     prop_n=(lambda L_, h: SH.remote(L_, h, -2.4)) if holding else None)
        face(v_, c2, r2)
    return SH.generic(KIT, v, t, draw, light=light_kitchen(v), motes=(400, 80, 800, 360))


def r_spare(t, u):
    """«А у меня запасной пульт. Я без него из дома не выхожу!» — close on smug Raisa pulling the spare remote out of her robe pocket;
    the TV volume jumps back to 100"""
    s, un = 0.82, 15.0
    seat = CHAIR[1] - 64 * s
    fy = seat + 6.4 * un - 18.6 * un * 1.2
    v = view_at(ROOM, 690, fy + 60, 1.42, 180, 300)
    lift_ = sm((u - 0.6) / 0.6)

    def draw(CH, v_):
        chair(CH, v_, s, 'back')
        cam, r = raisa_sit(CH, v_, t, s=s, unit=un, look=0.4, expr='smug',
                           hand_n=F.H(lerp(4.4, 6.4, lift_), lerp(8.4, 15.6, lift_)),
                           prop_n=lambda L_, h: SH.remote(L_, h, -1.0))
        tv(CH, v_, t, 100 if u > 1.6 else 0, x=TVX + 40, y=TVY + 40, s=1.7)
    big = room(v, t, draw, tv=1.0)
    if u > 1.6: waves(big, v, t, TVX + 70, TVY - 140)
    return big


def r_headphones(t, u):
    """«Вот вам наушники. Тишина… Я в этом доме мужик!» — Tolik slips big headphones on her; the TV goes silent; he puffs his chest"""
    v = view_at(ROOM, 700, 430, 1.1, 180, 330)
    on = u > 0.7

    def draw(CH, v_):
        chair(CH, v_, 0.65, 'back')
        cam, r = raisa_sit(CH, v_, t, look=0.8, expr='sweet')
        raisa_hp(CH, v_, cam, r, on)
        chair(CH, v_, 0.65, 'front')
        x, y, un = 800.0, 664.0, 12.0
        pose = dict(T.TPOSE['stand'], n=(5.2, 23.0)) if u < 0.8 else T.TPOSE['fists']
        c2 = v_.cam(x, y, un, flip=True)
        r2 = T.tolik(CH, c2, pose, t=t, mouth_=mouth('tolik', t), expr='proud' if u > 1.5 else 'smug')
        face(v_, c2, r2)
        tv(CH, v_, t, 0, x=TVX + 40)
    return room(v, t, draw, tv=0.6)


def r_twist(t, u):
    """TWIST: «МАРИНА, НЕ ВЕРЬ ЕМУ! ОН ЖЕ ЖЕНАТ!» — punch-in on Raisa screaming at the soap in her headphones; shockwave, shake"""
    s, un = 0.82, 15.5
    seat = CHAIR[1] - 64 * s
    fy = seat + 6.4 * un - 18.6 * un * 1.2
    v = view_at(ROOM, 660, fy + 40, 1.38 + 0.06 * sm(u / 0.25), 180, 300)

    def draw(CH, v_):
        chair(CH, v_, s, 'back')
        cam, r = raisa_sit(CH, v_, t, s=s, unit=un, expr='shout', look=0.9,
                           pose=dict(T.RPOSE['sit'], n=(6.0, 15.6), f=(5.0, 15.2)))
        raisa_hp(CH, v_, cam, r, True)
    big = room(v, t, draw, tv=1.0)
    for i in range(3):                                                             # shockwave rings from her mouth
        ph = (u * 1.5 + i / 3) % 1.0
        yy, xx = np.ogrid[:big.shape[0], :big.shape[1]]
        ring = np.abs(np.sqrt((xx - 640) ** 2 + (yy - 900) ** 2) - (120 + 700 * ph)) < 10
        a = 0.6 * (1 - ph)
        big[ring] = (big[ring] * (1 - a) + np.array((255, 255, 255)) * a).astype(np.uint8)
    B.shake(big, t, 10, 40)
    return big


def r_bang(t, u):
    """the neighbours bang on the radiator: the radiator shakes, plaster dust falls from the ceiling"""
    v = view_at(ROOM, 1020, 330, 1.42, 180, 300)
    big = room(v, t)
    B.shake(big, t, 16, 47)
    rng = np.random.default_rng(int(t * 30))
    for _ in range(40):                                                            # ceiling dust
        x = int(rng.integers(0, 1080)); y = int((rng.random() * 600 + u * 900) % 1920)
        big[y:y + 8, x:x + 8] = (236, 230, 214)
    return big


def r_pusya(t, u):
    """«Я тут третий день ничего не слышу.» — Pusya on the armrest, ears pressed flat, deadpan to camera"""
    un = 21.0
    x, y = 660.0, 640.0
    v = view_at(ROOM, x, y - 5.2 * un, 1.38 + 0.05 * sm(u / 3.0), 180, 300)

    def draw(CH, v_):
        L = Layer(v_.wcam()); T.armchair(L, CHAIR[0] - 40, CHAIR[1] + 30, 1.1, 'back'); CH.add(L)
        cam = v_.cam(x, y, un)
        r = T.pusya(CH, cam, t=t, mouth_=mouth('pusya', t, 2.0), expr='deadpan', shiver=1.5, ears_down=True)
        face(v_, cam, r, 2.0)
    return room(v, t, draw, tv=1.0)


def r_panic(t, u):
    """«Раиса Захаровна, тише! Вы теперь громче телевизора!» — Tolik flapping his hands, Raisa in headphones happily oblivious"""
    v = view_at(ROOM, 700, 430, 1.12, 180, 330)

    def draw(CH, v_):
        chair(CH, v_, 0.65, 'back')
        cam, r = raisa_sit(CH, v_, t, look=0.8, expr='sweet')
        raisa_hp(CH, v_, cam, r, True)
        chair(CH, v_, 0.65, 'front')
        x, y, un = 800.0, 664.0, 12.0
        c2 = v_.cam(x, y, un, flip=True)
        wob = 1.2 * math.sin(t * 14)
        r2 = T.tolik(CH, c2, dict(T.TPOSE['shock'], n=(5.2 + wob * 0.3, 20.4 + wob), f=(-3.6, 20.6 - wob)), t=t,
                     mouth_=mouth('tolik', t), expr='shout', shake=0.05)
        face(v_, c2, r2)
    return room(v, t, draw, tv=1.0)


def r_button(t, u):
    """«Что, Толечка? Сделать погромче?» — close on Raisa sweetly lifting one ear cup"""
    s, un = 0.82, 15.0
    seat = CHAIR[1] - 64 * s
    fy = seat + 6.4 * un - 18.6 * un * 1.2
    v = view_at(ROOM, 680, fy + 50, 1.42, 180, 300)

    def draw(CH, v_):
        chair(CH, v_, s, 'back')
        cam, r = raisa_sit(CH, v_, t, s=s, unit=un, expr='sweet', look=0.6,
                           pose=dict(T.RPOSE['sit'], f=(-1.6, 18.4)))
        raisa_hp(CH, v_, cam, r, True)
    return room(v, t, draw, tv=1.0)


def r_loop(t, u):
    """the TV volume bar shoots back up to 100 -> loop into the opening shout"""
    v = view_at(ROOM, TVX - 10, TVY - 90, 1.42, 180, 330)

    def draw(CH, v_):
        tv(CH, v_, t, int(min(100, 20 + 160 * u)), s=1.7)
    big = room(v, t, draw, tv=1.0)
    waves(big, v, t, TVX + 30, TVY - 140)
    return big


SHOT = dict(hook=r_hook, tv_raisa=r_tv_raisa, freezer=r_freezer, spare=r_spare, headphones=r_headphones, twist=r_twist, bang=r_bang,
            pusya=r_pusya, panic=r_panic, button=r_button, loop=r_loop)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 2, ['7 УТРА.', 'ГРОМКОСТЬ 100!'], hook_t=(0.06, 2.8), hook_y=200,
              stickers=[(O.sticker('ГРОМКОСТЬ 100', fg=(110, 255, 130), size=56), F0['tv_raisa'] + 0.3, F0['freezer'], 720, 560),
                        (O.sticker('В МОРОЗИЛКУ!', fg=(170, 220, 255), size=60), F0['freezer'] + 0.6, F0['spare'], 540, 520),
                        (O.sticker('МАРИНА!!!', fg=(255, 120, 150), size=90), TL.TWIST + 0.4, F0['bang'], 540, 560),
                        (O.sticker('БУМ! БУМ!', fg=(255, 222, 80), size=96), F0['bang'] + 0.05, F0['pusya'], 540, 900)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['tv_raisa'], F0['freezer'], F0['spare']],
              cap_y={'hook': 1500, 'pusya': 1420, 'twist': 1450, 'spare': 1450, 'button': 1450}, cap_default=1340)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
