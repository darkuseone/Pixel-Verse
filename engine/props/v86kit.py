"""«STILL 1986» episode kit: speaker colours, worlds (xAI backgrounds + v86decor) with depth maps (depth25), real-scale groups
(car = 2.4 hero heights, tow truck = 6.5 m; owner rule 12.11.2026), sunset / night / dawn lights, FRAN the talking neon flamingo
(drawn at output resolution, tubes flash with her syllables), the chrome 80s title, the VHS-label badge and cover plate, the
ParkMeMaybe phone screen, the fine-print insert, the 2.5D shot wrapper (parallax, depth of field, bloom, motes, bokeh, juice grade).
Coordinates: world px of the 1280x720 backgrounds; output 1080x1920. WSV = world px per hero sprite px on the street plane."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paths as P
import stage as ST
from stage import Light, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
import atmos as AT
import depth25 as D25
from props import v86pix as VX
from props import v86cast as C
from props import v86decor as DEC

SLUG = 'still-1986'
COL = dict(vince=(80, 235, 255), fran=(255, 110, 200), rey=(255, 170, 60), tiffany=(200, 255, 140), diaz=(120, 200, 255),
           gary=(255, 230, 90), roofe=(230, 240, 255))
WS = dict(ocean=1.34, ocean_night=1.34, side=1.34, club=2.2, disco=2.9, marina=2.2, bay=1.9, mall=2.7, studio=3.2)
WSV = 1.34                       # world px per hero sprite px on the street (door of the pink hotel = 75 px = 2.3 m; hero 1.8 m = 110 px)
PINK, CYAN, INK = (255, 70, 180), (60, 230, 255), VX.INK


def A(fn, wx, wy, s, flip=False, pin=None, rim=(VX.SUN, VX.CYAN), **kw):
    return VX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, rim=rim, **kw)


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


# ---------------------------------------------------------------- worlds + depth
_W = {}


def world(name):
    if name not in _W:
        Wd = ST.ai_world(P.series(SLUG) / 'bg' / f'{name}.png', colors=128)
        DEC.dress(name, Wd)
        _W[name] = Wd
    return _W[name]


def depth(name):
    return D25.of(world(name), P.series(SLUG) / 'bg' / f'{name}.png')


# ---------------------------------------------------------------- lights (heroes sit in the painted light)
def _keys(v, lamps):
    return [(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in lamps]


def light_sunset(v):
    return Light(amb=(1.06, 0.97, 0.98), keys=_keys(v, [(640, 160, 900, (255, 170, 110), 0.22)]),
                 grad=(1.04, 0.94))


def light_night(v):
    return Light(amb=(0.80, 0.76, 0.98), keys=_keys(v, [(620, 300, 380, (255, 70, 190), 0.45), (1080, 260, 420, (70, 220, 255), 0.35),
                                                         (840, 400, 260, (255, 210, 120), 0.30)]), grad=(1.0, 0.86))


def light_dusk(v):
    return Light(amb=(0.92, 0.86, 1.02), keys=_keys(v, [(1060, 260, 420, (255, 80, 170), 0.40), (1010, 340, 260, (255, 210, 130), 0.35),
                                                         (420, 330, 600, (255, 150, 110), 0.25)]), grad=(1.02, 0.88))


# ---------------------------------------------------------------- real-scale groups
def car_group(v, wx, wy, t, vince_kw=None, flip=False, speed=0.0, lights=False, rot=0.0, z=1.0, ws=None):
    """Vince's car with Vince seated: [car back, Vince, car front]. (wx, wy) = world px of the car's ground point under its
    centre; z = depth scale (1 = street plane). rot = degrees CCW (on the tow ramp) around the ground point"""
    ws = ws or WSV
    S = ws * 3 * v.Z * z                                    # output px per hero sprite px
    Sc = S * C.CAR_K
    d = -1 if flip else 1
    hx, hy = -6.0 * C.CAR_K + 1.6, 22.0 * C.CAR_K - 34.0     # hero feet anchor relative to the car origin (hero px): hips on the seat
    ox_, oy_ = hx * d, hy                                    # the rotation is done inside the sprite around the car origin (pivot)
    k = ws * z
    vk = dict(vince_kw or {}); vk.setdefault('legs', False)
    vk.setdefault('hand_n', (24.0, 46.0)); vk.setdefault('hand_f', (-12.0, 37.0))
    acts = [A(C.car, wx, wy, Sc, flip=flip, part='back', t=t, rot=rot),
            A(C.vince, wx + ox_ * k, wy - oy_ * k, S, flip=flip, t=t, rot=rot, pivot=(-hx, -hy), **vk),
            A(C.car, wx, wy, Sc, flip=flip, part='front', t=t, speed=speed, lights=lights, rot=rot)]
    return acts


def tow_group(v, wx, wy, t, tilt=0.0, car_u=None, vince_kw=None, rey_kw=None, beacon=True, chains=False, z=1.0, spin=0.0, ws=None):
    """Rey's tow truck at real size (~6.5 m): bed (+ the car on its deck at position car_u 0..1) + cab in front (+x).
    (wx, wy) = ground point under the bed's chassis centre"""
    ws = ws or WSV
    S = ws * 3 * v.Z * z; St = S * C.TOW_K; k = ws * z * C.TOW_K
    acts = [A(C.tow_bed, wx, wy, St, t=t, tilt=tilt, chains=chains, spin=spin)]
    if car_u is not None:
        px, py = C.deck_point(car_u, tilt)
        acts += car_group(v, wx + px * k, wy - py * k, t, vince_kw=vince_kw, rot=tilt, z=z, ws=ws)
    acts.append(A(C.tow_cab, wx + 112.0 * k, wy, St, t=t, beacon=beacon, rey_kw=rey_kw))
    return acts


