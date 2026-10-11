"""Machine critic (rule 10.10.2026, «критик», cheap part): renders the middle of every shot straight from the episode code with a
render log (stage.LOG) and checks what a vision critic used to find by eye — at zero Claude tokens:

  CUT_SIGN     a sign / sticker decal cut by the frame edge while it is still sharp (should be whole, out of frame or soft)
  TEXT_FACE    a caption / sticker / card / hook title over a character's face
  PLATE        the episode plate over a sharp sign
  HEAD_CUT     a face cut by the frame edge
  SEAM         (--seams, experimental) a straight colour step across the frame; off by default: too many false hits
  TIMING       length 30–38 s, twist at 50–60 % and <= 18 s, shots longer than 3.2 s
  AUDIO        mean -20…-22 dB, peak <= 0 dB (from final.mp4 if present)
  COVER        cover.png + cover_grid.png exist

  python3 engine/autocheck.py series/<slug>/episodes/epNN [--times t1 t2 ...]
    -> episodes/epNN/autocheck.md + build/<slug>-epNN/review/ (mid-shot frames, 3x2 sheets with the findings boxed in red)

The sheets are what a vision critic (sub-agent on a cheap model, or me) looks at — 3–4 images instead of 40 full frames."""
import sys, os, json, subprocess, importlib, pathlib, math, re
import numpy as np
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'engine'))
import stage as ST

W, H = ST.OUT_W, ST.OUT_H
SEAMS = '--seams' in sys.argv          # experimental seam scan (off by default: flat pixel-art edges look the same)


def _area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def _inter(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))


def _circle_box_overlap(face, box):
    """fraction of the face disc's bounding square covered by box"""
    cx, cy, r = face
    sq = (cx - r * 0.8, cy - r * 0.8, cx + r * 0.8, cy + r * 0.8)
    a = _area(sq)
    return _area(_inter(sq, box)) / a if a > 0 else 0.0


def seams(img):
    """ARTIFICIAL straight edges across the frame: a shade / tint band or a half-screen colour split changes every pixel of a row
    (column) by the SAME factor or offset although the picture along that row is varied. Natural edges (a sign band between two flat
    colours, a fence line under trees) are skipped: there the content is flat or the change differs from pixel to pixel."""
    L = img.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)
    out = []
    for axis, kind in ((0, 'row'), (1, 'col')):
        A = L if axis == 0 else L.T
        a, b = A[:-1], A[1:]
        var = a.std(1)                                           # the picture along the line is varied
        am, bm = a.mean(1, keepdims=True), b.mean(1, keepdims=True)
        alpha = ((a - am) * (b - bm)).mean(1) / np.maximum(var ** 2, 1e-3)          # per line fit  b = alpha * a + beta
        beta = bm[:, 0] - alpha * am[:, 0]
        fit = (np.abs(b - (alpha[:, None] * a + beta[:, None])) < 7).mean(1)
        moved = np.abs((alpha - 1) * 128 + beta) > 18                               # a mid-grey pixel changes visibly
        hit = np.where((var > 12) & (fit > 0.85) & moved)[0]
        n = A.shape[0]
        for i in hit:
            if 4 < i < n - 5: out.append((kind, int(i) + 1, float(abs((alpha[i] - 1) * 128 + beta[i]) / 255)))
    return out


