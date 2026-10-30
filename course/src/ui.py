"""Schematic screen mockups for the course (simplified; real interfaces may differ slightly). {{ui:name}} in the .md sources."""

P = lambda n: f'<span class="pin">{n}</span>'

UI = {}

UI['github_new'] = f'''<div class="ui"><div class="frame"><div class="bar"><i></i><i></i><i></i><span class="url">github.com/new</span></div>
<div class="screen"><div class="t">Create a new repository</div>
<div class="lbl">Owner / Repository name *</div><div class="row"><div class="inp" style="flex:0 0 22mm">твой-ник</div>/<div class="inp" style="flex:1">my-cartoons</div>{P(1)}</div>
<div class="lbl">Description (optional)</div><div class="inp ph">Мои пиксельные мультики</div>
<div class="row" style="margin-top:2.6mm"><span class="radio">Public</span><span class="radio on">Private</span>{P(2)}</div>
<div class="row"><span class="check on">Add README</span>{P(3)}</div>
<div class="row" style="justify-content:flex-end;margin-top:2.6mm"><span class="b">Create repository</span>{P(4)}</div></div></div>
<div class="caption">Схема экрана. Интерфейс GitHub иногда меняется, но поля называются так же.</div></div>'''

UI['github_upload'] = f'''<div class="ui"><div class="two">
<div class="frame"><div class="bar"><i></i><i></i><i></i><span class="url">github.com/твой-ник/my-cartoons</span></div>
<div class="screen"><div class="row" style="justify-content:space-between"><b>my-cartoons</b><span class="b ghost">Add file ▾</span>{P(1)}</div>
<div style="text-align:right"><div class="menu"><div>Create new file</div><div class="hi">Upload files {P(2)}</div></div></div>
<div class="list" style="margin-top:2mm"><div><span>README.md</span><span>Initial commit</span></div></div></div></div>
<div class="frame"><div class="bar"><i></i><i></i><i></i><span class="url">…/upload/main</span></div>
<div class="screen"><div class="inp ph" style="height:18mm;display:grid;place-items:center;text-align:center;border-style:dashed">Перетащи файл сюда<br>или <u>choose your files</u> {P(3)}</div>
<div class="file" style="margin-top:2mm">starter-kit.zip</div>
<div class="row" style="justify-content:flex-end"><span class="b">Commit changes</span>{P(4)}</div></div></div>
</div><div class="caption">Слева — меню «Add file», справа — страница загрузки. На телефоне открой github.com в браузере: всё то же самое.</div></div>'''

UI['el_key'] = f'''<div class="ui"><div class="frame"><div class="bar"><i></i><i></i><i></i><span class="url">elevenlabs.io/app/developers/api-keys</span></div>
<div class="screen"><div class="two" style="grid-template-columns:30mm 1fr">
<div class="list" style="font-size:7pt"><div><span>Home</span></div><div><span>Voices</span></div><div><span><b>Developers</b> {P(1)}</span></div></div>
<div><div class="row" style="justify-content:space-between"><b>API Keys</b><span class="b dark">+ Create Key</span>{P(2)}</div>
<div class="lbl">Name</div><div class="inp">claude-cartoons</div>
<div class="lbl">Ключ (показывается один раз)</div><div class="row"><div class="inp" style="flex:1">sk_••••••••••••••••••••</div><span class="b ghost">Copy</span>{P(3)}</div></div></div></div></div>
<div class="caption">Схема экрана. Если меню выглядит иначе, ищи раздел «API Keys»: он бывает в меню профиля или в разделе Developers.</div></div>'''

UI['claude_start'] = f'''<div class="ui"><div class="frame"><div class="bar"><i></i><i></i><i></i><span class="url">claude.ai/code</span></div>
<div class="screen"><div class="t" style="text-align:center;margin:2mm 0 3mm">Что делаем?</div>
<div class="inp ph" style="min-height:12mm">/start</div>
<div class="row"><span class="b ghost">☁ Default ▾</span>{P(1)}<span class="b ghost">⎇ my-cartoons ▾</span>{P(2)}<span class="b ghost">Auto ▾</span>{P(3)}<span class="b ghost">Opus ▾</span>{P(4)}</div></div></div>
<div class="caption">Под полем ввода: {P(1)} облачная среда, {P(2)} репозиторий, {P(3)} режим работы, {P(4)} модель. В приложении Claude это вкладка Code — там те же кнопки.</div></div>'''

