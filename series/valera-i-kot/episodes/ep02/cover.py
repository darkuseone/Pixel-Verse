"""S01E02 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
from PIL import Image

EP, SLUG = 'ep02', 'valera-i-kot'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['СКОЛЬКО?!']
CHARS = ("LEFT in the foreground: a heavyset middle-aged man with a huge bushy brown walrus moustache and a red bulbous nose, "
         "wearing a grey fur ushanka hat and a green camouflage jacket, eyes bulging in shock, mouth wide open; RIGHT behind the "
         "checkout counter: a bored blonde cashier woman with a big curly perm, heavy blue eyeshadow, red lipstick and a burgundy "
         "vest, blowing a big pink bubble gum bubble; an old cash register with a small blank green display between them, shelves "
         "of jars and cans behind, cold fluorescent light of an old grocery store.")


def ref():
    import ep02 as E
    from stage import View
    t = 2.9
    E.VX, E.VY, E.VU = 880.0, 720.0, 23.0                     # bring the two faces closer for the cover
    E.TX, E.TY = 1135.0, 625.0
    v = View(E.SHOP, 800, 0, 1.0, oy=190)
    big = E.shop_frame(v, t, ('valera', 'tamara'), 'shock', 'stand', texpr='bored', tkw=dict(gum=0.8))
    big[:190 * 3] = (big[190 * 3:190 * 3 + 1] * 0.5).astype(big.dtype)       # calm dark band for the title
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e02.png'], 2, TITLE,
                extra=lambda F: CG.lcd(F, '289', 400, 470, 40))
        print('ok')
