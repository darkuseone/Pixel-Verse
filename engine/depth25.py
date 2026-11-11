"""2.5D-стиль для AI-задников (правило владельца 11.11.2026, «новый стиль»): карта глубины задника -> параллакс камеры,
глубина резкости по глубине (фон и передний план мягкие, герой резкий), дымка вдаль, герой заходит ЗА предметы задника
(прилавок, забор, дверной косяк) без ручных масок, свечение только от ярких источников, лучи света. Работает поверх
stage.View / chikit.shot: shot25() — тот же shot(), плюс глубина.

Глубина: Depth Anything V2 Small (ONNX, лицензия Apache-2.0, ~27 МБ в library/models/, скачивается сам при первом вызове;
`pip install onnxruntime`) -> кэш `<bg>.depth.png` рядом с задником (16 бит, 1.0 = ближе всего, 0.0 = дальше всего).
Нет onnxruntime или сети -> запасной вариант «пол + горизонт» (horizon в `<bg>.depth.json`).
Ручные правки поверх модели — `<bg>.depth.json`:
    {"horizon": 300,                                  # для запасного варианта: строка горизонта в px задника
     "polys": [[0.9, [[x, y], [x, y], ...]], ...],    # многоугольник = плоскость с этой «близостью» (прилавок, косяк)
     "boost": [[0.1, [[x, y], ...]]]}                  # прибавить к близости внутри многоугольника
Проверка карты: python3 engine/depth25.py <bg.png>  -> <bg>.depth_check.png (задник | глубина | слои параллакса)."""
import json, math, os, sys, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
import paths as P
import stage as ST

MODEL = P.ROOT / 'library' / 'models' / 'depth_anything_v2_small_q.onnx'
URL = 'https://huggingface.co/onnx-community/depth-anything-v2-small/resolve/main/onnx/model_quantized.onnx'
_SESS = [None]
_CACHE = {}                                          # id(world) -> Depth


# ======================================================================= карта глубины
def _session():
    if _SESS[0] is None:
        import onnxruntime as ort
        if not MODEL.exists():
            MODEL.parent.mkdir(parents=True, exist_ok=True)
            tmp = MODEL.with_suffix('.part')
            urllib.request.urlretrieve(URL, tmp); tmp.rename(MODEL)
        so = ort.SessionOptions(); so.log_severity_level = 3
        _SESS[0] = ort.InferenceSession(str(MODEL), so, providers=['CPUExecutionProvider'])
    return _SESS[0]


