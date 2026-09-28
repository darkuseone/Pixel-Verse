"""ElevenLabs TTS/SFX. Usage:
  python3 engine/tts.py lines <slug> <ep> [keys...]     # voice/<ep>/lines.json -> voice/<ep>/<key>.mp3 (skips existing)
  python3 engine/tts.py sfx <out.mp3> <seconds> "<prompt>"
Key: ELEVENLABS_API_KEY (never printed)."""
import json, os, sys, urllib.request
import paths as P

API = 'https://api.elevenlabs.io/v1'


def _post(url, body, out):
    req = urllib.request.Request(url, json.dumps(body).encode(), {
        'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = r.read(); cost = r.headers.get('character-cost') or r.headers.get('x-character-count')
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code}: {e.read()[:400]!r}')
    open(out, 'wb').write(data)
    print(out, len(data), 'bytes', 'cost', cost)


def lines(slug, ep, keys):
    base = P.series(slug)
    voices = json.load(open(base / 'voices.json'))
    L = json.load(open(base / 'voice' / ep / 'lines.json'))
    model = voices.get('tts_model', 'eleven_v3')
    for k, (who, text) in L.items():
        out = base / 'voice' / ep / f'{k}.mp3'
        if (keys and k not in keys) or (not keys and out.exists()):
            continue
        vid = voices['characters'][who]['voice_id']
        _post(f'{API}/text-to-speech/{vid}?output_format=mp3_44100_128', {'text': text, 'model_id': model}, out)


if __name__ == '__main__':
    if sys.argv[1] == 'lines':
        lines(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif sys.argv[1] == 'sfx':
        _post(f'{API}/sound-generation', {'text': sys.argv[4], 'duration_seconds': float(sys.argv[3])}, sys.argv[2])
