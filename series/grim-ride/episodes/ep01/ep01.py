"""S01E01 «Class 3» (06.10.2026) — Death got downsized: the pale horse is gone, he rides a rented Class-3 e-bike («four easy payments»).
Pickup: HAROLD, 97. On Todd's lawn: «I am DEATH!» — «Not even twelve feet, buddy.» On the porch: «Harold. Your time is UP.» — «Over my
dead body.» — «That's the PLAN.» TWIST (59 %): the tarp flies off — Harold's unlocked black e-trike, «Catch me, BONES.» The prey is
faster than Death; the e-bike gang overtakes him («Relax, pal.»), the battery dies («Dead battery. Ironic.»), Harold rates him one star,
then laps him and bonks a raisin box off his hood: «Happy Halloween, KID!» Loop: he stomps the pedal, the bike rears up = first frame.
Heroes: props/grimcast.py in the «Lantern Stipple» manner (props/grimpix.py); kit: props/grimkit.py.
  python3 ep01.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import paths as P
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
from props.dibspix import blit
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
STREET = K.world('street')
YARD = K.world('todd_yard')
PORCH = K.world('porch')
A, wpt, aout = K.A, K.wpt, K.aout
SP = K.SP
LANE = 650.0                                       # street: riders' feet
WALK = 668.0                                       # Todd's yard: the sidewalk
LAWN = 560.0
PFLOOR = 492.0                                     # porch floor (feet)
KEV = 1.6                                          # Kevin is drawn 1.6x the people scale (12 ft)
WHEELIE = dict(rot=16.0, pivot=(-24.0, 0.5))


def mouth(who, t, k=1.8):
    return min(1.0, talk(who, t) * k)


def grim_kw(t, **kw):
    kw.setdefault('mouth_', mouth('grim', t))
    return kw


def cu(world, light, fn, t, cx, cy, s, head, Z=1.4, flip=False, blur=0, pre_=None, fx_=None, pin='head', extra=(), **kw):
    """close-up: the sprite anchor `pin` sits at output point `head`; the background is zoomed only Z (<= ~1.45) and optionally soft"""
    kw.setdefault('t', t)
    v0 = view_at(world, cx, cy, Z, 180, 320)
    hx, hy = wpt(v0, *head)
    a = A(fn, hx, hy, s, flip=flip, pin=pin, **kw)
    def pre(big, v):
        if pre_: pre_(big, v)
        if blur: big[:] = K.dof(big, blur)
    big = K.shot(world, light, cx, cy, Z, acts=list(extra) + [a], pre=pre, fx_=(lambda b, v: fx_(b, v, a)) if fx_ else None, sx=180, sy=320)
    return big, a


# ================================================================== shots
def put(v, fn, ox, oy, s, **kw):
    """an actor whose feet anchor lands on output point (ox, oy) of view v; sprites above ~7 px per sprite px are drawn at 2x"""
    if s > 7.0: kw.setdefault('hires', True)
    return A(fn, *wpt(v, ox, oy), s, **kw)


def r_hook(t, u, loop=False):
    """0.0: Death pops a wheelie on the e-bike down a Halloween street under the full moon, cloak and scythe streaming, lightning"""
    tt = t if not loop else t - 36.0
    cx = 380.0 + 70.0 * tt
    v = view_at(STREET, cx, 330.0, 1.25, 180, 320)
    bob = 10.0 * math.sin(t * 9.0)
    rot = 22.0 + 3.0 * math.sin(t * 5.0)
    if loop: rot = 22.0 * sm(min(1.0, u / 0.25)) + 3.0 * math.sin(t * 5.0)
    g = put(v, GC.grim, 560, 1790 + bob, 9.8, t=t, expr='proud' if not loop else 'angry', mouth_=mouth('grim', t) if not loop else 0.5, wind=1.0,
            spin=t * 26, batt=13, raven=True, raven_expr='deadpan', rot=rot, pivot=WHEELIE['pivot'])
    def f(big, v_):
        K.speed_streaks(big, t, 0.8)
        K.leaves(big, t, 22, seed=2, speed=1.6)
    big = K.shot(STREET, K.light_street, cx, 330.0, 1.25, acts=[g], fx_=f, sx=180, sy=320)
    K.lightning(big, t, 0.0 if not loop else 36.02, seed=3)
    B.shake(big, t, 4, 30)
    return big


def r_reveal(t, u):
    """wide crossing: he rides past the decorated houses (the scythe zip-tied to the rack, Edgar on the bar)"""
    v = view_at(STREET, 450.0 + 30 * u, 380.0, 1.3, 180, 320)
    g = put(v, GC.grim, lerp(120.0, 980.0, u / 1.5), 1700, 4.6, t=t, expr='proud', mouth_=mouth('grim', t), wind=0.8, spin=t * 22, raven=True)
    def f(big, v_):
        K.leaves(big, t, 16, seed=5)
        K.fog(big, t, 1500, OUT_H, 0.18)
    return K.shot(STREET, K.light_street, 450.0 + 30 * u, 380.0, 1.3, acts=[g], fx_=f, sx=180, sy=320)


def r_display(t, u):
    """insert: the handlebar display BATTERY 13% blinking; Edgar perched on the bar says it to camera"""
    v = view_at(STREET, 600.0, 520.0, 2.0, 180, 320)
    big = K.dof(v.bg(), 9)
    K.display_insert(big, t, 13, y0=140, y1=1000)
    sp = GX.draw(GC.edgar, 19.0, t=t, expr='deadpan', mouth_=mouth('edgar', t, 2.0), cam=True, look=(0.0, 0.0))
    blit(big, sp, 560, 1720 + 6 * math.sin(t * 3), 19.0, K.light_street(v))
    fx.vignette(big, 0.3)
    return big


def r_app(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    K.phone_app(big, t, 'pickup', u)
    return big


def r_todd(t, u):
    """Todd on his lawn filming everything, thrilled"""
    big, _ = cu(YARD, K.light_yard, GC.todd, t, 600.0, 430.0, 15.0, (560, 860), Z=1.4, blur=0, expr='hype', mouth_=mouth('todd', t),
                look=(-1.0, 0.0), phone=True, flip=True)
    K.fog(big, t, 1450, OUT_H, 0.22)
    return big


def r_arrive(t, u):
    """wide: he rides in on the sidewalk and brakes by Todd (skid); Kevin the 12-ft skeleton looms; sign HALLOWEEN IN: 5 DAYS"""
    v = view_at(YARD, 560.0, 400.0, 1.35, 180, 320)
    k = sm(min(1.0, u / 0.75))
    gx = lerp(-150.0, 470.0, k)
    acts = [put(v, GC.kevin, 250, 1480, 6.0, t=t),
            put(v, GC.pumpkin_inflatable, 1080, 1470, 6.0, t=t),
            put(v, GC.countdown_sign, 690, 1560, 4.4, days=5),
            put(v, GC.todd, 860, 1600, 5.0, t=t, expr='hype', mouth_=mouth('todd', t), look=(-1.0, 0.0), flip=True, phone=True),
            put(v, GC.grim, gx, 1830, 5.0, t=t, expr='proud', mouth_=0.0, wind=0.5 * (1 - k), spin=gx * 0.05, raven=True)]
    def f(big, v_):
        if 0.55 < k < 0.99:
            for i in range(5): B.puff(big, gx - 120 - 40 * i, 1810, 30 + 10 * i, 0.4, (170, 150, 190))
        K.fog(big, t, 1400, OUT_H, 0.2)
    return K.shot(YARD, K.light_yard, 560.0, 400.0, 1.35, acts=acts, fx_=f, sx=180, sy=320)


def r_shout(t, u):
    """«I am DEATH!»: close on the skull, eyes blazing, lightning"""
    def f(big, v, a):
        hx, hy = aout(a, v, 'eyes')
        K.glow_ring(big, hx, hy, 260, K.GC.GLOW, 0.35 * (1 - min(1.0, u / 1.2)))
    big, _ = cu(YARD, K.light_yard, GC.grim, t, 520.0, 430.0, 13.0, (520, 880), Z=1.4, fx_=f,
                **grim_kw(t, expr='angry', wind=0.9, raven=False, glow=1.0, pose='shout', shake=1.0 if u < 0.6 else 0.0))
    K.lightning(big, t, 9.33, seed=7)
    if u < 0.5: B.shake(big, t, 10, 34)
    return big


def r_compare(t, u):
    """low wide: Death on his bike barely reaches Kevin's knee; Kevin's head turns down to him; Todd, pitying"""
    v = view_at(YARD, 470.0, 330.0, 1.45, 180, 320)
    turn = sm(min(1.0, max(0.0, (u - 0.5) / 0.8))) * 0.9
    acts = [put(v, GC.kevin, 360, 1640, 8.6, t=t, turn=turn),
            put(v, GC.todd, 1010, 1720, 5.4, t=t, expr='pity', mouth_=mouth('todd', t), look=(-1.0, -0.2), flip=True, phone=True),
            put(v, GC.grim, 700, 1850, 5.0, t=t, expr='stunned', mouth_=0.0, raven=True, look=(-0.4, 0.6))]
    return K.shot(YARD, K.light_yard, 470.0, 330.0, 1.45, acts=acts, sx=180, sy=320)


def r_shortking(t, u):
    v = view_at(YARD, 520.0, 470.0, 1.6, 180, 320)
    big = K.dof(v.bg(), 8)
    sp = GX.draw(GC.edgar, 20.0, t=t, expr='deadpan', mouth_=mouth('edgar', t, 2.0), cam=True, look=(0.0, 0.0))
    blit(big, sp, 540, 1640, 20.0, K.light_yard(v))
    fx.vignette(big, 0.3)
    return big


def r_loom(t, u):
    """the porch: Harold rocks under the porch light, helmet already on; a tarp lump beside him («UNLOCKED» peeks out);
    Death looms in the foreground, claws up"""
    v = view_at(PORCH, 330.0, 380.0, 1.45, 180, 320)
    rock = 2.0 * math.sin(t * 2.4)
    har = put(v, GC.harold, 300, 1330, 7.0, t=t, pose='rock', rock=rock, expr='bored', mouth_=mouth('harold', t), look=(1.0, -0.2),
              rot=rock * 1.5, pivot=(0.0, 0.0))
    tarp = put(v, GC.tarp, 640, 1330, 7.0, t=t)
    hx, hy = wpt(v, 760, 1100)
    g = A(GC.grim, hx, hy, 10.5, t=t, flip=True, pin='head', ride=False, pose='loom', expr='menace', mouth_=mouth('grim', t), wind=0.3,
          look=(1.0, -0.3), scythe=True, hires=True)
    def f(big, v_):
        K.fog(big, t, 1500, OUT_H, 0.2)
    return K.shot(PORCH, K.light_porch, 330.0, 380.0, 1.45, acts=[tarp, har, g], fx_=f, sx=180, sy=320)


def r_harold(t, u):
    rock = 1.5 * math.sin(t * 2.4)
    big, _ = cu(PORCH, K.light_porch, GC.harold, t, 260.0, 380.0, 14.0, (520, 920), Z=1.4, pose='rock', rock=rock, expr='bored',
                mouth_=mouth('harold', t), look=(1.0, -0.1), rot=rock * 1.2, pivot=(0.0, 0.0))
    return big


def r_smug(t, u):
    big, _ = cu(PORCH, K.light_porch, GC.grim, t, 900.0, 430.0, 13.0, (560, 880), Z=1.4, flip=True,
                **grim_kw(t, ride=False, pose='stand', expr='smug', look=(1.0, 0.0), wind=0.2))
    return big


def r_twist(t, u):
    """the tarp flies off: Harold on his black unlocked e-trike, flames, flag, headlight — «Catch me, BONES.» The chair keeps rocking."""
    v = view_at(PORCH, 370.0, 380.0, 1.45, 180, 320)
    lift = sm(min(1.0, u / 0.3))
    rock = 2.5 * math.sin(t * 3.0)
    chair = put(v, lambda sp, **k: GC.rocking_chair(sp, rock), 230, 1330, 7.0, rot=rock * 1.5)
    go = sm(min(1.0, max(0.0, (u - 1.15) / 0.45)))
    hx = lerp(560.0, 1500.0, go)
    har = put(v, GC.harold, hx, 1420, 9.6, t=t, pose='ride', spin=-t * 18 * (u > 1.1), expr='grin', mouth_=mouth('harold', t),
              look=(-1.0, 0.0), flag=1.0)
    acts = [chair, har]
    if lift < 1.0: acts.append(put(v, GC.tarp, 560 - 260 * lift, 1420 - 600 * lift, 9.6, t=t, lift=lift))
    def f(big, v_):
        K.glow_ring(big, hx + 230, 1300, 320, (255, 230, 160), 0.35)
        if u > 1.1: K.speed_streaks(big, t, 0.5)
    big = K.shot(PORCH, K.light_porch, 370.0, 380.0, 1.45, acts=acts, fx_=f, sx=180, sy=320)
    if u < 0.35: B.shake(big, t, 9, 32)
    return big


def r_launch(t, u):
    """the trike jumps off the porch over the steps, straight over Death, who spins round"""
    v = view_at(PORCH, 760.0, 430.0, 1.3, 180, 320)
    k = min(1.0, u / 1.2)
    ox = lerp(-150.0, 1300.0, k); oy = lerp(1250.0, 1700.0, k) - 900.0 * 4 * k * (1 - k)
    har = put(v, GC.harold, ox, oy, 6.4, t=t, pose='ride', spin=-t * 30, expr='grin', mouth_=mouth('harold', t), look=(1.0, 0.0),
              rot=-14.0 * (1 - k) + 8.0 * k)
    g = put(v, GC.grim, 560, 1820, 6.0, t=t, ride=False, pose='claw', expr='panic' if k < 0.9 else 'stunned', mouth_=0.3, flip=k < 0.5,
            look=(1.0, 0.6), wind=0.6)
    def f(big, v_):
        K.speed_streaks(big, t, 0.4)
        K.leaves(big, t, 18, seed=8, speed=2.0)
    return K.shot(PORCH, K.light_porch, 760.0, 430.0, 1.3, acts=[g, har], fx_=f, sx=180, sy=320)


def r_chase(t, u):
    """crossing chase down the street: Harold ahead (flag snapping), Death pedalling like mad behind; battery 4%"""
    cx = 380.0 + 200.0 * u
    v = view_at(STREET, cx, 380.0, 1.35, 180, 320)
    har = put(v, GC.harold, 860 + 30 * math.sin(t * 2), 1640, 6.0, t=t, pose='ride', spin=-t * 34, expr='grin', mouth_=0.0, look=(-1.0, 0.0),
              flag=1.4)
    g = put(v, GC.grim, 250 - 20 * math.sin(t * 2), 1780 + 8 * math.sin(t * 14), 6.4, t=t, expr='panic', mouth_=mouth('grim', t), wind=1.0,
            spin=t * 40, crank=t * 30, batt=4, raven=True, lean=2.0)
    def f(big, v_):
        K.speed_streaks(big, t, 1.0)
        K.leaves(big, t, 24, seed=9, speed=2.4)
    return K.shot(STREET, K.light_street, cx, 380.0, 1.35, acts=[g, har], fx_=f, sx=180, sy=320)


def r_gang(t, u):
    """the masked e-bike gang overtakes Death in a wheelie formation; Kayden, nearest, glances over: «Relax, pal.»"""
    cx = 520.0 + 120.0 * u
    v = view_at(STREET, cx, 380.0, 1.35, 180, 320)
    acts = []
    for i, (oy, ox0, sp_, col, string) in enumerate(((1560, -350, 800, (70, 50, 82), (255, 120, 200)), (1640, -550, 850, (46, 70, 64), (255, 220, 60)),
                                                     (1830, -150, 750, GC.HOODIE, GC.LIME))):
        acts.append(put(v, GC.kayden, ox0 + sp_ * u, oy, 6.2 + 0.8 * (oy - 1560) / 270, t=t, spin=-t * 40, col=col, string=string, n=i,
                        expr='bored', look=(0.3 if i < 2 else -0.8, 0.0), rot=13.0 + 2 * math.sin(t * 6 + i), pivot=(-22.0, 0.5)))
    g = put(v, GC.grim, 640, 1740, 5.6, t=t, expr='stunned', mouth_=0.0, wind=0.6, spin=t * 22, batt=2, raven=True, look=(-0.2, 0.0))
    order = [acts[0], acts[1], g, acts[2]]
    def f(big, v_):
        K.speed_streaks(big, t, 0.7)
    return K.shot(STREET, K.light_street, cx, 380.0, 1.35, acts=order, fx_=f, sx=180, sy=320)


def r_dead(t, u):
    """the display: 1% -> 0% -> black; then Death coasts to a stop, Edgar to camera: «Dead battery. Ironic.»"""
    if u < 0.75:
        v = view_at(STREET, 700.0, 520.0, 2.0, 180, 320)
        big = K.dof(v.bg(), 9)
        K.display_insert(big, t, 1 if u < 0.35 else 0, dead=u > 0.42, y0=140, y1=1000)
        fx.vignette(big, 0.3)
        return big
    v = view_at(STREET, 780.0, 420.0, 1.4, 180, 320)
    g = put(v, GC.grim, 470, 1700, 8.0, t=t, expr='sad', mouth_=0.0, dead=True, batt=0, raven=False, look=(0.6, -0.6), wind=0.0)
    big = K.shot(STREET, K.light_street, 780.0, 420.0, 1.4, acts=[g], sx=180, sy=320)
    big[:] = K.dof(big, 3)
    sp = GX.draw(GC.edgar, 17.0, t=t, expr='deadpan', mouth_=mouth('edgar', t, 2.0), cam=True, look=(0.0, 0.0))
    blit(big, sp, 760, 1880, 17.0, K.light_street(v))
    return big


def r_rated(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    K.phone_app(big, t, 'rated', u)
    return big


def raisin(big, x, y, s=1.0):
    w, h = int(46 * s), int(60 * s)
    x, y = int(x - w / 2), int(y - h / 2)
    if 0 <= x < OUT_W - w and 0 <= y < OUT_H - h:
        big[y - 4:y + h + 4, x - 4:x + w + 4] = GX.INK
        big[y:y + h, x:x + w] = (120, 40, 140)
        big[y + h // 3:y + 2 * h // 3, x + 6:x + w - 6] = (250, 220, 90)


def r_button(t, u):
    """Death stands by the dead bike; Harold laps him, tosses a raisin box — BONK off the hood: «Happy Halloween, KID!»"""
    v = view_at(STREET, 760.0, 380.0, 1.4, 180, 320)
    bonk = t >= 35.17
    g = put(v, GC.grim, 640, 1660, 6.6, t=t, expr='angry' if bonk else 'sad', mouth_=0.0, dead=True, batt=0, raven=True, look=(-0.8, 0.0),
            jaw_drop=1.5 if bonk and t < 35.52 else 0.0)
    hx_ = lerp(-300.0, 1400.0, min(1.0, u / 1.7))
    har = put(v, GC.harold, hx_, 1850, 7.0, t=t, pose='ride', spin=-t * 34, expr='grin', mouth_=mouth('harold', t), look=(1.0, 0.0),
              flag=1.4, toss=1.0 if 34.62 < t < 35.02 else 0.0)
    def f(big, v_):
        K.speed_streaks(big, t, 0.4)
        hx, hy = aout(g, v_, 'hood_top')
        if 34.72 <= t < 35.17:
            q = (t - 34.72) / 0.45
            sx, sy = hx_ + 60, 1500
            raisin(big, lerp(sx, hx, q), lerp(sy, hy, q) - 240 * 4 * q * (1 - q), 1.6)
        elif 35.17 <= t < 35.62:
            q = (t - 35.17) / 0.45
            raisin(big, hx + 120 * q, hy - 200 * q + 400 * q * q, 1.6)
            for i in range(5):
                a = i * 1.26 + t * 4
                cx, cy = hx + math.cos(a) * 80, hy - 40 + math.sin(a) * 30
                big[int(cy):int(cy) + 14, int(cx):int(cx) + 14] = (255, 236, 120)
    return K.shot(STREET, K.light_street, 760.0, 380.0, 1.4, acts=[g, har], fx_=f, sx=180, sy=320)


def r_loop(t, u):
    return r_hook(t, u, loop=True)


SHOTS = [r_hook, r_reveal, r_display, r_app, r_todd, r_arrive, r_shout, r_compare, r_shortking, r_loom, r_harold, r_smug, r_twist, r_launch,
         r_chase, r_gang, r_dead, r_rated, r_button, r_loop]
NAMES = ['hook', 'reveal', 'display', 'app', 'todd', 'arrive', 'shout', 'compare', 'shortking', 'loom', 'harold', 'smug', 'twist', 'launch',
         'chase', 'gang', 'dead', 'rated', 'button', 'loop']
CAP = dict(hook=1640, display=1120, app=1760, rated=1760, todd=1560, shout=1560, harold=1600, smug=1560, shortking=1180, dead=900)

SHOW = K.Show(EPI, 1, ['DEATH GOT', 'AN E-BIKE?'], hook_t=(0.10, 3.0), hook_y=150, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('AFTERLIFEPAY x4', (200, 170, 255), 46), 3.85, 5.5, 540, 1080),
                        (K.st('EASY PICKUP!', (150, 255, 110), 52), 5.62, 6.3, 540, 420),
                        (K.st('12 FT', (255, 236, 120), 70), 11.7, 13.4, 640, 330),
                        (K.st('28 MPH?!', (255, 140, 40), 72), 21.9, 23.6, 560, 420),
                        (K.st('BATTERY 4%', (255, 90, 80), 52), 25.6, 27.5, 540, 380)],
              flashes=[21.80], mosaics=[3.60, 32.55])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
