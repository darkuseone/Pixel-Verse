"""Build the course PDFs: src/<doc>/*.md (+ shortcodes) -> out/<doc>.html -> PDF via Playwright (render.js).
  python3 build.py [doc ...]      docs: course, prompts, checklists (default: all)
Shortcodes in .md:
  :::ok|fix|tip|warn|money Title      ...      :::      coloured box
  :::prompt Title                     ...      :::      copy-paste prompt (verbatim)
  :::steps                            1. ...   :::      big numbered steps
  {{ui:name}}                                           screen mockup from src/ui.py"""
import re, sys, html, subprocess, pathlib, shutil
import markdown
sys.path.insert(0, str(pathlib.Path(__file__).parent / 'src'))
from ui import UI

HERE = pathlib.Path(__file__).resolve().parent
SRC, OUT = HERE / 'src', HERE / 'out'
DOCS = {
    'course': ('01_Курс_Мультстудия_в_кармане', 'Мультстудия в кармане'),
    'prompts': ('02_Промты_шпаргалка', 'Промты и команды'),
    'checklists': ('03_Чек-листы', 'Чек-листы'),
}
BOX = {'ok', 'fix', 'tip', 'warn', 'money'}


def pre(text):
    out, lines, i = [], text.split('\n'), 0
    while i < len(lines):
        m = re.match(r'^:::(\w+)\s*(.*)$', lines[i])
        if m:
            kind, title = m.group(1), m.group(2).strip()
            j = i + 1
            while lines[j].strip() != ':::': j += 1
            body = '\n'.join(lines[i + 1:j])
            if kind == 'prompt':
                out.append(f'<div class="prompt"><div class="pl"><span>{html.escape(title)}</span><span>скопируй целиком</span></div>'
                           f'<pre>{html.escape(body.strip())}</pre></div>')
            elif kind == 'steps':
                out.append(f'<div class="stp" markdown="1">\n\n{body}\n\n</div>')
            elif kind in BOX:
                bt = f'<span class="bt">{html.escape(title)}</span>' if title else ''
                out.append(f'<div class="box {kind}" markdown="1">{bt}\n\n{body}\n\n</div>')
            else:
                raise ValueError(kind)
            i = j + 1
            continue
        out.append(lines[i]); i += 1
    t = '\n'.join(out)
    return re.sub(r'\{\{ui:(\w+)\}\}', lambda m: UI[m.group(1)], t)


def build(doc):
    name, foot = DOCS[doc]
    parts = []
    for f in sorted((SRC / doc).glob('*')):
        t = f.read_text()
        parts.append(t if f.suffix == '.html' else markdown.markdown(pre(t), extensions=['md_in_html', 'tables', 'attr_list', 'sane_lists']))
    page = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{foot}</title>
<link rel="stylesheet" href="../fonts/fonts-local.css"><link rel="stylesheet" href="../src/style.css"></head>
<body>{''.join(parts)}</body></html>'''
    OUT.mkdir(exist_ok=True)
    h = OUT / f'{doc}.html'
    h.write_text(page.replace('src="img/', 'src="../img/'))
    pdf = OUT / f'{name}.pdf'
    subprocess.run(['node', str(HERE / 'render.js'), str(h), str(pdf), f'PIXEL VERSE · {foot}'], check=True)
    print(pdf, pdf.stat().st_size // 1024, 'KB')


for d in (sys.argv[1:] or list(DOCS)): build(d)
