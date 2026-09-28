"""Pixel canvas for code-drawn backgrounds: flat material colours + MAT/EMIT maps, then a stepped
(Bayer-dithered) lighting pass. Same technique as engine/saloon_keyframe.py, but reusable per section."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as PATHS

BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16.0
MAT_CHAR = 2          # "hero" material: flat light, no dither


def C(*c): return np.array(c, np.float32)


class Canvas:
    def __init__(s, W, H, seed=0):
        s.W, s.H = W, H
        s.YY, s.XX = [a.astype(np.float32) + 0.5 for a in np.mgrid[0:H, 0:W]]
        s.F = np.zeros((H, W, 3), np.float32)
        s.MAT = np.zeros((H, W), np.int16)
        s.EMIT = np.zeros((H, W), np.float32)
        s.A = np.ones((H, W), bool)       # coverage (for sprites)
        s.rng = np.random.default_rng(seed)

    # ---------------------------------------------------------------- primitives
    def rect(s, x0, y0, x1, y1, col, mat=0, emit=0.0):
        x0, y0, x1, y1 = int(max(0, x0)), int(max(0, y0)), int(min(s.W, x1)), int(min(s.H, y1))
        if x0 >= x1 or y0 >= y1: return
        s.F[y0:y1, x0:x1] = col; s.MAT[y0:y1, x0:x1] = mat; s.EMIT[y0:y1, x0:x1] = emit; s.A[y0:y1, x0:x1] = True

    def put(s, m, col, mat=0, emit=0.0):
        s.F[m] = col; s.MAT[m] = mat; s.EMIT[m] = emit; s.A[m] = True

    def ellm(s, cx, cy, rx, ry): return ((s.XX - cx) / rx) ** 2 + ((s.YY - cy) / ry) ** 2 <= 1

    def poly(s, pts):
        img = Image.new('L', (s.W, s.H), 0); ImageDraw.Draw(img).polygon([tuple(map(float, p)) for p in pts], fill=1)
        return np.array(img).astype(bool)

    def linem(s, x0, y0, x1, y1, w=1):
        img = Image.new('L', (s.W, s.H), 0); ImageDraw.Draw(img).line((x0, y0, x1, y1), fill=1, width=w)
        return np.array(img).astype(bool)

    def line(s, x0, y0, x1, y1, col, w=1, mat=0):
        s.put(s.linem(x0, y0, x1, y1, w), col, mat)

    def textm(s, txt, cx, cy, size):
        f = ImageFont.truetype(PATHS.FONT_PX, size); bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        img = Image.new('L', (s.W, s.H), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text((int(cx - tw / 2) - bb[0], int(cy - th / 2) - bb[1]), txt, font=f, fill=255)
        return np.array(img) > 127

    def text(s, txt, cx, cy, size, col, shadow=None, emit=0.0):
        m = s.textm(txt, cx, cy, size)
        if shadow is not None: s.put(np.roll(np.roll(m, 1, 0), 1, 1) & ~m, shadow)
        s.put(m, col, emit=emit)

    # ---------------------------------------------------------------- materials
    def planks_v(s, x0, x1, y0, y1, pw, base, seed=0, seam=None):
        r = np.random.default_rng(seed); F = s.F
        x = x0
        while x < x1:
            w = pw + r.integers(-2, 3)
            tone = base + r.uniform(-9, 9)
            s.rect(x, y0, x + w, y1, tone)
            for g in range(r.integers(2, 4)):
                gx = x + r.integers(2, max(3, w - 2)); ph = r.uniform(0, 6)
                ys = np.arange(y0, y1)
                xs = (gx + 1.2 * np.sin(ys * 0.07 + ph)).astype(int)
                ok = (xs >= x) & (xs < min(x + w, s.W)) & (xs >= 0)
                F[ys[ok], xs[ok]] = tone * 0.86
            for k in range(r.integers(0, 2)):
                ky = r.integers(y0 + 6, max(y0 + 7, y1 - 6)); kx = x + w // 2
                F[s.ellm(kx, ky, 1.8, 2.6)] = tone * 0.7
            if 0 <= x < s.W: F[y0:y1, x] = (seam if seam is not None else tone * 0.55)
            x += w

    def floor(s, y0, vpx, vpy, base=C(128, 82, 48), line_col=C(76, 46, 28), seam_col=C(96, 60, 36), dust=160):
        H, W = s.H, s.W
        for y in range(y0, H):
            s.F[y, :] = base * (0.9 + 0.1 * (y - y0) / (H - y0))
        for k in range(-24, 25):
            xb = vpx + k * 34
            s.line(vpx + (xb - vpx) * (y0 - vpy) / (H - vpy), y0, xb, H, line_col)
        yy, step = y0, 7
        while yy < H:
            s.rect(0, int(yy), W, int(yy) + 1, seam_col); yy += step; step *= 1.22
        for i in range(dust):
            x, y = int(s.rng.integers(0, W)), int(s.rng.integers(y0 + 2, H))
            s.F[y, x] = C(196, 150, 96) if i % 3 else C(90, 56, 34)

    # ---------------------------------------------------------------- lighting
    def glow(s, cx, cy, r, amp):
        d = np.sqrt((s.XX - cx) ** 2 + (s.YY - cy) ** 2) / r
        return amp * np.clip(1 - d, 0, 1) ** 1.6

    def beam(s, bx0, by0, bdx, bdy, w0=30, grow=0.12, amp=0.28, reach=700):
        t = ((s.XX - bx0) * bdx + (s.YY - by0) * bdy) / (bdx * bdx + bdy * bdy)
        px, py = bx0 + t * bdx, by0 + t * bdy
        dist = np.sqrt((s.XX - px) ** 2 + (s.YY - py) ** 2)
        m = (t > 0) & (dist < w0 + grow * t)
        return m, m * amp * np.clip(1 - t / reach, 0, 1)

    def lit(s, Lm, beams=(), dust_seed=5):
        """stepped + dithered light; heroes (MAT_CHAR) flat; emissive untouched. Returns float image."""
        H, W = s.H, s.W
        bay = np.tile(BAYER4, (H // 4 + 1, W // 4 + 1))[:H, :W]
        steps = 6
        Lq = np.floor(np.clip(Lm, 0.05, 1.35) * steps + (bay - 0.5) * 0.45) / steps
        Lsm = np.floor(np.clip(Lm, 0.05, 1.35) * 3 + 0.5) / 3
        one = np.ones_like(Lq)
        warm = np.stack([one * 1.06, one * 0.98, one * 0.86], -1)
        cool = np.stack([one * 0.82, one * 0.86, one * 1.06], -1)
        tint = np.where((Lq > 0.75)[..., None], warm, np.where((Lq < 0.5)[..., None], cool, 1.0))
        chars = s.MAT == MAT_CHAR
        tint = np.where(chars[..., None], 1.0, tint)
        Lq = np.where(chars, np.clip(Lsm, 0.8, 0.95), Lq)
        out = s.F * Lq[..., None] * 1.15 * tint
        out = np.where(s.EMIT[..., None] > 0, s.F, out)
        r = np.random.default_rng(dust_seed)
        for m in beams:
            d = m & (r.random((H, W)) > 0.994)
            out[d] = out[d] * 0.4 + 170
        return np.clip(out, 0, 255)


def quantize(img_u8, colors=110):
    q = Image.fromarray(img_u8).quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    return np.array(q.convert('RGB'))
