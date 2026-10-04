"""S01E02 cover (v2 cast).  python3 cover.py ref | ai | make
Environment through xAI edit (no people), heroes pasted from the sprite engine (ghost Dibs + Gary with the sandwich)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import stage as ST
import covergen_dibs as CG
from stage import view_at
from props import chikit as K
from props import dibscast as DC

EP, SLUG = 'ep02', 'agent-dibs'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['FREE', 'TRIAL?']
SIZES = [118, 112]
SCENE = ("Luxurious villain skyscraper lobby at night: black-and-white checkered marble floor, cyan and magenta neon light strips, a gold elevator "
         "door in the back, a mezzanine with a gold rail, a big window with a night skyline.")


def ref():
    world = K.world('lair_lobby')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 640.0, 420.0, Z, 180, 372)
    big = v.bg()
    CG.calm_night(big)
    Image.fromarray(big).save(REF); print(REF)


def heroes(F):
    CG.hero(F, DC.gary, (392, 676), 3.6, flip=True, pose='hold', t=0.3, mouth_=0.6, expr='shock', badge=True,
            props={'R': lambda sp, h, a, tt: DC.p_sandwich(sp, h, a, tt, bites=1)})
    CG.hero(F, DC.dibs, (176, 640), 4.0, ghost=0.7, pose=DC.walk('tiptoe', 0.4), t=0.3, mouth_=0.8, expr='shock', shades=False, sweat=0.6,
            props={'R': lambda sp, h, a, tt: DC.p_shovel(sp, h, a, tt, a=-0.9)})


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai_env(REF, RAW, SCENE)
    elif cmd == 'make':
        (P.series(SLUG) / 'covers').mkdir(exist_ok=True)
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e02.png'], 2, TITLE, SIZES, pre=heroes)
        print('ok')
