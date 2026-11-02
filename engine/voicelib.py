"""Ready-made voices from the ElevenLabs Voice Library (rule 02.11.2026: library first, Voice Design only if nothing fits).
Voices saved from the Voice Library do NOT take custom voice slots (help center, «How many voice slots…»); searching is free.

  python3 engine/voicelib.py search [--lang ru] [--gender male|female] [--age young|middle_aged|old] [--accent X] [--q "words"] [--n 12]
        -> list with voice_id, owner id, notice period (days the owner must warn before removing it: prefer >= 365)
  python3 engine/voicelib.py previews <voice_id> [...]        # download the previews to build/voices/lib/ + pitch/tempo metrics
  python3 engine/voicelib.py add <slug> <char> <public_owner_id> <voice_id>
        -> saves the voice to the account (no slot) and writes voice_id + library info into series/<slug>/voices.json

A library voice can disappear if its owner removes it (after the notice period): the registry (engine/voices.py) keeps the recorded
lines, so `voices.py restore` can re-create it by cloning. Key: ELEVENLABS_API_KEY (never printed)."""
import json, os, sys, urllib.request, urllib.parse
import paths as P

API = 'https://api.elevenlabs.io/v1'


def _req(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data, method=method, headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'],
                                                                  'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(r, timeout=120) as resp: return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code}: {e.read()[:400]!r}')


def search(lang='ru', gender=None, age=None, accent=None, q=None, n=12):
    p = dict(page_size=max(n * 3, 30), language=lang)
    for k, v in (('gender', gender), ('age', age), ('accent', accent), ('search', q)):
        if v: p[k] = v
    d = _req('GET', f'{API}/shared-voices?' + urllib.parse.urlencode(p))
    vs = [v for v in d.get('voices', []) if not lang or v.get('language') == lang][:n]
    for v in vs:
        print(f"{v['voice_id']}  owner={v['public_owner_id'][:12]}…  {v.get('gender')}/{v.get('age')}/{v.get('accent')}  "
              f"notice={v.get('notice_period')}d  {v['name']}\n    {(v.get('description') or '')[:200].replace(chr(10), ' ')}")
    json.dump(vs, open(P.build('voices', 'lib', 'last_search.json'), 'w'), ensure_ascii=False, indent=1)
    return vs


def previews(ids):
    from voicedesign import metrics
    last = {v['voice_id']: v for v in json.load(open(P.build('voices', 'lib', 'last_search.json')))}
    for vid in ids:
        v = last.get(vid)
        if not v or not v.get('preview_url'): print('no preview for', vid); continue
        f = P.build('voices', 'lib', f'{vid}.mp3')
        with urllib.request.urlopen(v['preview_url'], timeout=120) as r: open(f, 'wb').write(r.read())
        print(vid, v['name'], metrics(f, ''), f)


def add(slug, char, owner, vid):
    vj = P.series(slug) / 'voices.json'
    V = json.load(open(vj))
    c = V['characters'].setdefault(char, {'name': char})
    name = f"{V.get('cartoon', slug)} — {c.get('name', char)}"
    r = _req('POST', f'{API}/voices/add/{owner}/{vid}', {'new_name': name[:100]})
    c['voice_id'] = r.get('voice_id', vid)
    c['voice'] = name
    c['library'] = {'public_owner_id': owner, 'voice_id': vid}
    json.dump(V, open(vj, 'w'), ensure_ascii=False, indent=2)
    print(char, '->', c['voice_id'], '(Voice Library, no slot)')
    import voices
    voices.sync(quiet=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == 'search':
        kw = {}
        for i in range(1, len(a) - 1, 2):
            kw[a[i].lstrip('-')] = int(a[i + 1]) if a[i] == '--n' else a[i + 1]
        search(**kw)
    elif a[0] == 'previews': previews(a[1:])
    elif a[0] == 'add': add(*a[1:5])
