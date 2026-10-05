"""S01E06 cover (v2 cast).  python3 cover.py ref | ai | make
Environment through xAI edit (snowy Chicago side street at night, a cleared parking spot with a red ribbon on gold stanchions, steam from
the manhole, no people); heroes pasted from the sprite engine: Brad caught with the giant ribbon scissors («Ope.» face, sweat), behind him
the four neighbour ladies with a rolling pin, a frying pan, a casserole and a mop."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import stage as ST
import covergen_dibs as CG
from stage import view_at
from props import chikit as K
from props import dibscast as DC

EP, SLUG = 'ep06', 'agent-dibs'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['OPE.', 'BUSTED.']
SIZES = [132, 112]
SCENE = ("A snowy Chicago side street at night with brick two-flat houses and warm lit windows; in the middle a freshly shoveled parking "
         "spot with a red ceremonial ribbon stretched between two gold stanchions, white steam rising from a manhole, orange street lamps, "
         "snowbanks and parked cars buried in snow.")
L_HIP = (-17.0, 34.0)
LADIES = [('rose', 'casserole', (16.0, 68.0)), ('dot', 'pan', (16.0, 72.0)), ('bev', 'mop', (14.0, 64.0)), ('mrs_w', 'rolling_pin', (16.0, 72.0))]


def ref():
    import ep06 as E
    world = K.world('dibs_row')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 640.0, 400.0, Z, 180, 372)
    big = v.bg()
    CG.calm_night(big)
    E.ribbon(big, v, 0.3, 0.0)
    Image.fromarray(big).save(REF); print(REF)


def heroes(F):
    for i, (who, w, hand) in enumerate(LADIES):                                    # the ladies behind Brad, glaring
        CG.hero(F, DC.lady, (330 + i * 58, 600 + 10 * (i % 2)), 2.7, flip=True, who=who, pose='hold', t=0.3 + i, expr='glare', legs=True,
                clip_h=None, hands={'L': L_HIP, 'R': hand}, props={'R': w})
    CG.hero(F, DC.brad, (176, 560), 4.3, pose='hold', t=0.3, mouth_=0.6, expr='ope', sweat=1.0, hands={'R': (24.0, 60.0)}, props={'R': 'scissors'},
            look=0.6)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai_env(REF, RAW, SCENE)
    elif cmd == 'make':
        (P.series(SLUG) / 'covers').mkdir(exist_ok=True)
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e06.png'], 6, TITLE, SIZES, pre=heroes)
        print('ok')
