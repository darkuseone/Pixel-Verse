"""PROMO 01 «Курс» — an ad for the course (stories / reels, owner 30.10.2026). Valera wants his own cartoon but can't draw;
the cat: «А нас кто рисовал? Не художник.» — «А кто?!» — «Claude. С телефона.» (phone insert: the chat with a video card that shows
THIS kitchen — the clue). TWIST: pull back — the whole kitchen is a video on a phone in someone's hand; «Так я… тоже из телефона?!»
Cat: «Курс — в шапке профиля. Справится любой.» Valera: «Двадцать лет в армии! Я — продюсер!» Button: «Даже Валера справился.»
  python3 promo01.py test 1 5 20 | frames t… | all [4] | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import View, view_at, Chars, Light, shadow, OUT_W, OUT_H
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from props import decals as D
from props import rusigns as R
from props import folkgena as G
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG,
              endcard=dict(style='winter', lang='ru', promise='КУРС — В ШАПКЕ ПРОФИЛЯ'), promo='ru')
talk = EPI.talk
CUTS, NAMES = TL.CUTS + [TL.DUR], TL.NAMES                  # per-shot render: python3 promo01.py shots <i|name>
W = PK.build()
KIT = W['kitchen']
ZHEK = PK.q(Image.open(PK.BG / 'zhek.png').convert('RGB'))
NX, NY, NU = 680.0, 412.0, 17.0                       # Nina in the office bathtub (S01 callback), facing left
DESK_PHONE = (70.0, 400.0)
LAMP_Z = (632.0, 30.0)
STAND = (905.0, 660.0, 16.5)                          # Valera standing by the table, facing left (window side)
VALVE_V = (868.0, 660.0, 16.5)                        # Valera bent over the radiator valve
SIT = (985.0, 722.0, 16.5)                            # Valera on the stool with the phone, facing right
PHONE_BASE = (1118.0, 512.0)
PANE = PK.WINDOW_OPEN                                 # (660, 80, 780, 160) open ventilation pane
THERMO = (446.0, 176.0)                               # room thermometer taped to the left window frame (world top-left)

# ---------------------------------------------------------------- local signs (S02: УК «Уют» instead of the ЖЭК)
INK, RED, BLUE, PAPER = (34, 30, 30), (176, 30, 34), (40, 60, 150), (240, 234, 214)
D.attach(ZHEK, [
    (R.plate(150, 40, ['УК «УЮТ»', 'ДИСПЕТЧЕРСКАЯ'], bg=(236, 240, 246), colors=[BLUE, INK], border=(60, 70, 120), weights=[1, 0.55],
             pad=3), 470, 70),
    (R.plate(96, 50, ['ОТОПЛЕНИЕ', 'ПО ГРАФИКУ'], bg=(250, 230, 120), colors=[INK, RED], border=INK, pad=2.5, tilt=-3), 980, 150),
])
D.attach(KIT, [
    (R.plate(64, 30, ['ЖЭК → УК', '«УЮТ»'], bg=PAPER, colors=[INK, BLUE], border=(120, 100, 70), pad=2, tilt=4), 1180, 300),
])
NOTEBOOK = R.plate(46, 20, ['ЖУРНАЛ', 'ЖАЛОБ'], bg=(70, 110, 170), colors=[(250, 240, 200), (250, 240, 200)], border=INK, pad=1.5)


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def light_kit(v, warm=0.0):
    lx, ly = v.opt(*PK.LAMP_K)
    a = (lerp(0.9, 1.02, warm), lerp(0.97, 0.96, warm), lerp(1.12, 0.92, warm))
    return Light(amb=a, keys=[(lx, ly, 1100, (255, 196, 130), 0.75)], rim=(-1, -0.4, (186, 212, 255), 0.4), grad=(1.04, 0.9))


def light_zhek(v):
    lx, ly = v.opt(*LAMP_Z)
    tx, ty = v.opt(800.0, 380.0)
    return Light(amb=(0.98, 1.02, 0.98), keys=[(lx, ly, 1400, (230, 255, 236), 0.4), (tx, ty, 700, (255, 214, 160), 0.5)],
                 rim=(1, -0.3, (196, 220, 255), 0.3), grad=(1.05, 0.92))


# ---------------------------------------------------------------- props in the world
def thermo_img(val):
    """the room thermometer: white board, red column, big «+NN»"""
    sc = 4
    w, h = 28 * sc, 110 * sc
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=(244, 242, 232, 255), outline=INK + (255,), width=6)
    d.rectangle([w // 2 - 7, 10 * sc, w // 2 + 7, 86 * sc], fill=(210, 220, 230, 255), outline=INK + (255,), width=3)
    lvl = int(lerp(84, 14, min(1.0, max(0.0, (val - 0) / 40.0))) * sc)
    d.rectangle([w // 2 - 4, lvl, w // 2 + 4, 86 * sc], fill=(214, 30, 36, 255))
    d.ellipse([w // 2 - 14, 84 * sc, w // 2 + 14, 84 * sc + 28], fill=(214, 30, 36, 255), outline=INK + (255,), width=3)
    for k in range(0, 9):
        y = (14 + k * 8.5) * sc
        d.line([(w // 2 + 10, y), (w // 2 + 22, y)], fill=INK + (255,), width=3)
    txt = f'+{int(round(val))}'
    f = O.pfont(34)
    bb = f.getbbox(txt)
    d.rectangle([4, 96 * sc - 2, w - 5, h - 8], fill=(250, 250, 244, 255))
    d.text(((w - (bb[2] - bb[0])) // 2 - bb[0], 96 * sc + 4), txt, font=f, fill=(200, 20, 30, 255))
    return np.array(im)


_T = {}


def thermo(big, v, val):
    key = int(round(val))
    if key not in _T: _T[key] = thermo_img(key)
    D.blit(big, v, _T[key], THERMO[0], THERMO[1], ws=4)


def pane(big, v, k_open=1.0):
    """the ventilation pane: the background shows it open; k_open < 1 draws the sash swinging shut over the gap"""
    if k_open >= 0.999: return
    x0, y0, x1, y1 = PANE
    w = (x1 - x0) * (1 - k_open)
    if w * 4 < 60: return                                                    # sash still edge-on: nothing to draw
    im = Image.new('RGBA', (int((x1 - x0) * 4), int((y1 - y0) * 4)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    W_, H_ = im.size
    xr = W_ - int(w * 4)
    d.rectangle([xr, 0, W_ - 1, H_ - 1], fill=(104, 88, 72, 255), outline=(40, 32, 28, 255), width=8)       # wooden sash
    d.rectangle([xr + 22, 22, W_ - 23, H_ - 23], fill=(30, 46, 78, 255), outline=(40, 32, 28, 255), width=4)  # dark glass
    gw = W_ - 23 - (xr + 22)
    for i in range(6):                                                                                # frost streaks on the glass
        y = 40 + i * 52
        d.line([(xr + 26, y), (xr + 26 + gw * 0.6, y - 30)], fill=(150, 180, 220, 255), width=5)
    for i in range(10):
        px = xr + 30 + (i * 37) % max(1, gw - 20); py = 30 + (i * 53) % (H_ - 70)
        d.rectangle([px, py, px + 6, py + 6], fill=(220, 236, 255, 255))
    d.rectangle([xr, 0, W_ - 1, 14], fill=(236, 232, 220, 255))                                        # peeling white paint
    D.blit(big, v, np.array(im), x0, y0, ws=4)


def drift(CH, v, k=1.0):
    """snowdrift on the sill under the open pane + icicles on the sash"""
    L = Layer(v.wcam())
    F.ell(L, (720, 377), 64 * k, 13 * k, (236, 244, 255), 0, (255, 255, 255), (190, 206, 230))
    F.ell(L, (690, 372), 34 * k, 12 * k, (236, 244, 255), 0, (255, 255, 255), (190, 206, 230))
    for i, x in enumerate((672, 694, 716, 742, 766)):
        F.cap(L, (x, 160), (x, 160 + (14 + (i % 2) * 12) * k), 2.4, 0.4, (210, 236, 255), (250, 255, 255), (160, 196, 230))
    F.outline(L); CH.add(L)


def handset_cord(CH, v, hand_world):
    L = Layer(v.wcam())
    x, y = PHONE_BASE
    F.ell(L, (x, y), 34, 16, (214, 200, 170), 0, (236, 226, 200), (176, 160, 130))
    F.ell(L, (x, y - 6), 14, 9, (80, 74, 70)); F.ell(L, (x, y - 6), 8, 5, (214, 200, 170))
    pts = [(x - 28, y + 4)]
    for i in range(1, 13):
        k = i / 12
        px = lerp(x - 28, hand_world[0], k); py = lerp(y + 4, hand_world[1], k) + 40 * math.sin(math.pi * k)
        pts.append((px + 3 * math.sin(i * 2.4), py + 3 * math.cos(i * 2.4)))
    for a, b in zip(pts, pts[1:]): F.cap(L, a, b, 1.4, 1.4, (190, 176, 146))
    F.outline(L); CH.add(L)


def breath(big, v, t, hx, hy, k=1.0):
    for i in range(3):
        ph = (t * 0.9 + i / 3) % 1.0
        ox, oy = v.opt(hx + 10 + 30 * ph, hy + 6 - 24 * ph)
        B.puff(big, ox, oy, (14 + 40 * ph) * 3 * v.Z * 0.5, 0.45 * (1 - ph) * k)


def kitchen(v, t, draw=None, warm=0.0, k_open=1.0, snow=46, cat_kw=None, therm=14.0, drift_k=1.0):
    CH, FX = begin(v.Z)
    big = v.bg()
    thermo(big, v, therm)
    pane(big, v, k_open)
    if drift_k > 0: drift(CH, v, drift_k)
    if cat_kw is not None:
        x, y = PK.CAT_K
        F.cat(CH, v.cam(x, y, PK.CAT_K_UNIT), t=t, pose='loaf', **cat_kw)
    if draw: draw(CH, v)
    CH.comp(big, light_kit(v, warm))
    if k_open > 0.5: B.snow_in(FX, v, t, PANE, n=snow, drift=(-90, 220))
    FX.comp(big)
    if warm > 0.2: B.haze(big, v, t, (PK.RAD[0], PK.RAD[1] - 80, PK.RAD[2], PK.RAD[1] + 10), amp=10 * warm)
    fx.vignette(big, 0.28)
    return big


def face_w(x, y, un, flip=False, fwd=1.4, h=21.0):
    return (x - fwd * un) if flip else (x + fwd * un), y - h * un


def v_cold(CH, v, t, pos, pose='stand', expr='angry', flip=True, hand_n=None, prop_n=None, hand_f=None, prop_f=None, **kw):
    x, y, un = pos
    kw.setdefault('cold', 0.55); kw.setdefault('hat', 'ushanka')
    F.valera(CH, v.cam(x, y, un, flip=flip), F.VPOSE[pose] if isinstance(pose, str) else pose, t, mouth('valera', t), expr, 'home',
             hand_n=hand_n, prop_n=prop_n, hand_f=hand_f, prop_f=prop_f, **kw)



# ---------------------------------------------------------------- promo: cosy kitchen (pane shut, +22), Valera in his telnyashka
STAND = (905.0, 660.0, 16.5)                          # Valera by the table, facing left (window side)
SANS = '/home/user/Pixel-Verse/engine/fonts/BigShoulders-Bold.ttf'
_C = {}


def kit(v, t, draw=None, cat_kw=None):
    return kitchen(v, t, draw, warm=0.25, k_open=0.0, therm=22, drift_k=0.0, cat_kw=cat_kw)


def valera(CH, v, t, pose, expr, **kw):
    kw.setdefault('cold', 0.0); kw.setdefault('hat', None)
    v_cold(CH, v, t, STAND, pose, expr, **kw)


def drawing():
    """the sheet with Valera's own «cartoon»: a stick man in an ushanka, a lopsided cat, scribbles, «МУЛЬТ» crossed out"""
    if 'paper' in _C: return _C['paper']
    sc = 4
    w, h = 110 * sc, 82 * sc
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.polygon([(6, 10), (w - 4, 0), (w - 10, h - 6), (0, h - 1)], fill=(246, 242, 228, 255), outline=(34, 30, 30, 255))
    ink = (40, 50, 120, 255)
    cx, cy = 120, 110                                                     # stick man
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=ink, width=6)
    d.rectangle([cx - 34, cy - 44, cx + 34, cy - 22], outline=ink, width=6)                    # ushanka
    d.line([(cx, cy + 26), (cx + 4, cy + 120)], fill=ink, width=6)
    d.line([(cx - 50, cy + 60), (cx + 52, cy + 48)], fill=ink, width=6)
    d.line([(cx + 4, cy + 120), (cx - 34, cy + 186)], fill=ink, width=6); d.line([(cx + 4, cy + 120), (cx + 44, cy + 180)], fill=ink, width=6)
    d.line([(cx - 12, cy + 8), (cx + 14, cy + 6)], fill=ink, width=5)                          # moustache
    kx, ky = 300, 210                                                     # the «cat»: a potato with ears
    d.ellipse([kx - 60, ky - 34, kx + 60, ky + 34], outline=ink, width=6)
    d.polygon([(kx - 40, ky - 26), (kx - 30, ky - 62), (kx - 14, ky - 30)], outline=ink, width=5)
    d.polygon([(kx + 10, ky - 32), (kx + 26, ky - 64), (kx + 36, ky - 26)], outline=ink, width=5)
    d.text((250, 40), 'МУЛЬТ', font=O.pfont(34), fill=ink)
    d.line([(240, 70), (420, 40)], fill=(200, 30, 36, 255), width=7)
    for i in range(5): d.arc([330 + i * 9, 270 - i * 6, 400 + i * 9, 310 - i * 6], 180, 360, fill=ink, width=4)
    _C['paper'] = np.array(im.rotate(8, expand=True, resample=Image.NEAREST))
    return _C['paper']


