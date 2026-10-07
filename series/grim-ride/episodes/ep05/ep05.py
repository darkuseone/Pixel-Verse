"""S01E05 «Best Yard» (06.10.2026) — the closest Death ever gets. Disguised as a yard decoration among Harold's fake tombstones,
he must not move — a ghost kid pokes him with a stick: «Don't. Move.» Todd judges BEST YARD: «Ooh, a REAPER!» A mom: «Ugh. TACKY.»
— «I am DEATH.» — «Seven out of ten. Needs FOG.» Edgar: «Method acting.» Harold comes out and turns his back; Death slowly raises
the scythe — «Finally.» — «Harold. It's TIME.» TWIST (58 %, success is worse than failure): the crowd: «It MOVES! It's ANIMATRONIC!»
— camera flashes, he must freeze mid-swing — «Harold wins BEST YARD!» Harold, with the trophy: «Wanna buy him? Forty bucks.» —
«SOLD!» Death ends up zip-tied in Todd's yard next to Kevin (HALLOWEEN IN: 1 DAY); Kevin's head slowly turns to him. «Help.»
Button, Edgar: «Kinda chic.» Loop: the ghost kid pokes him again.
  python3 ep05.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from episode import Episode
from props import grimpix as GX
from props import grimcast as GC
from props import grimkit as K
from props import bytfx as B
from props.grimshots import Kit, put, A, wpt, aout
from props.dibspix import blit
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
KIT = Kit(EPI)
mouth = KIT.mouth
PORCH, YARD = KIT.PORCH, KIT.YARD
LP, LY = K.light_porch, K.light_yard
DAYS = 1
LAWN_VIEW = (990.0, 420.0, 1.2)                 # Harold's front lawn (right part of the porch background)


def lawn_view():
    cx, cy, Z = LAWN_VIEW
    return view_at(PORCH, cx, cy, Z, 180, 320)


def lawn_props(v, t):
    return [put(v, GC.tombstone, 130, 1620, 8.0, text='RIP'), put(v, GC.tombstone, 900, 1600, 7.5, text='BOO'),
            put(v, GC.pumpkin_inflatable, 990, 1860, 6.4, t=t), put(v, GC.tombstone, 340, 1900, 9.0, text='R.I.P')]


def stick(big, x0, y0, x1, y1, w=10):
    n = int(max(abs(x1 - x0), abs(y1 - y0)) / 4) + 1
    for i in range(n + 1):
        x, y = int(x0 + (x1 - x0) * i / n), int(y0 + (y1 - y0) * i / n)
        big[y - w // 2 - 3:y + w // 2 + 3, x - w // 2 - 3:x + w // 2 + 3] = GX.INK
    for i in range(n + 1):
        x, y = int(x0 + (x1 - x0) * i / n), int(y0 + (y1 - y0) * i / n)
        big[y - w // 2:y + w // 2, x - w // 2:x + w // 2] = (130, 90, 50)


def frozen_grim(v, t, ox=560, oy=1820, s=8.6, expr='deadpan', look=(0.0, 0.0), scythe_up=0.0, mouth_=0.0, **kw):
    return put(v, GC.grim, ox, oy, s, t=t, ride=False, pose='loom', scythe=True, expr=expr, mouth_=mouth_, look=look, wind=0.0,
               blink=False, rot=-10.0 * scythe_up, pivot=(0.0, 0.0), **kw)


def r_hook(t, u, loop=False):
    """0.0: Death frozen among Harold's fake tombstones; a ghost kid pokes him with a stick"""
    v = lawn_view()
    kid = put(v, GC.trick_or_treater, 190, 1880, 8.6, t=t, costume='ghost', n=0, pail=False)
    g = frozen_grim(v, t, look=(-0.6, -0.4), mouth_=mouth('grim', t) * 0.3)
    def f(big, v_):
        poke = 0.5 + 0.5 * math.sin(t * 9)
        hx, hy = aout(g, v_, 'pocket')
        stick(big, 330, 1600, lerp(hx - 140, hx - 40, poke), hy + 40)
        K.fog(big, t, 1500, OUT_H, 0.25)
    return K.shot(PORCH, LP, *LAWN_VIEW[:2], LAWN_VIEW[2], acts=lawn_props(v, t) + [kid, g], fx_=f, sx=180, sy=320)


