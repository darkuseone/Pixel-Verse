"""S01E01 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen as CG
from PIL import Image

EP = 'ep01'
REF, RAW = P.build(EP, 'cover_ref.png'), P.build(EP, 'cover_ai.png')
SRC = P.episode(EP) / 'cover_ai_source.jpg'
TITLE = ['САМЫЙ', 'БЫСТРЫЙ?']
CHARS = ("a brown horse galloping fast, ridden by a proud cowboy wearing a tan cowboy hat (messy brown hair, big brown mustache, red shirt, "
         "blue neckerchief) yelling with one arm raised. Dust clouds and speed lines behind them. Sunny Wild West desert with red rock mesas "
         "and a big green cactus ahead.")


def ref():
    import ep01 as E
    import stage as ST
    from stage import view_at, Chars
    t = 3.2
    v = view_at(E.ROAD, E.mol_x(t) + 60, 470, 1.3, 180, 440)
    ST.set_px(1); big = v.bg(); CH, FX = Chars(), Chars()
    E.scene(CH, FX, big, v, t)
    CH.comp(big, E.light()); FX.comp(big)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP) / 'cover.png', P.series() / 'covers' / 'cover_s01e01.png'], 1, TITLE)
        print('ok')
