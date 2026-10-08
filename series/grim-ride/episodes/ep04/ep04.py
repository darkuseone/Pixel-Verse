"""S01E04 «The Plug» (06.10.2026) — stuck at Class 1, Death goes to the dark gangway where the masked e-bike gang hangs out:
«I'm looking for the PLUG.» — «Who's ASKING?» — «I am DEATH.» — «Relax, pal.» — «Nice costume. Where'd you COP it?» — «It's NOT a
costume!» — «Bet.» He needs forty miles an hour: Harold's too fast. «Harold's a CUSTOMER.» TWIST (55 %, the villain is your own): Edgar
swoops down with his little fanny pack full of speed dongles — «Forty bucks. CASH.» — «EDGAR?!» — «A bird's gotta EAT.» — «You sold one
to HAROLD?!» — «He TIPS.» — «Family discount?» — «He's not FAMILY.» The dongle clicks in: UNLOCKED 40 MPH, the bike rockets over Todd's
lawn (HALLOWEEN IN: 2 DAYS) into the moon. Button, Edgar to camera: «No REFUNDS.» Loop: headlights in the gangway.
  python3 ep04.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
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

EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
KIT = Kit(EPI)
mouth = KIT.mouth
GANG, YARD = KIT.GANG, KIT.YARD
LG = K.light_gang
DAYS = 2
GCOL = [(70, 50, 82), GC.HOODIE, (46, 70, 64)]
GSTR = [(255, 120, 200), GC.LIME, (255, 220, 60)]


def headlights(big, pts, t, k=1.0):
    for (x, y) in pts:
        K.glow_ring(big, x, y, 240, (230, 240, 255), 0.45 * k)
        big[int(y) - 14:int(y) + 14, int(x) - 14:int(x) + 14] = (255, 255, 240)


def gang_acts(v, t, talk=True):
    acts, lights = [], []
    for i, (ox, oy, s) in enumerate(((430, 1360, 7.0), (900, 1390, 7.0), (680, 1580, 8.6))):
        n = 1 if i == 2 else (0 if i == 0 else 2)
        a = put(v, GC.kayden, ox, oy, s, t=t, flip=True, spin=0.0, n=i, col=GCOL[n], string=GSTR[n], expr='bored',
                look=(1.0, 0.0), rot=6.0 + 2 * math.sin(t * 3 + i), pivot=(-22.0, 0.5))
        acts.append(a)
        lights.append((ox - 21 * s, oy - 33 * s))
    return acts, lights


def r_hook(t, u, loop=False):
    """0.0: Death, blinded by e-bike headlights in a dark gangway, whispering"""
    def f(big, v, a):
        headlights(big, [(980, 760), (1060, 980), (900, 1200)], t, 1.0)
        K.fog(big, t, 1400, OUT_H, 0.25)
    big, _ = KIT.cu(GANG, LG, GC.grim, t, 520.0, 430.0, 13.5, (420, 900), Z=1.4, fx_=f, ride=True, pose='bar', raven=False, spin=0.0,
                    expr='nervous', mouth_=mouth('grim', t), look=(1.0, 0.0), wind=0.0, batt=13)
    return big


def r_gang(t, u):
    """the gang: three masked kids on electric dirt bikes in the fog, headlights on — «Who's ASKING?»"""
    v = view_at(GANG, 640.0, 420.0, 1.2, 180, 320)
    acts, lights = gang_acts(v, t)
    g = put(v, GC.grim, 40, 2060, 9.0, t=t, expr='nervous', mouth_=0.0, spin=0.0, raven=False, look=(1.0, -0.3))
    def f(big, v_):
        headlights(big, lights, t)
        K.fog(big, t, 1300, OUT_H, 0.25)
    return K.shot(GANG, LG, 640.0, 420.0, 1.2, acts=acts + [g], fx_=f, sx=180, sy=320)


def grim_cu(t, u, expr, head=(540, 900), sc=13.0, **kw):
    kw.setdefault('mouth_', mouth('grim', t))
    big, a = KIT.cu(GANG, LG, GC.grim, t, 560.0, 430.0, sc, head, Z=1.4, flip=True, ride=True, pose=kw.pop('pose', 'bar'), raven=False,
                    spin=0.0, expr=expr, wind=0.0, **kw)
    return big


