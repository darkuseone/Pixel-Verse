# Florida Man: Allegedly — STATUS (передача между сессиями)

Обновлено: 12.10.2026. Всё в `main` (PR #13 смержен).

## Готово
- Визуал v2 (10.10): герои ×2 (`dibspix.res_for`), `txt_box`, декали-антураж `engine/props/fmdecor.py` (11 локаций), обложки по сетке (`covergen_fm`), критик.
- Экономия (11.10): `engine/autocheck.py`, `engine/critic.py` (мини-листы), рендер по планам `epNN.py all|shots …`.
- E01–E06 v2 — отрендерены по планам, проверены (autocheck + мини-листы финала), отправлены владельцу 11.10.

- Плашка «SUBSCRIBE! (ALLEGEDLY)» (12.10) вшита в последние 1 с E01–E06 (`engine/endcard.py apply`); чистые мастера — `build/florida-man-epNN/final_noend.mp4` (не в git).
- `publish_s01.txt` отправлен владельцу.
- Расширенная версия «FLORIDA MAN ON TRIAL» (12.10): `movie/final.mp4` 5:00, 16:9, поворот 2:32 (51 %), плашка подписки за 3 с до конца, обложка `movie/cover.jpg`, выкладка `movie/publish_movie.txt` (вс 25.10, 16:00 Молдова). Пересборка: `cd series/florida-man/movie && PV_WIDE=1 python3 movie.py all && python3 mix.py`.

## Дальше
- Ждём статистику S01 → `docs/stats-us.md`, выводы в сезон 2 («SEASON 2: …» крючок из E06).

## Известные компромиссы
- E02 POV-кадр «$14.99» (16.98 с) режет меню намеренно — CUT_SIGN принят.
- Фоновые таблички (GATOR XING, NO TRESPASSING) на средних планах могут резаться краем — NIT по правилу размера.
