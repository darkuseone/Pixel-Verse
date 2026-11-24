"""S01E04 «$38 TO SHIP A MUG?!» (MOTION DETECTED, US; 32.2 s, twist 17.3 s / 54 %, type: the roles swap — callback to E01).
STORY (radio play): the post office, Glenn with an $8 mug «WORLD'S OKAYEST SON»: «Thirty-eight dollars to ship an EIGHT dollar mug?!» —
the clerk: «Ground shipping. Arrives after Christmas. NEXT.» — «I have a SYSTEM. I'll drive it MYSELF.» — the map: 412 miles, gas $61,
snacks $19 (already more than $38) — Doris from the dash phone: «Motion detected. Glenn. Driving six hours. To save thirty BUCKS.» —
2:07 AM, mom's porch: «Two in the morning. Mom's house. Mission COMPLETE.» — he presses the bell: click, a moon, no ring — mom's doorbell
plays her message: «Hi, sweetie! Mommy's on Do Not Disturb. Leave it by the GNOME!» — through the window mom sits one metre away in
front of the TV — Doris: «Huh. Wonder where she learned THAT.» — Glenn writes his own tag «SORRY I MISSED YOU, MOM» — the door opens:
Trent with pie: «Glenn! Your mom said YES to solar. Want some PIE?» (rewatch clue: «NO SOLICITORS (EXCEPT NICE ONES)»).
  python3 ep04.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import mdcast as C
from props import mdkit as K
from props import mimic as M
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, PRESS, TAGB, DOOR

EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='md', lang='us', promise='TOMORROW: IN-LAWS IN 1 HOUR'))
TAB = (C.XTRA, C.EXPR)
FG = M.Face([(0.0, 'furious'), (2.93, 'crushed'), (6.84, 'smug'), (8.96, 'stare'), (13.9, 'proud'), (PRESS, 'stare'), (17.7, 'shock'),
             (19.2, 'crushed'), (21.5, 'dead'), (TAGB, 'crushed'), (DOOR, 'shock'), (27.5, 'dead')], TAB, seed=3)
FD = M.Face([(0.0, 'deadpan'), (8.96, 'smirk'), (11.0, 'deadpan'), (21.5, 'sweet')], TAB, seed=8)
FC = M.Face([(0.0, 'dead')], TAB, seed=6)
FT = M.Face([(0.0, 'sales')], TAB, seed=5)
CLR = {k: (t0, t0 + d) for (k, _, _, t0, _, d, _, _) in VOICE}


def mouth(who, t): return M.mouth(EPI.talk, who, t)


def kw_(F, who, t, base, **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def gkw(t, base=(-0.8, 0.0), **kw): return kw_(FG, 'glenn', t, base, **kw)


def mug_n(sp, h):
    sp_ = sp
    x, y = h
    C.big_mug.__wrapped__(sp_, x, y) if hasattr(C.big_mug, '__wrapped__') else _mug_at(sp_, x, y)


def _mug_at(sp, x, y):
    sp.sup(x + 1.0, y + 3.0, 2.6, 3.0, C.tones((250, 250, 244)), n=4.0)
    ring = sp.m_ell(x + 4.0, y + 3.2, 1.4, 1.6)[0] & ~sp.m_ell(x + 4.0, y + 3.2, 0.8, 1.0)[0]
    sp.fill(ring, (210, 210, 200))
    sp.txt_box(['OKAYEST', 'SON'], (x - 1.4, y + 0.8, x + 3.4, y + 5.4), (200, 40, 60), pad=0.05)


def shot(name, cx, cy, Z, t, acts, **kw):
    kw.setdefault('dof_k', 0.0)
    return K.shot(name, cx, cy, Z, acts=acts, t=t, **kw)


def plate(big, text, y, fg=(255, 255, 255), size=44, x=None):
    img = O.sticker(text, fg=fg, size=size)
    O.overlay(big, img, (OUT_W - img.shape[1]) // 2 if x is None else x, y, 1.0)


# ---------------------------------------------------------------- post office: Glenn in front of the counter, the clerk behind it
PG = (790.0, 700.0)
CLK = (585.0, 402.0)
CS = 2.35


def clerk_act(t, Z, stamp=False):
    m = mouth('clerk', t)
    return K.A(C.clerk, CLK[0], CLK[1], CS * 3 * Z, flip=False, **dict(expr=FC.speak(t, m), mouth_=m, blink=FC.blink(t),
                                                                       look=FC.look(t, (0.8, -0.2)), t=t, stamp=stamp))


def r_hook(t, u):
    Z = 2.0 + 0.1 * glide(u / 2.9)
    cx, cy = PG[0] - 12.0, 450.0
    shake = 4 * math.sin(t * 30) * math.exp(-t * 1.5)
    g = K.A(C.glenn, PG[0], PG[1], K.ws_at(PG[1], 'postoffice') * 3 * Z, flip=True,
            **gkw(t, hand_n=(14.0, 90.0 + 3 * math.sin(t * 12)), prop_n=lambda sp, h: _mug_at(sp, *h), lean=-2.0))
    return shot('postoffice', cx, cy, Z, t, [g], par=(-4 + 6 * u, 0), kick=(shake, 0))


def r_clerk(t, u):
    Z = 2.4
    cx, cy = CLK[0] + 10.0, 330.0
    big = shot('postoffice', cx, cy, Z, t, [clerk_act(t, Z, stamp=u > 2.6)], par=(-2 + 3 * u, 0))
    if u > 2.7: plate(big, '$38.00', 1300, fg=(255, 120, 90), size=96)
    return big


def r_sys(t, u):
    Z = 1.3
    cx, cy = 690.0, 470.0
    g = K.A(C.glenn, PG[0], PG[1], K.ws_at(PG[1], 'postoffice') * 3 * Z, flip=False,
            **gkw(t, base=(0.9, 0.0), hand_n=(12.0, 70.0), prop_n=lambda sp, h: _mug_at(sp, *h), walk=t * 6 if u > 1.2 else None))
    return shot('postoffice', cx, cy, Z, t, [clerk_act(t, Z), g], par=(-3 + 4 * u, 0))


# ---------------------------------------------------------------- the road: a navigation-app insert with growing counters
def r_map(t, u):
    k = min(1.0, u / 4.6)
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (24, 28, 44)
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([60, 150, OUT_W - 60, OUT_H - 150], 50, fill=(20, 20, 24), outline=(90, 90, 100), width=10)
    d.rectangle([90, 200, OUT_W - 90, 1160], fill=(214, 226, 200))
    for i in range(14): d.line([(90, 260 + i * 66), (OUT_W - 90, 230 + i * 70)], fill=(236, 240, 228), width=6)
    pts = [(200, 1080), (300, 900), (520, 860), (600, 640), (820, 560), (880, 320)]
    d.line(pts, fill=(70, 140, 255), width=22)
    n = int(k * (len(pts) - 1))
    fr = k * (len(pts) - 1) - n
    a = pts[min(n, len(pts) - 1)]; b = pts[min(n + 1, len(pts) - 1)]
    cxp, cyp = a[0] + (b[0] - a[0]) * fr, a[1] + (b[1] - a[1]) * fr
    d.ellipse([cxp - 24, cyp - 24, cxp + 24, cyp + 24], fill=(250, 250, 255), outline=(70, 140, 255), width=8)
    d.ellipse([860, 300, 900, 340], fill=(220, 40, 40))
    d.text((640, 260), 'MOM', font=O.pfont(40), fill=(200, 40, 40))
    d.rectangle([90, 1160, OUT_W - 90, OUT_H - 200], fill=(240, 244, 250))
    miles = int(412 * k); gas = 61 * k; snacks = 19 * min(1.0, k * 1.6)
    d.text((130, 1200), f'{miles} mi   {int(6 * k)} h {int(14 * k):02d} min', font=O.pfont(56), fill=(30, 40, 60))
    d.text((130, 1300), f'GAS     ${gas:5.2f}', font=O.pfont(56), fill=(200, 40, 40))
    d.text((130, 1380), f'SNACKS  ${snacks:5.2f}', font=O.pfont(56), fill=(200, 40, 40))
    tot = gas + snacks
    d.text((130, 1480), f'TOTAL   ${tot:5.2f}', font=O.pfont(64), fill=(200, 40, 40) if tot > 38 else (30, 120, 60))
    d.text((130, 1570), 'SHIPPING WAS $38.00', font=O.pfont(40), fill=(120, 120, 130))
    return np.array(im)


# ---------------------------------------------------------------- mom's porch at 2 AM
MG = (420.0, 530.0)                       # Glenn on mom's porch facing the door (flip)
MBELL = (343.0, 360.0)
MDS = 1.25


def mom_bell(t, Z, dnd=True, ring=None):
    m = mouth('mom', t) if CLR['m1'][0] <= t < CLR['m1'][1] else 0.0
    return K.A(C.doris, MBELL[0], MBELL[1], MDS * 3 * Z, rim=None, expr='sweet', mouth_=m, look=(0.6, 0.0), t=t, dnd=dnd, ring=ring)


def mom_inside(t, Z):
    """mom in her armchair behind the picture window: drawn into the glass region only (behind the curtains, TV light)"""
    act = K.A(lambda sp, **kw: C.mom_chair(sp, t=t, nod=0.3 * math.sin(t * 1.3)), 600.0, 420.0, 3.6 * 3 * Z, flip=True, rim=None)
    def pre(big, v_):
        tmp = big.copy()
        act(tmp, v_, None)
        x0, y0 = v_.opt(470.0, 215.0); x1, y1 = v_.opt(730.0, 415.0)
        xa, xb, ya, yb = int(max(0, x0)), int(min(OUT_W, x1)), int(max(0, y0)), int(min(OUT_H, y1))
        if xa < xb and ya < yb:
            big[ya:yb, xa:xb] = np.clip(big[ya:yb, xa:xb] * 0.35 + tmp[ya:yb, xa:xb] * 0.65 * np.array((0.85, 0.95, 1.15)), 0, 255).astype(np.uint8)
    return pre


def door_open(k):
    def pre(big, v_):
        x0, y0 = v_.opt(180.0, 195.0); x1, y1 = v_.opt(305.0, 510.0)
        xa, xb, ya, yb = int(max(0, x0)), int(min(OUT_W, x1)), int(max(0, y0)), int(min(OUT_H, y1))
        if xa >= xb or ya >= yb: return
        reg = big[ya:yb, xa:xb].astype(np.float32)
        reg = reg * (1 - 0.85 * k) + np.array((70, 46, 34)) * 0.85 * k
        yy = np.linspace(0, 1, yb - ya)[:, None, None]
        reg += np.clip(1 - yy * 1.2, 0, 1) * 90 * k * np.array((1.0, 0.8, 0.5))
        big[ya:yb, xa:xb] = np.clip(reg, 0, 255).astype(np.uint8)
    return pre


def mglenn(t, Z, **kw):
    kw.setdefault('hand_n', (12.0, 62.0))
    kw.setdefault('prop_n', lambda sp, h: _mug_at(sp, *h))
    return K.A(C.glenn, MG[0], MG[1], K.ws_at(MG[1], 'momporch') * 3 * Z, flip=True, **gkw(t, **kw))


def r_mom(t, u):
    Z = 1.35
    cx, cy = 390.0, 330.0
    big = shot('momporch', cx, cy, Z, t, [mom_bell(t, Z), mglenn(t, Z, base=(-0.6, 0.0))], par=(-4 + 6 * u, 0), pre=mom_inside(t, Z))
    plate(big, '2:07 AM', 300, fg=(255, 214, 120), size=60)
    return big


def r_press(t, u):
    Z = 2.8 - 0.25 * glide(u / 0.6)
    cx, cy = MBELL[0] + 22.0, MBELL[1] - 30.0
    g = mglenn(t, Z, hand_n=(22.0, 62.0) if u < 0.5 else (12.0, 62.0), base=(-0.9, 0.2))
    return shot('momporch', cx, cy, Z, t, [mom_bell(t, Z), g], kick=kick(t, [(PRESS, 0.8)]))


def r_window(t, u):
    Z = 1.5 + 0.2 * glide(u / 2.3)
    cx, cy = 520.0, 320.0
    g = mglenn(t, Z, base=(0.9, 0.0))
    g.flip = False
    return shot('momporch', cx, cy, Z, t, [g], pre=mom_inside(t, Z))


def r_dcu(t, u):
    """Doris on Glenn's phone in his hand (he holds it up)"""
    Z = 3.0
    cx, cy = MG[0] - 20.0, 250.0
    m = mouth('doris', t)
    ph = lambda sp, h: C.phone_stand(sp, t=t, talk=m, expr=FD.speak(t, m), look=FD.look(t, (0.6, 0.0)), blink=FD.blink(t))
    g = mglenn(t, Z, hand_n=(16.0, 84.0), prop_n=None, base=(-0.6, 0.3))
    ws = K.ws_at(MG[1], 'momporch')
    phone = K.A(lambda sp, **kw: ph(sp, (0.0, 0.0)), MG[0] - 17.0 * ws, MG[1] - 82.0 * ws, 1.9 * 3 * Z, rim=None)
    phone.near = 0.995
    return shot('momporch', cx, cy, Z, t, [g, phone])


