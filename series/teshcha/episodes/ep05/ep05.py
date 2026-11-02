"""E05 «Пятьдесят голосовых!» — at the window shop Tolik gets 50 voice messages from the mother-in-law («купи хлеба… а в 79-м
году…»), mutes her: «Хлеб куплю — и хватит.» At home he bursts in to tell her off — the flat is empty. TWIST (the hunter asks for
help): the last voice message, 40 minutes old: «Толечка… я в лифте застряла. Помоги.» He prises the lift open; for the first time she
says, without sugar: «Спасибо, Толя. Ты… мужик.» — «Я в этом доме мужик!» Button: Lyusya steps out of the lift with a suitcase:
«А мы тоже на недельку!»
  python3 ep05.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
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

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=dict(K.COL, lyusya=(200, 140, 255), raisa_vm=K.COL['raisa']), slug=TL.SLUG,
              promo='ru', endcard=dict(style='teshcha', lang='ru', promise='ЗАВТРА: ТЁЩА УЕЗЖАЕТ?!'))
SH.init(EPI, day=230)
OFF = SH.world('office')
HALL = SH.world('hallway')
LAND = SH.LAND
F0 = TL.T0
RED = (184, 30, 40)
YEL = (255, 244, 170)
LIFT = (242, 96, 410, 500)


def _p(lines, w, h, bg=(250, 248, 240), fg=(34, 28, 30), border=(120, 110, 100), tilt=0, stripe=None, weights=None):
    kw = dict(bg=bg, colors=[fg] * len(lines), border=border, pad=1.0, tilt=tilt)
    if stripe: kw['stripe'] = stripe
    if weights: kw['weights'] = weights
    return R.plate(w, h, lines, **kw)


D.attach(OFF, [
    (_p(['ОКНА', 'ЛЮКС'], 74, 52, bg=(250, 214, 80), fg=(40, 60, 150), border=(150, 110, 30)), 882, 160),
    (_p(['ПЛАН ПРОДАЖ:', '40 ОКОН', 'ПРОДАНО: 2'], 78, 56, bg=(236, 246, 240), fg=(30, 80, 60), border=(60, 100, 80), weights=[0.8, 1, 0.8]),
     212, 230),
    (_p(['ЛИЧНЫЕ ЗВОНКИ — НЕЛЬЗЯ!'], 120, 16, bg=YEL, fg=RED, border=(150, 130, 70)), 590, 428),
    (_p(['9 990 Р.'], 44, 14, bg=(250, 250, 250), fg=RED, border=RED, tilt=-4), 325, 286),
    (_p(['ВОДА', 'КЛИЕНТАМ'], 46, 20, bg=(220, 236, 250), fg=(40, 60, 150)), 1172, 362),
])
D.attach(HALL, [
    (_p(['ДЕНЬ', '230'], 30, 38, fg=RED, stripe=((200, 40, 40), 0.3), weights=[0.55, 1]), 205, 160),
    (_p(['ТОЛЕЧКА,', 'КУПИ ХЛЕБА!'], 54, 28, bg=YEL, fg=RED, border=(150, 130, 70), tilt=-4), 1092, 300),
    (_p(['ТАПКИ ТОЛИКА'], 58, 12, bg=(236, 206, 120), border=(120, 84, 30)), 790, 508),
])
D.attach(LAND, [
    (_p(['ЛИФТ ИСПРАВЕН.', 'ПОЧТИ.'], 110, 26, bg=(250, 250, 240), fg=(40, 60, 150), weights=[1, 0.8]), 272, 62),
])


def light_off(v):
    lx, ly = v.opt(640.0, 40.0)
    return Light(amb=(1.0, 1.0, 1.02), keys=[(lx, ly, 1300, (240, 246, 255), 0.4)], rim=(1, -0.4, (255, 220, 180), 0.35), grad=(1.03, 0.92))


def light_hall(v):
    lx, ly = v.opt(610.0, 80.0)
    return Light(amb=(1.02, 0.96, 0.88), keys=[(lx, ly, 1200, (255, 210, 140), 0.55)], rim=(-1, -0.4, (255, 220, 170), 0.3), grad=(1.04, 0.9))


def office(v, t, draw=None, after=None):
    return SH.generic(OFF, v, t, draw, light=light_off(v), motes=(400, 80, 900, 360), after=after)


def hall(v, t, draw=None, after=None):
    return SH.generic(HALL, v, t, draw, light=light_hall(v), motes=(450, 60, 800, 300), after=after)


def landing(v, t, draw=None):
    return SH.generic(LAND, v, t, draw, light=K.light_landing(v), motes=(520, 40, 780, 300), vign=0.3)


def loaf(L, h):
    F.cap(L, (h[0] - 1.6, h[1] + 0.6), (h[0] + 2.4, h[1] - 1.0), 0.75, 0.7, (214, 160, 80), (240, 196, 120), (170, 116, 50))
    for k in range(3): F.cap(L, (h[0] - 0.6 + k * 1.0, h[1] + 0.4 - k * 0.4), (h[0] - 0.2 + k * 1.0, h[1] - 0.2 - k * 0.4), 0.1, 0.1, (150, 100, 40))


def tolik(CH, v, t, x, y, un, flip=False, pose='stand', expr='normal', m=None, **kw):
    cam = v.cam(x, y, un, flip=flip)
    pp = T.TPOSE[pose] if isinstance(pose, str) else pose
    r = T.tolik(CH, cam, pp, t=t, mouth_=mouth('tolik', t) if m is None else m, expr=expr, **kw)
    face(v, cam, r)
    return cam, r


def raisa(CH, v, t, x, y, un, pose='stand', expr='sweet', flip=False, pal=None, who='raisa', **kw):
    cam = v.cam(x, y, un, flip=flip)
    pp = T.RPOSE[pose] if isinstance(pose, str) else pose
    r = T.raisa(CH, cam, pp, t=t, mouth_=mouth(who, t), expr=expr, pal=pal, **kw)
    face(v, cam, r, 3.6)
    return cam, r


# ---------------------------------------------------------------- the phone screen insert (screen space, full res)
def phone_ui(big, u, items, header='ТЁЩА', sub='50 голосовых'):
    im = Image.fromarray(big).filter(ImageFilter.GaussianBlur(14))
    out = (np.asarray(im).astype(np.float32) * 0.5).astype(np.uint8)
    W_, H_ = 640, 1080
    ph = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(ph)
    d.rounded_rectangle((0, 0, W_ - 1, H_ - 1), 60, fill=(30, 30, 36, 255), outline=(10, 10, 12, 255), width=8)
    d.rounded_rectangle((28, 90, W_ - 28, H_ - 90), 24, fill=(222, 232, 216, 255))
    d.rectangle((28, 90, W_ - 28, 220), fill=(80, 140, 210, 255))
    d.text((W_ // 2, 135), header, font=O.pfont(46), fill=(255, 255, 255, 255), anchor='mm')
    d.text((W_ // 2, 190), sub, font=O.pfont(28), fill=(220, 236, 255, 255), anchor='mm')
    y = 250
    for it in items:
        if it[0] == 'card':                                                            # «Доброе утро!» postcard with roses
            d.rounded_rectangle((60, y, 420, y + 200), 20, fill=(255, 236, 244, 255), outline=(220, 120, 160, 255), width=4)
            for k in range(5):
                cx, cy = 100 + k * 72, y + 150 + (k % 2) * 14
                d.ellipse((cx - 26, cy - 22, cx + 26, cy + 22), fill=(206, 34, 84, 255)); d.ellipse((cx - 12, cy - 10, cx + 10, cy + 8), fill=(240, 86, 124, 255))
            d.text((240, y + 50), 'ДОБРОЕ УТРО!', font=O.pfont(30), fill=(184, 30, 90, 255), anchor='mm')
            y += 222
        else:                                                                          # a voice message bubble
            _, dur, prog, hl = it
            col = (255, 250, 220, 255) if hl else (255, 255, 255, 255)
            d.rounded_rectangle((60, y, 520, y + 92), 30, fill=col, outline=(190, 200, 190, 255), width=3)
            d.ellipse((76, y + 16, 136, y + 76), fill=(80, 140, 210, 255))
            d.polygon([(98, y + 30), (98, y + 62), (124, y + 46)], fill=(255, 255, 255, 255))
            rng = np.random.default_rng(y)
            for k in range(26):
                hgt = 8 + rng.random() * 30
                xk = 152 + k * 10
                c = (80, 140, 210, 255) if (prog is not None and k / 26 < prog) else (150, 160, 170, 255)
                d.rectangle((xk, y + 46 - hgt / 2, xk + 5, y + 46 + hgt / 2), fill=c)
            d.text((505, y + 72), dur, font=O.pfont(26), fill=(110, 116, 124, 255), anchor='rm')
            if hl and isinstance(hl, str):
                d.text((300, y + 118), hl, font=O.pfont(30), fill=(184, 30, 40, 255), anchor='mm')
                y += 40
            y += 110
    a = np.asarray(ph)
    sc = 0.9 + 0.1 * sm(u / 0.18)
    if sc < 1.0: a = np.asarray(ph.resize((int(W_ * sc), int(H_ * sc)), Image.NEAREST))
    O.overlay(out, a, (out.shape[1] - a.shape[1]) // 2, 330, 1.0)
    return out


# ---------------------------------------------------------------- office
def r_hook(t, u):
    """«Пятьдесят голосовых от тёщи! Я же на работе!» — Tolik in the window shop, the phone buzzing nonstop in his hand"""
    v = view_at(OFF, 660, 300 + 10 * sm(u / 3), 1.26 - 0.04 * sm(u / 3), 180, 300)
    jit = 0.25 * math.sin(t * 70)

    def draw(CH, v_):
        cam, r = tolik(CH, v_, t, 660, 660, 15.0, pose='phone', expr='shock', look=0.6,
                       prop_n=lambda L, h: T.phone(L, (h[0] + jit, h[1]), -1.75))
        hx, hy = r['hand_n']
        L = Layer(cam)
        for k in range(3):                                                           # buzz arcs
            rr = 1.4 + k * 0.7 + (t * 6 % 0.7)
            F.cap(L, (hx + 1.2 + rr * 0.6, hy - 2.4 - rr * 0.3), (hx + 1.6 + rr * 0.7, hy - 1.0), 0.09, 0.09, (255, 236, 120))
        CH.add(L)
    return office(v, t, draw)


def r_vm1(t, u):
    """«Толечка, купи хлеба. А ещё я тебе расскажу, как в семьдесят девятом году…» — the chat: postcards and 4-minute voice notes"""
    big = office(view_at(OFF, 660, 400, 1.3, 180, 300), t)
    items = [('card',), ('vm', '4:12', None, False), ('vm', '3:47', None, False), ('vm', '6:05', min(1.0, u / 6.0), True)]
    return phone_ui(big, u, items)


def r_mute(t, u):
    """«Всё, ставлю без звука. Хлеб куплю — и хватит.» — close on Tolik, decisive thumb on the button"""
    un = 15.0 * 1.3
    v = view_at(OFF, 640, 660 + 50 - 27 * un + 30, 1.42, 180, 300)

    def draw(CH, v_):
        tolik(CH, v_, t, 650, 710, un, pose='phone', expr='smug', prop_n=lambda L, h: T.phone(L, h, -1.75))
    return office(v, t, draw)


# ---------------------------------------------------------------- home
def r_pusya(t, u):
    """«Хлеб — это только начало.» — Pusya on the armchair at home, deadpan to camera"""
    un = 21.0
    x, y = 660.0, 640.0
    v = view_at(SH.ROOM, x, y - 5.2 * un, 1.38 + 0.05 * sm(u / 3.0), 180, 300)

    def draw(CH, v_):
        L = Layer(v_.wcam()); T.armchair(L, SH.CHAIR[0] - 40, SH.CHAIR[1] + 30, 1.1, 'back'); CH.add(L)
        cam = v_.cam(x, y, un)
        r = T.pusya(CH, cam, t=t, mouth_=mouth('pusya', t, 2.0), expr='deadpan', shiver=1.2)
        face(v_, cam, r, 2.0)
    return SH.room(v, t, draw)


def r_home(t, u):
    """«Раиса Захаровна, хватит мне писать! … Раиса Захаровна?» — he bursts into the hallway with a loaf; nobody, silence"""
    v = view_at(HALL, 760, 380 + 20 * sm((u - 1.6) / 1.0), 1.2, 180, 300)
    unsure = u > 1.9

    def draw(CH, v_):
        tolik(CH, v_, t, 840 + 40 * (1 - sm(u / 0.5)), 692, 15.0, flip=True, pose='stand' if unsure else 'fists',
              expr='sad' if unsure else 'angry', look=math.sin(t * 3) * 0.8 if unsure else 0.0, prop_n=loaf)
    return hall(v, t, draw)


def r_twist(t, u):
    """TWIST: the last voice message, 40 minutes old, quiet: «Толечка… я в лифте застряла. С сумками. Помоги.»"""
    big = hall(view_at(HALL, 760, 400, 1.2, 180, 300), t)
    items = [('vm', '6:05', None, False), ('vm', '2:31', None, False), ('vm', '0:09', min(1.0, u / 3.9), '40 мин. назад')]
    return phone_ui(big, u, items, sub='последнее сообщение')


# ---------------------------------------------------------------- landing: the lift
def lift_inside(L):
    x0, y0, x1, y1 = LIFT
    ST.wrect(L, x0, y0, x1, y1, (40, 36, 42)); ST.wrect(L, x0, y1 - 30, x1, y1, (66, 58, 54))
    ST.wrect(L, x0 + 20, y0 + 10, x1 - 20, y0 + 22, (250, 240, 200))                     # the dim lift lamp


def lift_doors(L, k):
    x0, y0, x1, y1 = LIFT
    mid = (x0 + x1) / 2; gap = (x1 - x0) / 2 * k
    ST.wrect(L, x0, y0, mid - gap, y1, (92, 94, 98)); ST.wrect(L, mid + gap, y0, x1, y1, (92, 94, 98))
    for xx in (x0 + 10, x1 - 14): ST.wrect(L, xx, y0 + 6, xx + 4, y1 - 6, (120, 124, 128))
    ST.wrect(L, mid - gap - 3, y0, mid - gap, y1, (60, 58, 56)); ST.wrect(L, mid + gap, y0, mid + gap + 3, y1, (60, 58, 56))


def pusya_held(CH, v, cam, r, t, un=5.6):
    wx, wy = u2w(v, cam, r['hand_n'])
    c = v.cam(wx - 4, wy + 2.6 * un, un)
    rp = T.pusya(CH, c, t=t, expr='shock', shiver=1.6)
    face(v, c, rp, 2.0)


def r_lift(t, u):
    """«Держитесь, Раиса Захаровна! Я иду!» — Tolik prises the lift doors apart; inside, Raisa with the bags and Pusya"""
    v = view_at(LAND, 380, 360, 1.15, 180, 330)
    k = 0.12 + 0.55 * sm((u - 0.6) / 1.4) + 0.02 * math.sin(t * 30)

    def draw(CH, v_):
        L = Layer(v_.wcam()); lift_inside(L); CH.add(L)
        cam, r = raisa(CH, v_, t, 326, 500, 9.5, pose='hold', expr='shock')
        L = Layer(v_.wcam()); T.chelnok(L, 286, 500, 46, 36, 0.1, 3); T.chelnok(L, 370, 500, 44, 34, -0.1, 5); CH.add(L)
        pusya_held(CH, v_, cam, r, t, 3.4)
        L = Layer(v_.wcam()); lift_doors(L, k); CH.add(L)
        tolik(CH, v_, t, 470, 600, 12.5, flip=True, pose=dict(T.TPOSE['stand'], n=(5.2, 18.6), f=(4.6, 18.2), bn=1, bf=1, nleg=(0.3, 0.0),
                                                              fleg=(-0.25, 0.0)), expr='angry', shake=0.06)
    big = landing(v, t, draw)
    if u > 1.4: B.shake(big, t, 4, 30)
    return big


def r_thanks(t, u):
    """«Спасибо, Толя. Ты… мужик.» — Raisa out of the lift, Pusya in her arms, for once sincere, no sugar"""
    x, y, un = 470.0, 640.0, 15.0 * 1.25
    v = view_at(LAND, x + 50, y + 50 - 21 * un + 30, 1.4, 180, 300)

    def draw(CH, v_):
        cam, r = raisa(CH, v_, t, x, y + 50, un, pose='hold', expr='sweet', look=0.5)
        pusya_held(CH, v_, cam, r, t, 7.0)
    return landing(v, t, draw)


def r_proud(t, u):
    """«Я в этом доме мужик!» — Tolik, moved, fist on chest, a tear rolls"""
    x, y, un = 560.0, 640.0, 15.0 * 1.3
    v = view_at(LAND, x - 20, y + 50 - 27 * un + 60, 1.42, 180, 300)

    def draw(CH, v_):
        cam, r = tolik(CH, v_, t, x, y + 50, un, flip=True, pose='proud', expr='proud')
        hx, hy = r['head']
        L = Layer(cam)
        for k in range(2):
            ty = hy + 0.4 + ((u * 1.2 + k * 0.5) % 1.0) * 2.4
            F.ell(L, (hx + 0.4 + k * 1.2, ty), 0.28, 0.4, (150, 210, 255), 0, (230, 246, 255), (90, 160, 230))
        CH.add(L)
    return landing(v, t, draw)


def r_button(t, u):
    """«А мы тоже на недельку!» — the lift opens again: Lyusya with a suitcase; Tolik freezes"""
    v = view_at(LAND, 420, 380, 1.12, 180, 330)
    k = sm(u / 0.35)

    def draw(CH, v_):
        L = Layer(v_.wcam()); lift_inside(L); CH.add(L)
        x = 326 + 70 * sm((u - 0.3) / 0.8)
        cam, r = raisa(CH, v_, t, x, 520 + 60 * sm((u - 0.3) / 0.8), 12.5, pose='offer', expr='sweet', pal=T.LYUSYA, who='lyusya')
        wx, wy = u2w(v_, cam, r['hand_n'])
        L = Layer(v_.wcam()); T.chelnok(L, wx + 24, wy + 40, 70, 54, 0.15, 11); CH.add(L)
        L = Layer(v_.wcam()); lift_doors(L, k); CH.add(L)
        tolik(CH, v_, t, 535, 640, 12.5, flip=True, pose='shock', expr='shock', m=0.6)
    return landing(v, t, draw)


def r_loop(t, u):
    big = r_hook(t, u + 0.5)
    fx.speed_lines(big, t, 0.8)
    return big


SHOT = dict(hook=r_hook, vm1=r_vm1, mute=r_mute, pusya=r_pusya, home=r_home, twist=r_twist, lift=r_lift, thanks=r_thanks,
            proud=r_proud, button=r_button, loop=r_loop)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 5, ['50 ГОЛОСОВЫХ', 'ОТ ТЁЩИ!'], hook_t=(0.06, 2.8), hook_y=200,
              stickers=[(O.sticker('БЕЗ ЗВУКА', fg=(150, 200, 255), size=78), F0['mute'] + 1.1, F0['pusya'], 540, 560),
                        (O.sticker('ЛИФТ!', fg=(255, 120, 150), size=120), TL.TWIST + 0.4, F0['lift'], 540, 1290),
                        (O.sticker('ТОЖЕ?!', fg=(200, 140, 255), size=110), F0['button'] + 0.5, F0['loop'], 540, 520)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['pusya'], F0['lift']],
              cap_y={'hook': 1500, 'vm1': 1640, 'twist': 1640, 'pusya': 1450}, cap_default=1380)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