# ---------------------------------------------------------------- FRAN: the talking neon flamingo
def _fran_paths(talk, lid, look):
    body = [(30 + 15 * math.cos(a), 44 + 9 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40)]
    tail = [(17, 41), (8, 35), (13, 44), (16, 46)]
    wing = [(23, 41), (29, 38), (37, 39), (34, 45), (27, 47)]
    neck = [(41, 39), (45, 31), (44, 24), (40, 18), (41, 12)]
    head = [(45 + 4.2 * math.cos(a), 8.5 + 4.2 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 22)]
    ang = math.radians(8 + 28 * talk)
    lower = [(49, 10), (49 + 6.4 * math.cos(ang), 10 + 6.4 * math.sin(ang))]
    upper = [(49, 7.4), (55, 9.0), (56.2, 12.6)]
    legs = [[(32, 53), (32, 79), (38, 79)], [(28, 53), (24, 63), (31.5, 65)]]
    return dict(pink=[body, tail, wing, neck, head], cyan=[upper, lower] + legs, eye=(46.2 + look * 0.8, 7.4), lid=lid)


def fran(big, x, y, h, t, talk=0.0, on=1.0, lid=0.55, look=0.0, q=None, glow=1.0):
    """FRAN at output (x, y) = bottom centre of the sign, h = sign height in output px. talk 0..1 (her mouth envelope) opens the
    beak and pulses the tubes; on 0..1 = power (flicker on). Pixel size q (default ~ the world pixel)."""
    u = h / 82.0
    q = q or max(3, int(round(u * 0.8)))
    s = u / q                                                       # low-res px per design unit
    Wl, Hl = int(70 * s) + 4, int(84 * s) + 4
    pa = _fran_paths(talk, lid, look)
    lvl = on * (0.86 + 0.14 * math.sin(t * 37) * math.sin(t * 13)) * (1 + 0.35 * talk)
    w = max(1, int(round(2.3 * s)))

    def layer(paths, closed_idx=(), width=w):
        im = Image.new('L', (Wl, Hl), 0); d = ImageDraw.Draw(im)
        for i, pts in enumerate(paths):
            pp = [(px * s + 2, py * s + 2) for px, py in pts]
            if i in closed_idx: pp = pp + [pp[0]]
            d.line(pp, fill=255, width=width, joint='curve')
            for p_ in (pp[0], pp[-1]): d.ellipse([p_[0] - width / 2, p_[1] - width / 2, p_[0] + width / 2, p_[1] + width / 2], fill=255)
        return np.array(im) > 0
    mp = layer(pa['pink'], closed_idx=(0, 4)); mc = layer(pa['cyan'])
    core_p = layer(pa['pink'], closed_idx=(0, 4), width=max(1, w // 2)) & mp
    core_c = layer(pa['cyan'], width=max(1, w // 2)) & mc
    ex, ey = pa['eye']
    me = np.zeros((Hl, Wl), bool); d0 = Image.new('L', (Wl, Hl), 0); dd = ImageDraw.Draw(d0)
    r_ = max(1.0, 1.2 * s)
    dd.ellipse([ex * s + 2 - r_, ey * s + 2 - r_, ex * s + 2 + r_, ey * s + 2 + r_], fill=255); me = np.array(d0) > 0
    ml = np.zeros((Hl, Wl), bool)
    if pa['lid'] > 0.3:
        d1 = Image.new('L', (Wl, Hl), 0); ImageDraw.Draw(d1).line([(43.4 * s + 2, (ey - 0.6 * pa['lid']) * s + 2), (48.8 * s + 2, (ey - 0.6 * pa['lid']) * s + 2)],
                                                                  fill=255, width=max(1, w - 1)); ml = np.array(d1) > 0
    rgb = np.zeros((Hl, Wl, 3), np.float32); a = np.zeros((Hl, Wl), np.float32)
    off_p, off_c = np.array((110, 50, 86), np.float32), np.array((50, 90, 110), np.float32)
    def put(m, col, core):
        c = np.array(col, np.float32)
        c = c * lvl if lvl > 0.3 else c * 0.30 + np.array((40, 24, 40), np.float32)
        rgb[m] = np.clip(c, 0, 255); a[m] = 1.0
        if lvl > 0.3: rgb[core] = np.clip(c * 0.35 + np.array((255, 240, 250), np.float32) * 0.65 * min(1.0, lvl), 0, 255)
    put(mp, PINK, core_p); put(mc, CYAN, core_c)
    rgb[me] = np.array((255, 236, 110), np.float32) * max(0.35, lvl); a[me] = 1
    rgb[ml] = np.array(PINK, np.float32) * max(0.35, lvl); a[ml] = 1
    # upscale to output
    up = lambda arr: np.repeat(np.repeat(arr, q, 0), q, 1)
    R, Al = up(rgb), up(a)
    x0, y0 = int(x - Wl * q / 2), int(y - Hl * q)
    H, W = big.shape[:2]
    xs, ys = max(0, x0), max(0, y0); xe, ye = min(W, x0 + R.shape[1]), min(H, y0 + R.shape[0])
    if xs >= xe or ys >= ye: return big
    sub = R[ys - y0:ye - y0, xs - x0:xe - x0]; sa = Al[ys - y0:ye - y0, xs - x0:xe - x0]
    if glow and lvl > 0.05:                                          # neon glow: blurred tubes, screen-blended (wide + tight)
        gimg = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
        g1 = np.asarray(gimg.filter(ImageFilter.GaussianBlur(max(1.0, 3.2 * s))), np.float32)
        g2 = np.asarray(gimg.filter(ImageFilter.GaussianBlur(max(1.0, 9.0 * s))), np.float32)
        G = np.asarray(Image.fromarray(np.clip(g1 * 1.6 + g2 * 1.4, 0, 255).astype(np.uint8)).resize((R.shape[1], R.shape[0]), Image.BILINEAR), np.float32)
        add = np.zeros(big.shape, np.float32)
        add[ys:ye, xs:xe] = G[ys - y0:ye - y0, xs - x0:xe - x0] * glow * min(1.2, lvl)
        AT.screen(big, add)
    reg = big[ys:ye, xs:xe].astype(np.float32)
    m = sa > 0
    reg[m] = sub[m]
    big[ys:ye, xs:xe] = reg.astype(np.uint8)
    if talk > 0.55:                                                  # a few sparks pop off the tubes on loud syllables
        AT.sparks(big, x + 14 * u, y - 70 * u, t, t - 0.05, n=4, col=(255, 200, 240), seed=int(t * 7), life=0.3, speed=160 * u / 6, px=max(3, q))
    if ST.LOG[0] is not None: ST.log('sprite', bbox=(x0, y0, x0 + R.shape[1], y0 + R.shape[0]), face=(x + 15 * u, y - 74 * u, 6 * u), scale=u)
    return big


# ---------------------------------------------------------------- the 2.5D shot
def shot(name, light, cx, cy, Z, acts=(), par=(0.0, 0.0), fx_=None, pre=None, t=0.0, kick=(0, 0), focus=None, dof_k=34.0, haze=None,
         motes=True, bokeh_=False, juice=True, rays=None, front=(), bloom=(232, 20, 0.32), vig=0.20, emit=None):
    """depth25.shot25 on a «STILL 1986» world + atmosphere: sunset motes, optional bokeh, the juicy grade (owner 12.11.2026)"""
    W_ = world(name)
    big = D25.shot25(W_, light, cx, cy, Z, depth(name), acts=acts, front=front, par=par, focus=focus, dof_k=dof_k, haze_=haze,
                     bloom_=bloom, rays_=rays, pre=pre, emit=emit, fx_=None, sx=180, sy=320, vig=0, t=t, kick=(0, 0))
    if bokeh_: AT.bokeh(big, t, box=(0, 0, OUT_W, 1000), seed=int(cx) % 7)
    if motes:
        col = (255, 214, 160) if name == 'ocean' else (255, 170, 230)
        AT.motes(big, t, n=34, col=col, seed=int(cx * 3) % 11, par=par[0] * 3)
    if fx_: fx_(big, None)
    if juice: AT.juice(big, 1.30, 1.12)
    if vig: fx.vignette(big, vig)
    if kick[0] or kick[1]:
        dx, dy = int(round(kick[0])), int(round(kick[1]))
        big[:] = np.roll(np.roll(big, dy, 0), dx, 1)
    return big


def blur(big, r=8):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


# ---------------------------------------------------------------- titles: chrome 80s letters
def _dil(m, r, step=2):
    d = m.copy()
    for dx in range(-r, r + 1, step):
        for dy in range(-r, r + 1, step):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def chrome_title(lines, size=80, width=OUT_W):
    """80s chrome letters: sky-blue -> white top half, a dark horizon line, sunset orange -> hot pink bottom half with dark
    horizontal cuts; hot-pink inner outline, deep indigo outer outline + drop, white star glints"""
    f = O.pfont(size)
    out = np.zeros((len(lines) * (size + 60) + 60, width, 4), np.uint8)
    y = 26
    for li, line in enumerate(lines):
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 64), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 22 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        o1 = _dil(m, 6, 1); o2 = _dil(m, 13)
        drop = np.roll(o2, 9, 0) & ~o2
        reg = out[y:y + m.shape[0]]
        reg[drop] = (12, 6, 30, 255); reg[o2] = INK + (255,); reg[o1 & ~m] = (255, 40, 160, 255)
        rr = np.where(m.any(1))[0]; r0, r1 = rr[0], rr[-1]
        for yy in range(r0, r1 + 1):
            k = (yy - r0) / max(1, r1 - r0)
            if k < 0.48: c = np.array((80, 190, 255)) * (1 - k / 0.48) + np.array((255, 255, 255)) * (k / 0.48)
            elif k < 0.56: c = np.array((70, 26, 96))
            else:
                kk = (k - 0.56) / 0.44
                c = np.array((255, 196, 70)) * (1 - kk) + np.array((255, 60, 170)) * kk
                if int((yy - r0)) % 7 in (0,): c = c * 0.62
            mm = m[yy]; reg[yy][mm, :3] = c.astype(np.uint8); reg[yy][mm, 3] = 255
        for x_ in np.where(m.any(0))[0][::max(1, size // 2)][:3]:
            cy_ = r0 + 4
            reg[max(0, cy_ - 8):cy_ + 9, x_:x_ + 3] = (255, 255, 255, 255); reg[cy_:cy_ + 3, max(0, x_ - 7):x_ + 10] = (255, 255, 255, 255)
        y += th + 60
    return out


def title_trim(a):
    m = a[..., 3] > 0
    r = np.where(m.any(1))[0]; c = np.where(m.any(0))[0]
    return a[r[0]:r[-1] + 1, c[0]:c[-1] + 1]


# ---------------------------------------------------------------- VHS label: badge / cover plate
STRIPES = ((255, 60, 160), (255, 140, 60), (255, 214, 70), (60, 220, 255))


def vhs_label(line1, line2, w=640, h=170):
    """a VHS cassette label: black cassette edge, cream label, 4 rainbow stripes, big title + small «EP n/6 • SP»"""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rounded_rectangle([0, 0, w - 1, h - 1], 16, fill=(22, 16, 30, 255))
    d.rounded_rectangle([10, 10, w - 11, h - 11], 10, fill=(250, 244, 226, 255))
    sh = (h - 20) // 2 // 4
    for i, c in enumerate(STRIPES):
        d.rectangle([10, h - 11 - (4 - i) * sh, w - 11, h - 11 - (3 - i) * sh - 1], fill=c + (255,))
    s1 = int(h * 0.30)
    while O.pfont(s1).getlength(line1) > w - 60 and s1 > 10: s1 -= 2
    d.text((30, 22), line1, font=O.pfont(s1), fill=(30, 18, 60))
    s2 = int(s1 * 0.5)
    while O.pfont(s2).getlength(line2) > w - 60 and s2 > 8: s2 -= 2
    d.text((32, 22 + s1 + 10), line2, font=O.pfont(s2), fill=(210, 40, 120))
    return np.array(img)


def badge(n, total=6):
    im = Image.new('RGBA', (470, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, 469, 63], 12, fill=(22, 16, 30, 210))
    for i, c in enumerate(STRIPES): d.rectangle([12 + i * 9, 12, 18 + i * 9, 51], fill=c + (255,))
    d.text((60, 20), f'STILL 1986 • EP {n}/{total}', font=O.pfont(21), fill=(255, 244, 226))
    return np.array(im)


# ---------------------------------------------------------------- the per-episode overlay pass
class Show:
    def __init__(s, epi, n, hook, hook_t=(0.10, 2.4), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1180, hook_y=300,
                 hook_size=78, vhs=()):
        s.epi = epi
        s.badge = badge(n)
        s.hook = chrome_title(hook, hook_size) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics); s.vhs = list(vhs)
        s.cap_y = cap_y or {}; s.cap_default = cap_default

    def apply(s, big, t, shot_):
        for a, b, k in s.vhs:
            if a <= t < b: fx.vhs(big, t, k)
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        O.overlay(big, s.badge, 36, 96, 1.0)
        if s.hook is not None and s.hook_t[0] <= t < s.hook_t[1]:
            k = min(1.0, (t - s.hook_t[0]) / 0.1) * (1 - sm((t - (s.hook_t[1] - 0.2)) / 0.2))
            O.overlay(big, s.hook, 0, s.hook_y, k)
            if ST.LOG[0] is not None: ST.log('title', bbox=(0, s.hook_y, OUT_W, s.hook_y + s.hook.shape[0]))
        s.epi.captions.draw(big, t, s.cap_y.get(shot_, s.cap_default))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


def st(text, fg=(255, 214, 80), size=58):
    return O.sticker(text, fg=fg, size=size)


# ---------------------------------------------------------------- covers (profile grid rule 10.10.2026)
GRID = (240, 1680)
SAFE_BOTTOM = 1520


def cover_make(frame, title, n=1, out='cover.png', title_size=96):
    big = frame.copy()
    p = vhs_label('STILL 1986', f'EPISODE {n}/6 • SP', w=640, h=170)
    py = GRID[0] + 22
    t = chrome_title(title, title_size)
    ty = py + p.shape[0] - 14
    y1 = ty + t.shape[0]
    shade = np.zeros((big.shape[0], 1, 1), np.float32); shade[:y1, 0, 0] = 0.30
    n_ = len(shade[y1:y1 + 140]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.30, 0.0, 140)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t, 0, ty, 1.0)
    Image.fromarray(big).save(out)
    g = big[GRID[0]:GRID[1]].copy()
    g[SAFE_BOTTOM - GRID[0]:] = (g[SAFE_BOTTOM - GRID[0]:] * 0.45).astype(np.uint8)
    Image.fromarray(g).resize((270, 360), Image.LANCZOS).save(str(out).replace('.png', '_grid.png'))
    return big


# ---------------------------------------------------------------- inserts
def phone_screen(t, t_fee=None, w=640, h=1060, total=None, title='ParkMeMaybe', zone='OCEAN DR • ZONE 86', rate='$14.00', unit='/ HOUR'):
    """Vince's smartphone in a 1986 brick case (chunky grey body, antenna, keypad) with the parking app on it;
    t_fee: time the red «+$3.50 CONVENIENCE FEE» stamp slams in"""
    S = 4                                                            # draw at 1/4, upscale nearest = pixel look
    wl, hl = w // S, h // S
    im = Image.new('RGBA', (wl, hl + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([wl - 26, 0, wl - 18, 44], fill=(50, 50, 60, 255)); d.ellipse([wl - 29, 0, wl - 15, 10], fill=(200, 50, 70, 255))   # antenna
    d.rounded_rectangle([0, 34, wl - 1, hl + 39], 14, fill=(70, 72, 84, 255), outline=(24, 20, 40, 255), width=2)
    d.rounded_rectangle([6, 40, wl - 7, hl + 33], 10, fill=(96, 98, 112, 255))
    sx0, sy0, sx1, sy1 = 14, 52, wl - 15, int(hl * 0.74)
    d.rectangle([sx0, sy0, sx1, sy1], fill=(14, 20, 40, 255))
    d.rectangle([sx0, sy0, sx1, sy0 + 26], fill=(60, 210, 140, 255))
    f1, f2, f3, f4 = O.pfont(9), O.pfont(6), O.pfont(20), O.pfont(9)
    d.text((sx0 + 8, sy0 + 8), 'P ' + title, font=f1, fill=(10, 30, 20))
    d.text((sx0 + 8, sy0 + 38), zone, font=f2, fill=(160, 200, 255))
    d.text((sx0 + 8, sy0 + 62), rate, font=f3, fill=(255, 255, 255))
    d.text((sx0 + 10, sy0 + 92), unit, font=f2, fill=(160, 200, 255))
    d.rounded_rectangle([sx0 + 10, sy1 - 34, sx1 - 10, sy1 - 10], 6, fill=(60, 210, 140, 255))
    d.text((sx0 + 34, sy1 - 27), 'PAY NOW', font=f4, fill=(10, 30, 20))
    for r in range(3):                                               # keypad bumps under the screen
        for c in range(3): d.rounded_rectangle([18 + c * ((wl - 36) // 3), sy1 + 12 + r * 18, 18 + c * ((wl - 36) // 3) + 26, sy1 + 24 + r * 18], 3, fill=(140, 142, 156, 255))
    a = np.array(im.resize((wl * S, (hl + 40) * S), Image.NEAREST))
    base = Image.new('RGBA', (a.shape[1] + 240, a.shape[0]), (0, 0, 0, 0)); base.paste(Image.fromarray(a), (120, 0))
    if t_fee is not None and t >= t_fee:                              # the stamp slams in (can stick out of the phone)
        k = min(1.0, (t - t_fee) / 0.12); sc = 1.0 + 0.6 * (1 - k)
        st_ = Image.fromarray(O.sticker('+$3.50 CONVENIENCE FEE', fg=(255, 70, 90), size=int(22 * sc))).rotate(-8, expand=True, resample=Image.NEAREST)
        if st_.width > base.width: st_ = st_.resize((base.width, int(st_.height * base.width / st_.width)), Image.NEAREST)
        base.alpha_composite(st_, ((base.width - st_.width) // 2, int(base.height * 0.47)))
    return np.array(base)


def fine_print(t, t_zoom=0.25, w=OUT_W, h=OUT_H):
    """the bait board close up: «FREE PARKING*», then the camera slams into the tiny asterisk line under it"""
    S = 3
    im = Image.new('RGB', (w // S, h // S), (36, 22, 60)); d = ImageDraw.Draw(im); d.fontmode = '1'
    W_, H_ = im.size
    d.rounded_rectangle([20, 220, W_ - 20, 470], 14, fill=(252, 244, 222), outline=PINK, width=6)
    f = O.pfont(38)
    for i, line in enumerate(('FREE', 'PARKING*')):
        tw = f.getlength(line); d.text(((W_ - tw) / 2, 250 + i * 70), line, font=f, fill=(230, 40, 110))
    fs = O.pfont(8)
    small = '*PARKING IS FREE. THE RIDE IS $350.'
    tw = fs.getlength(small); d.text(((W_ - tw) / 2, 428), small, font=fs, fill=(70, 40, 90))
    if t >= t_zoom and int((t - t_zoom) * 6) % 2 == 0:                  # the fine print gets circled (blinking pink marker)
        d.rounded_rectangle([(W_ - tw) / 2 - 8, 420, (W_ + tw) / 2 + 8, 446], 6, outline=(255, 40, 140), width=3)
    if t >= t_zoom:
        f2 = O.pfont(16); s2 = 'READ THE *'
        d.text(((W_ - f2.getlength(s2)) / 2, 160), s2, font=f2, fill=(255, 110, 200))
    a = np.array(im.resize((w, h), Image.NEAREST))
    return a


# ---------------------------------------------------------------- lights for E02–E06 worlds
def light_club(v):
    return Light(amb=(0.86, 0.80, 1.0), keys=_keys(v, [(520, 120, 520, (255, 70, 190), 0.45), (860, 300, 300, (80, 230, 255), 0.35)]), grad=(1.02, 0.9))


def light_disco(v, t=0.0):
    k = 0.5 + 0.5 * math.sin(t * 6)
    return Light(amb=(0.78, 0.70, 1.0), keys=_keys(v, [(400, 100, 500, (255, 70, 190), 0.30 + 0.25 * k), (900, 100, 500, (60, 230, 255), 0.55 - 0.25 * k),
                                                        (640, 600, 500, (255, 200, 90), 0.25)]), grad=(1.0, 1.05))


def light_marina(v):
    return Light(amb=(1.06, 0.95, 0.96), keys=_keys(v, [(780, 280, 900, (255, 170, 100), 0.35)]), grad=(1.05, 0.95))


def light_mall(v):
    return Light(amb=(0.84, 0.80, 1.0), keys=_keys(v, [(480, 200, 520, (255, 80, 190), 0.40), (540, 450, 400, (90, 220, 255), 0.30),
                                                       (160, 300, 260, (255, 210, 130), 0.30)]), grad=(1.0, 0.92))


def light_studio(v, tv=0.0):
    keys = [(1060, 330, 500, (255, 160, 90), 0.30), (1150, 250, 400, (255, 70, 190), 0.30)]
    if tv: keys.append((190, 330, 500, (120, 200, 255), 0.45 * tv))
    return Light(amb=(0.90, 0.84, 0.96), keys=_keys(v, keys), grad=(1.0, 0.95))


def light_rain(v):
    return Light(amb=(0.72, 0.74, 0.96), keys=_keys(v, [(620, 300, 380, (255, 70, 190), 0.45), (1080, 260, 420, (70, 220, 255), 0.35)]), grad=(0.95, 0.85))


def V(name, cx, cy, Z):
    return view_at(world(name), cx, cy, Z, 180, 320)


def S_of(v, name, z=1.0):
    """output px per hero sprite px for world `name` at depth scale z"""
    return WS[name] * 3 * v.Z * z


# ---------------------------------------------------------------- crowd silhouettes (club, line, disco)
def crowd(big, t, y0, y1, n=14, seed=1, cols=((255, 70, 190), (60, 230, 255)), headphones=False, dance=1.0, sunglasses=False, x0=0, x1=OUT_W,
          h=(260, 420), dark=(26, 16, 46)):
    """dark pixel silhouettes of people (heads, shoulders, bobbing to a beat) with a neon rim; headphones glow on the silent disco"""
    g = np.random.default_rng(seed)
    q = 6
    for i in range(n):
        x = g.uniform(x0, x1); y = g.uniform(y0, y1); H = g.uniform(*h) * (0.6 + 0.6 * (y - y0) / max(1, y1 - y0))
        ph = g.random() * 6.28
        bob = abs(math.sin(t * 6.0 * dance + ph)) * 18 * dance
        hw = H * 0.16; bw = H * 0.32
        cx, top = x + math.sin(t * 3 + ph) * 10 * dance, y - H - bob
        X0, X1 = int(cx - bw), int(cx + bw); Y0, Y1 = int(top), int(y)
        if X1 <= 0 or X0 >= OUT_W: continue
        yy, xx = np.mgrid[max(0, Y0):min(OUT_H, Y1), max(0, X0):min(OUT_W, X1)]
        if yy.size == 0: continue
        xx_ = (xx // q) * q + q / 2; yy_ = (yy // q) * q + q / 2
        head = ((xx_ - cx) / hw) ** 2 + ((yy_ - (top + hw * 1.1)) / (hw * 1.15)) ** 2 <= 1
        body = (yy_ > top + hw * 2.0) & (np.abs(xx_ - cx) < bw * np.clip((yy_ - top - hw * 1.6) / (hw * 1.4), 0.3, 1.0))
        m = head | body
        reg = big[max(0, Y0):min(OUT_H, Y1), max(0, X0):min(OUT_W, X1)]
        reg[m] = dark
        c = np.array(cols[i % len(cols)], np.uint8)
        edge = m & ~np.roll(m, q, 1)
        reg[edge] = c
        if headphones:
            band = (np.abs(np.sqrt((xx_ - cx) ** 2 + (yy_ - (top + hw * 1.1)) ** 2) - hw * 1.25) < q) & (yy_ < top + hw * 1.2)
            cups = ((np.abs(xx_ - (cx - hw * 1.15)) < q * 1.5) | (np.abs(xx_ - (cx + hw * 1.15)) < q * 1.5)) & (np.abs(yy_ - (top + hw * 1.2)) < q * 2.2)
            reg[band | cups] = c
        if sunglasses:
            gl = (np.abs(yy_ - (top + hw)) < q) & (np.abs(xx_ - cx) < hw * 0.9)
            reg[gl] = (10, 10, 14)
    return big


# ---------------------------------------------------------------- rain (E05)
def rain(big, t, k=1.0, seed=2, col=(170, 200, 255), angle=0.22):
    if k <= 0: return big
    g = np.random.default_rng(seed)
    n = int(160 * k)
    P_ = g.random((n, 3))
    for x0, y0, sp in P_:
        L = 40 + 50 * sp
        y = ((y0 * OUT_H + t * (1400 + 900 * sp)) % (OUT_H + 200)) - 100
        x = (x0 * OUT_W + y * angle) % OUT_W
        for j in range(0, int(L), 6):
            yy = int(y + j); xx = int(x + j * angle)
            if 0 <= yy < OUT_H - 6 and 0 <= xx < OUT_W - 3:
                reg = big[yy:yy + 6, xx:xx + 3].astype(np.float32)
                big[yy:yy + 6, xx:xx + 3] = np.clip(reg * 0.5 + np.array(col) * 0.5, 0, 255).astype(np.uint8)
    return big


# ---------------------------------------------------------------- UI screens (fees, rental board, car, TV)
def _screen(w, h, S=4, bg=(14, 20, 40), bezel=(70, 72, 84)):
    im = Image.new('RGBA', (w // S, h // S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, w // S - 1, h // S - 1], 10, fill=bezel + (255,), outline=(24, 20, 40, 255), width=2)
    d.rectangle([8, 8, w // S - 9, h // S - 9], fill=bg + (255,))
    return im, d


def fee_screen(t, rows, total=None, t_total=None, stamp=None, t_stamp=None, w=920, h=1100, title='TICKET • 86 NIGHT'):
    """the box office screen: rows = [(t_appear, label, price)], each row slams in; optional total row and a red stamp"""
    S = 4
    im, d = _screen(w, h, S)
    W_ = w // S
    d.rectangle([8, 8, W_ - 9, 34], fill=(255, 70, 180, 255))
    d.text((16, 16), title, font=O.pfont(9), fill=(255, 255, 255))
    y = 46
    for (ta, lab, pr) in rows:
        if t < ta: break
        f = O.pfont(9)
        d.text((16, y), lab, font=f, fill=(200, 220, 255) if 'FEE' not in lab.upper() else (255, 160, 190))
        d.text((W_ - 16 - f.getlength(pr), y), pr, font=f, fill=(255, 255, 255))
        y += 22
    if total and t_total is not None and t >= t_total:
        d.line([(16, y + 2), (W_ - 16, y + 2)], fill=(255, 255, 255), width=2)
        f = O.pfont(16)
        d.text((16, y + 12), 'TOTAL', font=f, fill=(255, 214, 80)); d.text((W_ - 16 - f.getlength(total), y + 12), total, font=f, fill=(255, 214, 80))
    a = np.array(im.resize((W_ * S, (h // S) * S), Image.NEAREST))
    base = Image.new('RGBA', (a.shape[1] + 200, a.shape[0]), (0, 0, 0, 0)); base.paste(Image.fromarray(a), (100, 0))
    if stamp and t_stamp is not None and t >= t_stamp:
        k = min(1.0, (t - t_stamp) / 0.12); sc = 1.0 + 0.6 * (1 - k)
        st_ = Image.fromarray(O.sticker(stamp, fg=(255, 70, 90), size=int(40 * sc))).rotate(-9, expand=True, resample=Image.NEAREST)
        if st_.width > base.width: st_ = st_.resize((base.width, int(st_.height * base.width / st_.width)), Image.NEAREST)
        base.alpha_composite(st_, ((base.width - st_.width) // 2, int(base.height * 0.62)))
    return np.array(base)


def car_screen(t, lines, w=860, h=520, col=(90, 236, 255)):
    """ROOF-E infotainment screen: a rounded dark panel with a roof icon and lines of text (each line = (t_appear, text, colour))"""
    S = 4
    im, d = _screen(w, h, S, bg=(8, 14, 26), bezel=(30, 30, 40))
    W_ = w // S
    d.text((16, 14), 'ROOF-E', font=O.pfont(10), fill=col)
    d.polygon([(W_ - 60, 34), (W_ - 40, 18), (W_ - 20, 34)], outline=col)                      # roof icon
    y = 46
    for (ta, txt, c) in lines:
        if t < ta: continue
        f = O.pfont(9 if len(txt) > 16 else 12)
        d.text(((W_ - f.getlength(txt)) / 2, y), txt, font=f, fill=c)
        y += 24
    return np.array(im.resize((W_ * S, (h // S) * S), Image.NEAREST))


def crt(screen_img, t, w=980, h=760):
    """a chunky CRT television frame around an RGB/RGBA image (scanlines, curvature-ish vignette, glow)"""
    tv = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(tv)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 40, fill=(60, 54, 62, 255), outline=(20, 16, 26, 255), width=8)
    d.rounded_rectangle([40, 40, w - 220, h - 40], 60, fill=(10, 12, 16, 255))
    for i in range(5): d.ellipse([w - 160, 120 + i * 90, w - 90, 170 + i * 90], fill=(40, 36, 44, 255), outline=(90, 86, 96, 255), width=3)
    sx0, sy0, sx1, sy1 = 64, 64, w - 244, h - 64
    scr = Image.fromarray(screen_img[..., :3] if screen_img.shape[2] == 4 else screen_img).resize((sx1 - sx0, sy1 - sy0), Image.NEAREST)
    a = np.array(scr).astype(np.float32)
    a[::6] *= 0.72
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    vg = 1 - 0.35 * (((xx / a.shape[1] - 0.5) * 2) ** 4 + ((yy / a.shape[0] - 0.5) * 2) ** 4)
    a = np.clip(a * vg[..., None], 0, 255).astype(np.uint8)
    tv.paste(Image.fromarray(a), (sx0, sy0))
    return np.array(tv)


def progress_screen(t, frac, label='DAY-ONE UPDATE', sub='150 GB • 6 HRS LEFT', w=640, h=480):
    im = Image.new('RGB', (w // 4, h // 4), (16, 20, 44)); d = ImageDraw.Draw(im); d.fontmode = '1'
    W_, H_ = im.size
    f, f2 = O.pfont(9), O.pfont(7)
    d.text(((W_ - f.getlength(label)) / 2, 30), label, font=f, fill=(90, 236, 255))
    d.rectangle([14, 56, W_ - 14, 70], outline=(255, 255, 255))
    d.rectangle([16, 58, 16 + int((W_ - 32) * frac), 68], fill=(255, 70, 180))
    d.text(((W_ - f2.getlength(sub)) / 2, 82), sub, font=f2, fill=(255, 214, 80))
    d.text(((W_ - f2.getlength(f'{int(frac * 100)}%')) / 2, 98), f'{int(frac * 100)}%', font=f2, fill=(255, 255, 255))
    return np.array(im.resize((w, h), Image.NEAREST))


def pedal_group(v, wx, wy, t, vince_kw=None, ws=None, z=1.0, pedal=0.0, water_y=None, rock=0.0):
    """pedal flamingo boat with Vince seated: [boat back, Vince, boat front]; water_y (world) cuts everything below the waterline"""
    ws = ws or WSV
    S = ws * 3 * v.Z * z; Sc = S * C.CAR_K
    hx, hy = -6.0 * C.CAR_K + 1.6, 18.0 * C.CAR_K - 34.0
    k = ws * z
    vk = dict(vince_kw or {}); vk.setdefault('legs', False); vk.setdefault('hand_n', (22.0, 44.0)); vk.setdefault('hand_f', (-14.0, 40.0))
    rot = rock * math.sin(t * 2.2)
    acts = [A(C.pedal_flamingo, wx, wy, Sc, t=t, part='back', rot=rot),
            A(C.vince, wx + hx * k, wy - hy * k, S, t=t, rot=rot, pivot=(-hx, -hy), **vk),
            A(C.pedal_flamingo, wx, wy, Sc, t=t, part='front', pedal=pedal, rot=rot)]
    if water_y is not None: acts = [WaterClip(a, water_y) for a in acts]
    return acts


class WaterClip:
    """draw an actor only above the waterline (world y); a foam line is added where it meets the water"""
    direct = True

    def __init__(s, act, wy):
        s.a, s.wy = act, wy

    def __call__(s, big, v, lt):
        tmp = big.copy()
        s.a(tmp, v, lt)
        y = int(v.opt(0, s.wy)[1])
        y = max(0, min(big.shape[0], y))
        diff = np.any(tmp[:y] != big[:y], axis=2)
        big[:y][diff] = tmp[:y][diff]
        cols = np.where(diff[max(0, y - 6):y].any(0))[0]
        if len(cols) and y < big.shape[0] - 8:
            big[y - 2:y + 6, cols] = np.clip(big[y - 2:y + 6, cols].astype(np.int32) + 70, 0, 255).astype(np.uint8)
        s.last = getattr(s.a, 'last', None)
