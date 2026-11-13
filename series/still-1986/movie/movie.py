"""«VINCE VELOUR'S GUIDE TO 1986» — STILL 1986 extended version, 16:9 (a fake 1986 late-night TV special on a VHS tape).
  python3 movie.py test 3 40 | frames 3 | all      then  python3 mix.py <noaudio.mp4> final.mp4      (PV_WIDE=1 is set here)"""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'episodes'))
import common as CM
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import fx
import atmos as AT
import overlays as O
from stage import OUT_W, OUT_H
from scene import sm
from cam25 import kick
from episode import Episode
import paths as P
from props import v86cast as C, v86kit as K
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, SHOTS, TWIST

assert (OUT_W, OUT_H) == (1920, 1080)
EPI = Episode('movie', VOICE, DUR, FPS, colors=K.COL, slug=SLUG,
              endcard=dict(style='v86', lang='us', sec=3.0, promise="IT'S FREE*", cy=300))
WS = float(os.environ.get('MV_WS', '3.4'))       # world px per hero sprite px at the host desk (desk ≈ 0.75 m ≈ 150 world px)
DESK = (270.0, 560.0)
SCR = (712.0, 184.0, 1068.0, 474.0)              # the studio screen (world)
FRAN_W, FRAN_H = (606.0, 395.0), 210.0

VTRACK = [(0.0, 'smooth')] + [(s[0], s[3]['expr']) for s in SHOTS if s[3].get('expr')]
FACE = CM.Faces(EPI, dict(vince=VTRACK, rey=[(0.0, 'chill')]))


