"""Finale: «Долетел» (return to the frozen frame of the cold open), credits with jokes, bloopers, Molniya almost smiles."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1])); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from kit import *
E6 = load_chapter('ch_ep06', 'ep06')
import ch1 as CH1

DUR = 32.0
DAY, INCOME = 1096, 158
VOICE = [
    ('z1', 'movie', 'z1', 0.50, 0.10, 4.95, 'molniya', 'Долетел. Три ГОДА, шесть глав и один КАКТУС.'),
    ('z2', 'movie', 'z2', 5.70, 0.03, 2.00, 'billy',   'Кто-нибудь... ВЫТАЩИТ?'),
    ('z3', 'movie', 'z3', 8.20, 0.15, 2.05, 'molniya', 'Вытаскивание — по ТАРИФУ.'),
    ('z4', 'movie', 'z4', 15.10, 0.10, 3.70, 'sam',    'Приятного аппе... Простите. ДУБЛЬ.'),
    ('z5', 'movie', 'z5', 23.10, 0.20, 3.30, 'billy',  'Дубль СЕМНАДЦАТЫЙ... Молния, ну хватит!'),
    ('z6', 'movie', 'z6', 26.70, 0.05, 2.00, 'molniya', 'Это не СЧИТАЕТСЯ.'),
]
SFX = [
    ('library/sfx/wind_gust.mp3', 0.20, 0.5), ('library/sfx/carrot_crunch.mp3', 4.90, 0.6), ('library/sfx/counter_blip.mp3', 9.00, 0.7),
    ('library/sfx/film_click.mp3', 11.00, 0.7), ('library/sfx/film_click.mp3', 14.50, 0.9), ('library/sfx/film_click.mp3', 22.70, 0.9),
    ('library/sfx/donkey_walk.mp3', 14.90, 0.5), ('library/sfx/ribbon_snap.mp3', 27.00, 0.5),
]
BEDS = [
    ('series/pochti-dikiy-zapad/music/finale_fanfare_15s.mp3', 14.9, 0.0, 11.4, 0.26, True),
    ('series/pochti-dikiy-zapad/music/credits_swing_15s.mp3', 15.0, 10.8, 32.0, 0.30, True),
]
EPI = episode('mv_finale', VOICE, DUR)
SUNSET = bgworld('sunset_road')
CRED_SEGS = [(11.0, 14.5), (18.9, 22.7), (28.9, 32.0)]
BLOOPERS = [(14.5, 18.9), (22.7, 28.9)]
CREDITS = [('РЕЖИССЁР', 'МОЛНИЯ'), ('СЦЕНАРИЙ', 'МОЛНИЯ (БИЛЛИ ПРЕДЛАГАЛ. НЕ ПРИНЯТО)'), ('В РОЛИ БИЛЛИ', 'БИЛЛИ (ПО НЕДОСМОТРУ)'),
           ('В РОЛИ СЭМА', 'КРИВОЙ СЭМ (ОН НАСТОЯЛ)'), ('КАКТУС', 'ИГРАЛ СЕБЯ. ВСЕ ДУБЛИ'), ('БАРМЕН', 'МОЛЧАЛ. ГОНОРАР — ВЫСОКИЙ'),
           ('МОРКОВЬ', '158 ШТ. (ОПЛАЧЕНО СЭМОМ)'), ('НИ ОДНА ЛОШАДЬ НЕ ПОСТРАДАЛА', 'КОШЕЛЁК БИЛЛИ — ДА'), ('ПОДПИШИСЬ', 'ОТМЕНА — ПИСЬМОМ')]
_CR = []


def credit_time(t):
    ct = 0.0
    for a, b in CRED_SEGS:
        if t >= b: ct += b - a
        elif t >= a: ct += t - a
    return ct


def credits_sheet():
    if _CR: return _CR[0]
    from PIL import ImageFont
    H_ = 400 * len(CREDITS) + 200
    img = Image.new('RGBA', (1920, H_), (0, 0, 0, 0))
    y = 100
    for head, name in CREDITS:
        for txt, size, col in ((head, 34, (255, 200, 110)), (name, 54, (255, 250, 236))):
            f = O.pfont(size); bb = f.getbbox(txt); tw = bb[2] - bb[0]
            if tw > 1780: size = int(size * 1780 / tw); f = O.pfont(size); bb = f.getbbox(txt); tw = bb[2] - bb[0]
            layer = Image.new('L', (tw + 24, bb[3] - bb[1] + 24), 0); d = ImageDraw.Draw(layer); d.fontmode = '1'
            d.text((12 - bb[0], 12 - bb[1]), txt, font=f, fill=255)
            m = np.array(layer) > 127; dil = O._dilate(m, 4)
            rgba = np.zeros(m.shape + (4,), np.uint8); rgba[dil] = (20, 10, 6, 255); rgba[m] = col + (255,)
            img.alpha_composite(Image.fromarray(rgba), ((1920 - tw) // 2 - 12, y))
            y += bb[3] - bb[1] + 60 if txt is head else bb[3] - bb[1] + 170
    _CR.append(np.array(img)); return _CR[0]


def clapper(big, t, t0):
    """clapperboard flash 'ДУБЛЬ N'"""
    u = t - t0
    if not (0 <= u < 0.6): return
    k = 1 - sm((u - 0.4) / 0.2)
    x0, y0, w, h = 660, 330, 600, 380
    big[y0:y0 + h, x0:x0 + w] = (big[y0:y0 + h, x0:x0 + w] * (1 - k) + np.array([22, 20, 22]) * k).astype(np.uint8)
    for i in range(6):
        cx = x0 + i * 100
        big[y0:y0 + 70, cx:cx + 50] = np.where(k > 0.5, (240, 240, 240), big[y0:y0 + 70, cx:cx + 50])
    WO.ptext(big, 'ДУБЛЬ 17' if t0 < 20 else 'ДУБЛЬ 23', x0 + w // 2, y0 + 210, 56, (245, 245, 245), 'c')
    WO.ptext(big, 'СЭМ · ПРИЯТНОГО АППЕТИТА' if t0 < 20 else 'БИЛЛИ · САМЫЙ БЫСТРЫЙ', x0 + w // 2, y0 + 300, 22, (200, 200, 200), 'c')


def render_scene(t):
    if t < 11.0:
        if t < 5.5: te = 41.3 + 0.18 * t
        elif t < 8.2: te = 37.5 + 0.2 * (t - 5.5)
        else: te = 39.4 + 0.2 * (t - 8.2)
        return E6.render_scene(te)
    for a, b in BLOOPERS:
        if a <= t < b:
            if a < 20:                                                     # Sam rides past Molniya (chapter 1 road)
                return CH1.render_scene(35.1 + (t - 14.5) * 0.35)
            if t < 26.6: return CH1.render_scene(4.6 + (t - 22.7) * 0.2)   # Billy at the ranch
            return CH1.render_scene(46.0 + (t - 26.6) * 0.3)               # Molniya CU
    # credits over the sunset
    ct = credit_time(t)
    v = wv(SUNSET, 640 + 6 * ct, 360, 1.0 + 0.01 * ct)
    big = v.bg()
    big = (big * 0.55).astype(np.uint8); fx.vignette(big, 0.4)
    return big


def render(t):
    big = render_scene(t)
    in_cred = any(a <= t < b for a, b in CRED_SEGS)
    if in_cred:
        sheet = credits_sheet(); ct = credit_time(t)
        y = int(1080 - ct * 300)
        O.overlay(big, sheet, 0, y, 1.0) if False else None
        src = sheet; ys = -y
        h = min(1080, src.shape[0] - ys)
        if ys < src.shape[0] and h > 0:
            crop = src[max(0, ys):max(0, ys) + h]
            oy = max(0, y)
            hh = min(crop.shape[0], 1080 - oy)
            if hh > 0: O.overlay(big, crop[:hh], 0, oy, 1.0)
    if t < 11.0:
        WO.hud(big, t, DAY, INCOME)
        if 8.9 <= t < 10.6:
            O.draw_sticker(big, O.sticker('ТАРИФ ×3', fg=(255, 210, 90), size=64), t, 8.9, 10.6, 960, 300)
        EPI.captions.draw(big, t, WO.CAP_Y)
    else:
        for a, b in BLOOPERS:
            if a <= t < b:
                EPI.captions.draw(big, t, WO.CAP_Y)
                clapper(big, t, a)
                WO.ptext(big, '● ДУБЛЬ', 1880, 60, 28, (255, 90, 80), 'r')
        if 26.7 <= t < 28.7: WO.ptext(big, '*молния почти улыбнулась*', 960, 980, 26, (255, 236, 170), 'c')
    flash_at(big, t, [0.0, 11.0], 0.12, 0.5)
    return big
