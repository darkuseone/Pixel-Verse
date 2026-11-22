"""Audio mix for S01E01 v2 variant B (same timeline as ep01) -> build/klyuchevoy-ep01b/ (+ mux).  python3 mix.py [noaudio.mp4 final.mp4]"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'ep01'))
import mix
import timeline as T

mix.run(T.SLUG, 'ep01b', T, *(sys.argv[1:3] if len(sys.argv) > 2 else (None, None)))
