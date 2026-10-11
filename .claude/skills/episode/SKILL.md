---
name: episode
description: Производство одной серии PIXEL VERSE по конвейеру (голоса, звук, задники, антураж, обложка, рендер по планам, машинный критик, плашка подписки, сдача). Использовать для «делай пилот», «делай серию N», «делай остальные серии».
---
# /episode <slug> <N|rest> — серия от реплик до отправки

Правила — CLAUDE.md §5–§8, `docs/pipeline.md` (Визуал v2, Экономия). Сначала `series/<slug>/STATUS.md`. Для `rest` — серии подряд без новых согласований, после каждой коммит + отправка.

1. **Реплики** `episodes/epNN/lines.json` из сценария: теги эмоций, US — КАПС ударения, РУ — U+0301 во всех словах. Голоса только из `voices.json`. `engine/tts.py` (eleven_v4), `engine/tighten.py`. STT не запускать.
2. **Звук:** сначала `library/sfx/` и `series/<slug>/sfx/`; новые — `engine/sfxbatch.py` → `engine/sfxcheck.py` → в библиотеку. Музыка — лупы сериала.
3. **Задники** (если новые): `engine/xai.py`, без людей/текста/«heat haze»; проверить с сеткой координат; артефакты — xAI edit по тому же задникy.
4. **Антураж:** 5–10 местных надписей/наклеек/реквизита + анимированная мелочь на локацию в `<kit>decor.py` (`decals.plate/text_box/sticker`, `anim`). Банк надписей дописать в `docs/humor-<рынок>.md`.
5. **Код серии** `epNN.py` + `timeline.py` (DUR, CUTS, TWIST, SFX, BEDS) на `engine/episode.py`; `Episode(..., endcard=dict(style=<стиль сериала>, lang=<ru|us>))` — плашка подписки в последнюю секунду.
6. **Обложка** `cover.py` (сетка профиля: табличка сверху 3:4, заголовок под ней, лица ниже, ничего важного ниже y 1520) → `cover.png` + `cover_grid.png`. До рендера.
7. **Контроль до рендера (0 токенов):** `python3 engine/critic.py series/<slug>/episodes/epNN` → `autocheck.md` + мини-листы. Смотреть только мини-листы и кроп подозрительного. Править код, повторить по нужным `--times`.
8. **Рендер:** `python3 epNN.py all` (по планам, в фоне; ждать соседний рендер только `pgrep -f "^python3 epMM"`) → `python3 mix.py <noaudio> final.mp4`.
9. **Финал:** мини-лист кадров из `final.mp4`, длина/громкость (autocheck AUDIO). Нашёл огрех → `python3 epNN.py shots <i|name>` → mix. Отчёт в `critic.md`.
10. **Сдача:** `meta.md`, `script.md` (доля поворота), коммит + пуш; `SendUserFile` final.mp4 + cover.png + 2–3 строки (кредиты, переиспользовано, что подрезал). Обновить `STATUS.md`, после сезона — `docs/series-list.md` и `/publish`.