def kay_cu(t, u, expr='bored', look=(1.0, 0.0)):
    def f(big, v, a):
        headlights(big, [(980, 1500)], t, 0.6)
    big, _ = KIT.cu(GANG, LG, GC.kayden, t, 700.0, 430.0, 13.0, (520, 820), Z=1.4, fx_=f, flip=True, spin=0.0, expr=expr, look=look)
    return big


def r_death(t, u):
    def f(big, v, a):
        hx, hy = aout(a, v, 'eyes')
        K.glow_ring(big, hx, hy, 200, GC.GLOW, 0.25 * (0.5 + 0.5 * math.sin(t * 30)))
    big, _ = KIT.cu(GANG, LG, GC.grim, t, 560.0, 430.0, 13.0, (560, 900), Z=1.4, flip=True, fx_=f, ride=True, pose='shout', raven=False,
                    spin=0.0, expr='menace', mouth_=mouth('grim', t), look=(1.0, 0.0), glow=0.6)
    return big


def r_relax(t, u): return kay_cu(t, u, 'bored')


def r_costume(t, u):
    """two-shot: Kayden rolls up close, sizing up the «costume»"""
    v = view_at(GANG, 640.0, 430.0, 1.3, 180, 320)
    k = put(v, GC.kayden, 760, 1720, 7.4, t=t, flip=True, spin=0.0, expr='squint', mouth_=0.0, look=(1.0, 0.3))
    g = put(v, GC.grim, 300, 1780, 7.4, t=t, expr='stunned', mouth_=0.0, spin=0.0, raven=False, look=(1.0, 0.0))
    def f(big, v_): headlights(big, [(1000, 1300)], t, 0.6); K.fog(big, t, 1400, OUT_H, 0.25)
    return K.shot(GANG, LG, 640.0, 430.0, 1.3, acts=[g, k], fx_=f, sx=180, sy=320)


def r_offended(t, u): return grim_cu(t, u, 'angry')


def r_bet(t, u): return kay_cu(t, u, 'deadpan', look=(0.0, 0.0))


def r_plead(t, u): return grim_cu(t, u, 'whine', head=(540, 880), sc=13.5)


def r_class(t, u):
    v = view_at(GANG, 640.0, 520.0, 2.0, 180, 320)
    big = K.dof(v.bg(), 9)
    K.display_insert(big, t, 13, y0=200, y1=1100, mph='12 MAX', banner='CLASS 1')
    fx.vignette(big, 0.3)
    return big


def r_customer(t, u): return kay_cu(t, u, 'sly', look=(1.0, -0.2))


def r_twist(t, u):
    """TWIST: Edgar swoops down out of the moon into the headlights and lands on a trash can — the fanny pack unzips: dongles"""
    v = view_at(GANG, 640.0, 420.0, 1.2, 180, 320)
    acts, lights = gang_acts(v, t)
    k = sm(min(1.0, u / 0.55))
    ex, ey = lerp(560, 640, k), lerp(150, 1220, k)
    e = put(v, GC.edgar, ex, ey, 14.0, t=t, expr='smug' if k >= 1 else 'deadpan', mouth_=mouth('edgar', t, 2.0), cam=k >= 1, look=(0.0, 0.0),
            flap=math.sin(t * 30) * (1 - k), stash=k >= 1, perch=False)
    g = put(v, GC.grim, 40, 2060, 9.0, t=t, expr='stunned', mouth_=0.0, spin=0.0, raven=False, look=(1.0, -0.6))
    def pre(big, v_):
        x0, y0 = v_.opt(888, 412)                                                    # the recycling bin under him
    def f(big, v_):
        headlights(big, lights, t)
        K.fog(big, t, 1300, OUT_H, 0.25)
        if k >= 1:
            K.glow_ring(big, ex + 30, ey - 40, 220, GC.PACK, 0.35)
    big = K.shot(GANG, LG, 640.0, 420.0, 1.2, acts=acts + [e, g], fx_=f, sx=180, sy=320)
    if 0.5 < u < 0.8: B.shake(big, t, 8, 30)
    return big


def edgar(t, u, expr='deadpan'):
    return KIT.edgar_cu(GANG, LG, t, cx=640.0, cy=470.0, sc=20.0, expr=expr, stash=True)


def r_shock(t, u):
    big = grim_cu(t, u, 'shock', head=(540, 880), sc=14.0, jaw_drop=2.0)
    if u < 0.4: B.shake(big, t, 9, 34)
    return big


