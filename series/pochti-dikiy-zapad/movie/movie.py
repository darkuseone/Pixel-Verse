"""«Почти Дикий Запад» — Сезон 1, режиссёрская версия (16:9, 1920x1080, 30 fps). Orchestrator.
  python3 movie.py plan                 # block offsets, chapter timestamps
  python3 movie.py sheet <block_id> t..  # contact sheet of a block (local block time, with chapter card)
  python3 movie.py video [workers]      # render all blocks in parallel -> build/movie/video.mp4
  python3 movie.py audio                # per-block mixes -> build/movie/audio.wav (loudness-normalised)
  python3 movie.py final                # mux -> movie/final.mp4
"""
import os, sys, json, pathlib, subprocess, importlib
os.environ['PV_WIDE'] = '1'
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine')); sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / 'blocks'))
FPS = 30
OUTD = ROOT / 'build' / 'movie'


def N(id, mod, t_in=0.0, t_out=None, card=None, chapter=None):
    return dict(id=id, kind='new', mod=mod, t_in=t_in, t_out=t_out, card=card, chapter=chapter)


def C_(id, d, mod, t_in=0.0, t_out=None, card=None, chapter=None):
    return dict(id=id, kind='ch', dir=d, mod=mod, t_in=t_in, t_out=t_out, card=card, chapter=chapter)


BLOCKS = [
    N('cold', 'cold'),
    N('title', 'title'),
    N('ch1', 'ch1', card=(1, 'САМЫЙ БЫСТРЫЙ', 1), chapter='Глава 1. Самый быстрый'),
    N('ad', 'ad'),
    N('ch2', 'ch2', card=(2, 'ЗАСАДА', 118), chapter='Глава 2. Засада'),
    N('board', 'board'),
    N('gate', 'gate', card=(3, 'ИНФОРМАТОР', 340), chapter='Глава 3. Информатор'),
    C_('ep03', 'ch_ep03', 'ep03', 0.0, 44.0),
    N('dismiss', 'dismiss', card=(4, 'ПРОКАТ', 620), chapter='Глава 4. Прокат'),
    C_('ep04a', 'ch_ep04', 'ep04', 0.0, 37.2),
    N('contract', 'contract'),
    C_('ep04b', 'ch_ep04', 'ep04', 37.2, 44.4),
    N('subscribe', 'subscribe', chapter='Пауза на подписку'),
    C_('ep05a', 'ch_ep05', 'ep05', 0.0, 11.4, card=(5, 'ПОЧТИ ПОЙМАЛ', 900), chapter='Глава 5. Почти поймал'),
    N('jump', 'jump'),
    C_('ep05b', 'ch_ep05', 'ep05', 11.4, 44.0),
    N('training', 'training', card=(6, 'САМЫЙ БЫСТРЫЙ. РЕВАНШ', 1090), chapter='Глава 6. Самый быстрый. Реванш'),
    C_('ep06', 'ch_ep06', 'ep06', 0.0, 44.6),
    N('finale', 'finale', chapter='Финал и титры'),
    N('post', 'post', chapter='Сцена после титров'),
]


def block_dur(b):
    if b['t_out'] is not None: return b['t_out'] - b['t_in']
    import audio
    return audio.timeline_of(b)[0] - b['t_in']


def plan():
    t = 0.0
    for b in BLOCKS:
        d = block_dur(b); b['g0'] = t; b['n'] = int(round(d * FPS)); t += b['n'] / FPS
    return t


