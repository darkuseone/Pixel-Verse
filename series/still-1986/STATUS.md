# STILL 1986 — STATUS (передача между сессиями)

Обновлено: 13.11.2026 (сезон 1 + расширенная версия готовы).

## Готово
- Сценарий сезона `season1_script.txt` (отправлен владельцу 12.11, ждёт «ок»), дизайн `design/`, лор и герои — `README.md`.
- Сезон 1 «DROP WEEK» готов: E01–E06 в `episodes/epNN/` (34–45 с, повороты 57–60 %), файл выкладки `publish_s01.txt` (пн 16.11 – сб 21.11, E04 в день релиза 19.11).
- Общие помощники серий E02+: `episodes/common.py` (тайминг по длительностям дублей, лица, крупные планы, Clip), правило звука 12.11: голоса громче, музыка 0,14.
- Риг: `engine/props/v86pix.py`, `v86cast.py`, `v86kit.py`, `v86decor.py`; атмосфера `engine/atmos.py` (общая для всех сериалов); стиль плашки подписки `v86` в `engine/endcard.py`.
- Голоса `voices.json`: vince, rey (Voice Library), fran (Voice Design). Звуки `sfx/`, музыка `music/synth_theme_phone.mp3`.

## Дальше
1. Статистика сезона от владельца → `docs/stats-us.md`.
2. Расширенная 16:9 готова: `movie/` (movie.py, timeline.py, mix.py, cover.py), файл выкладки `publish_movie.txt` (вс 22.11, YouTube).
3. Сезон 2 «SUMMER '87» (крючок в финале E06).

## Известные ограничения
- Задники xAI с «плавающей» перспективой (счётчик и гидрант на переднем плане крупнее реальных) — герои масштабированы по двери отеля (`WSV = 1.34`), передний план задника в кадр с героями не беру.
- Рендер ≈ 1,2 с/кадр (глубина, свечение, частицы) — серия ≈ 8–10 мин в 4 процесса.

## Команды
`cd series/still-1986/episodes/epNN && python3 cover.py && python3 epNN.py all && python3 mix.py ../../../../build/still-1986-epNN/noaudio.mp4 final.mp4`; критик `python3 engine/critic.py series/still-1986/episodes/epNN`.
