"""S01E06 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen as CG
from PIL import Image

EP = 'ep06'
REF, RAW = P.build(EP, 'cover_ref.png'), P.build(EP, 'cover_ai.png')
SRC = P.episode(EP) / 'cover_ai_source.jpg'
TITLE = ['РЕВАНШ']
CHARS = ("LEFT - a brown horse with a white blaze WEARING A TAN COWBOY HAT galloping with a cowboy rider (messy brown hair, big "
         "brown mustache, red shirt, blue neckerchief, NO hat) shouting heroically; RIGHT - a grey donkey ridden by a polite masked "
         "bandit in a black hat with a red band, black eye mask and crooked black mustache, purple shirt, holding a money sack, "
         "smirking. Dust clouds, speed and excitement. Behind them a Wild West race finish gate with a banner and bunting flags.")


def ref():
    import ep06 as E
    import stage as ST
    from stage import view_at, Chars
    t = 12.0
    v = view_at(E.FIN, 665, 470, 1.35, 180, 440)
    ST.set_px(1); big = v.bg(); CH, FX = Chars(), Chars()
    E.finish_scene(CH, FX, big, v, t, ('mol', 'sam'))
    CH.comp(big, E.light('finish')); FX.comp(big)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP) / 'cover.png', P.series() / 'covers' / 'cover_s01e06.png'], 6, TITLE)
        print('ok')
