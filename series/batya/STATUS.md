# Батя сам — STATUS (08.11.2026)
- **Заказ владельца (08.11):** новый РУ-сериал по новым правилам (formula §11), сценарий + пилот сразу, больше антуража, понятные герои, качество не падает от серии к серии.
- **Готово:** ресёрч (`docs/humor-ru.md` 08.11), дизайн-философия и модельный лист (`design/philosophy.md`, `design/cast_sheet.png`), риг `engine/props/batyacast.py` (batya, tema, ira + градусник, колокольчик, поднос, половник, ложка, коробки таблеток), сценарий сезона `season1_script.txt` v1.
- **Дальше:** пилот E01 «37,2 — ПОМИРАЮ!» (`episodes/ep01/`): голоса (Voice Library), задники xAI (`bedroom`, `kitchen`), антураж, обложка («вязаный» заголовок + табличка-рулетка), рендер, критик.
- **Выкладка (рекомендация):** пн 23.11 – сб 28.11 (E05 в Чёрную пятницу 27.11, E06 в канун Дня матери 29.11).
- **08.11.2026 — пилот E01 «37,2 — ПОМИРАЮ!»** (`episodes/ep01/`): 33,7 с, поворот 17,5 с (52 %, «спаситель оказался жертвой»). Голоса Voice Library (без слотов): Батя — «Ivan — Russian Storyteller», Тёма — «Motya Sugar — Chill», Ира — «Serafima Voloshina» (`voices.json`). Задники xAI `bg/bedroom.png`, `bg/kitchen.png`. Свои SFX `sfx/` (колокольчик, писк градусника, чих, кипящая кастрюля), подложки CC0 (mandolin → Fetch Contest). Кит `engine/props/batyakit.py` (заголовок «вязаный», табличка-рулетка, рамка стрима Тёмы), плашка подписки `style='batya'`.
- **Команды:** `cd series/batya/episodes/ep01 && python3 ep01.py test … | frames … | all | shots <i|name>`; `python3 mix.py <noaudio> final.mp4`; `python3 cover.py`; `python3 engine/critic.py series/batya/episodes/ep01`.
- **Дальше:** «ок» владельца по пилоту → E02 «−20 — НЕ ЗАВОДИТСЯ?!» (нужны задники: двор в снегу, подъезд; аккумулятор, табло «−20»).

