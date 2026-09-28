"""S01E04 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen as CG
from PIL import Image

EP = 'ep04'
REF, RAW = P.build(EP, 'cover_ref.png'), P.build(EP, 'cover_ai.png')
SRC = P.episode(EP) / 'cover_ai_source.jpg'
TITLE = ['ЧЕСТНЫЙ', 'КОНЬ']
CHARS = ("LEFT - a cowboy with messy brown hair and a big brown mustache, red shirt, blue neckerchief, brown vest, NO hat, "
         "amazed with wide eyes and raised hands; RIGHT - a brown horse with a white blaze wearing a tan cowboy hat, dark "
         "sunglasses and an obviously fake big black curly mustache, standing proudly in a stall with a red velvet curtain "
         "pulled open, sparkles around. Behind them a wooden Wild West stable interior with lanterns.")


def ref():
    import ep04 as E
    from stage import view_at, Chars
    from props import chars as CH_
    v = view_at(E.INT, 1120, 470, 1.6, 180, 420)
    big = v.bg(); CH = Chars()
    E.premium_stage(CH, v, 27.0, 1.0)
    Pz = CH_.molniya_pose(27.0)
    ax, ay = E.horse_anchor(E.PREM_X, E.PREM_FEET, E.U_PREM)
    CH_.molniya(CH, v.cam(ax, ay, E.U_PREM, True), 27.0, Pz, disguise=1.0)
    E.drapes(CH, v, 1.0, 27.0)
    CH_.billy(CH, v.cam(1062, E.R.INT_FEET + 30 - CH_.HIP_H * 11, 11), CH_.POSES['excited'], 0.05, 0.0, 'amazed')
    CH.comp(big)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP) / 'cover.png', P.series() / 'covers' / 'cover_s01e04.png'], 4, TITLE)
        print('ok')
