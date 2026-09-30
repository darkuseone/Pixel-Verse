"""«Sunny Palms HOA: The Complete Season» — feature cut (16:9, 1920x1080, 30 fps). Orchestrator.
  python3 movie.py plan                 # block offsets, chapter timestamps
  python3 movie.py sheet <block_id> t..  # contact sheet of a block (block-local seconds), with HUD/card
  python3 movie.py video [workers]      # render all blocks in parallel segments -> build/movie/video.mp4
  python3 movie.py audio                # per-block mixes -> build/movie/audio.wav (loudness-normalised)
  python3 movie.py final                # mux -> movie/final.mp4"""
import kit
from kit import *
import importlib, multiprocessing as mp

OUTD = ROOT / 'build' / 'movie'
ORDER = ['cold', 'title', 'welcome', 'ch1', 'ad', 'ch2i', 'ch2', 'minutes', 'ch3', 'ch4', 'presser', 'subscribe', 'ch5', 'campaign', 'ch6', 'credits', 'post']
_B = {}


def block(bid):
    if bid not in _B: _B[bid] = importlib.import_module(f'blocks.{bid}').BLOCK
    return _B[bid]


def plan():
    t = 0.0; fines = []; chap = []
    for bid in ORDER:
        b = block(bid); b.g0 = t
        for (dt, val) in b.FINES: fines.append((t + dt, val))
        if b.chapter: chap.append((t, b.chapter))
        t += b.n / FPS
    return t, fines, chap


FINES, CHAPS = [], []


def fines_str(g):
    cur = '$0'; prev = '$0'; tc = -9.0
    for (tt, val) in FINES:
        if tt <= g: prev, cur, tc = cur, val, tt
    return cur, prev, tc


def draw_hud(big, g, b):
    if not b.hud: return
    O.overlay(big, _BADGE, 36, 30, 1.0)
    cur, prev, tc = fines_str(g)
    k = (g - tc) / 0.5
    txt = cur
    pulse = 1.0 + 0.25 * math.sin(min(max(k, 0), 1) * math.pi) if 0 <= k < 1 else 1.0
    plate = _plate(txt, pulse, hot=(0 <= k < 1.6))
    O.overlay(big, plate, W_ - plate.shape[1] - 30, 26, 1.0)


_BADGE = None
_PL = {}


