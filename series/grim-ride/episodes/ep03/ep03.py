"""S01E03 «Full Size» (06.10.2026) — legend says Harold gives out FULL-SIZE bars: he HAS to open the door. Death joins the endless
trick-or-treat line with a pillowcase. Todd hands out singles: «One each, buddy. Seventeen bucks a BAG!» — Edgar: «Inflation.»
A mom: «Aren't you a little OLD for this?» — «I am DEATH! I'm four THOUSAND!» — «Then that's a NO.» — «Carded.» The gang cuts the line.
The door opens, a choir... TWIST (59 %, the reward is the same problem): the «full-size» bar is the size of a fingernail — «That's full
size NOW.» The whole line groans; Harold zooms off on his trike: «Catch me, BONES.» Kayden: «Bro. Did YOU kill full-size?» —
Button: «I didn't do THIS one.» Loop: Death back at the end of the line.
  python3 ep03.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
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

EPI = Episode('ep03', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
KIT = Kit(EPI)
mouth = KIT.mouth
PORCH, YARD, STREET = KIT.PORCH, KIT.YARD, KIT.STREET
DAYS = 3
COST = ['ghost', 'pumpkin', 'dino', 'witch', 'robot', 'vampire', 'ghost', 'dino', 'pumpkin']
# the line from Harold's door down the steps to the lawn (output px of the hook view), growing towards the camera
LINE = [(140, 1190, 4.4), (250, 1195, 4.5), (360, 1205, 4.6), (470, 1300, 5.0), (560, 1410, 5.4), (640, 1520, 5.8), (560, 1640, 6.4),
        (430, 1740, 6.8), (290, 1840, 7.2)]


def line_view():
    return view_at(PORCH, 520.0, 420.0, 1.0, 180, 320)


def the_line(t, v, groan=0.0, look=(-0.8, 0.0), skip=()):
    acts = []
    for i, (ox, oy, s) in enumerate(LINE):
        if i in skip: continue
        acts.append(put(v, GC.trick_or_treater, ox, oy, s, t=t, costume=COST[i], n=i, flip=True, look=look, groan=groan))
    return acts


def r_hook(t, u, loop=False):
    """0.0: the endless trick-or-treat line from Harold's lit door down the steps — Death at the very end with a pillowcase"""
    v = line_view()
    acts = the_line(t, v)
    acts.append(put(v, GC.mom, 660, 1880, 6.6, t=t, expr='normal', look=(-1.0, 0.0), flip=True))
    acts.append(put(v, GC.grim, 900, 1990, 8.6, t=t, ride=False, pose='stand', carry=0.3, scythe=False, flip=True, expr='smug',
                    mouth_=mouth('grim', t), look=(1.0, 0.2)))
    def f(big, v_):
        ox, oy = v_.opt(356, 380)
        K.glow_ring(big, ox, oy, 340, (255, 220, 140), 0.35)
        K.leaves(big, t, 12, seed=4)
        K.fog(big, t, 1600, OUT_H, 0.18)
    return K.shot(PORCH, K.light_porch, 520.0, 420.0, 1.0, acts=acts, fx_=f, sx=180, sy=320)


def r_scheme(t, u):
    big, _ = KIT.cu(PORCH, K.light_porch, GC.grim, t, 820.0, 430.0, 13.0, (520, 880), Z=1.4, flip=True, ride=False, pose='stand', carry=0.3,
                    scythe=False, expr='smug', mouth_=mouth('grim', t), look=(1.0, 0.3))
    return big


def r_todd(t, u):
    """next door: Todd hands out ONE candy per kid (the bag cost $17); it drops into Death's pillowcase"""
    v = view_at(YARD, 620.0, 430.0, 1.4, 180, 320)
    sign = put(v, GC.countdown_sign, 180, 1500, 6.0, days=DAYS)
    big, a = KIT.cu(YARD, K.light_yard, GC.todd, t, 620.0, 430.0, 13.5, (620, 820), Z=1.4, flip=True, expr='pity', mouth_=mouth('todd', t),
                    look=(-1.0, -0.4), phone=False, point=0.7, extra=[sign])
    hx, hy = aout(a, view_at(YARD, 620.0, 430.0, 1.4, 180, 320), 'hand')
    bx, by = int(hx) - 40, int(hy) + 10                                                          # the candy bowl in his hand
    big[by - 6:by + 56, bx - 96:bx + 96] = GX.INK
    big[by:by + 50, bx - 90:bx + 90] = (255, 130, 40); big[by:by + 12, bx - 90:bx + 90] = (200, 80, 20)
    k = min(1.0, max(0.0, (u - 1.2) / 0.5))
    if k < 1:                                                                                    # ONE candy falls into the pillowcase
        cy = int(lerp(by - 10, 1700, k * k))
        big[cy:cy + 22, bx - 11:bx + 11] = (255, 60, 120)
    sp = GX.draw(GC.sack, 18.0, x=0.0, y=0.0, fill=0.1)                                        # Death's pillowcase at the bottom
    blit(big, sp, 380, 2050, 18.0)
    return big


