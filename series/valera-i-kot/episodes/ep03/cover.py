"""S01E03 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
from PIL import Image

EP, SLUG = 'ep03', 'valera-i-kot'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['ОНИ ВИДЯТ', 'ВСЁ']
CHARS = ("two old Russian grandmothers sitting on a snowy wooden bench by the entrance of an old apartment block at night: LEFT a thin "
         "granny with a tall brown fur hat, huge round glasses glinting and a sharp nose, dark coat with a fur collar, staring with a "
         "suspicious smirk; RIGHT a round granny wrapped in a big grey wool shawl with rosy cheeks, knitting red yarn. In the "
         "foreground a heavyset man with a huge brown walrus moustache and a red nose crawls on his belly through the snow hidden "
         "under a white bedsheet, only his face and grey ushanka peeking out, looking worried. Snow falling, warm lamp above the door.")


def ref():
    import ep03 as E
    from stage import view_at
    t = 9.2
    import numpy as np
    from props import panelka as PK
    from PIL import Image as I
    E.BENCH = PK.q(I.open(PK.BG / 'bench.png').convert('RGB'))          # no notice text on the cover (AI would garble it)
    E.crawl_x = lambda tt: 560.0
    v = view_at(E.BENCH, 780, 470, 1.0, 180, 420)
    big = E.bench_frame(v, t, ('grannies',), valera=lambda CH, v_: E.prone(CH, v_, t, 0.0),
                        zina_kw=dict(look=-1.0, expr='smug'))
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e03.png'], 3, TITLE)
        print('ok')