def r_hook(t, u):
    """«Хочу свой мультфильм! А рисовать — не умею!» — close-up, he shakes his awful drawing at the camera"""
    x, y, un = STAND
    fx_, fy_ = face_w(x, y, un, flip=True, h=20.6)
    v = view_at(KIT, fx_ - 6, fy_ + 60, 1.45 + 0.06 * u, 180, 330)
    big = kit(v, t, lambda CH, v_: valera(CH, v_, t, 'shrug', 'shout'))
    p = drawing()
    O.overlay(big, p, 520 + int(10 * math.sin(t * 18)), 980 + int(8 * math.cos(t * 23)), 1.0)
    if u < 0.25: B.shake(big, t, 8, 30)
    return big


def r_cat(t, u, lid=0.6, expr='deadpan', Z=2.5):
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx, hy, Z + 0.06 * u, 180, 300)
    return kit(v, t, cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=lid, tail=0.4, expr=expr))


def r_vq(t, u):
    x, y, un = STAND
    fx_, fy_ = face_w(x, y, un, flip=True, h=20.6)
    v = view_at(KIT, fx_ - 6, fy_ + 40, 1.9, 180, 320)
    big = kit(v, t, lambda CH, v_: valera(CH, v_, t, 'shrug', 'shock'))
    if u < 0.3: fx.speed_lines(big, t, 0.5)
    return big


