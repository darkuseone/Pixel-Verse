"""YouTube Studio exports (RU interface, 3 CSV types) -> per-video / per-series tables, 0 tokens of reading the raw files.
  python3 -I engine/ytstudio.py <by_video.csv> [daily_by_video.csv] [daily_total.csv]
Files are recognised by header, order does not matter:
  by_video        — «Контент, Название видео, Время публикации…, Просмотры, Продолжили смотреть (%) …» (one row per video);
  daily_by_video  — «Дата, Контент, Название видео, …, Заинтересованные просмотры» (top videos by day);
  daily_total     — «Дата, Заинтересованные просмотры» (whole channel by day).
Notes (checked 08.11.2026):
  * «Средняя продолжительность просмотра» and «Средний процент просмотра» are counted over ENGAGED views only;
    real watch time per any view = «Время просмотра (часы)» * 3600 / «Просмотры» (≈ half of the shown value).
  * «Новые / Постоянные / Случайные зрители»: «Постоянные» is printed twice in the header; the 2nd one is regular (7+ days a month).
  * dates in daily files are in the channel's time zone (Pacific): a video posted 06:55 Chisinau lands on the PREVIOUS day's row.
Series are detected by keywords in the title (SERIES below; add new series there)."""
import csv, sys, re, datetime, collections

SERIES = [('valera-s2', ('валера и кот 2×',)), ('teshcha', ('тёща',)), ('prokhor', ('прохор',)), ('koschei', ('кощей',)),
          ('mazutych', ('мазутыч', '| серия')),
          ('valera-s1', ('бабушек', 'жэк', 'горяч', 'ценнике', 'прапорщик', '31 декабря', 'валера'))]
MONTHS = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}


def series(title):
    t = title.lower()
    for name, keys in SERIES:
        if any(k in t for k in keys): return name
    return 'other'


def num(x):
    try: return float(str(x).replace(',', '.').replace('%', '').strip())
    except ValueError: return None


def pubdate(s):
    m = re.match(r'(\w{3}) (\d+), (\d{4})', s.strip())
    return datetime.date(int(m.group(3)), MONTHS[m.group(1)], int(m.group(2))) if m else None


def load(path):
    rows = list(csv.reader(open(path, encoding='utf-8-sig')))
    return rows[0], [r for r in rows[1:] if r and any(r)]


def kind(h):
    if 'Название видео' in h and 'Просмотры' in h: return 'by_video'
    if 'Название видео' in h: return 'daily_by_video'
    return 'daily_total'


def by_video(h, rows):
    ix = {}
    for i, n in enumerate(h): ix.setdefault(n, i)                      # first occurrence of a duplicated header
    col = lambda r, n: num(r[ix[n]]) if n in ix and ix[n] < len(r) else None
    out = []
    for r in rows:
        if r[ix['Контент']].strip().startswith('Итог'): continue       # total row («Итоговое значение»)
        v = col(r, 'Просмотры')
        if not v: continue
        d = dict(id=r[ix['Контент']].strip(), title=r[ix['Название видео']].strip(), pub=pubdate(r[ix['Время публикации видео']]),
                 dur=col(r, 'Продолжительность'), views=v, eng=col(r, 'Заинтересованные просмотры'), stay=col(r, 'Продолжили смотреть (%)'),
                 avgpct=col(r, 'Средний процент просмотра (%)'), uniq=col(r, 'Уникальные зрители'), reach=col(r, 'Уникальный охват'),
                 new=col(r, 'Новые зрители'), ret=col(r, 'Постоянные зрители'), subs=col(r, 'Новые подписчики'), unsubs=col(r, 'Отказались от подписки'),
                 likes=col(r, 'Отметки "Нравится"'), comm=col(r, 'Новые комментарии'), shares=col(r, 'Поделились'),
                 hours=col(r, 'Время просмотра (часы)'), imp=col(r, 'Показы значков видео'), ctr=col(r, 'CTR для значков видео (%)'))
        d['series'] = series(d['title'])
        if d['new'] is not None and d['uniq'] and (d['new'] + (d['ret'] or 0)) < 0.8 * d['uniq']: d['new'] = d['ret'] = None   # fresh video, split not ready
        out.append(d)
    return out


def pr(x, w, f='{:.0f}'):
    return (f.format(x) if x is not None else '—').rjust(w)


