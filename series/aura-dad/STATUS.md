# Aura Dad — STATUS (03.11.2026)
- **Сделано:** сценарий S01 `season1_script.txt` (отправлен владельцу), голоса doug/kayden/tammy/mirra из Voice Library (без слотов),
  задники `bg/kitchen.png`, `bg/bathroom.png`, звуки `sfx/` (8 шт.), риг `engine/props/auracast.py`, кит `engine/props/aurakit.py`,
  пилот E01 «MINUS 400?!» `episodes/ep01/` (35,9 с, поворот 60 %).
- **Дальше:** ждать «ок»/правки владельца по сценарию и пилоту → E02 «$340 SKINCARE?!» (нужны: Lily, продавщица Skylar, задник
  магазина SEPHORIA, голоса из Voice Library).
- **Известное:** поворот на 60 % (верхняя граница) и после 18-й секунды — цена «понятной истории» с целыми фразами.
- **Команды:** `cd series/aura-dad/episodes/ep01 && python3 ep01.py test 1 5 | all | shots <i>`; `python3 mix.py <noaudio> final.mp4`;
  `python3 cover.py`; `python3 engine/critic.py series/aura-dad/episodes/ep01`.
