# S01E02 «Verify You're Human» — паспорт серии

- 32,4 с, 1080×1920, 30 fps, H.264 CRF 20 + AAC 192k. Обложка вшита в первые 0,1 с. mean −21,4 dB, max −0,3 dB.
- Голоса: eleven_v4, 15 реплик ≈ 92 кредита; новый голос DASHLEY (бот поддержки, Voice Design ≈ 230 кредитов, один раз).
- SFX: новые `flatline_beep`, `phone_ring_pocket` (≈ 33 кредита); из библиотеки — пинг, тап, сканер, гром, писк батареи, тромбон, скретч, трубка, музыка ожидания `hold_music_elise` (классика, общественное достояние).
- Задники: переиспользован `todd_yard` (табличка «4 DAYS»), без новых трат xAI.
- Экраны приложения (капча из спрайтов героев, чат, ожидание, входящий звонок) — `engine/props/grimkit.py` (`phone_app`, `captcha`).
- Пересборка: `python3 ep02.py all 4 && python3 mix.py ../../../../build/grim-ride-ep02/noaudio.mp4 final.mp4`.
