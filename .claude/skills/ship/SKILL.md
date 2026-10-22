---
name: ship
description: Сдача в main — коммит, пуш в рабочую ветку, PR, squash-мердж, с правильной обработкой ветки, где осталась уже смёрженная история. Использовать после каждой готовой серии, фильма, статистики или правил.
---
# /ship "<сообщение коммита>"

1. **Что коммитить:** `git status --short`. В git идут:
   - код;
   - `final.mp4` (≤ 95 МБ);
   - обложки;
   - mp3 реплик, звуков, музыки;
   - документы.

   Не идут:
   - `build/`;
   - H.264-мастера > 95 МБ;
   - сырые выгрузки владельца с личными данными (xlsx/csv с почтой).
2. **Коммит:** `git add -A <пути>` (не весь репозиторий вслепую) → `git commit -qm` с подписью из системного промпта. В сообщении и PR не упоминать модель.
3. **Пуш:** `git push -u origin <ветка>`.
   - Отказ (non-fast-forward) — сначала `git fetch origin <ветка> main` и `git log origin/<ветка> ^origin/main`.
   - Если на сервере только уже смёрженные коммиты (их изменения есть в main squash-коммитом) — `git push --force-with-lease`.
   - Иначе — `git merge origin/<ветка>`.
   - Сетевые сбои — до 4 повторов (2, 4, 8, 16 с).
4. **Свежая работа после мерджа:** `git fetch -q origin main && git checkout -q -B <ветка> origin/main` перед началом. Новые коммиты не складывать поверх смёрженной истории.
5. **PR и мердж** (GitHub MCP, загрузить через ToolSearch `select:mcp__github__create_pull_request,mcp__github__merge_pull_request`):
   - create_pull_request owner `darkuseone`, repo `pixel-verse`, base `main`, тело с подписью;
   - merge_pull_request `squash` — владелец просит сразу в main.
6. **Владельцу:** результат одной-двумя строками. Серии — файлами (`SendUserFile`), фильм — ссылкой `https://github.com/darkuseone/Pixel-Verse/raw/main/<путь>`.
