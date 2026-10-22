"""Owner's analytics CSV (TikTok + YouTube) -> per-video and per-series rates per 1 000 views (0 tokens of reading the raw table).
  python3 -I engine/statscsv.py <file.csv>
Series are detected by keywords in the title (SERIES below; add new series there). TikTok rows in the owner's export are shifted
by one column (the «Likes» column holds subscribers, ... «CTR» holds For You %); checked 22.10.2026 — if a new export is fixed, set shifted=False."""
import csv, sys, collections

SERIES = [('valera', ('валера', 'бабуш', 'горяч', 'ценник', 'цена на полке', 'жэк', 'прапорщик', '31 декабря')),
          ('mazutych', ('мазут', 'бензин', 'моноколес', 'премию', '25 лет')),
          ('prokhor', ('прохор', 'таёж', 'таеж')),
          ('koschei', ('кощей',))]


def series(title):
    t = title.lower()
    for name, keys in SERIES:
        if any(k in t for k in keys): return name
    return 'other'


def num(x):
    try: return float(str(x).replace(',', '.').replace('%', ''))
    except ValueError: return None


def main(path):
    rows = list(csv.DictReader(open(path, encoding='utf-8-sig')))
    agg = collections.defaultdict(lambda: collections.Counter())
    seen = set()
    print(f"{'платф':7s} {'ролик':42s} {'просм':>8s} {'подп/1k':>8s} {'комм/1k':>8s} {'реп/1k':>7s} {'сохр/1k':>8s} {'досм%':>6s}")
    for r in rows:
        v = num(r.get('Views'))
        if not v or r.get('Type') == 'Long': continue
        p = r.get('Platform', '')
        shifted = p == 'TikTok'                                    # owner's TikTok export: every metric one column to the right
        if p == 'TikTok' and shifted:
            subs, likes, comm, sh, sav, compl = (num(r.get(k)) for k in ('Likes', 'Comments', 'Shares', 'Saves', 'Completion_%', 'Retention_%'))
        else:
            subs, likes, comm, sh, sav, compl = (num(r.get(k)) for k in ('Subscribers_Gained', 'Likes', 'Comments', 'Shares', 'Saves', 'Completion_%'))
        key = (p, v, likes, comm)
        if key in seen: continue                                   # duplicate rows of the same video under another title
        seen.add(key)
        s = series(r['Title'])
        f = lambda x: f'{1000 * x / v:8.2f}' if x is not None else '       —'
        print(f"{p[:7]:7s} {r['Title'][:42]:42s} {v:8.0f} {f(subs)} {f(comm)} {f(sh)[1:]} {f(sav)} {compl if compl is not None else '—':>6}")
        a = agg[(p, s)]
        if subs is not None: a['v_s'] += v; a['subs'] += subs
        if comm is not None: a['v_c'] += v; a['comm'] += comm
        if sh is not None: a['v_sh'] += v; a['sh'] += sh
        if sav is not None: a['v_sv'] += v; a['sav'] += sav
        a['views'] += v
    print('\nпо сериалам (на 1 000 просмотров, только строки, где метрика есть):')
    for (p, s), a in sorted(agg.items()):
        g = lambda n, d: f'{1000 * a[n] / a[d]:.2f}' if a[d] else '—'
        print(f"  {p:8s} {s:10s} просм {a['views']:9.0f}  подп {g('subs', 'v_s')}  комм {g('comm', 'v_c')}  репост {g('sh', 'v_sh')}  сохр {g('sav', 'v_sv')}")


if __name__ == '__main__':
    main(sys.argv[1])
