"""S01E05 locations from xAI backgrounds (1280x720, grok-imagine-image-2.0 medium 1k):
camp_night (campfire), canyon (chase), town_square (post + sheriff's poster board). Text on signs by code."""
import os
import numpy as np
from PIL import Image
import paths as PATHS
from props.rental import _text

BG = PATHS.series() / 'bg'
# camp
FIRE = (462, 478)            # flame base centre
TROUGH = (915, 500)
CAMP_FEET = 600
# canyon
CANYON_FEET = 684
# town
POST_X, POST_BASE = 638, 618
TOWN_FEET = 640
BOARD = (432, 342, 520, 420)  # sheriff wanted-poster board (x0,y0,x1,y1)
SUN_TOWN = (70, 170)


def town():
    img = Image.open(BG / 'town_square.png').convert('RGB')
    a = np.array(img)
    x0, y0, x1, y1 = BOARD
    a[y0 + 6:y1 - 6, x0 + 6:x1 - 6] = (238, 222, 180)                 # fresh poster on the board
    a[y0 + 6:y1 - 6, x1 - 8:x1 - 6] = (200, 176, 124)
    img = Image.fromarray(a)
    img = _text(img, 'РОЗЫСК', (x0 + x1) / 2, y0 + 16, 8, (140, 36, 26))
    a = np.array(img)
    cx = (x0 + x1) // 2
    a[y0 + 26:y0 + 33, cx - 12:cx + 12] = (46, 40, 48)                  # bandit hat
    a[y0 + 33:y0 + 46, cx - 9:cx + 9] = (226, 176, 136)                # face
    a[y0 + 36:y0 + 40, cx - 9:cx + 9] = (24, 20, 24)                   # mask
    a[y0 + 37:y0 + 39, cx - 5:cx - 3] = (240, 240, 240); a[y0 + 37:y0 + 39, cx + 3:cx + 5] = (240, 240, 240)
    a[y0 + 42:y0 + 44, cx - 4:cx + 7] = (34, 26, 24)                   # crooked mustache
    img = _text(Image.fromarray(a), '$500', cx, y1 - 18, 16, (90, 50, 30))
    return img


def build(force=False):
    cache = PATHS.build('props', 'frontier.npz')
    if os.path.exists(cache) and not force:
        d = np.load(cache); return {k: d[k] for k in d.files}
    q = lambda im: np.array(im.quantize(colors=110, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))
    out = dict(camp=q(Image.open(BG / 'camp_night.png').convert('RGB')),
               canyon=q(Image.open(BG / 'canyon.png').convert('RGB')),
               town=q(town()))
    np.savez_compressed(cache, **out)
    return out


if __name__ == '__main__':
    d = build(True)
    for k, v in d.items(): Image.fromarray(v).save(PATHS.build('props', f'{k}.png'))
    print('ok')