def shot_of(t):
    i = max(0, min(len(SHOTS) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    return i, SHOTS[i]


# ---------------------------------------------------------------- episode clips (decoded once per shot, 405x720)
_CLIP = {}


def clip_frame(ep, a, b, t):
    key = (ep, a, b)
    if key not in _CLIP:
        _CLIP.clear()
        src = P.series(SLUG) / 'episodes' / ep / 'final.mp4'
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a:.3f}', '-t', f'{b - a + 0.1:.3f}', '-i', str(src), '-vf', 'scale=405:720',
                              '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
        _CLIP[key] = np.frombuffer(raw, np.uint8).reshape(-1, 720, 405, 3)
    arr = _CLIP[key]
    return arr[int(np.clip(round((t - a) * FPS), 0, len(arr) - 1))]


def screen_content(big, v, img, k=1.0, tall=False):
    """a picture into the studio screen; a 9:16 frame sits in the middle with a blurred, darkened pillar fill"""
    x0, y0 = v.opt(SCR[0], SCR[1]); x1, y1 = v.opt(SCR[2], SCR[3])
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    w, h = x1 - x0, y1 - y0
    if w < 20 or h < 20: return
    src = Image.fromarray(img)
    if tall:
        fill = np.asarray(src.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(2, w // 30))), np.float32) * 0.40
        cw = int(h * 9 / 16)
        lay = fill.copy(); cx = (w - cw) // 2
        lay[:, cx:cx + cw] = np.asarray(src.resize((cw, h), Image.BILINEAR), np.float32)
    else:
        lay = np.asarray(src.resize((w, h), Image.NEAREST), np.float32).copy()
    lay[::4] *= 0.86                                                         # CRT scanlines
    X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(OUT_W, x1), min(OUT_H, y1)
    if X0 >= X1 or Y0 >= Y1: return
    sub = lay[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    big[Y0:Y1, X0:X1] = np.clip(big[Y0:Y1, X0:X1] * (1 - k) + sub * k, 0, 255).astype(np.uint8)


def board_img(text, w=480, h=390):
    im = Image.new('RGB', (w // 3, h // 3), (24, 14, 46)); d = ImageDraw.Draw(im); d.fontmode = '1'
    W_, H_ = im.size
    d.rectangle([3, 3, W_ - 4, H_ - 4], outline=(255, 70, 180), width=2)
    for i, c in enumerate(K.STRIPES): d.rectangle([3, H_ - 18 + i * 3, W_ - 4, H_ - 16 + i * 3], fill=c)
    parts = text.split(': ')
    s1 = 12
    while O.pfont(s1).getlength(parts[0]) > W_ - 14 and s1 > 6: s1 -= 1
    d.text(((W_ - O.pfont(s1).getlength(parts[0])) / 2, 22), parts[0], font=O.pfont(s1), fill=(90, 236, 255))
    if len(parts) > 1:
        lines = parts[1].split(' (')
        for j, ln in enumerate(lines):
            ln = ln if j == 0 else '(' + ln
            s2 = 16 if j == 0 else 10
            while O.pfont(s2).getlength(ln) > W_ - 14 and s2 > 6: s2 -= 1
            d.text(((W_ - O.pfont(s2).getlength(ln)) / 2, 50 + j * 24), ln, font=O.pfont(s2), fill=(255, 214, 80) if j == 0 else (255, 110, 200))
    return np.asarray(im.resize((w, h), Image.NEAREST))


def logo_img(t, w=480, h=390):
    im = Image.new('RGB', (w // 3, h // 3), (20, 10, 40)); d = ImageDraw.Draw(im); d.fontmode = '1'
    W_, H_ = im.size
    sun = int(30 + 3 * math.sin(t * 2))
    d.ellipse([W_ // 2 - sun, 86 - sun, W_ // 2 + sun, 86 + sun], fill=(255, 150, 70))
    d.rectangle([0, 86, W_, H_], fill=(20, 10, 40))
    for i, c in enumerate(K.STRIPES): d.rectangle([0, 88 + i * 5, W_, 90 + i * 5], fill=c)
    f = O.pfont(13)
    for j, line in enumerate(('VINCE-O', 'VISION')):
        d.text(((W_ - f.getlength(line)) / 2, 14 + j * 18), line, font=f, fill=(255, 110, 200) if j else (90, 236, 255))
    return np.asarray(im.resize((w, h), Image.NEAREST))


def neon_phone(big, x, y, s):
    """a neon handset outline (Fran «on the line»)"""
    x, y, s = int(x), int(y), max(12, int(s))
    q = max(4, s // 12)
    for i in range(0, s, q):
        yy = y - int(math.sin(i / s * math.pi) * s * 0.28)
        if 0 <= yy < OUT_H - q and 0 <= x + i < OUT_W - q: big[yy:yy + q, x + i:x + i + q] = (90, 236, 255)
    for dx in (-q, s - q):
        if 0 <= y < OUT_H - q * 3 and 0 <= x + dx < OUT_W - q * 3: big[y:y + q * 3, x + dx:x + dx + q * 3] = (255, 70, 180)
    fx.glow(big, x + s // 2, y - s // 6, s, (90, 236, 255), 0.25)


def live_bug(big, t):
    im = Image.new('RGBA', (300, 56), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, 299, 55], 10, fill=(22, 16, 30, 200))
    if int(t * 1.5) % 2 == 0: d.ellipse([14, 18, 34, 38], fill=(255, 50, 60, 255))
    d.text((46, 17), 'LIVE • 1986', font=O.pfont(22), fill=(255, 244, 226, 255))
    O.overlay(big, np.array(im), 40, 34, 1.0)


def chyron(big, top, sub, x=60, y=860):
    im = Image.new('RGBA', (900, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, 899, 70], fill=(250, 244, 226, 235))
    for i, c in enumerate(K.STRIPES): d.rectangle([0, 70 + i * 5, 899, 74 + i * 5], fill=c + (255,))
    d.rectangle([0, 90, 640, 119], fill=(22, 16, 30, 230))
    s = 40
    while O.pfont(s).getlength(top) > 860 and s > 12: s -= 2
    d.text((20, 14), top, font=O.pfont(s), fill=(30, 18, 60, 255))
    d.text((16, 95), sub, font=O.pfont(18), fill=(255, 214, 80, 255))
    O.overlay(big, np.array(im), x, y, 1.0)


# ---------------------------------------------------------------- the studio
def fran_wall(big, v, t, talk=True):
    x, y = v.opt(*FRAN_W)
    K.fran(big, x, y, FRAN_H * 3 * v.Z, t, talk=CM.M.mouth(EPI.talk, 'fran', t) if talk else 0.0, look=-0.6)


def host(v, t, base=(0.9, 0.0), x=DESK[0], y=DESK[1], z=1.0, **kw):
    k, dy = FACE('vince', t, base, **kw)
    k.setdefault('legs', False)
    a = K.A(C.vince, x, y + dy * 2, WS * 3 * v.Z * z, t=t, **k)
    a.near = 0.15                                   # behind the desk (desk ≈ 0.24 on the near map, back wall ≈ 0.03)
    return a


def studio_light(v_):
    return K.light_studio(v_, 0.6)


def studio(t, Z, cx, cy, acts=(), screen=None, tall=False, fran=True, fx_=None, **kw):
    v = K.V('tvstudio', cx, cy, Z)
    def pre(big, _):                                                # wall stuff first: the actors stand in front of it
        if screen is not None: screen_content(big, v, screen, tall=tall)
        if fran: fran_wall(big, v, t)
    kw.setdefault('dof_k', 8)
    return K.shot('tvstudio', studio_light, cx, cy, Z, acts=acts, pre=pre, fx_=(lambda big, _: fx_(big, v)) if fx_ else None, t=t, **kw), v


def screen_now(t, kw):
    return board_img(kw['board']) if kw.get('board') else logo_img(t)


def hands(kw, u):
    e = {}
    if kw.get('phone'): e.update(hand_n=(10.0, 74.0), prop_n=C.phone)
    if kw.get('arms'): e.update(hand_n=(28.0, 92.0), hand_f=(-16.0, 92.0))
    if kw.get('point'): e.update(hand_n=(30.0, 72.0))
    if kw.get('tears'): e['tears'] = 1.0
    if kw.get('cough'): e['sweat'] = 1.0
    if kw.get('shades_off'): e['shades'] = 1.0 - sm((u - 0.5) / 1.0)
    return e


# ================================================================== shot renderers  r(t, u, kw, t0)
def vhs_card(lines, t, bg=(20, 40, 200), k=0.5):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = bg
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    for x, y, txt, s, c in lines: d.text((x, y), txt, font=O.pfont(s), fill=c)
    big = np.asarray(im).copy()
    fx.vhs(big, t, k)
    return big


def r_play(t, u, kw, t0):
    return vhs_card([(120, 100, 'PLAY >' if int(t * 3) % 2 == 0 else 'PLAY', 64, (255, 255, 255)),
                     (120, 940, 'SP  0:00:0' + str(int(t * 9) % 10), 36, (255, 255, 255))], t, k=0.6)


def r_host_wide(t, u, kw, t0):
    Z = 0.60 + (0.08 * sm(u / 6.0) if kw.get('push') else 0.0)
    cx = 640.0 - (100.0 * sm(u / 6.0) if kw.get('push') else 0.0)
    v = K.V('tvstudio', cx, 380.0, Z)
    a = host(v, t, (0.9, 0.0), **hands(kw, u))
    big, _ = studio(t, Z, cx, 380.0, acts=[a], screen=screen_now(t, kw), bokeh_=True)
    live_bug(big, t)
    return big


def r_host_cu(t, u, kw, t0):
    fr = kw.get('freeze_at')
    frozen = fr is not None and u > fr
    tt = t0 + fr if frozen else t
    Z = 1.25 * kw.get('zoom', 1.0) * (1 + 0.012 * u)
    cx, cy = 300.0, 395.0
    v = K.V('tvstudio', cx, cy, Z)
    a = host(v, tt, (0.9, 0.0), y=DESK[1] + 40.0, **hands(kw, u))       # a bit lower: the blazer hem hides behind the desk
    kk = kick(t, [(t0 + 0.35, 1.0)]) if kw.get('kick') else (0, 0)
    big, _ = studio(tt, Z, cx, cy, acts=[a], screen=screen_now(tt, kw), fran=False, focus=0.95, dof_k=16, kick=kk, bokeh_=True)
    if frozen:
        fx.vhs(big, t, 0.9)
        im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.text((120, 100), 'PAUSE ||', font=O.pfont(56), fill=(255, 255, 255)); big = np.asarray(im).copy()
    else:
        live_bug(big, t)
    return big


def r_fran_cu(t, u, kw, t0):
    Z = 1.6
    def pre(big, _): big[:] = K.blur(big, 6)
    def f(big, _):
        K.fran(big, 960, 1040, 900, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=-0.3)
        if kw.get('phone'): neon_phone(big, 1240, 360, 230)
    big = K.shot('tvstudio', studio_light, 606.0, 300.0, Z * (1 + 0.01 * u), pre=pre, dof_k=0, fx_=f, t=t, bloom=(200, 30, 0.7))
    live_bug(big, t)
    return big


def r_audience(t, u, kw, t0):
    """the «studio audience»: three cardboard cut-outs on sticks; the third one slowly falls over"""
    def f(big, _):
        for i, (x, skin, shirt) in enumerate(((360, (240, 200, 160), (255, 90, 170)), (960, (200, 150, 110), (80, 220, 255)),
                                              (1560, (250, 220, 190), (255, 200, 80)))):
            y0 = 420 + (i % 2) * 40
            lean = 0 if i < 2 else int(min(1.0, max(0.0, u - 0.9) / 0.4) * 120)
            def R_(a, b, c, d_, col):
                big[max(0, a):max(0, b), max(0, c + lean):max(0, d_ + lean)] = col
            R_(y0 + 230, y0 + 600, x - 150, x + 150, (205, 175, 125))
            R_(y0 + 260, y0 + 600, x - 120, x + 120, shirt)
            R_(y0, y0 + 250, x - 105, x + 105, (205, 175, 125))
            R_(y0 + 20, y0 + 230, x - 85, x + 85, skin)
            R_(y0 + 90, y0 + 118, x - 50, x - 18, (30, 30, 30)); R_(y0 + 90, y0 + 118, x + 18, x + 50, (30, 30, 30))
            R_(y0 + 165, y0 + 180, x - 45, x + 45, (190, 40, 60))
            R_(y0 + 600, OUT_H, x - 12, x + 12, (120, 90, 60))
        O.draw_sticker(big, ST_CRICKETS, t, t0 + 0.3, t0 + 1.6, 960, 240)
    def pre(big, _): big[:] = K.blur(big, 9)
    return K.shot('tvstudio', studio_light, 640.0, 560.0, 1.1, fx_=f, pre=pre, t=t, dof_k=0)


def r_title(t, u, kw, t0):
    big = K.shot('ocean', K.light_sunset, 640.0, 330.0, 0.56 + 0.02 * u, t=t, dof_k=0, rays=dict(src=(960, 420), a=0.3))
    AT.flare(big, 960, 420, 0.8)
    O.overlay(big, TITLE, 0, 250, min(1.0, u / 0.3))
    O.draw_sticker(big, ST_SPECIAL, t, t0 + 0.9, t0 + 9, 960, 840)
    if u < 0.4: fx.vhs(big, t, 1 - u / 0.4)
    return big


def r_screen(t, u, kw, t0):
    s_ = shot_of(t)[1]
    ep, a = kw['ep'], kw['a']
    b = a + (s_[1] - s_[0])
    img = clip_frame(ep, a, b, a + u)
    Z = 1.12 + 0.05 * sm(u / max(1.0, b - a))
    big, v = studio(t, Z, 890.0, 329.0, screen=img, tall=True, fran=False, dof_k=0, motes=False, bloom=(235, 18, 0.3))
    O.overlay(big, TAGS[ep], 40, 960, 1.0)
    return big


def r_reveal_tow(t, u, kw, t0):
    Z = 0.60
    v = K.V('tvstudio', 640.0, 380.0, Z)
    a = host(v, t, (0.9, 0.0))
    ws = 1.8                                     # the truck parked across the back of the studio, in front of the screen
    tow = K.tow_group(v, 700.0, 590.0, t, tilt=0.0, car_u=0.55, vince_kw=dict(expr='cool'), ws=ws, beacon=True)
    rk, dy = FACE('rey', t, (-0.8, 0.0))
    rk.update(point=True, hand_n=(-6.0, 74.0 + 4 * math.sin(t * 8)))
    rey = K.A(C.rey, 520.0, 610.0 + dy * 2, ws * 3 * v.Z * 1.15, t=t, flip=True, **rk)
    big, _ = studio(t, Z, 640.0, 380.0, acts=tow + [rey, a], screen=logo_img(t), fran=True)
    live_bug(big, t)
    return big


def r_adcard(t, u, kw, t0):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    yy = np.linspace(0, 1, OUT_H)[:, None, None]
    big[:] = (np.array((40, 20, 90)) * (1 - yy) + np.array((255, 90, 150)) * yy).astype(np.uint8)
    O.overlay(big, ADCARD, 0, 330, 1.0)
    fx.vhs(big, t, 0.5)
    return big


def ad_bug(big):
    O.overlay(big, AD_BUG, OUT_W - AD_BUG.shape[1] - 30, 20, 1.0)


def r_ad_rey(t, u, kw, t0):
    stage = kw.get('stage', 0)
    if stage == 0:
        rk, dy = FACE('rey', t, (0.6, 0.0))
        rk.update(point=True, hand_n=(26.0, 76.0))
        big, a, v = CM.cu('side', K.light_dusk, C.rey, t, 700.0, 380.0, 1.2, (820, 360 + dy * 8), 11.0, rk)
        chyron(big, "REY'S TOWING", 'WE FIND YOU. • 24/7', 60, 40)
    elif stage == 1:
        Z = 0.95
        v = K.V('side', 680.0, 470.0, Z)
        tow = K.tow_group(v, 760.0, 612.0, t, tilt=11.5, car_u=0.55 - 0.05 * sm(u / 2), vince_kw=dict(expr='outraged'), beacon=True)
        rk, dy = FACE('rey', t, (-0.8, 0.0))
        rk.update(point=True, hand_n=(-8.0, 76.0))
        rey = K.A(C.rey, 540.0, 640.0 + dy * 2, K.WSV * 3 * v.Z * 1.05, t=t, flip=True, **rk)
        sign = K.A(C.sign_free, 455.0, 645.0, K.WSV * 3 * v.Z * 2.2, t=t)
        big = K.shot('side', K.light_dusk, 680.0, 470.0, Z, acts=tow + [rey, sign], t=t, dof_k=10, bokeh_=True)
        O.draw_sticker(big, ST_REY, t, t0 + 0.3, t0 + 4.5, 1400, 200)
    else:
        big = K.shot('side', K.light_dusk, 700.0, 380.0, 0.75, t=t, dof_k=0)
        big[:] = (K.blur(big, 10) * 0.55).astype(np.uint8)
        im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
        crawl = '*PARKING: FREE   *RIDE: $350   *STORAGE: DAILY   *REY NOT LIABLE   *REY NOT SORRY   *FEES MAY APPLY   '
        d.rectangle([0, 880, 1920, 980], fill=(20, 10, 30))
        d.text((1920 - u * 900, 908), crawl * 2, font=O.pfont(34), fill=(255, 214, 80))
        big = np.asarray(im).copy()
        O.overlay(big, REY_LOGO, 0, 170, 1.0)
    ad_bug(big)
    return big


def r_ad_roof(t, u, kw, t0):
    stage = kw.get('stage', 0)
    if stage == 0:
        Z = 1.45 * (1 + 0.02 * u)
        v = K.V('ocean_night', 640.0, 545.0, Z)
        vk = dict(FACE('vince', t, (0.6, -0.5))[0], expr='shock', wet=1.0)
        acts = K.car_group(v, 640.0, 616.0, t, vince_kw=vk)
        big = K.shot('ocean_night', K.light_rain, 640.0, 545.0, Z, acts=acts, fx_=lambda b, _: K.rain(b, t, 1.2), t=t, dof_k=10, bokeh_=True)
        O.draw_sticker(big, ST_RAIN, t, t0 + 0.4, t0 + 9, 1450, 220)
    elif stage == 1:
        Z = 1.45
        v = K.V('ocean', 640.0, 545.0, Z)
        vk = dict(FACE('vince', t, (0.6, -0.5))[0], expr='defeated', sweat=2.0)
        acts = K.car_group(v, 640.0, 616.0, t, vince_kw=vk)
        acts[-1].P['roof'] = 1.0; acts[-1].P['fog'] = 1.0
        big = K.shot('ocean', K.light_sunset, 640.0, 545.0, Z, acts=acts, fx_=lambda b, _: AT.flare(b, 1100, 300, 1.0), t=t, dof_k=10,
                     rays=dict(src=(1100, 300), a=0.35))
    else:
        big = K.shot('ocean', K.light_sunset, 640.0, 300.0, 0.56 + 0.03 * u, t=t, dof_k=0)
        O.overlay(big, ROOFE_LOGO, 0, 260, min(1.0, u / 0.4))
    ad_bug(big)
    return big


def r_caller(t, u, kw, t0):
    ep, a, b = kw['src']
    img = clip_frame(ep, a, b, a + (u % (b - a)))
    Z = 0.68
    cx = 620.0
    v = K.V('tvstudio', cx, 360.0, Z)
    h = host(v, t, (0.9, -0.2), hand_n=(10.0, 74.0), prop_n=C.phone)
    def f(big, v_):
        x0, y0 = v.opt(SCR[0], SCR[1])
        O.overlay(big, CALLERS[kw['who']], int(x0), int(y0) - CALLERS[kw['who']].shape[0] + 10, 1.0)
    big, _ = studio(t, Z, cx, 360.0, acts=[h], screen=img, tall=True, fx_=f, bokeh_=True)
    live_bug(big, t)
    return big


def r_fax(t, u, kw, t0):
    Z = 0.66
    v = K.V('tvstudio', 600.0, 400.0, Z)
    a = host(v, t, (0.3, 0.6))
    def f(big, _):
        x0, y0 = v.opt(440.0, 470.0)
        L = int(min(1.0, u / 1.2) * 1600)
        for i in range(0, L, 10):                                     # the phone bill rolls out of the desk and across the floor
            x = int(x0 + i * 0.9); y = int(y0 + 60 * math.sin(i / 140.0) + i * 0.22)
            if 0 <= x < OUT_W - 70 and 0 <= y < OUT_H - 10:
                big[y:y + 10, x:x + 70] = (248, 246, 236)
                if (i // 10) % 3 == 0: big[y + 4:y + 6, x + 8:x + 56] = (120, 120, 140)
        O.draw_sticker(big, ST_CALLS, t, t0 + 0.4, t0 + 1.6, 1250, 640)
    big, _ = studio(t, Z, 600.0, 400.0, acts=[a], screen=board_img('LIVE CALL-IN: $86'), fx_=f)
    live_bug(big, t)
    return big


def r_bluescreen(t, u, kw, t0):
    lines = [(260, 280, 'PREMIUM REQUIRED', 84, (255, 255, 255)), (300, 450, '$9.99 TO CONTINUE 1986', 52, (255, 214, 80))]
    if kw.get('line') == 'xf2': lines.append((300, 600, '+ $3.50 CONVENIENCE FEE', 52, (255, 110, 140)))
    lines.append((120, 940, 'STOP []   SP 4:20:00', 34, (255, 255, 255)))
    return vhs_card(lines, t, k=0.35 if u > 0.3 else 1.0)


def r_rewind(t, u, kw, t0):
    t_back = max(1.2, 34.0 * (1 - u / 1.6))                              # scrub the tape back to the cold open
    i, s_ = shot_of(t_back)
    big = R[s_[2]](t_back, t_back - s_[0], s_[3], s_[0]).copy()
    fx.vhs(big, t, 1.0)
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.text((120, 100), '<< REWIND', font=O.pfont(64), fill=(255, 255, 255))
    big = np.asarray(im).copy()
    O.draw_sticker(big, ST_REWIND, t, t0 + 0.2, t0 + 9, 960, 820)
    return big


def r_endcard(t, u, kw, t0):
    v = K.V('tvstudio', 640.0, 380.0, 0.6)
    a = host(v, t, (0.9, 0.0), hand_n=(28.0, 92.0), hand_f=(-16.0, 92.0))
    big, _ = studio(t, 0.6, 640.0, 380.0, acts=[a], screen=logo_img(t), bokeh_=True)
    live_bug(big, t)
    return big


R = dict(play=r_play, host_wide=r_host_wide, host_cu=r_host_cu, fran_cu=r_fran_cu, audience=r_audience, title=r_title, screen=r_screen,
         reveal_tow=r_reveal_tow, adcard=r_adcard, ad_rey=r_ad_rey, ad_roof=r_ad_roof, caller=r_caller, fax=r_fax, bluescreen=r_bluescreen,
         rewind=r_rewind, endcard=r_endcard)
assert {s[2] for s in SHOTS} <= set(R), {s[2] for s in SHOTS} - set(R)

TITLE = K.chrome_title(["VINCE VELOUR'S", 'GUIDE TO 1986'], 92, width=OUT_W)
ADCARD = K.chrome_title(['COMMERCIAL', 'BREAK'], 96, width=OUT_W)
ROOFE_LOGO = K.chrome_title(['ROOF-E PREMIUM', "YOU DON'T OWN THE SKY"], 66, width=OUT_W)
REY_LOGO = K.chrome_title(["REY'S TOWING", '1-800-PARK-YOU'], 80, width=OUT_W)
ST_CRICKETS = K.st('*CRICKETS*', fg=(200, 255, 140), size=64)
ST_SPECIAL = K.st('A VERY SPECIAL 1986 SPECIAL', fg=(90, 236, 255), size=44)
ST_REY = K.st('WE FIND YOU.', fg=(255, 170, 60), size=64)
ST_RAIN = K.st('TIRED OF THE SKY?', fg=(90, 236, 255), size=56)
ST_CALLS = K.st('CALL FEES: $86', fg=(255, 110, 140), size=64)
ST_REWIND = K.st('BE KIND. REWIND.', fg=(255, 214, 80), size=60)
AD_BUG = K.st('PAID PROGRAMMING', fg=(255, 255, 255), size=30)
TAGS = {ep: K.st(f'FIELD TAPE • EP {ep[-1]}', fg=(90, 236, 255), size=32) for ep in ('ep01', 'ep02', 'ep03', 'ep04', 'ep05', 'ep06')}
CALLERS = {w: K.st(f'LINE {i + 1}: {w.upper()}', fg=(255, 214, 80), size=34) for i, w in enumerate(('tiffany', 'gary', 'diaz'))}
NO_CAP = {'screen', 'play', 'title', 'adcard', 'rewind', 'audience'}


def render(t):
    i, (t0, t1, name, kw) = shot_of(t)
    big = R[name](t, t - t0, kw, t0)
    if not big.flags.writeable: big = big.copy()
    if name not in NO_CAP: EPI.captions.draw(big, t, 940)
    if TWIST <= t < TWIST + 0.15: O.flash(big, 0.7 * (1 - (t - TWIST) / 0.15))
    if t0 <= t < t0 + 0.1 and name in ('title', 'adcard', 'bluescreen'): O.mosaic(big, int(30 * (1 - (t - t0) / 0.1)) + 1)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
