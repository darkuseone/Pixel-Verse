# Thanks, Randy — STATUS (передача между сессиями)

Обновлено: 21.10.2026.

## Готово
- Сезон 1 «Still Frozen»: E01–E06 в `episodes/epNN/` (`final.mp4`, `cover.png`, `script.md`, `meta.md`, `critic.md`, код).
- Файл выкладки `publish_s01.txt` (23–27.11.2026).
- Риг `engine/props/randypix.py` / `randycast.py` / `randykit.py` / `randydecor.py`; голоса `voices.json` (9 героев); звуки `sfx/`, музыка `music/`.

## Дальше
1. Расширенная версия 16:9 — только по согласию владельца (слот вс 29.11, Нью-Йорк 10:00 = Молдова 17:00).
2. Сезон 2 «Randy Hosts Christmas» (крючок в финале E06) — выкладка в неделю перед Рождеством.

## Команды
`cd episodes/epNN && python3 cover.py && python3 epNN.py all && python3 mix.py ../../../../build/thanks-randy-epNN/noaudio.mp4 final.mp4`; критик `python3 engine/critic.py series/thanks-randy/episodes/epNN [video]`.
