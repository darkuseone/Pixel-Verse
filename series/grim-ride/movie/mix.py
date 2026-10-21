"""Audio for «Grim Ride: ONE MORE HOUR»: lines + point SFX + ambience / music beds per scene
  python3 mix.py [<noaudio.mp4> <final.mp4>]   (default: build/grim-ride-movie/noaudio.mp4 -> final_h264.mp4 here)"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine'))
import mix
import timeline as T

a = sys.argv[1:3] if len(sys.argv) > 2 else (str(ROOT / 'build' / f'{T.SLUG}-movie' / 'noaudio.mp4'), str(HERE / 'final_h264.mp4'))
mix.run(T.SLUG, 'movie', T, *a)
