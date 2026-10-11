"""End card «SUBSCRIBE!» / «ПОДПИШИСЬ!» (owner rule 12.10.2026): a big pixel-text card in the series' own style pops in during the
last 1.0 s of every Short (3.0 s in the 16:9 extended version) and the video ends right on it. Slot (top / centre / bottom) is picked
where it covers no face and no caption.

  python3 engine/endcard.py apply series/<slug>/episodes/epNN [--lang us|ru] [--sec 1.0]   # finished final.mp4, no re-render
  python3 engine/endcard.py preview <style> <lang> out.png
In new episodes the card goes straight into the render: Episode(..., endcard=dict(style=..., lang=...)) (engine/episode.py).
Styles: 'fm' (Florida Man: postcard letters + (ALLEGEDLY) stamp + pixel bell), 'default' (any series: Press Start 2P, outline, glow).
"""
import sys, math, subprocess, pathlib, importlib, os
import numpy as np
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'engine'))
import overlays as O
import stage as ST

TEXT = dict(us='SUBSCRIBE!', ru='ПОДПИШИСЬ!')
SFX = ROOT / 'library' / 'sfx' / 'pushpin_pop.mp3'
_CACHE = {}

BELL = ['....XX....', '...XXXX...', '..XXXXXX..', '..XXXXXX..', '..XXXXXX..', '.XXXXXXXX.', 'XXXXXXXXXX', '....XX....']


def _bell(px=12, col=(255, 214, 40)):
    h, w = len(BELL), len(BELL[0])
    a = np.zeros(((h + 2) * px, (w + 2) * px, 4), np.uint8)
    for r, row in enumerate(BELL):
        for c, ch in enumerate(row):
            if ch == 'X':
                a[(r + 1) * px:(r + 2) * px, (c + 1) * px:(c + 2) * px] = col + (255,)
    m = a[..., 3] > 0
    ol = O._dilate(m, px // 2 + 2) & ~m
    a[ol] = (24, 18, 40, 255)
    return a


def _stack(parts, width, gap=10):
    h = sum(p.shape[0] for p in parts) + gap * (len(parts) - 1)
    out = np.zeros((h, width, 4), np.uint8)
    y = 0
    for p in parts:
        x = (width - p.shape[1]) // 2
        out[y:y + p.shape[0], x:x + p.shape[1]] = np.where(p[..., 3:4] > 0, p, out[y:y + p.shape[0], x:x + p.shape[1]])
        y += p.shape[0] + gap
    return out


def _trim(a):
    m = a[..., 3] > 0
    r = np.where(m.any(1))[0]; c = np.where(m.any(0))[0]
    return a[r[0]:r[-1] + 1, c[0]:c[-1] + 1] if len(r) else a


def card(style='default', lang='us', width=None):
    width = width or ST.OUT_W
    key = (style, lang, width)
    if key in _CACHE: return _CACHE[key]
    txt = TEXT[lang]
    def fit(a, maxw):
        if a.shape[1] <= maxw: return a
        f = maxw / a.shape[1]
        return np.array(Image.fromarray(a).resize((int(a.shape[1] * f), int(a.shape[0] * f)), Image.NEAREST))
    if style == 'fm':
        from props import fmkit as K
        title = fit(_trim(K.hook_title([txt], 120 if width <= 1080 else 150, width=width + 400, depth=18)), width - 60)
        stamp = K.allegedly_stamp(48)
        bell = _bell(12)
        row = np.zeros((max(stamp.shape[0], bell.shape[0]), bell.shape[1] + 30 + stamp.shape[1], 4), np.uint8)
        row[(row.shape[0] - bell.shape[0]) // 2:(row.shape[0] - bell.shape[0]) // 2 + bell.shape[0], :bell.shape[1]] = bell
        row[(row.shape[0] - stamp.shape[0]) // 2:(row.shape[0] - stamp.shape[0]) // 2 + stamp.shape[0], bell.shape[1] + 30:] = stamp
        img = _stack([title, row], width, gap=4)
    else:
        img = fit(O.sticker(txt, fg=(255, 214, 60), size=104 if width <= 1080 else 120, icon=_bell(11)), width - 30)
    _CACHE[key] = img
    return img


def draw(big, img, t, t0, cy):
    """pop-in with an overshoot and a tiny bounce, centred at height cy; stays to the end"""
    if t < t0: return
    u = t - t0
    s = min(1.0, u / 0.10) * (1.0 + 0.16 * math.sin(min(u, 0.45) * 16) * math.exp(-u * 7))
    s = max(0.25, s)
    im = img if abs(s - 1) < 0.01 else np.array(Image.fromarray(img).resize((max(1, int(img.shape[1] * s)), max(1, int(img.shape[0] * s))), Image.NEAREST))
    bounce = -abs(math.sin(u * 9)) * 24 * math.exp(-u * 5)
    O.overlay(big, im, int((big.shape[1] - im.shape[1]) / 2), int(cy - im.shape[0] / 2 + bounce), 1.0)


def pick_slot(frames_logs, h_card, H=None):
    """choose the card centre (top / middle / bottom third) that covers the least of faces and captions in the logged frames"""
    H = H or ST.OUT_H
    slots = [max(int(H * 0.155), 168 + int(h_card) // 2), int(H * 0.50), int(H * 0.80)]   # top: below the episode plate, centre, bottom
    best, score_best = slots[0], 1e18
    for cy in slots:
        box = (0, cy - h_card / 2 - 20, ST.OUT_W, cy + h_card / 2 + 20)
        sc = 0.0
        for log in frames_logs:
            for e in log:
                if e['kind'] == 'sprite' and e.get('face'):
                    fx, fy, r = e['face']
                    ov = max(0, min(box[3], fy + r) - max(box[1], fy - r)) * max(0, min(box[2], fx + r) - max(box[0], fx - r))
                    sc += 6.0 * ov                                                   # faces matter most
                elif e['kind'] in ('caption', 'sticker', 'title', 'card'):
                    b = e['bbox']
                    sc += max(0, min(box[3], b[3]) - max(box[1], b[1])) * max(0, min(box[2], b[2]) - max(box[0], b[0]))
        sc += abs(cy - slots[0]) * 0.5                                       # prefer the top when it is equally free
        if sc < score_best: best, score_best = cy, sc
    return best


def _episode_logs(ep, t0, t1, n=4):
    """render a few frames of the episode's last second from code with the render log (faces / captions)"""
    cwd = os.getcwd()
    os.chdir(ep); sys.path.insert(0, str(ep))
    try:
        mod = importlib.import_module(ep.name)
        logs = []
        for i in range(n):
            t = t0 + (t1 - t0) * (i + 0.5) / n
            ST.LOG[0] = []; ST.T_NOW[0] = t
            mod.render(t)
            logs.append(ST.LOG[0])
        ST.LOG[0] = None
        return logs
    finally:
        os.chdir(cwd)


def apply_video(src, dst, img, sec, cy, fps=30):
    """overlay the card on the last `sec` seconds of src (video re-encoded, audio kept + a soft pop at the card)"""
    probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration',
                            '-of', 'default=nw=1:nk=1', str(src)], capture_output=True, text=True).stdout.split()
    w, h, dur = int(probe[0]), int(probe[1]), float(probe[2])
    n = int(round(dur * fps)); f0 = n - int(round(sec * fps))
    t0 = f0 / fps
    tmp = pathlib.Path(dst).with_suffix('.v.mp4')
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(src), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', str(fps), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', os.environ.get('PV_CRF', '20'), '-pix_fmt', 'yuv420p', str(tmp)],
                           stdin=subprocess.PIPE)
    i = 0
    while True:
        buf = dec.stdout.read(w * h * 3)
        if len(buf) < w * h * 3: break
        fr = np.frombuffer(buf, np.uint8).reshape(h, w, 3).copy()
        if i >= f0: draw(fr, img, i / fps, t0, cy)
        enc.stdin.write(fr.tobytes()); i += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    ms = int(t0 * 1000)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp), '-i', str(src), '-i', str(SFX),
                    '-filter_complex', f'[2:a]volume=0.55,adelay={ms}|{ms}[p];[1:a][p]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', str(dst)], check=True)
    tmp.unlink()
    return t0


