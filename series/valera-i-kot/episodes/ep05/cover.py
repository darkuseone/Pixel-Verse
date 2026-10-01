"""S01E05 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
from PIL import Image

EP, SLUG = 'ep05', 'valera-i-kot'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['ОПЕРАЦИЯ', '«КИПЯТОК»']
CHARS = ("a heavyset bald middle-aged man with a huge bushy brown walrus moustache and a red bulbous nose, wearing a grey "
         "ushanka fur hat and a blue-and-white striped sailor undershirt (telnyashka), holding a flashlight under his chin that "
         "lights his face from below like a scary story, sly determined grin, in a dark damp Soviet basement full of rusty pipes; "
         "a big red valve handwheel with a cardboard sign next to him, steam leaking from the pipes; a fat ginger cat with "
         "half-closed eyes sitting at his feet.")


def sign(F):
    """hand-lettered «НЕ ТРОГАТЬ!» on the blank cardboard the AI left next to the valve (540x960 canvas)"""
    import numpy as np
    from props import panelka as PK
    img = Image.fromarray(F)
    img = PK.text(img, 'НЕ', 493, 628, 16, (176, 28, 28))
    img = PK.text(img, 'ТРОГАТЬ!', 493, 652, 8, (176, 28, 28))
    F[:] = np.array(img)


def ref():
    import ep05 as E
    from stage import view_at
    t = 11.0
    v = view_at(E.BASE, 900, 450, 1.05, 180, 380)
    big = E.base_frame(v, t, valera=lambda CH, v_: E.v_base(CH, v_, t, expr='sly', flash='chin'),
                       cat=lambda CH, v_: E.cat_b(CH, v_, t, 760), grade=(0.55, 0.6, 0.72))
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e05.png'], 5, TITLE, extra=sign)
        print('ok')
