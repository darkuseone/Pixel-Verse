"""S01E05 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen as CG
from PIL import Image

EP = 'ep05'
REF, RAW = P.build(EP, 'cover_ref.png'), P.build(EP, 'cover_ai.png')
SRC = P.episode(EP) / 'cover_ai_source.jpg'
TITLE = ['ПОЧТИ', 'ПОЙМАЛ']
CHARS = ("LEFT - a boastful cowboy with messy brown hair and a big brown mustache, red shirt, blue neckerchief, brown vest, "
         "NO hat, arms raised in triumph; CENTER - a polite masked bandit in a black hat with a red band, black eye mask and "
         "crooked black mustache, purple shirt, tied to a wooden post with rope, looking sideways at the horse; RIGHT - a brown "
         "horse with a white blaze WEARING A TAN COWBOY HAT, deadpan half-closed eyes, looking at the camera. Behind them a Wild West "
         "town square at golden hour with a sheriff's office and a wanted poster, warm sunset light.")


def ref():
    import ep05 as E
    import stage as ST
    from stage import view_at, Chars
    v = view_at(E.TOWN, 655, 500, 1.3, 180, 440)
    ST.set_px(1)
    big = v.bg(); CH, FX = Chars(), Chars()
    E.town_scene(CH, FX, big, v, 22.5, ('billy', 'sam', 'mol'))
    CH.comp(big, E.light_for('town', v, 22.5)); E.frame_fx('town', big, v, 22.5, FX)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP) / 'cover.png', P.series() / 'covers' / 'cover_s01e05.png'], 5, TITLE)
        print('ok')