def analyse(frame, log, t, shot):
    F = []
    faces = [e['face'] for e in log if e['kind'] == 'sprite' and e.get('face') and e['face'][2] >= 30]
    texts = [e for e in log if e['kind'] in ('caption', 'sticker', 'card', 'title')]
    plate = next((e['bbox'] for e in log if e['kind'] == 'plate'), None)
    for e in log:
        if e['kind'] != 'decal': continue
        full, vis = e['full'], e['bbox']
        fa = _area(full)
        if fa <= 0: continue
        frac = _area(vis) / fa
        hpx = full[3] - full[1]
        x0, y0, x1, y1 = [int(v) for v in vis]
        reg = frame[y0:y1, x0:x1].astype(np.int16)
        m = e['mask']
        if m.shape != reg.shape[:2] or not m.any(): continue
        sharp = np.abs(reg - e['patch'].astype(np.int16)).sum(-1)[m].mean() < 14      # drawn as is (not blurred, not covered)
        if e.get('prop'): continue                                                     # a flamingo cut by the edge is fine
        if 0.05 < frac < 0.97 and hpx >= 50:
            if sharp:
                big_ = hpx >= 240 or (full[2] - full[0]) >= 330            # a subject-sized sign; small background signs may be cut
                sev = 'FIX' if big_ else 'NIT'
                F.append(dict(t=t, shot=shot, code='CUT_SIGN', sev=sev, box=vis,
                              msg=f'sign cut by the frame edge ({frac:.0%} visible, {hpx:.0f} px tall), sharp'))
        if plate and sharp and _area(_inter(plate, vis)) > 0.3 * _area(plate) and hpx >= 50:
            x0, y0, x1, y1 = [int(v) for v in _inter(plate, vis)]
            F.append(dict(t=t, shot=shot, code='PLATE', sev='NIT', box=(x0, y0, x1, y1), msg='episode plate over a sign'))
    for tx in texts:
        for fc in faces:
            ov = _circle_box_overlap(fc, tx['bbox'])
            if ov > 0.12:
                cx, cy, r = fc
                F.append(dict(t=t, shot=shot, code='TEXT_FACE', sev='FIX' if ov > 0.25 else 'NIT', box=tx['bbox'],
                              msg=f"{tx['kind']} covers a face ({ov:.0%} of it) at ({cx:.0f}, {cy:.0f})"))
    for fc in faces:
        cx, cy, r = fc
        if 0 <= cx < W and 0 <= cy < H:
            out = max(0, r - cx, cx + r - W, r - cy) / (2 * r)
            if out > 0.3:
                F.append(dict(t=t, shot=shot, code='HEAD_CUT', sev='NIT', box=(cx - r, cy - r, cx + r, cy + r),
                              msg=f'face {out:.0%} out of frame'))
    if SEAMS:                                                     # experimental: too many false hits on flat pixel-art edges
        for kind, pos, fr in seams(frame):
            box = (0, pos - 3, W, pos + 3) if kind == 'row' else (pos - 3, 0, pos + 3, H)
            F.append(dict(t=t, shot=shot, code='SEAM', sev='NIT', box=box, msg=f'straight {kind} edge at {pos} — intended?'))
    return F


def timing(tl):
    F = []
    dur = tl.DUR
    if not (30.0 <= dur <= 38.0): F.append(dict(code='TIMING', sev='FIX', msg=f'length {dur:.1f} s (30–38)'))
    tw = getattr(tl, 'TWIST', None)
    if tw is not None:
        r = tw / dur
        if not (0.50 <= r <= 0.60) or tw > 18.0: F.append(dict(code='TIMING', sev='FIX', msg=f'twist at {tw:.2f} s = {r:.0%} (50–60 %, <= 18 s)'))
    for a, b in zip(tl.CUTS[:-1], tl.CUTS[1:]):
        if b - a > 3.2: F.append(dict(code='TIMING', sev='NIT', msg=f'shot {a:.2f}–{b:.2f} lasts {b - a:.1f} s (> 3 s)'))
    return F


