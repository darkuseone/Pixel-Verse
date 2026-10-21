"""«Grim Ride: ONE MORE HOUR» — Halloween time-loop mini-movie, 16:9 1920x1080, rendered by shots (timeline.py).
  python3 movie.py sheet <shot|index> ...     mini sheet of shot middles (build/grim-ride-movie/msheet.png)
  python3 movie.py test|frames t ...  |  all [N]      (engine/episode.py CLI)
  python3 mix.py                              -> final_h264.mp4"""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine')); sys.path.insert(0, str(HERE))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import stage as ST
from stage import view_at, Light, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
import paths as P
from episode import Episode
from props import grimpix as GX
from props import grimcast as GC
from props import grimkit as K
from props import grimprops as GP
from props import bytfx as B
from props.dibspix import blit
import timeline as TL

assert (OUT_W, OUT_H) == (1920, 1080)
SX, SY = 320, 180
INK = GX.INK
EPI = Episode('movie', TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG, endcard=dict(style='default', lang='us', sec=3.0, cy=930))
BK = f'{TL.SLUG}-movie'
WHEELIE = dict(rot=22.0, pivot=(-24.0, 0.5))

STREET, YARD, PORCH, GANG, HILL = K.world('street'), K.world('todd_yard'), K.world('porch'), K.world('gangway'), K.world('hilltop')
LS, LY, LP, LG, LH = K.light_street, K.light_yard, K.light_porch, K.light_gang, K.light_hill
GREEN, RED, GOLD, VIOLET = (150, 255, 110), (255, 90, 80), (255, 210, 60), (200, 170, 255)


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


# ======================================================================================= camera helpers
def put(v, fn, ox, oy, s, **kw):
    """an actor whose feet land on output point (ox, oy) of view v; above ~3.8 px per sprite px the sprite is drawn at 2x"""
    if s > 3.8: kw.setdefault('hires', True)
    return K.A(fn, *K.wpt(v, ox, oy), s, **kw)


def W(wx, wy, cx, cy, Z):
    """world px -> output px for a view centred on (cx, cy) at zoom Z (1.5 output px per world px at Z = 1)"""
    return 960 + (wx - cx) * 1.5 * Z, 540 + (wy - cy) * 1.5 * Z


PS = dict(grim=4.3, harold=5.0, kid=6.5, clock=4.5, chair=5.0, edgar=4.0, mom=5.3)   # porch: sprite scale per unit of zoom
PFLOOR = 462.0                                    # the porch floor (world y); the door is at x ~360, steps x 260..780 down to y ~640


def wide(world, light, cx, cy, Z, specs, t=0.0, fx_=None, pre=None, vig=0.26):
    """specs: (fn, ox, oy, s, kwargs) placed in output px; fx_(big, v, acts)"""
    v = view_at(world, cx, cy, Z, SX, SY)
    acts = [put(v, fn, ox, oy, s, **kw) for fn, ox, oy, s, kw in specs]
    big = K.shot(world, light, cx, cy, Z, acts=acts, fx_=(lambda b, v_: fx_(b, v_, acts)) if fx_ else None, pre=pre, sx=SX, sy=SY,
                 vig=vig, t=t)
    return big


def cu(world, light, fn, tt, head, sc, cx=640.0, cy=360.0, Z=1.3, blur=3, flip=False, pin='head', back=(), fx_=None, **kw):
    """close-up: the sprite anchor `pin` at output point `head`; the background zoomed only Z, soft. back: extra specs drawn too"""
    kw.setdefault('t', tt); t = tt
    v = view_at(world, cx, cy, Z, SX, SY)
    a = K.A(fn, *K.wpt(v, *head), sc, flip=flip, pin=pin, hires=True, **kw)
    acts = [put(v, f, ox, oy, s, **k) for f, ox, oy, s, k in back] + [a]
    def pre(big, v_):
        if blur: big[:] = K.dof(big, blur)
    return K.shot(world, light, cx, cy, Z, acts=acts, pre=pre, fx_=(lambda b, v_: fx_(b, v_, a)) if fx_ else None, sx=SX, sy=SY, t=t)


def gk(t, expr='proud', **kw):
    """Grim kwargs: talking mouth, Edgar's beak when Edgar rides along"""
    kw.setdefault('mouth_', mouth('grim', t))
    if kw.get('raven'): kw.setdefault('raven_mouth', mouth('edgar', t, 2.0))
    return dict(t=t, expr=expr, **kw)


def hk(t, expr='bored', **kw):
    kw.setdefault('mouth_', mouth('harold', t))
    return dict(t=t, expr=expr, **kw)


def grim_cu(world, light, t, expr, head=(1000, 430), sc=10.0, cx=640.0, cy=360.0, Z=1.3, blur=3, **kw):
    kw.setdefault('ride', False); kw.setdefault('pose', 'stand')
    return cu(world, light, GC.grim, t, head, sc, cx, cy, Z, blur, **gk(t, expr, **kw))


def harold_cu(world, light, t, expr, head=(900, 470), sc=11.0, cx=640.0, cy=360.0, Z=1.3, blur=3, **kw):
    return cu(world, light, GC.harold, t, head, sc, cx, cy, Z, blur, **hk(t, expr, **kw))


def edgar_cu(world, light, t, expr='deadpan', at=(1000, 1030), sc=21.0, cx=640.0, cy=300.0, Z=1.5, blur=7, cam=True, **kw):
    v = view_at(world, cx, cy, Z, SX, SY)
    big = K.dof(v.bg(), blur)
    sp = GX.draw(GC.edgar, sc, t=t, expr=expr, mouth_=mouth('edgar', t, 2.0), cam=cam, look=(0.0, 0.0), **kw)
    blit(big, sp, at[0], at[1], sc, light(v))
    fx.vignette(big, 0.3)
    return big


def other_cu(world, light, fn, who, t, head, sc, expr, cx=640.0, cy=360.0, Z=1.3, blur=3, **kw):
    kw.setdefault('mouth_', mouth(who, t))
    return cu(world, light, fn, t, head, sc, cx, cy, Z, blur, t=t, expr=expr, **kw)


# ======================================================================================= 2D inserts (drawn in output px)
def pf(sz): return O.pfont(sz)


def plate(big, text, x, y, size=30, fg=(255, 236, 160), bg=(16, 10, 26), anchor='lt', ol=INK, pad=14):
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    f = pf(size); bb = d.textbbox((0, 0), text, font=f); w, h = bb[2] - bb[0], bb[3] - bb[1]
    if anchor == 'mm': x, y = x - w // 2 - pad, y - h // 2 - pad
    elif anchor == 'rt': x = x - w - 2 * pad
    d.rectangle([x - 4, y - 4, x + w + 2 * pad + 4, y + h + 2 * pad + 4], fill=ol)
    d.rectangle([x, y, x + w + 2 * pad, y + h + 2 * pad], fill=bg)
    d.text((x + pad - bb[0], y + pad - bb[1]), text, font=f, fill=fg)
    big[:] = np.array(im)


