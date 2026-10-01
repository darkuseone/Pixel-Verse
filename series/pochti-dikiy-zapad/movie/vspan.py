"""Voiced spans of clips (100 Hz envelope): python3 vspan.py ep01 c1 n1 ... | python3 vspan.py movie all"""
import os, sys, pathlib
os.environ['PV_WIDE'] = '1'
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'engine'))
import numpy as np
import paths as P
import stage  # noqa  (sets scene globals)
import scene as S


def spans(ep, key, thr=0.10, gap=0.35):
    e = S.load_env(P.voice_wav(ep, key))
    on = e > thr * (e.max() + 1e-9)
    idx = np.nonzero(on)[0]
    if len(idx) == 0: return []
    out = []; s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if (i - p) / 100.0 > gap: out.append((s / 100.0, (p + 1) / 100.0)); s = i
        p = i
    out.append((s / 100.0, (p + 1) / 100.0))
    return out


if __name__ == '__main__':
    ep = sys.argv[1]
    keys = sys.argv[2:]
    if keys == ['all']:
        import json
        keys = list(json.load(open(P.series() / 'voice' / ep / 'lines.json')).keys())
    for k in keys:
        try:
            sp = spans(ep, k)
        except Exception as ex:
            print(ep, k, 'ERR', ex); continue
        print(f'{ep}/{k}: ' + '  '.join(f'[{a:.2f}-{b:.2f}]' for a, b in sp))
