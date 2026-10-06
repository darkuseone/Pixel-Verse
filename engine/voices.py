"""Voice registry of all series: which ElevenLabs voice each character has (or had), so later seasons reuse the same voices.
Files (in git): docs/voices.json (machine) + docs/voices.md (human table, regenerated on every write).

  python3 engine/voices.py sync                     # scan series/*/voices.json + the account -> registry (status, lines, samples)
  python3 engine/voices.py show [slug]              # print the registry (all series or one)
  python3 engine/voices.py free N [--keep slug] [--go]   # free N custom-voice slots: delete the least-needed series voices
                                                    #   (dry run without --go; the owner's own voices are never touched)
  python3 engine/voices.py delete <slug> <char> [--go]   # delete one series voice (recorded as deleted, samples kept)
  python3 engine/voices.py restore <slug> <char>    # re-create a deleted voice by Instant Voice Cloning from its recorded lines

Rules (owner, 06.10.2026):
  * PROTECTED: the owner's personal voices (NIKITA, NIKITA2, Cartman — ids in PROTECTED) and any account voice that no series
    uses are never deleted automatically.
  * Auto-free picks only voices of series characters, never of the series being worked on (--keep), fewest lines first,
    then fewest episodes, then the oldest. Before deleting, the voice's description, settings and preview link go to the
    registry, plus the list of its recorded line files in the repo (the material to re-clone it for a season 2).
  * engine/voicedesign.py save calls free(1) by itself when the account answers «voice_limit_reached», then syncs.
Key: ELEVENLABS_API_KEY (never printed)."""
import json, os, sys, glob, time, urllib.request, uuid, mimetypes
from collections import Counter, defaultdict
from pathlib import Path
import paths as P

API = 'https://api.elevenlabs.io'
REG = P.ROOT / 'docs' / 'voices.json'
MD = P.ROOT / 'docs' / 'voices.md'
PROTECTED = {'14NozJq5eoBmDc1FXFDq': 'NIKITA2', '7fU3YUxRrVGjNaZ5dzEH': 'NIKITA', 'Em7IfQCID6d4WZTp4VkN': 'Cartman'}


# ---------------------------------------------------------------- API
def _req(method, url, body=None, headers=None, raw=None):
    h = {'xi-api-key': os.environ['ELEVENLABS_API_KEY']}
    data = None
    if body is not None:
        data = json.dumps(body).encode(); h['Content-Type'] = 'application/json'
    if raw is not None:
        data, ct = raw; h['Content-Type'] = ct
    h.update(headers or {})
    req = urllib.request.Request(url, data, h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            t = r.read()
            return json.loads(t) if t else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'HTTP {e.code}: {e.read()[:500]!r}')


def account_voices():
    out, token = [], None
    while True:
        url = f'{API}/v2/voices?page_size=100&voice_type=personal' + (f'&next_page_token={token}' if token else '')
        d = _req('GET', url)
        out += d.get('voices', [])
        token = d.get('next_page_token')
        if not d.get('has_more') or not token: break
    return {v['voice_id']: v for v in out}


def slots():
    d = _req('GET', f'{API}/v1/user/subscription')
    return d.get('voice_slots_used'), d.get('voice_limit')


# ---------------------------------------------------------------- registry
def load():
    if REG.exists(): return json.load(open(REG))
    return {'protected': PROTECTED, 'voices': []}


def _key(e): return (e['slug'], e['char'])


def _usage(slug):
    """lines / episodes / sample files per character from series/<slug>/voice/<ep>/lines.json (tightened copies skipped)"""
    cnt, eps, files = Counter(), defaultdict(set), defaultdict(list)
    for lj in sorted(glob.glob(str(P.series(slug) / 'voice' / '**' / 'lines.json'), recursive=True)):
        ep_dir = Path(lj).parent
        if ep_dir.name.endswith('_t'): continue
        try: L = json.load(open(lj))
        except Exception: continue
        for k, val in L.items():
            who = val[0] if isinstance(val, list) else (val.get('who') if isinstance(val, dict) else None)
            if not who: continue
            cnt[who] += 1; eps[who].add(str(ep_dir.relative_to(P.series(slug) / 'voice')))
            f = ep_dir / f'{k}.mp3'
            if f.exists(): files[who].append(str(f.relative_to(P.ROOT)))
    return cnt, eps, files


