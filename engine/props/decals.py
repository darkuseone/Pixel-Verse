"""Decals: signs, plaques, stickers, posters and graffiti laid over a world (AI background) at HIGH resolution.

Why: AI backgrounds are 1280x720 world px; text baked straight into them is chunky and easily runs off its plate. A decal is an RGBA
image with WS decal px per world px (default 4), sampled on the output grid by View.bg(), so its letters stay crisp at any zoom.
Rule (10.10.2026): every inscription is FITTED into its plate (biggest font that fits inside border + padding, centred) and never
crosses the plate's edge; a decal sits on a real surface of the background (wall, fence, pole, glass) and is placed in world px.

  from props import decals as D
  img = D.plate(60, 22, ['GATOR', 'XING'], bg=(255, 214, 40), fg=(20, 20, 20), border=(20, 20, 20))
  D.attach(WORLD, [(img, x, y)])          # top-left in world px; View.bg() draws it on every frame of that world
  D.anim(WORLD, fn)                       # fn(big, v, t): animated ambience in the background layer (flags, flies, ripples)
"""
import math
import numpy as np
from PIL import Image
import stage as ST
from props.dibspix import FONT3

WS = 4
FONT = dict(FONT3)
FONT.update(N=['1001', '1101', '1011', '1001', '1001'], M=['10001', '11011', '10101', '10001', '10001'],
            W=['10001', '10001', '10101', '11011', '10001'], K=['1001', '1010', '1100', '1010', '1001'])
FONT.update({'&': ['010', '101', '010', '101', '011'], '*': ['000', '101', '010', '101', '000'], ',': ['000', '000', '000', '010', '100'],
             '%': ['101', '001', '010', '100', '101'], '#': ['101', '111', '101', '111', '101'], "'": ['010', '010', '000', '000', '000'],
             '"': ['101', '101', '000', '000', '000'], '(': ['01', '10', '10', '10', '01'], ')': ['10', '01', '01', '01', '10'],
             '+': ['000', '010', '111', '010', '000'], '=': ['000', '111', '000', '111', '000'], '@': ['111', '101', '111', '100', '011'],
             '<': ['001', '010', '100', '010', '001'], '>': ['100', '010', '001', '010', '100'], ';': ['000', '010', '000', '010', '100'],
             '~': ['000', '000', '011', '110', '000'], '^': ['010', '101', '000', '000', '000'], '_': ['000', '000', '000', '000', '111']})
# heart / star / arrow / skull-ish glyphs for stickers
FONT.update({'♥': ['01010', '11111', '11111', '01110', '00100'], '★': ['00100', '01110', '11111', '01110', '01010'],
             '→': ['00100', '00010', '11111', '00010', '00100'], '☺': ['01110', '10101', '11111', '10001', '01110']})


def glyph(ch):
    return FONT.get(ch.upper(), FONT.get(ch, FONT[' ']))


def text_w(s):
    """width in font px (1 px gap between letters)"""
    return sum(len(glyph(c)[0]) + 1 for c in s) - 1 if s else 0


