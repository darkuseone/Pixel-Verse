"""Stem balance check of an episode mix (owner 09.11.2026: «музыка и звуки громкие, голоса тихие»): renders voice-only, SFX-only and
music-only versions of the mix from the episode's timeline (no loudnorm) and measures their integrated loudness.
  python3 engine/mixcheck.py series/<slug>/episodes/epNN
Targets: voice ≈ -16 LUFS (T.VNORM = -16 levels every line); SFX 9–12 dB below the voice; music 16–18 dB below the voice.
Also lists single voice lines more than 4 dB quieter than the median when VNORM is not set."""
import sys, os, re, types, shutil, subprocess, importlib, importlib.util, statistics, pathlib

ENG = pathlib.Path(__file__).resolve().parent


def lufs(f):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', str(f), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    v = re.findall(r'I:\s+(-?[\d.]+) LUFS', r)
    return float(v[-1]) if v else None


def main(ep):
    ep = pathlib.Path(ep).resolve()
    os.chdir(ep); sys.path.insert(0, str(ENG)); sys.path.insert(0, str(ep))
    sp = importlib.util.spec_from_file_location('emix', ENG / 'mix.py'); mix = importlib.util.module_from_spec(sp); sp.loader.exec_module(mix)
    T = importlib.import_module('timeline')
    speakers = {v[6] for v in T.VOICE}
    res = {}
    for name, voice, sfx, beds in (('voice', True, False, False), ('sfx', False, True, False), ('music', False, False, True)):
        S = types.SimpleNamespace(**{k: getattr(T, k) for k in dir(T) if not k.startswith('__')})
        S.LUFS = None
        if not voice: S.VNORM = None; S.VGAIN = {k: 0.0001 for k in speakers}
        if not sfx: S.SFX = []
        if not beds: S.BEDS = []
        out = mix.run(T.SLUG, T.EP, S)
        dst = pathlib.Path(out).with_name(f'stem_{name}.wav'); shutil.copy(out, dst)
        res[name] = lufs(dst)
    v, s, m = res['voice'], res['sfx'], res['music']
    print(f'voice {v:.1f} LUFS | sfx {s:.1f} ({v - s:+.1f} dB under voice) | music {m:.1f} ({v - m:+.1f} dB under voice)')
    bad = []
    if v - s < 8: bad.append(f'SFX too loud: only {v - s:.1f} dB under the voice (want 9–12)')
    if v - m < 15: bad.append(f'music too loud: only {v - m:.1f} dB under the voice (want 16–18)')
    if getattr(T, 'VNORM', None) is None:
        lines = {k: lufs(T.ROOT / 'series' / T.SLUG / 'voice' / vep / f'{key}.mp3') for k, vep, key, *_ in T.VOICE}
        med = statistics.median(x for x in lines.values() if x is not None)
        for k, x in lines.items():
            if x is not None and x < med - 4: bad.append(f'line {k} is {med - x:.1f} dB quieter than the median: set VNORM = -16 in timeline.py')
    print('\n'.join(bad) if bad else 'OK')


if __name__ == '__main__':
    main(sys.argv[1])