# ---------------------------------------------------------------- the phone: a chat with a video card (the clue: it shows THIS kitchen)
PHONE = (150, 230, 930, 1700)                         # full-frame phone body on the insert


def thumb():
    """small still of the hook frame for the video card in the chat"""
    if 'thumb' not in _C:
        _C['thumb'] = np.array(Image.fromarray(r_hook(1.2, 1.2)).resize((216, 384), Image.LANCZOS))
    return _C['thumb']


def bubble(d, x, y, w, lines, me, size=34):
    f = O.pfont(size)
    h = len(lines) * (size + 18) + 30
    fill = (34, 24, 43) if me else (236, 230, 240)
    col = (255, 255, 255) if me else (34, 24, 43)
    x0 = x if not me else x - w
    d.rounded_rectangle([x0, y, x0 + w, y + h], 26, fill=fill)
    for i, s in enumerate(lines): d.text((x0 + 26, y + 18 + i * (size + 18)), s, font=f, fill=col)
    return y + h


def phone_screen(k):
    """chat screen at progress k 0..1 (bubbles appear one by one); returns RGB array of the screen area"""
    x0, y0, x1, y1 = PHONE
    w, h = x1 - x0 - 60, y1 - y0 - 120
    im = Image.new('RGB', (w, h), (250, 248, 252)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w, 110], fill=(240, 234, 244))
    d.text((32, 34), 'ЧАТ · МУЛЬТСТУДИЯ', font=O.pfont(30), fill=(34, 24, 43))
    y = 150
    if k > 0.05: y = bubble(d, w - 30, y, 560, ['Сделай мультик', 'про Валеру и кота'], True) + 30
    if k > 0.35: y = bubble(d, 30, y, 420, ['Готово! 31 сек.'], False) + 20
    if k > 0.6:
        th = thumb()
        d.rounded_rectangle([30, y, 30 + 260, y + 430], 18, fill=(236, 230, 240))
        im.paste(Image.fromarray(th), (52, y + 22))
        d.polygon([(130, y + 180), (130, y + 250), (190, y + 215)], fill=(255, 255, 255))           # play button
        d.text((300, y + 160), 'final.mp4', font=O.pfont(30), fill=(34, 24, 43))
        d.text((300, y + 210), '1080×1920', font=O.pfont(24), fill=(120, 110, 130))
    return np.array(im)


