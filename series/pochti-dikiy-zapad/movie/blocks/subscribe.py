"""«Пауза на подписку»: Molniya breaks the fourth wall (subscribe button, «отмена — только письмом», comments)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *
from PIL import ImageFont

DUR = 10.6
DAY, INCOME = 620, 30
VOICE = [
    ('g1', 'movie', 'g1', 0.60, 0.05, 3.55, 'molniya', 'ПОДПИШИТЕСЬ. Отмена — только ПИСЬМОМ.'),
    ('g2', 'movie', 'g2', 5.10, 0.05, 4.10, 'molniya', 'Комментарии читаю Я. Лайк БЕСПЛАТНЫЙ. Пока.'),
]
SFX = [('library/sfx/film_click.mp3', 0.00, 0.6), ('library/sfx/counter_blip.mp3', 3.40, 0.9), ('library/sfx/counter_blip.mp3', 6.70, 0.5),
       ('library/sfx/horse_snort.mp3', 4.90, 0.4), ('library/sfx/carrot_crunch.mp3', 9.20, 0.5)]
BEDS = [('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 0.0, 10.6, 0.26, True)]
EPI = episode('mv_sub', VOICE, DUR)
talk = EPI.talk
ROAD = bgworld('desert_road')
FEET, U = 590.0, 8.0
COMMENTS = ['первый!', 'Билли, беги', 'где мой тариф?', 'Молния — легенда', 'Сэм честный, я проверял', 'а морковка была оплачена?']
_S = {}


def sprites():
    if _S: return _S
    fb = ImageFont.truetype(P.FONT_BOLD, 40)
    def bubble(txt, who):
        w = int(ImageDraw.Draw(Image.new('L', (1, 1))).textlength(txt, font=fb)) + 70
        im = Image.new('RGBA', (w, 84), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, 83), 22, fill=(250, 242, 222, 235), outline=(60, 40, 24, 255), width=4)
        d.text((30, 20), txt, font=fb, fill=(50, 34, 24, 255))
        return np.array(im)
    _S['b'] = [bubble(c, i) for i, c in enumerate(COMMENTS)]
    def button(txt, col):
        fp = O.pfont(40); bb = fp.getbbox(txt)
        w, h = bb[2] - bb[0] + 90, 130
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((6, 10, w - 1, h - 1), 26, fill=(60, 20, 18, 255))
        d.rounded_rectangle((0, 0, w - 7, h - 12), 26, fill=col + (255,), outline=(30, 12, 10, 255), width=5)
        d.fontmode = '1'; d.text((45 - bb[0], 40 - bb[1]), txt, font=fp, fill=(255, 255, 255, 255))
        return np.array(im)
    _S['btn'] = button('ПОДПИСАТЬСЯ', (210, 40, 36)); _S['btn2'] = button('ВЫ ПОДПИСАНЫ', (110, 110, 116))
    return _S


def draw(CH, FX, big, v, t):
    fx.motes(FX, v, t, 0, 300, 1280, 700, n=26, seed=15)
    Pz = C.molniya_pose(t, chew=t >= 9.0, jaw_talk=talk('molniya', t))
    ax, ay = C.horse_anchor(470.0, FEET, U)
    shadow(big, v, 470.0, FEET, 16 * U, 1.8 * U)
    C.molniya(CH, v.cam(ax, ay, U), t, Pz, hat=True, carrot=t >= 9.0)


def render_scene(t):
    hx, hy = C.head_of_horse(470.0, FEET, U, C.molniya_pose(t))
    v = wv(ROAD, hx + 120 - 6 * t, hy + 40, 1.7)
    big = shot(v, t, lambda CH, FX, big, vv: draw(CH, FX, big, vv, t),
               Light(amb=(1.05, 0.97, 0.88), rim=(1, -1, (255, 236, 190), 0.45), grad=(1.06, 0.9)))
    return big


def render(t):
    big = render_scene(t)
    sp = sprites()
    pressed = t >= 3.4
    btn = sp['btn2'] if pressed else sp['btn']
    dy = 8 if 3.4 <= t < 3.6 else 0
    k = min(1.0, t / 0.2)
    O.overlay(big, btn, 1240, 250 + dy, k)
    WO.ptext(big, 'автопродление · отмена письмом' if pressed else '', 1560, 420, 26, (255, 236, 170), 'c')
    if t >= 5.0:                                                    # comments float up
        for i, b in enumerate(sp['b']):
            t0 = 5.4 + 0.65 * i
            if t < t0: continue
            y = 1000 - (t - t0) * 190
            if y < -100: continue
            O.overlay(big, b, 1880 - b.shape[1] - 30 - (i % 2) * 40, int(y), min(1.0, (t - t0) / 0.15))
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [0.0], 0.12, 0.5)
    return big
