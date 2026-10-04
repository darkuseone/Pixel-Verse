"""S01E05 cover (v2 cast).  python3 cover.py ref | ai | make
Environment through xAI edit (Chicago river canyon at night in a blizzard, no people);
Dibs pasted from the sprite engine: flying diagonally, both arms up on the briefcase, cheeks and tears blown back by the wind."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import paths as P
import stage as ST
import covergen_dibs as CG
from stage import view_at
from props import chikit as K
from props import dibscast as DC

EP, SLUG = 'ep05', 'agent-dibs'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ["DON'T", 'LET GO!']
SIZES = [124, 112]
SCENE = ("The Chicago river at night in a howling blizzard seen from above the water: tall skyscrapers with hundreds of lit windows rise on both "
         "banks like a canyon, a red-and-white bascule bridge with orange lamps crosses the river in the lower part, the dark green river "
         "reflects the city lights, strong wind blows the snow sideways in long streaks.")


def ref():
    world = K.world('skyline_river')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 640.0, 360.0, Z, 180, 372)
    big = v.bg()
    CG.calm_night(big)
    K.wind_snow(big, 0.3, 0.8)
    Image.fromarray(big).save(REF); print(REF)


def streaks(F, seed=5, n=34):
    """chunky white wind streaks (pixel speed lines) blowing right-to-left behind the hero"""
    r = np.random.default_rng(seed)
    for _ in range(n):
        y = int(r.uniform(300, 900)); x = int(r.uniform(-40, 540)); L = int(r.uniform(40, 150)); h = int(r.choice((2, 4)))
        a = r.uniform(0.35, 0.8)
        reg = F[y:y + h, max(0, x):max(0, min(540, x + L))]
        reg[:] = (reg * (1 - a) + np.array((236, 242, 255)) * a).astype(np.uint8)


def heroes(F):
    streaks(F)
    CG.hero(F, DC.dibs, (252, 606), 4.2, pose='arms_up', hands={'R': (32.0, 110.0)}, props={'R': 'briefcase'}, t=0.3, mouth_=0.85,
            expr='wind', wind=1.0, rot=-38.0, pivot=(0.0, 60.0))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai_env(REF, RAW, SCENE)
    elif cmd == 'make':
        (P.series(SLUG) / 'covers').mkdir(exist_ok=True)
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e05.png'], 5, TITLE, SIZES, pre=heroes)
        print('ok')