def r_phone(t, u, k0=0.0):
    """«Claude. С телефона.» — insert: the phone fills the frame, the chat fills up"""
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (255, 197, 49)
    import thumb16 as TH
    big[:] = TH.sunburst(OUT_W, OUT_H, (540, 900), [(255, 206, 40), (255, 140, 30), (236, 70, 40)], rays=22, px=8, core_r=360, rot=t * 0.05)
    x0, y0, x1, y1 = PHONE
    im = Image.fromarray(big); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0 - 10, y0 - 10, x1 + 10, y1 + 10], 70, fill=(28, 16, 12))
    d.rounded_rectangle([x0, y0, x1, y1], 62, fill=(34, 34, 40))
    d.rounded_rectangle([540 - 70, y0 + 24, 540 + 70, y0 + 44], 10, fill=(10, 10, 12))
    big = np.array(im)
    scr = phone_screen(min(1.0, k0 + u / 1.6))
    big[y0 + 70:y0 + 70 + scr.shape[0], x0 + 30:x0 + 30 + scr.shape[1]] = scr
    return big


# ---------------------------------------------------------------- TWIST: pull back — the kitchen is a video on a phone in a hand
SKIN, SKIN_SH, INK_H = (240, 186, 150), (206, 146, 116), (28, 16, 12)


