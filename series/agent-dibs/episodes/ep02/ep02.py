"""S01E02 «Free Trial» — Dibs is invisible on a free trial (Cloakify). The trial ends mid-lobby, the pop-up has a microscopic X, an unskippable
mattress ad freezes everybody, and the villains hand over the Doomsday disk just to get back to the mattress.
  python3 ep02.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import paths as P
import stage as ST
from stage import Chars, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from episode import Episode
from props import chi_cast as C
from props import chi_props as PR
from props import chikit as K
from props import chiui as UI
from props import bytfx as B
from props import folk
from timeline import DUR, FPS, VOICE, SLUG, DING_T

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
WORLD = K.world('lair_lobby')
FY = 520.0                                  # floor line of the mid-depth characters in the wide shots
BAL_Y = 205.0                               # balcony floor line (mezzanine)
GHOST_A = 0.46                              # wide shots
GHOST_CU = 0.54                             # close-ups (the face has to read)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def chew(t, on=True):
    return (0.15 + 0.35 * (0.5 + 0.5 * math.sin(t * 15))) if on else 0.0


def secs_left(t):
    return max(0, int(math.ceil(DING_T - t - 1e-6)))


# ================================================================== poses
def tiptoe(t, sp=4.2):
    s = math.sin(t * sp)
    return dict(n=(4.6, 12.6), f=(-3.0, 10.4), bn=1, bf=-1, nleg=(0.55 * s + 0.2, 0.6 * max(0.0, -s)), fleg=(-0.55 * s + 0.2, 0.6 * max(0.0, s)))


FROZEN = dict(n=(5.2, 13.6), f=(-3.2, 14.8), bn=1, bf=-1, nleg=(1.25, 0.1), fleg=(-0.04, 0.0))
PINCH = dict(n=(9.2, 16.4), f=(7.6, 15.6), bn=1, bf=1, nleg=(0.12, 0.0), fleg=(-0.12, 0.0))
LEAP = dict(n=(10.4, 17.6), f=(8.0, 15.4), bn=1, bf=1, nleg=(1.0, 0.5), fleg=(-0.5, 0.9))
STORK = FROZEN


# ================================================================== reusable shot pieces
def lobby(t, cx, acts=(), ghost=(), back=(), fx_=None, emit=None, Z=1.0, sy=320, ghost_a=GHOST_A, cy=400.0):
    return K.shot(WORLD, K.light_lobby, cx, cy, Z, acts=acts, ghost=ghost, back=back, fx_=fx_, emit=emit, sx=180, sy=sy, ghost_a=ghost_a, t=t)


def cu(fn, head, un, t, u, who, expr, Z=2.3, zoom=0.06, pose=None, flip=False, k=1.7, sy=262, hy=21.0, extra=(), ghost_=False, emit=None,
       ghost_a=GHOST_CU, front=(), look=0.0, **kw):
    """close-up of one character; `head` = world position of the head (decides which part of the lobby is behind it)"""
    sgn = -1 if flip else 1
    ax, ay = head[0] - sgn * 1.5 * un, head[1] + hy * un
    call = lambda CH, v: fn(CH, v.cam(ax, ay, un, flip), pose or C.POSE['stand'], t, mouth(who, t, k) if who else 0.0, expr, look, **kw)
    acts = list(extra) + ([] if ghost_ else [call])
    return K.shot(WORLD, K.light_lobby, head[0], head[1], Z + zoom * u, acts=acts, ghost=[call] if ghost_ else (), front=front, emit=emit,
                  sx=180, sy=sy, ghost_a=ghost_a, t=t)


DIBS_HEAD = (590.0, 338.0)
GARY_HEAD = (300.0, 440.0)
TERRY_HEAD = (1010.0, 262.0)


def dibs_cu(t, u, expr='smug', ghost_=True, pose=None, shades=True, hud=True, k=1.8, Z=2.3, zoom=0.06, extra=(), alpha=GHOST_CU, **kw):
    un = 13.0
    def emit(big, v):
        if hud and ghost_:
            UI.hud(big, 800, 300, secs_left(t), t, scale=0.70)
    return cu(C.dibs, DIBS_HEAD, un, t, u, 'dibs', expr, Z=Z, zoom=zoom, pose=pose, k=k, ghost_=ghost_, emit=emit, ghost_a=alpha,
              shades=shades, chair=False, extra=extra, **kw)


def gary_cu(t, u, expr='normal', pose=None, prop=None, k=1.7, hand=None, flip=False, bites=0, on=True, head=GARY_HEAD, **kw):
    un = 13.0
    return cu(C.gary, head, un, t, u, 'gary', expr, Z=2.3, zoom=0.05, pose=pose, flip=flip, k=k, hy=19.6, prop_n=prop, hand_n=hand,
              front=(), **kw)


def parapet(wy, t):
    """foreground balcony: gold rail with posts above a dark marble parapet (output px), `wy` = world y of the parapet top"""
    def emit(big, v):
        _, oy = v.opt(0, wy)
        y0 = int(oy)
        if y0 >= OUT_H: return
        big[y0:] = (18, 20, 34)
        yy, xx = np.ogrid[y0:OUT_H, 0:OUT_W]
        vein = ((xx * 3 + yy * 5) % 211 < 4) | ((xx * 7 - yy * 2) % 307 < 3)
        reg = big[y0:]; reg[vein] = (44, 46, 72)
        big[y0:y0 + 22] = (214, 168, 56); big[y0:y0 + 8] = (255, 226, 120); big[y0 + 22:y0 + 34] = (110, 78, 20)
        big[y0 + 56:y0 + 66] = (60, 235, 255)                                                     # cyan neon strip
        for x in range(30, OUT_W, 170):                                                            # rail posts
            big[y0 - 170:y0, x:x + 22] = (214, 168, 56); big[y0 - 170:y0, x:x + 7] = (255, 226, 120)
        big[y0 - 190:y0 - 168] = (214, 168, 56); big[y0 - 190:y0 - 182] = (255, 226, 120)
    return emit


def terry_cu(t, u, expr, hand=None, prop=None, pose=None, cat=True, cat_pose='sit', k=1.7, flip=True, extra_emit=None, cat_lid=0.55, tail=0.5):
    """Terry on the mezzanine (skyline behind him), a white cat on the parapet next to him"""
    un = 13.0
    sgn = -1 if flip else 1
    ax, ay = TERRY_HEAD[0] - sgn * 1.5 * un, TERRY_HEAD[1] + 22.3 * un
    par = ay - 15.2 * un
    pe = parapet(par, t)
    def emit(big, v):
        pe(big, v)
        if extra_emit: extra_emit(big, v)
    cats = []
    if cat:
        cats = [lambda CH, v: folk.cat(CH, v.cam(TERRY_HEAD[0] + sgn * 50.0, par + 2.0, 6.2, not flip), t, pose=cat_pose, lid=cat_lid, expr='smug', tail=tail)]
    acts = [lambda CH, v: C.terry(CH, v.cam(ax, ay, un, flip), pose or C.POSE['hold'], t, mouth('terry', t, k), expr, 0.0,
                                  hand_n=hand, prop_n=prop)]
    # the cat is drawn in front of the parapet block but behind the rail posts -> it goes through `front` before emit paints the marble below the top
    return K.shot(WORLD, K.light_lobby, TERRY_HEAD[0], TERRY_HEAD[1], 2.3 + 0.05 * u, acts=acts, front=cats, emit=emit, sx=180, sy=262)


# ================================================================== the shots
def r_hook(t, u):
    un, Z = 13.0, 2.3
    ax, ay = DIBS_HEAD[0] - 1.5 * un, DIBS_HEAD[1] + 21.0 * un
    gx, gy, gu = ax + 66.0, 520.0, 8.2
    bites = int(t * 1.5) % 3
    acts = [lambda CH, v: C.gary(CH, v.cam(gx, gy, gu), C.POSE['hold'], t, chew(t), 'normal', 0.0, hand_n=C.H(5.2, 16.6),
                                 prop_n=lambda L, h: PR.sandwich(L, h, bites=bites, t=t), front=PR.guard_badge)]
    ghost = [lambda CH, v: C.dibs(CH, v.cam(ax, ay, un), C.POSE['stand'], t, mouth('dibs', t, 1.9), 'smug', 0.0, True, chair=False)]
    big = K.shot(WORLD, K.light_lobby, DIBS_HEAD[0], DIBS_HEAD[1], Z + 0.05 * u, acts=acts, ghost=ghost, ghost_a=GHOST_A, t=t, sx=180, sy=262)
    if t > 0.1: B.shake(big, t, 1.5, 21)
    return big


def r_sneak(t, u):
    k = min(1.0, u / 2.8)
    x = lerp(500.0, 800.0, k)
    cx = lerp(600.0, 690.0, sm(k))
    un = 8.4
    dy = FY + 38.0
    gx = 585.0
    acts = [
        lambda CH, v: C.terry(CH, v.cam(700.0, BAL_Y, 4.3), C.POSE['hips'], t, 0.0, 'sly', 0.0, front=None),
        lambda CH, v: folk.cat(CH, v.cam(742.0, BAL_Y, 2.1), t, pose='sit', lid=0.55, expr='smug', tint=(1.12, 1.16, 1.28)),
        lambda CH, v: C.gary(CH, v.cam(gx, FY, 8.0), C.POSE['hold'], t, chew(t), 'normal', 0.0, hand_n=C.H(5.2, 16.6),
                             prop_n=lambda L, h: PR.sandwich(L, h, bites=int(t) % 3, t=t), front=PR.guard_badge),
    ]
    ghost = [lambda CH, v: C.dibs(CH, v.cam(x, dy, un), tiptoe(t), t, mouth('dibs', t, 1.6), 'smug', 0.0, True, chair=False,
                                  prop_n=lambda L, h: PR.shovel(L, h, -1.15), hand_n=C.H(4.6, 12.6))]
    def emit(big, v):
        hx, hy = v.opt(x + 30, dy - 22 * un)
        UI.hud(big, int(hx + 150), int(hy - 30), secs_left(t), t, scale=0.95)
    return lobby(t, cx, acts=acts, ghost=ghost, emit=emit)


def r_d2(t, u):
    return dibs_cu(t, u, 'smug', k=1.5)


def r_deb(t, u, expr='smile'):
    return K.deb_frame(t, expr, mouth('deb', t, 1.6), Z=2.0, u=u)


def r_d3(t, u):
    s = sm(u / 1.2)
    return dibs_cu(t, u, 'nervous', k=1.6, alpha=lerp(GHOST_A, 0.5, s) + 0.08 * math.sin(t * 40) * s)


def r_frozen(t, u):
    un = 8.4
    x, dy = 640.0, FY + 30.0
    acts = [
        lambda CH, v: C.terry(CH, v.cam(700.0, BAL_Y, 4.3), C.POSE['hips'], t, 0.0, 'smug', 0.0),
        lambda CH, v: folk.cat(CH, v.cam(742.0, BAL_Y, 2.1), t, pose='sit', lid=0.45, expr='smug', tint=(1.12, 1.16, 1.28)),
        lambda CH, v: C.gary(CH, v.cam(710.0, FY - 10, 8.0, True), C.POSE['hold'], t, chew(t), 'normal', 0.0, hand_n=C.H(5.2, 16.6),
                             prop_n=lambda L, h: PR.sandwich(L, h, bites=1, t=t), front=PR.guard_badge),
    ]
    ghost = [lambda CH, v: C.dibs(CH, v.cam(x, dy, un), FROZEN, t, 0.0, 'nervous', 0.0, True, chair=False,
                                  prop_n=lambda L, h: PR.shovel(L, h, -0.7), hand_n=C.H(5.2, 14.2),
                                  sweat=0.8)]
    alpha = 0.36 + 0.14 * math.sin(t * 30)
    def emit(big, v):
        hx, hy = v.opt(x + 30, dy - 22 * un)
        UI.hud(big, int(hx + 150), int(hy - 30), secs_left(t), t, scale=0.95)
    return lobby(t, 660.0 + 8 * u, acts=acts, ghost=ghost, emit=emit, ghost_a=alpha, Z=1.0 + 0.04 * u)


def r_terry_cat(t, u):
    return terry_cu(t, u, 'sly', pose=C.POSE['hold'], hand=C.H(6.4, 12.4))


def r_hud_cu(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    yy = np.arange(OUT_H)[:, None]
    big[:] = (np.array((10, 16, 44)) + (np.array((30, 70, 130)) * (0.5 + 0.5 * np.sin(yy / 40.0 + t * 8))[..., None] * 0.25)).astype(np.uint8)
    big[(yy[:, 0] % 8) < 2] = (big[(yy[:, 0] % 8) < 2] * 0.7).astype(np.uint8)
    sc = 2.0 + 0.35 * u
    UI.hud(big, 540, 900, secs_left(t), t, scale=sc)
    if u > 0.2: B.shake(big, t, 4 * u, 45)
    return big


def r_popup(t, u, who='wide'):
    un = 8.4
    x = 600.0
    dy = FY + 30.0
    dib = lambda CH, v: C.dibs(CH, v.cam(x, dy, un), C.POSE['shrug'], t, 0.0, 'shock', 0.0, True, chair=False, sweat=0.4)
    acts = [dib,
            lambda CH, v: C.gary(CH, v.cam(745.0, FY - 5, 8.0, True), C.POSE['hold'], t, mouth('gary', t, 1.7) if t > 12.1 else chew(t), 'normal', -0.5,
                                 hand_n=C.H(4.4, 12.8), prop_n=lambda L, h: PR.sandwich(L, h, bites=2, t=t), front=PR.guard_badge)]
    def emit(big, v):
        pop = sm(min(1.0, u / 0.12))
        UI.popup(big, 540, 400, t, w=int(720 * (0.4 + 0.6 * pop)), k=min(1.0, pop * 1.4), shake=max(0.0, 1 - u / 0.4))
    big = lobby(t, 672.0, acts=acts, emit=emit, Z=1.25 + 0.04 * u, sy=360, cy=470.0)
    if u < 0.12: O.flash(big, 0.6 * (1 - u / 0.12))
    if u < 0.5: B.shake(big, t, 10 * (1 - u / 0.5), 35)
    return big


def r_gary_cu(t, u):
    chewing = t < 12.0 or t > 14.1
    return gary_cu(t, u, 'normal', pose=C.POSE['hold'], prop=lambda L, h: PR.sandwich(L, h, bites=2, t=t), hand=C.H(4.2, 12.4), k=1.7, look=0.3)


def r_swat(t, u):
    d = u / 0.95
    sx = lerp(0.0, 1.0, sm(min(1.0, d * 1.4)))
    un = 13.0
    arm = C.blend(C.POSE['stand'], C.POSE['reach'], sm(min(1.0, d * 3)))
    big = dibs_cu(t, u, 'angry', ghost_=False, pose=arm, hud=False, k=1.6, Z=2.1, zoom=0.04)
    px = 760 + 330 * sx + 30 * math.sin(t * 28)
    UI.popup(big, int(px), 1020, t, w=620, dodge=1.0)
    return big


def r_bird(t, u):
    # squinting Dibs, then the X and the bird
    if u < 0.75:
        return dibs_cu(t, u, 'deadpan', ghost_=False, hud=False, k=1.6, Z=2.6, zoom=0.04)
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    big[:] = (22, 26, 56)
    w = 2400
    h = int(w * 0.64)
    xc = 580
    cx, cy = xc - (w // 2 - 24), 760 - (30 - h // 2)
    UI.popup(big, cx, cy, t, w=w, bird=True, xs=3.4)
    r = 150 + 8 * math.sin(t * 9)
    yy, xx = np.ogrid[:OUT_H, :OUT_W]
    d = np.sqrt((xx - xc) ** 2 + (yy - 760) ** 2)
    ring = (d > r - 10) & (d < r + 4)
    big[ring] = (255, 236, 110)
    fx.vignette(big, 0.2)
    return big


def r_pinch(t, u):
    un = 8.4
    if u < 1.0:
        acts = [lambda CH, v: C.dibs(CH, v.cam(560.0, FY + 30, un), PINCH, t, 0.0, 'nervous', 0.0, True, chair=False, sweat=0.6),
                lambda CH, v: C.gary(CH, v.cam(715.0, FY - 5, 8.0, True), PINCH, t, 0.0, 'nervous', front=PR.guard_badge)]
        def emit(big, v):
            UI.popup(big, 540, 380, t, w=600, k=0.95)
            yy, xx = np.ogrid[:OUT_H, :OUT_W]
            for i in range(2):                                                                      # pinch ripples
                rr = 50 + 80 * ((t * 2 + i * 0.5) % 1.0)
                for cx_ in (400, 640):
                    dd = np.sqrt((xx - cx_) ** 2 + (yy - 1150) ** 2)
                    big[(dd > rr - 5) & (dd < rr + 5)] = (255, 255, 255)
        return lobby(t, 640.0, acts=acts, emit=emit, Z=1.1, sy=330)
    big = lobby(t, 640.0, acts=[lambda CH, v: C.dibs(CH, v.cam(540.0, FY + 30, un), PINCH, t, 0.0, 'nervous', 0.0, True, chair=False),
                                lambda CH, v: C.gary(CH, v.cam(735.0, FY - 5, 8.0, True), PINCH, t, 0.0, 'nervous', front=PR.guard_badge)], Z=1.1, sy=330)
    w = 760
    xc, yc = UI.popup(big, 430, 440, t, w=w, k=1.0, bird=False)
    z = 1.0 + 2.2 * sm((u - 1.0) / 0.9)
    UI.lens(big, int(xc), int(yc), R=int(120 + 90 * sm((u - 1.0) / 0.5)), z=max(1.01, z))
    pct = 100 + (1 if u > 1.8 else 0)
    ov = Image.new('RGBA', (560, 110), (0, 0, 0, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(ov); d.rectangle([0, 0, 559, 109], fill=(0, 0, 0, 215), outline=(255, 255, 255, 255), width=5)
    UI._txt(d, (280, 56), f'ZOOM {pct}%', 50, (255, 236, 110), 'mm')
    UI.blit(big, ov, 260, 1130)
    return big


def r_ad(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    n = 5 - int((t - 19.2) / 1.0)
    UI.ad_full(big, t, max(1, n), False, t0=19.2)
    if u < 0.12: O.flash(big, 0.7 * (1 - u / 0.12))
    return big


def pip(n, t, u, skip=False):
    def emit(big, v): UI.ad_pip(big, t, n, box=(40, 190, 420, 475), t0=19.2, skip=skip)
    return emit


def r_gary_dream(t, u):
    n = 5 - int((t - 19.2) / 1.0)
    return cu(C.gary, GARY_HEAD, 13.0, t, u, 'gary', 'content', pose=C.POSE['hold'], hy=19.6, k=1.5, emit=pip(max(1, n), t, u),
              prop_n=lambda L, h: PR.sandwich(L, h, bites=2, t=t), hand_n=C.H(5.0, 14.6), look=-0.4)


def r_terry_wist(t, u):
    n = 5 - int((t - 19.2) / 1.0)
    return terry_cu(t, u, 'sad', pose=C.POSE['hold'], hand=C.H(6.4, 12.4), extra_emit=pip(max(1, n), t, u), cat_lid=0.8)


def r_dibs_hush(t, u):
    n = 5 - int((t - 19.2) / 1.0)
    return cu(C.dibs, DIBS_HEAD, 13.0, t, u, 'dibs', 'stunned', k=1.5, emit=pip(max(1, n), t, u), shades=False, chair=False, pose=C.POSE['hold'])


def r_skip_on(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    UI.ad_full(big, t, 1, True, t0=19.2, pulse=0.5 + 0.5 * math.sin(u * 22))
    if u < 0.1: O.flash(big, 0.6 * (1 - u / 0.1))
    return big


def r_fight(t, u):
    un = 8.4
    if u < 0.85:
        k = sm(u / 0.85)
        dx = lerp(470.0, 590.0, k)
        gx = lerp(790.0, 645.0, k)
        arc = 90 * math.sin(math.pi * k)
        acts = [lambda CH, v: C.dibs(CH, v.cam(dx, FY + 40 - arc, un), LEAP, t, 0.0, 'angry', 0.0, True, chair=False),
                lambda CH, v: C.gary(CH, v.cam(gx, FY + 35 - arc * 0.9, 8.4, True), LEAP, t, 0.0, 'angry', 0.0, front=PR.guard_badge)]
        def pre(big, v):
            UI.ad_pip(big, t, 1, box=(300, 720, 780, 1080), t0=19.2, skip=True, pulse=0.0)
        def emit(big, v): fx.speed_lines(big, t, 0.6)
        big = K.shot(WORLD, K.light_lobby, 650.0, 400.0, 1.0, acts=acts, pre=pre, emit=emit, sx=180, sy=320)
        return big
    def pre(big, v): UI.ad_pip(big, t, 1, box=(290, 560, 790, 935), t0=19.2, skip=True)
    def emit(big, v):
        if 28.75 <= t < 29.35: UI.cookies(big, 1150, t)
    big = K.shot(WORLD, K.light_lobby, 640.0, 400.0, 1.7, acts=[
        lambda CH, v: C.dibs(CH, v.cam(590.0, 585.0, 11.0), C.POSE['reach'], t, 0.0, 'angry', 0.0, True, chair=False),
        lambda CH, v: C.gary(CH, v.cam(700.0, 582.0, 11.0, True), C.POSE['reach'], t, 0.0, 'angry', 0.0, front=PR.guard_badge)],
        pre=pre, emit=emit, sx=180, sy=300)
    B.shake(big, t, 6, 40)
    return big


def r_tvoff(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    UI.ad_full(big, t, 1, True, t0=19.2, pulse=1.0)
    p = min(1.0, max(0.0, (u - 0.1) / 0.3))
    if p > 0:
        h = max(6, int(OUT_H * (1 - p) ** 2))
        img = Image.fromarray(big).resize((OUT_W, h), Image.NEAREST)
        out = np.zeros_like(big)
        y0 = (OUT_H - h) // 2
        out[y0:y0 + h] = np.array(img)
        if p > 0.7: out[y0 - 3:y0 + h + 3, :] = (255, 255, 255)
        big = out
    return big


def r_terry_disk(t, u):
    toss = max(0.0, (t - 31.2) / 0.25)
    arm = C.blend(C.POSE['hold'], C.POSE['reach'], sm(min(1.0, toss)))
    return terry_cu(t, u, 'sly' if u < 0.4 else 'sad', pose=arm, hand=None, cat=True, k=1.5, cat_lid=0.7)


def r_dibs_disk(t, u):
    un = 13.0
    big = cu(C.dibs, DIBS_HEAD, un, t, u, 'dibs', 'stunned', k=1.6, shades=True, chair=False, pose=C.POSE['hold'])
    d = UI.disk_labeled(400)
    k = sm(min(1.0, u / 0.25))
    ang = 8 * (1 - k)
    img = Image.fromarray(d).rotate(-12 + ang, expand=True, resample=Image.NEAREST)
    O.overlay(big, np.array(img), 640, int(lerp(-200, 1010, k)))
    return big


def r_terry_shrug(t, u):
    return terry_cu(t, u, 'deadpan', pose=C.POSE['shrug'], hand=None, cat=True, k=1.6, cat_lid=0.9)


def r_receipt(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    yy = np.arange(OUT_H)[:, None]
    big[:] = (14, 18, 40)
    big[(yy[:, 0] % 12) < 2] = (22, 28, 58)
    rc = Image.fromarray(UI.receipt())
    W_ = 900
    H_ = int(W_ * rc.size[1] / rc.size[0])
    rc = rc.resize((W_, H_), Image.NEAREST)
    k = sm(min(1.0, u / 0.35))
    y = int(lerp(-H_, 190, k)) + int(4 * math.sin(t * 50) * (1 - k))
    O.overlay(big, np.array(rc), (OUT_W - W_) // 2, y)
    if u > 0.5:                                                                                    # AUTO-RENEW stamp
        st_ = O.sticker('AUTO-RENEW', fg=(240, 60, 70), size=84)
        a = Image.fromarray(st_).rotate(14, expand=True, resample=Image.NEAREST)
        sc = 1.0 + 0.5 * max(0.0, 1 - (u - 0.5) / 0.08)
        a = a.resize((int(a.size[0] * sc), int(a.size[1] * sc)), Image.NEAREST)
        O.overlay(big, np.array(a), 540 - a.size[0] // 2, 960 - a.size[1] // 2)
    return big


def r_gary_link(t, u):
    return cu(C.gary, GARY_HEAD, 13.0, t, u, 'gary', 'sad', pose=C.POSE['hold'], hy=19.6, k=1.5,
              prop_n=lambda L, h: PR.phone_ad(L, h), hand_n=C.H(5.6, 13.0), look=0.2)


def r_loop(t, u):
    return r_hook(0.0 + (t - 37.0) * 0.0 + 0.0, 0.0)


# ================================================================== shot table
SHOTS = [
    (0.00, 1.50, 'hook'), (1.50, 4.30, 'sneak'), (4.30, 6.00, 'd2'), (6.00, 7.80, 'deb'), (7.80, 9.00, 'd3'), (9.00, 10.30, 'frozen'),
    (10.30, 11.20, 'terry_cat'), (11.20, 11.80, 'hud_cu'), (11.80, 13.10, 'popup'), (13.10, 14.50, 'gary_cu'), (14.50, 15.45, 'swat'),
    (15.45, 17.00, 'bird'), (17.00, 19.20, 'pinch'), (19.20, 20.40, 'ad'), (20.40, 23.00, 'gary_dream'), (23.00, 25.20, 'terry_wist'),
    (25.20, 27.10, 'dibs_hush'), (27.10, 27.90, 'skip_on'), (27.90, 29.60, 'fight'), (29.60, 30.00, 'tvoff'), (30.00, 32.20, 'terry_disk'),
    (32.20, 33.50, 'dibs_disk'), (33.50, 34.50, 'terry_shrug'), (34.50, 35.40, 'receipt'), (35.40, 37.00, 'gary_link'), (37.00, DUR + 1, 'loop'),
]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    return {'hook': r_hook, 'sneak': r_sneak, 'd2': r_d2, 'deb': r_deb, 'd3': r_d3, 'frozen': r_frozen, 'terry_cat': r_terry_cat,
            'hud_cu': r_hud_cu, 'popup': r_popup, 'gary_cu': r_gary_cu, 'swat': r_swat, 'bird': r_bird, 'pinch': r_pinch, 'ad': r_ad,
            'gary_dream': r_gary_dream, 'terry_wist': r_terry_wist, 'dibs_hush': r_dibs_hush, 'skip_on': r_skip_on, 'fight': r_fight,
            'tvoff': r_tvoff, 'terry_disk': r_terry_disk, 'dibs_disk': r_dibs_disk, 'terry_shrug': r_terry_shrug, 'receipt': r_receipt, 'gary_link': r_gary_link,
            'loop': r_loop}[name](t, u)


# ================================================================== overlays
def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 2, ['INVISIBLE', '(FREE TRIAL)'], hook_t=(0.15, 2.4),
              stickers=[
                  (st('DAY 7 OF 7', (255, 110, 110), 60), 8.95, 10.25, 540, 600),
                  (st('WHISPER FIGHT', (255, 255, 255), 56), 27.95, 29.05, 540, 520),
                  (st('TRIAL RENEWED. SURPRISE.', (110, 240, 255), 38), 37.05, 38.0, 540, 470),
              ],
              flashes=[], mosaics=[], cap_default=1400,
              cap_y={'sneak': 1450, 'frozen': 1450, 'popup': 1450, 'pinch': 1450, 'receipt': 1700})


def render(t):
    big = render_scene(t)
    if abs(t - DING_T) < 0.2 and t >= DING_T: pass
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