def audio(path):
    if not path.exists(): return [dict(code='AUDIO', sev='NIT', msg='no final.mp4 yet')]
    r = subprocess.run(['ffmpeg', '-v', 'info', '-i', str(path), '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True)
    mean = re.search(r'mean_volume: (-?[\d.]+)', r.stderr); mx = re.search(r'max_volume: (-?[\d.]+)', r.stderr)
    F = []
    if mean and not (-23.0 <= float(mean.group(1)) <= -19.0): F.append(dict(code='AUDIO', sev='FIX', msg=f'mean {mean.group(1)} dB (-20…-22)'))
    if mx and float(mx.group(1)) > 0.0: F.append(dict(code='AUDIO', sev='FIX', msg=f'peak {mx.group(1)} dB (> 0)'))
    info = f"mean {mean.group(1) if mean else '?'} dB, peak {mx.group(1) if mx else '?'} dB"
    return F, info


def main():
    ep = pathlib.Path(sys.argv[1]).resolve()
    name, slug = ep.name, ep.parents[1].name
    times = None
    if '--times' in sys.argv: times = [float(x) for x in sys.argv[sys.argv.index('--times') + 1:] if not x.startswith('--')]
    os.chdir(ep); sys.path.insert(0, str(ep))
    tl = importlib.import_module('timeline')
    mod = importlib.import_module(name)
    out = ROOT / 'build' / f'{slug}-{name}' / 'review'
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob('*.png'): f.unlink()
    cuts = list(tl.CUTS)
    names = getattr(mod, 'NAMES', [str(i) for i in range(len(cuts) - 1)])
    if times is None: times = [round((a + b) / 2, 2) for a, b in zip(cuts[:-1], cuts[1:])]
    F, frames = [], []
    for t in times:
        i = max(k for k in range(len(cuts) - 1) if cuts[k] <= t)
        ST.LOG[0] = []; ST.T_NOW[0] = t
        fr = mod.render(t)
        log = ST.LOG[0]; ST.LOG[0] = None
        found = analyse(fr, log, t, names[i] if i < len(names) else str(i))
        F += found
        p = out / f'f_{t:05.2f}.png'
        Image.fromarray(fr).save(p)
        frames.append((t, names[i] if i < len(names) else str(i), p, found))
        print(f'{t:6.2f} {names[i] if i < len(names) else i:14s} {len(found)} finding(s)', flush=True)
    F += timing(tl)
    au = audio(ep / 'final.mp4')
    ainfo = ''
    if isinstance(au, tuple): au, ainfo = au
    F += au
    for c in ('cover.png', 'cover_grid.png'):
        if not (ep / c).exists(): F.append(dict(code='COVER', sev='FIX', msg=f'{c} missing'))
    # review sheets: 3x2 frames at 540x960, findings boxed (red = FIX, yellow = NIT), time + shot name on top
    for j in range(0, len(frames), 6):
        sheet = Image.new('RGB', (540 * 3, 960 * 2), (16, 16, 16))
        for q, (t, nm, p, found) in enumerate(frames[j:j + 6]):
            im = Image.open(p).convert('RGB')
            d = ImageDraw.Draw(im)
            for f in found:
                x0, y0, x1, y1 = [int(v) for v in f['box']]
                d.rectangle([x0, y0, x1, y1], outline=(255, 40, 40) if f['sev'] == 'FIX' else (255, 220, 40), width=8)
            im = im.resize((540, 960), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            d.rectangle([0, 900, 540, 960], fill=(0, 0, 0))
            d.text((10, 912), f'{t:.2f}s  {nm}  ({len(found)})', fill=(255, 255, 255))
            sheet.paste(im, ((q % 3) * 540, (q // 3) * 960))
        sheet.save(out / f'sheet_{j // 6:02d}.png')
    nfix = sum(1 for f in F if f.get('sev') == 'FIX')
    lines = [f'# Autocheck {slug} {name}', '', f'Frames: {len(times)} (middle of every shot). Audio: {ainfo or "-"}.', '']
    for f in sorted(F, key=lambda f: (f.get('sev') != 'FIX', f.get('t', 99))):
        where = f"{f['t']:.2f}s {f['shot']} " if 't' in f else ''
        box = f" box {tuple(int(v) for v in f['box'])}" if 'box' in f else ''
        lines.append(f"- **{f['sev']}** {f['code']} {where}— {f['msg']}{box}")
    lines += ['', f'RESULT: {nfix} FIX, {len(F) - nfix} NIT', f'Review sheets: {out}']
    (ep / 'autocheck.md').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
