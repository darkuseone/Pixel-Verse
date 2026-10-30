# Land of the Fee — STATUS (передача между сессиями)

Обновлено: 30.10.2026.

## Готово
- Сезон 1 «Please Hold» — все 6 серий в `episodes/ep01…ep06/` (final.mp4, cover.png, script/meta/critic), звук каждой через earshot (launch-grade).
- Файл выкладки `publish_s01.txt`: только YouTube + Instagram (TikTok US не ведём с 30.10.2026), E01 пт 30.10 … E06 ср 04.11.
- Риг feepix/feecast/feekit/feedecor; голоса duke/sal/feebee/doris (свои) + madison/chuck/nurse/officer/rex (готовые, без слотов).
- Задники: apartment, mall, store, leasing, courtyard, roof, er, tower, billing, street, highway, shoulder, stadium, stage, gate, beach.
- Звуки: свой фоли `sfx/`, банк earshot `sfx/es/` (26), музыка `music/freedom_kazoo_v2_16s.mp3`.

## Дальше
1. Предложить владельцу расширенную 16:9 версию сезона (только по согласию).
2. Сезон 2 — крючок «SEASON 2: TAX SEASON» (налоги, апрель). Перед ним — статистика YouTube/Instagram по S01.

## Известные проблемы
- earshot везде даёт minor «mid 1–4 kHz high» — от голосов, принято как стиль.
- `sfx/coconut_wake.mp3` почти тишина (−70 дБ) — не использовать.

## Команды
earshot: `bash engine/earshot_setup.sh`, затем `/home/user/tools/earshot/.venv/bin/python engine/earshot_listen.py episodes/epNN/final.mp4 episodes/epNN/sound/cues.json ../../build/land-of-the-fee-epNN/es/vN`.
`cd episodes/epNN && python3 cover.py && python3 epNN.py all && python3 mix.py ../../../../build/land-of-the-fee-epNN/noaudio.mp4 final.mp4`;
критик `python3 engine/critic.py series/land-of-the-fee/episodes/epNN`.
