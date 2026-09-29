"""S01E04 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
from PIL import Image

EP, SLUG = 'ep04', 'valera-i-kot'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['ВЫ 143-Й']
CHARS = ("a heavyset bald middle-aged man with a thin comb-over, huge bushy brown walrus moustache, red bulbous nose, heavy "
         "three-day stubble and tired bloodshot eyes, wearing a blue-and-white striped sailor undershirt (telnyashka), pressing an "
         "old beige telephone handset to his ear, furious and exhausted, sitting in a shabby Soviet kitchen at night; a wall clock "
         "and a kettle behind him; a fat ginger cat with half-closed eyes asleep on the radiator in the background.")


def ref():
    import ep04 as E
    from stage import view_at
    t = 16.0
    v = view_at(E.KIT, 1000, 382, 1.45, 180, 420)
    big = E.kitchen_frame(v, t, 'angry', stubble=1.0)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e04.png'], 4, TITLE)
        print('ok')
