"""Post-credits scene: the silent bartender speaks — and gets paid; teaser «Сезон 2. Тариф — ТРИ»."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *
E3 = load_chapter('ch_ep03', 'ep03')

DUR = 14.2
VOICE = [
    ('p1', 'movie', 'p1', 1.30, 0.05, 1.95, 'bartender', 'Я всё ВИДЕЛ.'),
    ('p2', 'movie', 'p2', 4.60, 0.08, 1.50, 'molniya',   'Теперь тебе ПЛАТЯТ.'),
    ('p3', 'movie', 'p3', 6.50, 0.08, 2.55, 'bartender', '...Ничего не ВИДЕЛ.'),
    ('m2', 'ep06',  'm2', 9.60, 0.00, 3.47, 'molniya',   'Сезон два. Тариф — ТРИ.'),
]
SFX = [('library/sfx/film_click.mp3', 0.00, 0.8), ('library/sfx/glass_slide.mp3', 3.60, 0.9), ('library/sfx/coin_clink.mp3', 5.90, 0.6),
       ('library/sfx/title_stinger.mp3', 9.40, 0.9)]
BEDS = [('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 0.8, 9.2, 0.18, True),
        ('series/pochti-dikiy-zapad/music/finale_fanfare_15s.mp3', 14.9, 9.4, 14.2, 0.30, True)]
EPI = episode('mv_post', VOICE, DUR)
talk = EPI.talk
BT = E3.SAL.BT_X


def bar(t, cx, Z):
    ST.set_px(1)
    v = E3.view_at(BT + cx, 440, Z, 180, 330)
    big, xs, ys = E3.bg(v)
    E3.blit_world(big, xs, ys, E3.BT['polish%d' % (int(t * 4) % 2)], BT - 60, 0)
    CH = E3.Chars()
    show_mol = 3.0 <= t < 9.2
    if show_mol:
        E3.draw_molniya(CH, v.cam(BT + 215, 612 - 19 * 5.2, 5.2, True), t, carrot=t >= 5.6, chew=t >= 6.4)
    # the carrot sliding along the counter towards the bartender
    if 3.4 <= t < 9.2:
        k = sm((t - 3.6) / 1.4)
        x = lerp(BT + 190, BT + 40, k) if t < 5.9 else BT + 40
        if t < 5.9 or t < 6.4:
            L = Layer(v.cam(0, 0, 1.0)); L.cam.ax = 0; L.cam.ay = 0
            y = 436
            cap(L, (x, y), (x + 15, y - 3), 3.2, 1.0, (236, 128, 40), hi=(255, 176, 90))
            for a in (-0.5, 0.0, 0.5): cap(L, (x, y), (x - 5 * math.cos(a), y - 5 * math.sin(a) - 2), 1.1, 0.6, (84, 160, 60))
            outline(L, (40, 24, 14)); CH.add(L)
    CH.comp(big)
    return big


def render_scene(t):
    if t < 1.0:
        big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (12, 8, 8); return big
    if t < 3.2: return bar(t, 0, 2.6)
    if t < 6.4: return bar(t, 120, 1.55)
    if t < 9.2: return bar(t, 0, 2.6)
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (12, 8, 8)
    return big


def render(t):
    big = render_scene(t)
    if t < 1.0:
        WO.ptext(big, 'СЦЕНА ПОСЛЕ ТИТРОВ', 960, 540, 48, (255, 236, 170), 'c')
    if t >= 9.4:
        k = min(1.0, (t - 9.4) / 0.2)
        O.overlay(big, O.pixel_title(['СЕЗОН 2', 'ТАРИФ — ТРИ'], 88, width=1920), 0, 250, k)
        WO.ptext(big, 'ПОДПИШИСЬ, ПОКА НЕ ПОДОРОЖАЛО', 960, 720, 30, (255, 200, 110), 'c')
    if 1.0 <= t < 9.2: EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [1.0, 9.4], 0.12, 0.6)
    return big
