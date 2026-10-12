"""Audio for «ПРОПУСКНОЙ РЕЖИМ»: lines + point SFX + ambience / music beds per scene
  python3 mix.py [<noaudio.mp4> <final.mp4>]   (default: build/valera-i-kot-movie/noaudio.mp4 -> final.mp4 here)"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'engine'))
import mix
import timeline as T

a = sys.argv[1:3] if len(sys.argv) > 2 else (str(HERE.parents[2] / 'build' / f'{T.SLUG}-movie' / 'noaudio.mp4'), str(HERE / 'final_h264.mp4'))
mix.run(T.SLUG, 'movie', T, *a)
