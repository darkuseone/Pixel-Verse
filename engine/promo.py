"""Course promo chip on every RU episode (owner, 30.10.2026): «КАК СДЕЛАТЬ ТАКОЙ МУЛЬТ? / КУРС — В ШАПКЕ ПРОФИЛЯ ▲».
Sits right under the «СЕЗОН • СЕРИЯ» plate (the top ~90 px are covered by the TikTok / Reels tabs), visible from 3,0 s
(after the hook text) until the end card (last 1 s).
  new episodes:   Episode(..., promo='ru')                     (drawn by Episode.main, on top of everything)
  ready videos:   python3 engine/promo.py apply <final.mp4> [out.mp4]     -> out (default final_promo.mp4 next to it),
                  video re-encoded with the chip, audio copied; the original is never overwritten
  preview:        python3 engine/promo.py preview out.png"""
import os, sys, subprocess, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P

T0, TAIL = 3.0, 1.0                     # shown from T0 until dur - TAIL
X, Y = 36, 166                          # under the series plate (overlays.make_badge at y 96, 58 px tall)
LINES = {'ru': ('КАК СДЕЛАТЬ ТАКОЙ МУЛЬТ?', 'КУРС — В ШАПКЕ ПРОФИЛЯ')}
_C = {}


def chip(lang='ru'):
    if lang in _C: return _C[lang]
    a, b = LINES[lang]
    f1, f2 = ImageFont.truetype(P.FONT_BOLD, 27), ImageFont.truetype(P.FONT_BOLD, 31)
    w = int(max(f1.getlength(a), f2.getlength(b) + 40)) + 40
    h = 92
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 14, fill=(20, 12, 10, 150))
    d.text((20, 8), a, font=f1, fill=(255, 244, 214, 230))
    d.text((20, 44), b, font=f2, fill=(255, 200, 50, 255))
    ax = 20 + int(f2.getlength(b)) + 14                                   # ▲ arrow: «look up at the profile header»
    d.polygon([(ax, 72), (ax + 22, 72), (ax + 11, 52)], fill=(255, 200, 50, 255))
    _C[lang] = np.array(im)
    return _C[lang]


def visible(t, dur):
    return T0 <= t < dur - TAIL


def draw(fr, t, dur, lang='ru'):
    if not visible(t, dur): return
    c = chip(lang)
    k = min(1.0, (t - T0) / 0.25)                                         # quick fade-in
    h, w = c.shape[:2]
    reg = fr[Y:Y + h, X:X + w].astype(np.float32)
    al = c[..., 3:4].astype(np.float32) / 255 * k
    fr[Y:Y + h, X:X + w] = (reg * (1 - al) + c[..., :3] * al).astype(np.uint8)


def apply(src, dst=None, lang='ru'):
    src = pathlib.Path(src).resolve()
    dst = pathlib.Path(dst) if dst else src.with_name('final_promo.mp4')
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(src)],
                               capture_output=True, text=True).stdout)
    png = dst.with_suffix('.chip.png')
    Image.fromarray(chip(lang)).save(png)
    crf = os.environ.get('PV_CRF', '20')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-loop', '1', '-i', str(png), '-filter_complex',
                    f"[1:v]format=rgba,fade=in:st={T0}:d=0.25:alpha=1[c];[0:v][c]overlay={X}:{Y}:shortest=1:enable='between(t,{T0},{dur - TAIL:.3f})'[v]",
                    '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-crf', crf, '-pix_fmt', 'yuv420p', '-c:a', 'copy', str(dst)], check=True)
    png.unlink()
    print(dst)
    return dst


if __name__ == '__main__':
    a = sys.argv
    if a[1] == 'apply':
        apply(a[2], a[3] if len(a) > 3 and not a[3].startswith('--') else None, a[a.index('--lang') + 1] if '--lang' in a else 'ru')
    elif a[1] == 'preview':
        Image.fromarray(chip('ru')).save(a[2]); print(a[2])