def palm(d, cx, top, s):
    """the palm under the phone + the sleeve"""
    d.rounded_rectangle([cx - 250 * s, top - 160 * s, cx + 250 * s, top + 360 * s], int(120 * s), fill=SKIN, outline=INK_H, width=max(4, int(8 * s)))
    d.rectangle([cx - 900, top + 330 * s, cx + 900, OUT_H + 400], fill=(40, 70, 140), outline=INK_H, width=6)               # sleeve


def grip(d, sx, sy, fw, fh, s):
    """thumb over the left edge, three fingers over the right edge, drawn in front of the phone"""
    w = max(4, int(8 * s))
    d.rounded_rectangle([sx - 70 * s, sy + fh * 0.55, sx + 46 * s, sy + fh * 0.55 + 230 * s], int(46 * s), fill=SKIN, outline=INK_H, width=w)
    for i in range(3):
        yy = sy + fh * 0.5 + i * 92 * s
        d.rounded_rectangle([sx + fw - 40 * s, yy, sx + fw + 64 * s, yy + 80 * s], int(36 * s), fill=SKIN_SH, outline=INK_H, width=w)


def r_reveal(t, u):
    """«Так я… тоже из телефона?!» — the kitchen shot shrinks into a phone screen held by a hand"""
    x, y, un = STAND
    fx_, fy_ = face_w(x, y, un, flip=True, h=20.6)
    v = view_at(KIT, fx_ - 6, fy_ + 60, 1.45, 180, 330)
    inner = kit(v, t, lambda CH, v_: valera(CH, v_, t, 'shrug', 'shock', look=-0.4))
    k = sm(u / 0.7)
    import thumb16 as TH
    big = TH.sunburst(OUT_W, OUT_H, (540, 860), [(255, 206, 40), (255, 140, 30), (236, 70, 40)], rays=22, px=8, core_r=380, rot=-t * 0.05)
    fw, fh = lerp(OUT_W, 540, k), lerp(OUT_H, 960, k)
    sx, sy = lerp(0, 540 - 270, k), lerp(0, 300, k)
    im = Image.fromarray(big); d = ImageDraw.Draw(im)
    b = 34 * k
    if k > 0.02: palm(d, 540, sy + fh + 40 * k, k)
    d.rounded_rectangle([sx - b, sy - b * 1.6, sx + fw + b, sy + fh + b * 1.6], int(10 + 60 * k), fill=(34, 34, 40), outline=(28, 16, 12), width=6)
    im.paste(Image.fromarray(inner).resize((max(1, int(fw)), max(1, int(fh))), Image.NEAREST if k > 0.5 else Image.BILINEAR), (int(sx), int(sy)))
    if k > 0.02: grip(d, sx - b, sy, fw + 2 * b, fh, k)
    big = np.array(im)
    if 0.0 < u < 0.6: fx.speed_lines(big, t, 0.5)
    return big


