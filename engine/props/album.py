"""Дембельский альбом (DMB photo album) props for «Валера и кот»: the closed velvet cover with aluminium letters, the open spread
on the kitchen table, photos with corner tabs, stencil captions (Valera), pencil notes (the cat), transfer decals, a long
grocery receipt, a framed trophy bag, the surveillance page, the credits page. Everything is drawn with PIL in world px of a
1280x720 top-down table world (bg/table_top.png) or on a 640x360 logical page canvas (x3 -> 1920x1080).
Pixel font Press Start 2P only at multiples of 8 px so letters stay crisp."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as PATHS

VELVET = (112, 22, 40)
VELVET_HI = (150, 40, 60)
VELVET_SH = (70, 12, 26)
PAGE = (236, 228, 208)
PAGE_SH = (206, 196, 172)
INK_RED = (196, 36, 40)
INK_BLUE = (36, 70, 160)
GOLD = (214, 170, 60)
GRAPHITE = (70, 70, 78)
SPREAD = (220, 58, 1060, 662)            # open album on the table (world px)
SPINE = 640
COVER = (330, 74, 950, 646)              # closed album


def font(size):
    return ImageFont.truetype(PATHS.FONT_PX, size)


def text_img(lines, size, col, shadow=None, lead=1.5, align='c', jitter=0.0, seed=0, tilt=0.0):
    """RGBA text block; jitter = per-letter random offset (pencil hand), tilt = degrees"""
    f = font(size)
    rng = np.random.default_rng(seed)
    w = max(f.getlength(l) for l in lines) + size * 2
    h = int(len(lines) * size * lead + size * 2)
    im = Image.new('RGBA', (int(w), h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    for i, l in enumerate(lines):
        lw = f.getlength(l)
        x0 = size + ((w - 2 * size - lw) / 2 if align == 'c' else 0)
        y0 = size + i * size * lead
        if jitter <= 0:
            if shadow: d.text((x0 + max(1, size // 8), y0 + max(1, size // 8)), l, font=f, fill=shadow + (255,))
            d.text((x0, y0), l, font=f, fill=col + (255,))
        else:
            x = x0
            for ch in l:
                dx, dy = rng.normal(0, jitter, 2)
                d.text((x + dx, y0 + dy), ch, font=f, fill=col + (255,))
                x += f.getlength(ch)
    if tilt: im = im.rotate(tilt, resample=Image.NEAREST, expand=True)
    return im


def stencil(lines, size=16, col=INK_RED, seed=1):
    """Valera's stencil paint: bold letters, darker shadow, a few spray speckles around"""
    im = text_img(lines, size, col, shadow=tuple(int(c * 0.55) for c in col), lead=1.6)
    a = np.array(im)
    rng = np.random.default_rng(seed)
    ys, xs = np.nonzero(a[..., 3])
    if len(xs):
        for _ in range(len(xs) // 60):
            i = rng.integers(len(xs)); x = int(xs[i] + rng.normal(0, size * 0.5)); y = int(ys[i] + rng.normal(0, size * 0.5))
            if 0 <= x < a.shape[1] and 0 <= y < a.shape[0] and a[y, x, 3] == 0: a[y, x] = col + (200,)
    return Image.fromarray(a)


def pencil(lines, size=16, seed=2, tilt=-2.0):
    return text_img(lines, size, GRAPHITE, lead=1.5, jitter=size * 0.07, seed=seed, tilt=tilt, align='l')


def paste(dst, img, x, y, reveal=1.0, alpha=1.0):
    """alpha-paste RGBA img onto RGB numpy dst at (x, y) (top-left); reveal = fraction of width shown (writing)"""
    a = np.array(img) if not isinstance(img, np.ndarray) else img
    w = int(a.shape[1] * max(0.0, min(1.0, reveal)))
    if w <= 0: return
    a = a[:, :w]
    x, y = int(x), int(y)
    H, W = dst.shape[:2]
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + a.shape[1]), min(H, y + a.shape[0])
    if x0 >= x1 or y0 >= y1: return
    s = a[y0 - y:y1 - y, x0 - x:x1 - x]
    k = s[..., 3:4].astype(np.float32) / 255 * alpha
    d = dst[y0:y1, x0:x1]
    d[..., :3] = (d[..., :3] * (1 - k) + s[..., :3] * k).astype(np.uint8)
    if d.shape[2] == 4: d[..., 3] = np.maximum(d[..., 3], (k[..., 0] * 255).astype(np.uint8))


