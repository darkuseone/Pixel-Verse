"""Agent Dibs (v2) scene kit: cutaways drawn with the pixel-sprite cast (props/dibscast.py).
deb_frame / deb_window — Deb at her desk (full frame / picture-in-picture video call);
window_cut — moonlit brick wall, a nosy lady snaps the curtains open and leans out (binoculars / popcorn).
Everything else (shot(), lights, Show, digits) stays in props/chikit.py."""
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import Light, view_at, OUT_W, OUT_H
import overlays as O
import fx
from props import bytfx as B
from props import chikit as K
from props import dibspix as DX
from props import dibscast as DC

DEB_HEAD = (500.0, 463.0)               # world point of Deb's face in the Field Office background (desk edge at her waist)
DESK_Y = K.DESK_Y


def deb_frame(t, expr='smile', mouth=0.0, Z=2.0, dx=0.0, dy=0.0, zoom=0.05, u=0.0, s=12.5, hands=None, props=None, pose='hold',
              lean=0.0, sweat=0.0, shake_=0.0, fx_=None, look=0.0):
    """full 1080x1920 cutaway of Deb behind her desk (knitting by default); lower body hidden by redrawing the desk from the background"""
    Zt = Z + zoom * u
    W_ = K.world('field_office')
    hx, hy = DEB_HEAD
    v = view_at(W_, hx + 6.0 + dx, hy + 40.0 + dy, Zt, 180, 262)
    big = v.bg(); orig = big.copy()
    a = DX.Act(DC.deb, hx, hy, s_=s * Zt / Z, pin='head', pose=pose, t=t, mouth_=mouth, expr=expr, hands=hands, props=props,
               sweat=sweat, lean=lean, look=look)
    a(big, v, K.light_office(v))
    xs, ys = v.grid()
    m = (ys[:, None] > DESK_Y) & ((xs >= 20) & (xs <= 955))[None, :]
    big[m] = orig[m]
    if fx_: fx_(big, v)
    fx.vignette(big, 0.26)
    if shake_: B.shake(big, t, shake_, 35)
    return big


def deb_window(big, t, expr='smile', mouth=0.0, box=(660, 520, 1040, 900), label='DEB: CONTROL', **kw):
    """picture-in-picture video call window with Deb (cyan frame, blinking REC dot)"""
    fr = deb_frame(t, expr, mouth, Z=2.0, **kw)
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    crop = fr[260:260 + 1000, 40:1040]
    a = np.array(Image.fromarray(crop).resize((w, h), Image.NEAREST))
    big[y0 - 10:y1 + 10, x0 - 10:x1 + 10] = (60, 220, 250)
    big[y0 - 4:y1 + 4, x0 - 4:x1 + 4] = (10, 20, 40)
    big[y0:y1, x0:x1] = a
    d = Image.fromarray(big[y1 + 10:y1 + 70, x0 - 10:x1 + 10]); dd = ImageDraw.Draw(d)
    dd.rectangle([0, 0, d.size[0], 60], fill=(10, 20, 40))
    dd.text((14, 14), label, font=O.pfont(26), fill=(120, 240, 255))
    big[y1 + 10:y1 + 70, x0 - 10:x1 + 10] = np.array(d)
    if int(t * 2) % 2 == 0: big[y0 + 14:y0 + 34, x1 - 40:x1 - 20] = (240, 50, 60)


LADY_HANDS = dict(binoculars=dict(L=(-1.0, 55.5), R=(5.0, 55.5)), popcorn=dict(L=(-3.0, 50.0), R=(7.0, 50.0)),
                  rolling_pin=dict(L=(-8.0, 48.0), R=(14.0, 64.0)), casserole=dict(L=(-6.0, 50.0), R=(12.0, 60.0)),
                  pan=dict(L=(-8.0, 48.0), R=(14.0, 64.0)), mop=dict(L=(-8.0, 48.0), R=(12.0, 58.0)))


def window_cut(t, u, who='mrs_w', open_t=0.12, prop='binoculars', expr='deadpan', flip=False, shift=(0, 0), robe_cur=(214, 70, 96), s=13.0,
               hires=None):
    """full-frame cutaway: moonlit brick wall, lit window, curtains snap open at open_t and a lady leans out (binoculars / popcorn)"""
    wall = (K.brick_bg() * np.array([0.36, 0.42, 0.62])).astype(np.uint8)
    big = wall.copy()
    x0, y0, x1, y1 = 150 + shift[0], 330 + shift[1], 930 + shift[0], 1250 + shift[1]
    big[y0 - 70:y0, x0 - 90:x1 + 90] = (226, 232, 240)                                              # snow on the lintel
    big[y0 - 22:y1 + 22, x0 - 22:x1 + 22] = (30, 26, 30)                                            # frame
    big[y0:y1, x0:x1] = (255, 206, 120)                                                              # warm light
    k = min(1.0, max(0.0, (t - open_t) / 0.10))
    cw = int((x1 - x0) / 2 * (1.0 - 0.84 * k))
    big[y0:y1, x0:x0 + cw] = robe_cur; big[y0:y1, x1 - cw:x1] = robe_cur
    for q in range(0, max(cw, 1), 28):
        big[y0:y1, x0 + q:x0 + q + 6] = (170, 40, 68); big[y0:y1, x1 - q - 6:x1 - q] = (170, 40, 68)
    base_below = big.copy()
    if k > 0.02:
        sp = DX.draw(DC.lady, s, flip=flip, hires=hires, who=who, pose='hold', t=t, mouth_=0.0, expr=expr, look=0.0, hands=LADY_HANDS.get(prop),
                     props={'R': prop}, clip_h=None)                                        # 2x canvas at close-up scale
        hx, hy = sp.anchors['head']
        cx, cy = (x0 + x1) / 2 + (40 if flip else -40), (y0 + y1) / 2 - 60 + 60 * (1 - k)
        ox = cx + (hx if flip else -hx) * s
        DX.blit(big, sp, ox, cy + hy * s, s, Light(amb=(1.08, 1.0, 0.92), rim=(1, -0.3, (255, 230, 180), 0.3)), flip)
        big[y1:] = base_below[y1:]                                                                   # nothing below the sill
    big[y1:y1 + 50, x0 - 70:x1 + 70] = (210, 218, 232)                                              # sill with snow
    big[y0 - 40:y0 - 14, x0 - 22:x1 + 22] = (120, 90, 60)                                           # curtain rod
    fx.vignette(big, 0.3)
    return big
