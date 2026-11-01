# Тёща на недельку — STATUS (01.11.2026)
- **Сделано:** сценарий S01 `season1_script.txt` (отправлен владельцу), пилот E01 «НА НЕДЕЛЬКУ?!» `episodes/ep01/` (32,7 с, поворот 51 %, −14 LUFS, критик 0 FIX). Ждём «ок»/правки владельца.
- **Дальше:** после «ок» → `/episode teshcha 2` (E02 «СДЕЛАЙ ПОТИШЕ!», телевизор на 100). Нужны: задник кухни (E03), прихожей (E04), работы «ОКНА-ЛЮКС» (E05); голос Люси (Voice Design) к E04.
- **Голоса:** tolik, raisa, pusya, sveta — Voice Design, `voices.json` (выбраны по метрикам, владелец ещё не слушал).
- **Код:** риг `engine/props/teshcast.py` (Толик, Раиса, Пуся, Света + реквизит), кит `engine/props/teshkit.py` (миры, таблички, свет, заголовок, салфетка, Show), плашка подписки `style='teshcha'`.
- **Задники:** `bg/landing.png`, `room.png`, `balcony.png` (`gen_bg.py`). Звуки `sfx/` (22), музыка `music/gen_music.py`.
- **Известное:** голоса Мазутыча, Рэнди, Гены удалены автоочисткой слотов (в архиве, `/voices` вернёт); Валера восстановлен клоном 01.11.
- **Команды:** `cd series/teshcha/episodes/ep01 && python3 ep01.py test 1 5 20 | all | shots <i>`; `python3 mix.py <noaudio> final.mp4`; `python3 cover.py`; `python3 engine/critic.py series/teshcha/episodes/ep01`.