def draw_text(img, s, x, y, n, col, shadow=None):
    """3x5 text into an RGBA array: top-left (x, y) in decal px, n decal px per font px; optional 1-font-px drop shadow"""
    for (dx, dy, c) in ([(max(1, n // 2), max(1, n // 2), shadow)] if shadow else []) + [(0, 0, col)]:
        cx = x
        for ch in s:
            g = glyph(ch)
            for r, row in enumerate(g):
                for q, b in enumerate(row):
                    if b == '1':
                        y0, x0 = y + r * n + dy, cx + q * n + dx
                        img[y0:y0 + n, x0:x0 + n, :3] = c; img[y0:y0 + n, x0:x0 + n, 3] = 255
            cx += (len(g[0]) + 1) * n


def fit(lines, w, h, weights=None, lead=1.0):
    """biggest n (decal px per font px) at which every line (scaled by its weight) fits in w x h decal px. Returns n, scales"""
    weights = weights or [1.0] * len(lines)
    best = 0
    for n in range(1, 200):
        sc = [max(1, int(round(n * wt))) for wt in weights]
        tw = max(text_w(l) * s for l, s in zip(lines, sc))
        th = sum(5 * s for s in sc) + sum(int(lead * s) for s in sc[1:])
        if tw > w or th > h: break
        best = n
    if not best: return 0, None
    return best, [max(1, int(round(best * wt))) for wt in weights]


def plate(w, h, lines, bg=(250, 248, 238), fg=(20, 20, 24), border=(24, 24, 28), bw=1.0, pad=1.5, colors=None, weights=None,
          ws=WS, shadow=None, wear=0.0, seed=0, rivets=False, stripe=None, round_=0.0, tilt=0.0, max_n=None, align='c', lead=1.0):
    """a sign plate w x h WORLD px with auto-fitted, centred lines (never past border + pad). colors/weights per line;
    stripe = (colour, fraction) header band; wear = grime/rust specks 0..1; round_ = corner radius (world px); tilt = degrees.
    Returns an RGBA array in decal px (ws per world px)."""
    W_, H_ = int(round(w * ws)), int(round(h * ws))
    img = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    m = np.ones((H_, W_), bool)
    if round_ > 0:
        r = round_ * ws
        for cx, cy in ((r, r), (W_ - r, r), (r, H_ - r), (W_ - r, H_ - r)):
            corner = ((xx < r) if cx == r else (xx > W_ - r)) & ((yy < r) if cy == r else (yy > H_ - r))
            m &= ~(corner & ((xx - cx) ** 2 + (yy - cy) ** 2 > r * r))
    img[m, :3] = bg; img[m, 3] = 255
    b = int(round(bw * ws))
    if border is not None and b > 0:
        inner = np.zeros_like(m); inner[b:H_ - b, b:W_ - b] = m[b:H_ - b, b:W_ - b]
        if round_ > 0:
            inner = m.copy()
            for _ in range(b):
                inner = inner & np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
                inner[0, :] = inner[-1, :] = False; inner[:, 0] = inner[:, -1] = False
        img[m & ~inner, :3] = border
    else:
        b = 0
    top = b
    if stripe:
        sc_, fr = stripe
        sh = int(round((H_ - 2 * b) * fr))
        img[b:b + sh, b:W_ - b, :3] = sc_
        img[~m] = 0
    if rivets:
        for cx, cy in ((b + 2 * ws // 2 + 2, b + 2 * ws // 2 + 2), (W_ - b - ws - 2, b + ws // 2 + 2), (b + ws // 2 + 2, H_ - b - ws - 2), (W_ - b - ws - 2, H_ - b - ws - 2)):
            img[cy:cy + ws, cx:cx + ws, :3] = (150, 150, 150)
    p = int(round(pad * ws))
    lines = [l for l in lines]
    colors = colors or [fg] * len(lines)
    n, scs = fit(lines, W_ - 2 * (b + p), H_ - 2 * (b + p), weights, lead)
    if n and max_n: n, scs = fit(lines, min(W_ - 2 * (b + p), max(text_w(l) for l in lines) * max_n * ws), H_ - 2 * (b + p), weights, lead)
    if not n:
        raise ValueError(f'decal text does not fit: {lines} in {w}x{h} world px')
    th = sum(5 * s for s in scs) + sum(int(lead * s) for s in scs[1:])
    y = (H_ - th) // 2
    for l, s, c in zip(lines, scs, colors):
        lw = text_w(l) * s
        x = (W_ - lw) // 2 if align == 'c' else (b + p if align == 'l' else W_ - b - p - lw)
        draw_text(img, l, x, y, s, c, shadow)
        y += 5 * s + int(lead * s)
    if wear > 0: weather(img, wear, seed)
    if tilt: img = rotate(img, tilt)
    return img


def weather(img, k=0.3, seed=0, col=(120, 84, 50)):
    """grime specks, rust streaks under the top edge, a chipped corner"""
    r = np.random.default_rng(seed)
    H_, W_ = img.shape[:2]
    a = img[..., 3] > 0
    n = int(W_ * H_ * 0.004 * k)
    ys, xs = r.integers(0, H_, n), r.integers(0, W_, n)
    for y, x in zip(ys, xs):
        if a[y, x]: img[y:y + 2, x:x + 2, :3] = (img[y:y + 2, x:x + 2, :3] * 0.6 + np.array(col) * 0.4).astype(np.uint8)
    for q in range(int(3 * k) + 1):
        x = int(r.integers(4, max(5, W_ - 4))); ln = int(r.integers(H_ // 6, H_ // 2))
        sl = img[4:4 + ln, x:x + 2]
        sl[..., :3] = (sl[..., :3] * 0.7 + np.array(col) * 0.3).astype(np.uint8)


def rotate(img, deg):
    im = Image.fromarray(img, 'RGBA').rotate(deg, Image.NEAREST, expand=True)
    return np.array(im)


def sticker(text, bg=(255, 86, 160), fg=(255, 255, 255), w=None, h=None, shape='rect', ws=WS, tilt=0.0, outline=(255, 255, 255), lines=None):
    """bumper sticker / round sticker with a white die-cut edge; text auto-fitted. w, h in world px"""
    lines = lines or [text]
    h = h or 7
    w = w or max(10, h * 3)
    img = plate(w, h, lines, bg=bg, fg=fg, border=outline, bw=0.6, pad=0.8, ws=ws, round_=(min(w, h) / 2 if shape == 'round' else 0.8))
    if tilt: img = rotate(img, tilt)
    return img


def scribble(w, h, col=(40, 40, 44), ws=WS, seed=0, rows=3):
    """illegible small print / graffiti tag scrawl"""
    W_, H_ = int(w * ws), int(h * ws)
    img = np.zeros((H_, W_, 4), np.uint8)
    r = np.random.default_rng(seed)
    for q in range(rows):
        y = int((q + 0.5) * H_ / rows)
        x = 0
        while x < W_ - 4:
            ln = int(r.integers(ws * 2, ws * 6))
            img[y:y + max(1, ws // 2), x:min(W_, x + ln)] = (*col, 255)
            x += ln + int(r.integers(ws, ws * 2))
    return img


def from_sprite(sp_arr):
    """an RGB(A) numpy image (e.g. a rendered code prop) used as a decal as-is"""
    if sp_arr.shape[2] == 4: return sp_arr
    a = np.full(sp_arr.shape[:2] + (1,), 255, np.uint8)
    return np.concatenate([sp_arr, a], 2)


# ---------------------------------------------------------------- registry + drawing (View.bg() calls draw)
def attach(world, items, ws=WS):
    """items: [(img, wx, wy), ...] or (img, wx, wy, ws) — top-left in world px. Appends to whatever the world already has."""
    ent = ST.DECALS.setdefault(id(world), [world, [], []])
    for it in items:
        img, wx, wy = it[:3]
        ent[1].append((img, float(wx), float(wy), it[3] if len(it) > 3 else ws))
    return world


def anim(world, fn):
    """fn(big, v, t): animated ambience drawn right after the decals (still behind the characters)"""
    ent = ST.DECALS.setdefault(id(world), [world, [], []])
    ent[2].append(fn)


def clear(world):
    ST.DECALS.pop(id(world), None)


def copy_to(src, dst):
    """a world copied with .copy() (episode-local edits) inherits the decals of its source"""
    e = ST.DECALS.get(id(src))
    if e: ST.DECALS[id(dst)] = [dst, list(e[1]), list(e[2])]
    return dst


def blit(big, v, img, wx, wy, ws=WS, k=1.0):
    """sample a decal on the output grid of view v (nearest), alpha-blend into big"""
    s = v.Z * ST.UP / ws
    ox, oy = v.opt(wx, wy)
    h, w = img.shape[:2]
    x0, y0 = max(0, int(math.floor(ox))), max(0, int(math.floor(oy)))
    x1, y1 = min(big.shape[1], int(math.ceil(ox + w * s))), min(big.shape[0], int(math.ceil(oy + h * s)))
    if x0 >= x1 or y0 >= y1: return
    xs = ((np.arange(x0, x1) + 0.5 - ox) / s).astype(np.int32).clip(0, w - 1)
    ys = ((np.arange(y0, y1) + 0.5 - oy) / s).astype(np.int32).clip(0, h - 1)
    sub = img[ys[:, None], xs[None, :]]
    al = sub[..., 3:4].astype(np.float32) / 255.0 * k
    reg = big[y0:y1, x0:x1]
    reg[:] = (reg * (1 - al) + sub[..., :3] * al).astype(np.uint8)


def draw(big, v):
    e = ST.DECALS.get(id(v.world))
    if not e or e[0] is not v.world: return
    for img, wx, wy, ws in e[1]: blit(big, v, img, wx, wy, ws)
    for fn in e[2]: fn(big, v, ST.T_NOW[0])


def text_box(img, lines, box, colors, weights=None, lead=1.0, shadow=None, align='c'):
    """auto-fitted lines inside box = (x0, y0, x1, y1) decal px of an existing RGBA image (never past the box)"""
    x0, y0, x1, y1 = [int(v) for v in box]
    n, scs = fit(lines, x1 - x0, y1 - y0, weights, lead)
    if not n: raise ValueError(f'decal text does not fit: {lines} in box {box}')
    if not isinstance(colors, (list, tuple)) or isinstance(colors[0], int): colors = [colors] * len(lines)
    th = sum(5 * s for s in scs) + sum(int(lead * s) for s in scs[1:])
    y = y0 + (y1 - y0 - th) // 2
    for l, s, c in zip(lines, scs, colors):
        lw = text_w(l) * s
        x = x0 + (x1 - x0 - lw) // 2 if align == 'c' else x0
        draw_text(img, l, x, y, s, c, shadow)
        y += 5 * s + int(lead * s)
    return n


def sprite(fn, s, draw, flip=False, **kw):
    """render a code-drawn sprite (props) to an RGBA decal: s = decal px per sprite px; draw = the rig's draw() (e.g. fmpix.draw)"""
    from props.dibspix import blit as dblit
    sp = draw(fn, s, flip=flip, **kw)
    k = sp.k
    W_, H_ = int(sp.W / k * s) + 8, int(sp.H / k * s) + 8
    key = np.array((255, 0, 255), np.uint8)
    big = np.zeros((H_, W_, 3), np.uint8); big[:] = key
    ox, oy = sp.OX / k * s + 4, sp.OY / k * s + 4
    dblit(big, sp, ox, oy, s, None, flip)
    a = np.where((big == key).all(-1), 0, 255).astype(np.uint8)
    img = np.concatenate([big, a[..., None]], 2)
    ys, xs = np.nonzero(a)
    if not len(ys): return img, (0, 0)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return img[y0:y1, x0:x1], (ox - x0, oy - y0)               # + the feet anchor inside the cropped decal


def preview(world, out, k=3):
    """the whole world with its decals at k output px per world px (placement check), saved downscaled to 1920 wide"""
    big = np.repeat(np.repeat(world, k, 0), k, 1).copy()

    class _V:
        Z = k / ST.UP
        def opt(s, x, y): return (x * k, y * k)
    for img, x, y, ws in ST.DECALS.get(id(world), [None, []])[1]: blit(big, _V(), img, x, y, ws)
    Image.fromarray(big).resize((1920, int(1920 * big.shape[0] / big.shape[1])), Image.LANCZOS).save(out)


def tint(img, k=0.6, col=(255, 210, 140), a=0.15):
    """darken + colour a decal to sit in a dim / night scene (decals are not lit by stage.Light)"""
    out = img.copy()
    f = out[..., :3].astype(np.float32) * k
    out[..., :3] = np.clip(f * (1 - a) + np.array(col, np.float32) * k * a, 0, 255).astype(np.uint8)
    return out


def knockout(img, col=(0, 0, 0)):
    """make one colour transparent (letters only: graffiti, stencils, star rows)"""
    out = img.copy()
    out[(out[..., :3] == np.array(col, np.uint8)).all(-1), 3] = 0
    return out
