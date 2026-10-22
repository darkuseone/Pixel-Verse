"""CTR cover 1920x1080 for «Grim Ride: ONE MORE HOUR»: Death's giant panicking skull (left, ~50 % of the height) clutching his hood;
behind him Harold's grandfather clock, its hands spinning BACKWARDS (motion arcs), and tiny Harold on the right hooking the minute hand
with his cane, sipping cocoa, smug. Bright neon violet-orange burst with the full moon. Text «AGAIN?!» top-right (the title says
«one more hour»), a small loop counter «LOOP 96». Bottom-right timestamp zone empty.
  python3 cover.py -> cover.png + cover.jpg (<= 2 MB) + cover_small.png (320x180)"""
import movie as MV
from movie import *

t = 0.4
OUTD = HERE
KEY = (255, 0, 255)


def sprite_rgba(fn, sc, size, at, flip=False, **kw):
    """the sprite drawn on a key colour canvas -> RGBA with a sticker outline (thick white + ink)"""
    can = np.zeros((size[1], size[0], 3), np.uint8); can[:] = KEY
    sp = GX.draw(fn, sc, flip=flip, hires=True, **kw)
    blit(can, sp, at[0], at[1], sc, None, flip)
    m = ~np.all(can == KEY, axis=2)
    pad = 30
    bm = np.pad(m, pad)
    d1 = O._dilate(bm, 14)[pad:-pad, pad:-pad]
    d2 = O._dilate(bm, 22)[pad:-pad, pad:-pad]
    out = np.zeros((size[1], size[0], 4), np.uint8)
    out[d2] = INK + (255,)
    out[d1] = (255, 255, 255, 255)
    out[m, :3] = can[m]; out[m, 3] = 255
    return out


# background: the hilltop night pushed to neon — a violet/orange burst around the moon, the town glowing below
v = view_at(HILL, 900, 330, 1.15, SX, SY)
bg = v.bg().astype(float)
H, W = bg.shape[:2]
g = bg.mean(2, keepdims=True)
bg = np.clip(g + (bg - g) * 1.7, 0, 255) * 1.25 + 18
yy, xx = np.mgrid[0:H, 0:W]
ang = np.arctan2(yy - 300, xx - 1250)
burst = (np.sin(ang * 14) > 0.35)[..., None]
bg = np.where(burst, bg * 0.82 + np.array((255, 120, 200)) * 0.18, bg)
for (cx, cy, c, r) in ((1250, 300, (255, 170, 60), 800), (200, 900, (180, 60, 255), 800), (1800, 900, (255, 70, 160), 600)):
    k = np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1)[..., None] ** 1.5
    bg = bg * (1 - 0.45 * k) + np.array(c) * 0.45 * k
big = np.clip(bg, 0, 255).astype(np.uint8)
big[:] = K.dof(big, 3)

# the clock (centre-right) with backwards motion arcs
clock = sprite_rgba(GP.grandfather_clock, 11.0, (520, 980), (260, 950), t=t, hh=1, mm=10)
O.overlay(big, clock, 930, 70, 1.0)
cxk, cyk = 930 + 260, 70 + 950 - int(57.5 * 11)
im = Image.fromarray(big); d = ImageDraw.Draw(im)
for r, w in ((150, 14), (190, 10), (230, 6)):
    d.arc([cxk - r, cyk - r, cxk + r, cyk + r], 200, 320, fill=(150, 255, 110), width=w)
d.polygon([(cxk - 230 * 0.94, cyk - 230 * 0.34 - 30), (cxk - 230 * 0.94 - 40, cyk - 230 * 0.34 + 20), (cxk - 230 * 0.94 + 30, cyk - 230 * 0.34 + 26)],
          fill=(150, 255, 110))
big[:] = np.array(im)

# tiny smug Harold with cocoa, right, his cane hooked on the clock hands
har = sprite_rgba(GC.harold, 7.0, (520, 720), (230, 690), flip=True, t=t, expr='sly', pose='stand', mug=True, look=(-1.0, 0.3))
O.overlay(big, har, 1360, 330, 1.0)
im = Image.fromarray(big); d = ImageDraw.Draw(im)
d.line([cxk + 20, cyk - 60, 1500, 760], fill=INK, width=26); d.line([cxk + 20, cyk - 60, 1500, 760], fill=(130, 70, 40), width=16)
big[:] = np.array(im)

# the hero: Death's giant panicking skull, left
hero = sprite_rgba(GC.grim, 14.0, (1150, 1300), (540, 1620), t=1.0, expr='panic', ride=False, pose='point', jaw_drop=1.0, shake=0.0,
                   look=(0.6, -0.2), mouth_=1.0)
O.overlay(big, hero, -110, -30, 1.0)

# text: «AGAIN?!» top-right + the loop counter
title = K.hook_title(['AGAIN?!'], 118, width=1000)
O.overlay(big, title, 900, 6, 1.0)
MV.plate(big, 'LOOP 96', 1480, 250, 40, fg=(255, 120, 90))

Image.fromarray(big).save(OUTD / 'cover.png')
Image.fromarray(big).save(OUTD / 'cover.jpg', quality=90)
Image.fromarray(big).resize((320, 180), Image.LANCZOS).save(OUTD / 'cover_small.png')
print(OUTD / 'cover.png', (OUTD / 'cover.jpg').stat().st_size // 1024, 'KB')