def r_tag(t, u):
    Z = 1.75
    cx, cy = 330.0, 360.0
    g = mglenn(t, Z, hand_n=(20.0, 58.0 + 2 * math.sin(t * 20)), prop_n=None, base=(-0.9, -0.3))
    def f(big, v_):
        if u > 1.2:
            tg = K.A(lambda sp, **kw: _my_tag(sp), 262.0, 360.0, 2.4 * 3 * Z, rim=None)
            tg(big, v_, None)
    return shot('momporch', cx, cy, Z, t, [g], fx_=f)


def _my_tag(sp):
    pts = [(-1.0, 1.0), (11.0, 1.0), (11.0, -15.0), (-1.0, -15.0)]
    sp.poly(pts, C.tones(C.TAG), stripes=False)
    sp.txt_box(['SORRY', 'I MISSED', 'YOU,', 'MOM'], (-0.4, -13.4, 10.4, -1.0), (40, 20, 10), pad=0.15, lead=0.1)


def r_door(t, u):
    Z = 1.6
    cx, cy = 335.0, 330.0
    k = sm(u / 0.4)
    tr = K.A(C.trent, 245.0, 512.0, K.ws_at(512.0, 'momporch') * 1.34 * 3 * Z, flip=False, rim=None,
             **kw_(FT, 'trent', t, (0.9, 0.0), hand_n=(13.0, 44.0), prop_n=lambda sp, h: C.mug(sp, h, 'PIE')))
    acts = [tr] if k > 0.5 else []
    acts.append(mglenn(t, Z, base=(-0.9, 0.0), prop_n=None))
    return shot('momporch', cx, cy, Z, t, acts, pre=door_open(k))


ST_MOON = K.st('MOM: DO NOT DISTURB', fg=(150, 170, 255), size=52)
ST_TOT = K.st('$80 > $38', fg=(255, 120, 90), size=72)
ST_TAG = K.st('SORRY I MISSED YOU, MOM', fg=(255, 150, 60), size=44)
R = [r_hook, r_clerk, r_sys, r_map, r_mom, r_press, r_window, r_dcu, r_tag, r_door]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['$38 TO SHIP', 'A MUG?!'], hook_t=(0.10, 2.7), hook_y=1080, hook_size=76,
              stickers=[(ST_TOT, 12.6, 13.9, 540, 1720 - 640), (ST_MOON, PRESS + 0.3, 19.2, 540, 1250), (ST_TAG, 24.95, DOOR, 540, 1300)],
              flashes=[TWIST], mosaics=[8.96, 13.9],
              cap_y={0: 1580, 1: 1580, 2: 1580, 3: 1060, 4: 1580, 5: 1580, 6: 1600, 7: 1600, 8: 1580, 9: 1580})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
