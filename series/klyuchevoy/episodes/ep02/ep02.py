"""S01E02 «ПРЕМИИ НЕ БУДЕТ?!» (34.6 s, twist at 17.60 s / 51 %, type: the villain is one of us — Эдик himself).
Main question (opened at 0 s, closed at ~55 %): who stole Эдик's bonus?
HOOK: the cash window, Людмила stamps «ОТКАЗАНО»: «Эдуард, премии в этом году не будет.» — «Как не будет?! Я уже посчитал: сорок
тысяч!» (calculator tape: РЕЗИНА 15 000 / ШУБА 20 000 / ПИВО 5 000). Фикус: «Шуба за двадцать — это шапка.» Людмила: «Не положено. Треть
компаний премию не платит.» (1/3). Эдик with a loupe: «Тогда я найду, кто украл мою премию!» — the cooler, the boss's door («Теплее.»), the
honor board («Горячо.»). TWIST: the sheet «РАЦПРЕДЛОЖЕНИЕ ГОДА: ЭКОНОМИТЬ НА ВСЁМ! — Э. БУЛКИН» with Эдик's thumbs-up photo. «Это я в
январе… для галочки!» — the boss hugs him: «А мы приняли! Мы же одна семья!» — «В семье тоже не платят.» — «Зато вот тебе грамота! За
экономию!» — it is printed on the back of an invoice for 40 000. «На обороте счёта?!» — «У каждого в офисе есть такой экономист. Отправь ему.»
Clue in the first half: the sheet with Эдик's photo is on the honor board in every office shot.
  python3 ep02.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import fx
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import kscast as C
from props import kskit as K
from props import decals as D
from props import rusigns as R
from props import mimic as M
from props.kskit import at, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T0

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='ks', lang='ru', promise='ЗАВТРА: КОРПОРАТИВ'),
              promo='ru')
TAB = (C.XTRA, C.EXPR)
FE = M.Face([(0.0, 'hopeful'), (0.3, 'shock'), (2.7, 'shock'), (4.0, 'bark'), (13.0, 'scheme'), (15.7, 'hopeful'), (17.6, 'shock'),
             (18.55, 'pleading'), (21.45, 'nervous'), (24.3, 'crushed'), (26.3, 'hopeful'), (29.7, 'shock'), (31.4, 'crushed')], TAB, seed=3)
FF = M.Face([(0.0, 'deadpan'), (6.45, 'smirk'), (8.5, 'deadpan'), (24.3, 'smirk'), (31.4, 'deadpan')], TAB, seed=8)
FL = M.Face([(0.0, 'strict'), (9.98, 'strict'), (11.5, 'smirk')], TAB, seed=11)
FS = M.Face([(0.0, 'boss'), (21.45, 'sweet'), (26.3, 'boss')], TAB, seed=5)

# the clue: the rationalisation sheet with Эдик's photo on the honor board (office worlds)
for _n in ('office', 'office_night', 'office_morning'):
    D.attach(K.world(_n), [(R.plate(52, 56, ['РАЦПРЕДЛОЖЕНИЕ', 'ГОДА:', 'ЭКОНОМИТЬ', 'НА ВСЁМ!', '— Э. БУЛКИН'], bg=(252, 250, 240),
                                     colors=[(40, 70, 130), (40, 70, 130), (190, 40, 40), (190, 40, 40), (34, 30, 28)], border=None,
                                     pad=1.0, weights=[0.7, 0.7, 1, 1, 0.7]), 404, 184)])


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def kw_(F, who, t, base=(0.7, 0.0), **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def ekw(t, base=(0.7, 0.0), **kw): return kw_(FE, 'edik', t, base, **kw)
def fkw(t, base=(0.0, 0.0), **kw): return kw_(FF, 'fikus', t, base, **kw)
def lkw(t, base=(-0.7, 0.0), **kw): return kw_(FL, 'lyuda', t, base, **kw)
def skw(t, base=(0.7, 0.0), **kw): return kw_(FS, 'shef', t, base, **kw)


def glass(big, v, k=0.22):
    """the cash window pane: a cool tint + two diagonal glints"""
    x0, y0 = v.opt(470.0, 145.0); x1, y1 = v.opt(835.0, 415.0)
    xa, xb, ya, yb = int(max(0, x0)), int(min(OUT_W, x1)), int(max(0, y0)), int(min(OUT_H, y1))
    if xa >= xb or ya >= yb: return
    reg = big[ya:yb, xa:xb].astype(np.float32)
    reg = reg * (1 - k) + np.array((200, 230, 230)) * k
    yy, xx = np.mgrid[ya:yb, xa:xb]
    for off, w in ((0.25, 26), (0.38, 12)):
        m = np.abs((xx - xa) + (yy - ya) * 0.8 - (xb - xa) * off * 2) < w
        reg[m] = reg[m] * 0.6 + 255 * 0.4
    big[ya:yb, xa:xb] = reg.astype(np.uint8)


def stamp_fx(big, x, y, t, t0, text='ОТКАЗАНО'):
    if t < t0: return
    img = O.sticker(text, fg=(230, 50, 50), size=48)
    k = min(1.0, (t - t0) / 0.08)
    O.overlay(big, img, int(x - img.shape[1] / 2), int(y - img.shape[0] / 2), k)


# ================================================================== 0: HOOK — the cash window, «ОТКАЗАНО»
def r_hook(t, u):
    Z = 1.15
    cx, cy = 620.0, 330.0
    v = K.V('kassa', cx, cy, Z)
    ly = at(C.lyuda, v, 720, 900, 16.0, pin='head', near=0.99, **lkw(t, (-0.8, -0.2), hand_n=(10.0, 44.0) if (t % 1.2) < 0.6 or t > 0.9 else (10.0, 36.0)))
    ed = at(C.edik, v, 300, 1300, 24.0, pin='head', near=0.99, **ekw(t, (0.9, 0.2), hand_n=(18.0, 58.0), prop_n=lambda sp, h: C.calc(sp, h)))
    def f(big, v_):
        glass(big, v_)
        stamp_fx(big, 760, 1090, t, 0.85)
    return K.shot('kassa', cx, cy, Z, acts=[ly, ed], par=(-6 + 8 * u, 0), t=t, dof_k=18, fx_=f, kick=kick(t, [(0.85, 0.6)]))


# ================================================================== 1: «Как не будет?! Я уже посчитал: сорок тысяч!»
def r_e1cu(t, u):
    Z = 1.3
    cx, cy = 620.0, 300.0
    v = K.V('kassa', cx, cy, Z)
    ed = at(C.edik, v, 540, 820, 33.0, pin='head', near=0.99,
            **ekw(t, (0.6, 0.0), sweat=1.0, hand_n=(17.0, 52.0 + 2 * math.sin(t * 9)), prop_n=lambda sp, h: C.calc(sp, h)))
    return K.shot('kassa', cx, cy, Z, acts=[ed], par=(4 * u, 0), t=t, dof_k=36)


# ================================================================== 2: INSERT — the calculator tape
def r_calc(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    yy = np.linspace(0, 1, OUT_H)[:, None, None]
    big[:] = (np.array((70, 64, 60)) * (1 - yy) + np.array((40, 36, 34)) * yy).astype(np.uint8)
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([170, 980, 910, 1820], 40, fill=(96, 96, 104), outline=(30, 30, 34), width=10)
    d.rectangle([230, 1040, 850, 1190], fill=(150, 220, 150), outline=(30, 30, 34), width=8)
    n = min(3, int(u / 0.45) + 1)
    total = [15000, 35000, 40000][n - 1]
    tt = f'{total:,}'.replace(',', ' ')
    f = O.pfont(80)
    d.text((820 - f.getlength(tt), 1075), tt, font=f, fill=(20, 50, 20))
    for r in range(4):
        for c in range(4): d.rounded_rectangle([250 + c * 150, 1250 + r * 135, 360 + c * 150, 1350 + r * 135], 14, fill=(214, 214, 206))
    rows = [('РЕЗИНА', '15 000'), ('ШУБА', '20 000'), ('ПИВО', '5 000')][:n]
    h_ = 160 + 110 * len(rows) + (130 if n == 3 else 0)
    d.rectangle([250, 960 - h_, 830, 980], fill=(250, 248, 238))
    for i, (a, b) in enumerate(rows):
        y = 960 - h_ + 60 + i * 110
        d.text((280, y), a, font=O.pfont(40), fill=(40, 40, 44)); d.text((800 - O.pfont(40).getlength(b), y), b, font=O.pfont(40), fill=(40, 40, 44))
    if n == 3:
        y = 960 - h_ + 60 + 3 * 110
        d.line([(280, y - 20), (800, y - 20)], fill=(40, 40, 44), width=6)
        d.text((280, y), 'ИТОГО', font=O.pfont(44), fill=(190, 40, 40)); d.text((800 - O.pfont(44).getlength('40 000'), y), '40 000', font=O.pfont(44), fill=(190, 40, 40))
    return np.array(im)


# ================================================================== 3/11/14: FIKUS close-up on the windowsill
def r_fik(t, u, name='office'):
    Z = 1.35 + 0.05 * u
    cx, cy = 1020.0, 250.0
    v = K.V(name, cx, cy, Z)
    fk = at(C.fikus, v, 540, 900, 22.0, pin='head', near=0.99, **fkw(t))
    return K.shot(name, cx, cy, Z, acts=[fk], par=(-4 + 8 * u, 0), t=t, dof_k=30, clock='11:20')


# ================================================================== 4: Людмила close-up — «Не положено. Треть компаний…»
def r_l2cu(t, u):
    Z = 1.45
    cx, cy = 650.0, 280.0
    v = K.V('kassa', cx, cy, Z)
    ly = at(C.lyuda, v, 540, 900, 26.0, pin='head', near=0.99, **lkw(t, (0.0, 0.0), hand_n=(9.0, 40.0), prop_n=lambda sp, h: C.mug(sp, h, 'ЛЮДА')))
    def f(big, v_): glass(big, v_, 0.18)
    return K.shot('kassa', cx, cy, Z, acts=[ly], par=(-4 + 6 * u, 0), t=t, dof_k=30, fx_=f)


# ================================================================== 5: the hunt — under the cooler with a loupe
def r_cooler(t, u):
    Z = 1.25
    cx, cy = 1120.0, 420.0
    v = K.V('office', cx, cy, Z)
    ed = K.A(C.edik, 1050.0, 600.0, K.ws_at(600.0) * 3 * Z, flip=False, lean=4.0,
             **ekw(t, (0.9, -0.6), hand_n=(22.0, 34.0 + 2 * math.sin(t * 6)), prop_n=lambda sp, h: C.loupe(sp, h)))
    fk = K.A(C.fikus, 1040.0, 372.0, 2.9 * 3 * Z, **fkw(t))
    return K.shot('office', cx, cy, Z, acts=[fk, ed], par=(-6 + 10 * u, 0), t=t, dof_k=16, clock='11:22')


# ================================================================== 6: at the boss's door — «Теплее.»
def r_door(t, u):
    Z = 1.15
    cx, cy = 220.0, 360.0
    v = K.V('office', cx, cy, Z)
    ed = K.A(C.edik, 230.0, 545.0, K.ws_at(545.0) * 3 * Z, flip=True, lean=3.0,
             **ekw(t, (-0.9, 0.0), hand_n=(22.0, 50.0), prop_n=lambda sp, h: C.loupe(sp, h)))
    return K.shot('office', cx, cy, Z, acts=[ed], par=(6 - 8 * u, 0), t=t, dof_k=16, clock='11:23')


# ================================================================== 7: at the honor board — «Горячо.»
def r_board(t, u):
    Z = 1.35 + 0.25 * glide(u / 1.0)
    cx, cy = 440.0, 250.0
    v = K.V('office', cx, cy, Z)
    ed = at(C.edik, v, 760, 1500, 26.0, pin='head', near=0.99, flip=True,
            **ekw(t, (-0.9, 0.4), hand_n=(20.0, 62.0), prop_n=lambda sp, h: C.loupe(sp, h)))
    return K.shot('office', cx, cy, Z, acts=[ed], par=(4 * u, 0), t=t, dof_k=20, clock='11:24')


# ================================================================== 8: TWIST — the sheet, close-up
def r_twist(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (150, 104, 60)
    rng = np.random.default_rng(3)
    big[:] = np.clip(big + rng.integers(-14, 14, (OUT_H, OUT_W, 1)), 0, 255).astype(np.uint8)          # cork
    s = 1.0 + 0.08 * glide(u / 1.6)
    im = Image.new('RGB', (900, 1300), (252, 250, 240)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, 899, 1299], outline=(200, 196, 180), width=6)
    for i, (txt, sz, c) in enumerate([('РАЦПРЕДЛОЖЕНИЕ', 54, (40, 70, 130)), ('ГОДА:', 54, (40, 70, 130)), ('ЭКОНОМИТЬ', 84, (190, 40, 40)),
                                      ('НА ВСЁМ!', 84, (190, 40, 40))]):
        f = O.pfont(sz); y = 60 + sum((70, 80, 120, 120)[:i])
        d.text(((900 - f.getlength(txt)) / 2, y), txt, font=f, fill=c)
    d.rectangle([210, 520, 690, 1060], fill=(150, 180, 220), outline=(40, 30, 26), width=8)
    ph = np.array(im)
    from props import kspix as KX
    sp = KX.draw(C.edik, 7.0, expr='proud', legs=False, hand_n=(16.0, 72.0), t=0.0)
    from props.dibspix import blit
    blit(ph, sp, 450, 1240, 7.0, None)
    ph[1060:] = np.array(im)[1060:]
    im2 = Image.fromarray(ph); d2 = ImageDraw.Draw(im2); d2.fontmode = '1'
    d2.rectangle([210, 520, 690, 1060], outline=(40, 30, 26), width=8)
    f = O.pfont(56); d2.text(((900 - f.getlength('— Э. БУЛКИН')) / 2, 1120), '— Э. БУЛКИН', font=f, fill=(34, 30, 28))
    im2 = im2.resize((int(900 * s), int(1300 * s)), Image.NEAREST)
    a = np.array(im2)
    y0 = (OUT_H - a.shape[0]) // 2 + 40; x0 = (OUT_W - a.shape[1]) // 2
    ys, xs = max(0, -y0), max(0, -x0)
    big[max(0, y0):max(0, y0) + a.shape[0] - ys, max(0, x0):max(0, x0) + a.shape[1] - xs] = a[ys:ys + OUT_H - max(0, y0), xs:xs + OUT_W - max(0, x0)][:OUT_H - max(0, y0), :OUT_W - max(0, x0)]
    big[(OUT_H // 2 - 640 + 20):(OUT_H // 2 - 640 + 60), 500:580] = (220, 40, 40)                              # a red pushpin
    return big


# ================================================================== 9: «Это я в январе… для галочки!»
def r_e4(t, u):
    Z = 1.3
    cx, cy = 450.0, 260.0
    v = K.V('office', cx, cy, Z)
    ed = at(C.edik, v, 540, 820, 33.0, pin='head', near=0.99, **ekw(t, (0.0, 0.0), sweat=2.0, hand_n=(14.0, 52.0), hand_f=(-4.0, 50.0)))
    return K.shot('office', cx, cy, Z, acts=[ed], par=(-4 + 6 * u, 0), t=t, dof_k=34, clock='11:25')


# ================================================================== 10: the boss hugs him — «Мы же одна семья!»
def r_hug(t, u):
    Z = 1.2
    cx, cy = 400.0, 330.0
    v = K.V('office', cx, cy, Z)
    w = glide(u / 0.8)
    sh = at(C.shef, v, lerp(-80, 270, w), 1900, 15.0, **skw(t, (0.9, 0.0), hand_n=(30.0, 66.0) if w > 0.8 else None))
    ed = at(C.edik, v, 780, 1900 + 30 * w, 15.5, flip=True, **ekw(t, (-0.9, 0.2)))
    return K.shot('office', cx, cy, Z, acts=[ed, sh], par=(-4 + 6 * u, 0), t=t, dof_k=16, clock='11:26')


# ================================================================== 12: «Зато вот тебе грамота! За экономию!»
def r_gram(t, u):
    Z = 1.2
    cx, cy = 420.0, 330.0
    v = K.V('office', cx, cy, Z)
    give = t > 27.6
    sh = at(C.shef, v, 260, 1900, 15.0, **skw(t, (0.9, 0.0), hand_n=(30.0, 56.0), prop_n=(lambda sp, h: C.gramota(sp, h)) if not give else None))
    ed = at(C.edik, v, 800, 1900, 15.5, flip=True,
            **ekw(t, (-0.9, 0.0), hand_n=(18.0, 50.0) if give else None, prop_n=(lambda sp, h: C.gramota(sp, h)) if give else None))
    return K.shot('office', cx, cy, Z, acts=[ed, sh], par=(4 - 6 * u, 0), t=t, dof_k=16, clock='11:27')


# ================================================================== 13: INSERT — the certificate flipped: an invoice for 40 000
def r_back(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (60, 50, 44)
    flip = min(1.0, u / 0.35)
    w = int(860 * abs(math.cos(flip * math.pi)))
    im = Image.new('RGB', (860, 1180), (236, 236, 232)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, 859, 1179], outline=(200, 160, 70), width=26)
    if flip < 0.5:
        f = O.pfont(90); d.text(((860 - f.getlength('ГРАМОТА')) / 2, 140), 'ГРАМОТА', font=f, fill=(190, 40, 40))
        for i, l in enumerate(['ЗА ЭКОНОМИЮ', 'Э. БУЛКИНУ']):
            f = O.pfont(52); d.text(((860 - f.getlength(l)) / 2, 380 + i * 110), l, font=f, fill=(40, 40, 44))
    else:
        for i, (l, sz, c) in enumerate([('СЧЁТ № 418', 64, (40, 40, 44)), ('ВЕКТОР-СНАБ-СБЫТ', 40, (40, 40, 44)), ('', 40, (0, 0, 0)),
                                         ('К ОПЛАТЕ:', 52, (40, 40, 44)), ('40 000 ₽', 96, (190, 40, 40))]):
            f = O.pfont(sz); d.text(((860 - f.getlength(l)) / 2, 120 + i * 150), l.replace('₽', 'Р'), font=f, fill=c)
    if w > 4:
        a = np.array(im.resize((w, 1180), Image.NEAREST))
        x0 = (OUT_W - w) // 2; y0 = 330
        big[y0:y0 + 1180, x0:x0 + w] = a
    return big


def r_fik1(t, u): return r_fik(t, u)
def r_f5(t, u): return r_fik(t, u)
def r_f6(t, u): return r_fik(t, u)


R = [r_hook, r_e1cu, r_calc, r_fik1, r_l2cu, r_cooler, r_door, r_board, r_twist, r_e4, r_hug, r_f5, r_gram, r_back, r_f6]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['ПРЕМИИ', 'НЕ БУДЕТ?!'], hook_t=(0.10, 2.4), hook_y=230, hook_size=84,
              stickers=[(K.st('1/3 КОМПАНИЙ — БЕЗ ПРЕМИИ', fg=(255, 232, 110), size=44), 11.0, 12.98, 540, 380),
                        (K.st('ХОЛОДНО', fg=(140, 200, 255), size=60), 13.6, 15.6, 540, 420),
                        (K.st('ТЕПЛЕЕ', fg=(255, 200, 110), size=64), 15.8, 16.6, 540, 420),
                        (K.st('ГОРЯЧО!', fg=(255, 110, 90), size=72), 16.7, 17.6, 540, 420),
                        (K.st('ЭТО ТЫ?!', fg=(255, 110, 90), size=84), 17.7, 19.2, 540, 250)],
              flashes=[TWIST, 29.78], mosaics=[4.6],
              cap_y={0: 1560, 1: 1560, 2: 1560, 3: 1580, 4: 1560, 5: 1500, 6: 1500, 7: 1640, 8: 1700, 9: 1560, 10: 1300, 11: 1580,
                     12: 1300, 13: 1640, 14: 1580})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
