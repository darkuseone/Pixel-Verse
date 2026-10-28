"""16:9 CTR thumbnail helpers (owner 28.10.2026, after YouTube CTR 0.86-0.97 % on both RU movies):
one huge emotional face, bright pixel sunburst, sticker outlines, 1-2 huge words, bottom-right timestamp corner empty.
  rgba(draw)        hero(es) drawn by a rig into a Chars canvas -> RGBA 1920x1080 (mask taken before comp() clears it)
  sticker(a)        thick white + dark outline around an RGBA cut-out
  sunburst(...)     pixelized radial rays background
  save(big, dir, n) -> n.png, n.jpg (<= 2 MB), n_small.png (320x180)"""
import math
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
import overlays as O


def rgba(draw, begin):
    CH, _ = begin()
    draw(CH)
    big = np.zeros((ST.OUT_H, ST.OUT_W, 3), np.uint8)
    f = ST.UP * CH.k
    m = np.repeat(np.repeat(CH.m, f, 0), f, 1)
    CH.comp(big)
    out = np.zeros((ST.OUT_H, ST.OUT_W, 4), np.uint8)
    out[..., :3] = big; out[m, 3] = 255
    return out


def boost(a, sat=1.25, gain=1.05):
    c = a[..., :3].astype(float); g = c.mean(2, keepdims=True)
    a[..., :3] = np.clip((g + (c - g) * sat) * gain, 0, 255).astype(np.uint8)
    return a


def sticker(a, white=10, dark=17):
    m = a[..., 3] > 0
    P = dark + 4
    mp = np.pad(m, P)
    dw = O._dilate(mp, white)[P:-P, P:-P]
    dd = O._dilate(mp, dark)[P:-P, P:-P]
    out = a.copy()
    out[dd & ~m] = (28, 16, 12, 255)
    out[dw & ~m] = (255, 255, 255, 255)
    return out


def sunburst(W, H, c, cols, rays=20, px=8, core=(255, 244, 170), core_r=260, rot=0.0):
    yy, xx = np.mgrid[0:H, 0:W]
    yy = (yy // px) * px + px / 2; xx = (xx // px) * px + px / 2
    ang = (np.arctan2(yy - c[1], xx - c[0]) + rot) % (2 * math.pi)
    k = (ang / (2 * math.pi) * rays).astype(int) % len(cols)
    out = np.array(cols, np.uint8)[k]
    r = np.hypot(xx - c[0], yy - c[1])
    g = np.clip(1 - r / core_r, 0, 1)[..., None] ** 0.8
    out = out * (1 - g) + np.array(core) * g
    e = np.clip((r - 700) / 900, 0, 1)[..., None]                      # darker towards the edges = depth
    return np.clip(out * (1 - 0.35 * e), 0, 255).astype(np.uint8)


def pixel_text(txt, size, fg, bg=None, pad=10, border=None, bw=6, font=None):
    f = font or O.pfont(size)
    bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
    im = Image.new('RGBA', (w + 2 * bw, h + 2 * bw), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    if bg is not None: d.rectangle([0, 0, im.width - 1, im.height - 1], fill=bg + (255,), outline=(border or bg) + (255,), width=bw)
    d.text((bw + pad - bb[0], bw + pad - bb[1]), txt, font=f, fill=fg + (255,))
    return np.array(im)


def rot(a, deg):
    return np.array(Image.fromarray(a).rotate(deg, resample=Image.NEAREST, expand=True))


def save(big, d, name):
    im = Image.fromarray(big)
    im.save(d / f'{name}.png')
    im.resize((320, 180), Image.LANCZOS).save(d / f'{name}_small.png')
    q = 92
    while True:
        im.save(d / f'{name}.jpg', quality=q)
        if (d / f'{name}.jpg').stat().st_size <= 2_000_000 or q < 60: break
        q -= 4
    print(d / f'{name}.jpg', (d / f'{name}.jpg').stat().st_size // 1024, 'KB')


AI_PROMPT = ("Redraw this image as a bold, ultra-clickable YouTube thumbnail in crisp HD pixel art (modern indie pixel-art game style, "
             "visible chunky pixels, thick dark outlines, white sticker outline around the characters, saturated warm colours, strong "
             "contrast, glossy highlights). Keep exactly the same composition, the same cartoon characters with the same outfits, colours "
             "and props, but push the facial emotion to the maximum: ")
AI_END = (" Keep the warm yellow-orange-red sunburst background. Keep the top-right area simple for a title. "
          "No text, no letters, no numbers, no watermark.")


def ai_versions(scene, d, emotion, n=2, logical=(640, 360), colors=128, fresh=False):
    """code scene (no title) -> xAI edit (grok-imagine-image-2.0, ~$0.07 each) -> pixelized back into the series grid.
    Returns list of 1920x1080 arrays (titles are added by the caller, in code). Existing raws are reused unless fresh."""
    import xai
    ref = d / 'cover_xai_ref.png'
    Image.fromarray(scene).save(ref)
    raws = [d / f'cover_xai_raw{i + 1}.png' for i in range(n)]
    if fresh or not all(r.exists() for r in raws):
        xai.generate(AI_PROMPT + emotion + AI_END, [str(r) for r in raws], aspect='16:9', ref_png=str(ref))
    out = []
    for r in raws:
        im = Image.open(r).convert('RGB').resize(logical, Image.BOX)
        im = im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
        out.append(np.array(im.resize((scene.shape[1], scene.shape[0]), Image.NEAREST)))
    return out