def r_eat(t, u): return edgar(t, u, 'smug')


def r_harold(t, u): return grim_cu(t, u, 'angry', head=(540, 900), sc=13.0, pose='point')


def r_tips(t, u): return edgar(t, u, 'sly')


def r_discount(t, u): return kay_cu(t, u, 'smile', look=(1.0, 0.0))


def r_family(t, u): return edgar(t, u, 'deadpan')


def r_plug(t, u):
    """the dongle clicks into the display: UNLOCKED · 40 MPH, sparks"""
    v = view_at(GANG, 640.0, 520.0, 2.0, 180, 320)
    big = K.dof(v.bg(), 9)
    on = u > 0.15
    K.display_insert(big, t, 13, y0=200, y1=1100, mph='40' if on else '12 MAX', banner='UNLOCKED' if on else 'CLASS 1')
    dx = int(lerp(1100, 900, min(1.0, u / 0.15)))
    big[1040:1120, dx:dx + 200] = GX.INK; big[1050:1110, dx + 10:dx + 190] = (240, 240, 240)
    big[1060:1100, dx + 150:dx + 190] = GC.LIME
    if on and u < 0.5:
        r = np.random.default_rng(int(t * 30))
        for i in range(24):
            x, y = int(900 + r.random() * 260 - 130), int(1080 + r.random() * 200 - 100)
            big[y:y + 14, x:x + 14] = (255, 236, 120)
        B.shake(big, t, 10, 34)
    fx.vignette(big, 0.3)
    return big


def r_launch(t, u):
    """the bike rockets in a wheelie over Todd's lawn (HALLOWEEN IN: 2 DAYS) — straight up into the moon"""
    v = view_at(YARD, 560.0, 330.0, 1.25, 180, 320)
    k = u / 0.92
    ox, oy = lerp(-200, 1250, k), lerp(1850, 300, k * k)
    sign = put(v, GC.countdown_sign, 700, 1600, 4.6, days=DAYS)
    kev = put(v, GC.kevin, 250, 1500, 6.0, t=t, turn=-0.6 + 1.4 * k)
    g = put(v, GC.grim, ox, oy, 7.0, t=t, expr='panic', mouth_=0.6, wind=1.0, spin=t * 60, crank=t * 50, batt=13, raven=True,
            rot=24.0 + 20 * k, pivot=(-24.0, 0.5))
    def f(big, v_):
        K.speed_streaks(big, t, 1.0)
        for i in range(12):
            q = (t * 5 + i / 12) % 1.0
            x, y = int(ox - 150 - 300 * q), int(oy + 40 - 60 * q)
            if 0 <= x < OUT_W - 16 and 0 <= y < OUT_H - 16: big[y:y + 16, x:x + 16] = (255, 200, 80) if i % 2 else (255, 120, 40)
    return K.shot(YARD, K.light_yard, 560.0, 330.0, 1.25, acts=[kev, sign, g], fx_=f, sx=180, sy=320)


def r_button(t, u): return edgar(t, u, 'smug')


def r_loop(t, u): return r_hook(t, u, loop=True)


SHOTS = [r_hook, r_gang, r_death, r_relax, r_costume, r_offended, r_bet, r_plead, r_class, r_customer, r_twist, r_shock, r_eat, r_harold,
         r_tips, r_discount, r_family, r_plug, r_launch, r_button, r_loop]
NAMES = ['hook', 'gang', 'death', 'relax', 'costume', 'offended', 'bet', 'plead', 'class', 'customer', 'twist', 'shock', 'eat', 'harold',
         'tips', 'discount', 'family', 'plug', 'launch', 'button', 'loop']
CAP = dict(hook=1640, gang=1080, costume=1080, twist=900, eat=1180, tips=1180, family=1180, button=1180, launch=1500, plug=1300,
           **{'class': 1300})

SHOW = K.Show(EPI, 4, ['DEATH BUYS', 'A DONGLE?'], hook_t=(0.10, 2.6), hook_y=150, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('THE PLUG', (150, 255, 110), 70), 18.4, 20.6, 540, 420),
                        (K.st('$40 CASH', (255, 200, 60), 60), 19.2, 20.65, 760, 1880),
                        (K.st('40 MPH', (255, 90, 80), 72), 30.0, 31.4, 540, 1460)],
              flashes=[18.25, 30.50], mosaics=[14.40, 29.82])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