def r_judge(t, u):
    """Todd arrives with a clipboard: BEST YARD judging"""
    v = lawn_view()
    g = frozen_grim(v, t, look=(1.0, 0.0))
    td = put(v, GC.todd, 880, 1840, 8.6, t=t, flip=True, expr='hype', mouth_=mouth('todd', t), look=(-1.0, -0.2), phone=False, clip=True)
    def f(big, v_): K.fog(big, t, 1500, OUT_H, 0.25)
    return K.shot(PORCH, LP, *LAWN_VIEW[:2], LAWN_VIEW[2], acts=lawn_props(v, t) + [g, td], fx_=f, sx=180, sy=320)


def r_mom(t, u):
    big, _ = KIT.cu(PORCH, LP, GC.mom, t, 990.0, 430.0, 12.5, (560 + 180 * u, 760), Z=1.4, flip=True, expr='disgust' if False else 'squint',
                    mouth_=mouth('mom', t), look=(-1.0, 0.0))
    return big


def r_whisper(t, u):
    big, _ = KIT.cu(PORCH, LP, GC.grim, t, 990.0, 430.0, 13.0, (540, 900), Z=1.4, ride=False, pose='loom', scythe=False, expr='angry',
                    mouth_=mouth('grim', t) * 0.25, look=(1.0, 0.0), blink=False)
    return big


def r_score(t, u):
    big, _ = KIT.cu(PORCH, LP, GC.todd, t, 990.0, 430.0, 13.0, (560, 820), Z=1.4, flip=True, expr='pity', mouth_=mouth('todd', t),
                    look=(-1.0, -0.4), phone=False, clip='7/10')
    return big


def r_method(t, u):
    v = view_at(PORCH, 860.0, 470.0, 1.6, 180, 320)
    big = K.dof(v.bg(), 8)
    sp = GX.draw(GC.tombstone, 22.0, text='RIP')
    blit(big, sp, 540, 1950, 22.0, LP(v))
    sp = GX.draw(GC.edgar, 19.0, t=t, expr='deadpan', mouth_=mouth('edgar', t, 2.0), cam=True, look=(0.0, 0.0), perch=False)
    blit(big, sp, 540, 1560, 19.0, LP(v))
    fx.vignette(big, 0.3)
    return big


def r_harold(t, u):
    """Harold comes down to his lawn and turns his back, admiring a pumpkin; behind him, the «decoration»"""
    v = lawn_view()
    hx = lerp(1250, 800, sm(min(1.0, u / 1.0)))
    g = frozen_grim(v, t, look=(1.0, 0.0), expr='sly')
    h = put(v, GC.harold, hx, 1880, 9.0, t=t, pose='stand', flip=u < 1.0, expr='content', look=(1.0, -0.3))
    def f(big, v_): K.fog(big, t, 1500, OUT_H, 0.25)
    return K.shot(PORCH, LP, *LAWN_VIEW[:2], LAWN_VIEW[2], acts=lawn_props(v, t) + [g, h], fx_=f, sx=180, sy=320)


def r_fin(t, u):
    v = view_at(PORCH, 860.0, 470.0, 1.6, 180, 320)
    big = K.dof(v.bg(), 8)
    sp = GX.draw(GC.tombstone, 22.0, text='RIP')
    blit(big, sp, 540, 1950, 22.0, LP(v))
    sp = GX.draw(GC.edgar, 19.0, t=t, expr='sly', mouth_=mouth('edgar', t, 2.0), cam=True, look=(0.0, 0.0), perch=False)
    blit(big, sp, 540, 1560, 19.0, LP(v))
    fx.vignette(big, 0.3)
    return big