def r_inflation(t, u):
    return KIT.edgar_cu(YARD, K.light_yard, t, cx=620.0)


def mom_cu(t, u, expr, point=0.0):
    big, _ = KIT.cu(PORCH, K.light_porch, GC.mom, t, 700.0, 430.0, 13.0, (560, 760), Z=1.4, expr=expr, mouth_=mouth('mom', t),
                    look=(1.0, 0.0), point=point)
    return big


def r_mom1(t, u):
    return mom_cu(t, u, 'squint')


def r_death(t, u):
    def f(big, v, a):
        hx, hy = aout(a, v, 'eyes')
        K.glow_ring(big, hx, hy, 260, GC.GLOW, 0.35 * (1 - min(1.0, u / 1.2)))
    big, _ = KIT.cu(PORCH, K.light_porch, GC.grim, t, 820.0, 430.0, 13.5, (540, 900), Z=1.4, flip=True, fx_=f, ride=False, pose='claw',
                    carry=0.0, scythe=False, expr='angry', mouth_=mouth('grim', t), look=(1.0, 0.0), shake=1.0 if u < 0.6 else 0.0)
    K.lightning(big, t, 10.04, seed=5)
    if u < 0.5: B.shake(big, t, 10, 34)
    return big


def r_mom2(t, u):
    return mom_cu(t, u, 'deadpan', point=min(1.0, u / 0.3))


def r_carded(t, u):
    return KIT.edgar_cu(PORCH, K.light_porch, t, cx=700.0, expr='sly')


def r_gang(t, u):
    """the masked gang wheelies across the lawn and cuts straight to the front of the line"""
    v = line_view()
    acts = the_line(t, v, look=(1.0, 0.2))
    for i, (oy, ox0, sp_) in enumerate(((1560, -300, 700), (1700, -520, 760), (1840, -200, 640))):
        acts.append(put(v, GC.kayden, ox0 + sp_ * u, oy, 5.6 + 0.6 * i, t=t, spin=-t * 40, n=i,
                        col=[(70, 50, 82), (46, 70, 64), GC.HOODIE][i], string=[(255, 120, 200), (255, 220, 60), GC.LIME][i],
                        rot=13.0 + 2 * math.sin(t * 6 + i), pivot=(-22.0, 0.5), look=(0.2, 0.0)))
    def f(big, v_): K.speed_streaks(big, t, 0.5)
    return K.shot(PORCH, K.light_porch, 520.0, 420.0, 1.0, acts=acts, fx_=f, sx=180, sy=320)


def r_door(t, u):
    """the door swings open: golden light, a choir — Harold in the doorway holds out «a full-size bar»"""
    v = view_at(PORCH, 360.0, 380.0, 1.4, 180, 320)
    k = sm(min(1.0, u / 0.4))
    har = put(v, GC.harold, 520, 1560, 12.0, t=t, pose='stand', expr='smug', mouth_=0.0, look=(1.0, -0.2), offer=k)
    def pre(big, v_):
        x0, y0 = v_.opt(306, 296); x1, y1 = v_.opt(410, 470)
        w = int((x1 - x0) * k)
        big[int(y0):int(y1), int(x0):int(x0) + w] = (255, 230, 160)
    def f(big, v_):
        x0, y0 = v_.opt(356, 380)
        K.glow_ring(big, x0, y0, 700, (255, 230, 160), 0.45 * k)
        fx.shafts(big, t, a=0.12 * k, col=(255, 236, 180), x_off=int(x0) - 540)
    return K.shot(PORCH, K.light_porch, 360.0, 380.0, 1.4, acts=[har], pre=pre, fx_=f, sx=180, sy=320)


