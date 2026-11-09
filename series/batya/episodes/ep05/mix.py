"""Audio mix for E05 -> build/batya-ep05/mix.wav (+ mux).  python3 mix.py [noaudio.mp4 final.mp4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import mix
import timeline as T

mix.run(T.SLUG, T.EP, T, *(sys.argv[1:3] if len(sys.argv) > 2 else (None, None)))