def _noise(a, k, seed):
    rng = np.random.default_rng(seed)
    n = rng.integers(-k, k + 1, a.shape[:2])[..., None]
    return np.clip(a.astype(np.int16) + n, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- small transfer decals (переводные картинки), drawn with PIL
def decal(kind, s=2):
    """tiny pixel icons, s = px per icon pixel"""
    G = {
        'star': ["..r..", ".rrr.", "rrrrr", ".rrr.", "r...r"],
        'flake': ["b.b.b", ".bbb.", "bbbbb", ".bbb.", "b.b.b"],
        'ushanka': [".gggg.", "gggggg", "gyggyg", "gs..sg", "s....s"],
        'kettle': ["..kk...", ".kkkk.k", "kkkkkkk", "kkkkkk.", ".kkkk.."],
        'heart': [".r.r.", "rrrrr", "rrrrr", ".rrr.", "..r.."],
        'sausage': ["..ppppp..", ".pppppppp", "ppppppppp", ".ppppppp."],
        'bench': ["wwwwwww", "w.....w", "wwwwwww", "w.....w"],
        'phone': [".kkkkk.", "kk...kk", ".kkkkk.", ".k.k.k.", ".kkkkk."],
        'drop': ["..b..", ".bbb.", "bbbbb", "bbbbb", ".bbb."],
        'tree': ["..g..", ".ggg.", "ggggg", ".ggg.", "ggggg", "..w.."],
        'cat': ["o...o", "ooooo", "o.o.o", "ooooo", ".ooo."],
    }
    C = dict(r=(214, 40, 44), b=(90, 150, 230), g=(110, 110, 120), y=(226, 186, 60), s=(150, 150, 160), k=(60, 60, 70),
             p=(214, 128, 120), w=(150, 104, 60), o=(240, 140, 40))
    rows = G[kind]
    im = Image.new('RGBA', (len(rows[0]) * s + 2 * s, len(rows) * s + 2 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for yy, row in enumerate(rows):
        for xx, ch in enumerate(row):
            if ch != '.':
                for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    d.rectangle([(xx + 1 + ox) * s, (yy + 1 + oy) * s, (xx + 2 + ox) * s - 1, (yy + 2 + oy) * s - 1], fill=(255, 255, 255, 255))
    for yy, row in enumerate(rows):
        for xx, ch in enumerate(row):
            if ch != '.': d.rectangle([(xx + 1) * s, (yy + 1) * s, (xx + 2) * s - 1, (yy + 2) * s - 1], fill=C[ch] + (255,))
    return im


# ---------------------------------------------------------------- photo with corner tabs
def photo(frame, w, border=8, tilt=0.0, sepia=0.0):
    """frame: RGB image (PIL); returns RGBA photo w wide (keeps aspect) with a white border and black corner tabs"""
    h = int(w * frame.height / frame.width)
    ph = frame.convert('RGB').resize((w, h), Image.LANCZOS)
    if sepia > 0:
        a = np.array(ph).astype(np.float32); g = a.mean(2, keepdims=True)
        a = a * (1 - sepia) + g * np.array([1.08, 0.95, 0.78]) * sepia
        ph = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    im = Image.new('RGBA', (w + 2 * border, h + 2 * border), (250, 248, 240, 255))
    im.paste(ph, (border, border))
    d = ImageDraw.Draw(im)
    t = max(10, w // 9)
    W_, H_ = im.size
    for (x, y, sx, sy) in ((0, 0, 1, 1), (W_ - 1, 0, -1, 1), (0, H_ - 1, 1, -1), (W_ - 1, H_ - 1, -1, -1)):
        d.polygon([(x - sx * 3, y - sy * 3), (x + sx * t, y - sy * 3), (x - sx * 3, y + sy * t)], fill=(30, 30, 34, 255))
    if tilt: im = im.rotate(tilt, resample=Image.BICUBIC, expand=True)
    return im


# ---------------------------------------------------------------- the album on the table (world px)
def closed(world):
    """closed velvet album with aluminium letters on a copy of the table world"""
    a = world.copy()
    x0, y0, x1, y1 = COVER
    a[y0 + 10:y1 + 10, x0 + 12:x1 + 12] = (a[y0 + 10:y1 + 10, x0 + 12:x1 + 12] * 0.45).astype(np.uint8)       # shadow
    a[y0:y1, x0:x1] = VELVET
    a[y0:y1, x0:x1] = _noise(a[y0:y1, x0:x1], 10, 3)
    a[y0:y0 + 6, x0:x1] = VELVET_HI; a[y1 - 6:y1, x0:x1] = VELVET_SH; a[y0:y1, x0:x0 + 22] = VELVET_SH         # spine
    im = Image.fromarray(a)
    for img, cx, cy in ((text_img(['ДМБ'], 96, (206, 210, 218), shadow=(60, 60, 70)), 640, 250),
                        (text_img(['ЗИМА • 2026'], 24, (206, 210, 218), shadow=(60, 60, 70)), 640, 380),
                        (text_img(['ВАЛЕРА И КОТ'], 24, GOLD, shadow=(80, 50, 10)), 640, 470),
                        (text_img(['ДЕМБЕЛЬСКИЙ АЛЬБОМ'], 16, GOLD, shadow=(80, 50, 10)), 640, 530)):
        b = np.array(im); paste(b, img, cx - img.width // 2, cy - img.height // 2); im = Image.fromarray(b)
    b = np.array(im)
    for (x, y) in ((x0 + 60, y0 + 50), (x1 - 80, y0 + 50), (x0 + 60, y1 - 90), (x1 - 80, y1 - 90)):
        paste(b, decal('star', 4), x, y)
    paste(b, decal('ushanka', 5), 600, 110)
    return b


def spread(world, seed=0):
    """open album: velvet edge, two cream cardboard pages, spine shadow"""
    a = world.copy()
    x0, y0, x1, y1 = SPREAD
    a[y0 + 10:y1 + 12, x0 + 12:x1 + 12] = (a[y0 + 10:y1 + 12, x0 + 12:x1 + 12] * 0.45).astype(np.uint8)
    a[y0:y1, x0:x1] = VELVET
    a[y0 + 12:y1 - 12, x0 + 12:x1 - 12] = PAGE
    a[y0 + 12:y1 - 12, x0 + 12:x1 - 12] = _noise(a[y0 + 12:y1 - 12, x0 + 12:x1 - 12], 6, seed + 7)
    for k in range(18):                                                                               # spine gutter shadow
        f = (1 - k / 18) * 0.35
        for xx in (SPINE - 1 - k, SPINE + k):
            a[y0 + 12:y1 - 12, xx] = (a[y0 + 12:y1 - 12, xx] * (1 - f)).astype(np.uint8)
    a[y0 + 12:y1 - 12, SPINE - 1:SPINE + 1] = PAGE_SH
    return a


def page_flip(dst, k, x0=SPREAD[0] + 12, x1=SPREAD[2] - 12, y0=SPREAD[1] + 12, y1=SPREAD[3] - 12, back=PAGE):
    """a page turning right -> left over the spine (k 0..1) drawn onto a world array"""
    if k <= 0 or k >= 1: return
    ang = math.pi * k
    w = (x1 - SPINE) * math.cos(ang)
    lift = int(40 * math.sin(ang))
    xe = SPINE + w
    xa, xb = (SPINE, xe) if w > 0 else (xe, SPINE)
    im = Image.fromarray(dst); d = ImageDraw.Draw(im)
    d.polygon([(SPINE, y0), (xe, y0 - lift), (xe, y1 + lift), (SPINE, y1)], fill=back if w > 0 else (226, 216, 192))
    d.line([(xe, y0 - lift), (xe, y1 + lift)], fill=(150, 140, 120), width=3)
    dst[:] = np.array(im)
    sh = int(abs(w) * 0.25) + 6                                                                      # shadow the page casts
    xs = int(xb) if w > 0 else int(xa) - sh
    xs0, xs1 = max(x0, xs), min(x1, xs + sh)
    if xs0 < xs1: dst[y0:y1, xs0:xs1] = (dst[y0:y1, xs0:xs1] * 0.82).astype(np.uint8)


# ---------------------------------------------------------------- props on the page / table
def receipt(lines, w=150, line_h=20):
    """long cash-register receipt (RGBA), Press Start 8 px"""
    f = font(8)
    h = line_h * (len(lines) + 2)
    im = Image.new('RGBA', (w, h), (246, 244, 236, 255)); d = ImageDraw.Draw(im); d.fontmode = '1'
    for i, l in enumerate(lines):
        lw = f.getlength(l)
        d.text(((w - lw) / 2, line_h * (i + 1)), l, font=f, fill=(50, 50, 60, 255))
    for x in range(0, w, 6):                                                                          # zig-zag torn ends
        d.polygon([(x, 0), (x + 3, 4), (x + 6, 0)], fill=(0, 0, 0, 0))
    a = np.array(im); a[:, :2, :3] = (210, 206, 196); a[:, -2:, :3] = (210, 206, 196)
    return Image.fromarray(a)


def trophy_bag(w=180):
    """the plastic bag (90!) framed under glass, label «ТРОФЕЙ №1»"""
    h = int(w * 1.25)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=(176, 130, 50, 255)); d.rectangle([8, 8, w - 9, h - 9], fill=(226, 196, 110, 255))
    d.rectangle([16, 16, w - 17, h - 17], fill=(214, 226, 232, 255))
    bx0, by0, bx1, by1 = 40, 40, w - 40, h - 60                                                       # the bag
    d.polygon([(bx0, by0 + 20), (bx1, by0 + 20), (bx1 - 6, by1), (bx0 + 6, by1)], fill=(250, 250, 252, 255), outline=(150, 150, 160, 255))
    d.arc([bx0 + 10, by0 - 10, bx0 + 40, by0 + 30], 180, 360, fill=(150, 150, 160, 255), width=4)
    d.arc([bx1 - 40, by0 - 10, bx1 - 10, by0 + 30], 180, 360, fill=(150, 150, 160, 255), width=4)
    d.rectangle([bx0 + 6, by0 + 40, bx1 - 6, by0 + 52], fill=(214, 40, 44, 255))
    a = np.array(im)
    lab = text_img(['90'], 16, (214, 40, 44)); paste(a, lab, (w - lab.width) // 2, by0 + 60)
    t = text_img(['ТРОФЕЙ №1'], 8, (60, 40, 20)); paste(a, t, (w - t.width) // 2, h - 46)
    for (x, y) in ((24, 22), (w - 40, 30)):                                                           # glass glare
        cv = Image.fromarray(a); dd = ImageDraw.Draw(cv); dd.line([(x, y + 30), (x + 18, y)], fill=(255, 255, 255, 230), width=3); a = np.array(cv)
    return Image.fromarray(a)


def paw_pencil(dst, tip, s=1.0, wiggle=0.0):
    """the cat's ginger paw (from the right) holding a yellow pencil whose tip is at `tip` (x, y) of an RGB array"""
    im = Image.fromarray(dst); d = ImageDraw.Draw(im)
    tx, ty = tip[0] + wiggle, tip[1]
    L = 90 * s
    ex, ey = tx + L * 0.8, ty - L * 0.6                                                               # pencil end
    d.line([(tx, ty), (ex, ey)], fill=(40, 30, 20), width=int(12 * s))
    d.line([(tx + 10 * s, ty - 7 * s), (ex, ey)], fill=(242, 196, 50), width=int(10 * s))
    d.polygon([(tx, ty), (tx + 12 * s, ty - 3 * s), (tx + 6 * s, ty - 11 * s)], fill=(226, 196, 150))
    d.ellipse([tx - 3 * s, ty - 3 * s, tx + 3 * s, ty + 3 * s], fill=GRAPHITE)
    px, py = tx + 50 * s, ty - 38 * s                                                                 # paw + arm off to the right edge
    d.line([(px, py), (px + 400 * s, py - 70 * s)], fill=(30, 20, 14), width=int(64 * s))
    d.line([(px, py), (px + 400 * s, py - 70 * s)], fill=(236, 140, 50), width=int(56 * s))
    for k in range(4):
        x = px + 90 * s + k * 70 * s
        d.line([(x, py - 40 * s - k * 12 * s), (x - 10 * s, py + 14 * s - k * 12 * s)], fill=(200, 100, 30), width=int(10 * s))
    d.ellipse([px - 34 * s, py - 30 * s, px + 34 * s, py + 30 * s], fill=(30, 20, 14))
    d.ellipse([px - 30 * s, py - 26 * s, px + 30 * s, py + 26 * s], fill=(248, 244, 236))
    for k in range(3): d.ellipse([px - 26 * s + k * 18 * s, py - 30 * s, px - 12 * s + k * 18 * s, py - 16 * s], fill=(255, 190, 190))
    dst[:] = np.array(im)
