# STILL 1986 — STATUS (передача между сессиями)

Обновлено: 12.11.2026.

## Готово
- Сценарий сезона `season1_script.txt` (отправлен владельцу 12.11, ждёт «ок»), дизайн `design/`, лор и герои — `README.md`.
- Пилот E01 «FREE PARKING?» — `episodes/ep01/` (45,0 с, 2.5D, поворот 57 %).
- Риг: `engine/props/v86pix.py`, `v86cast.py`, `v86kit.py`, `v86decor.py`; атмосфера `engine/atmos.py` (общая для всех сериалов); стиль плашки подписки `v86` в `engine/endcard.py`.
- Голоса `voices.json`: vince, rey (Voice Library), fran (Voice Design). Звуки `sfx/`, музыка `music/synth_theme_phone.mp3`.

## Дальше
1. После «ок» владельца — E02–E06 по сценарию (серия 4 должна выйти в четверг релиза 19.11, если сезон пойдёт пн 16.11).
2. Новые локации: касса клуба NEON PALACE (E02), марина (E03), молл в полночь (E04), Ocean Drive под ливнем (E05), студия Винса (E06) — задники xAI.
3. Новые герои: Tiffany (касса), Officer Diaz, Gary (начальник) — голоса из Voice Library.

## Известные ограничения
- Задники xAI с «плавающей» перспективой (счётчик и гидрант на переднем плане крупнее реальных) — герои масштабированы по двери отеля (`WSV = 1.34`), передний план задника в кадр с героями не беру.
- Рендер ≈ 1,2 с/кадр (глубина, свечение, частицы) — серия ≈ 8–10 мин в 4 процесса.

## Команды
`cd series/still-1986/episodes/epNN && python3 cover.py && python3 epNN.py all && python3 mix.py ../../../../build/still-1986-epNN/noaudio.mp4 final.mp4`; критик `python3 engine/critic.py series/still-1986/episodes/epNN`.
