# Thanks, Randy — STATUS (передача между сессиями)

Обновлено: 21.10.2026.

## Готово
- Разведка US 21.10.2026 → `docs/humor-us.md`.
- Сценарий S01 `season1_script.txt` отправлен владельцу; дизайн-философия `design/philosophy.md` (черновик).

- «Ок» сценарию 21.10 («Делай пилот»). Риг: `engine/props/randypix.py` (манера), `randycast.py` (randy, tom, joyce, brayden, kiosk + bag_prop, мелкий реквизит), `randykit.py` (свет, миры, заголовок, ценник-табличка, day_card, thaw_meter, screen_ui, cover_make), `randydecor.py` (store, store_b); плашка подписки `endcard` style `randy`. Модельный лист `design/cast_sheet.png`.
- Голоса (`voices.json`): randy, tom, joyce, brayden, scandee. Звуки сериала: `sfx/` (18) + `music/randy_theme_15s.mp3`.
- **E01 «$89 TURKEY?!»** 30,8 с, поворот 16,80 с (55 %) — отрендерен, критик CLEAN, отправлен владельцу 21.10.

## Дальше
1. Ждём отзыв на пилот. После «ок» — E02 «GRAVY'S A LIQUID?!» (аэропорт: задник + Пэтти), E03–E06, `publish_s01.txt` (выкладка 23–27.11.2026).
2. Голоса эпизодических: Patty (E02), Carol (E03), Dunn (E04), Kyle (E06).

## Команды
`cd episodes/ep01 && python3 cover.py && python3 ep01.py all && python3 mix.py ../../../../build/thanks-randy-ep01/noaudio.mp4 final.mp4`; критик `python3 engine/critic.py series/thanks-randy/episodes/ep01 [video]`.

## Ограничения
- Сериал сезонный: всё должно быть готово до ~15.11.2026.
