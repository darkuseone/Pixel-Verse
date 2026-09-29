"""S01E02 «Цена по карте» — 199 on the shelf, 289 at the register; Valera wins 90 back and loses it on the bag.
  python3 ep02.py test 1 5 20 | frame 12 | all [4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import stage as ST
from stage import View, view_at, Chars, shadow
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from timeline import DUR, FPS, VOICE, SLUG

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
W = PK.build()
SHOP, KIT = W['shop'], W['kitchen']
CNT, CNTXY = W['counter'], W['counter_xy']
VX, VY, VU = PK.SH_VALERA
TX, TY, TU = PK.SH_TAMARA
ZX, ZY, ZU = PK.SH_ZINA
CAT_T = (1112.0, 500.0, 7.5)                  # cat on the kitchen table
SAUS = (1168.0, 497.0)


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def lcd_text(t):
    if t < 21.15: return '289'
    if t < 24.95: return '199'
    if t < 26.85: return '199+90'
    if t < 34.85: return '289'
    return '299'


# ---------------------------------------------------------------- characters
def valera(CH, v, t, expr, pose='stand', **kw):
    return F.valera(CH, v.cam(VX, VY, VU), F.VPOSE[pose] if isinstance(pose, str) else pose, t, mouth('valera', t), expr,
                    'street', **kw)


def tamara(CH, v, t, expr='bored', **kw):
    return F.tamara(CH, v.cam(TX, TY, TU, flip=True), t, mouth('tamara', t), expr, **kw)


def zina(CH, v, t):
    F.babushka(CH, v.cam(ZX, ZY, ZU), t, 'zina', 'stand', 0.0, 'smug', look=1.0, prop_n=F.string_bag)


def shop_frame(v, t, who=('valera', 'tamara', 'zina'), vexpr='normal', vpose='stand', texpr='bored', vkw=None, tkw=None):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    if 'zina' in who: zina(CH, v, t)
    if 'tamara' in who: tamara(CH, v, t, texpr, **(tkw or {}))
    CH.comp(big, K.light_shop(v))
    K.occlude(big, v, CNT, CNTXY)
    PK.lcd_digits(big, v, lcd_text(t))
    CH2 = Chars()
    if 'valera' in who:
        shadow(big, v, VX + 12, VY, 6 * VU, 0.9 * VU)
        valera(CH2, v, t, vexpr, vpose, **(vkw or {}))
    CH2.comp(big, K.light_shop(v))
    fx.vignette(big, 0.3)
    return big


def v_face():
    return K.face_w(VX, VY, VU, h=20.8)


def t_face():
    return TX - 2.0 * TU, TY - 20.5 * TU


# ---------------------------------------------------------------- shots
SHOTS = [
    (0.00, 1.10, 'hook'), (1.10, 3.55, 't_cu1'), (3.55, 5.30, 'v_point'), (5.30, 6.95, 'tag'), (6.95, 10.60, 't_cu2'),
    (10.60, 13.45, 'v_proud'), (13.45, 16.15, 't_cu3'), (16.15, 18.85, 'slam'), (18.85, 22.55, 't_sigh'),
    (22.55, 24.85, 'v_win'), (24.85, 26.85, 't_bag'), (26.85, 28.15, 'twitch'), (28.15, 30.55, 'cat_w'),
    (30.55, 33.00, 'cat_cu'), (33.00, 34.85, 'next_day'), (34.85, 36.80, 't_new'), (36.80, DUR + 1, 'loop'),
]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def r_hook(t, u):
    fx_, fy_ = v_face()
    v = view_at(SHOP, fx_ - 20, fy_ + 30, 1.6, 180, 290)
    big = shop_frame(v, t, ('valera',), 'shock', 'stand')
    return big


def r_t_cu(t, u, expr='bored', gum=None, Z=2.0, sx=180, **kw):
    x, y = t_face()
    v = view_at(SHOP, x, y, Z + 0.06 * u, sx, 300)
    g = gum(t) if gum else 0.0
    return shop_frame(v, t, ('tamara',), texpr=expr, tkw=dict(gum=g, **kw))


def r_v_point(t, u):
    v = view_at(SHOP, VX - 60, VY - 330, 1.2 + 0.04 * u, 180, 330)
    k = sm(u / 0.3)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    zina(CH, v, t)
    CH.comp(big, K.light_shop(v))
    shadow(big, v, VX - 12, VY, 6 * VU, 0.9 * VU)
    CH2 = Chars()
    F.valera(CH2, v.cam(VX, VY, VU, flip=True), F.VPOSE['stand'], t, mouth('valera', t), 'angry', 'street',
             hand_n=F.H(lerp(3.9, 10.5, k), lerp(10.4, 18.0, k)))
    CH2.comp(big, K.light_shop(v))
    fx.vignette(big, 0.3)
    return big


def r_tag(t, u):
    x0, y0, x1, y1 = PK.TAG
    k = sm((u - 0.6) / 0.7)
    cx = (x0 + x1) / 2; cy = lerp((y0 + y1) / 2, y1 - 16, k)
    v = view_at(SHOP, cx, cy, lerp(2.5, 4.3, k), 180, 320)
    big = v.bg()
    fx.vignette(big, 0.4)
    if k > 0.35:                                                                   # magnifier ring
        r = int(470 * min(1.0, (k - 0.2) * 1.6))
        yy, xx = np.ogrid[:big.shape[0], :big.shape[1]]
        d = np.sqrt((xx - 540) ** 2 + (yy - 960) ** 2)
        ring = (d > r) & (d < r + 18)
        big[ring] = (40, 36, 34)
        big[(d >= r + 18)] = (big[(d >= r + 18)] * 0.55).astype(np.uint8)
    return big


def r_v_proud(t, u):
    v = view_at(SHOP, VX + 40, VY - 330, 1.25 + 0.05 * u, 180, 330)
    sal = sm((t - 10.75) / 0.3)
    return shop_frame(v, t, ('valera', 'zina'), 'proud', F.vblend(F.VPOSE['stand'], F.VPOSE['proud'], sal))


def r_slam(t, u):
    v = View(SHOP, 760, 110, 0.9)
    tt = t - 16.25
    if tt < 0: hh = lerp(14.0, 18.5, sm((t - 16.15) / 0.1))
    else: hh = lerp(18.5, 12.6, min(1.0, tt / 0.08))
    hand = (1000 + (905 - VX) / VU, 1000 - hh) if t >= 16.15 else None
    big = shop_frame(v, t, ('valera', 'tamara', 'zina'), 'angry', 'stand', texpr='annoyed', vkw=dict(hand_n=hand))
    if 0 <= tt < 0.35: B.shake(big, t, 14 * (1 - tt / 0.35), 43)
    return big


def r_t_sigh(t, u):
    x, y = t_face()
    v = view_at(SHOP, x + 20, y + 60, 1.6 + 0.05 * u, 180, 290)
    typing = 20.55 <= t < 21.55
    hand = F.H(4.6 + (0.3 * math.sin(t * 40) if typing else 0), 12.2) if t > 20.35 else None
    return shop_frame(v, t, ('tamara',), texpr='sigh' if t < 20.75 else 'bored', tkw=dict(hand_n=hand))


def r_v_win(t, u):
    fx_, fy_ = v_face()
    v = view_at(SHOP, fx_ - 20, fy_ + 70, 1.45 + 0.05 * u, 180, 300)
    sal = sm((t - 22.65) / 0.25)
    return shop_frame(v, t, ('valera',), 'smug', F.vblend(F.VPOSE['stand'], F.VPOSE['fist'], sal))


def r_t_bag(t, u):
    x, y = t_face()
    v = view_at(SHOP, x + 10, y + 40, 1.8, 180, 300)
    k = sm(u / 0.25)
    return shop_frame(v, t, ('tamara',), texpr='smug', tkw=dict(hand_n=F.H(lerp(3.6, 5.2, k), lerp(10.8, 18.5, k)),
                                                             prop_n=F.plastic_bag))


def r_twitch(t, u):
    fx_, fy_ = v_face()
    v = view_at(SHOP, fx_, fy_, 2.5, 180, 300)
    big = shop_frame(v, t, ('valera',), 'shock' if int(t * 12) % 3 else 'angry', 'stand')
    return big


def cat_frame(v, t):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    cx, cy, cu = CAT_T
    chew = 0.35 * (1 + math.sin(t * 16)) if t < 29.35 or 30.55 < t < 31.25 else 0.0
    m = max(mouth('cat', t, 2.0), chew)
    L = Layer(v.wcam())
    left = max(0.25, 1.0 - (t - 28.15) / 5.0)
    F.cap(L, SAUS, (SAUS[0] + 44 * left, SAUS[1] - 2), 8.0, 8.0, (214, 128, 120), (236, 160, 150), (180, 100, 96))
    F.ell(L, SAUS, 8.0, 8.0, (240, 196, 186))                                   # cut end
    for k in range(5): F.dot(L, (SAUS[0] + 6 + 8 * k * left, SAUS[1] - 3 + (k % 2) * 4), (250, 236, 226), 1.2)
    F.cap(L, (1030, 522), (1066, 536), 7, 7, (244, 244, 236))                   # receipt
    F.outline(L); CH.add(L)
    F.cat(CH, v.cam(cx, cy, cu), t, 'loaf', m, 0.6, look=(0.3, -0.2))
    CH.comp(big, K.light_kit(v))
    if v.Z > 1.5:
        rx, ry = v.opt(1048, 529)
        img = O.sticker('289', fg=(40, 36, 40), size=int(24 * v.Z / 2) // 8 * 8 or 8)
        O.overlay(big, img, int(rx - img.shape[1] / 2), int(ry - img.shape[0] / 2), 0.9)
    fx.vignette(big, 0.3)
    return big


def r_cat_w(t, u):
    v = view_at(KIT, 1110, 430, 1.9 + 0.06 * u, 180, 330)
    return cat_frame(v, t)


def r_cat_cu(t, u):
    cx, cy, cu = CAT_T
    v = view_at(KIT, cx + 4.4 * cu, cy - 6.9 * cu, 3.1 + 0.08 * u, 180, 290)
    return cat_frame(v, t)


def r_next_day(t, u):
    fx_, fy_ = v_face()
    v = view_at(SHOP, fx_, fy_ + 60, 1.6, 180, 300)
    k = sm(u / 0.3)
    return shop_frame(v, t, ('valera', 'zina'), 'proud', 'stand',
                      vkw=dict(hand_n=F.H(lerp(3.9, 7.4, k), lerp(10.4, 19.5, k)), prop_n=F.plastic_bag))


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name in ('hook', 'loop'): return r_hook(t, u)
    if name == 't_cu1': return r_t_cu(t, u, 'bored', gum=lambda tt: max(0.0, min(1.0, (tt - 2.6) / 0.8)) if tt < 3.42 else 0.0)
    if name == 'v_point': return r_v_point(t, u)
    if name == 'tag': return r_tag(t, u)
    if name == 't_cu2': return r_t_cu(t, u, 'smug', Z=2.2)
    if name == 'v_proud': return r_v_proud(t, u)
    if name == 't_cu3': return r_t_cu(t, u, 'bored', Z=2.5, look=0.5)
    if name == 'slam': return r_slam(t, u)
    if name == 't_sigh': return r_t_sigh(t, u)
    if name == 'v_win': return r_v_win(t, u)
    if name == 't_bag': return r_t_bag(t, u)
    if name == 'twitch': return r_twitch(t, u)
    if name == 'cat_w': return r_cat_w(t, u)
    if name == 'cat_cu': return r_cat_cu(t, u)
    if name == 'next_day': return r_next_day(t, u)
    return r_t_cu(t, u, 'bored', Z=2.0)


LCD289 = K.lcd_sticker('289')
SHOW = K.Show(EPI, 2, ['НА ЦЕННИКЕ', 'БЫЛО 199'], hook_t=(0.15, 2.4),
              stickers=[(LCD289, 0.25, 1.1, 800, 820), (O.sticker('ПОБЕДА!', fg=(120, 255, 140), size=64), 22.75, 24.65, 540, 1560),
                        (O.sticker('199+90=289', fg=(255, 236, 120), size=56), 26.9, 28.15, 540, 600),
                        (O.sticker('НАЗАВТРА', fg=(150, 210, 255), size=56), 33.05, 34.35, 540, 520),
                        (K.lcd_sticker('299'), 35.05, 36.75, 800, 700)],
              flashes=[5.30, 24.90, 33.00], mosaics=[28.15], cap_y={'tag': 1480}, teaser='ДАЛЬШЕ: БАБУШКИ')


def render(t):
    big = render_scene(t)
    return SHOW.apply(big, t, shot_at(t)[2])


if __name__ == '__main__':
    EPI.main(render, __file__)
