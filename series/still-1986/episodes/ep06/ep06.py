"""S01E06 «UPDATE: 6 HRS» (season finale, ≈34 s, twist at 57 %: the reward taken by another — after a night of downloading, Fran
the neon sign is already playing Vince's game). Main question: will Vince finally play? Loop of the season: in the game a white
convertible parks on Ocean Drive — «PAY BY APP ONLY» (= E01) — «...It's twenty twenty-six, baby.» Hook for season 2.
  python3 ep06.py test 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
import math
import numpy as np
from PIL import Image
import fx
import atmos as AT
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import v86cast as C, v86kit as K
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T, E, TVON, LAPSE

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='v86', lang='us', promise="SEASON 2: SUMMER '87"))
FACE = CM.Faces(EPI, dict(
    vince=[(0.0, 'ecstatic'), (TVON, 'shock'), (T['v2'], 'outraged'), (T['f1'], 'defeated'), (T['v3'], 'smooth'), (T['v4'], 'scheming'),
           (T['r2'], 'defeated'), (LAPSE, 'tired'), (TWIST, 'shock'), (T['v5'], 'outraged'), (T['f4'], 'defeated'), (CUTS[13], 'cool'),
           (T['v6'], 'proudsad')],
    rey=[(0.0, 'chill'), (T['r2'], 'gotcha')]))
WS = K.WS['studio']
VIN = (560.0, 690.0)
SCREEN = (112.0, 282.0, 268.0, 388.0)            # the CRT screen in the world (px)
FRAN_W, FRAN_H = (1080.0, 410.0), 185.0
_GAME = {}


def progress(t):
    if t < LAPSE: return 0.01 * sm((t - TVON) / 10.0)
    return min(1.0, 0.01 + 0.99 * sm((t - LAPSE) / 2.0))


def tv_img(t):
    """what the CRT shows: the update progress bar, then the game"""
    if t < TWIST - 0.2:
        f = progress(t)
        hrs = max(0, int(round(6 * (1 - f))))
        return K.progress_screen(t, f, sub=f'150 GB • {hrs} HRS LEFT' if f < 0.99 else 'READY')
    return game_frame(t)


def game_frame(t, parking=False):
    """the in-game picture: a white convertible cruising Ocean Drive at sunset (the season loop to E01)"""
    key = (round(t * 6) / 6, parking)
    if key in _GAME: return _GAME[key]
    v = K.V('ocean', 600.0, 400.0, 1.0)
    x = 620.0 if parking else 300.0 + ((t * 120) % 600)
    acts = K.car_group(v, x, 616.0, t, vince_kw=dict(expr='cool'), speed=0.0 if parking else 12.0)
    big = K.shot('ocean', K.light_sunset, 600.0, 400.0, 1.0, acts=acts, t=t, dof_k=0, motes=False, bloom=None, juice=True, vig=0)
    if parking:
        st_ = K.st('PAY BY APP ONLY', fg=(255, 214, 80), size=90)
        O.draw_sticker(big, st_, t, CUTS[13] + 0.8, DUR, 540, 700)
    img = np.array(Image.fromarray(big).resize((270, 480), Image.NEAREST))
    img = np.array(Image.fromarray(img).resize((640, 480), Image.NEAREST))
    if len(_GAME) > 40: _GAME.clear()
    _GAME[key] = img
    return img


def room(t, Z, cx, cy, acts=(), fran=True, fran_kw=None, tv=True, light_tv=1.0, dawn=0.0, fx_=None, **kw):
    v = K.V('studio', cx, cy, Z)
    def f(big, _):
        if tv:
            x0, y0 = v.opt(SCREEN[0], SCREEN[1]); x1, y1 = v.opt(SCREEN[2], SCREEN[3])
            img = Image.fromarray(tv_img(t)).resize((max(1, int(x1 - x0)), max(1, int(y1 - y0))), Image.NEAREST)
            a = np.array(img).astype(np.float32); a[::6] *= 0.75
            X0, Y0 = max(0, int(x0)), max(0, int(y0)); X1, Y1 = min(OUT_W, int(x0) + a.shape[1]), min(OUT_H, int(y0) + a.shape[0])
            if X0 < X1 and Y0 < Y1: big[Y0:Y1, X0:X1] = a[Y0 - int(y0):Y1 - int(y0), X0 - int(x0):X1 - int(x0)].astype(np.uint8)
            fx.glow(big, int((x0 + x1) / 2), int((y0 + y1) / 2), int((x1 - x0) * 1.2), (110, 200, 255), 0.22)
        if fran:
            x, y = v.opt(*FRAN_W)
            K.fran(big, x, y, FRAN_H * 3 * v.Z, t, talk=CM.M.mouth(EPI.talk, 'fran', t), look=-0.6, **(fran_kw or {}))
            if t >= TWIST - 0.2: gamepad(big, x - 40 * v.Z, y - 70 * v.Z, 90 * v.Z, t)
        if dawn > 0:
            big[:] = np.clip(big.astype(np.float32) * (1 + dawn * np.array((0.08, 0.02, -0.06))) + dawn * np.array((30, 14, 0)), 0, 255).astype(np.uint8)
        if fx_: fx_(big, v)
    return K.shot('studio', lambda v_: K.light_studio(v_, light_tv), cx, cy, Z, acts=acts, fx_=f, t=t, **kw), v


def gamepad(big, x, y, w, t):
    """Fran's neon game controller: a cyan tube outline with pink buttons blinking as she plays"""
    x, y, w = int(x), int(y), int(w)
    h = int(w * 0.55); q = max(4, w // 20)
    for i in range(0, w, q):
        for yy in (y, y + h): big[max(0, yy):yy + q, max(0, x + i):x + i + q] = (90, 236, 255)
    for j in range(0, h, q):
        for xx in (x, x + w): big[max(0, y + j):y + j + q, max(0, xx):xx + q] = (90, 236, 255)
    for k in range(3):
        on = int(t * 8 + k) % 3 == 0
        bx, by = x + int(w * (0.62 + 0.1 * k)), y + int(h * (0.35 + 0.15 * (k % 2)))
        big[by:by + q * 2, bx:bx + q * 2] = (255, 70, 180) if on else (120, 40, 90)
    fx.glow(big, x + w // 2, y + h // 2, w, (90, 236, 255), 0.25)


def vince_cu(t, head, s, base=(0.8, 0.0), cx=600.0, cy=380.0, Z=1.3, kick_=(0, 0), **kw):
    k, dy = FACE('vince', t, base, **kw)
    big, a, v = CM.cu('studio', lambda v_: K.light_studio(v_, 1.0), C.vince, t, cx, cy, Z, (head[0], head[1] + dy * 10), s, k, kick=kick_)
    return big


def vince_act(v, t, x=VIN[0], y=VIN[1], flip=True, **kw):
    k, dy = FACE('vince', t, (-0.8 if flip else 0.8, 0.0), **kw)
    return K.A(C.vince, x, y + dy * 2, K.S_of(v, 'studio') * 0.9, t=t, flip=flip, **k)


# ================================================================== shots
def r_hook(t, u):
    return vince_cu(t, (470, 960), 16.0, (0.9, -0.3), hand_n=(18.0, 92.0), prop_n=C.game_box, sparkle=1.0)


def r_tv(t, u):
    v = K.V('studio', 250.0, 420.0, 1.1)
    big, _ = room(t, 1.1, 250.0, 420.0, acts=[vince_act(v, t, x=345.0)], fran=False, dof_k=10)
    return big


def r_six(t, u):
    return vince_cu(t, (520, 960), 21.0, (0.9, 0.0), kick_=kick(t, [(T['v2'] + 0.2, 1.2)]))


def r_fran(t, u):
    v = K.V('studio', 1000.0, 380.0, 1.05)
    big, _ = room(t, 1.05, 1000.0, 380.0, acts=[vince_act(v, t, x=935.0, flip=False)], dof_k=10)
    return big


def r_knock(t, u):
    v = K.V('studio', 760.0, 430.0, 1.35)
    k_t = T['v3'] - 0.25
    hand = (24.0, 74.0 + (4 if int((t - k_t) * 8) % 2 else 0)) if t < T['v3'] + 0.8 else (24.0, 70.0)
    big, _ = room(t, 1.35, 760.0, 430.0, acts=[vince_act(v, t, x=820.0, flip=False, hand_n=hand, lean=0.6)], fran=False, tv=False, dof_k=12)
    O.draw_sticker(big, ST_WALL, t, T['v3'] - 0.2, CUTS[5], 540, 360)
    return big


def rey_cu(t, u):
    k, dy = FACE('rey', t, (-0.8, 0.0))
    big, a, v = CM.cu('studio', lambda v_: K.light_studio(v_, 0.0), C.rey, t, 1000.0, 360.0, 1.35, (540, 980 + dy * 10), 17.0, k, flip=True,
                      blur=10)
    big[:] = np.clip(big.astype(np.float32) * np.array((0.85, 0.9, 1.08)), 0, 255).astype(np.uint8)    # «next door» tint
    O.draw_sticker(big, ST_NEXT, t, CUTS[5], CUTS[6], 540, 360)
    return big


def r_rey(t, u):
    return rey_cu(t, u)


def r_star(t, u):
    return vince_cu(t, (480, 980), 18.0, (0.9, 0.2), glint=1.0 if u > 0.6 else 0.0)


def r_rey2(t, u):
    big = rey_cu(t, u)
    O.draw_sticker(big, ST_20, t, T['r2'] + 0.8, CUTS[8], 540, 1280)
    return big


def r_lapse(t, u):
    v = K.V('studio', 250.0, 430.0, 1.1)
    k, dy = FACE('vince', t, (0.0, -0.5))
    k['expr'] = 'sleepy'; k['blink'] = True
    a = K.A(C.vince, 330.0, 720.0, K.S_of(v, 'studio') * 0.9, t=t, flip=True, legs=False, **{x: y for x, y in k.items() if x != 'expr'}, expr='sleepy')
    big, _ = room(t, 1.1, 250.0, 430.0, acts=[a], fran=False, dawn=sm(u / 2.0), dof_k=10)
    hrs = ['11:58 PM', '2:00 AM', '4:00 AM', '6:00 AM'][min(3, int(u / 0.6))]
    O.draw_sticker(big, K.st(hrs, fg=(255, 214, 80), size=56), t, CUTS[8], CUTS[9], 540, 360)
    zz = 'Z' * (1 + int(t * 3) % 3)
    O.draw_sticker(big, K.st(zz, fg=(200, 220, 255), size=48), t, CUTS[8], CUTS[9], 640, 820)
    return big


def r_twist(t, u):
    v = K.V('studio', 1000.0, 400.0, 1.05)
    big, _ = room(t, 1.05, 1000.0, 400.0, acts=[vince_act(v, t, x=935.0, flip=False)], dawn=1.0, dof_k=10,
                  kick=kick(t, [(TWIST + 0.05, 1.0)]))
    O.draw_sticker(big, ST_LVL, t, T['f2'] + 0.6, CUTS[10], 540, 360)
    return big


def r_mine(t, u):
    return vince_cu(t, (500, 960), 19.0, (0.9, 0.0), kick_=kick(t, [(T['v5'] + 0.3, 0.9)]))


def r_elec(t, u):
    v = K.V('studio', 1110.0, 300.0, 1.6)
    def pre(big, _): big[:] = K.blur(big, 6)
    def f(big, _):
        K.fran(big, 600, 1350, 900, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=-0.3)
        gamepad(big, 300, 1150, 380, t)
    return K.shot('studio', lambda v_: K.light_studio(v_, 0.0), 1110.0, 300.0, 1.6, pre=pre, dof_k=0, fx_=f, t=t, bloom=(200, 30, 0.7))


def r_share(t, u):
    v = K.V('studio', 1000.0, 400.0, 1.0)
    big, _ = room(t, 1.0, 1000.0, 400.0, acts=[vince_act(v, t, x=935.0, flip=False)], dawn=1.0, dof_k=10)
    return big


def r_play(t, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (24, 16, 40)
    tv = K.crt(game_frame(t, parking=True), t)
    CM.overlay_scaled(big, tv, (OUT_W - tv.shape[1] * 1.05) / 2, 560, 1.05)
    AT.juice(big, 1.1, 1.05)
    return big


def r_cool(t, u):
    return vince_cu(t, (480, 960), 19.0 * (1 + 0.02 * u), (0.0, 0.0), shades=1.0 - sm((u - 0.4) / 1.2))


def r_season2(t, u):
    v = K.V('ocean', 640.0, 360.0, 1.0)
    big = K.shot('ocean', K.light_sunset, 640.0, 360.0, 1.0 + 0.02 * u, t=t, dof_k=0)
    O.overlay(big, CARD2, 0, 560, min(1.0, u / 0.2))
    return big


ST_WALL = K.st('KNOCK KNOCK', fg=(255, 214, 80), size=56)
ST_NEXT = K.st('NEXT DOOR: REY', fg=(255, 170, 60), size=50)
ST_20 = K.st('PASSWORD: $20', fg=(255, 110, 140), size=60)
ST_LVL = K.st('LEVEL 9', fg=(255, 110, 200), size=84)
CARD2 = K.chrome_title(['SEASON 2', "SUMMER '87"], 96)
R = [r_hook, r_tv, r_six, r_fran, r_knock, r_rey, r_star, r_rey2, r_lapse, r_twist, r_mine, r_elec, r_share, r_play, r_cool, r_season2]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 6, ['FINALLY?'], hook_t=(0.10, 2.4), hook_y=260, hook_size=100,
              stickers=[(K.st('GAME FUND: -$461', fg=(90, 236, 255), size=46), T['v6'], CUTS[15], 540, 330)],
              flashes=[TWIST, CUTS[13], CUTS[15]], mosaics=[CUTS[8]],
              cap_y={0: 1500, 1: 1300, 2: 1500, 3: 1620, 4: 1500, 5: 1560, 6: 1500, 7: 1560, 8: 1300, 9: 1300, 10: 1500, 11: 1520,
                     12: 1620, 13: 1560, 14: 1520, 15: 1500})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