def _plate(txt, pulse, hot):
    key = (txt, round(pulse, 2), hot)
    if key in _PL: return _PL[key]
    fs = int(26 * pulse)
    f = O.pfont(fs); f2 = O.pfont(16)
    lab = 'TOTAL FINES'
    w = max(f.getbbox(txt)[2], f2.getbbox(lab)[2]) + 36
    img = Image.new('RGBA', (w, fs + 62), (30, 10, 60, 200)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, fs + 61], outline=(255, 110, 190, 255), width=3)
    d.text(((w - f2.getbbox(lab)[2]) // 2, 10), lab, font=f2, fill=(255, 200, 236, 255))
    d.text(((w - f.getbbox(txt)[2]) // 2, 36), txt, font=f, fill=(255, 84, 96, 255) if hot else (255, 236, 120, 255))
    _PL[key] = np.array(img)
    if len(_PL) > 300: _PL.pop(next(iter(_PL)))
    return _PL[key]


def draw_card(big, u, card):
    """chapter card: dim band, CHAPTER n / neon title / fines so far, slides in and out"""
    if card is None or not (0.0 <= u < 2.0): return
    n, title, sub = card
    a = min(1.0, u / 0.2) * (1 - min(1.0, max(0.0, (u - 1.6) / 0.4)))
    sh = int((1 - min(1.0, u / 0.3)) ** 2 * 500)
    y0, y1 = 360, 720
    reg = big[y0:y1].astype(np.float32)
    band = np.zeros((y1 - y0, W_, 3), np.float32); band[:] = (30, 10, 60)
    tmp = (reg * 0.25 + band * 0.75).astype(np.uint8)
    ptext(tmp, f'CHAPTER {n}', W_ // 2 - sh, 62, 32, (0, 214, 232), (20, 6, 40))
    size = min(96, 1700 // max(1, len(title)))
    ti = O.neon_title([title], size, width=W_)
    O.overlay(tmp, ti, sh, 90, 1.0)
    ptext(tmp, sub, W_ // 2 + sh, 305, 24, (255, 200, 236), (20, 6, 40))
    big[y0:y1] = (reg * (1 - a) + tmp.astype(np.float32) * a).astype(np.uint8)


def render_frame(bi, i):
    b = block(ORDER[bi])
    t = i / FPS
    big = b.render(t)
    draw_card(big, t, b.card)
    draw_hud(big, b.g0 + t, b)
    return big


def init():
    global FINES, CHAPS, _BADGE
    _BADGE = O.make_badge('SUNNY PALMS HOA • THE COMPLETE SEASON', 22)
    tot, FINES, CHAPS = plan()
    return tot


def fmt(t): return f'{int(t // 60)}:{int(t % 60):02d}'


def run_job(job):
    bi, a0, a1, out = job
    init()
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-preset', 'medium', '-crf', os.environ.get('PV_CRF', '20'), '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(a0, a1): proc.stdin.write(render_frame(bi, i).tobytes())
    proc.stdin.close(); proc.wait()
    return out


def jobs_all(seg=300):
    jobs = []
    (OUTD / 'seg').mkdir(parents=True, exist_ok=True)
    for bi, bid in enumerate(ORDER):
        b = block(bid)
        for k, a0 in enumerate(range(0, b.n, seg)):
            jobs.append((bi, a0, min(b.n, a0 + seg), str(OUTD / 'seg' / f'{bi:02d}_{bid}_{k:02d}.mp4')))
    return jobs


def cmd_video(workers=4, only=None):
    init()
    jobs = [j for j in jobs_all() if (not os.path.exists(j[3])) and (only is None or ORDER[j[0]] in only)]
    print(len(jobs), 'segments to render', flush=True)
    with mp.get_context('fork').Pool(workers) as pool:
        for k, out in enumerate(pool.imap_unordered(run_job, jobs), 1): print(f'[{k}/{len(jobs)}] {os.path.basename(out)}', flush=True)
    lst = OUTD / 'segs.txt'
    lst.write_text(''.join(f"file '{j[3]}'\n" for j in jobs_all()))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(OUTD / 'video.mp4')], check=True)
    print('video ok')


def cmd_audio(only=None):
    import mix
    tot = init()
    wavs = []
    for bid in ORDER:
        b = block(bid)
        out = ROOT / 'build' / f'{SLUG}-mv_{bid}' / 'mix.wav'
        if only is None or bid in only:
            if b.VOICE or b.SFX or b.BEDS: mix.run(SLUG, f'mv_{bid}', b, None, None)
            else:
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-t', str(b.n / FPS), str(out)], check=True)
        wavs.append(out)
    OUTD.mkdir(parents=True, exist_ok=True)
    lst = OUTD / 'audio.txt'
    lst.write_text(''.join(f"file '{w}'\n" for w in wavs))
    dry = OUTD / 'dry.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(dry)], check=True)
    # continuous music under the whole film: one looped theme, gain per block, ducked by voices/SFX (sidechain)
    gains = []
    for bid in ORDER:
        b = block(bid)
        for (p_, ln, a_, c_, g_, dk) in b.MUSIC: gains.append((b.g0 + a_, b.g0 + c_, g_))
    track = ROOT / 'series' / SLUG / 'music' / 'sunny_palms_theme_15s.mp3'
    loop = 14.6; n = int(tot / (loop - 0.5)) + 2
    ch = [f'[0:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,asplit={n}' + ''.join(f'[m{j}]' for j in range(n))]
    cur = '[m0]'
    for j in range(1, n):
        ch.append(f'{cur}[m{j}]acrossfade=d=0.5:c1=tri:c2=tri[mx{j}]'); cur = f'[mx{j}]'
    expr = '+'.join(f'{g}*between(t,{a_:.2f},{c_:.2f})' for a_, c_, g in gains) or '0'
    ch.append(f"{cur}atrim=0:{tot:.2f},asetpts=PTS-STARTPTS,volume='{expr}':eval=frame[mus]")
    ch.append('[1:a]asplit=2[k][d]')
    ch.append('[mus][k]sidechaincompress=threshold=0.02:ratio=7:attack=15:release=350:makeup=1[md]')
    ch.append('[d][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95:level=false[out]')
    raw = OUTD / 'audio_raw.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(track), '-i', str(dry), '-filter_complex', ';'.join(ch), '-map', '[out]', '-ar', '44100', str(raw)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', str(OUTD / 'audio.wav')], check=True)
    print('audio ok', tot)


def cmd_final():
    out = HERE / 'final.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUTD / 'video.mp4'), '-i', str(OUTD / 'audio.wav'), '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(out)], check=True)
    print(out)


def cmd_sheet(bid, ts):
    init()
    bi = ORDER.index(bid)
    cols = 3; rows = (len(ts) + cols - 1) // cols
    sheet = Image.new('RGB', (640 * cols, 360 * rows))
    for k, u in enumerate(ts):
        big = render_frame(bi, int(round(u * FPS)))
        sheet.paste(Image.fromarray(big).resize((640, 360), Image.LANCZOS), ((k % cols) * 640, (k // cols) * 360))
    p = OUTD / f'sheet_{bid}.png'; OUTD.mkdir(parents=True, exist_ok=True); sheet.save(p); print(p)


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'plan':
        ORDER[:] = [b for b in ORDER if (HERE / 'blocks' / f'{b}.py').exists()]
        tot = init()
        for bid in ORDER:
            b = block(bid); print(f"{fmt(b.g0)}  {bid:9} {b.n / FPS:6.1f}s" + (f"   <- {b.chapter}" if b.chapter else ''))
        print('TOTAL', fmt(tot), f'({tot:.1f}s, {int(round(tot * FPS))} frames)')
    elif c == 'sheet':
        ORDER[:] = [b for b in ORDER if (HERE / 'blocks' / f'{b}.py').exists()]
        cmd_sheet(sys.argv[2], list(map(float, sys.argv[3:])))
    elif c == 'video':
        ORDER[:] = [b for b in ORDER if (HERE / 'blocks' / f'{b}.py').exists()]
        cmd_video(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif c == 'audio':
        ORDER[:] = [b for b in ORDER if (HERE / 'blocks' / f'{b}.py').exists()]
        cmd_audio(sys.argv[2:] or None)
    elif c == 'final': cmd_final()
