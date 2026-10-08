"""«Мазутыч» shared shot helpers for episodes E02+ (E01 keeps its own copies in ep01.py).
  from props.mazshots import Kit
  KIT = Kit(EPI)            # talk/mouth from the episode, everything else is shared
Coordinates: world px of the xAI backgrounds (1280x720); output 1080x1920."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from props import mazpix as MX
from props import mazcast as MC
from props import mazkit as K
from props import bytfx as B

INK = MX.INK
SP = 4.2                                           # Мазутыч & people: output px per sprite px at Z = 1
CAR = 6.0
TRK = 7.0


def y_far(x): return 548.0 + 0.0625 * x
def y_near(x): return 590.0 + 0.0625 * x
def y_sh(x): return 618.0 + 0.0625 * x


def A(fn, wx, wy, s, flip=False, pin=None, **kw):
    return MX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, **kw)


def wpt(v, ox, oy):
    """output px -> world px"""
    return v.X0 + ox / (3 * v.Z), v.Y0 + (oy / 3 - v.oy) / v.Z


def aout(act, v, name):
    """output px of a named sprite anchor of an actor that has been drawn"""
    sp = act.last
    px, py = sp.anchors[name]
    ox, oy = v.opt(act.wx, act.wy)
    sc = act.scale(v)
    if act.pin:
        qx, qy = sp.anchors[act.pin]
        ox -= (-qx if act.flip else qx) * sc; oy += qy * sc
    return ox + (-px if act.flip else px) * sc, oy - py * sc


def rope(big, a, b, sag=40, w=10, col=(206, 172, 110)):
    (x0, y0), (x1, y1) = a, b
    n = int(max(abs(x1 - x0), abs(y1 - y0)) / 4) + 2
    pts = [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n + sag * 4 * (i / n) * (1 - i / n)) for i in range(n + 1)]
    for pad, colf in ((3, lambda i: INK), (0, lambda i: col if (i // 3) % 2 else (176, 140, 84))):
        for i, (x, y) in enumerate(pts):
            xa, ya = int(x - w / 2) - pad, int(y - w / 2) - pad
            xb, yb = xa + w + 2 * pad, ya + w + 2 * pad
            if xb > 0 and yb > 0 and xa < OUT_W and ya < OUT_H:
                big[max(0, ya):min(OUT_H, yb), max(0, xa):min(OUT_W, xb)] = colf(i)


def dof(big, r=6):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


def sparks(big, ox, oy, t, n=18, spread=220, back=True):
    r = np.random.default_rng(int(t * 30))
    for i in range(n):
        d = r.random() * spread; a = r.random()
        px, py = int(ox - (20 + d) * (1 if back else -1)), int(oy - 6 - a * 60 + d * 0.15)
        if 0 <= px < OUT_W - 12 and 0 <= py < OUT_H - 12: big[py:py + 12, px:px + 12] = (255, 220, 120) if i % 3 else (255, 140, 60)


def zzz(big, x, y, t, col=(200, 230, 255)):
    for i in range(3):
        ph = (t * 0.8 + i / 3) % 1.0
        img = O.pfont(int(40 + 40 * ph))
        im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.text((x + 60 * ph, y - 200 * ph), 'Z', font=img, fill=col, stroke_width=4, stroke_fill=INK)
        big[:] = np.array(im)


def paper(big, cx, cy, lines, w=520, h=300, rot=0.0, stamp=None, stamp_k=1.0, col=(246, 240, 222), sizes=None):
    """a paper slip insert drawn in screen space (coupon, notice): lines of pixel text, optional red stamp"""
    im = Image.new('RGBA', (w, h), col + (255,)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([6, 6, w - 7, h - 7], outline=(150, 130, 100), width=4)
    for k in range(0, w, 24): d.line([(k, h - 18), (k + 12, h - 18)], fill=(180, 160, 130), width=2)   # perforation
    y = 28
    for i, ln in enumerate(lines):
        sz = (sizes or [])[i] if sizes and i < len(sizes) else 28
        f = O.pfont(sz); bb = f.getbbox(ln)
        d.text(((w - (bb[2] - bb[0])) // 2 - bb[0], y - bb[1]), ln, font=f, fill=(40, 34, 30))
        y += sz + 20
    if stamp and stamp_k > 0:
        s_ = int(64 * (1.6 - 0.6 * min(1.0, stamp_k)))
        f = O.pfont(s_); bb = f.getbbox(stamp)
        st = Image.new('RGBA', (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); sd.fontmode = '1'
        sd.rectangle([2, 2, st.size[0] - 3, st.size[1] - 3], outline=(200, 30, 40, 230), width=6)
        sd.text((20 - bb[0], 20 - bb[1]), stamp, font=f, fill=(200, 30, 40, 230))
        st = st.rotate(14, resample=Image.NEAREST, expand=True)
        im.alpha_composite(st, ((w - st.size[0]) // 2, (h - st.size[1]) // 2))
    if rot: im = im.rotate(rot, resample=Image.NEAREST, expand=True)
    a = np.array(im)
    sh = np.zeros_like(a); sh[..., 3] = (a[..., 3] > 0) * 140
    O.overlay(big, sh, int(cx - a.shape[1] / 2) + 16, int(cy - a.shape[0] / 2) + 20, 1.0)
    O.overlay(big, a, int(cx - a.shape[1] / 2), int(cy - a.shape[0] / 2), 1.0)


def night(big, k=1.0, moon=None):
    """dusk -> night grade (k 0..1), optional moon at an output point"""
    if k <= 0: return
    f = np.array([1 - 0.62 * k, 1 - 0.55 * k, 1 - 0.30 * k], np.float32)
    big[:] = np.clip(big * f + np.array([4, 6, 22]) * k, 0, 255).astype(np.uint8)
    if moon and k > 0.4:
        x, y = moon
        fx.glow(big, x, y, 260, (200, 220, 255), 0.35 * k)
        yy, xx = np.ogrid[-70:71, -70:71]
        m = (xx * xx + yy * yy) <= 70 * 70
        reg = big[y - 70:y + 71, x - 70:x + 71]
        if reg.shape[:2] == m.shape:
            reg[m] = (236, 236, 214); reg[m & ((xx + 20) ** 2 + (yy - 10) ** 2 < 300)] = (210, 210, 190)


def digital_clock(big, txt, cx=540, cy=300, size=150, col=(255, 70, 60)):
    f = O.pfont(size); bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + 80, bb[3] - bb[1] + 80
    im = Image.new('RGBA', (w, h), (14, 12, 16, 235)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], outline=INK, width=8)
    d.text((40 - bb[0], 40 - bb[1]), txt, font=f, fill=col)
    O.overlay(big, np.array(im), int(cx - w / 2), int(cy - h / 2), 1.0)


class Kit:
    def __init__(s, epi):
        s.epi = epi
        s.HW = K.world('highway_azs')
        s.WIN = K.world('azs_window')
        s.GATE = K.world('refinery_gate')

    def mouth(s, who, t, k=1.8):
        return min(1.0, s.epi.talk(who, t) * k)

    def speaking(s, who, t):
        """1 while a line of `who` is playing (pauses between words included), else 0"""
        return 1.0 if any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in s.epi.voice) else 0.0

    def wheel_k(s, t):
        """how hard the wheel «talks» right now: voice envelope, never below 0.5 while its line plays"""
        return max(s.mouth('wheel', t, 1.6), 0.5 * s.speaking('wheel', t))

    def maz_act(s, t, x, y, Z, sz=None, **kw):
        kw.setdefault('t', t)
        kw.setdefault('mouth_', s.mouth('maz', t))
        kw.setdefault('wheel_talk', s.wheel_k(t))
        return A(MC.maz, x, y, sz or SP * Z, **kw)

    def queue_acts(s, t, Z, honk=0.0, xs=None):
        q = [(450, 'lada', 0), (570, 'buh', 1), (690, 'lada', 2), (800, 'lada', 3), (905, 'lada', 5)] if xs is None else xs
        acts = []
        for i, (x, kind, c) in enumerate(q):
            b = (abs(math.sin(t * 30 + i)) * 1.5 if honk > 0 else 0.0)
            y = y_far(x) - b
            if kind == 'lada':
                acts.append(A(MC.lada, x, y, CAR * Z, col=MC.CAR_COLS[c], rust=i + 1))
            else:
                acts.append(A(MC.buhanka, x, y, CAR * Z))
        return acts

    def cu(s, fn, who, t, u, world, cx, cy, Z=1.45, sz=16.0, head=(540, 960), pan=0.0, bob=0.0, light=K.light_hw, blur=0,
           flare=(664, 205), extra_fx=None, pre_fx=None, wind=0.0, flip=False, acts_before=(), **kw):
        """close-up of any hero: head pinned at an output point; background zoomed less (CU_BG rule) and optionally soft"""
        v0 = view_at(world, cx + pan * u, cy, Z, 180, 320)
        hx, hy = wpt(v0, head[0], head[1] + bob * math.sin(t * 8.0))
        kw.setdefault('mouth_', s.mouth(who, t, 1.6))
        if fn is MC.maz: kw.setdefault('wind', wind)
        if fn is MC.maz: kw.setdefault('wheel_talk', s.wheel_k(t))
        a = A(fn, hx, hy, sz, pin='head', t=t, flip=flip, **kw)
        def pre(big, v):
            if flare: K.flare(big, v, t, flare[0], flare[1], 1.0, 0.6)
            if pre_fx: pre_fx(big, v)
            if blur: big[:] = dof(big, blur)
        def f(big, v):
            if extra_fx: extra_fx(big, v, a)
        big = K.shot(world, light, cx + pan * u, cy, Z, acts=list(acts_before) + [a], pre=pre, fx_=f, sx=180, sy=320)
        if wind: K.wind_lines(big, t, 0.4 * wind)
        return big

    def cu_maz(s, t, u, world=None, cx=420.0, cy=330.0, **kw):
        return s.cu(MC.maz, 'maz', t, u, s.HW if world is None else world, cx, cy, **kw)

    def zoya(s, t, u, who='zoya', mega=False, Z0=1.45, push=0.05, gum=0.0, expr='bored', look=(0.3, 0.0), pose='desk', dark=0.0, lights=True,
             extra=None):
        """Зоя behind the kiosk glass (glass streaks + speaking grille restored in front of her); dark: night grade"""
        Z = Z0 + push * u
        sz = 4.0 * 3 * Z
        acts = [A(MC.zoya, 600.0, 470.0, sz, t=t, mega=mega, mouth_=s.mouth(who, t, 1.7), gum=gum, expr=expr, look=look, pose=pose)] if lights else []
        big = K.shot(s.WIN, K.light_win, 618.0, 300.0, Z, acts=acts, sx=180, sy=300)
        v = view_at(s.WIN, 618.0, 300.0, Z, 180, 300)
        xs, ys = v.grid()
        orig = v.bg()
        m = ((ys[:, None] >= 450) & (ys[:, None] <= 510)) & ((xs[None, :] >= 556) & (xs[None, :] <= 708))
        big[m] = orig[m]
        gl = ((ys[:, None] >= 92) & (ys[:, None] <= 520)) & ((xs[None, :] >= 226) & (xs[None, :] <= 1012))
        yy, xx = np.mgrid[0:OUT_H, 0:OUT_W]
        if not lights:
            big[gl] = (big[gl] * 0.25).astype(np.uint8)
        streak = (((xx + yy * 0.8 + 140) % 620) < 46) & gl
        big[streak] = (big[streak] * 0.72 + np.array([255, 236, 210]) * 0.28).astype(np.uint8)
        if extra: extra(big, v)
        if dark: night(big, dark)
        return big

    def shutter(s, big, v, k):
        """iron roller shutter coming down over the kiosk glass (k 0..1), with a painted notice"""
        if k <= 0: return
        x0, x1, y0, y1 = 220, 1018, 86, 526
        yb = y0 + (y1 - y0) * k
        img = np.zeros((int(y1 - y0), x1 - x0, 4), np.uint8)
        hh = int(yb - y0)
        if hh <= 0: return
        rows = np.arange(hh)
        img[:hh, :, :3] = np.where(((rows // 10) % 2 == 0)[:, None, None], np.array([150, 150, 156]), np.array([120, 122, 130]))
        img[:hh, :, 3] = 255
        img[max(0, hh - 14):hh, :, :3] = (70, 70, 76)
        if k > 0.95:
            im = Image.fromarray(img); d = ImageDraw.Draw(im); d.fontmode = '1'
            W_ = x1 - x0
            for txt, sz, yy, col in (('ЗАКРЫТО', 26, 150, (200, 40, 40)), ('ТАЛОНЫ —', 12, 205, (40, 40, 46)), ('ПО ЧЁТНЫМ', 12, 225, (40, 40, 46)),
                                     ('ЧЕТВЕРГ —', 12, 260, (40, 40, 46)), ('ЧЁТНЫЙ', 12, 280, (40, 40, 46))):
                f = O.pfont(sz); bb = f.getbbox(txt)
                d.text((398 - (bb[2] - bb[0]) // 2 - bb[0], yy - bb[1]), txt, font=f, fill=col)
            img = np.array(im)
        ST.blit_world(big, v, img, x0, y0)


def lcd_talk(big, x0, y0, x1, y1, t, k, col=(90, 230, 255)):
    """the wheel's display insert while it speaks: an equalizer of bars jumping with the voice (k 0..1)"""
    if k <= 0.05: return
    n = 9
    w = (x1 - x0) // n
    for i in range(n):
        h = int((y1 - y0) * min(1.0, k * (0.35 + 0.65 * abs(math.sin(t * 17 + i * 1.7)))))
        cx = x0 + i * w + w // 4
        cy = (y0 + y1) // 2
        big[cy - h // 2:cy + h // 2, cx:cx + w // 2] = col
