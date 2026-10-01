"""Chapter 4 gag: the auto-renewal contract unrolls across the screen; clause 14 = «Билли. Всё.»"""
import sys, pathlib, importlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *

_p = str(HERE / 'chapters' / 'ch_ep04')
sys.path.insert(0, _p); sys.modules.pop('timeline', None)
E4 = importlib.import_module('ep04')
sys.modules.pop('timeline', None); sys.path.remove(_p)

DUR = 7.8
DAY, INCOME = 620, 30
VOICE = [
    ('f3', 'movie', 'f3', 0.40, 0.10, 3.70, 'billy', 'Пункт четырнадцать: «Билли. ВСЁ.»?'),
    ('f4', 'movie', 'f4', 4.60, 0.15, 2.85, 'sam',   'МЕЛКИЙ шрифт, сэр. Мелкий шрифт.'),
]
SFX = [('library/sfx/paper_unroll.mp3', 0.10, 0.9), ('library/sfx/stamp.mp3', 3.50, 0.9), ('library/sfx/counter_blip.mp3', 4.55, 0.5)]
BEDS = [('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 0.0, 7.8, 0.26, True)]
EPI = episode('mv_contract', VOICE, DUR)
_PAPER = []


def make_paper():
    from PIL import ImageFont
    r = np.random.default_rng(14)
    words = ['СТОРОНА', 'ОБЯЗУЕТСЯ', 'АРЕНДАТОР', 'ПРОДЛЕНИЕ', 'МОРКОВЬ', 'НЕУСТОЙКА', 'ПИСЬМОМ', 'НЕОТЗЫВНО', 'ТАРИФ', 'КАКТУС',
             'ЛОШАДЬ', 'ВЕЧНО', 'ШТРАФ', 'СЭМ', 'ПУНКТ', 'ДОПЛАТА', 'БЕЗ ПРАВА', 'ПОВТОРНО', 'ДОГОВОР', 'ОТМЕНА']
    W_, H_ = 900, 2300
    img = Image.new('RGB', (W_, H_), (238, 226, 190)); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W_ - 1, H_ - 1), outline=(150, 120, 80), width=6)
    f = ImageFont.truetype(P.FONT_PX, 30); d.text((90, 40), 'ДОГОВОР ПРОКАТА', font=f, fill=(80, 40, 30))
    fs = ImageFont.truetype(P.FONT_PX, 10)
    y = 130; n = 1
    while y < H_ - 60:
        line = f'{n}. ' + ' '.join(r.choice(words) for _ in range(int(r.integers(6, 10)))) + '.'
        col = (90, 70, 56)
        if n == 14:
            d.rectangle((40, y - 8, W_ - 40, y + 26), fill=(255, 226, 150)); col = (150, 30, 26)
            line = '14. БИЛЛИ. ВСЁ.'
            d.text((70, y), line, font=ImageFont.truetype(P.FONT_PX, 16), fill=col)
        else:
            d.text((70, y), line[:70], font=fs, fill=col)
        y += 28 if n != 14 else 46; n += 1
    return np.array(img), 130 + 13 * 28 + 10


def paper_frame(t):
    if not _PAPER: _PAPER.append(make_paper())
    arr, y14 = _PAPER[0]
    Hh, Ww = arr.shape[:2]
    # visible window: unroll 0.1..1.6 (reveal), then pan/zoom to clause 14
    reveal = min(1.0, max(0.0, (t - 0.1) / 1.4))
    zoom = 1.0 + 1.1 * sm((t - 1.8) / 1.6)
    view_h = int(1080 / zoom * 1.0)
    cy = lerp(view_h / 2, y14, sm((t - 1.8) / 1.6))
    y0 = int(max(0, min(Hh - view_h, cy - view_h / 2)))
    crop = arr[y0:y0 + view_h]
    w_out = int(Ww * (1080 / view_h))
    img = np.array(Image.fromarray(crop).resize((w_out, 1080), Image.NEAREST))
    vis = int(1080 * reveal)
    return img, vis


def render_scene(t):
    te = 13.4 + (t * 0.25) % 2.0
    big = E4.render_scene(te)
    big[:] = (big * 0.55).astype(np.uint8)
    return big


def render(t):
    big = render_scene(t)
    img, vis = paper_frame(t)
    px0 = 90; px1 = min(1920, px0 + img.shape[1])
    reg = big[:vis, px0:px1]
    reg[:] = img[:vis, :px1 - px0]
    big[:vis, px0 - 8:px0] = (60, 40, 24); big[:vis, px1:px1 + 8] = (60, 40, 24) if px1 + 8 <= 1920 else big[:vis, px1:px1 + 8]
    if 3.5 <= t < 6.5:
        k = min(1.0, (t - 3.5) / 0.12)
        big[560:800, 380:1540] = (big[560:800, 380:1540] * (1 - 0.6 * k) + np.array([30, 16, 10]) * 0.6 * k).astype(np.uint8)
        O.overlay(big, O.pixel_title(['ПУНКТ 14:', 'БИЛЛИ. ВСЁ.'], 48, width=1920), 0, 600, k)
    WO.hud(big, t, DAY, INCOME)
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [0.0, 3.5], 0.12, 0.5)
    return big
