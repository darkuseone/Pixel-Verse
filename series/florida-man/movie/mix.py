"""Audio for the extended cut: court lines + point SFX + the six exhibits' own audio + court room tone / theme -> build/florida-man-movie/mix.wav
  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import mix
import timeline as T

mix.run(T.SLUG, 'movie', T, *(sys.argv[1:3] if len(sys.argv) > 2 else (None, None)))