def r_raise(t, u):
    """the scythe rises — eyes blazing — over Harold's helmet"""
    def f(big, v, a):
        hx, hy = aout(a, v, 'eyes')
        K.glow_ring(big, hx, hy, 240, GC.GLOW, 0.3 + 0.2 * math.sin(t * 20))
    v = view_at(PORCH, 860.0, 430.0, 1.4, 180, 320)
    har = put(v, GC.harold, 860, 2050, 12.0, t=t, pose='stand', expr='content', look=(1.0, -0.3))
    big, _ = KIT.cu(PORCH, LP, GC.grim, t, 990.0, 430.0, 12.0, (440, 760), Z=1.4, fx_=f, extra=[har], ride=False, pose='loom', scythe=True,
                    expr='menace', mouth_=mouth('grim', t) * 0.6, look=(1.0, 0.6), rot=-12.0 * min(1.0, u / 1.6), pivot=(0.0, 60.0))
    return big


def r_twist(t, u):
    """TWIST: the crowd — «It MOVES! It's ANIMATRONIC!» — phones flash; he freezes mid-swing"""
    v = lawn_view()
    g = frozen_grim(v, t, look=(-1.0, -0.2), expr='stunned', scythe_up=1.0)
    h = put(v, GC.harold, 800, 1880, 8.6, t=t, pose='stand', expr='stunned', look=(-1.0, 0.0), flip=True)
    crowd = [put(v, GC.todd, 1000, 1760, 7.6, t=t, flip=True, expr='hype', mouth_=mouth('todd', t), look=(-1.0, 0.0), phone=True),
             put(v, GC.mom, 120, 1720, 7.4, t=t, expr='shock', look=(1.0, 0.0), mouth_=0.6),
             put(v, GC.trick_or_treater, 260, 1900, 7.6, t=t, costume='pumpkin', n=1, expr='shock', look=(1.0, 0.0)),
             put(v, GC.trick_or_treater, 940, 1940, 7.8, t=t, costume='dino', n=2, flip=True, expr='shock', look=(-1.0, 0.0))]
    def f(big, v_):
        for i, tf in enumerate((0.2, 0.8, 1.6)):
            if tf <= u < tf + 0.12: O.flash(big, 0.75)
        K.fog(big, t, 1500, OUT_H, 0.25)
    big = K.shot(PORCH, LP, *LAWN_VIEW[:2], LAWN_VIEW[2], acts=lawn_props(v, t) + [g, h] + crowd, fx_=f, sx=180, sy=320)
    if u < 0.3: B.shake(big, t, 8, 30)
    return big


def r_winner(t, u):
    v = lawn_view()
    g = frozen_grim(v, t, look=(-1.0, -0.2), expr='stunned', scythe_up=1.0)
    h = put(v, GC.harold, 760, 1880, 9.0, t=t, pose='stand', expr='smug', look=(1.0, 0.0), cup=True)
    td = put(v, GC.todd, 1000, 1800, 8.0, t=t, flip=True, expr='hype', mouth_=mouth('todd', t), look=(-1.0, 0.0), phone=False, point=1.0)
    def f(big, v_):
        K.confetti(big, t, 20.5)
        K.fog(big, t, 1500, OUT_H, 0.25)
    return K.shot(PORCH, LP, *LAWN_VIEW[:2], LAWN_VIEW[2], acts=lawn_props(v, t) + [g, h, td], fx_=f, sx=180, sy=320)


def r_sell(t, u):
    big, _ = KIT.cu(PORCH, LP, GC.harold, t, 990.0, 430.0, 13.5, (540, 900), Z=1.4, pose='stand', expr='sly', mouth_=mouth('harold', t),
                    look=(1.0, 0.0), cup=True)
    return big


