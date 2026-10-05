"""S01E03 cover (v2 cast).  python3 cover.py ref | ai | make
Environment through xAI edit (street under the L, potholes, the Bureau sedan chasing the villains' SUV, no people);
Dibs pasted from the sprite engine, shouting and pointing ahead."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import stage as ST
import covergen_dibs as CG
from stage import Chars, view_at
from props import chikit as K, chi_props as PR
from props import dibscast as DC

EP, SLUG = 'ep03', 'agent-dibs'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['12 MPH', 'CHASE!']
SIZES = [112, 118]
SCENE = ("Snowy Chicago avenue at night under the elevated train tracks (steel girders, welding sparks), warehouses with rolled-down shutters, "
         "huge potholes full of icy water in the road; in the lower right a rusty beige 1990s sedan with BUREAU on the door chasing a black SUV "
         "with dark windows; both cars empty, exhaust puffs in the cold air.")


def ref():
    import ep03 as E
    world = K.world('avenue_under_L')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 620.0, 420.0, Z, 180, 372)
    big = v.bg()
    CG.calm_night(big)
    for cx, cy, rx, ry in E.SMALL_HOLES + [E.BIG]: E.draw_hole(big, v, cx, cy + 40, rx, ry, 0.3)
    CH = Chars()
    PR.suv(CH, v.cam(760.0, 600.0, 4.2), 0.3, drivers=(), signal=True)
    PR.sedan(CH, v.cam(640.0, 640.0, 5.4), 0.3, drivers=(), text='BUREAU')
    CH.comp(big, K.light_avenue(v))
    Image.fromarray(big).save(REF); print(REF)


def heroes(F):
    CG.hero(F, DC.dibs, (178, 640), 4.0, pose='point', t=0.3, mouth_=0.95, expr='shout', shades=True, flap=0.6, hands={'R': (46.0, 62.0)})


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai_env(REF, RAW, SCENE)
    elif cmd == 'make':
        (P.series(SLUG) / 'covers').mkdir(exist_ok=True)
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e03.png'], 3, TITLE, SIZES, pre=heroes)
        print('ok')
