"""Generic episode audio mix (any series) from a timeline module -> build/<ep>/mix.wav (+ mux with video).
Timeline module provides DUR, VOICE, SFX, BEDS and optionally VFX (speaker -> extra ffmpeg filter, e.g. phone band)
and VGAIN (speaker -> gain). Beds are looped with acrossfade, faded and ducked under speech.
Optional T.LUFS (e.g. -14, owner's test rule 25.10.2026): two-pass loudnorm of the final mix to LUFS / -1 dBTP instead of the
plain MASTER gain (older timelines without LUFS keep their exact old sound).
Optional, all off by default (sound-design pass with earshot, 30.10.2026): T.VOICE_LUFS (every voice clip measured and brought
to this loudness, VGAIN is then a relative trim), SFX entries (path, t, gain, a, b, pan[, filter]) with pan -1..1,
BEDS entries (path, loop, t0, t1, gain, duck, filter): duck True (x0.4 under speech) or a factor, an extra ffmpeg filter (timeline time t, e.g. a stop-down before
a hit or a Haas width), T.MASTER_EQ (filter on the summed mix before the limiter).
Usage from an episode folder:  python3 mix.py [noaudio.mp4 final.mp4]   (mix.py there calls run(...))"""
import json
import os
import subprocess
import paths as P

PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.3'


def run(slug, ep, T, video=None, out_mp4=None):
    DUR, VOICE, SFX, BEDS = T.DUR, T.VOICE, T.SFX, T.BEDS
    VFX = getattr(T, 'VFX', {}); VGAIN = getattr(T, 'VGAIN', {})
    inputs, chains, labels = [], [], []

    def add_input(path):
        inputs.extend(['-i', str(path)]); return len(inputs) // 2 - 1

    vl = getattr(T, 'VOICE_LUFS', None)
    for vid, vep, key, t0, a, b, who, txt in VOICE:
        src = P.series(slug) / 'voice' / vep / f'{key}.mp3'
        i = add_input(src); d = int(t0 * 1000)
        extra = (',' + VFX[who]) if who in VFX else ''
        g = VGAIN.get(who, 1.45)
        if vl is not None: g = VGAIN.get(who, 1.0) * 10 ** ((vl - clip_lufs(src)) / 20)
        chains.append(f'[{i}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, b - a - 0.03):.3f}:d=0.03,'
                      f'aresample=44100,aformat=channel_layouts=stereo{extra},volume={g:.3f},adelay={d}|{d}[v_{vid}]')
        labels.append(f'[v_{vid}]')
    for k, s in enumerate(SFX):
        path, t0, g = s[:3]; a, b = (s[3], s[4]) if len(s) > 4 else (None, None)
        pan = s[5] if len(s) > 5 else 0.0
        sf = (',' + s[6]) if len(s) > 6 and s[6] else ''
        i = add_input(P.ROOT / path); d = int(t0 * 1000)
        trim = f'atrim={a}:{b},asetpts=PTS-STARTPTS,' if a is not None else ''
        pn = ''
        if pan:                                                             # constant-power pan of a (mono-summed) effect
            import math
            th = (max(-1.0, min(1.0, pan)) + 1) * math.pi / 4
            pn = f',pan=stereo|c0={math.cos(th) * 1.41:.3f}*c0|c1={math.sin(th) * 1.41:.3f}*c1'
        chains.append(f'[{i}:a]{trim}aresample=44100,aformat=channel_layouts=stereo{sf}{pn},volume={g},adelay={d}|{d}[s{k}]')
        labels.append(f'[s{k}]')

    speech = '+'.join(f'between(t,{t0 - 0.05:.2f},{t0 + (b - a) + 0.1:.2f})' for _, _, _, t0, a, b, _, _ in VOICE)
    for k, bed in enumerate(BEDS):
        path, loop, t0, t1, g, duck = bed[:6]
        bf = (',' + bed[6]) if len(bed) > 6 and bed[6] else ''
        i = add_input(P.ROOT / path)
        dur = t1 - t0; n = int(dur / (loop - 0.5)) + 1
        if n > 1 and not getattr(T, 'LOOP_LEGACY', False):
            # 30.10.2026: asplit + acrossfade of one stream stopped after the FIRST pass (a bed longer than its loop went silent:
            # found by earshot, «no music after 0:15»). The loops are seamless (ElevenLabs loop=True, code-synth wraps its tail),
            # so aloop repeats them sample-exactly. LOOP_LEGACY = True in a timeline reproduces the old (buggy) beds.
            chains.append(f'[{i}:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,'
                          f'aloop=loop=-1:size={int(loop * 44100)},asetpts=N/SR/TB[b{k}_0]')
            n = 1
        elif n > 1:
            chains.append(f'[{i}:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,asplit={n}' +
                          ''.join(f'[b{k}_{j}]' for j in range(n)))
        else:
            chains.append(f'[{i}:a]atrim=0:{loop},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo[b{k}_0]')
        cur = f'[b{k}_0]'
        for j in range(1, n):
            chains.append(f'{cur}[b{k}_{j}]acrossfade=d=0.5:c1=tri:c2=tri[bx{k}_{j}]'); cur = f'[bx{k}_{j}]'
        d = int(t0 * 1000)
        dk = duck if (isinstance(duck, (int, float)) and not isinstance(duck, bool)) else 0.4      # duck = True (0.4) or a factor
        vol = f"volume='if(gt({speech},0),{g * dk:.3f},{g:.3f})':eval=frame" if duck else f'volume={g}'
        chains.append(f'{cur}atrim=0:{dur},afade=t=in:d=0.02,afade=t=out:st={max(0.0, dur - 0.3):.2f}:d=0.3,adelay={d}|{d},{vol}{bf}[bed{k}]')
        labels.append(f'[bed{k}]')

    master = getattr(T, 'MASTER', 1.0)
    chains.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR},'
                  f'volume={master}' + ((',' + T.MASTER_EQ) if getattr(T, 'MASTER_EQ', None) else '') + ',alimiter=limit=0.95:level=false[out]')
    out = P.build(ep if slug == P.PDZ else f'{slug}-{ep}', 'mix.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(chains), '-map', '[out]', '-ar', '44100', out],
                   check=True)
    lufs = getattr(T, 'LUFS', None)
    if lufs is not None: loudnorm(out, lufs)
    print(out)
    if video:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', out, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out_mp4], check=True)
        print(out_mp4)
    return out


_LU = {}


def clip_lufs(path):
    """integrated loudness of one clip (BS.1770 via ffmpeg ebur128), cached per path"""
    p = str(path)
    if p not in _LU:
        r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True)
        val = -20.0
        for ln in r.stderr.splitlines()[::-1]:
            if ln.strip().startswith('I:'):
                try: val = float(ln.split()[1])
                except (IndexError, ValueError): pass
                break
        _LU[p] = max(-40.0, val)
    return _LU[p]


def loudnorm(wav, target=-14.0, tp=-1.0, lra=11.0):
    """two-pass EBU R128 normalisation in place: measure, then apply in linear mode (keeps the mix dynamics when possible)"""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(wav), '-af', f'loudnorm=I={target}:TP={tp}:LRA={lra}:print_format=json',
                        '-f', 'null', '-'], capture_output=True, text=True, check=True)
    m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
    tmp = str(wav) + '.ln.wav'
    af = (f"loudnorm=I={target}:TP={tp}:LRA={lra}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=44100")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-af', af, '-ar', '44100', tmp], check=True)
    os.replace(tmp, wav)
    print(f"loudnorm: {float(m['input_i']):.1f} LUFS -> {target} LUFS, TP <= {tp} dBTP")