def r_sold(t, u):
    big, _ = KIT.cu(PORCH, LP, GC.todd, t, 990.0, 430.0, 13.0, (560, 820), Z=1.4, flip=True, expr='cheer', mouth_=mouth('todd', t),
                    look=(-1.0, 0.0), phone=False, point=1.0)
    if u < 0.4: B.shake(big, t, 8, 30)
    return big


def r_tied(t, u):
    """Todd's lawn: Death zip-tied to a stake next to Kevin (HALLOWEEN IN: 1 DAY); Kevin's head turns slowly down to him"""
    v = view_at(YARD, 470.0, 330.0, 1.45, 180, 320)
    turn = 0.9 * sm(min(1.0, max(0.0, (u - 0.3) / 1.0)))
    kev = put(v, GC.kevin, 380, 1640, 8.6, t=t, turn=turn)
    sign = put(v, GC.countdown_sign, 980, 1720, 5.6, days=DAYS)
    g = put(v, GC.grim, 700, 1850, 6.4, t=t, ride=False, pose='stand', scythe=False, expr='sad', look=(-0.8, 0.6))
    def f(big, v_):
        hx, hy = aout(g, v_, 'pocket')
        for dy in (-60, 40, 160):                                                             # zip ties
            big[int(hy) + dy:int(hy) + dy + 14, int(hx) - 110:int(hx) + 110] = (20, 20, 24)
            big[int(hy) + dy + 2:int(hy) + dy + 12, int(hx) + 100:int(hx) + 130] = (20, 20, 24)
        big[int(hy) - 200:int(hy) + 420, int(hx) - 150:int(hx) - 136] = (120, 90, 60)             # the stake
        K.fog(big, t, 1450, OUT_H, 0.2)
    return K.shot(YARD, LY, 470.0, 330.0, 1.45, acts=[kev, sign, g], fx_=f, sx=180, sy=320)


def r_help(t, u):
    def f(big, v, a):
        hx, hy = aout(a, v, 'pocket')
        for dy in (-120, 20):
            big[int(hy) + dy:int(hy) + dy + 22, 0:OUT_W] = (20, 20, 24)
    big, _ = KIT.cu(YARD, LY, GC.grim, t, 600.0, 430.0, 13.0, (540, 900), Z=1.4, fx_=f, ride=False, pose='stand', scythe=False, expr='whine',
                    mouth_=mouth('grim', t) * 0.5, look=(0.0, -0.4))
    return big


def r_chic(t, u):
    return KIT.edgar_cu(YARD, LY, t, cx=600.0, expr='smug')


def r_loop(t, u): return r_hook(t, u, loop=True)


SHOTS = [r_hook, r_judge, r_mom, r_whisper, r_score, r_method, r_harold, r_fin, r_raise, r_twist, r_winner, r_sell, r_sold, r_tied,
         r_help, r_chic, r_loop]
NAMES = ['hook', 'judge', 'mom', 'whisper', 'score', 'method', 'harold', 'fin', 'raise', 'twist', 'winner', 'sell', 'sold', 'tied',
         'help', 'chic', 'loop']
CAP = dict(hook=900, judge=900, method=1100, fin=1100, harold=900, twist=900, winner=900, tied=1060, chic=1180, loop=900)

SHOW = K.Show(EPI, 5, ['DEATH PLAYS', 'DECORATION?'], hook_t=(0.10, 2.6), hook_y=150, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('7/10', (255, 90, 80), 80), 10.2, 11.35, 760, 420),
                        (K.st('ANIMATRONIC?!', (255, 200, 60), 58), 17.6, 20.3, 540, 420),
                        (K.st('$40', (150, 255, 110), 80), 23.0, 24.2, 760, 420),
                        (K.st('1 DAY', (255, 140, 40), 64), 25.4, 26.8, 540, 380)],
              flashes=[17.50], mosaics=[12.75, 25.28])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