def big_clock(big, txt, sub=None, col=RED, cy=500, size=200, k=1.0, w=980):
    """a big digital clock box centred on the frame (pixel font), optional caption lines under it"""
    img = Image.new('RGBA', (OUT_W, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    x0, x1 = OUT_W // 2 - w // 2, OUT_W // 2 + w // 2
    d.rounded_rectangle([x0, 40, x1, 340], 40, fill=(10, 6, 18, 235), outline=col + (255,), width=10)
    d.text((OUT_W // 2, 190), txt, font=pf(size), fill=col + (255,), anchor='mm')
    for i, ln in enumerate((sub or '').split('\n')):
        if ln: d.text((OUT_W // 2, 410 + i * 60), ln, font=pf(46), fill=(255, 255, 255, 255), anchor='mm', stroke_width=6,
                      stroke_fill=(10, 6, 18, 255))
    O.overlay(big, np.array(img), 0, cy - 190, k)


def phone_screen(t, mode, u, **kw):
    """the season's DoomDash app (drawn for a 1080x1920 portrait canvas) -> a 607x1080 image for the 16:9 frame"""
    W0, H0 = K.OUT_W, K.OUT_H
    K.OUT_W, K.OUT_H = 1080, 1920
    try:
        can = np.zeros((1920, 1080, 3), np.uint8)
        K.phone_app(can, t, mode, u, **kw)
    finally:
        K.OUT_W, K.OUT_H = W0, H0
    return np.array(Image.fromarray(can).resize((607, 1080), Image.LANCZOS))


def phone_on(big, ph, x0=1240, k=1.0, tilt=0.0):
    h, w = ph.shape[:2]
    y0 = int((1 - k) * 160)
    if k < 1.0: ph = np.array(Image.fromarray(ph).resize((int(w * k), int(h * k)), Image.LANCZOS)); h, w = ph.shape[:2]
    x1 = min(OUT_W, x0 + w)
    big[y0:y0 + h, x0:x1] = ph[:, :x1 - x0]


def phone_center(t, mode, u, world=STREET, light=None, cx=640, cy=360, gexpr='squint', **kw):
    """Death (left, lit by the screen) reading the DoomDash app (right)"""
    light = light or {id(STREET): LS, id(PORCH): LP, id(HILL): LH}.get(id(world), LS)
    big = grim_cu(world, light, t, gexpr, head=(560, 470), sc=10.0, cx=cx, cy=cy, pose='phone', look=(0.8, -0.3), blur=8)
    K.glow_ring(big, 760, 600, 420, (120, 255, 200), 0.18)
    ph = phone_screen(t, mode, u, **kw)
    phone_on(big, ph, 1180)
    return big


def my_phone(big, lines, x0=1180, y0=70, w=600, h=940, t=0.0):
    """a 16:9-native DoomDash phone (custom screens): lines = [(text, size, colour), ...]"""
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 46, fill=(10, 8, 14), outline=(70, 60, 90), width=8)
    sx0, sy0, sx1, sy1 = x0 + 26, y0 + 50, x0 + w - 26, y0 + h - 50
    d.rectangle([sx0, sy0, sx1, sy1], fill=(36, 18, 54))
    d.rectangle([sx0, sy0, sx1, sy0 + 90], fill=(150, 60, 220))
    d.text((sx0 + 24, sy0 + 28), 'DOOMDASH', font=pf(34), fill=(255, 255, 255))
    y = sy0 + 140
    for text, sz, col in lines:
        if text: d.text((sx0 + 24, y), text, font=pf(sz), fill=col)
        y += int(sz * 1.9)
    big[:] = np.array(im)


def stipple_bg(t, col=(26, 14, 40), seed=0):
    r = np.random.default_rng(seed + int(t * 8) % 4)
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = col
    m = r.random((OUT_H // 6, OUT_W // 6)) > 0.93
    m = np.kron(m, np.ones((6, 6), bool))
    big[m] = (np.array(col) * 1.8).clip(0, 255).astype(np.uint8)
    return big


_TITLES = {}


def title_img(lines, size):
    key = (tuple(lines), size)
    if key not in _TITLES: _TITLES[key] = K.hook_title(list(lines), size, width=OUT_W)
    return _TITLES[key]


# ======================================================================================= HUD: loop counter + the clock
def loop_spans():
    """per loop number: (t0, t1) of its shots (rewind cards excluded) -> the in-story clock 1:00 .. 1:59"""
    sp = {}
    for s in TL.SHOTS:
        if s['name'] in ('rewind', 'cold_flip', 'title') or s['name'].startswith('card_'): continue
        a, b = sp.get(s['loop'], (s['t0'], s['t1']))
        sp[s['loop']] = (min(a, s['t0']), max(b, s['t1']))
    return sp


SPANS = loop_spans()
CLOCK_RANGE = {2: (0.0, 6.0), 96: (31.0, 47.0), 97: (49.0, 59.6)}
NOHUD = {'title', 'cold_flip', 'rewind', 'credits', 'post_card', 'post_flip', 's2_card', 'end_clock', 'end_app', 'twist_reveal',
         'm_counter', 'low_clues', 'plan_sign', 'deal_shake', 'b_human', 'b_eternity', 'race_app', 'end_town', 'end_porch',
         'end_sametime', 'end_bike', 'end_nevermore', 'end_stars', 'post_grim', 'post_harold'}


def story_clock(t, s):
    if s['name'] in ('cold_ride', 'cold_harold'):
        sec = 57 + int((t - TL.SHOTS[0]['t0']) / 1.6)
        return f'1:59:{min(59, sec):02d}'
    a, b = SPANS.get(s['loop'], (s['t0'], s['t1']))
    m0, m1 = CLOCK_RANGE.get(s['loop'], (0.0, 59.0))
    m = m0 + (m1 - m0) * (t - a) / max(0.1, b - a)
    mm = int(m); ss = int((m - mm) * 60)
    return f'1:{min(59, mm):02d}' if s['loop'] != 97 else f'1:{min(59, mm):02d}:{ss:02d}'


def hud(big, t, s):
    if s['name'] in NOHUD or s['name'].startswith('card_') or s['loop'] < 2: return
    c = (255, 120, 90) if s['loop'] >= 90 else GREEN
    plate(big, f'LOOP {s["loop"]}', 40, 36, 30, fg=c)
    plate(big, story_clock(t, s) + ' AM', OUT_W - 40, 36, 30, fg=(255, 236, 160), anchor='rt')


# ======================================================================================= shared sequences
REWIND_SUBS = {3: 'DAYLIGHT SAVING\nTIME HAS ENDED. AGAIN.', 9: 'STILL ENDED.', 17: 'IT KEEPS\nENDING.', 24: 'ENDED.\n(AGAIN.)',
               31: 'PLEASE STOP\nENDING.', 40: 'NOPE.', 45: 'SEE YOU AT 1:00'}


def rewind(t, s, u, sub=None):
    """1:59:59 -> 2:00 -> VHS rewind -> 1:00 (a different line under the clock each loop)"""
    v = view_at(STREET, 640, 360, 1.0, SX, SY)
    big = (K.dof(v.bg(), 6) * 0.5).astype(np.uint8)
    D = s['t1'] - s['t0']
    k1, k2 = 0.28 * D, 0.62 * D
    if u < k1:
        big_clock(big, '1:59:59', None, RED, 470, 170)
    elif u < k2:
        big_clock(big, '2:00:00', None, (255, 60, 50), 470, 170)
        O.mosaic(big, int(lerp(2, 40, (u - k1) / (k2 - k1))))
        K.speed_streaks(big, t, 1.0, dirn=1)
        fx.vhs(big, t, 1.0)
    else:
        sub = sub if sub is not None else REWIND_SUBS.get(s['loop'], 'AGAIN.')
        big_clock(big, '1:00:00', sub, GREEN, 470, 170)
        if u - k2 < 0.25: fx.vhs(big, t, 1.0 - (u - k2) / 0.25)
    if k1 - 0.05 < u < k1 + 0.15: B.shake(big, t, 10, 34)
    return big


CARDS = dict(card_a=('PLAN A:', 'SPEED'), card_b=('PLAN B:', 'THE APP'), card_c=('PLAN C:', 'CANDY'), card_d=('PLAN D:', 'THE PLUG'),
             card_e=('PLAN E:', 'DISGUISE'), card_f=('PLAN F:', 'ASK NICELY'), card_g=('PLAN G:', 'HIRE THE GANG'),
             card_hz=('PLANS', 'H TO Z'))


def card(t, s, u):
    big = stipple_bg(t, seed=s['i'])
    k = min(1.0, u / 0.18)
    a, b = CARDS[s['name']]
    plate(big, f'LOOP {s["loop"]}', OUT_W // 2, 260, 44, fg=GREEN, anchor='mm')
    O.overlay(big, title_img((a, b), 104), 0, 360 + int((1 - k) * 60), k)
    sp = GX.draw(GC.grim, 6.0, t=t, expr='menace' if s['name'] != 'card_hz' else 'whine', ride=True, spin=t * 20, wind=0.6, hires=True)
    blit(big, sp, 1560 + 30 * math.sin(t * 3), 1000, 6.0)
    sp = GX.draw(GP.grandfather_clock, 5.0, t=t, hh=1, mm=(u * 80) % 60, hires=True)
    blit(big, sp, 300, 1020, 5.0)
    return big


# ======================================================================================= 1. cold open
def cold_ride(t, s, u):
    cx = lerp(470, 760, u / (s['t1'] - s['t0']))
    rot = 22.0 * sm(min(1.0, u / 0.4)) + 3 * math.sin(t * 6)
    def f(big, v, acts):
        K.speed_streaks(big, t, 0.9); K.leaves(big, t, 30, seed=1, speed=1.8)
        K.lightning(big, t, 0.05, seed=5)
    return wide(STREET, LS, cx, 470, 1.6, [(GC.grim, 960, 1010, 5.6, dict(**gk(t, 'angry', pose='shout', wind=1.0, spin=t * 34, batt=13,
                                                                                   raven=True), rot=rot, pivot=(-24.0, 0.5)))],
                t, fx_=f)


def cold_harold(t, s, u):
    cx, cy, Z = 380, 330, 1.7
    return wide(PORCH, LP, cx, cy, Z, [(GP.grandfather_clock, *W(170, PFLOOR, cx, cy, Z), PS['clock'] * Z, dict(t=t, hh=1, mm=59.9)),
                                      (GC.harold, *W(520, PFLOOR, cx, cy, Z), PS['harold'] * Z, hk(t, 'smug', pose='rock', rock=math.sin(t * 2.4), mug=True,
                                                                                         look=(-1.0, 0.3), flip=True))], t)


def cold_app(t, s, u):
    big = wide(STREET, LS, 640, 470, 1.6, [(GC.grim, 560, 1010, 5.0, gk(t, 'stunned', ride=True, spin=0.0, raven=True, look=(0.8, -0.2)))],
               t, fx_=lambda b, v, a: K.fog(b, t, 820, OUT_H, 0.25))
    k = min(1.0, u / 0.2)
    my_phone(big, [('FINAL PICKUP', 34, GOLD), ('HAROLD, 97', 40, (255, 255, 255)), ('', 20, None), ('DEADLINE:', 30, (200, 170, 255)),
                   ('2:00 AM', 70, RED), ('', 20, None), ('LATE = DEACTIVATED', 22, RED), ('', 20, None),
                   ('HAVE A SPOOKY', 24, GREEN), ('NIGHT!', 24, GREEN)], x0=int(lerp(1950, 1220, sm(k))), y0=70, t=t)
    return big


def grim_again_cu(t, s, u):
    return grim_cu(STREET, LS, t, 'stunned', head=(980, 460), sc=10.5, cx=500, cy=420, look=(0.0, -0.2), jaw_drop=0.3)


def edgar_lamp(t, s, u):
    return edgar_cu(STREET, LS, t, 'deadpan', cx=570, cy=300)


def grim_shriek(t, s, u):
    big = grim_cu(STREET, LS, t, 'panic', head=(960, 440), sc=11.5, cx=760, cy=420, shake=1.0, jaw_drop=1.0, pose='claw')
    if u < 1.0: B.shake(big, t, 10, 34)
    return big


def edgar_lamp2(t, s, u):
    return edgar_cu(STREET, LS, t, 'bored', cx=900, cy=300, at=(1320, 1180), sc=25.0)


def title(t, s, u):
    v = view_at(HILL, 760, 300, 1.25, SX, SY)
    big = v.bg().copy()
    big = (big * 0.75).astype(np.uint8)
    k = min(1.0, u / 0.3)
    O.overlay(big, title_img(('GRIM RIDE',), 150), 0, 230 + int((1 - k) * 80), k)
    O.overlay(big, title_img(('ONE MORE HOUR',), 74), 0, 470, min(1.0, max(0.0, (u - 0.6) / 0.3)))
    sp = GX.draw(GP.grandfather_clock, 7.0, t=t, hh=1 - u * 0.3, mm=(60 - u * 140) % 60, hires=True)
    blit(big, sp, 1600, 1060, 7.0, None)
    K.lightning(big, t, s['t0'] + 0.02, seed=9)
    return big


# ======================================================================================= 2. the rules
def hill_plan(t, s, u):
    pace = math.sin(u * 2.2)
    return wide(HILL, LH, 640, 470, 1.25, [(GC.ebike, 560, 1000, 4.2, dict(t=t, spin=0.0, batt=13)),
                                            (GC.edgar, 470, 900, 4.2, dict(t=t, expr='bored', mouth_=mouth('edgar', t, 2.0), perch=False)),
                                            (GC.grim, 1020 + 60 * pace, 1010, 4.6, gk(t, 'menace', ride=False, pose='point', flip=pace < 0,
                                                                                     look=(0.6, 0.0)))], t)


PLAN = ['PLAN A: SPEED', 'PLAN B: THE APP', 'PLAN C: CANDY', 'PLAN D: THE PLUG', 'PLAN E: DISGUISE', 'PLAN F: ASK NICELY',
        'PLAN G: HIRE THE GANG', 'PLANS H-Z: ???']


def plan_sign(t, s, u):
    v = view_at(HILL, 640, 520, 1.4, SX, SY)
    big = K.dof(v.bg(), 8)
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([380, 90, 1540, 1020], fill=INK); d.rectangle([392, 102, 1528, 1008], fill=(250, 120, 30))
    d.rectangle([420, 130, 1500, 980], fill=(246, 236, 214))
    d.text((960, 190), "DEATH'S PLAN", font=pf(54), fill=(120, 20, 30), anchor='mm')
    n = int(min(len(PLAN), 1 + u / (s['t1'] - s['t0'] - 0.3) * len(PLAN)))
    for i, ln in enumerate(PLAN[:n]):
        d.text((480, 280 + i * 84), ln, font=pf(40), fill=(40, 24, 50) if 'H-Z' not in ln else (180, 20, 30))
    big[:] = np.array(im)
    i = n - 1
    sp = GX.draw(GC.bony_hand, 30.0, x=0.0, y=0.0, d=-1.0, grip=True, hires=True)
    hx = int(480 + len(PLAN[i]) * 40 + 30 + 8 * math.sin(t * 30)); hy = 330 + i * 84
    big[hy - 80:hy + 6, hx - 4:hx + 6] = (230, 190, 60)
    blit(big, sp, hx + 60, hy + 260, 30.0)
    return big


def hill_grand(t, s, u):
    def f(big, v, acts):
        K.lightning(big, t, s['t0'] + 0.3, seed=11)
        g = acts[0]
        x, y = K.aout(g, v, 'eyes'); K.glow_ring(big, x, y, 220, GC.GLOW, 0.3)
    return wide(HILL, LH, 1040, 300, 1.45, [(GC.grim, 900, 1240, 9.5, gk(t, 'proud', ride=False, pose='loom', wind=0.7, look=(0.4, 0.4)))],
                t, fx_=f)


def edgar_herewego(t, s, u):
    return edgar_cu(HILL, LH, t, 'bored', cx=1000, cy=280)


# ======================================================================================= 3. loop 3 — speed (E01)
HOUSE = (1180, 1000)                       # Harold's porch steps in the street view (output px at the wide framing)


def a_approach(t, s, u):
    gx = lerp(-200, 760, sm(u / (s['t1'] - s['t0'])))
    return wide(STREET, LS, 760, 470, 1.25, [(GC.tarp, 1360, 1000, 4.0, dict(t=t)),
                                             (GC.harold, 1560, 1000, 5.0, hk(t, 'smug', pose='stand', look=(-1.0, 0.0))),
                                             (GC.grim, gx, 1040, 4.4, gk(t, 'menace', ride=True, spin=t * 30, wind=0.6, raven=True))], t)


def a_tarp(t, s, u):
    lift = min(1.0, u / 0.7)
    return wide(STREET, LS, 860, 470, 1.6, [(GC.harold, 1080, 1020, 5.2, hk(t, 'grin', pose='ride', spin=0.0, look=(-1.0, 0.0), flag=1.4)),
                                             (GC.tarp, 1080, 1020, 5.2, dict(t=t, lift=lift))], t)


def a_catch(t, s, u):
    D = s['t1'] - s['t0']
    if u < D - 0.5:
        return harold_cu(STREET, LS, t, 'grin', head=(860, 470), sc=10.0, cx=900, cy=420, pose='ride', look=(-0.8, 0.0), flag=1.4,
                         spin=-t * 10)
    x = lerp(860, -800, (u - (D - 0.5)) / 0.5)
    big = harold_cu(STREET, LS, t, 'grin', head=(x, 470), sc=10.0, cx=900, cy=420, pose='ride', look=(-1.0, 0.0), spin=-t * 40)
    K.speed_streaks(big, t, 1.0)
    return big


def a_chase(t, s, u):
    D = s['t1'] - s['t0']
    k = u / D
    hx = lerp(2100, -300, k); gx = lerp(2600, 200, k)
    big = wide(STREET, LS, 640, 520, 1.5,
               [(GC.harold, hx, 1040, 4.6, dict(**hk(t, 'grin', pose='ride', spin=-t * 50, look=(1.0, 0.0), flag=1.4, wind=1.0), flip=True)),
                (GC.grim, gx, 1050, 4.6, dict(**gk(t, 'panic', ride=True, spin=-t * 50, wind=1.0, raven=True), flip=True))], t)
    K.speed_streaks(big, t, 1.0, dirn=1)
    return big


def a_slowdown(t, s, u):
    big = cu(STREET, LS, GC.grim, t, (900, 400), 9.0, 640 + 200 * math.sin(t), 400, 1.3, 4,
             **gk(t, 'panic', ride=True, spin=t * 40, wind=1.0, raven=True))
    K.speed_streaks(big, t, 0.9); B.shake(big, t, 4, 30)
    return big


def a_battery(t, s, u):
    v = view_at(STREET, 640, 520, 1.6, SX, SY)
    big = K.dof(v.bg(), 9)
    W0 = K.OUT_W; K.OUT_W = 1300
    try:
        sub = np.zeros((OUT_H, 1300, 3), np.uint8); sub[:] = big[:, 310:1610]
        K.display_insert(sub, t, 0, dead=False, y0=60, y1=1020, label='PALE HORSE 2', banner='BATTERY DEAD')
        big[:, 310:1610] = sub
    finally:
        K.OUT_W = W0
    sp = GX.draw(GC.edgar, 9.0, t=t, expr='deadpan', mouth_=mouth('edgar', t, 2.0), cam=True, hires=True)
    blit(big, sp, 1700, 1060, 9.0)
    return big


# ======================================================================================= 4. loop 9 — the app (E02)
CHAT1 = [('bot', "Oopsie! Let's try again. Are you a HUMAN?", 0.0)]


def b_captcha(t, s, u):
    big = grim_cu(STREET, LS, t, 'squint', head=(520, 470), sc=10.0, cx=500, cy=420, pose='phone', look=(0.6, -0.5))
    phone_on(big, phone_screen(t, 'captcha', min(1.0, u / 2.0), taps=[(0, 0.25), (4, 0.5), (2, 0.75)]), 1200)
    return big


def b_human(t, s, u):
    return phone_center(t, 'chat', u, msgs=CHAT1, gexpr='squint')


def b_death(t, s, u):
    big = grim_cu(STREET, LS, t, 'angry', head=(960, 430), sc=11.5, cx=640, cy=380, pose='claw', shake=1.0 if u < 0.6 else 0.0)
    K.lightning(big, t, s['t0'] + 0.05, seed=7)
    if u < 0.5: B.shake(big, t, 10, 34)
    return big


def b_eternity(t, s, u):
    return phone_center(t, 'wait', u + 1.0, gexpr='sad')


def b_myline(t, s, u):
    return grim_cu(STREET, LS, t, 'sad', head=(900, 450), sc=10.5 + 0.6 * u, cx=640, cy=400, pose='phone', look=(0.0, -0.6))


# ======================================================================================= 5. loop 17 — candy (E03)
def kids_line(t, xs, y, s_, costumes=('pumpkin', 'dino', 'witch', 'robot', 'vampire', 'ghost')):
    return [(GC.trick_or_treater, x, y, s_, dict(t=t, costume=costumes[i % len(costumes)], n=i, look=(-0.6, 0.0)))
            for i, x in enumerate(xs)]


def c_line(t, s, u):
    cx, cy, Z = 560, 470, 1.3
    specs = [(GC.trick_or_treater, *W(wx, wy, cx, cy, Z), PS['kid'] * Z, dict(t=t, costume=c, n=i, look=(-0.6, 0.3)))
             for i, (wx, wy, c) in enumerate([(380, 500, 'pumpkin'), (470, 545, 'dino'), (560, 590, 'witch'), (650, 635, 'robot'),
                                              (760, 670, 'vampire')])]
    specs.append((GC.grim, *W(930, 690, cx, cy, Z), PS['grim'] * Z, gk(t, 'sly', ride=False, pose='stand', carry=0.3, look=(-0.8, 0.0), flip=True)))
    return wide(PORCH, LP, cx, cy, Z, specs, t)


def c_mom(t, s, u):
    return other_cu(PORCH, LP, GC.mom, 'mom', t, (980, 440), 10.0, 'squint', cx=600, cy=440, point=min(1.0, u / 0.4), look=(0.8, 0.0))


def c_four(t, s, u):
    big = grim_cu(PORCH, LP, t, 'angry', head=(900, 430), sc=10.5, cx=800, cy=420, pose='claw', carry=0.3, flip=True)
    if u < 0.4: B.shake(big, t, 8, 30)
    return big


def c_no(t, s, u):
    return other_cu(PORCH, LP, GC.mom, 'mom', t, (980, 440), 10.5, 'deadpan', cx=600, cy=440, look=(0.8, 0.0))


def c_carded(t, s, u):
    big = edgar_cu(PORCH, LP, t, 'deadpan', cx=300, cy=300)
    plate(big, 'ID REQUIRED: 4000+', 660, 120, 34, fg=RED)
    return big


# ======================================================================================= 6. loop 24 — the plug (E04)
def gang_specs(t, xs=(1180, 1480, 1760), y=1000, s_=5.0):
    return [(GC.kayden, x, y, s_, dict(t=t, expr='bored', mouth_=mouth('kayden', t) if i == 0 else 0.0, n=i, bike=True,
                                       look=(-1.0, 0.0), flip=True)) for i, x in enumerate(xs)]


def headlights(big, t, pts):
    for x, y in pts: K.glow_ring(big, x, y, 260, (240, 240, 200), 0.35)


def d_plug(t, s, u):
    return wide(GANG, LG, 640, 470, 1.3, gang_specs(t) + [(GC.grim, 560, 1000, 5.4, gk(t, 'nervous', ride=False, pose='stand'))], t,
                fx_=lambda b, v, a: headlights(b, t, [(1120, 820), (1420, 820), (1700, 820)]))


def d_forty(t, s, u):
    v = view_at(GANG, 900, 300, 1.5, SX, SY)
    big = K.dof(v.bg(), 7)
    sp = GX.draw(GC.edgar, 13.0, t=t, expr='sly', mouth_=mouth('edgar', t, 2.0), cam=True, look=(0.0, 0.0), stash=True, hires=True)
    blit(big, sp, 960, 1060, 13.0, LG(v))
    plate(big, '$40 CASH', 1320, 130, 40, fg=GREEN)
    fx.vignette(big, 0.3)
    return big


def d_rocket(t, s, u):
    D = s['t1'] - s['t0']
    gx = lerp(-300, 2300, u / D)
    big = wide(STREET, LS, 640, 520, 1.45, [(GC.grim, gx, 1030, 4.8, dict(**gk(t, 'hype', ride=True, spin=t * 80, wind=1.0, raven=True, batt=99),
                                                                         rot=24, pivot=(-24.0, 0.5)))], t)
    K.speed_streaks(big, t, 1.4); B.shake(big, t, 5, 40)
    plate(big, '40 MPH', 960, 160, 60, fg=GOLD, anchor='mm')
    return big


def d_crash(t, s, u):
    rot = -u * 520
    big = wide(YARD, LY, 520, 420, 1.35, [(GC.kevin, 900, 1040, 4.2, dict(t=t, turn=min(1.0, u / 0.8), look=(-0.5, 0.6))),
                                          (GC.grim, 760 + 80 * u, 960 - 200 * math.sin(min(math.pi, u * 4)), 4.0,
                                           dict(**gk(t, 'panic', ride=True, spin=t * 60), rot=rot, pivot=(0.0, 30.0)))], t)
    if u < 0.5: B.shake(big, t, 14, 40)
    if u < 0.12: O.flash(big, 0.6)
    return big


def d_norefunds(t, s, u):
    return edgar_cu(GANG, LG, t, 'smug', cx=950, cy=260, stash=True)


# ======================================================================================= 7. loop 31 — disguise (E05)
LAWN = (420, 470, 2.0)


def e_dontmove(t, s, u):
    poke = 0.5 + 0.5 * math.sin(t * 9)
    def f(big, v, acts):
        x0, y0 = 700, 860
        big[y0 - 5:y0 + 5, int(x0 + 60 * poke):int(x0 + 300 + 60 * poke)] = (120, 90, 60)
    return wide(STREET, LS, *LAWN, [(GC.tombstone, 520, 1000, 5.0, dict(text='RIP')), (GC.tombstone, 1500, 1010, 5.0, dict(text='BOO')),
                                    (GC.trick_or_treater, 640, 1050, 7.5, dict(t=t, costume='ghost', look=(1.0, 0.0))),
                                    (GC.grim, 1060, 1030, 5.2, gk(t, 'nervous', ride=False, pose='stand', look=(-0.6, 0.0), blink=False))],
                t, fx_=f)


def e_fog(t, s, u):
    return other_cu(STREET, LS, GC.todd, 'todd', t, (860, 470), 9.5, 'smug', cx=420, cy=470, Z=1.6, clip='7/10', look=(1.0, 0.0),
                    back=[(GC.grim, 1500, 1060, 5.0, dict(t=t, expr='nervous', ride=False, pose='stand', blink=False))])


def e_time(t, s, u):
    lift = min(1.0, u / 1.0)
    return wide(STREET, LS, *LAWN, [(GC.harold, 760, 1040, 6.0, hk(t, 'content', pose='stand', look=(-1.0, -0.3), flip=True)),
                                    (GC.grim, 1060, 1030, 5.2, gk(t, 'menace', ride=False, pose='loom' if lift > 0.4 else 'stand',
                                                                  look=(-0.8, 0.3), flip=True))],
                t, fx_=lambda b, v, a: K.glow_ring(b, *K.aout(a[1], v, 'eyes'), 160, GC.GLOW, 0.3 * lift))


def e_animatronic(t, s, u):
    specs = [(GC.todd, 470, 1060, 6.4, dict(t=t, expr='awe', mouth_=mouth('todd', t), phone=True, look=(1.0, 0.0)))]
    specs += [(GC.mom, 190, 1060, 6.0, dict(t=t, expr='shock', look=(1.0, 0.0)))]
    specs += [(GC.grim, 1280, 1040, 5.4, gk(t, 'stunned', ride=False, pose='loom', blink=False, flip=True)),
              (GC.harold, 930, 1050, 6.0, hk(t, 'content', pose='stand', look=(-1.0, -0.3), flip=True))]
    big = wide(STREET, LS, 460, 470, 1.7, specs, t)
    if any(0 <= u - f < 0.08 for f in (0.3, 0.9, 1.3)): O.flash(big, 0.5)
    return big


# ======================================================================================= 8. loop 40 — ask nicely
def f_ask(t, s, u):
    cx, cy, Z = 520, 420, 1.45
    return wide(PORCH, LP, cx, cy, Z, [(GC.harold, *W(470, PFLOOR, cx, cy, Z), PS['harold'] * Z, hk(t, 'bored', pose='rock', rock=math.sin(t * 2), look=(1.0, 0.0))),
                                      (GC.grim, *W(800, 660, cx, cy, Z), PS['grim'] * Z, gk(t, 'content', ride=False, pose='stand', look=(-1.0, 0.0), flip=True))], t)


def f_body(t, s, u):
    return harold_cu(PORCH, LP, t, 'smug', head=(820, 500), sc=11.0, cx=380, cy=420, pose='rock', rock=math.sin(t * 2), look=(1.0, 0.0))


def f_plan(t, s, u):
    return grim_cu(PORCH, LP, t, 'smug', head=(1000, 430), sc=10.5, cx=640, cy=420, flip=True, look=(0.8, 0.0))


def f_slam(t, s, u):
    cx, cy, Z = 520, 420, 1.45
    big = wide(PORCH, LP, cx, cy, Z, [(GC.rocking_chair, *W(470, PFLOOR, cx, cy, Z), PS['chair'] * Z, dict(rock=math.sin(t * 5) * (1 - u))),
                                      (GC.grim, *W(800, 660, cx, cy, Z), PS['grim'] * Z, gk(t, 'shock', ride=False, pose='stand', flip=True))], t)
    if u < 0.35: B.shake(big, t, 12, 38)
    if u < 0.1: O.flash(big, 0.4)
    plate(big, 'SLAM!', 520, 160, 70, fg=RED)
    return big


# ======================================================================================= 9. loop 45 — hire the gang
def g_cop(t, s, u):
    return other_cu(GANG, LG, GC.kayden, 'kayden', t, (900, 470), 9.5, 'bored', cx=900, cy=440, bike=True, look=(-1.0, 0.0), flip=True)


def g_costume(t, s, u):
    big = grim_cu(GANG, LG, t, 'angry', head=(980, 430), sc=10.5, cx=500, cy=420, pose='claw')
    if u < 0.4: B.shake(big, t, 8, 30)
    return big


def g_customer(t, s, u):
    return other_cu(GANG, LG, GC.kayden, 'kayden', t, (1000, 470), 9.0, 'glare', cx=900, cy=440, bike=True, look=(-1.0, 0.2), flip=True,
                    back=[(GC.kayden, 1500, 1060, 4.0, dict(t=t, n=1, bike=True, flip=True)), (GC.kayden, 300, 1060, 4.0, dict(t=t, n=2, bike=True))])


# ======================================================================================= 10. montage, plans H-Z
def pizza_at(big, v, g, sc, dy=0):
    hx, hy = K.aout(g, v, 'hand')
    sp = GX.draw(GP.pizza_box, sc, hires=True)
    blit(big, sp, hx - 20, hy + 10 + dy, sc)


def m_pizza(t, s, u):
    cx, cy, Z = 380, 380, 1.6
    gx, gy = W(470, PFLOOR, cx, cy, Z)
    return wide(PORCH, LP, cx, cy, Z, [(GC.grim, gx, gy, PS['grim'] * Z, gk(t, 'hype', ride=False, pose='stand', look=(-1.0, 0.0), flip=True))],
                t, fx_=lambda b, v, a: pizza_at(b, v, a[0], PS['grim'] * Z))


def m_pizza_door(t, s, u):
    cx, cy, Z = 380, 380, 1.6
    gx, gy = W(470, PFLOOR, cx, cy, Z)
    big = wide(PORCH, LP, cx, cy, Z, [(GC.grim, gx, gy, PS['grim'] * Z, gk(t, 'sad', ride=False, pose='stand', look=(-1.0, 0.0), flip=True))],
               t, fx_=lambda b, v, a: pizza_at(b, v, a[0], PS['grim'] * Z, dy=40))
    plate(big, '(through the door)', 160, 150, 26, fg=(200, 190, 220))
    return big


def m_ghost(t, s, u):
    cx, cy, Z = 520, 470, 1.4
    specs = [(GC.trick_or_treater, *W(560, 600, cx, cy, Z), PS['kid'] * Z, dict(t=t, costume='pumpkin', look=(-0.6, 0.3))),
             (GC.trick_or_treater, *W(720, 640, cx, cy, Z), PS['kid'] * Z, dict(t=t, costume='witch', n=2, look=(-0.6, 0.3))),
             (GC.trick_or_treater, *W(420, 560, cx, cy, Z), PS['kid'] * Z * 1.5, dict(t=t, costume='ghost', look=(-0.6, 0.2))),
             (GC.harold, *W(250, PFLOOR, cx, cy, Z), PS['harold'] * Z, hk(t, 'bored', pose='stand', toss=min(1.0, u / 0.4), look=(1.0, -0.2)))]
    def f(big, v, acts):
        x, y = W(420, 560, cx, cy, Z); x = int(x) + 20; y = int(y) - 470          # the scythe blade pokes out of the sheet
        big[y:y + 150, x:x + 9] = (200, 200, 210)
        big[y - 18:y, x - 70:x + 9] = (220, 220, 230)
        if u > 0.45:                                                              # the raisin box flies into the pail
            k = min(1.0, (u - 0.45) / 0.3)
            x, y = int(1100 - 300 * k), int(700 + 120 * k)
            big[y:y + 30, x:x + 22] = (120, 40, 140)
    return wide(PORCH, LP, cx, cy, Z, specs, t, fx_=f)


def m_loop50(t, s, u):
    return edgar_cu(STREET, LS, t, 'sleepy', cx=570, cy=300)


def m_moon(t, s, u):
    v = view_at(STREET, 500, 110, 3.0, SX, SY)
    big = v.bg().copy()
    D = s['t1'] - s['t0']; k = u / D
    sp = GX.draw(GC.grim, 6.0, t=t, ride=True, spin=t * 40, wind=1.0, hires=True)
    tmp = np.zeros_like(big); tmp[:] = (255, 0, 255)
    blit(tmp, sp, int(lerp(-200, 2100, k)), int(700 - 260 * math.sin(k * math.pi)), 6.0)
    m = np.any(tmp != (255, 0, 255), axis=2)
    big[m] = (14, 8, 22)
    plate(big, 'PLAN K: FLY', 60, 940, 34, fg=GOLD)
    return big


def m_kevin(t, s, u):
    big = wide(YARD, LY, 560, 360, 1.25, [(GC.kevin, 820, 1040, 4.6, dict(t=t, turn=min(1.0, u / 0.9), look=(0.6, 0.8))),
                                          (GC.grim, 1120, 1040, 4.2, gk(t, 'whine', ride=False, pose='point', look=(-0.6, 0.8), flip=True))], t)
    if u > 0.7: O.draw_sticker(big, STK['short'], t, s['t0'] + 0.7, s['t1'], 1300, 260)
    return big


def m_loop73(t, s, u):
    return edgar_cu(STREET, LS, t, 'sleepy', cx=900, cy=300, at=(700, 1200), sc=26.0)


FLICK = ['a_tarp', 'b_death', 'c_four', 'd_crash', 'e_animatronic', 'f_slam', 'g_costume', 'm_moon', 'm_ghost', 'a_slowdown']


def m_counter(t, s, u):
    D = s['t1'] - s['t0']
    i = int(u / 0.26) % len(FLICK)
    s2 = TL.first(FLICK[i])
    big = SHOT[FLICK[i]](s2['t0'] + 0.4 + (u % 0.26), s2, 0.4 + (u % 0.26))
    big = (big * 0.55).astype(np.uint8)
    n = int(74 + (95 - 74) * min(1.0, u / (D - 0.3)))
    plate(big, f'LOOP {n}', OUT_W // 2, 540, 110, fg=RED if n > 90 else GREEN, anchor='mm')
    fx.vhs(big, t, 0.6)
    return big


# ======================================================================================= 11. low point, loop 96
def low_wide(t, s, u):
    return wide(HILL, LH, 640, 470, 1.25, [(GC.ebike, 620, 1030, 4.2, dict(t=t, dead=True, batt=0, scythe=False), ),
                                            (GC.edgar, 560, 930, 3.6, dict(t=t, expr='sleepy', perch=False)),
                                            (GC.grim, 1040, 1020, 4.6, gk(t, 'sad', ride=False, pose='stand', look=(-0.3, -0.8), lean=0.4))], t,
                fx_=lambda b, v, a: K.fog(b, t, 820, OUT_H, 0.3))


def low_cu(t, s, u):
    return grim_cu(HILL, LH, t, 'sad', head=(1000, 470), sc=10.0 + 0.8 * u / 4, cx=900, cy=380, look=(-0.2, -0.8))


def low_edgar(t, s, u):
    return edgar_cu(HILL, LH, t, 'sleepy', cx=900, cy=300, at=(1300, 1130))


def low_ready(t, s, u):
    return grim_cu(HILL, LH, t, 'teary', head=(940, 450), sc=10.5, cx=700, cy=380, look=(0.2, -0.4))


def tint(big, col=(170, 140, 255), a=0.35):
    g = big.mean(axis=2, keepdims=True)
    return (g * (1 - a) + np.array(col) * a * g / 255 * 1.4).clip(0, 255).astype(np.uint8)


def low_clues(t, s, u):
    D = s['t1'] - s['t0']; j = min(2, int(u / (D / 3)))
    if j == 0:
        big = harold_cu(PORCH, LP, t, 'smug', head=(860, 500), sc=10.0, cx=380, cy=420, pose='rock', look=(1.0, 0.0))
        lab = 'CLUE #1: HELMET. ALWAYS ON.'
    elif j == 1:
        big = wide(STREET, LS, 860, 470, 1.7, [(GC.harold, 1000, 1020, 5.2, hk(t, 'grin', pose='ride', look=(-1.0, 0.0))),
                                               (GC.tarp, 1000, 1020, 5.2, dict(t=t, lift=0.5))], t)
        lab = 'CLUE #2: TRIKE. ALWAYS READY.'
    else:
        cx, cy, Z = 300, 330, 2.1
        big = wide(PORCH, LP, cx, cy, Z, [(GP.grandfather_clock, *W(170, PFLOOR, cx, cy, Z), PS['clock'] * Z, dict(t=t, hh=1, mm=59.9)),
                                          (GC.harold, *W(380, PFLOOR, cx, cy, Z), PS['harold'] * Z, hk(t, 'sly', pose='stand', look=(-1.0, 0.6), flip=True))], t)
        lab = 'CLUE #3: 1:59. HE CHECKS THE CLOCK.'
    big = tint(big)
    fx.vhs(big, t, 0.35)
    plate(big, lab, 60, 950, 34, fg=GOLD)
    return big


# ======================================================================================= 12. the twist
def h_arrive(t, s, u):
    D = s['t1'] - s['t0']
    hx = lerp(2000, 1240, sm(u / D))
    big = wide(HILL, LH, 640, 470, 1.25, [(GC.ebike, 620, 1030, 4.2, dict(t=t, dead=True, batt=0, scythe=False)),
                                          (GC.grim, 980, 1020, 4.6, gk(t, 'sad', ride=False, pose='stand', look=(1.0, -0.2))),
                                          (GC.harold, hx, 1050, 5.6, dict(**hk(t, 'smile', pose='ride', spin=-t * 20, look=(-1.0, 0.0), mug=True),
                                                                          flip=True))], t)
    K.glow_ring(big, hx - 200, 900, 300, (255, 240, 200), 0.3)
    return big


def two_shot(t, gexpr='sad', hexpr='smile', glook=(1.0, -0.1), hlook=(-1.0, 0.1), gpose='stand', hpose='ride', mug=True, gmug=True):
    return wide(HILL, LH, 900, 450, 1.55, [(GC.grim, 760, 1050, 5.6, gk(t, gexpr, ride=False, pose=gpose, look=glook, mug=gmug)),
                                           (GC.harold, 1260, 1070, 7.0, dict(**hk(t, hexpr, pose=hpose, look=hlook, mug=mug), flip=True))], t)


def h_rough(t, s, u):
    return two_shot(t, gmug=False)


def g_remember(t, s, u):
    return grim_cu(HILL, LH, t, 'stunned', head=(900, 440), sc=11.0, cx=900, cy=380, look=(1.0, 0.0), jaw_drop=0.5)


def h_doing(t, s, u):
    return harold_cu(HILL, LH, t, 'sly', head=(980, 480), sc=11.0 + 1.2 * u / 2.6, cx=1000, cy=360, pose='ride', look=(-0.8, 0.1),
                     mug=True, flip=True)


def clock_face(big, cx, cy, r, hh, mm, label="HAROLD'S CLOCK"):
    im = Image.fromarray(big); d = ImageDraw.Draw(im)
    d.ellipse([cx - r - 36, cy - r - 36, cx + r + 36, cy + r + 36], fill=(112, 50, 30), outline=INK, width=10)
    d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14], fill=(230, 176, 60), outline=INK, width=6)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(236, 230, 210), outline=INK, width=4)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        x, y = cx + math.sin(a) * (r - 40), cy - math.cos(a) * (r - 40)
        d.text((x, y), str(12 if k == 0 else k), font=pf(30), fill=(40, 30, 40), anchor='mm')
    am = mm / 60 * 2 * math.pi; ah = ((hh % 12) + mm / 60) / 12 * 2 * math.pi
    d.line([cx, cy, cx + math.sin(am) * (r - 70), cy - math.cos(am) * (r - 70)], fill=(30, 20, 30), width=16)
    d.line([cx, cy, cx + math.sin(ah) * (r - 130), cy - math.cos(ah) * (r - 130)], fill=(160, 30, 30), width=22)
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(230, 176, 60), outline=INK, width=4)
    d.rectangle([cx - 230, cy + r + 50, cx + 230, cy + r + 104], fill=(230, 176, 60), outline=INK, width=4)
    d.text((cx, cy + r + 77), label, font=pf(24), fill=(90, 30, 20), anchor='mm')
    big[:] = np.array(im)
    return am


def twist_reveal(t, s, u):
    if u < 2.1:
        big = stipple_bg(t, (40, 18, 22), seed=3)
        k = sm(min(1.0, max(0.0, (u - 0.4) / 1.3)))
        mm = (59.9 - 60 * k) % 60; hh = 1 + (1 - k) * 0.99 if k < 1 else 1
        am = clock_face(big, 800, 470, 330, 1 if k > 0.98 else 1 + (1 - k), mm)
        tx, ty = 800 + math.sin(am) * 250, 470 - math.cos(am) * 250                     # Harold's cane hooks the minute hand
        im = Image.fromarray(big); d = ImageDraw.Draw(im)
        d.line([tx, ty, 1700, 1100], fill=(90, 50, 30), width=22); d.line([tx, ty, 1700, 1100], fill=INK, width=4)
        d.arc([tx - 40, ty - 40, tx + 40, ty + 40], 180, 360, fill=(90, 50, 30), width=18)
        big[:] = np.array(im)
        if u < 0.15: O.flash(big, 0.7)
        if 0.4 < u < 1.7: B.shake(big, t, 4, 30)
        return big
    v = view_at(HILL, 640, 470, 1.25, SX, SY)
    big = v.bg().copy()
    r = np.random.default_rng(7)
    n = int(min(18, (u - 2.1) / 1.2 * 18))
    for i in range(n):
        x, y = int(r.integers(380, 1500)), int(r.integers(560, 860))
        plate(big, '1:00', x, y, 22, fg=GREEN)
    return big


def h_byhand(t, s, u):
    return harold_cu(PORCH, LP, t, 'proud', head=(900, 480), sc=10.0, cx=300, cy=380, pose='stand', look=(1.0, 0.0),
                     back=[(GP.grandfather_clock, 380, 1160, 9.0, dict(t=t, hh=1, mm=0.5))])


def g_rewinding(t, s, u):
    big = grim_cu(HILL, LH, t, 'shock', head=(920, 430), sc=11.0, cx=900, cy=380, pose='claw', shake=1.0)
    if u < 0.5: B.shake(big, t, 9, 34)
    return big


def h_recycle(t, s, u):
    return two_shot(t, 'stunned', 'content', gmug=True)


def g_deactivated(t, s, u):
    return grim_cu(HILL, LH, t, 'whine', head=(900, 450), sc=10.5, cx=900, cy=380, pose='phone', look=(1.0, -0.2))


def h_race(t, s, u):
    return harold_cu(HILL, LH, t, 'grin', head=(1000, 470), sc=10.5, cx=1000, cy=360, pose='stand', wave=1.0, look=(-0.8, 0.0), flip=True)


def g_ifyou(t, s, u):
    return grim_cu(HILL, LH, t, 'awe', head=(900, 440), sc=10.5, cx=900, cy=380, look=(1.0, 0.0))


def h_onemore(t, s, u):
    return harold_cu(HILL, LH, t, 'smile', head=(1000, 470), sc=11.0, cx=1000, cy=360, pose='stand', offer=1.0, look=(-0.8, 0.0), flip=True)


def deal_shake(t, s, u):
    pump = 6 * math.sin(t * 14)
    def f(big, v, acts):
        x, y = K.aout(acts[0], v, 'hand'); x2, y2 = K.aout(acts[1], v, 'hand')
        mx, my = (x + x2) / 2, (y + y2) / 2
        r = np.random.default_rng(int(t * 30))
        for _ in range(46):
            a = r.random() * 6.28; d = r.random() * 160
            px, py = int(mx + math.cos(a) * d), int(my + math.sin(a) * d)
            if 0 <= px < OUT_W - 10 and 0 <= py < OUT_H - 10: big[py:py + 10, px:px + 10] = GREEN
        K.glow_ring(big, mx, my, 220, GC.GLOW, 0.4)
    big = wide(HILL, LH, 900, 430, 1.9, [(GC.grim, 760, 1150 + pump, 6.8, gk(t, 'proud', ride=False, pose='point', look=(1.0, 0.0))),
                                         (GC.harold, 1180, 1160 + pump, 8.4, dict(**hk(t, 'grin', pose='stand', offer=1.0, look=(-1.0, 0.0)),
                                                                                  flip=True))], t, fx_=f)
    if u < 0.12: O.flash(big, 0.6)
    plate(big, 'DEAL.', 960, 140, 70, fg=GOLD, anchor='mm')
    return big


def e_contract(t, s, u):
    return edgar_cu(HILL, LH, t, 'deadpan', cx=1000, cy=280, at=(700, 1130))


# ======================================================================================= 13. the race
def race_line(t, s, u):
    specs = kids_line(t, [140, 300], 1050, 5.6, ('witch', 'robot'))
    specs += [(GC.kayden, 1680, 1040, 4.0, dict(t=t, n=0, bike=True, flip=True)), (GC.kayden, 1860, 1050, 4.0, dict(t=t, n=1, bike=True, flip=True)),
              (GC.todd, 500, 1050, 5.2, dict(t=t, expr='hype', phone=True)), (GC.kevin, 1450, 1040, 4.6, dict(t=t, wave=1.0, look=(-0.3, 0.0))),
              (GC.grim, 880, 1050, 4.0, gk(t, 'menace', ride=True, spin=0.0, raven=True)),
              (GC.harold, 1180, 1050, 3.8, hk(t, 'grin', pose='ride', look=(-0.5, 0.0)))]
    def f(big, v, acts):
        K.rope_line(big, (700, 900), (1350, 900), sag=20, col=(250, 250, 250))
        plate(big, 'HILL -> PORCH', 1025, 820, 26, fg=RED, anchor='mm')
    return wide(HILL, LH, 640, 470, 1.25, specs, t, fx_=f)


def race_kayden(t, s, u):
    return other_cu(HILL, LH, GC.kayden, 'kayden', t, (960, 470), 9.5, 'bored', cx=640, cy=360, bike=True, look=(-0.6, 0.0), flip=True)


def race_todd(t, s, u):
    big = other_cu(HILL, LH, GC.todd, 'todd', t, (900, 470), 9.5, 'hype', cx=400, cy=380, phone=True, look=(0.6, 0.0))
    K.fog(big, t, 640, OUT_H, min(0.45, u * 0.3))
    return big


def race_app(t, s, u):
    return phone_center(t, 'deadline', u + 1.2, world=HILL, cx=640, cy=360, gexpr='nervous')


def race_kids(t, s, u):
    specs = []
    for i, (x, txt_, c) in enumerate([(420, 'GO BONES', (160, 30, 40)), (760, 'GO HAROLD', (40, 90, 160)), (1100, 'RIP?', (90, 30, 120)),
                                       (1440, 'GO BONES', (160, 30, 40))]):
        jump = abs(math.sin(t * 6 + i)) * 30
        specs.append((GP.sign_stick, x + 70, 820 - jump, 6.0, dict(text=txt_, fg=c)))
        specs.append((GC.trick_or_treater, x, 1060 - jump, 7.0, dict(t=t, costume=('ghost', 'pumpkin', 'dino', 'vampire')[i], n=i,
                                                                      expr='cheer' if i % 2 else 'grin')))
    return wide(HILL, LH, 640, 520, 1.45, specs, t)


def race_count(t, s, u):
    big = edgar_cu(HILL, LH, t, 'bored', cx=640, cy=280)
    n = ['3', '2', '...'][min(2, int(u / 0.8))]
    plate(big, n, 1450, 200, 120, fg=GOLD, anchor='mm')
    return big


def race_go(t, s, u):
    gx = 880 + 400 * u * u; hx = 1180 + 380 * u * u
    big = wide(HILL, LH, 640, 470, 1.25, [(GC.grim, gx, 1050, 4.0, gk(t, 'hype', ride=True, spin=t * 60, raven=True, wind=1.0)),
                                          (GC.harold, hx, 1050, 3.8, hk(t, 'grin', pose='ride', spin=t * 60, look=(1.0, 0.0), wind=1.0))], t)
    if u < 0.12: O.flash(big, 0.7)
    plate(big, 'GO!', 960, 300, 140, fg=GREEN, anchor='mm')
    K.speed_streaks(big, t, 0.6)
    return big


def race_down(t, s, u):
    D = s['t1'] - s['t0']
    cx = lerp(300, 900, u / D)
    big = wide(HILL, LH, cx, 520, 1.6, [(GC.harold, 760, 1020, 4.6, hk(t, 'grin', pose='ride', spin=t * 50, look=(1.0, 0.0), wind=1.0)),
                                        (GC.grim, 1100, 1040, 4.8, dict(**gk(t, 'hype', ride=True, spin=t * 50, raven=True, wind=1.0),
                                                                         rot=10, pivot=(-24.0, 0.5)))], t)
    K.speed_streaks(big, t, 1.0); K.leaves(big, t, 30, seed=3, speed=2.0)
    return big


def race_gang(t, s, u):
    D = s['t1'] - s['t0']
    k = u / D
    specs = [(GC.kayden, lerp(-200, 500, k), 960, 3.4, dict(t=t, n=1, bike=True)),
             (GC.kayden, lerp(-500, 300, k), 1060, 3.6, dict(t=t, n=2, bike=True)),
             (GC.harold, lerp(400, 900, k), 1010, 4.0, hk(t, 'grin', pose='ride', spin=t * 50, look=(1.0, 0.0), wind=1.0)),
             (GC.grim, lerp(700, 1350, k), 1040, 4.4, gk(t, 'hype', ride=True, spin=t * 50, raven=True, wind=1.0))]
    big = wide(STREET, LS, 760, 520, 1.45, specs, t)
    K.speed_streaks(big, t, 0.9)
    return big


def race_woohoo(t, s, u):
    big = cu(STREET, LS, GC.grim, t, (900, 400), 9.0, 700 + 200 * math.sin(t), 400, 1.3, 4,
             **gk(t, 'hype', ride=True, spin=t * 40, wind=1.0, raven=True, raven_expr='bored'))
    K.speed_streaks(big, t, 0.9)
    return big


def race_moon(t, s, u):
    v = view_at(HILL, 1070, 260, 2.6, SX, SY)
    big = v.bg().copy()
    D = s['t1'] - s['t0']; k = u / D
    tmp = np.zeros_like(big); tmp[:] = (255, 0, 255)
    for fn, kw, dx, dy in ((GC.grim, dict(ride=True, spin=t * 40, wind=1.0), 0, 0), (GC.harold, dict(pose='ride', spin=t * 40), -330, 40)):
        sp = GX.draw(fn, 5.0, t=t, hires=True, **kw)
        blit(tmp, sp, int(lerp(-300, 2300, k)) + dx, int(760 - 300 * math.sin(k * math.pi)) + dy, 5.0)
    m = np.any(tmp != (255, 0, 255), axis=2)
    big[m] = (14, 8, 22)
    return big


def race_kevin(t, s, u):
    D = s['t1'] - s['t0']; k = u / D
    big = wide(YARD, LY, 640, 430, 1.25, [(GC.kevin, 640, 1040, 4.8, dict(t=t, wave=min(1.0, u / 0.5), look=(0.6, 0.0))),
                                          (GC.harold, lerp(-300, 1500, k), 1060, 3.8, hk(t, 'grin', pose='ride', spin=t * 60, wind=1.0)),
                                          (GC.grim, lerp(100, 1900, k), 1070, 4.2, gk(t, 'hype', ride=True, spin=t * 60, raven=True, wind=1.0))], t)
    K.speed_streaks(big, t, 0.8)
    return big


def race_fog(t, s, u):
    big = wide(STREET, LS, 640, 520, 1.45, [(GC.grim, 960, 1040, 4.8, gk(t, 'menace', ride=True, spin=t * 50, raven=True, wind=1.0))], t)
    for k in range(3): K.fog(big, t + k * 2.3, 380 + 120 * k, OUT_H, 0.55, speed=220 + 60 * k)
    x, y = 1035, 700
    K.glow_ring(big, x, y, 240, GC.GLOW, 0.55)                          # his eye sockets cut through the fog like headlights
    K.speed_streaks(big, t, 0.7)
    return big


def race_street(t, s, u):
    D = s['t1'] - s['t0']; k = u / D
    big = wide(STREET, LS, 640, 470, 1.15, [(GC.harold, lerp(-100, 900, k), 1040, 3.6, hk(t, 'grin', pose='ride', spin=t * 50, wind=1.0)),
                                            (GC.grim, lerp(200, 1200, k), 1050, 3.8, gk(t, 'hype', ride=True, spin=t * 50, raven=True, wind=1.0))], t)
    K.fireworks(big, t, s['t0'], bursts=((420, 260), (960, 180), (1500, 280)))
    K.speed_streaks(big, t, 0.6)
    return big


def race_lead(t, s, u):
    big = cu(STREET, LS, GC.grim, t, (760, 420), 9.0, 1100, 420, 1.3, 4,
             **gk(t, 'hype', ride=True, spin=t * 40, wind=1.0, raven=True))
    K.speed_streaks(big, t, 0.8)
    plate(big, 'PORCH: 50 FT', 1880, 860, 34, fg=GOLD, anchor='rt')
    return big


def race_brake(t, s, u):
    D = s['t1'] - s['t0']
    if u < 1.6:
        big = cu(STREET, LS, GC.grim, t, (1100, 420), 9.0, 1100, 420, 1.3, 4,
                 **gk(t, 'content', ride=True, spin=t * 30, wind=0.6, raven=True, look=(-1.0, 0.0)))
        sp = GX.draw(GC.harold, 3.6, t=t, pose='ride', expr='smile', spin=t * 10, look=(1.0, 0.0), hires=True)
        blit(big, sp, 260, 980, 3.6)
        plate(big, 'HAROLD: TIRED. SMILING.', 60, 140, 26, fg=(255, 200, 140))
        return big
    v = view_at(STREET, 640, 520, 1.6, SX, SY)
    big = K.dof(v.bg(), 9)
    sq = min(1.0, (u - 1.6) / 0.35)
    im = Image.fromarray(big); d = ImageDraw.Draw(im)
    d.rectangle([300, 520, 1700, 580], fill=(60, 60, 70), outline=INK, width=6)                      # the handlebar
    d.line([1100, 600, 1500 - 120 * sq, 700 - 40 * sq], fill=(180, 180, 190), width=22)             # the brake lever
    big[:] = np.array(im)
    sp = GX.draw(GC.bony_hand, 20.0, x=0.0, y=0.0, d=-1.0, grip=sq > 0.5, hires=True)
    blit(big, sp, 1350 - 80 * sq, 820, 20.0)
    if sq >= 1.0: B.shake(big, t, 8, 34); plate(big, 'SKRRRT', 200, 160, 60, fg=RED)
    return big


def race_braked(t, s, u):
    return edgar_cu(STREET, LS, t, 'shock', cx=900, cy=300, at=(1300, 1150), sc=24.0)


def race_win(t, s, u):
    cx, cy, Z = 620, 480, 1.25
    hx = lerp(1300, 760, sm(min(1.0, u / 1.2)))
    big = wide(PORCH, LP, cx, cy, Z, [(GC.harold, *W(hx, 690, cx, cy, Z), PS['harold'] * Z, dict(**hk(t, 'cheer', pose='ride', spin=t * 20, look=(-1.0, 0.0)), flip=True)),
                                      (GC.trick_or_treater, *W(420, 600, cx, cy, Z), PS['kid'] * Z, dict(t=t, costume='pumpkin', expr='cheer')),
                                      (GC.trick_or_treater, *W(560, 640, cx, cy, Z), PS['kid'] * Z, dict(t=t, costume='ghost', n=1, expr='cheer'))], t)
    K.rope_line(big, (int(W(640, 640, cx, cy, Z)[0]), 820), (int(W(640, 640, cx, cy, Z)[0]) + int(200 * max(0, 1 - u)), 820 - int(200 * min(1, u))),
                sag=10, col=(250, 250, 250))
    K.confetti(big, t, s['t0'])
    return big


def h_letwin(t, s, u):
    return harold_cu(PORCH, LP, t, 'smile', head=(900, 480), sc=10.5, cx=520, cy=400, pose='ride', look=(1.0, 0.0))


def g_battery(t, s, u):
    big = grim_cu(PORCH, LP, t, 'nervous', head=(960, 440), sc=10.5, cx=700, cy=420, look=(0.6, -0.4), flip=True)
    plate(big, 'BATTERY: 64%', 1880, 900, 34, fg=GREEN, anchor='rt')
    return big


def e_didnot(t, s, u):
    return edgar_cu(PORCH, LP, t, 'smug', cx=300, cy=300, at=(760, 1150), sc=24.0)


# ======================================================================================= 14. 2:00 AM, standard time
def end_clock(t, s, u):
    cx, cy, Z = 280, 300, 2.3
    big = wide(PORCH, LP, cx, cy, Z, [(GP.grandfather_clock, *W(170, PFLOOR, cx, cy, Z), PS['clock'] * Z, dict(t=t, hh=1 if u < 1.5 else 2, mm=59.95 if u < 1.5 else 0.0)),
                                      (GC.harold, *W(390, PFLOOR, cx, cy, Z), PS['harold'] * Z, hk(t, 'content', pose='stand', offer=max(0.0, 1 - u / 1.2),
                                                                                       look=(-1.0, 0.6), flip=True))], t)
    if u > 1.5:
        if u < 1.62: O.flash(big, 0.5)
        plate(big, '2:00 AM - STANDARD TIME', 960, 120, 44, fg=GREEN, anchor='mm')
    return big


def end_app(t, s, u):
    return phone_center(t, 'resched', u, world=PORCH, cx=500, cy=400, gexpr='awe')


def end_stars(t, s, u):
    return grim_cu(PORCH, LP, t, 'teary', head=(960, 440), sc=10.5, cx=700, cy=420, pose='phone', look=(0.4, -0.6), flip=True)


def end_town(t, s, u):
    v = view_at(HILL, 640, 470, 1.25, SX, SY)
    big = v.bg().copy()
    k = min(1.0, u / 2.0)
    reg = big[520:900]; big[520:900] = (reg * (1 - 0.35 * k)).astype(np.uint8)
    plate(big, '2:00 AM', 960, 200, 70, fg=GREEN, anchor='mm')
    return big


def end_porch(t, s, u):
    cx, cy, Z = 470, 320, 1.5
    return wide(PORCH, LP, cx, cy, Z, [(GP.grandfather_clock, *W(170, PFLOOR, cx, cy, Z), PS['clock'] * Z, dict(t=t, hh=2, mm=1.0)),
                                      (GC.harold, *W(450, PFLOOR, cx, cy, Z), PS['harold'] * Z, hk(t, 'content', pose='rock', rock=math.sin(t * 2), mug=True)),
                                      (GC.edgar, *W(760, 410, cx, cy, Z), PS['edgar'] * Z, dict(t=t, expr='bored', perch=True)),
                                      (GC.grim, *W(650, PFLOOR, cx, cy, Z), PS['grim'] * Z, gk(t, 'content', ride=False, pose='stand', mug=True, flip=True,
                                                                                   look=(-1.0, 0.0)))], t)


def end_sametime(t, s, u):
    return harold_cu(PORCH, LP, t, 'sleepy', head=(860, 500), sc=10.5, cx=420, cy=420, pose='rock', rock=math.sin(t * 2), mug=True)


def end_bike(t, s, u):
    return grim_cu(PORCH, LP, t, 'content', head=(1000, 440), sc=10.5, cx=700, cy=420, mug=True, flip=True, look=(-0.8, 0.0))


def end_nevermore(t, s, u):
    return edgar_cu(PORCH, LP, t, 'deadpan', cx=1000, cy=300)


# ======================================================================================= 15. credits + post-credits
ROLES = [('DEATH', 'HIMSELF'), ('HAROLD, 97', 'HAROLD, 97'), ('EDGAR', 'A BIRD (TIPS ACCEPTED)'), ('KEVIN', 'HIMSELF, 12 FT'),
         ('TODD', 'TODD (NEEDS FOG)'), ('KAYDEN & CREW', 'RELAXED'), ('DASHLEY', 'A ROBOT, ALLEGEDLY'),
         ('THE EXTRA HOUR', 'ITSELF (x97)'), ('THE CLOCK', 'HAROLD')]


def credits(t, s, u):
    big = stipple_bg(t, (18, 10, 28), seed=5)
    O.overlay(big, title_img(('IN ROLES',), 70), 0, 30)
    D = s['t1'] - s['t0']
    y0 = 1100 - (u / D) * 1250
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    for i, (a, b) in enumerate(ROLES):
        y = y0 + i * 150
        if 170 < y < 1060:
            d.text((900, y), a, font=pf(40), fill=GOLD, anchor='rm')
            d.text((1020, y), b, font=pf(32), fill=(220, 210, 240), anchor='lm')
    big[:] = np.array(im)
    sp = GX.draw(GC.grim, 3.4, t=t, ride=True, spin=t * 20, wind=0.5, expr='content', raven=True, hires=True)
    blit(big, sp, int((u / D) * 2300) - 200, 1075, 3.4)
    return big


def post_card(t, s, u):
    v = view_at(PORCH, 640, 360, 1.0, SX, SY)
    big = (K.dof(v.bg(), 6) * 0.5).astype(np.uint8)
    plate(big, 'MARCH 14. 1:59 AM.', 960, 480, 60, fg=(255, 236, 160), anchor='mm')
    plate(big, '(SPRING FORWARD)', 960, 620, 34, fg=(200, 190, 220), anchor='mm')
    return big


def post_flip(t, s, u):
    v = view_at(PORCH, 640, 360, 1.0, SX, SY)
    big = (K.dof(v.bg(), 6) * 0.5).astype(np.uint8)
    if u < 0.6: big_clock(big, '1:59', None, RED, 470, 200)
    else:
        big_clock(big, '3:00', 'AN HOUR GONE.', RED, 470, 200)
        if u < 0.9: O.mosaic(big, int(lerp(30, 1, (u - 0.6) / 0.3))); B.shake(big, t, 10, 34)
    return big


def post_grim(t, s, u):
    cx, cy, Z = 470, 320, 1.5
    return wide(PORCH, LP, cx, cy, Z, [(GC.rocking_chair, *W(450, PFLOOR, cx, cy, Z), PS['chair'] * Z, dict(rock=math.sin(t * 3) * 0.6)),
                                      (GC.grim, *W(650, PFLOOR, cx, cy, Z), PS['grim'] * Z, gk(t, 'panic', ride=False, pose='stand', mug=True, flip=True,
                                                                           look=(-1.0, 0.0) if int(t * 2) % 2 else (1.0, 0.0)))], t)


def post_harold(t, s, u):
    cx, cy, Z = 400, 330, 1.7
    big = wide(PORCH, LP, cx, cy, Z, [(GC.grim, *W(560, PFLOOR, cx, cy, Z), PS['grim'] * Z, gk(t, 'stunned', ride=False, pose='stand', mug=True, flip=True,
                                                                                   look=(-1.0, 0.0)))], t)
    K.glow_ring(big, *map(int, W(360, 330, cx, cy, Z)), 260, (255, 200, 120), 0.35)    # the light in the door
    return big


def s2_card(t, s, u):
    v = view_at(HILL, 760, 300, 1.25, SX, SY)
    big = (v.bg() * 0.7).astype(np.uint8)
    k = min(1.0, u / 0.25)
    O.overlay(big, title_img(('SEASON 2:', 'SPRING FORWARD'), 96), 0, 90 + int((1 - k) * 60), k)
    big_clock(big, '3:00', None, RED, 640, 120, w=520)
    return big


# ======================================================================================= dispatch + overlays
SHOT = {}
for _nm, _fn in list(globals().items()):
    if callable(_fn) and getattr(_fn, '__module__', None) == __name__ and _nm in {s['name'] for s in TL.SHOTS}:
        SHOT[_nm] = _fn
for _nm in CARDS: SHOT[_nm] = card
SHOT['cold_flip'] = lambda t, s, u: rewind(t, s, u, 'DAYLIGHT SAVING\nTIME HAS ENDED.')
SHOT['rewind'] = rewind
_missing = sorted({s['name'] for s in TL.SHOTS} - set(SHOT))
if _missing: raise SystemExit(f'shots without a function: {_missing}')

STK = dict(short=K.st('SHORT KING', (255, 210, 60), 60), hand=K.st('BY HAND', (255, 90, 80), 84),
           mph=K.st('40 MPH', (150, 255, 110), 64), braked=K.st('HE BRAKED', (255, 210, 60), 64), stars=K.st('5 STARS', (255, 210, 60), 64))


def stickers():
    out = []
    s = TL.first('twist_reveal'); out.append((STK['hand'], s['t0'] + 0.2, s['t0'] + 2.0, 1500, 220))
    s = TL.first('race_braked'); out.append((STK['braked'], s['t0'] + 0.1, s['t1'], 1450, 220))
    s = TL.first('end_stars'); out.append((STK['stars'], s['t0'] + 0.1, s['t1'], 1450, 200))
    return out


STICKERS = stickers()
HOOK = None
NOCAP = {'title', 'credits', 's2_card', 'post_card', 'post_flip', 'cold_flip', 'rewind'} | set(CARDS)
CAPY = {}
FLASH_AT = {'title', 'twist_reveal', 'race_go', 'cold_flip', 's2_card', 'deal_shake'}
MOSAIC_AT = {'title', 'card_a', 'low_wide', 'h_arrive', 'race_line', 'end_clock', 'credits', 'post_card'}


def render(t):
    global HOOK
    s = TL.shot_at(t)
    u = t - s['t0']
    big = SHOT[s['name']](t, s, u)
    if s['i'] <= 1:
        if HOOK is None: HOOK = title_img(('DEATH STUCK', 'IN A LOOP?'), 80)
        if 0.06 <= t < 2.8:
            k = min(1.0, (t - 0.06) / 0.1) * (1 - sm((t - 2.6) / 0.2))
            O.overlay(big, HOOK, 0, 60, k)
    elif t >= 2.8:
        hud(big, t, s)
    for im, t0, t1, cx, cy in STICKERS: O.draw_sticker(big, im, t, t0, t1, cx, cy)
    if s['name'] not in NOCAP: EPI.captions.draw(big, t, CAPY.get(s['name'], 960))
    if s['name'] in FLASH_AT and u < 0.15: O.flash(big, 0.6 * (1 - u / 0.15))
    if s['name'] in MOSAIC_AT and u < 0.3: O.mosaic(big, int(lerp(40, 1, u / 0.3)))
    return big


CUTS, NAMES = TL.CUTS, TL.NAMES


def sheet(ids):
    tiles = []
    for x in ids:
        i = int(x) if x.isdigit() else next(k for k, nm in enumerate(NAMES) if nm == x or nm[4:] == x)
        s = TL.SHOTS[i]; tm = (s['t0'] + s['t1']) / 2
        im = Image.fromarray(render(tm)).resize((480, 270), Image.LANCZOS)
        ImageDraw.Draw(im).text((6, 4), f'{NAMES[i]} {tm:.1f}', fill=(255, 255, 0))
        tiles.append(im)
    cols = 3; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new('RGB', (480 * cols, 270 * rows))
    for k, im in enumerate(tiles): sh.paste(im, ((k % cols) * 480, (k // cols) * 270))
    out = P.build(BK, 'msheet.png'); sh.save(out); print(out)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet': sheet(sys.argv[2:])
    else: EPI.main(render, __file__)
