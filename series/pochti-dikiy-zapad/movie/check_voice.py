"""STT check of generated movie lines (scribe_v1) + durations. Run from repo root:
  python3 series/pochti-dikiy-zapad/movie/check_voice.py [keys...]"""
import json, os, re, subprocess, sys, urllib.request, uuid, pathlib

D = pathlib.Path(__file__).resolve().parents[1] / 'voice' / 'movie'
L = json.load(open(D / 'lines.json'))
key = os.environ['ELEVENLABS_API_KEY']


def stt(path):
    b = uuid.uuid4().hex
    data = open(path, 'rb').read()
    body = (f'--{b}\r\nContent-Disposition: form-data; name="model_id"\r\n\r\nscribe_v1\r\n'
            f'--{b}\r\nContent-Disposition: form-data; name="language_code"\r\n\r\nrus\r\n'
            f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n').encode() \
        + data + f'\r\n--{b}--\r\n'.encode()
    r = urllib.request.Request('https://api.elevenlabs.io/v1/speech-to-text', body,
                               {'xi-api-key': key, 'Content-Type': f'multipart/form-data; boundary={b}'})
    for attempt in range(4):
        try:
            return json.loads(urllib.request.urlopen(r, timeout=60).read())['text']
        except Exception as ex:
            print('  retry', attempt, type(ex).__name__)
    return '??'


res = {}
for k, (who, txt) in L.items():
    if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
    p = D / f'{k}.mp3'
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)]))
    clean = re.sub(r'\[[^\]]*\]', '', txt).replace('́', '').strip()
    got = stt(p)
    res[k] = {'dur': round(d, 2), 'want': clean, 'got': got}
    print(f'{k:3} {d:5.2f}s | {clean}\n        -> {got}')
old = json.load(open(D / 'check.json')) if (D / 'check.json').exists() else {}
old.update(res)
json.dump(old, open(D / 'check.json', 'w'), ensure_ascii=False, indent=1)
