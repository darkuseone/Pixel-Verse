"""ElevenLabs Voice Design: describe a character -> 3 previews -> pick by metrics -> save as a voice.
  python3 engine/voicedesign.py design <slug> <char>        # uses voices.json characters[char].design {description, text}
  python3 engine/voicedesign.py save <slug> <char> <n>      # keep preview n (0..2) -> voice_id into voices.json
Cost: the preview text length, charged once for all three previews. Key: ELEVENLABS_API_KEY (never printed).
Metrics printed per preview: duration, median pitch (Hz), pitch spread, speech rate (chars/s), loudness spread."""
import base64, json, os, subprocess, sys, urllib.request
import numpy as np
import paths as P

API = 'https://api.elevenlabs.io/v1'


class LimitError(Exception):
    pass


def _post(url, body, soft=False):
    req = urllib.request.Request(url, json.dumps(body).encode(), {
        'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read()), r.headers
    except urllib.error.HTTPError as e:
        msg = e.read()[:600]
        if soft and b'voice_limit' in msg: raise LimitError(msg)
        sys.exit(f'HTTP {e.code}: {msg!r}')


def pcm(path, sr=16000):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768, sr


def pitch_track(a, sr, fmin=60, fmax=420, hop=0.01, win=0.04):
    """plain autocorrelation F0 per frame (voiced frames only)"""
    n, h = int(win * sr), int(hop * sr)
    lo, hi = int(sr / fmax), int(sr / fmin)
    f0, rms = [], []
    for i in range(0, len(a) - n, h):
        x = a[i:i + n] - a[i:i + n].mean()
        e = float(np.sqrt((x * x).mean())); rms.append(e)
        if e < 0.02: continue
        c = np.correlate(x, x, 'full')[n - 1:]
        c = c / (c[0] + 1e-9)
        k = lo + int(np.argmax(c[lo:hi]))
        if c[k] > 0.45: f0.append(sr / k)
    return np.array(f0), np.array(rms)


def metrics(path, text):
    a, sr = pcm(path)
    f0, rms = pitch_track(a, sr)
    dur = len(a) / sr
    voiced = rms > 0.02
    talk = voiced.sum() * 0.01
    return dict(dur=round(dur, 2), f0=round(float(np.median(f0)), 1) if len(f0) else 0,
                f0_iqr=round(float(np.percentile(f0, 75) - np.percentile(f0, 25)), 1) if len(f0) else 0,
                rate=round(len(text) / max(talk, 0.1), 1), loud_sd=round(float(np.std(20 * np.log10(rms[voiced] + 1e-6))), 1))


def design(slug, char):
    vj = P.series(slug) / 'voices.json'
    V = json.load(open(vj))
    d = V['characters'][char]['design']
    body = {'voice_description': d['description'], 'text': d['text'], 'model_id': d.get('model', 'eleven_ttv_v3'),
            'guidance_scale': d.get('guidance', 5), 'loudness': d.get('loudness', 0.5)}
    if 'seed' in d: body['seed'] = d['seed']
    r, hdr = _post(f'{API}/text-to-voice/design', body)
    out = []
    for i, pv in enumerate(r['previews']):
        p = P.build('voices', slug, f'{char}_{i}.mp3')
        open(p, 'wb').write(base64.b64decode(pv['audio_base_64']))
        m = metrics(p, d['text'])
        out.append(dict(i=i, generated_voice_id=pv['generated_voice_id'], path=p, **m))
        print(char, i, m, p)
    json.dump(out, open(P.build('voices', slug, f'{char}_previews.json'), 'w'), indent=1)
    print('cost header:', hdr.get('character-cost'))


def save(slug, char, n):
    vj = P.series(slug) / 'voices.json'
    V = json.load(open(vj))
    c = V['characters'][char]
    prev = json.load(open(P.build('voices', slug, f'{char}_previews.json')))
    body = {'voice_name': f"{V['cartoon']} — {c['name']}", 'voice_description': c['design']['description'][:1000],
            'generated_voice_id': prev[n]['generated_voice_id'],
            'played_not_selected_voice_ids': [p['generated_voice_id'] for p in prev if p['i'] != n]}
    try:
        r, _ = _post(f'{API}/text-to-voice', body, soft=True)
    except LimitError:                                                    # account full: free one slot by the registry rules, retry
        import voices
        if not voices.free(1, keep=(slug,), go=True, reason=f'auto: room for {slug}/{char}'):
            sys.exit('voice limit reached and nothing may be deleted automatically')
        r, _ = _post(f'{API}/text-to-voice', body)
    c.pop('temp_premade', None)
    c['voice_id'] = r['voice_id']; c['voice'] = body['voice_name']
    c['design']['picked'] = {k: prev[n][k] for k in ('i', 'dur', 'f0', 'f0_iqr', 'rate', 'loud_sd')}
    json.dump(V, open(vj, 'w'), ensure_ascii=False, indent=2)
    print(char, '->', r['voice_id'])
    import voices
    voices.sync(quiet=True)                                               # the registry docs/voices.* always knows who has which voice


if __name__ == '__main__':
    if sys.argv[1] == 'design': design(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'save': save(sys.argv[2], sys.argv[3], int(sys.argv[4]))