def estimate(rgb, short=518):
    """нейросетевая близость 0..1 (1 = ближе) для RGB-массива HxWx3"""
    h, w = rgb.shape[:2]
    k = short / min(h, w)
    th, tw = max(14, int(round(h * k / 14)) * 14), max(14, int(round(w * k / 14)) * 14)
    x = np.asarray(Image.fromarray(rgb).resize((tw, th), Image.BICUBIC), np.float32) / 255.0
    x = (x - (0.485, 0.456, 0.406)) / (0.229, 0.224, 0.225)
    out = _session().run(None, {'pixel_values': x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    d = np.asarray(Image.fromarray(out.astype(np.float32)).resize((w, h), Image.BILINEAR), np.float32)
    lo, hi = np.percentile(d, 1.5), np.percentile(d, 99.5)
    return np.clip((d - lo) / max(1e-6, hi - lo), 0, 1).astype(np.float32)


def fallback(h, w, horizon=None):
    """без модели: всё выше горизонта — даль (0.05), ниже — пол, ближе к низу кадра"""
    hz = int(horizon if horizon is not None else h * 0.45)
    y = np.arange(h, dtype=np.float32)[:, None]
    n = np.where(y < hz, 0.05, 0.05 + 0.95 * ((y - hz) / max(1, h - hz)) ** 0.8)
    return np.repeat(n, w, 1).astype(np.float32)


def _poly_mask(h, w, pts):
    from PIL import ImageDraw
    im = Image.new('L', (w, h), 0); ImageDraw.Draw(im).polygon([tuple(p) for p in pts], fill=255)
    return np.asarray(im) > 127


def near_map(bg_path, size=None):
    """близость для файла задника (кэш <bg>.depth.png рядом с ним), правки из <bg>.depth.json; size=(w, h) — под размер мира"""
    bg_path = Path(bg_path)
    cache = bg_path.with_name(bg_path.stem + '.depth.png')
    meta = bg_path.with_name(bg_path.stem + '.depth.json')
    J = json.loads(meta.read_text()) if meta.exists() else {}
    if cache.exists() and cache.stat().st_mtime >= bg_path.stat().st_mtime:
        n = np.asarray(Image.open(cache), np.float32) / 65535.0
    else:
        rgb = np.asarray(Image.open(bg_path).convert('RGB'))
        try:
            n = estimate(rgb)
        except Exception as e:                                       # нет onnxruntime / сети: пол + горизонт
            print(f'depth25: модель недоступна ({type(e).__name__}), запасной вариант «пол + горизонт»', file=sys.stderr)
            n = fallback(*rgb.shape[:2], J.get('horizon'))
        Image.fromarray((n * 65535).astype(np.uint16)).save(cache)
    h, w = n.shape
    for v, pts in J.get('polys', []): n = np.where(_poly_mask(h, w, pts), np.float32(v), n)
    for v, pts in J.get('boost', []): n = np.clip(n + _poly_mask(h, w, pts) * np.float32(v), 0, 1)
    if size and (w, h) != tuple(size):
        n = np.asarray(Image.fromarray(n).resize(tuple(size), Image.BILINEAR), np.float32)
    return n


class Depth:
    """мир (world, как из stage.ai_world) + его карта близости того же размера"""
    def __init__(s, world, near):
        s.world, s.near = world, near.astype(np.float32)
        _CACHE[id(world)] = s

    def at(s, wx, wy):
        """близость в точке мира (ноги героя)"""
        h, w = s.near.shape
        return float(s.near[int(np.clip(wy, 0, h - 1)), int(np.clip(wx, 0, w - 1))])

    def floor(s, wx, wy, span=70, q=20):
        """близость пола под героем: дальний перцентиль строки у ног (±span px мира) — если ноги попали на кадку/прилавок,
        который герой загораживает собой или за которым стоит, берётся пол/стена позади, а не сам предмет"""
        h, w = s.near.shape
        y = int(np.clip(wy, 0, h - 1)); x0, x1 = int(np.clip(wx - span, 0, w - 1)), int(np.clip(wx + span, 1, w))
        return float(np.percentile(s.near[y, x0:x1], q))

    def grid(s, v, par=(0.0, 0.0), focus=0.5):
        """индексы мира для каждого пикселя кадра с параллаксом + близость в кадре"""
        xs, ys = v.grid()
        H_, W_ = s.near.shape
        X = np.broadcast_to(xs[None, :], (len(ys), len(xs))); Y = np.broadcast_to(ys[:, None], (len(ys), len(xs)))
        if not (par[0] or par[1]):
            return Y, X, s.near[Y, X]
        n = s.near[Y, X]
        for _ in range(2):                                              # две итерации: сдвиг считается по глубине точки, куда смотрим
            xi = np.clip(X + par[0] * (n - focus), 0, W_ - 1).astype(np.int32)
            yi = np.clip(Y + par[1] * (n - focus), 0, H_ - 1).astype(np.int32)
            n = s.near[yi, xi]
        return yi, xi, n

    def bg(s, v, par=(0.0, 0.0), focus=0.5):
        """задник с параллаксом (+ декали со своим сдвигом по глубине, + анимации мира). -> (кадр, близость в кадре)"""
        yi, xi, n = s.grid(v, par, focus)
        out = s.world[yi, xi]
        e = ST.DECALS.get(id(s.world))
        if e and e[0] is s.world:
            from props import decals as D
            for img, wx, wy, ws in e[1]:
                hh, ww = img.shape[:2]
                nd = s.at(wx + ww / ws / 2, wy + hh / ws * 0.9)
                D.blit(out, v, img, wx - par[0] * (nd - focus), wy - par[1] * (nd - focus), ws)
            for fn in e[2]: fn(out, v, ST.T_NOW[0])
        return out, n


def of(world, bg_path=None):
    """Depth для мира: из кэша или по файлу задника (размер подгоняется под мир)"""
    d = _CACHE.get(id(world))
    if d is not None and d.world is world: return d
    if bg_path is None: raise ValueError('depth25.of: нужен путь к заднику (series/<slug>/bg/<name>.png)')
    return Depth(world, near_map(bg_path, (world.shape[1], world.shape[0])))


# ======================================================================= эффекты по глубине
def _blur(img, r):
    if r <= 0.4: return img
    k = 2 if r > 3 else 1                                               # большой радиус — на половинном размере (быстро)
    im = Image.fromarray(img)
    if k > 1: im = im.resize((img.shape[1] // k, img.shape[0] // k), Image.BILINEAR)
    im = im.filter(ImageFilter.GaussianBlur(r / k))
    if k > 1: im = im.resize((img.shape[1], img.shape[0]), Image.BILINEAR)
    return np.asarray(im)


def dof(big, n, focus, k=38.0, rmax=13.0, near_k=1.25):
    """глубина резкости: радиус размытия (px кадра) = |близость - фокус| * k (ближе фокуса x near_k), не больше rmax"""
    d = n - focus
    r = np.clip(np.abs(d) * k * np.where(d > 0, near_k, 1.0), 0, rmax)
    if r.max() < 0.6: return big
    L = [big] + [_blur(big, rmax * i / 3) for i in (1, 2, 3)]
    u = r / (rmax / 3); i0 = np.clip(np.floor(u).astype(np.int32), 0, 2); f = (u - i0)[..., None]
    out = np.empty_like(big)
    for i in range(3):
        m = i0 == i
        if m.any(): out[m] = (L[i][m] * (1 - f[m]) + L[i + 1][m] * f[m]).astype(np.uint8)
    return out


def haze(big, n, col=(150, 170, 210), a=0.45, gamma=1.8):
    """воздушная перспектива: даль тонет в цвете неба/тумана"""
    w = (a * (1 - n) ** gamma)[..., None]
    big[:] = (big * (1 - w) + np.array(col, np.float32) * w).astype(np.uint8)
    return big


def bloom(big, thr=215, r=22, a=0.6):
    """свечение только от ярких источников (лампы, неон, окна, солнце), экраном поверх"""
    lum = big.max(axis=2).astype(np.float32)
    m = np.clip((lum - thr) / max(1.0, 255 - thr), 0, 1)[..., None]
    if m.max() <= 0: return big
    src = (big * m).astype(np.uint8)
    q = 4
    sm_ = Image.fromarray(src).resize((big.shape[1] // q, big.shape[0] // q), Image.BILINEAR).filter(ImageFilter.GaussianBlur(r / q))
    g = np.asarray(sm_.resize((big.shape[1], big.shape[0]), Image.BILINEAR), np.float32) * a
    big[:] = (255 - (255 - big.astype(np.float32)) * (255 - g) / 255).astype(np.uint8)
    return big


def rays(big, src, a=0.35, n_=14, spread=0.32, thr=200, col=None, mask=None):
    """лучи из яркого источника src=(x, y) px кадра (окно, фонарь, солнце): радиальное размытие ярких мест к src"""
    q = 4; h, w = big.shape[0] // q, big.shape[1] // q
    lum = big.max(axis=2).astype(np.float32)
    m = np.clip((lum - thr) / max(1.0, 255 - thr), 0, 1)
    if mask is not None: m = m * mask
    s_ = np.asarray(Image.fromarray((big * m[..., None]).astype(np.uint8)).resize((w, h), Image.BILINEAR), np.float32)
    acc = np.zeros_like(s_); cx, cy = src[0] / q, src[1] / q
    for i in range(n_):
        z = 1 + spread * i / n_
        M = Image.fromarray(s_.astype(np.uint8)).transform((w, h), Image.AFFINE, (1 / z, 0, cx - cx / z, 0, 1 / z, cy - cy / z), Image.BILINEAR)
        acc += np.asarray(M, np.float32) * (1 - i / n_)
    acc /= n_ / 2
    g = np.asarray(Image.fromarray(np.clip(acc, 0, 255).astype(np.uint8)).resize((big.shape[1], big.shape[0]), Image.BILINEAR), np.float32)
    if col is not None: g = g.max(axis=2, keepdims=True) * (np.array(col, np.float32) / 255)
    big[:] = (255 - (255 - big.astype(np.float32)) * (255 - g * a) / 255).astype(np.uint8)
    return big


def drop_shadow(big, v, D, wx, wy, w_, key=(0.6, -0.25), a=0.35, length=1.6):
    """тень героя на пол в сторону от ключевого света (дополняет контактную stage.shadow): мягкий клин по полу"""
    ox, oy = v.opt(wx, wy); W_ = w_ * v.Z * ST.UP
    L = W_ * length; dx, dy = -key[0], 0.18
    x0, x1 = int(max(0, min(ox, ox + dx * L) - W_)), int(min(big.shape[1], max(ox, ox + dx * L) + W_))
    y0, y1 = int(max(0, oy - W_ * 0.3)), int(min(big.shape[0], oy + W_ * 0.35))
    if x0 >= x1 or y0 >= y1: return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    u = ((xx - ox) * dx) / max(1.0, L); u = np.clip(u, 0, 1)
    across = np.abs((yy - oy) - u * dy * L) / (W_ * 0.28 * (1 - 0.5 * u) + 1)
    q = np.clip(1 - across, 0, 1) * (1 - u) * (u > 0)
    q = np.floor(q * 4) / 4                                              # ступеньками, как пиксель-арт
    reg = big[y0:y1, x0:x1]; reg[:] = (reg * (1 - a * q[..., None])).astype(np.uint8)


# ======================================================================= кадр
def shot25(world, light, cx, cy, Z, depth=None, acts=(), back=(), front=(), par=(0.0, 0.0), focus=None, dof_k=38.0, dof_max=13.0,
           haze_=None, bloom_=(215, 22, 0.55), rays_=None, occlude=True, eps=0.045, pre=None, emit=None, fx_=None,
           sx=180, sy=330, vig=0.26, t=0.0, kick=(0, 0)):
    """chikit.shot в 2.5D: depth = depth25.of(world, bg_path) (или None — как обычный shot, без глубины);
    par = (px, py) параллакс в px мира (сдвиг слоёв относительно плоскости фокуса); focus = близость плоскости фокуса
    (по умолчанию — ноги первого героя в acts); dof_k = 0 — без размытия; haze_ = (цвет, сила) — дымка вдаль;
    bloom_ = (порог, радиус, сила) или None; rays_ = dict(src=(x, y), a=..) — лучи; occlude — герои уходят за предметы задника;
    kick = (dx, dy) px кадра — удар камеры (cam25.kick)."""
    import fx
    ST.set_px(ST.px_for_zoom(Z))
    v = ST.view_at(world, cx, cy, Z, sx, sy)
    if depth is None:
        big = v.bg(); n = None
    else:
        heroes = [a for a in acts if hasattr(a, 'wx')]
        if focus is None: focus = (getattr(heroes[0], 'near', None) or depth.floor(heroes[0].wx, heroes[0].wy)) if heroes else 0.5
        big, n = depth.bg(v, par, focus)
        if haze_: haze(big, n, *haze_)
        if dof_k: big = dof(big, n, focus, dof_k, dof_max)
    if pre: pre(big, v)
    lt = light(v) if light else None
    for group in (back, acts, front):
        for a in group:
            before = big.copy() if (n is not None and occlude and hasattr(a, 'wx')) else None
            if getattr(a, 'direct', False): a(big, v, lt)
            else:
                CH = ST.Chars(); a(CH, v); CH.comp(big, lt)
            if before is not None:                                      # герой за предметом задника, который ближе его ног
                hn = getattr(a, 'near', None) or depth.floor(a.wx, a.wy)          # a.near — вручную, если пол под героем странный
                hide = (n > hn + eps) & np.any(big != before, axis=2)
                big[hide] = before[hide]
    if emit: emit(big, v)
    if bloom_: bloom(big, *bloom_)
    if rays_: rays(big, **rays_)
    if fx_: fx_(big, v)
    if vig: fx.vignette(big, vig)
    if kick[0] or kick[1]:
        dx, dy = int(round(kick[0])), int(round(kick[1]))
        big[:] = np.roll(np.roll(big, dy, 0), dx, 1)
    return big


# ======================================================================= проверка карты
def check(bg_path, out=None):
    """лист для глаз: задник | близость (тепловая) | три слоя параллакса"""
    rgb = np.asarray(Image.open(bg_path).convert('RGB'))
    n = near_map(bg_path)
    h, w = n.shape
    heat = np.stack([np.clip(n * 2 - 0.2, 0, 1), np.clip(1 - np.abs(n - 0.5) * 2, 0, 1) * 0.9, np.clip(1.2 - n * 2, 0, 1)], -1)
    heat = (heat * 255).astype(np.uint8)
    bands = (rgb * 0.35).astype(np.uint8)
    for lo, hi, c in ((0.0, 0.35, (80, 120, 255)), (0.35, 0.65, (90, 230, 120)), (0.65, 1.01, (255, 120, 80))):
        m = (n >= lo) & (n < hi); bands[m] = (bands[m] * 0.5 + np.array(c) * 0.5).astype(np.uint8)
    sheet = np.concatenate([rgb, heat, bands], 1)
    out = out or str(Path(bg_path).with_name(Path(bg_path).stem + '.depth_check.png'))
    Image.fromarray(sheet).save(out)
    return out


if __name__ == '__main__':
    for p_ in sys.argv[1:]: print(check(p_))
