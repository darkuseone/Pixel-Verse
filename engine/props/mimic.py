"""Мимика 2.5D (правило владельца 11.11.2026): живые лица для любого рига, у которого эмоция — словарь X
(eo — открытие глаз, pu — зрачок, bt — наклон бровей, bl — подъём бровей, mo — рот открыт, mc — уголки рта, lid, tears ...;
таблицы EXPR / XTRA в props/dibspix.py, fmcast.py, grimcast.py ...).

Что даёт:
- Face.X(t)      плавный переход между эмоциями за ~0,15 с вместо скачка (числа смешиваются, флаги — на середине перехода);
- Face.blink(t)  естественное моргание: интервалы 2,2–5,5 с, иногда двойное, обязательно — на смене эмоции (прячет скачок);
- Face.look(t)   «бегающий» взгляд: саккады раз в 0,7–2 с + лёгкий дрейф, поверх базового направления;
- Face.speak(t, m) акценты речи: на громких слогах брови подпрыгивают, глаза чуть шире; рот со сглаживанием (атака/спад);
- bob(t, m)      кивок/подпрыгивание головы и тела на акцентах (px мира: прибавить к wy героя);
- манпу-значки поверх кадра (пиксельные, в px кадра): sweat, vein, shock, blush, sparkle.

Пример (в эпизоде):
    from props import mimic as M
    FACE = M.Face([(0.0, 'zen'), (2.1, 'shock'), (3.4, 'cheer')], (C.XTRA, C.EXPR), seed=3)
    m = M.mouth(talk, 'fm', t)                                   # сглаженный рот из огибающей голоса
    E = FACE.speak(t, m)                                         # словарь эмоции на этот кадр
    A(C.fm, wx, wy + M.bob(t, m), s, expr=E, mouth_=m, blink=FACE.blink(t), look=FACE.look(t, (0.6, 0.2)))
Риг должен принимать словарь вместо имени: в его X() — `if isinstance(expr, dict): return dict(expr)` (см. M.X)."""
import math
import numpy as np
from PIL import Image, ImageDraw

FPS = 30
NUM = ('eo', 'pu', 'bt', 'bl', 'mo', 'mc', 'lid')


def _h(i, s=0):
    v = math.sin(i * 127.1 + s * 311.7) * 43758.5453
    return v - math.floor(v)


def X(expr, *tables):
    """имя эмоции или готовый словарь -> копия словаря (первая таблица, где нашлось имя; иначе 'normal')"""
    if isinstance(expr, dict): return dict(expr)
    for T in tables:
        if T and expr in T: return dict(T[expr])
    for T in tables:
        if T and 'normal' in T: return dict(T['normal'])
    return {}


def blend(A, B, u):
    """смесь двух эмоций: числовые поля линейно, остальные (флаги, слёзы) — от B после середины"""
    out = dict(B if u >= 0.5 else A)
    for k in set(A) | set(B):
        a, b = A.get(k), B.get(k)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
            out[k] = a + (b - a) * u
    return out


class Face:
    """track = [(время, эмоция-имя-или-словарь), ...]; tables = таблицы рига (XTRA, EXPR); seed — у каждого героя свой"""
    def __init__(s, track, tables, seed=0, ease=0.15):
        s.track = sorted(track, key=lambda k: k[0]); s.tables = tables; s.seed = seed; s.ease = ease
        s.swaps = [k[0] for k in s.track[1:]]

    def X(s, t):
        tr = s.track
        i = max([j for j, k in enumerate(tr) if k[0] <= t] or [0])
        cur = X(tr[i][1], *s.tables)
        if i == 0: return cur
        u = (t - tr[i][0]) / s.ease
        if u >= 1: return cur
        prev = X(tr[i - 1][1], *s.tables)
        u = u * u * (3 - 2 * u)
        return blend(prev, cur, u)

    def blink(s, t):
        """True на кадрах моргания (рисовать закрытые глаза)"""
        f = int(round(t * FPS))
        for ts in s.swaps:                                          # моргание на смене эмоции: 3 кадра, начиная чуть раньше
            k = f - int(round((ts - 0.04) * FPS))
            if 0 <= k < 3: return True
        start = int(-40 * _h(s.seed, 9))
        for n in range(300):
            if start > f: break
            if 0 <= f - start < 3: return True
            if _h(s.seed * 31 + n, 4) < 0.18 and 0 <= f - (start + 5) < 3: return True     # двойное
            start += int(FPS * (2.2 + 3.3 * _h(s.seed * 17 + n, 13)))
        return False

    def look(s, t, base=(0.6, 0.0), amp=0.32):
        """взгляд: base + саккады (быстрый перевод за 2 кадра, потом держит) + лёгкий дрейф"""
        T = 0.0; n = 0; prev = (0.0, 0.0); cur = (0.0, 0.0)
        while T <= t and n < 400:
            prev = cur
            cur = ((_h(s.seed * 7 + n, 1) - 0.5) * 2 * amp, (_h(s.seed * 7 + n, 2) - 0.5) * amp)
            dt = 0.7 + 1.3 * _h(s.seed * 7 + n, 3)
            T0 = T; T += dt; n += 1
        u = min(1.0, (t - T0) / (2.0 / FPS))
        x = prev[0] + (cur[0] - prev[0]) * u + 0.04 * math.sin(t * 1.7 + s.seed)
        y = prev[1] + (cur[1] - prev[1]) * u + 0.03 * math.sin(t * 1.3 + s.seed * 2)
        return (max(-1.0, min(1.0, base[0] + x)), max(-1.0, min(1.0, base[1] + y)))

    def speak(s, t, m=0.0):
        """эмоция кадра + акценты речи: громкий слог -> брови выше, глаза чуть шире"""
        E = s.X(t)
        if m > 0.55:
            k = (m - 0.55) / 0.45
            if 'bl' in E: E['bl'] = E['bl'] + 0.45 * k
            if 'eo' in E: E['eo'] = min(1.25, E['eo'] + 0.12 * k)
        return E