def r_proud(t, u):
    """«Двадцать лет в армии! Я — продюсер!» — salute, wide, the cat unimpressed on the radiator"""
    x, y, un = STAND
    fx_, fy_ = face_w(x, y, un, flip=True, h=20.6)
    v = view_at(KIT, fx_ - 40, fy_ + 110, 1.15 + 0.05 * u, 180, 330)
    big = kit(v, t, lambda CH, v_: valera(CH, v_, t, 'salute', 'proud'), cat_kw=dict(lid=0.85, tail=0.2, expr='deadpan'))
    if u < 0.25: B.shake(big, t, 6, 30)
    return big


SHOT = dict(hook=r_hook, cat1=lambda t, u: r_cat(t, u, 0.6, 'smug', 2.5), v_q=r_vq, phone=r_phone,
            phone2=lambda t, u: r_phone(t, u, (TL.T0['phone2'] - TL.T0['phone']) / 1.6), reveal=r_reveal,
            cat_ad=lambda t, u: r_cat(t, u, 0.55, 'smug', 2.2), v_proud=r_proud,
            button=lambda t, u: r_cat(t, u, 0.75, 'deadpan', 2.9), button2=lambda t, u: r_cat(t, u + 2.3, 0.85, 'deadpan', 2.9))


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


F0 = TL.T0


def arrow_sticker():
    """«КУРС — В ШАПКЕ ПРОФИЛЯ» with a big pixel arrow up"""
    if 'arr' not in _C:
        a, b = O.sticker('КУРС —', fg=(255, 236, 120), size=64), O.sticker('В ШАПКЕ ПРОФИЛЯ', fg=(255, 236, 120), size=64)
        w = max(a.shape[1], b.shape[1])
        s = np.zeros((a.shape[0] + b.shape[0] - 10, w, 4), np.uint8)
        s[:a.shape[0], (w - a.shape[1]) // 2:(w - a.shape[1]) // 2 + a.shape[1]] = a
        bb = s[a.shape[0] - 10:, (w - b.shape[1]) // 2:(w - b.shape[1]) // 2 + b.shape[1]]
        m = b[..., 3:4] > 0; bb[:] = np.where(m, b, bb)
        out = np.zeros((s.shape[0] + 150, w, 4), np.uint8)
        im = Image.new('RGBA', (w, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        c = w // 2
        d.polygon([(c - 70, 80), (c, 0), (c + 70, 80)], fill=(255, 200, 50, 255), outline=(28, 16, 12, 255))
        d.rectangle([c - 28, 78, c + 28, 146], fill=(255, 200, 50, 255), outline=(28, 16, 12, 255), width=5)
        out[:150] = np.array(im); out[150:] = s
        _C['arr'] = out
    return _C['arr']


SHOW = K.Show(EPI, 1, ['СВОЙ МУЛЬТИК?!'], hook_t=(0.06, 2.6), hook_y=150,
              stickers=[(O.sticker('НЕ ХУДОЖНИК', fg=(255, 150, 120), size=62), F0['cat1'] + 1.6, F0['v_q'], 540, 420),
                        (O.sticker('С ТЕЛЕФОНА', fg=(150, 220, 255), size=70), F0['phone'] + 0.9, F0['phone2'] + 0.6, 540, 1790),
                        (O.sticker('МЫ — МУЛЬТИК?!', fg=(255, 236, 120), size=58), TL.TWIST + 0.35, F0['cat_ad'], 540, 1730),
                        (arrow_sticker(), F0['cat_ad'] + 0.3, F0['button'] + 0.8, 540, 500),
                        (O.sticker('ПРОДЮСЕР', fg=(150, 230, 140), size=70), F0['v_proud'] + 1.3, F0['button'], 540, 1180)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['phone'], F0['cat_ad']],
              cap_y={'hook': 1500, 'phone': 1560, 'phone2': 1560, 'reveal': 1600, 'v_proud': 1500}, cap_default=1330)
SHOW.badge = O.make_badge('PIXEL VERSE • КУРС')


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
