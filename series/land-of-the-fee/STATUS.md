# Land of the Fee — STATUS (передача между сессиями)

Обновлено: 29.10.2026.

## Готово
- Разведка US (docs/humor-us.md, 29.10.2026), сценарий сезона `season1_script.txt` — отправлен владельцу, ждёт «ок».
- Пилот E01 «REPRESENTATIVE!» (31,0 с, поворот 17,70 с / 57 %) — `episodes/ep01/`.
- Риг feepix/feecast/feekit/feedecor, голоса duke/sal/feebee/doris, 23 SFX, музыка кодом, задники apartment/mall/store.

## Дальше
1. Ждать «ок»/правки владельца по сценарию и пилоту. После «ок» — E02–E06 подряд (`/episode land-of-the-fee rest`).
2. Новые задники: E02 офис Liberty Lofts + крыша, E03 ER + стеклянная башня, E04 хайвей + машина, E05 стадион, E06 аэропорт + пляж.
3. Эпизодные голоса: Madison (E02), Chuck (E03), офицер (E04), Rex (E05) — слоты ElevenLabs 30/30, освобождать по реестру (спросить владельца).

## Известные проблемы
- Музыка синтезирована кодом — я её не слышу; не зайдёт → луп ElevenLabs.
- Голоса выбраны по метрикам без прослушки.

## Команды
`cd episodes/ep01 && python3 cover.py && python3 ep01.py all && python3 mix.py ../../../../build/land-of-the-fee-ep01/noaudio.mp4 final.mp4`;
критик `python3 engine/critic.py series/land-of-the-fee/episodes/ep01 [--times ...]`.