def mouth(talk, who, t, k=1.8, attack=0.035, release=0.09):
    """рот из огибающей голоса со сглаживанием: быстро открывается, мягче закрывается (не «дребезжит»)"""
    raw = lambda tt: min(1.0, max(0.0, talk(who, tt)) * k)
    m = raw(t)
    for i in range(1, 4):
        tt = t - i / 60.0
        m = max(m, raw(tt) * math.exp(-i / 60.0 / release))
    nxt = raw(t + attack)
    return min(1.0, max(m, nxt * 0.6))


def bob(t, m, amp=0.7):
    """кивок на акцентах речи + дыхание: прибавка к wy героя (px мира, вниз — плюс)"""
    return amp * max(0.0, m - 0.5) * 2 * abs(math.sin(t * 9.0)) + 0.25 * amp * math.sin(t * 2.1)


# ======================================================================= манпу-значки (px кадра, пиксельные)
def _pix(big, img, x, y, px):
    """RGBA-картинку img (в «пикселях героя») увеличить в px раз и наложить по центру (x, y) кадра"""
    if img.size[0] == 0: return
    im = img.resize((img.size[0] * px, img.size[1] * px), Image.NEAREST)
    a = np.asarray(im, np.float32)
    h, w = a.shape[:2]; x0, y0 = int(x - w / 2), int(y - h / 2)
    X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(big.shape[1], x0 + w), min(big.shape[0], y0 + h)
    if X0 >= X1 or Y0 >= Y1: return
    sub = a[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]; al = sub[..., 3:4] / 255
    reg = big[Y0:Y1, X0:X1]; reg[:] = (reg * (1 - al) + sub[..., :3] * al).astype(np.uint8)


def sweat(big, hx, hy, r, t, side=1, px=4, t0=0.0):
    """капля пота у виска: появляется и сползает (hx, hy — центр головы, r — радиус головы, px кадра)"""
    u = ((t - t0) * 0.8) % 1.0
    im = Image.new('RGBA', (7, 10)); d = ImageDraw.Draw(im)
    d.polygon([(3, 0), (6, 6), (5, 8), (1, 8), (0, 6)], fill=(150, 210, 255, 255), outline=(30, 60, 110, 255))
    d.point([(2, 4), (2, 5)], fill=(255, 255, 255, 255))
    _pix(big, im, hx + side * r * 0.95, hy - r * 0.45 + u * r * 0.6, px)


def vein(big, hx, hy, r, t, side=1, px=4):
    """жилка злости (крестик) на лбу, пульсирует"""
    s_ = 7 if int(t * 6) % 2 else 6
    im = Image.new('RGBA', (s_ + 2, s_ + 2)); d = ImageDraw.Draw(im); c = (230, 40, 50, 255)
    m = (s_ + 1) // 2
    for a_, b_ in (((1, m - 1), (m - 1, 1)), ((m + 1, 1), (s_, m - 1)), ((1, m + 1), (m - 1, s_)), ((m + 1, s_), (s_, m + 1))):
        d.line([a_, b_], fill=c, width=2)
    _pix(big, im, hx + side * r * 0.55, hy - r * 0.75, px)


def shock(big, hx, hy, r, px=4, k=1.0):
    """линии шока над головой (вертикальные штрихи веером)"""
    for i in range(-2, 3):
        L = int(5 + 3 * (2 - abs(i)))
        im = Image.new('RGBA', (2, L)); ImageDraw.Draw(im).rectangle([0, 0, 1, L - 1], fill=(20, 20, 30, int(255 * k)))
        _pix(big, im, hx + i * r * 0.38, hy - r * 1.35 - abs(i) * px, px)


def blush(big, hx, hy, r, a=0.6, px=4, look=0.0):
    """румянец: два розовых пятна с шахматным растром"""
    for sx in (-1, 1):
        im = Image.new('RGBA', (8, 4))
        for y in range(4):
            for x in range(8):
                if (x + y) % 2 == 0 or 1 <= y <= 2 and 2 <= x <= 5:
                    im.putpixel((x, y), (255, 120, 140, int(255 * a)))
        _pix(big, im, hx + (sx * 0.5 + look * 0.15) * r, hy + r * 0.28, px)


def sparkle(big, x, y, t, px=4, col=(255, 250, 200)):
    """искорка (гордость, «дзынь»): мигающий ромбик"""
    s_ = 2 + int(abs(math.sin(t * 9)) * 2)
    im = Image.new('RGBA', (2 * s_ + 1, 2 * s_ + 1)); d = ImageDraw.Draw(im)
    d.line([(s_, 0), (s_, 2 * s_)], fill=(*col, 255)); d.line([(0, s_), (2 * s_, s_)], fill=(*col, 255))
    _pix(big, im, x, y, px)
