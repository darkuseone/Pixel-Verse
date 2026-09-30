"""Cover for the feature cut (1920x1080).  python3 cover.py ref | ai | make"""
from shots import *
import xai
import covergen_us as CG
from covergen2 import pixelize  # noqa (portrait helper unused; we quantize here)

OUT = pathlib.Path(P.build('movie', 'cover_ref.png')).parent
REF, RAW = OUT / 'cover_ref.png', OUT / 'cover_ai.png'
SRC = HERE / 'cover_ai_source.jpg'
CHARS = ("on the left a smug sunburnt Florida man with a bleached blond mullet, white president's sun visor with a pink stripe, teal Hawaiian shirt, holding a big clipboard titled FINES, "
         "grinning; on the right a horrified sweating woman with a frosted blonde bob, white sun visor and mint-green polo shirt, holding a pink notice with the number $250; "
         "in the lower middle a green alligator head peeking out of a pond with a bored half-closed yellow eye. Pastel Florida suburb with a pond and palm trees behind them.")


def fines_board(L, h): UP.clipboard(L, h, -0.12, w=4.6, hh=6.2, title='FINES')
def notice250(L, h): UP.notice(L, h, -0.2, 5.4, 6.8, '$250')


def ref():
    ctx = None
    cast = [dict(who='dale', x=450, y=602, u=13.0, pose=U.DPOSE['hold'], hand_n=U.H(6.4, 12.4), prop_n=fines_board, expr='smug', visor=True, mute=True),
            dict(who='brenda', x=790, y=602, u=13.0, flip=True, pose=U.BPOSE['stand'], hand_n=U.H(3.4, 12.4), prop_n=notice250, expr='shock', sweat=1.0, mute=True)]
    def before(C, v, t, u): U.earl(C, v.cam(640.0, 478.0, 9.0), 0.3, 0.0, 0.5, (0.0, 0.0), None, 0.0, 1.0, True)
    big = scene(None, 0.3, 0.0, 1.0, 'yard', cast, (620, 340, 1.0), before=before, vig=0.2)
    Image.fromarray(big).save(REF); print(REF)


def ai():
    xai.generate("Redraw this image as a highly detailed, vivid, saturated HD pixel art scene from a modern indie pixel-art adventure game (crisp visible pixels, rich environment detail, "
                 "warm tropical Florida sunlight). Keep the same wide 16:9 composition, the same background and exactly the same cartoon characters with their colors and outfits: " + CHARS +
                 " Funny, very expressive cartoon faces, large and clear. Keep the top third of the image calm and simple (sky and treetops) for a title. No text, no letters, no numbers, no watermark.",
                 [str(RAW)], aspect='16:9', ref_png=str(REF))


def make():
    Image.open(RAW).convert('RGB').save(SRC, quality=93)
    im = Image.open(SRC).convert('RGB').resize((960, 540), Image.BOX)
    F = np.array(im.quantize(colors=110, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))
    big = np.array(Image.fromarray(F).resize((1920, 1080), Image.NEAREST))
    for yy in range(0, 300, 6):
        big[yy:yy + 6] = (big[yy:yy + 6].astype(np.float32) * (0.72 + 0.28 * yy / 300)).clip(0, 255).astype(np.uint8)
    ti = O.neon_title(['FLORIDA MAN', 'VS. THE HOA'], 124, width=1920)
    O.overlay(big, ti, 0, 18, 1.0)
    # plank
    txt = 'THE COMPLETE SEASON  •  ALL 6 EPISODES'
    f = O.pfont(30); bb = f.getbbox(txt); w = bb[2] - bb[0] + 70; h = 84
    pl = np.zeros((h, w, 4), np.uint8); pl[..., :3] = (18, 4, 44); pl[..., 3] = 255
    pl[5:-5, 5:-5, :3] = (0, 214, 232); pl[9:-9, 9:-9, :3] = (255, 72, 176); pl[9:15, 9:-9, :3] = (255, 150, 214)
    O.overlay(big, pl, 40, 1080 - h - 34, 1.0)
    ptext(big, txt, 40 + w // 2, 1080 - h - 34 + h // 2, 30, (255, 255, 255), (40, 10, 88))
    for o in (HERE / 'cover.png',): Image.fromarray(big).save(o)
    Image.fromarray(big).convert('RGB').save(HERE / 'cover.jpg', quality=90)
    print(HERE / 'cover.png')


if __name__ == '__main__':
    {'ref': ref, 'ai': ai, 'make': make}[sys.argv[1]]()
