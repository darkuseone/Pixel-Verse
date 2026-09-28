"""S01E06 race finish (xAI bg race_finish.png, 1280x720) + banner text by code. Canyon is reused from frontier."""
import os
import numpy as np
from PIL import Image
import paths as PATHS
from props.rental import _text

BG = PATHS.series() / 'bg'
FEET = 648                 # track line for riders
GATE = (500, 790)          # gate opening x
BANNER = (505, 195, 780, 262)
POST_X = 700               # foreground finish post (code)
CACTUS_X = 1010            # foreground landing cactus (code)


def build(force=False):
    cache = PATHS.build('props', 'racetrack.npz')
    if os.path.exists(cache) and not force:
        d = np.load(cache); return {k: d[k] for k in d.files}
    img = Image.open(BG / 'race_finish.png').convert('RGB')
    cx = (BANNER[0] + BANNER[2]) / 2
    img = _text(img, 'СКАЧКИ', cx, 216, 24, (120, 40, 26), (240, 220, 180), (2, 2))
    img = _text(img, 'ПРИЗ $500', cx, 246, 16, (70, 44, 24))
    q = np.array(img.quantize(colors=110, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))
    np.savez_compressed(cache, finish=q)
    return dict(finish=q)


if __name__ == '__main__':
    d = build(True); Image.fromarray(d['finish']).save(PATHS.build('props', 'finish.png')); print('ok')
