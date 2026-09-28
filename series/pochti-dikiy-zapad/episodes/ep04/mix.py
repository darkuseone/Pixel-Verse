"""Audio mix for S01E04 from timeline.py -> build/ep04/mix.wav (+ mux with video if given).
  python3 mix.py [video.mp4 out.mp4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import subprocess
import paths as P
from timeline import DUR, VOICE, SFX, MUSIC, MUSIC_LOOP, MUSIC_MUTE

inputs, chains, labels = [], [], []
def add_input(path): inputs.extend(['-i', str(path)]); return len(inputs) // 2 - 1

# voice
for vid, ep, key, t0, a, b, who, txt in VOICE:
    i = add_input(P.series() / 'voice' / ep / f'{key}.mp3')
    d = int(t0 * 1000)
    chains.append(f'[{i}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, b - a - 0.03):.3f}:d=0.03,'
                  f'aresample=44100,aformat=channel_layouts=stereo,volume=1.25,adelay={d}|{d}[v_{vid}]')
    labels.append(f'[v_{vid}]')
# sfx
for k, (path, t0, g) in enumerate(SFX):
    i = add_input(P.ROOT / path); d = int(t0 * 1000)
    chains.append(f'[{i}:a]aresample=44100,aformat=channel_layouts=stereo,volume={g},adelay={d}|{d}[s{k}]')
    labels.append(f'[s{k}]')
# music: loop the usable part, duck under speech, mute for the freeze gag
speech = '+'.join(f'between(t,{t0 - 0.05:.2f},{t0 + (b - a) + 0.1:.2f})' for _, _, _, t0, a, b, _, _ in VOICE)
mute = '+'.join(f'between(t,{a},{b})' for a, b in MUSIC_MUTE) or '0'
i = add_input(P.ROOT / MUSIC)
n_loops = int(DUR / (MUSIC_LOOP - 0.5)) + 1
chains.append(f'[{i}:a]atrim=0:{MUSIC_LOOP},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,asplit={n_loops}' +
              ''.join(f'[m{k}]' for k in range(n_loops)))
cur = '[m0]'
for k in range(1, n_loops):
    chains.append(f'{cur}[m{k}]acrossfade=d=0.5:c1=tri:c2=tri[mx{k}]'); cur = f'[mx{k}]'
chains.append(f"{cur}atrim=0:{DUR},volume='if(gt({mute},0),0,if(gt({speech},0),0.10,0.25))':eval=frame[mus]")
labels.append('[mus]')
chains.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR},'
              'alimiter=limit=0.95:level=false[out]')
out = P.build('ep04', 'mix.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(chains), '-map', '[out]', '-ar', '44100', out], check=True)
print(out)
if len(sys.argv) > 2:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', sys.argv[1], '-i', out, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', sys.argv[2]], check=True)
    print(sys.argv[2])