def r_twist(t, u):
    """TWIST insert: on the bony palm — the «full-size» bar, the size of a fingernail. FULL SIZE* (*new size)"""
    v = view_at(PORCH, 400.0, 420.0, 1.4, 180, 320)
    big = K.dof(v.bg(), 9)
    hy_ = 1300 + 6 * math.sin(t * 3)
    sp = GX.draw(GC.bony_hand, 60.0, x=0.0, y=0.0, d=1.0, grip=False)
    blit(big, sp, 500, hy_, 60.0, K.light_porch(v))
    bx, by = 460, int(hy_) - 150                                                                 # the bar: 80 x 34 px on a 400 px palm
    big[by - 6:by + 40, bx - 6:bx + 86] = GX.INK
    big[by:by + 34, bx:bx + 80] = (120, 66, 34)
    big[by + 10:by + 24, bx + 12:bx + 68] = (250, 200, 60)
    big[by:by + 34, bx + 34:bx + 40] = (210, 40, 50)
    K.glow_ring(big, bx + 40, by + 17, 180, (255, 236, 160), 0.3)
    if u < 0.3: B.shake(big, t, 8, 30)
    fx.vignette(big, 0.35)
    return big


def r_groan(t, u):
    """the whole line groans; Harold shuts the door"""
    v = line_view()
    acts = the_line(t, v, groan=sm(min(1.0, u / 0.3)), look=(1.0, -0.3))
    acts.append(put(v, GC.mom, 660, 1880, 6.6, t=t, expr='sad', look=(-1.0, 0.0), flip=True))
    acts.append(put(v, GC.grim, 900, 1990, 8.6, t=t, ride=False, pose='stand', carry=0.3, scythe=False, flip=True, expr='stunned',
                    look=(1.0, -0.6)))
    return K.shot(PORCH, K.light_porch, 520.0, 420.0, 1.0, acts=acts, sx=180, sy=320)


def r_zoom(t, u):
    """out of the side yard: Harold on the trike, past Death and the line — «Catch me, BONES.»"""
    v = view_at(STREET, 640.0, 380.0, 1.35, 180, 320)
    hx = lerp(-250.0, 1450.0, min(1.0, max(0.0, (u - 0.3) / 2.2)))
    g = put(v, GC.grim, 760, 1700, 6.4, t=t, ride=False, pose='stand', carry=0.3, scythe=False, expr='stunned', look=(-1.0, 0.0))
    har = put(v, GC.harold, hx, 1860, 7.0, t=t, pose='ride', spin=-t * 34, expr='grin', mouth_=mouth('harold', t), look=(1.0, 0.0), flag=1.4)
    def f(big, v_): K.speed_streaks(big, t, 0.6); K.leaves(big, t, 20, seed=6, speed=2.0)
    return K.shot(STREET, K.light_street, 640.0, 380.0, 1.35, acts=[g, har], fx_=f, sx=180, sy=320)


def r_kayden(t, u):
    big, _ = KIT.cu(STREET, K.light_street, GC.kayden, t, 600.0, 430.0, 13.0, (520, 820), Z=1.4, flip=True, spin=0.0, expr='squint',
                    look=(1.0, 0.0))
    return big


def r_button(t, u):
    big, _ = KIT.cu(STREET, K.light_street, GC.grim, t, 760.0, 430.0, 13.0, (560, 880), Z=1.4, ride=False, pose='stand', carry=0.3,
                    scythe=False, expr='whine', mouth_=mouth('grim', t), look=(-0.8, -0.3))
    return big


def r_loop(t, u):
    return r_hook(t, u, loop=True)


SHOTS = [r_hook, r_scheme, r_todd, r_inflation, r_mom1, r_death, r_mom2, r_carded, r_gang, r_door, r_twist, r_groan, r_zoom, r_kayden,
         r_button, r_loop]
NAMES = ['hook', 'scheme', 'todd', 'inflation', 'mom1', 'death', 'mom2', 'carded', 'gang', 'door', 'twist', 'groan', 'zoom', 'kayden',
         'button', 'loop']
CAP = dict(hook=900, loop=900, inflation=1180, carded=1180, todd=1640, twist=1720, gang=900, groan=900, zoom=1060, door=1720)

SHOW = K.Show(EPI, 3, ['FULL-SIZE', 'BAR HOUSE?'], hook_t=(0.10, 2.6), hook_y=150, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('$17 A BAG', (255, 90, 80), 60), 4.6, 6.4, 760, 380),
                        (K.st('AGE: 4000', (200, 170, 255), 56), 11.0, 13.3, 540, 360),
                        (K.st('FULL SIZE?!', (255, 200, 60), 70), 18.5, 20.3, 540, 520),
                        (K.st('*NEW SIZE', (150, 255, 110), 46), 19.2, 20.35, 720, 1880)],
              flashes=[18.40], mosaics=[7.55, 27.80])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
