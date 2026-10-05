"""S01E04 cover (v2 cast).  python3 cover.py ref | ai | make
Environment through xAI edit (Sal's hot dog stand in a blizzard, a Chicago dog and fries on the ledge, no people);
Terry pasted from the sprite engine: sweating, ketchup bottle raised over the hot dog."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import stage as ST
import covergen_dibs as CG
from stage import Chars, view_at
from props import chikit as K, chi_props as PR
from props import dibscast as DC

EP, SLUG = 'ep04', 'agent-dibs'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['NO', 'KETCHUP!']
SIZES = [130, 104]
SCENE = ("A tiny old Chicago hot dog stand at night in a snowstorm: glowing orange neon sign above the service window, warm light inside, "
         "string lights, snow on the awning; on the window ledge in the lower right a Chicago-style hot dog with bright green relish, tomato "
         "wedges, a pickle spear and yellow mustard on a poppy-seed bun, next to a red basket of fries.")


def ref():
    import ep04 as E
    world = K.world('sals_stand')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 560.0, 380.0, Z, 180, 372)
    big = v.bg()
    CG.calm_night(big)
    CH = Chars()
    PR.chicago_dog(CH, v.cam(E.DOG_X + 30, E.LEDGE_Y, 7.5), 0.3, 1.0)
    PR.fries(CH, v.cam(E.FRY_X + 70, E.LEDGE_Y, 7.5), 1.0)
    CH.comp(big, K.light_stand(v))
    Image.fromarray(big).save(REF); print(REF)


def heroes(F):
    CG.hero(F, DC.terry, (150, 610), 4.0, pose='stand', t=0.3, mouth_=0.7, expr='panic', sweat=1.0, hands={'R': (40.0, 97.0)},
            props={'R': lambda sp, h, a, tt: DC.p_ketchup(sp, h, a, tt)})


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai_env(REF, RAW, SCENE)
    elif cmd == 'make':
        (P.series(SLUG) / 'covers').mkdir(exist_ok=True)
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e04.png'], 4, TITLE, SIZES, pre=heroes)
        print('ok')
