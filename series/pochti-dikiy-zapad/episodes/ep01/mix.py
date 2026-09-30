"""Audio mix for S01E06 from timeline.py -> build/ep01/mix.wav (+ mux with video if given).
Beds (music themes, ambience) are looped with acrossfade, windowed, faded and ducked under speech.
  python3 mix.py [video.mp4 out.mp4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import subprocess
import paths as P
from timeline import DUR, VOICE, SFX, BEDS

inputs, chains, labels = [], [], []
def add_input(path): inputs.extend(['-i', str(path)]); return len(inputs) // 2 - 1

for vid, ep, key, t0, a, b, who, txt in VOICE:
    i = add_input(P.series() / 'voice' / ep / f'{key}.mp3'); d = int(t0 * 1000)
    chains.append(f'[{i}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, b - a - 0.03):.3f}:d=0.03,'
                  f'aresample=44100,aformat=channel_layouts=stereo,volume=1.45,adelay={d}|{d}[v_{vid}]')
    labels.append(f'[v_{vid}]')
for k, (path, t0, g) in enumerate(SFX):
    i = add_input(P.ROOT / path); d = int(t0 * 1000)
    chains.append(f'[{i}:a]aresample=44100,aformat=channel_layouts=stereo,volume={g},adelay={d}|{d}[s{k}]')
    labels.append(f'[s{k}]')

speech = '+'.join(f'between(t,{t0 - 0.05:.2f},{t0 + (b - a) + 0.1:.2f})' for _, _, _, t0, a, b, _, _ in VOICE)
for k, (path, loop, t0, t1, g, duck) in enumerate(BEDS):
    i = add_input(P.ROOT / path)
    dur = t1 - t0; n = int(dur / (loop - 0.5)) + 1
    chains.append(f'[{i}:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,asplit={n}' +
                  ''.join(f'[b{k}_{j}]' for j in range(n)) if n > 1 else
                  f'[{i}:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo[b{k}_0]')
    cur = f'[b{k}_0]'
    for j in range(1, n):
        chains.append(f'{cur}[b{k}_{j}]acrossfade=d=0.5:c1=tri:c2=tri[bx{k}_{j}]'); cur = f'[bx{k}_{j}]'
    d = int(t0 * 1000)
    vol = f"volume='if(gt({speech},0),{g * 0.4:.3f},{g:.3f})':eval=frame" if duck else f'volume={g}'
    chains.append(f'{cur}atrim=0:{dur},afade=t=in:d=0.25,afade=t=out:st={dur - 0.3:.2f}:d=0.3,adelay={d}|{d},{vol}[bed{k}]')
    labels.append(f'[bed{k}]')

chains.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR},'
              'alimiter=limit=0.95:level=false[out]')
out = P.build('ep01', 'mix.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(chains), '-map', '[out]', '-ar', '44100', out], check=True)
print(out)
if len(sys.argv) > 2:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', sys.argv[1], '-i', out, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', sys.argv[2]], check=True)
    print(sys.argv[2])