UI['env_dialog'] = f'''<div class="ui"><div class="frame"><div class="bar"><i></i><i></i><i></i><span class="url">claude.ai/code · Edit cloud environment</span></div>
<div class="screen"><div class="t">Edit cloud environment</div>
<div class="list">
<div><span>Name</span><span>Default</span></div>
<div><span>Network access</span><span>Trusted ›</span></div>
<div><span><b>Network secrets</b> {P(2)}</span><span>0 ›</span></div>
<div><span><b>Setup script</b> {P(1)}</span><span>›</span></div>
<div><span>Environment variables</span><span>›</span></div></div>
<div class="row" style="justify-content:flex-end;margin-top:2.6mm"><span class="b dark">Save changes</span>{P(3)}</div></div></div>
<div class="caption">Окно настроек среды: открывается шестерёнкой у строки «Default» в меню среды.</div></div>'''

UI['setup_script'] = f'''<div class="ui"><div class="frame"><div class="bar"><i></i><i></i><i></i><span class="url">Setup script</span></div>
<div class="screen"><div class="inp" style="font-size:6.6pt;line-height:1.5;white-space:pre-wrap">#!/bin/bash
apt-get update -qq &amp;&amp; apt-get install -y -qq ffmpeg &gt; /dev/null
python3 -m pip install -q numpy pillow || python3 -m pip install -q --break-system-packages numpy pillow</div>
<div class="row" style="justify-content:flex-end;margin-top:2mm"><span class="b dark">Save changes</span></div></div></div></div>'''

UI['secret_form'] = f'''<div class="ui"><div class="frame"><div class="bar"><i></i><i></i><i></i><span class="url">Network secrets · Add secret</span></div>
<div class="screen"><div class="lbl">Secret type</div><div class="inp">Bearer</div>
<div class="lbl">Name {P(1)}</div><div class="inp">ElevenLabs</div>
<div class="lbl">Allowed websites {P(2)}</div><div class="inp">api.elevenlabs.io</div>
<div class="lbl">Custom headers {P(3)}</div>
<div class="row" style="flex-wrap:nowrap"><div class="inp" style="flex:1.2">xi-api-key</div><div class="inp ph" style="flex:.8">(пусто)</div><div class="inp" style="flex:1.4">sk_••••••••</div></div>
<div class="row" style="font-size:6.4pt;color:var(--muted);margin-top:-.6mm"><span style="flex:1.2">Name</span><span style="flex:.8">Prefix</span><span style="flex:1.4">Value</span></div>
<div class="row" style="justify-content:flex-end;margin-top:2mm"><span class="b dark">Add</span>{P(4)}</div></div></div></div>'''

UI['chat_phone'] = f'''<div class="ui"><div class="phone"><div class="notch"></div>
<div class="bubble me">/episode valera 1</div>
<div class="bubble ai">Пилот готов: 31,4 с, поворот на 55 %, громкость −14 LUFS. Потрачено 160 кредитов ElevenLabs.</div>
<div class="file"><img src="img/v02_0.6.jpg" alt="">final.mp4 · 18 МБ</div>
<div class="file"><img src="img/cov_v1_2.jpg" alt="">cover.png</div>
<div class="bubble me">Ок! Делай остальные серии</div></div>
<div class="caption" style="text-align:center">Так выглядит работа с телефона: команда → готовое видео прямо в чате.</div></div>'''

UI['usage'] = f'''<div class="ui"><div class="frame"><div class="bar"><i></i><i></i><i></i><span class="url">claude.ai/settings/usage</span></div>
<div class="screen"><div class="t">Usage</div>
<div class="lbl">Текущая сессия (5-часовое окно)</div><div style="height:3mm;background:var(--fog);border-radius:1.5mm"><div style="width:72%;height:100%;background:var(--fire);border-radius:1.5mm"></div></div>
<div class="row small" style="justify-content:space-between"><span>72 % использовано</span><span>сброс через 1 ч 40 мин</span></div>
<div class="lbl">Неделя</div><div style="height:3mm;background:var(--fog);border-radius:1.5mm"><div style="width:31%;height:100%;background:var(--sky);border-radius:1.5mm"></div></div>
<div class="row small" style="justify-content:space-between"><span>31 % использовано</span><span>сброс в понедельник</span></div></div></div>
<div class="caption">Схема страницы лимитов. Цифры для примера.</div></div>'''
