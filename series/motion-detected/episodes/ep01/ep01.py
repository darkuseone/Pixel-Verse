"""S01E01 «I WAS HOME!» (MOTION DETECTED, US; 36.8 s, twist 18.1 s / 49 %, type: the villain is your own — Glenn muted the bell himself).
STORY (radio play): dusk, 4:58 PM, Glenn on his porch in a tartan robe waving the orange tag: «I was HOME! All DAY! And they leave me
THIS?!» — Doris, the KNOCKR doorbell: «You were home, Glenn. Nine hours. In the ROBE.» — «I took a vacation day to sign for Linda's
GIFT!» (phone: SIGNATURE REQUIRED 8 AM–9 PM) — flashback 8:00 AM, the chair facing the door: «I had a SYSTEM. Chair. Coffee. Eyes on that
DOOR.» — «Correct. Let's watch two-fourteen.» FOOTAGE 2:14 PM: the PARCELZ courier presses the button (silence), slaps the tag and
vanishes; through the sidelight glass Glenn sits one metre away staring at the door. «He was RIGHT there. Why didn't it RING?» —
TWIST: «Do Not Disturb, Glenn. You set it Monday. For SOLICITORS.» (moon on the button, «SET BY: GLENN») — «Unmute it! NOW!» — DING-DONG:
Trent: «Hi there! Got a minute to talk about SOLAR?» — Doris: «Muted. Oh, and the depot closes at FIVE.» — «It's four fifty-EIGHT!» —
he sprints down the street in the robe, one slipper left on the porch: «Motion detected. Glenn. Running. In the ROBE.»
Rewatch clue in frame 1: «NO SOLICITORS — THIS MEANS YOU, TRENT» on the door and the moon on Doris's button.
No background blur (owner 22.11.2026). No loop-repeat at the end (owner 22.11.2026).
  python3 ep01.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import mdcast as C
from props import mdkit as K
from props import mimic as M
from props.mdkit import at, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T0, DING

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='md', lang='us', promise='TOMORROW: ONE BULB OUT'))
TAB = (C.XTRA, C.EXPR)
FG = M.Face([(0.0, 'furious'), (3.05, 'furious'), (4.2, 'crushed'), (6.39, 'furious'), (9.05, 'smug'), (12.44, 'stare'), (15.93, 'shock'),
             (17.0, 'crushed'), (18.1, 'shock'), (20.5, 'dead'), (22.25, 'panic'), (24.2, 'hopeful'), (25.3, 'dead'), (27.4, 'dead'),
             (29.6, 'shock'), (30.32, 'panic')], TAB, seed=3)
FD = M.Face([(0.0, 'deadpan'), (3.05, 'smirk'), (6.0, 'deadpan'), (12.44, 'deadpan'), (18.1, 'sweet'), (22.25, 'deadpan'), (27.4, 'sweet'),
             (32.0, 'deadpan')], TAB, seed=8)
FT = M.Face([(0.0, 'sales')], TAB, seed=5)

DORIS = (346.0, 324.0)            # her bottom on the wall right of the sidelight (≈1.3 m above the porch floor)
DS = 1.55                         # world px per Doris sprite px (≈ 22 cm tall: a real doorbell, cartoon-generous)
FEET = 528.0                      # porch floor row near the door
GX = 452.0                        # Glenn on the porch, right of Doris, facing her (flip)
TRENT_K = 1.34                    # trent / courier sprites are shorter: scale to adult height
COUR_K = 1.12


def mouth(who, t): return M.mouth(EPI.talk, who, t)


def kw_(F, who, t, base, **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def gkw(t, base=(-0.8, 0.0), **kw): return kw_(FG, 'glenn', t, base, **kw)
def dkw(t, base=(0.6, 0.0), **kw): return kw_(FD, 'doris', t, base, **kw)
def tkw(t, base=(0.8, 0.0), **kw): return kw_(FT, 'trent', t, base, **kw)


def doris_act(t, Z, dnd=None, ring=None, base=(0.6, 0.0)):
    if dnd is None: dnd = t < 22.25                                                   # the moon is on until he unmutes (22.25)
    return K.A(C.doris, DORIS[0], DORIS[1], DS * 3 * Z, rim=None, **dkw(t, base, dnd=dnd, ring=ring))


def glenn_act(wx, wy, t, Z, base=(-0.8, 0.0), flip=True, world='porch', k=1.0, **kw):
    return K.A(C.glenn, wx, wy, K.ws_at(wy, world) * 3 * Z * k, flip=flip, **gkw(t, base, **kw))


def tag_n(sp, h): C.door_tag(sp, h, 1.0, 0.25 * math.sin(sp_t[0] * 14))


sp_t = [0.0]


def shot(name, cx, cy, Z, **kw):
    kw.setdefault('dof_k', 0.0)
    return K.shot(name, cx, cy, Z, **kw)


def plate(big, text, y, fg=(255, 255, 255), size=44, x=None):
    img = O.sticker(text, fg=fg, size=size)
    O.overlay(big, img, (OUT_W - img.shape[1]) // 2 if x is None else x, y, 1.0)


# ================================================================== 0: HOOK — Glenn on the porch waving the tag at Doris
def r_hook(t, u):
    sp_t[0] = t
    Z = 1.45 + 0.10 * glide(u / 3.0)
    cx, cy = 418.0, 285.0
    shake = 4 * math.sin(t * 30) * math.exp(-t * 1.5)
    g = glenn_act(GX, FEET, t, Z, hand_n=(15.0, 96.0 + 3 * math.sin(t * 13)), prop_n=tag_n, lean=-2.0)
    return shot('porch', cx, cy, Z, acts=[doris_act(t, Z), g], par=(-4 + 6 * u, 0), t=t, kick=(shake, 0))


# ================================================================== 1/4/10: DORIS close-up = the camera moves in on the wall
def r_doris(t, u, Z0=3.0, dnd=None, look=(0.6, 0.0)):
    sp_t[0] = t
    Z = Z0 + 0.15 * glide(u / 3.0)
    cx, cy = DORIS[0] + 30.0, DORIS[1] - 30.0
    g = glenn_act(GX + 8, FEET, t, Z, base=(-0.9, 0.1), hand_n=(12.0, 50.0), prop_n=tag_n)
    return shot('porch', cx, cy, Z, acts=[doris_act(t, Z, dnd=dnd, base=look), g], par=(-2 + 3 * u, 0), t=t)


def r_d1(t, u): return r_doris(t, u, 2.7)
def r_dcu(t, u): return r_doris(t, u, 3.0, look=(0.0, -0.3))
def r_dcu2(t, u): return r_doris(t, u, 3.1, dnd=True)


# ================================================================== 2: PHONE — the delivery app
def r_phone(t, u):
    big = K.phone_insert(t)
    k = 1.0 + 0.04 * u
    h, w = big.shape[:2]
    ys = (np.arange(h) / k + h * (1 - 1 / k) / 2).astype(int); xs = (np.arange(w) / k + w * (1 - 1 / k) / 2).astype(int)
    return big[ys][:, xs]


# ================================================================== 3: FLASHBACK 8:00 AM — the chair facing the door
def r_flash(t, u):
    Z = 1.0 + 0.10 * glide(u / 3.3)
    cx, cy = 590.0, 380.0
    g = glenn_act(700.0, 582.0, t, Z, base=(-1.0, 0.0), world='hall', seated=True, hand_n=(17.0, 52.0),
                  prop_n=lambda sp, h: C.mug(sp, h, '#1 DAD'), hand_f=(16.0, 46.0))
    ch = K.A(C.chair, 706.0, 584.0, K.ws_at(584.0, 'hall') * 3 * Z, flip=True)
    big = shot('hall', cx, cy, Z, acts=[ch, g], par=(-4 + 6 * u, 0), t=t)
    plate(big, 'THIS MORNING 8:00 AM', 300, fg=(255, 232, 160), size=40)
    return big


# ================================================================== 5: FOOTAGE 2:14 PM — courier, silence, tag; Glenn behind the glass
def r_foot(t, u):
    Z = 1.15
    cx, cy = 335.0, 330.0
    if u < 0.45:
        x = lerp(600.0, 398.0, sm(u / 0.45)); arm = False; run = t * 14
    elif u < 0.95:
        x = 398.0; arm = True; run = 0.0
    else:
        x = lerp(398.0, 700.0, sm((u - 0.95) / 0.5)); arm = False; run = t * 16
    cr = K.A(lambda sp, **kw: C.courier(sp, t=t, run=run, arm_up=arm, look=(-0.8, 0.0)), x, FEET, K.ws_at(FEET) * COUR_K * 3 * Z, flip=True)
    acts = [doris_act(t, Z, dnd=True), cr]
    gl = glenn_act(296.0, 480.0, t, Z, base=(-0.2, 0.0), flip=False, k=0.95, seated=True, hand_n=(17.0, 52.0),
                   prop_n=lambda sp, h: C.mug(sp, h, '#1 DAD'))
    gl.rimc = None

    def pre(big, v_):
        tmp = big.copy()
        gl(tmp, v_, None)
        x0, y0 = v_.opt(281.0, 112.0); x1, y1 = v_.opt(311.0, 322.0)
        xa, xb, ya, yb = int(max(0, x0)), int(min(OUT_W, x1)), int(max(0, y0)), int(min(OUT_H, y1))
        if xa < xb and ya < yb:
            big[ya:yb, xa:xb] = np.clip(big[ya:yb, xa:xb] * 0.3 + tmp[ya:yb, xa:xb] * 0.7 * np.array((0.92, 0.98, 1.05)), 0, 255).astype(np.uint8)
    def f(big, v_):
        if u > 0.62:                                                                      # the tag is on the door
            tg = K.A(lambda sp, **kw: C.door_tag(sp, (0.0, 0.0), 1.0, 0.0), 232.0, 330.0, 3.0 * 3 * Z, rim=None)
            tg(big, v_, None)
        if 0.45 <= u < 0.95:
            plate(big, '*click*', 760, fg=(220, 220, 220), size=44)
    big = shot('porch', cx, cy, Z, acts=acts, t=t, pre=pre, fx_=f, juice=False, motes=False)
    return K.cam_look(big, t, stamp='11/23  2:14:%02d PM' % (7 + int(u * 1.5)))


# ================================================================== 6: «He was RIGHT there. Why didn't it RING?»
def r_g4(t, u):
    sp_t[0] = t
    Z = 2.3 + 0.12 * u
    cx, cy = GX - 10.0, 215.0
    g = glenn_act(GX, FEET, t, Z, base=(-0.9, 0.0), hand_n=(13.0, 60.0), prop_n=tag_n)
    return shot('porch', cx, cy, Z, acts=[doris_act(t, Z), g], par=(3 - 4 * u, 0), t=t)


# ================================================================== 7: TWIST — Do Not Disturb, set by Glenn
def r_twist(t, u):
    sp_t[0] = t
    Z = 3.5 - 0.3 * glide(u / 0.5)
    cx, cy = DORIS[0] + 6.0, DORIS[1] - 26.0
    g = glenn_act(GX + 8, FEET, t, Z, base=(-0.9, 0.1), hand_n=(12.0, 50.0), prop_n=tag_n)
    return shot('porch', cx, cy, Z, acts=[doris_act(t, Z, dnd=True, base=(0.0, 0.0)), g], t=t, kick=kick(t, [(TWIST, 0.9)]))


# ================================================================== 8: «Unmute it! NOW!» — he jabs at the button
def r_g5(t, u):
    Z = 1.6
    cx, cy = 436.0, 262.0
    jab = 0.5 + 0.5 * math.sin(t * 16)
    g = glenn_act(GX - 24, FEET, t, Z, base=(-1.0, 0.1), hand_n=(21.0 + 3 * jab, 61.0), sweat=1.0, lean=-4.0)
    return shot('porch', cx, cy, Z, acts=[doris_act(t, Z, dnd=u < 0.85), g], par=(-2 + 3 * u, 0), t=t)


# ================================================================== 9: DING-DONG — Trent and SOLAR
def r_trent(t, u):
    sp_t[0] = t
    Z = 1.42
    cx, cy = 440.0, 320.0
    w = sm((t - CUTS[9]) / 0.35)
    tr = K.A(C.trent, lerp(560.0, 392.0, w), FEET + 4, K.ws_at(FEET) * TRENT_K * 3 * Z, flip=False,
             **tkw(t, (0.9, 0.0), walk=t * 8 if w < 1 else None, hand_f=(-8.0, 52.0) if t < DING + 0.4 else None,
                   prop_n=lambda sp, h: C.clipboard(sp, h)))
    g = glenn_act(520.0, FEET + 6, t, Z, base=(-0.9, 0.0), hand_n=(12.0, 50.0), prop_n=tag_n)
    acts = [doris_act(t, Z, dnd=False, ring=1.0 if DING <= t < DING + 0.6 else None), tr, g]
    return shot('porch', cx, cy, Z, acts=acts, par=(-3 + 4 * u, 0), t=t)


# ================================================================== 11: «It's four fifty-EIGHT!» — the watch
def r_watch(t, u):
    Z = 2.5
    cx, cy = GX - 6.0, 210.0
    g = glenn_act(GX, FEET, t, Z, base=(0.6, -0.8), hand_n=(10.0, 84.0), sweat=2.0)
    big = shot('porch', cx, cy, Z, acts=[g], t=t, kick=(3 * math.sin(t * 40), 0))
    plate(big, '4:58 PM', 1360, fg=(255, 120, 90), size=70)
    return big


# ================================================================== 12: the sprint in the robe (button)
def r_run(t, u):
    p = sm(u / 4.0)
    Z = 1.0
    gx = lerp(520.0, 1180.0, min(1.0, u / 3.6)); gy = lerp(600.0, 470.0, min(1.0, u / 2.0))
    cx, cy = min(1100.0, max(480.0, gx - 40.0)), lerp(380.0, 370.0, p)
    S = K.ws_at(FEET) * 3 * Z * lerp(1.0, 0.62, min(1.0, u / 2.6))
    g = K.A(C.glenn, gx, gy, S, flip=False, **gkw(t, (1.0, 0.0), run=t * 15, slipper=False, sweat=2.0))
    slip = K.A(lambda sp, **kw: sp.sup(1.8, 0.6, 4.2, 1.1, C.tones(C.SLIDE), n=2.4, gloss=0.4), 470.0, FEET + 2, K.ws_at(FEET) * 3 * Z, rim=None)
    tr = K.A(C.trent, 400.0, FEET + 4, K.ws_at(FEET) * TRENT_K * 3 * Z, flip=False,
             **tkw(t, (1.0, 0.0), hand_n=(14.0, 60.0 + 6 * math.sin(t * 8)), prop_f=lambda sp, h: C.clipboard(sp, h)))
    return shot('porch', cx, cy, Z, acts=[doris_act(t, Z, dnd=False), slip, tr, g], par=(-6 * p, 0), t=t)


ST_DND = K.st('DO NOT DISTURB: ON', fg=(150, 170, 255), size=46)
ST_BY = K.st('SET BY: GLENN', fg=(255, 210, 90), size=66)
ST_SOLAR = K.st('SOLICITOR!', fg=(255, 120, 90), size=60)
R = [r_hook, r_d1, r_phone, r_flash, r_dcu, r_foot, r_g4, r_twist, r_g5, r_trent, r_dcu2, r_watch, r_run]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['I WAS HOME!'], hook_t=(0.10, 2.7), hook_y=1180, hook_size=88,
              stickers=[(ST_DND, 18.3, 22.2, 540, 1210), (ST_BY, 19.6, 22.2, 540, 1330), (ST_SOLAR, 25.0, 27.3, 540, 1300)],
              flashes=[TWIST, DING], mosaics=[9.05, 14.43],
              cap_y={0: 1560, 1: 1580, 2: 1640, 3: 1560, 4: 1580, 5: 1500, 6: 1600, 7: 1580, 8: 1560, 9: 1600, 10: 1580, 11: 1600, 12: 1500})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
