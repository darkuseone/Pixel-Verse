"""S01E03 cover: code-rendered reference frame -> xAI grok-imagine-image-2.0 (edit, best quality) -> pixelized
(540x960, shared palette) -> series plank + title by code.
  python3 cover.py ref        # build/ep03/cover_ref.png (free)
  python3 cover.py ai [n]     # calls xAI (costs), saves variants to build/ep03/cover_ai_K.png
  python3 cover.py make K     # final cover from variant K -> episodes/ep03/cover.png (+ keeps the AI source jpg)
Key: XAI_API_KEY (never printed)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import base64, json, os, subprocess, urllib.request
import numpy as np
from PIL import Image
import paths as P

EP = 'ep03'
TITLE = ['ИНФОРМАТОР?']
BADGE = 'ПОЧТИ ДИКИЙ ЗАПАД • 3/6'
SRC = P.episode(EP) / 'cover_ai_source.jpg'
PROMPT = (
    "Redraw this image as a highly detailed HD pixel art scene from a modern indie pixel-art adventure game "
    "(crisp visible pixels, rich environment detail, warm oil-lamp light, soft light beams with dust). "
    "Keep the same vertical composition, the same wild-west saloon interior and exactly the same three cartoon characters "
    "with their colors and outfits: LEFT - a boastful cowboy with messy brown hair and a big brown mustache, red shirt, "
    "blue neckerchief, brown vest, NO hat, leaning in with a suspicious sly look; MIDDLE - a polite bandit wearing a black "
    "hat with a red band, a black eye mask, black crooked mustache and a purple shirt, sitting at a round wooden table and "
    "hiding his face behind a small cream paper menu card; RIGHT - a brown horse with a white blaze wearing a tan cowboy hat, "
    "deadpan half-closed eyes, unimpressed. On the table: a money sack and two carrots. Funny cartoon expressions. "
    "Keep the top third of the image calm (wooden wall) for a title. No text, no letters, no numbers, no watermark, no signs with writing."
)


def ref():
    import ep03 as E
    v = E.view_at(598, 478, 1.75, 180, 420)
    CH = E.Chars()
    big, xs, ys = E.bg(v)
    E.corner_scene(CH, v, 23.8)
    CH.comp(big)
    out = P.build(EP, 'cover_ref.png'); Image.fromarray(big).save(out); print(out)


def ai(n=2):
    img = open(P.build(EP, 'cover_ref.png'), 'rb').read()
    body = {'model': 'grok-imagine-image-2.0', 'prompt': PROMPT, 'n': n,
            'image': {'url': 'data:image/png;base64,' + base64.b64encode(img).decode(), 'type': 'image_url'},
            'aspect_ratio': '9:16', 'resolution': '2k', 'quality': 'medium', 'response_format': 'b64_json'}
    req = urllib.request.Request('https://api.x.ai/v1/images/edits', json.dumps(body).encode(),
                                 {'Authorization': 'Bearer ' + os.environ['XAI_API_KEY'], 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code}: {e.read()[:600]!r}')
    for k, it in enumerate(d['data']):
        out = P.build(EP, f'cover_ai_{k}.png')
        open(out, 'wb').write(base64.b64decode(it['b64_json']))
        print(out, Image.open(out).size)
    print('usage:', {k: v for k, v in d.items() if k not in ('data',)})


def pixelize(im):
    im = im.convert('RGB')
    w, h = im.size; tw = h * 9 / 16
    if abs(w - tw) > 2: x0 = int((w - tw) / 2); im = im.crop((x0, 0, x0 + int(tw), h))
    small = im.resize((540, 960), Image.BOX)
    q = small.quantize(colors=110, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    return np.array(q)


def make(k):
    raw = P.build(EP, f'cover_ai_{k}.png')
    Image.open(raw).convert('RGB').save(SRC, quality=93)
    import cover as C                       # engine/cover.py (series plank + pixel title), 540x960 grid
    F = pixelize(Image.open(SRC))
    for i, yy in enumerate(range(0, 110, 22)):
        F[yy:yy + 22] = (F[yy:yy + 22].astype(np.float32) * (0.62 + 0.07 * i)).astype(np.uint8)
    C.plank(F, BADGE, 134, 16)
    C.pixel_text(F, TITLE, 206, 64, max_w=512, gap=10)
    img = Image.fromarray(F).resize((1080, 1920), Image.NEAREST)
    out = P.episode(EP) / 'cover.png'; img.save(out)
    img.save(P.series() / 'covers' / 'cover_s01e03.png'); print(out)


if __name__ == '__main__':
    {'ref': lambda: ref(), 'ai': lambda: ai(int(sys.argv[2]) if len(sys.argv) > 2 else 2),
     'make': lambda: make(int(sys.argv[2]) if len(sys.argv) > 2 else 0)}[sys.argv[1]]()
