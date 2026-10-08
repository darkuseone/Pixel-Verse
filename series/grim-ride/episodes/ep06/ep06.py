"""S01E06 «Fall Back» (06.10.2026) — season finale, Halloween night, 1:59 AM. On the hilltop above town Death faces Harold: «One
minute, Harold.» Dashley: «Deactivation in ONE minute!» Flashback of the last chase: the masked gang tows Death on a rope («Relax, pal.
We GOT you.»), Todd blasts his fog machine («Go, buddy! FOG'S ON!»), Edgar: «Tick tock.» At the top Harold stops: «Alright, Bones.
I'm READY.» — «I am DEATH.» — «I know, kid. I KNOW.» 1:59:58... 1:59:59... TWIST (54 %, the clocks give it back): 2:00 -> 1:00,
DAYLIGHT SAVING TIME HAS ENDED. «Extra hour, kid. Wanna RIDE?» They wheelie through the town together, fireworks. «Pickup
rescheduled. Next HALLOWEEN!» Harold rates him five stars, «Great ride.» — «Five. STARS.» Button, Edgar: «Nevermore.»
SEASON 2: SPRING FORWARD. Season loop: the last frame is the pilot's first frame — Death's wheelie — now with Harold beside him.
  python3 ep06.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
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

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
KIT = Kit(EPI)
mouth = KIT.mouth
HILL, STREET, YARD = KIT.HILL, KIT.STREET, KIT.YARD
LH, LS, LY = K.light_hill, K.light_street, K.light_yard
HILL_VIEW = (560.0, 420.0, 1.2)


def hill_view():
    cx, cy, Z = HILL_VIEW
    return view_at(HILL, cx, cy, Z, 180, 320)


def summit(t, g_expr='menace', h_expr='bored', scythe=False, h_flip=True, g_mouth=None, h_mouth=None):
    v = hill_view()
    g = put(v, GC.grim, 300, 1820, 7.4, t=t, expr=g_expr, mouth_=mouth('grim', t) if g_mouth is None else g_mouth, spin=0.0, raven=True,
            look=(1.0, -0.1), pose='bar', wind=0.3)
    h = put(v, GC.harold, 800, 1840, 7.6, t=t, pose='ride', spin=0.0, expr=h_expr, mouth_=mouth('harold', t) if h_mouth is None else h_mouth,
            look=(-1.0, 0.0), flip=h_flip, flag=1.0)
    return v, [g, h]


def r_hook(t, u):
    """0.0: the hilltop at 1:59 AM — Death and Harold face off under the moon"""
    v, acts = summit(t, 'menace', 'bored')
    def f(big, v_):
        K.fog(big, t, 1500, OUT_H, 0.25)
        K.leaves(big, t, 10, seed=3)
    big = K.shot(HILL, LH, *HILL_VIEW[:2], HILL_VIEW[2], acts=acts, fx_=f, sx=180, sy=320)
    K.clock(big, '1:59 AM', None, 1.0, y=900, size=130)
    return big


def r_deadline(t, u):
    return KIT.phone(t, 'deadline', u)


def r_tow(t, u):
    """flashback: the masked gang tows Death on a rope through the town, wheelies, his battery long dead"""
    cx = 420.0 + 220.0 * u
    v = view_at(STREET, cx, 380.0, 1.35, 180, 320)
    kay = put(v, GC.kayden, 760, 1680, 6.6, t=t, spin=-t * 40, rot=12.0 + 2 * math.sin(t * 6), pivot=(-22.0, 0.5), look=(-1.0, 0.0),
              expr='smile', mouth_=mouth('kayden', t))
    k2 = put(v, GC.kayden, 1000, 1560, 5.6, t=t, spin=-t * 40, n=1, col=(70, 50, 82), string=(255, 120, 200), rot=14.0, pivot=(-22.0, 0.5))
    g = put(v, GC.grim, 260, 1760, 6.6, t=t, expr='awe', mouth_=0.3, spin=t * 30, raven=True, wind=1.0, batt=0, dead=True)
    def f(big, v_):
        a = aout(kay, v_, 'rear'); b = aout(g, v_, 'front')
        K.rope_line(big, (a[0] - 30, a[1] - 60), (b[0] + 30, b[1] - 70), sag=30)
        K.speed_streaks(big, t, 1.0); K.leaves(big, t, 20, seed=6, speed=2.4)
    return K.shot(STREET, LS, cx, 380.0, 1.35, acts=[k2, g, kay], fx_=f, sx=180, sy=320)


def r_fog(t, u):
    """Todd blasts a wall of fog over the road for them; the sign says HALLOWEEN IN: 0 DAYS"""
    v = view_at(YARD, 560.0, 400.0, 1.35, 180, 320)
    acts = [put(v, GC.kevin, 250, 1480, 6.0, t=t, turn=0.4),
            put(v, GC.countdown_sign, 690, 1560, 4.4, days=0),
            put(v, GC.todd, 860, 1620, 6.0, t=t, flip=True, expr='cheer', mouth_=mouth('todd', t), look=(-1.0, 0.0), phone=False, point=1.0)]
    gx = lerp(-200, 1300, u / 1.9)
    acts.append(put(v, GC.grim, gx, 1860, 6.2, t=t, expr='awe', mouth_=0.3, spin=t * 30, raven=True, wind=1.0, batt=0, dead=True))
    def f(big, v_):
        K.fog(big, t, 1100, OUT_H, 0.45, speed=160)
        K.speed_streaks(big, t, 0.5)
    return K.shot(YARD, LY, 560.0, 400.0, 1.35, acts=acts, fx_=f, sx=180, sy=320)


def r_tick(t, u):
    v = view_at(STREET, 640.0, 470.0, 1.6, 180, 320)
    big = K.dof(v.bg(), 8)
    K.speed_streaks(big, t, 0.7)
    sp = GX.draw(GC.edgar, 20.0, t=t, expr='deadpan', mouth_=mouth('edgar', t, 2.0), cam=True, look=(0.0, 0.0), flap=0.3 * math.sin(t * 20))
    blit(big, sp, 540, 1640, 20.0, LS(v))
    fx.vignette(big, 0.3)
    return big


def r_ready(t, u):
    """the top of the hill: Harold stops and turns round to Death"""
    v, acts = summit(t, 'stunned', 'content', h_flip=u > 0.5)
    def f(big, v_): K.fog(big, t, 1500, OUT_H, 0.25)
    return K.shot(HILL, LH, *HILL_VIEW[:2], HILL_VIEW[2], acts=acts, fx_=f, sx=180, sy=320)


def r_soft(t, u):
    big, _ = KIT.cu(HILL, LH, GC.grim, t, 520.0, 430.0, 13.0, (540, 900), Z=1.4, ride=True, pose='bar', raven=False, spin=0.0,
                    expr='sad', mouth_=mouth('grim', t), look=(1.0, -0.2), glow=0.7)
    return big


def r_know(t, u):
    big, _ = KIT.cu(HILL, LH, GC.harold, t, 760.0, 430.0, 14.0, (560, 880), Z=1.4, pose='ride', flip=True, expr='smile', mouth_=mouth('harold', t),
                    look=(-1.0, 0.0))
    return big


def r_count(t, u):
    """1:59:58 ... 1:59:59 — the scythe rises against the moon"""
    v = view_at(HILL, 900.0, 300.0, 1.3, 180, 320)
    big = v.bg().copy()
    g = put(v, GC.grim, 420, 2050, 9.0, t=t, ride=False, pose='loom', scythe=True, expr='sad', look=(1.0, 0.4), rot=-10.0 * min(1.0, u / 0.9),
            pivot=(0.0, 60.0))
    big = K.shot(HILL, LH, 900.0, 300.0, 1.3, acts=[g], sx=180, sy=320)
    K.clock(big, '1:59:58' if u < 0.45 else '1:59:59', None, 1.0, y=520, size=110)
    return big


def r_twist(t, u):
    """TWIST: 2:00 -> 1:00 — DAYLIGHT SAVING TIME HAS ENDED"""
    v, acts = summit(t, 'shock', 'grin', h_mouth=0.0, g_mouth=0.4)
    big = K.shot(HILL, LH, *HILL_VIEW[:2], HILL_VIEW[2], acts=acts, sx=180, sy=320)
    txt = '2:00' if u < 0.25 else ('1:00' if u > 0.45 else ('2:00' if int(u * 30) % 2 else '1:00'))
    K.clock(big, txt, 'DAYLIGHT SAVING\nTIME HAS ENDED' if u > 0.45 else None, 1.0, col=(150, 255, 110) if u > 0.45 else (255, 90, 80),
            y=760, size=180)
    if 0.25 < u < 0.45: O.mosaic(big, 24); fx.vhs(big, t, 1.0)
    return big


def r_ride(t, u):
    big, _ = KIT.cu(HILL, LH, GC.harold, t, 760.0, 430.0, 14.0, (560, 880), Z=1.4, pose='ride', flip=True, expr='grin', mouth_=mouth('harold', t),
                    look=(-1.0, 0.0), wave=1.0)
    return big


def r_montage(t, u):
    """they wheelie down into the town side by side — the gang behind, fireworks, confetti"""
    cx = 380.0 + 160.0 * u
    v = view_at(STREET, cx, 380.0, 1.35, 180, 320)
    g = put(v, GC.grim, 360, 1760, 6.8, t=t, expr='cheer', mouth_=mouth('grim', t), spin=t * 30, raven=True, wind=1.0, batt=100,
            rot=20.0 + 3 * math.sin(t * 5), pivot=(-24.0, 0.5))
    h = put(v, GC.harold, 800, 1820, 7.0, t=t, pose='ride', spin=-t * 34, expr='grin', mouth_=0.4, look=(-1.0, 0.0), flag=1.4,
            rot=8.0 + 2 * math.sin(t * 6), pivot=(-18.0, 0.5))
    gang = [put(v, GC.kayden, 120 + 40 * i, 1500 + 40 * i, 4.6, t=t, spin=-t * 40, n=i, col=[(70, 50, 82), GC.HOODIE, (46, 70, 64)][i],
                string=[(255, 120, 200), GC.LIME, (255, 220, 60)][i], rot=14.0, pivot=(-22.0, 0.5)) for i in range(3)]
    def f(big, v_):
        K.fireworks(big, t, 20.8)
        K.speed_streaks(big, t, 0.6)
        K.confetti(big, t, 21.0, n=90)
    return K.shot(STREET, LS, cx, 380.0, 1.35, acts=gang + [g, h], fx_=f, sx=180, sy=320)


def r_resched(t, u):
    return KIT.phone(t, 'resched', u)


def r_tears(t, u):
    big, _ = KIT.cu(STREET, LS, GC.grim, t, 640.0, 430.0, 13.5, (540, 900), Z=1.4, ride=True, pose='phone', raven=False, spin=0.0,
                    expr='teary', mouth_=mouth('grim', t), look=(0.6, -0.5))
    return big


def r_nevermore(t, u):
    return KIT.edgar_cu(HILL, LH, t, cx=900.0, cy=420.0, expr='content')


def r_title(t, u):
    """SEASON 2: SPRING FORWARD — the clock jumps forward an hour"""
    v = view_at(HILL, 900.0, 300.0, 1.3, 180, 320)
    big = K.dof(v.bg(), 4)
    big = (big * 0.6).astype(np.uint8)
    O.overlay(big, K.hook_title(['SEASON 2:', 'SPRING', 'FORWARD'], 84), 0, 520, min(1.0, u / 0.2))
    K.clock(big, '2:00' if u < 0.7 else '3:00', 'AN HOUR GONE', min(1.0, u / 0.3), col=(255, 90, 80), y=1500, size=120)
    return big


def r_loop(t, u):
    """season loop: the pilot's first frame — Death's wheelie down the street — now with Harold riding beside him"""
    tt = t - 31.6
    cx = 380.0 + 70.0 * tt
    v = view_at(STREET, cx, 330.0, 1.25, 180, 320)
    rot = 22.0 * sm(min(1.0, u / 0.25)) + 3.0 * math.sin(t * 5.0)
    g = put(v, GC.grim, 560, 1790, 9.8, t=t, expr='proud', mouth_=0.5, wind=1.0, spin=t * 26, batt=13, raven=True, rot=rot, pivot=(-24.0, 0.5))
    h = put(v, GC.harold, 980, 1880, 7.4, t=t, pose='ride', spin=-t * 30, expr='grin', look=(-1.0, 0.0), flag=1.4)
    def f(big, v_):
        K.speed_streaks(big, t, 0.8); K.leaves(big, t, 22, seed=2, speed=1.6)
    big = K.shot(STREET, LS, cx, 330.0, 1.25, acts=[h, g], fx_=f, sx=180, sy=320)
    K.lightning(big, t, 31.62, seed=3)
    return big


SHOTS = [r_hook, r_deadline, r_tow, r_fog, r_tick, r_ready, r_soft, r_know, r_count, r_twist, r_ride, r_montage, r_resched, r_tears,
         r_nevermore, r_title, r_loop]
NAMES = ['hook', 'deadline', 'tow', 'fog', 'tick', 'ready', 'soft', 'know', 'count', 'twist', 'ride', 'montage', 'resched', 'tears',
         'nevermore', 'title', 'loop']
CAP = dict(hook=1760, deadline=1760, tow=1080, fog=1060, tick=1180, ready=1720, count=1500, twist=1760, montage=1080, resched=1760,
           nevermore=1180, title=1800, loop=1640)

SHOW = K.Show(EPI, 6, ["DEATH'S LAST", 'MINUTE?'], hook_t=(0.10, 2.6), hook_y=150, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('+1 HOUR', (150, 255, 110), 72), 18.0, 20.5, 540, 420),
                        (K.st('5 STARS', (255, 210, 60), 64), 25.0, 26.0, 540, 1500)],
              flashes=[17.60, 31.60], mosaics=[4.55, 30.15])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