def save_reg(R):
    R['voices'].sort(key=lambda e: (e['slug'], e['status'] != 'active', -e.get('lines', 0)))
    R['updated'] = time.strftime('%Y-%m-%d %H:%M')
    json.dump(R, open(REG, 'w'), ensure_ascii=False, indent=1)
    lines = ['# Голоса сериалов (реестр ElevenLabs)', '',
             'Генерируется `engine/voices.py` (не править руками). Читать перед каждым новым сериалом и сезоном: кто чем озвучен, что удалено и как вернуть.',
             'Голос героя не меняется никогда: для сезона 2 берём `voice_id` отсюда; если статус `deleted` — `python3 engine/voices.py restore <slug> <char>`',
             '(клон из записанных реплик, занимает слот). Личные голоса владельца (NIKITA, NIKITA2, Cartman) не трогаем никогда.', '',
             f'Обновлено: {R["updated"]}.', '']
    for slug in sorted({e['slug'] for e in R['voices']}):
        lines += [f'## {slug}', '', '| Герой | char | voice_id | Статус | Реплик / серий | Голос |', '|---|---|---|---|---|---|']
        for e in [x for x in R['voices'] if x['slug'] == slug]:
            st = e['status'] + (f' {e.get("deleted_on", "")}' if e['status'] == 'deleted' else '')
            lines.append(f'| {e.get("name", "")} | `{e["char"]}` | `{e["voice_id"]}` | {st} | {e.get("lines", 0)} / {e.get("episodes", 0)} | '
                         f'{(e.get("voice_name") or "").replace("|", "/")} |')
        lines.append('')
    lines += ['## Защищённые (личные голоса владельца)', ''] + [f'- `{k}` — {v}' for k, v in R.get('protected', PROTECTED).items()]
    MD.write_text('\n'.join(lines) + '\n')


def sync(quiet=False, acc=None):
    R = load()
    acc = account_voices() if acc is None else acc
    idx = {_key(e): e for e in R['voices']}
    for vj in sorted(glob.glob(str(P.ROOT / 'series' / '*' / 'voices.json'))):
        slug = Path(vj).parent.name
        V = json.load(open(vj))
        cnt, eps, files = _usage(slug)
        for c, ch in V.get('characters', {}).items():
            vid = ch.get('voice_id')
            if not vid: continue
            e = idx.get((slug, c))
            if e is None or (e['voice_id'] != vid and e['status'] != 'deleted'):
                if e is not None and e['voice_id'] != vid:                       # voice changed: keep the old one in history
                    e.setdefault('history', []).append({'voice_id': e['voice_id'], 'until': time.strftime('%Y-%m-%d')})
                e = e or {'slug': slug, 'char': c}
                idx[(slug, c)] = e
            if e.get('status') == 'deleted' and e['voice_id'] == vid:
                pass                                                              # stays deleted until restore
            else:
                e['voice_id'] = vid
                kind = 'active' if vid in acc else ('premade' if ch.get('temp_premade') else 'library_or_premade')
                e['status'] = kind
            e['name'] = ch.get('name', c)
            e['voice_name'] = (acc.get(vid) or {}).get('name') or ch.get('voice') or e.get('voice_name')
            e['lines'], e['episodes'] = cnt[c], len(eps[c])
            e['samples'] = sorted(files[c], key=lambda f: -os.path.getsize(P.ROOT / f))[:8]
            if ch.get('design'):
                e['design'] = {k: v for k, v in ch['design'].items() if k in ('description', 'text', 'picked')}
            if vid in acc:
                a = acc[vid]
                e['account'] = {'category': a.get('category'), 'description': a.get('description'), 'settings': a.get('settings'),
                                'created_at_unix': a.get('created_at_unix')}
    R['voices'] = list(idx.values())
    R['protected'] = PROTECTED
    others = {vid: v['name'] for vid, v in acc.items() if vid not in {e['voice_id'] for e in R['voices']}}
    R['unlisted_account_voices'] = others
    save_reg(R)
    if not quiet:
        u, l = slots()
        print(f'registry: {len(R["voices"])} voices, slots {u}/{l}; not in any series: {others}')
    return R


def candidates(R, keep=(), acc=None):
    """series voices that may be deleted: live in the account, generated by us, not protected, not of the kept series"""
    acc = account_voices() if acc is None else acc
    out = []
    for e in R['voices']:
        vid = e['voice_id']
        if e['status'] != 'active' or vid in PROTECTED or e['slug'] in keep or vid not in acc: continue
        if acc[vid].get('category') != 'generated': continue
        out.append(e)
    out.sort(key=lambda e: (e.get('lines', 0), e.get('episodes', 0), (e.get('account') or {}).get('created_at_unix') or 0))
    return out


