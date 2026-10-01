"""ElevenLabs speech-to-text check (scribe_v1): transcript + audio events, to verify Russian lines / voice previews.
  python3 engine/stt.py file1.mp3 [file2.mp3 ...]
Language: env STT_LANG (default ru), e.g. STT_LANG=en.
  python3 engine/stt.py --chars file.mp3 WORD   -> character timings inside WORD (stress check: the stressed vowel is longest)
Key: ELEVENLABS_API_KEY (never printed)."""
import json, os, sys, urllib.request, uuid

API = 'https://api.elevenlabs.io/v1/speech-to-text'


def transcribe(path, lang=None, gran='word'):
    lang = lang or os.environ.get('STT_LANG', 'ru')
    b = uuid.uuid4().hex
    parts = []
    for k, v in (('model_id', 'scribe_v1'), ('language_code', lang), ('tag_audio_events', 'true'), ('timestamps_granularity', gran)):
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{os.path.basename(path)}"\r\n'
                 f'Content-Type: audio/mpeg\r\n\r\n'.encode() + open(path, 'rb').read() + b'\r\n')
    parts.append(f'--{b}--\r\n'.encode())
    req = urllib.request.Request(API, b''.join(parts), {'xi-api-key': os.environ['ELEVENLABS_API_KEY'],
                                                        'Content-Type': f'multipart/form-data; boundary={b}'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code}: {e.read()[:400]!r}')


def vowels(path, word):
    """durations of the vowels of `word` (case-insensitive) from character timestamps"""
    d = transcribe(path, gran='character')
    for w in d.get('words', []):
        if w.get('type') == 'word' and w['text'].lower().strip('.,!?…—') == word.lower():
            out = []
            for c in w.get('characters', []):
                if c['text'].lower() in 'аеёиоуыэюя': out.append((c['text'], round(c['end'] - c['start'], 3)))
            return out
    return None


if __name__ == '__main__':
    if sys.argv[1] == '--chars':
        print(sys.argv[2], sys.argv[3], vowels(sys.argv[2], sys.argv[3])); sys.exit()
    for p in sys.argv[1:]:
        d = transcribe(p)
        ev = [w['text'] for w in d.get('words', []) if w.get('type') == 'audio_event']
        print(os.path.basename(p), '|', d.get('language_code'), round(d.get('language_probability', 0), 2), '|', d.get('text'), '| events:', ev)
