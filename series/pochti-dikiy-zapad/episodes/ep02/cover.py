"""S01E02 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen as CG
from PIL import Image

EP = 'ep02'
REF, RAW = P.build(EP, 'cover_ref.png'), P.build(EP, 'cover_ai.png')
SRC = P.episode(EP) / 'cover_ai_source.jpg'
TITLE = ['Я —', 'КАКТУС.']
CHARS = ("CENTER-RIGHT - a round green barrel-cactus costume with a pink flower on top and two funny cartoon eyes looking out of a dark hole "
         "(a cowboy is hiding inside), a masked bandit in a black hat with a red band, black eye mask and crooked mustache, purple shirt is "
         "about to sit on it; LEFT - a calm brown horse wearing a tan cowboy hat standing behind a thin wooden sign post with a wanted poster "
         "and a vulture on top. Sunny Wild West desert with cacti and red mesas.")


def ref():
    import ep02 as E
    import stage as ST
    from stage import view_at, Chars
    t = 18.6
    v = view_at(E.FIELD, 620, 520, 1.15, 180, 470)
    ST.set_px(1); big = v.bg(); CH, FX = Chars(), Chars()
    E.scene(CH, FX, big, v, t)
    CH.comp(big, E.light()); FX.comp(big)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP) / 'cover.png', P.series() / 'covers' / 'cover_s01e02.png'], 2, TITLE)
        print('ok')
