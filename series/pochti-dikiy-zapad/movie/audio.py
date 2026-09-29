"""Per-block audio mix (voice + sfx + ducked beds) for the feature cut -> build/movie/audio/<id>.wav (exact block length)."""
import os, sys, pathlib, subprocess, importlib.util
os.environ['PV_WIDE'] = '1'
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine'))
import paths as P


def timeline_of(block):
    """(DUR, VOICE, SFX, BEDS) of a block spec"""
    if block['kind'] == 'new':
        spec = importlib.util.spec_from_file_location('tl_' + block['mod'], HERE / 'blocks' / f"{block['mod']}.py")
        src = (HERE / 'blocks' / f"{block['mod']}.py").read_text()
        # cheap import-free extraction: execute only the constant definitions (VOICE/SFX/BEDS/DUR)
        ns = {}
        import ast
        tree = ast.parse(src)
        keep = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('DUR', 'VOICE', 'SFX', 'BEDS') for t in n.targets)]
        exec(compile(ast.Module(body=keep, type_ignores=[]), 'tl', 'exec'), ns)
        return ns['DUR'], ns['VOICE'], ns.get('SFX', []), ns.get('BEDS', [])
    spec = importlib.util.spec_from_file_location('tl_' + block['dir'], HERE / 'chapters' / block['dir'] / 'timeline.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    beds = getattr(m, 'BEDS', None)
    if beds is None:                                   # E03: single looped theme
        beds = [(m.MUSIC, m.MUSIC_LOOP, 0.0, m.DUR, 0.25, True)]
    return m.DUR, m.VOICE, m.SFX, beds


def mix_block(block, out):
    dur_all, VOICE, SFX, BEDS = timeline_of(block)
    t_in, t_out = block['t_in'], block['t_out'] if block['t_out'] is not None else dur_all
    L = t_out - t_in
    inputs, chains, labels = [], [], []

    def add_input(path):
        inputs.extend(['-i', str(path)]); return len(inputs) // 2 - 1

    speech_terms = []
    for vid, ep, key, t0, a, b, who, txt in VOICE:
        end = t0 + (b - a)
        if end <= t_in or t0 >= t_out: continue
        a2 = a + max(0.0, t_in - t0); t02 = max(t0, t_in); b2 = b - max(0.0, end - t_out)
        if b2 - a2 < 0.05: continue
        g = t02 - t_in
        i = add_input(P.series() / 'voice' / ep / f'{key}.mp3'); d = int(g * 1000)
        chains.append(f'[{i}:a]atrim={a2:.3f}:{b2:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, b2 - a2 - 0.03):.3f}:d=0.03,'
                      f'aresample=44100,aformat=channel_layouts=stereo,volume=1.45,adelay={d}|{d}[v{len(labels)}]')
        labels.append(f'[v{len(labels)}]')
        speech_terms.append((g - 0.05, g + (b2 - a2) + 0.1))
    for path, t0, gain in SFX:
        if not (t_in <= t0 < t_out): continue
        i = add_input(ROOT / path); d = int((t0 - t_in) * 1000)
        chains.append(f'[{i}:a]aresample=44100,aformat=channel_layouts=stereo,volume={gain},adelay={d}|{d}[s{len(labels)}]')
        labels.append(f'[s{len(labels)}]')
    for k, (path, loop, t0, t1, g, duck) in enumerate(BEDS):
        a0, a1 = max(t0, t_in), min(t1, t_out)
        if a1 - a0 < 0.3: continue
        dur = a1 - a0; off = a0 - t_in
        i = add_input(ROOT / path)
        n = int(dur / (loop - 0.5)) + 1
        if n > 1:
            chains.append(f'[{i}:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,asplit={n}' + ''.join(f'[b{k}_{j}]' for j in range(n)))
        else:
            chains.append(f'[{i}:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo[b{k}_0]')
        cur = f'[b{k}_0]'
        for j in range(1, n):
            chains.append(f'{cur}[b{k}_{j}]acrossfade=d=0.5:c1=tri:c2=tri[bx{k}_{j}]'); cur = f'[bx{k}_{j}]'
        d = int(off * 1000)
        terms = [f'between(t,{s:.2f},{e:.2f})' for s, e in speech_terms if e > off - 0.2 and s < off + dur + 0.2]
        sp = '+'.join(terms) or '0'
        vol = f"volume='if(gt({sp},0),{g * 0.4:.3f},{g:.3f})':eval=frame" if duck else f'volume={g}'
        fin = 0.05 if t0 < t_in + 0.01 and t_in > 0 else 0.25
        chains.append(f'{cur}atrim=0:{dur:.3f},afade=t=in:d={fin},afade=t=out:st={max(0, dur - 0.3):.2f}:d=0.3,adelay={d}|{d},{vol}[bed{k}]')
        labels.append(f'[bed{k}]')
    if not labels:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=stereo', '-t', f'{L:.3f}', out], check=True); return
    chains.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{L:.3f},apad=whole_dur={L:.3f},alimiter=limit=0.95:level=false[out]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(chains), '-map', '[out]', '-ar', '44100', '-ac', '2', out], check=True)
