"""S01E02 «Verify You're Human» (06.10.2026) — Harold is faster, so Death needs a speed unlock. The DoomDash app first wants a captcha:
«Select all squares with a PULSE» — every square Death taps flatlines (Harold's keeps beating). The support bot Dashley: «Are you a
HUMAN?» — «I am DEATH!» — «Sorry, I didn't catch that!» Instead of an unlock: «your bike is now Class ONE». «Transferring you to a
specialist...» TWIST (59 %, bureaucratic recursion): the phone in his own cloak rings — DOOMDASH SUPPORT is calling the specialist:
him. «Hello?» — «...hello?» Edgar: «Promoted.» «The specialist is unavailable!» — «I'M AVAILABLE!» Harold zooms past: «Evening,
Bones!» Button: «Your estimated wait time is ETERNITY!» — «That's MY line.» Loop: the captcha again.
  python3 ep02.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props.grimshots import Kit, put, rings, A, wpt, aout, WALK, LAWN
from props.dibspix import blit
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
KIT = Kit(EPI)
mouth = KIT.mouth
YARD = KIT.YARD
DAYS = 4
TAPS = [(0, 0.12), (4, 0.27), (5, 0.42), (2, 0.55)]          # Todd, Kayden, Edgar flatline; Harold keeps beating
CHAT1 = [('bot', "Oopsie! Let's try again. Are you a HUMAN?", 0.0)]
CHAT2 = [('bot', "Oopsie! Let's try again. Are you a HUMAN?", -9), ('me', 'I am DEATH!', -9), ('bot', "Sorry, I didn't catch that!", 0.05)]


def grim_cu(t, u, expr, pose='phone', head=(540, 900), sc=13.0, cx=560.0, **kw):
    kw.setdefault('mouth_', mouth('grim', t))
    big, a = KIT.cu(YARD, K.light_yard, GC.grim, t, cx, 430.0, sc, head, Z=1.4, expr=expr, pose=pose, wind=0.0, spin=0.0, raven=False, **kw)
    return big, a


def phone_glow(big, v, a):
    if 'phone' in a.last.anchors:
        px, py = aout(a, v, 'phone')
        K.glow_ring(big, px, py, 360, (120, 255, 200), 0.22)


# ================================================================== shots
def r_hook(t, u):
    """0.0: split — Death squints at his phone (lit green by the screen) / the captcha below: SELECT ALL SQUARES WITH A PULSE"""
    top, _ = grim_cu(t, u, 'squint', head=(600, 700), sc=12.5, fx_=phone_glow, look=(0.4, -0.6))
    ph = KIT.phone(t, 'captcha', 0.0, taps=())
    small = np.array(Image.fromarray(ph[280:1560, 100:980]).resize((660, 960), Image.NEAREST))
    big = top
    big[960:1920] = (big[960:1920] * 0.3).astype(np.uint8)
    big[960:1920, 210:870] = small
    big[952:960] = GX.INK
    return big


def r_taps(t, u):
    big = KIT.phone(t, 'captcha', u, taps=TAPS)
    for i, ut in TAPS:                                                   # the bony fingertip jabs each tile
        if ut - 0.08 <= u < ut + 0.1:
            x0 = 160 + (i % 3) * 270 + 120; y0 = 560 + (i // 3) * 270 + 120
            sp = GX.draw(GC.bony_hand, 16.0, x=0.0, y=0.0, d=-1.0, grip=False, point=True)
            blit(big, sp, x0 + 60, y0 + 40, 16.0)
    if u > 0.55: B.shake(big, t, 4, 30)
    return big


def r_oops(t, u):
    return KIT.edgar_cu(YARD, K.light_yard, t)


def r_chat1(t, u):
    return KIT.phone(t, 'chat', u, msgs=CHAT1)


def r_death(t, u):
    def f(big, v, a):
        hx, hy = aout(a, v, 'eyes')
        K.glow_ring(big, hx, hy, 260, GC.GLOW, 0.35 * (1 - min(1.0, u / 1.2)))
    big, _ = grim_cu(t, u, 'angry', pose='shout', fx_=f, shake=1.0 if u < 0.6 else 0.0)
    K.lightning(big, t, 6.88, seed=7)
    if u < 0.5: B.shake(big, t, 10, 34)
    return big


def r_chat2(t, u):
    return KIT.phone(t, 'chat', u, msgs=CHAT2)


def r_teeth(t, u):
    big, _ = grim_cu(t, u, 'menace', head=(560, 880), sc=14.0 + 1.2 * u / 3.2, fx_=phone_glow, look=(0.6, -0.5))
    return big


def r_class(t, u):
    v = view_at(YARD, 560.0, 520.0, 2.0, 180, 320)
    big = K.dof(v.bg(), 9)
    k = min(1.0, max(0.0, (u - 0.6) / 0.5))
    mph = '20' if k < 0.5 else '12'
    K.display_insert(big, t, 13, y0=200, y1=1100, label='PALE HORSE 2', mph=mph + ' MAX', banner='CLASS 1' if k >= 0.5 else 'CLASS 3')
    if 0.55 < u < 0.75: B.shake(big, t, 8, 30)
    fx.vignette(big, 0.3)
    return big


def r_transfer(t, u):
    return KIT.phone(t, 'transfer', u)


def yard_wide(t, u, pose, expr, harold_x=None, ring=False, look=(0.6, 0.0)):
    v = view_at(YARD, 560.0, 400.0, 1.35, 180, 320)
    acts = [put(v, GC.kevin, 250, 1480, 6.0, t=t),
            put(v, GC.countdown_sign, 700, 1560, 4.4, days=DAYS)]
    if harold_x is not None:
        acts.append(put(v, GC.harold, harold_x, 1830, 6.4, t=t, pose='ride', spin=-t * 34, expr='grin', mouth_=mouth('harold', t),
                        look=(1.0, 0.0), flag=1.4, wave=1.0))
    g = put(v, GC.grim, 470, 1780, 6.4, t=t, expr=expr, mouth_=mouth('grim', t), pose=pose, raven=True, look=look, spin=0.0)
    acts.insert(2, g)
    def f(big, v_):
        if ring:
            px, py = aout(g, v_, 'pocket')
            rings(big, px, py, t)
        K.fog(big, t, 1450, OUT_H, 0.2)
        if harold_x is not None: K.speed_streaks(big, t, 0.5)
    return K.shot(YARD, K.light_yard, 560.0, 400.0, 1.35, acts=acts, fx_=f, sx=180, sy=320)


def r_twist(t, u):
    """TWIST: on hold — and the phone in his own cloak rings: DOOMDASH SUPPORT calling... the specialist. He answers both."""
    if u < 0.6:
        big = yard_wide(t, u, 'ear', 'stunned', ring=True, look=(-0.6, -0.8))
        if u < 0.25: B.shake(big, t, 8, 30)
        return big
    # split: phone A (on hold) | phone B (incoming: DOOMDASH SUPPORT)
    a = KIT.phone(t, 'transfer', u)
    b = KIT.phone(t, 'incoming', u)
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    big[:, :540] = np.array(Image.fromarray(a).resize((540, OUT_H), Image.NEAREST))
    big[:, 540:] = np.array(Image.fromarray(b).resize((540, OUT_H), Image.NEAREST))
    big[:, 534:546] = GX.INK
    return big


def r_promoted(t, u):
    return KIT.edgar_cu(YARD, K.light_yard, t, expr='sly')


def r_listen(t, u):
    big, _ = grim_cu(t, u, 'stunned', pose='twophones', head=(540, 860), sc=13.0, look=(0.0, -0.3))
    return big


def r_available(t, u):
    big, a = grim_cu(t, u, 'angry', pose='twophones', head=(540, 900), sc=14.5, look=(0.8, -0.2), shake=1.0, jaw_drop=1.0)
    if u < 1.2: B.shake(big, t, 9, 34)
    return big


def r_harold(t, u):
    hx = lerp(-300.0, 1400.0, min(1.0, u / 1.3))
    return yard_wide(t, u, 'twophones', 'whine', harold_x=hx, look=(-1.0, 0.0))


def r_wait(t, u):
    return KIT.phone(t, 'wait', u)


def r_broken(t, u):
    big, _ = grim_cu(t, u, 'sad', pose='twophones', head=(540, 880), sc=13.0 + 0.8 * u, look=(0.0, -0.7))
    return big


def r_loop(t, u):
    return KIT.phone(t, 'captcha', 0.0, taps=())


SHOTS = [r_hook, r_taps, r_oops, r_chat1, r_death, r_chat2, r_teeth, r_class, r_transfer, r_twist, r_promoted, r_listen, r_available,
         r_harold, r_wait, r_broken, r_loop]
NAMES = ['hook', 'taps', 'oops', 'chat1', 'death', 'chat2', 'teeth', 'class', 'transfer', 'twist', 'promoted', 'listen', 'available',
         'harold', 'wait', 'broken', 'loop']
CAP = dict(hook=900, taps=1700, oops=1180, chat1=1700, chat2=1760, transfer=1700, twist=1700, promoted=1180, wait=1700, loop=1700,
           death=1560, teeth=1600, listen=1600, available=1620, broken=1600, harold=1060, **{'class': 1300})

SHOW = K.Show(EPI, 2, ['DEATH VS', 'CAPTCHA?'], hook_t=(0.10, 2.5), hook_y=150, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('CLASS ONE', (255, 200, 60), 64), 15.0, 17.2, 540, 1460),
                        (K.st('SPECIALIST: YOU', (150, 255, 110), 50), 19.3, 21.4, 540, 300),
                        (K.st('ON HOLD', (200, 170, 255), 60), 23.6, 25.3, 540, 380)],
              flashes=[19.15], mosaics=[3.95, 26.70])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
