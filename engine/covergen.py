"""Series cover pipeline: code-rendered reference frame -> xAI edit (grok-imagine-image-2.0, medium, 1k ≈ $0.07)
-> pixelize 540x960 / 110 colours -> big two-row plank «ПОЧТИ ДИКИЙ ЗАПАД / СЕРИЯ N/6» + title (engine/cover.py)."""
import importlib.util
import numpy as np
from PIL import Image
import paths as P
import xai

PROMPT_BASE = (
    "Redraw this image as a highly detailed HD pixel art scene from a modern indie pixel-art adventure game "
    "(crisp visible pixels, rich environment detail, warm lantern light, soft dusty light beams). Keep the same vertical "
    "composition, the same background and exactly the same cartoon characters with their colors and outfits: ")
PROMPT_END = (" Funny expressive cartoon faces. Keep the top third of the image calm for a title. "
              "No text, no letters, no numbers, no watermark.")


def engine_cover():
    spec = importlib.util.spec_from_file_location('engine_cover', P.ENGINE / 'cover.py')
    C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
    return C


def ai(ref_png, raw_png, characters):
    return xai.generate(PROMPT_BASE + characters + PROMPT_END, [raw_png], aspect='9:16', ref_png=ref_png)


def pixelize(im):
    im = im.convert('RGB')
    w, h = im.size; tw = h * 9 / 16
    if abs(w - tw) > 2: x0 = int((w - tw) / 2); im = im.crop((x0, 0, x0 + int(tw), h))
    small = im.resize((540, 960), Image.BOX)
    return np.array(small.quantize(colors=110, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))


def make(raw_png, src_jpg, out_pngs, n, title_lines):
    Image.open(raw_png).convert('RGB').save(src_jpg, quality=93)
    C = engine_cover()
    F = pixelize(Image.open(src_jpg))
    for i, yy in enumerate(range(0, 110, 22)):
        F[yy:yy + 22] = (F[yy:yy + 22].astype(np.float32) * (0.62 + 0.07 * i)).astype(np.uint8)
    yb = C.plank(F, f'ПОЧТИ ДИКИЙ ЗАПАД\nСЕРИЯ {n}/6', 138, 24)          # below the 3:4 grid crop line
    C.pixel_text(F, title_lines, yb + 22, 64, max_w=532, gap=10)
    img = Image.fromarray(F).resize((1080, 1920), Image.NEAREST)
    for o in out_pngs: img.save(o)
    return img
