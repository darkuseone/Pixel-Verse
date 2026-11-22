"""S01E01 v2, VARIANT B: the same episode with the office drawn entirely in code (engine/props/ksoffice.py) — owner test 22.11.2026.
  python3 ep01b.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import os, sys, pathlib
os.environ['KS_VAR'] = 'B'
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'ep01'))
import ep01 as E
from timeline import CUTS, NAMES

if __name__ == '__main__':
    E.EPI.main(E.render, __file__)
