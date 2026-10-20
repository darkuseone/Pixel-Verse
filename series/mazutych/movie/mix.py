"""Audio for «СЛЕДСТВИЕ ПО БЕНЗИНУ»: lines + point SFX + ambience / music beds per scene + the flashbacks' own sound
  python3 mix.py [<noaudio.mp4> <final.mp4>]   (default: build/mazutych-movie/noaudio.mp4 -> final_h264.mp4 here)"""
import sys, pathlib, subprocess
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine'))
import mix
import timeline as T

for ep in sorted({c['ep'] for c in T.CLIPS}):                    # the flashbacks' sound = the episode's final mix
    out = ROOT / 'build' / f'{T.SLUG}-movie' / f'fb_{ep}.wav'
    if not out.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(ROOT / 'series' / T.SLUG / 'episodes' / ep / 'final.mp4'), '-vn',
                        '-ar', '44100', '-ac', '2', str(out)], check=True)
a = sys.argv[1:3] if len(sys.argv) > 2 else (str(ROOT / 'build' / f'{T.SLUG}-movie' / 'noaudio.mp4'), str(HERE / 'final_h264.mp4'))
mix.run(T.SLUG, 'movie', T, *a)
