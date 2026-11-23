# MOTION DETECTED — STATUS (23.11.2026)
- **Сделано:** сценарий S01 (`season1_script.txt`, отправлен владельцу), герои `mdcast` (manner kspix), кит `mdkit`, антураж `mddecor`, задники porch/hall + карты глубины, голоса glenn/doris/trent (Voice Library), пилот E01 «I WAS HOME!» `episodes/ep01/`, файл выкладки `publish_s01.txt` (все 6 серий, E02–E06 — уточнить после серий).
- **Выкладка:** E01 пн 23.11 23:55 (владелец), дальше по серии в день до сб 28.11.
- **Дальше:** E02 «ONE BULB OUT?!» (нужен задник крыши/фасада ночью с гирляндой), E03 (офисная кухня), E04 (почта + дом мамы ночью), E05 (гостиная), E06 (крыльцо утром).
- **Команды:** `cd episodes/ep01 && python3 ep01.py test 1 5 20 | all | shots 0 7`; `python3 mix.py ../../../../build/motion-detected-ep01/noaudio.mp4 final.mp4`; `python3 cover.py`; `python3 engine/critic.py series/motion-detected/episodes/ep01`.
- **Важно про масштаб:** в K.A/K.at масштаб — ЭКРАННЫЕ px на px спрайта = ws_at(wy) × 3 × Z (как в kskit).