def _delete(e, R, reason):
    a = _req('GET', f'{API}/v1/voices/{e["voice_id"]}')
    e['account'] = {'category': a.get('category'), 'description': a.get('description'), 'settings': a.get('settings'),
                    'labels': a.get('labels'), 'created_at_unix': a.get('created_at_unix')}
    e['preview_url'] = a.get('preview_url')
    if a.get('preview_url'):                                                    # keep the voice preview in git as one more sample
        dst = P.ROOT / 'library' / 'voice_archive' / e['slug'] / f'{e["char"]}_preview.mp3'
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            with urllib.request.urlopen(a['preview_url'], timeout=120) as r: dst.write_bytes(r.read())
            rel = str(dst.relative_to(P.ROOT))
            if rel not in e.get('samples', []): e.setdefault('samples', []).insert(0, rel)
        except Exception as err:
            print('preview not saved:', err)
    _req('DELETE', f'{API}/v1/voices/{e["voice_id"]}')
    e['status'] = 'deleted'; e['deleted_on'] = time.strftime('%Y-%m-%d'); e['deleted_reason'] = reason
    print('deleted', e['slug'], e['char'], e['voice_id'], f'({e.get("lines", 0)} lines)')


def free(n, keep=(), go=False, reason='free slots'):
    acc = account_voices()
    R = sync(quiet=True, acc=acc)
    pick = candidates(R, keep, acc)[:n]
    for e in pick:
        if not e.get('samples'):
            print('skip (no recorded samples to restore it later):', e['slug'], e['char']); continue
        if go: _delete(e, R, reason)
        else: print('would delete', e['slug'], e['char'], e['voice_id'], e.get('lines'), 'lines')
    save_reg(R)
    return [e for e in pick if e['status'] == 'deleted']


def delete(slug, char, go=False, reason='manual'):
    R = sync(quiet=True)
    e = next(x for x in R['voices'] if x['slug'] == slug and x['char'] == char)
    if e['voice_id'] in PROTECTED: sys.exit('protected voice')
    if go: _delete(e, R, reason)
    else: print('would delete', slug, char, e['voice_id'])
    save_reg(R)


def restore(slug, char):
    """Instant Voice Cloning from the character's recorded lines -> new voice_id (written to series voices.json + registry)"""
    R = load()
    e = next(x for x in R['voices'] if x['slug'] == slug and x['char'] == char)
    files = [P.ROOT / f for f in e.get('samples', [])][:8]
    if not files: sys.exit('no samples recorded')
    b = uuid.uuid4().hex
    parts = []
    def field(k, v): parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    field('name', f'{slug} — {e.get("name", char)} (restored)')
    field('description', ((e.get('account') or {}).get('description') or (e.get('design') or {}).get('description') or '')[:900])
    for f in files:
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="files"; filename="{f.name}"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()
                     + f.read_bytes() + b'\r\n')
    parts.append(f'--{b}--\r\n'.encode())
    try:
        r = _req('POST', f'{API}/v1/voices/add', raw=(b''.join(parts), f'multipart/form-data; boundary={b}'))
    except RuntimeError as err:
        if 'voice_limit' not in str(err): raise
        free(1, keep=(slug,), go=True, reason=f'make room to restore {slug}/{char}')
        r = _req('POST', f'{API}/v1/voices/add', raw=(b''.join(parts), f'multipart/form-data; boundary={b}'))
    vj = P.series(slug) / 'voices.json'
    V = json.load(open(vj))
    old = e['voice_id']
    V['characters'][char]['voice_id'] = r['voice_id']
    V['characters'][char].setdefault('previous_voice_ids', []).append(old)
    json.dump(V, open(vj, 'w'), ensure_ascii=False, indent=2)
    e.setdefault('history', []).append({'voice_id': old, 'until': time.strftime('%Y-%m-%d'), 'note': 'deleted, restored as IVC clone'})
    e['voice_id'] = r['voice_id']; e['status'] = 'active'; e.pop('deleted_on', None)
    save_reg(R)
    print('restored', slug, char, '->', r['voice_id'])


def show(slug=None):
    R = load()
    for e in R['voices']:
        if slug and e['slug'] != slug: continue
        print(f"{e['slug']:20s} {e['char']:10s} {e['voice_id']}  {e['status']:9s} {e.get('lines', 0):3d} lines  {e.get('name', '')}")


if __name__ == '__main__':
    a = sys.argv[1:]
    keep = tuple(a[a.index('--keep') + 1].split(',')) if '--keep' in a else ()
    go = '--go' in a
    if a[0] == 'sync': sync()
    elif a[0] == 'show': show(a[1] if len(a) > 1 else None)
    elif a[0] == 'free': free(int(a[1]), keep, go)
    elif a[0] == 'delete': delete(a[1], a[2], go)
    elif a[0] == 'restore': restore(a[1], a[2])
