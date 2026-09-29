"""Generic episode audio mix (any series) from a timeline module -> build/<ep>/mix.wav (+ mux with video).
Timeline module provides DUR, VOICE, SFX, BEDS and optionally VFX (speaker -> extra ffmpeg filter, e.g. phone band)
and VGAIN (speaker -> gain). Beds are looped with acrossfade, faded and ducked under speech.
Usage from an episode folder:  python3 mix.py [noaudio.mp4 final.mp4]   (mix.py there calls run(...))"""
import subprocess
import paths as P

PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.3'


def run(slug, ep, T, video=None, out_mp4=None):
    DUR, VOICE, SFX, BEDS = T.DUR, T.VOICE, T.SFX, T.BEDS
    VFX = getattr(T, 'VFX', {}); VGAIN = getattr(T, 'VGAIN', {})
    inputs, chains, labels = [], [], []

    def add_input(path):
        inputs.extend(['-i', str(path)]); return len(inputs) // 2 - 1

    for vid, vep, key, t0, a, b, who, txt in VOICE:
        i = add_input(P.series(slug) / 'voice' / vep / f'{key}.mp3'); d = int(t0 * 1000)
        extra = (',' + VFX[who]) if who in VFX else ''
        chains.append(f'[{i}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, b - a - 0.03):.3f}:d=0.03,'
                      f'aresample=44100,aformat=channel_layouts=stereo{extra},volume={VGAIN.get(who, 1.45)},adelay={d}|{d}[v_{vid}]')
        labels.append(f'[v_{vid}]')
    for k, s in enumerate(SFX):
        path, t0, g = s[:3]; a, b = (s[3], s[4]) if len(s) > 4 else (None, None)
        i = add_input(P.ROOT / path); d = int(t0 * 1000)
        trim = f'atrim={a}:{b},asetpts=PTS-STARTPTS,' if a is not None else ''
        chains.append(f'[{i}:a]{trim}aresample=44100,aformat=channel_layouts=stereo,volume={g},adelay={d}|{d}[s{k}]')
        labels.append(f'[s{k}]')

    speech = '+'.join(f'between(t,{t0 - 0.05:.2f},{t0 + (b - a) + 0.1:.2f})' for _, _, _, t0, a, b, _, _ in VOICE)
    for k, (path, loop, t0, t1, g, duck) in enumerate(BEDS):
        i = add_input(P.ROOT / path)
        dur = t1 - t0; n = int(dur / (loop - 0.5)) + 1
        if n > 1:
            chains.append(f'[{i}:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,asplit={n}' +
                          ''.join(f'[b{k}_{j}]' for j in range(n)))
        else:
            chains.append(f'[{i}:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo[b{k}_0]')
        cur = f'[b{k}_0]'
        for j in range(1, n):
            chains.append(f'{cur}[b{k}_{j}]acrossfade=d=0.5:c1=tri:c2=tri[bx{k}_{j}]'); cur = f'[bx{k}_{j}]'
        d = int(t0 * 1000)
        vol = f"volume='if(gt({speech},0),{g * 0.4:.3f},{g:.3f})':eval=frame" if duck else f'volume={g}'
        chains.append(f'{cur}atrim=0:{dur},afade=t=in:d=0.02,afade=t=out:st={max(0.0, dur - 0.3):.2f}:d=0.3,adelay={d}|{d},{vol}[bed{k}]')
        labels.append(f'[bed{k}]')

    master = getattr(T, 'MASTER', 1.0)
    chains.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR},'
                  f'volume={master},alimiter=limit=0.95:level=false[out]')
    out = P.build(ep if slug == P.PDZ else f'{slug}-{ep}', 'mix.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(chains), '-map', '[out]', '-ar', '44100', out],
                   check=True)
    print(out)
    if video:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', out, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out_mp4], check=True)
        print(out_mp4)
    return out