def main(paths):
    vids, daily_v, daily_t, total = [], {}, {}, None
    for p in paths:
        h, rows = load(p)
        k = kind(h)
        if k == 'by_video':
            vids = by_video(h, rows)
            ix = {}
            for i, n in enumerate(h): ix.setdefault(n, i)
            tr = [r for r in rows if r[ix['Контент']].strip().startswith('Итог')]
            total = {n: num(tr[0][i]) for n, i in ix.items()} if tr else None
        elif k == 'daily_by_video':
            for r in rows: daily_v.setdefault(r[1].strip(), {})[r[0]] = num(r[-1]) or 0
        else:
            for r in rows: daily_t[r[0]] = num(r[1]) or 0
    if vids:
        print(f"{'id':6s} {'сер':9s} {'ролик':30s} {'вып':5s} {'с':>3s} {'просм':>6s} {'engag':>6s} {'e/v%':>5s} {'stay%':>5s} {'avg%':>5s} {'с/просм':>7s} {'подп/1k':>7s} {'лайк/1k':>7s} {'ком':>3s} {'нов%':>5s} {'вернул%':>7s}")
        for d in sorted(vids, key=lambda d: -(d['eng'] or 0)):
            if d['dur'] and d['dur'] > 90: continue                     # long films are listed separately below
            uq = d['uniq'] or 0
            print(f"{d['id'][:6]:6s} {d['series']:9s} {d['title'][:30]:30s} {d['pub'].strftime('%d.%m') if d['pub'] else '—':5s} {pr(d['dur'],3)} {pr(d['views'],6)} {pr(d['eng'],6)} "
                  f"{pr(100*d['eng']/d['views'] if d['eng'] else None,5,'{:.1f}')} {pr(d['stay'],5,'{:.1f}')} {pr(d['avgpct'],5,'{:.1f}')} {pr(3600*d['hours']/d['views'] if d['hours'] else None,7,'{:.1f}')} "
                  f"{pr(1000*d['subs']/d['views'] if d['subs'] is not None else None,7,'{:.2f}')} {pr(1000*d['likes']/d['views'] if d['likes'] is not None else None,7,'{:.1f}')} {pr(d['comm'],3)} "
                  f"{pr(100*d['new']/uq if d['new'] and uq else None,5,'{:.0f}')} {pr(100*d['ret']/uq if d['ret'] is not None and uq else None,7,'{:.0f}')}")
        print('\nпо сериям (просмотры / engaged / подп и лайки на 1 000 просмотров / взвешенный stay):')
        agg = collections.defaultdict(lambda: collections.Counter())
        for d in vids:
            if d['dur'] and d['dur'] > 90: continue
            a = agg[d['series']]
            a['n'] += 1; a['views'] += d['views']; a['eng'] += d['eng'] or 0; a['subs'] += d['subs'] or 0; a['likes'] += d['likes'] or 0
            a['comm'] += d['comm'] or 0; a['shares'] += d['shares'] or 0; a['stayw'] += (d['stay'] or 0) * d['views']
        for s, a in sorted(agg.items(), key=lambda kv: -kv[1]['eng']):
            print(f"  {s:10s} роликов {a['n']:2.0f}  просм {a['views']:7.0f}  engaged {a['eng']:7.0f}  на ролик {a['eng']/a['n']:6.0f}  подп/1k {1000*a['subs']/a['views']:.2f}  "
                  f"лайк/1k {1000*a['likes']/a['views']:.1f}  комм {a['comm']:.0f}  репост {a['shares']:.0f}  stay {a['stayw']/a['views']:.1f}")
        if total:
            print(f"\nитого канал: просм {total.get('Просмотры')}, engaged {total.get('Заинтересованные просмотры')}, stay {total.get('Продолжили смотреть (%)')}, ср.% {total.get('Средний процент просмотра (%)')}, "
                  f"уник. зрителей {total.get('Уникальные зрители')} (новые {total.get('Новые зрители')}, вернулись {total.get('Постоянные зрители')}), подписчики +{total.get('Новые подписчики')} −{total.get('Отказались от подписки')}")
            if total.get('Просмотры') and total.get('Время просмотра (часы)'):
                print(f"реальное время на любой просмотр: {3600*total['Время просмотра (часы)']/total['Просмотры']:.1f} с (показанное «среднее» считается только по engaged)")
        for d in vids:
            if d['dur'] and d['dur'] > 90: print(f"длинное: {d['title'][:50]} — {d['views']:.0f} просм, показы {d['imp']}, CTR {d['ctr']}")
    if daily_v:
        print('\nкривая по дням (engaged; день 0 = дата публикации в часовом поясе канала):')
        for vid, days in daily_v.items():
            v = next((x for x in vids if x['id'] == vid), None)
            ks = sorted(days)
            first = next((i for i, k in enumerate(ks) if days[k] > 0), 0)
            seq = [int(days[k]) for k in ks[max(first - 1, 0):]][:10]
            print(f"  {vid[:6]} {(v['title'][:28] if v else ''):28s} {seq}")
    if daily_t:
        ks = sorted(daily_t)
        print('\nканал по дням (engaged):', ', '.join(f"{k[5:]}:{int(daily_t[k])}" for k in ks))
        if daily_v:
            rest = {k: daily_t[k] - sum(days.get(k, 0) for days in daily_v.values()) for k in ks}
            print('без топ-роликов из daily_by_video:', ', '.join(f"{k[5:]}:{int(rest[k])}" for k in ks))


if __name__ == '__main__':
    main(sys.argv[1:])