# ---------------------------------------------------------------- chapter card
def draw_card(big, u, card):
    if card is None or not (0.1 <= u < 2.6): return
    import numpy as np
    import overlays as O, wideov as WO
    a = min(1.0, (u - 0.1) / 0.25) * (1 - min(1.0, max(0.0, (u - 2.2) / 0.35)))
    n, title, day = card
    y0, y1 = 340, 700
    reg = big[y0:y1].astype(np.float32)
    layer = (reg * 0.28 + np.array([12, 8, 6], np.float32) * 0.72)
    shift = int((1 - min(1.0, (u - 0.1) / 0.3)) ** 2 * 300)
    band = layer.copy()
    tmp = np.zeros((360, 1920, 3), np.uint8); tmp[:] = band.astype(np.uint8)
    WO.ptext(tmp, f'ГЛАВА {n}', 960 - shift, 60, 38, (255, 190, 90), 'c')
    size = min(84, 1700 // len(title))
    ti = O.pixel_title([title], size, width=1920)
    O.overlay(tmp, ti, -shift, 105, 1.0)
    WO.ptext(tmp, f'ДЕНЬ {day}', 960 + shift, 300, 28, (255, 240, 200), 'c')
    big[y0:y1] = (reg * (1 - a) + tmp.astype(np.float32) * a).astype(np.uint8)


# ---------------------------------------------------------------- worker
_MODS = {}


def module_of(b):
    key = (b['kind'], b.get('dir'), b['mod'])
    if key not in _MODS:
        import kit
        if b['kind'] == 'new':
            _MODS[key] = importlib.import_module(b['mod'])
        else:
            _MODS[key] = kit.load_chapter(b['dir'], b['mod'])
    return _MODS[key]


def render_frame(b, i):
    m = module_of(b)
    u = i / FPS
    t = b['t_in'] + u
    big = m.render(t)
    draw_card(big, u, b['card'])
    return big


def run_job(job):
    bi, a0, a1, out = job
    b = BLOCKS[bi]
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-preset', 'medium', '-crf', os.environ.get('PV_CRF', '20'), '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(a0, a1):
        proc.stdin.write(render_frame(b, i).tobytes())
    proc.stdin.close(); proc.wait()
    return out


def jobs_all(seg=300):
    jobs = []
    (OUTD / 'seg').mkdir(parents=True, exist_ok=True)
    for bi, b in enumerate(BLOCKS):
        for k, a0 in enumerate(range(0, b['n'], seg)):
            jobs.append((bi, a0, min(b['n'], a0 + seg), str(OUTD / 'seg' / f"{bi:02d}_{b['id']}_{k:02d}.mp4")))
    return jobs


def cmd_video(workers=4):
    import multiprocessing as mp
    plan()
    jobs = [j for j in jobs_all() if not os.path.exists(j[3])]
    print(len(jobs), 'segments to render', flush=True)
    with mp.get_context('fork').Pool(workers) as pool:
        for k, out in enumerate(pool.imap(run_job, jobs), 1):
            print(f'[{k}/{len(jobs)}] {os.path.basename(out)}', flush=True)
    allj = jobs_all()
    lst = OUTD / 'segs.txt'
    lst.write_text(''.join(f"file '{j[3]}'\n" for j in allj))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(OUTD / 'video.mp4')], check=True)
    print('video ok')


def cmd_audio():
    import audio
    total = plan()
    (OUTD / 'audio').mkdir(parents=True, exist_ok=True)
    wavs = []
    for b in BLOCKS:
        out = OUTD / 'audio' / f"{b['id']}.wav"
        audio.mix_block(dict(b, t_out=b['t_in'] + b['n'] / FPS), str(out)); wavs.append(out)
        print('audio', b['id'], flush=True)
    lst = OUTD / 'audio.txt'
    lst.write_text(''.join(f"file '{w}'\n" for w in wavs))
    raw = OUTD / 'audio_raw.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(raw)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', str(OUTD / 'audio.wav')], check=True)
    print('audio ok', total)


def cmd_final():
    out = HERE / 'final.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUTD / 'video.mp4'), '-i', str(OUTD / 'audio.wav'), '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(out)], check=True)
    print(out)


def cmd_sheet(bid, ts):
    import numpy as np
    from PIL import Image
    plan()
    b = next(x for x in BLOCKS if x['id'] == bid)
    cols = 3; rows = (len(ts) + cols - 1) // cols
    sheet = Image.new('RGB', (480 * cols, 270 * rows))
    for k, u in enumerate(ts):
        m = module_of(b)
        big = m.render(b['t_in'] + u); draw_card(big, u, b['card'])
        sheet.paste(Image.fromarray(big).resize((480, 270), Image.LANCZOS), ((k % cols) * 480, (k // cols) * 270))
    p = OUTD / f'sheet_{bid}.png'; OUTD.mkdir(parents=True, exist_ok=True); sheet.save(p); print(p)


def fmt(t): return f'{int(t // 60)}:{int(t % 60):02d}'


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'plan':
        tot = plan()
        for b in BLOCKS: print(f"{fmt(b['g0'])}  {b['id']:9} {b['n'] / FPS:6.1f}s" + (f"   <- {b['chapter']}" if b['chapter'] else ''))
        print('TOTAL', fmt(tot), f'({tot:.1f}s, {sum(b["n"] for b in BLOCKS)} frames)')
    elif c == 'sheet': cmd_sheet(sys.argv[2], list(map(float, sys.argv[3:])))
    elif c == 'video': cmd_video(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif c == 'audio': cmd_audio()
    elif c == 'final': cmd_final()
