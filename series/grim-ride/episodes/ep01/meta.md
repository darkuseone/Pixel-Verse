# S01E01 «Class 3» — паспорт серии

- Длина 36,8 с, 1080×1920, 30 fps, H.264 CRF 20 + AAC 192k, 20,2 МБ. Обложка `cover.png` вшита в первые 0,1 с.
- Громкость: mean −20,8 dB, max −0,5 dB.
- Голоса: eleven_v4, 15 реплик голосами героев (Voice Design, сохранены 06.10.2026 после освобождения слотов), ≈ 90 кредитов. Первая версия пилота (34,5 с) была на стандартных голосах ElevenLabs — заменена.
- Voice Design превью 5 героев + музыкальный луп ≈ 1 120 кредитов (один раз на сериал). Всего за пилот ≈ 1 270 кредитов ElevenLabs и $0,18 xAI.
- SFX: новые `raven_caw`, `etrike_rev`, `etrike_zoom`, `raisin_bonk` (≈ 55 кредитов, все прошли `sfxcheck`: ok); остальное из `library/sfx/` (гром, пинг, писк батареи, тромбон, скретч, ах толпы, скрип качалки, луп сверчков, вой моноколеса как мотор байка).
- Музыка: `music/grim_theme_15s.mp3` (surf-rock + терменвокс, луп 15 с) — на весь сезон.
- Задники xAI: `bg/street.png`, `bg/todd_yard.png`, `bg/porch.png` ($0,18).
- Код: `ep01.py` (20 планов), `timeline.py`, `mix.py`, `cover.py`.
- Пересборка: `python3 ep01.py all 4 && python3 mix.py ../../../../build/grim-ride-ep01/noaudio.mp4 final.mp4`.