def main():
    a = sys.argv
    if a[1] == 'preview':
        img = card(a[2], a[3])
        bg = np.zeros((ST.OUT_H, ST.OUT_W, 3), np.uint8); bg[:] = (60, 120, 140)
        draw(bg, img, 1.0, 0.0, ST.OUT_H // 2)
        Image.fromarray(bg).save(a[4]); print(a[4]); return
    if a[1] == 'apply':
        ep = pathlib.Path(a[2]).resolve()
        lang = a[a.index('--lang') + 1] if '--lang' in a else 'us'
        sec = float(a[a.index('--sec') + 1]) if '--sec' in a else 1.0
        style = a[a.index('--style') + 1] if '--style' in a else 'default'
        src = ep / 'final.mp4'
        bak = ROOT / 'build' / f'{ep.parents[1].name}-{ep.name}' / 'final_noend.mp4'
        bak.parent.mkdir(parents=True, exist_ok=True)
        if not bak.exists(): subprocess.run(['cp', str(src), str(bak)], check=True)      # always start from the clean master
        img = card(style, lang)
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(bak)],
                                   capture_output=True, text=True).stdout)
        try:
            cy = pick_slot(_episode_logs(ep, dur - sec, dur), img.shape[0])
        except Exception as e:                                               # no code / render error: top slot
            print('slot by default (', e, ')'); cy = int(ST.OUT_H * 0.22)
        t0 = apply_video(bak, src, img, sec, cy)
        print(f'{ep.name}: end card from {t0:.2f} s at y={cy}')


if __name__ == '__main__':
    main()
